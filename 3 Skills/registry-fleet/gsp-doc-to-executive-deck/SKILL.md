---
name: gsp-doc-to-executive-deck
description: Use when building an executive deck from source docs.
version: 1.0.0
author: Swarm (GSP)
license: MIT
tags: [gsp, deck, pptx, design-system, json-first, verification]
---

# Doc-to-Executive-Deck (JSON-first, DS-bound, verified)

## When to Use
- "buat N slide presentasi ke <eksekutif/instansi> dari file ini, pakai design system X"
- Deck must be content-complete for an executive audience and bound to a GSP
  master-design preset (bnn, polri, tni-ad, etc.), with JSON-first content.

Proven 2026-09-02: 20-slide BIN deck (WebLoc+Starlink, DS BNN), verdict PASS
after 5 countersign rounds. Mission trace:
`workspace/gsp-hermes/workspace/docs/2026-09-02-deck-bin-webloc-starlink.md`.

## Steps
1. **Extract sources.** docx: unzip `word/document.xml`, strip tags keeping
   `</w:tc>`/`</w:tr>` boundaries (tables carry the facts). PDF: pymupdf text
   layer; if chars/page ~0 it is image-based -> use the canonical preset token
   card in `gsp-design-system-grill/references/master-design/` instead, and say
   so honestly. Also extract `word/media/*` images and map embed order to
   "Figure N" captions before discarding them as assets.
2. **RT then TA dispatch** (controller must not translate or blueprint itself).
   Give RT the raw request + control list K1..Kn; give TA the translated
   contract + controller decisions file (lock every open Q explicitly).
3. **Freeze facts before writing slides.** Verify each number directly in the
   docx XML table cells (regex on `<w:tbl>`), e.g. payment terms may genuinely
   be a 3-row table totaling 100% with a missing 60% row - do not "fix" it,
   quote what exists. Never invent money figures absent from sources.
4. **JSON = single source of truth** (`slides_content.json`): deck_meta.chrome
   MUST declare footer/badge/page-number strings so the renderer hardcodes
   nothing; per-slide: chapter_label (with "NN / " prefix), title, kicker,
   layout enum, blocks (lead|bullets|table|compliance_table|metric_row|flow|
   quote_gold), metrics[] with source_ref, insight_highlight, source_refs[],
   speaker_note. Keep labels/titles byte-equal to the TA blueprint table.
5. **Render with python-pptx** at 1920x1080 px canvas via Emu(px*9525); palette
   only from the preset's 9 HEX; gold = attention token only. Layout rules that
   took iterations to get right (see Pitfalls): reserve band heights BEFORE
   placing tables (two-pass: compute natural heights, scale down to budget),
   two bullet blocks -> two full-width side-by-side panels, image frames sized
   to the photo (no empty matte), closing CTA box stretches to fill canvas.
6. **Export PNG previews via PowerPoint COM** (headless):
   `Presentations.Open(path,$true,$false,$false)` then `SaveAs(dir,18)` ->
   Slide{n}.PNG. This is the real render; python-pptx bounds alone miss table
   auto-growth.
7. **Deterministic gate (controller self-check) before claiming anything:**
   slide count == N; banned-term regex set == 0 across JSON + deck text +
   notes XML (casefold); U+2014/U+00B7 == 0 on all surfaces incl. entity
   decode; money-pattern == 0 unless sourced; srgbClr set in slide XML subset
   of preset palette, gold not top-1; overflow bounds == 0; table-x-text
   overlap >50% == 0; JSON-deck fidelity C-9 with legal transforms only
   (bullet "- " prefix, chip = value+2 spaces+label, chrome strings, header =
   chapter_label; casefold haystack joined by U+0001 sentinel to prevent seam
   matches).
8. **Independent countersign via HQ dispatch (gsp-verifier)** on frozen
   snapshots (copy artifacts to 05_verify/*.snapshot.* + record sha256[:16] in
   the prompt; verifier recomputes hashes). If FAIL: fix, re-snapshot, next
   round; keep hash chain in the contract doc.
9. **Visual QA loop:** dispatch gsp-image-analyst in batches of <=5 PNGs
   (single 20-image dispatch times out at RUN_TIMEOUT). If bridge vision fails,
   run vision_analyze per image from the controller instead - still real
   evidence. Vision misreads text sometimes: re-verify spelling claims against
   the JSON string before "fixing" (false positive: "Ketergantungan" reported
   as typo "Ketergantangan").
10. **Close trace:** kanban cards done with artifact evidence, contract doc
    chronology with per-round hashes, handoff copies + MEDIA links to user.

## Pitfalls
- Cards created without dependency edges get claimed instantly by idle workers
  (recurred 2026-09-02); audit artifacts per card before trusting status.
- Renderer drift: never type deck text in the render script; if chrome strings
  live only in code, fidelity check C-9 fails legitimately.
- python-pptx tables grow taller than assigned height when rendering: reserve
  ~52-62 px/row at 9.5pt and validate with the PNG export, not just EMU bounds.
- Metric chips at fixed y=CB-72 collide with tall tables (slide 18/19 case):
  compute flow/table heights from a budget that already subtracts mband+lead.
- Vision model may report HTTP 404 model_not_found transiently; retry once.
- Countersign rounds must test frozen snapshots, not live files, or a parallel
  worker edit invalidates the verdict (worker overwrote render_deck.py mid-mission).
- Lapis-render menyembunyikan cacat yang lolos ekstraksi teks (preseden DECK-ADINT-REVB-1016,
  16-10, verdict FAIL ronde-1 atas 3 kelas): (a) kartu KPI mencetak source_ref internal di
  wajah kartu padahal kontrak minta bersih ke catatan kaki — audit harus EKSTRAKSI TEKS PER
  BLOK + vision, bukan cuma 'angka hadir'; (b) blok visual_spec/figur yang dirute lewat
  kata-kunci teks bebas bisa jatuh ke jalur note sehingga 'figur dialokasikan outline' tidak
  pernah tergambar (panel kosong + caption palsu) — rute figur wajib lewat FIELD TERSTRUKTUR
  (kategori+nilai), dan gerbang bentuk menghitung marka bar per slide berfigur; (c) dua-pass
  anggaran ruang yang mem-break blok berlebih = kehilangan konten SENYAP — renderer wajib
  mencetak daftar blok terbuang/terkompresi ke stdout dan kompres via catatan kaki, tidak
  pernah diam. Vonis 'TERTUTUP' pada peta rekomendasi hanya sah bila ada bukti artefak
  (geometri/vision), bukan klaim patch notes (R-08/R-10 diklaim tertutup, ternyata tidak).
