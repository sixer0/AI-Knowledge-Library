# Timeout-Death-by-Reasoning, Card-vs-Artifact Adjudication & Replay Discipline (DDV-STD-1009 / RAFIF-MANUAL-FINAL-1009, 09-10)

Five patterns validated while supervising four concurrent missions in one afternoon.

## 1. Death by REASONING (distinct from pre-artifact death and partial-modal death)

BUILD-GEN timed out 3x at 1814s each. Signature that separates it from healthy
resume cases (`crash-loop-and-retry-modal-triage.md` section 1):
- target builder file exists but is **0 bytes** (created, never filled);
- only probe/scratch files grow between runs (`work/probe_*.py`);
- `hermes kanban log <id>` tail shows the worker still READING library/source
  files ("let me look at build_std.py ... grep CIT_RE ...") when killed.
State did NOT advance between runs -> steer alone will not fix a loop that
burns its budget exploring. Escalation ladder after such a pattern:
1. first occurrence: steer with measured state map (what is DONE on disk, what
   remains, exact gate commands) + unblock;
2. second occurrence of same signature: steer must CUT the exploration - name
   the exact skeleton to copy (a sibling green builder in the same mission),
   forbid further library reading, mandate build->assert->scan ONCE;
3. third occurrence with still-zero modal: REASSIGN (pattern proven: R-BUILD2
   class finished on another profile), not another passive retry. Record the
   threshold decision in the contract before acting.

## 2. Card text vs artifact measurement conflict -> controller adjudicates by MEASUREMENT (D-24 pattern)

Card said "Moda A campuran per-paragraf"; RULE RAIL-BUKTI selects mode
MECHANICALLY from the manuscript. Three runs died debating this. The controller
must not leave such contradictions to the worker: parse the frozen source
yourself (citation-bearing prose blocks = 0 of 115; the only `[R-n]` token sat
in frontmatter), rule the mode in a card comment + Decision Log entry, and
declare the card's phrasing a falsified upstream hypothesis. Two hard edges that
come with this ruling: (a) never let a worker ADD fake provenance to satisfy a
mode the content doesn't support - content-freeze pin wins; (b) paste your own
counting printout into the ruling so the next run can't re-litigate.

## 3. Gate prints older than the artifact = rerun the gates yourself

FIX-QA's printed scanner log (16:05) predated the final docx rebuild (16:24).
Worker claim "gerbang tercetak segar" was checked by RE-RUNNING scanner + lint
on the final bytes in the verdict turn, plus a byte-stability probe (sha16
unchanged since my own steer measurement) to validate "run-4 only verified,
didn't edit". Never diff-compare two logs of different eras; compare tool
output of THIS turn against the object that will ship.

## 4. Timeout chain that actually advanced: close-book steering

FIX-QA died 3x too, but each run grew real modal (edited source -> sanitized
builder -> full rebuild with all gates green at 16:24). When the remaining work
is ONLY the result write-up, say so explicitly in the steer ("sisa = penutupan
saja, jangan rebuild ulang, jangan sunting apa pun") - a worker that rebuilds a
green artifact burns the window again. Byte-stability between your steer-time
measurement and completion proves the worker obeyed; cite both hashes.

## 5. Role-capability gap closed by worker-created executor card is LEGITIMATE

TA session had no code-execution tool; instead of faking the merge or blocking,
it created REG-GABUNG (assignee gsp-coder-execution) with full handoff body and
parents = all four upstream registers. Controller verdict accepted this and
cross-checked the card's entry counts against the register files on disk
(825/641/743/1105 - note registers may be dicts with a `citations` key; a naive
len() on the top-level dict reports ~4 and looks like data loss). Distinguish
DECLARED deviation-with-correct-closure from silent failure; the former passes L2.

## Measurement gotchas this session
- json register shapes differ per producer (dict-with-keys vs list); measure
  the shape before counting entries, or you will "find" empty registers.
- middot triage by LOCATION: cover chrome + header/footer parts are declared
  D16-sah; only the BODY zone counts as defect - parse headers/footers
  separately from document.xml before declaring pass/fail.
- `hermes kanban show --json` can return card fields empty while plain `show`
  carries them; fall back to plain show + grep for status/result lines.
- Engine version bumps mid-mission create BREAKING downstream obligations
  (datum-house-style v2.3.0: Register.emit rejects unit=None -> register pin
  changes). When steering a rebuild card, always state which engine version is
  LIVE on disk and what its breaking deltas mean for that card's pins.
