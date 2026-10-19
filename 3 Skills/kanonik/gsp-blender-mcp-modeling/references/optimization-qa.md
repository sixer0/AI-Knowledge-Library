# Optimization and Measurable QA Standards

Chapter spine distilled from report Chapter 6 (lane 6, register AN-L6,
accessed 2026-10-16). Register block AN-06-nn carries every number; the gate
itself is `scripts/qa_gate.py` plus the validator step below. One known
limitation travels with the whole chapter and is stated here rather than
buried: three of the requested normative numbers do not exist as public
primaries as of 2026-10-16, so the chapter inherits empty register rows plus
named gaps instead of borrowed figures wearing costume citations.

## Competency: "high quality and standard" splits into two testable halves

The mission phrase deserves one explicit adjudication before the mechanics,
because most teams fuse the two words and then argue about taste. Yang
membedakan the halves is the kind of instrument each answer is allowed to
cite: one half resolves into an instrument with an exit code, the other half
into a budget table selected per asset domain and dated to 2026-10-16. Read
the rows that follow with that separation in mind.

1. Standard = normative conformance. The glTF 2.0 specification forbids
   degenerate triangles within primitives (SHOULD NOT, validator error class,
   AN-06-01), fixes winding by the sign of the transform determinant
   (AN-06-02), expects power-of-two texture dimensions with a resize
   recommendation otherwise (AN-06-03), and positions the official
   glTF-Validator as the binary pass-or-fail instrument whose CLI contract
   exits nonzero on any error (AN-06-05; FC-22).
2. High quality = domain-selected budgets. A print deliverable is judged on
   manifoldness (exactly two faces per edge, AN-06-14) and wall-thickness
   defaults from the official add-on source (AN-06-15 through AN-06-19). A
   real-time XR deliverable is judged on platform triangle budgets and
   draw-call classes measured against the vendor's published per-device
   guidance (AN-06-09 through AN-06-13), under the interactive framerate floor
   in AN-06-12.
3. Naming and identity discipline is part of the competency set because
   standards work is partly metadata work: the de-facto identifier convention
   and the modular-kit grid promise both trace to the community style guide the
   lane verified live (AN-06-20, AN-06-21; FC-24).
4. Batching ceilings give the runtime teeth: static and legacy dynamic batching
   caps in AN-06-07 and AN-06-08, numbers a script can assert without a human
   reviewer.

## Working procedure (battery implemented in scripts/qa_gate.py)

1. Export first, judge second: produce the GLB with the official exporter, run
   the pinned validator via its npm channel (version reality: it ships no
   GitHub releases, so the npm registry record in AN-06-24 is the pin), and
   treat nonzero exit as a blocking defect list, not advice (FC-22).
2. Run the soft topology battery in the same loop before human eyes touch the
   asset: manifold check by edge-face incidence, degenerate-area flagging,
   winding sign under negative scales, NPOT texture detection, UV stretch
   measurement through the overlay surface or its bmesh equivalent - all
   reachable headless through `bpy` and `bmesh`.
3. Apply the budget sheet selected for the asset class: print thresholds
   (AN-06-14 through AN-06-19) or the realtime ladder (AN-06-09 through
   AN-06-13), including LOD screen-coverage transitions via the documented
   extension id sequence in AN-06-06.
4. Lint naming mechanically: reject anything outside the identifier character
   set, require prefix discipline, verify pivot and snap behavior for modular
   kits against the grid rule. Marketplace rejection is a schedule failure as
   real as a crash (FC-24).
5. Mirror the exporter's own CI pattern as the acceptance loop: export,
   validate, round-trip re-import, compare measured bounds and counts, only
   then hand to visual review.
6. Count triangles post-export against budget rows, never pre-export on
   authoring quads: decimate triangulates and budgets computed on quads miss
   runtime truth (AN-02-09 context; FC-23).
7. For FBX deliverables state version reality plainly: the exporter is an
   add-on at the measured version with a stated minimum (AN-06-23), no public
   formal specification of FBX semantics exists to cite, so claims stay at
   documented-add-on-surface strength and nothing stronger.

## Limitations (inherited verbatim from the chapter)

- No public standard prescribes texel density numerically; any such number in a
  pipeline document is policy borrowed from practice, never conformance.
- glTF-Toolkit is archived (last commit measured, AN-06-25): reference pattern,
  not dependency.
- Epic's Nanite statement removes polygon and draw-call ceilings on supported
  platforms without publishing a replacement numeric ceiling (AN-06-22): budget
  claims for Unreal targets must say which side of the Nanite line they stand
  on.
- Documentation rot moved the print toolbox manual onto an archive path while
  the official source folder remains authoritative for defaults (AN-06-23):
  read source, not memory.
- Freshness pressure: every pin here carries a recheck obligation (report
  Chapter 6 closing note and Appendix F).

Register anchor block: AN-06-01 through AN-06-25.
