#!/usr/bin/env python3
"""Remediasi INV-7 (fail lean >cap 5) untuk 8 profil controller, 29-09-2026.
Pola = lean_budi_master01_20260902.py / lean_gspuser01_20260902.py (turunan
promote_rbac_controllers_20260831.py lean=True), digeneralisasi: keep diambil
dari marker .lean-policy masing-masing (always_load), BUKAN trio kaku.
rollout_enforcement_20260831.py tidak dipakai lagi karena crash di target basi
(user01/novriandy sudah tiada). Idempoten; backup zip penuh sebelum wipe; SOUL
tidak disentuh (hanya diverifikasi gate CONTROLLER + identitas Swarm).
"""
import json, shutil, time
from pathlib import Path

LA = Path("C:/Users/TRIAL/AppData/Local/hermes")
REG = LA / "skills" / "gsp"
WS = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace")
BACKUPS = WS / "backups" / f"2026-09-29-lean-fix-inv7-{time.strftime('%Y%m%d_%H%M%S')}"
NAMES = ["agentriset", "firmanhidayat", "gsp-creative", "gsp-master",
         "gsp-master01", "gspuser01", "gspuser02", "rafif"]

def fix(NAME):
    pdir = LA / "profiles" / NAME
    skills = pdir / "skills"
    assert pdir.is_dir(), f"profil {NAME} tidak ada"
    mk = json.loads((pdir / ".lean-policy").read_text(encoding="utf-8"))
    keep = list(mk["always_load"])
    assert mk.get("lean") and mk.get("lane") == "controller", f"{NAME}: marker bukan lean-controller"
    for s in keep:
        assert (REG / s / "SKILL.md").is_file(), f"registry hilang: {s}"
    have = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
    if have == sorted(keep):
        return {"profile": NAME, "skipped": True, "skills": have}
    # 1) backup zip penuh sebelum perubahan apa pun
    BACKUPS.mkdir(parents=True, exist_ok=True)
    shutil.make_archive(str(BACKUPS / f"{NAME}_skills"), "zip", root_dir=skills)
    # 2) wipe non-dot di luar keep, lalu salin ulang segar dari registry
    for child in skills.iterdir():
        if child.name.startswith(".") or child.name in keep:
            continue
        shutil.rmtree(child) if child.is_dir() else child.unlink()
    for s in keep:
        dst = skills / s
        if dst.is_dir():
            shutil.rmtree(dst)
        shutil.copytree(REG / s, dst)
    # manifest bundel basi + snapshot prompt basi -> hapus (di-build ulang engine)
    for junk in (skills / ".bundled_manifest", pdir / ".skills_prompt_snapshot.json"):
        if junk.exists():
            junk.unlink()
    # 3) verifikasi: fisik == keep, cap <=5, SOUL utuh (gate CONTROLLER + identitas)
    after = sorted(d.name for d in skills.iterdir() if d.is_dir() and not d.name.startswith("."))
    soul = (pdir / "SOUL.md").read_text(encoding="utf-8")
    gate_ok = "GATE ENFORCEMENT — LANE CONTROLLER" in soul
    ident_ok = soul.startswith("# Swarm") and "PT. Gemilang Satria Perkasa" in soul
    res = {"profile": NAME, "before": len(have), "after": after,
           "soul_gate_controller": gate_ok, "soul_identity_intact": ident_ok,
           "backup_zip": str(BACKUPS / f"{NAME}_skills.zip")}
    assert after == sorted(keep) and len(after) <= 5 and gate_ok and ident_ok, f"VERIFIKASI GAGAL {NAME}: {res}"
    return res

if __name__ == "__main__":
    out = [fix(n) for n in NAMES]
    print(json.dumps(out, indent=1))
