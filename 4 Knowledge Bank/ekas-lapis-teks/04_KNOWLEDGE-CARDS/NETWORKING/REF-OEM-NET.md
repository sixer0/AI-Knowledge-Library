---
record_type: knowledge_card
reference_id: REF-OEM-NET
reference_confidence_level: R4
title: "Lembar data perangkat jaringan, PBX, interkom"
domain: NETWORKING
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R4_OEM-TECHNICAL/NETWORK
---

# REF-OEM-NET — Lembar data perangkat jaringan, PBX, interkom

**Tingkat keyakinan:** **R4 — dokumentasi teknis pabrikan** · **28 berkas**
**Laci:** `03_SOURCE-VAULT/R4_OEM-TECHNICAL/NETWORK` · **Daftar isi:** `_ISI.md` pada laci yang sama

> **R4 adalah satu-satunya sumber sah untuk angka yang melekat pada produk.** Tidak ada
> buku teks yang dapat menggantikannya, dan tidak boleh ditaksir.

## 1. Yang dipasok

Kapasitas switching · jumlah port & anggaran PoE · throughput · jumlah sambungan SIP serentak

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

Anggaran PoE total sering lebih menentukan daripada jumlah port. Periksa daya per port **dan** daya total catu.

## 4. Menopang rantai

Rantai **H** (lebar pita puncak) dan perancangan catu PoE

## 5. Gate

Angka dari laci ini ditandai **`OEM-DERIVED`** pada lembar perhitungan (`TPL-02`), bukan
`SOURCE-DERIVED`. Gate **G3** menuntut penandaan itu; gate **G5** menuntut lembar datanya
dilampirkan sebagai bukti.
