# Modeling Theory and Topology

Chapter spine distilled from report Chapter 2 (lane 2, register AN, accessed
2026-10-16). Cite AN-02-nn rows from references/number-register.md for any
number; nothing here restates a threshold value inline. The known limitation
inherited from the lane travels with every rule below: community forum
evidence stays a restricted evidence class, and one book identifier remains
deliberately empty rather than plausibly filled (report Appendix F).

## Competency: three levels, never fused

1. Authoring level: quad-dominant meshes because the manual states they deform
   well and loops carry predictable edge flow. Subdivision level: Catmull-Clark
   math assumes a quad cage, so poles (valence different from four) become
   visible defects near deformation. Runtime level: every primitive becomes one
   GPU draw call and non-triangles are not defined by the exchange format, so
   engines eat triangles regardless of authoring virtue (AN-02-05, AN-02-09).
   Reason for separating them: the deform argument is manual-sourced and the
   planarity argument is computational geometry; conflating them is how forum
   folklore gets cited as fact.
2. Ngons are a measured boundary, not an absolute ban: safe on flat faces and
   non-deforming regions after applying modifiers, forbidden under Subdivision
   Surface where they produce recognizable artifacts (FC-17). Yang membedakan a
   boundary from a ban is arithmetic: the manual positions ngons as a judgment
   area with named failure conditions, so the QA battery, not a style rule,
   decides each case.
3. What automation officially promises: remesh and Quadriflow retopology, with
   the manual conceding that automatic retopology for deformation has no
   perfect solution. Honest pipelines are sculpt-then-retopologize with seed
   values locked for reproducibility (AN-02 rows on retopology limits).
4. Hard-surface and organic are two sourced recipes, not taste. Organic: low
   quad cage, support loops, Catmull-Clark or Multiresolution adds density.
   Hard-surface: Bevel modifier with segments at least two (below that, profile
   and miter settings do nothing measurable), Weighted Normals with face
   influence, smooth-by-angle; all exposed on the Python API so a script can
   assert parameters numerically (AN-02-04; FC-18).
5. In era 5.x smoothing-by-angle is a modifier, so scripts inspect the modifier
   stack instead of legacy mesh flags, and free normals replace legacy
   auto-smooth flags: clean hard-surface shading at the cost of compatibility
   on export paths that ignore custom split data, decided per target format by
   the QA gate.
6. Unit honesty: Unit Scale changes only what the interface displays, never
   internal physics (AN-02-06). Precision lives in Blender-unit numbers plus an
   explicit millimeter convention stated in project sheets.

## Working procedure (executable order; checks in scripts/topology_checks.py)

1. Author at the lowest tier that holds the silhouette: cube to loop cuts,
   loops following anticipated deformation lines, poles kept away from moving
   areas. Make the pole rule mechanical with the valence-counting check
   (valence three or five-plus flagged), not an eye test.
2. Apply subdivision with budgeted numbers read from the register: viewport
   levels never above render levels, the render level and evaluation quality
   defaults and full ranges are AN-02-01 through AN-02-03; adaptive subdivision
   keeps its pixel default unless instancing forces the object mode at its
   floor (object mode is required for instances).
3. Build the hard-surface stack in order and verify each stage: Bevel with the
   limit method chosen (angle or weight) and clamp overlap on, then Weighted
   Normals with face influence enabled, then Smooth By Angle as a modifier.
4. For sculpted high-poly sources: voxel or dynamic-topology sculpt, then
   Quadriflow or manual retopology with the random seed fixed, then hand the
   mesh to the UV chapter. The pipeline order is contractual because later
   stages inherit these decisions.
5. Cite the canonical curriculum ladder in order when training is requested:
   the Donut series rebuilt for Blender 5.x by Andrew Price as foundation,
   Grant Abbitt's game-ready and hard-surface courses (course shapes in
   AN-02-12), Dan Abbott's verified channel for hard-surface practice, and
   Blender Studio production lessons with open assets to dissect (AN-02-13).
6. Keep the literature chain honest: Catmull and Clark 1978 through Pixar
   subdivision course notes to the GDC tessellation talk and OpenSubdiv, each
   pinned by file-proven evidence (AN-02-10, AN-02-11, AN-02-14; see
   references/source-links.md rows D-035 through D-037, D-049 through D-053).

## Limitations

- No perfect automated deformation retopology exists in the official toolset
  (manual-level statement, not opinion).
- Community answers are a restricted evidence class here: the two highest-voted
  forum threads on ngons sit behind antibot walls and are cited only for the
  existence and direction of the consensus (AN-02-08).
- One book identifier stays deliberately empty in the register after failed
  primary lookups; the accuracy standard prefers an empty field over a
  plausible ISBN (report Appendix F rows).
- Industrial interactive subdivision sits around the OpenSubdiv baseline in
  AN-02-07; benchmark claims against it must state device and era.

Verification hooks: `scripts/topology_checks.py` asserts pole valence,
manifoldness, winding sign, and post-triangulation counts headlessly; run it
before any human review. Register anchor block: AN-02-01 through AN-02-14.
