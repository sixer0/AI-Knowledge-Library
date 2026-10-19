# Data-Collection Audit Discipline (EXPO26 sweep, 2026-09-02)

Rules for verifying large acquired datasets (thousands of rows, worker-produced
staging + controller pipeline). All checks are SCRIPTS; prose claims are data.

## Checker self-doubt first — the auditor is the weakest author too
Three "data failures" this session were actually DEFECTS IN MY OWN CHECKS:
- Junk-name detector with `re.I` matched "NaN" inside "Nanjing" → false junk.
  Fix: case-sensitive code-artifact regex (`[{}<>]|function\s*\(|undefined|NaN|\.json|\[object`).
- Sample-30 fidelity audit FAILed 23/30 because I asserted the wrong criterion
  (demanded evidence depth) when the order required organiser-directory fidelity
  (row fields match organiser listing). Re-read the source requirement text BEFORE
  coding any gate; re-run after fixing the checker (then 30/30 PASS).
- Classify produced 0% because validated.csv lacked the join column and the
  anchor column was named `booth_hall` not `booth`. Fix joins by inspecting
  actual headers, not assumed schema.
Protocol when an audit FAILs: (1) dump the failing rows, (2) classify each as
checker-defect vs data-defect, (3) only then dispatch fixes. Log the correction —
the next agent must know the first verdict was an artifact of the checker.

## Evidence filter for any field 'fill' (anti-fabrication)
When filling missing fields (country, website) from search/site scans:
accept a fill ONLY if the source host tokens overlap the company name tokens,
or the quote embeds structured evidence (ld+json addressCountry). Known traps:
- parked/wrong organiser links: `orbitalofficial.com` = a music duo, not the
  space-data exhibitor "Orbital Views" (real site orbitalviews.com, found via
  SERP with distinctive context words).
- false hits from unrelated pages (a summit site mentioning Thailand).
Rejected fills become `UNKNOWN (reason)` in notes — never a guess. Record each
accepted fill as a ledger claim row (claim_id, source_url, verbatim quote).

## Count reconciliation vs organiser numbers
- Compare staging count to organiser-published count; >±5% deviation must be
  explained. Marketing metrics ≠ public list ("1,240+" WRC stat vs canonical
  314-row public list; "1,900+ brands" IFA vs 1,873 directory rows = -1.42% OK).
- Third-party aggregators (Expolista 4,235 vs official 4,191) are last-resort
  rungs — sitemap cross-check showed only 488 suppliers = thin, NOT a full list.
  Cross-check any list against the host's own sitemap (diff both directions = 0).
- As-of caveat: directories grow before event dates; mark PARTIAL + schedule
  resweep instead of pretending saturation.

## Robots-gated sources: CAPPED-with-evidence is a valid terminal state
When robots.txt forbids AI agents on the live path (CES): do not route around via
AJAX/live endpoints; enumerate Internet Archive CDX, harvest archived JSON
responses, merge what exists, then label CAPPED with the ladder log (rung tried,
evidence, coverage % vs official). A ledger claim + contract decision (D17/D21)
documents why more attempts are futile — that satisfies "stop only at
SATURATION or CAPPED with proof".

## HTTP capture integrity
`urllib` without `Accept-Encoding` handling stored gzip bytes as text (U+FFFD
garbage rows). Fix fetcher to request identity / decode gzip+deflate, then
RECAPTURE affected rows (delete bad cache keys by content probe, refetch).
Detect: `txt.count("\ufffd") >= 5 or "\x00" in txt`.

## Ledger schema drift
Appended rows with a self-invented header corrupt the canonical ledger. Always
read the existing header line first and write rows against THOSE fields
(idempotent normalizer script pattern: `ledger_norm.py`).

## Gate-fail closure loop
Gate FAIL (e.g. 3 rows missing country) is a work order, not a shrug: resolve
each row with a sourced claim, patch data, RE-RUN the gate fresh, report
ALL PASS with numbers. Premature finish runs (watcher cap fired while stage1
still running) must be re-run after true completion — validated >= staging,
not 'file exists'.
