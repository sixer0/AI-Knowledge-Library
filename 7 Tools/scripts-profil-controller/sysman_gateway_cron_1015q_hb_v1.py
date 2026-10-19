# Saksi kesegaran gateway NON-WMI: baca state/gateway.heartbeat per profil (pid + updated_at UTC).
# Read-only. Vonis: umur heartbeat tiap profil dalam daftar hidup registri.
import json, os, sys, time, datetime

BASE = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"

with open(REG, encoding="utf-8") as f:
    reg = json.load(f)
live = reg["hidup"]
wajib = reg["gateway_wajib_hidup"]

now = time.time()
print("=== HEARTBEAT GATEWAY (non-WMI) %s ===" % datetime.datetime.now().isoformat(timespec="seconds"))
ROOT = "C:/Users/TRIAL/AppData/Local/hermes"
for p in live:
    hb = os.path.join(BASE, p, "state", "gateway.heartbeat")
    if not os.path.exists(hb) and p == "default":
        # profil default memakai home = root hermes, jadi heartbeatnya di state root
        # (pola sama dengan heartbeat_age_s di gsp_gateway_monitor_v1.py L53-54).
        hb = os.path.join(ROOT, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print("  %-22s TIDAK-ADA-BERKAS" % p)
        continue
    age = now - os.path.getmtime(hb)
    try:
        with open(hb, encoding="utf-8", errors="replace") as f:
            raw = f.read().strip()
    except Exception as e:
        raw = "ERR:%s" % e
    print("  %-22s umur=%6.0fs isi=%s" % (p, age, raw[:120].replace("\n", "|")))
print("--- wajib: %s ---" % ",".join(wajib))
