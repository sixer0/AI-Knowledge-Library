# Menambal INSTRUMEN verifikasi (bukan artefak) — resep red-green dua arah

Preseden: misi buku 25-09, ruling D-12 (gerbang rekons `check_guide.py`) dan
D-13 (parser subgraph `build_docx.py`). Kelas masalah: vonis FAIL/NEEDS_REVIEW yang
tidak bisa lagi berubah jadi PASS lewat suntingan artefak apa pun, karena PUTUSAN
KONTROLLER mengubah objek sementara instrumen beku masih mengukur rumus lama.

## Pola 1 — gate instrumen jadi tak-bisa-dilulusi (unpasseable)

Tanda: verifier melapor NR dengan akar "cacat alat", bukan cacat produk; ia bahkan
menyiapkan resep tambalan tapi MENOLAK menambal lalu memvonis hasilnya sendiri.
Hormati penolakan itu — itu prinsip penulis-bukan-verifikator bekerja.

Yang benar (controller):
1. Sahkan opsi tambal-instrumen, TOLAK opsi longgarkan-predikat. Bila verifier
   menawarkan "ubah predikat jadi cukup isi node saja" supaya hijau, itu penambalan
   gejala: struktur kontrak hilang dari dokumen, vonis jadi palsu.
2. Kartu FIX alat: sunting SATU titik pada instrumen, WAJIB simpan salinan
   pra-sunting (`x.py.R5-orig`) sebagai bukti, dan uji dua arah:
   - HIJAU: instrumen tertambal vs objek nyata -> PASS
   - MERAH-1: instrumen tertambal vs mirror TANPA stringsuntikan ruling -> tetap GAGAL
     (buktikan mirror byte-eksak: buang baris sisipan -> sha harus sama dengan sha
     pra-sunting)
   - MERAH-2: instrumen PRA-TAMBAL vs objek nyata -> tetap GAGAL
   Tiga hasil ini yang membuktikan hijau baru bukan pelonggaran buta.
3. Tambalan harus struktural-eksplisit, bukan fuzzy: cabang regex yang menuntut
   kalimat beku utuh (`'Catatan durasi.*?13 minggu.*?9 minggu.*?189'` DOTALL), bukan
   "kalau perlu, anggap koheren".
4. Vonis dilakukan verifier LAIN (atau run independen verifier yang sama dengan
   kontrol anti-pelonggaran): audit diff instrumen sendiri (SequenceMatcher, bukan
   salinan diff pekerja), dua run identik-byte, pin sha objek read-only sebelum dan
   sesudah.

## Pola 2 — builder/parser menghapus elemen desain

Tanda: gerbang tampil DOCX FAIL karena label/struktur sumber hilang di dokumen jadi
(misal `subgraph ID[Label]` dilewati parser -> diagram terbit datar).

Aturan: pulihkan struktur di BUILDER (kumpulkan label, cetak sebagai baris judul
grup), jangan redefine predikat verifier. Selaras RULE KONTRAK DESAIN ANTI-DRIFT:
keberadaan+bentuk elemen kontrak tidak boleh hilang; mekanisme boleh disesuaikan.
Setelah rebuild: catat sha256 baru, sumber md tetap read-only (sha sumber dipin =
objek vonis sebelumnya), dan ukur nyata di aplikasi target (Word COM: halaman, kata),
bukan hanya parse pustaka.

## Pola 3 — DEFECT PALSU dari alat ukur sendiri (paling sering terjadi)

Tiga kejadian nyata dalam satu sesi, semuanya alat controller yang salah, artefaknya
benar:
- Regex penanda `[C-nn]` melaporkan 0 pada bab yang memakai bentuk lintas lajur
  `[L6 C-06]` / `[L8 C-39]` -> bab-07 dilaporkan "tanpa sitasi"; sebenarnya 96 penanda sah.
- Penghitung `^### ` melaporkan "0 subseksi" pada bab yang menandai konsep dengan
  `## 5.x`. Level heading berbeda antar penulis, isinya lengkap.
- Field kunci register paket `reg_id` dibaca sebagai `id` -> semua rujukan dilaporkan
  "reg tak ada".

Aturan turunannya:
1. Sebelum menuduh pekerja, DUMP bentuk token/heading/field yang sebenarnya ada di
   artefak (Counter atas semua `\[[^\]]{1,24}\]`, histogram level heading, nama field
   JSON nyata), lalu lebarkan checker.
2. Laporkan koreksi sebagai cacat alat, dengan angka sebelum/sesudah, bukan sebagai
   cacat produk. Catatan jujur ke user lebih murah dari kartu FIX palsu.
3. Konvensi level heading antar berkas parallel wajib disatukan di langkah perakitan
   (ASM), kalau tidak uji anatomi downstream akan menangkap selisih cosmetic sebagai
   FAIL.
4. Ukuran berkas: angka kartu sering beda beberapa puluh byte dari disk (suntingan
   ekor setelah klaim). Selalu kutip angka DISK, catat selisihnya, jangan vonis cacat.

## Pola 4 — alat ukur ditulis sebagai berkas, bukan one-liner raksasa

Rangkaian `grep | awk | sed | sha256sum` panjang dalam satu baris memicu hardline
blocklist parser (`command parser limit or malformed executable payload`) dan output
terminal terpotong jadi "1 lines output". Resep yang jalan:
- Tulis helper `.py` kecil ke `$LOCALAPPDATA/Temp`, jalankan
  `uv run --python 3.11 python helper.py > out.txt 2>&1; cat out.txt`.
- Satu helper dipakai ulang lintas giliran (ukur 8 lajur, ukur berkas bab, cek board)
  sehingga angka antar giliran sebanding.
- Untuk JSON board: jangan inline `python -c "..."` bersarung kutip ganda — tulis
  skrip, eksekusi, baca file output.
