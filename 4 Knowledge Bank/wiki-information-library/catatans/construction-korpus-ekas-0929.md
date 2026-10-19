---
id: construction-korpus-ekas-0929
type: catatan
title: Korpus CONSTRUCTION EKAS - peta, metode, dan batas pengetahuan (CVLK-0929)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-29
catatan_verifikasi: "Iterasi-2 gsp-custodian 2026-09-29: VERDICT terverifikasi - kelima tambalan gatekeeper diuji ulang ke sumber nyata dan SAH (F-1 label intake = T24: heading pemilik CHANGELOG:629-631 adalah T24 di CL:621 dan baris 629-631 memang tabel CONSTRUCTION/DRAWING-CAD/BUILDING-CONSTRUCTION, T28 hidup di CL:797 dengan topik Rantai K dan M sehingga tidak diklaim objek untuk intake, sisa token T28 di body = 0 pada baris 115,117,128,369,377,418; F-2 karakter U+200E hilang - sapuan byte-level U+200E/U+200F/U+202A/U+202B/U+202C/U+FEFF = 0 dan baris _ISI.md bersih ASCII; F-3 contoh negatif produktivitas excavator kini bercoretan persis bentuk studi:325 dan angka 0,8 hanya hidup di dalam coretan penolakan pada baris 285 (satu-satunya kemunculan di body); F-4 wc -l nyata GAP-ACQUISITION-PLAN.md = 191 sama dengan klaim body:114, sisa '192 br' di body = 0; F-5 ukur ulang ekas/05_DOMAIN-KNOWLEDGE/PROJECT-QUALITY: 6 resume R3 = 327 baris + RANTAI-JAMINAN 143 baris = 470 total 7 berkas, cocok label body:130). GUARD REGRESI 24/24 PASS: 25 kunci frontmatter tanpa duplikat, yaml.safe_load utuh, title == H1 pertama, predikat 6.3 identik studi RD24/LG7/BTC5/DT8 = 44 dengan mismatch per-ID 0, em dash U+2014 / middle dot U+00B7 / en dash U+2013 / U+200E = 0 byte-level, pola nilai uang riil di body = 0, Rantai M PUTUS @4 tanpa perataan (21 penanda putus; kedua kutipan 'utuh' ternegasi atau dikutip untuk ditolak OVERSTATED), superlatif ketebalan di body = 0 dan hanya hidup sebagai register KD-N7 + LG-01, PROJECT-QUALITY tetap pointer-only (verbatim isi kartu = 0). Delta body terhadap cadangan pra-revisi iterasi-1 = 22 baris dan seluruhnya berada di wilayah hunk F-1..F-5; selisih token angka hanya 28 -> 24, 192 -> 191, serta 6/327/143 = nol angka teknik berubah. Verdict iterasi-1 tetap utuh di riwayat-catatan-verifikasi; body tidak disentuh."
sumber: "docs/2026-09-29-cvl-knowledge-register/research/construction-korpus-detail.md (hulu: studi t_9edc0954 vonis LAYAK controller; 627 baris / 48.941 B; 3 berkas domain + 3 kartu REF-CON penuh + 15 pendukung)"
halaman: marker [R-n, sumber, hal] per butir di body dipertahankan verbatim dari studi (koordinat resume Peurifoy/Holm/Mubarak + kartu REF-CON + GAP-REGISTER.csv:20 verbatim); koordinat lapis teks ditulis 'berkas:baris'
tanggal_akses: 2026-09-29
kelas_bukti: sintesis
sensitif: tidak
perkara: cvlk-0929
tags: [construction, perencanaan-pelaksanaan, alat-berat, produktivitas-alat, taksiran-biaya, rab, harga-satuan-pekerjaan, ahsp, estimasi, penawaran-subkontrak, overhead-laba, penjadwalan, cpm, jalur-kritis, perataan-sumber-daya, pemutakhiran-jadwal, pemampatan-waktu-biaya, k3-konstruksi, GAP-019, rantai-M, nol-R1, nol-R2, metode-boleh-angka-dilarang, known-defect]
links: [ekas/05_DOMAIN-KNOWLEDGE/CONSTRUCTION, ekas/04_KNOWLEDGE-CARDS/CONSTRUCTION, ekas/05_DOMAIN-KNOWLEDGE/PROJECT-QUALITY, ekas/05_DOMAIN-KNOWLEDGE/CIVIL-STRUCTURAL, docs/2026-09-29-cvl-knowledge-register/research/construction-korpus-detail.md]
defek-terkait: register known-defect KD-N1..KD-N8 (8 bertahan terukur) + KD-N9 (buta-titik register alat, tanpa beban rilis) di Bagian 6.2. Penandaan lapis rak menunggu kartu D2-FIXx (hanya-tambah); usulan U-1..U-5 menunggu nomor controller (V-16) - vonis rilis ditahan sampai tanda terpasang
penulis: gsp-pm-analyst
diajukan: 2026-09-29
domain: CONSTRUCTION
created: 2026-09-29
riwayat-catatan-verifikasi: "Verdict gsp-custodian 2026-09-29: perlu_revisi ringan kelas label/alamat (nol angka teknik berubah; sampling 90 needle koordinat ke rak nyata MISS 0; yaml utuh 25 kunci; predikat 6.3 identik studi RD24/LG7/BTC5/DT8=44; guard metode-vs-angka lolos pola nilai uang=0 di body; PUTUS mata 4 + sebagian mata 2 konteks ID utuh tanpa perataan; superlatif ketebalan muatan=0 hanya register KD-N7+LG-01; PROJECT-QUALITY pointer-only). TEMUAN WAJIB SEBELUM PROMOSI: (1) label T28 untuk CHANGELOG:629-631 SALAH - heading pemilik baris itu = T24 (T28 ada di :797, topik rantai K/M); perbaiki di baris objek 115,117,128,369,377,418 (ganti T24 atau hapus label); (2) baris objek 119 memuat karakter tak-kasat U+200E sebelum _ISI.md - literal jalur tidak identik byte dengan nama berkas rak, hapus; (3) deklarasi 6.3.4 (angka DT bukan contoh) berkontradiksi dengan contoh negatif Produktivitas excavator 0,8 m3/jam di tabel Mata 4 yang kehilangan coretan penolakan dari studi - pulihkan penanda coretan atau ganti placeholder X m3/jam; (4) plan 192 br mewarisi off-by-one cetakan hulu count-newline+1, wc -l nyata 191 - nyatakan basis; (5) klaim 7 resume 470 baris salah label: resume = 6 berkas 327 baris, 470 = total 7 berkas termasuk RANTAI-JAMINAN. REKOMENDASI: sunting lima butir redaksi/label ini hanya-tambah/koreksi-label tanpa angka baru, lalu naikkan status."
catatan_keputusan: "dipromosikan: CVLK-0929 C2-L2: verdict custodian independen terlampir di catatan_verifikasi, non-sensitif non-dosir; Rantai M baru terbit PUTUS @4 (+sebagian @2 konteks ID) apa adanya; 8 butir DILARANG TERBIT naik hanya sebagai pernyataan larangan tanpa angka harga; klaim superlatif KD-N7 dibuang dari muatan; adjacency PROJECT-QUALITY hanya pointer"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-29
dipromosikan-ke: catatans/construction-korpus-ekas-0929.md
---

# Korpus CONSTRUCTION EKAS - peta, metode, dan batas pengetahuan (CVLK-0929)

Objek master misi CVLK-0929 (id `construction-korpus-ekas-0929`, type catatan, domain
CONSTRUCTION = D2). Muatan = peta rak + metode acuan + RANTAI JAMINAN BARU (Rantai M) mata 1-5 +
ambang/norma harga yang TIDAK ada + register known-defect + celah resmi + batas kemampuan, satu
berkas (SATU objek master per domain; bentuk ikut preseden SDCY-0928 + objek CIVIL-STRUCTURAL
CVLK-0929 seksi 1-8).

Provenans: body dirakit dari SATU sumber, studi `research/construction-korpus-detail.md`
(t_9edc0954 complete, 627 baris / 48.941 B, ekstraksi read-only lapisan teks [`ekas/`](../../ekas-lapis-teks/) oleh
gsp-pm-analyst 2026-09-29). Vonis controller LAYAK dengan dasar terverifikasi ulang: 0 angka
uang rc=1, 3 PDF primer 196.540.165 B persis, guard 3 lapis hidup, rantai draf jujur putus @4
+ @2. Bukti ukur: `lib/c2-stu-evidence/measurement-report.txt` + `measurement-report-2.txt`
(ts 2026-09-29T06:39:09Z / 06:39:44Z); short check `c2-short-check-result.txt` VERDICT PASS ts
06:45:20Z. Kelas bukti: sintesis - R3 buku
berupa METODA + PETA LOKASI pointer; domain NOL R1, NOL R2, NOL R5 (terukur); yang tidak ada di
rak dinyatakan "tidak ada di rak" beserta sumber yang seharusnya.

PERNYATAAN BATAS STANDAR (wajib ikut terbit; [GAP-REGISTER.csv:20 verbatim; R3, Holm:46-48]):
korpus ini TIDAK dapat menyatakan harga satuan pekerjaan RAB "sesuai AHSP/SNI" - AHSP dan SNI
analisis harga satuan tidak ada di rak, laci R1 kosong 0 PDF, GAP-019 terbuka (terukur,
Bagian 2.1). Angka harga satuan Holm konteks Amerika Utara dan sudah usang bahkan di sana;
yang boleh dipakai METODE penyusunannya, bukan angkanya. Norma produktivitas alat dan regulasi
K3 konstruksi Indonesia juga tidak ada di rak. Setiap pekerjaan yang memakai objek ini wajib
membawa pernyataan ini apa adanya; uji penolakan V-10: satu kalimat pun positif "harga satuan
sesuai AHSP/SNI" bersandar rak = FAIL walau rute memori hidup.

Catatan wewenang: tidak ada PDF primer dibuka pada misi ini; vonis halaman = vonis LAPISAN
TEKS, verifikasi per halaman wewenang manusia (AGENTS.md; preseden SDCY catatan-2); lokasi +
byte PDF di Bagian 1.4, laci [`ekas/`](../../ekas-lapis-teks/) hanya cermin. Tipografi: rak asal memakai U+00B7/U+2014
(terukur [1]: Holm A1=10 A2=5; Peurifoy A1=8 A2=5; Mubarak A1=8 A2=5); objek ini nol keduanya -
pemisah ASCII, angka/jalur/baris disalin persis.

---

## Batas domain - apa yang TIDAK dicakup objek ini

| Area | Status cakupan | Alasan / kemana |
|---|---|---|
| Perencanaan pelaksanaan + produktivitas alat berat (galian, urugan, crane, beton lapangan) | CAKUP (metode) | Peurifoy [R3] |
| Taksiran biaya/RAB: struktur estimasi, volume, overhead, laba, penawaran subkontrak | CAKUP (metode; TANPA angka harga) | Holm [R3]; angka satuan DILARANG (GAP-019) |
| Penjadwalan CPM, perataan sumber daya, pemutakhiran, pemampatan waktu-biaya | CAKUP (metode) | Mubarak [R3] |
| Harga satuan pekerjaan Indonesia (AHSP/SNI/survei pasar) | TIDAK DAPAT dicakup | R1 laci kosong 0 PDF (terukur); GAP-019 [csv:20] |
| Ambang mutu struktur/bahan (SNI 1726/1727/1729/2847, ASTM/SNI uji) | TIDAK dicakup di sini | domain CIVIL-STRUCTURAL (GAP-015..018, GAP-020); ranah D1 |
| Manajemen proyek umum + mutu proyek + audit mutu | ADJACEN, provenance terpisah | domain PROJECT-QUALITY (REF-PRQ-001..006); POINTER saja, penyerapan butuh putusan controller (V-15) |
| Bangunan/gedung; CAD | TIDAK dicakup | domain BUILDING-CONSTRUCTION (ranah D3); DRAWING-CAD (ranah D5) |
| Peledakan batuan | DILUARI lingkup pekerjaan GSP | pernyataan eksplisit resume [R3, Peurifoy:59-60] |
| Angka produk alat (kapasitas, bbm, biaya sewa riil) | TIDAK ada | R4 lembar data alat per proyek/sewa |
| K3 konstruksi Indonesia (Permenaker PPPK) | TIDAK ada | tidak dirujuk SEMUA lapis domain (terukur); laci PERMENAKER kosong; usulan U-1 |

---

## Bagian 1 - Peta isi

### 1.1 Lapis domain [`ekas/05_DOMAIN-KNOWLEDGE/CONSTRUCTION/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/CONSTRUCTION/) (3 berkas, 189 baris, 7.470 B terukur; cetakan [1])

| Berkas | Baris | Byte | Peran |
|---|---|---|---|
| `R3 - Construction Planning, Equipment, and Methods (Peurifoy).md` | 65 | 2.595 | REF-CON-001, metode pelaksanaan + alat |
| `R3 - Construction Cost Estimating (Holm & Schaufelberger).md` | 58 | 2.371 | REF-CON-002, taksiran biaya |
| `R3 - Construction Project Scheduling and Control (Mubarak).md` | 66 | 2.504 | REF-CON-003, penjadwalan + kendali |
| TOTAL | 189 | 7.470 | cocok nominasi kartu; TIDAK ada RANTAI-JAMINAN.md (terukur False) - rantai baru berasal dari studi (Bagian 4) |

Lapis 05 ini TERTIPIS di batch calon (ukur 2 [J]: GROUNDING 548 > CIVIL 406 > DRAWING 236 >
CONSTRUCTION 189 > BUILDING 142); ketebalan bukan kriteria vonis.

### 1.2 Lapis kartu [`ekas/04_KNOWLEDGE-CARDS/CONSTRUCTION/`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/CONSTRUCTION/) (3 x 48 baris = 144 baris / 5.941 B terukur; cetakan [2])

| Kartu | Buku | Status | Wewenang ambang | Catatan |
|---|---|---|---|---|
| `REF-CON-001.md` | Peurifoy ed. 9 | ACTIVE | no-unless-contract-adopts | metode pelaksanaan + alat [:12-14]; batas produktivitas [:29-31] |
| `REF-CON-002.md` | Holm & Schaufelberger (2021) | ACTIVE | no-unless-contract-adopts | batas kanonik D2 [:31]; pointer adjacency REF-PRQ-001 [:57] |
| `REF-CON-003.md` | Mubarak (2019) | ACTIVE | no-unless-contract-adopts | tidak memasok durasi [resume:52-53]; istilah kontrak Amerika [:55-56] |

Cocok `MASTER-REFERENCE-REGISTER.csv:44-46` (ACTIVE, wewenang seragam, catatan "metode berlaku,
angka/pasal berbasis standar Amerika"; total 63 baris).

### 1.3 Lapis bersama (baris terkait konstruksi)

| Berkas | Letak | Yang dipasok |
|---|---|---|
| [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../../ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) | 613 br | SIFAR entri konstruksi (11 token taksiran/AHSP/CPM/produktivitas/crane/overhead dll = 0; 1 hit 'jadwal' :303 = konteks RCM; [10],[A]) - jembatan rumus BELUM ADA (KD-N4) |
| [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) | 186 br | 0 entri relevan ([11]) padahal kartu menuntut ASSUMPTION (KD-N5) |
| [`ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md`](../../ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md) | :75-87 | 0 baris KONSTRUKSI/HSP/AHSP ("Belum ada sumber sah" = 7 baris domain lain; [12],[K]) - gate induk buta celah D2 (KD-N6) |
| [`ekas/02_REGISTERS/GAP-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv) | :20 | GAP-019 (MENENGAH) satu-satunya gap berdomain CONSTRUCTION, verbatim: "Harga satuan pekerjaan untuk RAB ... Holm [R3] memberi metode; harga satuannya konteks Amerika Utara dan usang"; R1 = 9 baris, 21 data |
| `GAP-REGISTER.md` + `GAP-ACQUISITION-PLAN.md` | seluruh berkas | MD 165 br: 0 token GAP-019/AHSP/CONSTRUCTION [4]; plan 191 br via wc -l 0 hit [13] - sumber kebenaran = CSV (KD-N2) |
| `INTAKE-RINGKAS.md` + `R3-STATUS.md` | seluruh berkas | tidak melacak CONSTRUCTION [B],[13] - intake manual T24 [CHANGELOG:629-631]; register alat UNDERCOUNT (KD-N9) |
| [`ekas/01_GOVERNANCE/ASSURANCE-GATES.md`](../../ekas-lapis-teks/01_GOVERNANCE/ASSURANCE-GATES.md) | G1 :23, G2 :42, G3 :52, G6 :99; :160-172 | peta gate domain; tiga jalan sah generik rantai putus - untuk RAB: pemilik menetapkan daftar harga acuan tertulis |
| [`ekas/00_START-HERE/README.md`](../../ekas-lapis-teks/00_START-HERE/README.md) + `CHANGELOG.md` | README :48,:72,:79-81; CL :629-631,:718-724 | aturan ambang R1/R2 + angka produk R4; klaim "empat celah R1" README:48 basi vs CSV 9 baris (KD-N3); CHANGELOG mencatat intake T24 (3 buku) + vonis batch "metodenya boleh dipakai, angka dan pasalnya tidak" |
| `ekas/03_SOURCE-VAULT/R1_NATIONAL-NORMATIVE/*/_ISI.md` | 5/5 | KOSONG terukur [5], total PDF = 0 |
| [`ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/`](../../ekas-lapis-teks/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/) | 7 md | token AHSP/SNI/ASTM/ACI/AISC/ASCE = 0 semua [6] |
| [`ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CONSTRUCTION/_ISI.md`](../../ekas-lapis-teks/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/CONSTRUCTION/_ISI.md) | :3-6 | klaim `INTAKE_ONLY`/"belum diresume" KONTRADIKSI dengan 3 resume + 3 kartu ACTIVE (KD-N1); objek ini TIDAK mengutipnya sebagai status sahih |

### 1.4 Lapis laci sumber - jalur logis vs fisik nyata

Tiga PDF primer nyata di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/
CONSTRUCTION/` (stat cetakan [8], TIDAK dibuka): Peurifoy 138.478.599 B; Holm 42.183.926 B;
Mubarak 15.877.640 B; total 196.540.165 B. Laci workspace = cermin (preseden SDCY K-6), bukan
kehilangan berkas. Manifest laci mengklaim INTAKE_ONLY dan itu BASI (KD-N1): resume dibuat 21
Agu setelah intake T24, manifest tidak disunting. Tabel PDF primer (halaman = KLAIM RESUME, wewenang manusia): Peurifoy ed. 9 1.282 hal / 381
bookmark; Holm 2021 355 / 347; Mubarak 2019 595 / 341 [resume:20-38]. Tahun Peurifoy (2018)
HANYA dari nama berkas (KD-N8, BTC-04). Adjacency PROJECT-QUALITY (REF-PRQ-001; 6 resume 327 baris + RANTAI 143 = 470 total 7
berkas ada, ukur 2 [G],[17]) - HANYA pointer lintas domain (V-15).

---

## Bagian 2 - Nol R1, nol R2: tidak ada angka harga satuan maupun norma di rak

Konsekuensi pengikat (dinyatakan penuh di kepala Rantai M, Bagian 4): TIDAK ADA angka domain ini
yang boleh naik sebagai ambang lulus/tidak lulus atau harga RAB (ambang terima menuntut R1/R2
[README.md:72]; angka produk menuntut R4).

### 2.1 Lapis R1 (regulasi/SNI/AHSP Indonesia): KOSONG - terukur

Kelima laci R1 `_ISI.md` KOSONG (SNI, PUIL, OTHER-REGULATION, PERMENAKER, SKKNI; total PDF = 0,
[5]). Yang hilang: AHSP / SNI analisis harga satuan (GAP-019 [csv:20]) dan Permenaker PPPK K3
(usulan U-1). Jawaban kanonik SEMUA pertanyaan angka harga satuan: "tidak ada di rak; sumber
yang seharusnya: AHSP edisi terbaru terbitan PUPR / SNI analisis harga satuan / survei pasar
setempat". Token 'AHSP' di seluruh ekas hanya hidup di 4 tempat ([19]): CHANGELOG:720,
GAP-REGISTER.csv:20, REF-CON-002.md:31, Holm resume:48 - semuanya PERNYATAAN KEABSENAN, bukan
angka.

### 2.2 Lapis R2 (standar internasional): KOSONG untuk domain ini - terukur

Sapuan seluruh md laci R2 (7 berkas): AHSP/SNI/ASTM/ACI/AISC/ASCE = 0 semua [6]. Tidak ada jalur
"pakai standar induk buku Amerika sebagai R2" - untuk domain ini bahkan tidak ada standar induk
harga satuan yang tersimpan.

### 2.3 Lapis R3 (tiga buku): yang ADA adalah LOKASI dan METODA, bukan nilai

Uji silang pointer kartu-vs-resume (cetakan [15]): 12/12 cocok, selisih nol.

Uji penolakan internal (butir WAJIB D2, cetakan [D]): sapuan pola angka uang (Rp, $, dolar,
ribu, jt, USD) di SELURUH 05/CONSTRUCTION = 0 kemunculan - klaim "tidak ada angka HSP 'sesuai
AHSP/SNI' dari rak" terbukti TERUKUR, bukan hanya normatif. Frekuensi token domain ([14])
puncak pada 'subkontrak'/'produktivitas'/'CPM'/'harga satuan' - muatan domain = METODA
PELAKSANAAN + STRUKTUR ESTIMASI, keabsenan harga disebut tepat-di-titik-batasnya.

### 2.4 Lapis R4 (produk): per proyek, by-design

Produktivitas/biaya alat riil menuntut lembar data alat [R4] [R3, Peurifoy:53-54;
REF-CON-001:29-31]; penawaran subkontraktor = dokumen proyek [R4 setara]; harga satuan lokal =
AHSP/survei, bukan rak. Tidak ada laci R4 domain ini; pola sama GAP-014 sipil ("diminta ke
pabrikan tiap proyek").

### 2.5 Lapis R5: KOSONG untuk domain ini - terukur

Sensus MRR run studi: baris R5 = 3 (REF-SEC-003, REF-SEC-004, REF-SWD-001) - nol CONSTRUCTION
([H]); laci R5 mirror hanya 4 _ISI.md. R5 bukan sandaran akhir [README.md:79-81]; di sini tidak
relevan karena nol.

---

## Bagian 3 - Angka acuan per buku (pointer metode, bukan nilai)

| Buku [R3, kartu] | Untuk apa | Pointer muatan utama | Batas pemakaian | Gate |
|---|---|---|---|---|
| Peurifoy ed. 9 [REF-CON-001] | "merencanakan pelaksanaan pekerjaan sipil dan menaksir produktivitas alat" saat GSP pelaksana utama (galian jalur kabel, pondasi menara, jalan akses, pekerjaan tanah) [:12-14]; peta bab 1-16 [:21-38] | sewa vs beli + biaya per jam = bab 2 PDF 57 + R4 [:42-44]; crane + radius angkat bab 16 PDF 842 [:48-49] | produktivitas = taksiran umum bukan angka produk, nyata dari lembar data [R4] + lapangan [:53-54]; +-25% halaman tanpa lapis teks [:56-57]; peledakan di luar lingkup GSP [:59-60] | G1+G2 [:64-65] |
| Holm & Schaufelberger 2021 [REF-CON-002] | "buku pertama di rak yang membahas BAGAIMANA taksiran biaya disusun - bukan sekadar mengalikan volume dengan harga satuan" [:12-13]; peta bagian I-VI + apendiks [:20-28] | ketelitian estimasi per jenis [:34-36]; overhead+laba+risiko bagian V PDF 234 [:38-39]; menilai penawaran subkontrak bagian IV PDF 200 [:41-42] | batas kanonik D2 = pernyataan batas standar di kepala objek ini (parafrasa bermarker; teks utuh [:46-48]); pointer adjacency REF-PRQ-001 [:57, kartu tujuan ADA ukur 2 [G]] [:54-58] | G1 |
| Mubarak 2019 [REF-CON-003] | "buku paling teknis tentang penjadwalan di rak", berguna saat jadwal dipersoalkan [:12-17]; peta bab 2-12 [:21-33] | CPM bab 4 PDF 65 [:37-38]; perataan sumber daya bab 6 PDF 149 [:47-48]; pemutakhiran bab 7 PDF 183 [:40-42]; pemampatan waktu-biaya bab 8 PDF 243 [:44-45] | tidak memasok durasi kegiatan (dari produktivitas nyata REF-CON-001 + pengalaman sendiri); istilah kontrak konteks Amerika, EOT Indonesia ikut syarat kontrak setempat [:52-56]; terikat erat Holm [:60-66] | G1+G6 |

LABEL-GUARD LG-05 melekat pada tabel ini (baris LG-05 di 6.3.2).

### 3.1 Konvensi halaman

Ketiga buku dikutip lewat NOMOR PDF catatan lapis teks resume (tanpa catatan selisih cetak-PDF
untuk domain ini). Setiap nomor PDF = pointer lapis teks, BUKAN vonis halaman fisik (BTC-05).

---

## Bagian 4 - RANTAI JAMINAN BARU (Rantai M) mata 1-5 - hasil studi, status PUTUS jujur di kepala

Rantai ini TIDAK ADA di rak sebagai berkas (terukur False) - berasal dari studi D2-STU sebagai
draf pola RANTAI-K/RANTAI-J, disahkan terbit apa adanya oleh vonis controller; penempatan final
sebagai berkas rak wewenang pengelola rak.

### RANTAI M - Pelaksanaan konstruksi, taksiran biaya, dan penjadwalan

#### PERINGATAN: RANTAI INI PUTUS DI MATA 4 (dan sebagian mata 2 untuk konteks Indonesia)

Tidak ada satu pun sumber R1 atau R2 untuk harga satuan pekerjaan maupun norma produktivitas di
rak. Seluruh angka RAB yang mengikat - yang justru diminta tender - tidak dapat dibuktikan dari
rak ini. Mata 2 utuh untuk METODE, tetapi keputusan yang bersandar syarat kontrak dan regulasi
Indonesia (klaim perpanjangan waktu, K3) tidak punya sandaran normatif. Diterbitkan putus dengan
sengaja, seperti rantai D, J, dan K.

#### Mata 1 - Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Peurifoy, Construction Planning, Equipment, and Methods ed. 9 | R3 | ekonomi alat, pekerjaan tanah, excavator, crane, beton lapangan | PDF 57, 115, 392, 842 |
| Holm & Schaufelberger, Construction Cost Estimating (2021) | R3 | jenis & ketelitian estimasi, volume, harga pekerjaan sendiri, penawaran subkontrak, penyelesaian estimasi | PDF 30, 90, 150, 200, 234 |
| Mubarak, Construction Project Scheduling and Control (2019) | R3 | CPM, perataan sumber daya, pemutakhiran, pemampatan waktu-biaya | PDF 65, 149, 183, 243 |
| Lembar data alat + penawaran subkontraktor | R4 | produktivitas & biaya riil per proyek | per proyek (tiada laci) |
| REF-PRQ-001 (Siegel, manajemen proyek) | R3 domain PROJECT-QUALITY | pendamping manajemen | POINTER saja (V-15) |
| AHSP / SNI analisis harga satuan | R1 | harga satuan pekerjaan untuk RAB | TIDAK ADA - GAP-019 [csv:20] |
| SNI 1726/1727/1729/2847 (mutu struktur pekerjaan sipilnya) | R1 | ambang mutu hasil pekerjaan | TIDAK ADA - GAP-015..018 (ranah rantai K) |
| Regulasi K3 konstruksi (Permenaker PPPK) | R1 | syarat keselamatan kerja konstruksi | TIDAK ADA - laci PERMENAKER kosong; tidak dirujuk lapis mana pun (usulan U-1) |

Pola tabel identik rantai K: R1 kosong semua; yang ada hanya R3 + R4 per proyek.

#### Mata 2 - Keputusan desain (pelaksanaan)

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Tingkat ketelitian estimasi per tahap (awal/anggaran/penawaran) dinyatakan eksplisit | Holm PDF 30 | Menyebut angka awal dengan ketelitian angka akhir DITOLAK - melindungi GSP saat angka awal dibandingkan dengan akhir [Holm:34-36] |
| Pemisahan pekerjaan sendiri vs subkontrak | Holm bagian IV PDF 200 | Menilai penawaran subkontrak tanpa breakdown DITOLAK |
| Sewa vs beli alat + biaya per jam | Peurifoy bab 2 PDF 57 + R4 | Angka taksiran umum buku dipakai sebagai angka pasti DITOLAK [Peurifoy:53-54] |
| Pemilihan crane + radius angkat | Peurifoy bab 16 PDF 842 | Salah pilih crane = alat datang tetapi tidak sanggup mengangkat [Peurifoy:48-49] |
| Jadwal dasar CPM dibekukan sebagai lingkup | Mubarak bab 4 PDF 65 + G1 | Jadwal tanpa jalur kritis DITOLAK - tidak bisa membedakan keterlambatan berarti dan tidak |
| Keputusan percepatan (crash) dengan pertukaran waktu-biaya | Mubarak bab 8 PDF 243 | Menjanjikan percepatan tanpa angka DITOLAK |
| Ketentuan klaim perpanjangan waktu Indonesia | SYARAT KONTRAK SETEMPAT (bukan rak) | Memakai istilah kontrak Amerika dari Mubarak sebagai dasar klaim DITOLAK [Mubarak:55-56] - DISINI MATA 2 PUTUS UNTUK KONTEKS ID |

#### Mata 3 - Perhitungan

Urutan tertelusur (hasil = PROJECT-DERIVED [REF-CON-001..003 seksi 6]):

1. Tetapkan lingkup + breakdown pekerjaan [Holm bagian I-II, PDF 30-90].
2. Hitung volume dari gambar (quantity take-off) [Holm PDF 90].
3. Produktivitas alat/tenaga: taksiran umum buku [R3] WAJIB disetel lembar data alat [R4] +
   kondisi lapangan; tanpa keduanya = ASSUMPTION + sensitivitas + rencana penggantian
   [Peurifoy:53-54; aturan asumsi pustaka-teknis].
4. Biaya kepemilikan/operasi alat per jam [Peurifoy bab 2] - masukan harga lokal, BUKAN dolar
   buku.
5. Harga satuan pekerjaan: dari AHSP/SNI/survei pasar - TIDAK ADA DI RAK (GAP-019); selama
   absen, angka HSP ditandai ASSUMPTION dengan sumber disebut (AHSP edisi mana / survei mana /
   penawaran siapa).
6. Penyelesaian estimasi: langsung + upah + overhead + laba + risiko [Holm bagian V, PDF 234].
7. Jadwalkan: CPM forward/backward [Mubarak PDF 65] lalu perataan sumber daya [PDF 149] lalu
   bila perlu crash, kurva waktu-biaya [PDF 243].
8. Mutakhirkan berkala dengan dasar pembanding terjaga [Mubarak PDF 183].

Peringatan silang: durasi TIDAK dipasok Mubarak [Mubarak:52-53]; mata 3 jadwal bergantung mata 3
biaya-produktivitas. KATALOG-RUMUS tanpa baris domain ini (terukur) - jembatan hitungan resmi
belum dibangun (KD-N4, usulan U-2).

#### Mata 4 - Pengujian - MATA YANG PUTUS

| Butir | Ambang | Sumber |
|---|---|---|
| Kebenaran volume take-off | Rekonsiliasi gambar + uji hitung orang kedua | Metode internal [R3] + gate G3 |
| Wajar tidaknya harga satuan | Pembanding >= 2 penawaran/AHSP resmi | TIDAK ADA DI RAK - GAP-019 |
| Produktivitas terlaksana vs rencana | Kurva nyata proyek (data sendiri) | bukan norma; R3 hanya metode |
| Mutu hasil pekerjaan sipil (beton/urugan/padatan) | Ambang SNI/ASTM | tidak dapat diuji dari domain ini - ranah rantai K (putus juga) + GAP-020 |
| Kelayakan jadwal (logika CPM) | Aturan jaringan | R3 metode - sah sebagai metode, BUKAN ambang |
| Kesesuaian RAB dengan AHSP/SNI | tidak dapat dinyatakan | Regulasinya tidak ada di rak |
| Kepatuhan K3 konstruksi | tidak dapat diuji | Permenaker tidak ada |

Tiga baris terakhir yang membuat rantai ini putus; dua di antaranya justru yang paling sering
dijanjikan dokumen penawaran (RAB "sesuai AHSP" dan komitmen K3).

##### Yang boleh dan tidak boleh dikatakan

| Boleh | Tidak boleh |
|---|---|
| "Struktur estimasi mengikuti bagian I-V Holm & Schaufelberger [R3, PDF 30-234]; harga satuannya dari AHSP edisi X / survei pasar Y (lampiran terpisah)." | "RAB disusun dengan harga satuan Holm." (konteks Amerika Utara + usang) |
| "Produktivitas alat memakai taksiran umum [R3, Peurifoy bab 2-9] yang disetel lembar data alat (terlampir)." | ~~"Produktivitas excavator 0,8 m3/jam."~~ tanpa R4 = angka dari awan |
| "Jadwal CPM mengikuti metode Mubarak [R3, PDF 65]; ketentuan perpanjangan waktu mengikuti syarat kontrak ini." | "Klaim EOT kami sesuai praktik kontrak internasional." |
| "Metode taksiran boleh dikutip dari rak." | SATU KALIMAT PUN "harga satuan sesuai AHSP/SNI" bersandar pada rak (uji penolakan V-10) |

#### Mata 5 - Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Dokumen struktur estimasi berlabel ketelitian (tahap apa, akurasi berapa) | ya | Holm bagian I |
| Lembar perhitungan volume (take-off) tertelusur gambar | ya | Holm PDF 90 |
| Sumber harga satuan yang dipakai (salinan AHSP / surat penawaran / hasil survei) | ya | lampiran eksternal - TIDAK dapat digantikan rak |
| Hitungan sewa-vs-beli alat + lembar data alat [R4] | ya | Peurifoy bab 2 |
| Jadwal dasar beku + log pemutakhiran | ya | Mubarak bab 7; G6 |
| Dokumen pertukaran waktu-biaya untuk persetujuan percepatan | bila ada | Mubarak bab 8 |
| PERNYATAAN STANDAR YANG DIPAKAI (AHSP edisi/SNI mana, atau bahwa belum ada dan siapa yang menetapkan) | ya | pola rantai K [RANTAI-K:137] |
| Kartu kendali rantai berstatus "putus di mata 4" | ya | kejujuran status = isi |

#### Status rantai

"METODE LENGKAP - ANGKA & NORMA TIDAK ADA". Satu celah terdaftar mengikat (GAP-019, MENENGAH) +
dua keabsenan turunan (K3 yatim; ambang mutu milik rantai K). Menutup GAP-019 membuat MATA 3-4
harga bersandar R1 tetapi TIDAK membuat rantai utuh (ambang mutu tetap milik rantai K; K3 tetap
butuh regulasi; R4 tetap per proyek) - redaksi bertingkat, jangan klaim "sekali tutup jadi utuh"
(preseden KD-C9 sipil).

---

## Bagian 5 - Ambang terima, protokol hidup, dan kedudukan di gerbang induk

### 5.1 Peta "boleh / tidak boleh dikatakan" untuk editor proposal/RAB

Teks operasional kanonik = blok "Yang boleh dan tidak boleh dikatakan" dalam Mata 4; kolom boleh
memetakan READY RD-03..RD-24, kolom tidak boleh memetakan DT-01..DT-08 (6.3.4) - guard
metode-vs-angka adalah ISI objek ini, bukan catatan kaki. Silang: overhead/laba hanya metode +
nilai kebijakan perusahaan tertulis (DT-03); peledakan selalu redaksi penolakan (DT-07); struktur
menara selalu menunjuk rantai K (LG-07). Mekanisme gerbang: domain tanpa R1/R2 tidak bisa lewat
gerbang ambang biasa; pekerjaan jalan dengan metode R3 + R4 ASALKAN tiga jalan sah generik
[ASSURANCE-GATES.md:160-172] - untuk RAB: pemilik menetapkan daftar harga acuan tertulis - dan
pernyataan sumber harga + standar dipakai ikut bukti serah. Induk ambang `AMBANG-TERIMA-INDUK.md`
NOL baris konstruksi (:75-87 = 7 baris domain lain, terukur) - pernyataan "tidak dapat diuji"
hidup penuh di Rantai M (KD-N6; usulan U-3).

### 5.2 PROTOKOL KESELAMATAN DAN ASUMSI (wajib ikut terbit bersama metodenya)

1. Titik keselamatan jiwa domain ini: "Pemasangan menara dan perangkat berat" (Peurifoy:48)
   adalah IRISAN DOMAIN - perhitungan struktur menara = rantai K (putus @4, ranah D1);
   CONSTRUCTION hanya memasok pemilihan alat/radius angkat (LG-07). Crane salah pilih/radius
   angkat salah = alat datang tetapi tidak sanggup mengangkat [Peurifoy:48-49] - keputusan mata
   2 wajib membawa dasar R4.
2. Peledakan batuan DILUARI lingkup pekerjaan GSP dan diatur ketat di Indonesia
   [R3, Peurifoy:59-60].
3. K3 konstruksi Indonesia TIDAK dapat diuji dari rak (Permenaker tidak ada; usulan U-1) -
   komitmen K3 di dokumen penawaran wajib bersandar sumber di luar rak, bukan objek ini.
4. Selama GAP-019 terbuka, setiap pekerjaan estimasi/schedule GSP: (a) angka HSP = ASSUMPTION
   dengan sumber disebut (AHSP edisi mana / survei mana / penawaran siapa) + sensitivitas +
   rencana penggantian [aturan asumsi pustaka-teknis; REF-CON-002 seksi 6]; (b) angka alat wajib
   R4 atau berlabel taksiran [Peurifoy:53-54]; (c) keluaran penilaian lewat tiga jalan sah
   generik [ASSURANCE-GATES.md:160-172]; (d) bukti serah wajib memuat pernyataan sumber harga +
   standar yang dipakai [Mata 5]; (e) kalimat DT-01/DT-08 dilarang mutlak.
5. Orang kedua pemeriksa: gate G3 untuk struktur menuntut ahli bersertifikat
   [ASSURANCE-GATES.md:52,59; REF-CON-001..003 seksi 6] - struktur yang menopang pekerjaan
   konstruksi tetap urusan rantai K.

---

## Bagian 6 - Known-defect + tabel beban-rilis

### 6.1 Temuan kelas-nol (jawaban atas kelas yang diminta blueprint)

Sapuan lapis teks domain CONSTRUCTION: 0 angka uang (pola Rp/$/dolar/ribu/jt/USD) di seluruh
05/CONSTRUCTION ([D]), 0 PDF laci R1 [5], 0 token relevan laci R2 [6], 0 entri KATALOG-RUMUS
[10], keenam baris R1/R2/K3 mata 1 berstatus TIDAK ADA. Untuk kelas angka nilai murni (harga
satuan per jenis, biaya per jam alat, koefisien overhead/laba baku, durasi normatif, produktivitas
terjamin, pasal AHSP/SNI/Permenaker): **lapis teks tidak memuat angkanya sama sekali** - tidak ada
yang bisa dikontradiksikan dari rak, karena itu angka kelas itu DILARANG TERBIT (DT-01..DT-08,
6.3.4). Pertanyaan "berapa biaya per jam excavator menurut rak?" dijawab benar hanya dengan "lapis
teks tidak memuat angka uang apa pun; jalur benar: taksiran umum + R4 + harga lokal" - menjawab
angka = karangan = FAIL. Nama sumber (AHSP, SNI analisis harga satuan, Permenaker PPPK) boleh
disebut hanya sebagai nama + status ketiadaan, bukan angkanya.

### 6.2 Register known-defect (koordinat = jalur:baris hasil ukur studi)

| ID | Butir | Bukti (koordinat) | Vonis sementara | Bebani rilis? |
|---|---|---|---|---|
| KD-N1 | Manifest laci vault mengklaim INTAKE_ONLY / "belum diresume" | `_ISI.md:3-6` vs 3 resume 05 + 3 kartu ACTIVE (MRR csv:44-46); [7] | KONTRADIKSI terukur; catatan BASI (kelas persis KD-C1; resume 21 Agu setelah intake T24, manifest tak disunting). Objek ini TIDAK mengutip status INTAKE_ONLY sebagai keadaan sahih | ya (provenans) |
| KD-N2 | Keluarga gap register MD tidak sinkron CSV | GAP-REGISTER.md 165 br: 0 token GAP-019/AHSP/CONSTRUCTION [4]; CSV memuat GAP-019 utuh | Terukur (kelas KD-C2). Sumber kebenaran = CSV; MD dilarang untuk statistik celah | ya (statistik) |
| KD-N3 | README "Empat celah R1" vs sensus CSV 9 baris R1 | README.md:48 vs ukur [3] (GAP-001..004,015..019); CONSTRUCTION menyumbang GAP-019 | Kontradiksi terukur (kelas KD-C3, konfirmasi lintas domain) | ya ("empat" jangan terbit) |
| KD-N4 | KATALOG-RUMUS nol entri konstruksi meski 3 buku R3 ada | [10]: 0 hit 11 token; 1 hit 'jadwal' :303 = konteks RCM | Gap ekstraksi lapis-katalog (kelas KD-C6): jembatan rumus-buku-halaman belum dibangun | ya (eksplisitasi) |
| KD-N5 | ASUMSI-BAKU tanpa entri domain konstruksi | [11]: 0 hit harga satuan/AHSP/produktivitas/subkontrak; 2 hit 'alat' = domain lain | Cacat kelengkapan silang: kartu seksi 6 menuntut ASSUMPTION tetapi tabel asumsi baku domain belum dibuat | ya (asumsi) |
| KD-N6 | AMBANG-TERIMA-INDUK "Belum ada sumber sah" (:75-87) tanpa baris konstruksi | [12],[K]: 7 baris, 0 CONSTRUCTION/HSP/AHSP | Cacat kelengkapan silang (kelas KD-C4): gate induk buta celah harga + produktivitas | ya (gerbang; wewenang rak) |
| KD-N7 | Klaim peringkat ketebalan seluruh-rak pada resume Peurifoy salah lintas-laci | Peurifoy resume:16 vs sapuan klaim halaman semua resume [ukur 1 [16]]: CCNA Library 3.292 > Grondzik 1.855 > Peurifoy 1.282 | Cacat klaim superlatif lapis teks (halaman Peurifoy tetap BTC-01). Objek ini MEMBUANG klaim dari muatan; koreksi rak via FIX | ya (objek: buang - dilakukan) |
| KD-N8 | Header resume tidak seragam tahun terbit | Peurifoy tanpa "Terbit:"; Holm/Mubarak eksplisit [I] | Inkonsistensi presentasi terukur (kelas KD-C8); guard umur tidak seragam dari lapis teks | ya (label BTC-04) |
| KD-N9 | INTAKE-RINGKAS (auto) tidak melacak CONSTRUCTION; R3-STATUS/GAP-ACQUISITION-PLAN juga 0 | [B],[13] | Buta-titik register alat atas intake manual T24, bukan cacat angka; statistik register alat UNDERCOUNT domain ini | tidak (catatan hilir) |

Kontradiksi internal antar-resume: tidak ada selisih angka antar-lapis-teks - semua pointer
cocok ([15]), tak ada ambang yang bisa dibenturkan karena nol. KD-N1..N8 wajib ditandai di
semua lapis yang dibaca agen sebelum vonis rilis domain [V-12]; sebagian besar lewat kartu
D2-FIXx (hanya-tambah), bagian redaksi lewat body objek ini (KD-N7 dibuang di sini).

### 6.3 Tabel BEBAN-RILIS (44 butir; predikat dari studi, objek ini WAJIB mematuhinya)

Predikat: READY = terbit dengan penanda sumber; LABEL-GUARD = terbit hanya dengan labelnya;
BELUM TERKONFIRMASI = butuh PDF primer oleh manusia; DILARANG TERBIT = tanpa sandaran di lapis
teks. Jumlah per predikat diverifikasi ulang oleh alat terhadap tabel di bawah
(24 + 7 + 5 + 8 = 44), bukan dihitung tangan.

#### 6.3.1 READY (24 butir) - naik sebagai muatan

| ID | Butir | Marker sumber |
|---|---|---|
| RD-01 | Laci 05/CONSTRUCTION tidak punya RANTAI-JAMINAN; rantai baru berasal dari studi ini, putus @4 (+ sebagian @2 konteks ID) | [ukur 1 [1]; Bagian 4] |
| RD-02 | GAP-019 R1 AHSP/SNI harga satuan, MENENGAH, terbuka - satu-satunya gap berdomain CONSTRUCTION | [GAP-REGISTER.csv:20 verbatim; ukur [3]] |
| RD-03 | Peta bab->halaman Peurifoy (bab 1-16; pointer 57/115/164/201/240/284/348/392/463/503/564/622/687/760/842) | [R3, Peurifoy resume:21-38; kartu seksi 1] |
| RD-04 | Peta bagian->halaman Holm (I 30, II 90, III 150, IV 200, V 234, VI 292, Apendiks 338) | [R3, Holm resume:20-28] |
| RD-05 | Peta bab->halaman Mubarak (2-12; pointer 35/43/65/113/149/183/243/285/305/331/373) | [R3, Mubarak resume:21-33] |
| RD-06 | Uji silang pointer kartu-vs-resume 12/12 cocok, selisih nol | [ukur [15]] |
| RD-07 | Pertanyaan kanonik RAB alat = sewa vs beli + biaya per jam sesungguhnya; jawabannya bab 2 + R4 | [R3, Peurifoy:42-44] |
| RD-08 | Produktivitas alat di buku = taksiran umum, bukan angka produk; nyata dari lembar data [R4] + lapangan | [R3, Peurifoy:53-54; REF-CON-001:29-31] |
| RD-09 | Harga satuan Holm konteks Amerika Utara + usang bahkan di sana; yang dipakai METODE penyusunannya | [R3, Holm:46-48; REF-CON-002:31] |
| RD-10 | Estimasi awal/anggaran/penawaran punya ketelitian berbeda; menyebutkannya melindungi GSP | [R3, Holm:34-36] |
| RD-11 | Menilai penawaran subkontraktor = bab khusus (Holm IV) - cocok profil GSP (banyak pekerjaan disubkontrakkan) | [R3, Holm:41-42] |
| RD-12 | Mubarak tidak memasok durasi kegiatan; durasi dari produktivitas nyata + pengalaman sendiri | [R3, Mubarak:52-53; REF-CON-003 seksi 3] |
| RD-13 | Jalur kritis menentukan keterlambatan mana yang berarti dan mana yang tidak | [R3, Mubarak:37-38] |
| RD-14 | Jadwal yang tidak dimutakhirkan bukan alat kendali; mutakhirkan tanpa kehilangan dasar pembanding | [R3, Mubarak:40-42] |
| RD-15 | Pertukaran waktu-biaya menjawab "berapa biaya mempercepat dua minggu" dengan angka | [R3, Mubarak:44-45] |
| RD-16 | Jadwal benar-CPM sering tidak mungkin dikerjakan tanpa perataan sumber daya | [R3, Mubarak:47-48] |
| RD-17 | Lima laci R1 kosong 0 PDF; tujuh berkas laci R2 tanpa satu pun token AHSP/SNI/ASTM/ACI/AISC/ASCE - terukur | [ukur [5],[6]] |
| RD-18 | Nol angka uang di seluruh lapis teks domain (0 kemunculan pola Rp/$/dolar) - dasar terukur uji penolakan | [ukur 2 [D]] |
| RD-19 | Ketiga kartu ACTIVE, wewenang ambang seragam "no-unless-contract-adopts" | [MRR csv:44-46 terukur] |
| RD-20 | Penandaan angka: hasil hitung = PROJECT-DERIVED; angka produk = OEM-DERIVED; G3 untuk struktur menuntut orang kedua ahli bersertifikat | [REF-CON-001..003 seksi 6; ASSURANCE-GATES.md:52,59] |
| RD-21 | Peta gate: G1 (jadwal dasar beku + dasar penawaran), G2 (pemilihan metode), G6 (rekaman pemutakhiran = bukti kemajuan) | [kartu seksi 4; resume Menopang; heading G1 :23, G2 :42, G6 :99] |
| RD-22 | Bab peledakan di luar lingkup GSP + diatur ketat Indonesia | [R3, Peurifoy:59-60] |
| RD-23 | Rantai ketergantungan antar-buku: Peurifoy -> biaya (Holm) -> jadwal (Mubarak); waktu-biaya tak terpisahkan | [R3, Peurifoy:64-65; Holm:54-58; Mubarak:65-66] |
| RD-24 | Intake laci tercatat CHANGELOG:629-631 (T24, 3 buku); vonis batch "metodenya boleh dipakai, angka dan pasalnya tidak" :718-724 | [CHANGELOG terukur] |

#### 6.3.2 LABEL-GUARD (7 butir) - naik HANYA dengan labelnya

| ID | Butir | Label wajib |
|---|---|---|
| LG-01 | Klaim peringkat ketebalan seluruh-rak pada resume Peurifoy:16 | SUPERLATIF TIDAK KONSISTEN antar-lapis: sapuan klaim halaman semua resume [ukur 1 [16]]: CCNA Library 3.292 hal > Grondzik 1.855 > Peurifoy 1.282. Objek ini MEMBUANG klaim sebagai muatan (KD-N7); koreksi rak via FIX |
| LG-02 | "+-25% halaman tanpa lapis teks" (ketiga resume; Holm:50, Peurifoy:56, Mubarak implisit via kartu) | STATISTIK ATAS PDF, tidak terverifikasi lapis teks; pakai sebagai perkiraan berlabel; pencarian teks gagal = pakai bookmark |
| LG-03 | Jumlah halaman/bookmark 1.282/381, 355/347, 595/341 | KLAIM HEADER resume; konfirmasi = manusia buka PDF (BTC-01/02) |
| LG-04 | Tahun Peurifoy (ed. 9 tanpa "Terbit:" di header; 2018 hanya dari filename) | GUARD UMUR tidak dapat dieksekusi seragam dari lapis teks; semua <= 8 th, aman tapi berlabel (BTC-04; kelas KD-N8) |
| LG-05 | "Bagian yang paling sering dikerjakan asal-asalan dan paling menentukan apakah proyek untung" (Holm:38-39) | PERNYATAAN POLA PRAKTIK penulis resume; tidak ada register insiden di rak sebagai bukti |
| LG-06 | Pointer Holm:57 ke REF-PRQ-001 (manajemen proyek) | ADJACENCY PROJECT-QUALITY (V-15); kartu tujuan terbukti ada (ukur 2 [G]); pointer bukan penyerapan |
| LG-07 | "Pemasangan menara dan perangkat berat" (Peurifoy:48) | IRISAN DOMAIN: perhitungan struktur menara = rantai K (putus @4, ranah D1); CONSTRUCTION hanya memasok pemilihan alat/radius angkat; jangan terbaca sebagai kewenangan struktur |

#### 6.3.3 BELUM TERKONFIRMASI (5 butir) - naik HANYA dengan labelnya, dilarang mengikat

| ID | Butir | Kenapa | Jalan konfirmasi |
|---|---|---|---|
| BTC-01 | Jumlah halaman 1.282 / 355 / 595 | Klaim header resume; lapis teks tidak menghitung halaman dirinya sendiri | manusia buka PDF primer (lokasi+byte terukur Bagian 1.4) |
| BTC-02 | Jumlah bookmark 381 / 347 / 341 | sama | sama (kebijakan: PDF wewenang manusia, bukan keterbatasan alat) |
| BTC-03 | "Sekitar 25% halaman tanpa lapis teks" | Statistik atas PDF | manusia; objek IL pakai sebagai perkiraan berlabel |
| BTC-04 | Tahun terbit Peurifoy 2018 | HANYA dari nama berkas PDF; header menyebut "kesembilan" tanpa tahun | manusia; sampai itu klaim umur = "~8 th (dari filename)" berlabel |
| BTC-05 | Kandungan detail per halaman pointer (mis. apa di PDF 57 bab 2) | Lapis teks hanya menjamin judul bab + keberadaan pointer | manusia sebelum angka apa pun dari halaman itu dipakai |

#### 6.3.4 TIDAK DITERBITKAN - butir DILARANG TERBIT (8 butir kelas-nol)

Yang berikut TIDAK dinaikkan sebagai muatan: angkanya TIDAK ADA di lapis teks rak dalam bentuk
apa pun (terukur: 0 angka uang [D]; 0 PDF R1 [5]; 0 token R2 [6]; 0 entri katalog [10]) atau
merupakan klaim kepatuhan tanpa sandaran. Seksi ini pernyataan LARANGAN tanpa angka: menyajikannya
dengan angka = mengarang.

| ID | Yang dilarang terbit | Sumber yang seharusnya |
|---|---|---|
| DT-01 | SATU KALIMAT PUN positif "harga satuan kami sesuai AHSP/SNI" yang bersandar pada rak (UJI PENOLAKAN V-10 - inti delta D2) | salinan resmi AHSP/SNI analisis harga satuan (GAP-019) |
| DT-02 | Angka harga satuan mana pun dari buku Holm sebagai angka RAB Indonesia (konteks Amerika Utara + usang) | AHSP edisi berlaku + survei pasar setempat |
| DT-03 | Koefisien/angka overhead-laba "standar" sebagai nilai baku | kebijakan perusahaan + Holm bagian V sebagai metode |
| DT-04 | Angka produktivitas alat sebagai angka terjamin | lembar data alat [R4] + kalibrasi lapangan |
| DT-05 | Durasi kegiatan sebagai angka normatif | produktivitas nyata + pengalaman proyek [Mubarak:52-53] |
| DT-06 | Ketentuan klaim perpanjangan waktu "versi Mubarak" dipakai seolah syarat kontrak Indonesia | syarat kontrak setempat [Mubarak:55-56] |
| DT-07 | Prosedur/perkiraan peledakan sebagai lingkup kerja GSP | di luar lingkup + regulasi ketat [Peurifoy:59-60] |
| DT-08 | Pernyataan kepatuhan K3 konstruksi Indonesia bersandar pada rak | Permenaker PPPK (tidak ada; usulan U-1) |

Batas eksplisit: angka kelas DT-01..DT-08 TIDAK naik di objek ini dalam bentuk apa pun - bukan
angka, bukan contoh, bukan "misalnya". Jalur hilir = akuisisi AHSP/SNI resmi (GAP-019), lembar
data alat (R4), atau kebijakan perusahaan tertulis, lalu amandemen tercatat.

### 6.4 Kandidat ground-truth probe

Enam kandidat probe (P-1..P-6, dua jebakan: P-4 biaya per jam excavator, P-5 lokasi PDF +
INTAKE_ONLY basi) terdaftar di studi hulu Bagian 8.1 dengan jawaban kanonik + jalur bukti; objek
ini tidak menggandakannya (verifier mengukur sendiri ke rak). Rekap predikat: READY 24 +
LABEL-GUARD 7 + BELUM TERKONFIRMASI 5 + DILARANG TERBIT 8 = 44 butir. Pola identik
CIVIL-STRUCTURAL/SDCY: muatan siap-terbit didominasi METODA + PETA KEABSENAN; angka nilai murni
semua jatuh ke DILARANG TERBIT - payload yang terbit justru pernyataan batasnya.

---

## Bagian 7 - Gap register domain

### 7.1 Celah resmi GAP-REGISTER yang mengikat domain ini (verbatim register, terukur)

| Gap | Tingkat | Yang hilang | Prioritas | Status |
|---|---|---|---|---|
| GAP-019 | R1 | AHSP / SNI analisis harga satuan | MENENGAH | terbuka [csv:20] |
| GAP-015..018 | R1 | SNI 1727/1726/1729/2847 (ambang mutu struktur hasil pekerjaan) | TINGGI | terbuka - ranah D1/rantai K, dirujuk silang saja |
| GAP-020 | R2 | ASTM/SNI metode uji bahan | MENENGAH | terbuka - ranah D1 |
| GAP-014 | R4 | dokumentasi OEM per proyek | PER PROYEK | by-design - pola sama untuk lembar data alat |

Sinkronisasi GAP-019: catatan register sudah benar (verbatim cocok Holm resume:46-48 dan
REF-CON-002:31) - yang perlu = naikkannya ke lapis gerbang (usulan U-3). Gap sapuan lain
terwakili KD-N1..N6 + U-1..U-5.

### 7.2 Usulan celah/gap baru hasil studi (nomor final = controller, V-16 - JANGAN daftarkan diam-diam)

| Usulan | Tingkat | Butir | Dasar ukur |
|---|---|---|---|
| U-1 | R1 | Regulasi K3 konstruksi Indonesia (Permenaker PPPK, mis. Permenaker 05/2014) - tidak dirujuk SATU PUN lapis domain; laci PERMENAKER kosong | Bagian 4 mata 1/4; ukur [5]; sapuan K3/PERMENAKER di CSV = 0 |
| U-2 | - | Ekstraksi katalog: bangun seksi "konstruksi" di KATALOG-RUMUS dari 3 buku (pointer metode volume/produktivitas/CPM/waktu-biaya, TANPA angka ambang) | KD-N4; bukan akuisisi - kerja lapis teks |
| U-3 | - | Tambah baris CONSTRUCTION di "Belum ada sumber sah" AMBANG-TERIMA-INDUK (harga satuan + produktivitas + K3) | KD-N6; wewenang pengelola rak |
| U-4 | - | Tabel asumsi baku domain konstruksi (HSP sementara, produktivitas tanpa R4, durasi tanpa data) di ASUMSI-BAKU | KD-N5; wewenang pengelola rak |
| U-5 | - | Koreksi manifest INTAKE_ONLY laci CONSTRUCTION + sinkronisasi keluarga GAP-REGISTER.md | KD-N1/N2; wewenang pengelola rak (pola FIX D1) |

### 7.3 Yang justru KUAT di rak ini (agar objek tidak timpang)

Konsistensi penuh 12/12 pointer; guard metode-vs-angka tertulis eksplisit di TIGA lapis rak
sebelum registrasi (Holm resume:46-48, REF-CON-002:31, MRR notes csv:44-46); catatan GAP-019
verbatim akurat; PDF primer nyata 196.540.165 B; CHANGELOG:718-724 sejalan kartu; ketiga buku
saling merujuk membentuk rantai pelaksanaan-biaya-jadwal utuh sebagai metode (RD-23). Domain
lulus gerbang kelayakan karena keaslian bahan + kejujuran status, bukan tebalnya.

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek berisi metode yang menyembunyikan celah harga
= gagal maksud registrasi dan menabrak aturan EKAS. Vonis controller BUKAN "rak konstruksi
lengkap untuk RAB Indonesia" - yang terbit lapisan BATAS-PENGETAHUAN: peta metode
pelaksanaan-estimasi-penjadwalan + peta keabsenan norma harga.

1. **Status rantai apa adanya (tanpa perataan):** Rantai M (baru, berasal dari studi) **PUTUS di
   mata 4** dan **sebagian mata 2 untuk konteks Indonesia** - "METODE LENGKAP - ANGKA & NORMA
   TIDAK ADA" (Bagian 4). DILARANG KLAIM KESESUAIAN HARGA: tidak ada angka harga
   satuan/durasi/produktivitas boleh diterbitkan bersandar rak, dan tidak ada kalimat positif
   "harga satuan sesuai AHSP/SNI" boleh diterbitkan (DT-01; uji penolakan V-10). Terbit APA
   ADANYA; pernyataan batas standar (kepala dokumen ini) wajib ikut di setiap serah; meratakan
   status = cacat proses, custodian menolak. "Rantai utuh bila GAP-019 ditutup" OVERSTATED -
   yang tertutup hanya mata 3-4 harga, bukan ambang mutu (rantai K), K3 (regulasi), R4 (per
   proyek). Preseden KD-C9.
2. **Protokol keselamatan dan asumsi tidak boleh dilepas dari metode.** Irisan struktur menara
   (LG-07), bahaya crane, larangan peledakan, dan ketidakdapat-ujian K3 wajib terangkut ke
   setiap turunan objek ini (Bagian 5.2). Rak membuat GSP mampu MENYUSUN struktur estimasi dan
   menilai metode pelaksanaan - bukan menggantikan AHSP, survei pasar, lembar data alat, dan
   syarat kontrak.
3. **Keadaan rak: JANGAN kutip angka README/register alat sebagai fakta.** Statistik objek ini
   = yang terukur dari `GAP-REGISTER.csv` - README "empat celah R1" basi (KD-N3), MD gap
   register tidak sinkron (KD-N2), register alat BUTA domain ini sehingga UNDERCOUNT CONSTRUCTION
   (KD-N9).
4. **PDF primer belum dibuka manusia.** Vonis halaman = vonis lapis teks; wewenang manusia:
   BTC-01..BTC-05. Lokasi PDF di Bagian 1.4; laci [`ekas/`](../../ekas-lapis-teks/) = cermin; INTAKE_ONLY manifest = BASI
   (KD-N1) - tidak dikutip sebagai status sahih.
5. **Known-defect wajib ikut terangkut:** KD-N1..KD-N8 (rincian + bukti di 6.2; redaksi KD-N7
   sudah dibuang dari muatan objek ini) + KD-N9 catatan tanpa beban rilis. Penandaan rak
   menunggu kartu D2-FIXx (hanya-tambah) + penomoran controller U-1..U-5; sampai terpasang,
   vonis rilis domain ditahan. Bentuk lama tidak dihapus, hanya ditandai.
6. **Usia bahan.** Holm 2021, Mubarak 2019 eksplisit di header; Peurifoy ed. 9 TANPA tahun
   (2018 hanya dari filename - KD-N8, BTC-04). Umur tidak dihitung ulang dari lapis resume
   (melarang karangan); semua calon <= 8 th, guard 15-th aman tapi berlabel. Ketiganya R3 - tak
   satu pun ambang terima; Holm eksplisit usang angkanya bahkan untuk konteks aslinya.
7. **Adjacency (rujukan silang, tidak disalin).** PROJECT-QUALITY - pointer Holm:57 ->
   REF-PRQ-001 HANYA penunjuk lintas domain (V-15, LG-06); penyerapan butuh putusan controller.
   Ambang mutu struktur hasil pekerjaan sipil = ranah rantai K CIVIL-STRUCTURAL (putus juga) -
   objek ini tidak berwewenang atasnya (LG-07). Gedung = ranah D3; CAD = ranah D5.
8. **Sumber dan kebaruan ekstraksi.** Seluruh angka dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) diekstrak
   read-only 2026-09-29 oleh studi t_9edc0954; pengukuran = cetakan skrip
   `lib/c2-stu-evidence/c2_measure.py` + `c2_measure2.py`, bukan ingatan; short check studi
   VERDICT PASS ts 2026-09-29T06:45:20Z (18/18 koordinat cocok rak). [`ekas/`](../../ekas-lapis-teks/) read-only.
   Uji penolakan D2 (0 angka uang, rc=1) diverifikasi
   ulang controller sebelum vonis LAYAK.

STATUS: needs-review
