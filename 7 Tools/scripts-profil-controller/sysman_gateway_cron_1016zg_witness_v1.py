# Ronde 16-10 zg: saksi non-WMI (heartbeat) + audit login item autostart vs registri
import json, os, time, datetime, subprocess

HOME = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
REG = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
wajib = ["gsp-thinker", "gsp-worker", "gsp-worker-fast"]
hidup = json.load(open(REG, encoding="utf-8"))["hidup"]

def hb_path(p):
    # PITFALL 15-10 malam: home profil 'default' = ROOT hermes, bukan profiles/default
    return os.path.join(HOME if p == "default" else os.path.join(HOME, "profiles", p),
                        "state", "gateway.heartbeat")

now = time.time()
print("--- heartbeat wajib (saksi non-WMI) ---")
for p in wajib:
    f = hb_path(p)
    if not os.path.exists(f):
        print(f"  {p:20s} TIDAK-ADA-BERKAS")
        continue
    raw = open(f, encoding="utf-8", errors="replace").read().strip()
    age = now - os.path.getmtime(f)
    print(f"  {p:20s} umur={age:7.1f}s  isi={raw[:90]!r}")

print("--- heartbeat semua profil hidup yang punya berkas ---")
for p in hidup:
    f = hb_path(p)
    if os.path.exists(f):
        age = now - os.path.getmtime(f)
        flag = "SEGAR" if age < 180 else ("BASI" if age < 3600 else "MATI?")
        print(f"  {p:20s} umur={age:9.1f}s {flag}")
    else:
        print(f"  {p:20s} (tanpa berkas heartbeat)")

print("--- login item autostart (VBS Startup) vs registri ---")
startup = os.path.expandvars(r"C:/Users/TRIAL/AppData/Roaming/Microsoft/Windows/Start Menu/Programs/Startup")
vbs = sorted(f for f in os.listdir(startup) if f.lower().endswith(".vbs"))
live_l = {h.lower() for h in hidup}
for v in vbs:
    txt = open(os.path.join(startup, v), encoding="utf-8", errors="replace").read().lower()
    hit = [h for h in hidup if h.lower() in txt]
    toks = txt.replace('"', " ").replace("/", " ").replace("\\", " ").split()
    outside = sorted({t for t in toks if t.startswith("gsp-") and t not in live_l and t != "gsp-hermes"})
    print(f"  {v:46s} rujukan_hidup={hit if hit else '-'} token_luar={sorted(set(outside)) if outside else '-'}")
print(f"  total VBS aktif = {len(vbs)}")
