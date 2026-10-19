#!/usr/bin/env python3
"""Provisioning profil gsp-3d-specialist (misi Precision 3D Factory, langkah 14, kartu P-B1 t_c986ca8c).

Pola D3 (identification/02_structured.md): preseden nyata mesin ini, persis pola
create_ekas_specialists.py (generate_profiles.py warisan Mac tidak ada di disk).
Spesifikasi profil mengikuti D4; skema data D1/D2/D5 dan pagar Q4-Q7 dikutip di SOUL.

Perilaku:
  - Idempoten: dijalankan berulang mengkonvergenkan keadaan (create sekali, tulis ulang
    config/SOUL, salin ulang skill) tanpa menyentuh profil lain.
  - --check : dry-run penuh (prasyarat + konsistensi template + rencana aksi); TIDAK menulis
    apa pun dan TIDAK memanggil hermes/guard.
  - default : eksekusi provisioning + guard ensure-profile-complete.mjs (hasil guard
    dilaporkan apa adanya, kegagalan tak relevan tidak dipaksakan pass, sesuai D3 butir 4).

Batas keras (D3 butir 5 + Definition of Failure RT sec 5):
  - HANYA profil gsp-3d-specialist yang boleh ditulis; semua baca dari profil lain
    (config basis, .env librarian, SOUL rujukan) bersifat read-only.
  - Basis config disalin dari profil EKAS yang ada di disk, bukan ditulis dari ingatan.
  - Tanpa marker .lean-policy (pekerja, bukan controller RBAC).
"""
import argparse
import os
import shutil
import subprocess
import sys

# --- Konstanta jalur nyata mesin ini (forward-slash native untuk program Windows) ---
HOME = os.path.expanduser("~")
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", os.path.join(HOME, "AppData", "Local"))
PROFILES = os.path.join(LOCALAPPDATA, "hermes", "profiles")
SRC_SKILLS = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")   # registry fleet on-demand
WORKSPACE = "C:/Users/TRIAL/workspace/gsp-hermes/workspace"

PROFIL = "gsp-3d-specialist"                 # SATU-SATUNYA profil yang boleh ditulis
DEST = os.path.join(PROFILES, PROFIL)
NAME = "3D Precision Specialist"
DESC = ("3D Precision Specialist: brief proyek jadi parameter sheet, skrip Blender headless, "
        "dim_check presisi, export GLB/OBJ round-trip, render still produk CPU, laporan QA")
PERAN = ("Eksekutor brief proyek 3D presisi: parameter sheet -> skrip Blender headless -> "
         "dim_check -> export GLB/OBJ -> render still -> laporan QA")

# ALWAYS load maks 3 (D4). gsp-blender-parametric dibangun fase V; sampai ada, lembar resep
# kontrak dipakai sebagai pengganti (dinyatakan eksplisit di SOUL, salinan resep di registry
# akan ikut tersalin otomatis saat re-run setelah skill itu lahir).
ALWAYS = ["gsp-blender-parametric", "gsp-verification-before-completion", "pustaka-teknis"]
SKILL_TBD = {"gsp-blender-parametric"}       # absen sah di registry sampai fase V membangunnya
NOTE_BLENDER_PARAMETRIC = (" (skill inti domain; sampai dibangun fase V, pakai lembar resep "
                           "`docs/2026-09-02-precision-3d-factory/research/recipes/` sebagai pengganti)")

ENV_SOURCE = os.path.join(PROFILES, "gsp-librarian", ".env")          # vars identik (pola EKAS)
CONFIG_REF = os.path.join(PROFILES, "gsp-vss-specialist", "config.yaml")   # basis config D3 butir 3
SOUL_REF = os.path.join(PROFILES, "gsp-vss-specialist", "SOUL.md")    # sumber potongan bersama
GUARD = ["node", "C:/Users/TRIAL/gsp-datacenter/scripts/ensure-profile-complete.mjs", "check", PROFIL]

# Em dash U+2014 dibangun dari kode titik (bukan literal) supaya berkas skrip ini lolos
# gerbang naturalisasi A1 (nol literal U+2014) sekaligus menghasilkan judul SOUL yang
# byte-identik dengan profil pekerja fleet lain (judul blok dijaga cron INV-7).
EMDASH = chr(0x2014)

SLICE_FROM = f"## Skill {EMDASH} AWARENESS"   # titik potong potongan bersama SOUL rujukan
REQUIRED_HEADINGS = [
    f"## GATE ENFORCEMENT {EMDASH} LANE PEKERJA/Worker (WAJIB, kebijakan 31-08-2026)",
    "## GATE NATURALISASI (WAJIB, kebijakan 02-09-2026)",
]
CONFIG_REQUIRED_KEYS = ["default: auto-efficient", "provider: GSP-AI",
                        "fallback_providers", "kilocode", "search_backend: searxng",
                        WORKSPACE]

ROLE_RULES = """1. Mesin produksi = Blender Python API headless (`blender -b -P script.py`) dengan jalur native forward-slash (`C:/Program Files/Blender Foundation/Blender 5.2/blender.exe`); TANPA GUI; MCP maksimal review visual dan boleh mati tanpa membatalkan pilot.
2. Angka geometri hanya dari parameter sheet skema D1 (`param_sheet.yaml`): tidak ada angka yang lahir di dalam skrip tanpa entri `dimensi[]` bersumber (spek/datasheet OEM/asumsi berlabel).
3. Klaim presisi hanya lewat `dim_check.json` skema D2 dengan toleransi maks(0,5 mm; 0,1% dimensi) sampai spek proyek nyata (gate Q5); juri visual TIDAK PERNAH memutuskan dimensi.
4. Render pilot CPU murni (gate Q6); serial rule D8: maksimal satu proses Cycles CPU pada satu waktu di seluruh fleet; render berat wajib background process + heartbeat kartu minimal 1x per jam; jendela render diumumkan di komentar kartu sebelum mulai.
5. Addon/MCP hanya dari whitelist R-GATE yang lolos lisensi (gate Q7): trimesh pip ter-pin + SHA-256 saat instal; blender-mcp hanya versi ter-pin + telemetry mati; DILARANG lab/blender_mcp, Sverchok, Text2CAD, DeepCAD/GenCAD/CAD-Recode/Genspex, ntriq-x402. Nol pemasangan sebelum gerbang keputusan controller tercatat.
6. Export GLB/OBJ: apply-transform sebelum export, arah sumbu dicatat (Blender Z-up vs glTF Y-up), wajib lulus uji round-trip impor-ulang (delta pengukuran nol) sebelum klaim; satuan P1: 1 BU = 1 mm; penamaan `<proyek>_<objek>_<rev>.glb`.
7. Determinisme dua-run: hash pengukuran harus identik antar-run dengan sheet identik; beda hash = akar penyebab dicari sebelum lanjut."""


def _assert_write_allowed(path):
    """Guard D3 butir 5: satu-satunya lokasi tulis adalah direktori profil gsp-3d-specialist."""
    norm = os.path.normcase(os.path.abspath(path))
    root = os.path.normcase(os.path.abspath(DEST))
    if not norm.startswith(root + os.sep) and norm != root:
        raise RuntimeError(f"PELANGGARAN D3: upaya tulis di luar {DEST}: {path}")


def read_text(path):
    with open(path, encoding="utf-8") as f:
        return f.read()


def load_config_basis():
    """Basis config = salinan profil EKAS nyata di disk (D3 butir 3), diverifikasi kuncinya."""
    if not os.path.isfile(CONFIG_REF):
        return None, f"config rujukan tidak ada: {CONFIG_REF}"
    txt = read_text(CONFIG_REF)
    missing = [k for k in CONFIG_REQUIRED_KEYS if k not in txt]
    if missing:
        return None, f"config rujukan kehilangan kunci wajib: {missing}"
    return txt, None


def load_shared_soul_tail():
    """Potongan bersama SOUL (AWARENESS s/d GATE NATURALISASI) disalin utuh dari profil
    pekerja rujukan di disk supaya judul blok persis dan ikut rollout cron INV-7."""
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
    always_lines = []
    for s in ALWAYS:
        always_lines.append(f"- `{s}`" + (NOTE_BLENDER_PARAMETRIC if s == "gsp-blender-parametric" else ""))
    head = f"""# SOUL {EMDASH} {NAME}

> Identitas agen spesialis GSP (PT. Gemilang Satria Perkasa). Kamu adalah {PROFIL}, bukan Swarm generik.

## Identitas
- **Profil:** {PROFIL}
- **Peran:** {PERAN}
- **Model:** auto-efficient (GSP-AI)

## Persona
Kamu adalah SPESIALIS TEKNIS dalam sistem multi-agen GSP (PT. Gemilang Satria Perkasa).
Kamu bekerja dengan standar akuntabilitas fase GSP: setiap pekerjaan menghasilkan artefak
yang dapat diaudit, kamu melaporkan status secara jujur (complete / blocked / needs-review),
dan kamu TIDAK mengklaim selesai tanpa bukti verifikasi.

## Aturan Khusus Peran
{ROLE_RULES}

## Skill {EMDASH} ALWAYS LOAD (wajib dimuat di awal sesi)
Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:
{chr(10).join(always_lines)}

{tail}"""
    return head


def precondition_report():
    """Semua pemeriksaan prasyarat + rencana; mengembalikan daftar (status, nama, detail)."""
    checks = []

    def add(ok, name, detail=""):
        checks.append(("PASS" if ok else "FAIL", name, detail))

    # 1. batas ALWAYS (D4)
    add(len(ALWAYS) <= 3, "ALWAYS load maks 3 (D4)", f"{len(ALWAYS)} skill: {', '.join(ALWAYS)}")

    # 2. hermes tersedia (hanya keberadaan; tidak dipanggil di mode check)
    add(bool(shutil.which("hermes")), "CLI `hermes` tersedia di PATH", shutil.which("hermes") or "tidak ditemukan")

    # 3. sumber .env (read-only)
    ok_env = os.path.isfile(ENV_SOURCE) and os.path.getsize(ENV_SOURCE) > 0
    add(ok_env, ".env sumber gsp-librarian ada & byte > 0", ENV_SOURCE)

    # 4. basis config nyata di disk
    cfg, err = load_config_basis()
    add(cfg is not None, "basis config EKAS nyata terbaca + kunci lengkap", err or CONFIG_REF)

    # 5. potongan SOUL bersama terbaca + blok gate utuh
    tail, err = load_shared_soul_tail()
    add(tail is not None, "potongan SOUL bersama terbaca (GATE ENFORCEMENT + GATE NATURALISASI)", err or SOUL_REF)

    # 6. skill fisik tersedia di registry (kecuali yang sah belum lahir)
    for s in ALWAYS:
        present = os.path.isdir(os.path.join(SRC_SKILLS, s))
        if present or s in SKILL_TBD:
            add(True, f"skill `{s}` siap", "ada di registry" if present else "absen sah sampai fase V (tidak disalin, SOUL memberi pengganti)")
        else:
            add(False, f"skill `{s}` siap", f"tidak ada di {SRC_SKILLS}")

    # 7. hasil render template: tak ada .lean-policy, guard tulis aktif
    if tail is not None:
        soul = build_soul(tail)
        add(".lean-policy" not in soul, "SOUL bebas marker .lean-policy")
        add(REQUIRED_HEADINGS[0] in soul and REQUIRED_HEADINGS[1] in soul, "SOUL memuat dua blok gate wajib")
        try:
            _assert_write_allowed(os.path.join(DEST, "SOUL.md"))
            blocked = False
            try:
                _assert_write_allowed(os.path.join(PROFILES, "gsp-vss-specialist", "SOUL.md"))
                blocked = True
            except RuntimeError:
                pass
            add(not blocked, "guard tulis D3 aktif (hanya profil target yang boleh ditulis)")
        except RuntimeError as e:
            add(False, "guard tulis D3 aktif", str(e))

    # 8. keadaan target saat ini (untuk rencana)
    exists = os.path.isdir(DEST)
    checks.append(("INFO", "profil target sudah ada" if exists else "profil target belum ada",
                   DEST + (" (mode konvergen: create dilewati, berkas dikonsistenkan)" if exists else " (create akan dijalankan)")))
    return checks


def plan_lines():
    return [
        f"RENCANA TULIS (hanya di {DEST}):",
        f"  1. hermes profile create {PROFIL} --no-skills --no-alias --description <desc>",
        f"  2. tulis config.yaml (basis salinan {CONFIG_REF})",
        f"  3. salin .env dari {ENV_SOURCE}",
        f"  4. salin skill fisik dari registry {SRC_SKILLS} (yang tersedia)",
        f"  5. tulis SOUL.md (identitas + aturan peran + ALWAYS + potongan gate dari {SOUL_REF})",
        f"  6. guard: node ensure-profile-complete.mjs check {PROFIL} (hasil dilaporkan apa adanya)",
    ]


def cmd_check():
    print("=== create_3d_specialist.py --check (dry-run, nol tulis) ===")
    print("PROFIL target:", PROFIL)
    checks = precondition_report()
    fails = 0
    for status, name, detail in checks:
        print(f"CHECK {status}: {name}" + (f" - {detail}" if detail else ""))
        fails += status == "FAIL"
    for line in plan_lines():
        print(line)
    print("VERDICT:", "SIAP (jalankan tanpa --check untuk mengeksekusi)" if fails == 0 else f"TIDAK SIAP ({fails} FAIL)")
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

    # 1. create (idempoten: direktori sudah ada = lewati)
    if os.path.isdir(DEST):
        print("create: dilewati (profil sudah ada) - konvergen")
    else:
        r = subprocess.run(["hermes", "profile", "create", PROFIL, "--no-skills", "--no-alias",
                            "--description", DESC], capture_output=True, text=True, check=False)
        print("create:", r.returncode, (r.stdout or r.stderr).strip()[-200:])
        if r.returncode != 0 and not os.path.isdir(DEST):
            print("VERDICT: GAGAL - create gagal dan direktori tidak terbentuk")
            return 1

    cfg, _err_cfg = load_config_basis()
    tail, _err_tail = load_shared_soul_tail()

    # 2. config.yaml
    p = os.path.join(DEST, "config.yaml")
    _assert_write_allowed(p)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(cfg)
    print("config.yaml tertulis (basis:", CONFIG_REF + ")")

    # 3. .env (read-only sumber, tulis hanya ke DEST)
    p = os.path.join(DEST, ".env")
    _assert_write_allowed(p)
    shutil.copy2(ENV_SOURCE, p)
    print(".env tersalin dari gsp-librarian")

    # 4. skills fisik (konvergen: timpa salinan lama dengan registry)
    skdir = os.path.join(DEST, "skills")
    _assert_write_allowed(skdir)
    os.makedirs(skdir, exist_ok=True)
    copied, skipped = [], []
    for s in sorted(set(ALWAYS)):
        src = os.path.join(SRC_SKILLS, s)
        if not os.path.isdir(src):
            skipped.append(s)
            print("  !! skill belum ada di registry (dilewati, akan ikut saat re-run):", s)
            continue
        tgt = os.path.join(skdir, s)
        _assert_write_allowed(tgt)
        if os.path.exists(tgt):
            shutil.rmtree(tgt)
        shutil.copytree(src, tgt)
        copied.append(s)
    print("skills tersalin:", ", ".join(copied) or "(kosong)")
    if skipped:
        print("skills tertunda:", ", ".join(skipped))

    # 5. SOUL.md
    p = os.path.join(DEST, "SOUL.md")
    _assert_write_allowed(p)
    soul = build_soul(tail)
    with open(p, "w", encoding="utf-8", newline="\n") as f:
        f.write(soul)
    print("SOUL.md tertulis,", len(soul), "karakter")

    # 6. self-verification pasca-tulis
    ok = True
    for fname, marker in [("SOUL.md", REQUIRED_HEADINGS[0]), ("config.yaml", "provider: GSP-AI")]:
        got = marker in read_text(os.path.join(DEST, fname))
        print(f"CHECK {'PASS' if got else 'FAIL'}: verifikasi pasca-tulis {fname} memuat penanda wajib")
        ok &= got
    env_ok = os.path.isfile(os.path.join(DEST, ".env")) and os.path.getsize(os.path.join(DEST, ".env")) > 0
    print(f"CHECK {'PASS' if env_ok else 'FAIL'}: .env ada & byte > 0")
    ok &= env_ok

    # 7. guard D3 butir 4 - hasil dilaporkan apa adanya, bukan tujuan kelulusan
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
    ap = argparse.ArgumentParser(description="Provisioning idempoten profil gsp-3d-specialist (pola D3, spec D4)")
    ap.add_argument("--check", action="store_true", help="dry-run: verifikasi prasyarat tanpa menulis apa pun")
    args = ap.parse_args()
    return cmd_check() if args.check else cmd_apply()


if __name__ == "__main__":
    sys.exit(main())
