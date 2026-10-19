# Rantai T - Survei dan pemetaan geospasial untuk pekerjaan terpasang

> **PENAMAAN AD-HOC (kartu t_9b7ace41, 11-10-2026).** Huruf "T" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller (preseden: `MECHANICAL/RANTAI-JAMINAN.md` CATATAN SILANG-PEMILIK butir 1, yang
> menduga alokasi berurutan S,T = pasangan-1). Ganti huruf di kepala bila controller memutuskan
> lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_9b7ace41)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** (dua resume ber-halaman
`REF-GEO-001`/`REF-GEO-002` + `KEMAMPUAN.md` domain + dua kartu `04_KNOWLEDGE-CARDS/GEOSPATIAL-SURVEY/`
+ digest sapu-baca L1/L3) diperkuat buka-ulang halaman vault pada run kartu ini - termasuk
**menghitung ulang seluruh contoh numerik buku** dengan parser, bukan menyalin laporannya.
Mata ④ **tanpa ambang terima yang sah dari rak**: rak ini hanya punya R3, dan angka toleransi
yang tercetak di dalamnya adalah **kutipan R3 terhadap standar Amerika Serikat** (FGCS/NGS,
ALTA/ACSM) yang salinannya tidak ada di rak. Celah dibukukan apa adanya di mata ④.

**Daya-ikat tidak naik.** Kedua rujukan berstatus `ACTIVE` dengan kolom
`may_set_acceptance = no-unless-contract-adopts` di register induk (baris 36-37). Unit
kemampuan domain ini (`KM-0116`, `KM-0117`) masih `draft` + `draft-tidak-terverifikasi-insan`
(baris 117-118 `KEMAMPUAN-REGISTER.csv`, ukur 11-10-2026). Susunan mata ②-⑤ ini **menyiapkan**,
insan yang menandatangani; nol baris register disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode ukur, cara memeriksa
hitungannya, dan cara menyatakan seberapa baik sebuah hasil ukur**. Ambang ketelitian yang
mengikat ditetapkan **pemberi kerja atau standar yang mengikat kontrak** - ini ditegaskan
berkas resume `[R3, berkas rak Surveying, baris 40-41]` dan bukan tafsiran rantai ini.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 dengan pypdf + Xpdf 4.06 `pdftotext -layout`) |
|---|---|---|---|
| `REF-GEO-002` - Kavanagh & Mastin, *Surveying: Principles and Applications*, edisi **kesembilan**, Pearson 2014 | **R3** ACTIVE | Prinsip leveling: definisi BM/TBM/TP/BS/HI/FS/IS + **arithmetic check**; kurvatur+refaksi; kelas ketelitian leveling; traversi: *error of closure*, **precision ratio**, **Compass rule (Bowditch)**; survei konstruksi + *as-built*; spesifikasi survei konstruksi. | `[R3, Kavanagh, PDF 41]` (Eq. 2-2 + Tabel 2-3, folio 28); `[R3, PDF 49]` (definisi leveling, folio 36); `[R3, PDF 54]` (Gambar 2-15 *arithmetic check*, folio 41); `[R3, PDF 65]` (Contoh 2-4 ambang order/kelas + Tabel 2-1, folio 52); `[R3, PDF 169-172]` (bab 6 Traversi mulai, *error of closure* pertama PDF 172); `[R3, PDF 180]` (precision ratio + rentang rasio akurasi, folio 167); `[R3, PDF 182-184]` (6.9 Compass rule + Tabel 6-4, folio 169-171); `[R3, PDF 455]` (*as-built survey*, folio 442); `[R3, PDF 466]` (gambar as-built untuk konstruksi bawah tanah, folio 453); `[R3, PDF 470]` (13.21 spesifikasi survei konstruksi, folio 457) |
| `REF-GEO-001` - Bolstad & Manson, *GIS Fundamentals*, edisi **ketujuh**, terbitan 2022 | **R3** ACTIVE | Model data raster/vektor; koordinat geografis (paralel, meridian, sumbu rotasi); **geodesi, datum, epoch, proyeksi** - inti keputusan pemetaan; sistem koordinat Amerika Utara (State Plane, UTM). | `[R3, Bolstad, PDF 40]` (titik nol bujur bergeser ~102 m dari Royal Greenwich Observatory, folio 28); `[R3, PDF 41]` (Gambar 2-6/2-7 + contoh OCR rusak, folio 29, kepala "Chapter 2: Data Models"); `[R3, PDF 101]` (bab 3 Geodesy, Projections, and Coordinate Systems mulai); `[R3, PDF 103]` (aturan "satu datum, satu epoch, satu proyeksi", folio 91); `[R3, PDF 112]` (NAD27 -> NAD83(1986): *often tens to hundreds of meters*, folio 100); `[R3, PDF 116]` (*many datum shifts are quite large, up to tens of meters*, folio 104); `[R3, PDF 137-140]` (State Plane Coordinate System) |
| Paket kemampuan domain (2 unit kalkulator) | **belum insan** | `K-0116`/`SVY-001` Differential Leveling & Arithmetic Check (1 rumus, 6 uji); `K-0117`/`SVY-002` Traverse Closure & Compass Rule Adjustment (1 rumus, 6 uji); keduanya `composite_parent = SITE_SURVEY_WORKFLOW` | sumber halaman di register: `[R3, Kavanagh, PDF 49-54]` dan `[R3, Kavanagh, PDF 158-184]` - **jangkar awal rentang kedua meleset**, lihat CATATAN SILANG-PEMILIK butir 2 |
| Padanan untuk verifikasi dimensi & ketegakan struktur | R3 + kontrak | Rantai K (CIVIL-STRUCTURAL) menunjuk "Survei - rantai L" untuk baris itu | ⚠ penunjuk **kabur**: huruf L sudah dipakai BUILDING-CONSTRUCTION; yang dimaksud adalah rantai ini - lihat CATATAN SILANG-PEMILIK butir 4 |
| **SRGI2013** + aturan BIG/standar geodesi Indonesia | **R1/R2** | Datum, sistem koordinat, dan kelas ketelitian yang mengikat pekerjaan Indonesia | ❌ **TIDAK ADA di rak**, **belum punya gap_id** (mata ④ butir 3) |
| **FGCS/NGS Geometric Geodetic Accuracy Standards** (asal-usul kelas order/leveling) | **R2** | Sumber sah angka `0.008√K` dsb. yang dikutip Kavanagh | ❌ **TIDAK ADA** - hanya disebut lewat buku `[R3, Kavanagh, PDF 321]` (folio 308: "Federal Geodetic Control Subcommittee (FGCS) 1988 ... available through the National Geodetic Survey") |
| **ALTA/ACSM 2005 Standards** (Relative Positional Accuracy) | **R2** | Ambang RPA 95% yang dirujuk Kavanagh 11.1.2 | ❌ **TIDAK ADA** - hanya disebut `[R3, Kavanagh, PDF 180]` |
| Lembar data alat ukur (total station, level digital, GNSS) | **R4** | Ketelitian tulis instrumen tertentu, jarak operasi, kalibrasi | per proyek - **satu-satunya tingkat sah untuk angka alat** |

**Konversi halaman (terukur hari ini).** Kavanagh: **PDF = cetak + 13** pada seluruh titik uji
(PDF 41 -> folio 28, PDF 49 -> 36, PDF 54 -> 41, PDF 65 -> 52, PDF 158 -> 145, PDF 180 -> 167,
PDF 183 -> 170, PDF 184 -> 171, PDF 455 -> 442, PDF 470 -> 457). Bolstad: selisih **+12** pada
lima titik uji (PDF 40 -> 28, PDF 41 -> 29, PDF 103 -> 91, PDF 112 -> 100, PDF 116 -> 104);
konstanta ini **belum teruji di luar kelima titik itu** dan bagian depan buku memakai folio
romawi, jadi jangan mengonversi nomor bolak-balik tanpa memeriksa folio halaman yang dikutip.
Berkas resume menyebut "halaman 41" dan itu **nomor PDF**, bukan cetak (sudah dikoreksi berkas
resume lewat KOREKSI-RR3A, 11-10-2026).
Angka kepala kedua buku: Kavanagh 600 halaman / 340 bookmark, Bolstad 746 halaman / 0 bookmark -
keempatnya terukur ulang hari ini (pypdf), cocok dengan kepala resume.

**Provenans pembukaan halaman.** Seluruh jangkar di kolom terakhir dibuka sendiri pada run kartu
ini. Tidak ada yang diwarisi tanpa buka-ulang. Yang **tidak** ditemukan dan karenanya tidak
diklaim: badan Tabel 2-1 dan Tabel 2-2 (daftar nilai ambang per order/kelas) tidak ter-render
sebagai teks pada rentang PDF 45-72 yang dipindai - yang terbuka adalah **penggunaannya** di
Contoh 2-4 (`PDF 65`) dan catatan kakinya (`PDF 66`). Karena itu berkas ini **mengutip bentuk
rumus dan satu nilai kelas yang terbaca**, bukan menyalin seluruh tabel.

**Cara pakai dua buku ini berbeda dan itu menentukan (terakun L1):** Bolstad tanpa bookmark +
OCR rusak - Ctrl+F sering gagal, praktis dibaca berurutan; vonis "topik tidak ada" dari kegagalan
Ctrl+F = kesalahan kelas F. Kavanagh 340 bookmark - dirujuk normal. Bukti OCR rusak terukur ulang
hari ini: PDF 41 membuka dengan `Porollels. Eost-West lines of equol IOll!ude`, dan bahkan
halaman hak ciptanya (PDF 2) tercetak `Copyright (c) 1022 by Paul Bolstad, Steven Manson`
seharusnya 2022 - lapis teksnya rusak sistematis, bukan sporadis.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian; yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`).

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| **Datum, epoch, dan proyeksi dibekukan di dokumen sebelum satu titik pun diukur** - dan dinyatakan di setiap gambar/lembar data | Aturan buku: semua data harus dalam sistem koordinat **satu datum, satu epoch, satu proyeksi**; "Failure to adjust for datum and coordinate system differences is the root of many errors in spatial analysis" `[R3, Bolstad, PDF 103]` | "Nanti disamakan saat olah data" **ditolak** - selisih antar-datum terukur hingga puluhan meter `[R3, Bolstad, PDF 112, 116]`, cukup membuat penempatan tiang/kamera meleset `[R3, berkas rak GIS Fundamentals, baris 37-38]` |
| **Metode ukur dipilih sesuai besaran yang dibutuhkan** (bedanya tinggi -> leveling; posisi planimetris -> traversi/total station; cakupan luas -> penginderaan jauh sebagai suplemen) | Struktur Kavanagh: Bagian I prinsip (PDF 14), Bagian II indraja (PDF 368), Bagian III penerapan (PDF 416) `[R3, berkas rak Surveying, baris 17-20]` | Satu metode untuk semua besaran **ditolak** - beda tinggi tidak dapat diambil dari koordinat planimetris tanpa prosedur leveling |
| **BS dan FS dijaga kira-kira sama panjang** pada setiap setup leveling | Buku: teknik menyeimbangkan jarak "effectively cancels out this type of error" (kurvatur+refaksi) `[R3, Kavanagh, PDF 41]`; uji-peg menunjukkan selisih 10 m dengan galat collimation 0,00015 m/m hanya memberi efek 0,002 m `[R3, Kavanagh, PDF 62]` | Jarak panjang-sebelah-pendek **ditolak** - galat sistematis alat tidak saling membatalkan dan tidak terlihat di arithmetic check |
| **Line of sight ditahan >= 0,5 m di atas permukaan tanah** untuk leveling presisi | `[R3, Kavanagh, PDF 67]` (saran kerja alat butir 12, folio 54) | Membaca rendah di atas perkerasan panas **ditolak** - refaksi menelan selisih yang lebih besar daripada ketelitian alat |
| **Setiap rangkaian leveling ditutup (loop) ke BM awal atau BM lain yang diketahui, dan elevasi BM awal diverifikasi dulu** | `[R3, Kavanagh, PDF 54]` (arithmetic check); `[R3, Kavanagh, PDF 65]` (two-way leveling / GNSS presisi; "particularly important when the survey loops back to the starting BM and no other verification is planned") | Rangkaian terbuka tanpa penutup **ditolak** - arithmetic check tetap lulus sempurna padahal ada satu kesalahan besar |
| **Traversi dinilai dengan precision ratio E/P, lalu disesuaikan (Compass rule) sebelum koordinat dihitung** | `[R3, Kavanagh, PDF 180]` (E/P, pembulatan penyebut ke 100 terdekat); `[R3, PDF 182-184]` (6.9 Compass rule, Tabel 6-4) | Mengeluarkan koordinat dari data mentah yang belum tertutup **ditolak** - sisa penutup ikut "masuk" ke setiap titik berikutnya tanpa jejak |
| **Kelas ketelitian declared di dokumen rancangan** (order/kelas leveling atau rasio akurasi traversi), bukan diputuskan setelah ukur | Kavanagh mengaitkan kelas pekerjaan dengan rasio: pekerjaan konstruksi umum 1/3.000-1/5.000 `[R3, PDF 470]`; survei rekayasa 1/3.000-1/10.000, nilai minimum legislasi lazim 1/5.000-1/7.500 `[R3, PDF 180]` | Menetapkan target setelah melihat hasil **ditolak** - mengubah angka menjadi pembenaran |
| **Mutu alat dinyatakan dari lembar data, bukan dari jenisnya** | Angka buku untuk level digital (simpangan baku 1 km double-run 0,3-1,0 mm elektronik / 2,0 mm optik; jarak akurasi EDM ~1:1.000) adalah angka pabrikan yang **diringkas** R3 `[R3, Kavanagh, PDF 45]` | Memakai angka ringkasan buku sebagai spesifikasi alat **ditolak** - angka produk wajib `[R4]` |
| **Survei as-built sebagai bagian paket serah**, bukan kegiatan opsional | `[R3, Kavanagh, PDF 455]` (final survey = as-built survey, dipakai untuk pembayaran akhir kontraktor dan penyelesaian gambar as-built); `[R3, PDF 466]` (gambar as-built "especially important in urban areas where underground construction is extensive") | Menggambar kembali dari gambar rancangan **ditolak** - perbedaan terhadap gambar rancangan wajib dijelaskan (`09_HANDOVER/AS-BUILT/README.md`) |

> Keputusan paling menentukan di rantai ini: **yang dinilai lebih dulu adalah apakah sebuah
> kesalahan berarti, baru berapa besar angkanya.** Buku ini menjelaskan *kapan* kesalahan berarti
> dan kapan tidak `[R3, berkas rak Surveying, baris 31-33]`; itu yang membuat hasil ukur pihak
> ketiga dapat diperiksa, bukan ditelan apa adanya.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini, **bukan** di `06_ENGINEERING/CALCULATIONS/
KATALOG-RUMUS.md`: katalog tidak punya seksi survei/geospasial sama sekali (ukur 11-10-2026,
berkas 613 baris, heading seksi 1-13: optik, serat, pembumian, petir, listrik, keandalan,
penyimpanan, baterai, UPS, genset, jaringan, termografi, standar - `grep` untuk `traverse`,
`leveling`, `datum` = **0** hitung). Butir lintas-lapis ini dicatat sebagai celah; pengisian
KATALOG bukan wewenang LOCK ini (CATATAN SILANG-PEMILIK butir 5).

### 1. Kurvatur + refraksi pada pembacaan rambu

```
(c + r)m = 0,0675 * K^2        K = panjang sights dalam km   (Eq. 2-2)
(c + r)ft = 0,574 * K^2        K dalam mile                   (bentuk kaki, Tabel 2-3)
```

`[R3, Kavanagh, PDF 41]` (folio 28). Dasar fisiknya: `c = 0,0785 K^2` m dengan `r ~ -0,14c`,
sehingga `c + r = 0,0675 K^2`.

**Ukur ulang 11-10-2026 terhadap Tabel 2-3** (reproduksi parser, bukan salinan laporan):

| Jarak | Nilai buku | Hitung `0,0675 K^2` | Cocok pada desimal buku |
|---|---|---|---|
| 30 m | 0,0001 | 0,0000607 | ✅ (4 d) |
| 60 m | 0,0002 | 0,0002430 | ✅ (4 d) |
| 100 m | 0,0007 | 0,0006750 | ✅ (4 d) |
| 120 m | 0,001 | 0,0009720 | ✅ (3 d) |
| 150 m | 0,002 | 0,0015188 | ✅ (3 d) |
| 300 m | 0,006 | 0,0060750 | ✅ (3 d) |
| 1 km | 0,068 | 0,0675000 | ✅ (3 d) |

Pesan yang mengikat rancangan: **galat ini tumbuh dengan kuadrat jarak**, jadi efek pembacaan
rambut yang "kecil" pada sights pendek menjadi dominan pada sights panjang - inilah sebabnya
buku menyebut kesalahan jenis ini "of only marginal importance" **hanya** untuk jarak yang jarang
melebihi 60 m, dan kesimpulan itu bergantung jarak `[R3, Kavanagh, PDF 41; berkas rak Surveying,
baris 26-29]`.

### 2. Arithmetic check leveling (penyelesaian tinggi alat)

```
HI      = elevasi BM/TP + BS
Elev TP = HI - FS
CHECK   : Σ BS - Σ FS = elevasi akhir - elevasi awal
```

`[R3, Kavanagh, PDF 49]` (definisi BM, TBM, TP, BS, HI, FS, IS), `[R3, PDF 53-54]`
(Gambar 2-14/2-15, *arithmetic check*).

**Ukur ulang 11-10-2026** dari data Gambar 2-15 (satu rangkaian dua setup):

```
HI1     = 161,273 + 2,868 = 164,141     TP1 = 164,141 - 0,982 = 163,159
HI2     = 163,159 + 1,977 = 165,136     BM461 = 165,136 - 0,540 = 164,596
Σ BS - Σ FS = 4,845 - 1,522 = 3,323 = 164,596 - 161,273   ✅ cocok tepat
```

> **Check ini membuktikan aritmetika, BUKAN kebenaran lapangan.** Rangkaian yang salah di satu
> tempat tetapi tersambung kembali ke BM awal bisa lulus check ini - karena itu mata ② menuntut
> penutup loop dan verifikasi BM awal, bukan hanya check.

### 3. Precision ratio traversi

```
E       = linear error of closure = sqrt( (Σ lat)^2 + (Σ dep)^2 )
Precision ratio = E / P    ditulis 1/(P/E), penyebut dibulatkan ke 100 terdekat
```

`[R3, Kavanagh, PDF 180]` (folio 167).

**Ukur ulang 11-10-2026** dari contoh buku: `E = 0,49`, `P = 2.081,19` ->
`P/E = 4.247,3` -> **1/4.200**, persis seperti tercetak (`1/4,247 ~ 1/4,200`) ✅.

### 4. Compass rule (Bowditch) - distribusi galat penutup

```
C_lat(i) = error_lat * jarak(i) / P        C_dep(i) = error_dep * jarak(i) / P
tanda koreksi = LAWAN tanda error          setelah koreksi: Σ lat = 0,00 dan Σ dep = 0,00
```

`[R3, Kavanagh, PDF 182-184]` (6.9 Compass rule; Tabel 6-4 folio 171).

**Ukur ulang 11-10-2026 terhadap Tabel 6-4** (error lat +0,06; error dep -0,49; P = 2.081,19):

| Kursus | Jarak (ft) | `C_lat` hitung | `C_lat` buku | `C_dep` hitung | `C_dep` buku |
|---|---|---|---|---|---|
| AE | 350,10 | 0,01 | 0,01 | 0,08 | 0,08 |
| ED | 579,03 | 0,02 | 0,02 | 0,14 | 0,14 |
| DC | 368,28 | 0,01 | 0,01 | 0,09 | 0,09 |
| CB | 382,20 | 0,01 | 0,01 | 0,09 | 0,09 |
| BA | 401,58 | 0,01 | 0,01 | 0,09 | 0,09 |
| **Σ** | 2.081,19 | **0,06** | 0,06 | **0,49** | 0,49 |

Sepuluh dari sepuluh sel koreksi cocok dengan tabel buku pada presisi 0,01 ft; jumlah tertutup
pada nilai error ✅.

### 5. Masukan, tag, dan asumsi

| Besaran | Nilai contoh | Tag | Sumber |
|---|---|---|---|
| Konstanta kurvatur+refraksi metrik | 0,0675 m per km² | `SOURCE-DERIVED` | `[R3, Kavanagh, PDF 41]` |
| Panjang sights maksimum agar galat rambu "marginal" | 60 m (200 ft) | `SOURCE-DERIVED` (konteks Amerika Utara, lihat batas) | `[R3, Kavanagh, PDF 41]` |
| Tinggi sights minimum untuk leveling presisi | 0,5 m (18 in) | `SOURCE-DERIVED` | `[R3, Kavanagh, PDF 67]` |
| Rasio akurasi traversi pekerjaan konstruksi umum | 1/3.000 - 1/5.000 | `SOURCE-DERIVED` **sebagai praktik buku**, bukan ambang kontrak | `[R3, Kavanagh, PDF 470]` |
| Rasio akurasi survei rekayasa / nilai minimum legislasi setempat | 1/3.000 - 1/10.000 / 1/5.000 - 1/7.500 | `SOURCE-DERIVED` (praktik; **nilainya milik standar yang tidak ada di rak**) | `[R3, Kavanagh, PDF 180]` |
| Simpangan baku level digital 1 km double-run | 0,3 - 1,0 mm (elektronik), 2,0 mm (optik) | **`OEM-DERIVED` yang dikutip R3** - jangan dipakai tanpa `[R4]` | `[R3, Kavanagh, PDF 45]` |
| Ketelitian pembacaan rambu | 0,01 ft langsung (foot rod); 0,01 m + mm taksiran (metrik), dibukukan per 1/2 atau 1/3 cm | `SOURCE-DERIVED` | `[R3, Kavanagh, PDF 46]` (folio 33) |
| Besarnya pergeseran antar-datum | "up to tens of meters"; NAD27 -> NAD83(1986) "tens to hundreds of meters" | `SOURCE-DERIVED` (besaran order-of-magnitude, **bukan angka proyek lokal**) | `[R3, Bolstad, PDF 112, 116]` |
| Toleransi posisi yang diminta proyek GSP (tiang kamera, jalur kabel, beda tinggi) | **ASSUMPTION sampai pemberi kerja menetapkan** | `ASSUMPTION` - wajib sensitivitas (½x dan 2x) + rencana penggantian | tidak ada di rak; Kavanagh eksplisit: toleransi ditetapkan pemberi kerja/kontrak `[R3, berkas rak Surveying, baris 40-41]` |

**Aturan yang membatalkan hitungan bila dilanggar:** jangan menyerahkan koreksi traversi tanpa
menyatakan rasio **pra-koreksi** dan **pasca**-koreksi. Koreksi meratakan galat ke semua kursus;
tanpa rasio pra-koreksi, pembaca tidak dapat melihat apakah galatnya acak atau satu kursus salah
ukur - buku sendiri memerintahkan memeriksa **arah** galat penutup terhadap bearing kursus lebih
dulu `[R3, Kavanagh, PDF 180]`.

---

## ④ Pengujian - ⚠ MATA TANPA AMBANG SAH

Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak (`ASSURANCE-WORKFLOW.md`); R3 hanya
sah bila kontrak mengadopsinya tertulis, dan kolom register kedua buku berbunyi
`no-unless-contract-adopts` `[R3, register induk baris 36-37]`.

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Arithmetic check leveling | Σ BS - Σ FS = Δ elevasi, **tepat** | ✅ metode R3 `[R3, Kavanagh, PDF 54]` - ini syarat perlu, bukan syarat cukup |
| Penutup loop leveling | Misclosure <= ambang kelas yang **dinyatakan kontrak** | ❌ ambang tidak ada di rak; bentuknya `0,008√K` m untuk second-order class II `[R3, Kavanagh, PDF 65]` - **kutipan R3 atas standar FGCS yang tidak ada** |
| Verifikasi BM awal | Two-way leveling ke BM bersebelahan atau GNSS presisi sebelum loop dimulai | Metode R3 `[R3, Kavanagh, PDF 65]`; ambang = kontrak |
| Kelengkapan catatan lapangan | TP teridentifikasi, dapat dideskripsikan, mampu dibaca ke 0,01 ft / 0,001 m; rambu pada titik yang sama untuk BS dan FS | `[R3, Kavanagh, PDF 66]` (folio 53) - kriteria ada, **angka lulus tidak** |
| Precision ratio traversi | >= rasio yang ditetapkan pemberi kerja | ❌ **tidak dapat divonis dari rak**; rentang praktik buku 1/3.000-1/10.000 `[R3, Kavanagh, PDF 180, 470]` |
| Konsistensi penyesuaian | Σ koreksi = error; Σ lat/dep pasca-koreksi = 0,00 | ✅ sah sebagai uji intern metode `[R3, Kavanagh, PDF 182-184]` |
| Kesesuaian datum/proyeksi antar berkas | Semua berkas satu datum + epoch + proyeksi, dinyatakan eksplisit | Aturan R3 `[R3, Bolstad, PDF 103]`; **ambang deviasi = kontrak** |
| Ketelitian alat | Sesuai lembar data model yang dipakai, kalibrasi masih berlaku pada tanggal uji | **`[R4]`** - satu-satunya jalur sah; angka buku `[R3, Kavanagh, PDF 45]` bukan penggantinya |
| Bukti hasil ukur sebagai lampiran serah | Rekaman mentah + kondisi + alat + penyaksi | Gerbang **G5** (kartu REF-GEO-002 bagian 4) - bukan soal tingkat |
| Survei as-built dalam paket serah | Gambar terbangun + penjelasan setiap perbedaan vs rancangan | Gerbang **G6**; `09_HANDOVER/AS-BUILT/README.md` - aturan map: perbedaan wajib dijelaskan |
| **Kelas ketelitian resmi Indonesia (SRGI2013 + turunnannya)** | ❌ **tidak dapat diuji dari rak** | Standarnya tidak ada, gap_id-nya belum ada (butir 3) |

### Celah yang dibukukan (bukan dikarang)

1. **Tidak ada satu pun sandaran R1/R2 di domain ini.** Ukur 11-10-2026:
   `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` = 103 baris data dengan tepat **4 baris R1/R2**
   dan keempatnya domain lain; `GAP-REGISTER.csv` = 22 baris dengan **0 baris** menyebut
   GEOSPATIAL-SURVEY atau SRGI; `AMBANG-TERIMA-INDUK.md` (116 baris) = **0 butir** soal survei,
   datum, traverse, atau toleransi posisi (satu-satunya jejak token "survei" di berkas itu ada di
   dalam path `VIDEO-SURVEILLANCE`, bukan sebagai butir).
2. **Angka toleransi terbaik di rak ini adalah pinjaman berkonteks asing.** `0,008√K`,
   1/5.000-1/7.500, dan RPA ALTA/ACSM semuanya angka **Amerika Serikat** yang masuk lewat buku
   teks: sumber primernya (FGCS 1988, ALTA/ACSM 2005) disebut di `[R3, Kavanagh, PDF 180, 321]`
   tetapi tidak ada di rak. Memakainya sebagai ambang terima = memakai R3 sebagai R2 sekaligus
   mengimpor konteks hukum yang salah. Preseden yang sama tercatat untuk CIVIL-STRUCTURAL
   (`GAP-015..018`: "Hibbeler [R3] memakai ASCE 7 Amerika - angka bebannya berbeda").
3. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK ini):
   **SRGI2013 / peraturan geodesi Indonesia (BIG) + kelas ketelitian survei yang mengikat
   kontrak**. Klaim "tidak ada di rak" sudah dinyatakan kedua resume sejak 21-08-2026
   `[R3, berkas rak GIS Fundamentals, baris 44; berkas rak Surveying, baris 43-44]` dan
   dikonfirmasi lajur L1/L3, tetapi **tidak pernah punya gap_id** - ukur hari ini:
   `GAP-REGISTER.csv` 0 sebutan. Akibatnya seluruh vonis terima hasil ukur pihak ketiga berjalan
   tanpa sandaran.
4. **Usulan butir GAP kedua:** salinan berlapis teks bersih untuk `REF-GEO-001`. Berkas resume
   mengklaim kebutuhan ini "tercatat sebagai kebutuhan pada GAP-REGISTER"; sudah dikoreksi
   11-10-2026 oleh KOREKSI-RR3A-1 sebagai **tidak terdaftar** `[R3, berkas rak GIS Fundamentals,
   baris 58-63]`. Rantai ini mengonfirmasi ulang: 0 sebutan GIS/Bolstad di `GAP-REGISTER.csv`.
5. **Bentuk jawaban yang sah hari ini** saat ambang ketelitian survei diminta: nyatakan "tidak ada
   di rak ini; sumber yang seharusnya: R1/R2 kelas ketelitian survei Indonesia (SRGI2013 dan
   turunannya) atau pasal kontrak yang menetapkan rasio/misclosure", lalu mintakan angka itu ke
   pemilik pekerjaan. Yang boleh diserahkan sekarang: **metode + hasil ukur + rasio tercapai**,
   tanpa pernyataan "lulus" - pola yang sama dipakai rantai D untuk resistansi pembumian
   (`AMBANG-TERIMA-INDUK.md` bagian "Belum ada sumber sah", tiga jalan sah).

### Yang boleh dan tidak boleh dikatakan

| ✅ Boleh | ❌ Tidak boleh |
|---|---|
| *"Leveling dilaksanakan dengan BS/FS seimbang, sights >= 0,5 m, loop ditutup ke BM awal, dan arithmetic check terpenuhi [R3, Kavanagh, PDF 41, 54, 65, 67]; ambang misclosure mengikuti pasal kontrak No. ..." * | ~~"Misclosure 0,017 m jadi lulus"~~ tanpa menyebut kelas dan sumber ambangnya |
| *"Traversi ditutup dengan precision ratio 1/4.200 (pra-koreksi), disesuaikan dengan Compass rule; koreksi total 0,06/0,49 terhadap P 2.081,19 [R3, Kavanagh, PDF 180-184]."* | ~~"Traversi memenuhi standar"~~ bila tidak ada standar yang diadopsi kontrak |
| *"Seluruh berkas dalam datum/epoch/proyeksi tunggal yang dinyatakan; konversi antar-datum memakai transformasi yang disebut [R3, Bolstad, PDF 103]. Datum Indonesia (SRGI2013) mengikat bila kontrak menyebutnya."* | ~~"Peta sudah WGS84 jadi aman"~~ - WGS84 vs SRGI2013 bukan soal nama datum saja, tapi epoch dan realisasi |

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Pernyataan datum + epoch + proyeksi + satuan yang dipakai | ✅ | Titik paling sering hilang; akibatnya geser puluhan meter tak terlihat `[R3, Bolstad, PDF 112, 116]` |
| Catatan kelas ketelitian yang dituntut pekerjaan (order/kelas atau rasio) beserta **sumber angkanya** (pasal kontrak / pemilik pekerjaan) | ✅ | Bila belum ada: tulis "belum ada di rak" - jangan biarkan kosong tanpa keterangan |
| Buku ukur lapangan (field notes) mentah + *arithmetic check* | ✅ | Bentuk minimum: Gambar 2-15 `[R3, Kavanagh, PDF 54]`; gerbang G5 menuntut bukti mentah, bukan ringkasan |
| Perhitungan traversi: Σ lat/dep, E, precision ratio **pra- dan pasca**-koreksi, tabel koreksi | ✅ | Padanan bentuknya: Tabel 6-4 `[R3, Kavanagh, PDF 184]` |
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Status sah tertulis "menunggu R4" untuk angka alat |
| Lembar data alat (total station / level digital / GNSS) + tanggal terbitnya | ✅ **`[R4]`** | Satu-satunya sumber sah angka ketelitian alat; preseden GAP-014 (dokumentasi OEM diminta per proyek) |
| Sertifikat/record **kalibrasi masih berlaku pada tanggal uji** | ✅ | G5 gagal bila kalibrasi kedaluwarsa saat pengukuran (`ASSURANCE-GATES.md` bagian G5) |
| Daftar titik tetap (BM/TBM/TP) dengan elevasi terpasang + identitas deskriptif | ✅ | Kriteria TP: describable, identifiable `[R3, Kavanagh, PDF 66]` |
| **Survei as-built + daftar perbedaan terhadap gambar rancangan** | ✅ | Gerbang G6; `[R3, Kavanagh, PDF 455, 466]`; aturan map `09_HANDOVER/AS-BUILT/README.md` |
| Hasil pemeriksaan hasil ukur pihak ketiga (bila ada) | ✅ | Cara kerjanya dari Kavanagh `[R3, berkas rak Surveying, baris 11, 31-33]` |
| Daftar asumsi terbuka + daftar butir menunggu data OEM `[R4]` | ✅ | Dua baris yang paling sering hilang di G6 (`ASSURANCE-GATES.md`) |
| Catatan alat & versi perangkat lunak pengumpul/olah data | ✅ | Tanpa ini angka tidak dapat direproduksi; cermin ketertelusuran `TPL-06-P00-KETERTELUSURAN.md` |

**Keterbatasan kerangka yang ada:** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi, baterai, genset,
video, termal, penyimpanan) dan **tidak punya bagian untuk uji survei/geodesi** (kata "survei" di
berkas itu hanya muncul pada seksi pembumian Wenner, ukur 11-10-2026); pakai "Rangka umum -
berlaku untuk semua jenis" (bagian 1) plus tabel Ringkasan sumber ambang-nya, dan nyatakan bahwa
jenis uji survei belum punya template khusus.

**Cara mata ⑤ ini menutup rantai K.** Rantai K (CIVIL-STRUCTURAL) menggantungkan baris
"Verifikasi dimensi & tegak-lurus" pada survei `[R3, CIVIL-STRUCTURAL/RANTAI-JAMINAN.md baris 107]`.
Sejak berkas ini ada, gantungan itu punya alamat: bukti dimensi/ketegakan masuk sebagai lampiran
rantai ini (baris buku ukur + as-built di atas), dengan ambang tetap milik kontrak.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun; setiap angka bertanda `[R-n]` dengan
halaman yang dibuka ulang terhadap vault hari ini, dan **setiap contoh numerik dihitung ulang
oleh parser pada run ini** (tujuh baris Tabel 2-3, satu precision ratio, sepuluh sel Tabel 6-4,
satu rangkaian arithmetic check - semuanya cocok). Mata ④ jujur tanpa ambang: yang ada di rak
adalah metode dan **pinjaman angka standar Amerika Serikat**, bukan kriteria yang dapat dipakai
menvonis.

**Kapan rantai ini boleh disebut utuh:** setelah (a) kelas ketelitian survei Indonesia punya
sandaran R1/R2 di rak (SRGI2013 dan turunannya) atau kontrak mengadopsi angka tertentu secara
tertulis, (b) insan menandatangani unit `KEMAMPUAN.md` domain ini (2/2 masih
`draft-tidak-terverifikasi-insan`), dan (c) resume `REF-GEO-001` punya salinan berlapis teks
bersih sehingga jangkarnya dapat dibuka dengan cara normal.

**Batas konteks yang menempel pada seluruh berkas ini.** Kedua buku berkonteks Amerika Utara:
Kavanagh memakai State Plane/UTM dan standar FGCS/NGS/ALTA; Bolstad membahas NAD27/NAD83/NAVD88.
Rentang rasio dan nilai `0,008√K` di atas sahih sebagai **bukti bahwa metode ini bekerja dengan
kelas**, bukan sebagai angka yang dapat ditagih di Indonesia `[R3, berkas rak GIS Fundamentals,
baris 44; berkas rak Surveying, baris 43-44]`.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_9b7ace41. Berkas-berkas berikut bukan milik LOCK ini sehingga
tidak disunting.

1. **Edisi Bolstad tidak tercatat di lapisan mana pun, dan tahunnya 2022 (edisi ke-7).**
   Laci vault berisi `GIS Fundamentals_ A first text on Geographic information systems (2022)`,
   halaman hak cipta menulis *7th Edition*, "First printing April 2022" (terukur: teksnya rusak
   menjadi "Copyright (c) 1022"). Kepala resume hanya menulis "Paul Bolstad & Steven Manson"
   tanpa edisi/tahun; kartu `REF-GEO-001` juga tidak. Pemilik: berkas resume + kartu (jalur
   RESUME-R3/kurator).
2. **Jangkar `KEMAMPUAN-REGISTER.csv` baris KM-0117 meleset 11 halaman di ujung awal.** Register
   menulis `Surveying ... 9e [pdf hal. 158-184]` untuk *Traverse Closure & Compass Rule
   Adjustment*; PDF 158 (folio 145) berisi bab 5 *Total Stations and Theodolites* (ATR, 360°
   prism, remote positioning unit) - bukan traversi. Bab 6 *Traverse Surveys* mulai **PDF 169**,
   *error of closure* pertama **PDF 172**, Compass rule **PDF 182**, Tabel 6-4 **PDF 184**.
   Rentang yang benar 169-184. Pemilik: digest mesin `KEMAMPUAN-REGISTER.csv` / jalur W4
   (`w4_chains.py`) - mediasi controller.
3. **Register menyebut edisi "9e" untuk Kavanagh sementara kepala resume hanya "2014".** Edisi
   kesembilan terkonfirmasi dari halaman depan vault ("...the ninth edition text review"), jadi
   register benar dan resume tidak lengkap - bukan konflik, tetapi format kepala tidak seragam
   dengan domain lain yang mencantumkan edisi. Pemilik: berkas resume.
4. **Penunjuk "rantai L" di CIVIL-STRUCTURAL kabur.** `CIVIL-STRUCTURAL/RANTAI-JAMINAN.md:107`
   menunjuk "Survei - rantai L" untuk verifikasi dimensi & ketegakan, sedangkan huruf L sudah
   dipakai `BUILDING-CONSTRUCTION/RANTAI-JAMINAN.md` ("Rantai L - Batasan bangunan tempat
   perangkat dipasang"). Lajur L1 sudah mencatat penelusuran ini (23-09-2026) tanpa kesimpulan.
   Yang dimaksud adalah rantai survei - kini rantai ini. Rantai K bukan milik LOCK ini, jadi
   penunjuknya tidak diubah di sini.
5. **KATALOG-RUMUS.md tidak punya seksi survei** (ukur 11-10-2026: `traverse`/`leveling`/`datum`
   = 0 hitung pada 613 baris) padahal empat rumus tertambat-halaman tersedia di mata ③ berkas
   ini. Pengisian katalog bukan wewenang LOCK ini - usulan ke pemilik katalog (langkah 28).
6. **Kebutuhan salinan bersih `REF-GEO-001` masih tanpa gap_id** walau sudah dikoreksi oleh
   KOREKSI-RR3A-1 di berkas resume. Ukur hari ini: 0 sebutan GIS/Bolstad di
   `GAP-REGISTER.csv`. Pemilik: penulis register GAP (langkah 25-26).
7. **Tabrakan huruf rantai belum dialokasikan controller** (lihat kepala berkas ini). Rantai
   berjalan sampai R; MECHANICAL memakai "W" ad-hoc; dua kartu saudara memakai "S" dan "T".
   Duplikasi huruf "M" antara CONSTRUCTION dan PROJECT-QUALITY sudah terjadi lebih dulu (ukur
   11-10-2026) - penamaan rantai perlu registri tunggal, bukan kebiasaan lokal. Pemilik:
   controller/TA.
