#!/usr/bin/env python
# gerbang KORPUS-IDX-REPAIR-1005 — audit ulang deterministik (dipakai KVER)
# Cek: A set can<->reg, B frontmatter name==folder, C md5 12 skill EKAS,
#      D angka inventaris pustaka-teknis vs disk, E rujukan resolve,
#      F STORAGE-DATACENTER tersiar (putusan librarian), G akses gsp-master.
import hashlib, os, re, subprocess, sys, io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8")

REG = r"C:/Users/TRIAL/AppData/Local/hermes/skills/gsp"
CAN = r"C:/Users/TRIAL/workspace/gsp-hermes/skills"
WS  = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace"
EKAS = os.path.join(WS, "ekas", "05_DOMAIN-KNOWLEDGE")
CAT = []

def md5(p):
    try:
        with open(p, "rb") as f: return hashlib.md5(f.read()).hexdigest()[:8]
    except OSError: return None

def emit(n, ok, name, detail=""):
    v = "PASS" if ok else ("NEEDS_REVIEW" if ok is None else "FAIL")
    CAT.append(v)
    print(f"CHECK {n}: {v} - {name} | {detail}")

# A. set kanonik <-> registry (folder kategori 'cad' dikecualikan)
regs = {d for d in os.listdir(REG) if os.path.isdir(os.path.join(REG, d))}
cans = {d for d in os.listdir(CAN) if os.path.isdir(os.path.join(CAN, d))} - {"cad"}
only_reg = sorted(regs - cans); only_can = sorted(cans - regs)
emit("A", not only_reg and not only_can, "set kanonik<->registry selisih nol",
     f"only_reg={only_reg} only_can={only_can}")

# B. frontmatter name == nama folder (semua skill di kedua set)
bad = []
for base, tag in ((CAN, "CAN"), (REG, "REG")):
    for d in sorted(os.listdir(base)):
        sk = os.path.join(base, d, "SKILL.md")
        if not os.path.isfile(sk): continue
        m = re.search(r"^name:\s*(.+?)\s*$", open(sk, encoding="utf-8", errors="replace").read(4000), re.M)
        nm = (m.group(1).strip().strip('"\'') if m else "<none>")
        if nm != d: bad.append(f"{tag}/{d}:{nm}")
emit("B", not bad, "frontmatter name == folder (can+reg)", f"cacat={bad if bad else 0}")

# C. md5 12 skill EKAS kanonik == registry
EKAS12 = ["pustaka-teknis","rcm-analysis","fiber-link-design","power-backup-sizing",
          "grounding-lightning-design","cctv-system-designer","perimeter-security-designer",
          "hw-sw-config-master","digital-forensics-evidence-system","dems-polri-proposal-architect",
          "excel-master","onvif-interop"]
mism = [s for s in EKAS12 if md5(f"{CAN}/{s}/SKILL.md") != md5(f"{REG}/{s}/SKILL.md")]
emit("C", not mism, "md5 12 skill EKAS can==reg", f"bedabeda={mism if mism else 'nol (12/12 sinkron)'}")

# D. angka inventaris pustaka-teknis vs disk
doms = sorted(d for d in os.listdir(EKAS) if os.path.isdir(os.path.join(EKAS, d)))
rantai = sum(1 for d in doms if os.path.isfile(os.path.join(EKAS, d, "RANTAI-JAMINAN.md")))
txt = open(f"{REG}/pustaka-teknis/SKILL.md", encoding="utf-8").read()
m = re.search(r"\*\*(\d+)\s*di antaranya sudah punya", txt)
claim = int(m.group(1)) if m else -1
ver_ok = ("14" in txt.split("Daftar domain korpus")[1][:400]) if "Daftar domain korpus" in txt else False
emit("D", claim == rantai and ver_ok, "angka inventaris skill == disk",
     f"disk: {len(doms)} domain / {rantai} rantai; skill mengklaim '{claim} di antaranya'; seksi menyebut 14: {ver_ok}")

# E. rujukan path korpus resolve (elipsis dilarang; baris larangan/negative-example dikecualikan)
broken = []
for s in EKAS12:
    p = f"{REG}/{s}/SKILL.md"
    if not os.path.isfile(p): continue
    for ln in open(p, encoding="utf-8").read().splitlines():
        if re.search(r"jangan|bukan|\btidak\b", ln, re.I): continue  # negative example, bukan rujukan
        for r in set(re.findall(r"(?<![A-Za-z0-9_-])ekas/[A-Za-z0-9_./-]*", ln)):
            if "..." in r or "_..." in r: broken.append(f"{s}:{r}"); continue
            full = os.path.join(WS, r.rstrip("/"))
            if not os.path.exists(full): broken.append(f"{s}:{r}")
emit("E", not broken, "rujukan ekas/ resolve + tanpa elipsis", f"rusak={broken if broken else 0}")

# F. STORAGE-DATACENTER: simetris ATAS ada catatan putusan
cards = {d for d in os.listdir(os.path.join(WS,"ekas","04_KNOWLEDGE-CARDS")) if os.path.isdir(os.path.join(WS,"ekas","04_KNOWLEDGE-CARDS",d))}
sym = cards - set(doms)  # folder kartu tanpa domain
noted = False
for root, _, files in os.walk(os.path.join(WS,"ekas","02_REGISTERS")):
    for fn in files:
        t = open(os.path.join(root,fn), encoding="utf-8", errors="replace").read()
        if "STORAGE-DATACENTER" in t and re.search(r"(putusan|keputusan|sengaja|asimetri|lebur|disolved|merged)", t, re.I):
            noted = True
resolved_sym = "STORAGE-DATACENTER" not in sym
emit("F", resolved_sym or noted, "STORAGE-DATACENTER tersiar (simetris atau ada catatan putusan)",
     f"selisih_kartu_minus_domain={sorted(sym)}; ada_catatan_putusan={noted}")

# G. akses registry dari profil gsp-master: external_dirs TERPASANG + grants berisi pustaka-teknis terbaca
prof = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gsp-master"
cfg = open(os.path.join(prof, "config.yaml"), encoding="utf-8", errors="replace").read() if os.path.isfile(os.path.join(prof,"config.yaml")) else ""
m = re.search(r"external_dirs:\s*\n((?:\s*-\s*.+\n?)+)", cfg)
dirs = re.findall(r"-\s*(\S+)", m.group(1)) if m else []
grant_ok = any(os.path.isfile(os.path.join(d.strip('"'), "pustaka-teknis", "SKILL.md")) for d in dirs)
emit("G", bool(dirs) and grant_ok, "jalur akses registry utk gsp-master terpasang",
     f"external_dirs={dirs}; pustaka-teknis terbaca dari grants={grant_ok}")

# H. README register: 'Baris terisi' == hasil parser CSV (advisory KVER 05-10)
import csv as _csv
rd = open(os.path.join(WS,"ekas","02_REGISTERS","README.md"), encoding="utf-8").read()
def claimed(fn):
    m = re.search(rf"\|\s*`{fn}`\s*\|\s*\*\*?(\d+)\*\*?", rd)
    return int(m.group(1)) if m else None
def actual(fn):
    p = os.path.join(WS,"ekas","02_REGISTERS",fn)
    return max(0, len(list(_csv.DictReader(open(p, encoding="utf-8")))))
mism = [f"{fn}:README={claimed(fn)} disk={actual(fn)}" for fn in
        ("MASTER-REFERENCE-REGISTER.csv","GAP-REGISTER.csv") if claimed(fn) != actual(fn)]
emit("H", not mism, "README register == parser CSV", f"sel={mism if mism else 0}")

v = "FAIL" if "FAIL" in CAT else ("NEEDS_REVIEW" if "NEEDS_REVIEW" in CAT else "PASS")
print(f"VERDICT: {v}  (PASS={CAT.count('PASS')} FAIL={CAT.count('FAIL')} NR={CAT.count('NEEDS_REVIEW')})")
sys.exit(0 if v != "FAIL" else 1)
