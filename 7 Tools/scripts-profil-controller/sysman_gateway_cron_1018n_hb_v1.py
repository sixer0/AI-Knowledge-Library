# Saksi kesegaran gateway tanpa WMI: baca state/gateway.heartbeat per profil
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
live = REG["hidup"]
wajib = REG["gateway_wajib_hidup"]
now = time.time()

def hb_path(p):
    # profil `default` ber-home di ROOT hermes
    if p == "default":
        return os.path.join(HOME, "state", "gateway.heartbeat")
    return os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")

rows = []
for p in live:
    f = hb_path(p)
    if not os.path.exists(f):
        rows.append((p, "TIDAK-ADA-BERKAS", None, None))
        continue
    age = now - os.path.getmtime(f)
    pid = "?"
    try:
        d = json.load(open(f, encoding="utf-8"))
        pid = d.get("pid", d.get("Pid", "?"))
    except Exception as e:
        pid = "PARSE-GALAT"
    rows.append((p, f"{age/60:.1f} mnt", pid, age))

print("=== SAKSI HEARTBEAT (non-WMI) %s ===" % datetime.datetime.now().isoformat(timespec="seconds"))
fresh_wajib = 0
for p, age, pid, raw in sorted(rows, key=lambda r: (r[3] is None, r[3] or 0)):
    mark = "WAJIB" if p in wajib else "     "
    print(f"  {mark} {p:22s} umur={age} pid={pid}")
    if p in wajib and raw is not None and raw < 300:
        fresh_wajib += 1
print(f"WAJIB fresh(<5m) = {fresh_wajib}/3")
