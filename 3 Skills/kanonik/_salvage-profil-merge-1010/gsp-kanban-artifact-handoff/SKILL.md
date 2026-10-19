---
name: gsp-kanban-artifact-handoff
description: Use when completing kanban tasks with deliverable files.
category: devops
---

# Kanban completion with artifacts (GSP worker)

## Pitfall 1 - metadata.artifacts collides with the top-level artifacts param
`kanban_complete(artifacts=[...])` validates EVERY declared path as a regular file it must
preserve. Two failure modes observed on t_77d46f11 (02-09-2026):
- Relative paths (e.g. `docs/.../report.json`) fail with "could not preserve the declared
  artifacts ... still in-flight" even when the file exists in the shared workspace - path
  resolution is against the task scratch workspace, not cwd.
- A dict key literally named `artifacts` INSIDE `metadata` is also scanned; relative paths
  there trigger the same rejection loop (3 identical failures = tool-loop warning).

Fix: put ONLY absolute paths under the task's `$HERMES_KANBAN_WORKSPACE` in the top-level
`artifacts` param; list shared-workspace canonical files under `metadata.changed_files`
(different key name). Copy deliverables into the scratch workspace first:
`cp <shared>/file "$HERMES_KANBAN_WORKSPACE"/...` then declare those copies.

## Pitfall 2 - never attach placeholder bytes
`kanban_attach` with fabricated base64 stores garbage silently (a 33-byte stub was attached
once on t_77d46f11 before the real read). Read the real file bytes first (`base64 -w0 file`),
or skip the attachment and use `artifacts=[...]` instead.

## Handoff pattern for precision-3D export steps (steps 22-26 blueprint)
- Canonical artifacts live in the shared workspace
  `docs/<date>-precision-3d-factory/pilot_p1/`; scratch workspace gets copies for attachment.
- Child gate cards (e.g. P-P1-26-gate) auto-promote on parent `kanban_complete`; do NOT
  sticky-block the parent for review when a pre-created child depends on it.
- Record in metadata: sheet_sha256, measure-hash chain (build == dim_check == round-trip),
  rubric sha match, W1 library pin + wheel SHA-256, naturalization scan verdict + trail sha.

## Round-trip QA facts proven on SBOX-2624P (t_77d46f11, reusable for gate cards)
- Export determinism: two separate `blender -b` processes produce byte-identical GLB+OBJ
  when build is sheet-driven and transform_apply is full (check world matrix identity first).
- GLB round-trip into factory-default scene returns measure hash IDENTICAL to dim_check;
  importing into a scale_length=0.001 scene inflates 1000x (recipe c section 5 pitfall).
- OBJ importer attaches cosmetic rot-Z 180 (sin float32 8.74e-08): world bbox noise ~1.5e-05
  mm while local coords stay exact - report root cause, do not widen bands.
- Cross-language trimesh QA must `merge_vertices(merge_tex=True, merge_norm=True)` before
  watertight/body_count (exporter splits verts per face); OBJ keeps quads/n-gons so
  trimesh.is_watertight is always False there - use raw polygon edge parity instead.
- Native Blender does not understand MSYS paths (`/c/...`): pass `C:/...` forward-slash args.
