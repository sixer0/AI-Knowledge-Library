# Supervision Audit Recipes - Shipped-Artifact, Channel, and Retry-Note Patterns

Condensed from dual-board supervision (PROMANUAL and another book mission + EXPOWORLD
SAJI), 05-10. Each recipe was exercised and verified on disk that day.

## 1. Scanner fleet: ALWAYS pass `--channel`

`scan_ai_footprint.py <file>` without `--channel` runs the DEFAULT channel and
produces false FAILs (observed: false C-7 FAIL on a file that PASSes under
`--channel kitab`; the gate mandate named the channel). Protocol:
1. Read the card/mandate for the target channel.
2. `--help` once per session if unsure of flag spelling (`--channel kitab|doc|...`).
3. Reproduce the verifier's scan WITH the same channel before countersigning;
   report any channel-dependent divergence (e.g. C-15 RUNTUH-kanal: raw print
   said FAIL, report said INFO because the check collapses per kanal policy).

## 2. Verify what SHIPPED, not just what's on disk

When auditing a built artifact (DOCX/PDF) that claims to embed corrected sources:
- **Unzip probe (python zipfile):** hash every `word/media/*.png` part and match
  against sha256 of the source PNGs. Proves the corrected figure (new sha) is
  actually inside the book, not just on disk. 36/36 byte-match = strong claim.
- **PDF text-layer sweep (pypdf):** extract all pages, count banned tokens
  (`_work/`, `fetch/`, internal filenames). Then CLASSIFY hits: prose that
  deliberately cites a `[measured]` trail path is content (validated chapter
  convention), NOT a leak; a footnote on a figure face IS a leak. Report both
  numbers separately - never flatten "7 hits" into "leak found".
- **Page-targeted render QA:** when the fix targeted specific pages (fig on
  hal-28/218), render/extract exactly those pages.

## 3. Divergent counts = divergent DEFINITIONS, reconcile before verdict

Recurring pattern this session: worker 22 vs verifier 20 vs supervisor probe 28
slug labels - all three correct under their own detectors (gate-wide detector /
canonical paired-word STD pattern / loose lowercase regex that swallowed 8
single-token headers). Also 412 vs 413 URLs (brace-path normalization), 73 vs
77 tags (regex definition). Protocol:
1. Reproduce the verifier's number with YOUR parser tightened to THEIR stated
   definition (the 20 reproduced exactly with >=2-segment regex).
2. Quote all definitions in the countersign; never write "N" bare.
3. If your earlier note quoted a number without its detector, issue an explicit
   self-correction comment.

## 4. Pin-chain discipline

Record `sha256[:16]` of every release artifact in every verdict/comment that
touches it (build -> supervisor verdict -> next verifier card). Three-eye match
(builder pin == supervisor pin == verifier pin) makes edition lineage auditable
and catches stale-material rebuilds for free. Same for frozen registers: re-pin
register sha16 in chapter verdicts (R3 `849835d4`, R4 `e9aacc` survived ~20 audits).

## 5. Timeout/crash notes (retry cards) - content checklist

Measure disk FIRST, then post a note (never re-dispatch logic, never verdict):
- **Artifact-born-before-death?** (naskah/DOCX/PNG present, mtime before kill,
  structure complete) -> instruct run-2: RESUME, do not rewrite from zero;
  blind re-apply is corruption-dangerous (replace-on-already-fixed URL, overwriting
  clean `arsip_pre/` with polluted state).
- **Idempotency proof missing** -> make it a run-2 checklist item (two-run diff).
- **Budget ordering hint** when a card died twice: do the cheap/no-analysis half
  first (targets already mapped by prior verdicts), geometry/analysis phase last.
- **Crash-cause triage:** log tail (`preparing skill_view` post-artifact = died
  in paperwork phase, not writing phase); STY-A 402 pattern only applies to
  <30s death with zero tool calls.
- Interim findings (vision QA on the reviewer's partial render evidence, probes)
  may be posted AS NOTES explicitly labeled "bukan vonis final - kartu belum selesai".

## 6. Vision QA as a supervisor gate, with honest partiality

Figure patches need pixel verdicts, not sha verdicts (idempotent sha proves
replication, not semantics). When QA-ing a patch iteration: test EACH prior
defect individually by number, then hunt the SYSTEMIC root - observed: callout
markers placed INSIDE a screenshot force leader lines through interior
mathematically; each patch just relocates overlap. Root fix = move markers to
outer margin frame. Cosmetic residuals (shared trunk between two leader lines)
may be accepted as non-blocker rev-2 items when text-overlap is zero - state
the acceptance explicitly. If supervisor QA and reviewer verdict disagree on a
cosmetic reading but agree on non-blocking, record both readings.

## 7. Pre-send hygiene for verdict/comment text

Before `hermes kanban comment`:
- `len(t)` sanity check - a drafted verdict file can silently truncate (observed
  229 B stub); rewrite fully if truncated.
- Glyph scan: U+2014/U+00B7 == 0 AND CJK regex `[\u4e00-\u9fff]` == 0 (one stray
  CJK glyph caught pre-send).
- Board-map figures in the draft must come from a FRESH `kanban list | awk` print
  in the same turn (two drafts said "running" where the board said 0 running -
  corrected pre-send; post-send drift gets its OWN correction comment, never an
  edit of the old comment).
- Apostrophe-heavy text -> temp file + `$(cat)`; dedupe via `show | grep -c`
  BEFORE resending after a shell EOF failure.

## 8. L0-full memory consolidation (when replace is rejected on size)

Archive the OLD RECENT TASK verbatim to `memory/refs/<profile>/<date>_*.md`,
register one line in `_INDEX.md`, merge same-category INDEX entries (10 corpus
domain indexes -> 1 category entry listing domains + active known-defects),
then one batched `operations` call doing removes+adds atomically. Do not
loop retries of a single oversized replace.
