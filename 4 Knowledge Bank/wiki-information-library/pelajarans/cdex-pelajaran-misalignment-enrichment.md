---
id: cdex-pelajaran-misalignment-enrichment
type: pelajaran
title: "China Defence Expo — pelajaran: enrichment misalignment (Website/Email/Source_URL salah kolom, skor 18/100)"
status: active
sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/01_verification_report.md
halaman: Section 3, 7, 9
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: china-defence-expo-crawler
tags: [china, pelajaran, data-quality, misalignment, xlsx, defense-intel]
penulis: gsp-librarian
diajukan: 2026-08-25
created: 2026-08-25
writer: gsp-librarian
domain: defense-intel
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/china-defence-expo-crawler/2026-08-25_cdex-pelajaran-misalignment-enrichment.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# China Defence Expo — pelajaran: enrichment misalignment (Website/Email/Source_URL salah kolom, skor 18/100)

Pelajaran dari verifikasi Wave 7 (01_verification_report.md): langkah merge XLSX menaruh data enrichment DI KOLOM SALAH:
- Kolom Website diisi URL artikel berita (bukan situs vendor)
- Kolom Contact_Email diisi deskripsi sumber (bukan email)
- Kolom Source_URL diisi label confidence (bukan URL)

Akar masalah: batch files (22 website/email + 22 produk, 602 vendor) valid tetapi tidak di-merge ke kolom yang benar. 3 inkonsistensi kritis + 4 medium + 2 low; skor kualitas 18/100 FAIL.

Rekomendasi: mapping ulang batch -> kolom (Website->Website, Email->Contact_Email, Source->Source_URL, Confidence->confidence_score), buat batch 13 vendor hilang, hitung ulang composite score. Pelajaran: verifikasi tipe data per kolom SEBELUM klaim production-ready.

[Sumber: legacy-archive/china-defence-expo-crawler-20260824T085128Z-1-001/china-defence-expo-crawler/outputs/01_verification_report.md]
