# Saksi kesegaran gateway non-WMI: baca state/gateway.heartbeat per profil (read-only)
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"

live = json.load(open(REG, encoding="utf-8"))["hidup"]
wajib = ["gsp-thinker", "gsp-worker", "gsp-worker-fast"]
now = time.time()


def hb_path(p):
    # profil `default` ber-home di ROOT hermes
    if p == "default":
        return os.path.join(HOME, "state", "gateway.heartbeat")
    return os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")


print("=== HEARTBEAT GATEWAY (saksi non-WMI) %s ===" % datetime.datetime.now().isoformat(timespec="seconds"))
for p in live:
    f = hb_path(p)
    if not os.path.exists(f):
        print("  %-22s TIDAK-ADA-BERKAS" % p)
        continue
    age = now - os.path.getmtime(f)
    raw = open(f, encoding="utf-8", errors="replace").read().strip()[:120].replace("\n", " ")
    tag = "WAJIB" if p in wajib else "     "
    print("  %-22s %s umur=%6.0fs  %s" % (p, tag, age, raw))
