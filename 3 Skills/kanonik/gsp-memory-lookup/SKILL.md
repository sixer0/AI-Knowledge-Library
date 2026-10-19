---
name: gsp-memory-lookup
description: "Cari & baca memory GSP on-demand: index L0 → file refs L1 → snapshot arsip. Pasangan wajib dari gsp-memory-tiering."
version: 1.0.0
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, memory, lookup]
    category: orchestration
---

# GSP Memory Lookup — muat ingatan kerja on-demand (L0 → L1)

## When to use
- WAJIB dimuat setiap kali MEMBACA/MENCARI memory untuk tugas yang sedang berjalan:
  butuh detail entri yang sudah diarsipkan, verifikasi fakta lingkungan, atau
  melanjutkan kerja task sebelumnya.
- Pasangan wajib skill `gsp-memory-tiering` (yang menulis, ini yang membaca).

## Prosedur pencarian (bertingkat, murah → mahal)
1. **L0 — index di memory utama**: baca entri INDEX kategori di MEMORY.md (auto-inject).
   Tentukan kategori yang relevan (mis. #dispatch-bridge, #ekas, #skills).
2. **L1 — master index arsip**: baca `C:/Users/TRIAL/workspace/gsp-hermes/workspace/memory/refs/_INDEX.md`.
   Cocokkan kategori/tanggal/profil → dapatkan path file refs.
3. **L1 — file refs**: baca file spesifik `memory/refs/<profil>/<YYYY_MM_DD>_<slug>.md`
   (verbatim, dikelompokkan `## #kategori`). Muat HANYA file yang dirujuk — jangan
   baca semua arsip.
4. **L2 — kompaksi kategori**: jika kategori sudah digabung, entri kategori di L0
   menunjuk langsung ke file refs gabungan; buka file itu.
5. **Fallback**: `session_search` untuk riwayat percakapan yang tidak masuk arsip refs;
   `search_files(target=content)` di folder `memory/refs/` untuk keyword bebas.

## Konvensi lokasi
- Shared ws: `C:/Users/TRIAL/workspace/gsp-hermes/workspace/memory/refs/`
  - `_INDEX.md` = master index (kategori → file → ringkasan → profil).
  - `<profil>/<YYYY_MM_DD>_<slug>.md` = arsip verbatim per profil per kejadian.
- Memory profil: `$LOCALAPPDATA/hermes/memories/MEMORY.md` (default) /
  `$LOCALAPPDATA/hermes/profiles/<p>/memories/MEMORY.md` (profil lain); pemisah entri `§`.

## Pitfalls
- JANGAN menyimpulkan "tidak ada" hanya dari L0 — L0 sengaja ringkas; cek `_INDEX.md` dulu.
- File refs adalah VERBATIM snapshot: jangan edit isinya; koreksi = entri baru + index baru.
- Path Windows: pakai forward-slash saat menulis token MEDIA/CLI.

## Verification
- Setiap klaim dari arsip disertai path file refs asalnya (bukti, bukan ingatan kabur).
- Akhiri respons: `STATUS: complete|needs-review|blocked|failed` + `ARTIFAK: <path file refs yang dibaca>`.
