# Supervisor wave 2026-10-07b: artifact-over-summary, who-closed audit, render-kanvas semantics, done-label census

Board coverage: PROMANUAL-V2 (RBUILD2/G8SYNC/SERAH-B closeout), INDUK-1006 (L6/L7/L12/L13/FIX-SA3 chain), PV-1007 (riset+register+render batch-1), RAFIFFINAL-1007 (D2W parts census). All numbers below are tool prints from that shift.

## 1. Artefak menang atas RINGKASAN termasuk ringkasan vonis pengawas sendiri (pelajaran-ke-14)

FIX-SA3C result claimed `void=2 [47 56%]`; its own artifact `fixsa3c_audit_pass7.json` had `measured.void_pages=[30,37,55,69,74]` (5 pages). Worker L12B caught the contradiction by reading the JSON directly and ruled "artefak menang: 5 halaman". **My own countersign of SA3C had earlier read the correct 5-page list from the six-field comment but missed the contradicting result line** - the reconciliation rule must be applied to supervisor verdicts too.
Recipe: when a card's result and its machine artifact can disagree, read the artifact's structured fields (`json.load(...)['measured']`, not grep of prose); if a prior supervisor verdict cited the same number from a narrative comment, state which surface it came from.

## 2. Audit SIAPA yang menutup, bukan hanya APA yang mendarat

R3 PV: notification `gave up (retries exhausted)` then `completed` with result text "penutupan controller ber-bukti" - but the Runs table showed `#5385 completed @agentriset 0s`: the closing text was authored by gsp-master through the worker-result channel. Substantive audit still passed (14/14 recipes rendered, 28 files, sha spot-checks), but attribution in my first verdict was wrong and needed a separate correction comment (never edit the posted comment).
Recipe: before accepting "closed by controller" framing, read the Runs table (run id, assignee, duration). A 0s completion run = text injected by another hand. Kernel labels (`gave up`, `done`) on cards with complete artifacts = run the completeness audit (user standing rule), never blind re-dispatch.

## 3. done-label census sebelum promosi kartu rakit (RAFIFFINAL)

D2W4/W5/W8 status `done` while their results were `partial-handoff`; `parts/` census found five 177 B `(menyusul)` placeholder files, bab-11..14 zero parts, bab-22+lampiran missing. Downstream rakit card (D2W11) correctly reported 9 holes via register instead of patching (its contract forbids content fixes) - valid report, NOT promotable manuscript.
Recipe: before a rakit/promotion card is trusted, census the parts directory by size+mtime (`all(size > 5 KB)`), and cross-check "done" cards whose result_len is small or whose result starts `STATUS: partial-handoff`. Status done = kernel label; only byte census is a verdict.

## 4. Gate yang mengukur target sendiri bukan target mengikat (kanvas vs nominal)

PV L11 batch-1: manifest entries carry BOTH `kanvas_target_mm` (125/176, binding amaran P-08) AND `nominal_mm` (128/166, legacy grid); the extent-dev gate measured dev against each figure's OWN nominal and printed 0,0% PASS - it structurally cannot see "figures still on the old grid". Two verbatim-copy figures additionally rendered at 118,03 mm, contradicting the result's "lebar hanya token 128/166" (declared only in the render log via `nominal_mm_asal`).
Recipe: for any dimension/extent gate, ask "which field is the binding target and which does the gate actually compare against?" If gate-target mismatch exists, escalate the semantic question BEFORE mass production (63 figures pending), same class as F-GAKUR-01 (meter naskah vs cacat lahir-di-build). Also recompute grouped size claims: "15 PNG+15 SVG (1.175.552 B)" was 30 images (1.149.910) + manifest (25.642) - label arithmetic, non-blocking but call it out.

## 5. Append-integrity arithmetic untuk kartu resume

R1B appended an "ERA RESUME" section to r1_retorika.md. Byte test: first-105-lines prefix = 14.258 B > old whole file 14.138 B. Not corruption: a declared 120 B marker sentence was inserted at line 3 ("Era resume R1B ditambahkan"), and old seksi 9 remained intact.
Recipe for append-resume verification: compare prefix bytes vs old size, locate the delta with a marker grep, confirm the last pre-existing section is byte-present, and accept declared marker insertions (they differ from silent mutation).

## 6. Self-describing ledger (pattern to demand)

`pg-register-final.json` embedded its 14-CHECK validation results as structured fields (`check/nama/hasil`) inside the register itself; per-figure fields carried the binding amaran (kanvas, warna_kategori incl. one honest `n-a figur cacat berlabel`, sidecar 6/6, alt<=150). Verifier reads verdicts without re-running the validator; duplicate/gap census is one json.load away (my first parser guessed the wrong array key - use `entri`, lesson-11 again).
Recipe: when reviewing consolidated registers, prefer ones that ship their own validation block; when authoring one (as countersigner recommending follow-ups), ask for it.

## 7. Send-mechanics: terminal menolak perintah panjang

`terminal` repeatedly returned `Invalid command: expected string, got NoneType` when the command string was long (hermes kanban comment "$(cat ...)" + chained heredoc), even though short commands in the same directory worked fine. Working paths, both proven this shift: (a) split into short single-purpose commands; (b) `execute_code` with `subprocess.run(['hermes','kanban','comment', tid, text])` passing the full text as an argv element - no shell quoting at all, guard via `show | count(marker)`. Use (b) as fallback after 2 identical send failures; do not conclude terminal is broken (short commands kept working).

## 8. Pre-send glyph guard for Indonesian verdicts

Multiple drafts leaked foreign glyphs mid-session (CJK 豁免/时刻/收敛, typos KUNIJEMPA/gerbar/PENUTAN). Standing guard before posting: count U+2014, U+00B7, and CJK range `\u4e00-\u9fff` == 0 plus a typo eyeball, fix via file-based script (not nested-quote shell), then post. Corrections AFTER posting go to a separate comment + CONTRACT line (lesson-9 discipline), including map-line drift (census at comment time vs census at posting time differ when other cards land between).

## 9. Hotspot keempat simetris + traceroot E-07

Two L6 cards on one path both blocked-needs_input, each verifying the OTHER's candidate with their own scanner (one FAIL reproduced by me: exit 1, C-7 28,2%; one PASS exit 0, two-run logs identical sha) - deadlock koordinatif sehat, pecah hanya oleh controller (E-07 root cause: "DAG mempromosikan kartunya sendiri saat controller melepas manual"; E-09/E-10 rulings). Supervisor role: prove both candidates' gate states, name the urgent risk (canonical path held the FAIL variant; rakit reads output/blocks/), never pick. When the ruling cites a size that matches the WRONG variant (E-09 cited 53.415 B = the failing between-variant), publish the discrepancy with reproduction before step 12 lifts bad material - a one-line sha clarification closes it.
