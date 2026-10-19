---
name: gsp-self-healing-loop
description: >-
  Classify execution failures into discrete categories (transient, logic,
  permission, resource, or unexpected) and route each to the appropriate
  recovery strategy: automatic retry, compensation, user interrupt, or
  graceful stop. Prevents cascading failures by containing errors and
  applying structured responses.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/self-healing-loop
    license_path: LICENSE
---

# Self-Healing Loop

> **Cakupan (VERIF-SHORT, kebijakan user 03-09-2026):** pola di skill ini dijalankan di jalur ORKESTRASI oleh controller (kartu fix, reassign, eskalasi; maks 2 retry per tugas). Pekerja TIDAK memakai loop ini internal: short check gagal -> lapor jujur via `blocked`/`partial-handoff`, lalu controller yang memutuskan pemulihan. Lihat `gsp-orchestration-execution` non-negotiable 7.

When an error occurs during execution, classify it and apply the right
recovery strategy. Never silently retry the same operation without
understanding why it failed.

---

## Triggers

Use this skill when:
- "classify and recover from this error"
- "self-heal on execution failure"
- "error recovery strategy needed"
- "retry compensate interrupt or stop"
- "handle tool failure gracefully"
- "recover from transient failure"

Do NOT use for expected errors in normal control flow (e.g., "file not found"
when checking existence is part of the algorithm).

---

## Process

### Phase 0: Error Classification

When an error occurs, classify it immediately:

| Class | Signal | Example | Recovery |
|-------|--------|---------|----------|
| **TRANSIENT** | Timeout, network blip, rate limit | `ETIMEDOUT`, `429 Too Many Requests` | Retry with backoff (max 3) |
| **LOGIC** | Wrong approach, bad assumption | "SQL syntax error", "file not found at expected path" | Fix → retry once |
| **PERMISSION** | Access denied, auth failure | `EACCES`, `401 Unauthorized` | Interrupt — notify user |
| **RESOURCE** | Disk full, OOM, missing dependency | `ENOSPC`, `MODULE_NOT_FOUND` | Interrupt — notify user |
| **UNEXPECTED** | Unrecognized crash | Null pointer, assertion failure | Stop — log full context |

---

### Phase 1: Apply Recovery Strategy

Based on classification:

#### TRANSIENT → Retry with Backoff

```
Attempt 1 → fail → wait 2s
Attempt 2 → fail → wait 4s
Attempt 3 → fail → escalate to user
```

- Maximum 3 retries
- Exponential backoff: 2s, 4s, 8s
- After 3 failures: escalate with "Operation failed after 3 retries: <error>"

#### LOGIC → Diagnose and Fix

1. Understand the root cause (not just the symptom)
2. Apply a targeted fix
3. Retry exactly once
4. If the fix fails: escalate with "Logical approach failed: <diagnosis>"

#### PERMISSION → Interrupt and Notify

1. Stop the current operation
2. Inform the user: "Access denied to <resource>. Needs <permission>."
3. If the user provides credentials/approval, retry once

#### RESOURCE → Interrupt and Notify

1. Stop the current operation
2. Report: "<Resource> unavailable. <detail>"
3. If the user resolves the issue, resume from checkpoint

#### UNEXPECTED → Stop and Log

1. Capture full error context (stack trace, inputs, state)
2. Stop immediately — do not retry
3. Report: "Unexpected error: <summary>. Full context: <path to log>"

---

### Phase 2: Escalation Path

If recovery fails (all retries exhausted, fix didn't work, etc.):

```markdown
## Error Recovery Failed

**Error:** <original error>
**Classification:** <class>
**Recovery Attempted:** <what was tried>
**Failed At:** <step that still fails>

**Options for user:**
1. Provide additional context/credentials to unblock
2. Skip this step and continue (may produce partial results)
3. Abort the operation entirely
```

---

### Phase 3: Compensation (Optional)

For LOGIC errors where the fix changes the approach:
- Document the change: "Initial approach used X but failed because Y. Changed to Z."
- Re-verify any assumptions that may have changed

For other error classes, compensation does not apply (the operation either
succeeds or is interrupted cleanly).

---

## Error Log Template

```markdown
## Error Log

| # | Phase | Error | Class | Recovery | Result |
|---|-------|-------|-------|----------|--------|
| 1 | fetch-data | ETIMEDOUT | TRANSIENT | retry×3 | success |
| 2 | validate-schema | EACCES | PERMISSION | interrupt | user provided key |
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Blind retry without classification | Classify first, then choose strategy |
| Same retry count for all error types | TRANSIENT=3, LOGIC=1, OTHERS=0 |
| Ignoring retry-exhausted | Always escalate after max retries |
| Continuing after UNEXPECTED | Stop and report |
| Swallowing errors silently | Always log the error and recovery outcome |

---

## Execution Checklist

```
[ ] Phase 0: Error classified (TRANSIENT|LOGIC|PERMISSION|RESOURCE|UNEXPECTED)
[ ] Phase 1: Recovery strategy applied
[ ] Phase 1: Retry count ≤ max (3 for TRANSIENT, 1 for LOGIC)
[ ] Phase 2: Escalation to user if recovery failed
[ ] Phase 3: Compensation documented if applicable
[ ] Verify: All errors are logged with classification
[ ] Verify: No silent retries
```

---

## Verification

After healing:
1. Every error was classified before recovery
2. Retry limits were respected per class
3. UNEXPECTED errors stopped execution
4. User was informed of any escalated failures
