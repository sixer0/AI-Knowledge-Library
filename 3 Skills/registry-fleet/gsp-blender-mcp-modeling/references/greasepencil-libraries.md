# Grease Pencil 2D and Licensed Asset Libraries

Chapter spine distilled from report Chapter 7 (lane 7, register AN-L7,
accessed 2026-10-16). Census counts and catalogue totals are register rows in
block AN-07-nn; era-bound to the pinned Blender - pin the version next to every
count when quoting them elsewhere. Known limitation carried from the lane:
several licence texts were only partially reachable on access day, so licence
claims below stop at what the register rows state and no further.

## Competency

1. Grease Pencil in the pinned release is a first-class object type, not a
   canvas overlay: strokes live as points and edit-lines inside a datablock
   with materials bound at stroke level. Measured API census (classes and
   operators in AN-07-03, AN-07-04) gives an automation operator enough surface
   to work without touching any GUI.
2. The competency map covers the documented draw tools, onion skinning with
   full range control per layer, the Line Art modifier as the formal 3D-to-2D
   bridge, the generate-GP modifier family, automatic interpolation in two
   flavors, and multiframe editing (AN-07-01, AN-07-02 plus manual pages in
   source-links D-131 through D-148).
3. Rendering truth for claims: GP renders through Workbench, EEVEE, and Cycles
   panels, while the visual-effect types are viewport-first and cannot be
   applied - never promise baked effects the pipeline will drop (FC-27). Yang
   membedakan GP from the mesh pipeline here is object identity: strokes are
   first-class datablocks with their own shader model, so mesh habits imported
   wholesale produce silent style failures rather than errors.
4. Library competency is licensing literacy with numbers behind it. The CC0
   floors are measured inventories (Poly Haven and ambientCG rows AN-07-05
   through AN-07-12); Blendkit counts in AN-07-13 sit under two license
   families with commercial use safe but resale prohibited in identical form;
   marketplace terms bar standalone resale under Fab Standard and restrict
   editorial tiers (registered as partial-verification gaps in SKILL.md
   provenance); CGTrader runs three license classes (AN-07-16); Free3D stays
   off the recommended list until its license text is verified from a primary
   path.

## Working procedure (scripted workflow in templates/gp-workflow.md)

1. Instantiate a blank Grease Pencil object, enable auto-key for animated
   strokes, draw in Draw Mode, edit through the stroke-level surfaces; when
   scripting via `execute_blender_code`, target the operator namespace counted
   in AN-07-04 rather than emulating mouse paths.
2. Drive look through the two-part GP material shader model, remembering GP
   materials are not BSDFs and bind at stroke level.
3. Bridge dimensions with Line Art for cel-style over 3D geometry, choosing
   occlusion thresholds from the manual page; generate derived strokes with the
   generate-GP family before falling back to hand drawing.
4. Animate economically: key sparse extremes, then Interpolate or Interpolate
   Sequence for gaps and Multiframe for cross-frame corrections.
5. Export vector output deliberately: SVG works both directions; PDF export
   requires Object Mode with the largest-area viewport orientation - conditions
   scripts must set explicitly because headless inherits viewport state.
6. For asset sourcing, query APIs rather than scraping pages: Poly Haven
   exposes `files_hash` and `max_resolution` metadata for download integrity
   and resolution QA; ambientCG's full-JSON endpoint paginates through its
   documented next-page field; Blendkit's category endpoint publishes
   authoritative counts. Validate every filter token against the response echo
   - an unknown type token is silently ignored and returns the whole catalog
   instead of the slice (FC-26).

## Limitations

- The Blendkit search endpoint reports a count ceiling no matter how large the
  true catalog is; naive scripts conclude "ten thousand assets" where the
  category census says otherwise. Totals come from category census fields;
  search counts are caps (AN-07-13 versus AN-07-14; FC-25).
- VFX types resist application and resist per-layer treatment; exports depend
  on view orientation; API censuses are era-bound (pin the version).
- Licensing honesty: aggregate Sketchfab counts are unavailable to anonymous
  queries by design, Fab's terms text reachable only partially, CGTrader
  wording paraphrase-level, Free3D an explicit unverified-blocked source. None
  of these gaps licenses inventing a claim (SKILL.md provenance table).

Register anchor block: AN-07-01 through AN-07-16.
