---
name: gsp-eval-driven-improver
description: >-
  Create evaluation prompts and assertions to benchmark skill or workflow
  quality. Run evals with and without the skill under test, grade outputs
  against criteria, and iterate on skill design based on measured gaps.
  Enables data-driven, repeatable skill improvement.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: development
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/eval-driven-improver
    license_path: LICENSE
---

# Eval-Driven Improver

Create, run, and iterate on evaluations to improve skill quality. Establish
baselines, measure improvements, and validate that changes actually help
rather than just feel better.

---

## Triggers

Use this skill when:
- "benchmark this skill's performance"
- "create evals for this workflow"
- "measure skill quality with test cases"
- "improve based on evaluation results"
- "eval loop for iterative refinement"
- "compare with and without the skill"

Do NOT use for one-off tasks where no repeatable measurement is needed,
or when you are running a single test without iteration.

---

## Process

### Phase 0: Define Evaluation Scope

Before creating evals, clarify:

```markdown
## Eval Spec

**Target under test:** <skill name or workflow description>
**Purpose:** <what quality dimension are we measuring?>
**Baseline condition:** <without skill / old version / current behavior>
**Target condition:** <with skill / new version / desired behavior>

**Success threshold:** <what score or criteria means "improvement">
```

Typical quality dimensions:
- **Correctness:** Does the output meet requirements?
- **Completeness:** Are all subtasks addressed?
- **Consistency:** Is output stable across similar inputs?
- **Efficiency:** Is token/time usage optimized?
- **Robustness:** Does it handle edge cases and errors?

---

### Phase 1: Create Eval Prompts

Design 3-10 evaluation prompts that exercise the skill's target capability:

```yaml
evals:
  - id: eval-1
    name: <short name>
    prompt: <the exact prompt to send>
    expected_behavior: <what success looks like>
    priority: critical / high / medium / low
    category: <correctness / completeness / consistency / efficiency / robustness>
```

**Rules for good eval prompts:**
1. Each eval should test ONE specific capability
2. Prefer realistic, domain-specific prompts over generic ones
3. Include edge cases (empty input, unusual constraints, error scenarios)
4. Make prompts reproducible (same input = same expected behavior)
5. Cover happy path, failure path, and boundary conditions

**Recommended distribution:**
- 40% happy path (normal operation)
- 30% edge cases (boundaries, unusual inputs)
- 30% failure scenarios (missing data, errors, conflicts)

---

### Phase 2: Define Grading Criteria

For each eval, define how outputs are graded:

```markdown
### Eval: <id> — <name>

**Prompt:** <the prompt>

**Criteria:**
| # | Criterion | Weight | Pass Condition |
|
---|
---
---
-----|
---
-----|
---
---
---
---
----|
| 1 | <criterion> | mandatory / bonus | <specific, measurable condition> |
| 2 | <criterion> | mandatory / bonus | <specific, measurable condition> |

**Pass threshold:** <e.g., "all mandatory criteria pass">

**Expected output characteristics:**
- <characteristic 1>
- <characteristic 2>
```

**Grading scale per criterion:**
- **PASS (2):** Fully meets the criterion
- **PARTIAL (1):** Partially meets it (document what's missing)
- **FAIL (0):** Does not meet the criterion

---

### Phase 3: Run Baseline (Without Skill)

Run all eval prompts without the skill enabled. Grade each output:

```markdown
## Baseline Results

| Eval | C1 | C2 | C3 | Total | Pass? |
|
---
---|
----|
----|
----|
---
----|
---
----|
| eval-1 | 2 | 1 | 0 | 3/6 | FAIL |
| eval-2 | 2 | 2 | 2 | 6/6 | PASS |
| ... |   |   |   |       |       |

**Overall baseline:** <score summary>
**Key gaps:**
- <gap 1>
- <gap 2>
```

---

### Phase 4: Run Target (With Skill)

Apply the skill and run the same eval prompts. Use the same grading criteria:

```markdown
## Target Results

| Eval | C1 | C2 | C3 | Total | Pass? |
|
---
---|
----|
----|
----|
---
----|
---
----|
| eval-1 | 2 | 2 | 1 | 5/6 | PASS |
| eval-2 | 2 | 2 | 2 | 6/6 | PASS |
| ... |   |   |   |       |       |

**Overall target:** <score summary>
**Improvement vs baseline:** <+/- score>
```

---

### Phase 5: Analyze & Iterate

Compare baseline vs target. Identify specific gaps that remain:

```markdown
## Gap Analysis

| Gap | Baseline | Target | Improved? | Root Cause | Fix |
|
-----|
---
---
----|
---
-----|
---
---
-----|
---
---
---
---|
-----|
| <gap> | FAIL | PARTIAL | Yes | <why> | <skill change> |
| <gap> | FAIL | FAIL | No | <why> | <skill change> |
| <gap> | PASS | FAIL | Regression! | <why> | <revert or adjust> |
```

**Iteration loop:**
1. Identify the top 1-2 gaps that matter most
2. Propose a specific change to the skill (trigger, description, process, guidance)
3. Re-run Phase 4 (target test) to measure improvement
4. Check for regressions in previously-passing evals
5. Repeat up to 3 iterations

**Stop conditions:**
- All evals pass at the defined threshold
- 3 iterations completed without further improvement
- User accepts the current results

---

### Phase 6: Report

```markdown
## Eval Summary

**Target:** <skill name>
**Evals:** N (N happy path, N edge case, N failure)
**Iterations:** N
**Baseline score:** <score>
**Final score:** <score>
**Improvement:** <+/-> <percentage>

**Status:** PASS / PARTIAL / FAIL

**Recommendation:**
- <if PASS: ship the skill>
- <if PARTIAL: specific remaining gaps>
- <if FAIL: fundamental redesign needed>

**Regression check:** Previously-passing evals still pass? Yes / No
```

---

## Anti-Patterns

| Avoid | Instead |
|
---
----|
---
---
---|
| Writing evals that match the skill's own language | Write evals from the user's perspective |
| Grading subjectively without evidence | Require specific evidence for each score |
| Only testing happy path | Include edge cases and failure scenarios |
| Over-iterating past diminishing returns | Cap at 3 iterations or when no improvement |
| Ignoring regressions | Always re-run all evals after each change |
| Evals that are too easy (ceiling effect) | Include challenging cases that differentiate versions |

---

## Execution Checklist

```
[ ] Phase 0: Evaluation scope defined
[ ] Phase 1: 3-10 eval prompts created (happy/edge/failure)
[ ] Phase 2: Grading criteria established for each eval
[ ] Phase 3: Baseline run completed and scored
[ ] Phase 4: Target run completed and scored
[ ] Phase 5: Gap analysis performed (top 1-2 gaps identified)
[ ] Phase 5: Up to 3 iteration cycles completed
[ ] Phase 6: Final report with recommendation
[ ] Verify: Each eval has reproducible prompts
[ ] Verify: Scoring is consistent across baseline and target
[ ] Verify: Regressions are detected and reported
```

---

## Verification

After eval improvement:
1. All eval prompts are reproducible (same input → same expected behavior)
2. Baseline and target use identical grading criteria
3. Gap analysis identifies root causes, not just symptoms
4. Each iteration shows measurable improvement or is capped
5. Regression check is clearly reported
6. Final recommendation is actionable (ship / fix / redesign)
