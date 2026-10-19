# Read-only witness: gateway heartbeat freshness per profile, NO WMI.
# Pitfall guard: profile `default` home = ROOT hermes, not profiles/default/.
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
now = time.time()

live = json.load(open(REG, encoding="utf-8"))["hidup"]
wajib = json.load(open(REG, encoding="utf-8"))["gateway_wajib_hidup"]

def hb_path(p):
    return (os.path.join(HOME, "state", "gateway.heartbeat") if p == "default"
            else os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat"))

print("=== HEARTBEAT WITNESS (no WMI) ===")
rows = []
for p in live:
    f = hb_path(p)
    if not os.path.exists(f):
        rows.append((p, None, None, "NO-FILE"))
        continue
    age = now - os.path.getmtime(f)
    pid = ""
    try:
        txt = open(f, encoding="utf-8", errors="replace").read().strip()
        pid = txt.replace("\n", "|")[:60]
    except Exception as e:
        pid = "ERR:%s" % e
    rows.append((p, age, datetime.datetime.utcfromtimestamp(os.path.getmtime(f)).strftime("%m-%d %H:%M"), pid))

for p, age, ts, pid in sorted(rows, key=lambda r: (r[1] is None, r[1] or 0)):
    tag = "WAJIB" if p in wajib else "     "
    ages = ("%8.0fs" % age) if age is not None else "     n/a"
    fresh = ""
    if age is not None:
        fresh = "FRESH<180s" if age < 180 else ("STALE" if age < 3600 else "VERY-STALE")
    print("%s %-20s %s %-12s %-18s %s" % (tag, p, ages, fresh, ts or "-", pid))

print("\nwaived-check: wajib set =", wajib)
print("count live profiles =", len(live))
