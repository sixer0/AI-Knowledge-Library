---
id: civil-structural-korpus-ekas-0929
type: catatan
title: Korpus CIVIL-STRUCTURAL EKAS - peta, metode, ambang, dan batas pengetahuan (CVLK-0929)
status: active
verifikasi-oleh: menunggu gsp-custodian - naiknya status dari perlu_revisi adalah wewenang custodian, bukan penulis
verifikasi-pada: "-"
catatan_verifikasi: "VERDICT ITERASI-2: terverifikasi (gsp-custodian 2026-09-29; cakupan = uji 3 tambalan iterasi-1 terhadap rak nyata + guard integritas, BUKAN audit 7 dimensi ulang sesuai preseden D4-L2C). T-1 LOLOS - ukur AG:167-169 (pemilik menetapkan ambang tertulis / kontrak menyebut standar / laporkan hasil ukur) vs RANTAI-K:114-119 (kontrak menyebut standar / perhitungan ditandatangani ahli bersertifikat / nyatakan hasil ukur tanpa pernyataan lulus): hanya jalan ke-3 yang sama, jalan 1-2 beda mekanisme, dan larangan jalan ke-3 untuk menara/dudukan ketinggian memang hanya hidup di RANTAI-K:121-122 (token menara|ketinggian di ASSURANCE-GATES.md = 0 hit), jadi redaksi baru di objek baris 127 dan 338-341 benar. T-2 LOLOS - parse csv.DictReader MASTER-REFERENCE-REGISTER.csv: 62 baris data, r_level==R5 tepat 3 = REF-SEC-003 CYBERSECURITY + REF-SEC-004 CYBERSECURITY + REF-SWD-001 SOFTWARE-DATA, CIVIL di R5 = 0 (objek baris 209). T-3 LOLOS - wc -l ekas/02_REGISTERS/GAP-REGISTER.md = 165 (objek baris 125 dan 452). Konsistensi objek-vs-hulu pada tiga butir ini cocok (studi baris 18, 247-248, 297-300). Guard LOLOS - yaml.safe_load utuh 25 kunci tanpa duplikat, tepat satu baris status, nilai catatan_verifikasi/riwayat-catatan-verifikasi/catatan_keputusan utuh berkutip ganda tanpa # terpotong, body non-ASCII=0, blok BATAS PENGETAHUAN + status PUTUS @mata-4 + PROTOKOL KESELAMATAN + register KD-C1..C9 utuh; diff body vs backup-pra-revisi-iter1 = 5 hunk seluruhnya redaksi relasi/atribusi/basis-hitung, angka di luar hunk identik dan token selisih (166 jadi 165, 121, 122, enumerasi jalan 1/2/3) seluruhnya terverifikasi ke rak. Suntingan verdict ini HANYA 2 baris frontmatter (status + catatan_verifikasi); md5 body dipatok baa1b3a524339b537ab413566983cb19 tidak berubah. Kunci verifikasi-oleh/verifikasi-pada sengaja tidak disentuh sesuai cakupan suntingan dispatch; librarian mengisi keduanya saat promosi. INFO label (bukan cacat isi): catatan iterasi-1 menyebut objek baris 127/338/449, koordinat kini 127/338-341/452 karena tambalan menambah baris."
sumber: "docs/2026-09-29-cvl-knowledge-register/research/civil-structural-korpus-detail.md (hulu: studi t_d146e3b1 vonis LAYAK, 555 baris / 42.699 B; 5 berkas domain + 4 kartu REF-CIV dibaca penuh + 15 pendukung, terdaftar di Bagian 1 objek ini)"
halaman: "marker [R-n, sumber, hal] per butir di body dipertahankan verbatim dari studi: RANTAI-K (RANTAI-JAMINAN.md CIVIL-STRUCTURAL) :3-6,:8,:10-12,:25-28,:32-34,:57-69,:71-73,:75-83,:89-93,:105,:109-110,:112-122,:117-122,:128-138,:144,:149-150,:152-154; resume Hibbeler:22-33,47-58; Segui:18-30,34-38,50-54; Darwin:20-32,34-38,43-49; Mamlouk:20-33,37-39,46-53; kartu REF-CIV-001..004:19-47; koordinat lapis teks ditulis 'berkas:baris'"
tanggal_akses: 2026-09-29
kelas_bukti: sintesis
sensitif: tidak
perkara: cvlk-0929
tags: [civil-structural, struktur-penopang, analisis-struktur, beton-bertulang, baja-struktural, bahan-sipil, angkur, sambungan-las, tekuk, lendutan, penyaluran, dudukan-perangkat, menara-antena, tiang-kamera, SNI-1726, SNI-1727, SNI-1729, SNI-2847, AISC, ACI-318, ASTM, ASCE-7, rantai-K, nol-R1, nol-R2, ambang-tidak-ada, ahli-bersertifikat, known-defect]
links: [ekas/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL, ekas/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL, ekas/05_DOMAIN-KNOWLEDGE/BUILDING-CONSTRUCTION, ekas/05_DOMAIN-KNOWLEDGE/MECHANICAL, docs/2026-09-29-cvl-knowledge-register/research/civil-structural-korpus-detail.md]
defek-terkait: register known-defect KD-C1..KD-C6, KD-C8, KD-C9 (8 bertahan terukur) tercantum di Bagian 6.2 objek ini; KD-C7 dan KD-C10 gugur ber-bukti dan tidak dibebankan ke rilis. Penandaan di lapis rak menunggu kartu D1-FIXx (hanya-tambah); usulan celah U-1..U-4 menunggu penomoran controller (V-16) - vonis rilis domain ditahan sampai tanda terpasang
penulis: gsp-engineering-analyst
diajukan: 2026-09-29
domain: CIVIL-STRUCTURAL
created: 2026-09-29
riwayat-catatan-verifikasi: "Verdict: perlu_revisi (gsp-custodian 2026-09-29; sampling 42/42 koordinat cocok ke rak nyata; 7 dimensi mekanik LOLOS: yaml safe_load utuh 25 kunci tanpa duplikat, nilai tanpa kutip berisi # nol, title==H1, predikat tabel 6.3 sama dengan hulu RD23/LG7/BTC6/DT11=47, anatomi Batas-domain+Bagian 1-8 dan rantai mata 1-5 lengkap, blok BATAS status PUTUS @mata-4 utuh tanpa perataan beserta PROTOKOL KESELAMATAN + tabel boleh/tidak-boleh + usia bahan + pointer adjacency, register KD-C1..C6/C8/C9 bertahan 8 dan KD-C7/KD-C10 gugur tercatat, 6.3.4 pernyataan larangan tanpa angka nilai, body non-ASCII=0, 23/23 jalur rak yang disebut ada di disk). Alasan spesifik: (1) klaim \"pola tiga jalan ini identik dengan mekanisme generik [ASSURANCE-GATES.md:167-172]\" (objek baris 127 dan 338) TIDAK terukur identik - AG:167-169 adalah pemilik-menetapkan-ambang-tertulis / kontrak-sebut-standar / lapor-hasil-ukur-tanpa-lulus, sedangkan RANTAI-K:114-119 adalah kontrak-sebut-standar / ahli-bersertifikat-menandatangani / lapor-hasil-ukur-tanpa-lulus; hanya jalan ke-3 yang sama, jalan 1-2 beda mekanisme, dan larangan jalan-3 untuk menara hanya ada di RANTAI-K; (2) Bagian 2.5 \"baris R5 = 3, semuanya CYBERSECURITY\" salah atribusi - ukur MASTER-REFERENCE-REGISTER.csv: REF-SEC-003 dan REF-SEC-004 = CYBERSECURITY, REF-SWD-001 = SOFTWARE-DATA; (3) KD-C2 \"GAP-REGISTER.md (166 br)\" meleset satu - wc -l = 165, angka 166 lahir dari count(chr(10))+1 pada berkas yang berakhiran baris baru. Rekomendasi konkret: ganti kata \"identik\" menjadi \"sejalan pada jalan ke-3; jalan 1-2 berbeda (induk memakai penetapan ambang oleh pemilik, rantai K memakai kontrak-standar lalu ahli bersertifikat)\" di kedua tempat; tulis sensus R5 menjadi \"3 baris: 2 CYBERSECURITY + 1 SOFTWARE-DATA, sipil nol\"; nyatakan basis hitung baris MD atau pakai 165. Ketiga butir adalah salinan setia dari studi hulu (research/civil-structural-korpus-detail.md baris 297-298, 247-248, 443) sehingga perbaikan wajib dilakukan di HULU JUGA agar tidak propagasi. Nol angka teknik berubah dan blok BATAS wajib tetap terbit apa adanya - meratakannya tetap cacat. Kunci verifikasi-oleh/verifikasi-pada sengaja tidak disentuh sesuai cakupan suntingan dispatch; librarian mengisi keduanya saat promosi."
catatan_keputusan: "dipromosikan: CVLK-0929 C1-L2: verdict custodian independen terlampir di catatan_verifikasi, non-sensitif non-dosir; blok status rantai PUTUS @4 + pernyataan batas SNI + PROTOKOL KESELAMATAN terbit apa adanya; 11 butir DILARANG TERBIT naik hanya sebagai pernyataan larangan tanpa angka"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-29
dipromosikan-ke: catatans/civil-structural-korpus-ekas-0929.md
---

# Korpus CIVIL-STRUCTURAL EKAS - peta, metode, ambang, dan batas pengetahuan (CVLK-0929)

Objek master misi CVLK-0929 (id `civil-structural-korpus-ekas-0929`, type catatan, domain
CIVIL-STRUCTURAL = D1). Muatan = peta rak + metode acuan + rantai jaminan mata 1-5 + ambang
yang TIDAK ada + register known-defect + celah resmi + batas kemampuan, dalam satu berkas
(granularitas SATU objek master per domain; bentuk mengikuti preseden SDCY-0928 seksi 1-8).

Provenans: body ini dirakit dari SATU sumber,
`docs/2026-09-29-cvl-knowledge-register/research/civil-structural-korpus-detail.md` (studi
t_d146e3b1 status complete, 555 baris, 42.699 B, ekstraksi read-only dari lapisan teks [`ekas/`](../../ekas-lapis-teks/)
oleh gsp-engineering-analyst pada 2026-09-29; vonis kelayakan LAYAK non-penghenti per V-7; bukti
ukur `research/civ/measurement-report.txt` ts 2026-09-29T01:51:22Z + `measurement-report-2.txt`
ts 01:52:39Z; short check `research/civ/short-check-result.txt` VERDICT PASS ts
2026-09-29T01:59:41Z). Tidak ada pembacaan ulang korpus untuk angka baru pada giliran ini. Kelas
bukti objek: sintesis - kekuatan utamanya R3 buku (Hibbeler, Segui, Darwin, Mamlouk) berupa
METODA dan PETA LOKASI, campuran pengukuran lapis teks run ini; domain ini NOL R1, NOL R2, NOL
R5 (terukur), jadi tidak ada satu pun angka ambang yang bersandar norma. Pemisahan ditegakkan
lewat penanda `[R-n, sumber, hal]` per butir dan blok BATAS PENGETAHUAN di Bagian 8. Yang tidak
ada di rak dinyatakan "tidak ada di rak" beserta sumber yang seharusnya.

PERNYATAAN BATAS STANDAR (wajib ikut terbit; [R3, RANTAI-JAMINAN.md:3-6]): korpus ini TIDAK
dapat menyatakan pemenuhan SNI 1726 (ketahanan gempa), SNI 1727 (beban minimum), SNI 1729
(struktur baja), maupun SNI 2847 (struktur beton), karena keempatnya tidak ada di rak - nol R1
dan nol R2 relevan untuk domain ini (terukur, Bagian 2.1-2.2). Padanan Amerika dari buku-buku
R3 di rak (ASCE 7, AISC 360, ACI 318, ASTM) juga tidak ada di rak, sehingga tidak ada jalur
"pakai saja sumber induknya sebagai R2". Setiap pekerjaan yang memakai objek ini wajib membawa
pernyataan ini apa adanya; gerbang G6 menuntutnya tertulis di bukti serah.

Catatan wewenang: tidak ada PDF primer yang dibuka pada misi ini; vonis halaman = vonis LAPISAN
TEKS; verifikasi per halaman wewenang manusia (AGENTS.md; preseden SDCY catatan-2). Lokasi dan
byte PDF primer terukur di Bagian 1.4; laci [`ekas/03_SOURCE-VAULT/`](../../ekas-lapis-teks/03_SOURCE-VAULT/) di workspace hanya cermin.

Kepatuhan tipografi: rak asal memakai tanda bujur tengah (U+00B7) dan pisahan panjang (U+2014) -
terukur per berkas pada bagian [13] laporan ukur (mis. RANTAI-JAMINAN.md: A1=28, A2=34). Objek
ini nol kedua karakter itu; kutipan ditulis ulang dengan pemisah ASCII, angka/jalur/baris
disalin persis.

---

## Batas domain - apa yang TIDAK dicakup objek ini

| Area | Status cakupan | Alasan / kemana |
|---|---|---|
| Analisis gaya dalam (beban, determinasi, truss, portal) | CAKUP (metode) | Hibbeler [R3] |
| Perancangan beton bertulang (lentur, geser, penyaluran, kelayanan, kolom) | CAKUP (metode) | Darwin/Dolan/Nilson [R3] |
| Perancangan baja (ASD/LRFD, tarik, tekuk, balok, sambungan) | CAKUP (metode) | Segui [R3] |
| Sifat bahan sipil (tegangan-regangan, baja, agregat, semen, beton, aspal, kayu) | CAKUP (penjelasan bahan) | Mamlouk [R3] |
| Ambang lulus/tidak lulus struktur (SNI 1726/1727/1729/2847) | TIDAK DAPAT dicakup | keempatnya tidak ada di rak; GAP-015..018 [csv:16-19] |
| Prosedur uji bahan normatif (ASTM/SNI uji) | TIDAK dapat dicakup | tidak ada di rak; GAP-020 [csv:21] |
| Standar las (visual/NDT) sebagai acuan ambang | TIDAK dapat dicakup | disebut tanpa sumber di [RANTAI-K:104]; gap YATIM - usulan U-1 |
| Bangunan tempat perangkat dipasang | ADJACEN, provenance terpisah | domain BUILDING-CONSTRUCTION (Ching REF-BLD-001); RANTAI-K hanya memakai pointer [V-15; LG-05] |
| Mekanika teknik mesin (gandar, pegas, komponen mesin) | TIDAK dicakup | domain MECHANICAL (Shigley) - KATALOG-RUMUS.md:607 menunjuk ke sana, BUKAN ke sipil |
| Pondasi/geoteknik lanjut (daya dukung, tiang pancang) | NYARIS TIDAK tercakup | rak sipil tanpa buku geoteknik; hanya sisi beton pondasi Darwin; "tidak ada di rak" |
| Angka produk (kapasitas angkur, mutu baut, mill cert) | TIDAK ada | R4 per proyek (GAP-014 [csv:15]) - "menunggu data pabrikan" |
| Kode bangunan Indonesia (PPI/UBAPPI) | TIDAK ada | bukan domain ini; tercatat di D3 dan usulan U-2 |

---

## Bagian 1 - Peta isi

Path memakai NAMA FOLDER NYATA di disk. Uji keberadaan = baca langsung/ls, bukan glob.

### 1.1 Lapis domain [`ekas/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL/) (5 berkas, 395 baris, 17.613 B terukur; cetakan alat [1])

| Berkas | Baris | Byte | Peran |
|---|---|---|---|
| `RANTAI-JAMINAN.md` | 154 | 7.860 | Rantai K mata 1-5, status PUTUS @4 ditulis jujur di kepala dan ekor |
| `R3 - Structural Analysis (Hibbeler).md` | 68 | 3.087 | REF-CIV-001, gaya dalam (menara antena, tiang kamera, rangka atap, dudukan panel surya) |
| `R3 - Design of Concrete Structures (Darwin, Dolan & Nilson).md` | 58 | 2.242 | REF-CIV-002, beton |
| `R3 - Steel Design (Segui).md` | 58 | 2.226 | REF-CIV-003, baja (paling sering dibutuhkan di GSP) |
| `R3 - Materials for Civil and Construction Engineering (Mamlouk & Zaniewski).md` | 57 | 2.198 | REF-CIV-004, bahan |
| TOTAL | 395 | 17.613 | cocok nominasi blueprint (395 baris; F-10 terselesaikan: ukur 17.613 B); domain kedua tertebal batch ini (nominasi 01 S4: GROUNDING 548 > CIVIL 395 > DRAWING 236 > CONSTRUCTION 189 > BUILDING 142 baris lapis teks) |

### 1.2 Lapis kartu [`ekas/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/CIVIL-STRUCTURAL/) (4 x 47 baris = 188 baris / 7.508 B terukur; cetakan [2])

| Kartu | Buku | Status | Wewenang ambang | Catatan |
|---|---|---|---|---|
| `REF-CIV-001.md` | Hibbeler, Structural Analysis | ACTIVE | no-unless-contract-adopts | ambang "Tidak sendirian" + batas nasional [:21-31]; penandaan PROJECT-DERIVED/OEM-DERIVED, orang kedua = ahli bersertifikat [:43-47] |
| `REF-CIV-002.md` | Darwin/Dolan/Nilson, Design of Concrete Structures | ACTIVE | no-unless-contract-adopts | pola sama [:19-31] |
| `REF-CIV-003.md` | Segui, Steel Design | ACTIVE | no-unless-contract-adopts | pola sama [:19-31] |
| `REF-CIV-004.md` | Mamlouk & Zaniewski, Materials | ACTIVE | no-unless-contract-adopts | menopang G4/G5 [:35] |

Klasifikasi ini cocok dengan `MASTER-REFERENCE-REGISTER.csv:32-35` (semua ACTIVE, wewenang
ambang seragam `no-unless-contract-adopts`, catatan "diresume 21 Agu 2026 - metode berlaku,
angka/pasal berbasis standar Amerika"; total register 63 baris, terukur [4]). Rasio kartu:resume
4:4, struktur bersih (tidak seperti DRAWING-CAD 6:5 - domain ini tidak kena).

### 1.3 Lapis bersama (baris terkait sipil-struktur)

| Berkas | Letak | Yang dipasok |
|---|---|---|
| [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../../ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) | seluruh berkas | SIFAR entri struktur (sapuan beton/baja tulangan/angkur/lendut/tekuk/truss/rangka batang/Segui/Hibbeler/Darwin/Mamlouk/SNI 17/SNI 28 = 0 hit, terukur [8]); jembatan pertanyaan-rumus-buku-halaman untuk sipil BELUM ADA (KD-C6) |
| `KATALOG-RUMUS.md` | :607 | baris "Struktur & mekanik" menunjuk `R3/MECHANICAL/` (Shigley), BUKAN domain ini |
| [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) | :71 | 0 entri sipil (1 hit "Struktur lapisan tanah" = geologi pembumian, bukan struktur); CALCULATION-REGISTER.csv 0 baris sipil |
| [`ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md`](../../ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md) | :75-87 | 0 baris CIVIL di seluruh berkas; bagian "Belum ada sumber sah" memuat 7 baris (resistansi pembumian, ONVIF, PUIL, TIA-568, MTS, IEEE 450, IEC 61280-4-1) dan TIDAK memuat satu pun ambang struktur (terukur [C]; cacat kelengkapan silang KD-C4) |
| [`ekas/02_REGISTERS/GAP-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv) | :16-19, :21 | GAP-015/016/017/018 (TINGGI) + GAP-020 (MENENGAH); sensus se-register R1 = 9 baris, R2 = 8 baris, 21 baris data |
| [`ekas/02_REGISTERS/GAP-REGISTER.md`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.md) + `GAP-ACQUISITION-PLAN.md` | seluruh berkas | TIDAK sinkron dengan CSV: MD (165 br via wc -l, basis 19 Agu) memuat 0 token '1727/1726/1729/2847/GAP-015..020/AHSP/ASTM'; plan 0 CIVIL (terukur [B]) - sumber kebenaran = CSV (KD-C2) |
| [`ekas/02_REGISTERS/ASSET-REFERENCE-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/ASSET-REFERENCE-REGISTER.csv) | 1 baris | nol CIVIL (terukur) |
| [`ekas/01_GOVERNANCE/ASSURANCE-GATES.md`](../../ekas-lapis-teks/01_GOVERNANCE/ASSURANCE-GATES.md) | :42-92, :129-132, :167-172 | pemetaan gate G2-G5; "G4 tidak dapat ditutup selama G3 terbuka bila ambangnya berasal dari hitungan sendiri"; tiga jalan sah rantai putus (pola generik; sejalan dengan RANTAI-K:112-122 pada jalan ke-3 - jalan 1-2 berbeda: induk memakai penetapan ambang tertulis oleh pemilik dan kontrak menyebut standar, rantai K memakai kontrak menyebut standar lalu ahli bersertifikat menandatangani) |
| [`ekas/BACA-DULU.md`](../../ekas-lapis-teks/BACA-DULU.md) | :54-58, :72-74 | tabel tiga rantai putus (D, J, K) + contoh profil pemakaian tabel profil Segui |
| [`ekas/00_START-HERE/README.md`](../../ekas-lapis-teks/00_START-HERE/README.md) | :48-49, :70-72, :74-77, :79-81 | aturan ambang terima R1/R2, angka produk R4, R5 bukan sandaran akhir; klaim "empat celah R1" basi vs sensus 9 (KD-C3) |
| `ekas/03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/{SNI,PUIL,OTHER-REGULATION,PERMENAKER,SKKNI}/_ISI.md` | 5/5 | KOSONG terukur [7] |
| [`ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/`](../../ekas-lapis-teks/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/) | sapuan | token AISC/ACI/ASTM/ASCE = 0 (terukur [7]) |
| [`ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL/_ISI.md`](../../ekas-lapis-teks/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL/_ISI.md) | :3-6 | klaim `INTAKE_ONLY`/"belum diresume" - KONTRADIKSI dengan 4 resume + 4 kartu ACTIVE (KD-C1) |

### 1.4 Lapis laci sumber - jalur logis vs fisik nyata

Empat PDF primer nyata di
`C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CIVIL-STRUCTURAL/` (stat
berkas terukur, TIDAK dibuka oleh agen): Hibbeler 60.199.215 B; Segui 36.421.142 B; Darwin
24.226.949 B; Mamlouk 18.859.078 B; total 139.706.384 B. Laci [`ekas/03_SOURCE-VAULT/`](../../ekas-lapis-teks/03_SOURCE-VAULT/) di
workspace = cermin (preseden SDCY K-6), bukan kehilangan berkas. Manifest laci mengklaim
INTAKE_ONLY dan itu BASI (KD-C1): resume dibuat 21 Agu setelah intake 20 Agu, manifest tidak
disunting. Objek ini TIDAK mengutip status INTAKE_ONLY.

Tabel PDF primer (judul + jumlah halaman = KLAIM RESUME, wewenang verifikasi manusia): Hibbeler
Structural Analysis 2017 Pearson 736 hal / 274 bookmark [resume:22-33]; Segui Steel Design 2017
Cengage 771 hal / 128 bookmark [resume:18-30]; Darwin/Dolan/Nilson Design of Concrete Structures
801 hal / 277 bookmark [resume:20-32] (tahun 2015 hanya dari nama berkas PDF, header resume tanpa
tahun - KD-C8/BTC-03); Mamlouk & Zaniewski Materials 661 hal / 412 bookmark [resume:20-33]
(tahun 2018 hanya dari nama berkas PDF). Adjacency: Ching, Building Construction Illustrated
(domain BUILDING-CONSTRUCTION, REF-BLD-001) - pointer PDF 115/157 diuji silang cocok resume
ching:23-24, dibawa HANYA sebagai penunjuk lintas domain (V-15), bukan materi objek ini.

---

## Bagian 2 - Nol R1, nol R2: tidak ada angka ambang struktur di rak

Rantai K menyatakan eksplisit di kepala dokumen: "RANTAI INI PUTUS DI MATA 4 ... Tidak ada
satu pun SNI struktur di rak ... ambang lulus/tidak lulus tidak dapat ditetapkan dari rak ini"
[R3, RANTAI-JAMINAN.md:3-6]. Status rantai: "METODE LENGKAP - AMBANG TIDAK ADA"
[R3, RANTAI-K:144]. Konsekuensi pengikat: TIDAK ADA angka domain ini yang boleh naik sebagai
ambang lulus/tidak lulus (ambang terima menuntut R1/R2 [README.md:70-72]; angka melekat produk
menuntut R4 [README.md:74-77]).

### 2.1 Lapis R1 (regulasi/SNI Indonesia): KOSONG - terukur

Kelima laci R1 `_ISI.md` menyatakan KOSONG: SNI, PUIL, OTHER-REGULATION, PERMENAKER, SKKNI
(terukur [7]). Untuk struktur: SNI 1727 (beban minimum), SNI 1726 (gempa), SNI 1729 (baja),
SNI 2847 (beton) - keempatnya tidak ada di rak [R3, RANTAI-JAMINAN.md:25-28;
GAP-REGISTER.csv:16-19]. Jawaban kanonik untuk semua pertanyaan angka R1 struktur: "tidak ada
di rak; sumber yang seharusnya: salinan resmi SNI 1726/1727/1729/2847".

### 2.2 Lapis R2 (standar internasional): KOSONG untuk domain ini - terukur

Sapuan seluruh `_ISI.md` laci R2: token AISC/ACI/ASTM/ASCE = 0 (terukur [7]). Konfirmasi silang
klaim internal rak: "R2_INTERNATIONAL-STANDARDS tidak memuat AISC, dan R1 tidak memuat SNI
1729" [R3, Segui resume:54]; ASTM tidak ada di rak [R3, Mamlouk resume:52-53]; GAP-020 R2 metode
uji [csv:21]. Jadi bahkan standar ASLI buku-buku R3 ini (AISC 360, ACI 318, ASTM C39 dsb.,
ASCE 7) tidak ada.

### 2.3 Lapis R3 (empat buku): yang ADA adalah LOKASI dan METODA, bukan nilai ambang

Pointer halaman yang dipakai rantai K, terverifikasi silang rantai-vs-resume (uji [10], selisih
nol semua, 18/18 koordinat):

| Buku | Pointer halaman yang dipakai rantai K | Status uji silang |
|---|---|---|
| Hibbeler | PDF 21, 63, 108, 114, 128 | semua muncul di resume: OK |
| Segui | PDF 38, 58, 124, 202, 392 | semua muncul di resume: OK |
| Darwin | PDF 95, 145, 194, 239, 288 | semua muncul di resume: OK |
| Mamlouk | PDF 22, 110, 194, 288 | semua muncul di resume: OK |
| Ching (adjacency) | PDF 115, 157 | cocok resume BUILDING ching:23-24: OK (pointer saja, V-15) |

Frekuensi token dalam domain (terukur [12]): 'SNI' 29, 'tidak ada di rak' 12, 'las' 13,
'angkur' 9, 'AISC' 7, 'ACI' 5, 'ASTM' 3, 'ahli bersertifikat' 3, 'ASCE' 2, 'torsi' 1. Profil
ini sendiri adalah bukti muatan domain: teks sipil rak ini lebih banyak berbicara tentang
KEABSENAN (SNI / tidak ada di rak) dan KESELAMATAN (ahli / angkur / las) daripada tentang angka.

### 2.4 Lapis R4 (produk): per proyek, by-design

Kapasitas angkur, mutu baut, torsi prategang, mill certificate baja, hasil uji tekan beton riil
= R4 per proyek [R3, RANTAI-K:30,45,102-105; GAP-014 csv:15 "Tidak diadakan - diminta ke
pabrikan tiap proyek"]. Satu-satunya baris uji mata 4 yang tidak putus justru baris R4: "Uji
tarik angkur (pull-out): Kapasitas lembar data [R4] x faktor keamanan - R4 sah bila lembar
datanya ada" [R3, RANTAI-K:105,109-110]. Semua pemakaian angka ini di objek IL wajib berlabel
"menunggu data pabrikan" bila lembar data belum ada.

### 2.5 Lapis R5: KOSONG untuk domain ini

Tidak ada tesis/panduan sipil di MRR (sensus run ini: baris R5 = 3 - 2 CYBERSECURITY + 1 SOFTWARE-DATA; sipil nol).
`INTAKE-RINGKAS.md:41` mencatat CIVIL-STRUCTURAL = 4 berkas (semua R3). R5 tidak pernah jadi
sandaran akhir [README.md:79-81] - di domain ini nol sehingga tidak relevan.

---

## Bagian 3 - Angka acuan per buku (pointer metode, bukan nilai)

### 3.1 Hibbeler, Structural Analysis (2017, Pearson) [R3, REF-CIV-001]

Ukuran 736 hal / 274 bookmark (klaim resume; PDF 60.199.215 B terukur, tidak dibuka). Peta bab:
bab 1 beban PDF 15/21; bab 2 idealisasi+determinasi PDF 47/63; bab 3 truss PDF 95, simpul 108,
potongan 114, rangka ruang 128; bab 4 gaya dalam PDF 151 [resume:22-33]. Untuk apa: menara
antena, tiang kamera, rangka atap, dudukan panel surya [resume:12-15]. Batas: metode bukan
ambang; ASCE 7 != SNI 1727/1726; wajib tanda tangan ahli [resume:47-58]. Menopang G2/G3 + rantai
D silang; celah tersisa SNI 1726/1727, AISC, ACI [resume:62-68].

### 3.2 Segui, Steel Design (2017, Cengage) [R3, REF-CIV-003]

Ukuran 771 hal / 128 bookmark (klaim resume; PDF 36.421.142 B terukur). Peta bab: bab 2 ASD/LRFD
PDF 38; tarik 58; tekan/tekuk 124; balok 202; balok-kolom 314; sambungan sederhana 392;
eksentris 492; komposit 608; girder pelat 682; apendiks 738 [resume:18-30]. Muatan praktik: yang
gagal hampir selalu SAMBUNGAN bukan batang; tiang/kaki menara = TEKUK yang menentukan
[resume:34-38]. Struktur standar AISC Specification tiga bagian (penunjuk baca PDF 24 - LOKASI
saja, konten halaman belum dibuka manusia, LG-04) [resume:40-43]. Batas: AISC + imperial; R2
tidak memuat AISC, R1 tidak memuat SNI 1729 [resume:45-54].

LABEL-GUARD wajib (RD-09): tabel profil baja di buku ini adalah profil Amerika (W/HP/HSS).
Padanan WF/H-beam SNI tidak ada di rak (GAP-017), jadi tabelnya TIDAK dapat dipakai langsung
untuk penampang yang dibeli di Indonesia.

### 3.3 Darwin/Dolan/Nilson, Design of Concrete Structures [R3, REF-CIV-002]

Ukuran 801 hal / 277 bookmark (klaim resume; PDF 24.226.949 B terukur; tahun 2015 hanya dari
nama berkas - KD-C8). Peta bab: bab 2 bahan PDF 39; dasar+asumsi fundamental 80; lentur 95;
geser 145; lekat/angkur/panjang penyaluran 194; kelayanan 239; torsi 266; kolom pendek 288;
kolom langsing 325; balok-portal tak tentu 358; pelat satu/dua arah 395/405 [resume:20-32].
Paling sering dipakai: bab 6 penyaluran dan bab 7 kelayanan [resume:34-38]. Batas: berbasis ACI
318; SNI 2847 turunannya tapi TIDAK identik - faktor reduksi dan detail berbeda; metode berlaku,
angka/pasal tidak untuk Indonesia; perancangan struktural menuntut tanda tangan ahli
[resume:43-54]. Klaim "sekitar 12% halaman tanpa lapis teks" = BTC-04 (perkiraan berlabel)
[resume:51-52].

LABEL-GUARD wajib (LG-06): pernyataan resume bahwa penyaluran dan lendutan adalah "dua hal
paling sering keliru di lapangan" adalah PERNYATAAN POLA PRAKTIK penulis resume - tidak ada
register insiden di rak sebagai bukti.

### 3.4 Mamlouk & Zaniewski, Materials for Civil and Construction Engineering [R3, REF-CIV-004]

Ukuran 661 hal / 412 bookmark (klaim resume; PDF 18.859.078 B terukur; tahun 2018 hanya dari
nama berkas - KD-C8). Peta bab: bab 1 konsep rekayasa bahan PDF 22; sifat dasar 77; baja 110;
aluminium 169; agregat 194; semen/air/bahan tambah 244; beton 288; pasangan 370; aspal 386;
kayu 469; komposit 523; apendiks 553 [resume:20-33]. Nilai utama: memeriksa pekerjaan pihak
ketiga - apa yang diuji pada beton datang, arti hasil uji tekan [resume:15-16]. Prinsip: luas di
bawah kurva tegangan-regangan = kerja per satuan volume; alamat "(terverifikasi, PDF 40 area)" =
BELUM TERKONFIRMASI [resume:37-39; BTC-05]. Batas: buku sifat bahan bukan perancangan; ASTM
tidak ada di rak; SNI setara tidak identik; menopang G4/G5 [resume:46-57].

LABEL-GUARD wajib (LG-03): klaim "412 bookmark - navigasi terbaik di laci ini" adalah
SUPERLATIF internal-laci, terverifikasi hanya terhadap empat resume sipil (412 > 277 > 274 >
128), bukan terhadap laci lain.

### 3.5 Konvensi halaman

Keempat buku R3 sipil dikutip lewat NOMOR PDF sebagaimana tercatat di lapis teks resume; lapis
teks TIDAK mencatat selisih cetak-PDF untuk domain ini (bandingkan SDCY yang mencatat selisih
per buku). Setiap nomor PDF yang dikutip di objek ini adalah pointer lapis teks, BUKAN vonis
halaman fisik - kandungan detail per halaman pointer BELUM TERKONFIRMASI (BTC-06) dan butuh
manusia sebelum angka apa pun dari halaman itu dipakai.

---

## Bagian 4 - Kerangka terapan: Rantai K mata 1-5

Judul rantai: "Rantai K - Struktur penopang perangkat" [RANTAI-K:1]. Rantai putus KETIGA setelah
D (pembumian) dan J (keamanan siber) [R3, RANTAI-K:8; BACA-DULU.md:54-58]. Peringatan khas rak,
wajib ikut terbit: struktur yang gagal menjatuhkan perangkat dan bisa menimpa orang
[R3, RANTAI-K:10-12].

### 4.1 Mata 1 - Rujukan [RANTAI-K:16-30]

Enam baris tersedia (Hibbeler, Segui, Darwin, Mamlouk, Ching adjacency, + R4 per proyek) dan
enam baris TIDAK ADA (SNI 1727, SNI 1726, SNI 1729, SNI 2847, ASTM/SNI uji, lembar data per
proyek). Kalimat kunci: "Empat buku R3, empat SNI kosong. Buku-buku itu berbasis ASCE 7, AISC,
ACI 318, dan ASTM - Amerika. Padanan Indonesianya diturunkan dari sana tetapi tidak identik"
[R3, RANTAI-K:32-34].

### 4.2 Mata 2 - Keputusan desain [RANTAI-K:39-46]

Enam keputusan dengan dasar dan ALTERNATIF YANG DITOLAK:

1. Jenis dudukan - bracket dinding DITOLAK bila partisi ringan (pointer adjacency Ching
   PDF 157).
2. Beban rancangan - memakai berat perangkat saja DITOLAK; angin pada antena/kamera sering
   lebih besar [LG-01].
3. Bahan - baja tanpa proteksi korosi DITOLAK di pantai/industri.
4. Konfigurasi sambungan - las lapangan tanpa pemeriksaan DITOLAK.
5. Jenis/kedalaman angkur - angkur pasca-pasang tanpa lembar data DITOLAK.
6. Siapa yang menandatangani - perhitungan hanya diperiksa internal DITOLAK untuk struktur
   yang menanggung keselamatan.

Penutup mata 2, wajib ikut terbit: "Rak ini membuat GSP mampu memeriksa dan berdiskusi dengan
ahli struktur - bukan menggantikannya" [R3, RANTAI-K:48-49].

### 4.3 Mata 3 - Perhitungan: urutan 6 langkah [RANTAI-K:55-93]

(1) tetapkan beban [Hibbeler PDF 21; angka wajibnya SNI] -> (2) periksa determinasi dan
kestabilan [PDF 63] -> (3) gaya batang [PDF 108/114/128] -> (4) kapasitas elemen [Segui/Darwin]
-> (5) sambungan dan angkur [Segui PDF 392 + R4] -> (6) kelayanan/lendutan [Darwin PDF 239]
[R3, RANTAI-K:57-69].

Peringatan langkah 2, wajib ikut terbit: "rangka tidak stabil tetap menghasilkan angka dari
perangkat lunak tetapi angkanya tidak berarti apa-apa" [R3, RANTAI-K:71-73].

Tabel beban rancangan [R3, RANTAI-K:75-83]: mati [R4]; angin [SNI 1727 - tidak ada di rak];
gempa [SNI 1726 - tidak ada di rak]; pemasangan/pemeliharaan (praktik); es/salju (tidak berlaku
Indonesia - asumsi geografi, LG-02).

Penandaan wajib [R3, RANTAI-K:89-93]: hasil hitung = PROJECT-DERIVED; beban SNI =
SOURCE-DERIVED [R1]; SELAMA SNI belum ada, beban ditandai ASSUMPTION + sensitivitas + rencana
penggantian. Ini sesuai aturan generik gate: "G4 tidak dapat ditutup selama G3 terbuka bila
ambangnya berasal dari hitungan sendiri" [ASSURANCE-GATES.md:129-132].

### 4.4 Mata 4 - Pengujian: MATA PUTUS [RANTAI-K:99-122]

Tujuh baris uji; enam ber-ambang "tidak ada di rak" atau kontrak; satu-satunya TAK-PUTUS = uji
tarik angkur terhadap lembar data [R4] [:105,109-110]. Tiga jalan sah selama SNI absen
[:112-122]: (1) kontrak menyebut standar lalu peroleh salinannya - ambang naik R1/R2, jalan
paling benar; (2) perhitungan ditandatangani ahli bersertifikat; (3) nyatakan hasil ukur TANPA
pernyataan lulus - hanya untuk pekerjaan non-selamat. Pola tiga jalan ini sejalan dengan mekanisme generik
[ASSURANCE-GATES.md:167-172] hanya pada jalan ke-3; jalan 1-2 berbeda (induk: pemilik
menetapkan ambang tertulis, lalu kontrak menyebut standar; rantai K: kontrak menyebut standar,
lalu perhitungan ditandatangani ahli bersertifikat), dan larangan jalan ke-3 untuk menara/
dudukan ketinggian hanya hidup di RANTAI-K:121-122.

### 4.5 Mata 5 - Bukti serah: sembilan lampiran [RANTAI-K:128-138]

Perhitungan bertanda tangan ahli; gambar as-built; sertifikat mutu bahan [R4]; hasil uji tarik
angkur; rekaman torsi baut; laporan pemeriksaan las; verifikasi dimensi/ketegakan (rantai L
survei); PERNYATAAN STANDAR YANG DIPAKAI (wajib - menyebut SNI mana yang diacu "atau bahwa
belum ada dan siapa yang menetapkan"); kartu kendali rantai berstatus "putus di mata 4".

### 4.6 Status rantai [RANTAI-K:142-154]

"METODE LENGKAP - AMBANG TIDAK ADA" [:144]. Empat celah R1 prioritas tinggi GAP-015..018.
Klaim [:149-150] bahwa menutup keempatnya mengubah rantai dari putus menjadi utuh sudah diuji:
OVERSTATED (KD-C9) - keempatnya menutup AMBANG desain (mata 1-3), bukan seluruh mata 4 (uji
bahan masih butuh GAP-020, las butuh standar yatim, angkur/baut butuh R4). Objek ini memakai
redaksi bertingkat, bukan klaim utuh. Baris penutup penting [:152-154]: "Jangan tertukar: rak
punya ambang tahanan isolasi [R2] dan delta-T termografi [R2], tetapi tidak punya satu pun
ambang struktur. Kemampuan menghitung bukan kewenangan menyatakan lulus".

---

## Bagian 5 - Ambang terima dan protokol keselamatan

### 5.1 Uji rantai K mata 4: apa yang boleh dan tidak boleh dikatakan

| Butir uji | Ambang | Kelas sumber |
|---|---|---|
| Uji tarik angkur (pull-out) | Kapasitas lembar data [R4] x faktor keamanan | SATU-SATUNYA tak-putus; sah bila lembar datanya ada |
| Kapasitas lentur/geser/tekuk elemen | TIDAK DAPAT DIUJI dari rak | ambangnya SNI 1729/2847 - tidak ada |
| Beban angin dan gempa per lokasi | TIDAK DAPAT DIUJI dari rak | SNI 1727/1726 + peta bahaya - tidak ada |
| Mutu beton / tegangan izin baja sebagai ambang lulus | TIDAK DAPAT dinyatakan | spesifikasi kontrak + SNI + mill cert [R4] |
| Pemeriksaan las visual/UT/RT | TIDAK DAPAT DIUJI dari rak | standar las = gap yatim (usulan U-1) + kontrak |
| Torsi baut prategang | TIDAK DAPAT dinyatakan | lembar data baut [R4] + SNI 1729 |
| Pemenuhan SNI 1726/1727/1729/2847 | TIDAK DAPAT DINYATAKAN | standarnya tidak ada di rak (nol R1) |

Sumber tabel: [R3, RANTAI-K:99-110] + Bagian 2. Kelas R3 (metode buku), R4 (lembar data), dan
kontrak dilarang diratakan menjadi "standar"; hanya R1/R2 sah jadi ambang terima
[README.md:70-72].

### 5.2 Kata "boleh / tidak boleh dikatakan" (redaksi operasional untuk editor proposal)

| Boleh dikatakan (dengan batas) | TIDAK BOLEH dikatakan (terlarang) |
|---|---|
| "Analisis mengikuti urutan enam langkah rantai K [R3, RANTAI-K:57-69]; determinasi dan kestabilan diperiksa sebelum gaya batang." | klaim "desain memenuhi SNI 1726/1729/2847/1727" atas dasar rak ini (DT-11) |
| "Metode perancangan mengacu buku teks R3 (Hibbeler/Segui/Darwin/Mamlouk); angka beban diambil sebagai ASSUMPTION dengan sensitivitas dan rencana penggantian sampai SNI 1727/1726 diperoleh." | angka beban/pasal/faktor reduksi dari buku Amerika disajikan sebagai nilai sah Indonesia (RD-10/RD-11 vs DT-02/DT-03) |
| "Profil baja yang dipakai adalah padanan SNI; tabel W/HP/HSS di buku sumber tidak dipakai langsung." | menghitung dengan penampang tabel W/HP/HSS lalu menyebutnya WF/H-beam SNI (RD-09) |
| "Uji tarik angkur mengacu kapasitas lembar data pabrikan [R4] dikali faktor keamanan; lembar data dilampirkan." | kapasitas angkur atau torsi baut tanpa lembar data (DT-07/DT-08) |
| "Struktur penopang perangkat diperiksa dan ditandatangani ahli bersertifikat." | perhitungan struktur selamat hanya diperiksa internal (RD-15; RANTAI-K:46) |

Aturan pengikat: di SEMUA lapis objek/rute/laporan ini DILARANG ada kalimat positif yang
menyatakan pemenuhan SNI struktur (DT-11; uji PENOLAKAN V-10: menulisnya = FAIL walau rute
memori hidup).

### 5.3 Mekanisme gerbang untuk rantai putus

Domain tanpa satu pun R1/R2 tidak dapat melewati G4 dengan cara biasa; pekerjaan tetap boleh
jalan dengan metode R3 + lembar data R4 ASALKAN tiga jalan sah [RANTAI-K:112-122] dipakai dan
pernyataan batas standar ikut di bukti serah [ASSURANCE-GATES.md:167-172].

### 5.4 Kedudukan di ambang induk: NOL baris

`AMBANG-TERIMA-INDUK.md` tidak punya satu pun baris CIVIL, termasuk di bagian "Belum ada sumber
sah" (:75-87, terukur 7 baris semuanya domain lain). Konsekuensi: objek ini tidak bisa menunjuk
baris induk sebagai rumah ambang; pernyataan "tidak dapat diuji"-nya hidup penuh di Rantai K.
Cacat kelengkapan silang ini tercatat KD-C4 (perbaikan = usulan U-4).

### 5.5 PROTOKOL KESELAMATAN (wajib ikut terbit bersama angkanya)

1. Zona keselamatan jiwa: struktur penopang perangkat yang gagal menjatuhkan perangkat dan bisa
   menimpa orang [R3, RANTAI-K:10-12].
2. Larangan keras jalan-3: "Jalan ke-3 tidak boleh dipakai untuk menara, dudukan di ketinggian,
   atau apa pun yang dapat jatuh menimpa orang" [R3, RANTAI-K:117-122]. Untuk menara/dudukan
   ketinggian HANYA jalan 1 (standar diperoleh via kontrak) atau jalan 2 (ahli bersertifikat
   menandatangani).
3. Orang kedua pemeriksa hitungan struktur = AHLI BERSERTIFIKAT, bukan rekan internal
   [REF-CIV-001..004 seksi 6; RANTAI-K:46].
4. Las lapangan tanpa pemeriksaan DITOLAK sebagai konfigurasi [RANTAI-K:44-45]; angkur
   pasca-pasang tanpa lembar data DITOLAK.
5. Selama GAP-015..018 terbuka, setiap pekerjaan struktur GSP: (a) angka beban = ASSUMPTION
   dengan sensitivitas 1/2x dan 2x + rencana penggantian [RANTAI-K:91-93]; (b) keluaran hanya
   lewat tiga jalan sah [RANTAI-K:112-122]; (c) untuk menara/dudukan ketinggian HANYA jalan 1
   atau 2; (d) bukti serah wajib memuat pernyataan standar yang dipakai [RANTAI-K:137].
6. Titik rawan praktik yang WAJIB diperiksa pada pekerjaan GSP: sambungan (baut kurang / las
   tidak penuh / pelat tipis), tekuk tiang dan kaki menara, panjang penyaluran kurang, lendutan
   tak diperiksa [R3, Segui resume:34-38; Darwin resume:34-38].

---

## Bagian 6 - Known-defect + tabel beban-rilis

### 6.1 Temuan kelas-nol (jawaban atas kelas yang diminta blueprint)

Sapuan terhadap lapis teks domain CIVIL-STRUCTURAL: 0 entri rumus struktur di KATALOG-RUMUS
(terukur [8]), 0 baris ambang CIVIL di AMBANG-TERIMA-INDUK (terukur [C]), 0 entri sipil di
ASUMSI-BAKU dan CALCULATION-REGISTER, keenam baris R1/R2 mata 1 berstatus TIDAK ADA. Jadi untuk
kelas angka nilai murni (nomor pasal SNI, koefisien kombinasi beban, faktor reduksi, kuat
nominal penampang, panjang penyaluran berkoefisien, tekanan angin / respons spektrum, torsi
baut, kapasitas angkur, kriteria terima las, mutu beton sebagai ambang): **lapis teks tidak
memuat angkanya sama sekali**. Vonis: tidak ada yang bisa dikontradiksikan dari rak, dan karena
itu angka kelas itu DILARANG TERBIT dari objek ini (DT-01..DT-11, 6.3.4). Pertanyaan "berapa
faktor reduksi lentur beton menurut rak?" dijawab benar hanya dengan "tidak ada di rak; sumber
yang seharusnya: SNI 2847 (GAP-018)" - menjawab angka apa pun = karangan = FAIL. Nama standar
(SNI 1726/1727/1729/2847, AISC, ACI 318, ASTM, ASCE 7) boleh disebut hanya sebagai nama +
status ketiadaan, bukan dengan angka isinya.

### 6.2 Register known-defect (koordinat = jalur:baris hasil ukur studi)

| ID | Butir | Bukti (koordinat) | Vonis sementara | Bebani rilis? |
|---|---|---|---|---|
| KD-C1 | Laci vault mengklaim INTAKE_ONLY / "belum diresume" | `_ISI.md:3-6` vs 4 resume di 05 + 4 kartu ACTIVE (MRR csv:32-35) | KONTRADIKSI terukur; catatan BASI (kelas SDCY K-5). Objek ini tidak mengutip status INTAKE_ONLY | ya (jalur provenans) |
| KD-C2 | Keluarga gap register MD tidak sinkron CSV | GAP-REGISTER.md (165 br via wc -l, basis 19 Agu) 0 token sipil; GAP-ACQUISITION-PLAN.md 0 CIVIL; CSV 21 baris data (terukur [B]) | Terukur; sumber kebenaran = CSV. Hilir DILARANG mengutip MD untuk statistik celah | ya (jalur statistik + rencana akuisisi) |
| KD-C3 | README "Empat celah R1" vs sensus CSV 9 baris R1 | README.md:48-49 vs ukur [3] | KONTRADIKSI terukur (sudah tercatat SDCY K-2; sipil menyumbang 4 dari 9). Kalimat "empat" jangan ikut terbit | ya |
| KD-C4 | AMBANG-TERIMA-INDUK tanpa satu pun ambang struktur di "Belum ada sumber sah" | :75-87 terukur 7 baris, CIVIL=0; padahal RANTAI-K putus @4 dan BACA-DULU mendaftarkan K sebagai rantai putus ketiga | Cacat KELENGKAPAN SILANG (kelas SDCY K-10); perbaikan = kartu FIX pengelola rak (usulan U-4) | ya (jalur gerbang) |
| KD-C5 | Standar las disebut tanpa entri gap | RANTAI-K:104 "standar las tidak ada di rak"; GAP-REGISTER.csv tidak punya baris las (sensus [3]) | GAP YATIM (kelas SDCY G-5/K-13); usulan U-1, nomor final wewenang controller (V-16) | ya (usulan) |
| KD-C6 | KATALOG-RUMUS nol rumus struktur meski 4 buku R3 ada | terukur [8] 0 hit; bandingkan domain lain punya seksi hitungannya | GAP EKSTRAKSI lapis-katalog (bukan gap koleksi). Wajib dinyatakan agar pengguna katalog TIDAK menyimpulkan "rak tidak punya metode struktur"; perbaikan = usulan U-3 | ya (eksplisitasi) |
| KD-C8 | Header resume tidak seragam tahun terbit | Darwin & Mamlouk tanpa "Terbit:"; Hibbeler & Segui 2017 eksplisit; tahun Darwin/Mamlouk hanya di filename PDF (2015/2018) | Inkonsistensi presentasi terukur; guard umur 15-th tidak dapat dieksekusi seragam dari lapis teks; semua calon umur <= 11 th (aman, berlabel) | ya (label BTC-03) |
| KD-C9 | Klaim "menutup GAP-015..018 membuat rantai utuh" | RANTAI-K:149-150 vs mata 4 :99-107 | OVERSTATED terukur; objek IL wajib memakai redaksi BERTINGKAT (4.6) | ya (redaksi objek IL) |

Dua calon defect TIDAK dibebankan ke rilis karena gugur ber-bukti: KD-C7 (pointer phantom
`ekas/03_ENGINEERING-CALCULATIONS/` di body kartu misi - alamat benar
[`ekas/06_ENGINEERING/CALCULATIONS/`](../../ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/); cacat sitasi kartu, bukan rak) dan KD-C10 (uji koordinat
meleset karena kasus-huruf alat ukur sendiri, sudah dikoreksi di short_check pass kedua).
KD-1/KD-6 blueprint DIKONFIRMASI terukur (RD-01, RD-17, RD-18, RD-20), tidak diulang sebagai
defect baru. Kontradiksi internal antar-resume: tidak ditemukan selisih angka antar-lapis-teks
untuk domain ini - semua pointer halaman cocok (uji [10]) dan tidak ada angka ambang yang bisa
dibenturkan karena memang nol.

### 6.3 Tabel BEBAN-RILIS (47 butir; predikat dari studi, objek ini WAJIB mematuhinya)

Predikat: READY = boleh terbit dengan penanda sumber; LABEL-GUARD = boleh terbit hanya dengan
label yang disebut; BELUM TERKONFIRMASI = butuh PDF primer oleh manusia; DILARANG TERBIT = tidak
ada sandaran di lapis teks. Jumlah per predikat diverifikasi ulang oleh alat terhadap tabel di
bawah (23 + 7 + 6 + 11 = 47), bukan dihitung tangan.

#### 6.3.1 READY (23 butir) - naik sebagai muatan

| ID | Butir | Marker sumber |
|---|---|---|
| RD-01 | Rantai K PUTUS di mata 4; ambang lulus tidak dapat ditetapkan dari rak | [R3, RANTAI-JAMINAN.md:3-6] |
| RD-02 | Empat celah R1 struktur: SNI 1727/1726/1729/2847 = GAP-015..018 TINGGI terbuka | [GAP-REGISTER.csv:16-19; RANTAI-K:25-28] |
| RD-03 | GAP-020 R2 metode uji ASTM/SNI MENENGAH terbuka | [csv:21; Mamlouk resume:52-53] |
| RD-04 | Satu-satunya baris uji tak-putus = uji tarik angkur terhadap lembar data [R4] | [R3, RANTAI-K:105,109-110] |
| RD-05 | Urutan hitung 6 langkah beban->determinasi->gaya batang->kapasitas->sambungan->lendutan | [R3, RANTAI-K:57-69] |
| RD-06 | Determinasi/kestabilan wajib sebelum gaya batang; software memberi angka tanpa makna bila rangka tak stabil | [R3, RANTAI-K:71-73] |
| RD-07 | Beban wajib: mati [R4], angin [SNI 1727 absen], gempa [SNI 1726 absen], pemasangan | [R3, RANTAI-K:75-83] |
| RD-08 | Tiga jalan sah selama SNI absen + larangan jalan-3 untuk menara/dudukan ketinggian | [R3, RANTAI-K:112-122] |
| RD-09 | Tabel profil Segui = W/HP/HSS Amerika; != WF/H-beam SNI; tidak dapat dipakai langsung | [R3, Segui resume:50-52; BACA-DULU.md:72-74; GAP-017 notes] |
| RD-10 | Metode buku boleh; angka beban/pasal tidak untuk pekerjaan Indonesia | [R3, Hibbeler resume:51-54; REF-CIV-001:31] |
| RD-11 | ACI 318 != SNI 2847: faktor reduksi dan ketentuan detail berbeda; pasal tidak dapat dikutip | [R3, Darwin resume:43-49; REF-CIV-002:31] |
| RD-12 | Peta bab->halaman keempat buku (lokasi pointer, terverifikasi silang 2.3) | [R3, resume masing-masing:20-32; RANTAI-K:20-23] |
| RD-13 | Titik rawan praktik: sambungan (baut kurang/las tidak penuh/pelat tipis), tekuk tiang, penyaluran kurang panjang, lendutan tak diperiksa | [R3, Segui resume:34-38; Darwin resume:34-38] |
| RD-14 | Penandaan angka: hitungan PROJECT-DERIVED; bahan OEM-DERIVED; beban tanpa SNI = ASSUMPTION+sensitivitas+rencana penggantian | [R3, RANTAI-K:89-93; REF-CIV-001:43-47] |
| RD-15 | Orang kedua pemeriksa hitungan struktur = ahli bersertifikat | [REF-CIV-001..004 seksi 6; RANTAI-K:46] |
| RD-16 | Sembilan lampiran bukti serah mata 5 termasuk pernyataan standar yang dipakai (wajib) | [R3, RANTAI-K:128-138] |
| RD-17 | Kelima laci R1 kosong (SNI/PUIL/OTHER/PERMENAKER/SKKNI) - terukur run ini | [ukur 2 [7]] |
| RD-18 | Laci R2 tidak memuat AISC/ACI/ASTM/ASCE - terukur run ini + klaim Segui resume:54 | [ukur 1 [7]; R3, Segui:54] |
| RD-19 | KATALOG-RUMUS nol entri struktur; baris "Struktur & mekanik" -> MECHANICAL/Shigley | [ukur 1 [8]; KATALOG-RUMUS.md:607] |
| RD-20 | AMBANG-TERIMA-INDUK nol baris CIVIL (7 baris "belum ada sumber sah" semuanya domain lain) | [ukur 2 [C]; :75-87] |
| RD-21 | Rantai K = rantai putus ketiga setelah D dan J | [R3, RANTAI-K:8; BACA-DULU.md:54-58] |
| RD-22 | Wewenang ambang keempat REF-CIV = no-unless-contract-adopts; status ACTIVE | [MRR csv:32-35 terukur] |
| RD-23 | Domain menopang gate: G2/G3 (analisis+beton+baja), G4/G5 (bahan) | [resume Menopang; REF-CIV-004:35; ASSURANCE-GATES.md:42-92] |

#### 6.3.2 LABEL-GUARD (7 butir) - naik HANYA dengan labelnya

| ID | Butir | Label wajib |
|---|---|---|
| LG-01 | "Beban angin hampir selalu menentukan pada dudukan antena/kamera di ketinggian; parabola kecil dapat menghasilkan gaya angin beberapa kali berat sendirinya" | PENALARAN-REKAYASA R3 tanpa angka; bukan nilai desain; hitung angin wajib dari SNI/standar sah |
| LG-02 | "Es/salju tidak berlaku di Indonesia" | ASUMSI GEOGRAFI tanpa sumber rak; nyatakan sebagai asumsi proyek tropis |
| LG-03 | "412 bookmark - navigasi terbaik di laci ini" (Mamlouk) | SUPERLATIF internal-laci; terverifikasi hanya terhadap 4 resume sipil (412 > 277 > 274 > 128) |
| LG-04 | Struktur AISC Specification tiga bagian (Segui PDF 24) | LOKASI-klaim R3; konten halaman belum dibuka manusia; pakai sebagai penunjuk baca dokumen tender |
| LG-05 | Pointer Ching PDF 115/157 dalam mata 1 dan mata 2 | ADJACENCY BUILDING-CONSTRUCTION (V-15); pointer bukan penyerapan; domain asal dipegang D3 |
| LG-06 | Klaim resume Darwin "paling sering keliru di lapangan: penyaluran & lendutan" | PERNYATAAN POLA PRAKTIK penulis resume; tidak ada register insiden di rak sebagai bukti |
| LG-07 | Pemakaian lintas-domain: menara hasil hitung K juga membawa terminal udara (rantai D) | RUJUKAN SILANG; ambang pembumian tetap urusan rantai D (putus juga) |

#### 6.3.3 BELUM TERKONFIRMASI (6 butir) - naik HANYA dengan labelnya, dilarang mengikat

| ID | Butir | Kenapa | Jalan konfirmasi |
|---|---|---|---|
| BTC-01 | Jumlah halaman 801/771/736/661 | Klaim header resume; lapis teks tidak bisa menghitung halaman dirinya sendiri | manusia buka PDF primer (lokasi+byte terukur di kepala dokumen ini) |
| BTC-02 | Jumlah bookmark 277/128/274/412 | sama | sama (kebijakan: PDF wewenang manusia, bukan keterbatasan alat) |
| BTC-03 | Tahun terbit Darwin (2015) & Mamlouk (2018) | HANYA dari nama berkas PDF; header resume tidak memuat tahun (KD-C8) | manusia; sampai itu klaim umur = "~11 th (dari filename)" berlabel |
| BTC-04 | "sekitar 12% halaman tanpa lapis teks" (Darwin resume:51) | Statistik atas PDF, tidak terverifikasi dari teks | manusia; objek IL pakai sebagai perkiraan berlabel |
| BTC-05 | "(terverifikasi, PDF 40 area)" Mamlouk resume:39 | Klaim verifikasi warisan tanpa jejak alat | manusia; prinsip teg-reg umum boleh, alamat PDF 40 = BELUM TERKONFIRMASI |
| BTC-06 | Kandungan detail per halaman pointer (mis. apa di PDF 194 Darwin) | Lapis teks hanya menjamin judul bab dan keberadaan pointer | manusia sebelum angka apa pun dari halaman itu dipakai |

#### 6.3.4 TIDAK DITERBITKAN - butir DILARANG TERBIT (11 butir kelas-nol)

Sebelas butir berikut TIDAK dinaikkan sebagai muatan. Angka-angkanya TIDAK ADA di lapisan teks
rak dalam bentuk apa pun (terukur: 0 entri rumus struktur di KATALOG-RUMUS; 0 baris ambang
CIVIL di induk; keenam baris R1/R2 mata 1 berstatus TIDAK ADA). Seksi ini adalah pernyataan
LARANGAN tanpa angka: menyajikannya = mengarang. Yang dicantumkan di sini hanyalah KELAS angka
yang dilarang dan SUMBER YANG SEHARUSNYA memegang angka itu.

| ID | Kelas angka yang DILARANG terbit dari objek ini | Sumber yang seharusnya |
|---|---|---|
| DT-01 | nomor pasal dan isi pasal SNI struktur (1727/1726/1729/2847) | salinan resmi SNI (GAP-015..018) |
| DT-02 | koefisien kombinasi beban untuk pekerjaan Indonesia | SNI 1727/1726 |
| DT-03 | faktor reduksi material (lentur, geser, tekuk, tumpu) | SNI 2847/1729 (ACI/AISC asli pun tidak ada - R2 kosong) |
| DT-04 | kuat nominal penampang konkret | hitung proyek dari standar sah + R4 |
| DT-05 | rumus panjang penyaluran berkoefisien standar asing | SNI 2847; metode generik boleh dengan label |
| DT-06 | angka tekanan angin / respons spektrum gempa per lokasi | SNI 1727/1726 + peta bahaya |
| DT-07 | nilai torsi baut prategang / kapasitas sambungan las | lembar data baut [R4] + SNI 1729 |
| DT-08 | nilai kapasitas angkur (pull-out design) | lembar data angkur [R4] per proyek |
| DT-09 | kriteria terima las visual/UT/RT | standar las (gap yatim, usulan U-1) + kontrak |
| DT-10 | mutu beton / tegangan izin baja sebagai "ambang lulus uji" | spesifikasi kontrak + SNI 2847/1729 + mill cert [R4] |
| DT-11 | SATU KALIMAT PUN positif "desain memenuhi SNI 1726/1729/2847/1727" | jalur sah 1-2 (kontrak-standar / ahli bersertifikat) |

Batas eksplisit: angka kelas DT-01..DT-11 TIDAK naik di objek ini dalam bentuk apa pun - bukan
angka, bukan contoh, bukan "misalnya". Bila hilir membutuhkannya, jalurnya = akuisisi standar
resmi (GAP-015..018) atau lembar data pabrikan (GAP-014), lalu amandemen tercatat.

### 6.4 Kandidat ground-truth probe

Enam kandidat probe (P-1..P-6, dua di antaranya jebakan) terdaftar di studi hulu Bagian 8.1
dengan jawaban benar kanonik dan jalur buktinya; objek ini tidak menggandakannya (verifier
mengukur sendiri ke rak).

Rekapitulasi predikat: READY 23 + LABEL-GUARD 7 + BELUM TERKONFIRMASI 6 + DILARANG TERBIT 11 =
47 butir. Pola distribusi: muatan siap-terbit didominasi METODA + PETA KEABSENAN; semua angka
nilai murni jatuh ke DILARANG TERBIT - paralel struktural dengan CYBERSECURITY (SDCY): payload
yang harus terbit justru pernyataan batasnya.

---

## Bagian 7 - Gap register domain

### 7.1 Celah resmi GAP-REGISTER yang mengikat domain ini (verbatim register, terukur)

| Gap | Tingkat | Yang hilang | Prioritas | Status |
|---|---|---|---|---|
| GAP-015 | R1 | SNI 1727 beban minimum | TINGGI | terbuka [csv:16] |
| GAP-016 | R1 | SNI 1726 ketahanan gempa | TINGGI | terbuka [csv:17] |
| GAP-017 | R1 | SNI 1729 struktur baja (+tabel profil ID) | TINGGI | terbuka [csv:18] |
| GAP-018 | R1 | SNI 2847 struktur beton (ambang+reduksi) | TINGGI | terbuka [csv:19] |
| GAP-020 | R2 | ASTM/SNI metode uji bahan | MENENGAH | terbuka [csv:21] |
| GAP-014 | R4 | dokumentasi OEM (angkur/baut/mill cert) | PER PROYEK | by-design [csv:15] |

### 7.2 Usulan celah/gap baru hasil studi (nomor final = controller, V-16)

| Usulan | Tingkat | Butir | Dasar ukur |
|---|---|---|---|
| U-1 | R2 | Standar las struktur (visual + NDT; mis. klas AWS D1.x padanan SNI) | KD-C5; RANTAI-K:104,135 |
| U-2 | R1 | Kode bangunan Indonesia (PPI/UBAPPI) - ranah D3, dicatat di sini hanya karena RANTAI-K mata 2 menyentuh keputusan struktur bangunan | KD blueprint-3 (F-5); domain D3 |
| U-3 | - | Ekstraksi katalog: bangun seksi "struktur" di KATALOG-RUMUS dari 4 buku (pointer metode, TANPA angka ambang) | KD-C6; bukan akuisisi - kerja lapis teks |
| U-4 | - | Tambah baris CIVIL di bagian "Belum ada sumber sah" AMBANG-TERIMA-INDUK | KD-C4; wewenang pengelola rak |

### 7.3 Gap hasil sapuan (berbasis bukti sapuan, bukan dugaan)

| ID | Yang dicari | Keadaan |
|---|---|---|
| G-7 | Buku geoteknik/pondasi lanjut (daya dukung tanah, tiang pancang) | tidak ada di rak; hanya sisi beton pondasi Darwin |
| G-8 | Tabel profil baja SNI (WF/H-beam Indonesia) | tidak ada di rak (GAP-017); yang ada hanya tabel W/HP/HSS Amerika di Segui |
| G-9 | Standar las (AWS/ISO/EN) sebagai rujukan ambang | tidak ada di rak DAN tidak terdaftar di register (gap yatim, KD-C5) |
| G-10 | Peta bahaya gempa/win pressure Indonesia | tidak ada di rak (butuh SNI 1726/1727 + peta) |
| G-11 | Seksi perhitungan struktur di KATALOG-RUMUS | tidak ada di lapis katalog meski 4 buku R3 ada (KD-C6, gap ekstraksi) |
| G-12 | Lembar data R4 angkur/baut/mill cert | tidak ada di rak; by-design per proyek (GAP-014) |

### 7.4 Yang justru KUAT di rak ini (agar objek tidak timpang)

Enam keputusan desain mata 2 dengan alternatif ditolak + alasan [RANTAI-K:39-46]; urutan hitung
6 langkah tertelusur dengan peringatan kegagalan senyap [:57-73]; kejujuran struktural berupa
rantai yang diterbitkan PUTUS secara sengaja dan status putus ikut menjadi lampiran kartu
kendali [:3-6,138]; protokol keselamatan dengan larangan keras jalan-3 [:117-122]; konsistensi
pointer internal 18/18 cocok (uji [10]); mekanisme gerbang rantai putus sudah ternormalisasi di
governance [ASSURANCE-GATES.md:167-172].

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS.

1. **Status rantai apa adanya (tanpa perataan):** Rantai Jaminan CIVIL-STRUCTURAL **PUTUS di
   mata 4** - "METODE LENGKAP - AMBANG TIDAK ADA" [R3, RANTAI-K:3-6,144]. Rantai putus ketiga
   setelah D (pembumian) dan J (keamanan siber) [:8]. DILARANG KLAIM LULUS STANDAR: tidak ada
   satu pun angka domain ini yang boleh naik sebagai ambang lulus/tidak lulus, dan tidak ada
   satu pun kalimat positif pemenuhan SNI struktur yang boleh diterbitkan (DT-11). Ini keputusan
   penerbitan sadar, bukan kecelakaan: terbit APA ADANYA, dan pernyataan batas standar (kepala
   dokumen ini) wajib ikut di setiap serah. Meratakan status ini = cacat proses; custodian
   menolak. Redaksi "rantai menjadi utuh bila GAP-015..018 ditutup" adalah OVERSTATED (KD-C9) -
   yang tertutup hanya ambang desain mata 1-3, bukan mata 4 seluruhnya.
2. **Protokol keselamatan tidak boleh dilepas dari angka.** Zona keselamatan jiwa
   [RANTAI-K:10-12] dan larangan jalan-3 untuk menara/dudukan ketinggian [:117-122] wajib ikut
   terangkut ke setiap turunan objek ini (Bagian 5.5). Rak membuat GSP mampu MEMERIKSA dan
   berdiskusi dengan ahli struktur, bukan menggantikannya [:48-49].
3. **Keadaan rak: JANGAN kutip angka README sebagai fakta (KD-C3).** `README.md:48-49` ("empat
   celah R1") TIDAK rekonsiliasi dengan register hidup (sensus CSV terukur 9 baris R1, sipil
   menyumbang 4). Statistik yang tampil di objek ini adalah yang terukur dari register.
   Demikian pula keluarga MD gap register (KD-C2): sumber kebenaran = `GAP-REGISTER.csv`.
4. **PDF primer belum dibuka manusia.** Tidak ada verifikasi halaman ke PDF asli pada misi ini;
   vonis halaman = vonis lapis teks. Wewenang manusia: BTC-01..BTC-06 (rincian di tabel 6.3.3).
   Lokasi PDF nyata terukur di Bagian 1.4; laci [`ekas/`](../../ekas-lapis-teks/) workspace = cermin, dan klaim
   INTAKE_ONLY di manifest laci = BASI (KD-C1).
5. **Known-defect yang wajib ikut terangkut:** KD-C1 (manifest INTAKE_ONLY basi), KD-C2 (MD vs
   CSV tak sinkron), KD-C3 (README "empat celah" basi), KD-C4 (induk tanpa baris struktur),
   KD-C5 (standar las gap yatim), KD-C6 (KATALOG-RUMUS nol entri struktur), KD-C8 (header resume
   tanpa tahun), KD-C9 (klaim rantai-utuh overstated). Penandaan di lapis rak menunggu kartu
   D1-FIXx (hanya-tambah) dan penomoran controller untuk U-1..U-4; sampai terpasang, vonis
   rilis domain ditahan. Bentuk lama tidak dihapus di mana pun, hanya ditandai.
6. **Usia bahan.** Hibbeler dan Segui tercatat 2017 di header resume; Darwin dan Mamlouk TANPA
   tahun di header (tahun 2015/2018 hanya dari nama berkas PDF - KD-C8, BTC-03). Umur buku
   tidak dihitung ulang di sini dari lapis resume (melarang karangan); semua calon umur <= 11
   tahun sehingga guard umur 15-th [pustaka-teknis; README] aman, tetapi tetap berlabel.
   Keempatnya R3 (buku ajar/metode) - tidak satu pun jadi ambang terima.
7. **Adjacency (rujukan silang, tidak disalin).** Ching "Building Construction Illustrated"
   milik domain BUILDING-CONSTRUCTION (REF-BLD-001) - objek ini membawanya HANYA sebagai
   pointer PDF 115/157 untuk mata 1 dan mata 2 (V-15); domain asal dipegang D3. Baris "Struktur
   & mekanik" di `KATALOG-RUMUS.md:607` menunjuk domain MECHANICAL (Shigley), BUKAN sipil.
   Ambang pembumian pada menara hasil hitung K tetap urusan rantai D (LG-07; rantai D juga
   putus). Verifikasi dimensi/ketegakan masuk sebagai lampiran dari rantai L (survei).
8. **Sumber dan kebaruan ekstraksi.** Seluruh angka berasal dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) diekstrak
   read-only 2026-09-29 oleh studi t_d146e3b1; pengukuran byte/baris/aritmetika adalah cetakan
   skrip `research/civ/civ_measure.py` (ts 2026-09-29T01:51:22Z) dan `civ_measure2.py`
   (ts 01:52:39Z), bukan ingatan. Short check deterministik `research/civ/short_check.py`
   VERDICT PASS 2026-09-29T01:59:41Z dengan 18/18 sampel koordinat cocok rak. [`ekas/`](../../ekas-lapis-teks/) read-only
   - objek ini tidak mengubah rak. Tipografi kutipan dinormalisasi ASCII (angka, jalur, nomor
   baris disalin persis).

STATUS: needs-review
