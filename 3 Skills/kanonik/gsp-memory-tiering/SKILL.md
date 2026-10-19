---
name: gsp-memory-tiering
description: "Tulis & rawat memory GSP bertingkat: L0 pinned+index+recent, L1 arsip refs lossless, L2 kompaksi per kategori. Pasangan wajib: gsp-memory-lookup."
version: 1.0.0
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, memory, tiering]
    category: orchestration
---

# GSP Memory Tiering — menulis memory TANPA menghilangkan ingatan kerja

## When to use
- WAJIB dimuat setiap kali akan MENULIS, MENGUBAH, MENGHAPUS, atau MEMAMPATKAN
  entri memory (memory tool / MEMORY.md profil mana pun).
- Trigger: memory penuh/over-limit, compaction, atau users meminta merapikan memory.

## Arsitektur 3 tingkat
| Tingkat | Lokasi | Isi | Batas |
|---|---|---|---|
| **L0** | MEMORY.md profil (di-inject tiap turn) | Aturan PINNED (full-text, TIDAK BOLEH DIHAPUS) + INDEX kategori (1 baris/kategori → rujukan file refs) + RECENT TASK (terbaru saja) | tetap lean; target <50% kapasitas |
| **L1** | `<shared-ws>/memory/refs/<profil>/<YYYY_MM_DD>_<slug>.md` | Arsip lossless verbatim entri yang keluar dari L0 | tak terbatas; dibaca on-demand |
| **L2** | entri index di L0 | Bila index penuh: gabungkan baris index se-kategori jadi 1 entri kategori; detail rinci tetap di L1 | 1 entri per kategori |

Shared ws default: `C:/Users/TRIAL/workspace/gsp-hermes/workspace`. Master index arsip:
`memory/refs/_INDEX.md` (kategori → file → ringkasan 1 baris → profil).

## Prosedur menulis / compaction (JANGAN lossy)
1. **Baca semua entri** yang akan tersentuh (jangan compaction buta).
2. **Snapshot lossless dulu**: entri yang keluar dari L0 ditulis VERBATIM ke
   `memory/refs/<profil>/<YYYY_MM_DD>_<slug>.md` (dikelompokkan per kategori `## #kategori`).
3. **Perbarui `memory/refs/_INDEX.md`**: tambah 1 baris per file arsip
   (`| tanggal | kategori | file | ringkasan | profil |`).
4. **Tulis ulang L0**: PINNED tetap utuh di atas → baris index per kategori → recent task.
   Gunakan SATU batch memory tool (add+replace+remove atomik), bukan beberapa call.
5. **Verifikasi**: char usage L0 turun & <50%; setiap kategori di index punya file refs;
   PINNED masih ada; tidak ada entri yang hilang tanpa arsip (bandingkan jumlah sebelum/sesudah).

## Aturan PINNED (copy verbatim — jangan diringkas)
Lihat entri `ATURAN MEMORY MANAGEMENT (PINNED` di MEMORY.md profil masing-masing;
teks kanonik juga tersimpan di `memory/refs/_INDEX.md#teks-pinned`. Aturan itu:
dilarang dihapus/di-strip saat compaction, harus ada di SEMUA profil.

## Pitfalls
- **Lapor tanpa eksekusi = melanggar aturan pinned sendiri (kejadian 03-09)**: bila
  usage L0 >=90% dan user menyentuh budget memory, jalankan kompresi penuh
  (arsip -> index -> batch -> verifikasi) sebagai SATU tugas; JANGAN berhenti di
  laporan + penawaran "mau saya jalankan?". Aturan pinned sudah dianggap user
  sebagai persetujuan. Menunggu restu = kelas T5 (gap eksekusi controller).
- **Anchor arsip WAJIB identik dengan rujukan L0**: nama `## #kategori` di file refs
  ditulis DARI daftar rujukan yang akan dipakai L0, bukan menyalah-tempel nama
  kategori dari snapshot arsip lama (kejadian 03-09: `#fleet-models` vs rujukan L0
  `#fleet-model`, `#infra-pitfalls` vs `#pitfall-mesin`; lolos dari pembacaan
  manusia, tertangkap verifikasi regex).
- **Profil lean tidak me-resolve skill ini via skill_view** (pitfall #skills 02-09):
  baca langsung kanonik `~/workspace/gsp-hermes/skills/gsp-memory-tiering/SKILL.md`
  atau registry fleet; patch pun langsung ke kedua berkas itu via file tools.
- **Menutup kartu kanban misi**: `complete` ditolak saat run worker masih hidup ->
  `hermes kanban reclaim <id>` dulu baru `complete --result "<bukti angka>"`.
- **Strip = lossy**: menghapus entri tanpa arsip menghilangkan ingatan kerja permanen
  (insiden 29-08-2026: 31 entri nyaris ter-strip; hanya bersurvival lewat snapshot).
- Memory tool all-or-nothing: batch gagal → ulangi batch UTUH, jangan sebagian.
- CRLF Windows: tulis file refs via write_file (aman); hindari patch berisi \r\n.
- Profil lain punya MEMORY.md sendiri (`$LOCALAPPDATA/hermes/profiles/<p>/memories/MEMORY.md`,
  default: `$LOCALAPPDATA/hermes/memories/MEMORY.md`); pisah baris entri = `§`.

## Verification
- `_INDEX.md` berisi baris untuk setiap file arsip; file arsip ada di disk.
- L0 = PINNED + index + recent saja; usage <50%.
- Jalankan `scripts/verify_tiering.py [profil]` (uv run --python 3.11) — probe
  deterministik: PINNED posisi 1, semua entri pointer, anchor L0==anchor refs,
  terdaftar di _INDEX.md. Exit non-zero = ada temuan.
- Akhiri respons: `STATUS: complete|needs-review|blocked|failed` + `ARTIFAK: <path _INDEX.md>`.
