---
name: gsp-phase-accountability
description: The GSP phase-accountability contract — 10-phase task lifecycle, docs/ artifact conventions, scale categories, gates, and bounded feedback loops. Load when orchestrating a multi-phase task (delegasi multi-agen) or when a task must produce an auditable docs/ trail.
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
---

# Phase Accountability Contract (GSP Hermes)

Source of truth adapted from `/Users/mbp/.config/kilo/AGENTS.md` ("Documentation Accountability Contract") and `/Users/mbp/.config/kilo/documentation/orchestration-flow.md`. The main session is the controller: it opens/closes gates, delegates via the Agent tool, and is the first and last user-facing actor.

## Controller Boundaries & RT-FIRST

- Controller **only orchestrates** — it never executes implementation, analysis, or verification itself, and it does NOT translate the request nor write the blueprint. All work is delegated via `delegate_task(...)` to specialist profiles.
- **RT-FIRST (mandatory)**: the FIRST delegation for every request must go to `request-translator` — no exceptions, even for trivial-looking tasks. Bypassing it marks the task as failed with status `RT_BYPASS`. RT classifies the request as TRANSLATED / TRIVIAL / CLARIFICATION_NEEDED and produces `identification/01_translated.md`.
- After RT, delegate to `task-architect` for the structured blueprint (`identification/02_structured.md`).
- **Writer is the weakest verifier** (penulis adalah verifikator terlemah): whoever wrote an artifact must never be its sole verifier. Verification is always delegated to independent specialists (verifier, security-review, test-expert, senior-code-reviewer). Per tugas, pekerja hanya menjalankan SHORT check dengan healing maks 1 loop (VERIF-SHORT-B user 03-09: artefak ada, non-kosong, path benar, 1 smoke command; gagal kedua -> lapor jujur). Full verification ada di kartu fase verifikasi yang dipegang agen verifier khusus dengan MANDAT VERIFIKASI; healing lanjutan dilakukan orkestrator lewat kartu fix, bukan retry internal. Once a step is delegated, the controller's job is to orchestrate and verify that everything runs per the orchestration plan — checking artifacts, gates, statuses — not to redo the work itself.

## Scale Categories (classify first)

| Category | Description | Research Depth |
|----------|-------------|----------------|
| New Project | Greenfield development | Max: full Source + Spec + Impact |
| Enhancement | Additive feature on existing code | Medium: targeted source + spec |
| Refactor | Structural change, same behavior | Full: deep source + impact |
| Migration | Platform/language/dependency change | Full: all 7 external dimensions |
| Research | Feasibility, exploration, POC | Max: full source + external research |
| Debug | Bug reproduction and fix | Targeted: minimal source + spec |
| Administration | Config, docs, tooling | Minimal or none |

The category decides which phases are mandatory. Debug/Administration may collapse to: implement → verify → report. New Project/Migration use the full pipeline with a blueprint approval gate (Blueprints Approval Gate).

## Ten Phases and Artifacts

Task archive root: `docs/[YYYY_MM_DD]_[task_slug]/`. All filenames snake_case, zero-padded numbering, additive only (never delete/rename existing artifacts), never write to `output/`.

| Phase | Folder | Required Artifacts (example) | Producer |
|-------|--------|------------------------------|----------|
| 1. identification | `identification/` | `01_translated.md`, `02_structured.md` | `request-translator`, `task-architect` |
| 2. research | `research/` | `01_explore.md`, `02_collection.md`, `03_analysis.md` | Explore, `data-collector`, `data-analyst` |
| 3. masterplan | `masterplan/` | `01_specs.md`, `02_plan.md` | `data-analyst`, `pm-planner` |
| 4. initialization | `initialization/` | `01_env_check.md` (read-only env check) | controller/executor |
| 5. implementation | `implementation/` | numbered change/test artifacts + `99_implementation_report.md` | `coder-execution`, specialists |
| 6. gateway_check | `gateway_check/` | `01_gate_report.md` | controller |
| 7. test | `test/` | `01_test_report.md` | `test-expert` |
| 8. verification | `verification/` | `01_verification.md`, `02_security.md` (PASS/CAUTION/FAIL) | `verifier`, `security-review` |
| 9. report | `report/` | `report.md` (Highlight → Detail synthesis) | controller |
| 10. decisions | `decisions/` | `decisions.md` (updated as decisions happen) | controller |

Task-level files: `README.md` (task index) and `status_tasks.md` (live tracker) — written by the controller only.

## Structured Blueprint (identification/02_structured.md)

Produced by the `task-architect` agent as a Markdown table with exactly 7 columns: **Step, Task Description, Agent_to_Invoke, Expected Output, Depends On, Verification, Phase** — plus a mandatory `## Recommendation & Next-Plan Summary` section. Validate mechanically before presenting for approval (V1–V7): table exists; 7 columns; rows populated; steps atomic (one independent item per step); agent names valid; phase names valid; dependencies exist and are acyclic. Re-delegate with the specific failure on FAIL; after 3 failures on the same criterion, escalate to the user.

## Gates

- **Blueprint approval (HIL)** — for large categories, present the blueprint via Blueprints Approval Gate and wait for approval before research/implementation.
- **Post-research refinement severity** — if research changes the approved blueprint: MAJOR (new scope, different agents, >30% effort change, intent change) → re-approve with the user; MINOR (same scope, more detail) → proceed and record in `decisions/decisions.md`.
- **Phase gates** — a phase is complete only when its required artifacts exist, are non-empty, snake_case, and under `docs/`. The controller verifies each subagent's claimed files exist before proceeding.
- **Security gate** — `verification/02_security.md` FAIL or CAUTION → `clarify`: fix now / proceed with recorded risk / modify scope. After fixes, re-run the affected verifiers.
- **Final gate (before report)** — verify: no files deleted/renamed, nothing in `output/`, no emojis added to artifacts, required phase folders present.

## Bounded Loops

Feedback, iteration, checkpoint, rework, escalation — all bounded: max 3 cycles per criterion, then escalate to the user. Never loop unbounded.

## Delegation Contract

Every delegation prompt includes: task, target files/scope, the step's `Skills_to_Load` from the blueprint (the executor loads exactly those skills — the user is never asked which procedure to use), expected output format with explicit status (`complete` / `blocked` / `needs-review`), references to prior-phase artifacts to read, and which `docs/` artifact to produce. Parallel subagents must not write to the same file — assign each its own artifact; the controller synthesizes shared files (`status_tasks.md`, reports) afterward. Concurrency guidance: ≤5 parallel per mission wave, no per-agent-type limit (norma user 03-09B; host cap 20); overflow goes to the next wave.

## Research: 7 External Dimensions

When a task needs external research (Migration, Research, vendor decisions), scope the delegation across: 1 Technology Trends, 2 Technology Evaluation, 3 Vendor Evaluation, 4 Market Share & Positioning, 5 Regulatory & Compliance, 6 Competitive Landscape, 7 Industry Trends. Assign only the relevant dimensions.

## Completion

Status chain: FINAL_VERIFICATION → MEMORY_PERSISTENCE → COMPLETE. After the final report, persist durable lessons to memory (persistent memory Hermes; di shared workspace juga `memory/YYYY-MM-DD.md` konvensi log harian per AGENTS.md GSP). No completion claims without fresh verification evidence. Claim level mengikuti KLAIM-TRIAGE (user 03-09): kartu done = L1 (worker-done), klaim "selesai" ke user minimal L2 (verifier PASS + controller mengukur artefak sendiri), tutup misi ber-gate = L3 (user-accepted). Umpan balik review user di-triase dulu (T1..T6) sebelum ada pengakuan; permintaan maaf refleks tanpa triase dilarang.
