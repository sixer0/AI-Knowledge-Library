#!/usr/bin/env python3
"""Delivery QA gate for a Blender asset (headless: blender -b file.blend -P this.py).

Runs the naming lint of references/optimization-qa.md step 4 and the print /
realtime budget sheet selection of step 3, then prints one JSON verdict line.
glTF validation is a SEPARATE external instrument (the pinned validator's CLI,
contract AN-06-05): run it on the exported GLB and feed its exit code into
this report with --validator-exit N. Exit codes here: 0 pass, 3 policy FAIL,
2 usage error (CLI contract pattern AN-05-15).

Usage::

    blender -b scene.blend -P qa_gate.py -- --class print [--spec spec.json] [--validator-exit 0]

Budget values are NOT hardcoded opinions: they default to the register rows
listed per check and are overridable by a project spec JSON. Anchors:
  identifier charset      AN-06-20
  modular snap grid       AN-06-21
  print thickness         AN-06-15  (default 0.001 scene units)
  zero-area threshold     AN-06-16
  sharp/overhang/distort  AN-06-17..19 (160/45/45 deg)
  triangle runtime truth  AN-02-09; realtime budgets AN-06-09..13 upstream
"""
import json
import math
import re
import sys

try:
    import bpy
except ImportError as exc:
    print(json.dumps({"verdict": "ERROR", "reason": "run inside Blender: %s" % exc}))
    sys.exit(2)

IDENT_OK = re.compile(r"^[A-Za-z0-9_]+$")  # AN-06-20
SHARP_DEG = 160.0        # AN-06-17
OVERHANG_DEG = 45.0      # AN-06-18
DISTORT_DEG = 45.0       # AN-06-19
THICKNESS_MIN = 0.001    # AN-06-15 (scene units; 1 mm at 1 BU = 1 m convention)
ZERO_AREA = 0.0001       # AN-06-16
SNAP_GRID_MIN = 10.0     # AN-06-21 (modular kits only)


def args():
    out = {"class": "generic"}
    argv = sys.argv
    if "--" in argv:
        rest = argv[argv.index("--") + 1:]
        it = iter(rest)
        for a in it:
            if a.startswith("--"):
                out[a[2:]] = next(it, None)
    return out


def load_spec(a):
    if a.get("spec") and a["spec"] != "None":
        try:
            with open(a["spec"], "r") as f:
                return json.load(f)
        except Exception as e:
            print("WARN spec load failed: %s" % e)
    return {}


def main():
    a = args()
    spec = load_spec(a)
    asset_class = a.get("class", "generic")
    validator_exit = int(a.get("validator-exit", "0"))
    rep = {"checks": {}, "verdict": "PASS", "defects": 0, "asset_class": asset_class}
    defects = 0

    # 1. naming lint (FC-24). Blender auto-suffixes .001; strip before lint.
    # Prefix grammar is Prefix_Base_Variant_Suffix per AN-06-20 (style guide 00.1).
    bad_names = [o.name for o in bpy.data.objects
                 if not IDENT_OK.match(re.sub(r"\.\d+$", "", o.name))]
    rep["checks"]["naming"] = {"bad": bad_names, "fail": bool(bad_names)}
    defects += len(bad_names)

    # 2. geometry battery per class
    mesh_objs = [o for o in bpy.data.objects if o.type == "MESH"]
    zero_area_faces = 0
    for o in mesh_objs:
        for p in o.data.polygons:
            if p.area < ZERO_AREA:
                zero_area_faces += 1
        # thickness/overhang proxies need solidify-aware analysis; print class
        # defers to the official print-toolbox battery (see print_note below).
    rep["checks"]["degenerate_faces"] = {"count": zero_area_faces,
                                         "fail": zero_area_faces > 0,
                                         "anchor": "AN-06-16, AN-06-01"}
    defects += int(zero_area_faces > 0)

    if asset_class == "print":
        rep["checks"]["print_note"] = {
            "note": "wall-thickness and overhang checks follow AN-06-15..19 defaults"
                    " (thickness_min %.3f, angle_overhang %.0f deg); run the official"
                    " print-toolbox analysis headlessly for the full battery"
                    % (THICKNESS_MIN, OVERHANG_DEG),
            "fail": False}
    if asset_class == "realtime":
        total_tris = sum(max(0, len(p.vertices) - 2)
                         for o in mesh_objs for p in o.data.polygons)
        budget = float(spec.get("triangle_budget", 0))
        entry = {"runtime_triangles_unbudgeted": total_tris,
                 "anchor": "budgets AN-06-09..13 are per-device; set project spec triangle_budget"}
        if budget:
            entry["fail"] = total_tris > budget
            defects += int(entry["fail"])
        else:
            entry["fail"] = False
            entry["note"] = "no budget in spec: unbudgeted count is informational only"
        rep["checks"]["realtime_budget"] = entry

    # 3. validator verdict from the external instrument (AN-06-05)
    rep["checks"]["gltf_validator"] = {"exit_code": validator_exit,
                                       "fail": validator_exit != 0,
                                       "rule": "nonzero exit = blocking defect list, FC-22"}
    defects += int(validator_exit != 0)

    rep["defects"] = defects
    if defects:
        rep["verdict"] = "FAIL"
    print(json.dumps(rep, indent=1))
    sys.exit(3 if defects else 0)


if __name__ == "__main__":
    main()
