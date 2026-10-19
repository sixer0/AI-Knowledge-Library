---
name: gsp-doc-layout-verification
description: Use when emitting or auditing DOCX/PDF layout quality.
metadata:
  hermes:
    tags: [gsp, verification, documents, docx, pdf]
    category: verification
version: 1.2.0
---

# Layout Verification of Published DOCX/PDF

## When to use
- You built or rebuilt a DOCX/PDF deliverable containing tables or embedded figures (reports, manuals, standards, sajian releases).
- A user or judge says the output is "berantakan" / messy / not professional and you must find the concrete defects.
- You are about to claim a document is "rapi", "final", or "terbit".

## Iron doctrine: measure the PUBLISHED OBJECT
The gate must inspect the built `.docx` and the rendered `.pdf`, never the source markdown, the builder's claims, or the asset manifest. Two real misses (2026-10-06): the manifest said figures were nominal extent while the docx placed them 10x too wide; a green C16 gate still produced pages the user correctly called broken. A claim of tidiness without fresh geometry prints from these checks = violation.

## Automation (ENH-E, 08-10)

Steps 1-2 of this runbook are now a shipped instrument: `datum_figur.py` in
`datum-house-style` measures the published PDF (word-level overlap, not block
level - block-level sensors produced false positives on 08-10 because Word text
blocks span figure columns) and `datumcheck.py` CHECK A6 calls it automatically.
The dxa divisor here was itself wrong until 08-10 (`/567` returns cm, correct is
`/56.69`); any sensor constant must be red-green tested before it convicts.

## Runbook
1. **DOCX structure (python-docx):**
   - `inline_shapes`: `width/36000` = mm. Every body figure must equal an allowed token width (e.g. 128/166 mm). Values exactly 10x nominal = `Cm(mm)` unit bug; values like 1660.0 = the classic `add_picture(width=Cm(166))` mistake.
   - Tables: `tblGrid` `gridCol` values are **dxa (twips, 1/20 pt)**: **mm = dxa/56.69**
     (1440 dxa = 25.4 mm), pt = dxa/20. Using `dxa/567` returns CENTIMETRES mislabelled
     as mm and makes every healthy 128 mm table look tenth-scale (measured live 08-10:
     sensor v1 convicted 38/38 tables of EOSADINT before the divisor was fixed). Writing
     pt values into dxa yields tenth-scale tables whose label column wraps one character
     per line — the classic "Bidang" vertical-letter defect.
   - Tall tables (>=6 rows) that may split need `trPr/tblHeader` on the header row; count tables missing it.
2. **PDF geometry (pymupdf):**
   - Image overflow: `bbox[2] > page.rect.x1 + 3` (or left/bottom equivalents).
   - Caption-under-figure: caption block top within 0–30 pt below the image bbox bottom, same page; report percentage (target 100%).
   - Voids: on pages with body figures, measure distance from lowest content to footer band; >25% trailing void = flag (root cause usually keepNext chains or `cantSplit` on tall rows pushing whole blocks to the next page — check figure height first; a 33 pt figure with a 314 pt void is NOT a big-figure problem).
   - Overlap: image rect vs text blocks, EXCLUDING the figure's own caption/SUMBER blocks.
   - Page count: pymupdf `page_count` must match Word `ComputeStatistics(2)`; record both (they can legitimately differ by 1–2 during TOC convergence — report as declared delta).
3. **Vision pass (never skip):** render 8–18 sample pages at 80–100 dpi (include every previously defective page) and run a critical layout inspection per page. Geometry checks can pass while crops containing source-document header bars, inconsistent rhythm, or orphaned captions remain visible to a human.
4. Re-run the full battery after every fix; report red-before vs green-after numbers, not prose.

## Fix the sensor before you convict
Layout sensors produce false positives. Confirmed cases: case sensitivity (`GAMBAR` vs `Gambar`), register/appendix pages that legitimately contain the word "GAMBAR" inside table cells (cell text is content, not a caption), header/footer chrome counted as body, and regexes truncating paths at spaces. Before treating a FAIL as truth, run the sensor against one known-good page and one known-defective page; require red-green. A controller's own first-pass metric overstated a defect count (55 vs true 53) by counting healthy placements — claim counts only from a parser whose definition you tested.

## Word COM recipes
- `Dispatch("Word.Application")` raises "Call was rejected by callee" while another process holds Word; retrying Dispatch is useless. Use **`DispatchEx("Word.Application")`** (own instance) — worked first try in-session.
- Open source `ReadOnly=True`, export via `ExportAsFixedFormat(dst, 17)`, pages via `ComputeStatistics(2)`, then `Close(False)` + `Quit()`.
- Never open-and-save the released final DOCX in Word (re-pagination/style drift; standing ruling from the Unity manual mission).
- Remove `~$…` owner lock files after COM runs so they never ship in the release folder.

## Delivery pitfalls
- **MEDIA attachment paths containing spaces break delivery on some surfaces.** Keep the canonical (possibly spaced) name for provenance, but copy to a `serah/`-style folder with underscore-only names and link those copies; verify sha16 copy == original in the same breath.
- pymupdf `save(garbage=4, deflate=True, deflate_images=True)` can *increase* size when images are already optimally encoded (measured 105%). Measure before promising smaller files; discard the failed attempt and log why.

## Defect classes observed in the field
See [`references/sajian-fixsa-case.md`](references/sajian-fixsa-case.md) for the full red-green chain (numbers, commands, root causes). Summary: `Cm(mm)` 10x figures; pt-as-dxa tenth-scale tables; keepNext+cantSplit quarter-page voids; crops carrying source header/footer bars (fix the ASSET crop, never fabricate); captions orphaned across page breaks; split tables without repeated headers; caption text claiming N rows while the page shows fewer.

## Script
`scripts/layout_audit.py <docx> <pdf> [allowed_widths_mm_csv]` prints CHECK lines + VERDICT, exit 0 only when clean. Adapted from probes validated during the 2026-10-06 missions; sanity-run it once per environment against a known-good artifact before trusting its verdicts (sensor-first rule applies to this script too).

## Sensor calibration (VCTL-1007)

[`references/sensor-calibration-vctl.md`](references/sensor-calibration-vctl.md) + [`scripts/tcw_probe.py`](scripts/tcw_probe.py) (dinaikan apa adanya dari
satu-satunya salinan fisik di profil gsp-master01 oleh DUPSKILL-L3 kartu t_605e5f7c, 11-10-2026):
known-good calibration targets (DOCX widths harus {128.0, 166.0} mm; PDF caption 0-30 pt; XLSX
STD-SAJI gaya kepala), rantai positif-palsu yang tertangkap (EMU 360000 vs 36000; probe gridCol
buta saat DATUM tidak menulis tblGrid; batas atas 8200 dxa menvonis tabel rentang penuh 9410 yang
sah; fixture merah wajib `.set()` tcW yang ADA, bukan menambah elemen kedua), dan aturan
tenth-scale: flag HANYA `total < 3000` dxa tanpa batas atas. Jalankan probe pada artefak
known-good sebelum mempercayai vonisnya.

## Boundaries and overlaps
- Data/link integrity of document artifacts (cells, hyperlinks, URL targets) belongs to VERIF-GATE / `doc_gate_check.py` in `gsp-verification-before-completion`. Complementary: that skill proves the content is correct; this skill proves the page is tidy.
- Style/scanner gates (A1/A2, channel scans) belong to `gsp-output-naturalization`; run them alongside, not instead of, layout checks.
- Prefer canonical DATUM/machine builders over ad-hoc ones; an ad-hoc builder is itself a defect risk (two independent unit bugs shipped from one).
