---
id: pohon-chart-datman-1004
type: catatan
title: POHON PEMILIHAN CHART NAVIGABEL (CH-nn)
status: active
sumber: "docs/2026-10-04-datum-manual/library/pohon-pemilihan-chart.md (hulu: research/02-tipologi-chart-diagram.md, research/03-sintesis-dan-keputusan.md, corpus/lajur1-datum-dokumen.md, identification/02_structured.md)"
halaman: 32 chart CH-01..CH-32 pada daun bersyarat; apparatus AP-1..AP-10; self-check work/f6p12_check.py
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, chart, pohon-pemilihan, tipologi, navigabel, anti-kasus]
links: [docs/2026-10-04-datum-manual/library/pohon-pemilihan-chart.md]
penulis: gsp-document-writer
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_08c4025e
pin_sha16_artefak: a81bba8aabd5e9ff
catatan_keputusan: "dipromosikan: DATMANUAL-1004 P23: checker hulu diulang segar PASS; P22 verifier independen SALAH-TARGET=0 33/33; non-sensitif non-dosir"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/pohon-chart-datman-1004.md
---

# POHON PEMILIHAN CHART NAVIGABEL (CH-nn)

- Misi: DATMANUAL-1004 | Kartu: t_74657abf | Pekerja: gsp-document-writer
- Langkah 12 blueprint (fase konstruksi-pustaka). Konsumsi hiliran: langkah 14
  (library/INDEKS.md), langkah 17 (Bagian II manual), verifier F4/F6.
- Tanggal: 2026-10-05. Cacah dalam berkas ini dicetak alat
  `work/f6p12_check.py` pada giliran ini (jejak di `work/f6p12_check_out.txt`),
  bukan ingatan.
- Sumber (readonly, tidak diubah lajur ini):
  - R-1 = `research/02-tipologi-chart-diagram.md` - katalog CH-01..CH-32 dan
    DIA-01..DIA-20, aturan baca lintas tipologi AB-01..AB-10.
  - R-2 = `research/03-sintesis-dan-keputusan.md` - pohon tiga-cabang (A chart,
    B diagram, C simbol), apparatus wajib AP-1..AP-10, gerbang SPK-002.
  - R-3 = `corpus/lajur1-datum-dokumen.md` - register DAT-nn: DAT-70 (caption),
    DAT-73..DAT-80 (chart/figur), DAT-127 (9 keluarga diagram).
  - R-4 = `identification/02_structured.md` - KONTRAK-DESAIN KD-09 (lebar figur
    128/166 saja), KD-13, KD-15, KD-16, KD-24; keputusan D-TA-11 (skema ID).
- Skema sitasi pustaka (D-TA-02): `DATMAN/LIB/pohon-pemilihan-chart#<ID>` dengan
  ID = A.n (daun), CH-nn (chart), AP-n (apparatus).

## 1. Cara memakai pohon ini

Pohon ini menjawab satu pertanyaan pembaca: "chart apa yang benar untuk data dan
pesan saya, dan apparatus apa yang wajib menyertainya?" Pemakaian bertahap:

(1) Jalui Gerbang-Akar (bagian 2). Bila pertanyaan pembaca bukan tentang NILAI,
    berhenti di sini dan pindah ke cabang yang benar; pohon ini hanya mengurus
    chart.
(2) Turuni daun pertanyaan A.1..A.7 (bagian 4). Setiap daun punya syarat masuk
    terukur (angka batas atau uji ya/tidak); daun pertama yang terpenuhi menang,
    dan daun berikutnya yang juga terpenuhi dicatat sebagai kandidat kedua bila
    pembaca ragu.
(3) Di dalam daun, pilih chart memakai pembanding antar-sejenis (kolom "kapan
    dipilih"), lalu WAJIB baca kolom ANTI-kasus chart terpilih. Nol chart boleh
    dipakai tanpa anti-kasus terbaca (AP-10, R-2 bagian 3).
(4) Pasang apparatus wajib (bagian 6) sebelum gambar dianggap selesai; apparatus
    inti berlaku untuk SEMUA chart tanpa kecuali.
(5) Bila tidak ada daun yang cocok, pakai jalur fallback (bagian 7). Dilarang
    mengarang chart di luar tipologi terdaftar tanpa mencatat GAP.

Navigasi cepat: daftar isi daun ada di bagian 3; indeks chart per daun ada di
tabel rekonsiliasi bagian 5.

## 2. Gerbang-Akar (Lapis-0): jenis pertanyaan dulu, baru chart

| Jenis pertanyaan pembaca | Uji terukur | Rute |
|---|---|---|
| NILAI: berapa, seberapa besar, bagaimana berubah, bagaimana sebarannya, apa hubungannya | Jawaban akhir berupa angka yang dibandingkan | Masuk pohon ini (cabang A, daun A.1..A.7) |
| STRUKTUR/ALUR/JADWAL/KONEKSI: apa komponennya, siapa mengerjakan apa, kapan, bagaimana terhubung | Jawaban akhir berupa relasi antar objek, bukan angka | Cabangnya `library/registri-pola-diagram.md` (DIA-nn, dibangun langkah 13; sementara lihat R-2 bagian 2 cabang B) |
| MAKNA GLIF/TANDA pada gambar yang sudah ada | Jawaban akhir berupa definisi simbol | Cabangnya `library/katalog-simbol.md` (SIM-nn, dibangun langkah 11; sementara lihat R-2 bagian 2 cabang C) |

Satu figur boleh menyentuh lebih dari satu cabang (mis. bagan topologi dengan
panel utilisasi = cabang B + daun A.3); setiap cabang yang tersentuh menarik
apparatus-nya sendiri. Aturan komposisi R-2 tetap berlaku: diagram yang memakai
glif wajib menarik apparatus simbol dari kelas terkait, dan chart yang memuat
batas statistik menarik K-15 (ISO 7870-2:2023). Praktik lapangan justru sering
mencampurnya dalam satu gambar, sehingga aturan pemisahan apparatus inilah yang
menjaga figur hibrida tetap dapat diaudit per lapisan.

## 3. Registri daun (indeks navigasi)

| Daun | Pertanyaan inti | Chart ter-rute | Jalur build datumchart (R-1 bagian 5) |
|---|---|---|---|
| A.1 Peringkat kategori | mana terbesar/terkecil/teratas? | CH-01, CH-09, CH-17, CH-30 | bar (TERISI; Pareto butuh komponen kurva kumulatif) |
| A.2 Deret waktu | bagaimana berubah terhadap waktu? | CH-02, CH-04, CH-05, CH-19, CH-20, CH-22 | column (TERISI) + keluarga SERIES (diadopsi, bagian 5) |
| A.3 Nilai vs batas / stabilitas proses | apakah memenuhi target? apakah proses stabil? | CH-03, CH-06, CH-07, CH-08 | threshold (TERISI; control chart butuh apparatus sigma) |
| A.4 Distribusi satu variabel | bagaimana sebarannya? | CH-10, CH-11, CH-12, CH-15, CH-23, CH-31 | keluarga DISTRIBUSI (diadopsi, bagian 5) |
| A.5 Relasi antar variabel / diagnostik model | apa hubungannya? mana faktor berpengaruh? | CH-13, CH-14, CH-21, CH-24, CH-25, CH-26, CH-32 | keluarga RELASI (diadopsi, bagian 5) |
| A.6 Diagnostik ketergantungan serial | ada pola berulang/autokorelasi pada deret? | CH-27, CH-28, CH-29 | keluarga RELASI subgroup serial (diadopsi, bagian 5) |
| A.7 Sebagian-ke-seluruh / jembatan nilai | berapa kontribusi tiap bagian? dari mana ke mana nilai berubah? | CH-16, CH-18, CH-22 varian tumpuk | column + opsi offset bar (waterfall); treemap jalur baru |

Cacah rute pada tujuh daun menghasilkan 32 chart unik, sama persis dengan
populasi katalog R-1. Tidak ada tipologi yatim maupun chart dwi-keluarga;
kedua vonis itu dicetak alat CHECK 1 dan CHECK 2 pada bagian 10, bukan
dinyatakan lisan. Verifier cukup menjalankan ulang satu perintah untuk
membuktikannya pada berkas final.

## 4. Daun pertanyaan (cabang A)

Format tiap daun konsisten: syarat masuk terukur lebih dulu, lalu tabel chart
dengan kolom pembanding dan kolom ANTI-kasus, ditutup apparatus khusus daun.
Contoh buruk-vs-baik disajikan deskriptif karena sketsa ASCII maupun mermaid
hanyalah alat pikir penulis dan dilarang menjadi keluaran jadi (AP-9). Urutan
ini sengaja: pembaca yang berhenti di syarat masuk tidak akan pernah memakai
chart tanpa lebih dulu membaca anti-kasusnya.

### 4.1 Daun A.1 - Peringkat kategori

Syarat masuk (semua harus terpenuhi): kategori bersifat nominal tanpa urutan
alami, cacah kategori tidak lebih dari lima belas, dan tujuan baca pembaca
adalah urutan atau perbandingan besar-kecil antar kategori. Kategori yang
berurutan waktu bukan milik daun ini dan pindah ke A.2. Kategori dengan cacah
lebih dari lima belas wajib dirangkum lebih dulu, misalnya menggabungkan ekor
menjadi "lainnya" dengan catatan eksplisit, atau disajikan sebagai tabel.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-01 | Bar horisontal | Default peringkat; label kategori panjang muat di kiri | >15 kategori (label bertumpuk); kategori waktu (pakai CH-02); sebagian-ke-seluruh banyak irisan (jangan pie; pakai CH-21 matriks atau tabel) |
| CH-09 | Pareto | Kategori cacah dan pesan = few-vital (persentase kumulatif) | Kategori sedikit (kurva tak informatif); basis cacah berbeda antar kategori; tanpa definisi cacah di caption |
| CH-17 | Radar/spider | Profil multivariat vs acuan, metrik <= 6, audiens sudah sepakat soal sumbu | KUAT: urutan sumbu mengubah luas poligon secara arbitrer; jangan bandingkan luas; dokumen teknik resmi umumnya melarangnya sebagai alat keputusan (R-1 CH-17) |
| CH-30 | Star plot | Banyak baris profil perangkat, observasi kecil (<= 10 bintang) | Komunikasi ke pembaca awam; > 10 bintang |

Apparatus khusus: AB-03 sort menurun wajib untuk kategori tak-berurutan;
label nilai mono di ujung batang (AB-04, DAT-74); AB-01 nol bersama.

Contoh buruk-vs-baik. BURUK: daftar 12 risiko keselamatan ditampilkan urut
penemuan lapangan, pembaca harus memindai batang satu-satu untuk mencari yang
terbesar. BAIK: batang diurut menurun dari probabilitas-tertimbang terbesar,
label nilai tercetak di ujung tiap batang, satu warna aksen hanya pada tiga
risiko teratas yang menjadi dasar rekomendasi; urutan berubah menjadi pesan.

### 4.2 Daun A.2 - Deret waktu

Syarat masuk: tersedia sekurang-kurangnya dua titik waktu dan pertanyaan
pembaca adalah perubahan nilai terhadap waktu. Pembeda bentuknya diskret atau
kontinu: periode bulanan dan triwulanan bersifat diskret, sedangkan sinyal,
beban, dan degradasi bersifat kontinu. Jumlah titik juga menentukan, sebab
deret sangat jarang dengan jarak tidak tetap lebih jujur dibaca sebagai run
chart daripada garis tersambung.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-02 | Column deret waktu | Periode diskret (bulanan, triwulanan) | Banyak titik kontinu (pakai CH-04); sumbu Y terpotong tanpa tanda putus; pembacaan selisih antar periode (pertimbangkan CH-20) |
| CH-04 | Line chart | Besaran kontinu (kurva beban, degradasi, latency) | Kategori nominal di sumbu X (itu bar); > ~4 seri tanpa pembeda kuat; interpolasi antar titik yang tidak kontinu di dunia nyata |
| CH-05 | Run chart | Urutan observasi tanpa asumsi jarak waktu; progres sebelum batas kontrol ditetapkan | Dipakai menyimpulkan "proses terkontrol" (butuh CH-06); sumbu waktu implisit tanpa keterangan |
| CH-19 | Sparkline | Tren sebaris dalam tabel/narasi; bukan untuk membaca nilai absolut | Membaca nilai absolut (tanpa sumbu); satu sparkline membawa 3 seri; tanpa nilai akhir berlabel (gaya Tufte, DAT-79) |
| CH-20 | Slope chart | Tepat dua waktu; pesan = perubahan relatif | > 2 waktu (jadi spageti); > 10 kategori saling silang |
| CH-22 | Area chart | Kumulatif/tumpuk antar seri sepanjang waktu | Seri tengah/atas dibaca tingginya padahal hanya seri dasar akurat; transparansi bertumpuk; alternatif: small multiples line per seri |

Apparatus khusus: AB-05 waktu selalu di sumbu-x; AB-01; gridline hanya bila
nilai harus dibandingkan (DAT-74); sparkline ikut DAT-79 (lebar 14 letterspace,
satu tinta, nilai akhir dicetak di kanan, band normal didefinisikan dan
diungkapkan di caption).

Contoh buruk-vs-baik. BURUK: column konsumsi energi bulanan dengan sumbu Y
mulai 85% dari rata-rata; selisih dua bulan terlihat dua kali lipat padahal
hanya 6%. BAIK: sumbu mulai nol sehingga proporsi jujur, atau bila resolusi
selisih memang dibutuhkan, ganti ke slope chart dua waktu dengan label angka
delta di tiap segmen; pemotongan sumbu tidak pernah disembunyikan.

### 4.3 Daun A.3 - Nilai vs batas dan stabilitas proses

Syarat masuk: ada batas atau target numerik yang sah sumbernya (SLA kontrak,
KAK, ambang desain), atau pertanyaan stabilitas proses dengan sekurang-kurangnya
dua puluh titik data untuk menghitung batas kontrol. Batas spesifikasi tidak
boleh dipinjam sebagai batas kontrol karena keduanya konsep berbeda, penegasan
yang datang langsung dari NIST (R-1 CH-06). Daun inilah tempat DAT-77 bekerja
penuh: gambar melakukan perbandingan, bukan pembaca.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-03 | Bullet graph | Satu metrik vs batas/target + zona kualitas; pengganti gauge | > 5-6 metrik sejenis per panel; tanpa label batas numerik; zona kualitas tanpa dasar dokumen |
| CH-06 | Control chart Shewhart | Stabilitas proses, >= 20 titik, sebab umum vs khusus | < 20 titik tapi batas dihitung seolah stabil; batas spesifikasi dipakai sebagai batas kontrol |
| CH-07 | EWMA | Deteksi geseran kecil bertahap antar siklus (drift kalibrasi/daya) | Substitusi saat jumlah titik kecil; interpretasi visual tanpa menyebut konstanta bobot lambda |
| CH-08 | CUSUM | Pergeseran mean kecil yang akumulatif (keausan, penyimpangan panjang) | Laporan eksekutif (bobot keputusan tinggi, sulit dibaca awam); tanpa keputusan referensi h bila dipakai sebagai vonis |

Apparatus khusus: AB-09 nyatakan aturan sinyal (mis. 3-sigma) dan ukuran
sampel; apparatus simbol K-15 (payung ISO 7870-2:2023, R-2 daun A.3); DAT-77
untuk kasus threshold sederhana: garis batas berlabel + bar pelanggar memakai
tinta alert, sehingga gambar melakukan perbandingan, bukan pembaca.

Contoh buruk-vs-baik. BURUK: gauge speedometer hijau-kuning-merah untuk KPI
uptime, tanpa angka target, zona warna tanpa rujukan dokumen. BAIK: bullet
graph satu baris dengan garis target berlabel "99,5% (SLA kontrak nomor ...)",
zona kualitas bersumber dari dokumen KAK, satu aksen alert hanya saat nilai
aktual melanggar; gauge hilang karena tidak menambah informasi.

### 4.4 Daun A.4 - Distribusi satu variabel

Syarat masuk: pertanyaan pembaca adalah bentuk sebaran (simetri, ekor,
multimoda, persentil), bukan urutan waktu atau peringkat. Uji kecukupan n
menentukan bentuk yang boleh dipakai: dengan n di bawah tiga puluh per grup,
bacaan bentuk dari histogram dilarang dan data mentah lebih jujur lewat
CH-23 atau pernyataan keterbatasan. Batas tiga puluh itu konvensi konservatif
R-1 CH-10, bukan hukum alam; yang dilarang adalah membaca ekor distribusi dari
sampel yang terlalu kecil untuk punya ekor.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-10 | Histogram | n >= 30, bentuk umum satu grup | n kecil dibaca bentuknya; bin dipilih membentuk cerita; data diskret sedikit nilai (pakai CH-01) |
| CH-11 | Box plot | Bandingkan sebaran antar grup (site/perangkat), n besar per grup | n sangat kecil per grup; whisker 1,5-IQR vs min-max dicampur antar grup; pembaca awam disuruh menyimpulkan bentuk |
| CH-12 | Violin plot | Bentuk multimoda penting antar grup, n cukup | n kecil (densitas menipiskan noise jadi bentuk palsu); pembaca campuran yang tidak mengenalnya |
| CH-15 | Probability/Q-Q (termasuk Weibull) | Uji cocok-distribusi; analisis umur/keandalan (MTBF, weibullity) | n sangat kecil dianggap cukup memutuskan; sumbu log tanpa penanda eksplisit |
| CH-23 | Stem-and-leaf | Lampiran data mentah n <= 100 yang harus tetap terbaca | n besar; desimal banyak tanpa aturan pembulatan |
| CH-31 | Plot kumulatif (CDF) | Persentil/kuantil (p95/p99 SLA latency, butiran agregat) | Dibaca sebagai histogram: padatan lokal = kemiringan kurva, bukan tinggi |

Apparatus khusus: AB-09 konvensi whisker/CI wajib dinyatakan; n per grup di
caption; AB-07 satuan ISO 80000-1 di label sumbu; lebar bin dan aturan
pemilihan bin diumumkan di caption (CH-10); distribusi acuan + metode plotting
position di caption (CH-15); bandwidth estimator disebut (CH-12).

Contoh buruk-vs-baik. BURUK: histogram latency 12 sampel dengan 8 bin dibaca
"bimodal, ada dua penyebab". BAIK: 12 nilai mentah disajikan stem-and-leaf di
lampiran dengan caption berisi n, unit, dan aturan pembulatan; klaim bentuk
ditahan sampai n memadai, dan teks hanya melaporkan rentang serta median.

### 4.5 Daun A.5 - Relasi antar variabel dan diagnostik model

Syarat masuk: dua variabel kontinu atau lebih tersedia berpasangan. Eksplorasi
matriks hanya sah bila faktor mencapai tiga atau lebih dan tujuannya
prapemilihan, bukan kesimpulan final. Perlu ditegaskan bahwa kesimpulan
kausalitas tidak pernah berasal dari pola scatter saja (anti-kasus CH-13), apa
pun sejelas apa pun garis yang tampak.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-13 | Scatter (+ regresi) | Sepasang besaran kontinu; arah, kekuatan, pencilan | Mengklaim kausalitas dari pola; overplotting padat (pakai hexbin/proyeksi); regresi linear dipaksakan tanpa uji sisaan |
| CH-14 | SPLOM | Eksplorasi <= 6 variabel semua pasangan | > 6 variabel (kisi tak terbaca cetak); dipakai sebagai kesimpulan final |
| CH-21 | Heatmap/matriks warna | Nilai pada kisi kategori x kategori (matriks risiko dampak x kemungkinan, skor kesesuaian) | Membaca angka presisi tanpa label sel; colormap pelangi untuk data berurutan |
| CH-24 | Youden plot | Banding hasil antar laboratorium uji (dua bahan) | Studi single-lab; akreditasi formal tanpa prosedur ISO 5725 |
| CH-25 | Block plot | Efek utama robust outlier dengan blok batch | Interaksi kompleks (pakai CH-26) |
| CH-26 | Interaction plot | Dua faktor; garis tidak sejajar = interaksi | > 2 faktor tanpa small multiples; CATATAN provenans: jangan mengutip URL pri3361.htm sebagai interaction plot (salah-sasaran, R-1 CH-26 dan register 5.3 R-2) |
| CH-32 | DOE mean plot | Merangkum main effects eksperimen parameter | Efek interaksi diabaikan padahal ada (cek CH-26 dulu) |

Apparatus khusus: koefisien + interval kepercayaan ditulis di caption, bukan
hanya garis di plot (CH-13); AB-08 warna = skala, bukan dekorasi (palet
sekuensial untuk rasio, diverging untuk ada-tengah-nol, legenda warna
berangka); ukuran cetak SPLOM minimal separuh halaman.

Contoh buruk-vs-baik. BURUK: matriks risiko diwarnai pelangi rainbow tanpa
angka sel, dua sel merah-terang berbeda 1 poin skor terlihat identik bagi
pembaca. BAIK: palet sekuensial satu arah, legenda warna berangka (tick 1, 3,
5, 7), dan angka skor dicetak pada sel yang dibacakan dalam rapat keputusan;
warna mempersempit pencarian, angka menutup keputusan.

### 4.6 Daun A.6 - Diagnostik ketergantungan serial

Syarat masuk berupa prasyarat mutlak: data deret waktu dengan basis sampling
tetap, dan interval sampling dinyatakan sejak judul bersama tanggal berlaku.
Tanpa dua kondisi itu ketiga chart diagnostik di bawah kehilangan makna,
karena band signifikansi dan puncak spektrum sama-sama fungsi dari laju sampel.
Daun ini hampir selalu merupakan daun antara: hasilnya mengantar pembaca ke
A.2 untuk pemodelan, bukan berdiri sebagai kesimpulan akhir.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-27 | Lag plot | Prauji autokorelasi/osilasi: nilai vs nilai bergeser k | Menyimpulkan periode tunggal tanpa konfirmasi ACF (CH-28) |
| CH-28 | ACF | Kuantifikasi lag signifikan vs band white noise | Lag melebihi n/4 dibaca; interpretasi kausal |
| CH-29 | Spectrum plot | Daya vs frekuensi (FFT); diagnosis getaran/noise listrik | Resolusi frekuensi melebihi laju sampel; sumbu log tanpa penanda |

Apparatus khusus: interval sampling dinyatakan di judul (bersama tanggal
berlaku, AP-1); band batas pada ACF diberi keterangan tingkat signifikansi.

Contoh buruk-vs-baik. BURUK: ACF konsumsi alarm dibaca sampai lag 200 padahal
n = 80; ekor korelasi "penting" sebenarnya artefak jumlah sampel. BAIK: sumbu
lag dibatasi n/4 dengan caption menyatakan n, interval sampling 5 menit, dan
band 95%; kesimpulan periode hanya dari puncak yang lolos band dan terkonfirmasi
CH-27.

### 4.7 Daun A.7 - Sebagian-ke-seluruh dan jembatan nilai

Syarat masuk: total harus tertutup aritmetika, artinya jumlah seluruh bagian
sama dengan total, atau nilai awal ditambah rantai delta sama dengan nilai
akhir. Bila aritmetika tidak tertutup, perbaiki datanya lebih dulu, bukan
gambarnya; chart tidak pernah berwenang menutup selisih pembukuan. Daun ini
paling sering dipakai di dokumen biaya GSP (jembatan RAB dan rekonsiliasi
kapasitas), sehingga kepatuhan AP-1 pada subtotal bukan hiasan melainkan
syarat audit.

| CH | Nama | Kapan dipilih (pembanding) | ANTI-kasus (wajib dibaca) |
|---|---|---|---|
| CH-16 | Waterfall | Rantai perubahan berurutan (taksiran awal, hasil negosiasi, nilai kontrak), <= 8 langkah | > 8 langkah; langkah tidak aditif (irisan ganda); dipakai untuk peringkat (itu CH-01) |
| CH-18 | Treemap | Hierarki luas >= 3 tingkat (biaya per paket kerja dalam WBS) | Hierarki dangkal 2 tingkat sedikit daun (bar bergrup lebih baik); perbandingan presisi antar daun kecil |
| CH-22 varian tumpuk | Area tumpuk | Bauran bagian yang berevolusi terhadap waktu (juga ter-rute di A.2) | Seri tengah/atas dibaca tingginya; preferensi small multiples bila bagian penting |

Apparatus khusus: total masuk-keluar berlabel angka; waterfall menandai
subtotal dan hanya selisih yang melayang (AB-01 untuk total); warna beda untuk
total vs delta; treemap label langsung + warna kedalaman, bukan warna nilai
ganda.

Contoh buruk-vs-baik. BURUK: waterfall biaya 14 langkah tanpa subtotal,
pembaca kehilangan jejak aritmetika di tengah rantai. BAIK: rantai dipangkas
jadi 7 langkah dengan tiga subtotal berlabel angka, bar total dibedakan tinting
dari bar delta, dan rekonsiliasi pemangkasan 14 menjadi 7 langkah dicatat di blok derivasi
sehingga angka tetap tertelusur (KD-18).

## 5. Registri keluarga chart dan jalur build (keputusan adopsi kartu 12)

Baseline internal DAT-76 menutup tiga keluarga build: bar (peringkat), column
(deret waktu), threshold (nilai vs batas). Riset R-1 bagian 5 mengusulkan tiga
keluarga baru karena kekosongan mesin, dan R-2 bagian 6 menyerahkan putusan
adopsi ke hiliran. Putusan controller D-11 (contract.md, 05-10) meratifikasi
usulan tersebut: KETIGA keluarga DIADOPSI sebagai perluasan CH/DIA manual,
dan pohon ini menjadi rumah rutenya. Status jalur build per keluarga tetap
terpisah dari status adopsi normatif, seperti tabel berikut.

| Keluarga | Status | Anggota CH | Jalur build datumchart |
|---|---|---|---|
| bar (peringkat) | Baseline DAT-76, TERISI | CH-01, CH-09 | Ada; Pareto butuh komponen tambahan garis kumulatif |
| column (deret waktu) | Baseline DAT-76, TERISI | CH-02, CH-22 | Ada |
| threshold (nilai vs batas) | Baseline DAT-76, TERISI | CH-03, CH-06, CH-07, CH-08 | Ada; control chart butuh apparatus sigma (batas dihitung, bukan digambar bebas) |
| SERIES (deret kontinu/sebaris) | USULAN R-1, DIADOPSI PUTUSAN D-11 | CH-04, CH-05, CH-19, CH-20 | Jalur baru; spesifikasi JSON per KD-24 dengan apparatus penuh |
| DISTRIBUSI | USULAN R-1, DIADOPSI PUTUSAN D-11 | CH-10, CH-11, CH-12, CH-15, CH-23, CH-31 | Jalur baru; pertanyaan engine-vs-luar-scope masuk Register Riset Terbuka (D-10) |
| RELASI (dua variabel + diagnostik) | USULAN R-1, DIADOPSI PUTUSAN D-11 | CH-13, CH-14, CH-21, CH-24, CH-25, CH-26, CH-32 + subgroup serial CH-27, CH-28, CH-29 | Jalur baru; termasuk plot diagnostik NIST |
| Sebagian-ke-seluruh (varian build) | Varian keluarga column | CH-16 (offset bar), CH-18 | Waterfall perlu opsi offset bar; treemap jalur baru |

Dua catatan rekonsiliasi (dicatat jujur, bukan disembunyikan):

(1) R-1 bagian 5 menulis rentang "CH-10..CH-15" untuk keluarga distribusi,
    yang secara harfiah menabrak CH-13/CH-14 milik keluarga relasi. R-2 daun
    A.4/A.5 sudah menyelesaikan tumpang-tindih ini (distribusi = CH-10, 11, 12,
    15, 23, 31; relasi = CH-13, 14, 21, 24, 25, 26, 32). Pohon ini mengikuti
    penyelesaian R-2; tidak ada chart dwi-keluarga.
(2) RTM (matriks ketertelusuran) tetap BUKAN chart: ia tabel-matriks dan
    menjadi bahan kartu 13 (registri pola diagram), sesuai R-2 daun B.9.
    Pohon ini hanya mengarahkan: pertanyaan "persyaratan mana dipenuhi apa"
    keluar dari cabang A.

## 6. Apparatus wajib untuk SEMUA chart (berlaku tanpa kecuali)

Inti apparatus berlaku untuk setiap chart pada setiap daun tanpa kecuali, dan
dirangkum dari tiga hulu: sintesis AP R-2 bagian 3, register DAT R-3, serta
kontrak desain R-4. Apparatus khusus daun di bagian 4 menambah syarat yang
hanya relevan untuk bentuk chart tertentu, bukan menggantikan daftar ini.
Satu baris yang gagal di sini membatalkan gambar terlepas dari benar tidaknya
pemilihan chart, karena pohon memilih bentuk dan apparatus membuktikan klaim.

| AP | Aturan | Dasar |
|---|---|---|
| AP-1 | Caption bernomor di ATAS figur: identifier condensed kapital lalu satu kalimat isi; tanggal berlaku tercetak di judul/caption; baris SUMBER di BAWAH hairline | DAT-70, DAT-73, AB-06, KD-12, KD-13 |
| AP-2 | Mark provenans pada angka/figur berupa LABEL TEKS (TERUKUR, DITURUNKAN, PEMASOK, ASUMSI), bukan glif peran; temuan D-5: glif internal sudah diganti label teks oleh guideline 2026-10-03; angka beban-rilis tanpa mark = cacat | KD-16, R-2 AP-2 |
| AP-3 | Label sumbu memakai pasangan kuantitas-satuan ISO 80000-1 (mis. "U", "kWh", "dBm"); tanpa satuan = cacat | AB-07 |
| AP-4 | Basal nol bersama untuk enkoding panjang (bar/column/area); sumbu terpotong = cacat | AB-01, DAT-74 |
| AP-5 | Label langsung menggantikan legenda kotak bila <= 4 seri; legenda kotak pilihan terakhir | AB-04, DAT-74 |
| AP-6 | Satu aksen jenuh pada pesan; warna netral untuk konteks; 3-D, bayangan, gradien, ujung bar membulat, bingkai chart, label berkotak DILARANG | AB-08, DAT-74, DAT-75 |
| AP-7 | Gridline hanya bila nilai harus dibandingkan; tanpa judul di dalam plot area | DAT-74 |
| AP-8 | Semantik ketidakpastian eksplisit: error bar/kotak menyatakan SD, SE, CI, atau kuartil; mencampur tanpa keterangan = cacat | AB-09 |
| AP-9 | Teks nyata dalam gambar (SVG teks, bukan raster) agar dapat diaudit; lebar figur hanya 128 atau 166 mm; Mermaid/Figma-export dilarang sebagai keluaran jadi | DAT-73, KD-09, KD-24, R-2 AP-9 |
| AP-10 | Setiap pemilihan chart ditutup dengan pembacaan ANTI-kasus chart terpilih; nol chart terbit tanpa anti-kasus | R-2 AP-10, gerbang 52/52 R-1 |

Tata bahasa visual mengikuti KD-13/KD-15: garis horizontal saja pada sumbu
bantu, numeral mono rata-desimal, maksimal lima nilai warna terlihat per
halaman (KD-06), aside bergaris menggantikan callout box (KD-16).

Batas pohon ini terhadap dua aturan figur tetangga dalam rentang sumber
DAT-73..DAT-80: caption FOTO ikut DAT-78 (kredit lebih dulu dalam kurung,
lalu subjek, tempat, bulan, tahun - atribusi legal-first) dan PETA ikut
DAT-80 (seri nomor sendiri, mis. Peta 1.1, terpisah dari gambar agar tidak
menyamar sebagai diagram ber-spek). Keduanya bukan chart sehingga tidak
menjadi daun; pemakai yang berakhir di foto/peta dirute ke register DAT
tersebut lewat R-3.

## 7. Fallback dan eskalasi

Bila tidak ada daun A.1..A.7 yang memenuhi syarat masuk:

(1) Cek ulang Gerbang-Akar: kemungkinan pertanyaan sebenarnya struktur/alur
    (cabang B) atau makna glif (cabang C).
(2) Cek padanan terdekat di tabel bagian 3 dan baca ANTI-kasusnya; bila yang
    tersisa hanya chart dengan anti-kasus permanen untuk kasus Anda (mis.
    radar untuk dokumen keputusan resmi), bentuk yang benar adalah TABEL
    dengan apparatus AP-1/AP-3, bukan chart dipaksakan.
(3) Belum terjawab juga: catat sebagai butir GAP-nn (register perbaikan misi,
    dedup terhadap E-nn R-4 anatomi 30) dengan data contoh dan pertanyaan
    pembaca; jangan mengarang tipologi baru di luar CH-01..CH-32 tanpa lewat
    register tersebut. Ini menjaga pohon tertutup dan dapat diaudit.

## 8. Known-defect warisan yang menempel pada rute

Empat cacat diwarisi dari hulu (R-2 bagian 5.3) dan sudah tertempel di sel
rute masing-masing pada tabel berikut. Pemakai pohon wajib membaca baris yang
menyentuh rutenya sebelum mengutip, karena keempatnya adalah known-defect yang
jujur, bukan rahasia internal. Putusan controller D-10 (contract.md 05-10)
mengalihkan sisa verifikasinya ke Register Riset Terbuka lampiran manual, dan
kutipan dari daun yang belum terverifikasi tetap terblokir sampai alat
mengukurnya selesai.

| ID | Cacat | Dampak pada rute pohon |
|---|---|---|
| CH-26 | URL spesifik interaction plot salah-sasaran (galeri induk eda3/practic yang dipegang) | Sitasi CH-26 di daun A.5 hanya level galeri; pri3361.htm terlarang dikutip |
| CH-31 | Body lokal cumfreqp terindikasi salah-simpan (HTTP 200 ladder sah) | Definisi CDF daun A.4 diambil dari ringkasan Wikipedia + konvensi standar; verifikasi ulang oleh verifier |
| N-3 | Primer Few (displayingdata.com) mati DNS | Definisi bullet graph CH-03 dipegang pada rung Wikipedia; atribusi Stephen Few lewat entri tersebut |
| N-5 | IEEE C37.2 identifier KOSONG | Tidak menyentuh cabang A; dicatat agar pemuat silang dari cabang B tidak mengutipnya |

## 9. Referensi

| R | Sumber | Lokasi |
|---|---|---|
| R-1 | Tipologi chart/diagram CH-nn/DIA-nn + AB-01..AB-10 (F4-P9) | `docs/2026-10-04-datum-manual/research/02-tipologi-chart-diagram.md` |
| R-2 | Sintesis riset + pohon tiga-cabang + AP-1..AP-10 (F4-P10) | `docs/2026-10-04-datum-manual/research/03-sintesis-dan-keputusan.md` |
| R-3 | Register aturan lajur-1 DAT-nn (F1-P1) | `docs/2026-10-04-datum-manual/corpus/lajur1-datum-dokumen.md` |
| R-4 | Blueprint TA: DUMP sumber desain, KD-01..KD-32, D-TA-01..12 | `docs/2026-10-04-datum-manual/identification/02_structured.md` |

## 10. Cetakan self-check (alat `work/f6p12_check.py`)

Bagian ini diisi VERBATIM dari cetakan alat checker pada giliran ini setelah
berkas terbit, bukan diketik ulang dari ingatan. Jejak lengkapnya tersimpan di
`work/f6p12_check_out.txt` dan dapat dijalankan ulang oleh verifier dengan
perintah `python work/f6p12_check.py`. Sepuluh CHECK di bawah menutup tiga
tuntutan verifikasi kartu: rute penuh semua keluarga, syarat masuk terukur
per simpul, dan nol chart tanpa anti-kasus.

```text
CHECK 1: PASS - populasi CH di riset 02 = 32 | cetak=32
CHECK 2: PASS - hilang dari rute daun = 0 | hilang=[]
CHECK 3: PASS - 7 daun bersyarat masuk terukur | daun=7 cacat=[]
CHECK 4: PASS - nol kemunculan chart tanpa anti-kasus | baris_tabel=32 chart_unik_di_daun=32 tanpa_anti=[]
CHECK 5: PASS - apparatus wajib AP-1..AP-10 hadir | cetak=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
CHECK 6: PASS - apparatus inti disebut (lebar 128/166, Mermaid, caption, SUMBER, provenans) | 
CHECK 7: PASS - DAT-73..DAT-80 ter-referensi | cetak=['73', '74', '75', '76', '77', '78', '79', '80']
CHECK 8: PASS - jejak A1/A2 nol (U+2014=0, U+00B7=0) | U+2014=0 U+00B7=0
CHECK 9: PASS - frontmatter 6 key + H1==title | 
CHECK 10: PASS - artefak ada di disk non-kosong | bytes=28327
VERDICT: PASS
```

Catatan self-referensi yang jujur: angka `bytes=28327` pada CHECK 10 adalah
cetakan sebelum blok cetakan ini ditempel ke badan berkas; ukuran final di
disk tercatat pada jejak jalan-ulang `work/f6p12_check_out.txt` yang
di-regenerasi setelah penempelan, dan CHECK 10 hanya menuntut non-kosong
(> 15.000 B) sehingga vonisnya tidak berubah oleh penempelan.

Gerbang naturalisasi (scanner fleet, kanal doc) dijalankan pada giliran yang
sama: paragraf pendek C-7 = 0 dari 26, sinyal C-12 = 0, agregasi D-TA-09 tidak
terpicu; artefak ini berkas pustaka antar-agen yang akan dionaturalisasi ulang
saat digest Bagian II (langkah 17), dan tetap bebas A1/A2 sejak sekarang.
