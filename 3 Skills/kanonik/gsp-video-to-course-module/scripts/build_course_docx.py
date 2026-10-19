# -*- coding: utf-8 -*-
"""build_course_docx.py — Konversi deterministik 05_module/HERMES-ZERO-TO-HERO.md
(terverifikasi VERDICT PASS) menjadi modul course Word LENGKAP & profesional.
Konten TIDAK diubah; hanya penyajian. Grid/tipografi/palet per Acuan GSP 020/GSP/STD/VIII/2026 RevA
(gsp_lib terbukti 25-08) dengan klasifikasi TRAINING (dokumen pembelajaran, bukan laporan resmi).
Output: 05_module/HERMES-ZERO-TO-HERO-Course.docx
"""
import re, os, sys
from docx import Document
from docx.shared import Mm, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BASE = r"C:/Users/TRIAL/workspace/Test STT"
SRC = os.path.join(BASE, "05_module", "HERMES-ZERO-TO-HERO.md")
OUT = os.path.join(BASE, "05_module", "HERMES-ZERO-TO-HERO-Course.docx")

PAPER=RGBColor(0xFC,0xFC,0xFB); INK900=RGBColor(0x10,0x14,0x18); INK700=RGBColor(0x2B,0x36,0x40)
INK400=RGBColor(0x6B,0x77,0x83); INK200=RGBColor(0xC3,0xCB,0xD1); INK100=RGBColor(0xEF,0xF2,0xF4)
SIGNAL=RGBColor(0xB4,0x53,0x09); VERD=RGBColor(0x2F,0x6F,0x6B); WHITE=RGBColor(0xFF,0xFF,0xFF)
FS="Segoe UI Semibold"; FB="Georgia"; FD="Consolas"
DOC_ID="022/GSP/PEM/VIII/2026"; REV="REV B"; TANGGAL="31-VIII-2026"
CHIP="TRAINING"; TITLE="HERMES AGENT ZERO-TO-HERO"

def norm_em(t):
    if not t: return t
    t=t.replace(" — ", ", "); t=t.replace("—","–"); return t

def style_run(run, font=FB, size=10, color=INK700, bold=False, italic=False, caps=False, tracking=None):
    run.font.name=font; run.font.size=Pt(size); run.font.color.rgb=color
    run.font.bold=bold; run.font.italic=italic
    if caps: run.font.all_caps=True
    rPr=run._r.get_or_add_rPr()
    if tracking is not None:
        sp=OxmlElement("w:spacing"); sp.set(qn("w:val"), str(int(tracking*100))); rPr.append(sp)
    rf=rPr.find(qn("w:rFonts"))
    if rf is None: rf=OxmlElement("w:rFonts"); rPr.append(rf)
    rf.set(qn("w:ascii"),font); rf.set(qn("w:hAnsi"),font)
    return run

def set_cell_bg(cell, hexcolor):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement("w:shd")
    shd.set(qn("w:val"),"clear"); shd.set(qn("w:fill"),hexcolor); tcPr.append(shd)

def set_cell_margins(cell, top=40, start=60, bottom=40, end=60):
    tcPr=cell._tc.get_or_add_tcPr(); tcMar=OxmlElement("w:tcMar")
    for tag,val in (("top",top),("start",start),("bottom",bottom),("end",end)):
        el=OxmlElement(f"w:{tag}"); el.set(qn("w:w"),str(val)); el.set(qn("w:type"),"dxa"); tcMar.append(el)
    tcPr.append(tcMar)

def table_grammar(tbl, head_mm=0.25, row_mm=0.2):
    tblPr=tbl._tbl.tblPr; borders=OxmlElement("w:tblBorders")
    for edge in ("top","bottom"):
        el=OxmlElement(f"w:{edge}"); el.set(qn("w:val"),"single")
        el.set(qn("w:sz"),str(int(0.45*8))); el.set(qn("w:color"),"101418"); borders.append(el)
    for edge in ("left","right","insideV"):
        el=OxmlElement(f"w:{edge}"); el.set(qn("w:val"),"none"); borders.append(el)
    el=OxmlElement("w:insideH"); el.set(qn("w:val"),"single")
    el.set(qn("w:sz"),str(int(row_mm*8))); el.set(qn("w:color"),"C3CBD1"); borders.append(el)
    tblPr.append(borders)
    if len(tbl.rows)>0:
        for cell in tbl.rows[0].cells:
            tcPr=cell._tc.get_or_add_tcPr(); tcb=OxmlElement("w:tcBorders")
            b=OxmlElement("w:bottom"); b.set(qn("w:val"),"single")
            b.set(qn("w:sz"),str(int(head_mm*8))); b.set(qn("w:color"),"101418")
            tcb.append(b); tcPr.append(tcb)
        for cell in tbl.rows[0].cells:
            set_cell_bg(cell,"EFF2F4")

def add_field(p, code):
    run=p.add_run()
    f1=OxmlElement("w:fldChar"); f1.set(qn("w:fldCharType"),"begin")
    it=OxmlElement("w:instrText"); it.set(qn("xml:space"),"preserve"); it.text=code
    f2=OxmlElement("w:fldChar"); f2.set(qn("w:fldCharType"),"end")
    run._r.append(f1); run._r.append(it); run._r.append(f2)
    return run

# ── numbering (list bernomor restart tiap blok) ──────────────────────────────
def make_numid(doc):
    np=doc.part.numbering_part.element
    absids=[int(a.get(qn("w:abstractNumId"))) for a in np.findall(qn("w:abstractNum"))]
    nums=[int(n.get(qn("w:numId"))) for n in np.findall(qn("w:num"))]
    aid=max(absids+[0])+1; nid=max(nums+[0])+1
    a=OxmlElement("w:abstractNum"); a.set(qn("w:abstractNumId"),str(aid))
    lvl=OxmlElement("w:lvl"); lvl.set(qn("w:ilvl"),"0")
    st=OxmlElement("w:start"); st.set(qn("w:val"),"1"); lvl.append(st)
    nt=OxmlElement("w:numFmt"); nt.set(qn("w:val"),"decimal"); lvl.append(nt)
    lt=OxmlElement("w:lvlText"); lt.set(qn("w:val"),"%1."); lvl.append(lt)
    lv=OxmlElement("w:lvlOverride"); lv.set(qn("w:startOverride"),"1"); lvl.append(lv)
    ind=OxmlElement("w:pPr"); pind=OxmlElement("w:ind")
    pind.set(qn("w:left"),"480"); pind.set(qn("w:hanging"),"360"); ind.append(pind); lvl.append(ind)
    a.append(lvl); np.append(a)
    n=OxmlElement("w:num"); n.set(qn("w:numId"),str(nid))
    ra=OxmlElement("w:abstractNumId"); ra.set(qn("w:val"),str(aid)); n.append(ra)
    ov=OxmlElement("w:lvlOverride"); ov.set(qn("w:ilvl"),"0")
    so=OxmlElement("w:startOverride"); so.set(qn("w:val"),"1"); ov.append(so); n.append(ov)
    np.append(n)
    return nid

def numpr(p, numid):
    pPr=p._p.get_or_add_pPr(); num=OxmlElement("w:numPr")
    ilvl=OxmlElement("w:ilvl"); ilvl.set(qn("w:val"),"0"); num.append(ilvl)
    nid=OxmlElement("w:numId"); nid.set(qn("w:val"),str(numid)); num.append(nid)
    pPr.append(num)

# ── inline markdown → runs ───────────────────────────────────────────────────
INLINE=re.compile(r"(\*\*.+?\*\*|\*[^*\n]+?\*|`[^`\n]+`)")
def add_inline(p, text, base_size=10, base_color=INK700, base_font=FB, bold=False, italic=False):
    for tok in INLINE.split(norm_em(text)):
        if not tok: continue
        if tok.startswith("**") and tok.endswith("**") and len(tok)>4:
            style_run(p.add_run(tok[2:-2]), base_font, base_size, base_color, bold=True, italic=italic)
        elif tok.startswith("*") and tok.endswith("*") and len(tok)>2:
            style_run(p.add_run(tok[1:-1]), base_font, base_size, base_color, bold=bold, italic=True)
        elif tok.startswith("`") and tok.endswith("`") and len(tok)>2:
            style_run(p.add_run(tok[1:-1]), FD, base_size-0.5, INK900, bold=bold)
        else:
            style_run(p.add_run(tok), base_font, base_size, base_color, bold=bold, italic=italic)

def para(doc, text, size=10, color=INK700, align=WD_ALIGN_PARAGRAPH.JUSTIFY, after=5, font=FB):
    p=doc.add_paragraph(); p.alignment=align
    p.paragraph_format.space_after=Pt(after); p.paragraph_format.line_spacing=Pt(13.5)
    add_inline(p, text, base_size=size, base_color=color, base_font=font)
    return p

def h(doc, level, text):
    p=doc.add_paragraph(style=f"Heading {level}")
    p.paragraph_format.space_before=Pt(14 if level==1 else 9)
    p.paragraph_format.space_after=Pt(5 if level==1 else 3)
    p.paragraph_format.keep_with_next=True
    size={1:15,2:11.5,3:10.5}.get(level,10)
    color={1:INK900,2:INK900,3:INK700}.get(level,INK700)
    # Q-D fix: heading = struktur, tipografi MD dipertahankan (tanpa norm_em)
    for tok in INLINE.split(text):
        if not tok: continue
        if tok.startswith("**") and tok.endswith("**") and len(tok)>4:
            style_run(p.add_run(tok[2:-2]), FS, size, color, bold=True)
        elif tok.startswith("`") and tok.endswith("`") and len(tok)>2:
            style_run(p.add_run(tok[1:-1]), FD, size-0.5, color, bold=True)
        else:
            style_run(p.add_run(tok), FS, size, color, bold=True)
    if level==1:
        pPr=p._p.get_or_add_pPr(); pBdr=OxmlElement("w:pBdr"); bot=OxmlElement("w:bottom")
        bot.set(qn("w:val"),"single"); bot.set(qn("w:sz"),"12"); bot.set(qn("w:color"),"101418")
        pBdr.append(bot); pPr.append(pBdr)
    return p

def md_table(doc, rows_md):
    def cells(line):
        line=line.strip()
        if line.startswith("|"): line=line[1:]
        if line.endswith("|"): line=line[:-1]
        return [c.strip() for c in line.split("|")]
    header=cells(rows_md[0]); body=[cells(r) for r in rows_md[2:]]
    ncols=len(header)
    tbl=doc.add_table(rows=1+len(body), cols=ncols)
    tbl.alignment=WD_TABLE_ALIGNMENT.CENTER; tbl.autofit=False
    # isi sel
    for j,val in enumerate(header):
        c=tbl.rows[0].cells[j]; set_cell_margins(c)
        p=c.paragraphs[0]; add_inline(p, val, base_size=8.6, base_color=INK900, base_font=FS, bold=True)
    for i,row in enumerate(body):
        row=(row+[""]*ncols)[:ncols]
        for j,val in enumerate(row):
            c=tbl.rows[i+1].cells[j]; set_cell_margins(c)
            p=c.paragraphs[0]
            mono=any(ch.isdigit() for ch in val[:8])
            add_inline(p, val, base_size=8.6, base_color=INK700, base_font=(FD if mono else FB))
    table_grammar(tbl)
    doc.add_paragraph().paragraph_format.space_after=Pt(3)
    return tbl

# ── dokumen ──────────────────────────────────────────────────────────────────
doc=Document()
sec=doc.sections[0]
sec.page_width=Mm(210); sec.page_height=Mm(297)
sec.left_margin=Mm(24); sec.right_margin=Mm(20); sec.top_margin=Mm(16); sec.bottom_margin=Mm(16)
sec.header_distance=Mm(9); sec.footer_distance=Mm(9)

st=doc.styles["Normal"]; st.font.name=FB; st.font.size=Pt(10); st.font.color.rgb=INK700
rPr=st.element.get_or_add_rPr(); rf=OxmlElement("w:rFonts")
rf.set(qn("w:ascii"),FB); rf.set(qn("w:hAnsi"),FB); rPr.append(rf)

# header/footer
hdr=sec.header; hdr.is_linked_to_previous=False
ht=hdr.add_table(rows=1, cols=2, width=Mm(166))
c1,c2=ht.rows[0].cells
p=c1.paragraphs[0]; style_run(p.add_run("PT GEMILANG SATRIA PERKASA · GSP KNOWLEDGE PRODUCTION · HERMES AGENT ZERO-TO-HERO"), FD, 6.8, INK400, caps=True, tracking=0.16)
p=c2.paragraphs[0]; p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
r=p.add_run(f"  {CHIP}  "); style_run(r, FD, 6.8, WHITE, bold=True); set_cell_bg(c2,"2F6F6B")
ftr=sec.footer; ftr.is_linked_to_previous=False
ft=ftr.add_table(rows=1, cols=4, width=Mm(166))
cells=ft.rows[0].cells
vals=[f"GSP · {DOC_ID}", f"{REV} · {TANGGAL}", None, f"  {CHIP}  "]
for i,c in enumerate(cells):
    set_cell_margins(c, top=20, bottom=20); p=c.paragraphs[0]
    if i==2:
        p.alignment=WD_ALIGN_PARAGRAPH.CENTER
        style_run(p.add_run("PAGE "), FD, 6.8, INK400); rr=add_field(p,"PAGE"); style_run(rr,FD,6.8,INK400)
        style_run(p.add_run(" OF "), FD, 6.8, INK400); rr=add_field(p,"NUMPAGES"); style_run(rr,FD,6.8,INK400)
    elif i==3:
        p.alignment=WD_ALIGN_PARAGRAPH.RIGHT
        r=p.add_run(vals[i]); style_run(r, FD, 6.8, WHITE, bold=True); set_cell_bg(c,"2F6F6B")
    else:
        style_run(p.add_run(vals[i]), FD, 6.8, INK400)

# ── SAMPUL ──
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(2)
style_run(p.add_run("PT. GEMILANG SATRIA PERKASA — GSP KNOWLEDGE PRODUCTION"), FS, 8, SIGNAL, bold=True, caps=True, tracking=0.2)
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(0)
style_run(p.add_run("PROFESSIONAL LEARNING MODULE · COURSE BODY"), FS, 7.5, INK400, caps=True, tracking=0.2)
doc.add_paragraph()
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(2)
style_run(p.add_run("HERMES AGENT"), FS, 30, INK900, bold=True)
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(6)
style_run(p.add_run("ZERO-TO-HERO"), FS, 30, SIGNAL, bold=True)
p=doc.add_paragraph(); p.paragraph_format.space_after=Pt(18)
style_run(p.add_run("An Integrated Learning Module — synthesizing five complementary tutorial videos and the official documentation into one sequential curriculum."), FB, 12, INK700, italic=True)

ctl=[("Document ID", DOC_ID),("Revision","Rev B"),("Issue date","31 August 2026"),
     ("Classification","INTERNAL · TRAINING"),("Publisher","GSP Knowledge Production (Swarm fleet)"),
     ("Course title","Hermes Agent Zero-to-Hero: An Integrated Learning Module"),
     ("Audience","Absolute beginners through advanced practitioners; no DevOps background required"),
     ("Duration","±24–30 guided hours, 8 modules (2.5–4 h each incl. exercises)"),
     ("Assessment","Per-module quiz + auto-checkable exercise; capstone 'Hero Runbook' (Module 8)"),
     ("Source corpus","5 YouTube tutorials (85,516 transcribed words, caption coverage 98.5–99.9%) + official docs"),
     ("Verification","Deterministic checks AC1–AC10 VERDICT PASS + independent countersign (2026-08-31)")]
tbl=doc.add_table(rows=len(ctl)+1, cols=2); tbl.autofit=False
hdrc=tbl.rows[0].cells
for j,txt in enumerate(("Field","Value")):
    set_cell_margins(hdrc[j]); pp=hdrc[j].paragraphs[0]
    style_run(pp.add_run(txt), FS, 8.6, INK900, bold=True, caps=True)
for i,(k,v) in enumerate(ctl):
    a,b=tbl.rows[i+1].cells; set_cell_margins(a); set_cell_margins(b)
    a.width=Mm(38); b.width=Mm(128)
    style_run(a.paragraphs[0].add_run(k), FS, 8.6, INK700, bold=True)
    style_run(b.paragraphs[0].add_run(norm_em(v)), FB, 8.6, INK700)
table_grammar(tbl)
p=doc.add_paragraph(); p.paragraph_format.space_before=Pt(14)
style_run(p.add_run(f"// 31VIII2026 ID T — TERBITAN 1 · {DOC_ID} · {REV}"), FD, 8, INK400)
doc.add_page_break()

# ── DAFTAR ISI (field TOC — terisi saat dibuka di Word) ──
p=doc.add_paragraph(); style_run(p.add_run("TABLE OF CONTENTS"), FS, 14, INK900, bold=True)
p=doc.add_paragraph()
style_run(p.add_run("(Right-click → Update Field in Word to populate page numbers.)"), FB, 8.5, INK400, italic=True)
ptoc=doc.add_paragraph()
add_field(ptoc, r'TOC \o "1-3" \h \z \u')
doc.add_page_break()

# ── ISI: parse MD kanonis ──
md=open(SRC, encoding="utf-8").read()
lines=md.split("\n")
i=0
if lines[0].strip()=="---":
    i=lines.index("---",1)+1
skip_first_h1=True
while i < len(lines):
    ln=lines[i]
    s=ln.strip()
    if not s or s=="---":
        i+=1; continue
    m=re.match(r"^(#{1,4})\s+(.*)$", s)
    if m:
        lvl=len(m.group(1)); txt=m.group(2)
        if lvl==1 and skip_first_h1:
            skip_first_h1=False; i+=1; continue
        h(doc, min(lvl,3), txt); i+=1; continue
    if s.startswith("|"):
        rows=[]
        while i<len(lines) and lines[i].strip().startswith("|"):
            rows.append(lines[i].strip()); i+=1
        md_table(doc, rows); continue
    mb=re.match(r"^-\s+(.*)$", s)
    if mb:
        items=[]
        while i<len(lines) and lines[i].strip().startswith("- "):
            items.append(lines[i].strip()[2:]); i+=1
        for it in items:
            p=doc.add_paragraph(style="List Bullet")
            p.paragraph_format.space_after=Pt(2); p.paragraph_format.line_spacing=Pt(13)
            add_inline(p, it, base_size=10)
        continue
    mn=re.match(r"^(\d+)\.\s+(.*)$", s)
    if mn:
        items=[]; expect=1
        while i<len(lines):
            mm=re.match(r"^(\d+)\.\s+(.*)$", lines[i].strip())
            if not mm or int(mm.group(1))!=expect: break
            items.append(mm.group(2)); expect+=1; i+=1
        numid=make_numid(doc)
        for it in items:
            p=doc.add_paragraph()
            p.paragraph_format.space_after=Pt(2); p.paragraph_format.line_spacing=Pt(13)
            p.paragraph_format.left_indent=Mm(7); p.paragraph_format.first_line_indent=Mm(-5)
            numpr(p, numid)
            add_inline(p, it, base_size=10)
        continue
    if s.startswith(">"):
        p=para(doc, s.lstrip("> "), size=9.5, color=INK400)
        p.paragraph_format.left_indent=Mm(8)
        for r in p.runs: r.font.italic=True
        i+=1; continue
    # paragraf biasa (serap baris lanjutUntil blank/head)
    buf=[s]; i+=1
    while i<len(lines):
        t=lines[i].strip()
        if (not t) or t.startswith("#") or t.startswith("|") or t.startswith("- ") \
           or re.match(r"^\d+\.\s", t) or t=="---":
            break
        buf.append(t); i+=1
    para(doc, " ".join(buf))

# ── RIWAYAT REVISI ──
doc.add_page_break()
h(doc, 1, "Revision History")
rows=[["Rev B","31-VIII-2026","Gap remediation per INTEGRATION_GAP.md: Hermes Workspace section (GAP-01), local-model section Ollama/llama.cpp + Four Ways to Buy Intelligence (GAP-02/03), V3 failure case box (GAP-04), self-improving revenue machine worked example (GAP-05), deploy step (GAP-06), memory-snapshot discipline (GAP-07), desktop-app install variant (GAP-12), domain-build pointers (GAP-14); citation-end drift normalized (GAP-13); plus four-rung recovery-ladder subsection in Module 2. Module grows 15,635 to 18,193 words; re-verified AC1-AC10 PASS.","Independent integration-gap audit","Content additions only; layout unchanged","Swarm (GSP)"],
      ["Rev A","31-VIII-2026","First complete Word course-module edition; content identical to the verified Markdown deliverable (VERDICT PASS, AC1–AC10). Layout upgraded to professional course body: cover, control table, TOC field, header/footer, PAGE/NUMPAGES, GSP typography.","Student request via Swarm controller","Presentation only — zero content change","Swarm (GSP)"]]
tbl=doc.add_table(rows=3, cols=6); tbl.autofit=False
widths=[14,24,64,28,24,16]
hdrs=["REV","DATE","CHANGE","TRIGGER","IMPACT","BY"]
for j,(txt,w) in enumerate(zip(hdrs,widths)):
    c=tbl.rows[0].cells[j]; c.width=Mm(w); set_cell_margins(c)
    style_run(c.paragraphs[0].add_run(txt), FS, 8.2, INK900, bold=True, caps=True)
for i,row in enumerate(rows):
    for j,(v,w) in enumerate(zip(row,widths)):
        c=tbl.rows[i+1].cells[j]; c.width=Mm(w); set_cell_margins(c)
        style_run(c.paragraphs[0].add_run(norm_em(v)), FB, 8.2, INK700)
table_grammar(tbl)

doc.core_properties.title="Hermes Agent Zero-to-Hero: An Integrated Learning Module"
doc.core_properties.author="PT. Gemilang Satria Perkasa — GSP Knowledge Production"
doc.core_properties.subject="Professional learning module (course body), Rev B"

# Q-T fix: Word auto-update fields (TOC terisi saat dibuka, dengan konfirmasi)
settings = doc.settings.element
uf = OxmlElement("w:updateFields"); uf.set(qn("w:val"), "true")
settings.append(uf)
# Q-P fix: sampul tanpa header/footer nomor halaman (different first page)
sec.different_first_page_header_footer = True

doc.save(OUT)
print("WROTE", OUT, os.path.getsize(OUT), "bytes")
