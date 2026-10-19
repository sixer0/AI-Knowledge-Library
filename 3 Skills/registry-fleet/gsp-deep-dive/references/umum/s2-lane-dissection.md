# S2-S3 - Lane Dissection (general method; T2/T3; gates: per profile manifest)

Purpose: establish what the object really is and proves, at full depth, in all
lanes at once. Lane NAMES are defined by the profile (block B?.2); this file
defines HOW any lane is dissected so that every class meets the same bar. All
lanes run at equal full depth - depth equality is a user decision (D-17
principle), never a workload preference.

## General grid contract (AA.3)
Every lane dissection produces rows in a lane grid with the frozen eleven
columns: lane, question_id, question, answer, maturity, maturity_evidence,
dependency_and_country, evidence_source, evidence_date, ceiling_applied,
unknown_search_route. The profile names its lanes and its mandatory question
bank (block B?.3); the bank is a fixed set, not advisory. Minimum row count =
lanes x questions (profile manifests pin the number: B1 five layers x seven
questions = 35; thin profiles three lanes x seven = 21).

## Execution checklist (every lane)
1. Fill one grid row per lane x question. Empty cells are forbidden: UNKNOWN
   pairs with a filled unknown_search_route naming the concrete routes still
   open.
2. Maturity discipline: evidence labels are VENDOR-CLAIMED (self-reported by
   the counterparty - the label name is frozen history, the semantics are
   object-neutral), PRIMARY-DOC, THIRD-PARTY, or OBSERVED. Self-reported
   evidence alone caps maturity at M2 and must show ceiling_applied=Y. The cap
   is mechanical and parser-enforced.
3. Apply the profile's category banks where they match the object; a
   multi-category object gets every matching bank's rows.
4. Cross-cutting measurements per profile (typical: smallest sellable unit,
   skills GSP staff must maintain, integration into GSP lines, Indonesian
   language posture, export-control status MEASURED per flag class FL-2 and
   presented only).
5. Audit an object deliverable sample when one exists: observed vs inferred,
   provenance, method, baseline, reproducibility, language discipline.
6. Label every load-bearing number six ways: value, unit, year, source,
   Admiralty grade, verifier label. Unlabeled numbers do not enter the record.
7. Sweep with the offensive-search classes and log every route in
   query-log.csv; close each lane with saturation/<lane>.md carrying query
   count, exhausted route classes and date.
8. Independent verifier pass separate from the writer, per lane.

## Gate predicates (general half)
Ladder table complete with a numbered saturation verdict per lane; every
load-bearing number labeled; grid full with zero empty cells and paired
UNKNOWN routes; mechanical M2 ceiling applied to self-report-only evidence;
verifier pass from a separate account. The profile manifest adds the concrete
grid path, minimum rows, map requirements and saturation file names; run
`gate_check.py <record> --profile <name>` for the deterministic view.

## Common pitfalls
- Answering maturity from the marketing deck alone and skipping the cap.
- Recording "no information found" without the search route. The cell then
  fails the checker and hides an unexplored path from the Director.
- Letting one lane shrink because another looks richer. Equality is binding.
