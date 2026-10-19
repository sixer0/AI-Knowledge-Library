---
name: digital-forensics-evidence-system
description: Use when managing digital evidence or forensic workflows.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, forensics, digital-evidence, chain-of-custody, dems, cybersecurity]
  hermes:
    tags: [gsp, forensics, evidence]
    related_skills: [pustaka-teknis, dems-polri-proposal-architect]
---

# Digital Forensics Evidence System — Penanganan Bukti Digital (DEMS)

## When to Use

- Merancang **sistem manajemen bukti digital** (DEMS) untuk penegak hukum/instansi:
  pengumpulan, pengawetan, integritas, rantai kustodi, keterterimaan.
- Menyusun prosedur forensik: acquisition, examination, analysis, reporting.

## ⚠ Keadaan rak (jujur sejak awal)

- Korpus PUNYA: **proses forensik 4 tahap + rantai kustodi** dari Alsmadi (NICE Framework,
  Bab 11, PDF 268) [R3] · kerangka keamanan Anderson [R3] · penunjuk regulasi Indonesia via
  tesis [R5]: **UU 11/2008 (ITE)** dan **Peraturan BSSN No. 4/2021**.
- Korpus TIDAK punya: **NIST SP 800-86** dan **ISO/IEC 27037** (standar inti penanganan
  bukti) — GAP-ACQUISITION-PLAN prioritas 3, tersedia gratis dari sumber resmi.
- **Konsekuensi**: proses boleh dirancang dari R3; **kepatuhan/penerimaan bukti versi
  normatif tidak dapat dinyatakan** tanpa standar aslinya. Jangan menulis "sesuai ISO 27037".

## Alur kerja

1. **Identifikasi aset bukti** & sumber: media (HDD/SSD/memori/ponsel), log, cloud.
2. **Proses 4 tahap** [R3 — Alsmadi Bab 11 PDF 268]: collection → examination → analysis →
   reporting. Jangan dibalik; tiap tahap punya keluaran + jejak.
3. **Rantai kustodi**: siapa memegang, kapan, di mana, perubahan hash — setiap perpindahan
   tercatat dan diverifikasi. Integritas: hash (SHA-256) sebelum & sesudah setiap langkah
   [kerangka Anderson: integritas catatan].
4. **Pengawetan**: bekerja pada salinan forensik (write-blocker), simpan media asli sebagai
   bukti prima.
5. **Regulasi Indonesia (PENUNJUK saja — R5)**: tesis menyebut UU 11/2008 & Perban BSSN
   4/2021. Yang dikutip dalam dokumen resmi harus **teks regulasi aslinya (R1)** — belum ada
   di rak; nyatakan atau minta salinannya.
6. **Uji/verifikasi**: integritas hash, kesesuaian prosedur, rantai kustodi lengkap.

## Yang DILARANG

- Menyatakan kepatuhan terhadap NIST 800-86 / ISO 27037 / UU ITE tanpa memegang
  dokumen aslinya.
- Menulis prosedur "forensik" tanpa jejak rantai kustodi dan hash.
- Mengutip tesis sebagai dasar hukum — tesis adalah penunjuk, bukan sandaran (R5).

## Verifikasi sebelum mengklaim selesai

- Proses 4 tahap terdokumentasi dengan keluaran tiap tahap ✓
- Rantai kustodi: format isian + contoh terisi, setiap transisi hash ✓
- Regulasi: penanda "menunggu salinan resmi" atau tidak disebut ✓
- Artefak DEMS (rancangan) dapat diaudit: siapa-siapa-kapan-di mana ✓