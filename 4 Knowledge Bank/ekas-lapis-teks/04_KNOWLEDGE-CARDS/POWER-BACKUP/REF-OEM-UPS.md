---
record_type: knowledge_card
reference_id: REF-OEM-UPS
reference_confidence_level: R4
title: "Katalog UPS Riello (190 hal)"
domain: POWER-BACKUP
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R4_OEM-TECHNICAL/UPS
---

# REF-OEM-UPS — Katalog UPS Riello (190 hal)

**Tingkat keyakinan:** **R4 — dokumentasi teknis pabrikan** · **1 berkas**
**Laci:** `03_SOURCE-VAULT/R4_OEM-TECHNICAL/UPS` · **Daftar isi:** `_ISI.md` pada laci yang sama

> **R4 adalah satu-satunya sumber sah untuk angka yang melekat pada produk.** Tidak ada
> buku teks yang dapat menggantikannya, dan tidak boleh ditaksir.

## 1. Yang dipasok

Topologi · efisiensi pada beban parsial · daya keluaran · waktu cadangan menurut modul baterai

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

Efisiensi berubah menurut **beban parsial** — angka pada beban 100% menyesatkan bila sistem berjalan di 30%. Ambil dari kurva, bukan satu angka.

## 4. Menopang rantai

Rantai **C** — menutup butir *efisiensi UPS* yang dilarang diambil dari Emadi (2004)

## 5. Gate

Angka dari laci ini ditandai **`OEM-DERIVED`** pada lembar perhitungan (`TPL-02`), bukan
`SOURCE-DERIVED`. Gate **G3** menuntut penandaan itu; gate **G5** menuntut lembar datanya
dilampirkan sebagai bukti.
