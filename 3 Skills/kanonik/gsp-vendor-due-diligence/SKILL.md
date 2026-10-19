---
name: gsp-vendor-due-diligence
description: Use for vendor or person due diligence (uji tuntas) reports.
license: MIT
version: 1.1.0
metadata:
  hermes:
    tags: [gsp, procurement, due-diligence, research, orchestration]
    category: gsp
---

# Vendor Due Diligence (uji tuntas) — class pipeline

Derived from mission DD-VENNETEL-2609 (09-09): report on Venntel/Gravy Analytics +
person "Jessie", verdict BERSYARAT 60.95, verifier-gated DOCX delivered.

## When to use
- User asks "buatkan due diligence / uji tuntas" for a named vendor/company, optionally
  plus a named contact person, expecting a report (DOCX/Word default per user choice).
- Clarify BEFORE standing up the mission (3-question batch): (1) instrument/template vs
  filled report for one target, (2) output format, (3) rubric scope (general procurement
  GSP vs inherited ADINT D1-D5 vs sector-specific). If a person name appears, ask what
  it denotes (contact to trace vs typo vs separate company).

## Pipeline (phases, profiles, cards)
DAG: S0 baseline library + S1/S2 collect (parallel) -> S3 score -> S4+S5 write DOCX
(one card, one agent) -> S6 verify -> S7 vault proposal (only if PASS).
- Cards via `lad_card.py` with `--parents` AT CREATION (late links do not gate claims).
- Dispatch via `hq_dispatch_card.cjs <title> <profile> <prompt-file> <taskId> <agentId>`;
  success = stdout line `DISPATCHED id=` (never trust exit code when piped).
- Watch each wave with a background bash loop polling artifact existence on the CANONICAL
  path, `notify_on_complete=true`; typical ETAs measured 09-09: RT/TA pair ~5 min,
  collect cards 15-45 min, score ~3-15 min, DOCX write ~10-20 min.
- Worker closing a card `done` WITHOUT result is a known bridge bookkeeping pattern —
  reconcile from disk + the worker profile's state.db, not by re-dispatch.
- Legacy corpus hits (vault/ADINT) are HYPOTHESES ONLY: list them as H1..Hn in the raw
  request, require the collector to re-verify each against primary sources, and forbid
  legacy scores (e.g. an old 2.8/10) from appearing as verdicts.

## Rubric default (freeze in TA blueprint before scoring)
Five aspects, scale 0-100, weights: legalitas 25, finansial 15, teknis 20, mutu/K3 10,
kepatuhan 30. Anchor bands per aspect written into the blueprint (90-100 clean ... 0-29 barred).
Rules:
- EVIDENCE-INSUFFICIENT cap: aspect with < 2 primary REGISTER-BUKTI rows is capped at 50
  AND must carry the visible label in the report.
- Verdict bands: LAYAK >= 70 and no aspect < 40 and no hard flag; BERSYARAT 55-69 or any
  aspect 40-54; TIDAK LAYAK < 55 or aspect < 40 or hard flag (debarment/sanction/fraud);
  INCOMPLETE-EVIDENCE when > 30% of release-load fields empty/unverified.
- Hard-flag check (US vendors): SAM.gov exclusions probe is a REQUIRED rung before any
  final verdict — see references/sam-gov-debarment-probe.md. If FOUND, verdict flips to
  TIDAK LAYAK automatically.
- Borderline threshold readings: the worker must NOT pick the reading — escalate as
  "KEPUTUSAN DIBUTUHKAN"; controller decides, records in Decision Log, and ALL readings
  (raw/conservative/scoped percentages) must be disclosed verbatim in the report.
- Controller recomputes the weighted arithmetic independently (parser, delta must be 0)
  before promoting the score card.

## Evidence gates (SPK-002, non-negotiable in prompts)
- Every published field: REGISTER-BUKTI row (claim, URL, access timestamp, entity-match
  result, confidence) OR left empty + REGISTER-KOSONG. Empty beats wrong.
- Entity-match: identifier belongs to the target only if the name token appears in
  host/title/OG/body of official content; search-engine hits without the gate never enter
  the corpus.
- LADDER table: 8 search-path classes filled with URL/aksi + HTTP status + timestamp +
  result + decision; no "buntu" verdict without an account per rung.
- Report links must be real hyperlinks, styled (bold color + underline); builder/parser
  counts link-display defects, release blocked if > 0.
- Naturalization gate on final DOCX + chat reply: scan U+2014/U+00B7 = 0
  (scan_ai_footprint.py), numbers/names/citations content-preserving.

## Report shape (blueprint-locked, 10 parts)
Bab 0 sampul+identitas+TERBATAS; 1 ringkasan eksekutif+vonis; 2 metodologi+keterbatasan
cara; 3 profil korporat; 4 status hukum/regulator; 5 person (fenced); 6 lima aspek
(temuan, bukti, skor+dasar, bukti hilang, mitigasi); 7 skor gabungan+pita+rekomendasi
(bukan opini hukum); 8 register keterbatasan+KOSONG; LA register-bukti penuh; LB ladder
gabungan. Verify structure with python-docx parser: heading count, table count >= 6,
key-number presence (score, verdict word, threshold percentages, labels).

## Person-tracing guardrails
Given-name-only input => present as CANDIDATE entity-match with PROV ids + confidence per
field, plus an explicit sentence that the match to the user's intended contact CANNOT be
confirmed from public sources. Rejected candidates are logged (so downstream cannot reuse
them). A documented NEGATIF-RESULT block (paths tried + timestamps) is a valid outcome.
Never copy aggregator contact values; role attribution only. Full recipe:
references/person-tracing-recipe.md.

## Mode "Tanpa Orkestrasi" (explicit user directive 09-09)
User can direct that DD generation runs WITHOUT the card/orchestration pipeline: controller executes solo (payload JSON -> python-docx builder -> deterministic gates). Applies especially when cloning an EXISTING exemplar deck ("pelajari due diligence ini, untuk generate ..."). Even then, all SPK-002 gates stay mandatory (entity-match full population, link probe, naturalization scan, empty-beats-wrong). Design-contract rule still applies: dump the exemplar structure first (parser + XML: sections/margins/fonts/palette/fills/borders per block), lock anatomy per-item PERSIS/ADAPTASI/DIBUANG; visual drift complaints = diff vs dump first, restore the source system, never patch symptoms.
Working artifacts from the 09-09 study (4 exemplars, "DD Comprehensive Leadership Edition", GSP header/footer, 31 tables, Part I seksi 01-10 + Part II 11-20, rubrik D1-D5 30/25/20/15/10, KPI band EDF3F8/FDECEC, callout F4EEE2 border emas C8A45D, heading dua-run nomor emas + judul 17pt navy): C:/Users/TRIAL/workspace/DD-STUDI-TEMPLATE/KONTRAK-DESAIN-DD-COMPREHENSIVE.md + RESEP-GENERASI.md + dump/*.json (per-file paras/tables/styles). Two score systems must not be silently mixed: exemplar ADINT-fit score (e.g. Venntel 93/100 T1) vs procurement verdict (BERSYARAT 60.95) - present side-by-side labeled, or per user decision. Exemplar-sourced identifiers (e.g. CAGE/UEI) that our corpus never entity-matched must be re-gated before republication.

First solo run of this mode (09-09, DD-AZIRA-2609, target "Azira Sean"): produced DD_Comprehensive_Azira_Sean_Ott.docx via builder triple (scaffold+content1+content2 concatenated). Builder pitfalls proven: (1) python-docx hyperlinks need `r:id` namespace attr (w:id breaks Word rel resolution - gate counted 0 links); (2) published links must survive a plain-browser GET probe (sec.gov Archives 403s normal UA while data.sec.gov/efts accept contact-UA - link the efts query URL instead); (3) scan_ai_footprint B8 needs a limitation keyword ("limitation"/"keterbatasan") inside measurable prose for English docs; (4) keep the whole artifact English (sweep an Indonesian token list post-build); (5) Part II headings use "NN." dotted style vs Part I "NN " double-space.

Gates all green: 19/19 links live, 0 display defects, U+2014/U+00B7 = 0 across all XML parts, score recompute delta 0. Trace: docs/2026-09-09-dd-azira-tanpa-orkestrasi/contract.md.

## Pitfalls
- **Worker writes to typo'd sibling folder** (real case 09-09: `docs/...-dd-vennetel-jessie`
  with double-n while the canonical folder had one n; card closed done-without-result and
  the canonical-path watcher would have timed out). Recovery: `find docs -maxdepth 1 -newermt
  <mission-start>` for sibling dirs; replay the worker profile's `state.db`
  (`messages.tool_calls` -> write_file args) to see the REAL paths written; move artifact to
  canonical, delete typo dir (verify 0 remaining), comment the trace on the card. Prevention:
  put the full absolute canonical output path in every collect card body, and have the
  worker's self-check stat the canonical path before closing.
- **Primary-source PDFs behind bot walls**: guessing direct ftc.gov PDF URLs returns 404;
  download from the docket page's own file links, or a documented mirror (e.g. aclum) marked
  P (mirror) in the register — mirror status must be disclosed.
- **Terminal hardline**: nested `$(...)` inside a `sed` range argument is blocked as an
  oversized/unparseable payload; compute the line number in a separate call, then sed with
  the literal number.
- **Attacker/vendor numbers stay claims**: e.g. a breach size claimed by an attacker is
  recorded as claim-not-verified even when the incident itself is verified from the
  company's admission; figures inside regulator documents are cited as document quotes.
- **done-without-result reconciliation**: query the bridge DB (`AgentRequest` by
  `hermesTaskId`) via node+pg from `gsp-datacenter/hermes-bridge/node_modules`, and read
  the worker session from the profile `state.db` (columns include `tool_calls`, timestamp
  column is `timestamp`, not `created_at`) to confirm real completion before deciding
  whether re-dispatch is needed (rule: audit completeness, never blind re-dispatch).

## References
- [`references/solo-mode-exemplar-clone.md`](references/solo-mode-exemplar-clone.md) — full runbook for "Tanpa Orkestrasi" generation (proven twice 09-09: Azira, Adsquare): ladder order, SPA handling, link pre-probe, builder triple, four gates, delivery/trace rules.
- [`references/sam-gov-debarment-probe.md`](references/sam-gov-debarment-probe.md) — keyless SAM.gov exclusions endpoint, control-positive rule, dead endpoints.
- [`references/person-tracing-recipe.md`](references/person-tracing-recipe.md) — team-page/sitemap/DDGS/aggregator/CDX ladder with PROV table format.
- [`references/primary-source-acquisition.md`](references/primary-source-acquisition.md) — FTC docket+order PDFs, SEC EDGAR, Brreg, CourtListener patterns.
