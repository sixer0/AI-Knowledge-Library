# Kendali Dokumen

---

## Penomoran

| Awalan | Untuk | Contoh |
|---|---|---|
| `REF-` | Rujukan dalam register induk | `REF-ELC-002` |
| `GAP-` | Celah sumber | `GAP-001` |
| `REQ-` | Kebutuhan proyek | `REQ-P25-014` |
| `DDR-` | Catatan keputusan desain | `DDR-P25-003` |
| `CALC-` | Lembar perhitungan | `CALC-P25-007` |
| `TEST-` | Butir pengujian | `TEST-P25-011` |
| `ACC-` | Catatan penerimaan | `ACC-P25-011` |
| `NCR-` | Ketidaksesuaian | `NCR-P25-002` |
| `EV-` | Bukti | `EV-P25-041` |
| `SUR-` | Permintaan pembaruan sumber | `SUR-006` |
| `BA-` | Berita acara | `BA-P25-FO-014` |

Nomor proyek disisipkan di tengah (`P25` = proyek 2025-xx). Nomor rujukan dan celah
**tanpa** nomor proyek — keduanya milik perusahaan, bukan proyek.

**`P00` dicadangkan untuk contoh dan latihan** — jangan dipakai proyek sungguhan.

## Kode domain pada `REF-`

`BAT` baterai · `VSS` video · `ELC` kelistrikan · `FO` serat optik · `GRD` pembumian ·
`LPS` proteksi petir · `NET` jaringan · `PWR` catu daya · `RCM` keandalan · `STG`
penyimpanan · `THM` termal · `MEC` mekanik · `SEC` keamanan siber · `OPS` operasional ·
`CIP` infrastruktur kritis · `VAI` analitik video

---

## Status otoritas sumber

| Status | Arti | Boleh dipakai? |
|---|---|---|
| `ACTIVE` | Berlaku penuh dalam lingkupnya | ✅ |
| `ACTIVE_WITH_SCOPE_LIMITS` | Berlaku, tetapi ada hal di luar cakupannya yang sering disangka tercakup | ✅ **baca batasnya** |
| `POINTER_ONLY` | Hanya penunjuk ke sumber primer | ⚠ tidak sebagai sandaran |
| `INTAKE_ONLY` | Sudah di rak, **belum diresume dan belum dinilai** | ❌ belum boleh dipakai |
| `SUPERSEDED` | Digantikan edisi/dokumen lebih baru | ❌ arsip |
| `WITHDRAWN` | Ditarik karena keliru | ❌ |

Rincian: `01_GOVERNANCE/AUTHORITY-STATUS.md`

---

## Versi berkas

Berkas pengetahuan (map `01`–`05`, `10`) **tidak diberi nomor versi pada namanya.**
Riwayatnya ada di `CHANGELOG.md`. Nama berkas yang stabil membuat rujukan silang tidak putus.

Berkas proyek (map `06`–`09`) memakai **tanggal**, bukan nomor revisi:
`CALC-P25-007_2026-08-20.md`. Bila direvisi, berkas lama pindah ke
`99_ARCHIVE/SUPERSEDED/` — tidak ditimpa.

---

## Klasifikasi

Belum diterapkan pada struktur ini. Bila dokumen proyek menyangkut instansi yang menuntut
klasifikasi (BIASA / TERBATAS / RAHASIA), penandaannya mengikuti ketentuan instansi
tersebut dan **dicantumkan pada tiap halaman**, bukan hanya pada sampul.

---

## Keadaan migrasi — SELESAI 20 Agustus 2026

> ### ✅ Migrasi tuntas
>
> **Seluruh sumber teknis kini berada di dalam EKAS.** Folder topik lama sudah dihapus;
> rak lama tidak ada lagi.

| Isi | Jumlah | Tujuan |
|---|---|---|
| PDF sumber | **37** (993 MB) | `03_SOURCE-VAULT/` — 22 laci |
| PDF pra-OCR | 2 (239 MB) | `99_ARCHIVE/ORIGINAL-BEFORE-OCR/` |
| PDF edisi lama | 1 (39 MB) | `99_ARCHIVE/SUPERSEDED/` |
| Resume | 30 | `05_DOMAIN-KNOWLEDGE/<domain>/` |
| Rantai jaminan | 8 | `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md` |
| Tata kelola | 6 | `01_GOVERNANCE/` |
| Katalog rumus | 1 | `06_ENGINEERING/CALCULATIONS/` |
| Templat berita acara | 1 | `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/` |
| Perkakas | 8 | `90_TOOLS/` |
| Paket ekspor | 3 | `95_IMPORT-SNAPSHOTS/`, `99_ARCHIVE/OLD-EXPORTS/` |

### Rujukan jalur yang ikut diperbarui

**323 penyebutan jalur di 89 berkas** disunting mengikuti pemindahan — katalog rumus,
asumsi baku, prosedur, register, rantai jaminan, 30 resume, dan lima berkas rujukan skill
di luar EKAS.

Bentuk penulisan jalur yang dipakai sekarang, singkat supaya terbaca dalam kalimat:

| Bentuk | Arti |
|---|---|
| `` `R2/IEEE/` `` | `03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEEE/` |
| `` `R3/BATTERY/` `` | `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/BATTERY/` |
| `` `R5/THESIS/` `` | `03_SOURCE-VAULT/R5_RESEARCH-SECONDARY/THESIS/` |

> **Catatan riwayat sengaja TIDAK ikut disunting.** `CHANGELOG.md` memuat nama folder
> sebagaimana adanya saat peristiwa itu terjadi — catatan riwayat yang jalurnya
> "dimutakhirkan" berhenti menjadi catatan riwayat.

### Yang masih terbuka

1. **Dua sistem EKAS paralel.** `ENGINEERING KNOWLEDGE ASSURANCE SYSTEM/` (tiga zip dari
   transformasi terdahulu) sudah disalin ke `99_ARCHIVE/LEGACY-EKAS/`. Salinan aslinya di
   akar rak dapat dihapus setelah struktur ini dinyatakan induk.
2. **`RCM/Reliability Centered Maintenance`** — folder kosong sisa OCR. Terhapus bersama
   folder induknya pada 20 Agustus 2026.
3. **Bundel `_panduan`.** Empat berkas (termasuk **NIST SP 800-50r1**) dinilai bersama
   sebagai satu R5 karena dibundel dengan majalah. NIST SP itu layak dinilai sendiri dan
   kemungkinan naik ke R2. **Belum dipecah** — pemecahan mengubah penomoran `REF-SEC-*`.
