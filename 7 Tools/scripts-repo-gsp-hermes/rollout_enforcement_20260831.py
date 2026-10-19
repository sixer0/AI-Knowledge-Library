#!/usr/bin/env python3
"""Rollout 31-08-2026: Lean non-GSP + GATE ENFORCEMENT dua-lane (Controller/Worker).
Kontrak: docs/2026-08-31-enforcement-fleet/contract.md | Idempoten, byte-safe CRLF,
backup berstempel per-run SEBELUM perubahan apa pun.
"""
import json, os, re, shutil, sys, time
from pathlib import Path

RUN_STAMP = time.strftime("%Y%m%d_%H%M%S")
# [GAYA-AHLI-1005-PERSIST] --dry-run: tidak menulis/menghapus apa pun (selftest aman).
DRY = "--dry-run" in sys.argv
LOCALAPPDATA = Path(os.environ.get("LOCALAPPDATA", "C:/Users/TRIAL/AppData/Local"))
HERMES_HOME = LOCALAPPDATA / "hermes"
PROFILES = HERMES_HOME / "profiles"
REGISTRY = HERMES_HOME / "skills" / "gsp"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
BACKUPS = WS / "backups" / f"2026-08-31-enforcement-{RUN_STAMP}"
PAIR = ["gsp-orchestrator-worker", "gsp-orchestration-execution"]
VERIF = "gsp-verification-before-completion"

CONTROLLERS = {
    # name -> (physical skills to ensure, ALWAYS list for SOUL)
    "default": {"path": HERMES_HOME, "always": PAIR + [VERIF], "extra": []},
    "gsp-crawler-orchestrator": {"always": PAIR + [VERIF, "gsp-vendor-crawler"],
        "extra": ["gsp-social-media-collection-workflow"]},
    "gsp-skill-manager": {"always": PAIR + [VERIF, "gsp-skill-distribution"], "extra": []},
    "gsp-system-manager": {"always": PAIR + [VERIF, "gsp-system-manager-ops"], "extra": []},
    "gsp-pm-planner": {"always": PAIR + [VERIF, "gsp-writing-plans"], "extra": []},
    "user01": {"always": PAIR + [VERIF], "extra": [], "lean": True},
    "novriandy": {"always": PAIR + [VERIF], "extra": [], "lean": True},
    "firmanhidayat": {"always": PAIR + [VERIF], "extra": [], "lean": True},
    # RBAC=controller (gelombang 2, aturan user 31-08; detail: promote_rbac_controllers_20260831.py)
    "gsp-budi": {"always": PAIR + [VERIF], "extra": [], "lean": True},
    "gsp-creative": {"always": PAIR + [VERIF], "extra": [], "lean": True},
    "gsp-firman-custom": {"always": PAIR + [VERIF], "extra": [], "lean": False},
    # RBAC=controller (scan ke-3, akun baru otomatis via rbac_roster.mjs: agentriset)
    "agentriset": {"always": PAIR + [VERIF], "extra": [], "lean": True},
}
WORKER_LEAN = {}

GATE_CONTROLLER = """## GATE ENFORCEMENT — LANE CONTROLLER/Orchestrator (WAJIB, kebijakan 31-08-2026)
Kamu profil tipe CONTROLLER/Orchestrator. Aturan ini tidak bisa ditawar:
1. **Load skill orkestrasi di awal SETIAP tugas** — `gsp-orchestrator-worker` + `gsp-orchestration-execution` via `skill_view(name=...)`, bahkan untuk tugas kecil. LOAD ≠ EXECUTE: setelah dimuat, jalankan fasenya.
2. **Delegasi RT+TA wajib**: permintaan mentah → dispatch `gsp-request-translator` (RT) untuk penerjemahan; cetak biru tugas → dispatch `gsp-task-architect` (TA). Controller TIDAK menerjemahkan permintaan atau menyusun blueprint sendiri (RT-first; penulis = verifikator terlemah).
3. **Jejak wajib sebelum klaim selesai**: kartu kanban kontrak (buat sebelum eksekusi, tutup dengan bukti), contract doc di shared workspace docs/, dan dispatch trace via HQ (AgentRequest).
4. Batas skill: ALWAYS LOAD = {always_str}; fisik ≤5 skill (pair orkestrasi + verifikasi + skill inti peran).
"""
GATE_WORKER = """## GATE ENFORCEMENT — LANE PEKERJA/Worker (WAJIB, kebijakan 31-08-2026)
Kamu profil tipe PEKERJA (bukan controller). Alur wajib untuk SETIAP tugas:
1. **Parse detail tugas** — tuliskan di awal laporan: Role kamu + Tugas + apa yang akan kamu kerjakan (2-3 baris).
2. **Request skill ke Skill Manager** (`gsp-skill-manager`, dispatch HQ) dengan format: **Role:** <peranmu> / **Tugas:** <deskripsi> / **Skill yang dibutuhkan:** <kandidat>. Manager menimbang dan mempromosikan daftar skill + penunjang.
3. **Load skill hasil promosi** via `skill_view(name=...)`. Fallback mandiri (manager tak terjangkau / sesi oneshot): baca `SKILL.md` langsung dari registry fleet `$LOCALAPPDATA/hermes/skills/gsp/<nama>/`, dan catat request AWARENESS-mu di laporan agar distribusi tetap tercatat.
4. **Kerjakan tugas** sesuai skill yang dimuat; verifikasi fungsional sebelum klaim; lapor lewat kartu kanban (status + bukti), bukan hanya chat.
5. **Eskalasi manusia hanya via orkestrator**: butuh keputusan -> komentar "KEPUTUSAN DIBUTUHKAN: <pertanyaan>" di kartu + tutup STATUS needs_input/partial-handoff; DILARANG chat/assign manusia langsung (putusan user 08-09 D-10; normatif: gsp-orchestration-execution §Norma rute eskalasi dua-kanal).
"""
AWARENESS_BLOCK = """## Skill — AWARENESS (muat saat diminta / pemicu cocok)
Kamu tidak membawa skill on-demand secara fisik. Jika tugas membutuhkan skill spesifik, BERITAHU Skill Manager (`gsp-skill-manager`) dengan format: **Role:** <peran> / **Tugas:** <deskripsi> / **Skill yang dibutuhkan:** <nama>. Setelah menerima daftar, muat via `skill_view(name=...)` dan kerjakan.
"""

def eol_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"

def read(p: Path) -> str:
    return p.read_text(encoding="utf-8", errors="replace")

def write_bytesafe(p: Path, text: str):
    if DRY:
        print(f"[dry-run] tulis dilewati: {p}")
        return
    p.write_bytes(text.encode("utf-8"))

def is_stock_soul(text: str) -> bool:
    """[GAYA-AHLI-1005-PERSIST] Deteksi SOUL stok yang BENAR — sama seperti isStockSoul
    provisioning (ensure-profile-complete.mjs): awalan 'You are Hermes Agent'.
    Predikat lama 'Nous Research' in text SALAH: string itu ada di SEMUA SOUL fleet
    (kalimat larangan baris 29) sehingga cabang ganti-utuh terpicu pada SOUL custom."""
    return text.lstrip("\ufeff").lstrip().startswith("You are Hermes Agent")

def ensure_gate(soul: Path, kind: str, always: list) -> str:
    """Append the right gate (+awareness for profiles lacking it). Idempoten."""
    if not soul.is_file():
        return "no-soul"
    text = read(soul)
    e = eol_for(text)
    changed = []
    gate_src = GATE_CONTROLLER if kind == "controller" else GATE_WORKER
    gate = gate_src.replace("{always_str}", ", ".join(f"`{a}`" for a in always))
    gate = gate.replace("\n", e)
    if "GATE ENFORCEMENT — LANE CONTROLLER" in text and kind == "worker":
        text = text.replace("GATE ENFORCEMENT — LANE CONTROLLER", "GATE ENFORCEMENT — LANE PEKERJA")  # shouldn't happen
    if "GATE ENFORCEMENT" not in text:
        text = text.rstrip() + e + e + gate
        changed.append("gate")
    if kind == "worker" and "AWARENESS" not in text:
        text = text.rstrip() + e + e + AWARENESS_BLOCK.replace("\n", e)
        changed.append("awareness")
    if changed:
        write_bytesafe(soul, text)
    return "+".join(changed) if changed else "skip"

def rewrite_always(soul: Path, always: list) -> str:
    """Replace the ALWAYS LOAD bullet list in-place (fleet-style SOULs)."""
    text = read(soul)
    e = eol_for(text)
    m = re.search(r"(## Skill — ALWAYS LOAD[^\n]*\n)(.*?)(?=\n## )", text, re.S)
    if not m:
        return "no-section"
    body_lines = [f"- `{a}`{e}" for a in always]
    new_block = m.group(1) + f"Gunakan `skill_view(name=...)` untuk memuat skill berikut SEBELUM mulai bekerja:{e}" + "".join(body_lines) + "\n"
    text = text[:m.start()] + new_block.rstrip("\n") + text[m.end():]
    write_bytesafe(soul, text)
    return "rewritten"

def copy_skill(name: str, dst_root: Path) -> bool:
    src = REGISTRY / name
    if not (src / "SKILL.md").is_file():
        raise SystemExit(f"ABORT: skill {name} tidak ada di registry fleet — jangan lanjut.")
    dst = dst_root / name
    if DRY:
        print(f"[dry-run] copy_skill dilewati: {name} -> {dst}")
        return True
    if dst.is_dir():
        shutil.rmtree(dst)
    shutil.copytree(src, dst)
    return True

def lean_profile(pdir: Path, keep: list, tag: str):
    skills = pdir / "skills"
    # [GAYA-AHLI-1005-PERSIST] dry-run: jangan menyentuh pohon skill sama sekali.
    if DRY:
        print(f"[dry-run] lean_profile dilewati: {tag} ({pdir})")
        return {"policy": "lean+enforcement", "lean": True, "date": "2026-08-31", "lane": None,
                "always_load": keep, "contract": "docs/2026-08-31-enforcement-fleet/contract.md"}
    # backup penuh (zip) sebelum hapus
    BACKUPS.mkdir(parents=True, exist_ok=True)
    zip_base = BACKUPS / f"{tag}_skills"
    if not Path(str(zip_base) + ".zip").exists():
        shutil.make_archive(str(zip_base), "zip", root_dir=skills)
    # hapus SEMUA isi skills/ (kandidat bundle personal tanpa .bundled_manifest),
    # sisakan hanya daftar keep (flat), lalu salin ulang segar dari registry
    if skills.is_dir():
        for child in skills.iterdir():
            if child.name.startswith("."):
                continue
            if child.name in keep:
                continue
            if child.is_dir():
                shutil.rmtree(child)
            else:
                child.unlink()
    for name in keep:
        copy_skill(name, skills)
    # marker kebijakan
    marker = {"policy": "lean+enforcement", "lean": True, "date": "2026-08-31", "lane": None,
              "always_load": keep, "contract": "docs/2026-08-31-enforcement-fleet/contract.md"}
    return marker

def main():
    results = []
    # 1) Lean + physical skills untuk profil yang didefinisikan
    all_targets = {}
    for k, v in CONTROLLERS.items():
        all_targets[k] = (v, "controller")
    for k, v in WORKER_LEAN.items():
        all_targets[k] = (v, "worker")

    for name, (spec, kind) in all_targets.items():
        pdir = PROFILES / name if name != "default" else HERMES_HOME
        # [GAYA-AHLI-1005-PERSIST] target basi (folder profil tak ada, mis. user01/novriandy/
        # gsp-budi) DILEWATI — dulu crash FileNotFoundError di tengah loop melindungi profil
        # setelahnya secara kecelakaan; sekarang dilewati eksplisit dan terdokumentasi.
        if not pdir.is_dir():
            results.append((name, kind, "skip-no-profile-dir", "-", len(keep := spec["always"] + spec.get("extra", []))))
            continue
        keep = spec["always"] + spec.get("extra", [])
        if spec.get("lean"):
            marker = lean_profile(pdir, keep, name)
            marker["lane"] = kind
            write_bytesafe(pdir / ".lean-policy", json.dumps(marker, indent=1))
        # profil personal dgn SOUL stok lama -> ganti ke SOUL Swarm root (disimpan di backup).
        # [GAYA-AHLI-1005-PERSIST] predikat stock yang BENAR (awalan 'You are Hermes Agent'),
        # bukan lagi 'Nous Research' yang ada di SEMUA SOUL fleet (ganti-utuh SOUL custom).
        soul = pdir / "SOUL.md"
        if spec.get("lean") and soul.is_file() and is_stock_soul(read(soul)):
            if DRY:
                print(f"[dry-run] ganti-utuh SOUL dilewati: {soul}")
            else:
                BACKUPS.mkdir(parents=True, exist_ok=True)
                shutil.copy2(soul, BACKUPS / f"{name}_SOUL.md.pre")
                shutil.copy2(HERMES_HOME / "SOUL.md", soul)
        if not spec.get("lean"):
            # pair wajib fisik + verifikasi (sisa yang ada dibiarkan, cap ≤5 dicek verifier)
            skills = pdir / "skills"
            dst_root = skills / "gsp" if name == "default" else skills
            for s in keep:
                if not (dst_root / s / "SKILL.md").is_file():
                    copy_skill(s, dst_root)
            if name != "default":
                marker = {"policy": "lean+enforcement", "date": "2026-08-31", "lane": kind,
                          "always_load": spec["always"],
                          "contract": "docs/2026-08-31-enforcement-fleet/contract.md"}
                write_bytesafe(pdir / ".lean-policy", json.dumps(marker, indent=1))
        # 2) gate SOUL
        soul = pdir / "SOUL.md"
        gate_res = ensure_gate(soul, kind, spec["always"])
        always_res = "-"
        if name not in ("default",):  # swarm-personal/root SOUL tidak punya blok ALWAYS fleet-style
            always_res = rewrite_always(soul, spec["always"]) if "ALWAYS LOAD" in read(soul) else "appended-via-gate"
        results.append((name, kind, gate_res, always_res, len(keep)))

    # 3) gate utk SEMUA profil lain (worker lane)
    for pdir in sorted(PROFILES.iterdir()):
        if not pdir.is_dir() or pdir.name in all_targets:
            continue
        soul = pdir / "SOUL.md"
        res = ensure_gate(soul, "worker", [])
        results.append((pdir.name, "worker", res, "-", "-"))

    print(f"{'profile':32} {'lane':10} {'gate':22} {'always':18} keep")
    for r in results:
        print(f"{r[0]:32} {r[1]:10} {str(r[2]):22} {str(r[3]):18} {r[4]}")
    print(f"\nbackup -> {BACKUPS}")

if __name__ == "__main__":
    main()
