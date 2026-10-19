# Hasil audit bahasa AI Knowledge Library

Audit bertahap selesai pada 19 Oktober 2026. Sebanyak 4.429 berkas asli diinventarisasi:
4.246 berkas teks UTF-8 dipindai, sedangkan 183 berkas biner diperiksa keutuhannya.
Penyuntingan memperjelas singkatan, ungkapan internal, campuran bahasa, dan susunan
aturan yang padat. Sebanyak 859 berkas pustaka diperbarui, termasuk tujuh indeks,
README utama, dan manifest. Nama serta lokasi berkas asli tetap sama.

| Folder | Berkas asli | Diperbarui | Hasil dan laporan |
|---|---:|---:|---|
| 1 Workflow | 9 | 7 | [Prosedur dan istilah kerja diperjelas](1-laporan.md) |
| 2 Roles | 50 | 46 | [Petunjuk peran dan aturan padat diuraikan](2-laporan.md) |
| 3 Skills | 2321 | 282 | [Singkatan dan istilah internal diperjelas](3-laporan.md) |
| 4 Knowledge Bank | 1293 | 506 | [Label 459 kartu vendor dan prosa kurasi diperjelas](4-laporan.md) |
| 5 Integration | 7 | 3 | [Panduan bridge ditulis dalam bahasa Indonesia](5-laporan.md) |
| 6 Database | 3 | 1 | [Fungsi skema dan snapshot dijelaskan](6-laporan.md) |
| 7 Tools | 744 | 12 | [Indeks perkakas dan contoh prompt diperjelas](7-laporan.md) |

Jumlah perubahan pada tabel adalah keadaan akhir setelah pemeriksaan lintas folder.
Dua berkas tambahan di luar tabel adalah README utama dan MANIFEST.csv. Rincian setiap
berkas, jenis pemeriksaan, serta SHA-256 sebelum dan sesudah tersedia pada
[cakupan audit](cakupan-audit.csv). Masing-masing laporan juga menyertakan daftar
perubahan untuk foldernya. Kolom jumlah singkatan dan istilah pada CSV merupakan penunjuk pencarian, bukan skor mutu atau bukti tulisan mesin. Kemunculan dalam kode, contoh uji, kutipan, dan istilah teknis dapat tetap sah.

## Perubahan yang paling membantu pembaca

- Singkatan seperti “utk”, “dgn”, “yg”, dan “tsb” ditulis lengkap dalam prosa.
- Ungkapan “angka hantu”, “artefak mendarat”, dan “indikator menagih” diperjelas menurut konteksnya.
- Rangkaian aturan dalam satu paragraf diuraikan menjadi butir tanpa mengubah urutan, kewajiban, atau angka.
- Status pada kartu vendor diberi penjelasan, misalnya source-matched berarti isi sesuai dengan sumber. Status historis tersebut tidak dianggap sebagai hasil verifikasi baru.
- Berkas peran yang telah disunting diberi keterangan sebagai salinan editorial, sehingga tidak lagi dilabeli verbatim.

[Pedoman bahasa](PEDOMAN-BAHASA.md) menjelaskan prinsip penyuntingan yang dapat dipakai
pada pembaruan berikutnya.

## Verifikasi dan batas audit

Hasil verifikasi akhir: **LULUS**, dengan nol regresi tautan lokal yang terdeteksi. Rincian tercatat dalam [verifikasi.json](verifikasi.json). Pemeriksaan
mencakup keberadaan seluruh berkas asli, ukuran dan SHA-256 manifest, cakupan indeks,
metadata, blok kode, kode sebaris, URL, angka di luar penanda daftar pada prosa yang disunting, himpunan nilai
literal, serta konsistensi salinan skill. Sebanyak 1.130 pasangan skill yang semula
identik tetap identik. Sebanyak 19 pasangan yang sudah berbeda sebelum audit tetap
diperlakukan sebagai versi terpisah; lihat [perbandingan salinan](3-perbandingan-salinan.md).

Pemindaian pola dilakukan pada seluruh berkas teks; pembacaan editorial difokuskan
pada temuan dan pola berulang. Ini bukan pembacaan manual setiap kalimat dan bukan
penilaian apakah suatu tulisan dibuat oleh AI. Kutipan, teks sumber, data terstruktur,
korpus uji yang sengaja rusak, dan bukti biner dipertahankan. Teks Mandarin serta
bahasa Inggris yang jelas tidak diterjemahkan seluruhnya.

Audit tidak menjalankan layanan atau skrip operasional, mengubah konfigurasi provider
atau model, memperbarui host asal atau NAS, menguji ulang situs vendor, ataupun
memeriksa fakta eksternal dan keamanan. Nama profil dan model yang tertulis dalam
sumber adalah catatan sumber, bukan pengaturan sesi yang diubah.

Pemeriksaan akhir menemukan dua contoh korpus uji ikut tersunting; keduanya dipulihkan
ke versi awal sebelum audit ditutup. Koreksi ini memiliki commit tersendiri. Hasil
perbandingan byte, bukan klaim penyunting, menjadi dasar status keutuhan.

## Temuan teknis di luar penyuntingan bahasa

- README bridge sumber mencantumkan waktu tunggu bawaan 240000, sedangkan skrip mencantumkan 1800000. Catatan perbedaannya ditambahkan; konfigurasi tidak diubah.
- Modul gate_transport.mjs dan berkas launchd yang disebut panduan bridge tidak disertakan dalam salinan.
- Judul dan metadata versi standar penempatan skrip sudah berbeda pada edisi awal; audit bahasa tidak menetapkan versi kebijakan baru.
- Rujukan ke path host, arsip legacy, dan folder misi yang tidak disertakan dapat tetap tidak terbuka dari repositori ini. Pemeriksaan tautan membedakan masalah yang sudah ada dari regresi akibat penyuntingan.

## Riwayat commit

Repositori: [sixer0/AI-Knowledge-Library](https://github.com/sixer0/AI-Knowledge-Library), privat.

| Commit | Isi |
|---|---|
| [8785880](https://github.com/sixer0/AI-Knowledge-Library/commit/8785880) | Versi awal sebelum audit |
| [e11558f](https://github.com/sixer0/AI-Knowledge-Library/commit/e11558f) | Folder 1 Workflow |
| [7e180bc](https://github.com/sixer0/AI-Knowledge-Library/commit/7e180bc) | Folder 2 Roles |
| [503e982](https://github.com/sixer0/AI-Knowledge-Library/commit/503e982) | Folder 3 Skills |
| [e53c039](https://github.com/sixer0/AI-Knowledge-Library/commit/e53c039) | Folder 4 Knowledge Bank |
| [976fb02](https://github.com/sixer0/AI-Knowledge-Library/commit/976fb02) | Folder 5 Integration |
| [8b97884](https://github.com/sixer0/AI-Knowledge-Library/commit/8b97884) | Folder 6 Database |
| [2eb5db0](https://github.com/sixer0/AI-Knowledge-Library/commit/2eb5db0) | Folder 7 Tools |
| [877a550](https://github.com/sixer0/AI-Knowledge-Library/commit/877a550) | Pemulihan korpus uji dan penyesuaian pembulatan indeks |
| [3417689](https://github.com/sixer0/AI-Knowledge-Library/commit/3417689) | Penyuntingan istilah tersisa pada pemeriksaan akhir |

Commit penutup setelah daftar ini memuat README utama, laporan akhir, dan bukti
verifikasi. Untuk melihat kalimat yang berubah, buka commit terkait lalu pilih Files changed.

## Mengulang pemeriksaan

Jalankan dari root repositori:

```sh
python3 outputs/audit-bahasa-2026-10-19/periksa_audit.py
```

Skrip memakai pustaka standar Python dan Git. Skrip membaca riwayat serta berkas lokal;
skrip tidak menjalankan perkakas operasional. Opsi `--output <path>` menyimpan laporan
JSON bila diperlukan. Baseline yang dipakai adalah commit 8785880.
