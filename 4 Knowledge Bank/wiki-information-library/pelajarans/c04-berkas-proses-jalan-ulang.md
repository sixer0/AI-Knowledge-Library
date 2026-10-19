---
id: c04-berkas-proses-jalan-ulang
type: pelajaran
title: "C-04: berkas proses wajib disimpan agar dokumen dapat dijalankan ulang — 9 berkas disalin, SHA identik (diverifikasi di mesin pemesan)"
status: active
domain: digital
writer: gsp-librarian
created: 2026-08-25
sumber: legacy-archive/RISET SISTEM OPERASI AI GSP DAN KAM-20260824T085358Z-1-001/RISET SISTEM OPERASI AI GSP DAN KAM/GSP Kajian Riset AI Agentik [Pak Eka]/00 Indeks dan Serah Terima/Riwayat Revisi.md
halaman: Riwayat Revisi.md §3 C-04; Cara Menjalankan.md 007
tanggal_akses: 2026-08-10
kelas_bukti: primer
sensitif: tidak
perkara: riset-sistem-ai-gsp-kam
tags: [sistem-ai, c04, berkas-proses, jalan-ulang, reproduksibilitas]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/riset-sistem-ai-gsp-kam/2026-08-25_c04-berkas-proses-jalan-ulang.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# C-04: berkas proses wajib disimpan agar dokumen dapat dijalankan ulang — 9 berkas disalin, SHA identik (diverifikasi di mesin pemesan)

Cacat sedang yang ditutup 15 Agustus 2026: rantai perhitungan, register kuantitas, dan pembangun keluaran tidak tersimpan di mesin pemesan — tanpa berkas ini, 007 tidak dapat dijalankan ulang oleh siapa pun selain sesi pembuatnya.

Bukti (angka berujukan):
- Ditutup dengan menyalin sembilan berkas ke `06 Berkas Proses 007`: hitung.py, datumbind.py, Register Kuantitas.json, Tabel Pendukung.json, datumkajian.py, bangun.py, bukukerja.py, dasbor.py, Cara Menjalankan.md (Riwayat Revisi.md §3 C-04).
- Tiga jalur berkas yang semula ditanam mati diubah menjadi pencarian berurutan (berkas dapat dipindah tanpa disunting); datumbind.py disertakan berdampingan agar hitung.py berdiri sendiri tanpa skill DATUM (Riwayat Revisi.md §3 C-04).
- Verifikasi di mesin pemesan: rantai dijalankan langsung → 17 uji lulus, 191 besaran, SHA-256 register 1deb559c… identik dengan register Rev A (Riwayat Revisi.md §3 C-04).
- Pelajaran: dokumen yang tidak dapat dijalankan ulang adalah dokumen yang tidak dapat dipulihkan; 007 Rev B hanya menuntut perubahan beberapa baris masukan hitung.py (Riwayat Revisi.md §3 C-04; Cara Menjalankan.md §3).

Asumsi/tanda: primer (catatan verifikasi penyusun).
