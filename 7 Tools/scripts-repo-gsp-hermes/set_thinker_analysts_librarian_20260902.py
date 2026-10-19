# -*- coding: utf-8 -*-
"""
Set default model = GSP-AI / thinker untuk fleet thinker profiles
(keputusan user 02-09-2026): semua gsp-*-analyst + gsp-librarian.

Idempoten. Sequential (PITFALL 27-08: jangan pernah hermes config set paralel).
Backup config.yaml sebelum sentuh; verifikasi dengan re-read file.
"""
import os, subprocess, sys, shutil, datetime

try:
    import yaml
except ImportError:
    sys.exit("PyYAML missing - jalankan: uv run --with pyyaml python <script>")

PROFILES_BASE = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
BACKUP_ROOT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace_backups/2026-09-02-thinker-analyst-librarian"
TARGET_MODEL = "thinker"
TARGET_PROVIDER = "GSP-AI"

TARGETS = [
    "gsp-data-analyst",
    "gsp-document-analyst",
    "gsp-engineering-analyst",
    "gsp-image-analyst",
    "gsp-pm-analyst",
    "gsp-social-media-analyst",
    "gsp-librarian",
]

def cfg_path(p): return os.path.join(PROFILES_BASE, p, "config.yaml")

def read_model(p):
    with open(cfg_path(p), encoding="utf-8") as f:
        c = yaml.safe_load(f)
    m = c.get("model") or {}
    return m.get("default"), m.get("provider")

results = []
os.makedirs(BACKUP_ROOT, exist_ok=True)

for p in TARGETS:
    path = cfg_path(p)
    if not os.path.exists(path):
        results.append((p, "-", "-", "MISSING config.yaml"))
        continue
    before_def, before_prov = read_model(p)
    if before_def == TARGET_MODEL and before_prov == TARGET_PROVIDER:
        results.append((p, f"{before_prov}/{before_def}", "unchanged", "IDEMPOTEN-SKIP"))
        continue
    # backup
    shutil.copy2(path, os.path.join(BACKUP_ROOT, f"{p}.config.yaml"))
    # sequential hermes config set (official path, never hand-edit)
    r = subprocess.run(
        ["hermes", "-p", p, "config", "set", f"model.default", TARGET_MODEL],
        capture_output=True, text=True, timeout=120, shell=(os.name == "nt"),
    )
    if r.returncode != 0:
        results.append((p, f"{before_prov}/{before_def}", "ERR", (r.stderr or r.stdout)[:200]))
        continue
    # verify by re-parse (bukan percaya exit code)
    after_def, after_prov = read_model(p)
    # cek tidak ada junk top-level (corruption pattern 27-08)
    with open(path, encoding="utf-8") as f:
        c = yaml.safe_load(f)
    junk = [k for k in c.keys() if k in ("default", "provider", "base_url", "api_key")]
    ok = (after_def == TARGET_MODEL and after_prov == TARGET_PROVIDER and not junk)
    results.append((p, f"{before_prov}/{before_def}", f"{after_prov}/{after_def}",
                    "OK" if ok else f"CHECK! junk_top_level={junk}"))

print(f"{'PROFILE':<28} {'BEFORE':<22} {'AFTER':<22} STATUS")
for row in results:
    print(f"{row[0]:<28} {str(row[1]):<22} {str(row[2]):<22} {row[3]}")

fails = [r for r in results if r[3] not in ("OK", "IDEMPOTEN-SKIP")]
print("\nBACKUP:", BACKUP_ROOT)
print("RESULT:", "ALL PASS" if not fails else f"{len(fails)} FAILED")
sys.exit(1 if fails else 0)
