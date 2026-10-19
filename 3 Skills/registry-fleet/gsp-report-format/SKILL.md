---
name: gsp-report-format
description: >-
  Use when creating GSP official documents (DOCX/MD).
version: 1.4.0
author: GSP (PT. Gemilang Satria Perkasa) - Brahma Orchestrator
license: MIT
platforms: [windows, macos, linux]
metadata:
  hermes:
    tags: [gsp, report, format, docx, standar, datum]
    category: gsp
  gsp:
    category: document
    tags: [gsp, report, format, docx, standar, datum]
---

# GSP Report Format - dokumen resmi sesuai 020/GSP/STD/VIII/2026 RevA


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## GSP-SDT Integration (v1.2.0 - dokumen resmi berkelas)

Sumber kebenaran bentuk dokumen: [`skills/gsp/gsp-document-quality-standards/references/gsp-sdt/`](../gsp-document-quality-standards/references/gsp-sdt/)
(paket GSP-SDT; jangan salin isinya ke file ini). Default rezim skill ini: **SDT umum**;
rezim lain (SDTP/AD/AU/PL/CY/BIZ) dipilih eksplisit per pekerjaan via `delta-matra.md`.

Penerapan di skill ini (jalur DOCX resmi):
1. Halaman pertama memuat **blok identitas** bentuk rezim (kisi 6×4 pertahanan / strip
   profesional) - `blok-identitas.md`; field mesin ditambahkan di atas frontmatter Module L.2.
2. Register dokumen pola `GSP-SDT(-XXX)-nnn` + nomor `NNN/GSP/KODE/BULAN_ROMAWI/TAHUN`
   (provisional sampai Register Induk) - `penomoran-footer.md`; selaraskan dengan pola
   penamaan Tabel 7.1 skill ini (keduanya komplementer: SDT = identitas dokumen sistem,
   020/GSP = format terbitan laporan).
3. Klasifikasi empat tingkat B/T/R/SR tercetak di kepala, kaki, dan sampul; footer mengikuti
   pola nomor lembar rezim target (`n - mm`, `SHEET nn OF mm`, dst.) - C-16/C-22.
4. Urutan bagian dokumen = urutan baris matriks anatomi kelas target (`anatomi-per-kelas.md`);
   blok ● kosong = tahan terbit. Bobot kelas K1–K8 diketahui sebelum terbit (`kelas-dokumen.md`).
5. Provenans angka memakai glyph ■◈◇△ yang sudah dipakai skill ini - padanannya identik
   dengan C-18 (`provenans.md`); satu angka = satu provenans; wajib di K1/K4/K5.
6. Riwayat revisi: huruf berurut, terbaru di puncak, baris lama tidak diubah (C-24).
7. Gerbang pra-terbit: checklist 14 butir skill ini DIJALANKAN BERSAMAAN dengan
   `checklist-pra-terbit.md` GSP-SDT (22 butir) untuk dokumen berkelas K1–K8; keduanya LULUS
   sebelum ekspor. Konflik: FORMAT → Module L; BENTUK/ANATOMI/REGISTER → GSP-SDT; GAYA → H/K.
8. Generator: pakai [`templates/gsp_lib.py`](templates/gsp_lib.py) (skill ini) + helper `snippet-docx.py` paket SDT
   (blok identitas, header/footer klasifikasi, nomor lembar per rezim, tabel revisi).

Larangan: jangan salin tabel K1–K8/anatomi/checklist ke file ini; jangan campur total bobot
67 (keluarga pertahanan) dan 66 (PL/CY/BIZ); jangan kutip nomor register provisional sebagai final.
Revisi: v1.1.0 (2026-09-01, SM-2 t_4cc4e6b9) - section GSP-SDT + pointer paket (langkah 17).
- Em-dash U+2014 DILARANG MUTLAK tanpa pengecualian (D17); middle dot U+00B7 dilarang dengan pengecualian hanya string blok terkendali yang meniru master design verbatim. Berlaku atas seluruh teks keluaran; definisi + prosedur scan: `gsp-document-quality-standards/references/gsp-sdt/README.md` (bagian Aturan teks keluaran D15+D16).

## When to Use

Use this skill when the user asks to create or reformat any GSP official
document (laporan, proposal, technical report, memo, ringkasan pimpinan) in
DOCX/MD/PDF. The authoritative source is the acuan PDF
`Acuan_Standar_Format_Laporan_GSP_untuk_Sistem_AI_020GSPSTDVIII2026_RevA.pdf`
(8 hal). If the acuan is not attached, use the condensed values in
[`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) (Modules I–K) - NOTE: the
former bundle file "ringkasan-standar-format.md" does not exist in this
registry (verified 30-08-2026; do not re-add the dead reference).

Also load when delivering GSP files via Hermes WebUI `MEDIA:` tokens - see
Delivery pitfalls below.

## Core rules (condensed; full values in references/)

- **Grid:** A4 210×297 mm; margin kiri/kanan 24/20 mm; header/footer 13/13 mm;
  lebar penuh 166 mm; kolom baca 128 + selokan 6 + rel 32 mm; baseline 13,5 pt.
- **Fonts (fallback office jika IBM Plex tidak terpasang):**
  - Struktur (judul/kicker/kepala tabel): IBM Plex Sans Condensed → Segoe UI Semibold / Arial Narrow
  - Baca (teks isi): IBM Plex Serif → Georgia / Cambria
  - Data (angka/kode/label/footer): IBM Plex Mono → Consolas / Courier New
  - TERLARANG sebagai teks isi: Calibri, Times New Roman, Aptos, Arial.
- **Palet interior:** paper #FCFCFB; ink900 #101418; ink700 #2B3640;
  ink400 #6B7783, ink200 #C3CBD1, ink100 #EFF2F4, signal #B45309,
  alert #9B1C1C, verd #2F6F6B. Tanpa gradien/bayangan/3D.
- **Anatomi:** SAMPUL (logo, kicker, judul 2 baris, subjudul miring, tabel
  kendali, cap `// 25VIII2026 ID T - TERBITAN 1`) → RINGKASAN PIMPINAN
  (6 baris tetap: APA INI / UNTUK SIAPA / MENGAPA SEKARANG / KEYAKINAN /
  RISIKO TERBESAR / LANGKAH BERIKUT + opsional blok KEPUTUSAN) → BAGIAN
  (H1 + kicker "Bagian Satu", H2 bernomor) → PENUTUP → RIWAYAT REVISI.
- **Header:** kiri organisasi / divisi / judul kapital; kanan chip klasifikasi;
  garis tipis. **Footer 4 sel:** `GSP · ID` | `REV X · tgl` | `LEMBAR n DARI N` (field PAGE/NUMPAGES) | chip klasifikasi.
- **Aparatus bukti (4 glyph):** ■ TERUKUR (ink900, dibaca dari sumber/alat);
  ◈ DITURUNKAN (signal, dihitung; penurunan ditunjukkan), ◇ PEMASOK (ink400,
  klaim vendor belum diverifikasi), △ ASUMSI (alert, wajib identitas+dampak).
  Dokumen berangka (>~12 angka penting) wajib minimal satu blok bertanda.
- **Tabel:** keterangan DI ATAS (`TABEL n.n` amber + kalimat berujung titik);
  tanpa garis vertikal; horizontal bertingkat (0,45 mm ink900 atas kepala,
  0,25 mm bawah kepala, 0,2 mm ink200 antar baris, 0,45 mm di atas total);
  kepala kolom kapital; angka rata kanan + data font; kaki `SUMBER` (+`PROVENANS`).
- **Angka/bahasa:** desimal koma + ribuan titik (`2,3 juta`); "persen" dieja;
  spasi nilai-satuan (`40 W`); rentang `225 nm hingga 2400 nm`; em-dash
  **maks 3 per 1000 kata** (butir 9 checklist); ± harus didefinisikan.
- **Penamaan (Tabel 7.1):** ID `NNN/GSP/KODE/BULAN-ROMAWI/TAHUN`; nama berkas
  `Nama Ringkas NNN-GSP-KODE-VIII-2026 RevX.docx`; tanpa underscore; pasangan
  docx+pdf senama; revisi huruf naik (RevA→RevB); SHA-256 dicatat di register.

## Workflow

1. Baca acuan PDF (pymupdf) atau gunakan nilai kondensasi di skill
   `gsp-document-quality-standards` (Modules I–K).
2. Salin [`templates/gsp_lib.py`](templates/gsp_lib.py) ke folder laporan (helper python-docx yang
   sudah terbukti: grid, palet, header/footer + field LEMBAR n DARI N, blok
   bukti, grammar tabel, normalisasi em-dash).
3. Susun generator `buat_laporan.py` mengikuti anatomi (sampul → ringkasan →
   bagian → penutup → riwayat revisi). Gunakan `add_evidence_block` untuk
   klaim penting; label sesuai asal pengetahuan.
4. Bangun DOCX, lalu jalankan checklist 14 butir (Tabel 9.1 acuan) - semua
   harus YA; dokumen dengan satu TIDAK belum terbit.
5. Simpan dengan nama pola Tabel 7.1 + SHA-256; beri tahu user keterbatasan
   render (lihat Pitfalls).

## Pitfalls

- **Em-dash adalah butir 9 checklist dan paling sering dilanggar AI.** Ukur
  `teks.count("-")*1000/len(teks.split())`; jika >3, normalisasi: `" - "` → `", "`
  dan em-dash lain → en-dash `–`. Helper `gsp_lib.py` melakukan ini otomatis.
- **PDF pasangan tidak selalu bisa dibuat.** Tanpa Word/LibreOffice terpasang,
  docx→pdf gagal. Nyatakan batas ini JUJUR di dokumen (Bagian 8 acuan: batas
  yang disembunyikan lebih serius daripada batas itu sendiri), jangan diam.
- **Font IBM Plex sering tidak terpasang.** Gunakan fallback office yang
  diizinkan; JANGAN pakai Calibri/Times/Aptos/Arial sebagai teks isi.
- **Klasifikasi tergantung PENERIMA, bukan GSP.** Internal = TERBATAS (chip
  merah). Rezim Polri/ANRI: BIASA/TERBATAS/RAHASIA/SANGAT RAHASIA. Rezim
  pertahanan (Permenhan 26/2017): BIASA/RAHASIA/SANGAT RAHASIA - TIDAK mengenal
  TERBATAS; memakainya pada dokumen pertahanan = kesalahan kepatuhan.

## Delivery pitfalls (Hermes WebUI)

- **Token `MEDIA:` dengan backslash Windows (`MEDIA:C:\Users\...`) merusak
  parsing renderer** dan link download gagal. Selalu gunakan forward slash:
  `MEDIA:C:/Users/.../file.docx`. (Kasus nyata 25-08-2026: user tidak bisa
  download sampai path diganti forward-slash.)
- **`/api/media` butuh sesi login** (401 tanpa cookie) dan hanya menyajikan
  file di allowed roots: HERMES_HOME, /tmp, active workspace, plus
  `MEDIA_ALLOWED_ROOTS`. Simpan deliverable di dalam active workspace
  (mis. `<workspace>/OUTPUT/`), bukan di luar.
- Jika user melapor tidak bisa download: cek (1) format path forward-slash,
  (2) file ada di workspace, (3) cache/sesi browser.

## Verification (checklist 14 butir - semua harus YA)

1. Grid A4 + margin 24/20/13/13 mm, 2. Font stack, nol Calibri/Times/Aptos,
3. Sampul lengkap (kicker, judul, subjudul, tabel kendali, cap terbit),
4. Ringkasan pimpinan 6 label, 5. Header/footer + chip klasifikasi + LEMBAR
n DARI N benar, 6. Tabel: keterangan di atas, SUMBER di bawah, tanpa garis
vertikal, 7. Gambar: caption + SUMBER, panah berlabel, ≤5 warna, 8. Angka
gaya Indonesia, 9. Em-dash ≤3/1000 kata, 10. Blok asal-pengetahuan hadir,
11. Istilah Inggris utuh, kata kerja perilaku pada tujuan, 12. Penomoran
Tabel-Gambar urut per bagian tanpa duplikat, 13. ID + nama berkas pola +
revisi + riwayat + register, 14. Klasifikasi sesuai skema penerima.

## Support files

- [`templates/gsp_lib.py`](templates/gsp_lib.py) - helper python-docx terbukti (grid, palet, header/
  footer + field halaman, blok bukti, grammar tabel, normalisasi em-dash).
- Nilai acuan terperinci (grid, skala tipe, palet hex, anatomi, grammar,
  klasifikasi, penamaan): skill `gsp-document-quality-standards` Modules I–K
  ([`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md)) - berkas kondensasi
  lama "ringkasan-standar-format.md" TIDAK ada di registry.

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
