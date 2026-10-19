# Sysman cron 15-10: ukur umur log gateway tiga profil wajib (read-only, tanpa psutil).
import os, time, json

REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
BASE = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
now = time.time()
with open(REG, encoding="utf-8") as f:
    reg = json.load(f)
wajib = reg["gateway_wajib_hidup"]
print("wajib:", wajib)
for p in wajib:
    lp = os.path.join(BASE, p, "logs", "gateway.log")
    if not os.path.exists(lp):
        # coba lokasi alternatif
        for cand in (os.path.join(BASE, p, "gateway.log"),
                     os.path.join(BASE, p, "logs", "gateway", "gateway.log")):
            if os.path.exists(cand):
                lp = cand
                break
    if not os.path.exists(lp):
        print(f"  {p:20s} LOG-TIDAK-DITEMUKAN")
        continue
    age_min = (now - os.path.getmtime(lp)) / 60.0
    size = os.path.getsize(lp)
    print(f"  {p:20s} log={lp.replace(BASE,'~')} umur={age_min:.0f}mnt ukuran={size}B")
