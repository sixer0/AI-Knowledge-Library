# Hitung ulang berkas peluncur arsipan di folder Startup (read-only)
import os
startup = os.path.join(os.environ["APPDATA"], "Microsoft", "Windows",
                       "Start Menu", "Programs", "Startup")
allh = [f for f in os.listdir(startup) if f.lower().startswith("hermes_gateway")]
dis = [f for f in allh if ".disabled-" in f]
act = [f for f in allh if ".disabled-" not in f]
print("total hermes_gateway*:", len(allh), "| aktif:", len(act), "| arsipan .disabled:", len(dis))
