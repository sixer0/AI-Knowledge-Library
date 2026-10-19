#!/usr/bin/env python3
"""
Cek kepatuhan tapak arsitektur (gsp-architecture-code-compliance).
Memvalidasi KDB, KLB, KDH, jumlah lantai, dan GSB terhadap parameter zona.
Nilai zona harus berasal dari perda zonasi/RDTR setempat.

Pemakaian:
  python3 compliance_check.py --lahan 500 --kdb 0.6 --klb 2.4 --kdh 0.2 \
      --tapak 300 --lantai 300 300 300 [--gsb 4.0] [--lebar_jalan 8.0]
Keterangan:
  --lantai : daftar luas lantai per tingkat (m2) dari bawah ke atas
  --tapak  : luas lantai dasar (harus <= KDB * lahan); default = lantai[0]
Keluar exit code 1 bila ada pelanggaran (agar mudah diintegrasikan ke gate).
"""
import argparse, sys

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lahan", type=float, required=True, help="luas lahan (m2)")
    ap.add_argument("--kdb", type=float, default=None, help="KDB maksimum (0..1)")
    ap.add_argument("--klb", type=float, default=None, help="KLB maksimum (kali)")
    ap.add_argument("--kdh", type=float, default=None, help="KDH minimum (0..1)")
    ap.add_argument("--tapak", type=float, default=None, help="luas lantai dasar aktual (m2)")
    ap.add_argument("--lantai", type=float, nargs="+", default=[], help="luas lantai per tingkat (m2)")
    ap.add_argument("--gsb", type=float, default=None, help="GSB aktual (m)")
    ap.add_argument("--lebar_jalan", type=float, default=None, help="lebar jalan (m) utk estimasi GSB umum")
    args = ap.parse_args()

    laps = args.lantai if args.lantai else []
    tapak = args.tapak if args.tapak is not None else (laps[0] if laps else 0.0)
    total = sum(laps) if laps else (tapak if args.klb is None else None)
    issues, notes = [], []

    print(f"Lahan={args.lahan:,.2f} m2 | Lantai dasar={tapak:,.2f} m2 | Lantai={len(laps)} "
          f"({', '.join(f'{l:,.0f}' for l in laps)}) | Total={sum(laps):,.2f} m2")

    if args.kdb is not None:
        cap = args.kdb * args.lahan
        ok = tapak <= cap
        print(f"KDB {args.kdb:.1%}: tapak {tapak:,.2f} <= {cap:,.2f} -> {'OK' if ok else 'VIOLASI'}")
        if not ok: issues.append("KDB")
    else:
        notes.append("KDB tidak diberikan -> wajib cek perda.")

    if args.klb is not None and laps:
        cap = args.klb * args.lahan
        ok = sum(laps) <= cap
        print(f"KLB {args.klb:g}: total lantai {sum(laps):,.2f} <= {cap:,.2f} -> {'OK' if ok else 'VIOLASI'}")
        if not ok: issues.append("KLB")
        if args.kdb:
            floor_cap = int((args.klb / args.kdb) + 1e-9)
            print(f"Petunjuk: jumlah lantai teoritis maks ~KLB/KDB = {floor_cap}")
    elif args.klb is not None and not laps:
        cap = args.klb * args.lahan
        print(f"KLB {args.klb:g}: total lantai maks {cap:,.2f} m2 (tak dapat dicek tanpa --lantai)")
        notes.append("KLB tidak dicek penuh: --lantai kosong.")

    if args.kdh is not None:
        need = args.kdh * args.lahan
        green = args.lahan - tapak
        ok = green >= need
        print(f"KDH {args.kdh:.1%}: hijau tersedia {green:,.2f} >= perlu {need:,.2f} -> {'OK' if ok else 'VIOLASI'}")
        if not ok: issues.append("KDH")
    else:
        notes.append("KDH tidak diberikan -> wajib cek perda.")

    if args.gsb is not None:
        print(f"GSB: {args.gsb:g} m (cek terhadap perda: kelas jalan, sempadan sungai/pantai).")
    elif args.lebar_jalan is not None:
        print(f"GSB tidak diberikan; lebar jalan {args.lebar_jalan:g} m -> pedoman umum GSB "
              f"±{min(12, max(2, args.lebar_jalan * 0.5)):.1f} m; WAJIB cek perda setempat.")
        notes.append("GSB estimasi kasar — verifikasi perda.")

    for n in notes: print("NOTE:", n)
    if issues:
        print("RESULT: VIOLATION ->", ", ".join(issues))
        sys.exit(1)
    print("RESULT: OK" if laps or args.kdb is not None else "RESULT: REVIEW (parameter zona belum lengkap)")

if __name__ == "__main__":
    main()