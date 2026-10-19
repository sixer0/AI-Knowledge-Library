# Rantai X - Operasi layanan dan sistem padat data (arsip video, VMS/NVR, monitoring)

> **PENAMAAN AD-HOC (kartu t_20c6706f, 11-10-2026).** Huruf "X" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller (lihat CATATAN SILANG-PEMILIK butir 1). Ganti huruf di kepala bila controller
> memutuskan lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_20c6706f)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** (dua resume R3
ber-halaman + berkas penunjuk R5 + digest sapu-baca L2/L3). Mata ④ **tanpa ambang terima
dari rak**: ukur 11-10-2026 `MASTER-REFERENCE-REGISTER.csv` = 0 baris R1/R2
ber-domain SOFTWARE-DATA (seluruh R1/R2 di rak hanyalah empat baris, semuanya domain lain),
dan `KEMAMPUAN-REGISTER.csv` = 0 baris domain ini (folder tidak punya KEMAMPUAN.md - tidak
ada paket kalkulator; rantai ini murni metodologis, beda bentuk dari rantai MECHANICAL).
Celah dibukukan apa adanya di mata ④, bukan diisi angka kebijakan pihak lain.

**Daya-ikat tidak naik.** REF-SWD-002/003 berstatus `pending_verification` (P-5) dengan
kolom kontrak `no-unless-contract-adopts` (baris register 98-99); REF-SWD-001 `POINTER_ONLY`
(baris 43) dan **tidak pernah** menjadi sandaran akhir (aturan R5). Susunan mata ②-⑤ ini
**menyiapkan**, insan yang menandatangani; nol baris register disunting oleh berkas ini.

**Ambang berasal dari:** kebijakan pemilik layanan dan kontrak, bukan dari rak. Kedua buku
R3 ini memasok **kerangka (SLI/SLO/error budget, golden signals, replikasi/konsensus) dan
cara membuktikan operasi**; kedua resume menegaskan "angka target adalah kebijakan, bukan
hukum alam". Bila sebuah pekerjaan menuntut angka ketersediaan/RPO/RTO yang mengikat,
angkanya milik kontrak atau standar R1/R2 yang belum ada di rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 kecuali disebut) |
|---|---|---|---|
| `REF-SWD-002` - Site Reliability Engineering: How Google Runs Production Systems, Beyer dkk. (2016, O'Reilly) | **R3** ⏳pending | Kerangka risiko & SLO: menerima risiko, definisi SLI/SLO/SLA, error budget, monitoring empat sinyal emas, penanganan beban lebih. | `[R3, SRE Google, PDF 51]` (bab 3 Embracing Risk, teks terbuka: "past a certain point ... increasing reliability is worse for a service (and its users) rather than better"), `[PDF 63]` (bab 4 SLO; struktur SLI target; "nines" 99 % = 2 nines, 99,999 % = 5 nines), `[PDF 70]` (cetak 44, badan error budget, teks terbuka), `[PDF 81]` (bab 6 Monitoring), `[PDF 86]` (cetak 60, "The four golden signals of monitoring are latency, traffic, errors, and saturation", teks terbuka), `[PDF 273]` (bab 21 Handling Overload) |
| `REF-SWD-003` - Designing Data-Intensive Applications, Kleppmann (2017, O'Reilly) | **R3** ⏳pending | Blok bangunan sistem padat data (database/cache/indeks/stream/batch), replikasi leader-based dan tukarannya, toleransi fault & konsensus. | `[R3, Kleppmann DDIA, PDF 25]` (bab 1, daftar blok bangunan, teks terbuka), `[PDF 173-174]` (bab 5 Replication; sync vs async, leader-based), `[PDF 343]` (bab 9 Consistency and Consensus; asumsi jaringan: paket hilang/tertata ulang/terlambat, jam approximate) |
| `REF-SWD-001` - Deep Learning, LeCun, Bengio & Hinton (Nature 2015, makalah tinjauan 9 hal) | **R5** POINTER_ONLY | **Penunjuk, bukan sandaran.** Kosakata analitik video/ASR (jaringan konvolusi, recurrent, propagasi balik) pada tingkat tinjauan. | `[R5, LeCun Nature, PDF 1]` (dibuka ulang 11-10: "REVIEW doi:10.1038/nature14539", judul + afiliasi ketiga penulis terkonfirmasi) |

> Baris R3: sah untuk **metode dan penalaran dengan kutipan halaman sendiri**, belum sah
> menambat angka ambang terima (P-5; kolom register `no-unless-contract-adopts`). Baris R5:
> tidak pernah sandaran akhir - angka unjuk kerja analitik wajib R4 lembar data produk
> `[R5, berkas rak REF-SWD-001, L31-L33]`. Kartu batas pemakaian:
> `04_KNOWLEDGE-CARDS/SOFTWARE-DATA/REF-SWD-00{1,2,3}.md`.

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** seluruh jangkar
kolom terakhir dibuka ulang 11-10-2026 pada run kartu ini dengan `pdftotext -layout`
(Xpdf 4.06) terhadap berkas vault: SRE PDF 51, 63, 65-67, 69-71, 76-80, 81-84, 86, 92-95,
273; DDIA PDF 25, 173-176, 343; makalah Nature PDF 1. Jangkar yang **diwarisi dari peta
resume tanpa dibuka ulang di sini** (dipakai hanya sebagai penunjuk letak, bukan dasar
kutipan): `[R3, SRE Google, PDF 75]` (Eliminating Toil), `[PDF 113]` (Release Engineering),
`[PDF 123]` (Simplicity), `[PDF 133]` (Alerting), `[PDF 151, 159, 177, 187, 203, 209]`
(on-call s.d. Testing for Reliability) dan `[R3, Kleppmann DDIA, PDF 49, 91, 133, 221, 243,
295, 411, 461]` (peta bab).

**Konversi halaman (terpakai saat membaca rujukan; dicocokkan ulang hari ini):** SRE = cetak
+ 26 = PDF (terukur tiga titik: PDF 63 -> folio "Chapter 4" awal cetak 37; PDF 70 -> folio
43/44 tercetak di halaman; PDF 86 -> folio "Black-Box Versus White-Box | 59" berlanjut ke 60
- semua cocok selisih 26). DDIA = cetak + 22 = PDF (terukur dua titik: PDF 25 = bab 1 =
cetak 3; PDF 173 = bab 5 = cetak 151). Makalah Nature: nomor PDF = nomor cetak (9 halaman).

**Peran rak (terakun dari digest L2):** domain ini menjawab **kerangka operasi dan arsitektur
data**; pertanyaan angka akurasi produk analitik TIDAK dijawab di sini - wajib R4 lembar data
produk, dan dasar teoretis deteksi/pelacakan ada di laci VIDEO-SURVEILLANCE (Szeliski R3)
`[R3, digest L2 SOFTWARE-DATA, tabel routing + L40-L43]`.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian; yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`).

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Target keandalan layanan dinyatakan sebagai **SLO + error budget**, bukan "100 % uptime" | "It's both unrealistic and undesirable to insist that SLOs will be met 100 % of the time ... it is better to allow an error budget - a rate at which the SLOs can be missed - and track that on a daily or weekly basis" `[R3, SRE Google, PDF 70]`; "past a certain point ... increasing reliability is worse for a service (and its users) rather than better" `[PDF 51]` | Menulis "99,999 %" di dokumen serah tanpa SLI terukur ditolak - SLO tanpa SLI yang dapat diukur bukan sasaran, melainkan slogan; buku melarang keras SLA tanpa objek ukur `[R3, SRE Google, PDF 63]` |
| Monitoring minimal cukup **empat sinyal emas**: latency, traffic, errors, saturation (latency sukses dan gagal dipisah) | `[R3, SRE Google, PDF 86]` (teks terbuka, termasuk peringatan latency error cepat vs lambat) | Dashboard segalanya-dan-alat-belajar-"ajaib" ditolak: "We avoid 'magic' systems that try to learn thresholds" `[R3, SRE Google, PDF 84]` (teks terbuka); ambang yang tidak dapat dijelaskan alasannya tidak bisa dipertahankan ke pemeriksa |
| Arsip video/metadata memakai **replikasi leader-based**, dan mode sync-vs-async **dipilih sadar per kelas data** (frame vs indeks event) | Tukaran dinyatakan eksplisit: "whether to use synchronous or asynchronous replication, and how to handle failed replicas" `[R3, Kleppmann DDIA, PDF 174]` | Replikasi sinkron total untuk semua trafik ditolak - latensi dan ketersediaan tulis turun saat satu replica lambat; asinkron total untuk indeks pencarian ditolak - risiko kehilangan data saat failover (kelas "silent data loss" bab 5) |
| Desain toleransi fault **mengasumsikan jaringan buruk sejak awal**: paket hilang, tertata ulang, duplikat, terlambat; jam approximate; node bisa pause | `[R3, Kleppmann DDIA, PDF 343]` (teks terbuka, bab 9) | Menganggap timeout = mati ditolak - pola kegagalan distributed yang paling mahal justru yang tidak dibedakan dari lambat |
| Beban lebih ditangani **degradasi terencana** (serve degraded responses), bukan runtuh total | `[R3, SRE Google, PDF 273]` (bab 21, teks terbuka: "Gracefully handling overload conditions is fundamental to running a reliable serving system") | Load balancing saja tanpa kebijakan overload ditolak - sumbernya sendiri menyatakan "eventually some part of your system will become overloaded" |
| Angka unjuk kerja analitik video **tidak pernah** diambil dari makalah R5; wajib R4 lembar data produk; metode ujinya dari Szeliski (VIDEO-SURVEILLANCE) | Aturan R5 + routing digest L2 `[R5, berkas rak REF-SWD-001, L31-L33; R3, digest L2 SOFTWARE-DATA, L56-L61]` | Mengutip akurasi dari makalah tinjauan 2015 ditolak - arsitektur yang dibahas (AlexNet, LSTM) bukan mutakhir dan makalah tidak memuat angka produk |
| Kerentanan layanan dikurangi lewat **kesederhanaan** ("the price of reliability is the pursuit of the utmost simplicity") | `[R3, SRE Google, PDF 123]` (peta bab, diwarisi dari resume - belum dibuka ulang run ini; dipakai sebagai arah, bukan kutipan pengikat) | Menumpuk komponen khusus "demi keandalan" ditolak - setiap komponen menambah permukaan gagal (praktik uji keandalan bab 16 `[PDF 209]`, peta diwarisi) |

> Keputusan yang paling menentukan mutu di domain ini: **setiap angka target punya SLI yang
> dapat diukur dan sumber kebijakan yang disebut**, dan **setiap klaim keandalan punya
> skenario gagal yang sudah diasumsikan** (jaringan buruk, node pause, beban lebih).

---

## ③ Perhitungan

Domain ini tidak punya paket kalkulator (0 baris KEMAMPUAN-REGISTER; folder tanpa
KEMAMPUAN.md - ukur 11-10-2026). Hitungannya sederhana tetapi **jenis angkanya menentukan**:
anggaran downtime dihitung dari SLO; angka SLO-nya sendiri milik kebijakan/kontrak
(`ASSUMPTION`/kontrak), bukan rak. Rumus-rumus ini juga tidak hidup di
`06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` (ukur grep = 0 seksi operasi layanan) -
dicatat di kaki sebagai celah lintas-lapis.

### Anggaran downtime dari SLO (yang paling sering dibutuhkan dokumen serah)

```
budget_downtime = (1 - availability) x jendela_slo
```

| SLO (contoh kebijakan) | "Nines" `[R3, SRE Google, PDF 63]` | Anggaran per 30 hari (43.200 menit) | Tag |
|---|---|---|---|
| 99 % | "2 nines" | 432 menit = 7,2 jam | PROJECT-DERIVED (aritmetika; SLO-nya ASSUMPTION) |
| 99,9 % | "3 nines" | 43,2 menit | PROJECT-DERIVED |
| 99,99 % | "4 nines" | 4,32 menit | PROJECT-DERIVED |
| 99,95 % | "four and a half nines" `[R3, SRE Google, PDF 63]` | 21,6 menit | PROJECT-DERIVED |

Ukur ulang sendiri 11-10-2026 (0,001 x 43200 = 43,2; 0,0001 x 43200 = 4,32; 0,0005 x 43200 =
21,6). Sensitivitas dua skenario untuk target 99,9 %: melonggar ke 99 % = anggaran x10;
mengetat ke 99,99 % = anggaran /10 - pesan rancangan: **satu "nine" tambahan dibayar sepuluh
kali lipat** dalam anggaran maupun biaya sistem `[R3, SRE Google, PDF 51]` (logika biaya
keandalan ekstrem).

### Bentuk SLO yang sah dikutip (struktur, bukan angka)

```
SLI  target  ATAU  lower_bound <= SLI <= upper_bound
contoh bentuk buku: "average search request latency should be less than 100 milliseconds"
```

`[R3, SRE Google, PDF 63]` (teks terbuka). Nilai 100 ms adalah ilustrasi buku - **bukan**
ambang kontrak; buku menyebutnya sendiri "obviously an arbitrary value".

### Kerangka kapasitas arsip (DDIA, metode tingkat blok bangunan)

Blok yang dihitung per proyek surveilans skala besar: penyimpanan (retensi x bitrate x
jumlah kanal), indeks pencarian metadata, stream ingest, batch laporan `[R3, Kleppmann DDIA,
PDF 25]` (daftar blok bangunan, teks terbuka). Semua masukan bitrate/retensi =
`OEM-DERIVED`/kebutuhan klien; metode pemilihannya dari bab 3 (storage) dan bab 5 (replikasi)
dengan jangkar peta `[PDF 91]`, `[PDF 173]`.

> **Aturan yang membatalkan klaim bila dilanggar:** angka ketersediaan, RPO/RTO, atau latensi
> yang muncul di dokumen serah wajib menyebut **asal kebijakan + SLI pengukur + jendela
> pengukuran**. Tanpa ketiganya, angka itu `ASSUMPTION` dan tidak boleh jadi ambang terima
> final tanpa persetujuan tertulis (aturan rak, `ASSURANCE-WORKFLOW.md`).

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: kerangka menguji keandalan (testing for reliability, chaos
drills per bab 16/18 peta `[R3, SRE Google, PDF 209]`, jangkar diwarisi) dan bentuk bukti
operasi. Yang TIDAK bisa dinyatakan: ambang terima.** Urutan tingkat mata ini R1 -> R2 ->
kontrak; kolom register kedua buku R3 berbunyi `no-unless-contract-adopts`, dan R5 tidak
pernah naik.

Uji yang sah dijalankan (hasil dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Uji beban/overload | Simulasikan beban lebih; verifikasi degradasi terencana bekerja sesuai kebijakan | metode `[R3, SRE Google, PDF 273]`; **ambang % degradasi yang diterima = kebijakan pemilik layanan, tidak ada di rak** |
| Uji replikasi/failover | Matikan leader; ukur kehilangan tulis (sync vs async) vs RPO yang diklaim | metode `[R3, Kleppmann DDIA, PDF 173-174]`; **RPO target = kontrak** |
| Uji penerimaan penyimpanan | RAID/kapasitas/IOPS sesuai jenis BA 8 | `TEMPLATE-BERITA-ACARA.md` bagian "8. Uji penyimpanan / RAID" (ada, ukur 11-10-2026) - ambangnya milik domain STORAGE, bukan rak ini |
| Pelaporan SLO | SLO violation rate vs error budget, ditrack harian/mingguan | `[R3, SRE Google, PDF 70-71]`; **berapa besar pelanggaran dianggap cacat serah = kontrak** |
| Pemeriksaan orang kedua | Register SLO + konfigurasi monitoring ditinjau independen | gerbang G3 (`ASSURANCE-GATES.md`) |

**Celah yang dibukukan (bukan dikarang):**

1. **Nol R1/R2 domain ini di rak** (ukur 11-10-2026 terhadap `MASTER-REFERENCE-REGISTER.csv`:
   0 baris R1/R2 berdomain SOFTWARE-DATA; 0 baris domain ini di `GAP-REGISTER.csv` yang
   menyebut standar operasi - satu-satunya gap bertetangga GAP-011 TIA-568/TIA-942 milik
   STORAGE/NETWORKING, terbuka MENENGAH). Yang seharusnya masuk rak supaya mata ④ bisa terambat:
   standar manajemen layanan/tujuan keandalan setingkat R1/R2, atau adopsi tertulis R3 oleh
   kontrak proyek.
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK
   ini): "Ambang terima operasi sistem digital (ketersediaan layanan, RPO/RTO, ambang error
   budget) tidak memiliki sandaran R1/R2 di rak; sumber yang seharusnya: standar R1/R2
   manajemen layanan atau pasal adopsi SLO dalam kontrak."
3. **GAP-021 dicatat berubah bentuk:** berkas rak R5 masih menulis "Laci
   R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA/ KOSONG" `[R5, berkas rak REF-SWD-001, L39-L41]`,
   padahal ukur 11-10-2026 laci vault itu berisi dua buku (SRE, DDIA - promosi W1b/W3c) dan
   GAP-021 sudah `sebagian` dengan catatan 4 buku ML di laci AI-ML. Klaim "kosong" pada
   berkas rak basi untuk bagian non-ML-nya; lihat CATATAN SILANG-PEMILIK butir 2.
4. **Bentuk jawaban sah hari ini** bila ambang ketersediaan diminta: "tidak ada di rak ini;
   sumber yang seharusnya: pasal kontrak (SLO + SLI + jendela) atau standar R1/R2 manajemen
   layanan" - **jangan** mengambil angka ilustrasi buku (100 ms; lima nine; 0,06) sebagai
   ambang proyek.

---

## ⑤ Bukti serah

Bukti serah pekerjaan operasi/sistem data = bukti setiap angka target punya jalur ①->④ dan
setiap klaim keandalan punya uji yang pernah dijalankan.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Register SLO/SLI per layanan (SLI, target, jendela, sumber kebijakan) | ✅ | Padanan bentuk: struktur SLI-target `[R3, SRE Google, PDF 63]`; sumber kebijakan ditulis eksplisit (kontrak/keputusan pemilik, tanggal) |
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Status "menunggu R4" sah bila rating produk storage/analytics belum datang |
| Konfigurasi monitoring + definisi alert empat sinyal emas (snapshot) | ✅ | `[R3, SRE Google, PDF 86]`; alert harus actionable, bukan threshold "ajaib" `[PDF 84]` |
| Hasil uji failover/beban-lebih dengan BA | ✅ | Pakai "Rangka umum" + jenis 8 (penyimpanan) dari `TEMPLATE-BERITA-ACARA.md`; nyatakan jenis uji operasi layanan belum punya template khusus |
| Perhitungan anggaran downtime vs pencapaian aktual (jejak alat ukur) | ✅ | Aritmetika mata ③ + ekspor alat monitoring bertanggal |
| Bukti mode replikasi terpilih per kelas data | ✅ | Keputusan sync/async + alasan (mata ②) + hasil uji ④ |
| **Pemeriksaan orang kedua** | ✅ | G3 tidak tertutup tanpa ini |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi - di domain ini titik paling rawan tersamar karena angkanya kebijakan, bukan rumus |

**Keterbatasan kerangka:** `TEMPLATE-BERITA-ACARA.md` (ukur 11-10-2026, delapan jenis uji)
tidak punya jenis "uji operasi layanan/SLO"; jenis 8 hanya menyentuh penyimpanan/RAID.
Pakai rangka umum dan nyatakan eksplisit bahwa template khusus belum ada.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dengan setiap angka bertanda `[R-n]`
dan halaman yang dibuka ulang terhadap vault hari ini. Mata ④ jujur tanpa ambang: domain ini
memasok kerangka operasi; angka terimanya adalah kebijakan pemilik layanan yang diadopsi
kontrak, dan sandaran R1/R2 untuk itu belum ada di rak.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier menaikkan daya-ikat resume
REF-SWD-002/003 dari `pending_verification`, (b) insan menetapkan register SLO pertama GSP
(tanda tangan kebijakan - belum ada sampai hari ini; nol unit KEMAMPUAN domain ini untuk
ditandatangani), dan (c) ambang operasi punya sandaran R1/R2 atau adopsi kontrak tertulis.

**Beda bentuk yang jujur:** rantai ini TIDAK punya mata hitung ber-kalkulator seperti domain
lain (0 paket kemampuan). Kekuatan rak di domain ini kerangka keputusan dan cara bukti -
jadi jangan mencari angka ambang di tempat yang memang tidak menyimpannya.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_20c6706f. Berkas-berkas berikut bukan milik LOCK ini sehingga
tidak disunting.

1. **Tabrakan nama rantai (enam rantai tanpa huruf).** Blueprint 02 baris 31 menagih
   "25/25 domain punya RANTAI bermata"; enam rantai langkah 15-17 (kartu saudara paralel
   t_9b7ace41, t_bcbb928d) belum dialokasikan hurufnya oleh TA. Rantai berjalan sampai R.
   Kartu ini memakai "W" (MECHANICAL) dan "X" (ini) ad-hoc. Dugaan alokasi berurutan:
   S,T = pasangan-1; U,V = pasangan-2; W,X = ini. Wewenang controller mengonfirmasi/mengganti.
2. **Berkas rak R5 klaim "laci kosong" sudah basi sebagian.** `R5 - Deep Learning (LeCun,
   Bengio & Hinton 2015).md` L39-L41 menulis laci `R3_TEXTBOOK-HANDBOOK/SOFTWARE-DATA/`
   KOSONG; ukur 11-10-2026 laci vault berisi 2 buku (SRE, DDIA). Untuk buku teks ML memang
   masih kosong (benar - empat buku ML ada di laci AI-ML), tetapi kalimatnya perlu
   dipersempit agar tidak terbaca "domain tanpa R3 sama sekali". Pemilik: berkas rak
   (jalur kurasi librarian/W-verify) + catatan GAP-021.
3. **Resume SRE: butir bertambat PDF 29 tidak ada di tabel peta bab** (tabel daftar
   `[R3, SRE Google, PDF 51]` dst., daftar butir memuat juga PDF 29 = bab 1 Introduction).
   Bukan salah kutipan (halamannya terverifikasi berisi "chapter 1 introduction" saat dibuka
   run ini), hanya ketidaksinkronan dua daftar dalam satu berkas resume. Pemilik: berkas
   resume W3c.
4. **Kepala resume SRE/DDIA memakai istilah "gelombang W3c" dan bukti sha256[:16]**
   (`36bc8fec5a696c1b`, `3480da3ae9a35306`) yang tidak dapat direproduksi dari kartu ini
   tanpa berkas evidence hulu; rantai ini tidak mengadopsi klaim byte itu, hanya rujukan
   letaknya. Verifikasi byte adalah milik siklus verifier (langkah 31), bukan catatan
   koreksi.
