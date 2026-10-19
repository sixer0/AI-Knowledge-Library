---
id: pola-standard-terms-vendor-osint
type: pelajaran
title: Pola Standard Terms Vendor OSINT - Checklist Review Kontrak Vendor SaaS/OSINT
status: active
sumber: docs/2026-09-09-ixa0909-library-curation/source/W1-risk-analysis.md
halaman: seksi A.2, B (R-01..R-20), C, D (I-01..I-09)
tanggal_akses: 2026-09-09
kelas_bukti: sintesis
sensitif: tidak
perkara: ixa-0909-vendor-osint
tags: [kontrak, vendor, osint, saas, checklist, review, negosiasi]
links: [docs/2026-09-09-ixa0909-library-curation/source/LAPORAN-AKHIR.md, docs/2026-09-09-ixa0909-library-curation/source/VERIFIKASI.md]
penulis: gsp-librarian
diajukan: 2026-09-09
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-09
catatan_verifikasi: "Recheck 2026-09-09: verdict terverifikasi - kedua perbaikan librarian teruji cocok terhadap register-risiko.csv dan W1-risk-analysis.md: (1) seksi 4 kini memetakan butir 1=R-03 skor 16, 2=R-02 skor 20, 3=R-06 skor 15, 6=R-01 skor 20 ke band KRITIS dan butir 4=R-08, 5=R-07, 7=R-12 (skor 12) ke band TINGGI dengan prioritas P2 persis kolom prioritas CSV; (2) frasa kini 'register klausul hilang M-01 sampai M-14' sesuai seksi C W1 yang berhenti di M-14 (definisi-operasional). Tidak ada klaim baru yang menyimpang (spot-check pasal/ID R, I, M lain tetap cocok); mekanik lolos: yaml.safe_load, key unik, satu baris status, title==H1, nol U+2014/U+2013/U+00B7. Body tidak diubah. Riwayat verdict awal: Verdict: perlu_revisi. Alasan: klaim seksi 4 'butir 1, 3, 4, 7 menghasilkan band KRITIS' tidak cocok dengan register sumber; pemetaan butir ke W1 tabel A.2 / LAPORAN-AKHIR Tabel 5 memberi KRITIS pada butir 1 (R-03 skor 16), 2 (R-02 skor 20), 3 (R-06 skor 15), 6 (R-01 skor 20), sedangkan butir 4 (R-08 skor 12 TINGGI; R-13 skor 9 SEDANG) dan butir 7 (R-12 skor 12 TINGGI; R-15 skor 9 SEDANG) tidak mencapai KRITIS. Temuan minor: frasa 'daftar mitigasi M-01 sampai M-13' menamai register klausul hilang seksi C sebagai daftar mitigasi, dan rentang berhenti di M-13 padahal sumber memuat M-14. Sisanya lolos: 8 pola inti + 4 perluasan terpetik ulang utuh di W1 (nomor pasal dan ID R/I/M cocok), frontmatter lolos yaml.safe_load tanpa nilai terpotong, title==H1, nol U+2014/U+2013/U+00B7, tanpa nama vendor dan tanpa data sensitif GSP, dedup bersih vs wiki (784 entri) dan vault lain. Rekomendasi: ganti kalimat seksi 4 menjadi 'butir 1, 2, 3, 6 menghasilkan band KRITIS (R-03, R-02, R-06, R-01); butir 4, 5, 7 di band TINGGI (R-08, R-07, R-12) dan tetap prioritas redline P2'; ganti 'daftar mitigasi M-01 sampai M-13' menjadi 'register klausul hilang M-01 sampai M-14'."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-09
dipromosikan-ke: pelajarans/pola-standard-terms-vendor-osint.md
catatan_keputusan: "dipromosikan: kurasi S2 IXA-0909: pola generik tanpa nama entitas, custodian terverifikasi (recheck), non-sensitif"
---

# Pola Standard Terms Vendor OSINT - Checklist Review Kontrak Vendor SaaS/OSINT

## 1. Maksud

Checklist generik untuk review pra-tanda-tangan kontrak vendor SaaS/OSINT asing, dipakai ulang oleh reviewer dan procurement GSP. Bukan salin-tempel klausul dan bukan nasihat hukum. Sumber pola: kontrak satu vendor OSINT yang dianalisis tuntas dalam misi IXA-0909 (berkas rujukan di frontmatter); pola dipilih karena berulang dan struktural, tanpa menyebut nama vendor.

## 2. Daftar periksa (8 pola inti)

1. Modifikasi sepihak. Cari klausul perubahan syarat atas "sole discretion" penyedia dengan notifikasi minimal (di sumber: 7 hari, Pasal 35). Bahaya: menimpa kepastian klausul komersial lain termasuk tarif, bertentangan dengan klausul notifikasi tarif 30 hari (temuan I-01). Uji: adakah hak terminasi khusus saat perubahan, dan dokumen mana yang prevail.
2. Plafon liabilitas satu arah. Cap liabilitas penyedia sebesar fee yang dibayar (Pasal 25) plus pengecualian total kerugian tidak langsung, tanpa cermin batas liabilitas untuk sisi Client. Uji: adakah plafon dua arah dan carve-out untuk pelanggaran data/kerahasiaan.
3. Terminasi sepihak penyedia tanpa pemberitahuan dengan grounds luas, termasuk istilah tak terdefinisi (di sumber: "fair-use" Pasal 33(g), "the User" Pasal 33(c), "serious violation" Pasal 34). Uji: definisi setiap grounds dan simetri hak keluar (temuan I-03, I-07).
4. Fee non-refundable dibayar penuh di muka (Pasal 18 dan 29) digabung restriksi akses cepat karena tunggakan kecil (7 hari, Pasal 17). Kombinasi ini menghapus leverage bayar-terhadap-kinerja (temuan I-04).
5. SLA persentase rendah dengan remedy hanya kredit durasi (di sumber: 95 persen, Pasal 20 dan 21), pengecualian maintenance dan pihak ketiga tanpa batas, tanpa audit atau laporan ketersediaan, serta kontradiksi dengan klausul "AS IS" (temuan I-02). Uji: remedy finansial nyata dan definisi pengukuran uptime.
6. Forum sengketa negara penyedia dengan arbiter tunggal ditunjuk institusi setempat (di sumber Pasal 36: Arbitration Court Praha, satu arbiter dipilih presiden pengadilan, hukum Ceko, bahasa Inggris). Efek: hak gugat lintas negara menjadi tidak ekonomis. Uji: biaya forum relatif terhadap nilai kontrak.
7. Klausul pajak yang memindahkan withholding ke Client dan melarang pemotongan dari fee (Pasal 13), plus rezim PPN yang dirancang untuk pasar EU dengan penentuan negara pajak lewat GeoIP (Pasal 10 sampai 12). Jebakan gross-up bagi pembayar Indonesia. Uji: siapa penanggung beban pajak efektif dan bukti potong yang masih dapat dipakai di Indonesia.
8. Ketiadaan sistematis klausul pelindung: DPA/SCC, kerahasiaan timbal balik, indemnity konten/IP, breach notification, portabilitas data keluar, entire agreement/hierarchy dokumen (temuan seksi C sumber; register klausul hilang M-01 sampai M-14). Checklist negatif ini sering lebih menentukan daripada isi klausul yang ada.

## 3. Perluasan opsional (pola sekunder pada sumber yang sama)

- Ikatan berlapis: acceptance elektronik saat sign-up mengikat perusahaan pada T&C online yang dapat berubah (Pasal 3(ii) jo. Pasal 35; temuan R-14, I-05). Mitigasi: pendaftaran akun hanya lewat procurement dengan arsip versi terms tertanggal.
- Kenaikan tarif sepihak dengan notifikasi pendek (Pasal 15; R-04).
- Dukungan teknis hanya "within 7 days" (Pasal 26; R-18) dan bebas tanggung jawab atas akurasi informasi serta keputusan yang diambil darinya (Pasal 24; R-05).
- Hak pakai data pencarian anonim untuk improve tanpa definisi anonymization (Pasal 22; R-19, I-08).

## 4. Cara pakai

Jalankan checklist saat intake vendor SaaS/OSINT baru. Setiap butir yang gagal diberi skor dampak x kemungkinan dengan rubrik GSP (anchor operasional per level; band KRITIS/TINGGI/SEDANG/RENDAH). Pada sumber asal, butir 1, 2, 3, 6 menghasilkan band KRITIS (R-03, R-02, R-06, R-01); butir 4, 5, 7 di band TINGGI (R-08, R-07, R-12) dan tetap prioritas redline P2.

## 5. Batas klaim

Pola berasal dari analisis satu kontrak vendor OSINT per 2026-09-09; bukan jaminan vendor lain memakai klausul yang sama. Tidak ada klaim keabsahan hukum; interpretasi final adalah kewenangan penasihat hukum.
