---
name: rcm-analysis
description: Use when planning maintenance intervals or reliability work.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, rcm, reliability, fmea, maintenance, ffi, p-f]
  hermes:
    tags: [gsp, rcm, reliability]
    related_skills: [pustaka-teknis, power-backup-sizing]
---

# RCM Analysis — Keandalan & Interval Pemeliharaan

## When to Use

- Menyusun **program pemeliharaan** (preventive/on-condition) untuk aset: genset, UPS,
  baterai, perangkat proteksi, switch, server, peralatan elektrikal.
- Menjawab pertanyaan RCM: *"berapa interval uji/pemeriksaan?"*, *"tugas apa yang layak?"*,
  *"failure-finding kapan?"*.
- Menyusun analisis FMEA/FFMEA dan klasifikasi konsekuensi kegagalan.

Kanonik: `ekas/05_DOMAIN-KNOWLEDGE/RCM/RANTAI-JAMINAN.md` · resume Moubray / Gulati /
Nyman & Levitt di `ekas/05_DOMAIN-KNOWLEDGE/RCM/`.

## Alur wajib (urut — jangan dibalik)

1. **Konteks operasi ditetapkan dulu** — fungsi, standar unjuk kerja (terukur), konteks
   lingkungan. Menyalin program dari proyek lain **ditolak**: fungsi sama pada konteks
   berbeda menghasilkan tugas berbeda.
2. **Tujuh pertanyaan RCM** [R3 — Moubray PDF 31 dst.]: fungsi → kegagalan fungsi → moda →
   akibat → konsekuensi → (apa yang dapat mencegah) → (proteksi jika gagal).
3. **Klasifikasi konsekuensi**: hidden · safety/environmental · operational · non-operational.
   **89% moda kegagalan tidak terkait umur** — jangan otomatis overhaul berkala [R3 — PDF 31].
4. **Pilih jenis tugas** sesuai Decision Diagram:
   on-condition → restorasi → pembuangan → failure-finding (FF).
   Overhaul berkala HANYA bila moda terkait umur dan tugas itu layak secara teknis + berharga.
5. **Hitung interval** (rumus di `references/01-rumus-interval.md`).
6. **Sasaran MTBF kegagalan majemuk = keputusan PEMILIK**, bukan perancang. Tanpa itu,
   tulis menunggu keputusan tertulis.
7. **Uji kelayakan dua tahap** untuk tiap tugas: layak secara teknis DAN berharga.
8. Setiap tugas FF (fungsi tersembunyi) wajib **proteksi pengganti** saat pelaksanaan
   (dua proteksi jangan dilepas bersamaan) [R3 — PDF 193].

## Aturan yang paling sering dilanggar

- Interval "servis tiap 6 bulan" tanpa dasar → **ditolak**. Interval dari hitungan FFI/P-F.
- MTBF dari pengalaman → asumsi baku, bukan fakta: tandai `ASSUMPTION` + sensitivitas.
- Mencampur program pemeliharaan proyek A ke proyek B tanpa menetapkan konteks operasi.
- Analisis tanpa bukti (minimal tabel moda × konsekuensi × tugas × interval).

## Rujukan inti

| Sumber | R | Memasok | Halaman |
|---|---|---|---|
| Moubray, *RCM II* (1997, ⚠29 th — metodologi tetap acuan) | R3 | 7 pertanyaan, P-F, FFI, konsekuensi, pola kegagalan | PDF 31, 164, 166, 193, 195, 198 |
| Gulati, *Maintenance & Reliability Best Practices* (2021) | R3 | Tata kelola, KPI pemeliharaan | — |
| Nyman & Levitt, *Maintenance Planning, Coordination and Scheduling* (2010) | R3 | Perencanaan & penjadwalan kerja | — |

**Jawaban "tidak ada di rak"**: ambang kepatuhan hukum, standar nasional, dan angka produk
(MTBF pabrikan) tidak ada di korpus — R1 kosong, R4 per proyek.

## Verifikasi sebelum mengklaim selesai

- Konteks operasi tertulis SEBELUM analisis ✓
- Tiap moda punya konsekuensi terklasifikasi ✓
- Tiap tugas lulus uji kelayakan teknis + berharga ✓
- Interval dari hitungan (FFI/P-F), bukan kebiasaan ✓
- Sasaran kegagalan majemuk disetujui pemilik (atau status menunggu tertulis) ✓
- Tugas FF punya proteksi pengganti ✓
- Artefak: tabel moda × konsekuensi × tugas × interval + ringkasan program pemeliharaan.