# Rollout COMPACTCFG-0930: standarisasi prosedur compaction memori fleet.
# Set compression.threshold=0.8 + compression.target_ratio=0.25 pada root config
# + 56 profil (hermes-home aktif), idempoten, komentar terjaga (ruamel round-trip),
# backup .bak-compactcfg-20260930 per berkas. Dry-run default; --apply untuk menulis.
import sys, os, shutil, json
from ruamel.yaml import YAML

THRESHOLD = 0.8
TARGET_RATIO = 0.25
HOME = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
BACKUP_SUFFIX = ".bak-compactcfg-20260930"

targets = [os.path.join(HOME, "config.yaml")]
pdir = os.path.join(HOME, "profiles")
for name in sorted(os.listdir(pdir)):
    cfg = os.path.join(pdir, name, "config.yaml")
    if os.path.isfile(cfg):
        targets.append(cfg)

apply = "--apply" in sys.argv
yaml = YAML()
yaml.preserve_quotes = True
yaml.width = 4096

report = {"total": len(targets), "changed": 0, "already": 0, "no_file": 0, "errors": []}
rows = []
for path in targets:
    rel = os.path.relpath(path, HOME).replace("\\", "/")
    try:
        with open(path, encoding="utf-8") as f:
            data = yaml.load(f) or {}
        if not isinstance(data, dict):
            raise ValueError("root bukan mapping")
        comp = data.get("compression")
        had_block = isinstance(comp, dict)
        if not had_block:
            comp = {}
        old_t = comp.get("threshold", None)
        old_r = comp.get("target_ratio", None)
        if float(old_t or -1) == THRESHOLD and float(old_r or -1) == TARGET_RATIO:
            rows.append((rel, old_t, old_r, "already"))
            report["already"] += 1
            continue
        comp["threshold"] = THRESHOLD
        comp["target_ratio"] = TARGET_RATIO
        data["compression"] = comp
        if apply:
            bak = path + BACKUP_SUFFIX
            if not os.path.exists(bak):
                shutil.copy2(path, bak)
            tmp = path + ".tmp-compactcfg"
            with open(tmp, "w", encoding="utf-8", newline="\n") as f:
                yaml.dump(data, f)
            os.replace(tmp, path)
        rows.append((rel, old_t, old_r, "changed" + ("" if had_block else " (blok baru)")))
        report["changed"] += 1
    except Exception as e:
        report["errors"].append(f"{rel}: {e}")
        rows.append((rel, "-", "-", f"ERROR {e}"))

for rel, a, b, st in rows:
    print(f"{rel} | threshold={a} target_ratio={b} -> {st}")
print("MODE:", "APPLY" if apply else "DRY-RUN")
print(json.dumps(report))
