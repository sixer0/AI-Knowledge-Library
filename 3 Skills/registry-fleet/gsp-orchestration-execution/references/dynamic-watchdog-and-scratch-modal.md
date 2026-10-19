# Dynamic Board Watchdog & Scratch-Modal Decay (RAFIF-MOBILE-0928, 28-09)

Two lessons from one night of multi-lane fan-out missions; both generalize to
any long mission with a mutating card graph.

## 1. Watchdog must query the board by TENANT, never a static id map

Real failure (28-09, RAFIF-MOBILE): a watchdog seeded with the 16 lane ids
known at blueprint time silently missed two cards created mid-mission by
legitimate in-graph amendments (TA-REV2 amandemen + lajur baru L17). It would
have declared ALL_TERMINAL while real work was still running, or kept polling
forever if a late card blocked.

Correct pattern (validated, `rm_watch_dyn.py` shape):
- Poll `hermes kanban --board default list --json` every ~120s.
- The JSON stream can carry trailing junk: parse with
  `json.JSONDecoder().raw_decode` in a scan loop, flatten nested lists,
  filter `tenant == <MISI>` (or title contains the mission slug).
- Print a transition line only when a card's status CHANGED vs previous
  snapshot (id + short title + new status + HH:MM:SS).
- Exit 0 when no card of the tenant is outside TERMINAL = {done, archived}
  (add blocked/gave_up deliberately — blocked usually needs controller action,
  so keep it OUT of the terminal set if you want the watchdog to wake you).
- Hard deadline (10-16h for 16-lane waves) then print partial state and exit;
  run via terminal(background=true, notify_on_complete=true).
- When replacing a stale static watchdog: `process kill` the old one first,
  note the swap in the report so two notifications don't confuse the user.

## 2. Scratch workspaces are EPHEMERAL — worker "modal" claims decay

Cards run in `%LOCALAPPDATA%/hermes/kanban/workspaces/<card_id>` (scratch).
Two measured incidents 28-09 (PEMAHAMAN-DEMS):
- L3 result claimed "30 ready-to-read digest files in workspace/digests/" as
  the SISA_KERJA modal; at controller measurement time the scratch dir held
  0 files — only 3 digests survived, copied into the mission's `work/` folder.
- L5 claimed 9.013 lines of per-file dumps in its scratch workspace; gone.

Rules that came out of this:
- Before planning ANY resume/continuation card from a completed card's
  SISA_KERJA, re-measure the claimed modal on disk. If it lived only in
  scratch, the estimate "tinggal baca N jam" is void — recompute.
- Card bodies for lane/research work must instruct: canonical artifacts land
  in the mission folder under `docs/<date>-<slug>/` (lanes/, research/,
  work/), scratch is disposable. The lane NOTE file (e.g. `lanes/L6.md`) is
  the artifact of record; dumps/digests that matter must be copied there.
- Controller reports should quote the DISK measurement, not the card claim,
  when they differ (L6-style honest partial-handoff made this easy).

## 3. Gate placement of style defects found in INTERNAL lane artifacts

L11 (seni-audio-nolmodal) closed clean on structure (register 54, ladder 95
URLs, raw 51 files) but carried 8 U+2014 tokens. Per the 03-09 channel
narrowing this does NOT block the lane card (internal agent artifact), but the
controller must (a) book it in contract.md as a dated known-defect line,
(b) bind it to the assembly stage (editor gaya/ASM must reach zero with the
content-kekal multiset test), and (c) require VS to scan U+2014/U+00B7 across
ALL source chapters, not just the assembled output — otherwise the scan gate
only ever sees what the assembler already normalized.

## 4. Promotion-ordering probe (HARGA-DEMS-0927, 28-09)

KB promotion ran 07:21, BEFORE the FIX-1 remediation of a verifier FAIL landed
(findings 12:00, workbook rebuild 13:03). Probe that decided severity: grep
the promoted vault/wiki object for the DEFECT string (old label) — 0 hits, so
no wrong text entered the library; but the snapshot predates RELEASE (130-row
reconciliation delta per V2). Class lesson: after any post-promotion remediation,
measure (a) defect-string presence in promoted objects and (b) mtime ordering
promoted-vs-remediated, then book a re-promotion decision explicitly — silence
about staleness is how a library quietly diverges from its source of truth.
