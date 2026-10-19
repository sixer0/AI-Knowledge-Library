# Resume — Computer Vision: Algorithms and Applications

**Penulis:** Richard Szeliski · **Edisi:** kedua · **Penerbit:** Springer, 2022
**Berkas:** `Richard Szeliski - Computer Vision Algorithms and Applications (2nd Edition, 2022).pdf` — 938 halaman, 26,5 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark bawaan 354 entri sampai tingkat
> sub-bagian sudah ada.

Buku rujukan baku visi komputer, ditulis Richard Szeliski (mantan Microsoft Research,
kini Facebook/Meta). Fungsinya di rak ini: **landasan ilmiah untuk menilai klaim produk
analitik video** — bukan buku cara memakai perangkat lunak analitik.

Edisi kedua (2022) menambahkan satu bab penuh **Deep Learning** dan memperbarui bab
pengenalan objek dengan pendekatan berbasis jaringan saraf, sehingga sudah sejalan dengan
generasi produk analitik yang beredar sekarang.

---

## Peta isi

| Bab | Judul | PDF | Kaitan dengan analitik video |
|---|---|---|---|
| 1 | Introduction | 23 | Ruang lingkup dan sejarah |
| 2 | Image formation | 49 | Optik, sensor, warna, pencahayaan |
| 3 | Image processing | 106 | Penapisan, piramida, transformasi |
| 4 | Model fitting and optimization | 173 | Dasar matematis pencocokan |
| 5 | **Deep Learning** | 207 | Landasan produk analitik modern |
| 6 | **Recognition** | 292 | Deteksi & pengenalan objek, wajah |
| 7 | **Feature detection and matching** | 351 | SIFT dan sejenisnya |
| 8 | Image alignment and stitching | 418 | Penggabungan citra multi-kamera |
| 9 | **Motion estimation** | 459 | Optical flow, pelacakan gerak |
| 10 | Computational photography | 499 | HDR, penajaman, low-light |
| 11 | Structure from motion and SLAM | 559 | Rekonstruksi posisi dari citra |
| 12 | Depth estimation | 611 | Stereo, kedalaman |
| 13 | 3D reconstruction | 655 | Model tiga dimensi |
| 14 | Image-based rendering | 697 | Perenderan dari citra |
| 15 | Conclusion | 739 | Penutup |
| A | Linear algebra and numerical techniques | 742 | Lampiran matematis |
| B | Bayesian modeling and inference | 757 | Lampiran statistik |
| C | Supplementary material | 769 | Bahan pendukung |
| — | References · Index | 783 · 918 |

---

## Bagian yang paling sering dipakai

### A. Deep learning (Bab 5, PDF 207)

Bab baru pada edisi kedua. Isinya dasar jaringan saraf konvolusional, pelatihan, dan
arsitektur yang menjadi mesin hampir semua produk analitik video komersial hari ini.

**Kegunaan praktis:** memahami apa yang sebenarnya dijanjikan vendor saat menyebut
"AI-based analytics", dan pertanyaan apa yang perlu diajukan — arsitektur apa, dilatih pada
data apa, bagaimana unjuk kerjanya pada kondisi yang berbeda dari data latih.

### B. Pengenalan objek dan wajah (Bab 6, PDF 292)

Deteksi objek, pengenalan wajah, dan segmentasi. Ini bab yang dipakai saat menilai klaim
akurasi produk analitik.

Yang perlu dipegang saat mengevaluasi: **angka akurasi tanpa menyebut kondisi ujinya tidak
bermakna.** Unjuk kerja sistem pengenalan sangat bergantung pada sudut pandang, pencahayaan,
resolusi di bidang objek, dan kemiripan kondisi lapangan dengan data latih. Ini bertemu
langsung dengan pembahasan kerapatan piksel di buku CCTV (Damjanovski) — analitik tidak bisa
mengenali apa yang tidak terekam cukup detail.

### C. Deteksi dan pencocokan fitur (Bab 7, PDF 351)

SIFT (PDF 116) dan penerus-penerusnya. Dasar bagi penjejakan objek antar-bingkai dan
pencocokan antar-kamera.

### D. Estimasi gerak (Bab 9, PDF 459)

Optical flow dan penjejakan. Landasan fitur analitik yang paling sering diminta pelanggan:
deteksi lintasan, perhitungan orang, deteksi objek tertinggal, dan deteksi arah berlawanan.

### E. Pembentukan citra (Bab 2, PDF 49)

Optik, sensor, dan warna dari sudut pandang komputasi — melengkapi Bab 3 dan 5 buku CCTV
yang membahasnya dari sudut pandang praktik pemasangan.

### F. Computational photography (Bab 10, PDF 499)

HDR dan pemrosesan kondisi cahaya sulit. Relevan saat pelanggan menuntut hasil rekaman baik
pada kondisi kontras tinggi — gerbang menghadap matahari, pintu masuk gelap ke terang.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menilai klaim akurasi produk analitik vendor | Bab 6, PDF 292 + Bab 5, PDF 207 |
| Menyusun pertanyaan teknis untuk vendor analitik | Bab 5, PDF 207 |
| Menjelaskan batas kemampuan analitik ke pelanggan | Bab 6 + kerapatan piksel di buku CCTV |
| Dasar fitur penjejakan dan perhitungan orang | Bab 9, PDF 459 |
| Penggabungan pandangan multi-kamera | Bab 8, PDF 418 |
| Kondisi cahaya sulit | Bab 10, PDF 499 |
| Rujukan ilmiah pada kajian teknis | Daftar pustaka, PDF 783 |

**Pendamping di rak:** `R3/CCTV-VSS/` (Damjanovski) — pasangan wajib. Szeliski menjelaskan apa
yang bisa dilakukan algoritma; Damjanovski menentukan apakah kamera merekam cukup detail
untuk algoritma itu bekerja. Klaim analitik yang tidak lolos uji kerapatan piksel tidak akan
terpenuhi seberapa pun canggih algoritmanya.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 354 entri sangat rinci.
- Edisi kedua 2022 — buku termutakhir di rak ini.
- Sifatnya buku teks akademis dengan notasi matematis padat. Untuk pemakaian sehari-hari,
  Bab 5, 6, dan 9 sudah mencukupi; lampiran matematis dipakai hanya bila perlu menelusuri
  turunan rumusnya.
- Isinya tidak pernah diubah, jadi tidak ada cadangan `_asli/`.
