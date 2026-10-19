# Supervisor lessons 2026-10-07b: premature pin-freeze, same-name artifact addressing, send fallback

Condensed from the 07-10 evening wave (PROMANUAL-V2 closeout, INDUK-1006 E-09/E-11 rulings, PV-1007 render chain, RAFIFFINAL FG2/FG3/REG-D3/RAKIT-D3c, GAYAMANUAL GM-L1). Extends `supervisor-artifact-over-summary-who-closed-and-kanvas-semantics-2026-10-07b.md` and `supervisor-verdict-ledger-vacuum-pass-com-nondeterminism-and-done-label-census-2026-10-07.md`.

## 1. Premature pin-freeze class (MATERIALLYIZED, first real case)

A merge register promoted 1 minute after its parent lane closed `partial-handoff` consumed the lane's self-declared PROVISIONAL hashes as final: 8 figures with a named margin-defect list (from the parent's SISA_KERJA) entered the combined register with status "siap" and zero defect annotation (grep of the defect keyword in register + verification file = 0 hits, probed directly). When the future patch card lands, those 8 sha16 shift and the combined register is basi-by-construction.

Durable rules:
- Before countersigning any MERGE/COMBINED register card, read every parent's partial-handoff SISA_KERJA named-defect list and grep the merge artifact for any annotation of those defects. Silent "siap" over a known-defective byte = tagihan keras in the vonis, with explicit "valid as snapshot of hour X, not final pin" wording.
- Prefer remedy-by-regeneration: if the merge has an idempotent archived generator script, the clean path is patch -> rerun generator -> rerak, never manual edits to the frozen register. Verified here: the same generator later produced a byte-identical rebuild (17/17 snapshot hashes matched), so regeneration cost is near zero.
- The worker-side virtue to praise and propagate: AGE-HONEST HASHES - a report stating "sha16 currently reflects pre-patch artifacts; do not use as final pin; regenerate after cleaning" is worth more than a hash that merely looks final. Verifier duty: check whether downstream consumed such self-declared provisional pins anyway.

## 2. Same-name artifact addressing (supervisor self-rebuttal, pelajaran-ke-14 extended)

I rebutted a worker's "figure 7.3 orphan (marker absent)" verdict by probing a marker that exists - in the WRONG FILE. The board had two `naskah-lengkap.md` (one per mission subfolder, same filename, different books); the worker's claim was true for its own manuscript and survived a correctly-addressed probe. Durable rules:
- Before rebutting any finding, lock the EXACT absolute path the finding speaks about, and echo that path in the probe output. Filename alone is not an address on multi-mission boards.
- Self-correction goes in a SEPARATE comment on the affected card (never edit the old comment), per user discipline 05-10; state what changed and what did not.

## 3. Send-channel fallback when terminal payloads break mid-turn

Long combined terminal commands (heredoc + `python -c` with nested quotes + `$(cat file)` chained) intermittently failed transport-side with "Invalid command: expected string, got NoneType" - the command never reached bash. NOT a "terminal is broken" claim: short forms and plain `cd X && cmd` kept working. Durable retry-shape lesson:
- When a terminal send is rejected 2+ times with that shape error, stop re-sending variants; route the post through `execute_code` with `subprocess.run(['hermes','kanban','comment', tid, text])`, reading text from the temp file. Same call can then re-show the card and count the guard in one round-trip.
- Split guard+post+contract into separate short calls rather than one mega-call; a rejected mega-call wastes three turns.

## 4. Guard-phrase collision

`grep -c "<phrase>"` on a card can match the WORKER's own result text quoting similar words (returned 3 when my comment existed once). Use a unique heading prefix of your own comment (e.g. "Countersign pengawas silang atas X") as the guard string, and when a combined command fails, re-check with that exact-prefix grep before assuming double-post.

## 5. Parser field-blindness recurrence (pelajaran-ke-11, four fresh cases in one session)

- Register JSON array lives under key `entri`, not `figurs`/`items`; picking `list(j.values())[0]` grabbed a string field and crashed.
- Manifest entry counts: naive `len()` on an INT field raised TypeError; fields may be counts OR lists - normalize with a `num()` helper.
- Register table column "Berkas" held `figures-fg2/gbr-...png` with backticks, not the bare filename I assumed: first pass reported 38/38 mismatch, corrected parse gave 38/38 match. Wrong-parser "all missing" reads are instrument defects, not artifact defects - always print keys/first-row before aggregating.
- Naive path regex cut at whitespace, producing fake "path not found" for `DEMS/01 Masukan/...` and glob patterns; the worker's root_map verifier was more correct than my quick probe. Declared the correction openly.

## 6. Cheap cross-card controls that kept paying off

- MTIME-FREEZE CONTROL: prove "upstream untouched" by comparing file mtimes against the run window (e.g. engine/resep/naskah all older than claimed window). Zero-cost, deterministic, used across four boards; also catches the reverse (a "no-mutation" card whose claimed file is younger than its own window).
- Pin-lineage continuity: every re-verdict card must cite the CURRENT release pin (not the superseded one); when a ruling promotes bytes, the ledger of prior generations (`.cacat-N`, `_arsip-prerb`, `_arsip`) must remain probe-intact - verify old bytes still exist rather than trust "archived" wording.
- Two-notification redelivery of an already-countersigned card = verify state consistency, post NOTHING (guard grep first). Ruling-text that quotes a size which matches a DIFFERENT variant than the named winner needs a disk disambiguation line before downstream builds (E-09 case: cited size belonged to the scanner-FAIL variant).

## 7. Map-census self-transitions

Board counts drift between draft and post even when nothing is wrong (other cards close/promote mid-turn). Always print the map at comment time, and when the final census differs, append a one-line correction to CONTRACT citing pelajaran-ke-9; include the self-referential case where the card being countersigned is itself the transition (SA3D blocked->vonis).
