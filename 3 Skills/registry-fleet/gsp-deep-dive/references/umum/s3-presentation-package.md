# S4 - Presentation Package (general; executors: controller + reviewer on a separate account; gate: G3)

Purpose: assemble everything measured into the record presentation surface.
The package presents; it never concludes. The instrument set is fixed by the
standard for every object class: findings block, nine dimension cards with a
mechanical evidence ceiling, one arithmetic indicator, sensitivity, and a
blind completeness challenge. The profile sets the focus order of the dossier
sections (block B?.6), never the depth.

## Execution checklist
1. Fill `04-package/blok-temuan.md` from templates/blok-temuan.md, sections in
   the fixed order: flag register status (7 rows with source and date), nine
   dimension cards, one arithmetic indicator, sensitivity, known unknowns with
   search counts, top ask-list, demand headline (profile shapes this slot),
   then the empty slot `Director decision: ______`.
2. Dimension cards, nine dimensions (general names; profile B1 keeps its
   frozen legacy names where they match): technology and maturity; named buyer
   demand; GSP added value / moat; competitive position; economy; sovereignty
   and deployment; regulatory and export route; counterparty reliability and
   integrity; terms and channel position. Each card scores 0-5 pointing at
   claim ids in the ledger. Mechanical ceiling: a dimension whose referenced
   claims are ALL self-reported (label VENDOR-CLAIMED, frozen name) cannot
   exceed 3.
3. Indicator: computed by the parser from frozen weights
   WEIGHTS = [15,15,15,10,10,10,10,10,5], printed as
   `Indicator: <sum(weight_i * score_i) / 5>` with the companion sentence
   "arithmetic indicator only; no band-to-verdict mapping". Weight revision
   happens only through the official Decision Log, never inside a record.
4. Sensitivity is mandatory: name which measurement moves the indicator most
   if it changes one level; that address is where further research goes.
5. Risk register stays a measurement: likelihood and impact each with a basis,
   mitigation options listed, owner named. There is no decision column; choosing
   among options is the Director's right.
6. Ask-list ranked: asks request EVIDENCE not assurances; each row records why
   asked, evidence requested, which metric or ledger row it affects.
7. Blind completeness challenge: a reviewer account that wrote no lane in this
   record receives the package cold (ledger, registers, presentation, no author
   narrative) and tests whether numbers remain valid, whether contradictory
   evidence was quietly dropped, whether the demand map cherry-picks, whether
   any route class went untouched. Record what was tested, what broke, what was
   fixed, in `04-package/blind-challenge.md`. Invented objections are forbidden.
8. Term-sheet points are prepared ONLY on user direction, never on initiative.
9. Run the prohibited-vocabulary scan across the whole record before
   submitting the package.

## Gate G3 predicates
Every dimension card points at existing ledger rows; the self-report-only
ceiling is applied; the blind challenge file exists from a separate account;
zero outcome vocabulary anywhere in the record; indicator equals the parser
recomputation.

## Common pitfalls
- Presenting the indicator as a grade. It is arithmetic over evidence-limited
  inputs; two objects with equal indicators can sit on completely different
  evidence quality, which is exactly why cards and labels stay visible.
- Writing the blind challenge after reading the authors' summary. The reviewer
  gets the package without author narrative, or the challenge is worthless.
- Adding a "fleet position" paragraph anywhere. It does not exist in this
  procedure.
