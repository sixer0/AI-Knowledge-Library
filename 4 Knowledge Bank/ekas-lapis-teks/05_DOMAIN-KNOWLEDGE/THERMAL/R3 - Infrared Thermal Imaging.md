# Resume — Infrared Thermal Imaging: Fundamentals, Research and Applications

**Penulis:** Michael Vollmer, Klaus-Peter Möllmann · **Edisi:** kedua · **Penerbit:** Wiley-VCH, 2018
**Berkas:** `Michael Vollmer, Klaus-Peter Möllmann - Infrared Thermal Imaging (2nd Edition, 2018).pdf` — 787 halaman, 46,6 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark bawaan 301 entri sudah tersedia.

Buku **fisika termografi inframerah** yang lengkap, ditulis dua fisikawan. Bukan panduan
memakai kamera termal merek tertentu — ini yang menjelaskan **mengapa** hasil pengukuran
termal bisa menyesatkan dan bagaimana menghindarinya.

Untuk GSP, dua kegunaannya: mendukung pemeriksaan termal instalasi listrik, dan menilai
klaim kamera termal pada sistem pengawasan.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| — | Preface edisi kedua · List of Acronyms | 15 · 20 |
| 1 | **Fundamentals of Infrared Thermal Imaging** | 22 |
| 2 | **Basic Properties of IR Imaging Systems** | 128 |
| 3 | **Advanced Methods in IR Imaging** | 250 |
| 4 | Some Basic Concepts in Heat Transfer | 371 |
| 5 | Basic Applications for Teaching | 413 |
| 6 | **Shortwave Infrared Thermal Imaging (SWIR)** | 467 |
| 7 | **IR Imaging of Buildings and Infrastructure** | 497 |
| 8 | **Industrial Application: Detection of Gases** | 580 |
| 9 | Microsystems | 633 |
| 10 | **Selected Topics in Industry** | 663 |
| 11 | Selected Applications in Other Fields | 727 |
| — | Index | 783 |

---

## Bagian yang paling sering dipakai

### A. Dasar termografi (Bab 1, PDF 22)

Radiasi benda hitam, **emisivitas**, dan hubungan suhu dengan radiasi terukur.

**Emisivitas adalah sumber kesalahan terbesar dalam pengukuran termal di lapangan.**
Permukaan logam mengkilap memancarkan jauh lebih sedikit radiasi daripada permukaan cat
kusam pada suhu yang sama — sehingga busbar tembaga panas bisa terbaca dingin. Bab ini yang
menjelaskan mengapa, dan apa yang harus dilakukan.

### B. Sifat sistem pencitra IR (Bab 2, PDF 128)

Detektor, resolusi spasial dan termal, laju bingkai, dan rentang spektral. Bagian yang
dipakai saat **membaca spesifikasi kamera termal** — termasuk memahami perbedaan NETD,
resolusi detektor, dan IFOV, tiga angka yang sering dicampuradukkan dalam brosur.

### C. Metode lanjut (Bab 3, PDF 250)

Teknik pengukuran yang lebih teliti, termasuk penanganan pantulan dan koreksi lingkungan.

### D. SWIR (Bab 6, PDF 467)

Pencitraan inframerah gelombang pendek — rentang berbeda dari termal gelombang panjang,
dengan penerapan berbeda pula. Relevan saat menilai tawaran kamera yang menyebut "SWIR"
sebagai keunggulan.

### E. Bangunan dan infrastruktur (Bab 7, PDF 497)

Pemeriksaan termal selubung bangunan, kebocoran panas, dan kelembapan. Relevan untuk
pemeriksaan gedung pelanggan.

### F. Topik industri terpilih (Bab 10, PDF 663)

Termasuk pemeriksaan instalasi listrik — **deteksi titik panas pada panel, sambungan, dan
pemutus daya**. Ini penerapan yang paling sering diminta pada kontrak pemeliharaan.
Bertemu dengan `R3/ELECTRICAL/` (Gill) Bab 12 tentang pemeliharaan prediktif.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3 + K-5 (kalimat di atas): pointer ke Gill Bab 12 tidak menyimpan angka ambang termal - resume Gill nol kemunculan istilah termal (ukur grep -i), Bab 12 = 'Power Quality, Harmonics, Predictive Maintenance' PDF 754; kriteria ΔT dari NETA [R2]. Label `R3/ELECTRICAL/` adalah tingkat, bukan path: direktori `R3` tidak ada di `ekas/05_DOMAIN-KNOWLEDGE/` (register K-5); path nyata `ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/`.

### G. Deteksi gas (Bab 8, PDF 580)

Pencitraan optik gas. Penerapan khusus, relevan bila pelanggan menangani bahan berbahaya.

---

## Perhitungan siap pakai

Pada termografi, "perhitungan" yang menentukan hasil bukan rumus panjang, melainkan
**parameter yang harus disetel benar pada kamera**. Salah satu saja meleset, angka suhu
yang terbaca salah — dan kesalahannya tidak kelihatan, karena kamera tetap menampilkan
angka yang meyakinkan.

### 1. Parameter wajib sebelum mengukur (PDF 25)

Buku mendaftar parameter yang memengaruhi nilai suhu terukur:

| Parameter | Keterangan |
|---|---|
| **Emisivitas objek** | Yang paling menentukan; lihat butir 2 |
| **Jarak kamera ke objek** | Menentukan koreksi atmosfer |
| **Ukuran objek** | Terkait resolusi spasial; lihat butir 3 |
| **Kelembapan relatif** | Penyerapan oleh uap air |
| **Suhu lingkungan** | Radiasi pantulan dari sekitar |
| **Suhu atmosfer** | Koreksi jalur udara |
| **Suhu optik eksternal** | Bila memakai lensa tambahan |
| **Transmisi optik eksternal** | Bila memakai lensa tambahan |

> **Catatan penting dari buku (PDF 25):** sebagian kamera memungkinkan parameter ini
> **diubah setelah perekaman** dengan perangkat lunak yang sesuai — tetapi **ini tidak
> berlaku pada model termurah**. Bila kamera tidak mendukungnya, parameter salah berarti
> pengukuran harus diulang di lapangan. Periksa kemampuan ini sebelum membeli.

### 2. Emisivitas — sumber kesalahan terbesar

Prinsipnya (Bab 1, PDF 22): radiasi yang terukur bergantung pada suhu **dan** emisivitas
permukaan. Dua permukaan bersuhu sama memancarkan radiasi berbeda bila emisivitasnya
berbeda.

**Akibat praktis di lapangan:** busbar tembaga mengkilap punya emisivitas rendah, sehingga
**terbaca jauh lebih dingin daripada suhu sebenarnya**. Sambungan yang sudah panas
berbahaya bisa lolos pemeriksaan.

Penanganan yang lazim: ukur pada permukaan ber-emisivitas tinggi di dekatnya (cat kusam,
selubung isolasi, pita uji), atau setel emisivitas sesuai bahan — bukan membiarkannya di
nilai bawaan.

### 3. Resolusi spasial — apakah objeknya cukup besar untuk diukur

Bab 2 (PDF 128) membahas resolusi spasial dan termal. Tiga besaran yang sering
dicampuradukkan dalam brosur:

| Besaran | Artinya | Menentukan |
|---|---|---|
| **Resolusi detektor** | Jumlah piksel, mis. 640 × 480 | Detail gambar |
| **IFOV** | Sudut pandang satu piksel | **Ukuran objek terkecil yang dapat diukur** |
| **NETD** | Beda suhu terkecil yang terdeteksi | Kepekaan, mis. < 30 mK |

> **Aturan yang menentukan sah tidaknya pengukuran:** objek harus menutupi **beberapa
> piksel**, bukan satu. Bila objek lebih kecil dari IFOV pada jarak itu, nilai yang terbaca
> adalah campuran objek dan latar belakangnya — bukan suhu objek. Ini alasan sambungan
> kecil harus diukur dari jarak dekat atau dengan lensa tele.

### 4. Pantulan (Bab 1, PDF 33 dan Bab 3, PDF 250)

Permukaan memantulkan radiasi dari lingkungan, mulai dari pantulan terarah (spekular)
sampai baur. Bagian pantulan dan transmisi bergantung sudut datang dan dapat dihitung dari
**persamaan Fresnel** — buku menyatakan untuk keperluannya hasil grafis sudah memadai.

**Akibat praktis:** panel logam mengkilap dapat memantulkan citra termal orang yang
memeriksanya, tampak sebagai "titik panas" palsu. Ubah sudut pandang untuk memastikan
apakah titik panas ikut berpindah — kalau ikut, itu pantulan.

### Yang tidak ada di buku ini

Buku **tidak memberi tabel ambang suhu lulus/tidak lulus** untuk pemeriksaan panel listrik
(mis. "ΔT di atas 20 °C = kritis"). Kriteria semacam itu berasal dari standar pemeliharaan
seperti NETA, bukan dari buku fisika ini. Untuk kriteria penilaian, lihat
`R3/ELECTRICAL/` Bab 12 dan standar yang berlaku.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-11 (angka 20 °C pada paragraf di atas): JEBAKAN ANTI-CONTOH. Paragraf ini justru menyatakan buku TIDAK memberi ambang; 20 °C muncul satu-satunya di rak termal sebagai contoh hal yang tidak ada. DILARANG mengutip lepas 'Vollmer: ΔT 20 °C = kritis' - kutipan seperti itu persis pola penyebaran Tabel 7. Ambang ΔT sah hanya dari ANSI/NETA ATS-2017 Tabel 100.18 [R2] (register K-11).
> K-3 (pointer kriteria di akhir paragraf di atas): arah rujukan bertentangan dengan penetapan rak sendiri. 'Kriteria penilaian' yang dikirim ke `R3/ELECTRICAL/` Bab 12 TIDAK ada di sana (resume Gill 0 kemunculan istilah termal); kriteria yang dipakai rak = Tabel 100.18 [R2] di `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92`. Kelas cacat pointer: alamat menuju tempat yang tidak menyimpan angkanya (register K-3).

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Prosedur pemeriksaan termal panel listrik | Bab 10, PDF 663 + Bab 1 (emisivitas), PDF 22 |
| Membaca spesifikasi kamera termal | Bab 2, PDF 128 |
| Menilai klaim kamera termal pada sistem pengawasan | Bab 2 dan Bab 6, PDF 128 dan 467 |
| Menjelaskan hasil ukur yang janggal | Bab 1 (emisivitas) dan Bab 3 (pantulan) |
| Pemeriksaan termal bangunan | Bab 7, PDF 497 |
| Dasar perpindahan panas | Bab 4, PDF 371 |

**Pendamping di rak:** `R3/ELECTRICAL/` (Gill) Bab 12 untuk penerapannya pada
pemeliharaan prediktif instalasi listrik, `R3/CCTV-VSS/` (Damjanovski) untuk sisi sistem
pengawasannya.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 (label `R3/ELECTRICAL/` dan `R3/CCTV-VSS/` pada kalimat di atas): label tingkat, bukan path mesin - direktori `R3` tidak ada di `ekas/05_DOMAIN-KNOWLEDGE/` (terukur). Path nyata: `ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/` dan `ekas/05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/`; laci sumber = `ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/<DOMAIN>/`. Sah sebagai singkatan manusia, berbahaya sebagai resolve path (register K-5).

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 301 entri sudah terbaca.
- Edisi kedua 2018 — termasuk yang lebih baru di rak.
- Sifatnya buku fisika terapan dengan pembahasan matematis. Untuk pemakaian praktis,
  Bab 1, 2, dan 10 sudah mencukupi.
- Isinya tidak pernah diubah, jadi tidak ada cadangan `_asli/`.
