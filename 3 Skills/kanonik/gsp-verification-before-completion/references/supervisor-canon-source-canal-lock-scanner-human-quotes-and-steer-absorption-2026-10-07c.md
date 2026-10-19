# Supervisor lessons 2026-10-07c: canon-source pre-revision citations, canal-threshold lock, scanner human-quote false positives, steer absorption

Condensed from the 07-10 late wave (GAYAMANUAL GM-L2..L6b, VCTL-1007 RT/TA/R1/R1b/R4, GM-L3 figure bank). Extends `supervisor-premature-pin-freeze-artifact-addressing-and-send-fallback-2026-10-07b.md`.

## 1. Canon-source drift: verbatim from the MIRROR, not the REVISED BODY (materialized class)

A master doc carries BOTH an index table (mirror of an older outline) and a body with post-revision statements; an inventory card registered the delta (e.g. `mismatch_verbatim` = 25 non-identical, 17 substantive). When the writing outline then declared "INDEKS as single statement source", every block that faithfully copied the index shipped PRE-REVISION wording for exactly the delta entries — and the count grows with each block (probe: 16/16 L6 rules in blok3 were delta entries quoting the index).

Durable rules:
- When countersigning an INVENTORY card of a dual-representation doc (index+body), compute the delta set and store it queryably (JSON field, not prose). Later, when countersigning WRITE-BLOCK cards, re-probe: count how many delta ids appear quoting which representation. Report the number per block — "question X is now material in bytes".
- A worker faithfully following a flawed outline choice is SAH dalam cakupan — the defect belongs upstream (outline/controller). Never FAIL the copier; escalate the ruling with (a)/(b) options and cost comparison (cheap now vs requote N blocks later).
- Keep "tagihan hidup" (open bill) lines in vonis so the same decision is re-surfaced at each card where its cost rises, until a ruling lands. Chain here: L2 (question raised) -> L5 (first delta entries cited) -> L6 (16/16) -> pre-rakit deadline.

## 2. Scanner false positives: human quotes under trial + genre mismatch

Two shapes where a deterministic scanner's FAIL was NOT an artifact defect:
- **Pedagogical quotes**: the banned phrase ("let me know if") appeared only inside VERBATIM QUOTES OF REAL HUMAN LETTERS that the text itself puts on trial as anti-examples. Grep the CONTEXT of each scanner hit before vonis; quoted-material-with-path is an exclusion zone (same class as self-reference in standard docs citing the rule words they define).
- **Genre mismatch**: a prose-tuned channel (paragraph-length ratio C-7) FAILs a table-dense outline by design. Do not force prose to go green; either register known-defect-genre or defer the check to book-level assembly — controller ruling, with the log persisted.
- Supervisor duty when a card declares "scanner NOT-RUN (session without terminal)": run the canonical scanner yourself, persist your own log (sha16+size in the vonis), and dissect WHICH check fails before quoting VERDICT. FAIL[checks] that are all false-positive classes != work defect.

## 3. Canal-threshold lock on fix cards (F-GAKUR-01 canal variant)

When two scanner channels carry DIFFERENT thresholds for the same indicator (standard 20% vs doc <=1), a fix/resume card must lock the reference channel explicitly in its short-check, or it patches toward the wrong target. Detected by diffing the upstream worker's named channel vs the controller's close-out wording ("kanal standar" vs "kanal doc") — non-blocking note on the close card, resolved cleanly by the resume card (locked standard channel, left doc residual documented-not-forced). Praise pattern: two channels, two verdicts, never blended.

## 4. Steer-absorption verification (before-write vs mid-run)

Controller steer comments land either MID-run (PV R1B era: absorbed via append-era discipline) or BEFORE promotion (VCTL TA: comment 20:03, promoted 20:08, run 20:09). Verify absorption by CONTENT TOKEN census, not by trusting the result text: count the steer's distinctive terms in the final byte (Holistics x23, UNION x5, G-CAT-1b x4...). Also verify the timeline claim itself (comment ts < promote ts < claim ts). Pre-promotion steer is the cheaper pattern — note it to controllers.

## 5. Register anomaly arithmetic + frozen-source control (two denominators, two profiles)

Union catalogs from two sources: one register came 80 rows / 80 unique / 1..80 no-gap; the other 43 rows / 42 unique BECAUSE of source numbering anomalies (no.24 absent, no.38 double). Both are correct only if the anomaly is RECORDED-NOT-PATCHED (no invented row 24, no silent merge of 38). Countersign recipe: recount numbered rows yourself, diff rows-vs-unique, match against the declared anomaly; verify the snapshot pin (sha16 + mtime older than the whole run window) so "verified from frozen snapshot" is cross-handed. Reconciliation pairs like "80 vs 77" = two populations (heading units vs named sections) — declared definitions, not contradiction.

## 6. Supervisor parser self-defects, two fresh shapes (pelajaran-ke-11)

- **Filename case**: manifest `id` is `FIG-01-...` but files on disk are `fig-01-...`; naive exact-name lookup reported sha 0/5 mismatch. Lowercase-normalize before matching; corrected probe gave 10/10 (png+svg).
- **YAML folded continuation**: field-count regex `^\w+:` misses indented continuation lines of wrapped values, reporting "29/29 sidecars defective" when they had 14 complete fields. Read one full sample before aggregating any regex census over structured text.
Both defects were dissected and declared BEFORE the vonis was posted — instrument correction never rides silently into a verdict.

## 7. Stale-pin discovery across boards + lane-refusal praise

An inventory card found another skill's pinned reference still at revC while the live doc is revD — probe confirmed (revC token present, revD absent in SKILL.md). The finder REFUSED to patch cross-lane ("not this lane's authority", routed via defect-skill card). Praise and propagate: discovery + named route beats silent fix; controller owes a defect-skill card. Supervisor: re-probe such claims with token greps on the actual file before endorsing.
