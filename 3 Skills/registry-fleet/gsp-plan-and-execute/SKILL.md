---
name: gsp-plan-and-execute
description: >-
  Decompose complex tasks into staged, dependency-aware execution plans with
  explicit checkpoints. After each phase, evaluate progress, update the plan,
  and proceed to the next stage. Prevents "lost in the middle" failures by
  maintaining a visible, revisable roadmap.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/plan-and-execute
    license_path: LICENSE
---

# Plan and Execute

Break complex requests into a staged plan with explicit checkpoints, dependency
ordering, and completion criteria. After each major phase, replan based on
what was learned.

---

## Triggers

Use this skill when:
- "create staged plan with checkpoints"
- "decompose and execute step by step"
- "multi-phase execution plan"
- "plan with milestones and dependencies"
- "step-by-step with replan after each phase"
- "task decomposition with verification gates"

Do NOT use for simple single-step tasks or when the user only needs a
straightforward answer.

---

## Process

### Phase 0: Scope & Goal Clarification

Before drafting the plan, confirm:
- What is the **final deliverable**?
- What are the **constraints** (time, tools, quality bar)?
- What can be **assumed** vs what needs **validation**?
- What is the **acceptance criteria** for completion?

Output: One-paragraph restatement of goal with constraints.

---

### Phase 1: Decompose into Phases

Break the work into 3-7 sequential phases. For each phase, document:

```yaml
phase: <ordinal>
name: <short name>
goal: <what this phase achieves>
depends_on: <phase numbers this depends on, or "none">
checkpoint_criteria:
  - <measurable condition 1>
  - <measurable condition 2>
output: <artifact or state produced>
```

**Rules:**
- Each phase must produce a **verifiable artifact** or **measurable state change**
- Dependencies must form a DAG (no circular deps)
- Keep phases granular enough that a single phase is 1-3 execution blocks

---

### Phase 2: Execute Phases Sequentially

For each phase in dependency order:

1. Announce which phase is starting
2. Execute the work
3. Run checkpoint verification
4. If checkpoint passes → stage the output, log progress
5. If checkpoint fails → enter Phase 3 (replan)

```markdown
**Phase N: <name>** [IN PROGRESS]
Goal: <goal>
Checkpoint: <criteria>
Decision: PASS / FAIL → [continue / replan]
```

---

### Phase 3: Replan on Checkpoint Failure

When a checkpoint fails:

1. **Diagnose**: What went wrong? Unexpected input? Missing information? Wrong approach?
2. **Adjust**: Modify remaining phases or the current phase's approach
3. **Re-verify**: If the fix is local, retry the phase. If the fix changes scope, update future phases.
4. **Escalate**: If replanning fails twice, surface to the user with options.

Replanning resets the retry counter. Maximum 2 replans per phase before escalation.

---

### Phase 4: Deliver

When all phases complete successfully:
1. Summarize what was done (one paragraph)
2. List all artifacts/outputs
3. Note any unfinished items or known limitations
4. Present the deliverable

---

## Output Template

```markdown
## Execution Summary

**Goal:** <restated goal>
**Phases Completed:** N of N
**Decision Log:**
- Phase 1: PASS — <artifact>
- Phase 2: PASS — <artifact>
- Phase 3: REPLAN (1) → PASS — <artifact>

**Artifacts:**
- <path/file>: <description>

**Limitations:**
- <any known trade-offs or incomplete items>
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Planning every detail upfront | Discover details during execution |
| Phases without checkpoints | Every phase must have a pass/fail gate |
| Ignoring dependency order | Execute phases in strict dependency sequence |
| Replanning without diagnosing root cause | Diagnose first, then replan |
| More than 7 phases for most tasks | Break into coarser phases; use sub-tasks if needed |

---

## Execution Checklist

```
[ ] Phase 0: Goal clarified with user
[ ] Phase 1: Decomposition created (3-7 phases, DAG deps)
[ ] Phase 2: Each phase executed sequentially
[ ] Phase 2: Checkpoint verified after each phase
[ ] Phase 3: Replan applied only when checkpoint fails (max 2)
[ ] Phase 4: Delivery summary produced
[ ] Verify: All checkpoints passed
[ ] Verify: Replan count ≤ 2 per phase
```

---

## Verification

After execution:
1. All phases completed with PASS checkpoints
2. Delivery summary includes all artifacts
3. No circular dependencies in the original decomposition
4. Replan limit was respected
