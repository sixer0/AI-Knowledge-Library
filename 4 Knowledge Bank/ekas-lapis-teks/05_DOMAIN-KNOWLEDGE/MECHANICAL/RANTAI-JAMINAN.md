# Rantai W - Perhitungan mekanikal: dudukan, komponen mesin, fluida, termal

> **PENAMAAN AD-HOC (kartu t_20c6706f, 11-10-2026).** Huruf "W" dipakai di kepala ini hanya
> agar rantai bisa dirujuk; penunjukan resmi huruf rantai untuk langkah 15-17 adalah wewenang
> controller (lihat CATATAN SILANG-PEMILIK butir 1). Ganti huruf di kepala bila controller
> memutuskan lain - isi mata rantai tidak terpengaruh.

## RANTAI BERANTAI PARSIAL TERBIMBING (terbit 11-10-2026, kartu t_20c6706f)

Mata ①-③ dan ⑤ tersusun **terbimbing lapisan yang ada di rak ini** (tujuh resume ber-halaman
+ KEMAMPUAN.md domain + digest sapu-baca L1/L3). Mata ④ **tanpa ambang terima dari rak**:
ukur 11-10-2026 `MASTER-REFERENCE-REGISTER.csv` = 0 baris R1/R2 ber-domain MECHANICAL
(seluruh R1/R2 di rak hanyalah empat baris: IEEE 1188/IEC 62485-2 POWER-BACKUP, ANSI-NETA
ATS-2017 ELECTRICAL, IEC 61280-4-2 FIBER-OPTIC, BS EN 62676-1-2 VIDEO-SURVEILLANCE). Celah
dibukukan apa adanya di mata ④, bukan diisi nilai buku.

**Daya-ikat tidak naik.** Seluruh rujukan domain ini berstatus kolom `no-unless-contract-adopts`
di register induk (baris 12, 86-91; REF-MEC-002..006 `verified-sumber`, REF-MEC-007
`pending_verification`, REF-MEC-001 `ACTIVE`). Susunan mata ②-⑤ ini **menyiapkan**, insan yang
menandatangani; nol baris register disunting oleh berkas ini.

**Ambang berasal dari:** bukan dari rak ini. Rak ini memasok **metode hitung dan cara
membuktikannya**. Ambang terima (faktor keamanan, kelas mutu bahan, batas lelah) milik
**kontrak** atau standar R1/R2 yang belum ada di rak; lihat mata ④.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman (PDF, dibuka ulang 11-10-2026 kecuali disebut) |
|---|---|---|---|
| `REF-MEC-001` - Shigley's Mechanical Engineering Design SI Units, Budynas & Nisbett | **R3** ACTIVE | Tegangan/defleksi batang-balok, kegagalan statik & fatigue, sambungan baut/las, poros-bantalan-roda gigi, tabel material (A-5), kelas toleransi metrik (A-11/A-12). | `[R3, Shigley SI, PDF 1042]` (Table A-5 Physical Constants), `[PDF 1057-1058]` (A-11/A-12, sumber ANSI B4.2-1978), `[PDF 425]` (contoh torsi + teori energi-distorsi) |
| `REF-MEC-002` - Marks Standard Handbook for Mechanical Engineers, Avallone dkk. | **R3** ⏳ | Pelat datar & silinder (kekuatan bahan lintas-bab), satuan, properti besi-baja-aluminium. | `[R3, Marks Handbook, PDF 319-321]` (folio 5-47 "FLAT PLATES", verifikasi buka) |
| `REF-MEC-003` - Fundamentals of Fluid Mechanics 4e, Munson, Young & Okiishi | **R3** ⏳ | Bilangan Reynolds & rezim aliran, asumsi Bernoulli, panjang masuk pipa, kerugian, pompa. | `[R3, Munson Fluid, PDF 41]` (definisi Re), `[PDF 121]` (bab Bernoulli), `[PDF 131]` (Pers. 3.12 + asumsi), `[PDF 466]` (Eq. 8.1-8.2 panjang masuk), `[PDF 479]` (ambang transisi Re), `[PDF 307]` (soal pompa sentrifugal) |
| `REF-MEC-004` - MERM 13.4, Lindeburg | **R3** ⏳ | Rumus siap-pakai FE-style: siklus mesin bakar, kompresi gas, konveksi paksa, ventilasi. | `[R3, MERM 13.4, PDF 431]` (bab 28 Reciprocating Engine Cycles), `[PDF 473]` (bab 32 Gas Compression), `[PDF 531]` (bab 36 Forced Convection), `[PDF 581]` (bab 40 Ventilation) - keempatnya halaman peta bab (daftar isi), bukan badan rumus |
| `REF-MEC-005` - Mechanical Design of Machine Elements and Machines 2e, Collins, Busby & Staab | **R3** ⏳ | Perancangan berbasis pencegahan kegagalan: poros transmisi, bantalan gelinding (L10), sambungan baut (kelas metrik), ulir daya. | `[R3, Collins Design, PDF 359]` (bab 8 Power Transmission Shafting), `[PDF 447]` (bab 11 Rolling Element Bearings), `[PDF 454]` (folio 436, Pers. 11-2), `[PDF 512]` (folio 494, tabel kelas baut metrik), `[PDF 494]` (folio 476, Contoh 12.2 ulir daya) |
| `REF-MEC-006` - Fundamentals of Engineering Thermodynamics, Moran, Shapiro dkk. | **R3** ⏳ | Neraca energi volume-aturnya, siklus Rankine/Brayton, psikrometri. | `[R3, Moran Thermodynamics, PDF 196]` (folio 178, bab 4 CV energy analysis), `[PDF 546]` (folio 528, bab 9 gas power), `[PDF 784]` (folio 766 seksi 12.7 Psychrometric Charts) |
| `REF-MEC-007` - Machinery's Handbook 28th, Oberg dkk. | **R3** ⏳ | Dimensi standar fabrikasi: luas-tarik ulir, angka terpilih Renard, suai metrik, kecepatan potong. | `[R3, Machinery Handbook, PDF 1396]` (folio 1436, luas-tarik ulir metrik & Unified per JIS B 1082), `[PDF 678]` (folio 671 Preferred Numbers), `[PDF 656]` (folio 649 Preferred Metric Fits), `[PDF 982]` (folio 979 Speeds and Feeds; rumus kecepatan tercetak di folio 986 = PDF ~989, belum dibuka), `[PDF 2227]` (folio 2556 Measuring Units) |

> Semua baris R3 buku teks/handbook: sah untuk **metode dan penalaran dengan kutipan
> halaman sendiri**, belum sah menambat angka ambang terima (P-5; kolom register
> `no-unless-contract-adopts`). Kartu batas pemakaian: `04_KNOWLEDGE-CARDS/MECHANICAL/REF-MEC-00{1..7}.md`.

**Provenans pembukaan halaman (agar tidak ada klaim pinjaman tersamar):** seluruh jangkar
kolom terakhir di atas dibuka ulang 11-10-2026 pada run kartu ini dengan `pdftotext -layout`
(Xpdf 4.06) terhadap berkas vault - 30 halaman per berkas hitungan: Shigley 425/1042/1057-1058;
Munson 41/121/131/307/466/479; Collins 359/447/454/494/512; Marks 319-321; MERM 431/473/531/581;
Moran 196/546/784; Machinery 656/678/982-983/1396/2227. Jangkar tambahan yang **diwarisi dari
lapisan tanpa dibuka ulang di sini** (dipakai hanya sebagai penunjuk letak, bukan dasar kutipan):
peta bab penuh keenam resume W3b/W3c (mis. `[R3, MERM 13.4, PDF 159]` Fluid Properties).

**Konversi halaman (hasil buka ulang hari ini):** Marks = folio buku "5-47" → PDF 319 (offset
bab tetap, folio per-bab). Machinery = cetak + 7 (PDF 1396→1436, 678→671, 656→649, 982→979,
2227→2556 TIDAK cocok - blok daftar isi; selisih bervariasi, konsisten peringatan kepala
resume). Collins = PDF − 18 (454→436, 512→494, 494→476). Moran = PDF − 18 (196→178, 546→528,
784→766). Shigley SI = PDF + 1 (425→406, 1042→1023, 1057→1038). Munson = PDF − 18 (131→113,
466→448, 479→461). MERM = halaman peta bab (daftar isi), offset badan belum diukur.

**Peran rak (terakun dari digest L1):** di koleksi yang isinya elektronik/jaringan/kelistrikan,
domain ini satu-satunya sandaran perhitungan struktur-mekanik - dipakai untuk dudukan kamera,
bracket, tiang, menara, dan perangkat bergerak PTZ `[R3, berkas rak Shigley, baris 13-15]`.

---

## ② Keputusan desain

Tingkat R3 **cukup** untuk mata ini: keputusan rekayasa memang penilaian; yang wajib tertulis
adalah pilihan + alternatif yang ditolak + alasannya (`01_GOVERNANCE/ASSURANCE-WORKFLOW.md`,
tabel "Aturan tingkat pada tiap mata rantai").

| Yang ditetapkan | Dasar | Alternatif yang ditolak dan alasannya |
|---|---|---|
| Objek hitungan **komponen mesin** memakai laci MECHANICAL; objek **struktur gedung/menara** memakai laci CIVIL-STRUCTURAL (rantai K) | Irisan metodik antar kartu terakun: "Shigley ranah komponen mesin (poros, bearing, pegas, fatig), bukan struktur gedung; pemakai harus memilih laci yang benar" `[R3, digest L3 REF-MEC-001]` | Menghitung rangka menara dengan Shigley saja ditolak - kebutuhan keselamatan struktur penopang jatuh ke norma rantai K (ahli bersertifikat + SNI), bukan angka buku `[R3, digest L1 MECHANICAL, baris 75-80]` |
| Untuk tiang/bracket kamera: **kekakuan (defleksi) diperiksa lebih dulu**, baru kekuatan | Defleksi sering lebih menentukan daripada kekuatan: tiang kuat-tetapi-lentur = gambar bergoyang saat berangin, masalah pasca-pasang yang mahal diperbaiki `[R3, berkas rak Shigley, baris 45-47, 75]` | Memeriksa kekuatan saja lalu menyimpulkan "aman" ditolak - gagal di kriteria fungsional yang nyata walau lolos tegangan |
| Umur struktur luar ruang ditentukan **kelelahan (fatigue)** beban angin berulang, bukan kekuatan sekali beban | Prinsip terakun Part 2 `[R3, berkas rak Shigley, baris 51-53]`; kumulatif kerusakan pada beban fluktuatif `[R3, Collins Design, PDF 259]` (peta, diwarisi) | Desain statik satu-beban untuk menara luar ruang ditolak - umur ditentukan siklus, bukan puncak |
| Rezim aliran pipa ditetapkan lewat **Reynolds**, dan ambang transisi memakai angka buku yang **berhasil diukur di vault**: laminar Re < 2100, turbulen Re > 4000 (transisi 2100-4000) `[R3, Munson Fluid, PDF 479]` (cetak 461, teks terbuka: "less than approximately 2100 ... greater than approximately 4000") | Definisi Re = ρVD/μ `[R3, Munson Fluid, PDF 41]`; pemilihan rezim menentukan rumus kerugian yang sah dipakai | Memakai Re_kritis = 2000 warisan KEMAMPUAN.md (baris FLD-007) untuk vonis laminar/turbulen ditolak sebagai satu-satunya dasar - teks vault 4e menyebut 2100/4000; lihat CATATAN SILANG-PEMILIK butir 2 |
| Asumsi Bernoulli **dinyatakan eksplisit setiap kali dipakai**: steady, inviscid, incompressible, sepanjang streamline; Pers. (3.12) konstan lintas streamline untuk kasus khusus | `[R3, Munson Fluid, PDF 131]` (cetak 113, teks terbuka); peringatan buku: "the most used and the most abused equation in fluid mechanics" `[R3, Munson Fluid, PDF 121]` | Bernoulli telanjang pada aliran kental/transien/rotasi ditolak - kesalahan klasiknya persis yang diperingatkan sumbernya |
| Umur bantalan gelinding dilaporkan sebagai **L10 dengan penyesuaian reliabilitas LP = KR*L10**, bukan satu angka "umur" tunggal | `[R3, Collins Design, PDF 454]` (folio 436): "L10 = 10^6 revolutions (corresponds to P = 10 or R = 90), may be adjusted to any chosen ... LP = KR L10 (11-2)" - teks terbuka, cocok verbatim dengan jangkar W9B `pdf_p454 (cetak 436)` di KEMAMPUAN.md | Menulis hasil L10 sebagai jaminan umur produk ditolak - ia rating statistik 90% dari katalog; umur produk aktual menuntut data OEM (R4) |
| Baut sambungan dipilih dari **kelas properti metrik + beban bukti (proof load)**, bukan dari diameter saja | Tabel kelas properti baut metrik (digit kiri titik desimal ≈ kuat-tarik minimum dalam ratusan MPa) `[R3, Collins Design, PDF 512]` (folio 494, teks terbuka); luas-tarik ulir per JIS B 1082 `[R3, Machinery Handbook, PDF 1396]` (folio 1436, teks terbuka) | Memilih baut "yang muat" tanpa kelas/proving-load ditolak - kegagalan sambungan berbaut adalah mode gagal pemasangan yang paling sering (peran Part 3 di rak) |
| Ukuran baku fabrikasi diambil dari **deret terpilih (Renard) dan suai metrik standar** sebelum menetapkan toleransi bebas | `[R3, Machinery Handbook, PDF 678]` (folio 671 Preferred Numbers, ANSI Z17.1-1973), `[PDF 656]` (folio 649 Preferred Metric Fits, ANSI B4.2), `[R3, Shigley SI, PDF 1057-1058]` (A-11/A-12, sumber ANSI B4.2-1978) | Toleransi karangan perancang tanpa kelas suai ditolak - tidak dapat diperiksa lawan dan tidak baku untuk pembelian |
| Dimensi penampang poros dari **teori kegagalan energi-distorsi** dengan torsi T = daya/kecepatan sudut | Pola contoh terukur `[R3, Shigley SI, PDF 425]` (folio 406): T = 30000/(6*260) N*mm, F = T/r, S_sy = 0,577*S_y | Kombinasi tegangan tanpa teori kegagalan eksplisit ditolak - "tegangan maksimum" saja tidak membandingkan terhadap kuat luluh dengan cara yang diakui |

> Keputusan yang paling menentukan mutu hasil di domain ini: **objek hitung memilih laci
> yang benar** (mesin vs struktur), **kekakuan/lelah diperlakukan sebagai kriteria pertama
> yang sah**, dan **setiap angka produk (rating bantalan, kelas baut aktual, mutu bahan datang)
> dikembalikan ke R4/sertifikat pabrik**, bukan ke tabel buku.

---

## ③ Perhitungan

Rumus-rumus domain ini hidup di lapisan resume + KEMAMPUAN.md, **bukan** di
`06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`: ukur 11-10-2026, `grep -ci "shigley|collins|munson|machinery|mekanik mesin"` pada KATALOG-RUMUS.md = 0 (tidak ada seksi mekanikal murni). Butir lintas-lapis ini dicatat di kaki berkas sebagai celah; pengisian KATALOG bukan wewenang LOCK ini.

### Inventaris metode terakun (dari KEMAMPUAN.md domain, 79 unit)

Empat rantai demo `qa/chains.py` menyentuh domain ini (tabel di `KEMAMPUAN.md` bagian
"Rantai demo"): DYNAMICS_CHAIN (K-0122..K-0128 + K-0177), DESIGN_PUMPING_SYSTEM
(K-0129..K-0140), MATERIALS_TOOLBOX (K-0146..K-0160), DESIGN_ROTATING_MACHINE
(K-0159..K-0180); DESIGN_POWER_CYCLE menukik ke rantai POWER-BACKUP, STATICS_TOOLBOX ke
rantai CIVIL-STRUCTURAL (K, putus-④). Kind `stub-candidate` (MAT-001/002/008, MEC-003/004/009/
011..014) **INERT**: sumbernya Roark (tidak ada di rak) atau lookup tanpa calculator - jangan
dipakai mengklaim kemampuan.

### Jangkar angka yang terukur ulang hari ini (bukan salinan laporan hulu)

| Besaran | Nilai | Sumber (buka ulang 11-10) | Tag | Catatan pemakaian |
|---|---|---|---|---|
| Definisi Re | Re = ρVD/μ | `[R3, Munson Fluid, PDF 41]` | SOURCE-DERIVED | Gerbang pilih rezim; satuan SI m²/s untuk ν kinematik |
| Re transisi pipa | < 2100 laminar; > 4000 turbulen; plat datar ~500.000 | `[R3, Munson Fluid, PDF 479]` (cetak 461) | SOURCE-DERIVED | Klasifikasi metode; BUKAN ambang terima kontrak |
| Panjang masuk laminar | Le/D = 0,06*Re (Eq. 8.1); ≈120D saat Re=2000; praktis 10⁴-10⁵ → 20D ≤ Le ≤ 30D (Eq. 8.2 turbulen) | `[R3, Munson Fluid, PDF 466]` (cetak 448) | SOURCE-DERIVED | Cocok verbatim dengan jangkar W9B `pdf_p466/cetak 448` di KEMAMPUAN.md (FLD-007) |
| Konstanta Bernoulli lintas streamline | Pers. (3.12): p + ρV²/2 + γz = konst (steady, inviscid, incompressible) | `[R3, Munson Fluid, PDF 131]` (cetak 113) | SOURCE-DERIVED | Asumsi wajib ditulis tiap pemakaian (mata ②) |
| Batas hidup bantalan | L10 = 10⁶ revolusi (P=10%, R=90%); LP = KR*L10 (Pers. 11-2) | `[R3, Collins Design, PDF 454]` (folio 436) | SOURCE-DERIVED | KR dari kurva reliabilitas katalog; rating produk = R4 |
| Kelas properti baut | Digit kiri desimal ≈ Su minimum ×100 MPa; kolom tensile/yield/proof per kelas | `[R3, Collins Design, PDF 512]` (folio 494) | SOURCE-DERIVED | Nilai bukti individual = sertifikat pabrikan (R4) |
| Luas-tarik ulir | Metrik & Unified per JIS B 1082 (As dari diameter efektif pitch) | `[R3, Machinery Handbook, PDF 1396]` (folio 1436) | SOURCE-DERIVED | Dasar MEC-005/MEC-008 (pemilihan ukuran baut) |
| Kuat geser dari luluh | S_sy = 0,577*S_y (distortion-energy) | `[R3, Shigley SI, PDF 425]` (folio 406) | SOURCE-DERIVED | Faktor 0,577 = 1/√3, teori bentuk, bukan angka produk |
| Torsi dari daya | T = P/omega (contoh buku: hasil tercetak 474.727 N*mm pada 260 rev/min) | `[R3, Shigley SI, PDF 425]` | SOURCE-DERIVED | Pecahan di halaman itu tidak dievaluasi ulang dari ekstraksi teks (lihat catatan di bawah) - buka halaman asli sebelum meniru bentuknya |
| Deret Renard & suai | Seri terpilih (Renard) ANSI Z17.1-1973; hole-basis H / shaft-basis | `[R3, Machinery Handbook, PDF 678, 656]` | SOURCE-DERIVED | Standarisasi ukuran sebelum toleransi bebas |

**Catatan aritmetika terukur (anti-salin-mentah):** contoh Shigley folio 406 tercetak sebagai
`T = 30000/(6 × 260) = 474727 N*mm` pada ekstraksi teks kami - pecahan kiri TIDAK mengevaluasi
ke hasil kanan (30000/1560 = 19,23), sehingga ekstraksi `pdftotext -layout` dipastikan membuang
faktor numerator (konversi satuan daya mesin pada edisi tersebut). Pelajaran yang mengikat:
rumus dari halaman yang teksnya rusak hanya boleh dipakai setelah halaman aslinya dibuka
manusia/alat render, atau diganti rumus yang terekstraksi utuh; angka hasil akhir buku
(474.727 N*mm) boleh dikutip sebagai ilustrasi dengan penanda halaman, tapi bukan untuk
diturunkan ulang. Ini contoh kenapa tag masukan wajib PROJECT-DERIVED dengan jejak, bukan
tempel angka buku.

### Bentuk hitung yang mengikat (pola per kelas pekerjaan)

```
Dudukan/bracket : beban (mati+angin+es) -> gaya reaksi (STA-00x) -> tegangan (MAT-013/016/017)
                  -> defleksi (MAT-014) <- KRITERIA FUNGSIONAL -> lelah (Part 2) untuk umur
Sistem pompa    : properti fluida (FLD-001) -> kontinuitas Q=VA (FLD-004) -> rezim Re (FLD-007)
                  -> kerugian Darcy-Weisbach+minor (FLD-006/008 Colebrook) -> head pompa (FLD-010)
                  -> pemilihan dari katalog <- R4 (FLD-011)
Mesin berputar  : daya->torsi -> diameter poros (MEC-015) -> kelas baut sambungan (MEC-018)
                  -> bantalan L10/KR (MEC-017) -> suai & finish (MEC-006) -> ukuran Renard (MEC-007)
```

Setiap masukan hitungan bertanda `SOURCE-DERIVED` (dengan kutipan halaman di atas),
`PROJECT-DERIVED`, `OEM-DERIVED` (rating produk - wajib lembar data), atau `ASSUMPTION`
(wajib sensitivitas ½×/2× + rencana penggantian). `ASSUMPTION` tidak boleh menjadi ambang
terima final tanpa persetujuan tertulis (aturan rak, `ASSURANCE-WORKFLOW.md`).

---

## ④ Pengujian

**Yang bisa dinyatakan rak ini: cara memverifikasi hitungan dan bentuk uji. Yang TIDAK bisa
dinyatakan: ambang terima.** Urutan tingkat untuk mata ini R1 → R2 → kontrak; R3 hanya sah
bila kontrak mengadopsinya tertulis, dan kolom register ketujuh buku ini semuanya
`no-unless-contract-adopts`.

Uji intern yang sah dijalankan (hasil dilaporkan, **bukan** vonis lulus):

| Butir | Ketentuan | Status sumber |
|---|---|---|
| Verifikasi silang metode | Hasil tegangan/defleksi dihitung ulang dengan metode kedua (mis. Roark-formula vs integrasi; Collins vs Shigley untuk kelas yang sama) | metode R3; **selisih maksimum antar-metode = angka proyek/kontrak, tidak ada di rak** |
| Uji fungsi mekanik lapangan | Ukur defleksi/getaran tiang terpasang vs prediksi rancangan | **protokol + ambangnya tidak ada di rak**: `07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md` punya 8 jenis uji (serat, pembumian, isolasi, baterai, genset, video, termal, penyimpanan) - TIDAK punya bagian uji mekanik (ukur 11-10-2026) |
| Pembuktian torsi baut | Kunci torsi dikalibrasi membuktikan preload/proof sesuai kelas terpilih | alat+kalibrasi wajib di BA; **ambang % preload = kontrak/prosedur pabrikan (R4)** |
| Kelayakan rating bantalan | L10 proyek vs kurva katalog OEM | rating = R4; metode L10 `[R3, Collins Design, PDF 454]` sah sebagai metode, bukan jaminan |
| Pemeriksaan orang kedua | Setiap lembar hitungan GSP mekanik ditandatangani pemeriksa kedua | gerbang G3 (`ASSURANCE-GATES.md`); preseden jujur rak: `CALC-P00-001.md` masih "belum diperiksa orang kedua" |

**Celah yang dibukukan (bukan dikarang):**

1. **Nol R1/R2 domain ini di rak** (ukur 11-10-2026 terhadap `MASTER-REFERENCE-REGISTER.csv`:
   0 baris R1/R2 berdomain MECHANICAL). Yang seharusnya masuk rak supaya mata ④ bisa terambat:
   standar penerimaan struktur/baut (mis. ASTM A325/A490 atau padanan SNI - keduanya tercatat
   bersinggungan di GAP-017/018/020 milik CIVIL-STRUCTURAL, status terbuka), dan standar
   verifikasi hasil hitungan.
2. **Usulan butir GAP untuk langkah 25-26** (kewenangan penulis register GAP, bukan LOCK ini):
   "Ambang terima hasil hitungan mekanikal (faktor keamanan minimum, toleransi defleksi
   layanan, kriteria sisa-umur lelah) tidak memiliki sandaran R1/R2 di rak; sumber yang
   seharusnya: adopsi kontrak tertulis atau standar penerimaan."
3. **Bentuk jawaban sah hari ini** bila ambang diminta: "tidak ada di rak ini; sumber yang
   seharusnya: ..." - **jangan** mengambil angka contoh buku (mis. safety factor 1,5 pada
   Contoh 12.2 `[R3, Collins Design, PDF 494]`) sebagai ambang umum; ia spesifikasi contoh
   soal itu, bukan norma.
4. **Struktur penopang keselamatan tidak dijamin rantai ini:** hasilnya jatuh ke norma rantai
   K (CIVIL-STRUCTURAL, putus-④) - tanda tangan ahli bersertifikat atau ambang kontrak
   `[R3, digest L1 MECHANICAL, baris 75-80]`.

---

## ⑤ Bukti serah

Bukti serah pekerjaan mekanikal = bukti setiap angka punya jalur ①→④, bukan hanya hasil akhir.

| Lampiran | Wajib | Catatan |
|---|---|---|
| Kartu kendali rantai per besaran (`TPL-00`) | ✅ | Status sah tertulis "menunggu R4" bila rating produk belum datang (`ASSURANCE-WORKFLOW.md`) |
| Lembar perhitungan `TPL-02` dengan tag per masukan | ✅ | Termasuk pernyataan asumsi Bernoulli/rezim aliran bila hitungan fluida (mata ②) |
| **Pemeriksaan orang kedua** | ✅ | G3 tidak tertutup tanpa ini |
| Bukti kalibrasi alat ukur lapangan (kunci torsi, DV) | ✅ | Nomor + tanggal kalibrasi masuk BA |
| Sertifikat/lembar data produk datang (baut, bantalan, pompa) | ✅ | Kanal R4 satu-satunya untuk angka produk; tanpa ini kartu "menunggu R4" |
| Jejak verifikasi silang metode kedua | ✅ | Lampirkan selisihnya, bukan hanya hasil terpilih |
| Pernyataan asal ambang (mata ④) | ✅ | Sebut pasal kontrak/adopsi tertulis, atau tulis "belum ada di rak" |
| Catatan penerimaan `TPL-04` | ✅ | Bagian "Ambang dan sumbernya" wajib terisi - titik celah ④ paling sering tersamar |

**Keterbatasan kerangka:** tidak ada TEMPLATE-BERITA-ACARA khusus uji mekanik (lihat celah ④
butir 2); pakai "Rangka umum - berlaku untuk semua jenis" (bagian 1 berkas itu) dan nyatakan
bahwa jenis uji mekanik belum punya template khusus.

---

## Status rantai

**TERBIMBING SAMPAI MATA ④.** Mata ①-③ dan ⑤ tersusun dengan setiap angka bertanda `[R-n]`
dan halaman yang dibuka ulang terhadap vault hari ini. Mata ④ jujur tanpa ambang: domain ini
memasok metode hitung; ambang terimya milik kontrak/standar R1-R2 yang belum ada di rak, dan
untuk objek keselamatan diserap rantai K yang sendiri putus di ④.

**Kapan rantai ini boleh disebut utuh:** setelah (a) verifier menaikkan daya-ikat resume
`pending_verification` (REF-MEC-002..007), (b) insan menandatangani unit KEMAMPUAN.md domain
ini (79/79 masih `draft-tidak-terverifikasi-insan`; register induk 0/341 keputusan terisi per
baris GAP-022), dan (c) ambang terima mekanikal punya sandaran R1/R2 atau adopsi kontrak tertulis.

---

## CATATAN SILANG-PEMILIK (temuan di luar LOCK, dilaporkan, TIDAK ditambal di sini)

Tertanggal 11-10-2026, kartu t_20c6706f. Berkas-berkas berikut bukan milik LOCK ini sehingga
tidak disunting.

1. **Tabrakan nama rantai (enam rantai tanpa huruf).** Blueprint 02 baris 31 mewajibkan
   "25/25 domain punya RANTAI bermata"; enam rantai langkah 15-17 (dua kartu saudara
   berjalan paralel: t_9b7ace41, t_bcbb928d) belum dialokasikan hurufnya oleh TA. Rantai
   berjalan sampai R. Kartu ini memakai "W" (dan mitra SOFTWARE-DATA-nya "X") ad-hoc;
   bila controller mengalokasikan huruf lain untuk langkah 15-17, ganti kepala. Dugaan
   alokasi berurutan langkah: S,T = pasangan-1; U,V = pasangan-2; W,X = ini.
2. **KEMAMPUAN.md FLD-007 membawa dua angka transisi berbeda.** Baris jangkar W9B mencetak
   "Re ≤ 2000 laminar di pipa (pdf_p479/cetak 461) - vault menang atas kw hulu '2100'", tetapi
   teks vault PDF 479 yang terbuka hari ini berbunyi "less than approximately **2100** for
   laminar ... greater than approximately 4000". Angka 2000 di baris itu justru cocok dengan
   ilustrasi panjang-masuk PDF 466 ("Le ≈ 120D for Re ≈ 2000"), bukan dengan ambang transisi.
   Pemilik: jalur W9B/`KEMAMPUAN-REGISTER.csv` (digest mesin) - mediasi controller.
3. **Resume Shigley (REF-MEC-001) tidak memuat jangkar halaman** padahal resume enam buku
   lain gelombang W3b memuat peta bertanda `[R3, ..., PDF n]`; kartu REF-MEC-001 bagian
   "Halaman jangkar: -". Rantai ini mengisi tiga jangkar Shigley dari buka-ulang sendiri
   (PDF 425/1042/1057-1058); pemilik resume perlu menyelaraskan format.
4. **KATALOG-RUMUS.md tidak punya seksi mekanikal** (ukur grep = 0) padahal 79 unit
   kemampuan domain ini menunggu rumus tertambat; pengisian katalog bukan wewenang LOCK ini -
   usulan ke langkah 25-26 / pemilik katalog.
5. **Machinery's Handbook PDF 2227 ≠ folio 2227.** Kepala resume memperingatkan folio tidak
   seragam; hari ini terukur offset +7 pada empat halaman isi (1396/678/656/982) tetapi blok
   daftar isi PDF 2227 membawa folio 2556 - jangan pakai konversi linear untuk berkas ini.
