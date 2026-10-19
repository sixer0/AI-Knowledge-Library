# Rantai O - Pengolahan dan analisis citra sebagai dasar fungsi analitik video

## RANTAI BERANTAI PARSIAL TERBIMBING (sejak 11-10-2026, kartu t_7bee8b1e)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan R3 yang ada di rak ini** (dua resume
ber-halaman + KEMAMPUAN.md domain), dengan setiap jangkar yang dipakai di bawah dibuka
ulang langsung terhadap PDF vault pada run kartu ini. Mata ④ **tetap tanpa ambang terima**:
tidak ada satu pun baris R1/R2 untuk domain ini, jadi angka lulus/tidak-lulus **tidak
dapat** ditetapkan dari sini dan celahnya dibukukan apa adanya di mata ④ bawah.

**Daya-ikat tidak naik.** Seluruh rujukan domain ini tetap `pending_verification` (P-5) dan
kolom kontraknya `no-unless-contract-adopts` di `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
(ukur 11-10-2026: baris fisik 72-73, satu-satunya dua baris ber-domain COMPUTER-VISION dari
103 baris data register). Susunan mata ②-⑤ ini **menyiapkan**, insan yang menandatangani;
tidak ada baris register yang disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode geometri dan
pengolahan citra, contoh terhitung, dan cara membuktikan sebuah pipeline**. Bila sebuah
pekerjaan menuntut ambang terima analitik video (akurasi deteksi, lalu alarm palsu, galat
kalibrasi), ambangnya milik **kontrak** atau standar R1/R2 yang belum ada di rak; lihat
mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, sudah dibuka) |
|---|---|---|---|
| `REF-CVI-001` - Digital Image Processing 4e, Gonzalez & Woods (Pearson 2018) | **R3** ⏳pending | Pra-pemrosesan intensitas, histogram, filter spasial (rata/median), morfologi, segmentasi ambang (Otsu), DFT 2-D. | `[R3, Gonzalez-Woods DIP, PDF 48]` (peta langkah bab 1), `[PDF 66]` (akuisisi), `[PDF 74]` (sampling-kuantisasi), `[PDF 173, 177]` (transformasi power-law/gamma), `[PDF 189, 195]` (histogram processing; Contoh 3.5), `[PDF 225]` (dasar filter spasial), `[PDF 239]` (lowpass), `[PDF 252]` (median/order-statistic), `[PDF 296]` (bab 4 mulai), `[PDF 346]` (sifat DFT 2-D), `[PDF 807]` (erosi-dilatasi), `[PDF 876]` (§10.2 titik-garis-tepi; badan Sobel `[PDF 899-900]`), `[PDF 928, 933-935]` (ambang global; metode Otsu) |
| `REF-CVI-002` - Multiple View Geometry 2e, Hartley & Zisserman (Cambridge 2003) | **R3** ⏳pending | Model kamera pinhole (matriks K), DLT homografi, geometri epipolar (F, E), triangulasi linear. | `[R3, Hartley-Zisserman MVG, PDF 106]` (DLT + batas 4 korespondensi), `[PDF 111]` (ketunggalan homografi + dualitas), `[PDF 170-171]` (Part 3 + bab 6 proyeksi sentral, matriks K), `[PDF 257]` (bab 9 epipolar, matriks F), `[PDF 275]` (§9.6 matriks esensial), `[PDF 330]` (§12.2 triangulasi linear) |

> Semua baris: R3 buku teks/handbook, `pending_verification` - sah untuk **metode dan
> penalaran**, tidak sah sebagai ambang terima (lihat kartu `04_KNOWLEDGE-CARDS/
> COMPUTER-VISION/REF-CVI-001.md` dan `REF-CVI-002.md` bagian 3 dan 4).

**Konversi halaman (terpakai saat membaca rujukan):** DIP tidak seragam (bab 1: cetak 1 =
PDF 23; §3.3: cetak 168 = PDF 189 -> +21; §3.4: cetak 185 = PDF 225 -> +40; ada sisipan
halaman depan/figure) sehingga seluruh rujukan DIP memakai **nomor PDF**. MVG seragam
+17..+18 (folio 88 terukur di PDF 106 pada run ini). Konvensi dua-peran berlaku: nomor peta
bab bukan jangkar kutipan kalimat.

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** kolom "sudah
dibuka" di tabel ① berarti halaman PDF-nya dibuka ulang dengan `pdftotext -layout` (Xpdf
4.06) pada run kartu ini - DIP 48, 66, 74, 173, 175, 177, 189, 191-196, 209, 225, 239, 252,
264-266, 269, 296, 346, 440, 807, 876-881, 899-900, 928, 930-935 dan MVG 2-7, 106, 111,
170-171, 252-257, 275-284, 319-330. Tidak ada jangkar yang diwarisi tanpa dibuka: butir
resume yang tidak terkonfirmasi di sini **tidak** dikutip sebagai jangkar (lihat catatan
silang-pemilik). Sebagian halaman DIP mengandung byte NUL akibat cacat font CID yang sudah
dicatat di kepala resume; teks halaman yang dikutip di berkas ini terbaca bersih setelah
strip NUL.

**Edisi aktual berkas vault (ukur 11-10-2026):** MVG - *Second Edition* tercetak di PDF 2,
penerbit Cambridge University Press (PDF 3); cocok dengan klaim resume. DIP - halaman
katalog dalam PDF 5: `LCC TA1632 .G66 2018`, `ISBN 9780133356724`, situs pearsonhighered;
string "Fourth Edition" **tidak** ditemukan lewat pdftotext (kemungkinan bagian lapisan
font CID yang rusak - cacat ekstraksi yang sudah tercatat di kepala resume), jadi edisi
keempat **tercatat sebagai klaim resume yang belum tersangga teks lapisan ini**; tahun
2018 tersangga data katalog. Bukti byte kedua berkas diverifikasi ulang hari ini: sha256[:16]
`c0183a88e02f8395` (DIP) dan `7ba0104075b51152` (MVG) - **cocok** dengan kartu REF.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian, yang wajib
tertulis adalah pilihan + alternatif yang ditolak + alasannya
(`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`, tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Model kamera kerja: **proyeksi sentral (pinhole)** dengan parameter intrinsik dibundel dalam matriks K 3x3 | Semua kamera yang memodelkan proyeksi sentral adalah spesialisasi bentuk ini `[R3, Hartley-Zisserman MVG, PDF 171]`; K 3x3 `[R3, MVG, PDF 170]` | Model distorsi lensa dipasang sejak awal - ditolak: intrinsik ideal dan distorsi dipisahkan; angka distorsi milik lembar data pabrikan (R4) yang belum ada di rak untuk kamera proyek |
| Relasi dua-pandang: **estimasi F lebih dulu** (kasus tak-terkalibrasi); E hanya setelah kalibrasi | F mengemas geometri projektif intrinsik antara dua view `[R3, MVG, PDF 257]`; E adalah spesialisasi F untuk kasus terkalibrasi `[R3, MVG, PDF 275]` | Estimasi E langsung - ditolak: E menuntut intrinsik diketahui; memakai E tanpa K hasil kalibrasi menghasilkan angka yang salah secara diam-diam |
| Homografi bidang: **DLT linear dari >= 4 korespondensi titik general position** | "necessary to specify four point correspondences in order to constrain H fully" `[R3, MVG, PDF 106]`; dualitas 3 garis + 1 titik setara 4 titik `[R3, MVG, PDF 111]` | Kurang dari 4 titik - under-constrained secara teoretis, bukan sekadar buruk: batas minimumnya struktural. Least-squares biasa tanpa bentuk homogen - bentuk bilinear `x'ᵀHx = 0` `[R3, MVG, PDF 106]` memang dirancang agar solusinya linear |
| Titik 3D dari dua view: **triangulasi linear dua-sinar (mid-point)** sebagai taksiran awal | Metode triangulasi linear §12.2, projective-invariant karena hanya jarak citra yang dipakai `[R3, MVG, PDF 330]` | Langsung ke penajaman non-linear tanpa taksiran awal - bundle adjustment iteratif dan konvergensi optimumnya tidak terjamin dari sembarang titik awal (peringatan pemakaian di resume MVG §2, butir `[tanpa-jangkar]`) |
| Urutan pra-pemrosesan mengikuti **peta langkah fundamental** (enhancement -> restoration -> ... -> segmentasi -> representasi -> deskripsi -> pengenalan) | Peta bab 1 `[R3, Gonzalez-Woods DIP, PDF 48]` | Melompat langsung ke segmentasi pada frame mentah - setiap langkah sesudahnya punya prasyarat keluaran langkah sebelumnya; peta itu justru yang membuat kegagalan bisa dilokalisasi |
| Penajaman kontras sebelum ambang: **equalisasi histogram** bila sebaran intensitas sempit | Transformasi `s = T(r)` monotonik `[R3, DIP, PDF 191-196]`; mekanika Contoh 3.5 `[R3, DIP, PDF 195]` | Ambang pada citra asal berkontras rendah - pemisahan mode histogram tidak tercapai, Otsu memilih T dari sebaran yang belum berarti `[R3, DIP, PDF 928]` |
| Filter derau: **median (order-statistic)** untuk derau impuls/garam-merica; **lowpass rata** untuk pelemahan transisi tajam umum | Median menggantikan piksel pusat dengan median tetangga `[R3, DIP, PDF 252]`; lowpass mereduksi transisi tajam intensitas `[R3, DIP, PDF 239]` | Mean filter untuk derau impuls - ditolak: rata menyebarkan piksel impuls ke tetangganya alih-alih menghapusnya; ranking memisahkan nilai ekstrem dari isi statistik |
| Segmentasi ambang: **Otsu global** bila histogram bimodus; ambang tetap manual hanya dengan analisis sensitivitas tertulis | Otsu memilih T yang memaksimumkan variansi antar-kelas `[R3, DIP, PDF 933-935]`; iluminasi tak seragam menuntut ambang variabel `[R3, DIP, PDF 930]` | T konstan hasil intuisi operator tanpa dasar - bila histogram tidak bimodus, Otsu sendiri sudah peringatan bahwa premis separabilitasnya gagal `[R3, DIP, PDF 935]` |
| Masker hasil segmentasi dibersihkan dengan **morfologi** (erosi/dilatasi, buka/tutup) sebelum pengukuran | Erosi dan dilatasi fundamental bagi pemrosesan morfologi `[R3, DIP, PDF 807]` | Menyerahkan mask mentah ke tahap pengukuran/penghitungan - lubang dan sambatan derau mengubah besaran ukur; operasi ini murah dan deterministik |
| Penapisan domain-frekuensi **hanya bila signature periodik terlihat di spectrum** | Bab 4 dimulai PDF 296; sifat DFT/IDFT 2-D `[R3, DIP, PDF 346]` | Kernel spasial besar untuk derau periodik - signature periodik justru terpisahkan di domain frekuensi; di spasial ia melumer tanpa memilih |
| Batas domain dengan VIDEO-SURVEILLANCE: **kerapatan piksel (FI 250 / FR 125 pix/m) adalah masukan VSS, bukan ambang analitik CV** | Baris kerapatan piksel di `AMBANG-TERIMA-INDUK.md` bersandar Damjanovski + sasaran pemilik (domain VSS) | Memakai ambang VSS sebagai vonis lulus fungsi analitik - objek ukurnya berbeda: VSS mengukur kecukupan citra, analitik CV mengukur keputusan mesin atas citra itu |

> Keputusan yang paling menentukan mutu hasil analitik di domain ini: **rantai pra-pemrosesan
> dibekukan urutannya sebelum ambang mana pun dipilih** (model kamera -> kalibrasi ->
> penajaman -> derau -> segmentasi -> morfologi). Ia mengalir ke mata ③ sebagai rumus
> bertanda dan ke mata ④ sebagai dasar klaim apa yang sebenarnya diuji.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini (resume + KEMAMPUAN.md), **bukan** di
`06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`: katalog tidak punya seksi computer-vision
sama sekali (ukur 11-10-2026, `grep -ci "homografi|homography|otsu|median filter|epipolar|
pinhole"` pada `KATALOG-RUMUS.md` = 0). Butir lintas-lapis ini dicatat di kaki berkas
sebagai celah; pengisian KATALOG bukan wewenang LOCK ini.

### Geometri (MVG)

```
x' ~ K [R|t] x~          proyeksi pinhole: titik dunia -> titik citra
x'ᵀ H x = 0              kendala homografi bidang (bentuk bilinear DLT)
x'ᵀ F x = 0              kendala epipolar dua view (self-check korespondensi)
```

| Bentuk | Sumber | Status buka |
|---|---|---|
| Matriks K dan proyeksi sentral | `[R3, MVG, PDF 170-171]` | dibuka ulang run ini |
| DLT homografi + batas 4 korespondensi | `[R3, MVG, PDF 106]` | dibuka ulang run ini |
| Kendala epipolar F | `[R3, MVG, PDF 257]` | dibuka ulang run ini |
| Triangulasi dua-sinar mid-point | `[R3, MVG, PDF 330]` | dibuka ulang run ini |
| Kedalaman stereo terrektifikasi `Z = fB/d` | **tidak dibekukan di sini** | Nama rumus dan anggarannya diwarisi dari [`KEMAMPUAN.md`](KEMAMPUAN.md) baris K-0273/CV-006 yang menambatkan ke "MVG pdf hal. 275"; halaman 275 yang dibuka ulang berisi §9.6 matriks esensial, **bukan** relasi disparitas-kedalaman (lihat CATATAN SILANG-PEMILIK butir 3). Bahan disparitas tampak di sekitar PDF 319-326 tetapi badan rumusnya belum dibaca ulang sampai tuntas oleh kartu ini - jangan dikutip sebagai jangkar sebelum pemilik register mengoreksi |

### Pengolahan citra (DIP) - contoh terhitung (diukur ulang 11-10-2026, bukan disalin)

| Besaran | Aturan | Contoh | Rehitung run ini | Tag |
|---|---|---|---|---|
| Median 3x3 | nilai terbesar ke-5 dari 9 tetangga (5x5: ke-13) `[R3, DIP, PDF 252]` | (10,20,20,20,15,20,20,25,100) | terurut (10,15,20,20,20,20,20,25,100) -> median **20** - COCOK dengan lapisan W10 | `SOURCE-DERIVED` |
| Equalisasi histogram diskret | `s = T(r)` dengan `T(r_k) = (L-1) Σ CDF` `[R3, DIP, PDF 191-196]` | Contoh 3.5: citra 3-bit, 64x64 | L = 2^3 = **8** level; n = 64x64 = **4096** piksel - COCOK dengan jangkar W9B `[R3, DIP, PDF 195]` | `SOURCE-DERIVED` |
| Ambang Otsu | pilih k yang memaksimumkan variansi antar-kelas `[R3, DIP, PDF 934-935]` | - | **tidak ada angka tetap**: T adalah fungsi histogram citra itu sendiri; yang membeku metodenya, bukan nilainya | metode `SOURCE-DERIVED`; nilai per-citra `PROJECT-DERIVED` |
| Morfologi erosi/dilatasi | pasangan operasi dual pada himpunan piksel objek `[R3, DIP, PDF 807]` | - | deterministik per SE (structuring element); ukuran SE = keputusan proyek | metode `SOURCE-DERIVED`; SE `ASSUMPTION` (wajib sensitivitas + rencana penggantian) |

| Masukan yang selalu milik proyek (bukan rak) | Tag | Catatan |
|---|---|---|
| Ukuran kernel/grid uji, resolusi citra, jarak kamera ke bidang objek | `PROJECT-DERIVED` | Angka contoh buku (3-bit, 64x64) ilustrasi pedagogis, **bukan** ambang |
| Nilai T ambang, ukuran SE, batas inlier epipolar | `ASSUMPTION` | Wajib sensitivitas dua skenario (½x dan 2x) + rencana penggantian data |

> **Aturan yang membatalkan perhitungan bila dilanggar:** seluruh unit kemampuan domain ini
> (CV-001..CV-015, `KEMAMPUAN.md`) berjenis `calculator` dengan uji grid kecil - artinya
> keluarannya sah diverifikasi **manual per kasus** (kotak 3x3 dapat dihitung tangan). Hasil
> pipeline yang tidak dapat direplikasi pada grid kecil curigai sebagai bug implementasi,
> bukan "keberhasilan skala besar".

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara membuktikan sebuah pipeline citra. Yang TIDAK bisa
dinyatakan: ambang terima.** Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak
(`ASSURANCE-WORKFLOW.md`); R3 hanya sah bila kontrak mengadopsinya tertulis, dan kolom
`may_set_acceptance` kedua baris CV di register induk berbunyi `no-unless-contract-adopts`.

Uji intern metode (sah dijalankan, hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Cek deterministik grid kecil | Setiap unit calculator CV-001..CV-015 punya uji grid mini yang dapat dihitung tangan (median, equalisasi, DLT 4 titik, erosi/dilatasi) | [`KEMAMPUAN.md`](KEMAMPUAN.md) kolom `uji` = 5-7 per unit; metode `[R3, DIP, PDF 252, 195, 807]` + `[R3, MVG, PDF 106]`; **plafon selisih lulus = angka proyek, tidak ada di rak** |
| Kendala epipolar sebagai self-check korespondensi | Hitung `x'ᵀ F x` atas pasangan korespondensi; residual besar = padanan salah | `[R3, MVG, PDF 257]` - sah sebagai uji konsistensi; **batas inlier (mis. ambang piksel/derajat) tidak ada di rak** |
| Pembanding dua metode | DLT linear vs penajaman iteratif; triangulasi linear vs bundle - laporkan selisihnya | kerangka estimasi `[R3, MVG, PDF 106, 330]`; peringatan konvergensi bundle dari resume §2 `[tanpa-jangkar]`; **selisih maksimum antar-metode = angka proyek** |
| Kalibrasi ground-truth sintetis | Grid titik dengan koordinat dunia diketahui -> proyeksikan -> bandingkan K/R/t hasil estimasi dengan truth | metode komposisi pinhole `[R3, MVG, PDF 170-171]`; **toleransi reproduksi titik = belum ada di rak** |
| Sanity segmentasi berpasangan | Otsu + morfologi menghasilkan mask yang stabil terhadap sensitivitas ½x/2x parameter | `[R3, DIP, PDF 933-935, 807]`; stabilitas dilaporkan sebagai rentang, bukan lulus/gagal |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima analitik citra di rak ini.** Ukur 11-10-2026:
   `MASTER-REFERENCE-REGISTER.csv` = 103 baris data dengan **0 baris R1**; keempat baris R2
   yang ada (IEEE 1188/IEC 62485-2, ANSI-NETA ATS-2017, IEC 61280-4-2, BS EN 62676-1-2)
   semuanya domain lain; `GAP-REGISTER.csv` (23 baris) = 0 sebutan computer-vision/citra;
   `AMBANG-TERIMA-INDUK.md` tidak punya butir analitik CV (baris video yang ada milik domain
   VIDEO-SURVEILLANCE: kerapatan piksel dan deteksi hilang sinyal, bukan keputusan mesin).
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK
   ini): ambang terima fungsi analitik video (laju deteksi benar, alarm palsu/salah lewat,
   akurasi kalibrasi geometris, galat reproyeksi) tidak memiliki sandaran R1/R2. Yang
   seharusnya masuk rak: protokol evaluasi kinerja analitik dari badan uji (kelas
   evaluasi publik seperti program NIST untuk pengenalan wajah), atau dokumen kesesuaian
   analitik antarprodusen (jalur CVON/ONVIF - dan catatan rak sendiri sudah menyatakan
   ONVIF tidak ada di rak, baris "Interoperabilitas perangkat video" di
   `AMBANG-TERIMA-INDUK.md`), atau adopsi tertulis R3 oleh kontrak proyek.
3. **Bentuk jawaban yang sah hari ini** saat ambang analitik diminta: nyatakan "tidak ada
   di rak ini; sumber yang seharusnya: protokol evaluasi badan uji atau pasal adopsi R3
   dalam kontrak", lalu mintakan angka itu ke pemilik pekerjaan - **jangan** mengambil
   angka contoh buku (median 20; 4096 piksel; L=8) sebagai ambang, dan **jangan** memakai
   ambang kerapatan piksel VSS (FI 250 / FR 125) sebagai vonis fungsi analitik.

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan yang memakai analitik citra = bukti bahwa **setiap angka dan
setiap keputusan punya jalur ①->④**, termasuk citra yang menjadi bahan keputusan.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Bentuk minimum di `ASSURANCE-WORKFLOW.md` bagian "Kartu kendali rantai"; status kartu sah bila tertulis "menunggu R4" |
| Lembar perhitungan `TPL-02` dengan tag per masukan | ✅ | Tiap masukan bertanda `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`; tiap `ASSUMPTION` punya sensitivitas + rencana penggantian (gerbang G3, `ASSURANCE-GATES.md` syarat 1-4) |
| **Pemeriksaan orang kedua** | ✅ | G3 tidak tertutup tanpa ini (syarat 4 gerbang G3) |
| Citra bahan uji + konfigurasi kamera (K hasil kalibrasi, resolusi, jarak bidang objek) | ✅ | Tanpa bahan uji yang direkam, keputusan mesin tidak dapat direproduksi; simpan di `08_EVIDENCE/` |
| Versi alat dan skrip (interpreter, pustaka CV, seed bila acak, versi berkas kalibrasi) | ✅ | Tanpa ini hasil tidak dapat direproduksi; `09_HANDOVER/TPL-06-P00-KETERTELUSURAN.md` sebagai cermin ketertelusuran |
| Jejak uji intern (tabel residual epipolar, selisih dua metode, hasil grid kecil) | ✅ | Bentuknya per tabel mata ④; laporkan angka, bukan kesimpulan rasa |
| Penyataan asal ambang (mata ④) | ✅ | Bila ambang dari kontrak: sebut pasalnya; bila belum ada: tulis "belum ada di rak" - jangan biarkan kosong tanpa keterangan |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi; ini titik di mana celah mata ④ paling sering tersamar |

**Keterbatasan kerangka yang ada:** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi, baterai,
genset, video, termal, penyimpanan) dan **tidak punya bagian untuk uji kinerja analitik
citra**; bagian "6. Uji terima sistem video" mengukur kerapatan piksel dan transmisi
(domain VSS), bukan keputusan mesin atas citra. Pakai "Rangka umum - berlaku untuk semua
jenis" (bagian 1 berkas itu) plus tabel Ringkasan sumber ambang-nya, dan nyatakan bahwa
jenis uji analitik CV belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dan setiap angkanya bertanda `[R-n]`
dengan halaman yang sudah dibuka ulang terhadap vault. Mata ④ **jujur kosong untuk ambang**:
rak ini memasok metode geometri dan pemrosesan citra beserta cara membuktikannya, tetapi
ambang terima kinerja analitik menuntut R1/R2 atau adopsi kontrak yang belum ada.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier W3 menaikkan daya-ikat resume
dari `pending_verification`, (b) insan menandatangani unit [`KEMAMPUAN.md`](KEMAMPUAN.md) domain ini
(ukur 11-10-2026: 15/15 baris CV di `KEMAMPUAN-REGISTER.csv` masih `draft` dengan
sign-off `draft-tidak-terverifikasi-insan`), dan (c) ambang terima analitik punya sandaran
R1/R2 atau adopsi kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_7bee8b1e. Semua butir terukur langsung dari berkas vault
(Xpdf pdftotext 4.06) atau berkas lapisan; berkas-berkas itu bukan milik LOCK ini sehingga
**tidak disunting**.

1. **Peta bab DIP menambat bab 4 ke PDF 269; salah.** `R3 - Digital Image Processing
   (Gonzalez & Woods).md` §1 menulis bab 4 "Filtering in the Frequency Domain" pada
   `[PDF 269]`; PDF 269 masih berisi Contoh 3.23 (penapisan spasial, bab 3). Bab 4 mulai di
   **PDF 296** (heading "4 Filtering in the Frequency Domain" terukur). Berkas ini memakai
   PDF 296.
2. **Butir resume "Histogram processing (equalization) - PDF 209" meleset.** PDF 209 berisi
   seksi "Exact Histogram Matching (Specification)"; equalisasi sendiri terbaca di
   **PDF 191-196** (heading "Histogram Equalization" di PDF 191, Contoh 3.5 di PDF 195).
   Berkas ini mengutip rentang yang benar.
3. **Jangkar [`KEMAMPUAN.md`](KEMAMPUAN.md) CV-006 "Rectified Stereo Depth (Z = fB/d)" ke MVG pdf hal. 275
   salah sasaran.** PDF 275 = §9.6 "The essential matrix". Material disparitas/rektifikasi
   MVG berada di sekitar PDF 319-326 (bab 11), dan sumber padanan yang dicatat register
   untuk unit yang sama adalah Szeliski [pdf hal. 615] yang tidak terverifikasi di sini
   (lihat butir 4). Rumus `Z = fB/d` **tidak dibekukan** di mata ③ sampai pemilik register
   mengoreksi jangkarnya.
4. **Szeliski 2e dikutip sebagai sumber 4 unit CV tetapi tidak punya baris register.**
   [`KEMAMPUAN.md`](KEMAMPUAN.md)/`KEMAMPUAN-REGISTER.csv` menyebut "Computer Vision: Algorithms and
   Applications 2e - Szeliski (2022, Springer)" pada CV-002, CV-004, CV-007; berkas PDF-nya
   nyata ada di laci vault `R3_TEXTBOOK-HANDBOOK/CCTV-VSS/` (27.834.637 B, terukur), tetapi
   `MASTER-REFERENCE-REGISTER.csv` = 0 baris Szeliski. Kutipan ke sumber tak-terdaftar ini
   tidak boleh naik ke dokumen serah sebelum diinkas register.
5. **Edisi DIP "keempat" belum tersangga teks lapisan.** String "Fourth Edition" tidak
   ditemukan di seluruh ekstraksi pdftotext (1307 halaman) - konsisten dengan cacat font
   CID yang dicatat kepala resume; data katalog dalam (PDF 5) menyangga 2018/Pearson.
   Pemilik resume perlu memverifikasi edisi lewat tampilan visual halaman hak cipta.
6. **Lapisan sekitar menyinggung banner lama.** [`README.md`](README.md) domain dan kedua kartu
   `REF-CVI-00x.md` bagian 5 masih menulis "masih berbanner belum berantai penuh"; sejak
   hari ini banner rantai berubah menjadi "berantai parsial terbimbing" sesuai klausul
   langkah 10. Berkas-berkas itu di luar LOCK; sinkronisasi milik controller/owner.

Butir 1-2 menyentuh berkas resume W3a (milik jalur BUKUV3); butir 3-4 menyentuh
[`KEMAMPUAN.md`](KEMAMPUAN.md)/`KEMAMPUAN-REGISTER.csv` (digest mesin); butir 5 menyentuh kepala resume
DIP; butir 6 menyentuh README domain + kartu REF. Mediasi lewat controller (M2).
