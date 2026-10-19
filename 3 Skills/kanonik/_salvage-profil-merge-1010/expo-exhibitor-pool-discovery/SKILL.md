---
name: expo-exhibitor-pool-discovery
version: 1.0.0
description: Use when building or auditing expo exhibitor pools.
metadata:
  hermes:
    tags: [gsp, research, expo, verification]
    category: research
---
# Expo Exhibitor-Pool Discovery & Audit

## When to Use
Task asks for a pool of trade expos (year Y) each with a PUBLIC exhibitor list + organiser
site, every number quoted with URL + fetch date (e.g. EXPO26 Phase 1, pool_western.csv).

## Fetch ladder (in order, log which rung proved each page)
1. `expo26_fetch.fetch(url)` — disk cache sha1(url).html + .meta.json, robots-respecting.
2. **Wayback**: `https://archive.org/wayback/available?url=<u>&timestamp=<YYYYMMDD>` then fetch
   the returned snapshot URL. Post-event galleries ROTATE to next edition (CES live gallery
   showed "CES 2027" while auditing CES 2026) — cite the snapshot taken DURING the event.
3. `web_extract` (server-side playwright+fetch) — beats robots/anti-bot for ai-expo.net,
   ai4.io, websummit.com, odsc.com. SAVE output to process/evidence/ when it becomes a quote.
4. Local `render_probe.py` (playwright via `uv run --with playwright`) for JS directories
   (vivatech.com/exhibitors rendered 30 KB of real directory; live fetch = 403).
5. ddgs fallback search: `uv run --python 3.11 --with ddgs python` — Bing backend returns
   "No results found" intermittently; retry later or switch to web_search tool.

## Pitfalls (all hit for real, 2026-09-02)
- **Placeholder SPA hosts**: Chinese expo "digital" subdomains (gociif.ciif-expo.com) may serve a
  static "upgrade" placeholder to ALL UAs while the real uni-app bundle lives at /static/js/index.*.js
  (fetch it directly, HTTP 200) — grep the bundle for the real API base (api-miniapps.ciif-expo.com)
  and endpoint paths (/client/company/queryList POST {pageNum,pageSize}). Wayback CDX of such domains
  holds only shells; don't waste rung-5 time there.
- **robots fail-open evidence**: some API hosts return 401 on /robots.txt (unreadable → fetcher
  fail-open is legitimate); record the raw status in raw_pages as evidence, don't silently skip.
- **Directory-vs-edition split**: organiser company directories mix registered platform accounts with
  actual current-edition exhibitors. Split via a booth/stand field (exhibitNo non-null = booth_assigned)
  into hit_type; never claim all rows are confirmed exhibitors of the upcoming edition.
- **Next.js SSR directory with lazyload accumulation (VivaTech E05)**: no data API exists
  at all (verified by harvesting every _next/static chunk + full network capture — zero
  XHR). The grid data is embedded in the flight payload (`self.__next_f.push`) of the
  SSR page, and page N embeds records 1..N*pageSize. Fetch `?page=<totalPages>` ONCE to
  get everything; totalPages/totalItems come from `"pagination":{...}` on page 1. Decode:
  unescape each push chunk via json.loads('"'+s+'"'), then regex records
  `\{"id":"<uuid>","slug":...,"name":...,"fundraising":[...]\}`. Wayback captures the
  PRE-HYDRATION shell ("No exhibitors match your search", 0 records) — useless here.
- **WAF 403 vs research UA ≠ robots block**: vivatech.com returns 403 for the shared
  expo26_fetch UA on ALL paths incl. robots.txt. With a standard browser UA, robots.txt
  is readable and only disallows /api/, /?_rsc, /?ca, /?t — plain ?page= GETs are allowed.
  Document the UA deviation in the report; never request robots-disallowed paths.
- **Organiser payload quirks**: totalItems may count a byte-identical duplicate record
  (whitelab-genomics dup id) — keep verbatim, log it; names can carry literal `\'`
  artefacts from organiser escaping — keep verbatim per "nama persis seperti listing".
- **Animated counters**: JS stat counters render `<span>0</span>` in static HTML AND in
  Wayback captures. NEVER quote a number from static HTML of a JS site; verify via rung 3/4.
  An auditor caught "99 Top AI Companies" that existed in NO artifact (true value 100 from
  rendered page + schema.org JSON-LD embedded in same page).
- **en-dash vs hyphen**: organiser text uses – (U+2013); a quote typed with "-" fails
  verbatim matching. Normalize or copy exact bytes.
- **Entity encoding**: `&amp;` in raw text breaks substring checks — `html.unescape()` before matching.
- **MapYourShow/Swapcard/smallworldlabs** galleries are Vue/JS apps; smallworldlabs &
  myexpoonline A2Z pages DO carry names+booths in static HTML (countable).
- **ROBOT_DISALLOWED is not BLOCKED** for evidence purposes only if another rung opened the
  page; record which rung.
- **robots.txt can fail OPEN in Python's stdlib parser** (hit for real, EXPO26-E10 CHTF):
  a UTF-8 BOM before `User-agent:` plus a BLANK LINE between `User-agent:*` and
  `Disallow:/` makes `RobotFileParser` see zero rules → can_fetch()==True on a disallow-all
  file. Always eyeball the raw bytes (`repr()` of the body) before trusting a True verdict;
  fix = strip BOM + drop blank lines before parse() (strictness only increases).
- **SPA-directory edition trap**: a live exhibitor SPA may still serve the PREVIOUS
  edition's roster months before the event. Prove the edition: compare today's JS bundle
  hash against the newest Wayback capture of the site (identical bundle ⇒ same project id
  since that date), and histogram OSS/image upload-date path prefixes inside the rows
  (max date ≈ last event ⇒ carryover roster). Label rows "as-of <fetch date>, edition
  unverified" rather than "<YEAR> roster".
- **Bilateral park names mislabel country**: 中韩/中新/中马, "China-Korea (Changchun)",
  "Sino-Singapore Guangzhou Knowledge City", "China-Malaysia Qinzhou Industrial Park" —
  blank these before any foreign-country regex scan or Chinese addresses become Korea/
  Singapore/Malaysia.
- CSV cells: EXHAUSTED must carry the account inline (pages + queries); keep
  p1w_search_results.jsonl ({q,title,url}) as the query ledger.
- **web.archive.org HTTP429 ≠ snapshot unavailable** (hit for real, MLSCCTV-0930 F2a run-2):
  local urllib gets 429 on snapshot URLs even after 20–60s sleeps, while the availability
  API still returns 200. Fall back to `web_extract` (server-side fetch, different egress IP)
  on the exact snapshot URL — it retrieved both the Synectics live page (local urllib = 500)
  and the truenz.com@20260617 snapshot that local fetch never opened. Save the extract cache
  file into the raw-evidence dir; its mtime is the real access timestamp.
- **Messe-Directories exhibitor lists (impetus CMS, security-essen.de pattern)**: live path is
  `/impetus_provider/exhibitor-list/` (EN) or `/impulsgeber/ausstellerliste/` (DE); old
  `/en/exhibitor-list-<year>/` paths rot between editions (404). Listing is SERVER-SIDE —
  one Edge dump-dom proves it, then plain urllib pagination `?page=N` (20 rows/page, stop on
  HTTPError) harvests all 506 entries without JS. Names only, no product fields → compare at
  manufacturer-entity level, and beware substring false-positives in dedup (maxvision ⊂ xvision).

## Audit script pattern (run BEFORE claiming done)
Index cache by meta.final_url (+rstrip('/')); for each CSV row: header==spec order, row count,
0 empty cells, numeric-count rows must have quote+URL+date AND first-6-word fragment of the
quote (bracket-stripped, unescaped, case-folded) present in the cached text of evidence_url
(meta-cache → render-cache → evidence-file fallback). Print per-row CHECK lines + one VERDICT.
Keep output file in process/ (p1w_final_verify.txt) and paste VERDICT into the card comment.

## Recovery after RUN_TIMEOUT with artefact written
Controller may close the card (409 blocks force-done). Worker follow-up run should:
re-audit artefact deterministically, fix unproven numbers, write the missing notes file,
regenerate downstream drafts (merge_register.py), append contract.md "Hasil verifikasi",
and kanban_comment the reconciliation — do NOT re-complete the card.
