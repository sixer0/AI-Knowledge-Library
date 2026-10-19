---
name: gsp-observability-tracer
description: >-
  Record tool calls, state transitions, decisions, failures, and resource
  usage during execution for debugging, evaluation, and improvement.
  Captures a structured trace log that can be reviewed post-hoc to
  understand agent behavior, diagnose failures, and identify optimization
  opportunities.
license: MIT
metadata:
  hermes:
    tags: [gsp, observability]
    category: observability
  category: observability
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/observability-tracer
    license_path: LICENSE
---

# Observability Tracer

Record structured traces of agent execution — tool calls, state transitions,
decisions, failures, and costs — so you can debug failures, evaluate
performance, and improve workflows with data-driven insight.

---

## Triggers

Use this skill when:
- "trace this execution"
- "debug this workflow"
- "record state transitions"
- "observability for this task"
- "log tool calls and decisions"
- "monitor execution flow"
- "instrument this workflow for debugging"
- "capture execution trace for analysis"

Do NOT use for simple one-shot tasks where no debugging or analysis is
needed, or when the user explicitly asks not to log execution details.

---

## Process

### Phase 0: Define Trace Scope

Before tracing begins, define what to capture:

```markdown
## Trace Configuration

**Trace ID:** <unique-id>
**Task goal:** <what is being traced>

**Capture scope:**
- [ ] **All tool calls** — name, input params (sanitized), output summary, duration
- [ ] **State transitions** — before/after snapshots at decision points
- [ ] **Decisions** — what was decided, why, alternatives considered
- [ ] **Failures** — error messages, stack traces, retry attempts
- [ ] **Costs** — token estimates per tool call / per phase
- [ ] **State snapshots** — full context state at checkpoints

**Output location:** `<trace-dir>/trace-<trace-id>.md`
**Max trace entries:** <N> (sliding window — oldest entries pruned when exceeded)
```

**Scope selection guidelines:**
| Scenario | Recommended Scope |
|
---
---
----|
---
---
---
---
---
----|
| Debugging a specific failure | Tool calls + Failures + State at failure point |
| Performance optimization | All tool calls + Costs + Duration per call |
| Eval improvement | Tool calls + Decisions + State transitions |
| General monitoring | Tool calls + Failures + Duration (lightweight) |
| Full audit | All categories |

---

### Phase 1: Initialize Trace

Create the trace log file:

```markdown
# Execution Trace: <trace-id>

**Task:** <goal>
**Started:** <ISO 8601 timestamp>
**Trace scope:** <captured categories>

## Trace Entries

| # | Time | Type | Component | Detail | Duration | Tokens (est.) | Status |
|
---|
---
---|
---
---|
---
---
-----|
---
-----|
---
---
----|
---
---
---
---
---|
---
-----|
```

**Trace file rules:**
- Use markdown for human readability
- Each entry is a row in the trace table
- Type is one of: `tool_call`, `state_transition`, `decision`, `failure`, `checkpoint`
- Status is one of: `success`, `failure`, `in_progress`, `skipped`

---

### Phase 2: Record Events

For each event during execution, append a trace entry:

#### Tool Call

```markdown
| 1 | 12:00:01 | tool_call | read_file | "Read config.yaml (512 bytes)" | 0.3s | ~150 | success |
```

**What to capture for tool calls:**
- Tool name
- Input summary (sanitize secrets — never log API keys, passwords, tokens)
- Output summary (truncate to 100 chars or first N lines)
- Duration in seconds (if measurable)
- Token estimate (input + output tokens where available)
- Status

#### Decision

```markdown
| 2 | 12:00:05 | decision | orchestrator | "Chose reflection-loop over plan-and-execute because task is small and quality-focused" | 0.1s | ~200 | success |
```

**What to capture for decisions:**
- What was decided
- Why (rationale — avoid "seemed right", prefer "because X criteria")
- Alternatives considered (briefly)
- Any trade-offs acknowledged

#### State Transition

```markdown
| 3 | 12:00:30 | state_transition | context | "Phase: research → implement. Files loaded: 3. Decisions made: 2." | 0s | ~50 | success |
```

**What to capture for state transitions:**
- From state → to state
- Key state changes (files loaded, context compacted, subtasks completed)
- Trigger for the transition (what caused it)

#### Failure

```markdown
| 4 | 12:01:00 | failure | read_file | "ENOENT: path not found 'missing.txt'" | 0.2s | ~100 | failure |
```

**What to capture for failures:**
- Error type and message
- Where it occurred (component, phase, line)
- Recovery attempted (if any) and outcome
- Full error context written to separate error log if needed

---

### Phase 3: Generate Trace Summary

When tracing is complete or at regular intervals:

```markdown
## Trace Summary

**Trace ID:** <trace-id>
**Duration:** <total time>
**Total entries:** N

### Statistics

| Metric | Value |
|
---
-----|
---
----|
| Total tool calls | N |
| Successful | N |
| Failed | N |
| Retries | N |
| Total decisions | N |
| State transitions | N |
| Estimated tokens | N |
| Total duration | <time> |

### Category Breakdown

**By tool type:**
| Tool | Calls | Avg Duration | Failures |
|
---
---|
---
----|
---
---
---
----|
---
---
----|
| read_file | 15 | 0.3s | 1 |
| write_file | 5 | 0.5s | 0 |
| web_search | 3 | 1.2s | 0 |

**By failure type:**
| Failure | Count | Root Cause |
|
---
---
---|
---
----|
---
---
---
---|
| ENOENT | 1 | Typo in filename |
| ETIMEDOUT | 2 | Network issues |

### Anomalies Detected

- <unusual patterns, e.g., "read_file called 15 times — possible inefficiency">
- <repeated failures, e.g., "ENOENT occurred twice in same directory">
- <long-running operations, e.g., "web_search took 1.2s avg — slowest tool">

### Recommendations

- <actionable insight from trace analysis>
```

---

### Phase 4: Analyze Trace for Improvement

Use the trace data to drive improvements:

```markdown
## Improvement Analysis

### Efficiency opportunities:
- <tool> called N times but could be batched: <suggestion>
- <tool> returns large responses but only <N>% used: <suggestion>

### Failure patterns:
- <error> occurs in <N>% of traces: <root cause and fix>
- <decision> was reversed N times: <suggestion>

### Cost optimization:
- Top 3 most expensive operations: <list>
- Estimated tokens saved if <change>: <estimate>
```

**Analysis approaches:**
| Pattern | What It Indicates | Action |
|
---
---
---|
---
---
---
---
---
----|
---
-----|
| High retry count on same tool | Tool unreliable or misused | Review tool definition or error handling |
| Many small file reads | Fragmented I/O pattern | Batch reads or restructure data access |
| Long decision time on routine choices | Missing context or confusing options | Add clearer guidance or defaults |
| Repeated state transitions | Context thrashing | Restructure phase boundaries |
| Expensive tool calls for trivial results | Poor tool selection | Improve tool descriptions or ordering |

---

### Phase 5: Archive or Clean Up

After analysis:

```markdown
## Trace Archival

**Trace ID:** <trace-id>
**Status:** <archived / deleted / retained for comparison>

**Retention decision:**
- Keep for comparison with future traces? <yes/no>
- Contains sensitive data? <yes/no — if yes, sanitize>
- Reference in eval improvement? <yes/no — eval-id if applicable>
```

**Trace retention rules:**
- Keep traces from failed/debugged tasks for at least 7 days
- Keep traces referenced by eval improvements indefinitely
- Sanitize traces containing secrets before retention
- Prune traces older than 30 days unless explicitly retained

---

## Anti-Patterns

| Avoid | Instead |
|
---
----|
---
---
---|
| Logging secrets, API keys, or credentials | Sanitize all sensitive data before recording |
| Capturing everything without focus | Define scope in Phase 0 based on the objective |
| Verbose output summaries that bloat traces | Truncate outputs to 100 chars or key lines |
| Only capturing success, never failure | Failures are the most valuable trace entries |
| Measuring without acting on data | Always extract recommendations from trace analysis |
| Infinite trace growth with no pruning | Set max entries and retention policy |
| Trace as an afterthought (too late to capture) | Initialize trace at the start of execution |

---

## Execution Checklist

```
[ ] Phase 0: Trace scope defined (which categories to capture)
[ ] Phase 1: Trace log initialized with ID, goal, scope, table header
[ ] Phase 2: Each event recorded (tool_call, decision, state_transition, failure)
[ ] Phase 2: Secrets sanitized in all entries
[ ] Phase 3: Trace summary generated (statistics, breakdown, anomalies)
[ ] Phase 4: Improvement analysis performed from trace data
[ ] Phase 5: Trace archived or pruned with retention decision
[ ] Verify: No secrets or credentials in any trace entry
[ ] Verify: Every failure has a corresponding trace entry
[ ] Verify: Trace summary includes actionable recommendations
[ ] Verify: Trace scope matches the analysis objective
```

---

## Verification

After tracing:
1. A trace log exists with structured entries for all captured event types
2. No sensitive data (secrets, keys, tokens) appears in any trace entry
3. Trace summary provides statistics and anomaly detection
4. Improvement analysis identifies at least one actionable recommendation
5. Trace retention policy is applied (archive / delete / retain)
6. Trace data is usable for eval-driven improvement (referenced by eval ID if applicable)
