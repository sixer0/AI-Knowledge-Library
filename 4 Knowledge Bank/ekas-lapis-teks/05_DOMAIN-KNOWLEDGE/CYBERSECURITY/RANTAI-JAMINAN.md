# Rantai J — Keamanan siber dan penanganan bukti digital

## ⚠ RANTAI INI PUTUS DI MATA ④

**Tidak ada satu pun sumber R1 atau R2 keamanan siber di rak.** Seluruh kriteria kepatuhan —
yang justru menjadi isi pokok tender instansi — **tidak dapat dibuktikan dari rak ini**.

Diterbitkan dalam keadaan putus **dengan sengaja**, seperti rantai **D**. Ini rantai kedua
yang putus, dan putusnya lebih luas.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Anderson, *Security Engineering* (2020) | **R3** | Analisis ancaman · kendali akses bertingkat · **integritas jejak audit** · metodologi pengembangan aman | PDF 17 · 187, 279 · 437 · 846, 889 |
| Alsmadi, *NICE Cyber Security Framework* (2019) | **R3** | **Proses forensik 4 tahap + rantai kustodi** · tanggap insiden · kualifikasi personel | **PDF 266–268** · 343 · 77 |
| Johnson (ed.), *Protecting Critical Infrastructures* (2015) | **R3** | Aset kritis, ketahanan, pemetaan ketergantungan | `R3/CRITICAL-INFRASTRUCTURE/` |
| Bundel panduan operasional | **R5** | Pengerasan AD · **mutu pencatatan log** · program pembelajaran | `R5/TECHNICAL-GUIDES/` |
| 4 tesis UI | **R5** | **Penunjuk** ke UU 11/2008 dan Perban BSSN 4/2021 | `R5/THESIS/` |
| **UU 11/2008 (ITE)** | **R1** | Dasar hukum bukti elektronik | ❌ **TIDAK ADA** — `GAP-002` |
| **Peraturan BSSN No. 4/2021** | **R1** | Kriteria audit keamanan instansi | ❌ **TIDAK ADA** — `GAP-003` |
| **ISO/IEC 27001 & 27002** | **R2** | Persyaratan SMKI | ❌ **TIDAK ADA** — `GAP-006` |
| **NIST SP 800-86 · ISO/IEC 27037** | **R2** | Penanganan bukti digital | ❌ **TIDAK ADA** — `GAP-007` |

> **Perhatikan pola tabel ini.** Empat baris terakhir — seluruh yang bertingkat R1/R2 —
> kosong. Yang ada hanya R3 dan R5.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Model ancaman** sistem | Anderson PDF 17 | Merancang kendali sebelum ancaman ditetapkan **ditolak** — menghasilkan kendali yang mahal dan tidak mengena |
| **Kendali akses & pemisahan hak** | Anderson PDF 187, 279 | Satu peran administrator untuk semua **ditolak** |
| **Rancangan jejak audit yang tidak dapat disangkal** | Anderson PDF 437 | Log yang dapat disunting administrator **ditolak** — pada sistem bukti digital itu membatalkan nilainya |
| **Proses penanganan bukti 4 tahap** | Alsmadi PDF 266–268 ⭐ | Menyalin bukti tanpa rantai kustodi **ditolak** |
| Kebijakan & mutu pencatatan log | Joint CSI **[R5]** | Mencatat semuanya tanpa kebijakan ditolak — biaya besar, temuan sedikit |
| Pengerasan identitas (Active Directory) | ASD-CISA **[R5]** | Setelan bawaan ditolak |
| **Kriteria kepatuhan yang dijanjikan** | ⚠ **harus R1/R2** | Menjanjikan "sesuai ISO 27001" tanpa salinan standarnya **ditolak** |

> **Baris terakhir adalah keputusan yang paling berbahaya di seluruh rak.** Menuliskan
> "sesuai ISO/IEC 27001" atau "sesuai Peraturan BSSN" dalam proposal **tanpa memiliki
> salinan standarnya** menjanjikan sesuatu yang tidak dapat diperiksa sendiri.

---

## ③ Perhitungan

**Domain ini hampir tanpa perhitungan.** Yang ada bersifat penilaian, bukan rumus:

| Yang dinilai | Cara | Sifat |
|---|---|---|
| Prioritas risiko | Kemungkinan × dampak | Kualitatif / semi-kuantitatif — **beri label metode internal** |
| Cakupan sumber log | Matriks sumber log terhadap taktik yang dipantau | Metode internal |
| Cakupan kompetensi personel | Matriks peran/KSA — Alsmadi | Metode internal |
| Waktu tanggap insiden | Dari kontrak / SLA | **Bukan** dari buku |

> Angka apa pun yang dihasilkan di sini ditandai **`PROJECT-DERIVED`** dan **wajib menyebut
> bahwa metodenya internal** — bukan metode normatif. Skor risiko yang tampak seperti angka
> objektif padahal hasil penilaian sendiri adalah bentuk penyesatan yang paling halus.

---

## ④ Pengujian — ⚠ MATA YANG PUTUS

| Butir | Ambang | Sumber |
|---|---|---|
| Pengerasan identitas / AD | Daftar periksa ASD-CISA | ⚠ **R5** — bukan sandaran sah |
| Mutu & kelengkapan pencatatan log | Panduan Joint CSI | ⚠ **R5** |
| Verifikasi integritas jejak audit | Rancangan mata ② | R3 + kontrak |
| **Rantai kustodi bukti digital** | Proses 4 tahap Alsmadi | ⚠ **R3** — kerangka, bukan norma |
| Uji penetrasi | Lingkup & kriteria dari kontrak | Kontrak |
| **Kepatuhan ISO/IEC 27001** | ❌ **tidak dapat diuji** | Standarnya tidak ada |
| **Kepatuhan Perban BSSN 4/2021** | ❌ **tidak dapat diuji** | Regulasinya tidak ada |
| **Keterterimaan bukti di pengadilan** | ❌ **tidak dapat dinyatakan** | UU ITE tidak ada |

**Tiga baris terakhir yang membuat rantai ini putus.** Ketiganya justru yang paling sering
diminta pada tender DEMS dan sistem keamanan instansi.

### Yang boleh dan tidak boleh dikatakan

| ✅ Boleh | ❌ Tidak boleh |
|---|---|
| *"Rancangan mengikuti proses penanganan bukti empat tahap beserta rantai kustodi [R3, Alsmadi PDF 266–268]."* | ~~*"Sistem ini memenuhi ISO/IEC 27037."*~~ |
| *"Kebijakan pencatatan log disusun mengacu panduan Joint CSI 2024 [R5]; standar normatifnya belum diadopsi."* | ~~*"Sesuai standar internasional penanganan bukti."*~~ |
| *"Kriteria audit mengacu Perban BSSN 4/2021 — salinan regulasi diperoleh terpisah dan dilampirkan."* | ~~*"Sesuai Peraturan BSSN"* dengan menyandarkan pada tesis~~ |

> **Tesis di `R5/THESIS/` menyebut UU 11/2008 dan Perban BSSN — itu penunjuk, bukan dasar
> hukum.** Yang masuk dokumen resmi adalah **pasal dari regulasi aslinya**.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Dokumen model ancaman | ✅ | Dasar seluruh kendali |
| Matriks peran & hak akses | ✅ | Termasuk pemisahan tugas |
| **Rancangan & bukti integritas jejak audit** | ✅ | Yang membuat sistem bukti bernilai |
| **Formulir rantai kustodi** | ✅ | Kerangka dari Alsmadi PDF 268 |
| Dasar konfigurasi pengerasan | ✅ | Beserta penyimpangan yang disetujui |
| Matriks sumber log + contoh peringatan | ✅ | |
| Rekaman pelatihan & kesadaran | ✅ | `09_HANDOVER/TRAINING/` |
| Laporan uji penetrasi | bila disyaratkan | Lingkup tertulis |
| **Pernyataan batas kepatuhan** | ✅ **wajib** | Menyebut standar mana yang **belum** dapat dibuktikan |
| Kartu kendali rantai | ✅ | Status: **putus di mata ④** |

**Baris kedua dari bawah adalah yang membedakan dokumen jujur dari dokumen yang akan
dipersoalkan.** Menyatakan batas kepatuhan sejak awal jauh lebih kuat daripada menunggu
pemeriksa menemukannya.

---

## Cara menutup rantai ini

Empat celah, seluruhnya prioritas tinggi:

| Celah | Yang dibutuhkan | Akibat bila tetap kosong |
|---|---|---|
| `GAP-002` | **UU 11/2008 (ITE)** + perubahannya | Keterterimaan bukti tidak dapat dinyatakan |
| `GAP-003` | **Peraturan BSSN No. 4/2021** | Kriteria audit instansi tidak dapat diuji |
| `GAP-006` | **ISO/IEC 27001 & 27002** | Klaim SMKI tidak dapat dipertahankan |
| `GAP-007` | **NIST SP 800-86 · ISO/IEC 27037** | Penanganan bukti hanya berkerangka R3 |

**NIST SP 800-86 tersedia bebas dari NIST.** Itu yang paling cepat dan paling murah ditutup
— dan ia langsung menaikkan lini DEMS dari R3 ke R2.

Sampai keempatnya ada, pekerjaan tetap boleh berjalan — **asalkan batasnya dinyatakan.**
Lihat `01_GOVERNANCE/ASSURANCE-GATES.md` bagian "rantai yang sengaja berhenti di G4".
