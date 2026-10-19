---
name: gsp-dry-run-verify-fix
description: >-
  Validate changes before final delivery by simulating realistic execution
  paths, inspecting errors, applying targeted fixes, and repeating in a
  bounded loop. Prevents "hallucinated success" where the agent believes
  work is complete despite latent failures.
license: MIT
metadata:
  hermes:
    tags: [gsp, verification]
    category: verification
  category: development
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/dry-run-verify-fix
    license_path: LICENSE
---

# Dry Run → Verify → Fix

Before declaring work complete, run a realistic simulation of the delivery
path. Inspect any failures, fix them, and repeat. Cap iterations to prevent
runaway loops.

---

## Triggers

Use this skill when:
- "dry-run before final delivery"
- "pre-ship validation with simulation"
- "verify and fix in a bounded loop"
- "simulate the execution path and fix errors"
- "validate changes before finishing"
- "bounded repair iteration before ship"

Do NOT use for analysis-only tasks (reading, researching, planning without
execution) or when immediate delivery is requested with no validation step.

---

## Process

### Phase 1: Define the Delivery Path

Identify what needs to happen for the work to be "shipped":

```markdown
## Delivery Path

**What was produced:** <files, config, or artifacts>
**How to validate:** <the steps to verify correctness>
**Expected results:** <what success looks like>
```

Examples of validation steps:
- Running a script and checking its output
- Syntax-checking generated files
- Simulating tool calls with expected inputs
- Running dry-mode builds or lints
- Querying a test endpoint

---

### Phase 2: Dry-Run Execution

Execute the validation path without side effects (or with sandboxed side
effects). For each step:

```markdown
### Step: <name>
**Command/Action:** <what was run>
**Expected:** <what should happen>
**Actual:** <what happened>
**Result:** PASS / FAIL
```

**If ALL steps pass:** → Phase 5 (deliver)

**If ANY step fails:** → Phase 3 (diagnose), then Phase 4 (fix)

---

### Phase 3: Diagnose Failure

For each failure:

1. **Reproduce:** Is the failure consistent or flaky?
2. **Root cause:** What is the actual source of the failure?
3. **Scope:** Is this a local fix or does it affect other parts?
4. **Severity:** BLOCKER (must fix) / WARNING (should fix) / INFO (note)

```markdown
### Failure: <step name>

**Symptom:** <what failed, including error messages>
**Root Cause:** <why it failed>
**Scope:** <local / cross-cutting>
**Severity:** BLOCKER / WARNING / INFO

**Fix:** <specific change needed>
```

---

### Phase 4: Apply Fix

1. Apply the fix from Phase 3 diagnosis
2. Return to Phase 2 (re-run the dry-run from scratch)
3. Increment repair counter

**Repair limits:**
- Maximum 3 repair cycles per session
- After 3 failures → escalate with summary and options
- If the fix introduces new failures → revert and try a different approach

---

### Phase 5: Deliver

When all steps pass or repair limit reached:

```markdown
## Validation Summary

**What was validated:** <delivery path>
**Dry-run cycles:** N
**Repairs applied:** N
**Final status:** ALL PASS / PARTIAL (N failures deferred)

**Deferred items (if any):**
- <failure>: deferred because <reason>

**Verification evidence:**
- Step 1: PASS — <artifact/log>
- Step 2: PASS — <artifact/log>
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Dry-running with mocked data that hides real failures | Use realistic inputs that exercise real code paths |
| Fixing without re-running the full path | Always re-run the full dry-run from scratch |
| Ignoring WARINING severity | Document and defer with reason |
| More than 3 repair cycles | Escalate after limit |
| Skipping dry-run on "trivial" changes | Even small changes may break things |

---

## Execution Checklist

```
[ ] Phase 1: Delivery path defined
[ ] Phase 2: Dry-run executed (realistic simulation)
[ ] Phase 3: Failures diagnosed with root cause
[ ] Phase 4: Fix applied and retry initiated
[ ] Phase 4: Repair counter ≤ 3
[ ] Phase 5: Validation summary delivered
[ ] Verify: All failures documented with root cause
[ ] Verify: BLOCKER items resolved before delivery
```

---

## Verification

After validation:
1. All BLOCKER-severity failures are fixed
2. Repair cycles ≤ 3
3. Each repair cycle re-ran the full dry-run path
4. Delivery summary documents all results
