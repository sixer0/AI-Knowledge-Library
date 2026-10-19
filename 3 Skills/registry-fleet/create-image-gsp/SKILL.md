---
name: create-image-gsp
description: "Perintah global /create-image-gsp: satu gambar/imagegen Imagegen 3.0 no-edit dari konten user; design tanpa input user = HIL wajib; hasil wajib dipreview ke user."
version: 1.6.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: orchestration
    tags: [gsp, imagegen, image, hil, perintah]
  hermes:
    tags: [gsp, imagegen21, image, command]
---

# /create-image-gsp — Generate Image (STANDAR IMAGEGEN-3.0, prosedur final no-edit)

Gunakan skill ini ketika user memanggil `/create-image-gsp`. Argumen trailing = konten
permintaan. SATU perintah = SATU gambar dengan parameter lengkap (keputusan user 25-09;
batch bukan v1). Jalankan TANPA ORKESTRASI (direktif user 25-09): render dan seluruh
verifikasi dieksekusi LANGSUNG oleh agen pemanggil dalam sesi ini; dilarang delegate_task
atau kartu pekerja, karena layanan imagegen FIFO satu-request. Rujukan wajib: SOP
`C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md` (**bagian 0 = PROSEDUR FINAL v3
no-edit, mengikat; bagian jalur sunting di bawahnya DICABUT untuk perbaikan hasil generate**),
template `slide_spec_template.json` (dipakai sebagai spec gambar tunggal), `build_prompt.py`.

## GERBANG 1 — Konten (WAJIB)

Konten dari user HARUS ada. Bila kosong: STOP, minta konten. Angka/fakta/named entity/klaim
tidak boleh kamu improvisasi (haram SOP). Level improvisasi default L2: gaya dan struktur
boleh diangkat ke standar penuh, isi tidak.

## GERBANG 2 — System Design (WAJIB; TANPA DESIGN USER = HIL WAJIB)

Dua sumber sah:
1. Berkas `design_master.json` (dari `/create-deck-gsp` atau user langsung), atau
2. Preset bernama MASTER_DESIGN yang DISEBUT user (GENERAL/BUSINESS/dll, lihat skill `gsp-design-system-grill`).

**Bila user TIDAK memberikan system design: WAJIB HIL sebelum render apa pun
(direktif user 25-09).** Agent dilarang memilihkan design sendiri, memakai default
diam-diam, atau lanjut ke spesifikasi gambar. Sajikan daftar pilihan lewat pertanyaan
terstruktur (clarify/form): semua preset MASTER_DESIGN bernama + opsi "design khusus".
Bila user memilih design khusus: kerjakan LANGSUNG dengan skill
`gsp-design-master-extraction` (terpasang di semua profil) — mampu MENGEKSTRAK dari PDF
brand-manual (jalur E) atau gambar (jalur I) yang user lampirkan, atau menyusun dari nol
(jalur S); hasil wajib lolos `validate_design_master.py`. Tanpa orkestrasi: jangan dispatch
profil lain kecuali user minta eksplisit. Logo hanya dari BERKAS asli user, tanpa berkas = logo tidak
digambar. Tunggu PILIHAN
user tercatat, baru lanjut. Pilihan user dicatat di jejak misi.

Konversi preset -> spec: warna dalam KATA + urutan, bukan hex mentah (SOP §13.2).

## SPESIFIKASI GAMBAR (isi slide_spec versi tunggal)

Tanya/lengkapi: tujuan gambar, rasio (default 16:9 2752x1536; varian lain = catat sebagai
penyimpangan), daftar string teks yang WAJIB muncul persis (identity flags), region layout,
referensi visual (PNG latar gelap @512, maks 10, logo lockup terakhir "reproduce exactly"),
seed (wajib; tanpa seed deck_base, pakai seed basis baru yang dicatat).

## EKSEKUSI

1. `build_prompt.py` dari spec (tolak sisa `<<>>`, non-ASCII, id tak dikenal).
   **Penguatan hulu SEBELUM render** (kunci minim-revisi, SOP v3 §0): token rawan ditulis
   KAPITAL (teks mikro kapital-rendah gagal statistik; kapital selalu andal), akronim rapuh
   diganti kepanjangan resmi dari sumber, kata bilangan rawan jadi digit, ukuran tipe teks
   mikro diperbesar.
2. health -> generate via tunnel :8040 (serial; 503 tunggu Retry-After; 422 perbaiki, jangan retry utuh).
3. **QA zona penuh SEKALI jalan**: seluruh zona dibaca huruf-demi-huruf dari PNG mentah
   dalam satu giliran; semua cacat didaftarkan sekaligus dengan predikat per zona.
4. **Vonis 3 pemicu generate ulang**: (a) judul/label salah atau typo; (b) identitas
   (entitas/produk/standar/kontak) salah atau typo; (c) angka/data tidak akurat. Typo teks
   kecil non-identitas = revision list, BUKAN pemicu. Jika pemicu menyala: **SATU generate
   ulang dengan PROMPT LANJUTAN** (prompt asli + blok revisi gabungan: kutip kata salah,
   eja bentuk benar, nyatakan bentuk terlarang, larang mencetak catatan revisi). DILARANG
   seed ulang prompt identik; DILARANG KERAS memperbaiki via sunting kotak/paint/komposit
   di atas render (`edit_grid.py` dicabut user 25-09 untuk kelas perbaikan ini).
   **Cap keras 2 generation.** Kandidat terbaik dipromosikan apa adanya walau residu kecil
   tersisa; residu dilaporkan sebagai revision list + opsi iterasi — USER yang memutuskan.
5. Serahkan: PNG + record.json (prompt SHA-256, seed, referensi+sha256, predikat zona per
   generation) + catatan improvisasi.
6. **PREVIEW IMAGE WAJIB DITAMPILKAN KE USER (direktif user 25-09, ditegaskan ulang).** Pesan
   FINAL penyerahan WAJIB memuat preview gambar hasil generation: baris
   `MEDIA:<path-absolut-png>` (forward-slash) untuk setiap gambar yang dihasilkan, tampil
   langsung di chat. Dilarang hanya menyebut path atau nama berkas tanpa gambar tampil.
   Untuk deck: tampilkan per slide saat penyelesaian, dan gambar hasil generate ulang
   tampilkan lagi (bandingkan sebelum vs sesudah). Preview dikirim SEBELUM klaim selesai,
   termasuk saat status parsial/buntu (user tetap melihat apa yang sudah ada).

Simpan jejak kerja di `docs/<tanggal>-image-<slug>/` (atau folder misi aktif). Untuk satu
gambar cepat tanpa kontrak penuh, minimal record.json + hasil cek identity wajib tetap ada.

## RANTAI EKSTRAKSI LOGO TRANSPARAN (SOP §0.5; ruling user 28-09)

DILARANG menyerahkan crop mentah PDF/gambar sebagai aset logo: crop hanya memotong persegi
dan tetap membawa latar halaman. Aset yang diserahkan wajib PNG RGBA tembus QA dua latar.
Skrip rantai ikut skill ini di `scripts/logo-transparency/` (jalankan lewat
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

- Render tanpa design sah (gerbang 2) atau tanpa konten user (gerbang 1).
- **Mendelegasikan render ke worker/subagent/kartu kanban** (mode tanpa orkestrasi; layanan FIFO).
- **Menyerahkan hasil TANPA preview gambar tampil di chat** (langkah 6 wajib; path saja tidak cukup).
- **Melanjutkan ke render tanpa pilihan design dari user saat design tidak diberikan** (HIL wajib, gerbang 2).
- Paralel request; restart layanan; edit design_master in-place.
- **Memperbaiki hasil render via sunting kotak/paint/komposit (`edit_grid.py` dsb.)** — jalur ini DICABUT user 25-09; perbaikan hanya via generate ulang dengan prompt lanjutan (SOP v3 §0).
- **Menyerahkan crop mentah PDF/gambar sebagai aset logo** — wajib rantai transparan SOP §0.5 (regenerate `--ref` + kunci latar flood-fill + QA dua latar), ruling user 28-09. Skrip: `scripts/logo-transparency/`.
- **Merantai lebih dari 2 generation** atau menolak promosi karena residu typo non-pemicu — keputusan iterasi lanjutan milik user.
- Mengklaim "selesai" tanpa cek struktur + identity terdokumentasi.


## PITFALL EMPIRIS iterasi mutu (misi cover DEMS EDGE CLIENT 30-09, 4 generation terdokumentasi)
- Blok revisi lanjutan (kutip salah + eja benar + bentuk terlarang) ANDAL untuk typo kata dan jumlah ubin: RECORDOING->RECORDING, Haah->Hash, 5 ubin->4 ubin pulih dalam SATU regenerasi (seed sama 30932).
- Label MIKRO sekunder pada objek (teks kecil di pelat port) tetap berganggu walau dilarang eksplisit; bentuk terlarang yang dikutip justru bisa terbit ulang (AC? CAM). Obat: perintah "jika label tak bisa bersih, biarkan logam polos tanpa huruf" + jangan masukkan string mikro ke spec.
- Blok revisi UPLIFT MUTU (PBR/studio) memicu REGRESI teks baru -> QA zona penuh WAJIB diulang setiap generation, bukan hanya generation pertama.
- Kata tagline rawan huruf dobel (Serviccable); cek zoom 3x per kata sebelum promosi.
