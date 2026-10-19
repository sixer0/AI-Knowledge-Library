# Saksi (b): kesegaran heartbeat gateway per profil vs daftar hidup registri.
import os, time, json, glob
now = int(time.time())
root = "C:/Users/TRIAL/AppData/Local/hermes"
paths = [root + "/state/gateway.heartbeat"] + sorted(glob.glob(root + "/profiles/*/state/gateway.heartbeat"))
fresh = []
stale = []
for p in paths:
    n = p.replace("\\", "/")
    prof = "default" if "/profiles/" not in n else n.split("/profiles/")[1].split("/")[0]
    try:
        mt = os.path.getmtime(p)
        age = round((now - mt) / 60.0, 1)
        (fresh if age < 5 else stale).append((prof, age))
    except OSError:
        stale.append((prof, "NOFILE"))
print("fresh(<5m) =", len(fresh))
for f_ in fresh: print("  ", f_)
print("stale/nofile =", len(stale))
for s in stale: print("  ", s)
