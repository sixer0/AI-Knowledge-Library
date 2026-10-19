# Audit bahasa: 6 Database

Tanggal: 19 Oktober 2026. Pemeriksaan dan penyuntingan dilakukan oleh Codex secara berurutan.

Keterangan indeks diperjelas agar pembaca memahami fungsi skema dan snapshot. Istilah snapshot dijelaskan sebagai salinan keadaan basis data pada waktu tertentu. Skema Prisma dan basis data tetap sama dengan versi awal.

| Cakupan | Jumlah |
|---|---:|
| Berkas asli diinventarisasi | 3 |
| Berkas diperbarui, termasuk indeks | 1 |
| Berkas tetap utuh | 2 |

| Sebelum | Sesudah |
|---|---|
| snapshot hangat / file hidup | salinan keadaan basis data saat layanan berjalan / data layanan pada host asal |

Verifikasi: **LULUS**. Tidak ada berkas asli yang hilang. Metadata YAML, blok kode, kode sebaris, dan URL pada dokumen yang disunting tetap utuh. Berkas non-Markdown tetap sama dengan versi awal. Indeks diperbarui mengikuti ukuran berkas; ukuran pada manifest dihitung ulang.

Ketiga berkas diinventarisasi. Skema diperiksa sebagai struktur teknis; basis data dibandingkan melalui SHA-256. Isi tabel, nama kolom, komentar skema, dan data historis tidak dinaturalisasi. Tidak menjalankan migrasi, membuka koneksi produksi, atau menguji kelayakan pemulihan basis data. Tidak ada klaim pemeriksaan editorial setiap nilai teks di dalam snapshot.

Rincian berkas dan sidik SHA-256: [6-perubahan.csv](6-perubahan.csv). Perbandingan kalimat lengkap tersedia pada commit folder ini. Versi sebelum penyuntingan ada pada commit awal `8785880`.
