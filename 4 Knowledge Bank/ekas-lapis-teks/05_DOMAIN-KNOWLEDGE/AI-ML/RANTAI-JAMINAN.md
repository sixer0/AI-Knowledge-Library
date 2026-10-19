# Rantai P - Pembelajaran mesin dan sistem berbasis data untuk fungsi analitik & otomasi

## RANTAI BERANTAI PARSIAL TERBIMBING (sejak 11-10-2026, kartu t_54065872)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan R3 yang ada di rak ini** (empat resume W3a
ber-halaman + tambalan W9B/W10 + KEMAMPUAN.md domain). Mata ④ **tetap tanpa ambang terima**:
tidak ada satu pun baris R1/R2 untuk domain ini, jadi angka lulus/tidak-lulus **tidak dapat**
ditetapkan dari sini dan celahnya dibukukan apa adanya di mata ④ bawah.

**Daya-ikat tidak naik.** Seluruh rujukan buku domain ini tetap `pending_verification` (P-5)
dan kolom kontraknya `no-unless-contract-adopts` di
`02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` (ukur 11-10-2026: baris 64-67). Susunan mata
②-⑤ ini **menyiapkan**, insan yang menandatangani; tidak ada baris register yang disunting
oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode evaluasi, prosedur
validasi, dan gerbang operasi**. Bila sebuah pekerjaan menuntut ambang terima kinerja sistem
ML (akurasi minimum, anggaran latensi, batas drift yang dapat diterima), ambangnya milik
**kontrak** atau standar R1/R2 yang belum ada di rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026) |
|---|---|---|---|
| `REF-AIM-001` - Designing Machine Learning Systems, Huyen | **R3** ⏳pending | Sistem ML produksi: framing, evaluasi, kalibrasi, drift, promosi model. | `[R3, Huyen ML Systems, PDF 29]`, `[PDF 36]`, `[PDF 110]`, `[PDF 111]`, `[PDF 122]`, `[PDF 126]`, `[PDF 139]`, `[PDF 146]`, `[PDF 203]`, `[PDF 250]`, `[PDF 258]`, `[PDF 263]`, `[PDF 264]`, `[PDF 284]`, `[PDF 302]` |
| `REF-AIM-002` - Data-Driven Science and Engineering, Brunton & Kutz | **R3** ⏳pending | Ekstraksi pola (SVD/POD), seleksi model (parsimony, CV, kriteria informasi), DMD/SINDy/PINN. | `[R3, Brunton-Kutz DDSE, PDF 212]`, `[PDF 213]`, `[PDF 216]`; peta bagian: bab 4 mulai `[PDF 186]`, bab 7 `[PDF 332]` (diwarisi dari resume, belum dibuka ulang) |
| `REF-AIM-003` - Hands-On Machine Learning 2e, Géron | **R3** ⏳pending | Metrik regresi/klassifikasi, holdout vs cross-validation, regularisasi linear, K-Means/inertia, pembanding optimizer. | `[R3, Géron HOLML, PDF 52]`, `[PDF 55]`, `[PDF 56]`, `[PDF 65]`, `[PDF 105]`, `[PDF 108]`, `[PDF 126]`, `[PDF 127]`, `[PDF 128]`, `[PDF 130]`, `[PDF 131]`, `[PDF 135]`, `[PDF 137]`, `[PDF 182]`, `[PDF 303]`, `[PDF 305]`, `[PDF 308]`, `[PDF 446]` |
| `REF-AIM-004` - Deep Learning, Goodfellow dkk. | **R3** ⏳pending | Fondasi teori: cross-entropy/KL, stabilitas numerik softmax, kapasitas & regularisasi, default Adam. | `[R3, Goodfellow DL, PDF 96]`, `[PDF 101]`, `[PDF 140]`, `[PDF 324]` |

> Semua baris: R3 buku teks/handbook, `pending_verification` - sah untuk **metode dan
> penalaran dengan kutipan halaman**, tidak sah sebagai ambang terima (lihat kartu
> `04_KNOWLEDGE-CARDS/AI-ML/REF-AIM-001..004.md` bagian 3 dan 4).

**Baris register tambahan yang perlu dikenal:** `REF-AIM-005` (baris 104 register) adalah
model latih internal EKAS-Qwen3-4B berstatus **R5 POINTER_ONLY, LOKAL-SAJA** - hanya metadata
yang diarsipkan, bobot tidak disalin. Sesuai aturan pustaka-teknis, R5 tidak pernah menjadi
sandaran akhir; ia hanya penunjuk sumber primernya.

**Konversi halaman (terpaksa berbeda per buku karena lapisan menulis nomor PDF, bukan folio):**
Huyen = cetak + 20 (dicoorkan ulang 11-10-2026 pada sembilan titik folio: PDF 29->9,
PDF 122->102, PDF 126->106, PDF 139->119, PDF 162->142, PDF 250->230, PDF 258->238,
PDF 284->264, PDF 302->282 - konsisten semua). Brunton = cetak + 26 (tiga titik: PDF 212->186,
PDF 213->187, PDF 216->190). Goodfellow tidak seragam antar bagian; folio 301 terkonfirmasi di
PDF 324. Géron: folio tidak ter-render oleh ekstraksi; berkas ini mengutip **nomor halaman PDF
langsung**; offset cetak = pdf - 39 tercatat di tambalan W10 (jejak ukur F2-AIM-04) dan tidak
divonis ulang di sini.

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** kolom "dibuka
ulang" berarti halaman PDF diekstrak dengan `pdftotext -layout` (Xpdf 4.06) pada run kartu
ini dan isinya dicocokkan dengan butir yang dikutip. Jangkar yang **diwarisi dari resume
tanpa dibuka ulang di sini**: peta bab Huyen (PDF 21/45/69/101/139/169 sebagai batas seksi),
peta bagian Brunton, dan seluruh butir Géron yang tidak muncul di tabel ① ini (mis. `eta =
0.1` di PDF 167).

**Bukti byte vault (diukur ulang 11-10-2026 dengan `sha256sum` pada keempat PDF; keempatnya
cocok dengan catatan register):** Géron `adcada20e01633bd`, Goodfellow `427e7af5c0599fd7`,
Huyen `f06ce909ab4af999`, Brunton `6143dd66cc07cfce`.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian, yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`,
tabel "Aturan tingkat pada tiap mata rantai", baris ②).

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| **Kebutuhan bisnis dulu, ML belakangan**; tuntutan akurasi-vs-latensi dibaca dari kelas aplikasi | Enterprise vs konsumen punya profil berbeda: akurasi lebih ketat, latensi lebih dimaafkan (contoh pengenalan bicara 95% -> 95,5% tidak terasa konsumen) `[R3, Huyen ML Systems, PDF 29]`; riset mengejar throughput, produksi mengejar latensi rendah `[R3, Huyen ML Systems, PDF 36]` | Mulai dari arsitektur model ditolak - skor offline tinggi tidak menjawab pertanyaan siapa yang dilayani dan pada anggaran latensi berapa |
| **Metrik dipilih dari distribusi kelas**, bukan kebiasaan | Class imbalance = selisih jumlah sampel antar kelas yang besar (contoh X-ray paru 99,99% vs 0,01%) `[R3, Huyen ML Systems, PDF 122]`; dua model kanker dengan akurasi sama 0,9 tetapi sensitivitas 10% vs 90% `[R3, Huyen ML Systems, PDF 126]`; klasifier "selalu bukan-5" mencapai akurasi >90% `[R3, Géron HOLML, PDF 127]` | Akurasi telanjang pada data miring ditolak - kinerja kelas mayoritas mendominasi metrik dan menyembunyikan kegagalan di kelas yang justru ditagih |
| **Arah trade-off presisi/recall ditetapkan dari biaya operasional**, bukan dari skor | F1 = rata-rata harmonik presisi+recall Eq. (3-3) `[R3, Géron HOLML, PDF 130..131]`; contoh dua kutub: deteksi video aman anak menuntut presisi tinggi, deteksi pencurian toko "30% presisi asal 99% recall" `[R3, Géron HOLML, PDF 131]`; kurva PR disukai bila kelas positif langka `[R3, Géron HOLML, PDF 137]` | Satu angka tunggal untuk semua kasus ditolak - menaikkan presisi menurunkan recall dan sebaliknya (trade-off), jadi pilihan titik operasi adalah keputusan pemilik pekerjaan |
| **Seleksi model lewat validation set / cross-validation; test set hanya sekali di akhir** | Mengukur galat generalisasi berkali-kali pada test set lalu menyetel model kepadanya menghasilkan 5% di laporan dan 15% di produksi; holdout validation memisahkan pemilihan dari penilaian `[R3, Géron HOLML, PDF 55]`; repeated cross-validation untuk data kecil `[R3, Géron HOLML, PDF 56]`; tanpa strategi CV "hampir pasti menghasilkan model yang tidak dapat generalisasi" `[R3, Brunton-Kutz DDSE, PDF 216]` | Menyetel hyperparameter terhadap test set ditolak - test set berhenti menjadi estimat tak-bias; tuning tanpa CV pada data kecil juga ditolak (validasi terlalu pendek = evaluasi tidak teliti) |
| **Model paling sederhana yang mencapai galat minimum menang** (parsimony eksplisit) | Galat runtuh setelah suku kuadrat lalu **naik** lagi ketika derajat polinomial ditambah; "parabolic fit approximately twice as good as a polynomial with degree 10" `[R3, Brunton-Kutz DDSE, PDF 212]`; kerangka Pareto front + Lex Parsimoniae `[R3, Brunton-Kutz DDSE, PDF 213]` | Menambah parameter/suku "siapa tahu berguna" ditolak - memperbaiki galat latih tetapi memperburuk galat uji; ekstrapolasi model overfit meledak sampai orde 10^13 `[R3, Brunton-Kutz DDSE, PDF 216]` |
| **Probabilitas keluaran wajib terkalibrasi bila angkanya dikonsumsi** (bukan hanya peringkatnya) | Kalibrasi = prediksi 70% terjadi 70% dari waktunya; contoh tim A: prediksi 70% vs kenyataan 60% dari 1.000 pertandingan = tidak terkalibrasi `[R3, Huyen ML Systems, PDF 203]` | Skor mentah sebagai angka absolut ditolak - untuk ranking tidak perlu kalibrasi, untuk estimasi jumlah klik/risiko/biaya perlu; ini beda keputusan desain yang harus dinyatakan di muka |
| **Promosi model lewat champion-challenger lalu uji produksi bertahap (shadow -> canary/A-B)**, bukan adu skor offline saja | Model lama = champion, replika ter-update = challenger; jangan deploy sebelum evaluasi `[R3, Huyen ML Systems, PDF 284]`; shadow deployment = "mungkin cara paling aman": rutekan ke dua model, hanya serving model lama, log prediksi baru `[R3, Huyen ML Systems, PDF 302]`; backtest tidak menggantikan test set statis (data rusak di pipeline bikin backtest menipu) `[R3, Huyen ML Systems, PDF 302]` | Promosi langsung atas dasar satu skor offline ditolak - distribusi bergeser dan kegagalan pipeline tidak terlihat di test set beku; continual learning naif (update tiap sampel) juga ditolak: catastrophic forgetting + boros compute `[R3, Huyen ML Systems, PDF 284]` |
| **Monitoring drift wajib diperlengkapi, dan penyebabnya diverifikasi sebelum menyalahkan data** | Dua mode gagal baku: train-serving skew dan degradasi pasca-deploy akibat distribusi bergeser `[R3, Huyen ML Systems, PDF 250]`; definisi kanonis covariate shift (P(X) berubah, P(Y\|X) tetap), label shift (P(Y) berubah), concept drift (P(Y\|X) berubah) `[R3, Huyen ML Systems, PDF 258]`; statistik ringkas (mean/median/variance) tidak cukup - "jika mirip, tidak ada jaminan tidak ada pergeseran" `[R3, Huyen ML Systems, PDF 263]`; uji dua sampel (KS) hanya untuk 1-D dan bisa murah-murahan alert salah `[R3, Huyen ML Systems, PDF 264]` | Dashboard statistik ringkas sebagai satu-satunya bukti drift ditolak; juga ditolak vonis "data bergeser" tanpa memeriksa bug pipeline lebih dulu - estimasi CTO layanan monitoring: 80% drift yang tertangkap disebabkan kesalahan manusia `[R3, Huyen ML Systems, PDF 250]` (kutipan lisan, bukan angka rak) |
| **Provenans data latih dijaga sejak awal (data lineage) dan fitur distandarkan sebelum masuk model** | Mencampur sumber tanpa kualitas tercatat membuat model memburuk dan sulit diobati; lacak asal tiap sampel + labelnya `[R3, Huyen ML Systems, PDF 110]`; fitur berskala jauh berbeda membuat model memberi bobot salah; imputasi nilai hilang yang menabrak nilai sah memicu bug panjang `[R3, Huyen ML Systems, PDF 146]` | Menggabungkan data baru murah (crowdsourcing) ke corpus lama tanpa audit label ditolak - contoh buku: 1 juta label baru justru menurunkan kinerja |
| **Bentuk regularisasi dipilih sesuai tugas; tidak ada algoritma terbaik universal** | Definisi: regularisasi = modifikasi algoritma belajar yang menurunkan galat generalisasi tanpa menurunkan galat latih; no free lunch theorem `[R3, Goodfellow DL, PDF 140]`; konstrain model menyederhanakan dan menekan risiko overfit `[R3, Géron HOLML, PDF 52]`; Ridge = regresi linear + suku kuadrat bobot, evaluasi memakai ukuran tak-terregularisasi `[R3, Géron HOLML, PDF 182]` | Satu bentuk regularisasi default untuk semua model ditolak - teori menyatakan tidak ada bentuk terbaik; juga ditolak mengevaluasi model dengan biaya terregularisasi (yang benar: latih terregularisasi, uji tanpa) |

> Keputusan yang paling menentukan mutu sistem ML di domain ini: **titik operasi dan metrik
> dibekukan sebelum melatih** (kelas mana yang ditagih, presisi atau recall yang mahal,
> apakah angka keluaran dikonsumsi sebagai probabilitas). Semua itu mengalir ke mata ③
> sebagai rumus terpilih dan ke mata ④ sebagai dasar klaim - yang ambangnya tetap harus
> datang dari kontrak.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini, **bukan** di `06_ENGINEERING/CALCULATIONS/
KATALOG-RUMUS.md`: katalog tidak punya entri domain ini sama sekali (ukur 11-10-2026,
`grep -ci "huyen|geron|goodfellow|machine learning|pembelajaran mesin|AIM-"` pada
`KATALOG-RUMUS.md` = 0; `ASUMSI-BAKU.md` juga 0). Butir lintas-lapis ini dicatat di kaki
berkas sebagai celah; pengisian KATALOG bukan wewenang LOCK ini.

### Metrik utama yang tertambat halaman

```
RMSE(X, h) = sqrt( (1/m) * SUM_{i=1..m} ( h(x^(i)) - y^(i) )^2 )   (Eq. 2-1, Géron)
F1 = 2 * (precision * recall) / (precision + recall)               (Eq. 3-3, Géron)
precision = TP / (TP + FP) ;  recall = TP / (TP + FN)              (dari matriks konfus)
inertia(k-means) = rata-rata kuadrat jarak tiap instans ke centroid terdekat
H(P, Q) = H(P) + D_KL(P || Q)                                      (Eq. 3.51, Goodfellow)
```

| Rumus | Sumber | Batas pemakaian |
|---|---|---|
| RMSE Eq. (2-1), termasuk notasi "m = jumlah instans" | `[R3, Géron HOLML, PDF 65]` (badan rumus tercetak utuh) | Memberat kesalahan besar; angka targetnya milik proyek |
| F1 Eq. (3-3) + presisi/recall dari matriks konfus | `[R3, Géron HOLML, PDF 130..131]`, matriks konfus `[PDF 128]` | F1 menghukum ketimpangan presisi/recall; tidak cocok bila biayanya asimetris - pilih titik operasi sendiri |
| ROC AUC: acak murni = 0,5; sempurna = 1 | `[R3, Géron HOLML, PDF 137]` | Sumbu kurva, bukan ambang terima; preferensi ROC vs PR per `[PDF 137]` |
| Inertia K-Means + `n_init` default 10 (ambil solusi terbaik) | `[R3, Géron HOLML, PDF 308]` | Nilai contoh buku 223,3 / 237,5 / 211,6 = ilustrasi, bukan target |
| Grid search / random search atas kisi hyperparameter dengan CV | `[R3, Géron HOLML, PDF 108]` (GridSearchCV cv=5), K-fold cv=10 `[PDF 105]`, cv=3 stratified `[PDF 127]`, manual StratifiedKFold `[PDF 126]` | Ukuran kisi = anggaran komputasi proyek; tidak ada angka rak untuk "cukup" |
| Default Adam: lr 0,001; beta1 0,9; beta2 0,999; eps 1e-8 | `[R3, Goodfellow DL, PDF 324]` (Algorithm 8.7, folio 301) | **Default algoritma dari kotak pseudocode**, bukan angka desain GSP; Tabel 11-2 pembanding optimizer `[R3, Géron HOLML, PDF 446]` |
| Softmax perlu stabilisasi terhadap underflow/overflow | `[R3, Goodfellow DL, PDF 101]` (Eq. 4.1) | Aturan implementasi; konsekuensi: jangan bandingkan logit mentah lintas versi runtime |

### Contoh terhitung (diukur ulang 11-10-2026 dengan skrip sendiri, bukan disalin dari laporan hulu)

```
Géron PDF 130-131 (deteksi angka 5 MNIST): TP=4096, FP=1522, FN=1325
  precision = 4096/5618 = 0,7290850836596654   (buku: 0,7290850836596654 - cocok)
  recall    = 4096/5421 = 0,7555801512636044   (buku: 0,7555801512636044 - cocok)
  F1        = 0,7420962043663375               (buku: 0,7420962043663375 - cocok)
```

```
Huyen PDF 126 (dua model kanker, 1.000 kasus, 100 CANCER):
  Model A: TP=10 FN=90 FP=10 TN=890 -> acc 0,9000 | recall 0,1000 | presisi 0,5000
  Model B: TP=90 FN=10 FP=90 TN=810 -> acc 0,9000 | recall 0,9000 | presisi 0,5000
  -> akurasi identik, sensitivitas terpaut 9x; F1 A=0,1667 vs B=0,6429
```

```
Huyen PDF 36 (latensi vs throughput dengan batching):
  1 query @10 ms -> 100 q/s ; 10 query @10 ms -> 1.000 q/s ; 50 query @20 ms -> 2.500 q/s
  (ketiganya dihitung ulang: cocok dengan teks buku)
```

```
Kalibrasi (Huyen PDF 203): prediksi "A menang 70%" vs fakta 600 menang dari 1.000
  -> model terkalibrasi seharusnya menyebut 60%
```

```
Mini-demo Eq. (2-1) pada kasus buatan (y = [1,2,3,4]; h = [1,1; 1,9; 3,3; 3,8]):
  RMSE = 0,1936 ; MAE = 0,1750  (dihitung skrip run ini; PROJECT-DERIVED, bentuknya
  sah dipakai di lembar hitung, angkanya bukan target)
```

| Masukan | Nilai contoh | Tag | Sumber |
|---|---|---|---|
| Konstanta rumus (pangkat 1/m, harmonik 2) | tetap | `SOURCE-DERIVED` | `[R3, Géron HOLML, PDF 65]`, `[PDF 131]` |
| Titik operasi presisi/recall (mis. 90% precision) | 0,90 (contoh buku, threshold ~8.000) | `ASSUMPTION` untuk proyek nyata (kebutuhan pemilik, bukan angka rak) | `[R3, Géron HOLML, PDF 135]` |
| Jumlah lipatan CV | 3 / 5 / 10 (contoh kode buku) | `PROJECT-DERIVED` (pilihan anggaran komputasi) | `[R3, Géron HOLML, PDF 105, 108, 127]` |
| Ambang deteksi drift (nilai statistik uji) | tidak ada | **belum ada di rak** - lihat mata ④ | metode uji `[R3, Huyen ML Systems, PDF 263..264]` |

> **Aturan yang membatalkan hitungan bila dilanggar:** angka contoh buku (0,9; 7.816; 211,6;
> 0,001/0,9/0,999) adalah ilustrasi pedagogis. Memakainya sebagai target kinerja =
> angka tanpa asal-usul (langgar aturan 3 dan 6 `pustaka-teknis`). Biaya pelatihan/inferensi
> (GPU-jam, anggaran latensi ms) tidak ada di rak ini - wajib `ASSUMPTION` dengan
> sensitivitas + rencana penggantian, atau `OEM-DERIVED` dari lembar data perangkat.

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara membuktikan sebuah sistem ML bekerja dan bertahan
bekerja. Yang TIDAK bisa dinyatakan: ambang terima.** Urutan tingkat untuk mata ini adalah
R1 -> R2 -> kontrak (`ASSURANCE-WORKFLOW.md` baris ④); R3 hanya sah bila kontrak
mengadopsinya tertulis, dan kolom register keempat buku ini berbunyi
`no-unless-contract-adopts`.

Uji intern metode (sah dijalankan, hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Evaluasi tak-bias | Pisahkan train/validation/test; test set hanya untuk estimat akhir; validasi representatif terhadap data produksi (aturan set representatif + train-dev) | metode R3 `[R3, Géron HOLML, PDF 55, 56]` |
| Konsistensi lintas lipatan | Jalankan CV; sebar skor antar fold dilaporkan bersama rata-ratanya | `[R3, Géron HOLML, PDF 105, 126, 127]`; **plafon sebaran antar-fold = belum ada di rak** |
| Metrik per kelas | Laporkan matriks konfus + presisi/recall per kelas, bukan akurasi tunggal, pada data miring | `[R3, Huyen ML Systems, PDF 122, 126]`; `[R3, Géron HOLML, PDF 128..131]` |
| Uji kalibrasi | Frekuensi kejadian nyata vs probabilitas prediksi pada sample representatif | `[R3, Huyen ML Systems, PDF 203]`; **deviasi maksimum yang diterima = belum ada di rak** |
| Deteksi skew/shift | Uji dua sampel (KS untuk 1-D; LSDD/MMD multivariat; reduksi dimensi dulu), bandingkan train vs serving | `[R3, Huyen ML Systems, PDF 263, 264]`; **nilai-p / ambang alert = angka proyek** |
| Gerbang promosi | Challenger tidak menggantikan champion sebelum evaluasi lulus; shadow deployment melayani cermin trafik tanpa efek ke pengguna, hasil logfile dibandingkan | `[R3, Huyen ML Systems, PDF 284, 302]`; **kriteria "lebih baik" = kontrak** |
| Regresi mutu saat training | Pilih optimizer sadar trade-off (kecepatan vs kualitas konvergensi) | `[R3, Géron HOLML, PDF 446]` (Tabel 11-2); default Adam `[R3, Goodfellow DL, PDF 324]` - konsistensi implementasi, bukan ambang mutu |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima kinerja ML di rak ini.** Ukur 11-10-2026:
   `MASTER-REFERENCE-REGISTER.csv` = 0 baris R1/R2 ber-domain AI-ML (seluruh R1/R2 di rak
   hanyalah 4 baris: IEEE 1188/IEC 62485-2, ANSI-NETA ATS-2017, IEC 61280-4-2,
   BS EN 62676-1-2 - semuanya domain lain); `AMBANG-TERIMA-INDUK.md` = 0 butir menyebut
   machine learning/akurasi analitik; `GAP-REGISTER.csv` = 0 baris ber-domain AI-ML
   (satu-satunya baris yang menyebut keempat buku ini adalah GAP-021, domain SOFTWARE-DATA,
   status `sebagian`); `KEMAMPUAN-REGISTER.csv` = 23 baris AIM, 23/23
   `draft-tidak-terverifikasi-insan`.
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK
   ini): ambang terima kinerja sistem ML (akurasi/recall minimum per kelas, anggaran latensi
   inferensi, batas drift yang memicu retrain) tidak memiliki sandaran R1/R2. Yang seharusnya
   masuk rak: standar pengujian/validasi sistem pembelajaran mesin, atau adopsi tertulis R3
   oleh kontrak proyek. Catatan: GAP-021 (buku teks ML sebagai dasar analitik video & ASR)
   kini **sebagian tertutup di sisi lapisan teks** oleh rantai ini - tetapi statusnya naik
   hanya lewat jalur register, bukan lewat berkas ini.
3. **Bentuk jawaban yang sah hari ini** saat ambang kinerja ML diminta: nyatakan "tidak ada
   di rak ini; sumber yang seharusnya: R1/R2 pengujian model ML atau pasal adopsi R3 dalam
   kontrak", lalu mintakan angka itu ke pemilik pekerjaan - **jangan** mengambil angka contoh
   buku (0,9; 0,729/0,756; 211,6; default Adam) sebagai ambang. Keempat resume menegaskan
   bagian 4-nya: "bukan ambang kontrak".

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan yang memakai sistem ML = bukti bahwa **setiap klaim kinerja punya
jalur ①->④ dan kondisi operasinya tercatat**, bukan hanya skor akhir satu baris.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Kartu kendali rantai per klaim kinerja (`TPL-00`) | ✅ | Bentuk minimum di `ASSURANCE-WORKFLOW.md` bagian "Kartu kendali rantai"; sah tertulis "menunggu kontrak" untuk ambangnya |
| Beku kebutuhan: objektif bisnis, kelas aplikasi (enterprise/konsumen), anggaran latensi | ✅ | Titik keputusan mata ② `[R3, Huyen ML Systems, PDF 29, 36]`; cermin format `TPL-06` (ketertelusuran requirement) |
| Register dataset + split (train/validation/test) dengan provenans | ✅ | Data lineage `[R3, Huyen ML Systems, PDF 110]`; set validasi/test representatif `[R3, Géron HOLML, PDF 56]`; simpan manifest hash per split agar tidak ada duplikat silang |
| Lembar perhitungan metrik `TPL-02` dengan tag per masukan | ✅ | Rumus Eq. 2-1/3-3 + tag `SOURCE-DERIVED`/`PROJECT-DERIVED`/`ASSUMPTION`; tiap `ASSUMPTION` punya sensitivitas + rencana penggantian (gerbang G3, `ASSURANCE-GATES.md:52-58`) |
| **Pemeriksaan orang kedua** atas hitungan metrik | ✅ | G3 tidak tertutup tanpa ini; preseden jujur di rak: `CALC-P00-001.md` masih "belum diperiksa orang kedua" |
| Jejak pelatihan: seed, versi pustaka, kisi hyperparameter yang dicoba, skor per lipatan | ✅ | Contoh bentuk jejak: `random_state=42` + skor tiga fold `[R3, Géron HOLML, PDF 126, 127]`; kisi GridSearchCV `[PDF 108]`; tanpa ini hasil tidak dapat direproduksi |
| Bukti kalibrasi dan metrik per kelas saat serah | ✅ | `[R3, Huyen ML Systems, PDF 126, 203]`; laporkan matriks konfus aktual, bukan hanya satu angka |
| Rekam promosi: challenger vs champion + hasil shadow/canary | ✅ | `[R3, Huyen ML Systems, PDF 284, 302]`; simpan di `08_EVIDENCE/SCREENSHOTS-LOGS/` |
| Rencana monitoring drift + pernyataan asal ambangnya | ✅ | Metode `[R3, Huyen ML Systems, PDF 258, 263]`; ambang alert harus menyebut kontrak atau tertulis "belum ada di rak" - jangan kosong tanpa keterangan |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi; ini titik di mana celah mata ④ paling sering tersamar |

**Keterbatasan kerangka yang ada:** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi, baterai,
genset, video, termal, penyimpanan) dan **tidak punya bagian untuk uji sistem ML/analitik**;
pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas itu) plus tabel Ringkasan
sumber ambang-nya, dan nyatakan bahwa jenis uji ML belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dan setiap angkanya bertanda `[R-n]`
dengan halaman yang sudah dibuka ulang terhadap vault; angka contoh dihitung ulang sendiri
oleh run ini. Mata ④ **jujur kosong untuk ambang**: tidak ada R1/R2 untuk domain ini, dan
kinerja ML yang mengikat hanya sah bila kontrak menyebut angkanya.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier W3 menaikkan daya-ikat resume
dari `pending_verification`, (b) insan menandatangani unit `KEMAMPUAN.md` domain ini
(ukur 11-10-2026: 23/23 baris AIM register masih `draft-tidak-terverifikasi-insan`), dan
(c) ambang terima kinerja ML punya sandaran R1/R2 atau adopsi kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_54065872. Semua butir terukur langsung dari berkas vault
(pdftotext Xpdf 4.06) dan lapisan teks; berkas-berkas itu bukan milik LOCK ini sehingga
**tidak disunting**.

1. **Resume Huyen, baris "Validasi data (TFX)" salah jangkar.** Berkas resume menambatkan
   butir alat validasi statistik-ringkas ke `PDF 250`; teks "TensorFlow Extended's built-in
   data validation tools use only summary statistics" ada di **PDF 263** (folio 243). PDF 250
   berisi train-serving skew + catatan kaki CTO 80% (jangkar F2-AIM-03 - yang itu benar).
2. **Resume Huyen, baris "Latensi vs akurasi ... PDF 110..112" salah jangkar.** Contoh
   pengenalan bicara 95% -> 95,5% ada di **PDF 29** (folio 9, dikonfirmasi); PDF 110-112
   berisi data lineage dan natural labels, tanpa token "95,5".
3. **Resume Huyen, baris "Feature store ... bab 10, PDF 162" menyesatkan.** PDF 162 masih
   bab 5 (folio 142) dan hanya *menunjuk* bab 10; bab 10 (Infrastructure and Tooling for
   MLOps) mulai di **PDF 313**.
4. **Resume Huyen, jangkar "Data leakage PDF 139" menunjuk pintu masuk, bukan badan.**
   PDF 139 = halaman judul bab 5 yang *menjanjikan* seksi leakage ("section 'Data Leakage'
   on page 135" tercetak di PDF 146); badan seksi mulai sekitar PDF 155 dst. Sah dibaca
   sebagai rujukan-batas-seksi, tidak sah sebagai jangkar kalimat definisi.
5. **Resume Géron, baris "Overfitting/underfitting lewat contoh polinomial PDF 8" salah.**
   PDF 8 adalah halaman daftar-isi bab 1; contoh polinomial bias/variance ada di PDF 53-54
   dan 177-182 (yang terakhir dibuka kartu ini: PDF 182 memuat teks trade-off bias +
   definisi Ridge).
6. **KEMAMPUAN.md kolom halaman AIM-012 tidak seragam dengan jejak ukurnya.** Baris unit
   menulis `[pdf hal. 135]` untuk ROC-AUC, sedangkan baris jangkar W9B berkas yang sama
   (F2-AIM-01) mencatat `pdf_p137 (cetak 98)` - dan memang kalimat "AUC acak = 0,5;
   sempurna = 1" berada di PDF 137. PDF 135 berisi contoh threshold 90% precision.
7. **Kepala resume Brunton menulis "Cambridge University Press, 2022"; halaman hak cipta
   vault (PDF 6) menulis "Copyright (c) 2021 Brunton & Kutz, Cambridge University Press"**
   dan judul kartu REF-AIM-002 ikut "(2021...)". Edisi kedua terkonfirmasi teks ("Overview
   of Second Edition"). Satu berkas, dua tahun terbit.
8. **Banner KEMAMPUAN.md mengunci "sign-off engineer 0/332"** (tanggal beku 09-10-2026),
   sedangkan `KEMAMPUAN-REGISTER.csv` kini berisi 372 baris (ukur 11-10-2026) - digest
   butuh regenerasi angka (kelas IDX; di luar LOCK ini).

Butir 1-7 menyangkut berkas resume W3a dan digest W4/W9B/W10 (milik jalur BUKUV3); butir 8
menyangkut sinkronisasi digest-register. Semuanya lewat mediasi controller ke profil pemilik
(M2); tidak ada yang ditambal di run ini.
