# Resume — Reliability-centered Maintenance (RCM II)

**Penulis:** John Moubray · **Edisi:** kedua · **Penerbit:** Industrial Press / Butterworth-Heinemann
**Berkas:** `John Moubray - Reliability-centered Maintenance RCM II (2nd Edition).pdf` — 444 halaman, 89,5 MB
**Disusun:** 19 Agustus 2026, dari teks OCR buku ini (bukan dari sumber lain)

> **Cara membaca rujukan halaman.** Nomor halaman cetak di buku berselisih **+18** dengan
> nomor halaman PDF. Contoh: definisi RCM ada di halaman cetak 7 = **PDF 25**. Di seluruh
> dokumen ini ditulis `cetak 7 / PDF 25`. Bookmark PDF sudah dipasang (100 entri), jadi
> lompatan bab bisa lewat panel daftar isi.

---

## 1. Inti dalam satu halaman

RCM bukan metode merawat mesin. RCM adalah **metode memutuskan apa yang harus dilakukan**
agar aset terus melakukan apa yang dikehendaki penggunanya. Pergeseran ini yang membedakannya
dari pemeliharaan pencegahan klasik: fokusnya bukan pada *kondisi* aset, melainkan pada
*fungsi* yang aset itu jalankan dalam konteks operasi tertentu.

Dua definisi kunci (cetak 7 / PDF 25):

> **Maintenance:** memastikan aset fisik terus melakukan apa yang dikehendaki penggunanya.
>
> **Reliability-centered Maintenance:** proses untuk menentukan apa yang harus dilakukan agar
> setiap aset fisik terus melakukan apa yang dikehendaki penggunanya **dalam konteks operasi
> yang berlaku saat ini**.

Frasa "konteks operasi" bukan hiasan. Dua pompa identik di dua tempat berbeda bisa
menghasilkan program pemeliharaan yang berbeda, karena akibat kegagalannya berbeda.

### Tujuh pertanyaan RCM (cetak 7 / PDF 25)

| # | Pertanyaan | Dibahas di |
|---|---|---|
| 1 | Apa **fungsi** dan standar unjuk kerja aset dalam konteks operasi saat ini? | Bab 2 |
| 2 | Dengan cara apa aset **gagal memenuhi** fungsinya? (kegagalan fungsional) | Bab 3 |
| 3 | Apa **penyebab** tiap kegagalan fungsional? (moda kegagalan) | Bab 4 |
| 4 | Apa yang **terjadi** saat tiap kegagalan muncul? (efek kegagalan) | Bab 4 |
| 5 | Dengan cara apa tiap kegagalan **berarti**? (konsekuensi) | Bab 5 |
| 6 | Apa yang bisa dilakukan untuk **memprediksi atau mencegah** tiap kegagalan? | Bab 6–7 |
| 7 | Apa yang dilakukan bila **tugas proaktif yang cocok tidak ditemukan**? | Bab 8–9 |

Pertanyaan 1–4 dijawab pada **Information Worksheet**; pertanyaan 5–7 pada **Decision
Worksheet**. Dua lembar kerja itulah produk formal dari analisis RCM.

---

## Perhitungan siap pakai

| Perhitungan | Rumus | Lihat |
|---|---|---|
| **Interval tugas on-condition** | `interval = ½ × interval P-F` | Bab 7 · cetak 146 / PDF 164 |
| **Nett P-F interval** | `nett P-F = interval P-F − interval pemeriksaan` | Bab 7 · cetak 146 / PDF 164 |
| **Uji kelayakan on-condition** | `nett P-F > waktu yang dibutuhkan bertindak` | Bab 7 · cetak 148 / PDF 166 |
| **Interval failure-finding (sederhana)** | `FFI = 2 × ketaktersediaan × MTBF` | Bab 8 · cetak 177 / PDF 195 |
| **Interval failure-finding (lengkap)** | `FFI = 2 × M_perangkat × M_terproteksi ÷ M_majemuk` | Bab 8 · cetak 180 / PDF 198 |
| **Koreksi bila uji merusak** | kalikan `(1 − p)`; abaikan bila p < 0,05 | Bab 8 · cetak 181 / PDF 199 |

Contoh terhitung untuk masing-masing ada pada Bagian 2 (uraian per bab) dan Bagian 3
(tabel angka dan rumus) di bawah.

---

## 2. Ringkasan per bab

### Bab 1 — Introduction to Reliability-centered Maintenance (cetak 1 / PDF 19)

Latar perubahan: jumlah dan kerumitan aset melonjak, harapan terhadap pemeliharaan bergeser
ke keselamatan, lingkungan, mutu produk, dan ketersediaan. Bab ini memperkenalkan definisi,
tujuh pertanyaan, dan — bagian terpentingnya — **enam pola kegagalan** (cetak 13 / PDF 31).

Pandangan klasik menganggap tiap komponen punya "umur pakai" dan aus setelahnya. Studi pada
pesawat sipil menunjukkan sebaran yang jauh berbeda:

| Pola | Bentuk | Porsi |
|---|---|---|
| A | Kurva bak mandi: kematian dini tinggi → datar → zona aus | 4% |
| B | Datar/naik pelan → berakhir di zona aus (pandangan klasik) | 2% |
| C | Naik pelan terus, tanpa umur aus yang jelas | 5% |
| D | Rendah saat baru → naik cepat → datar | 7% |
| E | Datar di semua umur (kegagalan acak) | 14% |
| F | Kematian dini tinggi → turun ke datar | **68%** |

**Implikasi praktis:** 89% moda kegagalan (D+E+F) tidak terkait umur. Untuk kelompok itu,
batas umur dan overhaul terjadwal tidak memperbaiki keandalan — malah bisa memperburuk,
karena overhaul menyuntikkan kematian dini ke sistem yang tadinya stabil. Ini dasar
argumen paling sering dipakai saat menolak jadwal overhaul yang diwariskan tanpa dasar.

### Bab 2 — Functions (cetak 21 / PDF 39)

Menetapkan fungsi adalah menetapkan tujuan pemeliharaan. Fungsi ditulis sebagai
**kata kerja + objek + standar unjuk kerja yang terukur** — misal "memindahkan air dari
tangki X ke tangki Y pada laju tidak kurang dari 800 liter/menit".

- **Kemampuan awal aset harus melebihi standar unjuk kerja yang diinginkan**, karena harus
  ada ruang untuk penurunan kondisi. Bila tidak, aset tidak akan pernah bisa dirawat sampai
  memuaskan — itu masalah desain, bukan masalah pemeliharaan.
- **Fungsi primer** (alasan aset diadakan) dan **fungsi sekunder**. Buku memakai jembatan
  keledai **ESCAPES** untuk mendaftar fungsi sekunder (cetak 38 / PDF 56):
  **E**nvironmental integrity · **S**afety/structural integrity ·
  **C**ontrol/containment/comfort · **A**ppearance · **P**rotection ·
  **E**conomy/efficiency · **S**uperfluous functions.
  Kehilangan fungsi sekunder bisa berakibat lebih serius daripada kehilangan fungsi primer,
  sehingga sering menuntut pemeliharaan lebih banyak — bukan lebih sedikit.

### Bab 3 — Functional Failures (cetak 45 / PDF 63)

**Kegagalan** = ketidakmampuan aset melakukan apa yang dikehendaki penggunanya.
**Kegagalan fungsional** = keadaan gagal itu sendiri, dinyatakan relatif terhadap standar
unjuk kerja pada Bab 2. Satu fungsi bisa punya beberapa kegagalan fungsional: gagal total,
gagal sebagian, gagal di atas batas, gagal di bawah batas.

### Bab 4 — Failure Modes and Effects Analysis (cetak 53 / PDF 71)

**Moda kegagalan** = peristiwa apa pun yang menyebabkan kegagalan fungsional (cetak 53 / PDF 71).
Yang dicatat bukan "pompa rusak" melainkan peristiwanya: bantalan macet, impeler lepas,
kopling patah. Cakupannya termasuk kegagalan akibat keausan, kesalahan manusia (operator
maupun perawat), dan cacat desain.

- **Seberapa rinci?** (4.4) Tingkat analisis dipilih pada level yang menghasilkan jumlah moda
  kegagalan yang masih terkelola per fungsi. Terlalu rinci membuat analisis tak selesai;
  terlalu kasar membuat tugas pemeliharaan tak bisa ditetapkan.
- **Efek kegagalan** (4.5) menjawab "apa yang terjadi", bukan "apa akibatnya" — bukti bahwa
  kegagalan terjadi, bahaya terhadap keselamatan/lingkungan, dampak ke produksi, kerusakan
  fisik, dan apa yang harus dikerjakan untuk memperbaikinya.
- Keluarannya: **Information Worksheet** (Figure 4.13).

### Bab 5 — Failure Consequences (cetak 90 / PDF 108)

Bab paling menentukan. RCM tidak memperlakukan semua kegagalan sama; **konsekuensi** yang
menentukan apakah suatu tugas layak dikerjakan. Empat kategori:

| Kategori | Uji | Ukuran "layak dikerjakan" |
|---|---|---|
| **Hidden** (tersembunyi) | Kegagalan tidak terlihat operator saat keadaan normal | Menurunkan risiko **kegagalan majemuk** ke tingkat yang dapat ditoleransi |
| **Keselamatan & lingkungan** | Bisa melukai/menewaskan orang, atau melanggar baku mutu | Menurunkan risiko ke tingkat yang dapat ditoleransi |
| **Operasional** | Berdampak pada produksi: keluaran, mutu, layanan, biaya operasi | Biaya tugas selama satu periode **lebih kecil** daripada biaya konsekuensi + perbaikan |
| **Non-operasional** | Hanya biaya perbaikan langsung | Biaya tugas **lebih kecil** daripada biaya perbaikan |

Perhatikan asimetrinya: dua kategori pertama diuji dengan **risiko**, dua terakhir dengan
**uang**. Menyamaratakan keempatnya adalah kesalahan paling umum dalam praktik.

Fungsi tersembunyi hampir selalu melekat pada **perangkat proteksi** — alarm, katup pengaman,
sistem cadangan. Kegagalannya tidak berakibat apa pun sendirian; yang berbahaya adalah
**kegagalan majemuk**: perangkat proteksi sudah gagal diam-diam, lalu fungsi yang
diproteksinya ikut gagal.

### Bab 6 — Proactive Maintenance 1: Preventive Tasks (cetak 129 / PDF 147)

Tindakan terbagi dua: **tugas proaktif** (sebelum gagal) dan **tindakan default** (setelah,
atau saat proaktif tidak ada). Tugas proaktif dalam RCM: *scheduled restoration*,
*scheduled discard*, dan *on-condition*.

> **Kelayakan teknis** (cetak 129 / PDF 147): sebuah tugas layak secara teknis bila secara
> fisik memungkinkan tugas itu mengurangi — atau memungkinkan tindakan untuk mengurangi —
> konsekuensi moda kegagalan terkait sampai tingkat yang dapat diterima pemilik atau pengguna.

Restorasi dan pembuangan terjadwal **hanya masuk akal bila ada umur aus yang teridentifikasi**
(pola A, B, C). Untuk 89% sisanya, keduanya sia-sia. Ini konsekuensi langsung dari Bab 1.

### Bab 7 — Proactive Maintenance 2: Predictive Tasks (cetak 144 / PDF 162)

Meski sebagian besar kegagalan tidak terkait umur, sebagian besar **memberi peringatan**.

- **Kegagalan potensial** = kondisi terindentifikasi yang menandakan kegagalan fungsional
  akan atau sedang terjadi (cetak 144 / PDF 162).
- **Kurva P-F**: titik P = kegagalan mulai terdeteksi; titik F = kegagalan fungsional.
  **Interval P-F** = jarak waktu keduanya.
- **Interval pemeriksaan harus lebih pendek dari interval P-F.** Aturan praktis buku:
  **ambil setengah interval P-F** (cetak 146 / PDF 164). Bila interval P-F tidak konsisten,
  ambil jauh di bawah yang terpendek (cetak 149 / PDF 167).
- **Nett P-F interval** = interval P-F − interval pemeriksaan; yaitu sisa waktu minimum yang
  benar-benar tersedia untuk bertindak. Inilah yang menentukan kelayakan, bukan interval P-F
  mentah. Contoh buku (cetak 147 / PDF 165): interval P-F 9 bulan — diperiksa bulanan, nett
  8 bulan; diperiksa 6-bulanan, nett hanya 3 bulan.
- Uji kelayakan teknis: **nett P-F interval > waktu yang dibutuhkan untuk bertindak**
  (cetak 148 / PDF 166). Memeriksa lebih sering tidak mencegah kegagalan — ia memperpanjang
  waktu bertindak.

> Tugas on-condition layak secara teknis bila: kondisi kegagalan potensial dapat didefinisikan
> dengan jelas; interval P-F cukup konsisten; praktis memantau pada interval lebih pendek dari
> interval P-F; dan nett P-F interval cukup panjang untuk bertindak (cetak 149 / PDF 167).

Satu moda kegagalan bisa punya beberapa teknik deteksi dengan interval P-F berbeda —
contoh bantalan (cetak 154 / PDF 172): analisis getaran 1–9 bulan, analisis oli 1–6 bulan,
suara 1–4 minggu, panas dengan sentuhan 1–5 hari. Teknik yang lebih dini memberi waktu
bertindak lebih panjang, tapi biasanya lebih mahal.

### Bab 8 — Default Actions 1: Failure-finding (cetak 170 / PDF 188)

Tindakan default ditentukan oleh konsekuensi (cetak 170 / PDF 188):

- fungsi tersembunyi, tanpa tugas proaktif yang memadai → **failure-finding**; bila itu pun
  tidak ada dan kegagalan majemuk berdampak keselamatan/lingkungan → **redesain wajib**
- keselamatan/lingkungan, tanpa tugas proaktif → **redesain atau ubah proses (wajib)**
- operasional / non-operasional → awalnya **tanpa pemeliharaan terjadwal**; bila biaya tetap
  tak tertahankan → redesain

**Failure-finding** = memeriksa fungsi tersembunyi secara berkala untuk memastikan ia masih
bekerja. Bukan mencegah kegagalan perangkat proteksi, melainkan menurunkan peluang
kegagalan majemuk.

**Rumus interval (FFI):**

```
FFI = 2 × ketaktersediaan × MTBF perangkat proteksi          (cetak 177 / PDF 195)
```

Contoh dari buku: lampu rem MTBF 4 tahun, ketersediaan diinginkan 99% (ketaktersediaan 1%)
→ FFI = 2 × 1% × 48 bulan = **1 bulan**.

Bentuk lengkapnya, langsung dari sasaran kegagalan majemuk:

```
FFI = (2 × M_perangkat × M_terproteksi) / M_kegagalan_majemuk    (cetak 180 / PDF 198)
```

Contoh dari buku: sasaran MTBF kegagalan majemuk 1000 tahun, MTBF pompa cadangan 8 tahun,
MTBF fungsi terproteksi 10 tahun → FFI = 2 × 8 × 10 / 1000 = 0,16 tahun ≈ **2 bulan**.

Catatan penting: bila perangkat proteksi harus dilumpuhkan untuk diperiksa, proteksi
pengganti harus disediakan atau fungsi terproteksi dimatikan selama pemeriksaan.

### Bab 9 — Other Default Actions (cetak 187 / PDF 205)

**No scheduled maintenance** sah hanya dalam dua keadaan: fungsi tersembunyi yang kegagalan
majemuknya tidak berdampak keselamatan/lingkungan dan tak ada tugas yang cocok; atau
kegagalan berkonsekuensi operasional/non-operasional yang tidak ada tugas hemat biayanya.
Ini keputusan sadar, bukan kelalaian.

**Redesain** wajib untuk konsekuensi keselamatan/lingkungan yang tak tertangani, dan opsional
(berdasar biaya) untuk selainnya. Bab ini juga membahas **walk-around check** yang berada di
luar kerangka keputusan formal.

### Bab 10 — The RCM Decision Diagram (cetak 198 / PDF 216)

Menyatukan Bab 5–9 jadi satu alur keputusan yang diterapkan **pada tiap moda kegagalan**.
Urutan pertanyaannya:

1. **Apakah hilangnya fungsi akibat moda kegagalan ini menjadi nyata bagi operator dalam
   keadaan normal?** → memisahkan tersembunyi dari nyata
2. Apakah berdampak keselamatan atau lingkungan? → apakah operasional?
3. Apakah tugas **on-condition** layak secara teknis dan sepadan dikerjakan?
4. Apakah **scheduled restoration** layak dan sepadan?
5. Apakah **scheduled discard** layak dan sepadan?
6. Bila semua tidak — jatuh ke tindakan default sesuai konsekuensi

Keluarannya **Decision Worksheet**: tugas rutin apa, seberapa sering, oleh siapa; kegagalan
mana yang cukup serius untuk menuntut redesain; dan kasus mana yang sengaja dibiarkan gagal.

### Bab 11 — Implementing RCM Recommendations (cetak 212 / PDF 230)

Analisis tanpa implementasi tidak menghasilkan apa-apa. Langkah kuncinya: seluruh rekomendasi
disetujui formal oleh manajer yang bertanggung jawab; tugas rutin diuraikan jelas; perubahan
sekali-jalan diidentifikasi dan dilaksanakan; tugas dirangkai ke dalam **work package**; dan
dimasukkan ke sistem perencanaan agar dikerjakan orang yang tepat pada waktu yang tepat.

**RCM audit** (11.2) adalah gerbang mutu: memeriksa bahwa analisis benar sebelum jadi perintah
kerja. Bagian 11.6 membahas keterkaitan dengan sistem perencanaan/CMMS, 11.7 pelaporan cacat.

### Bab 12 — Actuarial Analysis and Failure Data (cetak 235 / PDF 253)

Pembahasan mendalam enam pola kegagalan, konsep umur, MTBF, dan probabilitas bersyarat.
Kesimpulan pentingnya: **catatan riwayat teknis di kebanyakan industri jarang cukup lengkap**
untuk dijadikan dasar tunggal keputusan pemeliharaan. Data berguna, tetapi tidak menggantikan
penalaran RCM. Ini alasan Bab 13 mengandalkan pengetahuan orang, bukan basis data.

### Bab 13 — Applying the RCM Process (cetak 261 / PDF 279)

Siapa yang tahu jawabannya? Bukan satu orang. RCM dijalankan oleh **review group** kecil
berisi operator, perawat, penyelia, dan spesialis, dipandu **fasilitator** terlatih.
Fasilitator memastikan proses ditegakkan, bukan memasok jawaban teknis.

Isi lain: strategi implementasi (13.4), menjaga RCM tetap hidup setelah analisis awal (13.5),
**cara RCM tidak boleh diterapkan** (13.6 — analisis oleh satu ahli tanpa keterlibatan
operator, atau memakai perangkat lunak sebagai pengganti penalaran), dan pembangunan
kompetensi (13.7).

### Bab 14 — What RCM Achieves (cetak 292 / PDF 310)

Membedakan **maintenance effectiveness** (seberapa baik pemeliharaan menjaga aset melakukan
yang dikehendaki pengguna — ukuran bagi pelanggan) dari **maintenance efficiency** (seberapa
baik sumber daya pemeliharaan dipakai — ukuran bagi manajer pemeliharaan). Tiga keluaran
nyata RCM: jadwal pemeliharaan, prosedur operasi yang direvisi, dan daftar perubahan
sekali-jalan. Buku menyatakan sebagian besar penerapan membayar dirinya sendiri dalam
hitungan bulan.

### Bab 15 — A Brief History of RCM (cetak 318 / PDF 336)

1974, Departemen Pertahanan AS menugasi United Airlines menyusun laporan tentang cara
industri penerbangan sipil membuat program pemeliharaan. Laporan **Nowlan & Heap** itulah
yang berjudul *Reliability-centered Maintenance*. Bab ini juga membahas evolusi ke RCM2 dan
posisi versi-versi RCM lain terhadap **standar SAE**.

### Apendiks

| Apendiks | Isi | Halaman |
|---|---|---|
| 1 | Hierarki aset, plant register, functional block diagram — penentuan tingkat analisis | cetak 327 / PDF 345 |
| 2 | Kesalahan manusia: faktor antropometrik, sensorik, fisiologis, psikologis, dan penanganannya dalam RCM | cetak 335 / PDF 353 |
| 3 | Kontinum risiko: menggabungkan risiko keselamatan dan ekonomi dalam satu skala toleransi | cetak 343 / PDF 361 |
| 4 | Teknik condition monitoring — katalog teknik deteksi kegagalan potensial beserta interval P-F | cetak 348 / PDF 366 |

Apendiks 4 adalah yang paling tebal (64 halaman) dan paling sering dipakai di lapangan.

---

## 3. Angka dan rumus yang perlu diingat

| Hal | Nilai / rumus | Sumber |
|---|---|---|
| Moda kegagalan tak terkait umur | 89% (pola D+E+F) | cetak 13 / PDF 31 |
| Pola paling umum | F — kematian dini lalu datar, 68% | cetak 13 / PDF 31 |
| Interval tugas on-condition | Setengah interval P-F (aturan praktis) | cetak 146 / PDF 164 |
| Nett P-F interval | `interval P-F − interval pemeriksaan` | cetak 146 / PDF 164 |
| Kelayakan on-condition | Nett P-F > waktu yang dibutuhkan bertindak | cetak 148 / PDF 166 |
| Interval failure-finding (sederhana) | `FFI = 2 × ketaktersediaan × MTBF` | cetak 177 / PDF 195 |
| Interval failure-finding (lengkap) | `FFI = 2 × M_perangkat × M_terproteksi / M_majemuk` | cetak 180 / PDF 198 |
| Koreksi bila pengujian sendiri merusak | Faktor `(1 − p)`; abaikan bila p < 0,05 | cetak 181 / PDF 199 |

---

## 4. Kesalahan penerapan yang disorot buku

- Menerapkan RCM tanpa menetapkan **konteks operasi** — hasilnya program generik yang salah sasaran.
- Menulis fungsi tanpa **standar unjuk kerja terukur** — kegagalan fungsional jadi tak bisa didefinisikan.
- Menyamakan uji "sepadan dikerjakan" untuk semua konsekuensi — risiko dan biaya tidak boleh dicampur.
- Menjadwalkan overhaul atau penggantian berkala pada moda kegagalan yang **tidak terkait umur**.
- Menganggap failure-finding sebagai pencegahan — ia hanya menurunkan peluang kegagalan majemuk.
- Analisis dikerjakan satu ahli atau konsultan tanpa operator dan perawat (13.6).
- Memakai perangkat lunak sebagai pengganti penalaran review group (13.6).
- Berhenti di lembar kerja tanpa audit dan implementasi formal (Bab 11).

---

## 5. Pemakaian di GSP

| Keperluan | Bagian yang dipakai |
|---|---|
| Metodologi usulan layanan keandalan | Bab 1 (definisi, 7 pertanyaan), Bab 10 (kerangka keputusan) |
| Penyusunan FMEA aset pelanggan | Bab 4 + Information Worksheet |
| Pembelaan jadwal pemeliharaan dalam kajian teknis | Bab 5 (konsekuensi), Bab 6–7 (kelayakan teknis) |
| Penentuan interval pemeriksaan | Bab 7 (P-F) dan Bab 8 (FFI) — keduanya berumus, bisa dipertanggungjawabkan |
| Argumen menolak overhaul berkala warisan | Bab 1 (enam pola) + Bab 12 |
| Tata kelola dan KPI kontrak pemeliharaan | Bab 11 (implementasi, audit), Bab 14 (efektivitas vs efisiensi) |
| Perangkat proteksi (fire alarm, UPS bypass, genset cadangan) | Bab 5 (fungsi tersembunyi) + Bab 8 (FFI) |

Untuk menjalankan analisisnya, gunakan skill `rcm-analysis` yang mengacu ke resume ini.
