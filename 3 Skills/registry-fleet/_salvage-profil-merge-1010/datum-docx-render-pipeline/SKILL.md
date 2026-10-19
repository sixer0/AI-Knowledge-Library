---
name: datum-docx-render-pipeline
description: Use when building DATUM DOCX+PDF. COM and font pitfalls.
metadata:
  hermes:
    tags: [gsp, docx, word-com, fonts]
    category: devops
---
# DATUM DOCX -> PDF pipeline (validated DEMS-DATUM-0925, 26-09-2026)

Engine token source: `docs/2026-09-03-expo26-workbook-standard/scripts/build_contoh_datum_docx.py`
(functions style_run/fmt_para/spacer/para/cell_*/fix_table/tab_right/setup_section copied verbatim).
Working example: `docs/2026-09-25-dems-datum/scripts/build_laporan_datum_dems.py` +
`render_pdf_datum_dems.py` + `check_laporan_datum_short.py`.

## Commands
1. Build: `uv run --python 3.11 --with python-docx python scripts/build_laporan_datum_dems.py`
2. Render: `uv run --python 3.11 --with pywin32 --with pypdf python scripts/render_pdf_datum_dems.py`
3. Check: `uv run --python 3.11 --with python-docx --with pypdf python scripts/check_laporan_datum_short.py`

## Pitfalls found the hard way
- **Word COM export**: `Documents.Open(..., ReadOnly=True)` then `ExportAsFixedFormat` FAILS
  ("can't save, read-only"). Open with `ReadOnly=False, AddToRecentFiles=False`; still
  `doc.Close(False)` so the source file is never modified. Use `DispatchEx` for own instance.
- **Stale PDF**: delete target PDF before re-export, else success may be reported against old bytes.
- **PAGE/NUMPAGES fields**: after `Repaginate()`, update footer fields per section
  (`sec.Footers(i).Range.Fields.Update()`), then Repaginate again before ComputeStatistics(2).
- **IBM Plex not installed by default** on this machine (registry HKLM/HKCU Fonts empty).
  Per-user install pattern (no admin): copy ttf to `%LOCALAPPDATA%\Microsoft\Windows\Fonts`,
  write value "<Family> <Style> (TrueType)" -> filename under HKCU `...\CurrentVersion\Fonts`
  (open with KEY_WOW64_64KEY), then `AddFontResourceExW(path, 0, 0)` + broadcast WM_FONTCHANGE.
  Fleet ttf sources: `workspace/EXPO [2026]/Font_DATUM/` (SansCond Reg/SemiBold, Mono Reg/SemiBold),
  `gsp-hermes/skills/gsp-canvas-design/canvas-fonts/` (Serif full set, Mono Bold). SansCondensed
  *Bold* (true nameID1 "IBM Plex Sans Condensed") only from google/fonts GitHub raw:
  `ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Bold.ttf` (SemiBold files have family name
  "...SemiBold" = separate family, Word won't synthesize-bold-match them reliably).
- **Glifs ■◈◇△ have no glyph in IBM Plex**: Word falls back to Courier/CambriaMath at render
  (same as source exemplar CONTOH-DATUM). Keep run tokens MONO AMBER in XML - do NOT swap fonts.
- **XML audit**: `&` appears as `&amp;` in document.xml - unescape before verbatim-string grep.
- **MD parser traps** (naskah-komprehensif grammar): single-row `| SUMBER | refs |` tables must be
  dispatched BEFORE generic table rendering AND gated on `len(rows)==1` plus exact header cell
  `SUMBER` — a general table whose first header cell is "Sumber" (e.g. `Sumber|Tautan|Klaim`,
  15 rows) must NOT be swallowed by the SUMBER branch (RAFIF-V2 build lost it until gated); orphan continuation rows separated by up to 2 blank
  lines belong to the previous table (merge only if same col count and next is not `| SUMBER`);
  standalone `Tabel n.n Judul` lines carry the caption - pass (num, desc) tuple into ONE caption
  call, never as list-of-runs (python-docx flattens tuples into duplicated text like "7.1Rantai").
- **Void-tail before tall figures is structural** (validated 2026-10-06, t_3934fc55
  FIX-SA3B): a figure unit (image+caption+SUMBER, keepNext chain) taller than the
  remaining page space jumps whole and leaves the tail of the PREVIOUS page empty
  — Word sequential flow cannot fill it with text that comes after the figure.
  Shrinking the unit (portrait->128mm grid, one-line caption, allow break only
  between caption and SUMBER) reduced 7->5 pages but cannot reach 0 for ~500pt
  portrait units; a gate demanding void=0 on body pages needs either an agreed
  threshold exception or per-figure pageBreakBefore/floating anchors (decision
  belongs to the controller, not the worker).
- **Caption-regex sensors catch prose**: a `^(GAMBAR|Gambar)\s` caption detector
  also flags audit lines like "Gambar terpasang 53 dari ..." — false
  "caption-without-figure". Anchor the sensor to the machine caption format
  (`^GAMBAR \d+\s`) or keep generated prose from starting with that word.
- **Numeric column role**: apply MONO right-align only when >=50% of cells match pure-number regex;
  mixed-text numeric-headed columns stay text role.
- **ensure_fonts() hard-fail**: check registry for "plex serif"/"plex sans condensed"/"plex mono"
  before building; raise, never silently fall back (V-3 prerequisite).
- **Body-row borders**: dump contract says body rows are pure sz4 C_HAIR bottom; do NOT add an
  sz5 closing border on the last row (invented deviation = anti-drift FAIL).
- **Zip-edit of theme1.xml must be whitespace-tolerant** (GM-H11b-R2, 08-10): python-docx's stock
  theme1.xml is pretty-printed (newline + 8-space indent), NOT minified. A literal replace of
  `'<a:minorFont><a:latin typeface="Cambria"/>'` never matches -> silent n=0, Word still embeds a
  Cambria subset via TOC minorHAnsi (symptom: font gate asing=['...+Cambria'] with zero printed
  glyphs). Use regex with `\s*` between tags and ASSERT match count == expected (fail-fast; a
  printed count alone was missed twice in gm_h11b_chain.log). Verify post-build by re-reading the
  part from the final artifact, not just the log.

- **Template-placeholder URLs become ACTIVE bad links** (validated 2026-10-10, t_496d0386 FIX-FINAL): a register row whose URL contains `<id>`/`{...}` (family prefix, not a real identifier) gets hyperlinked TWICE over — engine `_inline` (after adapter strips its backticks via `` re.sub(r"`(https?://...)`") ``) and `emit_fence`. Word percent-encodes to `Target="...%3cid"`, PDF carries a live Link annotation. Fix at BOTH call sites: skip hyperlinking when token matches `[<>{}]`, keep backticks so engine prints MONO plain text; gate on rels (`Target=` regex incl `%3[CcEe]`) + PDF link URIs; red-green against the prior era artifact (1 red vs 0 green proved teeth). F-A token count must exclude placeholder-adjacent tokens or the equality gate breaks by exactly the number of demoted URLs.
- **pdfgate reads output/build/*.pdf** — after render_word.py writes into work/build-pdf/, run the serah/pin sync BEFORE `build_rakit_rafif.py pdfgate`, else FileNotFoundError (hit twice in one run).
- **json.dump rewrites CRLF->LF**: sha256 of a reformatted JSON differs from the upstream claim even when content is identical; compare in text-normalized mode before declaring drift, and record both hashes honestly.
- **Word save STRIPS w:updateFields + datumcheck A2 flags TOC anchors** (validated 2026-10-10, t_7bd806e3 RAKIT-FIN):

  - (a) `updateFields` in settings.xml is a once-only flag — after COM Fields.Update+Save, Word removes it, so datumcheck A5 (G-DQ-12) FAILs post-repaginate; restore via zip-edit inserting `<w:updateFields w:val="true"/>` immediately before `<w:compat>` (schema order), preserving ZipInfo entries.
  - (b) `TOC \h` generates `w:hyperlink w:anchor="_Toc..."` with NO r:id; datumcheck A2 demands an external http(s) rel for EVERY hyperlink, so a legitimately-linked TOC always reads raw-FAIL — report A2 two-layer (raw tool verdict + external-class defect count computed separately: only r:id links lacking a valid http(s) rel count).
  - (c) Repaginate (Open ReadOnly=False, TOC.Update, Fields.Update, Repaginate, footer fields per section, Repaginate, Save) creates lastRenderedPageBreak traces that flip datum_lint DATUM-14 (per-page colour visibility) from false-red to PASS; re-run assert/register AFTER the Word save since the bytes changed.
- **QC-verdict gate for embedded figures** (validated 2026-10-10, RAKIT-FIN): build gates must cross-check each placed figure PNG's sha8 against verdict tables in verification/QC-*.md (parse table rows id+verdict+sha, order files by mtime so later reports supersede; rows without sha bind nothing). Attribution-card checks alone let a red-verdict byte ship (build-2 incident daa58d02).
- **Stale sibling PDF poisons docx gates**: datumcheck A6/A7 measure the PDF at `<docx-basename>.pdf`; an old-era PDF there both measures wrong bytes and can crash the CLI (registry TypeError bug when defects exist). Archive/move stale variants before running gates on the new object.

## Layout-gate pitfalls (validated 2026-10-06, t_c9443f56 FIX-SA2)
- **DatumDocx.figure() lineRule exact**: the engine sets `w:line exact` on the
  image paragraph (max(h_mm pt,2)); Word clips below-baseline space and pushes
  the caption 33-66pt below the image bbox. Fix at call site: after figure(),
  delete `w:line`/`w:lineRule` attrs from that paragraph's w:spacing and set
  jc=center — engine caption/SUMBER structure stays untouched.
- **Caption-gap measurement**: pymupdf `get_text("blocks")` bboxes include
  line-box padding ABOVE the baseline -> false "no-caption-below"/gap inflation.
  Use `get_text("dict")` and compare span `origin[1]` (baseline) vs image bbox
  y1. Same run: blocks-level said 0/53 ok, dict-level said 53/53.
- **datumcheck CLI crash on A6 non-clean** (RAFIF BUILD-PDF 10-10): run_cli prints
  `overflow=%s` but the detail tuple feeds `res["overflow_pages"]` where a list is
  fine — yet when PDF HAS defects a later `%d` on a list raises TypeError and kills
  the CLI before A7/A1. Workaround: driver script calling `datum_figur.battery(pdf)`
  + `datumcheck.audit_wrap_digit(pdf)` directly; report classes yourself. Registry
  bug -> propose fix to skill-manager.
- **F2 caption sensor blind for page-filling figures**: portrait figure unit
  (caption-above + image + SUMBER) taller than one body page pushes SUMBER to the
  NEXT page top; F2 reports "caption HILANG" though caption renders ABOVE (DT-15).
  Root fix belongs to the rakit adapter (shrink/split), not the renderer. A citation
  chip sitting ON a figure's top border registers as F3 overlap (~50 pt^2) — one
  spacer paragraph upstream clears it. Void-tail pages: declare via --allow-void.
- **Word COM serial two-variant render** (validated t_cbafb48b): ONE DispatchEx
  instance, loop variants sequentially (TOC.Update -> Fields.Update -> Repaginate ->
  footer Fields per section -> Repaginate -> ComputeStatistics(2) ->
  ExportAsFixedFormat(dst,17,False,0,0,1,1,0,True,True,1,True,False,False)); ~22 s
  per 199-page book; delete target PDF first. CreateBookmarks=1 => /Outlines count ==
  H1+H2+H3 style uses exactly; DocStructureTags=True => StructTreeRoot+Marked true,
  but /Lang stays 'en' (PDF/UA not fully claimed).
- **Cetak-variant zip surgery without touching source**: swap bg fill + ink hexes in
  document/styles/header/footer XML; gutter 0->+3 mm AND shrink w:right by the same
  twips to keep the text column in place; LANCZOS-resize PNG media whose placed dpi
  < 302 (pair wp:extent with r:embed). Assert pin(source)==pin(copy) before surgery.
- **Vision QC false alarm at low dpi**: rail chips ([S-xxx] mono small) between text
  lines read as corrupt glyphs ('Ãssistant') in compressed previews — zoom >=400 dpi
  crop before claiming a glyph defect.
- **scan_ai_footprint on PDF** requires pypdf importable IN THE GATE INTERPRETER
  (`--with pypdf`); without it the scanner silently falls back to latin-1 raw
  bytes and reports thousands of phantom U+00B7 findings (C-2 FAIL 25163).
- **Markdown pipe-in-code-span** (`\`GSP | 002/...\`` inside a cell) splits the
  row into extra columns -> ragged table. Rejoin extras into the content column
  before width solving.
- **G3 floor solver**: datumcheck G3 caps ~2.05 chars/mm at 3 wrapped lines;
  solve per-column min widths (binary search on `int(w*2.05)+8)*3 >= len`),
  promote table to full-span 166mm when floors exceed 128mm; totals must hit
  128/166 exactly (guard G2 tol 0.05mm). GridCol gate tolerance: allow 2 dxa
  rounding drift on totals.
- **datum_lint inherited trio** DATUM-06 (empty centered spacer paras from the
  engine's own cover), DATUM-16 ('0%' literal from verbatim body), DATUM-22
  (normative paragraph containing 'datasheet'+digit): compare lint output
  against the previous .cacat artifact before calling them regressions.

## Diagram pitfalls (validated 2026-10-09, t_559f107b FIGUR-1)
- **datum_diagram.py apparatus foot overlaps nodes**: engine draws KEY/caption/SUMBER
  at foot=H-2*LATTICE_Y but Sheet.height reserves only 2*LATTICE_Y below the last
  node -> with a non-empty `legend` the KEY line prints ON TOP of the bottom row.
  Caller-side fix (engine untouched): subclass Sheet.height +2*LATTICE_Y when
  legend non-empty (see docs/2026-10-09-rafif-manual-final-1009/work/figur1_diagwrap.py).
- **layout_graph col pitch unbounded**: x = col*4*LATTICE_X with no x+w<=sheet.W test;
  DATUM-37 then CLAMPS width instead of rejecting -> right column bleeds off-canvas.
  Fix in wrapper: dynamic pitch = min(4*LX, (W-maxw_lastcol)/(ncols-1)) + centering.
- **_node_size underestimates long `sub`** (graph family): text overruns box edge;
  shorten spec sub-text rather than fight the estimator.
- **pustakachart fig.text footer at y=-0.075 collides with legends placed via
  bbox_to_anchor below axes** — push footer further (fy≈-0.42) or place legend inside.
- **Numeric gates alone pass broken layouts**: run a vision inspection on at least one
  figure per family before claiming the shepherd green.

## Diagram-label & chart-collision pitfalls (validated 2026-10-09, t_b932e7ba FIX-FIGUR2-REREND)
- **datum_diagram v2.5.0 `_label_knockout` erases FOREIGN connectors**: the engine picks a
  label position then punches a paper rect over whatever is behind it — measured 92 events
  of a band deleting a segment of a connector that was NOT the label's own edge (class G7).
  Wrapper fix: search free-space positions along the edge's own polyline (fraction x
  perpendicular-offset ladder) BEFORE falling back to engine behavior; require the label's
  REAL ink box = union(text glyph box at baseline my-pt2mm(1.2), knockout band rect
  height 1.7*size anchored my-1.15*size) — testing only the text box leaves a ~0.65mm sliver
  where the band still eats lines.
- **matplotlib `Annotation.get_window_extent()` is NOT usable for collision tests**: with no
  arrowprops it returns the arrow-patch bbox (empty), so every candidate looks free and
  pierced-label defects survive silently. Measure glyphs with `TextPath` at
  `fontsize*dpi/72` and compute the display point yourself from anchor+offset*scale; store
  the chosen bbox on the artist (`t._fixbb`) for subsequent labels' obstacle lists.
- **Red-green the placer**: disable the collision test and rebuild — output bytes MUST
  change, otherwise the gate has no teeth and "labels clear" is unproven.
- **Long annotations in narrow gaps**: when no offset fits, wrap the text (verbatim content,
  line breaks only) and widen the candidate ladder; `bbox_inches="tight"` never clips, so an
  edge-touch pixel test cannot detect chart overflow — vision or axes-inset geometry must.
- **Calibrate any geometric defect-gate against prior human QC**: one known-clean artifact
  must score 0 false positives and known-dirty artifacts must name the same labels; build
  text metrics from real font files (fontTools hmtx), never from the engine's
  `est_text_mm = len*size*0.56` estimator (under-estimates IBM Plex Condensed -> R3 class).

## Verification pattern
CHECK V-1 reopen+sections+counts; V-2 XML token audit vs dump (fonts/tracking{30,28,16,12}/
w:line270 exact/border{10,5,4}/12 hex/margins <0.05mm/verbatim strings/PAGE fields);
V-3 COM pages == pypdf pages + BaseFont families present + footer NN/TOTAL extractable.
Print `CHECK n: PASS|FAIL` + `VERDICT:` and exit non-zero on FAIL.

## Sajian-gate pitfalls (validated 2026-10-07, t_d6715b08 VCTL SB)
- **C-14 false positive from ListBullet conversion**: md bullet blocks ("intro: - a. - b.")
  are ONE scanner sentence in md (dash blocks the `. X:` sentence splitter), but
  ListBullet style strips the dash in docx -> splitter cuts at every ". Label:" ->
  adjacent register-template entries become near-duplicate sentences (measured: md 1
  copy vs docx 17). Keep the literal "- " in the run text (indent+hanging still
  engine-styled); do NOT "fix" content upstream.
- **C-13 hard class after backtick loss**: md inline-code ticks vanish at render, so
  snake_case recipe/module names become bare prose. Sanctioned remedy = sajian-layer
  nat_label pass (H.4.6; precedents nat_label_pass DATUM, nat_label_visual f18) using
  the scanner's OWN regexes imported from scan_ai_footprint.py (no duplicate matcher).
- **openpyxl determinism**: wb.properties.modified is overwritten with save-time NOW
  regardless of what you set; freeze zip entry timestamps AND rewrite
  dcterms:modified in docProps/core.xml post-save for byte-identical two-run builds.
- **Cover wordmark clipped by seal band** is inherited DATUM-engine behavior (identical
  in DATUM 002 published PDF) — record as engine traceroot note, never hot-patch at
  the worker build (anti-drift contract).
- **Footer/header chrome edits must be measured post-Word-save** (GM-H15b, 08-10,
  t_35c72329): `DatumDocx._footer_register` prints `REV <rev>` in cell 2; to key it to
  an edition without touching the fleet engine, patch the built docx by zip-editing
  `word/footer*.xml` after `D.doc.save()` (same ZipInfo-preserving pattern as
  `_fix_theme_minor`), assert the replaced-part count >= expected, and gate on the
  PUBLISHED object. Two traps hit in one run: (a) Word's save SPLITS runs, so an
  XML-literal grep like `>REV </w:t>` or counting `EDISI v1.3` in raw XML reads 0 even
  when the text renders — strip tags (`re.sub(r"<[^>]+>","",xml)`) or read PDF text
  instead; (b) `doc.paragraphs`/`doc.tables` in python-docx EXCLUDE header/footer parts,
  so a "version label present" check over body text can never see footer chrome.
- **Longer footer label != taller footer**: widening a footer cell's text (e.g. `REV A`
  5 chars -> `EDISI v1.3` 10 chars) does NOT reflow the body if the cell still fits one
  line. Prove it before blaming a page-count regression: compare footer span baselines
  and body-bottom y per identical page across the two eras (they matched exactly at
  792.0/805.1/814.6 pt). Then attribute the page delta arithmetically: strip chrome,
  count reading characters per era, divide the delta by the book's own char/page density
  (2.622 char / 2.290 = 1.14 pages), and check WHERE growth concentrates vs which sections
  were edited — plus measure the predecessor's own artifact to prove the growth predates
  your patch.
