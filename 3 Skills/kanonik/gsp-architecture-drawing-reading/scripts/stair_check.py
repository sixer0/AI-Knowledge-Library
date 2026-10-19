#!/usr/bin/env python3
"""
Cek geometri tangga (gsp-architecture-drawing-reading).
Mode A: --floor_h H --n N   -> riser = H/N (m); cek terhadap pedoman
Mode B: --riser R --tread T -> cek 2R+T terhadap 60-63 cm
Mode C: --floor_h H --riser R -> n = ceil(H/R); sisa langkah
Pedoman praktis: riser 0.15-0.20 m, tread 0.25-0.30 m, 2R+T ~ 0.60-0.63 m.
Catatan: verifikasi SNI/perda setempat untuk bangunan publik/aksesibel.
"""
import argparse, math, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--floor_h", type=float, default=None, help="tinggi lantai-ke-lantai (m)")
    ap.add_argument("--n", type=int, default=None, help="jumlah anak tangga (riser)")
    ap.add_argument("--riser", type=float, default=None, help="tinggi anak tangga (m)")
    ap.add_argument("--tread", type=float, default=None, help="lebar injakan (m)")
    a = ap.parse_args()
    issues = []
    if a.floor_h is not None and a.n:
        riser = a.floor_h / a.n
        print(f"Riser dari {a.floor_h:.2f} m / {a.n} = {riser:.3f} m")
        a.riser = riser
    elif a.floor_h is not None and a.riser:
        n = math.ceil(a.floor_h / a.riser)
        print(f"Jumlah anak tangga ~ceil({a.floor_h:.2f}/{a.riser:.3f}) = {n}")
        a.n = n
    if a.riser is not None and not (0.12 <= a.riser <= 0.22):
        issues.append(f"riser {a.riser:.3f} m di luar rentang umum 0.12-0.22 m")
    if a.tread is not None and not (0.22 <= a.tread <= 0.32):
        issues.append(f"tread {a.tread:.3f} m di luar rentang umum 0.22-0.32 m")
    if a.riser is not None and a.tread is not None:
        formula = 2 * a.riser + a.tread
        print(f"2R + T = {formula:.3f} m (target ~0.60-0.63 m)")
        if not (0.56 <= formula <= 0.67):
            issues.append("2R+T di luar target 0.56-0.67 m")
    if a.floor_h is not None and a.n and a.riser is not None:
        print(f"Total naik aktual = {a.n * a.riser:.3f} m (floor_h {a.floor_h:.3f} m)")
    if issues:
        print("ISSUES:")
        for i in issues: print("  -", i)
        sys.exit(1)
    print("RESULT: OK (geometri tangga dalam pedoman; verifikasi standar lokal untuk publik)")

if __name__ == "__main__":
    main()