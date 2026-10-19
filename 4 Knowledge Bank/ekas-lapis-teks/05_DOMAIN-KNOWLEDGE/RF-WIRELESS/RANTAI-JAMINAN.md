# Rantai N - Komunikasi radio dan gelombang mikro untuk tautan nirkabel sistem terpasang

## RANTAI BERANTAI PARSIAL TERBIMBING (sejak 11-10-2026, kartu t_4bb6e4ef)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan R3 yang ada di rak ini** (tiga resume
ber-halaman W3a + `KEMAMPUAN.md` domain + tambalan W9B/W10). Mata ④ **tetap tanpa ambang
terima**: tidak ada satu pun baris R1/R2 untuk domain ini, jadi angka lulus/tidak-lulus
**tidak dapat** ditetapkan dari sini dan celahnya dibukukan apa adanya di mata ④ bawah.

**Daya-ikat tidak naik.** Seluruh rujukan domain ini tetap `pending_verification` (P-5) dan
kolom kontraknya `no-unless-contract-adopts` di `02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`
(ukur 11-10-2026: baris 95-97, tiga barisnya saja, semuanya R3). Susunan mata ②-⑤ ini
**menyiapkan**, insan yang menandatangani; tidak ada baris register yang disunting oleh
berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode, rumus, dan cara
membuktikan hitungan tautan**. Ambang mutu layanan radio (SNR minimum, BER target, peluang
padam, margin fade, kepatuhan spektrum) milik **kontrak** atau standar R1/R2 (lembaga
spektrum/ETSI/IEEE) yang **belum ada di rak**; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, sudah dibuka) |
|---|---|---|---|
| `REF-RFW-001` - Wireless Communications, Goldsmith (2005, Cambridge) | **R3** ⏳pending | Model rugi lintasan: definisi path loss, free-space, dua-slope, shadowing log-normal, peluang padam, kapasitas kanal, SNR/BER, adaptasi modulasi. | `[R3, Goldsmith WC, PDF 60]` (definisi PL, Eq. 2.4-2.5), `[PDF 61]` (free-space Eq. 2.7-2.9), `[PDF 76]` (Tabel 2.2 eksponen tipikal), `[PDF 68]` (difraksi pisau-edana Fresnel), `[PDF 81]` (sek. 2.9 outage + Contoh 2.5), `[PDF 129]` (Shannon Eq. 4.1), `[PDF 130]` (contoh kapasitas), `[PDF 201]` (definisi SNR, PSD N0/2), `[PDF 202]` (probabilitas galat BPSK/QPSK), `[PDF 318]` (MQAM adaptif) |
| `REF-RFW-002` - Antenna Theory, Balanis edisi 4 (2016, Wiley) | **R3** ⏳pending | Parameter fundamental antena: HPBW/FNBW, directivity, efisiensi dan gain, polarisasi, persamaan transmisi Friis, dipol λ/2. | `[R3, Balanis Antenna, PDF 62]` (definisi HPBW IEEE), `[PDF 63]` (D0 = 4Umax/Prad, Eq. 2-16a), `[PDF 73]` (tabel bandingan Kraus vs Tai-Pereira), `[PDF 83]` (gain/realized gain, Γ masukan), `[PDF 110]` (persamaan Friis, sek. 2.17), `[PDF 198]` (dipol λ/2, Rr = 73 ohm) |
| `REF-RFW-003` - Microwave Engineering, Pozar edisi 4 (2012, Wiley) | **R3** ⏳pending | Teori garis transmisi dan analisis jaringan: Smith chart, SWR, return loss, transformer seperempat gelombang, pencocokan L/stub, filter. | `[R3, Pozar MW, PDF 68]` (bab 2 terbuka), `[PDF 78]` (RL Eq. 2.38; SWR Eq. 2.41), `[PDF 95]` (identitas pencocokan, diwarisi dari tambalan W10), `[PDF 267]` (Eq. 5.25, running head `5.4 The Quarter-Wave Transformer 247`) |

> Semua baris: R3 buku teks/handbook, `pending_verification` - sah untuk **metode dan
> penalaran**, tidak sah sebagai ambang terima (lihat kartu `04_KNOWLEDGE-CARDS/RF-WIRELESS/
> REF-RFW-001.md` bagian 3 dan 4, berlaku sama untuk 002/003).

**Konversi halaman (terpakai saat membaca rujukan):** Goldsmith = cetak + 29; Balanis =
cetak + 22; Pozar = cetak + 20. Ketiganya dicocokkan ulang 11-10-2026 terhadap folio
halaman yang dikutip di berkas ini (Goldsmith PDF 61 -> folio 32, PDF 81 -> 52; Balanis
PDF 110 -> 88, PDF 198 -> 176; Pozar PDF 78 -> 58, PDF 267 -> 247 running head).

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** kolom "sudah
dibuka" di tabel ① berarti halaman PDF-nya dibuka ulang dengan `pdftotext -layout` (Xpdf
4.06) pada run kartu ini - Goldsmith 59, 60, 61, 68, 76, 81, 128, 129, 130, 201, 202, 318;
Balanis 62, 63, 73, 83, 110, 198; Pozar 68, 78, 267. Untuk butir yang ditemukan lewat
pencocokan baris pada dump teks penuh (Goldsmith 68, 76, 318; Balanis 73; Pozar 78 SWR),
nomor halamannya ditetapkan dari hitungan batas halaman form-feed dump - metode tercatat.
Satu jangkar **diwarisi dari tambalan W10** dan tidak dibuka ulang di sini:
`[R3, Pozar MW, PDF 95]` (identitas Pers. 2.63).

**Edisi aktual berkas vault (cek 11-10-2026, halaman hak cipta PDF):** Pozar = *Fourth
Edition*, copyright 2012 (cocok dengan kepala resume); Balanis = *FOURTH EDITION* (cocok).
Halaman hak cipta Goldsmith tidak terbaca pada dump halaman awal - tahun 2005 diikuti judul
berkas laci; tidak ada selisih yang terukur, jadi tidak ada yang dikoreksi.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian, yang wajib
tertulis adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/
ASSURANCE-WORKFLOW.md`, tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Model propagasi tautan LOS titik-titik: **free-space path loss** sebagai lantai, margin ditambah eksplisit | PL = Pt/Pr, turun kuadrat jarak dan panjang gelombang `[R3, Goldsmith WC, PDF 60]`-`[PDF 61]` Eq. (2.4)-(2.9) | Eksponen tunggal untuk seluruh rentang jarak ditolak - model dua-slope (konstanta K, n1 sampai dc lalu n2, Tabel 2.2 `[R3, Goldsmith WC, PDF 76]`) menunjukkan eksponen berubah setelah jarak patah; memakai satu n di luar rentang sahnya = salah taksir sistematis |
| Rintangan pada jalur LOS: **difraksi pisau-edana Fresnel** sebagai pemeriksaan first-order | Model pisau-edana + parameter Fresnel-Kirchhoff `[R3, Goldsmith WC, PDF 68]` | Analisis medan penuh per kasus ditolak untuk pekerjaan rutin - biaya tinggi, sementara rugi difraksi umumnya dapat dijaring dengan margin + pengecekan zona; radius zona Fresnel itu sendiri belum bertambat halaman di rak (lihat celah C-3 mata ④) |
| Variabilitas daya terima: **shadowing log-normal di atas path loss**, desain terhadap **peluang padam**, bukan terhadap daya rata-rata | Outage Pout(Pmin, d) gabungan path loss + shadowing `[R3, Goldsmith WC, PDF 81]` (sek. 2.9) | Mendesain pada nilai rata-rata ditolak - rata-rata menyembunyikan ekor bawah distribusi; sigma log-normal **harus dari survei lokasi (proyek)**, bukan dari nilai contoh buku (3,65 dB di resume hanyalah latihan, ditegaskan "bukan ambang") |
| Pemilihan antena: **gain + beamwidth + polarisasi dibaca bersama pola**, bukan angka gain tunggal | Definisi HPBW IEEE `[R3, Balanis Antenna, PDF 62]`; D0 `[R3, Balanis Antenna, PDF 63]`; gain vs directivity lewat efisiensi radiasi `[R3, Balanis Antenna, PDF 83]` | Memakai "gain maksimum" katalog tanpa pola/polarisasi ditolak - tautan titik-titik menilai arah, bukan puncak; directivity aproksimasi (Kraus/Tai-Pereira) hanya sah untuk pola yang memenuhi asumsinya, bandingannya tercetak di `[R3, Balanis Antenna, PDF 73]` |
| Pencocokan feeder: **kuarter-wave transformer hanya untuk beban resistif**; beban kompleks dicocokkan dulu (L-network/stub) | Z1 = sqrt(Z0 ZL) Eq. (5.25) `[R3, Pozar MW, PDF 267]`; keterbatasan resistif + prasyarat lambda0/4 pada f0 `[R3, Pozar MW, PDF 95]` (diwarisi W10) | Mencocokkan beban kompleks langsung dengan seksi tunggal ditolak - metode tidak terdefinisi untuk itu; solusi manual Pozar tidak ada di vault, jadi tidak ada jalan pintas jawaban |
| Pelaporan kualitas pencocokan: **return loss dan SWR** sebagai pasangan angka | RL = -20 log abs(Gamma) dB Eq. (2.38); match = tak hingga dB, refleksi total = 0 dB; SWR Eq. (2.41) `[R3, Pozar MW, PDF 78]` | Melaporkan hanya "VSWR bagus" tanpa angka ditolak - tidak dapat diaudit di mata ④/⑤ |
| Feed tautan umum: **dipol λ/2** dipilih bila impedansi 73 ohm cukup dekat dengan garis 50/75 ohm | Rr = 73 ohm, pencocokan ke garis 50/75 ohm tersederhana pada resonansi `[R3, Balanis Antenna, PDF 198]` | Antena khusus (patch, array) ditolak **tanpa kebutuhan** - desainnya menuntut lapisan yang belum terverifikasi (patch/array hanya jangkar `KEMAMPUAN.md`, halamannya belum dibuka ulang kartu ini) |
| Uji kelayakan laju data: **batas Shannon sebagai langit-langit**, bukan target | C = B log2(1 + SNR) Eq. (4.1) `[R3, Goldsmith WC, PDF 129]`; teorema pengkodean = laju mendekati C dengan galat negligible, di atas C mustahil `[R3, Goldsmith WC, PDF 128]`–`[PDF 129]` | Menjanjikan throughput di atas C, atau memakai C sebagai angka kinerja nyata sistem, ditolak - C mengandaikan pengkodean tak terbatas kompleksitasnya; MQAM adaptif `[R3, Goldsmith WC, PDF 318]` memberi metode penyesuaian laju, tetap sebagai metode |

> Keputusan yang paling menentukan mutu rancangan tautan di domain ini: **daya terima
> dirancang terhadap distribusi (outage), bukan rata-rata, dan setiap margin dinyatakan
> asal angkanya** (rumus R3, masukan proyek, asumsi, atau datasheet R4). Ia mengalir ke
> mata ③ sebagai masukan bertanda dan ke mata ④ sebagai dasar klaim.

---

## ③ Perhitungan

Rumus-rumus di bawah hidup di lapisan ini, **bukan** di `06_ENGINEERING/CALCULATIONS/
KATALOG-RUMUS.md`: katalog tidak punya satu pun baris rf-wireless (ukur 11-10-2026,
`grep -ci "goldsmith|pozar|balanis|path loss|link budget|friis|antena"` pada
`KATALOG-RUMUS.md` = 0). Butir lintas-lapis ini dicatat di kaki berkas sebagai celah;
pengisian KATALOG bukan wewenang LOCK ini.

### Rugi lintasan ruang bebas (yang paling sering dibutuhkan pekerjaan)

```
PL_linier = (4 pi d / lambda)^2                    (rasio Pt/Pr, isotropik)
PL_dB     = 10 log10 (4 pi d / lambda)^2
```

| Bentuk | Sumber |
|---|---|
| Definisi PL = Pt/Pr dan bentuk dB, Eq. (2.4)-(2.5) | `[R3, Goldsmith WC, PDF 60]` (cetak 31) |
| Pr/Pt = (Gl/4pi d)^2 dan free-space path loss Eq. (2.7)-(2.9) | `[R3, Goldsmith WC, PDF 61]` (cetak 32) |

| Masukan | Nilai contoh | Tag | Sumber |
|---|---|---|---|
| Frekuensi | 2,44 GHz (lambda = 0,12295 m) | `ASSUMPTION` (ilustrasi; frekuensi kerja milik proyek) | - |
| Jarak | 1.000 m | `PROJECT-DERIVED` (yang menentukan proyek) | - |
| Pola antena | isotropik (Gl = 1) | `ASSUMPTION` | penyederhanaan model `[R3, Goldsmith WC, PDF 61]` |

### Contoh terhitung (diukur ulang 11-10-2026 dengan python, bukan disalin dari laporan pihak lain)

```
PL(2,44 GHz, 1 km)  = 10 log10 (4 pi * 1000 / 0,12295)^2 = 100,19 dB
PL(900 MHz, 5 km)   = 10 log10 (4 pi * 5000 / 0,33333)^2 = 105,51 dB
```

Sensitivitas terhadap jarak (aturan asumsi: dua skenario 1/2x dan 2x, hukum kuadrat balik):

| Skenario | PL(2,44 GHz) | Selisih |
|---|---|---|
| Jarak buku contoh 1 km | 100,19 dB | - |
| 1/2x (500 m) | 94,17 dB | -6,02 dB |
| 2x (2 km) | 106,21 dB | +6,02 dB |

Pesan yang mengikat rancangan: **setelah dua kali jarak, rugi bertambah tepat 6 dB** -
margin fade yang lebih kecil dari itu tidak bertahan terhadap perubahan tata letak tapak.

### Persamaan transmisi Friis (daya terima antar dua antena)

Relasi Pr/Pt lewat efektif area dan jarak jauh R > 2 D^2/lambda (D dimensi terbesar
kedua antena) - `[R3, Balanis Antenna, PDF 110]` (mulai Pers. 2-113, sek. 2.17).
Catatan ekstraksi: `pdftotext` menjatuhkan pangkat dan pembagian pada syarat jarak jauh
(keluar `R > 2D2`); bentuk 2 D^2/lambda diterbitkan dari konteks seksi yang sama dan
**wajib dibaca ulang di kertas sebelum dijadikan dasar angka**.

### Metrik pencocokan feeder

| Besaran | Ketentuan | Sumber |
|---|---|---|
| Return loss | RL = -20 log abs(Gamma) dB; beban match (Gamma = 0) = tak hingga dB; refleksi total = 0 dB; nonnegatif untuk jaringan pasif | `[R3, Pozar MW, PDF 78]` Eq. (2.38) (cetak 58) |
| SWR | rasio gelombang berdiri dari Gamma, Eq. (2.41); sirkuit-terbuka/short => tak hingga | `[R3, Pozar MW, PDF 78]` (cetak 58) |
| Transformer seperempat gelombang | Z1 = sqrt(Z0 ZL), hanya beban resistif, panjang listrik lambda0/4 pada f0 | `[R3, Pozar MW, PDF 267]` Eq. (5.25) (cetak 247) + identitas padanan `[R3, Pozar MW, PDF 95]` (diwarisi W10) |
| Impedansi dipol λ/2 | Rr = 73 ohm; zin = 73 + j42,5 ohm | `[R3, Balanis Antenna, PDF 198]` (cetak 176; angka diwarisi tercetak dari tambalan W9B, halaman dibuka ulang kartu ini) |

### Kapasitas kanal sebagai langit-langit laju

```
C = B log2(1 + SNR)     bits/s     (Eq. 4.1)
```

| Uji banding | Nilai | Sumber | Verifikasi kartu ini |
|---|---|---|---|
| Contoh buku: B = 30 kHz, SNR = 33 (d = 100 m) | C = 152,6 kbps | `[R3, Goldsmith WC, PDF 130]` | dihitung ulang: 30000 * log2(34) = 152.623,9 bps - cocok |
| Contoh buku: B = 30 kHz, SNR = 0,033 (d = 1 km) | C = 1,4 kbps | `[R3, Goldsmith WC, PDF 130]` | dihitung ulang: 30000 * log2(1,033) = 1.405,2 bps - cocok |
| Definisi SNR dan PSD derau N0/2 | landasan Eb/N0 | `[R3, Goldsmith WC, PDF 201]` | badan definisi terbuka (bab 6 sek. 6.1) |
| Probabilitas galat BPSK/QPSK atas AWGN (fungsi Q/erfc) | metode | `[R3, Goldsmith WC, PDF 202]` (sek. 6.1.2) | kepala seksi + badan awal terbuka; **tabel koefisien per-modulasi belum dibuka halaman-per-halaman** |

> **Aturan yang membatalkan hitungan bila dilanggar:** angka unjuk kerja perangkat
> (daya pancar aktual, figure of noise, rugi kabel/konektor, gain antena terkirim)
> **wajib R4 lembar data pabrikan** - bukan angka buku. Semua hasil di atas adalah
> metode + contoh aritmetika; tidak satu pun menjadi ambang terima (mata ④).

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara membuktikan sebuah rancangan tautan. Yang TIDAK bisa
dinyatakan: ambang terima.** Urutan tingkat untuk mata ini adalah R1 -> R2 -> kontrak
(`ASSURANCE-WORKFLOW.md`); R3 hanya sah bila kontrak mengadopsinya tertulis, dan kolom
register ketiga buku ini berbunyi `no-unless-contract-adopts`.

Uji intern rancangan (sah dijalankan, hasilnya dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Daya terima terprediksi vs terukur | Hitung Pr dengan Friis/FSPL (mata ③), ukur RSSI lapangan, laporkan selisihnya | metode `[R3, Goldsmith WC, PDF 60]`, `[R3, Balanis Antenna, PDF 110]`; **selisih maksimum yang boleh = angka proyek/kontrak, tidak ada di rak** |
| Kualitas pencocokan feeder | Ukur RL/SWR pada port; laporkan angkanya | definisi `[R3, Pozar MW, PDF 78]`; **ambang RL/SWR lulus-tidak-lulus tidak ada di rak** (praktik umum industri bukan R-n di rak ini) |
| Kejernihan spektrum/zona Fresnel | Periksa halangan vs radius zona pada segmen kritis | model difraksi `[R3, Goldsmith WC, PDF 68]`; **rumus radius zona per-halaman belum tertambat** (klaim `KEMAMPUAN.md` K-0219 menambatnya ke hal. 56-60 yang berisi definisi PL, bukan zona - lihat CATATAN SILANG-PEMILIK butir 4) |
| Kelayakan laju data | Bandingkan laju target dengan langit-langit Shannon Eq. (4.1) | `[R3, Goldsmith WC, PDF 129]`; sah sebagai uji konsistensi rancangan, **bukan** ambang mutu |
| BER terhadap SNR | Kurva teoretis BPSK/QPSK sebagai pembanding hasil ukur | `[R3, Goldsmith WC, PDF 201]`-`[PDF 202]`; **target BER (mis. 1e-6) milik kontrak/aplikasi, tidak ada di rak** |

**Celah yang dibukukan (bukan dikarang):**

1. **Tidak ada ambang terima radio di rak ini.** Ukur 11-10-2026:
   `MASTER-REFERENCE-REGISTER.csv` = 0 baris R1/R2 ber-domain RF-WIRELESS (tiga barisnya
   semua R3, baris 95-97); `GAP-REGISTER.csv` = 0 baris menyebut RF-WIRELESS;
   `07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md` = 0 butir
   radio/wireless/antena; `TEMPLATE-BERITA-ACARA.md` punya 8 jenis uji dan **tidak satu pun
   jenis uji radio/tautan nirkabel**.
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK
   ini): ambang terima tautan radio (margin fade, SNR/BER minimum, RL/SWR maksimum,
   kepatuhan emisi spektrum) tidak memiliki sandaran R1/R2. Yang seharusnya masuk rak:
   peraturan lembaga spektrum Indonesia (mis. tata cara izin frekuensi) atau standar R2
   (ETSI/IEEE) yang relevan, atau pasal adopsi tertulis R3 oleh kontrak proyek.
3. **Bentuk jawaban yang sah hari ini** saat ambang radio diminta: nyatakan "tidak ada di
   rak ini; sumber yang seharusnya: R1/R2 regulasi spektrum atau pasal adopsi kontrak",
   lalu mintakan angka itu ke pemilik pekerjaan - **jangan** mengambil angka contoh buku
   (152,6 kbps; 3,65 dB; K = -31,54 dB; n = 3,71) sebagai ambang. Angka-angka itu
   ilustrasi pedagogis (ditegaskan resume Goldsmith bagian 2: "nilai contoh latihan,
   bukan ambang").

---

## ⑤ Bukti serah

Bukti serah untuk pekerjaan tautan nirkabel = bukti bahwa **setiap angka punya jalur
①->④**, bukan hanya hasil akhirnya.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | `10_TEMPLATES/TPL-00-KARTU-KENDALI.md`; status kartu sah bila tertulis "menunggu R4" untuk angka produk |
| Lembar perhitungan `TPL-02` dengan tag per masukan | ✅ | Tiap masukan bertanda `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` / `ASSUMPTION`; tiap `ASSUMPTION` punya sensitivitas + rencana penggantian (gerbang G3, `ASSURANCE-GATES.md:52-58`) |
| **Pemeriksaan orang kedua** | ✅ | G3 tidak tertutup tanpa ini. Preseden jujur di rak: `CALC-P00-001.md` masih tertulis "belum diperiksa orang kedua" - contoh itu sendiri belum lewat G3 |
| Hasil ukur lapangan (RSSI per segmen, RL/SWR port, peta halangan LOS) | ✅ | Simpan mentahnya di `08_EVIDENCE/`; bandingkan vs prediksi mata ③ sebagai tabel selisih |
| Lembar data pabrikan (R4) untuk setiap angka produk | ✅ | Daya pancar radios, gain antena terkirim, figure of noise, rugi feeder - tanpa R4 angka produk tidak sah masuk dokumen serah |
| Izin/kepatuhan frekuensi | ✅ | Dokumen R1 regulasi spektrum - **belum ada di rak** (mata ④ celah 2); sampai masuk, nyatakan "menunggu dasar hukum" |
| Versi alat ukur + kalibrasi | ✅ | Tanpa ini pengukuran RSSI/RL tidak dapat direproduksi; `09_HANDOVER/TPL-06-P00-KETERTELUSURAN.md` sebagai cermin ketertelusuran |
| Penyataan asal ambang (mata ④) | ✅ | Bila ambang berasal dari kontrak: sebut pasalnya; bila belum ada: tulis "belum ada di rak" - jangan biarkan kosong tanpa keterangan |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi; ini titik di mana celah mata ④ paling sering tersamar |

**Keterbatasan kerangka yang ada:** `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/
TEMPLATE-BERITA-ACARA.md` menyediakan 8 jenis uji (serat, pembumian, isolasi, baterai,
genset, video, termal, penyimpanan) dan **tidak punya bagian untuk uji tautan radio**;
pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas itu) plus tabel Ringkasan
sumber ambang-nya, dan nyatakan bahwa jenis uji radio belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dan setiap angkanya bertanda `[R-n]`
dengan halaman yang sudah dibuka ulang terhadap vault. Mata ④ **jujur kosong untuk ambang**:
ambang mutu tautan radio menuntut R1/R2 (regulasi spektrum / standar sistem) atau adopsi R3
tertulis oleh kontrak - ketiganya belum ada di rak ini.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier menaikkan daya-ikat resume
dari `pending_verification`, (b) insan menandatangani unit `KEMAMPUAN.md` domain ini
(ukur 11-10-2026: 25 baris RF-WIRELESS di `KEMAMPUAN-REGISTER.csv`, seluruhnya lahir
`pending_verification` / `draft-tidak-terverifikasi-insan`, sign-off 0), dan (c) ambang
terima radio punya sandaran R1/R2 atau adopsi kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_4bb6e4ef. Butir 1-2 terukur langsung dari berkas vault dan
berkas hulu; berkas-berkas itu bukan milik LOCK ini sehingga **tidak disunting**.

1. **Jangkar outage resume Goldsmith meleset.** `R3 - Wireless Communications (Goldsmith).md`
   bagian 2 menambatkan "Peluang padam (outage probability) gabungan path loss + shadowing"
   ke `[R3, Goldsmith WC, PDF 86..87]`; PDF 86-87 (cetak 57-58) adalah halaman **PROBLEMS**
   (Gambar 2.11, 2.12 untuk soal 2-11 dan 2-14). Seksi 2.9 dan Contoh 2.5 yang sebenarnya
   ada di **PDF 81 (cetak 52)**. Berkas ini mengutip PDF 81.
2. **Anchor longgar `KEMAMPUAN.md` per-baris register.** K-0205/K-0206 menulis "pdf hal.
   68+" - definisi RL/SWR (Eq. 2.38/2.41) justru di PDF 78; K-0219 menulis "Free-Space Path
   Loss & Fresnel Zone ... pdf hal. 56-60" - halaman itu memuat definisi PL, sedangkan
   materi zona/difraksi Fresnel ada di PDF 68; K-0203 menulis "pdf hal. 266 (92)" - badan
   Eq. (5.25) ada di PDF 267 (tambalan W10 sudah membetulkan ke 267, baris register aslinya
   belum). `KEMAMPUAN.md` adalah digest mesin dari `KEMAMPUAN-REGISTER.csv` - jalur mediasi
   controller ke pemilik register.
3. **README domain dan kartu REF masih menyebut rantai "belum berantai penuh" / resume
   "menyusul".** `README.md` domain dan bagian 5 kartu `REF-RFW-001..003` menunjuk status
   lama; sejak 11-10-2026 berkas ini berbanner "berantai parsial terbimbing" dan resume W3a
   sudah ada di rak. Berkas-berkas itu di luar LOCK kartu ini (04_KNOWLEDGE-CARDS dan
   README domain) - perlu kartu penyelarasan terpisah agar rujukan silang tidak kabur.
