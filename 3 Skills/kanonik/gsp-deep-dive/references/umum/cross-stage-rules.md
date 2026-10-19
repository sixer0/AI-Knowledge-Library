# Cross-Stage Working Rules (general lane law for every deep-dive stage)

Authority: GSP Deep-Dive Standard Part A section A4 and blueprint 02b section 2.1.
These rules bind every lane at every stage and every object class; a gate
failure on any of them stops promotion of the stage output, not just the lane
that produced it. Profile files (references/profiles/) may add specifics but
never relax these rules.

## 1. Measure, not decide (binding lane law)
- The fleet measures, fills, searches, and presents. It never issues a business
  outcome. Outcome vocabulary is reserved to the Director. Every deliverable
  carries the empty slot `Director decision: ______` and nothing else that
  resembles a decision. The fleet never fills the slot.
- Research is never trimmed by decision-relevance: every lane is swept until a
  saturation statement with numbers (query count, exhausted route classes,
  date) or the user deadline. Absence of data is a reported finding together
  with the queries that prove it.
- The prohibited-vocabulary register (Daftar-A) is enforced mechanically: the
  DAFTAR_A constant in scripts/gate_check.py scans every output-surface file
  (word-boundary, case-insensitive). The register text itself lives in Annex C
  of the issued standard; this reference deliberately does not spell the
  banned tokens so the skill folder stays clean under the same scan. Sole
  exemptions: the literal slot `Director decision:` and column labels.
- Flag labels are descriptive only: blocker-candidate, caution, note, clear,
  unresolved-after-N-searches (N explicit). The fleet never emits the legacy
  veto word for a flag state.
- Dimension scores are always called arithmetic indicators and carry the
  companion sentence "arithmetic indicator only; no band-to-verdict mapping".
  Band-to-verdict tables are forbidden anywhere (SC-5).

## 2. Offensive search (8 route classes, all booked before any dead-end verdict)
Target stays fixed; the route flexes. A lane may stop only with a saturation
statement or the deadline. Every route tried is logged in query-log.csv with
its class, date and outcome.
1. Primary official route (object site exact pages, organizer endpoints/APIs,
   official exports).
2. Domain/subdomain variants and ALL sitemap variants.
3. Platform/CMS probes (WP REST, custom post types, Next.js data, SPA payloads).
4. Active multilingual search (local-language queries, site: operators,
   directory phrases; results 1-30; aggregators marked PROV).
5. Archives (CDX per URL and per domain, archive.today).
6. Official documents (press releases, catalog PDFs, OCR).
7. Social/news as name supplement (never a directory substitute).
8. Interactive browser render hunting XHR endpoints.
Inherited rules: a per-route verdict without an account is treated as NOT run;
CAPPED-with-evidence is a request for ruling to the controller, not a worker
decision; budget/rate exhaustion is a partial-handoff checkpoint, not a dead
end; robots/named-agent blocks constrain the route, not the goal.

## 3. Data accuracy (SPK-002, absolute)
- Truth over fidelity: inherited or source-file data is re-tested against
  primary sources for every release-bearing field.
- Entity-match mandatory: an external identifier (URL/contact) belongs to an
  entity only if the name token appears in the host/label-domain or in the
  title/OG/body of the page. Precedent: two unrelated companies sharing the
  "EOS" brand token (EOSRAY-1009).
- Empty beats wrong: unverified identifiers are blanked and registered, never
  carried forward as-is.
- Upstream flags block: rows carrying failed-validation flags do not rise into
  release columns without field-level remediation.
- Release gate is 100% deterministic over the whole population of
  release-bearing fields (not sampling); the VERIFIKASI-AKURASI table is
  attached to the closing card and release happens only at SALAH-TARGET = 0.
- Links on delivered output must be live hyperlinks with visible link styling
  (firm color + underline); link-display defects block release.
- CER-001 ladder for Chinese entities and expos in China: R0 official site via
  organizer API (identity authority) > R1 CN registry (name bridge only, never
  a published link) > R2 Mandarin search "<nama_cn> 官网" > R3 ICP footer
  evidence > R4 CDX .cn + Wikipedia-ZH. City/province names are never proof of
  ownership; directory/tourism/portal/news domains are never published links.
- Every load-bearing number carries six labels: value, unit, year, source,
  Admiralty grade, verifier label.

## 4. Process discipline
- One kanban card per stage per deep dive on the default board; result =
  measured evidence; checkpoint file `DD-<object>-S<n>.md` after every session
  so a closed session never loses state.
- Writer-is-not-verifier at every gate; claims to the user are at least L2
  (verified by a separate account).
- Full data accompanies every presentation: claims ledger, source ledger,
  query log, economy workbook, buyer register attached as indexed working
  files (xlsx/csv), never summarized away.
- Counterparty silence: no chasing clocks from the fleet. Unanswered items
  stay as dated named open items and are re-presented in every delta note,
  without billing and without conclusions.

## 5. Output language and shape
- English throughout (standard, skill, record, all fleet output). Indonesian
  regulation and program names stay verbatim: UU 21/2013, UU 16/2012,
  UU 27/2022 (PDP), TKDN, BSSN, BIG, LPSE, INAPROC, e-katalog LKPP, SiRUP,
  RENSTRA/LAKIP.
- Shape: DATUM house style (datum-house-style, rail rev B), STD-GAYA-AHLI-001
  for prose, STD-VISUAL-001 for figures, STD-SAJI-001 for xlsx annexes.
- Record order: the general frame is findings block, object one paragraph,
  demand and named buyers, market and competition, regulation and procurement,
  technical lanes, entity and ownership, claims ledger summary and consistency
  flags, economy, risk register, ask-list, completeness challenge, full data
  annexes. Each section closes with two lines: what is still unknown here, and
  how to search for it. The profile sets the concrete focus order (B?.6);
  focus order never shifts depth.
- Deliverable per tier: T1 = screen report 1-2 pages; T2 = record + ask-list +
  data annexes; T3 = full record + economy workbook + risk register +
  term-sheet points on command + an independent route for every load-bearing
  number.
