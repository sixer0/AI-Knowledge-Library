# Rantai K — Struktur penopang perangkat

## ⚠ RANTAI INI PUTUS DI MATA ④

**Tidak ada satu pun SNI struktur di rak.** Metode perhitungan lengkap tersedia, tetapi
**ambang lulus/tidak lulus tidak dapat ditetapkan** dari rak ini.

Rantai ketiga yang putus, setelah **D** (pembumian) dan **J** (keamanan siber).

> **Peringatan yang berbeda dari rantai lain.** Struktur yang gagal **menjatuhkan
> perangkat, dan bisa menimpa orang**. Rantai ini bukan soal dokumen yang dipersoalkan
> auditor — ini soal keselamatan.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Hibbeler, *Structural Analysis* (2017) | **R3** | Jenis & besaran beban · determinasi · **gaya batang** · rangka ruang | PDF 21 · 63 · 108, 114 · 128 |
| Segui, *Steel Design* (2017) | **R3** | ASD/LRFD · batang tarik · **tekuk** · balok · **sambungan** | PDF 38 · 58 · 124 · 202 · 392 |
| Darwin dkk., *Design of Concrete Structures* | **R3** | Lentur · geser · **panjang penyaluran** · kelayanan · kolom | PDF 95 · 145 · 194 · 239 · 288 |
| Mamlouk & Zaniewski, *Materials* | **R3** | Sifat bahan · baja · agregat · **beton** | PDF 22 · 110 · 194 · 288 |
| Ching, *Building Construction Illustrated* | **R3** | Apa yang ada di balik dinding/lantai | PDF 115 · 157 |
| **SNI 1727** beban minimum | **R1** | Beban rancangan | ❌ **TIDAK ADA** — `GAP-015` |
| **SNI 1726** ketahanan gempa | **R1** | Beban gempa | ❌ **TIDAK ADA** — `GAP-016` |
| **SNI 1729** struktur baja | **R1** | Ambang tegangan · **tabel profil Indonesia** | ❌ **TIDAK ADA** — `GAP-017` |
| **SNI 2847** struktur beton | **R1** | Ambang & faktor reduksi | ❌ **TIDAK ADA** — `GAP-018` |
| **ASTM / SNI** metode uji bahan | **R2** | Prosedur uji beton, baja, agregat | ❌ **TIDAK ADA** — `GAP-020` |
| Lembar data angkur, baut, profil | **R4** | Kapasitas angkur · mutu baut | ❌ per proyek |

> **Empat buku R3, empat SNI kosong.** Buku-buku itu berbasis ASCE 7, AISC, ACI 318, dan
> ASTM — **Amerika**. Padanan Indonesianya diturunkan dari sana tetapi **tidak identik**.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Jenis dudukan** — tiang, bracket dinding, rangka atap, menara | Beban + tempat + akses pemeliharaan | Bracket dinding **ditolak** bila dinding partisi ringan — lihat Ching PDF 157 sebelum memutuskan |
| **Beban rancangan** | Hibbeler PDF 21 · **angkanya wajib SNI** | Memakai berat perangkat saja **ditolak** — beban angin pada antena/kamera sering lebih besar |
| Bahan: baja / beton | Lingkungan, umur layan, biaya | Baja tanpa perlindungan korosi **ditolak** di lingkungan pantai atau industri |
| **Konfigurasi sambungan** | Segui PDF 392 | Las lapangan tanpa pemeriksaan **ditolak** — mutu las lapangan tidak dapat diandalkan tanpa uji |
| Jenis & kedalaman angkur | **R4 wajib** | Angkur pasca-pasang tanpa lembar data **ditolak** — kapasitasnya bergantung mutu beton dan kedalaman |
| **Siapa yang menandatangani** | ⚠ **wajib ahli bersertifikat** | Perhitungan yang hanya diperiksa internal **ditolak** untuk struktur yang menanggung keselamatan |

> **Baris terakhir bukan formalitas.** Rak ini membuat GSP mampu **memeriksa dan berdiskusi**
> dengan ahli struktur — bukan menggantikannya.

---

## ③ Perhitungan

### Urutan yang benar

```
1. Tetapkan beban                    Hibbeler PDF 21   ← angkanya dari SNI 1727/1726
              ↓
2. Periksa determinasi & kestabilan  Hibbeler PDF 63
              ↓
3. Hitung gaya batang / gaya dalam   Hibbeler PDF 108, 114, 128
              ↓
4. Periksa kapasitas elemen          Segui (baja) / Darwin (beton)
              ↓
5. Periksa sambungan & angkur        Segui PDF 392 + lembar data angkur [R4]
              ↓
6. Periksa kelayanan (lendutan)      Darwin PDF 239
```

**Langkah 2 sering dilewati** dan itu fatal: rangka yang tidak stabil **tidak menghasilkan
gaya batang yang bermakna** — perangkat lunak tetap memberi angka, tetapi angkanya tidak
berarti apa-apa.

### Beban yang wajib diperhitungkan

| Beban | Sumber angka |
|---|---|
| Mati — berat perangkat + dudukan | Lembar data **[R4]** |
| **Angin** — pada antena, kamera, penutup | ⚠ **SNI 1727** — tidak ada di rak |
| **Gempa** | ⚠ **SNI 1726** — tidak ada di rak |
| Pemasangan & pemeliharaan | Beban orang + peralatan — praktik |
| Es / salju | Tidak berlaku di Indonesia |

> **Beban angin hampir selalu menentukan** pada dudukan antena dan kamera di ketinggian —
> bukan berat perangkatnya. Antena parabola kecil dapat menghasilkan gaya angin beberapa
> kali berat sendirinya.

### Penandaan

Seluruh hasil hitungan ditandai **`PROJECT-DERIVED`**. Beban dari SNI ditandai
**`SOURCE-DERIVED [R1]`** — dan selama SNI belum ada, ditandai **`ASSUMPTION`** dengan
sensitivitas serta rencana penggantian.

---

## ④ Pengujian — ⚠ MATA YANG PUTUS

| Butir | Ambang | Sumber |
|---|---|---|
| Mutu beton (uji tekan silinder) | ⚠ **tidak ada di rak** | SNI 2847 / spesifikasi kontrak |
| Mutu baja & sertifikat pabrik | ⚠ **tidak ada di rak** | SNI 1729 / mill certificate **[R4]** |
| **Torsi baut** | ⚠ **tidak ada di rak** | Spesifikasi baut **[R4]** + SNI 1729 |
| **Pemeriksaan las** | Visual + NDT bila disyaratkan | Kontrak · standar las tidak ada di rak |
| **Uji tarik angkur** (pull-out) | Kapasitas lembar data **[R4]** × faktor keamanan | ✅ **R4 sah** bila lembar datanya ada |
| Lendutan terpasang | Hasil hitung mata ③ langkah 6 | R3 + kontrak |
| Verifikasi dimensi & tegak-lurus | Toleransi kontrak | Survei — rantai **L** |

**Satu-satunya baris yang tidak putus adalah uji tarik angkur**, karena kapasitasnya berasal
dari lembar data pabrikan **[R4]** — satu-satunya tingkat sah yang tersedia di domain ini.

### Tiga jalan sah selama SNI belum ada

1. **Kontrak menyebut standar tertentu** (SNI atau lainnya) → peroleh salinannya; ambang
   naik ke R1/R2. **Jalan yang paling benar.**
2. **Perhitungan ditandatangani ahli bersertifikat** → tanggung jawab dan ambang berpindah
   ke ahli tersebut, dan itu memang tempatnya.
3. **Nyatakan hasil ukur tanpa pernyataan lulus** → hanya untuk pekerjaan yang **tidak
   menanggung keselamatan orang**.

> **Jalan ke-3 tidak boleh dipakai untuk menara, dudukan di ketinggian, atau apa pun yang
> dapat jatuh menimpa orang.** Pada pekerjaan seperti itu, hanya jalan 1 dan 2 yang sah.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| **Perhitungan struktur bertanda tangan ahli** | ✅ | Untuk struktur yang menanggung keselamatan |
| Gambar struktur as-built | ✅ | Dimensi, mutu bahan, detail sambungan |
| **Sertifikat mutu bahan** (mill cert, uji tekan beton) | ✅ **[R4]** | Dari pemasok |
| Hasil uji tarik angkur | ✅ | Terhadap kapasitas lembar data |
| **Rekaman torsi baut** | ✅ | Per sambungan kritis |
| Laporan pemeriksaan las | ✅ | Visual minimum; NDT bila disyaratkan |
| Verifikasi dimensi & ketegakan | ✅ | Rantai **L** |
| **Pernyataan standar yang dipakai** | ✅ **wajib** | Menyebut SNI mana yang diacu — atau bahwa belum ada dan siapa yang menetapkan |
| Kartu kendali rantai | ✅ | Status: **putus di mata ④** |

---

## Status rantai

**METODE LENGKAP · AMBANG TIDAK ADA.**

Empat buku memberi seluruh metode yang dibutuhkan — dari beban sampai sambungan. Yang tidak
ada adalah **angka yang menyatakan cukup atau tidak**, dan itu justru yang mengikat.

**Empat celah R1 prioritas tinggi:** `GAP-015` sampai `GAP-018`. Menutup keempatnya mengubah
rantai ini dari putus menjadi utuh — perbaikan terbesar yang tersedia untuk domain ini.

> **CATATAN DEFECT (CVLK-0929/C1-FIX, 2026-09-29):** known-defek **KD-C9** dari objek IL
> `civil-structural-korpus-ekas-0929` (`vault/cvlk-0929/2026-09-29_civil-structural-korpus-ekas-0929.md`,
> register: `docs/2026-09-29-cvl-knowledge-register/`). Vonis custodian: klaim dua baris di atas
> **OVERSTATED**. Menutup GAP-015..018 menghilangkan penyebab putus di mata ④ untuk ambang DESAIN
> (mata ①-③) TAPI status "utuh" baru sah setelah angka ambang terverifikasi manusia terhadap PDF
> primer (SNI 2847 / SNI 1729 / ACI edisi berlaku) — mata ④ sendiri masih terbuka: uji bahan butuh
> GAP-020, las butuh standar yatim (KD-C5), angkur/baut butuh R4. Vonis sementara lapis teks; status
> BELUM TERKONFIRMASI sampai manusia membuka PDF primer. Sambil menunggu: setiap jawaban ke klien
> WAJIB memakai redaksi bertingkat (metode sah, ambang menunggu verifikasi) dan **DILARANG KLAIM
> LULUS STANDAR** (DT-11). Baris asli di atas tidak diubah; blok ini hanya-tambah.

**Jangan tertukar:** rak punya ambang **tahanan isolasi** [R2] dan **ΔT termografi** [R2],
tetapi **tidak punya satu pun ambang struktur**. Kemampuan menghitung bukan kewenangan
menyatakan lulus.
