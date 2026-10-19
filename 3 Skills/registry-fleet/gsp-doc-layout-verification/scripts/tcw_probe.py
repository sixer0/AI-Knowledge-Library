# -*- coding: utf-8 -*-
"""tcw_probe.py - calibration probe for DATUM-published DOCX.

Prints inline-shape widths in mm (shape.width/36000) and per-table row-0 tcW sums in dxa.
Use on a KNOWN-GOOD artifact first: widths must be exactly {128.0, 166.0}; tenth-scale
flag rule is `total < 3000` dxa (no upper bound; 166mm spans reach ~9411).

Run: uv run --python 3.11 --no-project --with python-docx python tcw_probe.py <docx>
"""
import sys
from collections import Counter
from docx import Document
from docx.oxml.ns import qn

doc = Document(sys.argv[1])
print("inline widths mm:", sorted({round(s.width / 36000, 1) for s in doc.inline_shapes}))
buckets = Counter()
deviant = []
for i, t in enumerate(doc.tables):
    if not t.rows:
        continue
    total = 0
    for c in t.rows[0].cells:
        tcPr = c._tc.find(qn('w:tcPr'))
        if tcPr is None:
            continue
        w = tcPr.find(qn('w:tcW'))
        if w is not None and w.get(qn('w:w')):
            total += int(w.get(qn('w:w')))
    buckets[total // 1000] += 1
    if 0 < total < 3000:
        deviant.append((i, len(t.rows), len(t.rows[0].cells), total))
print("table count:", len(doc.tables), "| total-dxa buckets (k):", dict(sorted(buckets.items())))
print("tenth-scale suspects (<3000 dxa):", len(deviant))
for x in deviant[:20]:
    print("  suspect tbl", x)
