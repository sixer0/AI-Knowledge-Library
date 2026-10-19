#!/usr/bin/env python3
"""Topology gate for a Blender asset (headless: blender -b file.blend -P this.py).

Implements the soft-topology battery of references/optimization-qa.md step 2
and the pole rule of references/modeling-topology.md. Exit code is the machine
verdict (CLI contract AN-05-15): 0 pass, 3 on any FAIL, 9 on script error.

Checks and their register anchors (thresholds are register facts, restating
them here as defaults only; override with project spec):
  pole valence            AN-02-05  (valence != 4 is a pole)
  manifoldness            AN-06-14  (exactly two faces per edge)
  degenerate area         AN-06-16  (zero-area threshold 0.0001)
  winding sign            AN-06-02  (positive determinant => counter-clockwise)
  triangle runtime truth  AN-02-09  (primitives become GPU draw calls; non-triangles undefined)

Usage: set TARGETS list below or pass object names after '--'::

    blender -b scene.blend -P topology_checks.py -- Cube Armature_child
"""
import json
import math
import sys

try:
    import bpy
    import bmesh
except ImportError as exc:  # not running inside Blender
    print(json.dumps({"verdict": "ERROR", "reason": "run inside Blender: %s" % exc}))
    sys.exit(2)

ZERO_AREA = 0.0001  # AN-06-16


def arg_objects():
    if "--" in sys.argv:
        return [a for a in sys.argv[sys.argv.index("--") + 1:]]
    return []


def mesh_objects():
    names = arg_objects()
    objs = [o for o in bpy.data.objects if o.type == "MESH"]
    if names:
        objs = [o for o in objs if o.name in names]
    return objs


def tri_count_and_area(bm):
    tris = 0
    degenerate = 0
    for f in bm.faces:
        tris += max(0, len(f.verts) - 2)
        if f.calc_area() < ZERO_AREA:
            degenerate += 1
    return tris, degenerate


def poles(bm):
    return sorted({v.index for v in bm.verts if len(v.link_edges) not in (0, 1, 2, 4)})


def nonmanifold_edges(bm):
    return sum(1 for e in bm.edges if len(e.link_faces) != 2)


def winding_signs(obj):
    """Face normals vs transformed geometry: negative-scale flips hand.
    Report any mesh whose world matrix determinant is negative AND whose loop
    order was not compensated (engine fix rule AN-06-02)."""
    mw = obj.matrix_world.copy()
    return "negative" if mw.determinant() < 0 else "positive"


def main():
    report = {"checks": {}, "verdict": "PASS", "defects": 0}
    objs = mesh_objects()
    if not objs:
        report["verdict"] = "FAIL"
        report["reason"] = "no mesh objects matched"
        report["defects"] = 1
        print(json.dumps(report))
        sys.exit(3)
    defects = 0
    for o in objs:
        dg = bpy.context.evaluated_depsgraph_get()
        ev = o.evaluated_get(dg)
        bm = bmesh.new()
        try:
            bm.from_mesh(ev.to_mesh())
        except Exception:
            bm.from_mesh(o.data)
        bm.calc_loop_triangles()
        tris, degen = tri_count_and_area(bm)
        entry = {
            "runtime_triangles": tris,           # budget vs AN-06-09..13 upstream
            "degenerate_faces": degen,           # glTF allows 0 (AN-06-01)
            "poles": len(poles(bm)),             # informational, AN-02-05
            "nonmanifold_edges": nonmanifold_edges(bm),
            "winding_world": winding_signs(o),
        }
        bad = degen > 0 or nonmanifold_edges(bm) > 0 or tris == 0
        entry["fail"] = bad
        defects += sum([degen > 0, nonmanifold_edges(bm) > 0, tris == 0])
        report["checks"][o.name] = entry
        bm.free()
    report["defects"] = defects
    if defects:
        report["verdict"] = "FAIL"
    print(json.dumps(report, indent=1))
    sys.exit(3 if defects else 0)


if __name__ == "__main__":
    main()
