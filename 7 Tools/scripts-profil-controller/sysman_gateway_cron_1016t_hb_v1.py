# Ronde cron sysman 16-10: saksi kesegaran heartbeat non-WMI utk 3 gateway wajib
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
now = time.time()
print("registri hidup:", len(REG["hidup"]), "| wajib:", REG["gateway_wajib_hidup"])
for p in REG["gateway_wajib_hidup"]:
    # PITFALL 15-10: profil `default` home = ROOT hermes, bukan profiles/default
    cands = [os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat"),
             os.path.join(HOME, "state", "gateway.heartbeat")] if p == "default" else \
            [os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")]
    found = False
    for hb in cands:
        if os.path.exists(hb):
            raw = open(hb, encoding="utf-8", errors="replace").read().strip()
            age = now - os.path.getmtime(hb)
            print(f"  {p:22s} heartbeat umur={age:7.1f}s isi={raw[:80]!r}")
            found = True
            break
    if not found:
        print(f"  {p:22s} TIDAK ADA BERKAS heartbeat")
