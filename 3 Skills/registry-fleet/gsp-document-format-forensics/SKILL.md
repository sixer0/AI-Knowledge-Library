---
name: gsp-document-format-forensics
description: Use when auditing DOCX/XLSX/PDF formatting with evidence.
version: 1.0.0
author: Swarm (GSP controller)
license: MIT
metadata:
  hermes:
    tags: [gsp, docx, xlsx, pdf, verification, datum]
    category: analytics-and-reporting
---

# Document Format Forensics (DATUM fleet)

## When to use
- Auditing whether documents actually follow a design standard (DATUM, STD-SAJI,
  master-design presets), or building an inventory/analysis of styled outputs.
- Verifying a worker's formatting claims against the real bytes (claim ≠ file).
- Spot-checking release gates: font drift, palette drift, glyph fallback, structure gaps.

Validated 2026-10-03 (misi DATUM-GUIDELINE-1003: 235-file DATUM inventory + 21-artifact
forensic dissection). See `references/forensic-recipes.md` for exact commands and
`scripts/inventory_spotcheck.py` for the seeded table verifier.

## Core rules
1. **Measure, never vibe.** Every format claim must trace to a grep/regex over
   `word/document.xml`, `word/styles.xml`, `xl/styles.xml`, or PDF `/BaseFont` bytes.
   A claim with no dump citation is not a finding.
2. **On-disk wins.** Compare `stat -c "%s"` against the size/byte claims in the report
   before trusting any table row; re-verify after any regeneration (see skill
   `gsp-controller-delegation-ops` artifact-race protocol).
3. **Cross-check against the frozen engine tokens**, not memory of them. DATUM canonical
   token source: `docs/2026-09-03-expo26-workbook-standard/scripts/build_contoh_datum_docx.py`
   (15 tokens: IBM Plex Serif/Sans Condensed/Mono; INK 14110F, MAROON 6E1420, CREAM F6E9E9,
   WARMGRAY 7A756E, SUBJ 33302C, HAIR_W C4BEB4, C_INK 101418, C_SLATE 6B7783, C_BODY 2B3640,
   C_HAIR C3CBD1, AMBER B45309, RED 9B1C1C; CONTENT_W_PT 470.55). Legacy fallback stack
   gsp_lib.py (31-08): Segoe UI Semibold / Georgia / Consolas + teal VERD 2F6F6B.
   Both stacks legitimately exist in the corpus — label which one each artifact uses.

## High-yield detection patterns (all proven this session)
- **Font-stack drift:** `unzip -p docx word/document.xml | grep -oE 'w:ascii="[^"]+"' | sort | uniq -c`
  → reveals Arial/Calibri intruders inside "DATUM" docs.
- **Foreign palette:** same dump, `grep -oE 'w:val="[0-9A-F]{6}"' | sort | uniq -c`;
  any hex outside the frozen token list = local-palette defect (G-DESAIN FAIL class).
- **Glyph blind-render:** role glyphs ■◈◇△ have no glyph in IBM Plex; PDF companion proves
  substitution — regex `/BaseFont\s*/([A-Za-z0-9+\-]+)` over raw PDF bytes; presence of
  `CourierNewPSMT`/`CambriaMath` next to `IBMPlex*` = confirmed fallback defect.
- **Engineering-grade gaps that read cheap:** `w:tblHeader` (repeat header row) count vs
  total `<w:tbl>` count; field `SEQ` count (auto captions); `numPr` count (style-based
  numbering — DATUM writes "BAB 1" as literal text); approval/ttd block presence;
  core.xml default-python-docx metadata leak (provenance unauditable).
- **Size-unit trap:** DOCX `w:sz` is half-points — body 9.5pt = val 19, 8.0pt = val 16.
  Grep `w:sz w:val="1[456]"` to catch undersized-body regressions.
- **U+00B7 exception:** middle dot is FORBIDDEN in user output generally, but is a
  controlled separator inside DATUM ribbon/pita verbatim blocks — do not flag those.

## Verifying a worker's inventory table (controller-side, deterministic)
Run `scripts/inventory_spotcheck.py <INVENTORY.md> [--seed N]`: parses table rows, stats
every path, compares claimed byte sizes/sha prefixes to disk, prints PASS/FAIL per check +
VERDICT line. Seeded random sample ≥15 rows for byte claims, ≥3 for sha256 prefixes.
This is how the 235-row inventory was independently confirmed (235/235 paths, 15/15 bytes,
3/3 sha) — reuse it for any SPK-002 gate on tabular deliverables.

## Pitfalls
- `strings` binary absent in git-bash — use python `re` over raw PDF bytes instead.
- `&` appears as `&amp;` in document.xml — unescape before verbatim-string greps.
- Row numbers in a regenerated inventory shift — remap downstream consumers by path/sha8.
- PDFs with subset-embedded fonts can negative-grep for "IBM Plex" while the DOCX twin is
  positive; test the DOCX as primary evidence, PDF as render evidence.
- A `tail`/`head` pipe masks hermes CLI failure exit codes — re-run unpiped when output
  contains error text.
