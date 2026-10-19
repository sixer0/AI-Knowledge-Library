---
name: grounding-lightning-design
description: Use when designing grounding or lightning protection.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, grounding, lightning, wenner, fall-of-potential, rolling-sphere]
  hermes:
    tags: [gsp, grounding, lightning]
    related_skills: [pustaka-teknis]
---

# Grounding & Lightning Design — Pembumian dan Proteksi Petir

## When to Use

- Merancang **sistem pembumian** (elektroda, grid, bonding) dan **proteksi petir**
  (rolling sphere, tingkat proteksi).
- Menyusun **uji pembumian** (Wenner/fall-of-potential) dan verifikasi zona lindung.

Kanonik: `ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/RANTAI-JAMINAN.md` + resume
Joffe & Lock / Uman · ASUMSI-BAKU §C.

## ⚠ Baca ini dulu: rantai PUTUS di mata ④

Rak ini **tidak memiliki sumber sah untuk ambang resistansi pembumian** (tidak R1, tidak R2).
PUIL/SNI [R1] kosong. **Menghitung metode boleh; menyatakan lulus TIDAK** tanpa sumber sah.
Tiga jalan sah: (1) pemilik menetapkan ambang tertulis, (2) kontrak mengadopsi standar
tertentu, (3) lapor hasil ukur **tanpa pernyataan lulus**.
Yang **tidak** sah: mengisi "< 5 Ω" karena angka itu sering terdengar.

Jangan tertukar: rak PUNYA ambang **tahanan isolasi** (MΩ, NETA Tabel 100.1 [R2]) — itu
**bukan** ambang **resistansi pembumian** (Ω).

## Alur wajib (urut — jangan dibalik)

1. **Ukur resistivitas tanah DULU** (metode Wenner, `ρ = 2πaR`) [R3 — Joffe PDF 579–580].
   **Resistivitas tidak boleh diasumsikan** — survei wajib; tanpa itu seluruh desain tebak-tebakan.
2. **Tentukan ambang yang dituju** → wajib dari pemilik/standar mengikat (lihat ⚠ di atas).
3. **Desain elektroda**: jumlah, kedalaman, jarak — dari resistivitas terukur & lapisan tanah
   (survei multi-jarak `a`).
4. **Bonding & ekipotensial** (daftar periksa Apendiks G Joffe) [R3 — PDF 1111].
5. **Proteksi petir**: tentukan tingkat proteksi → **rolling sphere** (Tabel 4.1 Uman —
   tersimpan sebagai GAMBAR tabel, buka PDF 89–90 langsung) [R3 — Uman PDF 89–90].
   ⚠ Ukuran mesh BUKAN pengganti analisis bola gelinding [PDF 90].
6. **Proteksi surja internal** — proteksi eksternal saja ditolak (kerusakan berulang umumnya
   karena ketiadaan proteksi internal).
7. **Uji**: fall-of-potential tiga pasak; **konduktor penghubung WAJIB dilepas dari
   elektroda sebelum diukur** — satu baris yang menentukan keabsahan hasil [R3 — PDF 580].

## Rujukan inti

| Sumber | R | Memasok | Halaman |
|---|---|---|---|
| Joffe & Lock, *Grounds for Grounding* (2023) | R3 | Wenner, fall-of-potential, bonding, daftar periksa | PDF 562, 579–580, 1111, 1149 |
| Uman, *The Art and Science of Lightning Protection* (2008, ⚠18 th) | R3 | Rolling sphere, tingkat proteksi — mengutip IEC 62305:2006 (usang) | PDF 89–90 |
| PUIL / SNI pembumian | R1 | Ambang resistansi yang mengikat | ❌ TIDAK ADA |
| SNI / IEC 62305 edisi berlaku | R1/R2 | Tingkat proteksi yang mengikat | ❌ TIDAK ADA — Uman kutip edisi 2006 |

## Verifikasi sebelum mengklaim selesai

- Survei resistivitas ada (bukan asumsi) — nilai + metode Wenner ✓
- Ambang lulus: penetapan pemilik / kontrak / laporan tanpa pernyataan lulus — TERTULIS ✓
- Desain elektroda dari resistivitas terukur; bonding/ekipotensial tercakup ✓
- Zona lindung petir terhadap rancangan bola gelinding; catat edisi standar yang dipakai ✓
- BA memuat pernyataan "konduktor penghubung telah dilepas sebelum pengukuran" ✓
- Tidak ada klaim lulus dengan angka tanpa sumber ✓