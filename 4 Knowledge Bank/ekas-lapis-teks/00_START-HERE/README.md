# GSP — Engineering Knowledge & Assurance System

**PT Gemilang Satria Perkasa** · Struktur dibangun 20 Agustus 2026
Rak sumber: `C:\Users\gspen\Videos\Buku`

---

## Apa ini

Sistem yang membuat **setiap rujukan berujung ke keputusan desain, perhitungan, pengujian,
dan bukti serah terima** — bukan berhenti sebagai daftar buku.

```
①  RUJUKAN   →  ②  KEPUTUSAN  →  ③  HITUNGAN  →  ④  UJI  →  ⑤  BUKTI SERAH
   [R1–R5]       desain           + asumsi        + ambang    berita acara
```

Setiap sumber membawa **tingkat keyakinan R1–R5** yang menentukan **untuk apa angkanya
boleh dipakai**:

| | Jenis | Boleh menetapkan ambang terima? |
|---|---|---|
| **R1** | Regulasi Indonesia / SNI / standar normatif nasional | ✅ **ya — mengikat secara hukum** |
| **R2** | Standar internasional (IEC, IEEE, BS EN, ANSI/NETA) | ✅ ya, bila diadopsi kontrak |
| **R3** | Buku teks / handbook rekayasa | ⚠ hanya bila kontrak mengadopsinya tertulis |
| **R4** | Dokumentasi teknis pabrikan (OEM) | ✅ **wajib** untuk angka melekat produk |
| **R5** | Sumber sekunder (tesis, makalah, panduan) | ❌ **tidak pernah** — penunjuk saja |

---

## Keadaan sekarang

```
R1  ░░░░░░░░░░░░░░░░░░░░   0 sumber   ← tidak ada dasar hukum Indonesia
R2  ███░░░░░░░░░░░░░░░░░   5 sumber
R3  ████████████████████  24 sumber   ← kekuatan sistem ini
R4  ░░░░░░░░░░░░░░░░░░░░   0 sumber   ← selalu dari pabrikan, per proyek
R5  ███░░░░░░░░░░░░░░░░░   8 sumber
```

**Artinya:** GSP dapat **merancang dan menghitung** dengan baik dari sini, dan dapat
**menetapkan ambang** untuk lima jenis pengujian — tetapi **tidak dapat menyatakan
kepatuhan hukum Indonesia** dan **tidak dapat menyebut angka produk** tanpa bahan dari luar.

Dua kekosongan itu berbeda sifatnya:

- **R4 tidak perlu diadakan.** Ia melekat pada produk yang dipilih; diminta per proyek.
- **R1 perlu diadakan.** Empat celah R1 ada di `02_REGISTERS/GAP-REGISTER.csv`, prioritas
  tinggi seluruhnya.

---

## Mulai dari mana

| Anda sedang… | Buka |
|---|---|
| Baru pertama memakai sistem ini | `EKAS-SYSTEM-MAP.md` |
| Mengerjakan proyek nyata | `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md` |
| Mencari rumus | `06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` |
| Menyusun berita acara | `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/` |
| Ingin tahu bobot sebuah sumber | `04_KNOWLEDGE-CARDS/<domain>/REF-*.md` |
| Menambah sumber baru | `01_GOVERNANCE/SOURCE-UPDATE-PROCEDURE.md` |
| Ingin tahu apa yang belum ada | `02_REGISTERS/GAP-REGISTER.csv` |

---

## Enam aturan yang tidak boleh dilanggar

**1. Setiap angka teknis membawa penanda tingkat.**
`[R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223]` — bukan angka telanjang.

**2. Ambang terima menuntut R1 atau R2.**
Ambang dari R3 hanya sah bila kontrak mengadopsinya secara tertulis.

**3. Angka melekat produk menuntut R4.**
Derating, efisiensi, DoD, umur siklus, unjuk kerja tulis — **wajib** surat pabrikan.
Bila belum ada, tulis "menunggu data pabrikan", jangan diisi angka umum.

**4. R5 tidak pernah menjadi sandaran akhir.**
Tesis yang menyebut UU 11/2008 adalah petunjuk bahwa **UU-nya** perlu dibuka.

**5. Asumsi dinyatakan, tidak disembunyikan.**
Tiap asumsi membawa sensitivitas dan rencana penggantian datanya.

**6. Yang tidak ada di rak dinyatakan tidak ada.**
Menyebut "tidak tersedia, ambil dari PUIL" jauh lebih berguna daripada mengisi angka dari
pengetahuan umum.

---

## Batas yang harus diketahui pemakai

- **Nomor halaman merujuk halaman PDF**, bukan halaman cetak, kecuali dinyatakan keduanya.
- **Diesel Generator Handbook kehilangan ± 55 halaman** — Bab 11 (emergency & standby)
  seluruhnya. Materinya tidak tersedia.
- **Tiga buku catu daya terbit 2000–2004.** Kerangka hitungnya sahih; angka produknya tidak.
- **Berkas fisik PDF belum dipindahkan ke `03_SOURCE-VAULT/`** — lihat
  `DOCUMENT-CONTROL.md` bagian "Keadaan migrasi".
