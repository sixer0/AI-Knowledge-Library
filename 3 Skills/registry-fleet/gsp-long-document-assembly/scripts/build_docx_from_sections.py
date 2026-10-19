#!/usr/bin/env python3
"""Assemble ordered markdown section files into a styled A4 DOCX.

Proven workflow (Maiza knowledge summary, 61 pages, 46 tables, zero markdown
leaks). Edit the three CONFIG constants, then run with the venv python that
has python-docx installed.

Handles: # / ## / ### headings (page break before each top-level part),
pipe tables with shaded header row and zebra body (separator rows skipped),
**bold** and *italic* inline runs, blockquotes, numbered/bulleted lists,
footer page numbers.
"""
import re, os, sys
from docx import Document
from docx.shared import Pt, Inches, RGBColor
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# ---------------- CONFIG ----------------
BASE  = r"C:\path\to\sections"                      # dir holding the .md files
OUT   = r"C:\path\to\output.docx"                   # assembled document path
ORDER = ["sec_01_front.md", "sec_02_body.md"]       # assembly order
# -----------------------------------------

doc = Document()
for s in doc.sections:
    s.page_width, s.page_height = Inches(8.27), Inches(11.69)  # A4
    s.left_margin = s.right_margin = Inches(1.0)
    s.top_margin = s.bottom_margin = Inches(0.9)

st = doc.styles
n = st['Normal']; n.font.name = 'Georgia'; n.font.size = Pt(10.5)
n.paragraph_format.space_after = Pt(6); n.paragraph_format.line_spacing = 1.15
rpr = n.element.get_or_add_rPr(); rf = rpr.get_or_add_rFonts()
rf.set(qn('w:eastAsia'), 'Georgia')
for name, size, color, before, after in [
        ('Heading 1', 17,   '1F3864', 18, 8),
        ('Heading 2', 13.5, '2E4A7D', 14, 6),
        ('Heading 3', 11.5, '3E5C92', 10, 4)]:
    h = st[name]; h.font.name = 'Georgia'; h.font.size = Pt(size); h.font.bold = True
    h.font.color.rgb = RGBColor.from_string(color)
    h.paragraph_format.space_before = Pt(before)
    h.paragraph_format.space_after = Pt(after)
    h.paragraph_format.keep_with_next = True

def add_runs(p, text):
    tokens = re.split(r'(\*\*.+?\*\*|\*[^*\n]+?\*)', text)
    for t in tokens:
        if not t:
            continue
        if t.startswith('**') and t.endswith('**') and len(t) > 4:
            r = p.add_run(t[2:-2]); r.bold = True
        elif t.startswith('*') and t.endswith('*') and len(t) > 2:
            r = p.add_run(t[1:-1]); r.italic = True
        else:
            p.add_run(t)

def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear'); shd.set(qn('w:fill'), hexcolor)
    tcPr.append(shd)

def flush_table(rows):
    if not rows:
        return
    ncols = max(len(r) for r in rows)
    header = rows[0] + [''] * (ncols - len(rows[0]))
    t = doc.add_table(rows=len(rows), cols=ncols)
    t.style = 'Table Grid'; t.alignment = WD_TABLE_ALIGNMENT.CENTER
    for j, cellv in enumerate(header):
        c = t.cell(0, j); c.text = ''
        p = c.paragraphs[0]; add_runs(p, cellv.strip())
        for r in p.runs:
            r.bold = True; r.font.size = Pt(8.5)
            r.font.color.rgb = RGBColor.from_string('FFFFFF')
        set_cell_bg(c, '2E4A7D')
    for i, row in enumerate(rows[1:], 1):
        row = row + [''] * (ncols - len(row))
        for j in range(ncols):
            c = t.cell(i, j); c.text = ''
            p = c.paragraphs[0]; add_runs(p, row[j].strip())
            for r in p.runs:
                r.font.size = Pt(8.5)
            if i % 2 == 0:
                set_cell_bg(c, 'EDF1F7')
    sp = doc.add_paragraph(); sp.paragraph_format.space_after = Pt(2)

first_h1 = True
for fname in ORDER:
    text = open(os.path.join(BASE, fname), encoding='utf-8').read()
    tbl = []
    for ln in text.split('\n'):
        s = ln.rstrip()
        if s.startswith('|') and s.count('|') >= 2:
            if not re.match(r'^\s*\|?[\s:\-\|]+\|?\s*$', s):   # skip |---|---|
                tbl.append([c for c in s.strip().strip('|').split('|')])
            continue
        else:
            flush_table(tbl); tbl = []
        if not s.strip() or s.strip() == '---':
            continue
        if s.startswith('# '):
            if not first_h1:
                doc.add_page_break()
            first_h1 = False
            h = doc.add_heading(level=1); add_runs(h, s[2:])
        elif s.startswith('## '):
            h = doc.add_heading(level=2); add_runs(h, s[3:])
        elif s.startswith('### '):
            h = doc.add_heading(level=3); add_runs(h, s[4:])
        elif s.startswith('> '):
            p = doc.add_paragraph(); p.paragraph_format.left_indent = Inches(0.4)
            add_runs(p, s[2:])
            for r in p.runs:
                r.italic = True; r.font.size = Pt(10)
        elif re.match(r'^\d+\.\s', s):
            p = doc.add_paragraph(style='List Number')
            add_runs(p, re.sub(r'^\d+\.\s', '', s))
        elif s.startswith('- ') or s.startswith('* '):
            p = doc.add_paragraph(style='List Bullet'); add_runs(p, s[2:])
        else:
            p = doc.add_paragraph(); add_runs(p, s)
flush_table(tbl)

for sec in doc.sections:                       # footer page numbers
    fp = sec.footer.paragraphs[0]
    fp.alignment = 1
    fld = OxmlElement('w:fldSimple'); fld.set(qn('w:instr'), 'PAGE')
    run_el = OxmlElement('w:r'); t_el = OxmlElement('w:t'); t_el.text = '1'
    run_el.append(t_el); fld.append(run_el)
    fp._p.append(fld)

doc.save(OUT)
words = sum(len(re.findall(r"[A-Za-z0-9'\u2019\-]+",
              open(os.path.join(BASE, f), encoding='utf-8').read())) for f in ORDER)
print("saved", OUT, "| total words:", words)
