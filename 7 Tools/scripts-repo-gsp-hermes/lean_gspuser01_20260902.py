#!/usr/bin/env python3
"""Lean-kan profil gspuser01 ke kelas CONTROLLER (2026-09-02).
Pola = promote_rbac_controllers_20260831.py (gel. lean=True) + marker
.no-bundled-skills (contoh gsp-budi) agar engine sync tidak menimbun ulang
bundled skills. Backup zip penuh skills/ sebelum wipe. Idempoten.
"""
import json, shutil, time
from pathlib import Path

LA = Path("C:/Users/TRIAL/AppData/Local/hermes")
REG = LA / "skills" / "gsp"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
BACKUPS = WS / "backups" / f"2026-09-02-lean-gspuser01-{time.strftime('%Y%m%d_%H%M%S')}"
NAME = "gspuser01"
TRIO = ["gsp-orchestrator-worker", "gsp-orchestration-execution", "gsp-verification-before-completion"]

def main():
    BACKUPS.mkdir(parents=True, exist_ok=True)
    pdir = LA / "profiles" / NAME
    skills = pdir / "skills"
    assert pdir.is_dir(), f"profil {NAME} tidak ada"
    before = sum(1 for _ in skills.rglob("SKILL.md"))
    # 1) backup zip penuh lalu wipe (kecuali dotfile), sisakan trio segar dari registry
    shutil.make_archive(str(BACKUPS / f"{NAME}_skills"), "zip", root_dir=skills)
    for child in skills.iterdir():
        if child.name.startswith("."):
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    for s in TRIO:
        src = REG / s
        assert (src / "SKILL.md").is_file(), f"registry hilang: {s}"
        shutil.copytree(src, skills / s)
    # manifest bundel basi + snapshot prompt basi -> hapus (di-build ulang engine)
    for junk in (skills / ".bundled_manifest", pdir / ".skills_prompt_snapshot.json"):
        if junk.exists():
            junk.unlink()
    # 2) marker: .lean-policy (ensure-profile-complete) + .no-bundled-skills (engine sync)
    (pdir / ".lean-policy").write_text(json.dumps({
        "policy": "lean+enforcement", "lean": True, "date": "2026-09-02",
        "lane": "controller", "always_load": TRIO, "rbac": True,
        "contract": "docs/2026-08-31-enforcement-fleet/contract.md",
    }, indent=1), encoding="utf-8")
    nbm = pdir / ".no-bundled-skills"
    if not nbm.exists():
        nbm.write_text("lean controller: no bundled seeding\n", encoding="utf-8")
    # 3) SOUL: harus sudah ada gate CONTROLLER (dari provisioning); JANGAN tulis ulang
    soul = (pdir / "SOUL.md").read_text(encoding="utf-8")
    gate_ok = "GATE ENFORCEMENT — LANE CONTROLLER" in soul
    ident_ok = soul.startswith("# Swarm") and "PT. Gemilang Satria Perkasa" in soul
    shutil.copy2(pdir / "SOUL.md", BACKUPS / f"{NAME}_SOUL.md.pre")
    after = sum(1 for _ in skills.rglob("SKILL.md"))
    have = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
    print(json.dumps({
        "skill_md_before": before, "skill_md_after": after, "skills_fisik": have,
        "lean_policy": (pdir / ".lean-policy").is_file(),
        "no_bundled_skills": nbm.is_file(),
        "soul_gate_controller": gate_ok, "soul_identity_intact": ident_ok,
        "backup_zip": str(BACKUPS / f"{NAME}_skills.zip"),
    }, indent=1))
    assert after == 3 and gate_ok and ident_ok, "VERIFIKASI GAGAL"

if __name__ == "__main__":
    main()
