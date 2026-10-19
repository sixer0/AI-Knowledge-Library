# Saksi kesegaran heartbeat gateway tanpa WMI (read-only), fallback default = HOME root.
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
live = REG["hidup"]
wajib = REG["gateway_wajib_hidup"]
now = time.time()

def hb_path(p):
    # profil `default`: home = ROOT hermes, bukan profiles/default
    return os.path.join(HOME, "state", "gateway.heartbeat") if p == "default" \
        else os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")

print("=== SAKSI HEARTBEAT GATEWAY (non-WMI) %s ===" % datetime.datetime.now().isoformat(timespec="seconds"))
fresh_wajib, stale_wajib, fresh_other = [], [], []
for p in live:
    f = hb_path(p)
    if not os.path.exists(f):
        print("  %-22s TIDAK-ADA-BERKAS" % p)
        if p in wajib:
            stale_wajib.append(p)
        continue
    age = now - os.path.getmtime(f)
    raw = open(f, encoding="utf-8", errors="replace").read().strip()[:120].replace("\n", " ")
    tag = "FRESH" if age < 180 else ("AGING" if age < 900 else "STALE")
    print("  %-22s age=%8.0fs %-5s | %s" % (p, age, tag, raw))
    if p in wajib:
        (fresh_wajib if age < 180 else stale_wajib).append(p)
    elif age < 180:
        fresh_other.append(p)

print("--- vonis ---")
print("  WAJIB fresh(<180dtk): %d/%d %s" % (len(fresh_wajib), len(wajib), fresh_wajib))
if stale_wajib:
    print("  WAJIB TIDAK FRESH : %s" % stale_wajib)
print("  luar-wajib fresh    : %d profil %s" % (len(fresh_other), fresh_other))
