# COMPACTCFG-0930 verifikasi: (1) diff per berkas vs backup = hanya kunci sasaran;
# (2) load_config engine per home -> threshold & target_ratio efektif 0.8/0.25;
# (3) idempotensi skrip. Cetak CHECK n + VERDICT.
import os, sys, subprocess, difflib, json

HOME = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
BAK = ".bak-compactcfg-20260930"
SCRIPT = r"C:/Users/TRIAL/workspace/gsp-hermes/scripts/rollout_compaction_0930_v3.py"
sys.path.insert(0, os.path.join(HOME, "hermes-agent"))

targets = [os.path.join(HOME, "config.yaml")]
pdir = os.path.join(HOME, "profiles")
for name in sorted(os.listdir(pdir)):
    cfg = os.path.join(pdir, name, "config.yaml")
    if os.path.isfile(cfg):
        targets.append(cfg)

ALLOWED = ("threshold:", "target_ratio:", "compression:")
fails = []

# CHECK 1: diff baris vs backup (EOL dinormalisasi; baris kosong imbang diabaikan)
bad_diff = []
for path in targets:
    rel = os.path.relpath(path, HOME).replace("\\", "/")
    a = [l for l in open(path + BAK, encoding="utf-8").read().splitlines() if l.strip()]
    b = [l for l in open(path, encoding="utf-8").read().splitlines() if l.strip()]
    for line in difflib.unified_diff(a, b, lineterm="", n=0):
        if line.startswith(("+", "-")) and not line.startswith(("+++", "---")):
            body = line[1:].strip()
            if not any(body.startswith(k) or body == k.rstrip(":") for k in ALLOWED):
                bad_diff.append(f"{rel}: {line[:90]}")
if bad_diff:
    fails.append("CHECK 1: ada baris berubah di luar kunci sasaran")
print(f"CHECK 1: {'PASS' if not bad_diff else 'FAIL'} - diff vs backup hanya kunci sasaran ({len(targets)} berkas, selisih tak-sasaran={len(bad_diff)})")
for x in bad_diff[:10]:
    print("   ", x)

# CHECK 2: nilai efektif via loader engine (baca teks + parse YAML, root merge default)
from hermes_cli.config import load_config  # noqa: E402
import hermes_cli.config as cfgmod  # noqa: E402

vals = {}
os.environ["HERMES_HOME"] = HOME
cfgmod._LOAD_CONFIG_CACHE.clear()
c = load_config()
vals["<root>"] = (c["compression"]["threshold"], c["compression"]["target_ratio"])
for path in targets[1:]:
    home = os.path.dirname(path)
    name = os.path.basename(home)
    os.environ["HERMES_HOME"] = home
    cfgmod._LOAD_CONFIG_CACHE.clear()
    c = load_config()
    comp = c.get("compression", {})
    vals[name] = (comp.get("threshold"), comp.get("target_ratio"))

bad_val = {k: v for k, v in vals.items() if (v[0], v[1]) != (0.8, 0.25)}
print(f"CHECK 2: {'PASS' if not bad_val else 'FAIL'} - load_config engine: threshold=0.8 target_ratio=0.25 pada {len(vals)-len(bad_val)}/{len(vals)} home")
for k, v in list(bad_val.items())[:10]:
    print("   ", k, v)
if bad_val:
    fails.append("CHECK 2: nilai efektif menyimpang")

# CHECK 3: idempotensi (dry-run kedua harus unchanged=57)
r = subprocess.run(["uv", "run", "--python", "3.11", "python", SCRIPT],
                   capture_output=True, text=True, cwd=os.path.join(HOME, "hermes-agent"))
last = r.stdout.strip().splitlines()[-1] if r.stdout.strip() else ""
idem = "unchanged=57" in last and "errors=0" in last
print(f"CHECK 3: {'PASS' if idem else 'FAIL'} - idempoten (dry-run ulang: {last})")
if not idem:
    fails.append("CHECK 3: tidak idempoten")

# CHECK 4: YAML masih parse + kunci lain utuh (jumlah top-level keys sama dgn backup)
import yaml as pyyaml  # noqa: E402
bad_keys = []
for path in targets:
    rel = os.path.relpath(path, HOME).replace("\\", "/")
    try:
        new = pyyaml.safe_load(open(path, encoding="utf-8"))
        old = pyyaml.safe_load(open(path + BAK, encoding="utf-8"))
    except Exception as e:
        bad_keys.append(f"{rel}: parse error {e}")
        continue
    ko, kn = set(old or {}), set(new or {})
    if ko - kn:
        bad_keys.append(f"{rel}: kunci hilang {sorted(ko-kn)}")
    extra = kn - ko
    if extra and extra != {"compression"}:
        bad_keys.append(f"{rel}: kunci baru tak terduga {sorted(extra)}")
    for k in ko & kn:
        if k == "compression":
            continue
        if old[k] != new[k]:
            bad_keys.append(f"{rel}: nilai '{k}' berubah")
print(f"CHECK 4: {'PASS' if not bad_keys else 'FAIL'} - semantik YAML: kunci & nilai non-sasaran identik backup")
for x in bad_keys[:10]:
    print("   ", x)
if bad_keys:
    fails.append("CHECK 4: perubahan di luar sasaran")

print("VERDICT:", "FAIL" if fails else "PASS")
sys.exit(1 if fails else 0)
