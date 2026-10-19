# -*- coding: utf-8 -*-
"""verify_word.py — AC-W1..W8 deterministik untuk HERMES-ZERO-TO-HERO-Course.docx
Dipakai controller (self-check) dan jadi acuan verifier STT-W3. Read-only."""
import re, os, sys, subprocess, json
from collections import Counter
from docx import Document

BASE = r"C:/Users/TRIAL/workspace/Test STT"
DOCX = os.path.join(BASE, "05_module", "HERMES-ZERO-TO-HERO-Course.docx")
MD   = os.path.join(BASE, "05_module", "HERMES-ZERO-TO-HERO.md")

results = []
def check(n, name, ok, evidence):
    results.append((n, name, "PASS" if ok else "FAIL", evidence))

doc = Document(DOCX)
md  = open(MD, encoding="utf-8").read()
body_text = "\n".join(p.text for p in doc.paragraphs)
tbl_text  = "\n".join(c.text for tb in doc.tables for r in tb.rows for c in r.cells)
all_text  = body_text + "\n" + tbl_text

# W1: package valid
vp = os.path.join(os.environ.get("LOCALAPPDATA",""), "hermes/skills/productivity/docx/scripts/docx_validate.py")
r = subprocess.run([sys.executable, vp, DOCX], capture_output=True, text=True)
try: okv = json.loads(r.stdout).get("ok") is False or json.loads(r.stdout).get("ok") is True
except Exception: okv = False
try: okv = json.loads(r.stdout)["ok"]
except Exception: okv = False
check(1, "AC-W1 package .docx valid (docx_validate ok=true)", okv, r.stdout.strip()[:120])

# W2: cover elements
cover = ("HERMES AGENT" in body_text and "ZERO-TO-HERO" in body_text
         and "Document ID" in tbl_text and "TERBITAN 1" in body_text)
check(2, "AC-W2 sampul: judul + control table + cap terbit", cover,
      f"HERMES AGENT={'HERMES AGENT' in body_text}, ZERO-TO-HERO={'ZERO-TO-HERO' in body_text}, ctrlTable={'Document ID' in tbl_text}, cap={'TERBITAN 1' in body_text}")

# W3: TOC field + PAGE/NUMPAGES fields
xml_all = "\n".join(rr._r.xml for p in doc.paragraphs for rr in p.runs)
hdr_ftr = ""
for s in doc.sections:
    for part in (s.header, s.footer):
        for p in part.paragraphs:
            for rr in p.runs: hdr_ftr += rr._r.xml
        for tb in part.tables:
            for row in tb.rows:
                for c in row.cells:
                    for p in c.paragraphs:
                        for rr in p.runs: hdr_ftr += rr._r.xml
w3 = ("TOC" in xml_all) and ("PAGE" in hdr_ftr) and ("NUMPAGES" in hdr_ftr)
check(3, "AC-W3 field TOC + footer PAGE/NUMPAGES", w3,
      f"TOC={'TOC' in xml_all} PAGE={'PAGE' in hdr_ftr} NUMPAGES={'NUMPAGES' in hdr_ftr}")

# W4: heading outline matches MD (H1/H2/H3 counts, excluding added front/back matter)
lv = Counter(p.style.name for p in doc.paragraphs if p.style.name.startswith("Heading"))
md_lv = Counter(len(m) for m in re.findall(r"^(#+) ", md, re.M))
h1d = lv.get("Heading 1",0); h2d = lv.get("Heading 2",0); h3d = lv.get("Heading 3",0)
# docx adds: 'TABLE OF CONTENTS'(H? we used plain para) + 'Revision History'(H1)
w4 = (h2d == md_lv.get(2,0)) and (h3d == md_lv.get(3,0)) and (h1d >= md_lv.get(1,0)-1)  # -1: MD H1 title on cover
check(4, "AC-W4 heading-match dengan MD kanonis", w4,
      f"docx H1={h1d} H2={h2d} H3={h3d} vs md H1={md_lv.get(1)} H2={md_lv.get(2)} H3={md_lv.get(3)} (H1 docx +Revision History, -title sampul)")

# W5: content fidelity — chunk-level coverage (window 8 kata, marker daftar &
# URL/sitasi dinormalkan; angka penanda list tidak dihitung karena Word memakai
# auto-numbering yang dirender saat dibuka — bukti visual dicek manual)
def norm_flat(t):
    t = re.sub(r"^\s*\d+\.\s+", " ", t, flags=re.M)   # list markers
    t = re.sub(r"^\s*[-*>]+\s?", " ", t, flags=re.M)
    t = re.sub(r"[#*`>|]+", " ", t)
    t = re.sub(r"\[V\d[^\]]*\]", " ", t)
    t = re.sub(r"https?://\S+", " ", t)
    t = re.sub(r"&[a-z]+;", " ", t)
    return re.sub(r"\s+", " ", t.lower())
def toks(t): return re.findall(r"[a-z0-9']+", t)
dflat = norm_flat(all_text)
dtxt = " " + " ".join(toks(dflat)) + " "
mflat = norm_flat(md)
md_lines = [l for l in mflat.split("\n") if len(toks(l)) >= 8]
total = 0; hit = 0; misses = []
for l in md_lines:
    w = toks(l)
    for i in range(0, len(w)-7):
        win = " " + " ".join(w[i:i+8]) + " "
        total += 1
        if win in dtxt: hit += 1
        else: misses.append(win.strip())
cov = 100*hit/total if total else 100
check(5, "AC-W5 fidelitas konten >=99% (coverage 8-gram MD di docx)", cov >= 99.0,
      f"coverage={cov:.2f}% ({hit}/{total}) sample_miss={misses[:6]}")

# W6: all tables from MD present (>= md table count; header cells found)
def md_tables(s):
    out=[]; cur=None
    for l in s.split("\n"):
        if l.strip().startswith("|"):
            cur = cur or []; cur.append(l.strip())
        else:
            if cur: out.append(cur); cur=None
    if cur: out.append(cur)
    return out
mt = md_tables(md)
found = 0
for t in mt:
    hdr = [c.strip() for c in t[0].strip("|").split("|")]
    key = hdr[0][:12].lower()
    if key and key in tbl_text.lower(): found += 1
check(6, "AC-W6 semua tabel MD terkonversi (header terdeteksi)", found == len(mt),
      f"md tables={len(mt)} found={found}")

# W7: citations preserved (timestamp citations in docx >= 95% of count in MD)
cm = len(re.findall(r"\[V\d \d", md)); cdn = len(re.findall(r"\[V\d \d", all_text))
check(7, "AC-W7 sitasi timestamp [Vn MM:SS] utuh (>=95%)", cdn >= 0.95*cm,
      f"md={cm} docx={cdn}")

# W8: file in mission folder + core properties + revision history section
w8 = (os.path.exists(DOCX) and "Revision History" in body_text
      and doc.core_properties.title.startswith("Hermes Agent"))
check(8, "AC-W8 file di folder misi + core properties + riwayat revisi", w8,
      f"size={os.path.getsize(DOCX)}B revhist={'Revision History' in body_text} title='{doc.core_properties.title[:40]}'")

for n,name,st,ev in results:
    print(f"CHECK {n}: {st} — {name} — {ev}")
verdict = "PASS" if all(r[2]=="PASS" for r in results) else "FAIL"
print("VERDICT:", verdict)
sys.exit(0 if verdict=="PASS" else 1)
