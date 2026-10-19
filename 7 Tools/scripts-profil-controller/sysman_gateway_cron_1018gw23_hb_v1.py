# Ronde penjaga gateway 18-10-23: saksi heartbeat non-WMI (read-only)
import json, os, time, io

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
WAJIB = ["gsp-thinker", "gsp-worker", "gsp-worker-fast"]

reg = json.load(open(REG, encoding="utf-8"))
live = reg["hidup"]
now = time.time()

def hb_path(p):
    if p == "default":
        return os.path.join(HERMES, "state", "gateway.heartbeat")
    return os.path.join(HERMES, "profiles", p, "state", "gateway.heartbeat")

print("=== SAKSI HEARTBEAT (non-WMI) ===")
for p in live:
    f = hb_path(p)
    if not os.path.exists(f):
        print(f"  {p:22s} TIDAK-ADA-BERKAS")
        continue
    age = now - os.path.getmtime(f)
    raw = open(f, encoding="utf-8", errors="replace").read().strip()[:120].replace("\n", " ")
    tag = "WAJIB" if p in WAJIB else "     "
    fresh = "FRESH" if age < 180 else ("STALE" if age < 3600 else "BASIS")
    print(f"  {p:22s} {tag} age={age:9.0f}s {fresh:5s} | {raw}")
