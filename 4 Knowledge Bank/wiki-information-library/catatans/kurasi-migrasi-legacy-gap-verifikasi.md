---
id: kurasi-migrasi-legacy-gap-verifikasi
type: catatan
title: GAP Kurasi Migrasi Legacy — 7 item butuh OCR / verifikasi manusia
status: active
sumber: docs/2026_08_24_kurasi_vault_migrasi_legacy/report.md
halaman: "Bagian: GAP (butuh OCR/verifikasi manusia), item 1–7"
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kurasi-migrasi-legacy
domain: library
writer: gsp-librarian
tags: [kurasi, migrasi, legacy, gap, verifikasi, ocr, backlog, vault]
links: [kurasi-migrasi-legacy-keputusan-gate, arsenal-ids-migrasi-gap-ekstraksi-visual, gap-verifikasi-vision-wave3-5-item]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Ketujuh item GAP cocok verbatim dengan report.md bagian GAP item 1-7 (KEMHAN 35 hal scan; RANSUS BIN 20 hal scan; ADINT 13,6 MB image-based; deck Arsenal 20 slide 0 text run + SLIDE 7 hilang dan SLDIE 14 salah eja; RAB dua iterasi; CIDEX2024 teks penuh hanya hal 1-3; mirror IL localhost:9011 tidak merespons). Catatan penutup '46 menunggu_persetujuan + 2 dipromosikan' cocok baris 112 report. Target links (gap-verifikasi-vision-wave3-5-item, kurasi-migrasi-legacy-keputusan-gate, arsenal-ids-migrasi-gap-ekstraksi-visual) ada di vault. YAML lulus, title==H1, satu baris status, grouping library sesuai isi (objek proses kurasi internal). || Rekomendasi: Tidak ada perubahan isi. Saat promosi beri penanda kadaluarsa pada item 7 karena bridge IL kini aktif (terpantau pada gelombang G0/G1), supaya backlog tidak menyesatkan pembaca berikutnya. || Riwayat: Verdict awal (gsp-custodian, 2026-08-25): terverifikasi — DICABUT oleh verifikasi independen Wave B (2026-08-25) karena bukti tidak mendukung. Koreksi Wave B-revisi 2026-08-25 oleh gsp-librarian: . Status kembali usulan untuk verifikasi ulang custodian."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: catatans/kurasi-migrasi-legacy-gap-verifikasi.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 batch M1a: verdict custodian terverifikasi (C-M1a-verdict.md), cek I5 lulus, non-sensitif non-dosir"
---

# GAP Kurasi Migrasi Legacy — 7 item butuh OCR / verifikasi manusia

## Ringkasan
Laporan kurasi 2026-08-24 mencatat 7 gap yang menghalangi kurasi lebih lanjut
(tanpa OCR/vision atau verifikasi manusia). Item ini adalah backlog verifikasi.
[sumber: report.md, bagian GAP]

## Daftar gap
1. `KEMHAN/v1.1 Pengadaan Ransus Pengamanan Informasi.pdf` — 35 hal scan tanpa text layer (butuh OCR).
2. `RANSUS/RANSUS BIN 11 AGUSTUS 2026 V1.pdf` — 20 hal scan tanpa text layer (butuh OCR).
3. `ADINT/GSP Technical Report ADINT.pdf` (13,6 MB) — image-based (butuh OCR).
4. Deck gambar `Arsenal IDS Barat Timur.pptx` (20 slide, 0 text run); PNG slide Arsenal
   Tahap 4 (SLIDE 7 hilang; SLDIE 14 salah eja) — butuh vision/OCR.
5. Angka final RAB ARSENAL (dua iterasi: Rp 24.945.404.550 vs Rp 24.750.028.288) —
   verifikasi manusia/owner dokumen.
6. `China Expo - Toni Research/4.4_CIDEX2024_会刊.pdf` — teks penuh hanya hal. 1–3;
   angka vendor di luar sheet xlsx dari katalog terindeks.
7. Mirror IL API (localhost:9011) tidak merespons di env kurasi — bridge mirror
   diverifikasi saat layanan aktif.
[sumber: report.md, bagian GAP, item 1–7]

## Catatan
Gap 1–4 butuh OCR/vision; gap 5 butuh keputusan manusia/owner; gap 6 butuh sumber
katalog terindeks; gap 7 adalah kendala lingkungan (bukan konten). Setelah gap
tertutup, objek vault terkait (46 menunggu_persetujuan + 2 dipromosikan) dapat
dikurasi lanjut / diverifikasi untuk promote.
