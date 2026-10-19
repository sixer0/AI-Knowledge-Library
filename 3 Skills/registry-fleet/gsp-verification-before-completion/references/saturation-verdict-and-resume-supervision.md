# Saturation Verdicts, Stale Handoff Numbers, and Resume Supervision
(PROMANUAL-1004 + RAFAI-1004 supervision, 2026-10-04)

## 1. Three tiers of "jenuh/saturated" — never let downstream conflate them

Research lanes can carry a saturation formula (e.g. TA-D-02: ladder 8/8 classes
accounted + two consecutive cycles each <10% new release-load facts + every
release-load field has primary source + entity-match). A card closing can
legitimately claim different tiers:

- **Card-threshold saturation** — the card's own numeric thresholds were met
  (e.g. register >= 30 rows, >= 3 vendor guides, >= 8 papers). Verified by
  recounting IDs in the artifacts (unique `KL-R1b-\d+` grep = 45 confirmed the
  "threshold exceeded" claim pattern).
- **Lane-formula saturation** — the two-cycle <10% condition measured per lane.
- **Aggregate verdict** — held by the independent verifier card (R-3 class),
  not by the acquisition worker.

Supervision action: when a card result says "selesai dengan vonis jenuh" but the
artifacts contain no cycle ledger (grep token `siklus` = 0), freeze the verdict
as card-threshold only and tag the card + contract: "must not rise to final
report as lane verdict". Caught twice (R2a, R1b PROMANUAL) before any downstream
misread.

## 2. Boundary cases in acceptance formulas are precedents — escalate, don't absorb

RAFAI R3 closed JENUH using a "combined two-cycle window 9.1%" because cycle 2
was exactly 10.0% (strictly not <10) and cycle 3 was 0%. The worker was honest
(raw numbers printed, "verifier may re-judge"), but an unstated reinterpretation
of the formula, if silently accepted, becomes the norm: any lane could then
claim saturation with 10.1%+9.9%. Correct supervisor move: record as an
INTERPRETATION QUESTION to controller/verifier demanding one canonical ruling
("<10 two consecutive; exactly-10 counts as not-saturated; no combined window"
OR formally legalize the window) BEFORE the next wave closes. Same class of
lesson as the TRUSTED-tier calibration finding (one lane TRUSTED=0 vs another
51 at equal budget — gate semantics differ per lane; require one canonical
tier rule before cross-lane aggregation).

Also healthy, and worth distinguishing from premature claims: workers that hit
the boundary and instead file a PUTUSAN REQUEST (R1: "one cycle <10% achieved,
controller may rule JENUH-BERSYARAT") or hold their own verdict (R9: "JENUH
must not be issued until the UJI evidence card closes"). Support those paths;
only flag silent reinterpretation.

## 3. Stale handoff numbers: poll until the run closes, then measure

PROMANUAL TA's first completion notification quoted "317 baris, 33.408 B" —
that measurement never existed on disk at any point I watched (16:50=465 lines,
16:51=582, 16:56=642 while frontmatter still said `kerangka-paralel`). The card
then closed at 16:57 with the FINAL result quoting 642/67.981 B, which matched
my own sha/size measurement exactly. Pattern:

- If notification numbers disagree with disk AND the card still shows
  `running` (or file mtime keeps moving), HOLD the verdict; re-measure after
  the status flips to done (sleep 60–150s between probes is enough for a
  finalizing writer).
- Never write the audit comment against a mid-write artifact; the later
  re-issued notification with corrected numbers is the one to audit.
- Rule to demand upstream (frozen into contract): handoff/result numbers must
  be printed from disk at the closing turn, not captured mid-run.

## 4. Timeout at the bridge hard cap with intact modal = resume guidance, not re-dispatch

Three PROMANUAL cards (R1a, R2b, R2c) died at `elapsed 1814s / limit 1800s`
with `retry_status: ready` and a dispatcher retry already active minutes later.
Supervisor checklist that proved right:

1. Measure the modal: `ls raw/R1a | wc -l` (133 files, last write 2 min before
   death) and whether final artifacts exist (`research/R1a/` absent for R1a;
   R2b had nearly-complete korpus/register-KL/ladder + its own CHECK1+2 PASS).
2. Confirm the retry run exists (`hermes kanban show` Runs section) — do NOT
   create cards or re-dispatch (dual-controller boundary).
3. Leave one comment on the card aimed at the retry run: "do not re-fetch the
   N files already on disk; finish from modal (counts, register-KL, ladder,
   close with card-threshold verdict like sibling lanes); Ambang-B again =
   partial-handoff checkpoint with list, not buntu."
4. Watch for the PATTERN across cards: three identical 1814s deaths = the card
   class needs a bigger budget or a split (acquisition | finalization). Report
   that as a controller decision item after the second retry, not the first.

## 5. Cross-lane vocabulary drift breaks downstream gates

Four lanes of one mission used four status vocabularies for near-identical
concepts (SD/SD-parsial/PROV/KV/TK vs TP/SD/PROV vs VERIFIED/PROBE/REGISTER vs
TERVERIFIKASI-SNAPSHOT), and ID conventions differed (`R7-F01` vs bare `F01`),
which made my own fact-count come out 66 vs claimed 72 (both defensible under
different matchers). Before synthesis/merge: demand ONE mapping table (vocabulary
canonicalization) and one ID convention; otherwise the accuracy gate
mis-classifies which rows may publish. Episode family: the recurring
vendor-unique counter off-by-2 across lanes (77 vs 76, 136 vs 134) — same root
cause, no frozen normalization rule.

## 6. Leak-test of rejection lists (positive pattern)

When a lane reports discarding false-identity candidates (e.g. 10 guessed arXiv
IDs that resolved to unrelated papers), verify the claim mechanically: grep the
rejected identifiers against the published register (must be 0 hits) and check
their only appearance is inside the negative-register section with page titles
recorded. R1b passed this test ("tidak ada yang bocor ke register" = true by
grep). This is the closure half of the entity-match lesson from
[`vs-gate-countersign-and-entity-type-matcher.md`](vs-gate-countersign-and-entity-type-matcher.md): not just catching the bad
row, but proving it never propagated.
