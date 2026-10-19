# Gates: definitions, folder layout, profiles, and how to run the checker

Gate philosophy: a gate judges COMPLETENESS and measurement correctness, never
business outcomes. Every predicate below is checked deterministically by
scripts/gate_check.py; a human can verify the same predicates by reading the
same files. Gate verdicts are L1 facts about the folder, not L2 claims about
the object.

General gates (every class): G0 nomination/registration, G1 screen report,
G3 presentation package, G4 close-out. Lane gates are defined by the profile
manifest (B1 uses the legacy ids G2T and G2K; thin profiles define their own
gate specs under those ids). Without --profile the lane gates are reported as
skipped via INFO, never silently passed.

## Expected record folder layout (general)
```
docs/<date>_dd-<object>/            (B1 legacy shape: docs/<date>_ddv-<vendor>/)
  00-record/       nomination.md, document-register.csv, entity-match.md,
                   thesis.md (B1 may keep prospect-thesis.md),
                   flag-register.seed.csv
  01-screen/       screen-report.md
  02-lanes/        lane-grid.csv                     <- profile-defined grid
                   (B1 keeps 02-technical/five-layer.csv)
  03-commercial/   profile maps where the manifest requires them
                   (B1: prospect-map.csv, buyer-map.csv)
  (record root)    claims-ledger.csv, risk-register.csv, ask-list.csv,
                   query-log.csv
  04-package/      blok-temuan.md, blind-challenge.md
  saturation/      one file per lane, named in the profile manifest
  05-closeout/     il-promotion-note.md, master-register-update.md,
                   refresh-triggers.md, validation-first-arrival.(md|csv)
                   (validation form required only when this is the first real DD)
```

## Fixed mini-schemas used by the checker
- nomination.md must contain `Object: ...` (or the legacy `Vendor: ...` on B1
  records), plus `Deadline: YYYY-MM-DD`, `Tier: T1|T2|T3`,
  `First real DD: yes|no`.
- entity-match.md must contain the token `Entity match:` and an ISO date.
- document-register.csv header (exact, ordered):
  `document_name,date_received,pages,doc_type,status,what_is_missing`
  The what_is_missing cell is never empty (write `none` or the missing item).
- flag-register.seed.csv header: `class_id,class_name,status,evidence_source,date`
  with exactly 7 data rows FL-1..FL-7 and descriptive status labels only.
- query-log.csv header: `query_id,date,route_class,language,query_or_url,result_summary,evidence_status`;
  route_class values 1..8 are the offensive-search classes; the ladder check
  requires all eight classes present.
- Saturation statements (saturation/<lane>.md) must contain the three lines
  `Query count: <int>`, `Route classes exhausted: <n>/8`, `Date: YYYY-MM-DD`.
- Lane grid CSVs use the frozen eleven-column schema of AA.3 (see
  s2-lane-dissection.md); minimum rows per profile manifest.
- blok-temuan.md dimension cards, one line each, DIM-1..DIM-9 exactly once:
  `DIM-<n> | <dimension name> | score: <0-5> | claims: CLM-xxx[,CLM-yyy]`
  plus one line `Indicator: <value>` and the sentence
  "arithmetic indicator only; no band-to-verdict mapping".
- Indicator formula (parser-owned, frozen weights):
  `WEIGHTS = [15,15,15,10,10,10,10,10,5]`;
  `indicator = sum(weight_i * score_i) / 5`, rounded to 1 decimal, maximum 100.

## General gate predicates
### G0 - Nomination and registration
1. entity-match.md exists and carries an `Entity match:` result with an ISO date.
2. No duplicate dossier: slug checked against the master register when
   `--master-register <csv>` is supplied; otherwise reported as skipped.
3. document-register.csv header exact and every what_is_missing cell filled.
4. thesis.md (or B1 legacy prospect-thesis.md) has 3-5 content lines.
5. flag-register.seed.csv has exactly the 7 classes FL-1..FL-7.
6. nomination.md records tier (T1|T2|T3) and the user deadline date.

### G1 - Screen report
1. screen-report.md exists.
2. Flag Register First Pass table has exactly 7 rows, each with status,
   evidence_source and date filled; statuses are descriptive labels only.
3. Prohibited-vocabulary scan (DAFTAR_A) returns 0 hits on the screen report
   and the root ledgers.
4. Every claim id cited in the screen report exists as a row in
   claims-ledger.csv, and the ledger is non-empty.

### G3 - Presentation package
1. blok-temuan.md exists with all nine dimension cards DIM-1..DIM-9.
2. Every score points to claim ids that exist in claims-ledger.csv.
3. Mechanical ceiling: a dimension whose referenced claims are all
   self-reported (frozen label VENDOR-CLAIMED) cannot exceed score 3.
4. The printed Indicator equals the parser recomputation WEIGHTS.scores/5
   (tolerance 0.05) and the companion sentence is present.
5. blind-challenge.md exists, is non-empty, and names the reviewer account
   (an account that wrote no lane in this record).
6. Prohibited-vocabulary scan returns 0 hits across the whole record.

### G4 - Close-out and promotion
1. il-promotion-note.md exists and is non-empty.
2. master-register-update.md exists and is non-empty.
3. refresh-triggers.md lists at least 4 trigger lines.
4. When nomination.md says `First real DD: yes`, the
   validation-first-arrival form must be attached in 05-closeout/.

## Profile gate extensions (scripts/profiles/<name>.json)
The manifest maps gate ids to specs: kind "legacy_vendor" runs the frozen B1
predicates (five-layer 35-row grid, M2 ceiling, prospect/buyer maps with exact
headers, workbook pointer, numbered saturation, 8-class ladder); kind
"lane_grid" runs the generic grid engine (path, schema, min_rows, paired
UNKNOWN, self-report ceiling, saturation files, query log); kind "maps" runs
the generic map engine (exact headers, url/date/workbook column rules). A gate
id absent from the manifest stays general. Unknown kinds FAIL loudly.

## Running the checker
```
uv run --python 3.11 python scripts/gate_check.py <record-dir> --profile <name> [--gate all] [--json]
```
Exit codes: 0 = all selected gates pass; 1 = at least one FAIL (names printed);
2 = misuse (unknown profile, unreadable folder or register). Self-test pairs
under scripts/fixtures/: for EVERY profile the complete record must exit 0 and
the broken record must exit 1 with named FAILs (empty grid cells, saturation
without numbers, a dimension card pointing at a fake claim id). Re-run all
pairs after any script edit. The vendor pair additionally carries the
regression contract: identical fixtures must produce verdicts identical to the
dd-vendor era checker (blueprint 02b section 4 term 3).

## Running the recompute checker
```
uv run --python 3.11 python scripts/recompute-checks.py <claims-ledger.csv> [--tolerance 2.0] [--json]
```
Unchanged from the dd-vendor era (the ledger schema is frozen). Writes
`<ledger>.checked.csv` beside the input (input never modified). Exit 0 = every
evaluated numeric claim within tolerance; 1 = mismatch beyond tolerance or a
load-bearing numeric claim without test_method; 2 = misuse or header mismatch.
Supported test_method grammar is a restricted arithmetic subset (numbers,
+ - * / parentheses, optional % suffix); the parser is self-contained and
never calls eval().

## Class acceptance procedure (new object class, blueprint 02b section 2.4)
1. Copy templates/profiles/_template/ (six blocks, locked columns) and fill
   B?.1 trigger, B?.2 lanes, B?.3 mandatory questions, B?.4 typical flags,
   B?.5 typical artifacts, B?.6 presentation focus. Every mandatory question
   must name its provenance (a precedent mission or a Decision Log entry);
   without provenance it is invalid.
2. Write scripts/profiles/<class>.json declaring the lane-gate specs.
3. Create the fixture pair scripts/fixtures/{complete,broken}/<class>-record/
   and prove both directions: gate_check --profile <class> exits 0 on complete
   and nonzero with named FAILs on broken.
4. Register one row in the profile register table (standard Part B5) plus one
   Decision Log row.
5. Regression: the general layer is unchanged (zero diff) and every existing
   profile fixture pair still exits as before.
