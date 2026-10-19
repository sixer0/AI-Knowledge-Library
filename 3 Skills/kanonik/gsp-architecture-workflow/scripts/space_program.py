#!/usr/bin/env python3
"""
Space program builder untuk workflow arsitektur GSP (gsp-architecture-workflow).
Input : CSV program ruang: kode,nama_ruang,jumlah_unit,luas_netto_m2,keterangan
        (opsional: baris pertama boleh berisi header)
Output: ringkasan netto, brutto (faktor koreksi), cek KDB/KLB terhadap luas lahan.

Pemakaian:
  python3 space_program.py program.csv [--fasilitas BRUTTO_FACTOR] [--lahan AREA_M2] [--kdb 0.6] [--klb 2.0]
Faktor brutto default 1.40 (umum mixed-use; hunian 1.25, kantor 1.35, rumah sakit 1.45).
"""
import csv, sys, argparse

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("csv", help="CSV program ruang")
    ap.add_argument("--fasilitas", type=float, default=1.40, help="faktor brutto (default 1.40)")
    ap.add_argument("--lahan", type=float, default=None, help="luas lahan m2 (untuk cek KDB/KLB)")
    ap.add_argument("--kdb", type=float, default=None, help="KDB maksimum (0..1)")
    ap.add_argument("--klb", type=float, default=None, help="KLB maksimum")
    args = ap.parse_args()

    rows = []
    with open(args.csv, newline="", encoding="utf-8-sig") as f:
        rdr = csv.DictReader(f)
        for r in rdr:
            try:
                luas = float(r.get("luas_netto_m2") or 0)
                unit = int(float(r.get("jumlah_unit") or 1))
            except ValueError as e:
                print(f"!! baris tidak valid (skip): {r} -> {e}")
                continue
            rows.append((r.get("kode","?"), r.get("nama_ruang","?"), unit, luas))

    netto = sum(unit * luas for _, _, unit, luas in rows)
    brutto = netto * args.fasilitas

    print(f"Ruang      : {len(rows)}")
    print(f"Luas NETTO : {netto:,.2f} m2")
    print(f"Luas BRUTO : {brutto:,.2f} m2  (faktor {args.fasilitas})")
    print()
    for kode, nama, unit, luas in rows:
        print(f"  {kode:<8} {nama:<30} {unit:>3} x {luas:8.2f} = {unit*luas:10.2f} m2")

    if args.lahan:
        print("\n--- Cek KDB/KLB ---")
        print(f"Lahan       : {args.lahan:,.2f} m2")
        if args.klb is not None:
            lantai_teoritis = brutto / args.lahan
            max_floor_area = args.klb * args.lahan
            print(f"KLB {args.klb:g} -> luas lantai maks {max_floor_area:,.2f} m2; kebutuhan {brutto:,.2f} m2 "
                  f"({lantai_teoritis:.2f}x KLB) -> {'OK' if brutto <= max_floor_area else 'MELEBIHI KLB'}")
        if args.kdb is not None:
            print(f"Catatan: cek KDB butuh luas lantai dasar aktual (bukan brutto); bandingkan "
                  f"luas tapak bangunan <= {args.kdb:g} x {args.lahan:,.2f} m2 = {args.kdb*args.lahan:,.2f} m2")
        ok = (args.klb is None or brutto <= args.klb * args.lahan)
        print("RESULT:", "OK" if ok else "REVIEW")

if __name__ == "__main__":
    main()