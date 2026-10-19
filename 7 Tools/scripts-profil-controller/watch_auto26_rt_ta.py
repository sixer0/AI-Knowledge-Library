#!/usr/bin/env python3
"""Watcher AUTO26: tunggu RT lalu TA selesai (STATUS: complete di disk), lalu exit."""
import time, sys, os, re
WS = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-04-automate26-deepdive/identification"
RT = os.path.join(WS, "01_translated.md")
TA = os.path.join(WS, "02_structured.md")

def done(path):
    try:
        if not os.path.exists(path): return False
        t = open(path, encoding="utf-8", errors="replace").read()
        return bool(re.search(r"STATUS:\s*complete", t)) and len(t) > 3000
    except OSError:
        return False

deadline = time.time() + 3600*2  # 2 jam maksimum
while time.time() < deadline:
    r, t = done(RT), done(TA)
    if t:
        print(f"AUTO26 WATCHER: RT={r} TA={t} - blueprint siap; {time.strftime('%H:%M:%S')}")
        sys.exit(0)
    time.sleep(60)
print("AUTO26 WATCHER: TIMEOUT 2 jam tanpa 02_structured.md complete")
sys.exit(1)
