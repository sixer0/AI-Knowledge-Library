---
name: dems-polri-proposal-architect
description: Use when structuring DEMS proposals for law enforcement.
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, dems, proposal, polri, forensics, evidence]
  hermes:
    tags: [gsp, dems, proposal]
    related_skills: [digital-forensics-evidence-system, pustaka-teknis]
---

# DEMS POLRI Proposal Architect — Arsitektur Proposal Sistem Bukti Digital

## When to Use

- Menyusun/meninjau **proposal atau dokumen tender sistem manajemen bukti digital**
  (DEMS) untuk penegak hukum: arsitektur, alur kerja, kepatuhan, jaminan mutu.

## ⚠ Batas yang wajib dijaga di proposal

- Korpus mendukung **proses & arsitektur** (Alsmadi [R3], Anderson [R3], tesis penunjuk [R5]).
- Korpus TIDAK mendukung **klaim kepatuhan normatif**: NIST SP 800-86, ISO/IEC 27037,
  UU 11/2008, Perban BSSN 4/2021 — belum ada di rak.
- **Aturan proposal**: janji yang tidak dapat diperiksa GSP sendiri tidak boleh ditulis.
  Tulis "mengacu pada ... setelah salinan resmi diperoleh dan diverifikasi".
- Kutip penunjuk [R5] hanya sebagai konteks; dasar klaim di dokumen resmi harus [R1].

## Alur menyusun proposal (kerangka yang dapat dipertanggungjawabkan)

1. **Kebutuhan & lingkup** (dari pemberi kerja): jenis bukti, volume, retensi, instansi.
2. **Arsitektur DEMS**: alur 4 tahap (collection → examination → analysis → reporting)
   dipetakan ke modul sistem; rantai kustodi sebagai tulang punggung.
3. **Modul fungsi**: intake/registrasi bukti · pengawetan & imajing (write-blocker, hash) ·
   penyimpanan bukti (RAID, lihat hw-sw-config-master) · kendali akses & log · pelaporan.
4. **Jaminan mutu**: setiap modul punya uji terima; integritas hash diuji; rantai kustodi
   diuji alurnya (siapa-siapa-kapan).
5. **Kepatuhan**: tabel ringkas "acuan & status bahan" — jujur mana yang dimiliki,
   mana yang menunggu salinan resmi.
6. **Risiko & asumsi**: asumsi dinyatakan + sensitivitas (ASUMSI-BAKU); blocker regulasi
   disajikan sebagai risiko yang dimitigasi, bukan disembunyikan.

## Yang DILARANG di proposal

- "Sesuai ISO/IEC 27037" / "sesuai UU ITE" tanpa memegang dokumennya.
- Angka kapasitas/kinerja produk tanpa lembar data (R4).
- Overpromise analitik forensik tanpa spesifikasi unjuk kerja terukur.

## Verifikasi sebelum proposal dinyatakan selesai

- Arsitektur memetakan 4 tahap forensik + rantai kustodi ✓
- Tiap klaim kepatuhan punya status bahan (dimiliki / menunggu / tidak tersedia) ✓
- Asumsi & risiko tertulis; blocker regulasi dimitigasi eksplisit ✓
- Angka produk dari R4; referensi silang ke skill terkait ✓