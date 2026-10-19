# Read-only ronde penjaga gateway: umur heartbeat per profil (saksi non-WMI) + daftar hidup registri.
import json
import os
import time
from datetime import datetime, timezone

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
WS = "C:/Users/TRIAL/workspace/gsp-hermes/workspace"
REG = os.path.join(WS, "fleet", "PROFILE-REGISTRY.json")
now = time.time()

with open(REG, encoding="utf-8") as f:
    reg = json.load(f)
live = set(reg["hidup"])
wajib = set(reg["gateway_wajib_hidup"])
print("registri: hidup=%d wajib=%d -> %s" % (len(live), len(wajib), ",".join(sorted(wajib))))


def hb_age(path):
    try:
        raw = open(path, encoding="utf-8", errors="replace").read().strip()
    except OSError:
        return None, None
    age = now - os.path.getmtime(path)
    pid = None
    try:
        data = json.loads(raw)
        if isinstance(data, dict):
            pid = data.get("pid") or data.get("Pid") or data.get("PID")
    except Exception:
        pass
    return age, pid


rows = []
prof_root = os.path.join(HOME, "profiles")
for name in sorted(os.listdir(prof_root)):
    p = os.path.join(prof_root, name, "state", "gateway.heartbeat")
    if os.path.isfile(p):
        rows.append((name, hb_age(p)))
# profil default: home = ROOT hermes
p = os.path.join(HOME, "state", "gateway.heartbeat")
if os.path.isfile(p):
    rows.append(("default", hb_age(p)))

FRESH = 180
print("\n%-26s %10s %-6s %-6s %s" % ("profil", "umur_dtk", "fresh", "hidup", "pid"))
fresh_set = set()
ghost = []
for name, (age, pid) in rows:
    fresh = age is not None and age < FRESH
    if fresh:
        fresh_set.add(name)
    if fresh and name not in live:
        ghost.append(name)
    print("%-26s %10s %-6s %-6s %s"
          % (name, ("%.0f" % age) if age is not None else "NA",
             "Y" if fresh else "n", "Y" if name in live else "n", pid))

print("\nFRESH(<%ds)=%d -> %s" % (FRESH, len(fresh_set), ",".join(sorted(fresh_set)) or "-"))
missing = wajib - fresh_set
print("WAJIB tanpa heartbeat fresh: %s" % (",".join(sorted(missing)) or "NONE"))
print("HANTU (heartbeat fresh tapi di luar daftar hidup): %s" % (",".join(sorted(ghost)) or "NONE"))
print("DI DAFTAR HIDUP tanpa heartbeat fresh: %s"
      % (",".join(sorted(live - fresh_set)) or "-"))
print("now_utc=%s" % datetime.now(timezone.utc).isoformat(timespec="seconds"))
