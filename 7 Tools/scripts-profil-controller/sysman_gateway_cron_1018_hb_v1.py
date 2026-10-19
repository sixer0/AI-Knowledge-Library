# Saksi kesegaran heartbeat gateway (non-WMI) + cek hantu registri, ronde cron 18-10.
import json, os, time

HERMES = "C:/Users/TRIAL/AppData/Local/hermes"
REG = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
live = json.load(open(REG, encoding="utf-8"))
wajib = live["gateway_wajib_hidup"]
hidup = set(live["hidup"])
now = time.time()

def hb_age(profile):
    # PITFALL 15-10 malam: home profil default = ROOT hermes, bukan profiles/default
    if profile == "default":
        p = os.path.join(HERMES, "state", "gateway.heartbeat")
    else:
        p = os.path.join(HERMES, "profiles", profile, "state", "gateway.heartbeat")
    if not os.path.exists(p):
        return None
    return now - os.path.getmtime(p)

print("=== HEARTBEAT WITNESS (non-WMI) ===")
for prof in wajib:
    a = hb_age(prof)
    print(f"  WAJIB {prof:<16} heartbeat={'TIDAK-ADA-BERKAS' if a is None else f'{a:.0f}s'}")

print("--- profil hidup lain (informasi; bukan set gateway wajib) ---")
for prof in sorted(hidup - set(wajib)):
    a = hb_age(prof)
    print(f"  {prof:<20} heartbeat={'TIDAK-ADA-BERKAS' if a is None else f'{a:.0f}s'}")

# Hantu: folder profil yang punya heartbeat segar (<180s) tapi tidak ada di daftar hidup
print("--- cek hantu: heartbeat segar pada profil di luar daftar hidup ---")
ghosts = []
proot = os.path.join(HERMES, "profiles")
for name in sorted(os.listdir(proot)):
    if name in hidup or ".disabled-" in name or not os.path.isdir(os.path.join(proot, name)):
        continue
    a = hb_age(name)
    if a is not None and a < 180:
        ghosts.append((name, a))
if ghosts:
    for name, a in ghosts:
        print(f"  HANTU: {name} heartbeat {a:.0f}s (di luar registri!)")
else:
    print("  (nol hantu)")
print("SELESAI")
