# Bulk Transforms, Contamination Gates, and Exact Recovery (EXPO26 lessons, 02-09)

Patterns proven during the AI EXPO 2026 sweep (10 expos, ~24k rows). All were real incidents
on disk, not theory.

## 1. Never trust a join key without checking emptiness (the drain-all bug)
A strip operation keyed on `row_id` matched `{''}` against rows whose `row_id` column was
EMPTY on every row → hit ALL 2,902 rows, wiped their websites, and mass-flipped verdicts
(YES 675/WEAK 1.037 → all NO). Detected only because the QA board showed an impossible
distribution vs history.

Rules for ANY destructive bulk transform on CSV/DB rows:
- Before keying on a column, assert non-empty rate (`empty = sum(not r[k].strip())`). If
  any empties exist, use a dual key: primary id + normalized-name fallback
  (`_nk = re.sub(r'[^a-z0-9]+','',name.lower())`).
- Auto-backup under the transform itself (`shutil.copy(vp, vp + ".pre-strip.bak")`) —
  not a manual step.
- Post-transform sanity assertion: affected-row count must equal the intended suspect
  count; derived distributions must not swing more than expected. Print the key used
  (`key=row_id` vs `key=name`).
- Impossible-distribution detection belongs in the periodic board/QA pull, not only in
  the writer: "all rows NO" next to a historical YES=675 is the tripwire that caught this.

## 2. Exact offline recovery beats re-crawl
When a derived column is corrupted but the RAW sub-columns (here t1/t2/t3 test results)
and the upstream staging file survive, rebuild deterministically: recompute the derived
verdict from raw columns using the ORIGINAL rule copied verbatim from the producer script,
restore source fields (website) from staging by normalized name, keep legitimately-flagged
rows flagged. Result was byte-exact to the historical distribution (675/1037/1190) with
zero network calls. Recipe: backup corrupted → map staging by `_nk(name)` → recompute rule
→ atomic replace → verify distribution equals pre-incident expectation.

## 3. Search-fallback contamination gate (`site_plausible` pattern)
Web-search fallbacks resolve real-but-wrong domains (ALTAVE→calculator.net, a Chinese
exhibitor→walmart.com, an alliance→bbc.com). Gate any resolved URL before accepting:
- Generic-domain regex (marketplaces, social, wikis, calculators, news, URL shorteners).
- Token overlap test between entity name and domain, tokens ≥3 chars only (CNN→cnn.com
  legit; 3-letter sigla saves Canva/CNN, walmart/bbc stay suspect).
- For social/storefront hosts, accept when an entity token appears in the URL PATH
  (linkedin company page legit vs bare feed); subdomain slugs on supplier platforms are
  NOT proof (conservative: reject unless token matches).
- Corporate whitelist for domains legitimately operated by the exhibitor
  (aws.amazon.com, leo.amazon.com, box.com...).
- Unit-test the gate with adversarial cases both directions (~15 cases caught 3 of my own
  over/under-corrections before deployment).
- Heuristic caution: pure "domain token differs from name token" over-flags massively
  (174 flagged vs 13 truly contaminated — siglenteu.com IS Siglent). Generic-domain AND
  no-token-overlap is the criterion; single signals are not.
- Provenance MARKERS ("via search fallback") get overwritten by later verdict passes —
  detect contamination by content/domain signature, never by marker text.
- When stripping a site that a YES/WEAK verdict was derived FROM: void the verdict
  (→NO beralasan), don't keep a verdict whose evidence was fake.

## 4. Tool-defect vs data-error distinction in audits
An evidence audit FAILed with cache_miss=26 but mismatch=0 → NOT a data problem: rows
validated via a non-caching scrape path never wrote disk bytes, and the population change
(Tier B recalibration) shifted the seeded `Random(42)` sample onto those rows. Fix:
one live re-fetch per miss through the bounded, robots-respecting fetcher (which caches),
prove the quote live, and report a `live_refetch` count column so the audit stays honest.
Rule: mismatch>0 = data problem (investigate); miss-only = tool gap (fix the tool, label
the proof mode). Seeded samples are only reproducible against a FROZEN population — note
this whenever upstream recalibration changes the pool.

## 5. Background-chain exit-1 reconciliation
Chains killed deliberately via `taskkill /T /F` report exit 1 to the completion notifier.
Before treating as failure: confirm the kill was intentional, then verify the SUCCESSOR
process is alive and advancing on disk (row count + mtime). Log the reconciliation in the
method-log so the board doesn't carry phantom failures.

## 6. Pipeline ordering
In staged pipelines, a hand-rolled direct chain that skips a stage (triage) dies with
FileNotFoundError downstream. Reuse the supervisor's full stage sequence; when starting a
new queue, copy the proven command chain verbatim.

## 7. Status reporting
For "what's done" asks, generate numbers by a board script that reads disk
(staging/validated/promoted/audit JSON + report line counts) — never from memory. Check
column-name assumptions first (verdict lived in `validated`, not `verdict`; a wrong column
silently printed zeros). Link reports via MEDIA paths.
