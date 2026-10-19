---
name: gsp-checkpoint-resume
description: >-
  Persist workflow state at explicit checkpoints so long-running tasks can
  be interrupted and resumed without losing context or progress. Captures
  goal, completed steps, artifacts, decisions, and the next action needed.
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration]
    category: orchestration
  category: orchestration
  source:
    repository: 'https://github.com/anthropics/skills'
    path: skills/checkpoint-resume
    license_path: LICENSE
---

# Checkpoint & Resume

Create persistent checkpoints during long-running tasks so work can be
interrupted and resumed without losing context, progress, or decisions.
Each checkpoint captures a complete snapshot of what was done and what
comes next.

---

## Triggers

Use this skill when:
- "create a checkpoint for this workflow"
- "save progress and resume later"
- "stateful workflow with recovery points"
- "checkpoint before risky operation"
- "save and restore task state"
- "interruption-safe execution"

Do NOT use for short tasks that complete in a single session, or when no
interruption risk exists.

---

## Process

### Phase 0: Define Checkpoint Strategy

Before executing work, define where checkpoints are needed:

```markdown
## Checkpoint Plan

**Task goal:** <restated goal>
**Estimated duration:** <short / medium / long — if long, checkpoint aggressively>

**Checkpoint points:**
| # | Trigger | What to Capture | Priority |
|---|---------|-----------------|----------|
| 1 | Before risky operation | Current state + rollback plan | HIGH |
| 2 | After each major step | Completed work + artifacts | HIGH |
| 3 | Before user interruption | Full context + next action | MEDIUM |
| 4 | Periodically (every N turns) | Compact log of decisions + progress | LOW |

**Checkpoint location:** `<task-dir>/_checkpoint.yaml` or `<task-dir>/checkpoints/checkpoint-N.yaml`
```

**When to checkpoint:**
- Before any destructive or irreversible operation
- After completing a major subtask (especially if it took >5 tool calls)
- Before asking the user a question (in case they return later)
- Periodically on long tasks (every 10-15 tool calls)
- When the agent detects potential interruption (timeout approaching, long operation)

---

### Phase 1: Create Checkpoint

At each trigger point, create a checkpoint file:

```yaml
# _checkpoint.yaml  or  checkpoints/checkpoint-<timestamp>.yaml

checkpoint:
  version: 1
  timestamp: <ISO 8601>
  task_id: <unique identifier for this task>

goal:
  original: <user's original request>
  current: <refined understanding after progress>

status:
  overall_progress: <percentage estimate or "phase X of Y">
  phases_completed:
    - phase: <name>
      status: completed
      artifacts:
        - path: <path>
          description: <what it contains>
      decisions:
        - <key decision made>
    - phase: <name>
      status: in_progress / pending
      # ...

context:
  input_files: [<paths that were read>]
  output_files: [<paths that were created or modified>]
  key_decisions:
    - decision: <what was decided>
      rationale: <why>
      alternatives_considered: [<options that were rejected>]
  known_issues:
    - issue: <problem>
      status: resolved / deferred / blocking

next_action:
  immediate: <the very next thing to do>
  blocked_by: <anything that must happen first, or "none">

metadata:
  tool_calls_so_far: <count>
  tokens_used_estimate: <rough estimate>
  skill_in_use: <skill name if applicable>
```

**Checkpoint file rules:**
- Use YAML for machine readability (easy for agent to re-read)
- Keep checkpoints in the task's working directory
- Sequential numbering for multiple checkpoints
- Each checkpoint captures cumulative state (not delta)

---

### Phase 2: Resume from Checkpoint

When resuming a task:

1. **Detect checkpoint:** Check if `_checkpoint.yaml` or `checkpoints/` exists in the task directory
2. **Load checkpoint:** Read the latest checkpoint file
3. **Restore context:**

```markdown
## Resume from Checkpoint

**Task:** <goal.current>
**Progress:** <status.overall_progress>

**Completed:**
<list of phases_completed with artifacts>

**Decisions made so far:**
<list of key_decisions>

**Next action:**
<next_action.immediate>

**Blocked by:**
<next_action.blocked_by or "nothing">
```

4. **Validate context:**
   - Are all referenced artifacts still present?
   - Are the decisions still valid?
   - Has the environment changed since checkpoint?
5. **Proceed:** Execute `next_action.immediate`
6. **After completion of the resumed step:** Create a new checkpoint

**Resume vs restart:**
- If checkpoint file exists and is < 24h old: resume
- If checkpoint file exists but is > 24h old: validate decisions with user before resuming
- If no checkpoint file exists: start fresh

---

### Phase 3: Handle Checkpoint Gaps

When resuming reveals missing or corrupted checkpoint data:

```markdown
## Checkpoint Gap Detected

**Missing:** <what should be in the checkpoint but isn't>

**Recovery options:**
1. **Partial resume:** Continue with available context; document the gap
2. **Reconstruct:** Look at available artifacts and conversation to rebuild state
3. **Fresh start:** Abandon checkpoint and begin from scratch

**Recommended:** Partial resume with gap documentation
```

---

### Phase 4: Finalize Checkpoint

When the task is complete:

1. Create a final checkpoint capturing the complete task
2. Mark the checkpoint as `status: complete`
3. Optionally archive checkpoints (keep for reference or clean up)

```yaml
checkpoint:
  version: 1
  timestamp: <ISO 8601>
  status: complete

goal:
  original: <original request>
  completed: true

summary:
  total_checkpoints: N
  total_tool_calls: N
  phases_completed: N of N
  all_artifacts:
    - path: <path>
      type: created / modified / read

outcome:
  success: true
  deferred_items:
    - <anything knowingly left unfinished>
  lessons_learned:
    - <insight from the task>
```

---

## Example: Checkpoint Layout

```
task-directory/
  _checkpoint.yaml          # Latest checkpoint (symlink or copy)
  checkpoints/
    checkpoint-20260612_100000.yaml
    checkpoint-20260612_103000.yaml
    checkpoint-20260612_110000-final.yaml
  _task_state.yaml          # (Optional) Detailed state, read on demand
```

---

## Anti-Patterns

| Avoid | Instead |
|-------|---------|
| Checkpointing every tool call (too granular) | Checkpoint at natural boundaries (subtask, user interaction, risky op) |
| Not checkpointing before risky operations | Always checkpoint before destructive/irreversible operations |
| Relying on auto-save without explicit checkpoints | Create explicit, intentional checkpoints |
| Storing checkpoints outside the task directory | Store checkpoints in the working task directory |
| Not validating checkpoints on resume | Always verify artifacts and decisions still hold |
| Checkpoints without "next action" | Every checkpoint must include the immediate next step |

---

## Execution Checklist

```
[ ] Phase 0: Checkpoint strategy defined (trigger points, location)
[ ] Phase 1: Checkpoint created with all required fields
[ ] Phase 1: YAML file written to task directory
[ ] Phase 2: On resume — checkpoint loaded and context restored
[ ] Phase 2: Artifacts validated for existence and integrity
[ ] Phase 3: Checkpoint gaps handled (partial resume / reconstruct / fresh start)
[ ] Phase 4: Final checkpoint created on completion
[ ] Verify: Every checkpoint includes "next_action"
[ ] Verify: Checkpoint files are valid YAML
[ ] Verify: Resume path restored the correct next action
```

---

## Verification

After checkpoint/resume:
1. Checkpoint files exist in the task directory and are valid YAML
2. Each checkpoint includes: goal, completed phases, artifacts, decisions, next action
3. Resume correctly restores the task context and proceeds to the next action
4. Risky operations were preceded by a checkpoint
5. Final checkpoint marks the task as complete with all artifacts listed
6. No previous context is lost when resuming from a checkpoint
