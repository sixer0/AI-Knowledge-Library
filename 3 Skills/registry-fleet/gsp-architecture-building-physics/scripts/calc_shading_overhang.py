#!/usr/bin/env python3
"""
Shading overhang (gsp-architecture-building-physics).
D = V / tan(alpha)  (kedalaman overhang agar bukaan penuh ternaungi pada altitudo alpha)

Pemakaian:
  python3 calc_shading_overhang.py --drop 0.6 --altitude 60 [--gap 0]
--drop    : jarak vertikal tepi bawah overhang ke tepi atas bukaan (m)
--altitude: altitudo matahari kritis (deg). Tropis: tengah hari 60-75; pagi/sore <40.
--gap     : offset horizontal dari dinding ke bukaan (opsional, m) - tambah ke hasil.
Contoh: drop 0.6 m, alt 60 -> D ~ 0.35 m. Untuk barat/timur, shading horizontal saja
tidak cukup - tambah sirip vertikal/eggcrate.
"""
import argparse, math, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--drop", type=float, required=True, help="V: jarak vertikal (m)")
    ap.add_argument("--altitude", type=float, required=True, help="altitudo matahari (deg)")
    ap.add_argument("--gap", type=float, default=0.0, help="offset horizontal bukaan (m)")
    a = ap.parse_args()
    if a.altitude <= 0 or a.altitude >= 90:
        print("!! altitude harus 0<alt<90"); sys.exit(2)
    d = a.drop / math.tan(math.radians(a.altitude)) + a.gap
    print(f"V={a.drop:.2f} m | alt={a.altitude:.1f} deg | gap={a.gap:.2f} m")
    print(f"Kedalaman overhang D = {d:.2f} m")
    print("Catatan: untuk fasad barat/timur, kombinasi horizontal + sirip vertikal lebih efektif.")

if __name__ == "__main__":
    main()