---
name: gsp-reflection-loop
description: >-
  Self-critique and iterative refinement with explicit evidence-based review.
  After generating output, critique it against success criteria, identify
  specific gaps, revise, and repeat. Bounded iteration prevents infinite loops
  while maximizing output quality.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: development
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/reflection-loop
    license_path: LICENSE
---

# Reflection Loop

Generate → critique → revise in a bounded loop. Each critique must cite
specific evidence from the output, and each revision must address every
identified gap.

---

## Triggers

Use this skill when:
- "critique and revise this output"
- "evidence-based self-review"
- "reflect on the result and improve"
- "iterative refinement with quality gates"
- "review against explicit criteria and fix gaps"
- "self-critique loop with bounded iterations"

Do NOT use for trivial outputs where a single pass is sufficient, or when
the user explicitly says "no review needed."

---

## Process

### Phase 1: Establish Success Criteria

Before reflecting, define what "good" looks like. If the user provided
criteria, use those. Otherwise, infer from context:

- **Correctness**: Does it do what was asked?
- **Completeness**: Are all requirements addressed?
- **Clarity**: Is the output understandable?
- **Conciseness**: Is it appropriately scoped?
- **Consistency**: Are there internal contradictions?

Output: Explicit list of 3-5 criteria with brief definitions.

---

### Phase 2: Generate Initial Output

Produce the best output you can in one pass, given the criteria above.
Do not hold back — this is the baseline.

---

### Phase 3: Evidence-Based Critique

For each criterion, evaluate the output:

```markdown
### Criterion: <name>

**Assessment:** PASS / FAIL / PARTIAL

**Evidence (exact quote or specific reference):**
> "<quoted passage from the output>"

**Gap:**
<specific, actionable description of what is missing or wrong>

**Severity:** HIGH / MEDIUM / LOW
```

**Rules for critique:**
1. Every assessment MUST cite exact quotes or line numbers
2. "Looks good" without evidence is NOT a valid critique
3. HIGH severity gaps must be fixed; MEDIUM should be fixed; LOW may be deferred
4. If all criteria are PASS with no HIGH severity, skip to Phase 5

---

### Phase 4: Revise

Produce a new version that addresses every gap identified in Phase 3:

1. For each FAIL or PARTIAL criterion, apply the specific fix
2. For HIGH severity gaps: must fix
3. For MEDIUM severity gaps: should fix (document if skipped)
4. For LOW severity gaps: may fix or defer with explanation

After revision, if iteration count < max:
- Go back to Phase 3 (re-critique the revised output)
- If iteration count >= max: proceed to Phase 5

**Default max iterations:** 3 (configurable: user may say "iterate 5 times")

---

### Phase 5: Final Delivery

When all criteria pass or max iterations reached:

```markdown
## Reflection Summary

**Criteria:** N criteria defined
**Iterations:** N
**Final Status:**
- Criterion 1: PASS
- Criterion 2: PASS
- Criterion 3: PARTIAL → deferred (reason)

**Unresolved Gaps:**
- <gap> (deferred, severity LOW)
```

---

## Example

**User:** "Write a Python function to merge two sorted lists."

**Phase 2 output:** Simple `sorted(a + b)` approach.

**Phase 3 critique:**
```
Criterion: Correctness — FAIL
Evidence: "sorted(a + b)" has O(n log n) not O(n)
Gap: Should use two-pointer merge for O(n)
Severity: HIGH
```

**Phase 4 revision:** Two-pointer merge implementation.

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Vague critique ("could be better") | Cite exact text, describe the gap |
| Ignoring LOW severity gaps | Defer with explanation |
| Changing what works | Only change what was flagged |
| Infinite iterations | Hard cap at configured max |
| Siloing | Consider interaction between criteria |

---

## Execution Checklist

```
[ ] Phase 1: Success criteria defined (3-5 items)
[ ] Phase 2: Initial output generated
[ ] Phase 3: Evidence-based critique for each criterion
[ ] Phase 4: Revision addresses all gaps
[ ] Phase 4: Iteration count tracked (max N)
[ ] Phase 5: Final summary delivered
[ ] Verify: Each critique cites specific evidence
[ ] Verify: Each HIGH severity gap is addressed
[ ] Verify: Iteration count did not exceed max
```

---

## Verification

After reflection:
1. Every criterion was evaluated with specific evidence
2. All HIGH severity gaps are fixed
3. Iteration count ≤ max (default 3)
4. Final summary documents deferred items
