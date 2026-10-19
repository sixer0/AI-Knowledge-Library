# Resume — Uninterruptible Power Supplies and Active Filters

**Penulis:** Ali Emadi, Abdolhosein Nasiri, Stoyan B. Bekiarov · **Penerbit:** CRC Press, 2004
**Berkas:** `Ali Emadi, Abdolhosein Nasiri, Stoyan B. Bekiarov - Uninterruptible Power Supplies and Active Filters (2004).pdf` — 285 halaman, 15,2 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark 218 entri berjenjang lima tingkat —
> sampai sub-sub-bagian — sudah tersedia.

Buku **elektronika daya**, bukan buku pemilihan produk. Membahas topologi UPS dan penyaring
aktif dari sisi rangkaian dan kendalinya. Nilainya untuk GSP: menjelaskan **mengapa** satu
topologi berperilaku berbeda dari yang lain, sehingga penawaran vendor bisa dinilai dari
prinsipnya, bukan dari brosurnya.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| — | Preface · Biography · Contents | 7 · 8 · 10 |
| 1 | **Uninterruptible Power Supplies** | 16 |
| 2 | **Active Filters** | 78 |
| 3 | Unified Power Quality Conditioners | 131 |
| 4 | Reduced-Parts Uninterruptible Power Supplies | 147 |
| 5 | Reduced-Parts Active Filters | 225 |
| 6 | Modeling, Analysis, and Digital Control | 258 |

Bookmark rincinya turun sampai tingkat seperti `1.1.1.1.1 Normal Mode of Operation`,
jadi topologi tertentu bisa dituju langsung dari panel daftar isi.

---

## Bagian yang paling sering dipakai

### A. Klasifikasi UPS (Bab 1, PDF 16 dst.)

Tiga golongan utama beserta mode operasinya, masing-masing dengan sub-bagian sendiri:

| Topologi | PDF | Ciri |
|---|---|---|
| **On-line (double conversion)** | 19 | Beban terus dipasok lewat penyearah dan inverter |
| **Off-line** | 21 | Beban normalnya langsung dari jala-jala |
| **Line-interactive** | 23 | Di antara keduanya |

Tiap topologi dirinci ke **normal mode**, **stored-energy mode**, dan (untuk on-line)
**bypass mode**.

**Kunci pembedanya** (PDF 19): pada UPS on-line terjadi **konversi ganda** — AC/DC lalu
DC/AC. Penyearah mengisi baterai sekaligus memasok inverter. Karena beban selalu dipasok
dari inverter, **pengondisian jala-jala sangat baik** — itu alasan teknis mengapa on-line
dipilih untuk beban sensitif seperti ruang server dan sistem pengawasan, meski efisiensinya
lebih rendah dan harganya lebih tinggi.

Selain itu dibahas **rotary UPS** dan **hybrid static/rotary** — jarang dipakai di lingkup
GSP, tetapi berguna saat menghadapi instalasi warisan.

### B. Penyaring aktif (Bab 2, PDF 78)

Definisi harmonisa, sumbernya, dan cara penyaring aktif menanganinya. Relevan saat beban
non-linier pelanggan — UPS, VSD, catu daya switching, lampu LED dalam jumlah besar —
menimbulkan masalah pada instalasi.

### C. Unified Power Quality Conditioner (Bab 3, PDF 131)

Gabungan penyaring seri dan paralel. Untuk kasus kualitas daya yang tidak selesai dengan
satu jenis penyaring saja.

### D. Topologi hemat komponen (Bab 4–5, PDF 147 dan 225)

Bagian terpanjang buku. Membahas rancangan dengan jumlah komponen dikurangi — latar belakang
teknis di balik perbedaan harga dan keandalan antar produk di pasar.

### E. Pemodelan dan kendali digital (Bab 6, PDF 258)

Sisi kendali. Dipakai bila perlu memahami perilaku transien saat peralihan sumber.

---

## Perhitungan siap pakai

### 1. Efisiensi — pertukaran yang melekat pada topologi (PDF 20)

Buku menyatakan tegas: UPS on-line **tidak dapat memanfaatkan jaringan listrik dan instalasi
lokal secara efisien**, dan **efisiensi rendah itu melekat pada topologinya** karena sifat
konversi ganda. Aliran daya melewati penyearah dan inverter selama operasi normal berarti
**rugi daya lebih besar dan efisiensi lebih rendah** dibanding UPS off-line dan
line-interactive.

> **Konsekuensi yang harus masuk perhitungan:** memilih on-line untuk beban sensitif adalah
> keputusan yang benar, tetapi **berbayar dalam bentuk rugi daya terus-menerus**. Rugi itu
> menjadi panas yang harus dibuang pendingin ruangan — jadi muncul dua kali dalam
> perhitungan: sebagai konsumsi listrik dan sebagai beban pendinginan.

```
Rugi daya (W)      =  daya beban (W) × (1 ÷ efisiensi − 1)
Beban pendinginan  =  rugi daya (W)          [seluruhnya menjadi panas]
```

*Contoh ilustrasi:* beban 10 kW pada UPS on-line berefisiensi 92%
→ rugi = 10.000 × (1 ÷ 0,92 − 1) ≈ **870 W** yang terbuang menjadi panas, terus-menerus.
Angka efisiensi harus diambil dari lembar data produk — **jangan dari buku ini**, karena
efisiensi UPS masa kini jauh di atas era 2004.

### 2. Koreksi faktor daya (bagian 1.8, PDF 17 dst.)

Buku membahas **Power Factor Correction** pada UPS, dibagi teknik **pasif** (1.8.1) dan
**aktif** (1.8.2). Relevan karena UPS adalah beban non-linier: tanpa PFC, ia menimbulkan
harmonisa pada instalasi hulu.

Ini yang menghubungkan Bab 1 dengan Bab 2 buku ini — masalah yang ditimbulkan UPS
diselesaikan dengan teknik yang sama seperti penyaring aktif.

### 3. Kerangka penentuan kapasitas

```
kVA UPS  ≥  (total daya beban ÷ faktor daya beban)  ×  margin pertumbuhan
```

dengan tiga pemeriksaan tambahan yang sering terlewat:

1. **Arus puncak (crest factor) beban** — catu daya switching menarik arus berbentuk pulsa,
   bukan sinus; UPS harus sanggup melayaninya
2. **Waktu cadangan** → menentukan bank baterai, bukan kVA. Perhitungannya di resume
   `R3/BATTERY/`
3. **Beban pendinginan** dari rugi daya — lihat butir 1

### Yang tidak ada di buku ini

- **Angka efisiensi produk masa kini** — buku terbit 2004. Topologi **eco-mode** dan
  **UPS modular** belum ada di dalamnya.
- **Rumus perhitungan waktu cadangan baterai** — itu ada di ranah `R3/BATTERY/` (Crompton).

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Memilih topologi UPS untuk ruang server / pusat kendali | Bab 1, PDF 16–26 |
| Membela pemilihan on-line dalam kajian teknis | PDF 19 (konversi ganda, pengondisian jala-jala) |
| Menjawab masalah harmonisa di instalasi pelanggan | Bab 2, PDF 78 |
| Menilai perbedaan harga antar produk sejenis | Bab 4–5 (topologi hemat komponen) |
| Perilaku saat peralihan sumber | Bab 6, PDF 258 |
| Penentuan kapasitas baterainya | → `R3/BATTERY/` (Crompton) |
| Pembumian unit | → `R3/GROUNDING/` Bab 7 |

**Pendamping di rak:** `R3/BATTERY/` untuk penentuan kapasitas dan waktu cadangan,
`R3/GENSET/` untuk catu daya cadangan berikutnya, `R3/ELECTRICAL/` Bab 12 untuk
kualitas daya dari sisi pengujian, `R3/GROUNDING/` Bab 7 untuk pembumiannya.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark 218 entri lima tingkat.
- **Outline lama terkubur di bawah dua lapis pembungkus** bernama `3035_c00.pdf` dst.
  Pembungkusnya dikupas 19 Agustus 2026; struktur asli di bawahnya ternyata utuh dan benar.
- **Terbitan 2004 — ini buku tertua kedua di rak setelah Battery.** Prinsip elektronika
  dayanya tetap sahih, tetapi **efisiensi, kerapatan daya, dan fitur UPS modern sudah jauh
  berubah**; topologi eco-mode dan UPS modular belum tercakup. Untuk angka efisiensi dan
  spesifikasi produk masa kini, jangan mengutip buku ini — pakai sebagai penjelas prinsip.
- Cadangan sebelum perbaikan bookmark: `_asli/UPS and Active Filters [ASLI sebelum perbaikan bookmark].pdf`
