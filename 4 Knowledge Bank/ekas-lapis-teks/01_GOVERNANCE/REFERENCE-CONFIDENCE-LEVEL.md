# Tingkat Keyakinan Rujukan (R1–R5)

**Bagian dari:** Engineering Knowledge & Assurance System (EKAS) · **Disusun:** 20 Agustus 2026

Setiap angka yang masuk dokumen GSP membawa **tingkat keyakinan** sumbernya. Tingkat itu
menentukan **untuk apa angka tersebut boleh dipakai** — bukan sekadar penanda mutu.

Aturan pokoknya satu kalimat:

> **Semakin mengikat akibat sebuah angka, semakin tinggi tingkat rujukan yang dituntut.**
> Angka yang menentukan lulus/tidak lulus serah terima menuntut R1 atau R2. Angka yang
> menjelaskan *mengapa* boleh R3.

---

## Definisi

| Tingkat | Jenis sumber | Contoh | Sifat |
|---|---|---|---|
| **R1** | **Regulasi dan standar nasional yang mengikat** | PUIL, SNI, UU 11/2008 (ITE), Peraturan BSSN, Permen, Perkap | **Mengikat secara hukum** di Indonesia. Tidak dapat dibantah dengan pendapat teknis |
| **R2** | **Standar internasional** | IEC, IEEE, ISO/IEC, BS EN, ANSI/NETA | Mengikat **bila diadopsi kontrak**. Diterima luas sebagai dasar ambang uji |
| **R3** | **Buku teks dan handbook rekayasa** | Moubray, Damjanovski, Gill, Joffe, Uman, Hayes | Menjelaskan **mengapa** dan **bagaimana**. Bukan penetap ambang, kecuali kontrak mengadopsinya tertulis |
| **R4** | **Dokumentasi teknis pabrikan (OEM)** | Lembar data, manual, kurva derating, surat pabrikan | **Satu-satunya sumber sah** untuk angka yang melekat pada produk tertentu |
| **R5** | **Sumber sekunder** | Tesis, disertasi, makalah, buku putih, panduan vendor | **Penunjuk, bukan sandaran.** Dipakai untuk menemukan sumber primernya |

---

## Aturan pemakaian menurut jenis keluaran

| Keluaran | Tingkat minimum | Alasan |
|---|---|---|
| **Ambang lulus/tidak lulus dalam berita acara** | **R1 → R2 → kontrak** | Yang diperiksa auditor. R3 saja tidak dapat dipertahankan |
| **Angka melekat produk** (derating, efisiensi, DoD, umur siklus, kurva laju) | **R4 wajib** | Berbeda antar produk. R3 memberi kerangka, bukan angkanya |
| **Metode dan rumus perhitungan** | **R2 atau R3** | R3 sah di sini — buku memang tempat rumus dijelaskan |
| **Keputusan rancangan** (topologi, konfigurasi, pendekatan) | **R3 cukup**, dinyatakan | Keputusan rancangan memang penilaian rekayasa |
| **Latar dan pembahasan** | **R3 atau R5** | Tidak ada akibat mengikat |
| **Dasar hukum** | **R1 mutlak** | Tesis yang menyebut UU **bukan** dasar hukum |

### Empat larangan

1. **R5 tidak pernah menjadi sandaran akhir.** Tesis yang mengutip UU 11/2008 adalah
   petunjuk bahwa UU-nya perlu dibuka. Yang masuk dokumen adalah **pasal dari UU-nya**.
2. **R3 tidak menetapkan ambang terima**, kecuali kontrak menyebutnya secara tertulis
   sebagai acuan. Bila diadopsi, sebutkan: *"ambang mengacu Gill (2008) sebagaimana
   diadopsi pasal … kontrak"*.
3. **R4 tidak boleh digantikan taksiran.** Bila lembar data belum ada, tulis
   **"menunggu data pabrikan"** — bukan angka umum.
4. **Tingkat tidak naik karena diulang.** Angka R3 yang dikutip di tiga dokumen tetap R3.

---

## Penurunan mutu karena usia

Berlaku pada R2 dan R3. Sumber tidak berubah tingkatnya, tetapi **wajib disertai
peringatan** bila melewati ambang usia:

| Umur terbitan | Perlakuan |
|---|---|
| < 5 tahun | Dipakai apa adanya |
| 5–15 tahun | Dipakai; **periksa apakah ada edisi lebih baru** bila menyangkut angka batas |
| > 15 tahun | Dipakai untuk **prinsip dan metode**; **angka batas dan rujukan standarnya wajib diperiksa ulang** |

Contoh di rak ini: Crompton (2000), Emadi (2004), Mahon (2004), Troppens (2009), dan
Nyman & Levitt (2010) melewati 15 tahun. Kerangka hitungnya
tetap sahih; angka produknya harus dari R4.

---

## Penanda dalam dokumen

Tulis tingkatnya melekat pada kutipan, di kurung siku:

> Ambang tahanan isolasi 100 MΩ untuk peralatan 600 V **[R2, ANSI/NETA ATS-2017,
> Tabel 100.1, PDF 223]**.

> Faktor derating genset pada 700 mdpl dan 35 °C **[R4, menunggu surat pabrikan]**.

> Interval uji beban dihitung dari MTBF gagal start **[R3, Moubray, RCM II, PDF 198]**,
> diadopsi sebagai ketentuan pemeliharaan pada pasal … kontrak.

Penanda ini yang memungkinkan pemeriksa **menilai bobot sebuah angka tanpa membuka
sumbernya** — dan yang membuat kelemahan terlihat sebelum dipersoalkan pihak lain.

---

## Peringatan menyeluruh untuk rak ini

Rak GSP saat ini berisi **R2, R3, dan R5. Tidak ada R1. Tidak ada R4.**

| Tingkat | Jumlah di rak |
|---|---|
| R1 — regulasi Indonesia | **0** |
| R2 — standar internasional | **5** |
| R3 — buku teks | **24** |
| R4 — dokumentasi OEM | **0** (memang selalu dari luar) |
| R5 — sekunder | **3** + 21 makalah |

**Akibat praktisnya, dan ini yang harus disadari sebelum menyusun dokumen apa pun:**

- Tidak ada satu pun ambang di rak ini yang **mengikat secara hukum Indonesia**. Setiap
  pekerjaan yang menuntut kepatuhan PUIL/SNI harus mengambil dari luar rak.
- Setiap angka melekat produk **harus** diminta ke pabrikan. Rak tidak dapat menggantikannya
  dan tidak dirancang untuk itu.

Ini bukan cacat yang harus disembunyikan — ini **batas yang harus dinyatakan**. Dokumen
yang menyatakan batasnya lebih kuat daripada dokumen yang menyamarkannya.
