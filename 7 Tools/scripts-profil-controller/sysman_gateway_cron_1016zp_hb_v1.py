# Saksi kesegaran heartbeat gateway (non-WMI) - ronde cron sysman 16-10
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
live = set(REG["hidup"])
wajib = REG["gateway_wajib_hidup"]

now = time.time()
print("registri hidup:", len(live), "| wajib:", wajib)
for p in wajib:
    # PITFALL default: home = ROOT hermes, bukan profiles/default
    hb = os.path.join(HOME, "state", "gateway.heartbeat") if p == "default" \
        else os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print(f"  {p:20s} TIDAK-ADA-BERKAS {hb}")
        continue
    age = now - os.path.getmtime(hb)
    try:
        data = json.load(open(hb, encoding="utf-8"))
    except Exception as e:
        data = {"err": str(e)}
    print(f"  {p:20s} umur={age:7.0f}s pid={data.get('pid')} ts={data.get('updated_at')}")

# sensus profil ber-heartbeat segar di seluruh disk -> bandingkan registri
fresh = []
pdir = os.path.join(HOME, "profiles")
for p in sorted(os.listdir(pdir)):
    hb = os.path.join(pdir, p, "state", "gateway.heartbeat")
    if os.path.exists(hb) and (now - os.path.getmtime(hb)) < 180:
        fresh.append(p)
if os.path.exists(os.path.join(HOME, "state", "gateway.heartbeat")) and \
   (now - os.path.getmtime(os.path.join(HOME, "state", "gateway.heartbeat"))) < 180:
    fresh.append("default")
print("heartbeat segar (<180s):", fresh)
luar = [p for p in fresh if p not in live]
print("DI-LUAR-REGISTRI:", luar if luar else "TIDAK ADA")
