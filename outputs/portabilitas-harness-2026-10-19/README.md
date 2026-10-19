# Penyesuaian rujukan untuk harness di perangkat

Selesai pada 19 Oktober 2026 untuk lintas harness: Codex, Claude Code, dan pembaca berkas lokal lainnya. Baseline penyesuaian adalah commit `6e31e8b`, yaitu hasil akhir audit bahasa sebelumnya.

Sebanyak **5.914 tautan lokal** ditambahkan atau diperbaiki pada koleksi. Seluruh **4.420 entri** dalam tujuh indeks kini berupa hyperlink relatif yang dapat dibuka dari dokumen indeks. Sebanyak **372 jangkar** ditambahkan sesuai ID baris kemampuan pada 20 dokumen domain. Tidak ada layanan, profil, provider, model, atau konfigurasi global harness yang dipasang atau diubah.

## Hasil per folder

| Folder | Dokumen diperbarui | Tautan lokal baru/diperbaiki | Rincian |
|---|---:|---:|---|
| 1 Workflow | 5 | 28 | [1-tautan.csv](1-tautan.csv) |
| 2 Roles | 45 | 103 | [2-tautan.csv](2-tautan.csv) |
| 3 Skills | 313 | 3378 | [3-tautan.csv](3-tautan.csv) |
| 4 Knowledge Bank | 72 | 1647 | [4-tautan.csv](4-tautan.csv) |
| 5 Integration | 3 | 13 | [5-tautan.csv](5-tautan.csv) |
| 6 Database | 1 | 2 | [6-tautan.csv](6-tautan.csv) |
| 7 Tools | 1 | 743 | [7-tautan.csv](7-tautan.csv) |

Jumlah dokumen pada tabel adalah keadaan akhir, termasuk koreksi manual. Jumlah tautan dihitung dari selisih kemunculan tujuan tautan sebelum dan sesudah. CSV per folder mencatat konversi otomatis; koreksi tambahan terdapat pada [rujukan lama yang diperbaiki](rujukan-lama-diperbaiki.csv). Seluruh tautan tambahan dan targetnya tercantum pada [daftar terverifikasi](tautan-lokal-terverifikasi.csv).

## Cara menggunakan hasilnya

1. Mulai dari [HARNESS.md](../../HARNESS.md). Panduan ini menjadi pintu masuk bersama.
2. Gunakan [library.json](../../library.json) untuk menemukan koleksi dan memetakan alias lama.
3. Jika membaca path Windows atau rujukan `ekas/` dan `roles/`, jalankan resolver baca-saja [tools/library.py](../../tools/library.py).
4. Jalankan `python3 tools/library.py check` untuk memeriksa seluruh hyperlink Markdown dalam manifest, alias, cakupan berkas, ukuran, dan SHA-256.

Semua tautan navigasi baru relatif terhadap dokumen pemiliknya; path pada peta konfigurasi relatif terhadap root clone. URL sumber publik dan riwayat commit tetap eksternal. Endpoint localhost, IP privat, dan path host pada catatan lama tetap menjadi konteks sumber, bukan konfigurasi layanan perangkat pembaca.

## Sumber yang belum disertakan

| Indeks | Keadaan | Jumlah |
|---|---|---:|
| Unit pengetahuan | Path digest menunjuk dokumen yang tidak tersedia di clone | 557 |
| Unit pengetahuan | Kolom rujukan digest kosong pada sumber | 1001 |
| Kemampuan | File dan jangkar baris tersedia secara lokal | 372 |

Keadaan 1.558 entri unit di atas merupakan keterbatasan bahan sumber. Audit ini tidak menggantinya dengan dokumen lain yang berbeda, dan tidak mengubah nilai CSV. Rincian per entri terdapat pada [status sumber indeks](status-sumber-indeks.csv). File lain yang disebut dalam kode atau kutipan historis juga dapat membutuhkan lingkungan sumber; resolver mengembalikan status yang sesuai.

Empat hyperlink BIM diperbaiki ke subfolder references yang benar. Delapan hyperlink ke content-repurposer dan hashtag-analyzer diganti menjadi keterangan bahwa skill belum disertakan, sambil mempertahankan alamat rujukan aslinya. Bukti jangkar kemampuan terdapat pada [jangkar-kemampuan.csv](jangkar-kemampuan.csv).

## Verifikasi

- Uji resolver: 16 pengujian, seluruhnya lulus. Kasus mencakup path relatif, Unicode dan spasi, alias Windows, cwd berbeda, relokasi, fragmen, sumber hilang, alias ambigu, contoh kode, dan cakupan manifest.
- Pemeriksaan berkas: seluruh 1.546 berkas kode/data/aset sumber non-Markdown tetap identik dengan baseline. Metadata, blok kode, URL eksternal sumber, dan isi kode sebaris yang dipertahankan diperiksa. Delapan keterangan sumber hilang menambahkan path aslinya sebagai kode sebaris secara terkontrol.
- Pemeriksaan navigasi: tidak ada hyperlink lokal rusak pada cakupan Markdown yang diperiksa. Cakupan dan hash manifest lulus.
- Clone lengkap diuji setelah dipindahkan ke direktori dengan spasi dan Unicode serta dipanggil dari cwd lain. Hasil mesin tercatat pada [verifikasi.json](verifikasi.json).

Ringkasan perbandingan dengan baseline: [audit-rujukan.json](audit-rujukan.json). Daftar ukuran dan hash dokumen yang berubah: [berkas-diubah.csv](berkas-diubah.csv).

Kode dan data operasi lama dipertahankan sebagai sumber. Penyesuaian ini membuat penelusuran pustaka portabel; ini tidak menyatakan bahwa seluruh skrip arsip dapat dijalankan lintas sistem operasi. Uji layanan host, pemeriksaan fakta eksternal, dan pemasangan skill ke konfigurasi harness tidak dijalankan.

Laporan audit bahasa di folder sebelah adalah catatan historis pada commit `6e31e8b`; hash di dalamnya mendahului perubahan rujukan ini. Gunakan pemeriksaan library.py untuk keadaan clone saat ini. Riwayat perubahan dapat ditinjau pada [commit repositori](https://github.com/sixer0/AI-Knowledge-Library/commits/main/).
