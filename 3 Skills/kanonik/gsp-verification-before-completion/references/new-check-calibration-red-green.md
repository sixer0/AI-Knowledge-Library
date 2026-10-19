# Kalibrasi CHECK BARU pada gerbang deterministik — resep merah-hijau + korpus nyata

Preseden: NAT-GATE-R1 30-09 (scanner `scan_ai_footprint.py` v1.4.1 -> v1.5.0, indikator
baru B11/C-13 + B12/C-14, ambang C-6 25->18 dan B8 80->56). Kelas masalah: menambah atau
melonggarkan check pada instrumen gerbang — bukan menambal instrumen yang rusak
(itu [`instrument-gate-patch-red-green.md`](instrument-gate-patch-red-green.md)), melainkan membuat daya pisah baru yang
belum pernah diuji dunia.

## Hukum induk

Detektor baru lahir SALAH sampai dibuktikan benar pada dua arah: fixture selftest
(merah wajib FAIL, hijau wajib PASS) DAN korpus artefak nyata (vonis lama vs baru
dibandingkan per berkas). Selftest saja membuktikan detektor bekerja; hanya korpus
nyata membuktikan ia tidak menampar yang benar.

Lima cacat desain detektor baru tertangkap dalam SATU sesi ini — semuanya oleh
fixture/korpus, nol oleh penalaran awal:

1. **Bobot metrik salah**: menghitung PASANGAN kalimat identik membuat satu gagasan
   diulang 3x = 1 pasangan (INFO), sementara dua gagasan diulang 2x = 2 pasangan
   (FAIL) — kasus terparah terasa paling ringan. Tambalan: metrik SALINAN BERLEBIH
   (ukuran kelompok − 1) lewat clustering, bukan counting pasangan.
2. **Normalisasi kasus lupa**: "Gerbang" (awal kalimat) ≠ "gerbang" (tengah) sehingga
   parafrase lolos similarity. Fixture merah jadi INFO, bukan FAIL. Lowercase SEBELUM
   tokenisasi apa pun.
3. **Buta morfologi bahasa target**: kata persis tidak mengenali memeriksa↔diperiksa
   (aktif/pasif Indonesia). Stem prefiks heuristik (meng/mem/per/di/ter/…, sisa ≥4
   char) + ambang kemiripan diturunkan 0.80→0.70 SETELAH diukur, bukan ditebak.
4. **Label struktural dihitung prosa**: kepala tabel/`Sumber ...`/`Gambar ...` WAJIB
   seragam format antar bagian (Module L.3-L.4) — persamaannya bukan pengulangan.
   Tanpa pengecualian: 18 temuan PALSU pada satu deliverable nyata; setelahnya 0.
5. **Kelas ambigu jangan menghasilkan FAIL**: kode kebijakan/standar (SPK-002, V-1) sering
   jadi OBJEK pembicaraan laporan verifikasi dan penjelasannya berupa prosa, bukan
   kurung. Pisahkan kelas KERAS (id kartu, status mentah, hash, nama kolom — selalu
   jejak mesin → FAIL) dari kelas LUNAK (→ INFO dulu, naikkan setelah korpus ≥20).

## Resep kalibrasi korpus (terbukti jalan)

1. Simpan salinan scanner PRA-perubahan sebagai baseline alami (kanonik belum
   terdistribusi = kebetulan yang bisa dipakai; jangan andalkan — snapshot sendiri
   kalau perlu).
2. Tulis SATU pembanding `compare_gate_versions.py --old --new --files ... [--channel]`
   yang mencetak per berkas: vonis lama, vonis baru, FAIL hilang, FAIL baru; plus
   ringkasan agregat. Simpan di `scripts/fleet-ops/<misi>/`.
3. Pilih berkas UJI dari kanal yang BENAR (deliverable klien kanal etalase, bukan
   kontrak internal — berkas internal dikecualikan gerbang dan vonisnya tidak
   berarti). Temuan FAIL baru WAJIB diverifikasi konteks manual sebelum diterima:
   dump ±70 karakter di sekitar token dengan regex, baca apakah kodenya objek
   pembicaraan sah.
4. Angka ringkasan masuk SKILL.md + Decision Log sebagai bukti kalibrasi (mis.
   "8 berkas: 3 tak berubah, 3 FAIL hilang, 2 FAIL baru nyata, 0 palsu tersisa").
5. Determinisme: dua run selftest byte-identik (sha bandingkan), exit 0.

## Jebakan verifikasi distribusi (terukur 30-09)

- `sha256sum` pada Windows MSYS mencetak awalan `\` pada path → `cut -c1-16` memotong
  string SALAH dan diff string tampak beda padahal hash identik. Jangan bandingkan
  hash lewat pemotongan string shell.
- Pipeline `a=$(sed 's/^\\//' <<< ...)` gagal parse (sed error) tapi TETAP mengembalikan
  0; kedua variabel jadi KOSONG; `[ "$a" = "$b" ]` bernilai benar → mencetak "IDENTIK"
  palsu untuk SEMUA berkas. Equality antara dua nilai kosong bukan bukti.
- Resep benar: satu helper Python kecil (`hashlib.sha256(open(p,'rb').read())`) yang
  membandingkan HEKS PENUH kedua sisi dan print per pasangan. Bila shell dipakai juga,
  assert kedua sisi non-empty sebelum membandingkan.

## Batas suntingan berkas kebijakan

Menyunting berkas standar itu sendiri WAJIB lolos sapuan byte-level U+2014/U+2013/
U+2212/U+00B7 SEBELUM klaim selesai — dalam sesi ini dua em dash dan satu minus
matematis tersisip oleh suntingan tentang larangan em dash, plus satu aksara CJK
siluman di tabel contoh. Grep byte-level per baris, bukan mata.
