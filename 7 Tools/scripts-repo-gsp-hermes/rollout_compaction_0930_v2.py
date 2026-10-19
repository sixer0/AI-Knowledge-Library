# COMPACTCFG-0930 v2: suntingan tekstual minimal (bukan round-trip YAML) supaya
# hanya dua kunci sasaran yang berubah byte; sisa berkas identik.
# Mode: --restore (pulihkan dari backup) | --apply | default dry-run
import sys, os, glob

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
            data = open(bak, "rb").read()
            with open(path, "wb") as f:
                f.write(data)
            n += 1
    print(f"restored {n}/{len(targets)} dari backup")
    sys.exit(0)

apply = "--apply" in sys.argv
changed = already = errors = 0
rows = []
for path in targets:
    rel = os.path.relpath(path, HOME).replace("\\", "/")
    try:
        raw = open(path, encoding="utf-8", newline="").read()
        lines = raw.split("\n")
        # temukan blok top-level 'compression:'
        try:
            ci = next(i for i, l in enumerate(lines) if l.rstrip("\r") == "compression:")
        except StopIteration:
            ci = None
        if ci is None:
            # append blok baru di akhir (jaga CRLF/LF + trailing newline asli)
            eol = "\r\n" if "\r\n" in raw else "\n"
            tail = "" if raw.endswith(("\n", "\r\n")) else eol
            block = f"{eol}compression:{eol}  threshold: {THRESHOLD}{eol}  target_ratio: {TARGET_RATIO}{eol}"
            new_raw = raw + tail + block
            rows.append((rel, "blok baru"))
            changed += 1
        else:
            # batas blok: baris berikutnya yang top-level (karakter non-spasi kolom 0)
            end = len(lines)
            for j in range(ci + 1, len(lines)):
                s = lines[j].rstrip("\r")
                if s and not s[0].isspace() and not s.startswith("#"):
                    end = j
                    break
            got_t = got_r = False
            for j in range(ci + 1, end):
                s = lines[j].rstrip("\r")
                stripped = s.strip()
                if stripped.startswith("threshold:"):
                    val = stripped.split(":", 1)[1].strip()
                    if float(val) == float(THRESHOLD) and got_t is False:
                        got_t = True
                    lines[j] = s.replace(stripped, f"threshold: {THRESHOLD}")
                    got_t = True
                elif stripped.startswith("target_ratio:"):
                    lines[j] = s.replace(stripped, f"target_ratio: {TARGET_RATIO}")
                    got_r = True
            if not got_t:
                lines.insert(end, "  threshold: " + THRESHOLD)
            if not got_r:
                lines.insert(end, "  target_ratio: " + TARGET_RATIO)
            new_raw = "\n".join(lines)
            old_has = ("threshold: " + THRESHOLD) and True
            rows.append((rel, "blok existing"))
            changed += 1
        if new_raw != raw:
            if apply:
                bak = path + BAK
                if not os.path.exists(bak):
                    import shutil; shutil.copy2(path, bak)
                with open(path, "wb") as f:
                    f.write(new_raw.encode("utf-8"))
        else:
            already += 1
    except Exception as e:
        errors += 1
        rows.append((rel, f"ERROR {e}"))

for rel, st in rows[:4]:
    print(rel, "->", st)
print(f"MODE={'APPLY' if apply else 'DRY-RUN'} changed={changed} unchanged={already} errors={errors} total={len(targets)}")
