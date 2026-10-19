# Supervisor lessons: artifact-first reconciliation, hotspot ops, self-guards (06-10/07-10 INDUK+PROMANUAL-V2 supervision)

Descriptive names, not global "pelajaran-ke-N" numbers (that series already lives in
supervisor-verification-and-sensor-discipline.md; reusing numbers collides).

## Artifact beats summary (even beats your own verdict)
- When a card's result text and its own measured artifact disagree (observed: result said
  "void=2 [47 56%]" while its audit_pass7.json measured void_pages=[30,37,55,69,74]),
  the ARTIFACT wins. Reconcile before citing any number.
- A supervisor countersign drafted from the narrative comment can itself miss the
  result-vs-artifact contradiction (this happened: the worker's short-check caught what the
  supervisor's verdict had not). Rule: open the artifact's measured fields (JSON keys like
  `measured`, `void_pages`), not just the prose, before ruling.
- Frozen-copy wrappers add bytes: a preserved "alt" copy may differ from the original claim
  by the frontmatter wrapper size (+334 B observed). Declared wrapper != content mutation.

## Cross-card citation robustness
- Cite sha16 of a file between cards, NOT byte size: writers mutate the file mid-window
  (observed: TA cited 37.659 B of a file still being written by RT; disk final 38.038 B).
  Line count + classification token survive; size does not.
- Reproduce a verifier's hash/number by RUNNING ITS OFFICIAL SCRIPT, not by guessing hash
  formulas (three naive formulas all differed from `c61a5f18...`; the script run matched).
- Two tools measuring the same property with different definitions (regex vs scanner,
  strict threshold vs tolerance zone, body-with-footer vs body-excluding-footer) legitimately
  differ in count. Verify DIRECTION and MAGNITUDE, declare both definitions, never call it
  a contradiction.

## Double-issuance / hotspot playbook (same output path, two cards)
Observed 4 cases in one day (B18, L5, L7, L6). Healthy worker-side handling, in order:
1. Detect: two size/sha probes spaced apart showing the file growing = another writer active;
   read `task_ref:` frontmatter of the file for ownership evidence.
2. Do NOT write while the sibling run holds the lock. Flip your card's scope to
   verify-and-align (measure the single artifact against BOTH cards' gates).
3. Preserve your own variant as a frozen copy in work/ with a declared frontmatter wrapper;
   never delete either candidate.
4. Re-verify the SIBLING's bytes against your own gates and report pass/fail - this converts
   an ownership fight into a content decision for the controller.
5. Escalate needs_input with the two decisions the controller must make (path owner,
   duplicate-card merge/cancel). Never self-supersede.
Dispatcher-side root cause (report upstream): re-issuing a card with corrected spec WITHOUT
explicitly superseding/closing the old card = two cards, one path. Correct mechanism:
explicit supersede at issuance. Watchdogs (task-monitor class) should detect dual-writer
pairs and route a comment-only note, never touching card status.

## Self-text guards before posting verdicts
- Guard every outgoing human-facing text for U+2014==0, U+00B7==0 AND CJK==0
  (CJK leaked twice into supervisor drafts: 收敛, 时刻). Run the guard from a small python
  script FILE; nested double quotes inside `python -c "..."` inside shell broke command
  delivery twice ("expected string, got NoneType" at send).
- If a command/tool call is rejected at submission 2+ times with identical arguments, do NOT
  retry unchanged: change strategy (different working dir, shorter form, or run the same
  Python probe via execute_code - which worked every time this session).
- Board-map drift: print the awk census in the SAME turn as posting; if the map changes
  between draft and post (self-referential transitions included), post a separate
  addendum/correction comment - never edit a posted comment.

## Promotion discipline patterns worth demanding of builders
- Promote-with-archive: previous release renamed `.cacat-N` / `_arsip-prerb/RBUILD-<sha>.*`
  + PIN ledger; every ever-probed byte stays recoverable. Multi-generation ledgers verified
  across PROMANUAL-V2 (5 book generations) and VISUAL sajian (5 generations).
- Freeze-the-engine: pin engine sha16+mtime once, re-probe each turn (caf47d62 @09:01:20 held
  across ~10 cards). Any mtime newer than the artefact under verdict = engine drift finding.
- Verifier must never patch the artefact it judges; findings become named follow-up cards.
- Stale-ledger class: after any rebuild that mutates the release, downstream gates must
  migrate pins explicitly ("vonis lama dinyatakan batal sesuai kartu") - watch for gerbang
  v3-on-byte-v2 inheritance.
