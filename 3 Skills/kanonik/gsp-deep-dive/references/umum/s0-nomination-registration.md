# S0 - Nomination and Registration (general; executor: controller; gate: G0)

Purpose: turn a user nomination into a clean, deduplicated, dated deep-dive
record before any research lane starts. Nothing downstream may begin while G0
is open. The profile file supplies the concrete nomination unit and tiering
examples for its class; everything here applies to every class.

## Execution checklist
1. Record the nomination verbatim in `00-record/nomination.md`: object name as
   given, the object CLASS named at nomination (vendor, technology, market,
   client-integration, or an accepted new class), everything the user attached
   (email, deck, URL), the deadline the user set at nomination time, and the
   initial tier T1. Add the machine lines the checker reads: `Object:` (or the
   legacy `Vendor:` alias on profile B1 records), `Deadline:`, `Tier:`,
   `First real DD:`.
2. Disambiguate the entity BEFORE any other work (SPK-002 entity-match; CER-001
   ladder for Chinese entities). Write `00-record/entity-match.md` with the
   token `Entity match:` and an ISO date, listing exact-match versus
   similar-name candidates with the evidence that separates them. Precedent to
   keep in mind: two unrelated companies both carrying the "EOS" token.
3. Deduplicate against the living registers (master register of the class,
   EKAS corpus, any earlier dossier). Reuse an old basis only after re-checking
   it against live sources the same day, tagged `[reuse-MMDD, verified]`.
4. Build `00-record/document-register.csv` (schema in templates/): every file
   received with name, date, pages, type, plus what is missing. Absence is
   data; the what_is_missing cell is never empty.
5. Write `00-record/thesis.md` in 3-5 lines: which buyer or beneficiary, which
   problem, what GSP gains. It is a hypothesis to be tested hard in the lane
   stages, not a conclusion. (Profile B1 keeps the legacy filename
   prospect-thesis.md; the checker accepts both.)
6. Seed `00-record/flag-register.seed.csv` with exactly the seven baseline
   classes FL-1 to FL-7 plus any class-specific items noted at intake (the
   profile lists its typical extra classes). Statuses are descriptive labels
   only.
7. Confirm folder placement: everything lives under the mission folder named
   in the profile (B1: `docs/<date>_ddv-<vendor>/`; other classes follow the
   same shape).

## Gate G0 predicates (see gates.md for the script view)
Entity validated with a dated result; no duplicate dossier; document register
complete with missing items named; thesis and seed flag register written; tier
and deadline recorded; all artifacts inside the mission folder.

## Common pitfalls
- Starting a research lane on a name that has not been entity-matched. The
  screen report then inherits the wrong entity's facts and every downstream
  number is unfixable without a rebuild.
- Treating the tier as fixed. T1 is always run; T2/T3 are the user's choice
  after reading the screen report, never the fleet's initiative.
- Leaving what_is_missing blank because nothing seems missing. Write `none`.
- Starting without a stated object class. Ask once; do not guess a profile.
