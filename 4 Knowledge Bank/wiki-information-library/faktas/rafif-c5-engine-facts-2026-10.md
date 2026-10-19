---
id: rafif-c5-engine-facts-2026-10
type: fakta
title: Fakta Engine Game Mobile Terverifikasi Okt-2026 (Godot / Unity / Construct 3)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict: terverifikasi || Alasan: 24/24 angka tertelusur (Godot via L2 U-3 + freshness U-10; Unity via L2 U-4 + K-12; Construct via L2 U-5 + freshness U-13 + matriks B-36 + K-9; pin byte-identik); baris Construct 3 membawa label ARSIP-BERLABEL + dua snapshot 22-Sep dan 06-Okt identik + penyebab (HTTP 503 anti-bot) sesuai kewajiban; register terlarang X-7 tidak mengalir sebagai fakta (angka 82.99/154.99/309.99/7.49 = 0 kemunculan; penyebutan Team/Enterprise hanya sebagai negasi sah); redaksi Unity persis putusan K-12 termasuk larangan '6.6 LTS' dan 'terbaru 6000.6.3f1'; granularitas satu objek sah per preseden VSSKB-0923 (marker per baris + BATAS kelas bukti per kelompok); dedup 0; YAML utuh. || Rekomendasi: nol perubahan muatan; nomor versi engine volatile - patuhi prosedur DELTA terhadap salinan beku sebelum angka dipakai di dokumen rilis setelah kuartal ini."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L2_domain_map.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: L2 ss.1 U-3..U-5; L3 ss.1 U-9 + ss.2.2 T12; R5 ss.2 baris 4-7
tanggal_akses: 2026-10-11
kelas_bukti: primer
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [godot, unity, construct-3, arsip-berlabel, engine, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L2_domain_map.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: faktas/rafif-c5-engine-facts-2026-10.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: gate biasa, custodian terverifikasi 2026-10-11, proposa 99 cc2cf2e093641ecf"
---

# Fakta Engine Game Mobile Terverifikasi Okt-2026 (Godot / Unity / Construct 3)

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C5, lajur riset L2/L3). Kelas bukti campuran per baris: PRIMER (API/resmi vendor terukur langsung) dan ARSIP-BERLABEL (baris Construct 3, lihat seksi 4). Semua angka terukur ulang pada giliran promosi 2026-10-11 pukul 10:12-10:19 WIB (probe P-10, P-11) terhadap artefak riset beku ber-pin.

## 1. Godot (PRIMER)

- Versi stabil terbaru: `4.7.2-stable`, dipublikasikan 2026-08-18T16:12:28Z (API resmi github.com/godotengine/godot releases/latest; identik pada probe giliran promosi). [R-3 U-3; R-1 B-35; R-7 P-10]
- Dependensi ekspor Android resmi: OpenJDK 17, SDK Platform-Tools 35.0.x, Build-Tools 35.0.1, SDK Platform 35, CMake 3.10.2.4988404, NDK r28b (28.1.13356709). [R-5 U-10; R-3 A-2]
- Lisensi MIT, gratis permanen (materi berubah-lambat; label warisan korpus l4 dengan verifikasi-ulang RG2). [R-3 A-2]

## 2. Unity (PRIMER)

- Versi terbaru: `6000.6.5f1` (rilis 2026-10-08) berstatus SUPPORTED, BUKAN LTS; stream 6000.6 berjalan 6000.6.0f1..6000.6.5f1. [R-3 U-4; R-1 B-35, K-12; R-7 P-11 redirect whats-new ke /whats-new/6000.6.5f1]
- LTS terkini stream 6000.3 = `6000.3.26f1`. Redaksi sah: 'Unity terbaru 6000.6.5f1 (SUPPORTED, bukan LTS); produksi = stream LTS 6000.3 (terkini 6000.3.26f1)'. DILARANG mengulang klaim 'terbaru 6000.6.3f1' dan DILARANG menyebut '6.6 LTS'. [R-3 U-4; R-1 K-12; R-7 P-11 arsip memuat 6000.3.26f1 dan 6000.3.25f1]
- Ambang plan Personal: pendapatan pendanaan < US$200K (token ambang hadir di halaman produk resmi saat uji). [R-5 U-12; R-3 A-2]
- Default frame rate mobile: dengan `QualitySettings.vSyncCount = 0` dan `Application.targetFrameRate = -1`, konten dirender FIXED 30 fps demi hemat baterai; nilai target dibulatkan KE BAWAH ke pembagi refresh rate terdekat (contoh resmi: set 25 pada layar 60 Hz -> jalan 20 fps); ProMotion mati (default proyek baru) = native 60 Hz. Konsekuensi penulisan: klaim '60 fps' wajib ditulis EKSPLISIT di paket skill, tidak boleh dianggap default. [R-4 T12/U-9, docs.unity3d.com 6000.3 Application-targetFrameRate]

## 3. Construct 3 - HANYA tabel ARSIP-BERLABEL (dua snapshot saling menguatkan)

Baris harga Construct 3 berikut BUKAN fakta live: halaman beli construct.net menolak akses bot (HTTP 503) pada giliran hulu, dan angka dipulihkan dari arsip web. Label wajib menempel setiap kali angka ini dikutip. Dua snapshot yang diuji pasang heading->harga: 2026-09-22 dan 2026-10-06, hasil IDENTIK. [R-3 U-5; R-5 U-13 baris 6; R-1 B-36, K-9]

- Personal: $15.99/bulan atau $129.99/tahun. [ARSIP web.archive.org construct.net/en/make-games/buy-construct snapshot 22-Sep+06-Okt; R-3 U-5]
- Startup: $234.99/tahun. [idem]
- Business: $469.99/tahun. [idem]
- Educational: $9.99/bulan atau $32.99/tahun. [idem]
- Struktur plan lama (Team License / Enterprise dan token harga pendampingnya) = 0 kemunculan di kedua snapshot -> tabel harga Construct lama di korpus hulu (struktur lima plan dengan nama Team/Enterprise) divonis STALE-STRUKTUR bahkan terhadap arsip 22-Sep (nama plan berubah Team/Enterprise -> Startup/Business, angka ikut berubah); angka tabel lama itu masuk register terlarang X-7 dan DILARANG mengalir sebagai fakta, sehingga tidak dikutip di objek ini. [R-3 U-5]

## 4. BATAS dan prospektif

- Nomor versi engine adalah klaim volatile: sah per tanggal akses 2026-10-11, wajib uji ulang sebelum dipakai dalam dokumen rilis setelahnya. Prosedur DELTA memakai salinan beku `vault/rafif-gameskill-1010/sources/` (bukan berkas hidup).
- Kelas bukti Construct 3 berbeda dari dua engine lain (ARSIP vs PRIMER) dan sengaja tetap satu objek master karena tiap baris membawa marker sendiri + blok BATAS menyatakan kelas per kelompok (preseden putusan granularitas VSSKB-0923; dicatat di proposa bagian 7 butir 2).
- Register terlarang yang TIDAK masuk objek ini: harga Construct struktur lama (X-7).

## 5. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.7 baris B-35/B-36; ss.5 K-9/K-12.
- [R-3] `vault/rafif-gameskill-1010/sources/L2_domain_map.md` (22.482 B, sha256[:16] 8086e5da4844a1f9) ss.1 U-3..U-5; ss.3 butir 1/3.
- [R-4] `vault/rafif-gameskill-1010/sources/L3_quality_bar.md` (31.665 B, sha256[:16] 32e41ac440292210) ss.1 U-9; ss.2.2 baris T12.
- [R-5] `vault/rafif-gameskill-1010/sources/02_freshness_test.md` (24.736 B, sha256[:16] 8c1702cf52c56016) ss.2 baris 4-7; U-9..U-13.
- [R-7] Probe hidup giliran librarian 2026-10-11 WIB: P-10 api.github.com godot releases/latest tag 4.7.2-stable published 2026-08-18T16:12:28Z identik; P-11 unity.com whats-new redirect 307 ke /whats-new/6000.6.5f1 (251 token) + arsip memuat 6000.3.26f1 dan 6000.3.25f1. Tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
