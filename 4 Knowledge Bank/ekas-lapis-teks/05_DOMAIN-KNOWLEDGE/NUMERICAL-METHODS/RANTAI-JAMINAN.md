# Rantai R - Metode numerik sebagai mesin hitung domain lain

## RANTAI BERANTAI PARSIAL TERBIMBING (sejak 11-10-2026, kartu t_fda23cbb)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan R3 yang ada di rak ini** (dua resume
ber-halaman + KEMAMPUAN.md domain). Mata ④ **tetap tanpa ambang terima**: tidak ada satu pun
baris R1/R2 untuk domain ini, jadi angka lulus/tidak-lulus **tidak dapat** ditetapkan dari
sini dan celahnya dibukukan apa adanya di mata ④ bawah.

**Daya-ikat tidak naik.** Seluruh rujukan domain ini tetap `pending_verification` (P-5) dan
kolom kontraknya `no-unless-contract-adopts` di `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
(ukur 11-10-2026: baris 92-93). Susunan mata ②-⑤ ini **menyiapkan**, insan yang
menandatangani; tidak ada baris register yang disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode, anggaran galat, dan
cara membuktikan hitungan**. Bila sebuah pekerjaan menuntut ambang numerik yang mengikat
(mis. toleransi konvergensi hasil hitungan yang masuk dokumen serah), ambangnya milik
**kontrak** atau standar R1/R2 yang belum ada di rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, sudah dibuka) |
|---|---|---|---|
| `REF-NUM-001` - Applied Numerical Methods with MATLAB, Chapra | **R3** ⏳pending | Anggaran iterasi bisection, bracketing, kondisi matriks, regresi kalibrasi, ODE. | `[R3, Chapra ANM, PDF 153]` (badan aturan), `[PDF 155]` (peta bab 5), `[PDF 167]` (Eq. 5.6), `[PDF 169]` (contoh false position), `[PDF 305]` (bab 11) |
| `REF-NUM-002` - Numerical Methods for Engineers, Chapra & Canale | **R3** ⏳pending | Angka berarti dan pelaporan galat, propagasi galat + condition number, bisection/false position, Newton-Raphson, Brent, golden-section. | `[R3, Chapra-Canale NME, PDF 77]`, `[PDF 79]`, `[PDF 121]`, `[PDF 146]`, `[PDF 151]`, `[PDF 154]`, `[PDF 170]`, `[PDF 181]`, `[PDF 380]`, `[PDF 382]` |

> Semua baris: R3 buku teks/handbook, `pending_verification` - sah untuk **metode dan
> penalaran**, tidak sah sebagai ambang terima (lihat kartu `04_KNOWLEDGE-CARDS/
> NUMERICAL-METHODS/REF-NUM-001.md` bagian 3 dan 4).

**Konversi halaman (terpakai saat membaca rujukan):** ANM = cetak + 17; NME = cetak + 18.
Dua-duanya dicocokkan ulang 11-10-2026 terhadap folio halaman yang dikutip di berkas ini
(NME PDF 77 -> folio 59, PDF 121 -> 103, PDF 151 -> 133, PDF 382 -> 364; ANM PDF 167 -> 150,
PDF 169 -> 152). Konvensi dua-peran per KOREKSI-W11B berlaku: nomor peta bab bukan jangkar
kutipan kalimat.

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** kolom "sudah
dibuka" di tabel ① berarti halaman PDF-nya dibuka ulang dengan `pdftotext -layout` (Xpdf
4.06) pada run kartu ini - NME 77, 79, 121, 146, 151, 153(badan 5.2.3), 154, 170, 181, 380,
382 dan ANM 167, 169, 305. Dua jangkar ANM **diwarisi dari verifikasi W11(b)** (kartu
t_3a7f8a60, catatan KOREKSI-W11B di berkas resume) dan tidak dibuka ulang di sini:
`[R3, Chapra ANM, PDF 153]` (badan aturan bracketing) dan `[PDF 155]` (peta bab 5).

**Edisi aktual berkas vault (ukur 11-10-2026, halaman hak cipta kedua PDF):** ANM =
*Fourth Edition*, copyright 2018; NME = *Eighth Edition*, McGraw-Hill Education [2021],
ISBN 978-1-260-23207-3. Kepala kedua berkas resume menuliskan edisi/tahun yang berbeda
(lihat CATATAN SILANG-PEMILIK di kaki berkas ini; berkas resume bukan milik LOCK ini, jadi
tidak disunting di sini).

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian, yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`,
tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Kelas metode akar: **bracketing** bila yang ditagih adalah jaminan konvergensi; **open** bila yang ditagih kecepatan dan turunan tersedia | Bisection menjamin konvergensi selama akar terbracket, lajunya linear `[R3, Chapra-Canale NME, PDF 146, 151]`; Newton-Raphson cepat tetapi bergantung tebakan awal dan turunan `[R3, Chapra-Canale NME, PDF 170]` | Newton-Raphson telanjang ditolak untuk hitungan yang masuk dokumen serah - gagal senyap bila tebakan awal buruk atau turunan hilang; bisection murni ditolak bila jumlah evaluasi fungsi mahal - laju linear memboroskan evaluasi |
| **Brent** sebagai pilihan baku bila keduanya dituntut (andal tanpa turunan, secepat open methods) | Gabungan bracketing + interpolasi `[R3, Chapra-Canale NME, PDF 181]`; unit `NUM-007` Root Finding Orchestrator (Bracket + Polish) `KEMAMPUAN.md` | False position murni ditolak sebagai default - konvergensinya bisa melambat parah pada selang cekung (diskusi efisiensi di `[R3, Chapra-Canale NME, PDF 154]`) |
| **Anggaran iterasi dihitung sebelum iterasi jalan** (bukan dihentikan seadanya) | "Error formulations are developed to help you determine how much computational effort is required to estimate the root to a prespecified level of precision" `[R3, Chapra ANM, PDF 153]`; Eq. (5.5) NME `[R3, Chapra-Canale NME, PDF 151]`, Eq. (5.6) ANM `[R3, Chapra ANM, PDF 167]` | Berhenti karena batas iterasi pustaka (default) ditolak - default pustaka bukan angka proyek dan tidak dapat dipertanggungjawabkan di mata ④ |
| **Toleransi berhenti diturunkan dari presisi keluaran yang dibutuhkan**, bukan dari mesin | Formulasi galat menentukan beban komputasi `[R3, Chapra ANM, PDF 153]`; peringatan implementasi: galat pembulatan menenggelamkan metode bila toleransi terlalu kecil (resume NME bagian 2, butir `[tanpa-jangkar]`) | Toleransi sekecil-kecilnya ditolak - melampaui digit pasti masukan hanya menambah galat pembulatan dan biaya |
| **Digit pasti masukan = plafon digit yang dilaporkan** | Angka berarti = digit pasti + satu digit taksiran `[R3, Chapra-Canale NME, PDF 77]`; definisi galat relatif Eq. (3.1)-(3.3) `[R3, Chapra-Canale NME, PDF 79]` | Menyalin seluruh digit keluaran kalkulator ke tabel serah ditolak - menyatakan ketelitian yang tidak dimiliki masukan |
| **Condition number diperiksa sebelum hasil sistem linear diterima** | Condition number = rasio galat relatif keluaran/masukan, Eq. (4.28); nilai 1 tidak memperbesar ketidakpastian, nilai > 1 memperbesar (ill-conditioned) `[R3, Chapra-Canale NME, PDF 121]`; kerangka bab 11 ANM `[R3, Chapra ANM, PDF 305]` | Menyerahkan solusi linear tanpa ukuran kondisi ditolak - sistem yang ill-conditioned menghasilkan angka yang sah secara aritmetika tetapi tidak bermakna rekayasa |
| Optimasi 1-D: **golden-section** untuk fungsi unimodal | Rasio emas R = 0,61803 Eq. (13.6) `[R3, Chapra-Canale NME, PDF 380]`; setiap putaran memangkas selang ~61,8%, 10 putaran tersisa 0,008 (0,8%) `[R3, Chapra-Canale NME, PDF 382]` | Grid/sweep padat ditolak untuk 1-D unimodal - biaya evaluasi lebih besar untuk ketelitian yang sama; metode turunan ditolak bila turunan tidak analitik |
| Cara membuktikan solver itu sendiri: **MMS + dual-method + observed order** | `NUM-017` Manufactured Solutions, `NUM-010` Linear Solver with Dual-Method Verification, `NUM-019` Observed Order & Richardson - angka halamannya diwarisi dari `KEMAMPUAN.md` (register menulis "pdf hal." tanpa menyebut folio) dan **belum dibuka ulang ke vault oleh kartu ini** | Percaya satu kali jalan tanpa solusi pembanding ditolak - bug implementasi tidak tampak sebagai galat numerik, ia tampak sebagai hasil yang rapi |

> Keputusan yang paling menentukan mutu hasil hitungan di domain ini: **anggaran galat
> dinyatakan sebelum menghitung** (toleransi + digit pasti masukan + besaran kondisi). Ia
> mengalir ke mata ③ sebagai masukan bertanda dan ke mata ④ sebagai dasar klaim.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini, **bukan** di `06_ENGINEERING/CALCULATIONS/
KATALOG-RUMUS.md`: katalog tidak punya seksi numerik sama sekali (ukur 11-10-2026,
`grep -ci "chapra|numerik|numerical"` pada `KATALOG-RUMUS.md` = 0). Butir lintas-lapis ini
dicatat di kaki berkas sebagai celah; pengisian KATALOG bukan wewenang LOCK ini.

### Anggaran iterasi bisection (yang paling sering dibutuhkan pekerjaan)

```
Ea^n = x0 / 2^n                    (batas galat absolut setelah n iterasi)
n    = log(x0 / Ea,d) / log 2      (iterasi yang dibutuhkan untuk target Ea,d)
```

| Bentuk | Sumber |
|---|---|
| `Ea = x0/2^n` Eq. (5.4) dan `n = log2(x0/Ea,d)` Eq. (5.5) | `[R3, Chapra-Canale NME, PDF 151]` (cetak 133) |
| Eq. (5.6) bentuk ANM, `n = log2(Delta x0 / Ea,d)` | `[R3, Chapra ANM, PDF 167]` (cetak 150) |

| Masukan | Nilai contoh | Tag | Sumber |
|---|---|---|---|
| Lebar selang awal `x0` | 150 (mis. 200 - 50) | `PROJECT-DERIVED` | uji buku `[R3, Chapra ANM, PDF 167]` |
| Target galat absolut `Ea,d` | 0,5859 | `ASSUMPTION` (kebutuhan proyek, bukan angka rak) | nilai contoh buku `[R3, Chapra ANM, PDF 167]` |
| Laju pemangkasan per iterasi | 1/2 (tepat) | `SOURCE-DERIVED` | `[R3, Chapra-Canale NME, PDF 151]` |

### Contoh terhitung (diukur ulang 11-10-2026, bukan disalin dari laporan pihak lain)

```
n = log2(150 / 0,5859) = 8,0001  ->  8 iterasi   (cocok dengan hasil buku: n = 8)
sisa selang setelah 8 iterasi = 150 / 2^8 = 0,5859
```

Sensitivitas terhadap target galat (aturan asumsi: dua skenario 1/2x dan 2x):

| Skenario | `Ea,d` | `n` | Dibulatkan |
|---|---|---|---|
| Target buku | 0,5859 | 8,0001 | 8 iterasi |
| 1/2x (lebih ketat) | 0,29295 | 9,0001 | 10 iterasi |
| 2x (lebih longgar) | 1,1718 | 7,0001 | 8 iterasi |

Pesan yang mengikat rancangan: **mengetatkan toleransi dua kali lipat hanya menambah dua
iterasi** pada bisection (laju tetap), jadi anggaran komputasi domain ini hampir selalu
determined oleh pemilihan metode, bukan oleh ketelitian target.

### Pembanding terukur lain yang tersedia di lapisan

| Besaran | Nilai | Sumber | Catatan pemakaian |
|---|---|---|---|
| Rasio emas `R` | 0,61803 | `[R3, Chapra-Canale NME, PDF 380]` Eq. (13.6) | Pemangkasan selang per putaran golden-section |
| Sisa selang setelah 10 putaran | 0,618^10 = 0,008 (0,8%) | `[R3, Chapra-Canale NME, PDF 382]` | Ukur ulang: 0,00813 |
| Contoh false position (ANM) | `m = 142,74 kg`, 21 iterasi, `ea = 5,345e-005`, `fx = 4,6089e-007` | `[R3, Chapra ANM, PDF 169]` (cetak 152) | Ilustrasi jejak konvergensi yang harus dilampirkan, **bukan** ambang |
| Condition number | rasio galat relatif keluaran/masukan; 1 = netral | `[R3, Chapra-Canale NME, PDF 121]` Eq. (4.28) | Ambang "kapan dianggap ill-conditioned" TIDAK ada di rak - milik proyek/kontrak |

> **Aturan yang membatalkan hitungan bila dilanggar:** jangan menuntut toleransi hasil lebih
> ketat daripada digit pasti masukan. Galat pembulatan menenggelamkan metode bila toleransi
> terlalu kecil (resume NME bagian 2, butir `tanpa-jangkar`); digit pasti = digit pasti +
> satu digit taksiran `[R3, Chapra-Canale NME, PDF 77]`.

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara membuktikan sebuah hitungan. Yang TIDAK bisa
dinyatakan: ambang terima.** Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak
(`ASSURANCE-WORKFLOW.md`); R3 hanya sah bila kontrak mengadopsinya tertulis, dan kolom
register kedua buku ini berbunyi `no-unless-contract-adopts`.

Uji intern metode (sah dijalankan, hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Solusi pembanding | Jalankan dua metode berbeda atas kasus yang sama (mis. bisection vs Brent; Gauss vs LU) - `NUM-010`, `NUM-007` | metode R3 `[R3, Chapra-Canale NME, PDF 267, 301]` - **diwarisi dari `KEMAMPUAN.md`, belum dibuka ulang ke vault oleh kartu ini**; **selisih maksimum antar-metode = angka proyek, tidak ada di rak** |
| Manufactured Solution | Ganti solusi dengan fungsi yang diketahui, turunkan residual yang diharapkan - `NUM-017` | metode R3 + praktik (`KEMAMPUAN.md` baris K-0017, sumber kedua `-` kosong); **plafon residual lulus = belum ada di rak** |
| Orde teramati | Hitung orde konvergensi dari dua penajaman grid; bandingkan dengan orde teori - `NUM-019` | `[R3, Chapra-Canale NME, PDF 75, 85, 101, 117, 122]` - **rentang diwarisi dari `KEMAMPUAN.md`; hanya PDF 101-122 sebagian terbuka (PDF 113, 121 dibuka kartu ini), PDF 75/85 belum**; **toleransi cocok-tidak-cocok = belum ada di rak** |
| Anggaran iterasi | Jumlah iterasi nyata <= `n` hasil mata ③ | `[R3, Chapra ANM, PDF 167]` - sah sebagai uji konsistensi, bukan ambang mutu |
| Pelaporan galat | Setiap hasil disertai `Et`/`ea` terdefinisi Eq. (3.1)-(3.3) | `[R3, Chapra-Canale NME, PDF 79]` |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima numerik di rak ini.** Ukur 11-10-2026: `MASTER-REFERENCE-REGISTER.csv`
   = 0 baris R1/R2 ber-domain NUMERICAL-METHODS (seluruh R1/R2 di rak hanyalah 4 baris:
   IEEE 1188/IEC 62485-2, ANSI-NETA ATS-2017, IEC 61280-4-2, BS EN 62676-1-2 - semuanya domain
   lain); `GAP-REGISTER.csv` = 0 baris menyebut numerical-methods;
   `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` = 0 butir numerik.
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK ini):
   ambang terima hasil hitungan numerik (toleransi residual, selisih antar-metode, deviasi
   orde teramati) tidak memiliki sandaran R1/R2. Yang seharusnya masuk rak: standar verifikasi
   dan validasi model/simulasi, atau adopsi tertulis R3 oleh kontrak proyek.
3. **Bentuk jawaban yang sah hari ini** saat ambang numerik diminta: nyatakan "tidak ada di
   rak ini; sumber yang seharusnya: R1/R2 verifikasi-validasi model atau pasal adopsi R3 dalam
   kontrak", lalu mintakan angka itu ke pemilik pekerjaan - **jangan** mengambil nilai contoh
   buku (0,5859; 5,345e-005; 0,008) sebagai ambang. Angka-angka itu ilustrasi pedagogis
   (ditegaskan kedua resume bagian 4: "bukan ambang kontrak").

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan yang dihitung secara numerik = bukti bahwa **setiap angka punya
jalur ①->④**, bukan hanya hasil akhirnya.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Bentuk minimum di `ASSURANCE-WORKFLOW.md` bagian "Kartu kendali rantai"; status kartu sah bila tertulis "menunggu R4" |
| Lembar perhitungan `TPL-02` dengan tag per masukan | ✅ | Tiap masukan bertanda `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`; tiap `ASSUMPTION` punya sensitivitas + rencana penggantian (gerbang G3, `ASSURANCE-GATES.md:52-58`) |
| **Pemeriksaan orang kedua** | ✅ | G3 tidak tertutup tanpa ini. Preseden jujur di rak: `CALC-P00-001.md` masih tertulis "belum diperiksa orang kedua" - contoh itu sendiri belum lewat G3 |
| Jejak konvergensi run (jumlah iterasi, residual akhir, toleransi yang dipakai) | ✅ | Padanan bentuknya: tabel iterasi `[R3, Chapra ANM, PDF 169]`; simpan di `08_EVIDENCE/SCREENSHOTS-LOGS/` |
| Versi alat dan skrip (interpreter, pustaka, seed bila acak) | ✅ | Tanpa ini hasil tidak dapat direproduksi; `09_HANDOVER/TPL-06-P00-KETERTELUSURAN.md` sebagai cermin ketertelusuran |
| Catatan kondisi matriks / kestabilan bila ada sistem linear | ✅ | Condition number `[R3, Chapra-Canale NME, PDF 121]` |
| Penyataan asal ambang (mata ④) | ✅ | Bila ambang berasal dari kontrak: sebut pasalnya; bila belum ada: tulis "belum ada di rak" - jangan biarkan kosong tanpa keterangan |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi; ini titik di mana celah mata ④ paling sering tersamar |

**Keterbatasan kerangka yang ada:** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi, baterai,
genset, video, termal, penyimpanan) dan **tidak punya bagian untuk hitungan numerik**;
pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas itu) plus tabel Ringkasan
sumber ambang-nya, dan nyatakan bahwa jenis uji numerik belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dan setiap angkanya bertanda `[R-n]`
dengan halaman yang sudah dibuka ulang terhadap vault. Mata ④ **jujur kosong untuk ambang**:
domain ini adalah mesin hitung bagi domain lain, jadi ambang terimanya ikut ambang domain
yang dilayani (serat, baterai, termal, dst.) atau menuntut standar verifikasi-validasi yang
belum ada di rak.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier W3 menaikkan daya-ikat resume
dari `pending_verification`, (b) insan menandatangani unit `KEMAMPUAN.md` domain ini
(ukur 11-10-2026: 372/372 unit register masih `draft-tidak-terverifikasi-insan`, termasuk
28/28 baris domain ini), dan (c) ambang terima numerik punya sandaran R1/R2 atau adopsi
kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_fda23cbb. Ketiga butir di bawah terukur langsung dari berkas
vault dan berkas hulu; berkas-berkas itu bukan milik LOCK ini sehingga **tidak disunting**.

1. **Edisi NME salah di kepala resume.** `R3 - Numerical Methods for Engineers (Chapra &
   Canale).md` menulis "Edisi: ketujuh ... 2020"; halaman hak cipta berkas vault menulis
   *EIGHTH EDITION*, [2021], ISBN 978-1-260-23207-3. `KEMAMPUAN.md` menyebutnya "9e" pada 4
   baris. Tiga klaim berbeda untuk satu berkas.
2. **Edisi ANM salah di kepala resume.** `R3 - Applied Numerical Methods with MATLAB
   (Chapra).md` menulis "Edisi: ketiga ... 2017"; hak cipta vault menulis *Fourth Edition*,
   copyright 2018 (edisi sebelumnya 2012, 2008).
3. **Jangkar "definisi formal galat relatif/persentase" meleset.** Resume NME bagian 2
   menambatkan butir itu ke `[R3, Chapra-Canale NME, PDF 113]`; PDF 113 (cetak 95) berisi
   seksi Deret Taylor dan sama sekali tidak memuat definisi galat. Definisi Eq. (3.1)-(3.3)
   ada di **PDF 79 (cetak 61)**. Berkas ini mengutip PDF 79.
4. **Penamaan nomor persamaan lintas-edisi.** `KEMAMPUAN.md` baris K-0008 menyebut
   `Ea = abs(x_u - x_l)/2^n` sebagai "Pers. 5.4" di PDF 151 - benar untuk NME; sedangkan
   formulasi jumlah iterasi di halaman yang sama bernomor **(5.5)**, dan padanannya di ANM
   bernomor **(5.6)** (PDF 167). Rujukan silang antar-lapis perlu menyebut buku agar nomor
   tidak tertukar.

Butir 1-3 menyangkut berkas yang disentuh W11(b)/W9B/W10 (BUKUV3-JURY) - jalur mediasi
controller ke profil pemilik; butir 4 menyentuh `KEMAMPUAN.md` (digest mesin, sumber
`KEMAMPUAN-REGISTER.csv`).
