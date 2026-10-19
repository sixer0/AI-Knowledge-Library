---
id: forensic-nfl-2026-aset-analisa
type: catatan
title: "Aset analisa folder FORENSIC: analyze_forensic.py + analysis_summary.txt (57.172 chars, 202 item, 298 manufacturer, D1–D7)"
status: active
sumber: legacy-archive/FORENSIC-20260824T085317Z-1-001/FORENSIC/analyze_forensic.py; legacy-archive/FORENSIC-20260824T085317Z-1-001/FORENSIC/analysis_summary.txt
halaman: analyze_forensic.py (seluruh berkas); analysis_summary.txt
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: forensic-nfl-2026
tags: [forensic, nfl, tier0, analisa, skrip, python, library]
links: [forensic-nfl-2026-vendor-master-298, forensic-nfl-2026-skala-program]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Dua file RAW dibuka. analysis_summary.txt cocok verbatim (57172 chars, Total items 202, Total manufacturers 298, Disciplines D1-D7). analyze_forensic.py mengonfirmasi klaim teknis: sheet BOQ_TIER0 header=None dengan header_row iloc[4] (baris 5) dan data iloc[5:] (dari baris 6), filter nomor item <=202, pemetaan disiplin D1-D7 sesuai label skrip. Klaim konsistensi 298 terverifikasi juga di GSP-NFL-2026_Vendor_Master_Report.docx ('298 vendor unik dari 202 item BOQ'). YAML lulus, title==H1, satu baris status, target links ada. || Rekomendasi: Presisikan frasa '~300 pola manufacturer' menjadi '298 manufacturer (analysis_summary.txt)' agar angka bulat tidak terbaca sebagai taksiran. Saat promosi tambahkan field domain=defense-intel (seluruh 18 sibling folder forensic-nfl-2026 kosong field domain - temuan sistemik dilaporkan terpisah). || Riwayat: Verdict awal (gsp-custodian, 2026-08-25): terverifikasi — DICABUT oleh verifikasi independen Wave B (2026-08-25) karena bukti tidak mendukung. Koreksi Wave B-revisi 2026-08-25 oleh gsp-librarian: sumber ditunjuk ke file kode konkret (teks terbaca). Status kembali usulan untuk verifikasi ulang custodian."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: catatans/forensic-nfl-2026-aset-analisa.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 batch M1a: verdict custodian terverifikasi (C-M1a-verdict.md), cek I5 lulus, non-sensitif non-dosir"
---

# Aset analisa folder FORENSIC: analyze_forensic.py + analysis_summary.txt (57.172 chars, 202 item, 298 manufacturer, D1–D7)

Aset analisa otomatis dalam folder FORENSIC — bukti alur kerja pengolahan korpus, bukan knowledge unit baru (data derivatif dari BOQ):
- analyze_forensic.py: skrip Python (pandas) membaca sheet BOQ_TIER0 (header baris 5, data dari baris 6), mengambil 202 item ber-nomor, mengekstrak ~300 pola manufacturer, mengelompokkan per disiplin D1–D7 dan blok fungsional; mencetak manufacturer unik, jumlah item per disiplin, dan teknologi per disiplin (mis. D1 Trace/Balistik/Dokumen & Sidik Jari, D2 Bahan Peledak & CBRNE, D3 Kimia & Toksikologi, D4 Biologi/DNA/Bio-threat, D5 Narkotika, D6 Digital/Siber/Kripto, D7 Infrastruktur/Mobile).
- analysis_summary.txt: "ANALYSIS COMPLETE - 57172 chars of raw data extracted; Total items: 202; Total manufacturers found: 298; Disciplines: D1-D7".

Catatan: angka "298 manufacturers" pada ringkasan ini konsisten dengan 298 vendor unik pada Vendor Master Report (perbedaan istilah manufacturer vs vendor). File letterhead GSP.docx dan logo GSP-01.png = aset branding perusahaan (bukan knowledge).
