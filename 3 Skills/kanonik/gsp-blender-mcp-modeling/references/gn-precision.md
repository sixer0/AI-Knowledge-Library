# Geometry Nodes and Precision Parametric Work

Chapter spine distilled from report Chapter 5 (lane 5, register AN-L5,
accessed 2026-10-16). Register block AN-05-nn in references/number-register.md
carries every number and probe print referenced here. The known limitation of
this chapter is its youth: every API seam below was probed on 2026-10-16 and
Blender minor releases move under it, so the drift checks are re-runnable
probes, not permanent truths.

## Competency

1. Geometry nodes are a modifier, not a separate editing mode: the object-level
   handle is a `NodesModifier` (type `NODES`) whose `node_group` points at a
   node tree. Measured class census of modifiers and geometry-node types in the
   pinned RNA: AN-05-02 (AN-05-01 confirms full GN evaluation headless).
2. Fields are functions evaluated per element in an explicit context;
   connecting, capturing, or sampling the wrong context is the classic
   silent-corruption source. Treat Capture Attribute and Statistic nodes as
   stabilization tools, not optional polish. Yang membedakan GN scripting from
   ordinary Python automation is exactly that context rule: the same
   expression evaluated in the wrong element context returns confident numbers
   instead of errors.
3. Performance doctrine is measurable: lazy evaluation, instancing over
   realize, selection gates on expensive nodes, the Timing overlay as the
   profiler. An unbounded tree shows up as wall-clock cost immediately.
4. The decisive automation competency in 2026 is surviving the API drift Blender
   5.2 introduced in exactly the seam scripts rely on. The old `items_new`
   interface method is gone; `new_socket` is the only declared way to build a
   group interface (AN-05-04). Socket identifiers arrive as `Socket_0`,
   `Socket_1`, and onward in declaration order (AN-05-05). Direct dictionary
   assignment on the modifier raises a type error (AN-05-06; FC-05); the
   sanctioned write path is `mod.properties.inputs["Socket_N"]["value"]`
   followed by an update tag (AN-05-08).

## Working procedure (generator skeleton in templates/gn-parametric-generator.md)

1. Build the skeleton in the measured order: create the tree, declare the
   interface with `new_socket(name=..., in_out=..., socket_type=...)` ensuring
   an OUTPUT socket exists, insert nodes reading the interface sockets, then
   attach the `NODES` modifier. Skipping the output socket yields an empty mesh
   with a warning (AN-05-03; FC-16).
2. Drive parameters through modifier inputs only: write via the sanctioned
   route, set `update_tag`, force `view_layer.update()`, and read results from
   the evaluated depsgraph mesh, never the base mesh (AN-05-08 records the
   verified dimension change through exactly this route).
3. Do not fight the interface-default propagation dead end: five forced-update
   routes failed to propagate edited `default_value`s in-process (AN-05-09).
   Interface defaults are authoring-time metadata; runtime variation lives on
   modifier inputs (FC-06).
4. For non-GN parametric links use drivers with the pinned enum vocabulary
   (`SCRIPTED` expression; the legacy `PYTHON` type is rejected, AN-05-10;
   FC-15). Bind variables to other objects' properties, call
   `view_layer.update()`, read back the dependent transform (AN-05-11). A
   driver reading its own object's dimensions produces a measured
   dependency-cycle warning; rebuild through a helper empty (AN-05-12; FC-14).
5. Run everything headless under the CLI contract: `blender -b -P script.py
   --python-exit-code 9`; parse exit codes as the machine verdict; whitelist
   known host noise in stderr so the gate does not false-fail on the addon's
   background-refusal message (AN-05-15).
6. Verify dimensions with the `dim_check` pattern: evaluate, read bounding
   dimensions from the evaluated mesh, compare against the fleet tolerance
   (max(0.5 mm, 0.1 percent of dimension) while no project spec narrows it -
   the ISO primary path is a registered gap, see SKILL.md provenance), and
   export with the apply flag so evaluated geometry lands in the file, then
   re-import in a fresh process and compare (AN-05-18 through AN-05-20).
7. Close the loop with the two-run identity gate: identical scripts in two
   separate processes must print identical JSON and byte-identical GLB digests
   (AN-05-20, AN-05-21 - demonstrated on this build).

## Limitations

- The silent-empty failure family dominates GN automation and is contractual,
  not buggy: the exporter writes base meshes unless told otherwise, so a
  procedural object can produce a valid-but-empty GLB (byte-size contrast in
  AN-05-18) with no error beyond an omitted-primitives note. Validate by
  measured primitive counts, not exit codes alone (FC-04).
- API seam traps are recorded with their exact sanctioned alternatives:
  `hasattr` lies about `modifier_apply_as_new_mesh` (stub attribute, operator
  missing, AN-05-16; FC-07), socket dictionary writes are rejected (FC-05),
  interface edits stall in-process (FC-06).
- Unit discipline stays unforgiving: `scale_length` is cosmetic for internal
  physics, millimeter-convention scenes still store plain Blender units
  (AN-05-14), and crossing the glTF meter contract without normalization
  produced a measured thousandfold inflation on import (FC-13).

Register anchor block: AN-05-01 through AN-05-21.
