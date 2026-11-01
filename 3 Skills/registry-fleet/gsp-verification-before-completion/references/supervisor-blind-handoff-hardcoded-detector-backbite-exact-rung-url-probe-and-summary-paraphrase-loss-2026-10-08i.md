# Supervisor lessons — batch I (2026-10-08 late): blind-handoff, parser two-era sanity, hardcoded-detector backbite, exact-rung URL probe, summary paraphrase loss

Continues the 2026-10-08 letter series (f=git-closeout/vault/DAG-edge, g=item-bank quota/forbidden-word context, h=stale-notification replay/prepost sensor). Boards in play: GAYAMANUAL-1007 (V15 final), PSIKOTES-1008 (bank wave A–F, QC trio L18/L19/L20, FIX-3/4/5, CS-3), MLSCCTV-0930 (F2d-Ra resume, F2e master).

## 1. Blind judgment with a PROTECTED MECHANISM, not just a declaration
When two independent scorers judge the same byte in parallel, the leak channel is the handoff payload, not good intentions. Observed upgrade (GM-J15A): the peer's sheet ALREADY EXISTED on disk during the run (peer mtime earlier), yet blindness held because (a) the parent-handoff carried only gate results + pin hashes, NOT peer scores, and (b) the reviewer declared "directory census shows file names only; I did not open it". Durable rule for orchestrators: **handoff payloads to second-seat judges must contain verdict-gates and artifact pins, never peer aggregates.** Verify blindness structurally by mtime ordering (scorer's own sheet timestamp < peer sheet when claimed-first; or when peer sheet predates, demand the explicit non-read declaration naming the mechanism).

## 2. Parser must prove itself against TWO PRIOR ERAS before the final verdict
GM-V15 adjudication printed a sanity clause: recomputing from raw cells reproduced the reshoot-2 prints exactly AND the V13-era prints exactly, before the final aggregation was trusted. Generalizes the supervisor's own anti-hallucination discipline (measure fresh every turn) to derived-number instruments: **a parser/aggregator used for a release-gating number must first reproduce known historical outputs from its own inputs.** If it cannot, the parser is wrong, not the history. (Contrast failure mode seen same session: supervisor's own sensitivity list mis-assembled 3-vs-4 downgraded cells gave 3.5 vs claimed 3.33 — read the artifact's own structure section BEFORE computing, then compare.)

## 3. Hardcoded-detector backbite: gate bakes the OLD claim as its expectation
Class discovered twice in one board (PSIKOTES CHECK 33): a QC detector that compares solver output against a **hardcoded literal of the pre-fix claim** (`if jPos != [1,4]` while printing "Rationale says '1 or 4'") will keep emitting the fixed finding forever after a legitimate fix — positive-palsu-by-design, the mirror of the self-referential pin class (CS-1/FIX-2). Signatures: (a) fixed item still listed post-fix; (b) the failure message quotes pre-fix text verbatim. Cure path observed end-to-end and worth copying:
- The WRITER must not edit another account's instrument. Instead: build own text-reading claim-check + report the detector defect in the result (FIX-4/FIX-5 did exactly this).
- The TOOL OWNER reconciles: archive era-instrument with sha (pre-cs3.py), switch detector to read-the-artifact-text, and add **back-detector red-green variants** (R8–R10: re-inject the old defect, detector MUST fire again) so the relaxation is proven discriminating, not dulled.
- Baseline "before" output is archived too (pra-rekonsiliasi.txt) so the era transition is evidenced, not asserted.

## 4. Delta-byte arithmetic = surgical-edit proof
Repeatedly decisive: byte-count difference between pre/post files equals exactly the sum of (len(new)-len(old)) of the edited phrases (FIX-2 −10 B label swap; FIX-4 +4 B; FIX-5 +97 B; PSIKOTES RT 26 B transposition typo). Pair with reverse-edit reconstruction (edit back → sha equals pre-pin) for cryptographic "only this clause changed". Cheap, deterministic, catches silent rewrites that line-count checks miss.

## 5. Probe the EXACT URL from the evidence ladder, never a guessed canonical one
Near-miss false conviction (vendor research): supervisor probed `cdn.example.com/News/News/201912/000000` (normalized guess) → 200 but no "Vendor Name" token → almost ruled "address not proven". The ladder rung held the true URL `.../000000_000000_0.htm` (http, with numeric suffix) → 209 KB, token present, title present. Rules:
- For acquisition/QC verdicts, replay **the byte-exact URL recorded in the rung/ledger row**, including scheme and suffixes.
- Soft-404: HTTP 200 with body containing "not found/404" markers — judge by body semantics, not status code (worker's "404 permanen" claim was coherent under this reading).
- When your probe contradicts a worker claim, first suspect your probe's address (lesson-ke-14 pattern: pin the artifact address before rebutting).

## 6. Summary-layer paraphrase loss = flag for decision, not defect
Master-table assembly (MLSCCTV F2e) merged a verified branch address correctly into the register layer but rendered the reader-facing cell as narrative DISCLOSURE ("address printed in article body") without the verbatim string — information survives upstream, lost to the master reader. If the builder design is deliberate (`cell += DISCLOSURE: catatan`), classify MINOR-for-disposition: controller chooses verbatim-in-cell vs referenced-paraphrase (two legitimate channels; precedent kutipan-vs-deskripsi L.A.4). Do not convert a design choice into a worker FAIL.

## 7. Census instruments must read real headers first (recurrent, 12th instance)
Two same-turn supervisor probe failures before verdict: "68 rows without URL" (URLs live INSIDE D-K33 status-formatted cells, no column named `url`) and "model-unik=1" (column is `Product Model`, guess was `model`). Also: delta rows with empty `vendor_key` are partial-update-by-design keyed on `row_id` — downstream must merge-by-row_id, never append-blind (this exact check — 2 partial updates + 14 appends + idempotent + unique — is what made F2e's CHECK 5 a real gate). Read the header row and one sample row before writing any census regex.

## 8. Stale/replayed completion notifications
A "Task completed" notification arrived while the board showed the card RUNNING and its output file absent; the notification's result text was the OLD blocked-run summary. Rule unchanged and reconfirmed: the verdict waits for the artifact on disk; guard greps prevent double-posting when the real completion notification arrives later. (Full mechanics in batch-h file.)
