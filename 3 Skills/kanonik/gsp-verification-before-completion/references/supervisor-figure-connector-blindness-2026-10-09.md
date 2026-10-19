# Figure connector blindness — mechanical gate 0 != pixel fit (RAFIF-MF-1009, 2026-10-09/10)

Two independent confirmations in one night that `cacat_gerbang:0` from fontTools-based
diagram gates (gerbang_geometri.py d2734ee7 lineage) does NOT imply the rendered PNG is
technically readable. Both directions of error observed:

- **F2-B / G4.2 (t_904a2817):** run-1 published 6 ids all `cacat_gerbang:0`,
  `deterministik_dua_run:true`, correct machine pin, sidecar attribution clean —
  yet controller independent vision ruled TIDAK-LAYAK: dangling stub segments, a
  connector mis-routed into a foreign column, an arrowhead detached from its node,
  a dashed line crawling along a field border.
- **F1-B / G3.4 + G9.1 (t_421f2836):** after steer-2 added connector gates K1–K4,
  8/10 ids published; controller spot-vision on the two DATUM-33 geometry-change ids
  FAILED BOTH: G3.4 red polyline broken with two floating ends; G9.1 vertical bus
  collinear-overlapping the left borders of two nodes (>3 mm) plus two more floating
  segments. Labels/content intact — pure geometry defect the gate cannot see.

## Residual blind classes after K1–K4 (name them in every figure card)

- **K5 arrow-orientation-vs-border:** an arrowhead may sit exactly on a TOP border yet
  point horizontally (tangent), which reads as detached. Assert marker direction is
  perpendicular (or a deliberate corner-apex entry) relative to the border it lands on.
- **K6 line-through-label-box:** connector passing THROUGH the ink box of a text label
  (not just near it). Knockout-band fixes can create the inverse (band erases foreign
  segments — class G7); assert both: label ink untouched by foreign strokes, and no
  knockout covering non-owned segments.
- **Bus collinearity:** a bus/connector running parallel and <= ~1 mm over a node border
  reads as "border merged with wire". Require >= 3–4 mm separation; measure x-coords of
  vertical bus vs node left/right edges in the SVG, not pixels.
- **Polyline continuity:** gates checking endpoints may still pass a path whose MIDDLE
  segment list has a gap (two polylines that look joined at zoom). Test continuity of the
  full path point sequence against node/bus attachment points.

## Controller vision protocol for figures (six-point, per id, before any L2 vonis)

Run `vision_analyze` on the PUBLISHED PNG asking exactly:
(a) floating/dangling segments without node or bus? (b) every arrowhead landing on the
destination border with perpendicular orientation? (c) any line overlapping a node border
> 3 mm? (d) any label pierced/overlapped by a line or border? (e) all label text complete
and readable (nothing clipped)? (f) content still matches the figure spec (nothing dropped
to achieve the geometry fix)? Verdict LAYAK only if all six pass. Diamond apex entry is
accepted as a corner-entry exception on (b), stated explicitly.

## Worker self-vision claims are the WEAKEST rung

The F2-B worker reported "visus mata CLEAR" for G4.2 while the identical artifact failed
controller vision minutes later. Rule: a worker's own vision pass never closes a figure;
controller (or QC card) re-runs the six-point protocol on the published bytes. When the
worker's mechanical evidence (hashes, determinism, manifest) matches disk but the visual
claim does not survive, vonis = partial: accept the mechanics, convict the id, remediation
card lists the concrete defects WITH coordinates from the controller's own vision output
(gives the next run a targeted repair map instead of a re-debate).

## Steer pattern that worked (timeout/gave_up mid-publish)

Audit disk first (sidecar `kartu` field + manifest sha16 + PNG mtimes distinguish
already-published-by-this-card vs old bytes), then steer: state map (N done, exact sha16,
which ids still old bytes), the specific defect list per failing id with coordinates, the
new mandatory checks (K5/K6 + six-point vision), publish-per-id anti-loss rule, and a
budget-priority order when <50% window remains. Unblock (`hermes kanban unblock`) after
`gave_up` — dispatcher's "will retry" does NOT fire while status=blocked; verify
status=ready in the same turn.
