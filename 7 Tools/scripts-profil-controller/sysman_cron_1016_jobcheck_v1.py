# Read-only: status job cron penjaga gateway milik profil sysman + umur output terakhir.
import json, os, time, glob

P = "C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-system-manager/cron/jobs.json"
d = json.load(open(P, encoding="utf-8"))
jobs = d if isinstance(d, list) else d.get("jobs", d)
rows = jobs if isinstance(jobs, list) else list(jobs.values())
print("=== JOB CRON PENJAGA GATEWAY (profil gsp-system-manager) ===")
for j in rows:
    if not isinstance(j, dict):
        continue
    blob = json.dumps(j).lower()
    if "gateway" not in blob:
        continue
    print("  id=%s name=%s enabled=%s schedule=%s" % (
        j.get("id"), j.get("name"), j.get("enabled", j.get("status")),
        j.get("schedule") or j.get("cron")))
    print("     next=%s last=%s last_status=%s" % (
        j.get("next_run_at"), j.get("last_run_at"), j.get("last_status")))

print("=== OUTPUT SIKLUS TERAKHIR ===")
fs = sorted(glob.glob("C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-system-manager/cron/output/*/*.md"))
byjob = {}
for f in fs:
    byjob.setdefault(os.path.dirname(f), []).append(f)
for folder, files in sorted(byjob.items()):
    files = sorted(files)[-2:]
    print("-- job dir:", os.path.basename(folder))
    for f in files:
        body = open(f, encoding="utf-8", errors="replace").read().strip()
        print("   %s  bytes=%d  isi=%.160s" % (
            os.path.basename(f), len(body), body.replace("\n", " | ")))
