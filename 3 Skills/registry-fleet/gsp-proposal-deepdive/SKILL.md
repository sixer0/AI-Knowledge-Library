---
name: gsp-proposal-deepdive
version: 1.0.2
description: >-
  Use when deep-diving a technical proposal into a GSP report.
metadata:
  hermes:
    tags: [gsp, proposal, deep-dive, research, vendor, due-diligence, report]
    category: gsp
  gsp:
    category: engineering
    tags: [gsp, proposal, deep-dive, research, vendor, report]
---

# GSP Proposal Deep-Dive — pendalaman komprehensif dokumen teknis/proposal


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
## When to Use

Use this skill when the user hands over a technical proposal / engineering
report (PDF, PPTX, DOCX) and asks for a **comprehensive deep-dive**, typically
with some or all of: (1) deconstruct the proposal into parts and test the truth
of every assumption, (2) categorize and catalog the solution/vendor landscape
worldwide, (3) per-vendor dossiers checking each vendor's website, (4) due
diligence enrichment, (5) competitive industry landscape per vendor, (6) final
deliverable as an official GSP document. Works for ADINT-class intel proposals
and any engineering/defence/tech proposal.

## Workflow (fase)

### Fase 0 — Ekstraksi & pembacaan penuh (JANGAN langsung OCR)
1. **Preflight lapisan teks dulu**: `read_file` kadang SALAH melaporkan
   "PDF has no extractable text / OCR is required" pada PDF yang sebenarnya
   punya lapisan teks penuh (kasus nyata: GSP-TR-ADINT-2026, 150 hal,
   read_file bilang "OCR required" tapi pymupdf mengekstrak 426.885 karakter,
   0 halaman kosong). Probe:
   ```bash
   python -c "import pymupdf; d=pymupdf.open(PATH); t=[len(d[i].get_text().strip()) for i in range(len(d))]; print('total',sum(t),'empty',sum(1 for x in t if x<50))"
   ```
   Total >> 0 dan sedikit halaman kosong → ekstrak teks, bukan OCR vision.
   Detail lengkap: skill `gsp-document-vision-ocr` →
   [`skills/gsp/gsp-document-vision-ocr/references/pymupdf-text-layer-preflight.md`](../gsp-document-vision-ocr/references/pymupdf-text-layer-preflight.md).
2. Ekstrak teks ke Markdown dengan penanda halaman untuk sitasi:
   `<!-- ===== PAGE N ===== -->` per halaman.
3. **Baca baris per baris TANPA terlewat** (user eksplisit minta). Dokumen 150
   hal ≈ 8.000+ baris; baca dalam chunk 1000 baris via read_file.

### Fase 1 — Dekomposisi (sebelum orkestrasi)
- Tulis `00_decomposition.md`: struktur dokumen (bab/lampiran), peta asumsi
  kunci (beri nomor), daftar vendor per kategori, rencana eksekusi.
- Tulis `vendor_lists.md`: daftar vendor per kategori (nama, origin, produk,
  website) — bahan yang akan dibaca subagen.
- Identifikasi label keyakinan dokumen ([PUBLIC]/[ASSESSED]/[VENDOR]/[ESTIMATE]/
  [UNVERIFIED]) dan pertahankan konvensinya di laporan.

### Fase 2 — Orkestrasi riset paralel (subagen)
- Pecah kerja: (1) verifikasi asumsi teknis, (2-4) dossier vendor per kelompok
  kategori, (5) landscape industri. Maks ~4 subagen paralel.
- **Setiap subagen menulis ke output path UNIK** (isolasi paralel):
  `research/01_*.md`, `dossier/01_*.md`, `dossier/02_*.md`, dst. Dua subagen
  TIDAK boleh menulis file yang sama.
- Prompt subagen wajib berisi: path daftar vendor, format output per vendor,
  label [VENDOR] untuk klaim pemasaran, instruksi "JANGAN mengarang; website
  mati = tulis mati; angka coverage = VENDOR CLAIM", dan path output absolut.
- **Arahkan subagen ke web_search/web_extract, LARANG browser_exec** — di
  subagen, browser_exec sering timeout 420s dan steering tidak bisa memotong
  tool call yang sedang berjalan. Task besar (46 vendor) wajar 20-30 menit.
- Verifikasi file output subagen benar-benar ADA (subagen kadang menulis
  bahan di raw/ tapi lupa file final) dan konsisten topiknya.

### Fase 3 — Verifikasi mandiri orkestrator (paralel dengan subagen)
- Orkestrator melakukan verifikasi langsung klaim-klaim kunci (jangan serahkan
  semua ke subagen): cari sumber primer (regulator, spek, jurnal, investigasi).
- **Hemat web_search**: ada guardrail ~50 panggilan web_search per turn
  (loop_web_search_cap). Pakai web_extract untuk URL yang sudah dikenal,
  batch pencarian, dan serahkan penelusuran massal ke subagen.
- Catat temuan ke `report/09_koreksi_temuan.md` (koreksi asumsi, angka vendor
  yang berubah, status hukum yang kedaluwarsa).

### Fase 4 — Sintesis laporan resmi GSP
- Struktur: Ringkasan Eksekutif → Metodologi → Dekomposisi → Uji Asumsi →
  Kategorisasi Solusi → Dossier Vendor → Due Diligence → Landscape → Koreksi &
  Temuan Kritis → Rekomendasi → Lampiran (peta korelasi proposal↔temuan,
  daftar vendor, bibliografi).
- Tulis file master `GSP-TR-<TOPIC>-DEEP-2026.md` + skrip rakit yang menggabungkan
  bagian-bagian + output subagen (jalankan saat semua subagen selesai).
- Tandai klasifikasi (GSP-CONFIDENTIAL) dan tanggal pemeriksaan.

## Pitfalls

- **read_file "OCR required" ≠ image-based.** Selalu probe pymupdf dulu
  (Fase 0). Mengirim 150 hal ke OCR vision = buang waktu + rawan halusinasi.
- **Subagen hang di browser_exec**: timeout ~420s; steering baru berlaku
  SETELAH tool call selesai — tidak bisa memotong. Cegah: larang browser di
  prompt awal.
- **Klaim sukses subagen = self-report**: cek file output ada dan isinya
  konsisten (pola: subagen menulis bahan di raw/ tapi lupa file final).
- **Angka vendor (coverage/labels) = klaim pemasaran**: selalu label [VENDOR],
  rekonfirmasi ke situs live, dan catat tanggal pemeriksaan.
- **Jangan ulangi web_search setelah guardrail** (loop_web_search_cap) — ganti
  strategi (web_extract, subagen), bukan retry panggilan yang sama.

## Verification (sebelum klaim selesai)

```
[ ] Teks sumber diekstrak penuh (bukan OCR bila ada lapisan teks)
[ ] Dokumen dibaca baris per baris tanpa lompat
[ ] Setiap subagen: file output ada + topik konsisten + output path unik
[ ] Asumsi kunci diverifikasi dengan sumber primer; yang tak terverifikasi diberi label [UNVERIFIED]
[ ] Laporan final menyatukan SEMUA bagian (tidak ada bab placeholder)
[ ] Klasifikasi dokumen + tanggal pemeriksaan tercantum
```

## Referensi
- [`references/adint-deepdive-2026-08.md`](references/adint-deepdive-2026-08.md) — studi kasus pendalaman proposal
  ADINT 150 hal (dekomposisi, orkestrasi, temuan koreksi, pitfalls nyata).
- Ekstraksi teks: skill `gsp-document-vision-ocr` (skills/gsp/gsp-document-vision-ocr/references/pymupdf-text-layer-preflight.md).
- Orkestrasi fleet: skill `gsp-orchestrator-worker` (workflow default Brahma).
