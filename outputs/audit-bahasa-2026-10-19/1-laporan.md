# Audit bahasa: 1 Workflow

Tanggal: 19 Oktober 2026. Pemeriksaan dan penyuntingan dilakukan oleh Codex secara berurutan.

Bahasa prosedur diperjelas, istilah campuran diganti dengan padanan yang lazim, dan paragraf kebijakan yang padat dipisahkan. Penjelasan controller, worker, dispatch, registry, attest, provenans, dan snapshot ditambahkan pada berkas kebijakan. Jadwal, batas 50 operasi, kewajiban, serta larangan tetap berlaku seperti pada sumber.

| Cakupan | Jumlah |
|---|---:|
| Berkas asli diinventarisasi | 9 |
| Berkas diperbarui, termasuk indeks | 7 |
| Berkas tetap utuh | 2 |

| Sebelum | Sesudah |
|---|---|
| usable dan trackable | dapat dibaca manusia, diproses mesin, dan dilacak riwayatnya |
| mutasi (move/rename/edit metadata) | perubahan (pemindahan, penggantian nama, atau penyuntingan metadata) |
| folder cryptic | folder yang sulit dikenali |
| skrip sekali-pakai tanpa alamat; lahir langsung | skrip sekali-pakai di lokasi sembarang; dibuat langsung |

Verifikasi: **LULUS**. Tidak ada berkas asli yang hilang. Metadata YAML, blok kode, kode sebaris, dan URL pada dokumen yang disunting tetap utuh. Berkas non-Markdown tetap sama dengan versi awal. Indeks diperbarui mengikuti ukuran berkas; ukuran pada manifest dihitung ulang.

Pemeriksaan mencakup seluruh tujuh dokumen Markdown dan inventaris dua JSON. JSON cron dipertahankan utuh karena merupakan definisi tugas yang dapat dieksekusi. Prosedur yang menyebut host Windows dan API lokal adalah materi pustaka; prosedur tersebut tidak dijalankan dalam audit ini. Perbedaan versi pada judul dan metadata standar skrip sudah ada sebelum audit, dan tidak diubah sebagai keputusan kebijakan baru.

Rincian berkas dan sidik SHA-256: [1-perubahan.csv](1-perubahan.csv). Perbandingan kalimat lengkap tersedia pada commit folder ini. Versi sebelum penyuntingan ada pada commit awal `8785880`.
