# Grease Pencil Workflow Recipe (scripted 2D in the pinned release)

Purpose: drive Grease Pencil work entirely through the API surface counted in
AN-07-03 and AN-07-04, with no GUI emulation. Census numbers are era-bound to
the pinned Blender 5.2: pin the version next to any count you re-quote
(FC-35 discipline). Known limitation stated up front: this recipe was validated
against 12 draw tools and 123 operators on the 2026-10-16 census, and the next
minor release can move either count without touching your script's logic.

Dependencies stated: Blender 5.2.x (GUI session for interactive passes; GP
object creation and stroke editing also evaluate headless for batch work, but
export orientation rules below inherit viewport state). No external packages.

1. Instantiate a blank Grease Pencil object; enable auto-key before drawing
   animated strokes; enter Draw Mode for interactive work. When scripting via
   `execute_blender_code`, target the documented operator namespace rather than
   emulating mouse paths (tool and modifier family censuses: AN-07-01,
   AN-07-02).
2. Materials bind at STROKE level and GP materials are not BSDFs: drive look
   through the two-part GP shader model, not Principled BSDF habits. A
   Principled material on a GP stroke line is a silent style failure, not an
   error.
3. 3D-to-2D bridge: use the Line Art modifier for cel-style over geometry,
   choosing camera or scene-space occlusion thresholds from the manual page
   (source-links D-136); generate derived strokes with the generate-GP family
   before falling back to hand drawing.
4. Animation economy: key sparse extremes, then Interpolate or Interpolate
   Sequence for the gaps; Multiframe for cross-frame corrections. Onion
   skinning is per-layer with full range control (manual pages D-135, D-139,
   D-140).
5. Vector I/O conditions are explicit code, not user habits: SVG import/export
   works both directions; PDF export REQUIRES Object Mode plus the
   largest-area viewport orientation - set both in the script because headless
   inherits viewport state unpredictably.
6. Rendering claims boundary (FC-27): GP renders through the Workbench, EEVEE,
   and Cycles Grease Pencil panels; the visual-effect types are viewport-first
   and cannot be applied. Rasterize the intended look through the GP render
   panels or bake to texture; never promise VFX baking into final frames.
7. Verification prints: object exists with expected stroke/point counts, frame
   range keys present, export file non-empty with byte size recorded, and a
   render pass written to disk. Measure from disk; report numbers, not adjectives.

Common failures route to references/failure-catalog.md FC-27 (VFX promised but
absent) and the era-pinning rule of FC-35 (census quoted without a version).
