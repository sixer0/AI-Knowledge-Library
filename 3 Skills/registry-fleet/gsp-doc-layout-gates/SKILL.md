---
name: gsp-doc-layout-gates
description: Use when emitting or auditing DOCX/PDF layout quality.
version: 1.1.0
metadata:
  hermes:
    tags: [gsp, documents, verification]
    category: gsp
---

# Document Layout Gates (DOCX/PDF emitted-object verification)

Class of task: producing or checking professional DOCX/PDF deliverables (DATUM-format
documents, manuals, reports with figures and tables). Born from a three-round user
rejection chain on 06-10-2026 ("hasilnya cacat" -> "masih berantakan"): each round a
different layout layer was broken while the previous gate passed, because every gate
measured the SOURCE asset instead of the EMITTED object.

## Canonical thresholds (pointer, do not duplicate)

Form thresholds live in one house each: DATUM tokens.json + `datum-house-style`
(grid 24/128/6/32/20, widths 128/166 mm, hair floor 0.18 mm, caption ABOVE for
DATUM tables per DT-15; STD-VISUAL-001 revD puts figure captions BELOW objects -
open collision logged 08-10 as T-09, awaiting controller ruling; until ruled,
DATUM docs follow DT-15 and visual-standard artifacts follow SV-TAB-04. PUTUSAN USER 08-10: DT-15 caption ABOVE wins for all DATUM documents - measured on the published manual (captions sit 2-12 pt above every image bbox, pages 19/50/54); STD-VISUAL must adopt ABOVE at its next revision.)
Figure placement gate is now automated: `datum_figur.py` (ENH-E battery: overflow,
caption<=40pt, word-level overlap, void) runs inside `datumcheck.py` as CHECK A6.
`figure()` uses line_rule=auto + keepNext since v2.1.0 (ENH-C): exact-height lines
made Word paint images over preceding paragraphs (EOSADINT RevB pages 11/15/29).

## Core doctrine (three rules)

1. **Measure the emitted object.** A figure file can be a perfect 166 mm @300 dpi and
   still be placed 1660 mm wide in the docx or overflow the pdf page. Gates must parse
   the built docx/pdf: inline-shape widths, table grid columns, image bboxes vs page
   rect, caption proximity, vertical gaps.
2. **Never hand-roll a layout builder for standard formats.** Two independent unit bugs
   in one builder in one session (`Cm(w_mm)` treating mm as cm -> 10x wide; column width
   in pt written as dxa without x20 -> tables collapsed to 1/10 width, header words
   broken one letter per line). Use the canonical engine (fleet registry
   `datum-house-style`: datum_docx.py + tokens.json + datum_lint 38 checks); an adapter
   may only MAP STRUCTURE to the engine API, never set units/widths by hand.
3. **Fix the sensor before judging with it.** The first audit script flagged 113
   "overlaps" and 52 "missing captions" that were mostly sensor bugs (searched
   lowercase `Gambar` while the document prints `GAMBAR`; counted the caption block as
   "text overlapping its own image"). After fixing, real defects were different and
   fewer. Never relay raw first-pass sensor output to a verdict or to the user.

## Measurement constants (verified)

| Quantity | Formula | Source |
|---|---|------|
| docx inline shape mm | `shape.width / 36000` (EMU) | python-docx |
| docx table column mm | `int(gridCol/@w:w) / 56.69` (dxa; 1440 dxa = 25.4 mm) | `tbl._tbl.find(qn('w:tblGrid'))` |
| correct dxa from pt | `pt * 20` | OOXML |
| pdf body zone | exclude `y1 < 70pt` (header) and `y0 > H-60` (footer) | pymupdf bboxes |
| caption placement | caption block top within 0-30 pt BELOW image bbox bottom, horizontally overlapping, SAME page | pymupdf text blocks |
| page counts | Word COM `ComputeStatistics(2)` and pymupdf `page_count` can differ by ~2; record both, declared | lesson F18 |

## Gate catalog (what "rapi" means, testable)

- C-lebar: every inline shape width in allowed token set (e.g. 128/166 mm +/- 0.6),
  plus a registered exception list (logo, hairline rules).
- C-kolom: no table column below ~9.5 mm except registered ID columns; per-table
  grid total equals the engine's content width.
- C-bbox: zero image bboxes crossing page margins; zero image-vs-text overlaps
  EXCLUDING caption/SUMBER blocks of the same figure.
- C-caption: 100% body figures have their caption on the same page, directly below
  (keepNext chain: image -> caption -> SUMBER must stay together).
- C-void: no page with figures carrying >25% empty vertical band (figure pushed whole
  blocks down; fix row-break/keep settings, not content).
- C-split: table spanning a page break repeats its header row; no table shows fewer
  rows than its caption claims without a continuation header.
- C-crop-chrome: evidence crops must exclude the source document's own header/footer
  bands (foreign "LEMBAR n DARI m" inside a figure reads as identity corruption).

## Word COM recipes

- `Dispatch("Word.Application")` can return "Call was rejected by callee" while another
  worker holds Word. Fix: `DispatchEx` (own instance), `ReadOnly=True` open, retry loop
  with sleep. Do not conclude COM is broken.
- Export PDF via `ExportAsFixedFormat(dst, 17)`. NEVER open-save the final release docx
  in Word afterwards (re-save mutates it - standing fleet lesson).
- Scanner over PDF text layer needs the pypdf dependency recipe
  (`--with pypdf`), else it honestly returns NEEDS_REVIEW fallback - not an artifact fail.

## Delivery rules (user-facing)

- MEDIA paths with SPACES break chat attachment rendering (user: "tidak semua hasil
  bisa saya buka"). Keep canonical filenames, but always also place an underscored copy
  under `serah/` and present THAT path.
- WebUI `/api/media` serves ONLY files inside an allowed root: HERMES_HOME, ~/.hermes,
  /tmp, and the session's ACTIVE WORKSPACE (`get_last_workspace`; see the
  `[Workspace::v1: ...]` tag on every user message). Mission folders outside the active
  workspace (e.g. shared `workspace/gsp-hermes/...`) return 403 "Path not in allowed
  location" and the browser shows "file wasn't available on site" (preseden PSIKOTES-1008
  09-10, traceroot gsp-brahma api/routes.py `_handle_media`). Rule: always copy release
  artifacts into `<active-workspace>/<slug>-serah/` (or HERMES_HOME) and present THAT
  path; keep sha256 parity check vs the canonical copy in the same turn.
- Re-saving a big-figure PDF via pymupdf garbage/deflate can grow it (~105%) when
  images are already optimally compressed - do not promise size reduction from it.
- When replacing a defective artifact, mark the old one (`.cacat`, `.cacat-2`) instead
  of deleting - it is audit evidence and doubles as teaching material.

## Verification workflow (red-green, mandatory)

1. Run the (fixed) audit + render 12-18 sample pages at 100 dpi BEFORE fixing; keep the
   red printout and PNGs.
2. Fix through the canonical engine only.
3. Re-run identical commands; attach before/after numbers and page renders to the result.
4. Vision-inspect rendered pages with pointed questions (tables proportional? caption
   under its figure? uniform spacing? clipped text?) - numbers alone miss voids and
   orphan captions.

Run the consolidated sensor: `scripts/layout_audit.py <docx> <pdf>` (checks above,
prints CHECK lines + VERDICT; exception lists are parameters). Condensed history and
orchestration side-lessons (pin ledger, one-writer-per-path): `references/fixsa-lesson-chain.md`.

## Related but distinct

`gsp-verification-before-completion` (VERIF-GATE, doc_gate_check.py) covers DATA and
LINK integrity of xlsx/docx (table values, hyperlinks, URLs). This skill covers LAYOUT
GEOMETRY. Apply both to released documents.
