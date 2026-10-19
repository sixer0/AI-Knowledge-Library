# Tree-walk FTP NAS GSP berbasis cwd (menghindari quirk dir(path) SmbFTPD).
# Pemakaian: python nas_tree_find.py <substring> [maxdepth]   (default maxdepth 4)
# Kredensial dibaca dari ~/.gsp-mail/nas_gsp.env (NAS_HOST/NAS_USER/NAS_PASS).
import ftplib, os, sys

sub = (sys.argv[1] if len(sys.argv) > 1 else "").lower()
maxdepth = int(sys.argv[2]) if len(sys.argv) > 2 else 4

env = {}
for line in open(os.path.expanduser("~/.gsp-mail/nas_gsp.env")):
    line = line.strip()
    if "=" in line and not line.startswith("#"):
        k, v = line.split("=", 1); env[k.strip()] = v.strip()

f = ftplib.FTP(env.get("NAS_HOST", "192.168.0.90"), timeout=120)
f.login(env["NAS_USER"], env["NAS_PASS"])
f.voidcmd("TYPE I")

def ls():
    lines = []
    f.dir(lines.append)  # TANPA argumen path - quirk SmbFTPD
    out = []
    for ln in lines:
        if not ln.strip():
            continue
        parts = ln.split(None, 8)
        if len(parts) >= 9:
            out.append((parts[0], parts[8]))
    return out

hits = []

def walk(name, depth):
    try:
        f.cwd(name)
    except Exception as e:
        print(f"{'  '*depth}[skip {name}: {type(e).__name__}]")
        return
    try:
        entries = ls()
    except Exception as e:
        print(f"{'  '*depth}[skip {name}: {type(e).__name__}]")
        f.cwd(".."); return
    for typ, nm in entries:
        if nm in (".", ".."):
            continue
        isdir = typ.startswith("d") or typ.startswith("l")
        if sub and sub in nm.lower():
            hits.append(("/" if isdir else "") + nm)
            print(f"{'  '*depth}HIT: {'DIR ' if isdir else 'FILE'} {nm}")
        if isdir and depth < maxdepth:
            walk(nm, depth + 1)
    f.cwd("..")

print(f"== search '{sub}' di /GSP-DATA (depth<={maxdepth}) ==")
f.cwd("/GSP-DATA")
walk(".", 1)
print("\n== RINGKASAN ==")
for h in hits:
    print(h)
if not hits:
    print("TIDAK ADA nama mengandung substring pada depth tersebut.")
f.quit()
