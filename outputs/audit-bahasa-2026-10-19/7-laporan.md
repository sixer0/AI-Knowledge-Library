# Audit bahasa: 7 Tools

Tanggal: 19 Oktober 2026. Pemeriksaan dan penyuntingan dilakukan oleh Codex secara berurutan.

Indeks menjelaskan fungsi kedua kelompok skrip dan arti watchdog. Bahasa pada contoh prompt tugas dirapikan: istilah campuran diganti dengan padanan yang jelas, tanpa mengubah instruksi operasional, kewenangan, nama profil, atau model yang tercatat. Kode skrip, konfigurasi, laporan mesin, dan log tetap utuh.

| Cakupan | Jumlah |
|---|---:|
| Berkas asli diinventarisasi | 744 |
| Berkas diperbarui, termasuk indeks | 12 |
| Berkas tetap utuh | 732 |

| Sebelum | Sesudah |
|---|---|
| orkestrasi migrasi knowledge GSP | koordinasi migrasi pengetahuan GSP |
| gatekeeper Information Library | penanggung jawab kurasi Information Library |
| Baca dulu runbook dan standarmu | Baca dulu panduan kerja dan standarmu |
| cek dedup vs wiki | periksa duplikasi terhadap wiki |

Verifikasi: **LULUS**. Tidak ada berkas asli yang hilang. Metadata YAML, blok kode, kode sebaris, dan URL pada dokumen yang disunting tetap utuh. Berkas kode, konfigurasi, dan data tetap sama dengan versi awal. Indeks diperbarui mengikuti ukuran berkas; ukuran pada manifest dihitung ulang.

Seluruh 744 berkas diinventarisasi. Prosa pada indeks dan contoh prompt TXT dibaca sebagai petunjuk; perintah, path, jumlah, persetujuan historis, dan nama model dipertahankan. Berkas Python, shell, JavaScript, JSON, PID, serta laporan keluaran mesin tidak ditulis ulang. Skrip tidak dijalankan: sebagian mengatur layanan, mengirim tugas, atau menulis sistem host asal. Audit ini tidak menyatakan seluruh skrip berfungsi pada Mac atau siap dijalankan sebagai paket mandiri.

Rincian berkas dan sidik SHA-256: [7-perubahan.csv](7-perubahan.csv). Perbandingan kalimat lengkap tersedia pada commit folder ini. Versi sebelum penyuntingan ada pada commit awal `8785880`.
