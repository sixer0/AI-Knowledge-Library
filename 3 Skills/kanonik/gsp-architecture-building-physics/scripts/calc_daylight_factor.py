#!/usr/bin/env python3
"""
Daylight factor estimasi (gsp-architecture-building-physics).
DF ~ (Awin * tau * theta) / (Aroom * (1 - rho)) * 100%

Pemakaian:
  python3 calc_daylight_factor.py --win 4.0 --room 20 [--tau 0.6] [--theta 0.25] [--rho 0.5]
tau = transmisi kaca (0.5-0.7 jernih, 0.3-0.5 coated); theta = faktor sudut langit
(~0.2-0.3 jendela dinding termasuk frame/dirt, 0.5-0.6 skylight);
rho = reflektansi rata-rata ruang (0.4-0.6).
Target praktis: DF >= 1-2% cukup siang; >= 2-5% terang; >5% risiko silau/panas.
Estimasi fase desain - distribusi aktual butuh simulasi (Radiance dll).
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--win", type=float, required=True, help="luas bukaan kaca (m2)")
    ap.add_argument("--room", type=float, required=True, help="luas lantai ruang (m2)")
    ap.add_argument("--tau", type=float, default=0.6)
    ap.add_argument("--theta", type=float, default=0.25)
    ap.add_argument("--rho", type=float, default=0.5)
    a = ap.parse_args()
    if a.room <= 0 or a.tau <= 0 or a.rho >= 1:
        print("!! cek parameter: room>0, tau>0, rho<1"); sys.exit(2)
    df = (a.win * a.tau * a.theta) / (a.room * (1 - a.rho)) * 100.0
    print(f"Awin={a.win:.2f} m2 | Aroom={a.room:.2f} m2 | tau={a.tau:.2f} | theta={a.theta:.2f} | rho={a.rho:.2f}")
    print(f"Daylight Factor ~ {df:.2f} %")
    if df < 1:
        print("Band: rendah (<1%) - pertimbangkan bukaan lebih besar/tinggi atau skylight.")
    elif df < 2:
        print("Band: cukup siang (1-2%).")
    elif df < 5:
        print("Band: terang (2-5%) - waspadai silau pada area kerja.")
    else:
        print("Band: sangat terang (>5%) - risiko silau/panas berlebih.")

if __name__ == "__main__":
    main()