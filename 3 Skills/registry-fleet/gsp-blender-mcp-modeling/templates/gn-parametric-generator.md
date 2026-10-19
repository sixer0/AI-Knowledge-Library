# GN Parametric Generator Recipe (verified-dimension procedural assets)

Purpose: build a geometry-nodes generator headlessly that produces assets with
DIMENSIONS PROVEN on disk, not assumed. Register anchors: AN-05-nn block; every
trap below has an FC row in references/failure-catalog.md. Known limitation of
this recipe: it encodes the API seams of one measured era (pins of 2026-10-16),
so treat each step as a re-runnable probe rather than permanent truth when the
minor version moves.

Dependencies stated: Blender 5.2.x headless (`blender -b -P`); no external
packages; the `bpy` API surface of the pinned version (paths drift across
eras - re-read the RNA when the version moves, FC-35 context).

Skeleton order (contractual; skipping a step has a measured failure mode):

1. Create the node tree, then declare the interface with
   `tree.interface.new_socket(name=..., in_out=..., socket_type=...)` in
   declaration order. Ensure an OUTPUT socket EXISTS: without it the modifier
   evaluates to zero vertices with a depsgraph warning (AN-05-03; FC-16).
   Socket identifiers arrive as `Socket_0`, `Socket_1`, ... in declaration
   order; do not guess stable names for them (AN-05-05).
2. Insert nodes reading the interface sockets, then attach a `NODES`-type
   modifier pointing at the tree (modifier census context: AN-05-02; full
   headless GN evaluation confirmed by AN-05-01).
3. Write parameters ONLY through the sanctioned path:
   `mod.properties.inputs["Socket_N"]["value"] = x`, then set the update tag
   and force `view_layer.update()` (AN-05-08). Direct dictionary assignment
   `mod["Socket_N"] = x` raises TypeError in 5.2 - do not resurrect it
   (AN-05-06; FC-05).
4. Read results from the EVALUATED depsgraph mesh, never the base mesh:
   `dg = bpy.context.evaluated_depsgraph_get(); me = obj.evaluated_get(dg).to_mesh()`.
5. Never edit interface `default_value`s expecting in-process propagation:
   five forced-update routes failed (AN-05-09; FC-06). Defaults are
   authoring-time metadata; runtime variation is step 3.
6. Never trust `hasattr(bpy.ops..., "modifier_apply_as_new_mesh")`: the stub
   attribute exists while the operator raises could-not-be-found (AN-05-16;
   FC-07). Call inside try and verify the effect, not the attribute.
7. Dimensional verification (`dim_check` pattern): read bounding dimensions
   from the evaluated mesh; compare against the fleet tolerance max(0.5 mm,
   0.1 percent of dimension) while no project spec narrows it (gap register:
   ISO primary absent, see SKILL.md provenance); units stay plain Blender
   units regardless of display convention (AN-05-14).
8. Export with `export_apply=True` so evaluated geometry lands in the file
   (exporter applies only this flag among the apply-family, AN-05-17). Without
   it you get the silent-empty trap: a valid GLB of ~10^-1 KB holding nothing,
   with at most an omitted-primitives note (AN-05-18; FC-04).
9. Post-export validation by measured primitive counts, not exit codes:
   re-import the file in a FRESH process, evaluate, and compare vertex counts
   and dimensions against expectations (AN-05-19). Assert non-empty before
   claiming success.
10. Two-run identity gate: run the identical script in two separate processes;
    printed JSON must be identical and the two GLB digests byte-identical
    (AN-05-20, AN-05-21 - demonstrated on the pinned build). Any nondeterminism
    here means a seed or a dictionary order leaked into the graph.
11. Crossing the glTF meter contract requires normalization: importing a
    millimeter-convention asset unnormalized produced a measured thousandfold
    inflation (FC-13); assert bounding dimensions after every import before any
    dimensional claim.
12. Drivers as the non-GN parametric fallback: enum vocabulary `SCRIPTED` only
    (legacy `PYTHON` rejected, AN-05-10; FC-15); break self-dimension loops
    through a helper empty (AN-05-12; FC-14); read back after
    `view_layer.update()` (AN-05-11).

Gate contract: `blender -b -P gen.py --python-exit-code 9`; exit 0 plus a JSON
line containing the keys `n_verts`, `dims`, `glb_bytes`, `glb_sha16`, and
`tolerance_pass` is the machine verdict (AN-05-15). Print, measure from disk,
cite register rows.
