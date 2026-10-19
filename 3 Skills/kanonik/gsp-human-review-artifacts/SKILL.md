---
name: gsp-human-review-artifacts
description: "Use when making reviewable HTML/PDF artifacts for humans."
version: 1.0.0
author: Swarm GSP (curator)
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [gsp, artifact, html, pdf, naturalisasi, review]
    category: gsp
    related_skills: [gsp-output-naturalization, gsp-document-quality-standards, gsp-verification-before-completion]
---

# Human-Readable Review Artifacts (HTML + PDF) under the GSP Gate

Class of task: the user asks for a reviewable artifact summarizing fleet state,
standards, or gate history ("buat artifact html keterbacaan manusia", "minta versi
pdfnya"). This skill defines how to build, verify, and ship it so it passes the
naturalization gate AND is actually pleasant for a human to read.

## Hard rules (user corrections, do not renegotiate)

1. **Zero machine tokens when the user says no machine codes.** No check codes
   (C-nn/B-nn style), no clause/module numbers, no internal package names, no card
   ids, no tool jargon ("fixture", "registry", "sha256") — *not even parenthesized
   "for cross-reference" ones*. Preseden 30-09 R4-a: draf pertama memuat 28 kode
   inline dengan rasionalisasi silang-rujuk = pelanggaran instruksi tersurat, dicabut
   total. The "label or move to appendix" rule (H.4.6) applies to *unasked* leaks; an
   explicit ban means zero tokens in the body AND the glossary.
2. **Bright background, high contrast** (user taste 08-09): light palette from
   MASTER_DESIGN presets (BUSINESS/GENERAL); institutional identity via elements
   (thick rules, accent bars), never dark backgrounds.
3. **Narrative spine per Module H.3.5**: background → movement → a deliberately
   placed climax section → goals/next-steps. Include a plain-language wordlist
   (H.4.1) — this also satisfies the gate's glossary check without reintroducing codes.
4. **Single self-contained file**: zero external dependencies (no webfonts, no CDN).
5. **Print fidelity**: browsers strip background colors when printing. Embed
   `print-color-adjust: exact; -webkit-print-color-adjust: exact;` on every colored
   element (table headers, badges, rules) BEFORE producing the PDF.
6. **Numbers are re-measured, never recalled** (SPK-002 rule 9): versions, test
   counts, badge counts come from grep/count on live files during the session; prose
   claims must match the tables printed in the same document (preseden: prosa
   "sembilan pantauan" vs tabel 7 tertangkap audit).

## Procedure

1. Gather facts from live sources (skill frontmatter versions, `--selftest` count,
   Decision Log sections, git log for version history). Save scratch measurements.
2. Draft the HTML (structure per rules 2-4), then **run the gate on the artifact
   itself** with `--channel etalase`. Expect FAIL on your own drafts; FAIL returns to
   naturalization, never to delivery. Preseden: the recap of the gate's own fixes was
   rejected twice by the gate (short paragraphs, missing limitation admission) —
   fixing it is the proof the system is alive; say so plainly in the artifact.
3. Token sweep (regex + byte-level) before declaring done — see
   `references/render-verify-pdf.md` for exact commands.
4. Visual verify: headless Chrome screenshot with window height LARGER than the
   document, locate content end by scanning for the last non-background row, crop
   head/table/footer regions and inspect with vision.
5. PDF: same Chrome, `--print-to-pdf --no-pdf-header-footer`. Verify page count,
   real text layer (selectable text via pypdf), footer marker present, colors
   rendered (vision-check one table page).
6. Scan the PDF itself through the gate (`--channel etalase`). Length metrics are
   N/A on pdf by sweep-matrix design — the source format carries them; both verdicts
   belong in the delivery note.
7. Ship: write into the mission contract folder, mirror to repo
   (`hermes-home/workspace/docs/<kontrak>/`), verify sha256 identical, changelog
   pointer, commit + push (standing user policy).

## Pitfalls

- **Truncation blind spot**: a screenshot window shorter than the document silently
  cuts content, and "last row inside the window" checks cannot detect it (preseden
  30-09: window 7.000px vs tinggi nyata 9.546px). Re-render taller whenever content
  ends within ~100px of the window bottom.
- **pymupdf 1.28 API**: `Page.get_text()` and `doc.page_count`; `extract_text()` on
  a Page raises AttributeError.
- **Em dash / CJK sneak-in**: your own patches introduce U+2014 or stray CJK
  characters; run the byte sweep after every edit to an artifact, not just once at the
  end (multiple occurrences caught this way in one session).
- **Scanner version matters**: HTML artifacts scanned by scanner < v1.8.1 get false
  length verdicts (style/script counted as prose, table cells merged into one giant
  sentence). If metrics look absurd on an HTML file, check `__version__` first.
- **Gate on the final chat reply** (`--channel chat`) is separate from the gate on
  the artifact; both need traces.
- **Browser-use harness may fail to start** (daemon down); headless Chrome via
  terminal is the working fallback for screenshots and PDF, not a reason to skip
  visual verification.

## Scope boundary

Social-media analysis HTML deliverables are owned by `gsp-sosmed-html-insight`
(user policy 08-09); this skill covers general review/recap artifacts. The two are
complementary, not overlapping.

## Support files

- `references/render-verify-pdf.md` — exact command recipes: Chrome headless
  screenshot/print-to-pdf, content-end detection, token sweeps, pypdf/pymupdf
  verification snippets.
