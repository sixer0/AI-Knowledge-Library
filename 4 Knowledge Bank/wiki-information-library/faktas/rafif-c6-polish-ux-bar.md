---
id: rafif-c6-polish-ux-bar
type: fakta
title: Bar Polish dan UX Lintas Platform untuk Game Mobile (target sentuh, kontras, respons, warna, motion, juice)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict: terverifikasi || Alasan: 27/27 angka dan identitas tertelusur ke L3 P1..P7 + register U-10..U-22 (pin byte-identik); label kelas bukti per baris jujur dan lengkap (PRIMER platform/W3C, RISET-UX, SEKUNDER dengan gap G-6, PROV dengan bukti shell JS rung-8, KUALITATIF-IDENTITAS, RESMI-KOMUNITAS); ejaan kurva cubic-bezier(0.4.0,0.2.1) disalin persis dengan deklarasi kesetiaan ke sumber hulu; register terlarang X-6 (MDH) dan X-8 (Art of Screenshake) hanya muncul sebagai negasi/LARANGAN (sensus konteks: 0 pemakaian sebagai fakta); MDA primer Hunicke utuh; kelengkapan 17/17 butir proposa; dedup 0; YAML utuh. INFO non-pemblokir: ID G-5 dan X-8 tertulis di dalam kurung [R-4 ...] padahal hidupnya di matriks/proposa - prosa pada baris yang sama sudah menamai 'matriks sumber' dan 'proposa sumber' sehingga alamat pulih saat dibaca. || Rekomendasi: saat promosi rapikan pemisahan kurung (G-5 diberi tag [R-1 G-5]; X-8 menunjuk register proposa); tidak ada angka yang berubah dan vonis tidak bergantung pada rapian ini."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L3_quality_bar.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: ss.1 U-10..U-17,U-20..U-21; ss.2.3 P1..P7
tanggal_akses: 2026-10-11
kelas_bukti: primer
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [ux, polish, aksesibilitas, wcag, touch-target, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L3_quality_bar.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: faktas/rafif-c6-polish-ux-bar.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: gate biasa, custodian terverifikasi 2026-10-11, proposa 99 cc2cf2e093641ecf"
---

# Bar Polish dan UX Lintas Platform untuk Game Mobile (target sentuh, kontras, respons, warna, motion, juice)

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C6, lajur riset L3). Kelas bukti campur per baris dengan label eksplisit: PRIMER platform/W3C untuk ambang, RISET-UX untuk temuan persepsi manusia, SEKUNDER untuk angka yang sumber primernya belum dibuka, PROV untuk warisan tak ter-upgrade. Semua angka terukur pada giliran hulu 2026-10-11 00:38-01:05 WIB dengan artefak cache tersimpan; objek ini naik atas dasar rantai ukur beku (lihat rujukan).

## 1. Target sentuh (PRIMER platform + W3C)

- Google: target sentuh interaktif >= 48x48 dp ('lebih besar lebih baik'). [R-4 P1/U-10; R-1 B-37]
- Apple: iOS/iPadOS default control size 44x44 pt, minimum 28x28 pt (dibaca dari JSON resmi HIG accessibility). [R-4 P1/U-11; R-1 B-37]
- W3C WCAG 2.2: SC 2.5.8 Target Size (Minimum, level AA) >= 24x24 CSS px; SC 2.5.5 Target Size (Enhanced, level AAA) >= 44x44 CSS px. [R-4 P1/U-12; R-1 B-37]
- Sintesis bar unggul lintas platform: >= 48 dp/pt (keputusan desain, turunan dari tiga primer di atas - bukan kutipan satu halaman). [R-4 P1]

## 2. Kontras teks (PRIMER platform)

- Rasio >= 4,5:1 untuk teks kecil (< 18sp, atau bold < 14sp); >= 3:1 untuk teks besar. [R-4 P2/U-10; R-1 B-38]

## 3. Waktu respons persepsi manusia (RISET-UX)

- 0,1 s = terasa instan (tanpa feedback khusus); 1,0 s = batas alur pikir tak terputus; 10 s = batas perhatian (di atasnya wajib indikator progres + jalan batal). Aturan dipertahankan 'sama selama 46 tahun' (update halaman 2014). [R-4 P3/U-13 NN/g Jakob Nielsen; R-1 B-39]

## 4. Legibilitas warna (SEKUNDER - label jujur)

- Buta warna merah-hijau: hingga 1 in 12 pria (8%) dan 1 in 200 wanita (0,5%) -> jangan andalkan warna saja sebagai pembawa informasi. Kelas SEKUNDER: angka diambil dari Wikipedia 'Color blindness' yang merujuk NEI sebagai primer; halaman primer NEI belum dibuka pada misi ini (gap G-6). [R-4 P4/U-17; R-1 B-40]

## 5. Motion UI (PROV - warisan, tidak ter-upgrade)

- Durasi micro-interaction 75-500 ms dan kurva standar `cubic-bezier(0.4.0,0.2.1)` (ejaan persis seperti tercatat di sumber hulu) dari halaman Material Design: status PROV dipertahankan karena halaman m2 hari ini berupa shell JS (0 token kurva di HTML mentah, rung-8 ladder); angka diwarisi dari korpus l5 C-11 dengan label PROV. Dilarang menaikkan kelasnya jadi PRIMER tanpa pengukuran baru. [R-4 P5/U-22 catatan ladder; register gap G-5 pada matriks sumber]

## 6. Juice / game feel (KUALITATIF-IDENTITAS)

- 'Juice it or lose it' - talk Martin Jonasson & Petri Purho, kanal grapefrukt: identitas terverifikasi via YouTube oEmbed (title + author). [R-4 P6/U-15; R-1 B-41]
- 'Game Feel' - Steve Swink, 2008 (OpenLibrary API: median 376 hal, ISBN cetak 9780123743282): identitas terverifikasi. [R-4 P6/U-16; R-1 B-41]
- 'Art of Screenshake' (Vlambeer): NEGATIF terkonfirmasi (live 404 + CDX nihil s/d 20.000 baris + archive.ph 404) -> JANGAN dikutip; konsep screenshake tetap terdokumentasi lewat talk juice di atas. [R-4 U-21; register terlarang X-8 pada proposa sumber]

## 7. Aksesibilitas gameplay (komunitas)

- Panduan kontrol virtual besar+berjarak, sensitivitas dapat diatur, alternatif kontrol sederhana (daftar lengkap hidup di gameaccessibilityguidelines.com; isi per-butir = suplemen, belum dibedah per baris). Predikat jujur: RESMI-KOMUNITAS, bukan platform. [R-4 P7]

## 8. BATAS dan prospektif

- Kerangka desain 'MDH' TIDAK masuk objek ini: NEGATIVE-TERDOKUMENTASI (tiga jalur akun; diduga kuat typo MDA) - lihat register terlarang X-6 pada proposa sumber. Yang sah adalah MDA (Mechanics-Dynamics-Aesthetics, paper primer Hunicke/LeBlanc/Zubek) sebagai kerangka kualitatif tanpa angka ambang intrinsik. [R-4 D7/D8/U-14/U-20; R-1 K-6]
- Baris 4 dan 5 membawa label kelas bukti lebih rendah dari baris lain secara sengaja; konsumen wiki dilarang membaca angka PROV/SEKUNDER sebagai ambang mengikat.
- Prospektif: prosedur DELTA memakai salinan beku `vault/rafif-gameskill-1010/sources/` (pin di bawah), bukan berkas hidup.

## 9. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.7 baris B-37..B-41; ss.5 K-6; ss.6 gap G-5/G-6/G-7.
- [R-4] `vault/rafif-gameskill-1010/sources/L3_quality_bar.md` (31.665 B, sha256[:16] 32e41ac440292210) ss.1 U-10..U-17, U-20..U-21; ss.2.3 baris P1..P7.
- [R-5] `vault/rafif-gameskill-1010/sources/02_freshness_test.md` (24.736 B, sha256[:16] 8c1702cf52c56016) ss.2 baris 16 (kelompok FRESH-INTERNAL/teori).
- [R-6] Rantai verifikasi: `vault/rafif-gameskill-1010/sources/01_verifier_report.md` (23.207 B, sha256[:16] 9b76395d61c4622c) + `verification/02_countersign.md` (14.619 B, sha256[:16] 52df35384621bef2) + `seed_log.json` (3.390 B, sha256[:16] 056afe926aa719b9) - countersign AGREE mereproduksi angka hulu pada byte identik.
- [R-7] Vonis promote-turn: nol delta vs hulu 11-10 pada URI yang dapat diprobe; detail probe di tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
