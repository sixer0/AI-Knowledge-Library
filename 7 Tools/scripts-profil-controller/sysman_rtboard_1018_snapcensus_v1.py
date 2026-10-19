# Sensus snapshot terminal lintas profil: marker child + HERMES_KANBAN_* yang bocor ke snapshot
import glob, os, re, time

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
pats = [os.path.join(HOME, "cache", "terminal", "hermes-snap-*.sh"),
        os.path.join(HOME, "profiles", "*", "cache", "terminal", "hermes-snap-*.sh")]
rows = []
for pat in pats:
    for f in glob.glob(pat):
        try:
            txt = open(f, encoding="utf-8", errors="replace").read()
        except Exception as e:
            rows.append((f, "ERR", str(e), "")); continue
        marker = "HERMES_DELEGATED_CHILD_CONTEXT" in txt
        kanban = re.findall(r'declare -x (HERMES_KANBAN_[A-Z_]+)=', txt)
        mt = time.strftime('%m-%d %H:%M', time.localtime(os.path.getmtime(f)))
        prof = f.split(os.sep + "profiles" + os.sep)[1].split(os.sep)[0] if "profiles" + os.sep in f else "ROOT(default)"
        rows.append((prof, mt, "MARKER" if marker else "-", ",".join(sorted(set(kanban))) or "-"))

print(f"{'PROFIL':28} {'MTIME':12} {'MARKER':7} KANBAN_VARS_DI_SNAPSHOT")
for r in sorted(rows):
    print(f"{r[0]:28} {r[1]:12} {r[2]:7} {r[3]}")
print("TOTAL snapshot:", len(rows), "| ber-marker:", sum(1 for r in rows if r[2]=='MARKER'))
