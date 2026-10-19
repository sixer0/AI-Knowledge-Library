# Case chain: sajian STD-VISUAL revD, three repair rounds (2026-10-06)

Red-green numbers from the FIX-SA / FIX-SA2 / FIX-SA3(B/C) chain. Use as the
worked example when explaining why gates must measure published objects.

## Round 0 — release that shipped broken
- Builder: ad-hoc `f18_build_sajian.py` (NOT the canonical DATUM machine).
- Bug A: `add_picture(width=Cm(w_mm))` → figures placed at 10x nominal
  (1660.0 mm / 1280.0 mm). PDF overflow: 53/53 body images past right margin
  (3101–4178 pt over).
- Gate blind spot: C16 measured the manifest/source PNG extent (nominal) —
  green gate over a broken doc. Lesson: gates measure the PUBLISHED object.
- Controller metric bug: loose parser counted 55 "bad" inline shapes; strict
  definition gave 53. Always test the parser's definition.

## Round 1 — FIX-SA (symptom patch, still messy)
- One-line unit fix (`Cm(w_mm/10)`), rebuild via same ad-hoc builder.
- Verified: 53→0 bad widths; PDF overflow 53→0; pages 162→115 (figures no
  longer bleed).
- User verdict: "masih berantakan" — correct. Geometry pass alone missed:
  collapsed tables, rhythm, caption placement, crop chrome.

## Round 2 — FIX-SA2 (canonical rebuild)
- Root cause of table collapse: builder wrote pt values into dxa fields
  (`gridCol w="72"` = 3.6 pt). Six-field tables rendered 12.8 mm wide; label
  column wrapped per letter ("B/i/d/a/n/g"); long tables looked empty.
- Rebuild through DatumDocx v2.0.0 adapter (lint 38 + datumbind), zero manual
  widths. Result: all shapes 128/166 mm, tables proportional, 96 pages.
- Vision pass on rendered pages still found: quarter-page voids, orphaned
  GAMBAR captions on a page without their figure, crops carrying source
  header/footer bars, split tables without repeated headers, caption text
  claiming "baris 1-4" while the page showed 2.

## Round 3 — FIX-SA3 → 3B (C18 battery, 11 checks)
- Crop chrome fixed at the ASSET layer (re-crop script, two-run identical,
  manifest history) — never fabricate pixels.
- tblHeader added to tall tables; keepNext chains rebuilt so figure→caption→
  SUMBER stay together as one unit.
- C18 result: 9/11 PASS — caption-under-figure 53/53 = 100%, split-without-
  header 0, TOC converged (pass6==pass7), scanner clean, pages 93
  (pymupdf == ComputeStatistics).
- Remaining FAILs and their true roots:
  - CHECK-1 voids on 5 tail pages: NOT big figures — page 69 had a 33 pt
    figure with a 314 pt void. Root = cantSplit on tall rows + keepNext
    chains pushing whole blocks to next page. Fix levers: cantSplit=false +
    tblHeader repeat; break the keepNext chain at SUMBER→next-block boundary.
  - CHECK-4: sensor FALSE POSITIVE. Page 91 is an appendix register whose
    table cells legitimately contain the word "GAMBAR" — cell text is
    content, not a caption. Sensor v4 must scope caption candidates to blocks
    outside table cells in figure sections; prove red-green on page 91.

## Process lessons worth reusing
- A worker card that refuses to run downstream ("penahan gagal terverifikasi
  disk") while a gate is red is CORRECT behavior — endorse in comments, open
  the successor card with fresh levers, keep the blocked card as a trace.
- When a fixer exhausts its declared levers it must partial-handoff with the
  red baseline + ready builder, not silently widen the gate.
- Two writers producing divergent variants of one chapter (DAG promotion vs
  manual release collision): controller picks owner by measured quality
  (command-density metric), archives the other intact, books the process
  defect. Never merge prose blindly.
- `.cacat-N` suffix convention: mark defective artifacts as evidence trails;
  never delete, never ship alongside without the marker.
