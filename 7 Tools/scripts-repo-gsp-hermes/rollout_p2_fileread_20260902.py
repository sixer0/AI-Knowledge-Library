# -*- coding: utf-8 -*-
"""Rollout EXPO-OPT-P2 2026-09-02: file_read_max_chars: 30000 di profil pekerja.
- Target sama dengan rollout P1 (non-exclude), TANPA menyentuh kunci lain.
- Wave 1 (gsp-data-collector, gsp-vendor-crawler-specialist, gsp-explore) sudah
  memasang kunci ini saat rollout P1; skrip ini tetap idempoten padanya.
- Backup ke workspace_backups/2026-09-02-worker-speedup-p2/<profil>/config.yaml
  (hanya dibuat bila belum ada; salinan P1 pra-rollout juga tetap utuh di root lama).
- Tulis atomik (temp + os.replace), validasi yaml sebelum tulis, baca-ulang setelah tulis.
Pemakaian: python rollout_p2_fileread_20260902.py before|apply|verify
"""
import io, os, shutil, sys, yaml

PROF_ROOT = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
BACKUP_ROOT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace_backups/2026-09-02-worker-speedup-p2"
P1_BACKUP_ROOT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace_backups/2026-09-02-worker-speedup"
VALUE = 30000

EXCLUDE = {  # controller & akun RBAC: tidak disentuh (daftar sama dgn rollout P1)
    "gsp-master01", "gsp-master", "gsp-crawler-orchestrator", "gsp-skill-manager",
    "gsp-system-manager", "gsp-pm-planner", "gspuser01",
    "firmanhidayat", "gsp-creative", "gsp-firman-custom", "novriandy", "gsp-budi",
}

def targets():
    return sorted(d for d in os.listdir(PROF_ROOT)
                  if os.path.isfile(os.path.join(PROF_ROOT, d, "config.yaml"))
                  and d not in EXCLUDE)

def read_cfg(prof):
    p = os.path.join(PROF_ROOT, prof, "config.yaml")
    return yaml.safe_load(io.open(p, encoding="utf-8").read()) or {}

def snapshot():
    rows = []
    for prof in targets():
        d = read_cfg(prof)
        rows.append((prof, d.get("file_read_max_chars")))
    return rows

def edit(path):
    src = io.open(path, encoding="utf-8").read()
    lines = src.split("\n")
    out, hit = [], False
    for ln in lines:
        if not hit and ln.startswith("file_read_max_chars:"):
            out.append("file_read_max_chars: %d" % VALUE)
            hit = True
        else:
            out.append(ln)
    if not hit:
        body = "\n".join(out).rstrip("\n")
        out = (body + "\nfile_read_max_chars: %d\n" % VALUE).split("\n")
    return "\n".join(out)

def apply():
    changed, kept = [], []
    for prof in targets():
        cfg = os.path.join(PROF_ROOT, prof, "config.yaml")
        before = read_cfg(prof).get("file_read_max_chars")
        if before == VALUE:
            kept.append((prof, before, before))
            continue  # idempoten: tanpa tulis, tanpa backup kosong-meaningless
        bdir = os.path.join(BACKUP_ROOT, prof)
        os.makedirs(bdir, exist_ok=True)
        bpath = os.path.join(bdir, "config.yaml")
        if not os.path.exists(bpath):
            shutil.copy2(cfg, bpath)
        new = edit(cfg)
        yaml.safe_load(new)  # validasi parse sebelum tulis
        tmp = cfg + ".tmp-p2"
        io.open(tmp, "w", encoding="utf-8", newline="\n").write(new)
        os.replace(tmp, cfg)
        after = read_cfg(prof).get("file_read_max_chars")
        changed.append((prof, before, after))
    print("CHANGED (%d):" % len(changed))
    for r in changed:
        print("  %-32s %s -> %s" % r)
    print("ALREADY-SET (%d): %s" % (len(kept), ", ".join(p for p, _, _ in kept)))
    print("TOTAL TARGETS:", len(changed) + len(kept))

def verify():
    bad = []
    n = 0
    for prof in targets():
        n += 1
        d = read_cfg(prof)
        v = d.get("file_read_max_chars")
        if v != VALUE:
            bad.append((prof, v))
        # jejak pra-keadaan: backup P2 (profil yang benar-benar diubah skrip ini)
        # atau backup P1 (profil yang sudah memuat kunci sebelum kartu P2 dimulai)
        bp2 = os.path.join(BACKUP_ROOT, prof, "config.yaml")
        bp1 = os.path.join(P1_BACKUP_ROOT, prof, "config.yaml")
        if not (os.path.exists(bp2) or os.path.exists(bp1)):
            bad.append((prof, "NO-BACKUP"))
        elif os.path.exists(bp1):
            b = yaml.safe_load(io.open(bp1, encoding="utf-8").read()) or {}
            if b.get("file_read_max_chars") == VALUE:
                bad.append((prof, "P1-BACKUP-NOT-PRESTATE"))
    print("profiles checked:", n)
    print("problems:", bad if bad else "NONE")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode == "before":
        for prof, v in snapshot():
            print("%-32s %s" % (prof, v))
    elif mode == "apply":
        apply()
    else:
        verify()
