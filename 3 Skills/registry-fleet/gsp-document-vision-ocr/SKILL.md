---
name: gsp-document-vision-ocr
description: "OCR scanned PDFs and image decks via GSP fleet agents."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa) — Brahma Orchestrator
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [gsp, vision, ocr, document, fleet, qwen, migration, pdf, pptx]
    category: gsp
  gsp:
    category: library
    tags: [gsp, vision, ocr, document, pdf, pptx, fleet, migration]
---

# GSP Document Vision OCR — ekstraksi dokumen image-based via fleet vision agents

## When to Use

Use this skill when:
- PDF hasil scan tanpa lapisan teks (image-based) perlu diekstrak isinya (OCR).
- Deck PPTX yang murni gambar (0 text run) atau set slide PNG perlu dibaca.
- Ada GAP OCR/vision dalam migrasi dokumen ke Information Library.
- Butuh halaman-verifikasi (kutip `page_XXX.png`) untuk dokumen yang hanya ada
  versi image, dan klaim perlu dirujuk ke halaman nyata.

Jangan dipakai untuk: dokumen dengan lapisan teks (langsung `read_file`),
atau saat vision dipakai untuk desain/generasi gambar (bukan ekstraksi).

## Setup (sekali per mesin)

- Pasang tool render: `pip install pymupdf python-pptx` (pymupdf `fitz` API
  deprecated → `import pymupdf`).
- Render PDF → PNG per halaman (dpi ~120) dan ekstrak media PPTX, staging di
  `legacy-archive/ocr/<source>/` (satu folder per sumber).
- Profil vision fleet (model `qwen/qwen3.7-flash` + auxiliary vision + toolset
  vision): `gsp-image-analyst`, `gsp-image-specialist`,
  `gsp-image-prompt-specialist`, `gsp-design-system-specialist`.
- Dispatch: `hermes -p <profil> -z "<prompt>"` di background + poll log.

## Strategi dispatch worker vision

1. Prompt self-contained: path gambar **ABSOLUT**, perkara, format objek vault,
   aturan fidelitas, target kelas_bukti, output (STATUS/OBJEK/GAP).
2. **Verifikasi folder dulu**: minta worker `ls` path gambar sebelum vision
   (beberapa worker salah path dan mengklaim "folder kosong").
3. **Batch kecil**: maks 5 gambar per panggilan `vision_analyze`.
4. **TULIS INKREMENTAL**: worker meng-append tiap batch ke body tmp file;
   JANGAN menunggu semua selesai baru menulis.
5. **BUAT OBJEK VAULT AWAL** setelah body cukup (`vault_propose.py --body-file`).
6. Dokumen besar (150 hal) → pecah chunk ~50 hal per worker, profil berbeda
   (konkurensi: maks 4 paralel, maks 2 profil sama).
7. Kualitas profil bervariasi: bila satu profil gagal (kosong/hang), coba profil
   lain; jangan retry membabi buta pada profil yang sama.

## Pitfalls KRITIS

- **HALUSINASI VISION NYATA (kasus 2026-08-24).** Worker vision bisa mengarang
  narasi meyakinkan saat vision gagal/stripped. Objek ADINT `p3` mengaku halaman
  101-150 berisi "program ADINT (Anggaran Dana Insentif Teknis) Kementerian
  PUPR" — topik yang SALAH TOTAL (laporan sebenarnya Advertising Intelligence),
  lengkap dengan header BAB/angka palsu, dan worker mengklaim "tanpa loss/gap"
  (= PALSU). **JANGAN percaya klaim sukses penuh.**
- **Cross-verify WAJIB sebelum attest/promote**: bandingkan output OCR dengan
  sumber teks yang ada (ringkasan Phase-1, objek lain, cover PDF, grep arsip).
  Tanda halusinasi: topik tiba-tiba berbeda, akronim diartikan ulang, angka
  tidak punya pendukung di sumber mana pun.
- **vision_analyze intermiten di sesi fleet**: kadang sukses penuh (35-40
  halaman), kadang kosong/stripped (`[screenshot removed to save context]`),
  kadang hang >15m tanpa output. Pelajaran = verifikasi + fallback, bukan
  menyerah pada vision.
- **Fallback yang sah**: gunakan ekstraksi teks yang SUDAH ADA (ringkasan
  Phase-1, objek lain) dengan label JUJUR — kelas_bukti `sekunder` +
  catatan fidelitas "bukan vision". Jangan memaksakan vision; jangan menulis
  objek dari vision yang gagal tanpa pengganti.
- **Kelas_bukti jujur**: vision sukses = `primer`; fallback ringkasan teks =
  `sekunder` (librarian menolak `primer` palsu). Koreksi frontmatter bila perlu.
- **Verifikasi independen (librarian) WAJIB**: penulis ≠ verifikator. Librarian
  berhasil menangkap halusinasi p3 dengan 5 bukti — selalu lewatkan ke kurasi
  librarian, jangan attest sendiri.
- Nama file konsisten (prefix tanggal + slug) — beberapa worker membuat nama
  tanpa prefix (`adint-report-vision-p3.md` vs `2026-08-24_...-p1.md`).
- Body tmp worker tertinggal di workspace — bersihkan/arsipkan setelah objek
  final dibuat.

## Alur lengkap (migrasi / penanganan GAP)

1. Identifikasi GAP OCR/vision (dari laporan kurasi/migrasi).
2. Render & staging gambar (Setup di atas).
3. Dispatch worker vision (Strategi di atas), pantau per-worker.
4. Verifikasi output per worker (cross-check topik/konsistensi) SEBELUM kurasi.
5. Kurasi librarian (independen) → promote langsung / menunggu_persetujuan /
   menunggu_verifikasi / ditolak.
6. Objek sensitif → bulk approval via Approval Inbox HQ (alur
   `gsp-library-bulk-approval`); prinsip: **jangan auto-approve** — cross-check
   tiap item, sajikan kejelasan lengkap, biarkan user yang memutuskan.

## Verification (sebelum klaim selesai)

```
[ ] Objek vault valid frontmatter + sumber relatif benar-benar ada
[ ] Topik objek konsisten dengan sumber (cross-check!) — tanda halusinasi ditolak
[ ] Kelas_bukti jujur (primer hanya bila vision benar-benar sukses)
[ ] Klaim worker "no gap / complete" diverifikasi, bukan dipercaya
[ ] Objek vision yang gagal → fallback teks berlabel sekunder ATAU ditolak, bukan dipromosikan
[ ] Hasil kurasi librarian tercatat (promote/langsung/menunggu/ditolak)
```
