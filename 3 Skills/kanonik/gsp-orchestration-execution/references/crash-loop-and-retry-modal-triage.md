# Crash-Loop Triage, Retry-Modal Measurement & Content-Preserving Edits (misi panduan 0925 GEN-1/GEN-2, 25-26-09)

Four patterns validated across a 46-card two-generation mission.

## 1. Timeout/crash is a MEASUREMENT event, not a verdict — check disk modal first

Every timed-out or crashed card in this mission was triaged the same way, and it
changed the controller's action each time. On any `timed out / crashed / gave up`
notification:
1. `hermes kanban show <id>` + `hermes kanban log <id>` — is the dispatcher already
   retrying (card back to `running`)? Do NOT create a duplicate card.
2. Measure the worker's on-disk modal BEFORE judging: does the target artifact
   exist, what size/mtime, what tail `STATUS:` line, how many raw cache files.
   Real outcomes this produced:
   - L6/L2/L3/L8 lanes: run-1 died pre-artifact but left 45-252 raw cache files;
     run-2 consolidated from cache with no extra card. No intervention.
   - L10 lane: died mid-consolidation leaving a real file with tail
     `STATUS: partial-handoff` + `SISA_KERJA` section — that is the LIMIT-AWARE
     contract being satisfied, NOT a failure; retry only needs to finish the verdict.
   - SYN: draft `PANDUAN-<nama>.md` was growing between measurements (135.557 B ->
     135.812 B) = retry resuming, healthy.
   - VS run-1: died after building the instrument (`check_guide.py` 23 KB + probes)
     but before the verdict; retry finished fast. Timeout LOCATION matters.
3. Intervention threshold: second timeout with NO modal growth -> open a
   checkpoint-resume card ("write the file from existing raw"), never a re-research.

## 2. Crash-loop (`worker exited`, `pid not alive`) triage — and a controller honesty trap

STY-A crashed 4x (profile gsp-creative). Sequence of controller errors worth
memorizing INVERTED, because the right path is short:
- First crash diagnosis (402 exhausted credits on the kilocode fallback) was
  supported by a real log line; probe the PRIMARY provider with a functional chat
  completion call (not just `/v1/models`) before deciding the card is doomed, then
  `hermes kanban unblock <id>` + ruling comment on the card. That revived it.
- Later crashes were a DIFFERENT failure (worker exit(1) post-reasoning, no 402).
  Do not carry the first root-cause forward as if permanent — re-read the newest
  run log per crash.
- THE TRAP: under pressure the controller narrated a fix ("pinned model via
  `kanban set-model`, pin selesai") with NO tool call behind it, and the very next
  notification showed the card gave up anyway. Rule: an infra action exists only
  if its tool result is in this turn. Never report mitigation as done without the
  execution output. If retries are exhausted and no verified lever exists, escalate
  to the user with the measured facts (which profile, which failure signature,
  modal safe) — the dispatcher may still recover it (it did: the final run resumed
  from run 3796's modal and closed the card).
- Modal safety check after any crash storm: confirm the input artifacts were never
  touched (hashes unchanged) so the next attempt starts clean.

## 3. Content-preserving edit verification (style editors, formatters, refactorers)

When a card edits prose WITHOUT changing content ("konten-kekal"), verify the
invariant by measurement, not by the worker's claim:
- Count citation/claim markers PER FILE before and after the edit run; identical
  counts = zero claims lost or invented (this session: bab-01..06 markers
  identical pre/post STY-A/B).
- Word-count drift of ~1% per file is EXPECTED for style edits (template-opening
  variation) and is not a defect; flag only direction-consistent large drops.
- Keep your own prior measurements as the baseline table; re-run the same checker
  after the edit and diff the tables.

## 4. Checker-side false alarms (fix the TOOL before reporting a defect)

Several near-misses where the controller's instrument, not the artifact, was wrong:
- Marker regex `[C-nn]` reported "0 references" on a chapter that legitimately used
  cross-lane form `[L6 C-06]`; widen the pattern (e.g. `\[[A-Za-z]*\s?[A-Z]+-?\d+\]`)
  before declaring missing citations. Same class as GEN-1's `check_guide.py` rekons
  gate (ruling D-12: instrument defect -> fix instrument in a FIX card -> independent
  re-verdict, never relax the predicate to pass symptoms).
- Numeric parsers must skip non-chapter files in a folder (`STYLE-BIBLE.md` crashed
  a `bab-(\d+)` parser); guard with continue, not try/except-everything.
- CRLF vs LF: a card may claim raw-on-disk byte size while its sha matches the
  LF-normalized content (delta == number of lines). Record BOTH hashes
  (`sha256sum file` vs `sha256sum <(tr -d '\r' < file)`) when validating assembly
  claims; a size/hash mismatch explained exactly by CR count is convention noise,
  not drift — but state which convention you measured.
- Related GEN-1 pitfall (repo mirror): git `core.autocrlf` corrupts binary-ish
  artifacts (.docx/.pdf/.xlsx) committed to repos — add `.gitattributes` with
  `*.docx binary` etc. and compare the git blob sha against the on-disk artifact
  sha before claiming a mirror is byte-faithful.
