# COMPACTCFG-0930 v3: suntingan tekstual minimal, EOL-safe (CRLF/LF per berkas),
# idempoten, tanpa baris hiasan. Set compression.threshold / target_ratio.
import sys, os

THRESHOLD = "0.8"
TARGET_RATIO = "0.25"
HOME = os.path.expandvars(r"C:/Users/TRIAL/AppData/Local/hermes")
BAK = ".bak-compactcfg-20260930"

targets = [os.path.join(HOME, "config.yaml")]
pdir = os.path.join(HOME, "profiles")
for name in sorted(os.listdir(pdir)):
    cfg = os.path.join(pdir, name, "config.yaml")
    if os.path.isfile(cfg):
        targets.append(cfg)

if "--restore" in sys.argv:
    n = 0
    for path in targets:
        bak = path + BAK
        if os.path.exists(bak):
            with open(bak, "rb") as s, open(path, "wb") as d:
                d.write(s.read())
            n += 1
    print(f"restored {n}/{len(targets)}")
    sys.exit(0)

apply = "--apply" in sys.argv
changed = unchanged = errors = 0
detail = []
for path in targets:
    rel = os.path.relpath(path, HOME).replace("\\", "/")
    try:
        raw = open(path, encoding="utf-8", newline="").read()
        # pisahkan terminator tiap baris, simpan persis
        lines = raw.splitlines(keepends=True)
        ci = None
        for i, l in enumerate(lines):
            if l.rstrip("\r\n") == "compression:":
                ci = i
                break
        if ci is None:
            eol = "\r\n" if any(l.endswith("\r\n") for l in lines) else "\n"
            if lines and not lines[-1].endswith(("\n",)):
                lines[-1] = lines[-1] + eol
            lines.append(f"compression:{eol}")
            lines.append(f"  threshold: {THRESHOLD}{eol}")
            lines.append(f"  target_ratio: {TARGET_RATIO}{eol}")
            status = "blok baru"
        else:
            end = len(lines)
            for j in range(ci + 1, len(lines)):
                s = lines[j].rstrip("\r\n")
                if s and not s[0].isspace() and not s.lstrip().startswith("#"):
                    end = j
                    break
            eol = "\r\n" if lines[ci].endswith("\r\n") else "\n"
            got_t = got_r = False
            for j in range(ci + 1, end):
                body = lines[j].strip()
                if body.startswith("threshold:"):
                    indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
                    lines[j] = f"{indent}threshold: {THRESHOLD}{eol}"
                    got_t = True
                elif body.startswith("target_ratio:"):
                    indent = lines[j][: len(lines[j]) - len(lines[j].lstrip())]
                    lines[j] = f"{indent}target_ratio: {TARGET_RATIO}{eol}"
                    got_r = True
            ins = []
            if not got_t:
                ins.append(f"  threshold: {THRESHOLD}{eol}")
            if not got_r:
                ins.append(f"  target_ratio: {TARGET_RATIO}{eol}")
            lines[ci + 1 : ci + 1] = ins
            status = "blok existing"
        new_raw = "".join(lines)
        if new_raw == raw:
            unchanged += 1
            continue
        changed += 1
        if apply:
            bak = path + BAK
            if not os.path.exists(bak):
                import shutil
                shutil.copy2(path, bak)
            with open(path, "wb") as f:
                f.write(new_raw.encode("utf-8"))
        detail.append(f"{rel} ({status})")
    except Exception as e:
        errors += 1
        detail.append(f"{rel} ERROR {e}")

for d in detail[:5]:
    print("  ", d)
print(f"MODE={'APPLY' if apply else 'DRY-RUN'} changed={changed} unchanged={unchanged} errors={errors} total={len(targets)}")
