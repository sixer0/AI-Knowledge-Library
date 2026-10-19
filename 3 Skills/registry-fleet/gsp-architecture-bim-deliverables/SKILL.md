---
name: gsp-architecture-bim-deliverables
description: "Deliverable arsitektur & konvensi BIM/CAD GSP: skala-garis-notasi gambar, daftar set DED (arsitektur/struktur/MEP), LOD 100-500 & IFC, struktur RKS, RAB/BOQ + script template CSV. Muat saat menyusun dokumen kontrak, daftar gambar, spesifikasi, atau estimasi biaya."
version: 1.0.1
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, deliverables, bim, cad, ded, rks, rab, drawing, ifc, lod, specifications]
---

# GSP Architecture BIM & Deliverables

> Standar penyusunan deliverable arsitektur: dari paket gambar kerja (DED) hingga RKS dan
> RAB/BOQ, plus literasi BIM (LOD/IFC) untuk koordinasi digital. Output digital agent:
> dokumen (MD/PDF/DOCX/XLSX), skema (SVG/HTML), dan deskripsi teknis yang akurat — bukan
> pengganti file CAD/Revit asli.


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

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
## Konvensi Gambar (umum)

- **Kertas:** A4/A3/A2/A1/A0 sesuai kompleksitas; kop gambar berisi: judul proyek, nama
  gambar, nomor lembar, skala, tanggal, revisi, sumber (koordinat utara).
- **Skala umum:** site plan 1:500/1:1000; denah/tampak/potongan 1:100 (1:50 untuk detail);
  detail 1:20/1:10/1:5; potongan potongan bawah 1:50.
- **Garis:** garis tebal (terpotong bidang), sedang (terlihat), tipis (referensi/dimensi),
  putus-putus (tersembunyi), arsiran material.
- **Notasi:** level elevasi (±0.000), datum, grid kolom (A, B, C / 1, 2, 3), arah utara pada
  site plan, dimensi antar modul, simbol pintu/jendela konsisten.
- **Penomoran lembar:** A-101 (arsitektur), S-101 (struktur), M-101 (mekanikal), E-101
  (elektrikal); 3 digit = disiplin + nomor urut.

## Set Gambar DED (daftar lengkap umum)

**Arsitektur (A):** site plan; denah tiap lantai (furniture, dimensi, level); tampak
(4 sisi, material); potongan (memanjang/melintang, minimal 2); denah atap & detail talang;
RCP (plafon) + titik lampu; detail arsitektur (tangga, jendela, pintu, railing, kusen);
jadwal pintu & jendela; detail interior (bila perlu); landscape/site development;
perspektif & material board (opsional, komunikasi).

**Struktur (S):** denah pondasi & detail; denah kolom/balok/plat per lantai; detail
penulangan; detail sambungan; tangga struktur; jadwal kolom/balok.

**MEP (M + E):** denah plumbing air bersih/air kotor/vent; detail kamar mandi & septic;
skema hydrant/sprinkler/fire alarm (bila ada); denah titik listrik & panel; single line
diagram; penangkal petir; data & komunikasi (opsional).

**Non-gambar:** RKS; RAB/BOQ; jadwal pelaksanaan; perhitungan struktur/fisika (lampiran).

## BIM: LOD & IFC

| LOD | Makna (AIA/AGC) | Tahap |
|-----|-----------------|-------|
| 100 | Konsep: massa & luas | Konsep |
| 200 | Skematik: ukuran, bentuk, lokasi umum | Skematik |
| 300 | Detail: ukuran, bentuk, material persis | Pengembangan Rancangan |
| 350 | Konstruksi: koordinasi antar disiplin | Sebelum konstruksi |
| 400 | Fabrikasi/pemasangan | Konstruksi |
| 500 | As-built | Handover |

- **IFC (openBIM):** format pertukaran netral (buildingSMART). Pastikan model dapat diekspor
  IFC & bebas clash antar disiplin (clash detection).
- Agent GSP tidak membuat file CAD/Revit; untuk koordinasi, hasilkan: matriks LOD per elemen,
  daftar isu koordinasi, dan instruksi ekspor (mis. "ekspor IFC 2x3/4 dengan properti ruang
  + level"). Skema 2D dapat digambar ulang sebagai SVG/HTML untuk dokumentasi cepat.

## RKS — Struktur Bab (contoh)

1. Umum (lingkup, kualitas, referensi SNI, jaminan)
2. Pekerjaan persiapan & temporer
3. Pekerjaan tanah & pondasi
4. Pekerjaan struktur (beton/baja/kayu)
5. Pekerjaan arsitektur (dinding, plesteran, lantai, plafon, atap, pintu-jendela, railing)
6. Pekerjaan MEP (plumbing, sanitasi, elektrikal, tata udara, proteksi kebakaran)
7. Pekerjaan finishing & lansekap
Setiap item: mutu, tebal/ukuran, merek/standar, cara pemasangan, toleransi, pengujian.

## RAB / BOQ — Struktur & Estimasi

Urutan pekerjaan umum (subtotal per item berfungsi sebagai check):

1. Persiapan (mobilisasi, bouwplank, direksi keet)
2. Tanah & pondasi (galian, urugan, pondasi, sloof)
3. Struktur (kolom, balok, plat, tangga)
4. Dinding & plesteran
5. Penutup lantai & dinding
6. Plafon & rangka
7. Atap (rangka, penutup, talang)
8. Pintu, jendela, kusen
9. Sanitasi & plumbing
10. Elektrikal & pencahayaan
11. Finishing (cat, coating)
12. Lansekap & pekerjaan luar

Script `scripts/rab_template.py` membuat template CSV (kolom: no, pekerjaan, satuan,
volume, harga_satuan, subtotal) + ringkasan total; konversi ke XLSX via skill `xlsx`
bila klien butuh file Excel.

## Konvensi File & QA

- Folder per fase: `ded/` (gambar), `ded/rks.md`, `ded/rab.csv`, `ded/jadwal.md`.
- Penamaan snake_case; versi kanonik 1 file per deliverable (hindari duplikasi).
- QA (cross-ref gsp-document-quality-standards): semua ruang program muncul di denah;
  dimensi konsisten antar gambar; RKS menyebut SNI; RAB subtotal per pekerjaan; no file
  kosong atau placeholder.

## Pitfalls

- Jangan mencampur skala fase (konsep 1:500 vs DED 1:100) dalam satu paket tanpa label.
- Jangan klaim "gambar DED siap tender" bila daftar gambar tidak lengkap atau dimensi
  tidak konsisten.
- RAB tanpa satuan/volume = estimasi kasar, bukan BOQ; beri label jelas.
- Hindari menyebut merek tanpa dasar spesifikasi (mutu & standar lebih penting).

## Verifikasi

Sebelum selesai: set gambar mencakup arsitektur+struktur+MEP (sesuai skala proyek), RKS punya
referensi SNI, RAB punya subtotal & total, dan ketiganya konsisten (nama item sama antara
gambar-RKS-RAB). Template CSV diuji: `python3 rab_template.py > rab.csv` lalu buka CSV.