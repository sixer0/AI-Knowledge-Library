# Supervisor wave 2026-10-06b (VISUAL R12→F17/INV-9/A19, RAFIFUNITY close, PROMANUAL-V2 resume-wave)

Lessons extracted from countersigns performed purely from disk measurement. Each entry: symptom → root cause → durable rule.

## 1. Manifest probe must read the CANONICAL column pair (R12 false-positive)
- Symptom: probe over `assets/aset.json` printed "6 berkas cocok, 56 hilang" on a manifest later verified 62/62 present.
- Root cause: probe read `png`/`sha256_png` keys that only some entries populate; canonical pair is `path`/`sha256`.
- Rule: before trusting any JSON-manifest sensor, print one sample entry and identify which fields are universally populated. "N berkas hilang" at absurd scale = almost always parser column error, not missing files. Re-probe with corrected columns BEFORE stating any finding. Same class as V4/V1 path-regex false positives (2026-10-06a): the instrument, not the artifact, was wrong both times.

## 2. Structure parsers must tolerate blank lines (R14B caption false-negative)
- Symptom: adjacency parser reported "caption BAWAH: 0 | DI-ATAS: 0" while all five captions were correctly below their images.
- Root cause: markdown separates image line and caption line by a blank line; parser required strict k±1 adjacency.
- Rule: positional checks (caption-below, heading-followed-by-table, etc.) must scan a window (e.g. next non-blank line), and when a positional check returns zero on BOTH branches, treat it as instrument suspicion first: dump the actual line map (grep -n of both patterns) and read it before any verdict.

## 3. Verdict prints inside artifacts can be from an older era (RWG-R17)
- Symptom: `rwg-laporan.md` contained "VERDIK GERBANG DIRI BAB 16: FAIL" while the card claimed complete.
- Resolution: the FAIL print was from run-2 (pre-edit bytes, header pointed to parent card); the LIVE byte passed the same meter re-run by supervisor. Two prints, two eras, coherent — not a contradiction.
- Rule: when a stored verdict contradicts a claim, do not adjudicate between prints — re-run the instrument against the LIVE artifact and let the fresh print govern; then explicitly declare the era-lineage of both prints in the countersign so nobody "reconciles" by editing history.

## 4. Invocation parity when reproducing worker instruments (cecer_meter M2 None)
- Symptom: supervisor re-run printed `M2 definisi-first None% (0/0)` while worker printed 100% (15/15).
- Root cause: supervisor invoked `cecer_meter.py <file>` bare; worker's runner passes the per-bab `istilah` argument that feeds M2.
- Rule: reproducing a worker's instrument requires reproducing its invocation (check the runner script in `_work_<card>/`). If only partial parity is achieved, state exactly which sub-metrics are independently verified (headline verdict, M1) and which remain worker-declared (M2) — never silently downgrade or upgrade.

## 5. Unchanged manifest/mtime is itself evidence (A19 partial)
- Symptom: card claims "mechanism installed, population NOT yet re-rendered".
- Verification: `assets/aset.json` sha + mtime identical to the census taken two hours earlier → disk state matches the partial claim; zero hidden claims.
- Rule: for partial-handoff verdicts, check the negative space — pins/timestamps of things the worker says they did NOT touch must be unchanged since your last census. A partial that lies about scope-creep is caught by unchanged-bytes evidence, the same way a resume is proven by an unshifted frozen naskah pin (SPEC4/RWC/RWE pattern: `bab-9 8ce560f8` unshifted == "not rewritten" verified by byte).

## 6. Close-via-audit for gave-up cards whose artifacts exist (SPEC5 precedent)
- Pattern: builder card exhausts retries (gave_up ×2) BUT final artifact + full raw-print report exist on disk (DOCX born after the timeout event, report contains lint/datumcheck/uji-tampil prints, summary=PASS).
- Correct closure: assignor watchdog audits report-vs-card-scope item-by-item from the frozen artifact and closes via jalur-asignor; re-dispatch of the same render is FORBIDDEN (wastes a full turn and risks mutating a passing artifact).
- Preconditions the supervisor verified before endorsing: artifact size+mtime identical between supervisor censuses (frozen), report contains raw prints not claims, pin pair recorded. Watchdog's closure comment + supervisor countersign form the decision trail.

## 7. Adoption blocks must carry DUAL pins when revisions followed the verdict (F17/INV-9)
- Situation: verdict-lepas bound byte `a3503a73` (revB); post-verdict named revisions produced live `eddb2866` (revC, self-audit insertion). Fleet SOUL block adopted with BOTH: "pin hidup eddb2866 (revC; badan aturan a3503a73 sah era revB, ledger di CONTRACT)".
- Rule: any fleet-adoption/closeout artifact must name the live pin AND the verdict-bound body pin plus a ledger pointer — otherwise downstream picks a pin arbitrarily (the pin-komentar-vs-artefak-hidup class, now prevented structurally). Residual gap to always check at closeout: the verdict-bound byte should exist as an ARCHIVED FILE, not only as a hash string; label drift between archive filenames and prose usage ("revB" filename = different byte than "badan era revB" prose) needs one ledger line before git closeout.

## 8. Persistence guards for fleet standards need red-green proof of specificity (INV-9)
- Verified pattern copied from INV-8: synthetic-red test = strip the standard block from ONE sandbox SOUL copy → guard must FAIL exactly that profile, leave the other 17 clean, and NOT trip the sibling guard (INV-8 unaffected). Plus byte-exact reconstruction diff (delta = docstring + marker block only) and byte-identical backup + manifest.
- Supervisor duty: reproduce the suite read-only and compare fail_total against the pre-existing baseline (here 3: INV-3×2 + INV-6) — zero NEW fails, and declare the baseline as owned by another lane rather than endorsing it as "clean total".

## 9. Board census must be measured, patched into draft, then sent (map discipline)
- Recurring micro-failure this wave: verdict drafts contained placeholder or remembered map numbers ("2 running" when the tool printed 1). Fix procedure that worked: run the awk census BEFORE sending, sed the real numbers into the draft file, grep-verify the draft contains the printed value, then post; if a wrong number already shipped, post a SEPARATE correction comment quoting the tool print (never edit silently) — lesson-ke-9 applied 3× this wave, each time the vonis itself unaffected because all its numbers came from same-turn prints.
- Census one-liner: `hermes kanban list | awk '/TENANT/{if(/done/)d++; else if(/running/)r++; else if(/blocked/)b++; else if(/ready|todo/)t++} END{print d"/"r"/"b"/"t}'`.

## 10. Resume-with-gate is the standard closer for oversized builder cards
- Empirical (6 closers in one board): freeze naskah across runs; closing turn does gate-only work (meter + six-field report) and completes. Supervisor proof points: at least one per-card artifact UNCHANGED from the previous census pin (proves "not rewritten"), plus named deltas for the rest (declared, direction-plausible: ±3..+356 B small edits; a −23% shift with NO report = audit-vs-blueprint bill, not assumed benign).
- When even the gate loop times out 3× and only the report is missing, recommend explicitly: next run = meter+report+close (<30 min from full bekal) OR close-via-audit per SPEC5 precedent; never a 5th same-scope turn.

## Cross-check with existing references
- Complements 2026-10-06a files (sensor pitfalls, two-era pins, jury corridor). The −23%/+103 B unreported-shift audit bill is carried into the successor micro-cards' scope by the controller (verified: micro card bodies literally include "AUDIT STRUKTUR BAB-3/5") — supervisor notes that survive supersession must be checked against replacement card bodies, which is how recommendation-loss is detected (here: zero loss).
