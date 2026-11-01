# Supervisor countersign playbook — definition reconciliation & board discipline (05-10 session, five tenants)

Dense rules distilled from ~30 countersign/vonis cycles across a sibling book / PROMANUAL / EXPOWORLD / the Unity book / DATMANUAL / GAYA-AHLI boards. Each rule cites its evidence case so future supervisors can recognize the pattern, not just obey it.

## 1. Definition reconciliation: N numbers = N detectors
When reports disagree on a count of the same property, do NOT pick a winner. Enumerate every definition, reproduce each with your own parser, and require the released verdict to close arithmetically with a printed mapping formula.
- Slug count on one sheet: gate-wide detector 22 / STD canonical paired-word detector 20 / supervisor's loose probe 28 (it counted 8 single lowercase tokens). Tightened regex `>=2 segments` reproduced 20 exactly. All three were "right" in their own definition.
- Dead-URL count: run-1 said MATI=34, supervisor counter said 33; gap = 2 template fragments (`arxiv.org/abs/<id`, `hf.co/<org`) classified N/A-PLACEHOLDER in run-1 vs MATI in rev-2. Resolution demanded a closed crosstab: BENAR 709 + MATI 34 + N/A-ENDPOINT 9 = 752 exactly, status-by-class readable. Verifier printed it; supervisor cross-checked against own Counter of the accounts jsonl (404=28 decomposed 4+1+23, 401=10=7+3...).
- URL uniques 412 vs 413: brace-pattern URLs normalized-to-base by verifier, kept whole by supervisor.
Gate wording for workers/verifiers: any predicate count must ship with the formula mapping raw statuses to predicates, and the sum must equal the population.

## 2. Fleet scanner: `--channel` is mandatory
`scan_ai_footprint.py` defaults to a different channel when `--channel` is omitted; a plain call produced false FAIL C-7 on a review file that PASSED under `--channel kitab`. Always pass the target channel (chat|deck|doc|etalase|kanban|kitab|notif|sosmed; see `--help`) and record the channel in the verdict trace. (Durable note for `gsp-output-naturalization` — that skill is USER-OWNED, supervisor cannot patch it; raise via proposal.)

## 3. Subject-of-content class: adjudicate, never edit
When the flagged token IS the object being measured, editing = falsifying the record. Route to controller as a per-class allow-list decision with evidence:
- Emoji rows in a tokenization register (KL-R1-141..144, ZWJ family) — the emoji are the measured content.
- Two DIFFERENT git commands sharing stem "Type git config --global user." flagged as C-14 duplication — varying them breaks instruction truth (stem-instruction false-positive).
- 4x identical "Retrieved October 3, 2026" APA access-date lines — citation convention uniformity is format truth (boilerplate-citation false-positive).
- Machine-output headers of UJIJ VARIANSI blocks left verbatim on purpose — varying = fabricating measurement.
Corollary: a detector bug is a fleet ticket, not a content fix — C-8b LIMITATION_WORDS list is Indonesian-only and false-FAILs English limitation sentences; confirmed cross-board (the Unity book CH02 + PROMANUAL SUNTA laporan) before escalating.

## 4. Board print beats notification claim
If a notification says `completed` but `hermes kanban show | grep status:` still prints running: freeze measurements in an INTERIM note (explicitly: "final verdict held until administrative closure"), and when closure lands, open the final verdict with "PENUTUS INTERIM" + verify the previously-missing deliverables (e.g. scanner trail absent in interim, present at closure). Redelivered notifications for cards already carrying your verdict are no-ops (grep -c first). Never re-post a comment without `show | grep -c <unique phrase>` = 0.

## 5. Resume-diff discipline (supervisor side)
Compare ONLY the same file set: `backup ∩ now`. Union comparisons produced a fake regression "155 -> 181 template occurrences" (new-state covered 22 chapters, backup only the 16 touched ones); intersected comparison showed the true 155 -> 151 = exactly the 4 targeted variations. Same shape as the PROMANUAL placeholder-census lesson: report the intersection, not the union.

## 6. Reverse the order when a validator exists (render-as-analyzer)
FIX-FIGUR on the Unity book burned two full 2700s runs probing annotation geometry manually and produced ZERO rerendered PNGs, while the generator already contained `margin_check` raising `GeometryError` before savefig — the validator IS the analysis tool: one render pass to a temp path yields the complete raise-backlog = the coordinate fix-list. Prescribed pattern: render-as-is → collect raises → patch coords per raise → two-run idempotent → manifest honest. Escalation if run-3 dies the same way: chain-form change (generator-only vs render-QC split) is an owner decision, not a worker retry loop.

## 7. Probe the real ID/heading format before any counting regex
Assumed `L0-1` diktum IDs → 0 findings (false negative); real format `L0-D1` → 39 diktum matching the claim exactly. Cheap guard: print a few actual headings/IDs FIRST, then write the counting regex. Same family as the 'FIG-' prefix bug and the `[Bab 1]` space-notation miss.

## 8. Callers may live outside code (Unity scene YAML)
`.Show()` grep in C# stayed 0 after the fix — the caller is a persistent UnityEvent in Main.unity (CreditsButton m_OnClick wired in inspector). Naive code-grep would have failed a real fix. For engine/UI boards, check scene/prefab YAML wiring before asserting "no caller".

## 9. Self-misstatement repair protocol (recap)
Misattributed one verdict summary to another card; drafts truncated to 229 B; wrong board counts at send time. Protocol that worked: corrections go in a SEPARATE comment (never edit history), measure length + board state before sending, and keep the correction visible in the trace.
