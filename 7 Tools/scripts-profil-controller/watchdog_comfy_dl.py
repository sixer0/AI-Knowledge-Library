#!/usr/bin/env python3
# watchdog_comfy_dl.py — bungkus bash watchdog pakai Git-bash ABSOLUT (hindari WSL relay).
# no_agent cron: stdout kosong = diam (sehat); stdout terisi = restart/WEIGHTS_READY.
import os, subprocess, sys

BASH = r"C:\Program Files\Git\bin\bash.exe"
SCRIPT = r"C:\Users\TRIAL\workspace\comfyui-check\watchdog_comfy_dl.sh"

if not os.path.exists(BASH):
    for cand in (r"C:\Program Files\Git\usr\bin\bash.exe",):
        if os.path.exists(cand): BASH = cand; break

r = subprocess.run([BASH, SCRIPT], capture_output=True, text=True, timeout=240)
out = (r.stdout or "").strip()
if out:
    print(out)
elif r.returncode != 0:
    print(f"WATCHDOG-ERROR rc={r.returncode}: {(r.stderr or '')[:300]}")
sys.exit(0)
