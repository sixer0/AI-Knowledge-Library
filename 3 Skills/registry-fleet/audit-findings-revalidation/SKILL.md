---
name: audit-findings-revalidation
description: Use when rechecking an old audit against the live system.
metadata:
  hermes:
    tags: [gsp, audit, verification, orchestration]
    category: gsp
---

# Audit Findings Revalidation

**Class of task:** user hands over a past audit / QA standard / findings report (often a big HTML or PDF) and asks: "are these findings still relevant to our ecosystem now? make a work list."

## Core doctrine

1. **The audit's numbers are NOT facts about today.** An audit typically ran against a *snapshot on another host at another time*. Never carry its counts forward as current — re-measure every headline number on the live tree, and say which source each number came from.
2. **Findings age into three classes** — every finding gets exactly one verdict backed by fresh evidence:
   - **RESOLVED** — the condition no longer exists (or the dangerous tool itself was removed, which counts as resolved-but-record-why).
   - **STILL RELEVANT** — re-measured, condition present, with the *new* count (it will differ from the audit's).
   - **NEW** — re-measurement surfaces a live failure the audit never saw (common: cron jobs that died *after* the audit snapshot).
   Also flag **NOT RE-MEASURABLE HERE** honestly when the audit's tooling (e.g. `hqa.py`) didn't migrate to this host — do not extrapolate the old number onto the new tree.
3. **Disk evidence beats self-report** (the audit's own criterion, C-CONN-CRON-EVIDENCE): compare `cron/jobs.json` `last_status`/`failure_streak` against actual files in `cron/output/<job_id>/`. A job saying "ok" while its latest output says failed is itself a finding.
4. **Preserve the audit's ordering constraints.** If the report defines waves/gates (e.g. "nothing may run before drift direction is settled"), keep them in the work list even when individual items resolved — the gate usually protects the still-open items.
5. **Keep the "forbidden actions" table.** Audits that list explicitly-dangerous remediations (mass sed passes, blanket truncation, redeploy before W0) should have those restated in the final list — they get re-proposed by every fresh agent.

## Steps

1. **Extract the findings sections** from the document. For large HTML (multi-MB, `read_file` truncates), use `execute_code` with regex section-slicing by heading `id="..."` + tag-strip → text. Pull: summary table, operational warnings, unfinished-migration section, remediation plan (§ waves), forbidden-actions table. See `references/recheck-recipes.md` for the working extractor and probes.
2. **Snapshot current shape first**: profile count, skill-tree counts (fleet shared vs per-profile), repo-vs-live counterpart counts. The audit's unit-of-presentation may no longer match (e.g. 46 units then, 51 now) — state both.
3. **Re-measure each finding class** with the deterministic probes in `references/recheck-recipes.md` (drift by SHA-256 tree match, description-length >60/>1024, cross-skill citation tapak, cron evidence, leftover-migration path grep, duplicate asset size).
4. **Git sanity probe on the corpus repo**: `os.path.isdir(repo/.git)` — an audit recommending "seal into version control" is *more* urgent if the repo still has no `.git` at all.
5. **Write the report** to the shared workspace `docs/<date>_relevansi-audit-<ID>.md`: context line (what host/snapshot the original audit ran on), verdict table (finding → status → fresh evidence with date), then a numbered work list ordered by the audit's own wave constraints, adapted to what's actually left. Final chat reply = verdict summary + work list + pointer to the file; offer to start with the actively-broken item first.

## Pitfalls found in practice

- **`drift_skip:silent` (Hermes cron):** an *unpinned* cron job silently refuses to run when global inference config changed since creation (provider/model drift) — `RuntimeError: [drift_skip:silent] ... job is unpinned`. Symptom: `failure_streak` climbing, output md contains the RuntimeError. Fix: `hermes cron edit <id> --provider <p> --model <m>` (pin either the new or original values). Check ALL recurring jobs for pin state when one hits this, not just the reported one.
- **Audit tooling doesn't auto-migrate.** The kit referenced in the report (e.g. `hqa.py`) may be absent on the current host. Either port it or substitute hand-written probes; label which numbers are hand-measured vs kit-measured (different denominators, per the audit's own rule about publishing invocations).
- **"Tool removed" ≠ "risk resolved."** If the destructive deployer the audit warned about no longer exists here, the underlying *direction* finding (repo is not source of truth; production is) usually still stands — verify counterpart coverage counts before downgrading.
- **Description-length parsing:** frontmatter `description: >-` folded blocks must be joined across continuation lines before measuring; naive single-line grep undercounts badly. (This skill's own creation was rejected at >60 chars — the runtime enforces what the audit measured.)
- **Cross-skill citation counts:** grep pattern `skills/<name>/<file.ext>` catches doc examples too — report the raw tapak count and mark it "needs triage", don't claim it all broken.
- **Long `os.walk` scans:** a full recursive search of `C:\Users\<u>` timed out (~85s) for one probe; scope walks to known repos/hermes-home, and avoid full-drive `dir /s /b` searches.

## Verification before delivering

Each table row must cite a probe actually run this session (file path, count, timestamp). No row may carry the original audit's number as "current" without a fresh measurement next to it. The work list's first item should be whatever is *actively broken now* (e.g. a cron job failing daily), not the audit's highest-severity historical item if that one already resolved.
