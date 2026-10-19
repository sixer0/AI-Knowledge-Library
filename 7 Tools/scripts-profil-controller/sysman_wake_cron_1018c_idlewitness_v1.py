# Saksi idle sehat 18-10c: mtime cron/output terbaru + heartbeat gateway vs set WAJIB monitor
import os, time, glob, json

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
now = time.time()

print("-- cron output terbaru per job (mtime menit) --")
rows = []
for d in glob.glob(os.path.join(HOME, "profiles", "*", "cron", "output", "*")) + \
         glob.glob(os.path.join(HOME, "cron", "output", "*")):
    prof = d.split(os.sep)
    try:
        files = [f for f in glob.glob(os.path.join(d, "*")) if os.path.isfile(f)]
    except OSError:
        continue
    if not files:
        continue
    newest = max(files, key=os.path.getmtime)
    rows.append(((now - os.path.getmtime(newest)) / 60.0, "/".join(prof[-5:-3]), os.path.basename(newest)))
rows.sort()
for age, job, fn in rows[:12]:
    print(f"{age:8.1f} min  {job}  {fn}")

print("\n-- heartbeat gateway per profil --")
reg = None
regp = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
if os.path.exists(regp):
    try:
        reg = json.load(open(regp, encoding="utf-8"))
    except Exception as e:
        print("registry read err:", e)
print("registry keys:", (list(reg.keys()) if isinstance(reg, dict) else type(reg).__name__) if reg else "NONE")

hb = []
for base in (os.path.join(HOME, "profiles"), HOME):
    for p in sorted(glob.glob(os.path.join(base, "*", "state", "gateway.heartbeat"))) + \
             ([os.path.join(HOME, "state", "gateway.heartbeat")] if base == HOME else []):
        try:
            age = (now - os.path.getmtime(p)) / 60.0
        except OSError:
            continue
        name = p.split(os.sep)[-3] if "profiles" in p else "default"
        hb.append((age, name))
seen = {}
for age, name in hb:
    if name not in seen or age < seen[name]:
        seen[name] = age
for name, age in sorted(seen.items(), key=lambda kv: kv[1]):
    print(f"{name:28s} hb_age={age:9.1f} min")
con.close() if False else None
