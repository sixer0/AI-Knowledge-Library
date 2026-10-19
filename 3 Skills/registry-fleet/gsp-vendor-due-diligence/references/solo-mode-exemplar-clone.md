# Solo Mode: Clone Exemplar "DD Comprehensive Leadership Edition"
Two proven runs (09-09): DD-AZIRA-2609 ("Azira Sean") and DD-ADSQUARE-2609 ("Adsquare May Yin Lee").
Directive basis: user said the exemplars are for generating "Tanpa Orkestrasi" -> controller executes end-to-end, no worker cards.

## Inputs
- Target string from user: "<Vendor> <PersonFirst>" (may be bare; no clarification needed if mode + format are established; person = candidate to trace, fenced).
- Exemplar dump: DD-STUDI-TEMPLATE/dump/*.json + KONTRAK-DESAIN-DD-COMPREHENSIVE.md + RESEP-GENERASI.md (anatomy, palette, fonts, block recipes). Re-dump only if exemplars change.

## Procedure (order matters)
1. Local corpus first: grep vault/ADINT files for vendor token -> treat hits as HYPOTHESES.
2. Primary sweep (requests): official site robots/sitemaps (main + pages-sitemap), about/company/contact/imprint/legal/privacy/GDPR pages; sweep every page text for person token (case-insensitive, word-boundary).
3. SPA sites: static GET returns shell only. If sitemap paths 404 (stale sitemap), render homepage with browser_exec and read real nav hrefs, then render those routes (body.innerText). adsquare.com case: /who-we-are 404, real path /company/who-we-are.
4. Regulator/registry sweep: SEC EDGAR full-text (contact UA + Referer), USAspending API POST (valid award_type_codes; 0 rows = processed-empty), CourtListener, Google News RSS for history/events, archive.org CDX for domain history. SAM.gov: see references/sam-gov-debarment-probe.md; if endpoint 404s incl. control-positive, record NOT-YET-REACHABLE (never "clean") + risk item + re-probe via browser before contract.
5. Search fallback ladder: web_search -> DDGS -> html/lite DuckDuckGo (rate-limits with 202 fast) -> SearXNG local :8080 -> Bing via browser_exec rendered search (proven for person-attribution queries) -> The Org / RocketReach as C-grade personnel signals (role attribution only, never copy contact values).
6. Link pre-probe BEFORE writing register: every candidate URL must return 200 on plain-browser GET (sec.gov Archives direct = 403 for normal UA -> link the efts.sec.gov search-index URL instead; data.sec.gov OK with contact UA). Dead-in-probe never enters the doc as a live link; cite via news index or mark mirror.
7. Build with the triple: builder scaffold (copy from proven run, sed VEND/PERSON/OUT) + content1 (cover, Part I seksi 01-10) + content2 (Part II 11-20 + addendum Z-* + save). cat > full.py, run under `uv run --python 3.11 --with python-docx`.
8. Gates (all mandatory, in this order):
   a. Structure parser: anatomy "NN " Part I + "NN." Part II headings, tables >= 25 (exemplar 31; count varies with content, anatomy is the contract not the count), key numbers present, score recompute delta 0, weights sum 100.
   b. XML hygiene: U+2014/U+00B7 = 0 across ALL parts; hyperlink rels count == expected (r:id attr!); Indonesian token sweep on final text (list: dan|atau|tidak|dengan|untuk|dari|pada|ini|itu|akan|sudah|belum|hanya|juga|hlm|dokumen|nama|perusahaan|laporan|tanggal|sumber|halaman|kosong -> must be 0; inspect each hit for false positives inside English words).
   c. Link probe: every rels href, plain-browser GET, dead list must be empty.
   d. scan_ai_footprint.py --channel doc on the DOCX -> VERDICT PASS (B8 needs a "limitation" keyword in measurable prose).
9. Deliver: copy to workspace root etalase (sha256 must equal source), trace folder docs/<date>-dd-<vendor>-tanpa-orkestrasi/ (contract/REGISTER_BUKTI.md + builder/gate scripts + linkprobe.json), changelog line + commit + push (stage only your changelog line; other writers may be active in CHANGELOG.md - verify `git diff --cached` shows 1 insertion).

## Scoring in solo mode
Exemplar rubric D1-D5 (30/25/20/15/10) with T1/T2/T3 bands + HARD BLOCKS section (sanctioned/debarment, unverifiable provenance, material adverse judgment, non-consensual sourcing, restricted-market breach). This is the ADINT-fit system; do NOT mix with the 5-aspect procurement verdict unless both shown side-by-side labeled. D3 (Indonesia/APAC relevance) typically scores low for US/EU vendors - justify with absence-of-evidence + concrete APAC facts (offices, named staff, case studies).

## Person handling (proven twice)
Given-name-only -> CANDIDATE with entity-match (name token + vendor token co-occurring in official/attributable page), confidence per field, explicit "cannot confirm this is the intended contact" sentence, rejected/weak signals to Z-D addendum rows grade C. The Org team page + conference speaker lists are legitimate B/C-grade attribution sources.

## Register format
A-nn rows (claim | source+link | note) in Lampiran A; Z-* rows in addendum (A/B/C grade); REGISTER-KOSONG = fields left empty with reason (state registries not reached, private-co financials, etc.). Empty beats wrong, always.

## Proven results (reference points)
- Azira LLC / Sean Ott: T2 CONDITIONAL 59/100, links 25/25 live, gates green. sha16 91478e99.
- Adsquare GmbH / May Yin Lee: T2 CONDITIONAL 66/100, links 19/19 live, gates green. sha16 0788098f.
- Typical solo runtime per target: ~30-45 min including ladder exploration; budget most of it for search-engine rate-limit fallbacks and SPA rendering.
