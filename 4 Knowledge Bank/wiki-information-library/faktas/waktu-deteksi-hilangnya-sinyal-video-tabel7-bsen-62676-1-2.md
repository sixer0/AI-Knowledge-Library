---
id: waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2
type: fakta
title: Waktu deteksi hilangnya sinyal video per security grade — Tabel 7 BS EN 62676-1-2:2014
sumber: docs/2026-08-24_fleet_test_data_collector_ekas/collection_report.md; ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md; ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md
halaman: BS EN 62676-1-2:2014 Tabel 7 PDF 34, performance class PDF 29 (KATALOG-RUMUS baris 470-477; RANTAI-JAMINAN baris 95)
tanggal_akses: 2026-08-24
kelas_bukti: sekunder
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: engineering
writer: gsp-librarian
tags: [engineering, security-cctv, video-surveillance, bs-en-62676, hilangnya-sinyal, security-grade]
penulis: gsp-librarian
diajukan: 2026-08-25
riwayat-catatan-verifikasi: "Verdict awal (gsp-custodian, 2026-08-25): terverifikasi — DICABUT oleh verifikasi independen Wave B (2026-08-25) karena bukti tidak mendukung. Koreksi Wave B-revisi 2026-08-25 oleh gsp-librarian: path sumber tak-eksis dibuang, sisanya dipertahankan. Status kembali usulan untuk verifikasi ulang custodian."
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Verdict: terverifikasi. || Alasan: challenge penuh 7 dimensi lulus. Anti-karangan: 3 RAW dibuka - ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md baris 470-477 (Tabel 7: deteksi 8/4/4/2 s; durasi tidak tersedia 180/180/30/30 s; catatan performance class independen PDF 29 - semua cocok; urutan baris tabel objek ditukar dari sumber tetapi nilai per kolom grade identik), ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md baris 95 (konfirmasi R2 PDF 34), dan docs/2026-08-24_fleet_test_data_collector_ekas/collection_report.md fakta #3 (grade 1-4 dan durasi cocok). Dedup: tidak ada entri wiki serupa. Metadata: YAML aman, 1 status, title==H1. Grouping engineering/security-cctv sesuai. Sensitif tidak, dosir tidak. || Rekomendasi: siap dipromosikan. Opsional: samakan urutan baris tabel dengan sumber (deteksi dulu, durasi kemudian) agar pembaca PDF tidak tertukar."
status: active
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/waktu-deteksi-hilangnya-sinyal-video-tabel7-bsen-62676-1-2.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 L-B3: verdict custodian terverifikasi (C-B3-verdict.md), YAML kelas-I5 lulus, non-sensitif non-dosir"
known-defect: ya
known-defect-pada: 2026-09-23
known-defect-oleh: gsp-librarian
known-defect-rujuk: catatans/vss-korpus-ekas-0923.md#batas-angka-tabel-7 (misi VSSKB-0923)
updated: 2026-09-23
---

# Waktu deteksi hilangnya sinyal video per security grade — Tabel 7 BS EN 62676-1-2:2014

Tabel 7 BS EN 62676-1-2:2014 — pemantauan interkoneksi video surveillance [R2]:

| Persyaratan | Grade 1 | Grade 2 | Grade 3 | Grade 4 |
|---|---|---|---|---|
| Maks. waktu deteksi hilangnya sinyal | 8 s | 4 s | 4 s | 2 s |
| Maks. durasi perangkat tidak tersedia | 180 s | 180 s | 30 s | 30 s |

Performance class independen dari security grade (PDF 29) — jangan dicampur dalam spesifikasi.

Provenans: ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md baris 470–477 (bagian 13.2) — R2 — BS EN 62676-1-2:2014, Tabel 7, PDF 34; dikonfirmasi di ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md baris 95 (R2 — BS EN 62676-1-2 PDF 34). Kelas bukti: sekunder (lapisan teks EKAS; standar primer di PDF sumber).

## CATATAN DEFECT (23-09, misi VSSKB-0923)

Pemetaan per-grade dalam bentuk EMPAT nilai pada tabel di atas (waktu deteksi 8/4/4/2 detik;
durasi tidak tersedia 180/180/30/30 detik) BELUM TERKONFIRMASI terhadap geometri PDF primer di
rak. Ukur gsp-custodian 2026-09-23 atas PDF 34 BS EN 62676-1-2:2014: `pdftotext -layout` dan
`-table` hanya merender TIGA nilai deteksi dan DUA nilai durasi; geometri sel pymupdf (batas
kolom x = 375,8 / 403,8 / 439,3 / 481,7 / 524,2 pt; header grade 1-4 terpusat di
391/423/462/504) menempatkan 8 s, 4 s, 2 s di kolom grade 2, 3, 4 dan 180 s, 30 s di kolom
grade 3, 4, sementara sel grade 1 baris kedua dan sel grade 2 baris durasi hanya berisi satu
karakter spasi (nol glyph, tanpa anotasi, widget, maupun gambar).

Lapisan teks hulu yang menjadi sumber entri ini membawa DUA bentuk angka untuk tabel yang sama:
bentuk dua nilai 8/4/2 detik di `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md:95`
dan `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md:58`, versus bentuk empat nilai
8/4/4/2 detik di `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:45-48` dan
`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md:470-477`. Akar temuan ada di kontradiksi hulu
ini, bukan pada angka itu sendiri.

Rujukan analisis lengkap: seksi BATAS Bagian 4 objek master `catatans/vss-korpus-ekas-0923.md`
(vault `vsskb-0923/2026-09-23_vss-korpus-ekas-0923.md`, misi VSSKB-0923).

Pemakaian: entri ini TIDAK boleh dipakai sebagai ambang uji serah terima sampai rekonsiliasi
dengan publikasi resmi BSI/IEC dilakukan oleh manusia. Status entri tetap `active` dengan
penanda defect (SPK-002 butir 7: temuan pasca-terbit ditandai, ditraceroot, gerbang ditambal).
Body faktual di atas blok ini tidak diubah.
