#!/usr/bin/env python3
"""
U-value selubung multi-lapis (gsp-architecture-building-physics).
U = 1 / (Rsi + sum(d/lambda) + Rse)   [W/m2K]; Rsi=0.13, Rse=0.04 m2K/W.

Pemakaian:
  python3 calc_thermal_uvalue.py 'plester:0.015:0.8' 'aac:0.10:0.17' 'plester:0.015:0.8'
  (format lapisan: nama:tebal_m:lambda_W_mK)
"""
import sys

RSI, RSE = 0.13, 0.04

def main():
    if len(sys.argv) < 2:
        print(__doc__); sys.exit(2)
    layers = []
    for a in sys.argv[1:]:
        try:
            name, d, l = a.split(":")
            layers.append((name, float(d), float(l)))
        except ValueError:
            print(f"!! format salah (skip): {a}")
    Rtot = RSI + RSE
    print(f"{'Lapisan':<14}{'tebal(m)':>10}{'lambda':>9}{'R (m2K/W)':>12}")
    for name, d, l in layers:
        r = d / l
        Rtot += r
        print(f"{name:<14}{d:>10.3f}{l:>9.3f}{r:>12.3f}")
    print(f"\nR total = {Rtot:.3f} m2K/W")
    print(f"U-value = {1.0/Rtot:.3f} W/m2K")
    print("Catatan: rongga udara tidak berventilasi menambah R ~0.18 m2K/W; bukaan/kusen "
          "dan jembatan termal tidak dihitung di sini.")

if __name__ == "__main__":
    main()