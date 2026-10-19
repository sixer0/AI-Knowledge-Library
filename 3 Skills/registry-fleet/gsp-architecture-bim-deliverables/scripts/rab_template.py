#!/usr/bin/env python3
"""
Template RAB/BOQ arsitektur (gsp-architecture-bim-deliverables).
Menghasilkan CSV template ke stdout (ganti isi volume/harga sesuai proyek).

Pemakaian:
  python3 rab_template.py > rab.csv            # template penuh (12 kelompok)
  python3 rab_template.py --kecil > rab.csv    # template ringkas (rumah tinggal)
  python3 rab_template.py --cek rab.csv        # ringkas subtotal per kelompok + total
"""
import csv, io, sys, argparse

SKELETON = [
    ("1. Pekerjaan Persiapan", ["Mobilisasi & demobilisasi", "Bouwplank & pengukuran", "Direksi keet / gudang", "Pembersihan lapangan"]),
    ("2. Tanah & Pondasi", ["Galian tanah pondasi", "Urugan pasir bawah pondasi", "Pondasi batu kali / beton", "Sloof & pembesian", "Urugan tanah kembali"]),
    ("3. Struktur", ["Kolom (beton bertulang)", "Balok (beton bertulang)", "Plat lantai", "Tangga", "Pembesian & bekisting"]),
    ("4. Dinding & Plesteran", ["Pasangan dinding bata ringan", "Plesteran & acian", "Beton rabat / spesi"]),
    ("5. Penutup Lantai & Dinding", ["Lantai keramik/granit", "Dinding keramik km/wc", "Plint lantai"]),
    ("6. Plafon & Rangka", ["Rangka plafon", "Penutup plafon gypsum", "List plafon"]),
    ("7. Atap", ["Rangka atap (kayu/baja ringan)", "Penutup atap", "Talang & flashing", "Overstek & lisplang"]),
    ("8. Pintu, Jendela & Kusen", ["Kusen pintu/jendela", "Daun pintu", "Daun jendela", "Kunci & hardware"]),
    ("9. Sanitasi & Plumbing", ["Pipa air bersih & fitting", "Pipa air kotor & vent", "Sanitair (kloset, wastafel, bak)", "Septic tank & resapan"]),
    ("10. Elektrikal & Pencahayaan", ["Instalasi titik listrik", "Panel & MCB", "Fitting & lampu", "Stop kontak & saklar", "Penangkal petir (bila ada)"]),
    ("11. Finishing", ["Cat dinding & plafon", "Cat kayu & besi", "Coating lantai (bila perlu)"]),
    ("12. Lansekap & Luar", ["Paving & area parkir", "Taman & tanaman", "Drainase & resapan"]),
]

def cek(fn):
    seen, order = {}, []
    with open(fn, newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            g = (row.get("kelompok") or "").strip()
            if g not in seen:
                seen[g] = 0.0; order.append(g)
            try:
                seen[g] += float(row.get("subtotal") or 0)
            except ValueError:
                pass
    tot = sum(seen.values())
    print(f"{'Kelompok':<42}{'Subtotal':>16}")
    for g in order:
        print(f"{g:<42}{seen[g]:>16,.0f}")
    print(f"{'TOTAL':<42}{tot:>16,.0f}")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--kecil", action="store_true", help="template ringkas (rumah tinggal)")
    ap.add_argument("--cek", metavar="FILE", help="ringkas subtotal per kelompok dari CSV")
    a = ap.parse_args()
    if a.cek:
        cek(a.cek); return
    groups = SKELETON
    if a.kecil:
        groups = [g for g in SKELETON if g[0] in
                  ("1. Pekerjaan Persiapan", "2. Tanah & Pondasi", "3. Struktur",
                   "4. Dinding & Plesteran", "5. Penutup Lantai & Dinding", "6. Plafon & Rangka",
                   "7. Atap", "8. Pintu, Jendela & Kusen", "9. Sanitasi & Plumbing",
                   "10. Elektrikal & Pencahayaan", "11. Finishing")]
    out = io.StringIO()
    w = csv.writer(out)
    w.writerow(["no", "kelompok", "pekerjaan", "satuan", "volume", "harga_satuan", "subtotal"])
    no = 1
    for g, items in groups:
        for it in items:
            w.writerow([no, g, it, "", "", "", ""])
            no += 1
    sys.stdout.write(out.getvalue())

if __name__ == "__main__":
    main()