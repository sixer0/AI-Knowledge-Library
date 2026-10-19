---
name: gsp-human-in-loop-gate
description: >-
  Pause execution and request user input when ambiguity, safety concerns,
  high-impact decisions, or destructive operations are detected. The gate
  presents the situation, available options, and recommended action, then
  waits for user approval before proceeding. Prevents automated decisions
  that should involve human judgment.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: safety
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/human-in-loop-gate
    license_path: LICENSE
---

# Human-in-the-Loop Gate

Pause execution at decision boundaries where human judgment is required.
Present the context, options, and recommendation, then wait for explicit
user approval before proceeding.

---

## Triggers

Use this skill when:
- "pause for user approval"
- "human-in-the-loop"
- "require user confirmation"
- "ask before proceeding"
- "high-impact decision gate"
- "safety check needed"
- "confirm this action before execution"
- "interrupt for user decision"

Do NOT use for routine decisions that clearly fall within the agent's
authority, or when the user has explicitly granted blanket approval for
a category of actions.

---

## Process

### Phase 0: Gate Classification

When a decision point is reached, classify the gate type immediately:

| Gate Class | Signal | Example | Action |
|------------|--------|---------|--------|
| **AMBIGUITY** | Unclear intent, multiple valid interpretations | "Do you want to refactor the entire module or just one function?" | Present options with trade-offs |
| **SAFETY** | Destructive operation, data loss, irreversible change | "Delete 50 files matching pattern" | Require explicit approval |
| **HIGH-IMPACT** | Significant cost, time, scope, or external effect | "Deploy to production" or "Spend $500 on API credits" | Require explicit approval with impact summary |
| **PERMISSION** | External action, credential use, data sharing | "Email this report to client@example.com" | Require confirmation of recipients and content |
| **AUTHORITY** | Decision outside stated scope or policy | "Override the security policy configured in project settings" | Escalate — require explicit override |
| **CONFIRMATION** | User asked a question back to the agent | (Any user query that expects a decision) | Gate is automatically satisfied when user responds |

---

### Phase 1: Build Gate Presentation

For each gate, construct a structured presentation:

```markdown
## ⏸ Gate: <class>

**Operation:** <what is about to happen>

**Context:**
- <relevant facts, inputs, state>
- <why this gate was triggered>

**Risk assessment:**
- **Impact:** <high / medium / low — what's at stake>
- **Reversibility:** <reversible / partially reversible / irreversible>
- **Cost:** <monetary, time, or resource estimate if applicable>

**Options:**
1. **Proceed** — <what happens, any conditions>
2. **Modify** — <suggested adjustment, if appropriate>
3. **Abort** — <stop and return to previous state>
4. <any additional options>

**Recommendation:** <option #, with rationale>

**Awaiting your decision...**
```

**Gate presentation rules:**
1. State the operation in plain language — no jargon
2. Quantify impact when possible ("will delete 12 files", "will cost ~$0.50")
3. Always include the "recommendation" — the agent should have an opinion
4. Include an "abort" option that restores prior state or stops cleanly
5. Never present a false choice (e.g., "proceed or abort" when both do the same thing)

---

### Phase 2: Present Gate to User

Output the gate presentation and pause:

```markdown
**Gate active:** Waiting for user input before proceeding.

The task is paused at this decision point. Once you respond, execution
will continue based on your choice.
```

**Pause behavior:**
- Do NOT take further actions until user responds
- Do NOT make assumptions about the user's choice
- If the user's response is ambiguous, clarify before proceeding
- If the user asks a question about the options, answer and re-present the gate

---

### Phase 3: Process User Decision

When the user responds:

```markdown
## Gate Resolved

**User decision:** <proceed / modify / abort / custom>
**User input:** <verbatim response>

**Action taken:**
- <what happens next>

**Gate log:**
| Gate | Class | Decision | Time |
|------|-------|----------|------|
| <operation> | <class> | <decision> | <timestamp> |
```

**Decision handling:**

| User Says | Action |
|-----------|--------|
| "Proceed" / "Yes" / "Go ahead" | Execute the operation as presented |
| "Modify" / "Change X" | Apply the modification, re-present gate if scope changes significantly |
| "Abort" / "No" / "Stop" | Abort the operation, return to prior state |
| "Let me think..." / "What does X mean?" | Answer the question, re-present the gate |
| Ambiguous / unclear | Ask for clarification: "I understood <X>. Is that correct?" |

**After resolution:**
- Log the decision to the gate log
- If proceeding: execute the operation
- If aborting: execute any cleanup / rollback
- If modifying: adjust parameters and either execute directly (low-risk) or re-gate (if modification changes risk profile)

---

### Phase 4: Gate Logging

Maintain a running log of all gates triggered during a session:

```markdown
## Gate Log

| # | Timestamp | Operation | Class | Decision | Duration |
|---|-----------|-----------|-------|----------|----------|
| 1 | 12:00:00 | Delete temp files | SAFETY | Proceed | 5s |
| 2 | 12:05:00 | Email draft to client | PERMISSION | Modify | 30s |
| 3 | 12:10:00 | Refactor auth module | AMBIGUITY | Abort | 15s |
```

**Gate log rules:**
- Record every gate, regardless of outcome
- Include the time between gate presentation and resolution
- If gates are too frequent (> 3 in a session), flag to the user:
  "Gates triggered N times. Would you like to adjust the gate sensitivity?"

---

### Phase 5: Gate Sensitivity Adjustment

If the user expresses frustration with too many (or too few) gates:

```markdown
## Gate Sensitivity Settings

**Current sensitivity:** <normal / high / low>

**Adjustment options:**
1. **High sensitivity** — Gate on AMBIGUITY, SAFETY, HIGH-IMPACT, PERMISSION, AUTHORITY (default)
2. **Normal sensitivity** — Gate on SAFETY, HIGH-IMPACT, AUTHORITY only
3. **Low sensitivity** — Gate on SAFETY and AUTHORITY only
4. **Custom** — Define specific gate classes or operations to always/never gate

**How to change:**
- "Set gate sensitivity to low"
- "Never gate on file deletions under 10 files"
- "Always gate on any deployment operation"
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Gating trivial decisions (analysis paralysis) | Only gate when impact, ambiguity, or risk is substantial |
| Presenting options without a recommendation | Always recommend a specific course of action |
| Making the user read a wall of text | Keep gate presentations concise and scannable |
| Proceeding without waiting for a response | Truly pause — no actions until user input |
| Re-gating the same operation multiple times | If the user said "proceed", proceed without re-gating |
| Gate on every tool call | Gate on decision boundaries, not individual operations |
| Assuming user intent from partial input | Wait for a clear, unambiguous response |

---

## Execution Checklist

```
[ ] Phase 0: Gate classified (AMBIGUITY / SAFETY / HIGH-IMPACT / PERMISSION / AUTHORITY / CONFIRMATION)
[ ] Phase 1: Gate presentation built (operation, context, risk, options, recommendation)
[ ] Phase 2: Gate presented to user, execution paused
[ ] Phase 3: User decision received and processed
[ ] Phase 3: Decision logged in gate log
[ ] Phase 4: Gate log maintained for the session
[ ] Phase 5: Sensitivity adjusted if user feedback indicates
[ ] Verify: No actions were taken before user responded
[ ] Verify: Gate presentation includes all 5 elements (operation, context, risk, options, recommendation)
[ ] Verify: Abort option always present and includes cleanup/rollback
```

---

## Verification

After gate execution:
1. No action was taken before the user responded to the gate
2. Gate presentation included: operation, context, risk assessment, options, and recommendation
3. The user's decision was correctly interpreted and executed
4. Gate log captures: operation, class, decision, and duration
5. Abort path cleanly restores prior state
6. Gate sensitivity is appropriate for the session (not too many, not too few)
