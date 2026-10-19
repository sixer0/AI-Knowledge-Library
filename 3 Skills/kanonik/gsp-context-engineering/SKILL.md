---
name: gsp-context-engineering
description: >-
  Manage long-running agent context to prevent token overflow, focus on
  relevant state, and preserve critical information. Uses compaction,
  summarization, structured memory, and subagent isolation to keep the
  working context lean and effective.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: optimization
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/context-engineering
    license_path: LICENSE
---

# Context Engineering

Manage the agent's working context to stay within token limits while
retaining critical information. Apply compaction, summarization, structured
memory, and context isolation to prevent degradation on long-running tasks.

---

## Triggers

Use this skill when:
- "context is too long for the token limit"
- "compact the conversation history"
- "manage long-running agent context"
- "reduce token usage without losing information"
- "summarize and focus the working state"
- "memory and compaction needed for this task"

Do NOT use for short, single-turn interactions where context is not a
concern, or when the user wants full verbatim history preserved.

---

## Process

### ⚠️ Phase 0 (MANDATORY): Document Task Progress First

**Before ANY compaction action**, the agent MUST document current task progress. This ensures no state is lost if compaction truncates conversation history.

#### Step 0a: Identify Task Folder

Determine the active task folder:
```
/docs/YYYY_MM_DD_<judul-task>/
```
If no task folder exists (ad-hoc session), skip to Phase 1.

#### Step 0b: Update `status_tasks.md`

Read and update the task's status file:
```markdown
## Status Update (Pre-Compaction Snapshot)

**Timestamp:** <ISO 8601>

### Completed Items
- [x] <item just completed>
- [x] <item completed earlier in this session>

### In Progress
- [ ] <current active step>

### Pending
- [ ] <next steps not yet started>

### Decisions Made This Session
- <decision 1>: <rationale>
- <decision 2>: <rationale>

### Current Blockers
- <blocker or "none">

### Key State / Artifacts
- <files created or modified>
- <data obtained, decisions recorded>
```

**Rules:**
- EVERY compaction must be preceded by a status update — even if it feels redundant
- Capture ALL decisions made since the last update — not just code changes
- Note any data, credentials, or context that would be costly to re-obtain
- If the task uses `implementation_plan.md`, update its tracking table too

#### Step 0c: Write Compact Snapshot to Memory

Write a compact snapshot to `memory/tasks/` for post-compaction recovery:

Write file: `memory/tasks/compact-<YYYYMMDD_HHmmss>.md`
```markdown
# Compaction Snapshot: <task title>

**Compacted at:** <ISO 8601>
**Original context utilization:** <percentage>

## Task Identity
- **Task folder:** `/docs/YYYY_MM_DD_<judul-task>/`
- **Current phase/goal:** <what the agent was working on>

## Progress Summary
- Completed: <list>
- In progress: <current step>
- Pending: <next steps>

## Decisions
| Decision | Rationale |
|----------|-----------|
| <decision> | <why> |

## Critical Context (must survive compaction)
- <item that must not be lost>
- <reference to files that contain full detail>

## Open Questions / Blockers
- <anything unresolved>
```

#### Step 0d: Verify Documentation Completeness

Confirm before proceeding:
- [ ] `status_tasks.md` updated with latest progress
- [ ] `implementation_plan.md` tracking table reflects current state (if applicable)
- [ ] Compact snapshot written to `memory/tasks/`
- [ ] All decisions and blockers documented
- [ ] Critical context identified for preservation

---

### Phase 1: Context Audit

Assess the current context state:

```markdown
## Context Audit

**Total estimated tokens:** <rough estimate based on message count and content>
**Token limit:** <known limit, e.g., 200K for Claude>
**Utilization:** <percentage>

**Context composition:**
| Category | Messages | Est. Tokens | Retention Value |
|----------|----------|-------------|-----------------|
| Goal/instructions | N | ~N | CRITICAL |
| Recent work (last N turns) | N | ~N | HIGH |
| Past work (older turns) | N | ~N | LOW-MEDIUM |
| Error logs / tool output | N | ~N | LOW |
| Conversation history | N | ~N | VARIES |

**Recommendation:** <no action needed / compact / summarize / purge>
```

**Red-zone triggers (consider compaction when):**
- Utilization > 70% of limit
- More than 20% of context is low-value (past errors, verbose tool output)
- Agent shows signs of "lost in the middle" (forgets earlier instructions)

---

### Phase 2: Select Compaction Strategy

Choose the right strategy based on utilization and task type:

| Strategy | When to Use | Token Savings | Risk |
|----------|-------------|---------------|------|
| **Summarize** | Need to preserve narrative but reduce verbosity | 40-60% | Loss of nuance |
| **Prune** | Remove redundant tool output, resolved errors, irrelevant history | 20-40% | Loss of error trace context |
| **Restructure** | Replace verbose sections with structured data (YAML, tables) | 30-50% | Loss of prose readability |
| **Fork** | Spin off completed subtasks to subagent, keep only summary | 60-80% | Loss of detailed reasoning |
| **Memory file** | Write detailed state to a file, keep only path + summary | 50-70% | Requires read-back for detail |

**Default recommendation for utilization:**
- 50-70%: Prune + Restructure
- 70-90%: Summarize + Fork
- 90%+: Memory file + Fork (aggressive)

---

### Phase 3: Apply Compaction

Execute the selected strategy:

#### Summarize

For each section identified as "past work" or "low-medium value":

```markdown
<details>
<summary>Compact: <topic> (original N messages)</summary>

**Summary:** <2-3 sentence summary of what happened and what was decided>

**Key outcomes:**
- <outcome 1>
- <outcome 2>

**Open items:**
- <anything still pending>
</details>
```

#### Prune

Remove entirely:
- Successful tool outputs that are no longer referenced
- Error messages for resolved issues
- Conversation turns resolved by later actions
- Duplicate information

**Do NOT prune:**
- Current goal and instructions
- Unresolved decisions or pending items
- User's explicit requirements and constraints
- The latest 2-3 turns (active conversation context)

#### Restructure

Replace verbose prose with structured formats:

- Free-text file lists → YAML manifest
- Long error descriptions → Error ID + summary (full text in log file)
- Step-by-step narratives → Status table

#### Fork (subagent isolation)

When a subtask is complete or can run independently:

1. Summarize the subtask context: goal, inputs, decisions, outputs
2. Open a forked subagent with the summary + detailed state file reference
3. In the main context, keep only: "Subtask X completed: <3-line summary>. Full state: <path>"

#### Memory File

For critical state that exceeds available context:

1. Write current state to `_task_state.yaml` or similar in the working directory
2. Keep only in context: file path + 3-line summary + next action
3. Read back only when needed for the next step

---

### Phase 4: Verify Context Integrity

After compaction, verify that no critical information was lost:

```markdown
## Post-Compaction Verification

| Critical Item | Preserved? | Location |
|---------------|------------|----------|
| Current goal | Yes | Context header |
| User constraints | Yes | Context header |
| Pending decisions | Yes | Open items list (summary) |
| Key artifacts | Yes | File paths in summary |
| Unresolved errors | Partially | Full log in error.log |
```

**If critical info was lost:**
- Re-expand the relevant section from memory file or full history
- Adjust compaction strategy to be less aggressive

**If compaction was applied in the last 5 turns:**
- Flag to the user: "Context was compacted to manage token usage. <N> messages summarized."

---

### Phase 5: Maintenance Cadence

For long-running tasks, set a maintenance schedule:

```markdown
## Context Maintenance Plan

**Check frequency:** every <N> turns / every <N> tool calls
**Next check at:** <turn count or timestamp>
**Strategy:** <compact / fork / memory file>
**Triger conditions:**
- Token utilization > 70%
- Agent repeats or forgets information
- User requests context review
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Compacting without documenting progress first | ALWAYS run Phase 0 (Document Task Progress) before any compaction |
| Compacting while a subtask is mid-execution | Wait for a natural breakpoint (subtask completion, user interaction) |
| Over-summarizing (losing details that matter) | Keep summaries as expandable details; write full state to files |
| Compacting too frequently | Check every 10-15 turns or at 70%+ utilization |
| Only compacting — never restructuring | Restructure first to reduce bulk; compact only if still needed |
| Silently compacting without user awareness | Flag compaction events briefly ("Context compacted: N messages summarized") |
| Assuming `status_tasks.md` is already up to date | Always re-read and update — it may be stale from a previous session |

---

## Execution Checklist

```
[ ] Phase 0: Task progress documented (status_tasks.md updated)
[ ] Phase 0: Compact snapshot written to memory/tasks/
[ ] Phase 0: Documentation completeness verified (5 checks passed)
[ ] Phase 1: Context audit performed (utilization, composition)
[ ] Phase 2: Compaction strategy selected
[ ] Phase 3: Strategy applied (summarize/prune/restructure/fork/memory file)
[ ] Phase 4: Context integrity verified (no critical info lost)
[ ] Phase 5: Maintenance cadence established for long-running tasks
[ ] Verify: Current goal and constraints are preserved
[ ] Verify: User-facing compaction notice is provided
[ ] Verify: Token utilization is now < 60%
[ ] Verify: Task can be resumed from memory/tasks/ snapshot if needed
```

---

## Verification

After context engineering:
1. Token utilization is below threshold (< 60% recommended)
2. Current goal and user constraints are explicitly preserved
3. All unresolved items (decisions, errors, pending actions) are documented
4. Compaction method is documented and could be reversed if needed
5. Agent behavior (correctness, recall) is not degraded after compaction
6. A compact snapshot exists in `memory/tasks/` if compaction was applied to a task session
7. Task progress is recoverable from documentation alone — no critical info exists only in conversation history
