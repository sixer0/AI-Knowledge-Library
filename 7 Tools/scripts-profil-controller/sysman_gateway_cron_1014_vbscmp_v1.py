# Read-only: bandingkan VBS autostart aktif vs registri hidup (sysman cron 14-10)
import json, os, re

startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows",
                       "Start Menu", "Programs", "Startup")
reg = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json",
                     encoding="utf-8"))
live = set(reg["hidup"])
wajib = reg["gateway_wajib_hidup"]

active, disabled = [], 0
for fn in sorted(os.listdir(startup)):
    low = fn.lower()
    if not low.startswith("hermes_gateway") or not low.endswith(".vbs"):
        continue
    if ".disabled-" in fn:
        disabled += 1
        continue
    m = re.match(r"Hermes_Gateway_(.+)\.vbs$", fn, re.IGNORECASE)
    active.append(m.group(1) if m else "(entri-umum:" + fn + ")")

profiles = [a for a in active if not a.startswith("(entri-umum")]
out = [p for p in profiles if p not in live]
print("VBS aktif:", len(active), "| entri arsip .disabled:", disabled)
print("profil ber-VBS :", sorted(profiles))
print("VBS di luar daftar hidup:", out if out else "(kosong)")
missing = [w for w in wajib if w not in profiles]
print("WAJIB tanpa VBS autostart:", missing if missing else "(kosong)")
