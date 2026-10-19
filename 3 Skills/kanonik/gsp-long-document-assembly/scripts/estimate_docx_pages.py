#!/usr/bin/env python3
"""Estimate printed page count of a DOCX without Word/LibreOffice.

Use when the user demands "minimum N pages" and no converter is installed.
Word COM (pywin32) and soffice --convert-to pdf are the exact-count paths —
try them first if present. Otherwise this walks the body in order, sums
estimated element heights against the A4 text block, and adds explicit page
breaks. Accuracy on a Georgia 10.5pt prose+table doc: estimated 61 pages,
consistent with the assembled layout.

Edit PATH then run. Prints height, flowing pages, breaks, ESTIMATE, stats.
"""
import re
from docx import Document
from docx.table import Table
from docx.text.paragraph import Paragraph

PATH = r"C:\path\to\document.docx"
PAGE_W_IN, PAGE_H_IN = 8.27, 11.69
MARGIN_TB, MARGIN_LR = 1.8, 2.0            # top+bottom, left+right
TEXT_W = PAGE_W_IN - MARGIN_LR
TEXT_H = PAGE_H_IN - MARGIN_TB
PT = 1 / 72

doc = Document(PATH)
body = doc.element.body

def para_height(p):
    txt = p.text
    if not txt.strip():
        return 0.0
    style = p.style.name
    if style == 'Heading 1': fs, bold, sb, sa = 17, 1, 18, 8
    elif style == 'Heading 2': fs, bold, sb, sa = 13.5, 1, 14, 6
    elif style == 'Heading 3': fs, bold, sb, sa = 11.5, 1, 10, 4
    else:
        fs = max((r.font.size.pt for r in p.runs if r.font.size), default=10.5)
        bold, sb, sa = 0, 0, 6
    ind = p.paragraph_format.left_indent.inches if p.paragraph_format.left_indent else 0
    usable = TEXT_W - ind
    cw = fs * (0.53 if bold else 0.50) * PT     # avg glyph width, Georgia mixed
    cpl = max(int(usable / cw), 1)
    lines = max(1, -(-len(txt) // cpl))
    return sb * PT + lines * (fs * 1.18 * PT) + sa * PT

def table_height(t):
    ncols = len(t.columns)
    colw = TEXT_W / max(ncols, 1)
    total = 0.0
    for row in t.rows:
        maxlines = 1
        for cell in row.cells:
            txt = cell.text.strip()
            cw = 8.5 * 0.52 * PT
            cpl = max(int((colw - 0.10) / cw), 1)
            maxlines = max(maxlines, (-(-len(txt) // cpl)) if txt else 1)
        total += maxlines * (8.5 * 1.15 * PT) + 2 * (2 * PT)
    return total + 3 * PT

heights = []
for child in body.iterchildren():
    tag = child.tag.split('}')[-1]
    if tag == 'p':
        h = para_height(Paragraph(child, doc))
    elif tag == 'tbl':
        h = table_height(Table(child, doc))
    else:
        h = 0.0
    heights.append(h)

total_in = sum(heights)
pb = open(PATH, 'rb').read().decode('latin-1').count('w:type="page"')
pages_flow = total_in / TEXT_H
print(f"total content height: {total_in:.1f} in")
print(f"text block per page : {TEXT_H:.2f} in")
print(f"flowing pages       : {pages_flow:.1f}")
print(f"explicit page breaks: {pb}")
print(f"ESTIMATED PAGES     : {pages_flow + pb:.0f}")
words = sum(len(re.findall(r"[A-Za-z0-9'\u2019\-]+", p.text)) for p in doc.paragraphs)
print(f"prose words: {words}, tables: {len(doc.tables)}, "
      f"table rows: {sum(len(t.rows) for t in doc.tables)}")
