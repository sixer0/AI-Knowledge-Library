#!/usr/bin/env python3
"""
Ventilasi alami ACH (gsp-architecture-building-physics).
Q = Cd * A_open * v (m3/s); ACH = Q * 3600 / V.

Pemakaian:
  python3 calc_ventilation_ach.py --volume 50 --opening 1.0 --wind 1.0 [--cross]
--cross memakai Cd 0.75 (ventilasi silang efektif); default Cd 0.55 (single-sided).
Contoh realistis: ruang 50 m3, bukaan 1.0 m2, angin 1.0 m/s silang -> ACH ~54.
Pedoman: ruang tinggal berventilasi silang baik 20-60 ACH (tropis); target minimum
kesehatan ~2-4 ACH. Estimasi - sangat sensitif terhadap posisi bukaan; verifikasi CFD bila kritis.
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--volume", type=float, required=True, help="volume ruang (m3)")
    ap.add_argument("--opening", type=float, required=True, help="luas bukaan efektif (m2)")
    ap.add_argument("--wind", type=float, required=True, help="kecepatan angin tapak (m/s)")
    ap.add_argument("--cross", action="store_true", help="ventilasi silang (Cd 0.75)")
    a = ap.parse_args()
    cd = 0.75 if a.cross else 0.55
    if a.volume <= 0 or a.opening <= 0:
        print("!! volume & opening harus > 0"); sys.exit(2)
    q = cd * a.opening * a.wind
    ach = q * 3600.0 / a.volume
    print(f"C_d={cd:.2f} | A_open={a.opening:.2f} m2 | v={a.wind:.2f} m/s | V={a.volume:.2f} m3")
    print(f"Aliran Q = {q:.2f} m3/s")
    print(f"ACH = {ach:.2f} pertukaran/jam")
    if ach >= 20:
        print("Band: tinggi (>=20 ACH) - ventilasi tropis baik; cek kenyamanan tiupan.")
    elif ach >= 4:
        print("Band: memadai (4-19 ACH) untuk ruang tinggal berventilasi alami.")
    else:
        print("Band: rendah (<4 ACH) - tambah bukaan/pastikan aliran silang.")

if __name__ == "__main__":
    main()