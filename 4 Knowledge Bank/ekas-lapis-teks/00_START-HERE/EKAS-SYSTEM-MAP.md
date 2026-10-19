# Peta Sistem EKAS

Apa isi tiap folder, **siapa yang menulisnya**, dan **kapan diisi**.

---

## Dua jenis folder dan cara memakainya

| Jenis | Map | Sifat |
|---|---|---|
| **Pengetahuan** — milik perusahaan, lintas proyek | `01` `02` `03` `04` `05` `10` | Berubah **hanya** saat sumber baru masuk atau kekeliruan ditemukan |
| **Pekerjaan** — milik proyek | `06` `07` `08` `09` | Diisi tiap proyek, tidak pernah menimpa map pengetahuan |

> Kesalahan paling merusak pada sistem seperti ini adalah **menulis angka proyek ke map
> pengetahuan**. Loss budget proyek A masuk `06_ENGINEERING/CALCULATIONS/`, bukan ke
> `KATALOG-RUMUS.md`.

---

## Rincian tiap folder

### `00_START-HERE/` — pintu masuk

| Berkas | Isi |
|---|---|
| [`README.md`](README.md) | Apa sistem ini, enam aturan, keadaan sekarang |
| [`EKAS-SYSTEM-MAP.md`](EKAS-SYSTEM-MAP.md) | Berkas ini |
| [`DOCUMENT-CONTROL.md`](DOCUMENT-CONTROL.md) | Penomoran, versi, status, keadaan migrasi |
| [`CHANGELOG.md`](CHANGELOG.md) | Riwayat pembangunan rak (T1–T19) |

### `01_GOVERNANCE/` — aturan main

| Berkas | Menjawab |
|---|---|
| `REFERENCE-CONFIDENCE-LEVEL.md` | Apa arti R1–R5 dan untuk apa masing-masing boleh dipakai |
| `AUTHORITY-STATUS.md` | Status otoritas tiap sumber: aktif, terbatas, digantikan, hanya intake |
| `ASSURANCE-WORKFLOW.md` | Lima mata rantai ①→⑤ dan aturan tingkat di tiap mata |
| `ASSURANCE-GATES.md` | Gate G0–G7 — kapan sebuah butir boleh dinyatakan selesai |
| `AI-USAGE-POLICY.md` | Apa yang boleh dan tidak boleh dikerjakan model bahasa di sistem ini |
| `SOURCE-UPDATE-PROCEDURE.md` | Cara menambah sumber tanpa meninggalkan berkas basi |

### `02_REGISTERS/` — daftar induk

Delapan berkas `.csv` supaya dapat disaring dan dibaca mesin, plus dua `.md` penjelas.

| Register | Diisi oleh | Kapan |
|---|---|---|
| `MASTER-REFERENCE-REGISTER.csv` | pengelola rak | saat sumber masuk |
| `GAP-REGISTER.csv` | pengelola rak | saat celah ditemukan/ditutup |
| `REQUIREMENT-REGISTER.csv` | tim proyek | awal proyek (gate G1) |
| `DESIGN-DECISION-REGISTER.csv` | tim proyek | tiap keputusan |
| `CALCULATION-REGISTER.csv` | tim proyek | tiap hitungan |
| `TEST-REGISTER.csv` | tim proyek | saat ITP disusun |
| `EVIDENCE-REGISTER.csv` | tim proyek | saat bukti masuk |
| `ASSET-REFERENCE-REGISTER.csv` | tim proyek | menjelang serah |

### `03_SOURCE-VAULT/` — berkas sumber, dilaci menurut tingkat

**Tingkat R ditentukan penerbitnya, bukan topiknya.** Buku bagus tetap R3; majalah bagus
tetap R5.

```
R1_NATIONAL-NORMATIVE     ← kosong. Empat celah prioritas tinggi
R2_INTERNATIONAL-STANDARDS ← 5 berkas: IEC(1) IEEE(2) EN-BS(1) ANSI-NETA(1)
R3_TEXTBOOK-HANDBOOK       ← 24 buku, 16 laci topik
R4_OEM-TECHNICAL           ← kosong secara rancangan. Diisi per proyek
R5_RESEARCH-SECONDARY      ← 8 berkas: tesis(4) panduan(4)
```

Tiap laci punya `_ISI.md` yang mendaftar isinya. Laci kosong tetap ada beserta penjelasan
mengapa kosong — **laci kosong adalah informasi**, bukan kelalaian.

> `ANSI-NETA/` ditambahkan ke luar daftar baku (IEC, ISO-IEC, IEEE, TIA, ITU-T, EN-BS)
> karena NETA bukan salah satu dari keenamnya dan menaruhnya di laci lain akan menyesatkan.

### `04_KNOWLEDGE-CARDS/` — satu kartu per rujukan

30 kartu. Tiap kartu menjawab, dalam satu halaman:
apa yang dipasok · halaman jangkar · rumusnya · **boleh menetapkan ambang atau tidak** ·
**batas pemakaian** · rantai jaminannya · gate yang harus dilewati.

Kartu adalah **jawaban cepat**; resume lengkap ada di `05_DOMAIN-KNOWLEDGE/`.

### `05_DOMAIN-KNOWLEDGE/` — pengetahuan per domain

Tiap domain berisi resume-resume bertanda tingkat R di depan namanya, plus
`RANTAI-JAMINAN.md` — rantai lengkap ①→⑤ untuk domain itu.

**Mulai dari `RANTAI-JAMINAN.md`, bukan dari resume.** Rantai yang memberi urutan kerja;
resume memberi rinciannya.

### `06_ENGINEERING/` … `09_HANDOVER/` — folder pekerjaan proyek

Tiap folder punya [`README.md`](README.md) sendiri yang menyebut aturannya. Yang perlu diingat:

| Map | Aturan yang paling sering dilanggar |
|---|---|
| `06` | Keputusan desain tanpa **alternatif yang ditolak** |
| `07` | Ambang uji tanpa **sumber ambang** |
| `08` | Berkas mentah **disunting** |
| `09` | Serah terima tanpa **daftar asumsi yang masih terbuka** |

### `10_TEMPLATES/` — delapan templat

`TPL-00` kartu kendali rantai · `TPL-01` catatan keputusan desain · `TPL-02` lembar
perhitungan · `TPL-03` prosedur uji · `TPL-04` catatan penerimaan · `TPL-05` paket bukti
serah · `TPL-06` ketertelusuran kebutuhan · `TPL-07` permintaan pembaruan sumber.

### `90_TOOLS/` — perkakas

OCR, pembangun katalog, pembangun paket ekspor, pembangun struktur ini, dan
`migrasi_sumber.py` untuk memindahkan PDF ke `03_SOURCE-VAULT/`.

### `95_IMPORT-SNAPSHOTS/` — rekaman keadaan saat impor

`BATCH-01/` dan `BATCH-02/` — paket .zip apa adanya saat masuk. Tidak disunting; dipakai
untuk menelusuri "apa yang berubah sejak impor".

### `99_ARCHIVE/` — yang sudah tidak berlaku

`SUPERSEDED/` edisi lama · `ORIGINAL-BEFORE-OCR/` berkas pra-OCR ·
`LEGACY-EKAS/` sistem EKAS sebelumnya · `OLD-EXPORTS/` paket ekspor lama.

**Arsip tidak dihapus dan tidak dipakai.** Ia ada supaya pertanyaan "dulu angkanya berapa"
dapat dijawab.

---

## Alur satu pekerjaan, dari awal sampai serah

```
1. Kebutuhan dibekukan              → 06_ENGINEERING/REQUIREMENTS       [G1]
2. Buka rantai domainnya            → 05_DOMAIN-KNOWLEDGE/<dom>/
3. Keputusan desain + alternatif    → 06_ENGINEERING/DESIGN-DECISIONS   [G2]
4. Hitung, tandai tiap masukan      → 06_ENGINEERING/CALCULATIONS       [G3]
5. Isi kartu kendali per besaran    → TPL-00
6. Susun ITP + ambang + sumbernya   → 07_VERIFICATION-VALIDATION/ITP    [G4]
7. Uji, simpan bukti mentah         → 08_EVIDENCE/                      [G5]
8. Rekap + berita acara             → 09_HANDOVER/                      [G6]
9. Diterima pemberi kerja                                                [G7]
```

**Kartu kendali (langkah 5) yang paling sering dilewati** — dan kartu itulah yang menjawab
pemeriksa tanpa membongkar ulang perhitungan berbulan kemudian.
