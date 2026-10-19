# Bersihkan snapshot terminal terkontaminasi: buang baris marker child + HERMES_KANBAN_*
# (nilai Kanban diinjeksi ulang per perintah dari env proses pemilik; snapshot hanya boleh
#  memuat keadaan shell pengguna. Preseden kelas bocor-lintas-sesi base.py L569.)
import glob, os, re

HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
pats = [os.path.join(HOME, "cache", "terminal", "hermes-snap-*.sh"),
        os.path.join(HOME, "profiles", "*", "cache", "terminal", "hermes-snap-*.sh")]
PAT = re.compile(r'^declare -x (HERMES_DELEGATED_CHILD_CONTEXT|HERMES_KANBAN_[A-Z_]+)=')
changed = []
total = 0
for pat in pats:
    for f in glob.glob(pat):
        total += 1
        try:
            txt = open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        lines = txt.splitlines(keepends=True)
        kept = [ln for ln in lines if not PAT.match(ln)]
        if len(kept) != len(lines):
            open(f, "w", encoding="utf-8", newline="").writelines(kept)
            changed.append((f, len(lines) - len(kept)))
for f, n in changed:
    print(f"DIBERSIHKAN ({n} baris): {f}")
print(f"TOTAL snapshot dipindai={total} | diubah={len(changed)}")
# verifikasi ulang
sisa = 0
for pat in pats:
    for f in glob.glob(pat):
        try:
            txt = open(f, encoding="utf-8", errors="replace").read()
        except Exception:
            continue
        sisa += sum(1 for ln in txt.splitlines() if PAT.match(ln))
print("SISA baris terlarang di semua snapshot:", sisa)
