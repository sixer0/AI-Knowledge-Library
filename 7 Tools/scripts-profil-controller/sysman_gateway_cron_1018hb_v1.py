# Saksi non-WMI: umur heartbeat gateway per profil (read-only, tanpa CIM)
import json, os, time, datetime

HOME = "C:/Users/TRIAL/AppData/Local/hermes"
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
live = REG["hidup"]
wajib = REG["gateway_wajib_hidup"]
now = time.time()

def hb_path(p):
    # profil `default`: home = ROOT hermes, bukan profiles/default
    if p == "default":
        return os.path.join(HOME, "state", "gateway.heartbeat")
    return os.path.join(HOME, "profiles", p, "state", "gateway.heartbeat")

print("SET WAJIB:", wajib)
for p in wajib:
    f = hb_path(p)
    if not os.path.exists(f):
        print(f"  {p}: TIDAK-ADA-BERKAS")
        continue
    age = now - os.path.getmtime(f)
    raw = open(f, encoding="utf-8", errors="replace").read().strip()[:200]
    print(f"  {p}: heartbeat_age={age:.0f}s raw={raw}")

print("SEMUA PROFIL HIDUP (cek gateway tak terduga):")
for p in live:
    f = hb_path(p)
    if os.path.exists(f):
        age = now - os.path.getmtime(f)
        print(f"  {p}: age={age:.0f}s ({age/3600:.1f}h)")
    else:
        print(f"  {p}: tidak ada berkas heartbeat")

# profil di disk yang TIDAK ada di registri hidup (calon hantu)
prof_dir = os.path.join(HOME, "profiles")
on_disk = sorted(d for d in os.listdir(prof_dir) if os.path.isdir(os.path.join(prof_dir, d)) and not d.endswith(".disabled-2026-10-10"))
extra = [d for d in on_disk if d not in live]
print(f"PROFIL DI DISK: {len(on_disk)} | DI LUAR REGISTRI HIDUP: {len(extra)}")
for d in extra:
    f = hb_path(d)
    age = (now - os.path.getmtime(f)) if os.path.exists(f) else None
    print(f"  luar-registri: {d} hb={'-' if age is None else format(age,'.0f')+'s'}")
