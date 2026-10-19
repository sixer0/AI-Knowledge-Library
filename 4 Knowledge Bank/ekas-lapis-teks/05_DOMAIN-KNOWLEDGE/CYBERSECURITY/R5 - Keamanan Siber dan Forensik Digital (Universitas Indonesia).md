# Resume — Empat Tesis Universitas Indonesia

**Program:** Manajemen Keamanan Jaringan Informasi / Teknik Elektro, Fakultas Teknik UI
**Tahun:** 2021–2023 · **Total:** 430 halaman
**Disusun:** 19 Agustus 2026 · **Rujukan halaman memakai nomor PDF**

Empat karya akademik berbahasa Indonesia yang menyentuh langsung dua lini kerja GSP:
**forensik digital / manajemen bukti** dan **audit keamanan siber instansi pemerintah**.

> ### Mengapa keempatnya bernilai untuk rak ini
>
> Seluruh buku keamanan di rak berbasis luar negeri — Anderson (Inggris), NIST, CISA.
> Keempat tesis ini **menerapkan kerangka internasional itu ke dalam konteks hukum dan
> regulasi Indonesia**, menyebut dasar hukumnya secara eksplisit:
>
> - **UU No. 11 Tahun 2008 (ITE)** — dasar sahnya dokumen elektronik sebagai alat bukti
> - **Peraturan BSSN No. 4 Tahun 2021** — dasar audit keamanan siber instansi
> - **NIST SP 800-101** — acuan forensik perangkat bergerak
>
> Itulah yang tidak ada di buku mana pun di rak. Statusnya **karya akademik, bukan standar**
> — dipakai sebagai penunjuk ke regulasi aslinya dan sebagai contoh penerapan, bukan sebagai
> dasar hukum yang dikutip langsung.

---

## 1. Ayubi Wirara (2021) — Forensik aplikasi pesan instan

**Judul:** *Analisis dan Profiling Jejak Digital untuk Pengembangan Acuan Metode Forensik
pada Aplikasi Pesan Instan Berdasarkan Standard NIST 800-101*
**Pembimbing:** Dr. Muhammad Salman · 90 halaman

**Yang paling relevan untuk GSP.** Latar belakangnya langsung menyebut dasar hukum yang
menjadi pijakan seluruh lini DEMS:

> Sejak diberlakukannya **UU Nomor 11 Tahun 2008 tentang ITE**, dokumen atau informasi
> elektronik telah menjadi **alat bukti hukum yang sah di Indonesia**.

Isinya mengembangkan **acuan metode forensik** untuk aplikasi pesan instan dengan
berpedoman **NIST SP 800-101** (forensik perangkat bergerak).

**Dipakai untuk:** menyusun bagian metodologi forensik pada proposal DEMS; menunjuk NIST
800-101 sebagai acuan; menjelaskan dasar hukum keabsahan bukti elektronik di Indonesia.

## 2. Abdul Hakim (2021) — Forensik aplikasi keamanan data Android

**Judul:** *Analisis Forensik pada Aplikasi Keamanan Data Perangkat Smartphone Android*
**Pembimbing:** Dr. Yohan Suryanto · 89 halaman

Membahas forensik terhadap aplikasi yang **mengenkripsi dan menyembunyikan informasi** pada
ponsel — kunci galeri, pengaman data, dan sejenisnya.

**Dipakai untuk:** memahami tantangan pengambilan bukti dari perangkat yang datanya
sengaja disembunyikan; melengkapi bagian akuisisi bukti pada rancangan DEMS.

## 3. Nana Mulyana (2021) — Cyber Kill Chain dengan Elastic Stack

**Judul:** *Identifikasi Tahapan Serangan Berdasarkan Model Cyber Kill Chain Menggunakan
Elastic Stack: Studi Kasus Lembaga Kebijakan Pengadaan Barang/Jasa Pemerintah*
**Pembimbing:** Prof. Kalamullah Ramli · 80 halaman

Menerapkan model **Cyber Kill Chain** untuk mengidentifikasi tahapan serangan, dengan
**Elastic Stack** sebagai perkakasnya. Studi kasusnya **instansi pemerintah** (LKPP).

**Dipakai untuk:** rancangan pemantauan keamanan (SOC) di lingkungan instansi; contoh
penerapan Elastic Stack pada konteks pemerintahan Indonesia; memetakan temuan log ke tahapan
serangan. Bertemu dengan panduan *Best Practices for Event Logging* di `_panduan/`.

## 4. Ivan Bashofi (2023) — Kriteria audit keamanan siber per Peraturan BSSN

**Judul:** *Perancangan Kriteria Cyber Security Audit Menggunakan NIST CSF dan CIS Controls
v8 Sesuai dengan Peraturan Badan Siber dan Sandi Negara Nomor 4 Tahun 2021*
*(Studi Kasus: Pusat Data dan Teknologi Informasi Komunikasi Badan XYZ)*
**Pembimbing:** Dr. Muhammad Salman · 171 halaman — yang paling tebal

**Ini yang paling dekat dengan celah ISO 27001 di rak.** Menyusun kriteria audit dengan
memadukan **NIST CSF** dan **CIS Controls v8**, diselaraskan ke **Peraturan BSSN No. 4
Tahun 2021** — regulasi yang mengikat instansi pemerintah Indonesia.

**Dipakai untuk:** menyusun bagian kepatuhan pada proposal untuk instansi; menunjuk Perban
BSSN 4/2021 sebagai dasar; contoh pemetaan kerangka internasional ke regulasi nasional.
Studi kasusnya **pusat data instansi** — konfigurasi yang sering masuk lingkup GSP.

---

## Pemakaian di GSP

| Keperluan | Tesis |
|---|---|
| Dasar hukum bukti elektronik Indonesia (UU ITE) | Ayubi Wirara |
| Metodologi forensik perangkat bergerak (NIST 800-101) | Ayubi Wirara |
| Akuisisi bukti dari aplikasi terenkripsi | Abdul Hakim |
| Rancangan pemantauan keamanan instansi | Nana Mulyana |
| Pemetaan log ke tahapan serangan | Nana Mulyana |
| **Kriteria audit siber per Perban BSSN 4/2021** | **Ivan Bashofi** |
| Pemetaan NIST CSF / CIS Controls ke regulasi nasional | Ivan Bashofi |

**Pendamping di rak:** `R3/SECURITY/` (Anderson) untuk kerangka berpikir keamanan;
`_panduan/` untuk panduan operasional; `R3/OPERATIONS/` (Limoncelli) untuk penerapan
operasionalnya.

---

## Batas keempatnya

- **Karya akademik, bukan standar.** Untuk dokumen resmi, kutip **regulasi aslinya** —
  UU ITE, Perban BSSN 4/2021, NIST SP 800-101 — bukan tesisnya. Tesis dipakai sebagai
  penunjuk dan contoh penerapan.
- **Regulasi berubah.** Perban BSSN 4/2021 dan turunannya perlu diperiksa apakah masih
  berlaku atau sudah direvisi.
- **NIST SP 800-101 dan SP 800-86 sendiri belum ada di rak** — keduanya tersedia bebas dari
  NIST dan masih tercatat sebagai celah pada `PETA-CELAH-KOLEKSI.md`.
- Studi kasus tesis bersifat spesifik; temuannya tidak otomatis berlaku pada instalasi lain.
