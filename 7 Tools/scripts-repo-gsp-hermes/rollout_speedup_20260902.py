# -*- coding: utf-8 -*-
"""Rollout EXPO-OPT 2026-09-02 (P1,P2,P6) ke profil pekerja.
!! PERINGATAN WF-CRAWL-0911 (11-09-2026, keputusan controller D-04):
   P1 searxng->ddgs SUDAH DIBALIK untuk roster koleksi
   (gsp-data-collector, gsp-explore, gsp-social-media-crawler,
   gsp-vendor-crawler-specialist, gsp-crawler-orchestrator) atas direktif user
   "enforce firecrawl+searxng paralel". JANGAN jalankan wave1/wave2 ulang tanpa
   mengecualikan kelima profil itu - lihat docs/2026-09-11-firecrawl-searxng-parallel-enforcement/.
- P1: web.search_backend searxng -> ddgs
- P2: web.extract_char_limit 10000 (semua target); file_read_max_chars 30000 (hanya wave1)
- P6: agent.run_budget_seconds 1500 -> 1680 (bila kunci ada)
Backup tiap config ke workspace_backups/2026-09-02-worker-speedup/<profil>/config.yaml
Tulis atomik (temp + os.replace). Verifikasi baca-ulang dengan yaml.safe_load.
Pemakaian: python rollout_speedup_20260902.py wave1|wave2|verify
"""
import io, os, re, shutil, sys, yaml

PROF_ROOT = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
BACKUP_ROOT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace_backups/2026-09-02-worker-speedup"

EXCLUDE = {  # controller & akun RBAC: tidak disentuh
    "gsp-master01", "gsp-master", "gsp-crawler-orchestrator", "gsp-skill-manager",
    "gsp-system-manager", "gsp-pm-planner", "gspuser01",
    "firmanhidayat", "gsp-creative", "gsp-firman-custom", "novriandy", "gsp-budi",
}
WAVE1 = ["gsp-data-collector", "gsp-vendor-crawler-specialist", "gsp-explore"]

def targets(wave):
    if wave == "wave1":
        return WAVE1
    allp = sorted(d for d in os.listdir(PROF_ROOT)
                  if os.path.isfile(os.path.join(PROF_ROOT, d, "config.yaml")))
    return [p for p in allp if p not in EXCLUDE and p not in WAVE1]

def edit(path, wave1_flag):
    src = io.open(path, encoding="utf-8").read()
    out = src
    # P1
    out = re.sub(r"(?m)^(\s*)search_backend:\s*searxng\s*$", r"\1search_backend: ddgs", out)
    # P2a: extract_char_limit dalam blok web (setelah search_backend)
    if "extract_char_limit" not in out:
        out = re.sub(r"(?m)^(\s*)search_backend:\s*ddgs\s*$",
                     r"\1search_backend: ddgs\n\1extract_char_limit: 10000", out, count=1)
    # P2b: file_read_max_chars top-level (hanya wave1)
    if wave1_flag and "file_read_max_chars" not in out:
        out = out.rstrip("\n") + "\nfile_read_max_chars: 30000\n"
    # P6
    out = re.sub(r"(?m)^(\s*)run_budget_seconds:\s*1500\s*$", r"\1run_budget_seconds: 1680", out)
    return out

def apply(wave):
    wave1_flag = (wave == "wave1")
    rows = []
    for prof in targets(wave):
        cfg = os.path.join(PROF_ROOT, prof, "config.yaml")
        bdir = os.path.join(BACKUP_ROOT, prof)
        os.makedirs(bdir, exist_ok=True)
        bpath = os.path.join(bdir, "config.yaml")
        if not os.path.exists(bpath):
            shutil.copy2(cfg, bpath)
        new = edit(cfg, wave1_flag)
        yaml.safe_load(new)  # validasi parse sebelum tulis
        tmp = cfg + ".tmp-speedup"
        io.open(tmp, "w", encoding="utf-8", newline="\n").write(new)
        os.replace(tmp, cfg)
        d = yaml.safe_load(io.open(cfg, encoding="utf-8").read())
        web = d.get("web", {}) or {}
        agent = d.get("agent", {}) or {}
        rows.append((prof, web.get("search_backend"), web.get("extract_char_limit"),
                     d.get("file_read_max_chars"), agent.get("run_budget_seconds")))
    print("%-32s %-8s %-6s %-6s %-6s" % ("profile", "search", "extrL", "fileR", "budget"))
    for r in rows:
        print("%-32s %-8s %-6s %-6s %-6s" % r)
    print("TOTAL:", len(rows))

def verify():
    bad = []
    for prof in targets("wave2") + WAVE1:
        cfg = os.path.join(PROF_ROOT, prof, "config.yaml")
        d = yaml.safe_load(io.open(cfg, encoding="utf-8").read())
        sb = (d.get("web") or {}).get("search_backend")
        if sb != "ddgs":
            bad.append((prof, sb))
    print("profiles checked:", len(WAVE1) + len(targets("wave2")))
    print("NOT ddgs:", bad if bad else "0 (semua ddgs)")

if __name__ == "__main__":
    mode = sys.argv[1] if len(sys.argv) > 1 else "verify"
    if mode in ("wave1", "wave2"):
        apply(mode)
    else:
        verify()
