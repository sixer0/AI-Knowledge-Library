---
id: kurasi-migrasi-legacy-rekonsiliasi-angka
type: catatan
title: Rekonsiliasi Angka Kurasi Migrasi Legacy — 7 pasang angka lintas-perkara (jangan dicampur)
status: active
sumber: docs/2026_08_24_kurasi_vault_migrasi_legacy/report.md
halaman: "Bagian: Rekonsiliasi angka yang di-flag worker (item 1–7)"
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: kurasi-migrasi-legacy
domain: library
writer: gsp-librarian
tags: [kurasi, migrasi, legacy, rekonsiliasi, angka, provenans, vault]
links: [kurasi-migrasi-legacy-keputusan-gate, arsenal-tahap4-konflik-rab-dua-versi, china-expo-toni-vendor-master-593, cdex-inkonsistensi-angka-deliverable]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, batch M1b). Alasan: ketujuh pasang angka diverifikasi verbatim terhadap report.md bagian \"Rekonsiliasi angka yang di-flag worker\": 772/1.417/859; USD9,8-37,2jt vs USD14,2-52,8jt (most likely 18-28jt); 161 vendor/62 produk vs 1.360/337; Rp 24.945.404.550 vs Rp 24.750.028.288; 298 vs 203 (32+142+14+3+0+12); 594 vs 593 (Security China 563 + CIDEX 30; 578/11/4); Do Not Contract narasi 14 vs daftar 15 (12 CRITICAL + 3 HIGH). Keempat target links ada di vault. YAML kelas-I5 lulus, title==H1, satu baris status, grouping library sesuai isi. kelas_bukti sintesis jujur: objek melaporkan hasil rekonsiliasi report.md, bukan klaim verifikasi primer ulang. Dedup bersih: tidak ada objek/wiki lain dengan cakupan lintas-perkara yang sama. || Rekomendasi: tidak ada perubahan wajib sebelum promosi. Pertahankan batas interpretasi saat promosi: angka bersumber laporan kurasi 2026-08-24 (snapshot); sumber primer hulu (xlsx/docx/json) tidak dibuka ulang oleh objek ini maupun verifikasinya. Riwayat: catatan_verifikasi lama (verdict awal 2026-08-25 dicabut verifikasi independen Wave B, lalu dikoreksi gsp-librarian 2026-08-25 dan status dikembalikan ke usulan) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: catatans/kurasi-migrasi-legacy-rekonsiliasi-angka.md
catatan_keputusan: "dipromosikan: batch M1b paruh B terverifikasi custodian (C-M1b-verdict.md)"
---

# Rekonsiliasi Angka Kurasi Migrasi Legacy — 7 pasang angka lintas-perkara (jangan dicampur)

## Ringkasan
Laporan kurasi 2026-08-24 merekonsiliasi 7 kelompok angka yang sempat di-flag
worker. Prinsip: setiap angka sah dalam konteksnya sendiri; JANGAN dicampur.
[sumber: report.md, bagian "Rekonsiliasi angka yang di-flag worker"]

## Item 1 — ADINT 772 vs 1.417 vs 859 (tiga angka sah, konteks berbeda)
- 772 = vendor unik dianalisis (12h_master_document Bab 1; saturasi >95% vs universe 850–950) — terverifikasi.
- 1.417 = total_vendors LIBRARY_INDEX frontmatter (termasuk grup bulk Cat4) — terverifikasi.
- 859 = rows `01_master_vendor_list.xlsx` (enrichment workstream, 6 kolom) — terverifikasi (01_translated.md).
[sumber: report.md, Rekonsiliasi #1]

## Item 2 — Biaya ADINT USD9,8–37,2jt vs USD14,2–52,8jt (dua sumber beda)
- USD9,8–37,2jt = ch8_strategic_recs §8.1 (terverifikasi).
- USD14,2–52,8jt (most likely 18–28jt) = ADINT_Executive_Briefing §2.5 (terverifikasi docx).
Keduanya sah; tidak ada angka kanonik tanpa keputusan manajemen.
[sumber: report.md, Rekonsiliasi #2]

## Item 3 — Vendor China 161 vs 1.360 (inkonsistensi antar deliverable)
- 161 vendor / 62 produk = report.md v1.0 (verdict CAUTION; 17 orphan produk) — terverifikasi.
- 1.360 vendor / 337 produk = china_defence_expo_report_v2.md v2.1 rebuild (70 shortlist) — terverifikasi.
Keputusan: v2.1 lebih representatif, tapi belum diklaim kanonik tanpa verifikasi ulang 12 file korpus regional.
[sumber: report.md, Rekonsiliasi #3]

## Item 4 — Arsenal RAB Rp 24.945.404.550 vs Rp 24.750.028.288 (dua iterasi RAB)
- Rp 24.945.404.550 = proposal GSP/IDSBT-PRP/2026-01 + design system master + RAB xlsx v2 (terverifikasi).
- Rp 24.750.028.288 = JSON 033/GSP/KT/VIII/2026 Rev B, 43 mata pembayaran, konsisten internal (terverifikasi).
Angka final menunggu verifikasi manusia/owner dokumen.
[sumber: report.md, Rekonsiliasi #4]

## Item 5 — FORENSIC 298 vs 203 (dua angka beda konteks, JANGAN dicampur)
- 298 = pattern-match analyze_forensic.py (analysis_summary.txt) — terverifikasi.
- 203 = entri enumerasi vendor_master_database.json.vendors_by_region (32+142+14+3+0+12) — terverifikasi.
[sumber: report.md, Rekonsiliasi #5]

## Item 6 — China Expo 594 vs 593 (koreksi minor)
Sheet Vendor Master = 593 record data (Security China 563 + CIDEX 30; 578 tahun 2024,
11 tahun 2023, 4 tahun 2022), bukan 594. Selisih 1 baris.
Tercatat di catatan_keputusan objek `china-expo-toni-vendor-master-593` (id kanonik vault
saat ini; nama `china-expo-vendor-master-594` dipakai laporan lama).
[sumber: report.md, Rekonsiliasi #6]

## Item 7 — Do Not Contract ADINT "14" (disparitas internal dokumen)
Narasi dokumen menyebut 14, daftar nama = 15 (12 CRITICAL + 3 HIGH).
Disparitas internal dokumen; dicatat jujur di objek, verifikasi manusia disarankan.
[sumber: report.md, Rekonsiliasi #7]

## Status
Semua angka di atas telah diverifikasi di sumber nyata saat kurasi (spot-check
grep/PDF/XLSX/DOCX/JSON); tidak ada yang dikarang. Objek terkait sudah ada di
vault per perkara (lihat links).
