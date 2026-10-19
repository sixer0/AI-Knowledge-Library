# Deterministic Verification + Light Countersign (validated 2026-08-29)

## Problem
A narrati­ve verification dispatch (multi-check contract, e.g. "scan 48 SOULs,
grep 4 skill locations, probe 3 endpoints, reconcile contract") sent to a
gsp-* verifier via the HQ bridge died at `hermes CLI timeout after 1800000ms`
— status `failed`, empty `result`, 30 minutes burned. Heavy LLM-driven checks
are the wrong shape for a dispatched oneshot with RUN_TIMEOUT_MS=1800s.

## Validated pattern (this session)
1. **Script the checks.** Write one deterministic Python script that performs
   every mechanical check and writes a timestamped report to the contract's
   docs folder, printing one line per check (`CHECK n: PASS|FAIL|NEEDS_REVIEW — name`)
   plus a final `VERDICT:` line. Reference implementation:
   `C:/Users/TRIAL/workspace/gsp-hermes/scripts/verify_lean_fleet_r2.py`.
   Rules for the script: evidence from re-read files/commands only; classify
   honestly (NEEDS_REVIEW for "waiting on a human decision" is NOT FAIL);
   keep the report path fixed so the countersign can find it.
2. **Run it locally first** (orchestrator side) to fix bugs before paying a
   dispatch. ~seconds, no LLM cost.
3. **Dispatch a LIGHT countersign request** to the verifier profile. Prompt
   must be ≤4 explicit steps and forbid initiative:
   - run `python <script path>`
   - read the generated report
   - write a short countersign file next to it (agree/disagree + reason;
     explicitly instruct: NO fixes, NO extra checks)
   - end with fixed format: `STATUS: complete` + result containing
     `COUNTERSIGN: agree|disagree` and `VERDICT: <script verdict>`
4. **Poll once via background loop**, then verify both artifacts on disk
   (report + countersign file exist, verdict lines consistent).

## Results this session
- Narrati­ve dispatch: 1800s timeout, failed, empty result.
- Countersign-only dispatch of the same verification scope: ~30s,
  status needs-review, full result, countersign artifact written,
  independent reviewer confirmed the NEEDS_REVIEW item was a pending user
  decision, not a defect.

## Also caught
- The verifier's OWN summary field contradicted its artifact (summary said
  "PASS", artifact said "NEEDS_REVIEW"). Always treat the artifact as the
  source of truth and reconcile the summary in the contract doc; add an
  explicit line to verifier prompts: "result field MUST agree with your
  report's verdict line."
