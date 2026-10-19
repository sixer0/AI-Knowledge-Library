#!/usr/bin/env python3
"""Provisioning profil gsp-imagegen-worker (DECKDEMS-0925 / OPS-01, kartu t_dd876c30).

Pola: preseden create_3d_specialist.py (idempoten, --check dry-run, guard tulis sempit).
Basis config = salinan profil gsp-vss-specialist nyata di disk, dimutasi:
  - model.default -> worker-fast (spek mapping docs/2026-09-25-imagegen21-orchestration-mapping.md S6)
  - platform_toolsets.cli += vision (vision_analyze utk cek struktur mandiri, mapping S6)
SOUL = kepala identitas peran + potongan bersama dari SOUL gsp-vss-specialist
(AWARENESS s/d GATE NATURALISASI) supaya blok gate INV-7 byte-persis.
Skill fisik: create-image-gsp, create-deck-gsp, gsp-verification-before-completion
(registry fleet; 'gsp-imagegen21-ops' tidak ada di disk - SOP riil = dua perintah gsp itu).
Marker .no-bundled-skills di ROOT profil (opt-out re-seed bundled).
Tanpa .lean-policy (pekerja, bukan controller RBAC).
"""
import argparse
import os
import shutil
import subprocess
import sys

HOME = os.path.expanduser("~")
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", os.path.join(HOME, "AppData", "Local"))
PROFILES = os.path.join(LOCALAPPDATA, "hermes", "profiles")
SRC_SKILLS = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")
WORKSPACE = "C:/Users/TRIAL/workspace/gsp-hermes/workspace"

PROFIL = "gsp-imagegen-worker"
DEST = os.path.join(PROFILES, PROFIL)
NAME = "Imagegen Worker"
EMOJI = "\U0001F3A8"
DESC = ("Pekerja render Imagegen 2.1 (recipe A4): generate/edit slide via klien kanonik ke "
        "inference-kaytus:8040 lewat tunnel ssh, cek struktur vision mandiri, record.json")
PERAN = ("Eksekutor render Imagegen 2.1: generate/edit gambar slide dari SPEC + design_master "
         "via layanan inference-kaytus, verifikasi struktur mandiri, serah PNG + record.json")

ALWAYS = ["create-image-gsp", "create-deck-gsp", "gsp-verification-before-completion"]

ENV_SOURCE = os.path.join(PROFILES, "gsp-vss-specialist", ".env")
CONFIG_REF = os.path.join(PROFILES, "gsp-vss-specialist", "config.yaml")
SOUL_REF = os.path.join(PROFILES, "gsp-vss-specialist", "SOUL.md")
GUARD = ["node", "C:/Users/TRIAL/gsp-datacenter/scripts/ensure-profile-complete.mjs", "check", PROFIL]

EMDASH = chr(0x2014)
SLICE_FROM = f"## Skill {EMDASH} AWARENESS"
REQUIRED_HEADINGS = [
    f"## GATE ENFORCEMENT {EMDASH} LANE PEKERJA/Worker (WAJIB, kebijakan 31-08-2026)",
    "## GATE NATURALISASI (WAJIB, kebijakan 02-09-2026; cakupan dipersempit 03-09-2026)",
]
CONFIG_REQUIRED_KEYS = ["provider: GSP-AI", "fallback_providers", WORKSPACE,
                        "allow_private_urls"]

ROLE_RULES = """1. Render HANYA lewat layanan Imagegen 2.1 (host `inference-kaytus`, 127.0.0.1:8040 via ssh tunnel sendiri: `ssh -N -f -L 8040:127.0.0.1:8040 inference-kaytus`; kunci & host sudah terdaftar di ~/.ssh/config). WAJIB `client.health()` dulu (ok:true, state:ready, recipe:A4); tunnel mati di tengah misi -> bangun ulang tunnel sendiri. DILARANG merestart layanan/tunnel milik operator.
2. Satu request pada satu waktu (server FIFO). 503 = back-pressure normal: tunggu header Retry-After (30/60 dtk), maks 6 retry, catat tiap retry di laporan.
3. Alat kanonik (jangan tulis ulang): klien `C:/Users/TRIAL/workspace/handoff/imagegen21_client.py` (cfg 2.0, UDEC-62 - jangan override), `edit_grid.py` metode grid `--cells` + `--margin` (DILARANG tebak kotak piksel), prompt disusun `build_prompt.py` dari slide_spec + design_master.
4. Maks 2 seed per butir (generate maupun edit). Gagal lagi -> lapor FAIL ke controller dengan catatan spesifik; DILARANG regenerasi penuh otomatis.
5. Konten sakral (haram SOP): angka, fakta, named entity hanya dari SPEC/materi user; improvisasi maksimal L2 (gaya/struktur). Design tanpa input user = gerbang HIL (skill create-image-gsp/create-deck-gsp).
6. Sebelum serah: cek struktur mandiri via `vision_analyze` vs SPEC (jumlah tile/callout, logo lockup 1x, tanpa teks liar/seam); simpan PNG + record.json di folder misi `docs/<misi>/` shared workspace; laporkan hash SHA-256 PNG.
7. Rujukan wajib: SOP `C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md` (SOP v2 recipe A4) + mapping `docs/2026-09-25-imagegen21-orchestration-mapping.md`."""


def _assert_write_allowed(path):
    norm = os.path.normcase(os.path.abspath(path))
    root = os.path.normcase(os.path.abspath(DEST))
    if not norm.startswith(root + os.sep) and norm != root:
        raise RuntimeError(f"PELANGGARAN batas tulis: upaya tulis di luar {DEST}: {path}")


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def build_config():
    """Basis config nyata dari disk + mutasi terarah (model.default, toolset vision)."""
    txt = read_text(CONFIG_REF)
    missing = [k for k in CONFIG_REQUIRED_KEYS if k not in txt]
    if missing:
        return None, f"config rujukan kehilangan kunci wajib: {missing}"
    lines = txt.split("\n")
    out, in_model, model_done = [], False, False
    for ln in lines:
        if ln == "model:":
            in_model, model_done = True, False
        elif in_model and not model_done and ln == "  default: auto-efficient":
            ln = "  default: worker-fast"
            model_done = True
        elif in_model and (ln[:1].strip() or not ln.startswith(" ")):
            in_model = False
        out.append(ln)
    if not model_done:
        return None, "penanda '  default: auto-efficient' tidak ditemukan di blok model:"
    txt2 = "\n".join(out)
    # sisipkan '- vision' di akhir daftar cli: di bawah platform_toolsets:
    lines = txt2.split("\n")
    out, i = [], 0
    inserted = False
    while i < len(lines):
        out.append(lines[i])
        if lines[i] == "  cli:":
            j = i + 1
            while j < len(lines) and lines[j].startswith("    - "):
                out.append(lines[j]); j += 1
            if "    - vision" not in out:
                out.append("    - vision")
            inserted = True
            i = j
            continue
        i += 1
    if not inserted:
        return None, "blok '  cli:' tidak ditemukan di platform_toolsets:"
    return "\n".join(out), None


def load_shared_soul_tail():
    if not os.path.isfile(SOUL_REF):
        return None, f"SOUL rujukan tidak ada: {SOUL_REF}"
    txt = read_text(SOUL_REF)
    idx = txt.find(SLICE_FROM)
    if idx < 0:
        return None, f"penanda potong '{SLICE_FROM}' tidak ditemukan di {SOUL_REF}"
    tail = txt[idx:]
    missing = [h for h in REQUIRED_HEADINGS if h not in tail]
    if missing:
        return None, f"potongan rujukan kehilangan judul blok wajib: {missing}"
    if ".lean-policy" in tail:
        return None, "potongan rujukan memuat .lean-policy (pekerja tidak boleh membawanya)"
    return tail, None


def build_soul(tail):
    always_lines = "\n".join(f"- `{s}`" for s in ALWAYS)
    return f"""# SOUL {EMDASH} {NAME}

> Identitas agen spesialis GSP (PT. Gemilang Satria Perkasa). Kamu adalah {PROFIL}, bukan Hermes generik.

## Identitas
- **Profil:** {PROFIL}
- **Peran:** {PERAN}
- **Model:** worker-fast (GSP-AI, vision-capable)

## Persona
Kamu adalah PEKERJA RENDER dalam sistem multi-agen GSP (PT. Gemilang Satria Perkasa), spesialis Imagegen 2.1 (Qwen-Image-2.1 recipe A4).
Kamu bekerja dengan standar akuntabilitas fase GSP: setiap pekerjaan menghasilkan artefak
yang dapat diaudit, kamu melaporkan status secara jujur (complete / blocked / needs-review),
dan kamu TIDAK mengklaim selesai tanpa bukti verifikasi.

## Aturan Khusus Peran
{ROLE_RULES}

## Skill {EMDASH} ALWAYS LOAD (wajib dimuat di awal sesi)
Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:
{always_lines}

{tail}"""


def precondition_report():
    checks = []

    def add(ok, name, detail=""):
        checks.append(("PASS" if ok else "FAIL", name, detail))

    add(len(ALWAYS) <= 3, "ALWAYS load maks 3", f"{len(ALWAYS)} skill: {', '.join(ALWAYS)}")
    add(bool(shutil.which("hermes")), "CLI `hermes` tersedia di PATH", shutil.which("hermes") or "tidak ditemukan")
    add(os.path.isfile(ENV_SOURCE) and os.path.getsize(ENV_SOURCE) > 0, ".env sumber ada & byte > 0", ENV_SOURCE)
    cfg, err = build_config()
    add(cfg is not None, "basis config terbaca + mutasi target sah (worker-fast, vision)", err or CONFIG_REF)
    tail, err = load_shared_soul_tail()
    add(tail is not None, "potongan SOUL bersama terbaca (GATE ENFORCEMENT + GATE NATURALISASI)", err or SOUL_REF)
    for s in ALWAYS:
        present = os.path.isdir(os.path.join(SRC_SKILLS, s))
        add(present, f"skill `{s}` ada di registry fleet", "" if present else SRC_SKILLS)
    if tail is not None and cfg is not None:
        soul = build_soul(tail)
        add(".lean-policy" not in soul, "SOUL bebas marker .lean-policy")
        add(REQUIRED_HEADINGS[0] in soul and REQUIRED_HEADINGS[1] in soul, "SOUL memuat dua blok gate wajib")
        add("worker-fast" in cfg and "    - vision" in cfg, "config hasil: model worker-fast + toolset vision")
    add(os.path.isfile("C:/Users/TRIAL/workspace/handoff/imagegen21_client.py"),
        "klien kanonik imagegen21 ada", "C:/Users/TRIAL/workspace/handoff/imagegen21_client.py")
    add(os.path.isfile("C:/Users/TRIAL/.ssh/id_kaytus"), "kunci ssh id_kaytus ada (jalur tunnel)", "C:/Users/TRIAL/.ssh/id_kaytus")
    exists = os.path.isdir(DEST)
    checks.append(("INFO", "profil target sudah ada" if exists else "profil target belum ada",
                   DEST + (" (mode konvergen)" if exists else " (create akan dijalankan)")))
    return checks


def cmd_check():
    print("=== create_imagegen_worker.py --check (dry-run, nol tulis) ===")
    checks = precondition_report()
    fails = 0
    for status, name, detail in checks:
        print(f"CHECK {status}: {name}" + (f" - {detail}" if detail else ""))
        fails += status == "FAIL"
    print("VERDICT:", "SIAP" if fails == 0 else f"TIDAK SIAP ({fails} FAIL)")
    return 0 if fails == 0 else 1


def cmd_apply():
    print(f"=== provisioning {PROFIL} (apply) ===")
    checks = precondition_report()
    fails = [c for c in checks if c[0] == "FAIL"]
    for status, name, detail in checks:
        print(f"CHECK {status}: {name}" + (f" - {detail}" if detail else ""))
    if fails:
        print("VERDICT: DIBATALKAN - prasyarat FAIL, tidak ada yang ditulis")
        return 1

    if os.path.isdir(DEST):
        print("create: dilewati (profil sudah ada) - konvergen")
    else:
        r = subprocess.run(["hermes", "profile", "create", PROFIL, "--no-skills", "--no-alias",
                            "--description", DESC], capture_output=True, text=True, check=False)
        print("create:", r.returncode, (r.stdout or r.stderr).strip()[-200:])
        if r.returncode != 0 and not os.path.isdir(DEST):
            print("VERDICT: GAGAL - create gagal dan direktori tidak terbentuk")
            return 1

    cfg, _ = build_config()
    tail, _ = load_shared_soul_tail()

    p = os.path.join(DEST, "config.yaml")
    _assert_write_allowed(p)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(cfg)
    print("config.yaml tertulis (basis:", CONFIG_REF + "; mutasi: worker-fast + vision)")

    p = os.path.join(DEST, ".env")
    _assert_write_allowed(p)
    shutil.copy2(ENV_SOURCE, p)
    print(".env tersalin dari", ENV_SOURCE)

    skdir = os.path.join(DEST, "skills")
    _assert_write_allowed(skdir)
    os.makedirs(skdir, exist_ok=True)
    copied = []
    for s in sorted(set(ALWAYS)):
        src = os.path.join(SRC_SKILLS, s)
        tgt = os.path.join(skdir, s)
        _assert_write_allowed(tgt)
        if os.path.exists(tgt):
            shutil.rmtree(tgt)
        shutil.copytree(src, tgt)
        copied.append(s)
    print("skills tersalin:", ", ".join(copied))

    p = os.path.join(DEST, "SOUL.md")
    _assert_write_allowed(p)
    soul = build_soul(tail)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(soul)
    print("SOUL.md tertulis,", len(soul), "karakter")

    # marker opt-out re-seed bundled (ROOT profil)
    mkr = os.path.join(DEST, ".no-bundled-skills")
    _assert_write_allowed(mkr)
    open(mkr, "w").close()
    print("marker .no-bundled-skills ditulis di ROOT profil")

    # self-verification pasca-tulis
    ok = True
    for fname, marker in [("SOUL.md", REQUIRED_HEADINGS[0]),
                          ("SOUL.md", REQUIRED_HEADINGS[1]),
                          ("config.yaml", "  default: worker-fast"),
                          ("config.yaml", "    - vision"),
                          ("config.yaml", "provider: GSP-AI"),
                          ("config.yaml", WORKSPACE)]:
        got = marker in read_text(os.path.join(DEST, fname))
        print(f"CHECK {'PASS' if got else 'FAIL'}: {fname} memuat '{marker}'")
        ok &= got
    env_ok = os.path.isfile(os.path.join(DEST, ".env")) and os.path.getsize(os.path.join(DEST, ".env")) > 0
    print(f"CHECK {'PASS' if env_ok else 'FAIL'}: .env ada & byte > 0 ({os.path.getsize(os.path.join(DEST, '.env'))} B)")
    ok &= env_ok
    import yaml
    try:
        parsed = yaml.safe_load(read_text(os.path.join(DEST, "config.yaml")))
        good = (parsed["model"]["default"] == "worker-fast"
                and "vision" in parsed["platform_toolsets"]["cli"]
                and parsed["terminal"]["cwd"] == WORKSPACE)
        print(f"CHECK {'PASS' if good else 'FAIL'}: config.yaml re-parse YAML valid + nilai target benar")
        ok &= good
    except Exception as e:
        print("CHECK FAIL: config.yaml tidak dapat di-parse:", e)
        ok = False

    try:
        g = subprocess.run(GUARD, capture_output=True, text=True, timeout=180, check=False)
        out = ((g.stdout or "") + (g.stderr or "")).strip()
        print("guard exit:", g.returncode)
        print(out[-1500:] if out else "(guard tanpa output)")
    except (OSError, subprocess.TimeoutExpired) as e:
        print("guard tidak dapat dijalankan:", e, "- dicatat, bukan digagarkan")

    print("VERDICT:", "PROFIL TERSEDIA" if ok else "BELUM LULUS verifikasi mandiri")
    return 0 if ok else 1


def main():
    ap = argparse.ArgumentParser(description="Provisioning idempoten profil gsp-imagegen-worker")
    ap.add_argument("--check", action="store_true", help="dry-run tanpa menulis")
    args = ap.parse_args()
    return cmd_check() if args.check else cmd_apply()


if __name__ == "__main__":
    sys.exit(main())
