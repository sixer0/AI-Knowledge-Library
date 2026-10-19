---
name: create-deck-gsp
description: "Perintah global /create-deck-gsp: deck presentasi Imagegen 3.0 no-edit dari materi user, gerbang HIL design+panjang, hasil wajib dipreview ke user."
version: 1.6.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: orchestration
    tags: [gsp, imagegen, deck, hil, perintah]
  hermes:
    tags: [gsp, imagegen21, deck, command]
---

# /create-deck-gsp — Deck Presentasi (STANDAR IMAGEGEN-3.0, prosedur final no-edit)

Gunakan skill ini ketika user memanggil `/create-deck-gsp` (dengan atau tanpa argumen).
Argumen trailing = instruksi/materi awal user. Jalankan TANPA ORKESTRASI (direktif user
25-09): semua langkah, termasuk render, dieksekusi LANGSUNG oleh agen pemanggil dalam sesi
ini, SATU slide pada satu waktu. Dilarang memakai delegate_task/kartu pekerja untuk render,
karena layanan imagegen FIFO satu-request dan fan-out tidak menambah kecepatan, hanya
menambah tabrak antrean.

Rujukan wajib (baca sebelum eksekusi):
- SOP: `C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md` (**bagian 0 = PROSEDUR FINAL v3 no-edit, mengikat; bagian jalur sunting di bawahnya DICABUT untuk perbaikan hasil generate**)
- Template: `C:/Users/TRIAL/workspace/handoff/templates/` (design_master, deck_plan, slide_spec, revision_log)
- `docs/2026-09-25-imagegen21-orchestration-mapping.md` = RUJUKAN FORMAT artefak saja
  (bentuk CONTRACT.md, record.json, VERIFICATION.md); jalur kartu/fasenya TIDAK dipakai.

## GERBANG 1 — Materi (WAJIB, tanpa negosiasi)

Konten materi dari user HARUS ada (teks, berkas, atau URL yang kamu ekstrak).
Bila kosong: STOP, minta materi. Dilarang mengarang topik (aturan haram SOP: angka,
fakta, named entity, klaim tidak boleh improvisasi; level improvisasi default L2 hanya
untuk gaya/struktur, bukan isi).

## GERBANG 2 — System Design (HIL)

Tanya/cek: user menyediakan design system atau agent yang membuat?

**A. Dari user:** terima salah satu bentuk —
  - berkas `design_master.json` (validasi: `approved_by_user` terisi; versi tidak diedit in-place), atau
  - preset bernama MASTER_DESIGN (GENERAL, BUSINESS, VISUAL, TEKNIK, POLRI, TNI-AD/AL/AU, BNN, BNPT, KEMHAN, CYBER-SECURITY, MILITARY) dari skill `gsp-design-system-grill/references/master-design/`.
  Konversi preset -> `design_master.json`: hex/nama font dari preset JANGAN disalin mentah ke prompt;
  isi `brand_rules` DALAM KATA (SOP §13.2: warna disebut nama+urutan, bukan hex).

**B. Dibuat agent:** kumpulkan dulu informasi kompleksitas dari user lewat HIL:
  1. kebutuhan hero image (per bagian/slide),
  2. spektrum warna (atau pilih preset),
  3. tema gelap/terang,
  4. logo + identitas: **WAJIB minta BERKAS logo asli** (PNG; latar gelap lebih baik).
     Tanpa berkas logo: logo TIDAK digambar sama sekali, catat di register. Deskripsi lisan
     tidak pernah jadi dasar menggambar logo (keputusan user 25-09).
     Bila logo diambil dari PDF/gambar (bukan berkas aset lepas): WAJIB jalankan rantai
     ekstraksi transparan SOP §0.5 (crop presisi -> regenerate imagegen --ref kanvas kecil
     -> kunci latar flood-fill -> QA dua latar); DILARANG menyerahkan crop mentah berlatar.
     Skrip rantai ikut skill ini di `scripts/logo-transparency/` (lihat bagian Rantai
     Ekstraksi Logo Transparan di bawah untuk urutan pakai + dependensi uv).
  5. materi brand yang tersedia: PDF manual / gambar papan gaya / tidak ada.
  Lalu SUSUN LANGSUNG master design dengan skill `gsp-design-master-extraction`
  (terpasang di semua profil; jalur E ekstrak PDF, jalur I ekstrak gambar, jalur S dari
  nol; konversi hex->kata SOP §13.2; hasil WAJIB lolos `validate_design_master.py`
  sebelum diajukan). Tanpa orkestrasi: jangan dispatch profil lain kecuali user minta
  eksplisit. Hasil berupa `design_master_<brand>_v<N>.json`
  + refs @512 + tabel bukti per token, lalu **approval user** (SOP §13.3).

Tema TERANG: boleh penuh atas keputusan user (25-09) — perlakukan setara gelap;
namun tetap render slide pertama lebih dulu dan nilai (pilot alami alur kerja),
karena arah D2/D4/D5 belum punya bukti terukur seperti D1. Catat di Decision Log kontrak.

## GERBANG 3 — Panjang & storyline deck (HIL)

Bila user tidak menyebut jumlah slide: baca materi, usulkan struktur (panduan SOP §15.3:
5-10 slide, campur archetypes: title -> konteks/masalah -> proses -> perbandingan ->
monitoring -> penutup; satu pesan per slide; deck eksekutif umum ±15 per grill G7.Q3).
Sertakan ESTIMASI WAKTU: 5-7 menit/slide, serial (10 slide ≈ 50-70 menit; layanan FIFO).
Minta PERSETUJUAN user sebelum lanjut. Hasil: `deck_plan.json` (1 entri/slide: archetype,
outline, message, data source, hero_concept, seed) — approval user (SOP §13.3).

## EKSEKUSI (setelah 3 gerbang lolos; TANPA ORKESTRASI)

Buat jejak misi `docs/<tanggal>-deck-<slug>/` (CONTRACT.md + Decision Log) sebagai berkas
biasa, tanpa kartu kanban dan tanpa dispatch pekerja. Render semua slide sendiri, berurutan.
Pipeline per slide (PROSEDUR FINAL no-edit, SOP v3 §0; direktif user 25-09):

1. **Spec + penguatan hulu** (SEBELUM render pertama, kunci minim-revisi): semua string
   dengan flag identitas; angka verbatim dari dokumen sumber; region per string; token
   rawan ditulis KAPITAL (teks mikro kapital-rendah gagal statistik: STIX 13x, Keycloak
   8x, PUSAT 6 variasi; kapital selalu andal); akronim rapuh diganti kepanjangan resmi dari
   sumber; kata bilangan rawan jadi digit; ukuran tipe teks mikro diperbesar di template.
2. **Render pertama** via `build_prompt.py` (ASCII, SHA-256 tercatat) -> generate (tunnel
   :8040, seed deck_base+100*nn).
3. **QA zona penuh SEKALI jalan**: semua zona dibaca huruf-demi-huruf dari PNG mentah dalam
   satu giliran; semua cacat didaftarkan sekaligus dengan predikat per zona. Dilarang
   mengejar per-token lintas seed.
4. **Vonis 3 pemicu generate ulang**: (a) judul/label/judul panel salah atau typo; (b)
   identitas (entitas/produk/standar/kontak) salah atau typo; (c) angka/data tidak akurat.
   Typo teks kecil non-identitas = revision list, BUKAN pemicu.
5. **Jika pemicu menyala: SATU generate ulang dengan PROMPT LANJUTAN** = prompt asli + satu
   blok revisi gabungan (kutip kata salah, eja bentuk benar, nyatakan bentuk terlarang,
   larang mencetak catatan revisi di slide). DILARANG seed ulang prompt identik (terukur
   mengulang cacat yang sama). DILARANG KERAS memperbaiki via sunting kotak/paint/komposit
   di atas render (`edit_grid.py` dicabut untuk kelas perbaikan ini).
6. **Cap keras 2 generation/slide.** Kandidat terbaik DIPROMOSIKAN APA ADANYA walau residu
   kecil tersisa; residu dilaporkan ke user sebagai revision list + opsi iterasi; USER yang
   memutuskan lanjut atau berhenti. Controller/agen dilarang merantai generasi ke-3+ demi
   nol-cacat (preseden boros: 24 request untuk 1 slide).
7. Catat di revision_log + record.json (seed, SHA prompt, predikat zona per generation).
Serahkan: PNG + record.json + ringkasan improvisasi + VERIFICATION.md.
Setiap slide selesai -> tampilkan preview-nya di chat (jangan simpan semua untuk akhir).
**Pesan FINAL WAJIB memuat preview setiap slide yang dihasilkan sebagai baris
`MEDIA:<path-absolut-png>` (forward-slash) yang tampil di chat (direktif user 25-09);**
path saja tanpa gambar tampil = penyerahan tidak sah.

## RANTAI EKSTRAKSI LOGO TRANSPARAN (SOP §0.5; ruling user 28-09)

DILARANG menyerahkan crop mentah PDF/gambar sebagai aset logo: crop hanya memotong persegi
dan tetap membawa latar halaman. Aset yang diserahkan wajib PNG RGBA tembus QA dua latar.
Skrip rantai ikut skill ini di [`scripts/logo-transparency/`](scripts/logo-transparency/) (jalankan lewat
`uv run --python 3.11 --with pymupdf --with pillow --with numpy python <skrip>`; simpan
semua hasil di `assets/<misi>/`, catat seed + ambang di record).

0. `extract_pdf_images.py <pdf> <outdir>` -> cek alpha bawaan citra tertanam (nama file
   berakhiran ALPHA/OPAQUE). Bila sumber sudah transparan: lompat ke langkah 4.
1. `detect_crop_logo.py <pdf> <halaman> <crop.png> [y0frac y1frac]` -> crop presisi 300 dpi,
   kotak pembatas terdeteksi programatik (mask saturasi untuk emblem berwarna; ganti mask
   gelap untuk aset monokrom), BUKAN koordinat kira-kira.
2. REGENERATE lewat imagegen (jalur utama): prompt = deskripsi datar unsur demi unsur dari
   crop + kalimat kunci "isolated and centered on a perfectly plain pure white background
   filling the entire canvas, no frame, no shadow, no texture"; perintah
   `imagegen21_client.py generate --prompt-file <p> --ref <crop.png> --ref-res 512
   --size <kanvas kecil sebanding rasio aset, mis. 896x1152> --seed <catat> --out flat.png`.
   Kanvas slide 2752x1536 boros memori (rawan 503 admission_refused). Bila GPU jenuh:
   jadwalkan ulang, JANGAN diam-diam melompat ke fallback; fallback crop-300-dpi langsung
   hanya dengan izin user/controller dan dinyatakan di laporan.
3. `key_out_bg.py <flat.png|crop.png> <alpha.png>` -> kunci latar deterministik: median warna
   tepi, ambang Otsu dijepit [24,128], flood-fill DARI TEPI SAJA (warna yang sama dengan
   latar tapi di DALAM desain, mis. pita putih, tidak ikut bolong), feather 1 px, crop RGBA
   rapat isi.
4. GERBANG RIWAYAT: `qa_alpha.py <alpha.png>` menempel aset di latar putih + gelap; vonis
   visual per butir: tidak ada kotak tersisa, tepi bersih tanpa halo, tidak ada lubang pada
   warna yang sama dengan latar, teks emblem utuh. QA latar gelap WAJIB lulus sebelum aset
   diserahkan/dipakai slide.
5. Bukti terkurasi 28-09: emblem BARESKRIM, rantai 1->3->4 lulus penuh (crop 478x582 @300dpi
   -> RGBA 407x514, isi 58,6%, QA gelap bersih, pita utuh).

## Larangan

- Mulai render sebelum ketiga gerbang TERTULIS lolos (jejak di CONTRACT.md).
- **Mendelegasikan render ke worker/subagent/kartu kanban** (mode tanpa orkestrasi; layanan FIFO).
- **Menyerahkan akhir tanpa preview gambar slide tampil di chat (baris MEDIA wajib).**
- Paralelkan request ke layanan (FIFO; 503 = tunggu Retry-After).
- **Memperbaiki hasil render via sunting kotak/paint/komposit (`edit_grid.py` dsb.)** — jalur ini DICABUT user 25-09; perbaikan hanya via generate ulang dengan prompt lanjutan (§0 SOP v3).
- **Merantai lebih dari 2 generation per slide** atau menolak promosi karena residu typo non-pemicu — keputusan iterasi lanjutan milik user.
- Merestart layanan/tunnel milik operator.
- Mengedit design_master in-place (selalu versi baru + changelog).
