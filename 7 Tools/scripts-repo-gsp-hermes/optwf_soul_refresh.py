#!/usr/bin/env python3
"""OPT-WF-G14 (approved user D-13): refresh blok GATE LANE PEKERJA pada SOUL profil pekerja
agar memuat BUTIR 5 (rute eskalasi dua-kanal, putusan D-10).

Cara: replace-blok gate '## GATE ENFORCEMENT ... LANE PEKERJA' dengan teks kanonis
GATE_WORKER dari rollout_enforcement_20260831.py (satu-satunya sumber). Profil controller /
tanpa-gate tidak disentuh. Backup setiap SOUL sebelum tulis. Idempoten: skip bila butir 5
sudah ada. --apply untuk menulis; tanpa flag = dry-run.
"""
import re, sys, time, shutil
from pathlib import Path

sys.path.insert(0, r"C:/Users/TRIAL/workspace/gsp-hermes/scripts")
import rollout_enforcement_20260831 as R

APPLY = "--apply" in sys.argv
PROFILES = Path(R.__dict__["PROFILES"])
NEW_BULLET = "Eskalasi manusia hanya via orkestrator"
BACKUPS = Path(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/backups") / f"optwf-g14-soul-{time.strftime('%Y%m%d_%H%M%S')}"
GATE_RE = re.compile(r"## GATE ENFORCEMENT[^\n]*LANE PEKERJA.*?(?=\n## |\Z)", re.S)

def eol_for(text: str) -> str:
    return "\r\n" if "\r\n" in text else "\n"

rows = []
for pdir in sorted(PROFILES.iterdir()):
    soul = pdir / "SOUL.md"
    if not pdir.is_dir() or not soul.is_file():
        continue
    text = soul.read_text(encoding="utf-8", errors="strict")
    m = GATE_RE.search(text)
    if m is None:
        rows.append((pdir.name, "out-of-scope (controller/no-gate)"))
        continue
    if NEW_BULLET in m.group(0):
        rows.append((pdir.name, "skip (butir-5 sudah ada)"))
        continue
    e = eol_for(text)
    new_gate = R.GATE_WORKER.replace("{always_str}", "").replace("\n", e)
    # GATE_WORKER tidak memakai placeholder always_str; pastikan bersih
    new_block = R.GATE_WORKER.replace("\n", e)
    updated = text[:m.start()] + new_block.rstrip() + text[m.end():]
    if APPLY:
        BACKUPS.mkdir(parents=True, exist_ok=True)
        shutil.copy2(soul, BACKUPS / f"{pdir.name}_SOUL.md.pre")
        soul.write_text(updated, encoding="utf-8", newline="")
    rows.append((pdir.name, "REFRESHED" if APPLY else "would-refresh"))

n_ref = sum(1 for _, a in rows if a in ("REFRESHED", "would-refresh"))
n_skip = sum(1 for _, a in rows if a.startswith("skip"))
n_oos = sum(1 for _, a in rows if a.startswith("out-of-scope"))
mode = "APPLY" if APPLY else "DRY-RUN"
print(f"[{mode}] total={len(rows)} refresh={n_ref} skip={n_skip} out-of-scope={n_oos}")
for name, act in rows:
    if act in ("REFRESHED", "would-refresh"):
        print(f"  {name:34} {act}")
if APPLY:
    print(f"backup -> {BACKUPS}")
