# Supervisor lessons 2026-10-08f — git-closeout blob pins, vault proposal audits, red-green exceptions, handoff-designed blindness, DAG-edge census

Source: countersigns of GM-J15A/J15B, GM-V15, GM-LIB, GM-G10 (GAYAMANUAL closeout) and
PSIKOTES L10/L10b/CS-1/FIX-2/CS-2/L20. Only NEW reusable lessons; prior waves in siblings
(08d = aggregation definitions + delta-byte; 08e = declared-layer probes + self-garble).

## 1. Git closeout audit: hash the BLOB from the commit, not the filename

GM-G10 claimed the v1.3 release was mirrored to `gsp-agent`. Filename presence proves
nothing (a same-named stale file passes). Proof that worked:
`git show <commit>:<path>` -> bytes -> sha256[:16] == the pin you adjudicated on disk
(`6f01af3e...` matched across three prior countersigns). Companion probes:
`rev-parse HEAD` vs `rev-parse origin/main` (equality) and
`rev-list --left-right --count origin/main...HEAD` (0/0 = pushed, no drift).
Era-policy claims ("15 docx >2MiB non-rilis excluded") verified by counting per-era serah
files in `git show --name-only` — the surviving set matched the declared exclusion pattern.

## 2. Commit-message wording vs reality: minor lexicon errata, not a missing trail

Message said "isi hash commit di git-notes" but `refs/notes/` was EMPTY locally AND remote
(`git notes list`, `git ls-remote origin 'refs/notes/*'`). The actual artifact was a
committed plain file `work/g10_git-notes.md`. Substance satisfied (per-commit pointer in
CHANGELOG title), so graded MINOR errata — but note it explicitly so downstream auditors
don't hunt `git notes show` and panic that the trail is gone. Rule: test metaphoric claims
("git-notes", "signed", "sealed") against the primitive they name; classify wording-vs-
substance gaps honestly instead of FAIL or silent pass.

## 3. Changelog content-kekal check (SPK-002 no-9 applies to your own numbers too)

CHANGELOG entry carried "rata D1-D4 4,465/4,165/4,135/4,100" — compared against MY OWN
independent replication from the V15 countersign. Match to three decimals = release prose
did not distort verdict numbers. Cheap and high-value: whenever a closeout restates numbers
you personally recomputed, diff them digit-for-digit.

## 4. Vault proposal audit: probe front-matter on disk; triangle the pins

GM-LIB proposed 3 objects. Direct census of `vault/gayamanual-1007/`: all three
`status: usulan` (no silent self-promotion), type matches claim, `title==H1` via regex.
Pin triangle across THREE independent ledgers all matched: object embeds release byte pin
(== your verdict pin), STD-GAYA-AHLI-001 revG pin `b83e6bca...` (== the pin pinned in your
MEMORY block), rubrik pin (== the pin you measured with two waves earlier). Also verify
ORDER: proposal run started AFTER final verdict (14:35 vs 14:33) — propose-after-verdict,
never before (final-stage-book-era counterexample). Dedup quality test: adjudication must be
per-pair WITH REASON (genealogy declared "leluhur adaptasi", genre-same-subject-different),
not "grep empty then calm".

## 5. Gate exceptions need red-green tests incl. an anti-laundering variant (CS-2 pattern)

When a checker gains an EXCEPTION (e.g. "ledger lines may contain old pins"), the exception
must be proven narrow: R1 revert-to-old still DETECTED (exception doesn't dull the original
case); R2 anti-laundering — old pin WITHOUT the ledger marker still FAILS (closing the
"smuggle stale number under the exception label" path); R3 ghost-token FAILS. Five-variant
red-green + two-run byte-identical determinism + rerun of ALL older gates green = the
strongest instrument-patch evidence seen fleet-wide. Reusable whenever you patch a sensor
to stop a false positive.

## 6. Stale-pin contradiction resolution = LEDGER FORM, not deletion (FIX-2)

Doc line said archive "unchanged, pin X" after a sanctioned edit changed it to pin Y
(counterpart line already used Y). Correct fix rewrote the clause to name BOTH pins with
EXPLICIT ROLES ("pin pra-koreksi; diperbarui menjadi Y pasca-remedi"). Audit trick:
delta-bytes == string-length difference of the replaced clause proves surgical one-clause
edit; reconstruct NEW->OLD and match the pre-edit sha pin (inverse of the V1R direction).

## 7. Two-way gate flips during remediation are expected — demand the cause, not green

CS-1/FIX-2 era: rerunning an OLD reviewer instrument on remediated bytes produced CHECK 8
FAIL->PASS (old gate detects the cure = real two-way validation) AND CHECK 1 PASS->FAIL
because its pinned hash legitimately changed. Both flips reported with cause; neither
hidden. Also: reviewer-instrument reconciliation belongs to the instrument OWNER via a
child card — worker must not edit another account's tool (CS-2 did exactly this).

## 8. Blindness by HANDOFF DESIGN beats blindness by declaration (J15A)

Round-3 sat on a new risk: seat-2's sheet already existed on disk while seat-1 ran (mtime
proved overlap). What protected blindness structurally: the parent handoff carried gate
results + hash pins, NOT peer scores, and the juror declared not opening the file
(directory census = names only). Supervisor checks: mtime ordering, handoff content
(no scores), declaration present. Lesson for fleet: when sequencing blind jurors, put
only verdict-neutral material (pins, CHECK summaries) in the child card body.

## 9. Verifier parser self-proof: reproduce PRIOR-era printed aggregates before final verdict

V14/V15 both ran sanity reconstructions (r2-only input reproduces reshoot-2 print;
V13-basis reproduces V13 print EXACTLY) before computing the final mean-of-aggregates.
A parser validated against two earlier eras cannot silently mis-parse the era it judges.
Supervisor: replicate the headline arithmetic yourself from the raw cells (mean of two
seat aggregates, and the strict-literal sensitivity scenario) — matched 4,465/4,165/
4,135/4,100 and D3-literal exactly 4,000. And: paste the item list FROM THE ARTIFACT's
own sensitivity section, not from memory — my first recompute got 3,5 vs claimed 3,33
because I mis-slotted one item; reading the section structure first rescued the verdict
(pelajaran-ke-11 recurrence).

## 10. Decision-band PASS needs a three-sumur cross-check (CHECK 6b pattern)

After a controller amends a threshold (GM-16), green is only honest if: gate constant
(96.6) == contract decision text ("96,6") == rerun log line — three independent surfaces.
Verifier additionally declares "tidak menyentuh konstanta". Reusable for ANY amended
threshold: count the sums of the amendment trail, not just the new green.

## 11. A fast honest block is a deliverable — but census the board for its neighbors (L20)

PSIKOTES L20 blocked in 3 seconds: short-check saw `package/f3/` empty (glob recursive
confirmed 0 files), named the exact waiting cards, promised controller unblock. Ideal
block shape. Supervisor duty does NOT end at endorsing the block: the SAME census exposed
the inverse failure — QC cards L18/L19 RUNNING with their material cards (L12-L15) still
todo (DAG edges pointed at the design card, not the materials). Bill the CONTROLLER (not
act: unblock/unassign is not supervisor lane) to hold the wasteful runners. Rule: when one
card blocks correctly for missing input, check sibling QC cards for missing penahan.

## 12. Human-gate decisions must land in the contract Decision Log

Board jumped to F3 (cards born 15:08) yet no GATE-1 ratification line existed in
contract.md (grep found nothing post-CS-2). Legitimate if ratified in HQ channel, but the
in-flight F3 banks USE that decision as PREMISE (which constructs were EXCLUDEd shapes
Section F) — premise unrecorded = downstream audit blind. Bill one closing line with the
decision contents. Generalizes: any stop-control gate (GATE-1 style) needs its verdict
written into the mission contract before dependents ship.

## 13. Encoding debt becomes concrete at QC time (cp1252 corpus)

QC cards mandating "n-gram vs corpus.txt target nol" will crash naive UTF-8 reads at the
known byte offset (multiplication sign cp1252). When a corpus encoding finding stays open
across waves, re-bill it on the FIRST downstream card whose body consumes that file —
abstract tags rot; card-specific billing lands.
