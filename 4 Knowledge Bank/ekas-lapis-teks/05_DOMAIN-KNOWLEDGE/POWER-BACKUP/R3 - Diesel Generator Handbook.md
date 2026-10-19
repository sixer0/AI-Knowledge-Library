# Resume — Diesel Generator Handbook

**Penulis:** L. L. J. Mahon · **Penerbit:** Elsevier / Newnes, 2004
**Berkas:** `L. L. J. Mahon - Diesel Generator Handbook (2004).pdf` — 578 halaman, 12,5 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> ### ⚠ Berkas ini tidak lengkap
> Sekitar **55 halaman hilang**: **Bab 11 "Emergency and standby" seluruhnya** dan bagian
> awal Bab 12. Nomor halaman cetak melompat dari 394 (PDF 388) ke 450 (PDF 391), di tengah
> kalimat. Penyebabnya: berkas dirakit dari potongan `1.pdf`–`13.pdf` dan potongan `10.pdf`
> tidak ikut.
>
> **Bab 11 justru bab yang paling relevan untuk pekerjaan genset cadangan.** Penanda sudah
> dipasang di daftar isi berkas, tetapi isi yang hilang perlu dicarikan salinan pengganti.

> **Rujukan halaman memakai nomor PDF.** Bookmark 21 entri dibangun ulang 19 Agustus 2026
> dari daftar isi mini yang ada di halaman pembuka tiap bab.

Buku rujukan menyeluruh tentang unit pembangkit diesel — dari mesin penggeraknya sampai
pemasangan dan pemeliharaan di lokasi.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| — | Preface | 5 |
| 1 | Reciprocating internal combustion engines | 7 |
| 2 | **Power rating and performance** | 34 |
| 3 | A.C. generators — general | 46 |
| 4 | A.C. generators — performance characteristics | 93 |
| 5 | **Load considerations** | 136 |
| 6 | Engine governing | 183 |
| 7 | Automatic voltage regulation | 213 |
| 8 | **Parallel operation of generating sets** | 242 |
| 9 | Switchgear and controlgear | 279 |
| 10 | Prime mover and generator protection | 340 |
| ⚠ | **HILANG — Bab 11 + awal Bab 12** (cetak 395–449) | 389 |
| 12 | Fuels and lubricating oils *(hanya bagian akhir)* | 389 |
| 13 | **Installation and commissioning** | 397 |
| 14 | Plant noise reduction | 473 |
| 15 | **Operation and maintenance** | 539 |
| A | Useful conversion factors | 556 |
| B | Batteries | 559 |
| C | Soil resistivity measurements | 564 |
| D | Device function numbers | 566 |
| — | Index | 568 |

---

## Bagian yang paling sering dipakai

### A. Klasifikasi rating daya (Bab 2, PDF 34–36)

Bagian paling penting saat menyusun spesifikasi pengadaan. Buku memperingatkan (PDF 36):

> Berhati-hatilah terhadap klasifikasi rating yang didefinisikan longgar. *Standby rating*,
> *continuous duty with time-limitation*, *reserve rating*, dan *intermittent rating*
> hanyalah beberapa klasifikasi yang bermunculan.

**Implikasi praktis:** menyebut "genset 500 kVA" tanpa menyebut kelas ratingnya membuat
penawaran tidak dapat dibandingkan. Rating harus disebut eksplisit dalam RAB dan spesifikasi.

Parameter unjuk kerja yang perlu ditetapkan (PDF 35): **load acceptance**, regulasi tegangan
dan frekuensi (transien maupun mantap), serta batasan harmonisa pada bentuk gelombang.

### B. Pertimbangan beban (Bab 5, PDF 136)

Penilaian beban, penentuan kapasitas, dan unsur beban yang memengaruhi ukuran dan unjuk kerja
unit. Dipakai saat menghitung kapasitas genset untuk beban pelanggan — termasuk beban dengan
arus start besar.

### C. Operasi paralel (Bab 8, PDF 242)

Untuk konfigurasi lebih dari satu unit: pembagian beban, sinkronisasi, pemerataan daya
reaktif. Relevan pada instalasi dengan redundansi.

### D. Pemasangan dan komisioning (Bab 13, PDF 397)

Tata letak, kategori instalasi, dan prosedur komisioning. Dipakai menyusun kerangka berita
acara serah terima unit.

### E. Pengurangan kebisingan (Bab 14, PDF 473)

Sering jadi persyaratan pada lokasi perkotaan dan gedung pemerintahan. Bab tersendiri, cukup
rinci.

### F. Operasi dan pemeliharaan (Bab 15, PDF 539)

Dasar penyusunan program pemeliharaan berkala unit. Dipakai bersama **Moubray, *RCM II*** dan **Gulati, *Maintenance & Reliability Best
Practices*** — keduanya di `R3/RCM/` — untuk menentukan tugas dan intervalnya secara berdasar.

### G. Apendiks B — Baterai (PDF 559)

Baterai starter genset. Bertemu dengan `R3/BATTERY/` (Crompton) di rak untuk penentuan kapasitas.

### H. Apendiks C — Pengukuran resistivitas tanah (PDF 564)

Untuk pembumian unit. Bertemu dengan `R3/GROUNDING/` Bab 10.

---

## Perhitungan siap pakai

### 1. Derating terhadap kondisi lingkungan (PDF 40–42)

Mesin diesel menghirup udara. **Kerapatan udara menentukan daya yang dapat dihasilkan**,
dan kerapatan itu dipengaruhi tiga hal (PDF 40):

| Faktor | Pengaruh |
|---|---|
| **Suhu lingkungan naik** | Udara lebih hangat → kerapatan turun → daya turun |
| **Ketinggian naik** | Tekanan barometrik turun → kerapatan turun → daya turun |
| **Kelembapan relatif naik** | Uap air menggantikan udara → kerapatan turun |

> **Konsekuensi untuk pengadaan:** daya nameplate berlaku pada kondisi acuan pabrikan.
> Untuk lokasi panas atau berketinggian — dan sebagian besar lokasi di Indonesia panas —
> **daya tersedia lebih kecil daripada nameplate.** Faktor deratingnya harus diminta dari
> pabrikan untuk kondisi lokasi yang sebenarnya, dan dicantumkan dalam spesifikasi.

Buku juga mencatat kasus khusus (PDF 42): suhu udara manifold sekitar **8 °C di atas suhu
lingkungan** menghasilkan derating daya yang besar. Solusinya sistem pendingin
**udara-ke-udara** (air-to-air charge cooling), yang membuat derating akibat suhu manifold
umumnya tidak diperlukan lagi kecuali pada suhu lingkungan sangat tinggi.

### 2. Kelas rating harus disebut, bukan hanya kVA (PDF 35–36)

Buku memperingatkan agar berhati-hati terhadap klasifikasi rating yang didefinisikan
longgar: *standby*, *continuous duty with time-limitation*, *reserve*, *intermittent* —
dan masih banyak lagi yang bermunculan.

Parameter unjuk kerja yang perlu ditetapkan bersama rating (PDF 35):

- **Load acceptance** — kemampuan menerima beban mendadak
- **Regulasi tegangan dan frekuensi** — keadaan transien maupun mantap
- **Karakteristik bentuk gelombang** — batasan harmonisa

> **Aturan praktis untuk RAB dan spesifikasi:** menyebut "genset 500 kVA" saja membuat
> penawaran tidak dapat dibandingkan. Yang harus tertulis: **kVA + kelas rating + kondisi
> lokasi (suhu, ketinggian) + load acceptance yang disyaratkan.**

### 3. Kerangka penentuan kapasitas

Dari Bab 5 (PDF 136) tentang pertimbangan beban:

```
kVA genset  ≥  (beban puncak ÷ faktor daya)  ×  faktor derating lokasi  ×  margin pertumbuhan
```

dengan pemeriksaan terpisah bahwa **arus start beban terbesar** masih dalam kemampuan
load acceptance unit. Untuk beban dengan motor besar, pemeriksaan kedua ini yang sering
menentukan ukuran — bukan beban puncak tunak.

### Yang tidak ada di berkas ini

**Bab 11 "Emergency and standby" hilang** — bab yang membahas penerapan genset sebagai
catu daya darurat, termasuk skema peralihan dan persyaratan waktu start. Untuk pekerjaan
genset cadangan, bagian itu harus diambil dari sumber lain sampai salinan pengganti
diperoleh.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menyusun spesifikasi pengadaan genset | Bab 2, PDF 34–36 — **sebut kelas ratingnya** |
| Menghitung kapasitas dari profil beban | Bab 5, PDF 136 |
| Konfigurasi redundansi / paralel | Bab 8, PDF 242 |
| Berita acara komisioning | Bab 13, PDF 397 |
| Persyaratan kebisingan | Bab 14, PDF 473 |
| Program pemeliharaan berkala | Bab 15, PDF 539 |
| Pembumian unit | Apendiks C + `R3/GROUNDING/` |
| **Sistem emergency & standby** | ⚠ **tidak ada di berkas ini** — Bab 11 hilang |

**Pendamping di rak:** `R3/UPS/` untuk catu daya tak terputus, `R3/BATTERY/` untuk baterai starter,
`R3/ELECTRICAL/` untuk pengujian instalasinya, `R3/GROUNDING/` untuk pembumian.

---

## Catatan mutu berkas

- Teks dapat dicari.
- **Outline lama berisi 2.377 entri sampah** keluaran alat OCR (`page1`, `images`, `tableN`),
  banyak menunjuk halaman −1. Diganti seluruhnya dengan 21 entri bersih pada 19 Agustus 2026.
- **Isi tidak lengkap** — lihat peringatan di atas.
- Terbitan 2004; prinsip mesin dan generator tidak berubah, tetapi rujukan standar dan
  praktik kontrol elektronik modern perlu diperiksa terhadap sumber yang lebih baru.
- Cadangan sebelum perbaikan bookmark: `_asli/Diesel Generator Handbook [ASLI sebelum perbaikan bookmark].pdf`
