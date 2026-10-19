---
name: kanban-complete-artifact-paths
version: 1.0.0
description: Use when kanban_complete rejects declared artifacts.
metadata:
  hermes:
    tags: [gsp, kanban]
    category: devops
---
# kanban_complete artifact path resolution (validated 2026-10-04, t_d42578f9)

## The pitfall
`kanban_complete` preserves declared artifacts by copying them from the task's SCRATCH workspace. Two failure modes observed:

1. Relative paths (e.g. `docs/.../R4.md`) in the top-level `artifacts` param fail with
   "declared scratch artifact is unavailable or not a regular file" even when the file
   exists at that location relative to the shared workspace - resolution is against
   `$HERMES_KANBAN_WORKSPACE`, not the cwd or shared ws.
2. The kernel ALSO scans `metadata.artifacts` (any key named `artifacts`) and tries to
   preserve those paths the same way. A metadata entry `"artifacts": ["docs/..."]`
   reproduces the same error even when the top-level `artifacts` param is correct.

## The fix
- Put deliverables that must upload as native attachments INTO the scratch workspace
  (`cp` them there first) and declare their absolute paths under `$HERMES_KANBAN_WORKSPACE`.
- In `metadata`, NEVER name a key `artifacts` for reference/canonical paths - use
  `path_kanonik_shared_ws` / `changed_files` instead (those are not resolved as files).
- Canonical shared-ws copies stay where the Documentation Contract requires; the scratch
  copies are just for attachment delivery (note both locations in metadata).

## Verification
Retry after fixing keys succeeded first try: `{"ok": true}` with attachments preserved.
