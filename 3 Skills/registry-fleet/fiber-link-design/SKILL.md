---
name: fiber-link-design
description: Use when designing or testing fiber optic link budgets.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, fiber, optic, loss-budget, otdr, ols, iec-61280]
  hermes:
    tags: [gsp, fiber-optics]
    related_skills: [pustaka-teknis]
---

# Fiber Link Design — Loss Budget, Uji & Berita Acara

## When to Use

- Merancang **jalur serat optik**: loss budget, pemilihan komponen, margin.
- Menyusun **prosedur uji & berita acara** (OTDR/OLTS, ambang lulus, ORL).
- Menyelesaikan perselisihan hasil ukur (RTM).

Kanonik: `ekas/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/RANTAI-JAMINAN.md` · resume Hayes (FOA)
& JDSU di folder yang sama · BA §1 di `ekas/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md`.

## Alur wajib (urut — jangan dibalik)

1. **Kumpulkan konfigurasi jalur**: jenis serat (OS/OM), panjang, jumlah konektor
   (tiap patch panel = sepasang), jumlah sambungan, panjang gelombang uji (1310/1550 nm,
   atau sesuai transceiver).
2. **Hitung loss budget** (lihat `references/01-loss-budget-dan-uji.md`) untuk tiap λ.
3. **Bandingkan dengan anggaran daya transceiver (R4)**.
4. **Tetapkan ambang lulus = kolom terburuk** (worst case) [R3 — Hayes PDF 145] —
   bukan rata-rata, bukan angka terbaik.
5. **Susun prosedur uji**: metode (OFSTP-7 SM / OFSTP-14 MM / IEC 61280-4-2), pilihan
   test cord (one/three/two-cord), alat wajib OLTS/LSPM (OTDR pelengkap), kabel referensi
   (rugi ≤ 0,5 dB, uji FOTP-171).
6. **Bila OTDR dipakai**: catat λ, lebar pulsa, rentang, averaging, indeks bias, panjang
   launch/receive cable — tanpa itu jejak tak dapat ditafsirkan ulang.
7. **BA**: lampirkan ambang + rincian hitungannya (butir paling sering hilang).

## Angka kunci loss budget (SM)

| Komponen | Nilai | Sumber |
|---|---|---|
| Rugi serat SM premises | **1,0 dB/km** | R3 — Hayes PDF 129 |
| Rugi serat SM outside plant | **0,5 dB/km** | R3 — Hayes PDF 129 |
| Rugi konektor | **0,75 dB** (batas TIA-568) | R3 — Hayes PDF 129 |
| Rugi sambungan fusi | 0,1–0,3 dB | R3 · R4 bila alat menyebut lain |

> Aturan Hayes: **jangan memakai spesifikasi terbaik.** Bila ragu, ambil yang lebih buruk —
> margin itulah yang menyelamatkan saat pelaksanaan tidak sempurna.

## Standar uji

| Standar | R | Peran | Halaman |
|---|---|---|---|
| **IEC 61280-4-2:2014** | R2 | Empat metode uji redaman SM · RTM · ORL | PDF 14, 17, 20, 43 |
| Hayes FOA Reference Guide | R3 | Rumus loss budget, batas komponen, praktik | PDF 129, 145 |
| JDSU Fiber Optic Testing Vol 1 | R3 | OTDR, ketidakpastian ukur | cetak 37 / PDF 44 |

**Batas cakupan**: IEC 61280-4-2 = singlemode; multimode = IEC 61280-4-1 (**tidak ada di rak**).
Perselisihan hasil ukur diselesaikan dengan **RTM** [R2 — PDF 14].

## Verifikasi sebelum mengklaim selesai

- Loss budget terhitung per λ, ambang = kolom terburuk ✓
- Anggaran daya transceiver (R4) dibandingkan, bukan diasumsikan ✓
- Metode uji + pilihan test cord disebut (IEC 61280-4-2) ✓
- Kabel referensi ≤ 0,5 dB dan dikalibrasi ✓
- BA memuat: data jalur, ambang + rincian hitungan, hasil per λ, alat + kalibrasi ✓
- Bila data pabrikan (rugi sambungan, daya transceiver) belum ada → "menunggu data pabrikan" ✓