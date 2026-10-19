---
record_type: knowledge_card
reference_id: REF-OEM-STG
reference_confidence_level: R4
title: "Lembar data server, SSD, komputer tepi"
domain: STORAGE
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R4_OEM-TECHNICAL/SERVER-STORAGE
---

# REF-OEM-STG — Lembar data server, SSD, komputer tepi

**Tingkat keyakinan:** **R4 — dokumentasi teknis pabrikan** · **19 berkas**
**Laci:** `03_SOURCE-VAULT/R4_OEM-TECHNICAL/SERVER-STORAGE` · **Daftar isi:** `_ISI.md` pada laci yang sama

> **Catatan kurasi (05-10-2026, KORPUS-IDX-REPAIR-1005 G6):** folder kartu ini semula
> berlabel triase `STORAGE-DATACENTER`; dirapikan ke domain `STORAGE` karena kartu ini
> menopang Rantai H milik STORAGE. Kaidah domain: `02_REGISTERS/README.md`.

> **R4 adalah satu-satunya sumber sah untuk angka yang melekat pada produk.** Tidak ada
> buku teks yang dapat menggantikannya, dan tidak boleh ditaksir.

## 1. Yang dipasok

Kapasitas & antarmuka cakram · TBW/DWPD · suhu kerja · daya

## 2. Boleh menetapkan ambang terima?

**Ya — untuk parameter produk yang bersangkutan**, bila produk itu memang yang terpasang
dan kontrak mengikat pada spesifikasinya. **Tidak** untuk ambang yang berasal dari regulasi
atau standar; itu tetap R1/R2.

## 3. Batas pemakaian — baca sebelum mengutip

**Berlaku hanya untuk model dan versi yang tercantum pada berkasnya.** Sebelum angka dari
laci ini masuk dokumen serah:

1. Cocokkan **nomor model** dengan yang benar-benar terpasang — varian yang mirip sering
   berbeda spesifikasi.
2. Cocokkan **versi firmware/perangkat lunak** bila angkanya bergantung padanya.
3. Periksa **tanggal terbit** lembar datanya; pabrikan merevisi tanpa mengganti nama berkas.

⚠ **Tidak memuat unjuk kerja pengendali RAID maupun waktu rekonstruksi** — dua angka itu ditentukan pengendali, bukan cakram. Masih celah R4.

## 4. Menopang rantai

Rantai **H** (kapasitas RAID)

## 5. Gate

Angka dari laci ini ditandai **`OEM-DERIVED`** pada lembar perhitungan (`TPL-02`), bukan
`SOURCE-DERIVED`. Gate **G3** menuntut penandaan itu; gate **G5** menuntut lembar datanya
dilampirkan sebagai bukti.
