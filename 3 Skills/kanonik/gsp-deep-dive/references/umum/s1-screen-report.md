# S1 - Screen Report (T1; executors: lanes + verifier; gate: G1)

Purpose: the first presentation surface. One to two pages of pure measurement
that lets the Director choose the next depth. This is also human gate number
one: the user reads the screen report and picks T2, T3, partial measurement or
stop. That choice belongs to the user, never to the fleet. Identical for every
object class; the profile fills the sketch slot with its own demand shape.

## Execution checklist
1. Every material claim found so far enters `claims-ledger.csv` verbatim with
   source document and page. Every percentage or ratio is recomputed in code
   (`scripts/recompute-checks.py`), not by eye.
2. Measure the seven flag classes for the first time: status plus evidence
   source plus date per class. Unfinished classes are recorded as
   unresolved-after-N-searches with N explicit.
3. Draft the top five asks in `ask-list.csv`: ask for evidence, not assurances.
4. Demand sketch: named buyers or beneficiaries and competitors visible in the
   first sweep, with the query count that produced them (the profile defines
   what a sketch row looks like for its class).
5. Fill `01-screen/screen-report.md` from templates/screen-report.md, sections
   in the fixed order, ending with the empty slot `Director decision: ______`.
6. Run the prohibited-vocabulary scan over the report before submitting; the
   report must be free of outcome vocabulary outside the decision slot.
7. Independent verifier (separate account) checks the ledger rows and the flag
   statuses; the writer cannot sign this gate.

## Gate G1 predicates
Screen report present; seven flag rows each with status, source and date; the
report passes the SPK-002 field gate; every numeric claim has a ledger row;
prohibited-vocabulary hits = 0; independent verifier pass.

## Common pitfalls
- Writing the report as a narrative instead of a measurement surface. Every
  sentence should trace to a ledger row, a flag row or a logged query.
- Softening a flag because it looks awkward next to a promising sketch.
  Flags are measurements; discomfort is not a reason to relabel them.
- Filling the decision slot. It stays empty.
