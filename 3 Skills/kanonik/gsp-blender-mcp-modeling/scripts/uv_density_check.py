#!/usr/bin/env python3
"""UV texel-density and overlap checker (headless: blender -b file.blend -P this.py).

Blender ships no native density checker (report Chapter 3), so this is the
pipeline's own. Density thresholds are PROJECT POLICY, never conformance law:
the practice band is AN-03-03/AN-03-04 (reference values ~2.56 to ~20.48
px/cm) and must be set per project via CLI argument below. Overlap check uses
island bounding-box intersection as a fast conservative proxy.

Exit codes: 0 pass, 3 policy FAIL, 9/2 usage error (AN-05-15 contract).

Usage::

    blender -b scene.blend -P uv_density_check.py -- --pxcm 5.12 --atlas 2048

Defaults: --pxcm required to pass loudly; atlas 2048 px assumed.
Register anchors: bake margin rule AN-03-01 (islands >= 2 px apart), density
band AN-03-03/AN-03-04, texture memory arithmetic pattern AN-03-10.
"""
import json
import math
import sys

try:
    import bpy
except ImportError as exc:
    print(json.dumps({"verdict": "ERROR", "reason": "run inside Blender: %s" % exc}))
    sys.exit(2)


def args():
    out = {}
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        it = iter(rest)
        for a in it:
            if a.startswith("--"):
                out[a[2:]] = next(it, None)
    return out


def uv_area_poly(uv_loop):
    """Signed area of the UV polygon of one face (abs)."""
    pts = [l.uv for l in uv_loop]
    if len(pts) < 3:
        return 0.0
    s = 0.0
    for i in range(len(pts)):
        x1, y1 = pts[i]
        x2, y2 = pts[(i + 1) % len(pts)]
        s += x1 * y2 - x2 * y1
    return abs(s) / 2.0


def main():
    a = args()
    if "pxcm" not in a:
        print(json.dumps({"verdict": "ERROR",
                          "reason": "density is project policy: pass --pxcm <float> (practice band cites AN-03-03/AN-03-04)"}))
        sys.exit(9)
    policy_pxcm = float(a["pxcm"])
    atlas = int(a.get("atlas", 2048))
    report = {"policy_px_per_cm": policy_pxcm, "atlas_px": atlas,
              "checks": {}, "verdict": "PASS", "defects": 0}
    defects = 0
    for o in [x for x in bpy.data.objects if x.type == "MESH"]:
        me = o.data
        if not me.uv_layers.active:
            continue
        uv = me.uv_layers.active.data
        total_uv_area = 0.0
        total_area_m2 = 0.0  # BU^2 surface (1 BU = 1 m convention unless spec says otherwise)
        overlap_pairs = 0
        # world-unit surface area + UV coverage + face UV bboxes
        boxes = []
        for p in me.polygons:
            total_area_m2 += p.area
            total_uv_area += uv_area_poly([uv[li].uv for li in p.loop_indices])
            us = [uv[li].uv[0] for li in p.loop_indices]
            vs = [uv[li].uv[1] for li in p.loop_indices]
            boxes.append((min(us), min(vs), max(us), max(vs)))
        # O(n^2) bbox overlap is fine for gate-sized meshes; note: adjacent
        # faces share edges so equality-touch counts as overlap only beyond eps
        eps = 1e-6
        for i in range(len(boxes)):
            for j in range(i + 1, len(boxes)):
                b1, b2 = boxes[i], boxes[j]
                if b1[2] - eps <= b2[0] or b2[2] - eps <= b1[0]:
                    continue
                if b1[3] - eps <= b2[1] or b2[3] - eps <= b1[1]:
                    continue
                # skip direct neighbours (share a vertex)
                if set(me.polygons[i].vertices) & set(me.polygons[j].vertices):
                    continue
                overlap_pairs += 1
                break
        cm2 = total_area_m2 * 10000.0  # 1 BU assumed 1 m per project sheet convention
        # even-average texel density: px per cm = atlas * sqrt(uv_fraction / cm2)
        achieved_pxcm = atlas * math.sqrt(total_uv_area / cm2) if cm2 > 0 else 0.0
        entry = {
            "uv_area_fraction": round(total_uv_area, 6),
            "surface_cm_equiv": round(math.sqrt(cm2), 3) if cm2 else 0.0,
            "avg_px_per_cm": round(achieved_pxcm, 3),
            "policy_px_per_cm": policy_pxcm,
            "nonadjacent_uv_bbox_overlaps": overlap_pairs,
        }
        low = achieved_pxcm < policy_pxcm * 0.8
        entry["fail"] = bool(low or overlap_pairs)
        defects += int(low) + int(overlap_pairs > 0)
        report["checks"][o.name] = entry
    report["defects"] = defects
    if defects:
        report["verdict"] = "FAIL"
    print(json.dumps(report, indent=1))
    sys.exit(3 if defects else 0)


if __name__ == "__main__":
    main()
