# Sensor calibration worked example (VCTL-1007, 2026-10-07)

Battery: `docs/2026-10-07-vctl-chart-catalog/verification/qa_final_vctl.py` (13 checks on
published docx+pdf+xlsx) plus three selftests `qa_sensor_selftest*.py` in the same folder.

## Known-good calibration targets (real fleet artifacts)
- DOCX: `docs/2026-10-06-visual-instrument/serah/STD-VISUAL-001-GSP-STD-X-2026_RevA.docx`
  -> inline widths must read exactly {128.0, 166.0} mm; 91 tables, devian must be 0.
- PDF: `docs/2026-10-06-visual-instrument/serah/LAPORAN-HASIL-VISUAL-1005.pdf`
  -> 4 pages, 3 images, overflow 0, caption 'Gambar' within 0-30 pt below every image.
- XLSX: `docs/2026-09-21-expoworld-1026/output/EXPOWORLD-1026-registri-master-SAJI-RevD.xlsx`
  -> header Consolas 11 bold white FFFFFF on fill 0F2A4A, freeze A2, 350/350 hyperlinks
  underline-styled. Use these as the green case for STD-SAJI-001 style checks.

## False-positive chain caught (each fixed before convicting the product)
1. EMU constant 360000 (wrong) vs 36000 (right): good artifact showed 10x-small widths.
2. gridCol-based table width probe: DATUM writes no tblGrid, so all 91 tables read total=0.
3. Upper bound 8200 dxa in tenth-scale detector convicted a legitimate 9410-dxa full-span
   table (table81 of the good artifact). Rule: flag only `total < 3000`.
4. Red fixture appended a second w:tcW after python-docx's default 4320 element; the
   reader took the default and the synthetic defect went undetected. Fix: find existing
   tcW and `.set()` its w:w attribute.

## Run recipe
```
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --no-project \
  --with python-docx --with pymupdf --with openpyxl python qa_final_vctl.py \
  <docx> <pdf> <xlsx> <manual.md> <catalog.csv>
```
Checks: figure widths 128/166 only; tenth-scale (tcW<3000); tblHeader repeat on >=6-row
tables; inline count == PNG count on disk; PDF overflow; caption-under-figure >=95%;
void diagnostic (NR, not FAIL); konten-kekal N==csv==md-subseksi==VC-in-docx; numbered
figure references; A1/A2 zero in prose (apparatus glif excepted); xlsx rows+freeze+link
style; manifest sha256[:16] vs disk. Exit 1 only on FAIL; NR printed separately.

## pymupdf notes
`import fitz` still works (deprecation warning only). get_image_info() bbox is in pt on
page.rect; compare with x1+3 tolerance per skill runbook. Vision pass still required:
geometry green while crops/voids remain visible to a human is a known failure mode.
