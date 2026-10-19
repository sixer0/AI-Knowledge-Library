import glob, io, os
MARK = "## RULE AKURASI DATA MUTLAK"
OLD = "Rujukan penuh: shared ws docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md"
NEW = ("8. **Tautan pada keluaran wajib AKTIF dan TERLIHAT**: setiap sel/teks URL yang disajikan harus hyperlink sungguhan (target http/https) dengan gaya tautan (warna tegas + garis bawah); gerbang builder menghitung defect tampil-tautan dan rilis diblokir bila >0 (preseden 04-09: hyperlink ada tapi warna krem tanpa garis bawah = terasa mati).\n"
       "9. **Angka laporan = cetakan alat pada giliran itu** (anti-halusinasi): dilarang mengutip angka dari ingatan/laporan pihak lain tanpa ukur ulang; berkas belum lolos gerbang 100% berlabel KERJA, dilarang jadi acuan.\n"
       + OLD)
home = r"C:\Users\TRIAL\AppData\Local\hermes"
targets = [os.path.join(home, "SOUL.md")] + sorted(glob.glob(os.path.join(home, "profiles", "*", "SOUL.md")))
up = skip = 0
for f in targets:
    if not os.path.exists(f):
        continue
    t = io.open(f, encoding="utf-8").read()
    if MARK not in t:
        continue
    if "Tautan pada keluaran wajib AKTIF" in t:
        skip += 1
        continue
    if OLD not in t:
        print("SKIP-TANPA-RUJUKAN:", f)
        continue
    t2 = t.replace(OLD, NEW, 1)
    assert t2.replace(NEW, OLD, 1) == t
    io.open(f, "w", encoding="utf-8", newline="").write(t2)
    up += 1
print(f"updated={up} skipped={skip} total={len(targets)}")
