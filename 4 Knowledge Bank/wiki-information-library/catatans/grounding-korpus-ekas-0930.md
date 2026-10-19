---
id: grounding-korpus-ekas-0930
type: catatan
title: Korpus GROUNDING-LIGHTNING EKAS - peta metode ukur, kerangka rantai, dan batas pengetahuan (CVLK-0929)
status: active
catatan_verifikasi: "VERDICT: terverifikasi (gsp-custodian, 2026-09-30). ALASAN: 7 dimensi lolos dengan bukti ukur ulang - sampling 44 koordinat ke berkas rak nyata (43 HIT langsung; 1 MISS = false-negative needle verifier di GAP-REGISTER.md:46, konten 'terlengkap yang ada' terkonfirmasi hadir); meta PDF primer cocok persis (Joffe 1216 hal/bookmark 979; Uman 255 hal/bookmark 72) dan anchor teks p.579/580/581/1111/1149 + Uman p.62/p.90 kena isi (kalimat PDF 580 = peringatan bahaya melepas konduktor, mengonfirmasi D-C4-01); kepala RANTAI-D PUTUS @4 dikutip apa adanya tanpa perataan; sensus 16/5/2/4=27 == studi dan marker RD-01..RD-16 identik studi 16/16; DT-01..DT-04 tanpa angka telanjang (grep ambang ohm=0, 10/350=0, impuls spesifik=0 di body); tipografi em/en/middot=0, non-ASCII hanya U+03A9 x8 (omega satuan, whitelist verbatim rak); semua jalur rak terprobe ada; agregat 664 baris/28.294 B/27.859 char + sha12 x5 + ukuran PDF cocok ukur ulang disk. REKOMENDASI librarian sebelum promosi: pasang label interpretasi D-C4-01 dua arah (rak + skill fleet) via kartu FIX berizin; angkut kepala PUTUS @4, blok BATAS, dan register D-C4-01..08 apa adanya; normalisasi dash GAP-004 (U+2014 menjadi tanda hubung) sudah dideklarasikan objek - terdeclare, bukan cacat."
sumber: "docs/2026-09-29-cvl-knowledge-register/research/grounding-lightning-korpus-detail.md (hulu: studi t_87ac1a6e vonis LAYAK BERTINGKAT diterima controller (D-22); 220 baris / 20.506 B / sha256[:12] f9e647dab032 terukur ulang 2026-09-30; bahan terdaftar di Bagian 1 objek ini)"
halaman: marker [R-n, sumber, hal] per butir dipertahankan verbatim dari studi hulu; 'PDF nnn' = NOMOR PDF konvensi lapis teks rak (pointer lapis teks, BUKAN vonis halaman fisik oleh manusia); koordinat lapis teks ditulis 'berkas:baris' dan diukur segar 2026-09-30 (cetakan lib/c4-l1-evidence/c4l1_measure.py -> c4l1_evidence_measure.json)
tanggal_akses: 2026-09-30
kelas_bukti: sintesis
sensitif: tidak
perkara: cvlk-0929
tags: [grounding-lightning, pembumian, uji-pembumian, wenner, fall-of-potential, resistivitas-tanah, bonding, ekipotensial, apendiks-g, apendiks-h, proteksi-petir, rolling-sphere, joffe-lock, uman, iec-62305-2006-usang, rantai-D, putus-di-mata-4, nol-R1, nol-R2, metode-boleh-ambang-dilarang, jangan-tertukar-MOmega-vs-omega, GAP-001, GAP-004, known-defect]
links: [ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING, ekas/04_KNOWLEDGE-CARDS/GROUNDING-LIGHTNING, ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL, docs/2026-09-29-cvl-knowledge-register/research/grounding-lightning-korpus-detail.md]
defek-terkait: "register known-defect D-C4-01..D-C4-08 (8 butir: 1 TINGGI, 3 SEDANG, 1 SEDANG-metadata, 3 RENDAH per studi Bagian 6). D-C4-01 menembus rak + kartu + skill fleet - perbaikan label dua arah lewat kurasi, bukan sunting sepihak pekerja. Penandaan lapis rak menunggu kartu FIX berizin; vonis rilis domain ditahan sampai tanda terpasang."
penulis: gsp-grounding-specialist
diajukan: 2026-09-30
domain: GROUNDING-LIGHTNING
created: 2026-09-30
catatan_keputusan: "dipromosikan: CVLK-0929 C4-L2: verdict custodian independen terlampir di catatan_verifikasi, non-sensitif non-dosir; RANTAI-D rak terbit APA ADANYA PUTUS @4 tanpa perataan; D-C4-01 berlabel interpretasi + konsekuensi perilaku lapangan; 4 DT kelas-nol tanpa angka telanjang; provenance dua laci GROUNDING/LIGHTNING benar per berkas; GAP-001 rujukan silang ELECTRICAL + GAP-004 usang IEC 62305:2006 tercatat; skill fleet grounding-lightning-design hanya pointer; sensus==studi 16/5/2/4=27"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-30
dipromosikan-ke: catatans/grounding-korpus-ekas-0930.md
---

# Korpus GROUNDING-LIGHTNING EKAS - peta metode ukur, kerangka rantai, dan batas pengetahuan (CVLK-0929)

Objek master misi CVLK-0929 (id `grounding-korpus-ekas-0930`, type catatan, domain
GROUNDING-LIGHTNING = D4). Muatan = peta rak + angka kunci berpredikat + validasi RANTAI-D yang
SUDAH ADA di rak (mata 1-5, status PUTUS @4 dipertahankan apa adanya) + register known-defect +
celah resmi + batas kemampuan, satu berkas (SATU objek master per domain; bentuk ikut preseden
objek CIVIL-STRUCTURAL + CONSTRUCTION + BUILDING-CONSTRUCTION CVLK-0929 seksi 1-8). Provenans:
body dirakit dari SATU sumber studi `research/grounding-lightning-korpus-detail.md` (t_87ac1a6e
complete, 220 baris / 20.506 B, ekstraksi read-only `ekas/` + teks PDF primer via pypdf,
2026-09-30); vonis controller LAYAK BERTINGKAT (D-22) dengan dasar terukur: 6/6 alamat halaman
jangkar rantai kena isi saat diuji ke teks PDF primer, 0 pointer phantom halaman (1 pointer NAMUN
phantom: berkas pengadaan, D-C4-04), sensus predikat 27 butir. Kelas bukti sintesis - R3 buku
berupa METODE UKUR + KERANGKA RANTAI; domain NOL R1/R2/R4/R5 untuk domain ini (terukur); yang
tidak ada di rak dinyatakan "tidak ada di rak" beserta sumbernya.

PERNYATAAN BATAS STANDAR (wajib ikut terbit; [R3, RANTAI-JAMINAN.md:3-7; ukur 2026-09-30]): rak
ini TIDAK memiliki sumber sah untuk ambang resistansi pembumian - PUIL/SNI [R1] kosong terukur,
standar internasional edisi berlaku [R2] kosong untuk domain ini. Menghitung metode boleh;
menyatakan lulus TIDAK, kecuali lewat tiga jalan sah: (1) pemilik menetapkan ambang tertulis,
(2) kontrak mengadopsi standar tertentu, (3) lapor hasil ukur TANPA pernyataan lulus. Yang tidak
sah: mengisi angka ambang karena angka itu sering terdengar (guard rak: BACA-DULU.md:47,
AI-USAGE-POLICY.md:78, ASSURANCE-GATES.md:172, RANTAI-JAMINAN.md:31,:122, KATALOG-RUMUS.md:567 -
semua dalam bentuk penolakan/coretan, bukan klaim). Jangan tertukar: rak PUNYA ambang tahanan
isolasi MΩ (ANSI/NETA ATS-2017 [R2], milik domain ELECTRICAL) - itu BUKAN ambang resistansi
pembumian (Ω). Setiap pemakaian objek wajib membawa pernyataan ini apa adanya.

Peringatan ketipisan (syarat vonis): lapis teks domain 5 berkas / 28.294 B / 27.859 karakter
(terukur [M]) - tipis-terpusat: dua rujukan, keduanya R3. Sebagai ganti ketebalan, dua PDF primer
nyata ada dan terbaca teks (Joffe 139.612.063 B; Uman 26.856.687 B - cetakan 2026-09-30; catatan
drift: metadata handoff hulu menyebut 26.856.688 B, selisih 1 byte, cetakan alat giliran ini yang
dipakai). Yang terbit = densitas verifikasi (6/6 jangkar halaman kena isi teks primer) + kejujuran
status (PUTUS @4 apa adanya), bukan ketebalan. Wewenang: PDF hanya dibuka ALAT (pypdf read-only)
untuk uji lapis teks; vonis halaman visual (khususnya tabel bergambar/berekstraksi kacau) wewenang
manusia (AGENTS.md; preseden SDCY catatan-2); laci `ekas/` hanya cermin. Tipografi: rak asal
memakai U+2014/U+2013/U+00B7 + glif peringatan (tanda centang/peringatan/silang + lingkaran
nomor); objek ini nol semuanya - saat mengutip blok rak, glif dinormalisasi ekuivalen teks dan koordinat baris rak selalu
disertakan agar byte asli dapat ditelusuri; huruf Yunani satuan (rho, pi, Omega) dipertahankan
karena bermakna teknis. Konvensi hitung baris objek ini = wc -l (jumlah baris-akhir); cetakan
studi hulu memakai basis count-newline+1 (selisih tetap +1 per berkas, isi identik).

---

## Batas domain - apa yang TIDAK dicakup objek ini

| Area | Status | Alasan / kemana |
|---|---|---|
| Metode ukur resistivitas tanah (Wenner, koreksi jarak, profil multi-`a`) | CAKUP (metode + pointer halaman terverifikasi teks) | Joffe & Lock [R3] |
| Metode ukur resistansi terpasang (fall-of-potential tiga pasak, aturan 61,8%) | CAKUP (metode) | Joffe & Lock [R3] |
| Kerangka rantai pembumian: urutan kerja, bonding/ekipotensial, bukti serah (Apendiks G/H) | CAKUP (kerangka + daftar periksa pointer) | Joffe [R3]; RANTAI-D rak |
| Proteksi petir: kerangka rolling sphere, Level IV 60 m, kurva alternatif, peringatan mesh | CAKUP (metode; nilai tabel lengkap = BT, lihat 5.2) | Uman [R3] |
| Ambang resistansi pembumian (angka lulus/tidak lulus) | TIDAK DAPAT dicakup | R1 kosong terukur; DT-01; tiga jalan sah |
| Tingkat proteksi / koordinasi LPS mengikat per edisi berlaku | TIDAK DAPAT dicakup | SNI/IEC 62305 edisi berlaku absen; DT-02; GAP-004 |
| Parameter bentuk gelombang arus impuls petir (muatan spesifik per bentuk gelombang) | TIDAK DAPAT dicakup | kelas-nol: sapuan token di SELURUH ekas = 0 berkas kena; DT-03 |
| Pernyataan kepatuhan hukum instalasi listrik Indonesia | TIDAK DAPAT dicakup | GAP-001 terbuka; DT-04 |
| Ambang tahanan isolasi (MΩ, NETA Tabel 100.1) | TIDAK dicakup di sini | domain ELECTRICAL (pemegang sah); "Jangan tertukar" = guard internal rantai (pointer saja, V-15) |
| Data produk (elektroda, earth tester, SPD) | TIDAK ada | R4 lembar data pabrikan per proyek; laci R4 domain ini kosong terukur |
| Rancangan pembumian/petir proyek konkret | TIDAK dicakup | skill fleet `grounding-lightning-design` (adjacency V-15, pointer saja) |
| Hitungan sipil-struktur penunjang/tanah per proyek | TIDAK dicakup | ranah lain; tidak ada pointer hidup yang terukur dari domain ini |

---

## Bagian 1 - Peta isi

### 1.1 Lapis domain `ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/` + kartu (ukur segar 2026-09-30 [M])

| Berkas | Baris (wc -l) | Byte | Karakter | sha256[:12] | Peran |
|---|---|---|---|---|---|
| `RANTAI-JAMINAN.md` | 126 | 6.040 | 5.903 | 95e52d7d6162 | Rantai D mata 1-5, PUTUS @4 ditulis jujur di kepala |
| `R3 - Grounds for Grounding.md` (Joffe & Lock) | 245 | 10.765 | 10.578 | 59f934f0d74d | REF-GRD-001, Wenner/FOP/bonding/apendiks |
| `R3 - The Art and Science of Lightning Protection.md` (Uman) | 177 | 7.863 | 7.818 | cc9b01d8869e | REF-LPS-001, rolling sphere/tingkat proteksi |
| `04_KNOWLEDGE-CARDS/GROUNDING-LIGHTNING/REF-GRD-001.md` | 58 | 1.793 | 1.760 | 70aaeec2669c | kartu kendali Joffe |
| `04_KNOWLEDGE-CARDS/GROUNDING-LIGHTNING/REF-LPS-001.md` | 58 | 1.833 | 1.800 | 9c0b22b2bdb3 | kartu kendali Uman |
| TOTAL | 664 | 28.294 | 27.859 | - | cocok nominasi studi (baris: studi cetak +1 karena basis count-newline+1; byte/karakter identik) |

Domain TERHITUNG tipis-terpusat: dua rujukan, keduanya R3, nol R1/R2/R4/R5 untuk domain ini
([M]). Sensus kartu: 2 ACTIVE, `reference_confidence_level: R3`, kolom 3 seragam "Tidak
sendirian" (konsisten rantai putus @4).

### 1.2 Lapis kartu pengetahuan

Kedua kartu (`REF-GRD-001.md`, `REF-LPS-001.md`) ACTIVE, wewenang seragam `no-unless-contract-adopts`
di MASTER-REFERENCE-REGISTER.csv ([M]). Kartu REF-GRD-001:41 memuat prasyarat lepas-konduktor
tanpa label - titik penetrasi ketiga D-C4-01 (selain rantai dan skill fleet; lihat 6.2).

### 1.3 Lapis bersama dan registri (hasil sapuan segar [M])

| Berkas | Temuan terukur | Kedudukan objek |
|---|---|---|
| `ekas/02_REGISTERS/GAP-REGISTER.csv` | 2 baris berdomain GROUNDING-LIGHTNING: GAP-001 (shared ELECTRICAL), GAP-004 - keduanya TINGGI terbuka (verbatim di Bagian 7) | gap RESMI ADA (beda BUILDING-CONSTRUCTION yang yatim); tidak ada usulan celah baru dari studi (nomor final tetap hak controller, V-16) |
| `ekas/02_REGISTERS/INTAKE-QUEUE.csv` | 12 baris bertoken domain ini - isinya brosur satelit-geospasial (4), datasheet PBX Yeastar (4), switch TP-Link (2), manual PSU Corsair (2): klasifikasi SESAT DOMAIN | D-C4-07; jangan dipromosikan ke laci domain ini |
| `ekas/02_REGISTERS/MASTER-REFERENCE-REGISTER.csv` | 2 baris (REF-GRD-001, REF-LPS-001); token ground* muncul 10 kali sebagai occurrence lintas kolom | cetakan studi "10 baris" = basis occurrence; basis baris = 2; isi identik, deklarasikan basis |
| `ekas/02_REGISTERS/INTAKE-RINGKAS.md:36` | "- **GROUNDING-LIGHTNING** - 12" (1 hit) | konsisten 12 baris INTAKE-QUEUE (yang sesat domain itu) |
| Guard "< 5" fleet-wide (sapuan segar [M]) | kemunculan angka ambang legendaris itu HANYA dalam konteks penolakan/coretan: `ekas/BACA-DULU.md:47`, `01_GOVERNANCE/AI-USAGE-POLICY.md:78` (keduanya coretan ~~...~~), `01_GOVERNANCE/ASSURANCE-GATES.md:172`, `RANTAI-JAMINAN.md:31,:122`, `06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md:567` ("Tidak ada"), resume Joffe:211 (bentuk ternegasi). Positif-palsu disingkirkan: "< 5 MB" (CHANGELOG:594, R3-STATUS:36), "< 5 tahun" (AUTHORITY-STATUS:97, REFERENCE-CONFIDENCE-LEVEL:59) | bersih: tidak ada satu pun klaim ambang telanjang di rak; objek ini TIDAK mengulang angkanya (DT-01) |
| `ekas/02_REGISTERS/GAP-REGISTER.md:3` | kepala masih menyebut path basis lama `C:\Users\gspen\Videos\Buku` (pra-migrasi) | D-C4-08; MD naratif tidak memakai ID GAP-nnn - sinkron ID hanya hidup di CSV (kondisi, bukan defect baru) |

### 1.4 Lapis sumber - provenance DUA LACI (delta V-9 D4; hasil cek segar [M])

| Laci (cermin `ekas/`) | Isi cermin terukur | Klaim `_ISI.md` | PDF nyata (`C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`) |
|---|---|---|---|
| `R3_TEXTBOOK-HANDBOOK/GROUNDING/` | hanya `_ISI.md` 231 B | "1 berkas. Berkas fisik **sudah berada di laci ini**" - SALAH ALAMAT | `Elya B. Joffe, Kai-Sang Lock - Grounds for Grounding (2nd Edition, 2023).pdf` = 139.612.063 B |
| `R3_TEXTBOOK-HANDBOOK/LIGHTNING/` | hanya `_ISI.md` 225 B | klaim sama - SALAH ALAMAT | `Martin A. Uman - The Art and Science of Lightning Protection (2008).pdf` = 26.856.687 B |
| `R1_NATIONAL-NORMATIVE/PUIL/` | hanya `_ISI.md` "**Kosong.**" | konsisten | - |
| `R1_NATIONAL-NORMATIVE/SNI/` | hanya `_ISI.md` "**Kosong.**" | konsisten | - |
| `R2_INTERNATIONAL-STANDARDS/IEC/` | hanya `_ISI.md` (+ anotasi defect NWSKILL-0923/D2-FIXx) | klaim salah alamat SUDAH dianotasi untuk fiber (domain lain) | IEC 61280-4-2 (fiber, domain lain) |

Kedua laci primer ADA dan benar identitasnya (Joffe di GROUNDING, Uman di LIGHTNING - tidak
tertukar); ukuran yang diklaim `_ISI.md` (133,1 MB / 25,6 MB) cocok sebagai MiB dengan ukuran
terukur - identitas berkas sahih, ALAMATNYA yang cacat -> D-C4-03 (kelas sama dengan anotasi
laci IEC, belum beranotasi di kedua laci ini). Alamat benar untuk verifikasi manusia = jalur
`gsp-ekas/lengkap` di atas; `ekas/` hanya cermin (preseden SDCY K-6).

---

## Bagian 2 - Nol R1, nol R2: tidak ada norma Indonesia maupun standar petir di rak

Konsekuensi pengikat (dinyatakan penuh di kepala RANTAI-D, Bagian 4): TIDAK ADA angka ambang
resistansi pembumian maupun tingkat proteksi yang boleh naik sebagai ambang lulus/tidak lulus;
seluruh muatan sah domain ini adalah METODE (R3) + tiga jalan sah generik
[ASSURANCE-GATES.md:160-172].

### 2.1 Lapis R1 (norma Indonesia): KOSONG - terukur + diakui

Laci PUIL dan SNI hanya berisi `_ISI.md` "**Kosong.**" ([M]; cek segar 2026-09-30). Tidak ada
ambang resistansi pembumian mengikat, tidak ada SNI proteksi petir. Kelas-nol berikut DILARANG
TERBIT (daftar tanpa angka di 5.3): ambang resistansi dalam ohm; tingkat proteksi/LPS mengikat
per edisi berlaku; parameter bentuk gelombang arus impuls; pernyataan kepatuhan hukum Indonesia.

### 2.2 Lapis R2 (standar internasional): KOSONG untuk domain ini - terukur

Laci IEC hanya memuat IEC 61280-4-2 (fiber, domain lain). ANSI/NETA ATS-2017 [R2] ada di rak
tetapi milik domain ELECTRICAL (tahanan isolasi MΩ) - POINTER saja: rantai GROUNDING sendiri
sudah menegaskan "Jangan tertukar" (MΩ isolasi != Ω pembumian, RANTAI-JAMINAN.md:79-91) dan itu
konsisten dengan rantai ELECTRICAL yang memegang Tabel 100.1. GAP-001 shared dengan ELECTRICAL =
rujukan silang SATU entri registri dua domain, bukan salinan (sesuai delta D4; sudah begitu di
CSV, pertahankan).

### 2.3 Lapis R3 (dua buku): METODE yang TERVERIFIKASI sampai teks PDF primer

Verifikasi studi hulu = dibaca langsung dari lapisan teks PDF primer (pypdf, ekstraksi nyata;
bukan ingatan): 6/6 alamat halaman jangkar rantai kena isi yang diklaim (PDF 562/579/580/1111/1149
+ Uman 89-90); meta buku cocok persis (Joffe 1.216 hal / bookmark 979; Uman 255 hal / bookmark
72); peta bab Uman 1-14 + Preface cocok 100% outline; peta bab + apendiks Joffe cocok outline
(Bab 3=167, Bab 10 area 553+, Ap G=1111, Ap H=1149). Muatan angka terverifikasi per butir dengan
predikat = Bagian 3 (RD-01..RD-16), 5.1 (LABEL-GUARD), 5.3 (BELUM TERKONFIRMASI).

### 2.4 Lapis R4 (produk): kosong untuk domain ini

Tidak ada lembar data pabrikan (elektroda, earth tester, SPD) di laci R4 untuk domain ini. Semua
angka produk: "menunggu data pabrikan". Catatan silang: 12 baris INTAKE-QUEUE berlabel domain ini
ternyata datasheet perangkat domain LAIN (D-C4-07) - jangan dianggap sebagai R4 domain ini.

### 2.5 Lapis R5: kosong untuk domain ini - terukur.

---

## Bagian 3 - Angka kunci READY (16 butir) - muatan yang naik

Penanda sumber persis seperti studi hulu 2.3 (butir 1-16); verifikasi = ekstraksi teks PDF primer
giliran studi, cetakan `lib/c4-stu-evidence/`. Predikat seluruh baris: READY (terbit dengan
penanda sumber).

| ID | Butir | Marker sumber |
|---|---|---|
| RD-01 | Wenner susunan 4 elektroda; rho = 4*pi*a*R / (1 + 2a/sqrt(a^2+4b^2) - a/sqrt(a^2+b^2)) (Pers. 10.17) | [R3, Joffe, PDF 579] |
| RD-02 | Bentuk praktis rho = 2 pi a R (Pers. 10.18); rata-rata resistivitas sampai kedalaman ~a | [R3, Joffe, PDF 580] |
| RD-03 | Keterbatasan Wenner jarak besar -> sarankan Schlumberger-Palmer | [R3, Joffe, PDF 580] |
| RD-04 | Fall-of-potential tiga pasak; aturan 61,8% (X0 = 0,62 d) | [R3, Joffe, PDF 580-582] |
| RD-05 | Prinsip: resistansi pembumian sebanding resistivitas medium -> survei dahulu, baru konfigurasi elektroda | [R3, Joffe, PDF 562] |
| RD-06 | Apendiks G daftar periksa verifikasi (judul tepat di halaman) | [R3, Joffe, PDF 1111] |
| RD-07 | Apendiks H isi dokumentasi serah (judul tepat di halaman) | [R3, Joffe, PDF 1149] |
| RD-08 | Radius bola gelinding Level IV = 60 m (disebut eksplisit di teks terkait Tabel 4.1) | [R3, Uman, PDF 90] |
| RD-09 | Kurva alternatif: Level IV -> 54 m atau 48 m; Level II 30 m -> 23/24 m | [R3, Uman, PDF 90] |
| RD-10 | Peringatan mesh: bola gelinding meramalkan sambaran DALAM mesh; IEC tanpa teori pembenaran ukuran mesh - ukuran mesh BUKAN pengganti analisis bola gelinding | [R3, Uman, PDF 90] |
| RD-11 | Ketinggian bangunan > 60 m hampir pasti tersambar; terminal sisi dinding | [R3, Uman, PDF 89] |
| RD-12 | Sudut kerucut setara dapat dihitung per tingkat proteksi/ketinggian | [R3, Uman, PDF 90] |
| RD-13 | Striking distance sebagai dasar fisika zona lindung (Bab 3) | [R3, Uman, PDF 65] |
| RD-14 | Daftar mitos pembumian (rod mencegah sengatan; tambah rod; netral+ground banyak titik) - kutipan verbatim terverifikasi ADA di PDF 32 (area Bab 1; frasa lokator resume menyesatkan - D-C4-05) | [R3, Joffe, PDF 32] |
| RD-15 | Sikap single-point vs multipoint; multipoint ke baja bangunan untuk lingkungan transien | [R3, Joffe, PDF 175-181] |
| RD-16 | Contoh tegangan langkah (parameter 70 kg, 100 ohm-meter, 3 s - nilai contoh terverifikasi, BUKAN ambang) | [R3, Joffe, PDF 402] |

Catatan enumerasi (jujur ke custodian): sensus studi menghitung READY = 16 dengan enumerasi
"butir 1-16, 19"; butir 19 (fakta-kutipan "Uman mengutip IEC 62305-1..5:2006 + NFPA 780:2004",
[R3, Uman, PDF 62], teks persis terverifikasi) TIDAK dinaikkan di sini sebagai baris payload
terpisah agar sensus dua kolom objek == studi (16/5/2/4 = 27); isinya hidup sebagai fakta-kutipan
di Bagian 4 (mata 1) dan Bagian 7 (GAP-004). Bila controller menghendaki baris tersendiri, sensus
naik jadi 17/5/2/4 = 28 dan studi hulu perlu diamandemen - keputusan controller, bukan pekerja.

---

## Bagian 4 - RANTAI-D: SUDAH ADA di rak, tervalidasi, PUTUS @4 dipertahankan APA ADANYA

Beda dengan C1..C3 (rantai lahir dari studi lalu diterbitkan): rantai domain ini sudah hidup di
rak dan TIDAK disunting oleh studi maupun objek ini. Validasi = setiap pointer halaman dibuka ke
teks PDF primer (pypdf) dan diuji isi semantiknya. Kepala rantai dikutip dari rak
(RANTAI-JAMINAN.md:3-7, sha256[:12] 95e52d7d6162; glif dinormalisasi, kata utuh):

> ### RANTAI INI PUTUS DI MATA 4
> **Tidak ada sumber sah untuk ambang resistansi pembumian di rak ini.** Diterbitkan dalam keadaan
> putus **dengan sengaja**, supaya kelemahannya terlihat sebelum dipakai - bukan setelah
> dipersoalkan pemeriksa.

### 4.1 Hasil validasi per mata (studi Bagian 3)

| Mata | Isi rantai | Vonis validasi |
|---|---|---|
| Kepala PUTUS @4 | sengaja diterbitkan putus | **PERTAHANKAN APA ADANYA** - diverifikasi: tidak ada sumber sah ambang di rak (laci R1/SNI kosong terukur; sapuan threshold-like di Joffe PDF 553/562/579/580/1031 = 0 kena) |
| 1 Rujukan | Joffe R3 [PDF 562, 579-580, 1111, 1149]; Uman R3 [PDF 89-90]; PUIL/SNI R1 TIDAK ADA; SNI/IEC 62305 berlaku TIDAK ADA; pemilik sistem per proyek | **SEMUA POINTER JANGKAR SAHIH** (6/6 alamat kena isi; rincian RD-01..RD-16). Penanda "Uman 2008 = 18 th" aritmetika benar (2026-2008). Fakta-kutipan: Uman mengutip IEC 62305-1..5:2006 + NFPA 780:2004 [R3, Uman, PDF 62] - edisi berlaku tetap tidak ada di rak (GAP-004) |
| 2 Keputusan desain | elektroda dari profil; bonding ekipotensial (pembumian terpisah per subsistem ditolak); level dari penilaian risiko (Level IV baku ditolak); proteksi internal wajib; ambang dari pemilik | **SAHIH** - konsisten resume + sumber (Uman Bab 6 PDF 114 surja internal; Joffe PDF 562 urutan kerja) |
| 3 Perhitungan | rho = 2 pi a R; multi-`a` -> profil; Level IV 60 m; mesh bukan pengganti | **SAHIH terverifikasi teks** (RD-02, RD-08..RD-10). Catatan enrichment (bukan cacat): aturan 61,8% FOP ADA di sumber (PDF 581-582) tapi TIDAK termuat di rantai/resume |
| 4 Pengujian (PUTUS) | metode FOP R3; prasyarat lepas konduktor; ambang lulus TIDAK ADA; Apendiks G; zona lindung vs bola gelinding | Struktur putus **BENAR dan dipertahankan**. Satu cacat semantik: baris "Prasyarat wajib" menunjuk PDF 580 yang kalimat sumbernya justru peringatan BAHAYA MELEPAS konduktor -> prasyarat wajib-lepas = INTERPRETASI rekayasa dari metode FOP elektroda tunggal, BUKAN kutipan [R3] (D-C4-01, TINGGI; label wajib di 5.1 LG-01) |
| 5 Bukti serah | BA, data Wenner per titik, konfigurasi, pernyataan lepas-konduktor, kalibrasi, ambang+sumber, Apendiks G/H, kartu kendali putus | Kerangka R3 sahih (alamat Apendiks G/H terverifikasi). Butir "pernyataan konduktor dilepas" ikut label interpretasi D-C4-01 |
| Penutup "Cara menutup" | tiga jalan sah + rujukan `DAFTAR-PENGADAAN-BAHAN.md` urutan kedua | Tiga jalan sah konsisten kebijakan generik. **Pointer berkas pengadaan PHANTOM** - find ekas + seluruh shared ws = 0 berkas (D-C4-04) |

### 4.2 Tiga jalan sah (isi rantai :113-124, dinormalisasi; wajib ikut setiap turunan)

Selama R1 belum ada di rak, pilih SATU dan NYATAKAN: (1) pemilik sistem menetapkan ambang secara
tertulis - cantumkan surat penetapannya sebagai lampiran berita acara; (2) kontrak menyebut
standar tertentu - peroleh salinannya, kutip pasalnya, ambang naik menjadi R1/R2; (3) nyatakan
hasil ukur TANPA pernyataan lulus/tidak lulus - berita acara memuat angka terukur dan metode,
dengan catatan penilaian menunggu penetapan ambang. Yang tidak sah: mengisi angka ambang warisan
"karena sering terdengar" - pada pekerjaan pembumian angka begitu justru mudah dipersoalkan karena
setiap pemeriksa berpengalaman tahu angkanya bergantung kebutuhan sistem.

### 4.3 Tabel BOLEH / TIDAK BOLEH dikatakan (untuk editor proposal, BA, Spesifikasi Teknis)

| Boleh | Tidak boleh |
|---|---|
| "Resistivitas tanah diukur metode Wenner, rho = 2 pi a R [R3, Joffe PDF 579-580]; ukur beberapa nilai `a` -> profil kedalaman, bukan satu angka." | Mengasumsikan resistivitas tanah tanpa survei - seluruh desain menjadi tebak-tebakan (RD-02/RD-05). |
| "Resistansi elektroda terpasang diukur fall-of-potential tiga pasak, aturan 61,8% [R3, Joffe PDF 580-582]; hasil dilaporkan sebagai angka terukur + metode TANPA pernyataan lulus (jalan sah 3)." | Menyatakan lulus/tidak lulus tanpa ambang dari penetapan pemilik tertulis atau kontrak yang mengadopsi standar (DT-01). |
| "Zona lindung dianalisis dengan bola gelinding per tingkat proteksi rancangan; radius Level IV 60 m [R3, Uman PDF 90]; catat bahwa buku mengutip IEC 62305:2006 (usang - GAP-004)." | Menjadikan 60 m sebagai pilihan baku tanpa penilaian risiko (mata 2 rantai); menyalin nilai lengkap Tabel 4.1/4.2 sebelum transkripsi manusia (BT-01/BT-02). |
| "Prasyarat ukur: konduktor penghubung dilepas dari elektroda sebelum pengukuran - praktik rekayasa (INTERPRETASI dari syarat isolasi elektroda pada metode FOP; varian tanpa-lepas dibahas terpisah di sumber PDF 584), BUKAN kutipan [R3] (D-C4-01); BA mencatat pelepasan + mitigasi bahaya pelepasan." | Mengutip prasyarat ini sebagai kalimat [R3] verbatim dari PDF 580 - kalimat sumber sebenarnya adalah peringatan BAHAYA melepas konduktor, bukan norma wajib-lepas (sapuan must/should+disconnect PDF 553-590 = 0 norma). |
| "Verifikasi bonding & ekipotensial mengikuti daftar periksa Apendiks G [R3, Joffe PDF 1111]; dokumentasi serah mengikuti Apendiks H [R3, PDF 1149] - dapat dipakai apa adanya." | Menukar tahanan isolasi (MΩ, NETA Tabel 100.1 [R2], ranah ELECTRICAL) dengan resistansi pembumian (Ω) - BA menyebut standar yang tidak mengatur yang diuji. |
| "Proteksi surja internal direncanakan bersama eksternal - proteksi eksternal saja ditolak (kerusakan berulang umumnya karena ketiadaan proteksi internal) [R3, Uman Bab 6 PDF 114 via rantai]." | Menjanjikan tingkat proteksi mengikat per edisi standar berlaku (DT-02; SNI/IEC edisi berlaku tidak ada di rak). |

---

## Bagian 5 - Tabel beban-rilis (27 butir; predikat dari studi, objek ini WAJIB mematuhinya)

### 5.0 Rekap sensus predikat (dua kolom; WAJIB identik dengan studi Bagian 4)

| Predikat | Jumlah |
|---|---|
| READY | 16 |
| LABEL-GUARD | 5 |
| BELUM TERKONFIRMASI | 2 |
| DILARANG TERBIT | 4 |
| Total butir dinilai | 27 |

Predikat: READY = terbit dengan penanda sumber; LABEL-GUARD = terbit HANYA dengan labelnya;
BELUM TERKONFIRMASI = butuh PDF primer dibuka manusia; DILARANG TERBIT = tanpa sandaran di rak,
dilarang terbit dalam bentuk angka apa pun. Pemetaan per-ID: RD-01..RD-16 = studi 2.3 butir 1-16
(catatan enumerasi butir 19 di bawah Bagian 3); LG-01..LG-05 = studi Bagian 4 baris LABEL-GUARD;
BT-01..BT-02 = studi 2.3 butir 17 (dua tabel); DT-01..DT-04 = studi 2.1 (empat kelas-nol).

### 5.1 LABEL-GUARD (5 butir) - naik HANYA dengan labelnya

| ID | Butir | Label wajib |
|---|---|---|
| LG-01 | Prasyarat ukur FOP: konduktor penghubung dilepas dari elektroda sebelum diukur (bentuk rak: "prasyarat wajib-lepas", RANTAI:68,:74,:102; resume Joffe:115,:187; REF-GRD-001:41; skill fleet SKILL.md:52 + references/01:15) | INTERPRETASI REKAYASA dari syarat isolasi elektroda pada metode fall-of-potential (varian tanpa-lepas dibahas terpisah di sumber PDF 584) - BUKAN kutipan [R3]: kalimat PDF 580 yang dirujuk justru peringatan BAHAYA melepas konduktor; penanda [R3]-nya salah level (D-C4-01). Konsekuensi perilaku lapangan: praktiknya tetap dijalankan (hasil gabungan sistem tidak sah untuk BA) tetapi BA/jawaban klien TIDAK boleh mengutip "sumber Joffe PDF 580" untuk normanya - kutip sebagai praktik metode + catat mitigasi bahaya pelepasan |
| LG-02 | Karakterisasi resume Joffe: "buku pembumian paling lengkap di rak ini, dan salah satu yang paling lengkap yang ada" (resume:11) | OPINI tanpa pembanding terukur (D-C4-06) - label opini atau hapus saat promosi; tidak memuat angka |
| LG-03 | Karakterisasi rantai/resume: "Tabel 4.1 tersimpan sebagai GAMBAR tabel" (RANTAI:57) | KARAKTERISASI MENYESATKAN (D-C4-02): lapisan teks PDF 89-90 SEBENARNYA memuat data tabel (ekstraksi kacau, kolom tergabung); guard "buka PDF langsung" tetap benar - pertahankan guard, koreksi karakterisasi |
| LG-04 | Klaim manifest `_ISI.md` dua laci: "berkas fisik sudah berada di laci ini" | SALAH ALAMAT (D-C4-03): cermin `ekas/` hanya berisi `_ISI.md`; PDF nyata di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/` (ukuran cocok sebagai MiB); tempelkan anotasi defect kelas NWSKILL-0923/D2-FIXx ke kedua laci |
| LG-05 | Rujukan penutup rantai: "urutan kedua `DAFTAR-PENGADAAN-BAHAN.md`" (RANTAI:126) | POINTER PHANTOM (D-C4-04): berkas 0 ditemukan di ekas maupun shared ws (find segar 2026-09-30) - jangan dikutip sebagai alamat; tunjukkan lokasi sebenarnya atau ganti rujukan ke GAP-ACQUISITION-PLAN.md |

### 5.2 BELUM TERKONFIRMASI (2 butir) - naik HANYA dengan labelnya, dilarang mengikat

| ID | Butir | Kenapa | Jalan konfirmasi |
|---|---|---|---|
| BT-01 | Nilai lengkap Tabel 4.1 Uman per tingkat proteksi I-III | lapisan teks ADA tapi ekstraksi kacau (kolom tergabung, mis. artefak "I2 0"); 60 m/54 m/48 m/30 m terbaca teks sebagai kalimat terpisah (sudah naik sebagai RD-08/RD-09) - TRANSKRIPSI tabel utuh belum sah | manusia buka PDF primer 89-90; sampai itu dilarang mentranskripsi tabel penuh dari output alat |
| BT-02 | Nilai Tabel 4.2 (ukuran mesh per tingkat proteksi) | idem - teks kacau; dan perhatikan RD-10: mesh bukan pengganti analisis bola gelinding | manusia buka PDF primer 90 |

### 5.3 TIDAK DITERBITKAN - butir DILARANG TERBIT (4 butir kelas-nol, TANPA angka)

Yang berikut TIDAK dinaikkan sebagai muatan: angkanya TIDAK ADA di rak dalam bentuk apa pun
(terukur: laci R1 PUIL/SNI kosong; laci R2 domain kosong; sapuan token kelas impuls di SELURUH
ekas = 0 berkas kena). Menyajikan seksinya dengan angka = mengarang. Jalur hilir = akuisisi resmi
(lihat rekomendasi studi 5.2: PUIL/SNI via pembelian resmi - salinan bajakan DILARANG masuk vault;
IEC 62305 edisi berlaku via webstore IEC; SNI IEC 62305 via BSN; lembar data R4), lalu amandemen
tercatat.

| ID | Yang dilarang terbit | Sumber yang seharusnya |
|---|---|---|
| DT-01 | Angka ambang resistansi pembumian dalam ohm untuk pernyataan lulus/tidak lulus | PUIL/SNI [R1] (kosong) ATAU penetapan pemilik tertulis ATAU adopsi kontrak (tiga jalan sah, 4.2); guard rak sudah berbentuk penolakan (1.3) - objek ini tidak mengulang angkanya |
| DT-02 | Tingkat proteksi / koordinasi LPS yang dinyatakan mengikat per edisi standar berlaku | SNI / IEC 62305 edisi berlaku [R1/R2] - absen; Uman hanya fakta-kutipan edisi 2006 (usang, GAP-004) |
| DT-03 | Parameter bentuk gelombang arus impuls petir (kelas muatan spesifik per gelombang) | tidak ada di rak - sapuan token kelas ini di SELURUH ekas = 0 berkas kena (cetakan studi [measure]) |
| DT-04 | SATU KALIMAT PUN pernyataan kepatuhan instalasi listrik/proteksi petir Indonesia bersandar rak ini | GAP-001 (shared ELECTRICAL) - PUIL/SNI kosong; uji penolakan sekelas V-10 domain D3 |

---

## Bagian 6 - Known-defect

### 6.1 Temuan kelas-nol (jawaban atas kelas yang diminta blueprint)

Sapuan lapis teks + laci: laci R1 PUIL/SNI "**Kosong.**" (terukur [M]); laci R2 domain kosong;
sapuan token kelas impuls = 0 berkas kena fleet-wide; ambang ohm hanya hidup sebagai PENOLAKAN
(coretan/larangan) di enam koordinat (1.3). Pertanyaan "berapa ambang ohm menurut rak?" dijawab
benar hanya dengan: "rak tidak punya sumber sah; jalur benar = penetapan pemilik / adopsi kontrak
/ laporan tanpa pernyataan lulus" - menjawab angka = karangan = FAIL (DT-01).

### 6.2 Register known-defect D-C4 (usulan studi Bagian 6; koreksi lewat register, BUKAN suntingan sepihak; koordinat dipersegar [M])

| ID | Kelas | Severity | Lokasi (koordinat segar) | Temuan | Tindakan disarankan |
|---|---|---|---|---|---|
| D-C4-01 | semantik/atribusi | TINGGI | RANTAI:68,:74,:102; resume Joffe:115,:187; REF-GRD-001:41; skill fleet SKILL.md:52 + references/01:15 | "Konduktor penghubung WAJIB dilepas sebelum diukur [R3, Joffe PDF 580]" - kalimat PDF 580 sebenarnya peringatan bahaya MELEPAS ("precautions ... in view of the danger of removing the connecting conductor"); norma wajib-lepas tidak ditemukan di PDF 553-590. Praktik sahih sebagai INTERPRETASI teknik FOP elektroda tunggal (bandingkan PDF 584 varian tanpa-lepas), tapi penanda [R3]-nya salah level. KONSEKUENSINYA NYATA: label keliru ini menembus skill fleet + kartu - agen yang mengajarkannya sebagai kutipan akan membela angka/norma ke klien dengan rujukan yang salah | Ubah jadi "praktik rekayasa (INTERPRETASI dari metode FOP), bukan kutipan [R3]"; sinkronkan label DUA ARAH (rak + skill fleet) lewat kurasi (bukan sunting sepihak pekerja) |
| D-C4-02 | karakterisasi | SEDANG | RANTAI:57; resume Uman:148; skill fleet | "Tabel 4.1 tersimpan sebagai GAMBAR tabel" - lapisan teks PDF 89-90 sebenarnya memuat data tabel (ekstraksi kacau); guard "buka PDF" tetap benar, karakterisasi menyesatkan | Koreksi karakterisasi; transkripsi manusia untuk Tabel 4.1/4.2 (BT-01/BT-02) |
| D-C4-03 | alamat bukti | SEDANG | `_ISI.md` laci R3/GROUNDING + R3/LIGHTNING | Klaim "berkas fisik sudah berada di laci ini" salah - cermin hanya berisi `_ISI.md`; PDF nyata di gsp-ekas/lengkap (139.612.063 B / 26.856.687 B terukur [M]). Kelas sama dgn anotasi NWSKILL-0923/D2-FIXx (laci IEC) tapi belum beranotasi di sini | Tempelkan anotasi defect kelas yang sama ke kedua laci |
| D-C4-04 | pointer phantom | SEDANG | RANTAI:126 | Rujukan "urutan kedua `DAFTAR-PENGADAAN-BAHAN.md`" - find ekas + shared ws = 0 berkas (sapuan segar [M]) | Tunjukkan lokasi sebenarnya atau ganti rujukan ke GAP-ACQUISITION-PLAN.md |
| D-C4-05 | lokator | RENDAH | resume Joffe:72 | Kutipan mitos disebut "dikutip di halaman pembuka bab (PDF 32)" padahal Bab 3 mulai PDF 167; kutipan memang ADA di PDF 32 (area Bab 1) - verifikasi isi LULUS, frasa lokator menyesatkan | Perbaiki frasa saat revisi berikutnya |
| D-C4-06 | superlatif | RENDAH | resume Joffe:11; GAP-REGISTER.md:46 | "paling lengkap ... yang ada" tanpa pembanding terukur - opini; tak memuat angka | Label opini atau hapus saat promosi (LG-02) |
| D-C4-07 | metadata registri | SEDANG | INTAKE-QUEUE.csv:95-98,:238-245 (12 baris) | Isinya brosat satelit-geospasial, datasheet PBX Yeastar, switch TP-Link, manual PSU Corsair - klasifikasi domain sesat; mencemari akuisisi R4 domain nanti | Triase ulang baris; jangan dipromosikan ke laci domain ini |
| D-C4-08 | warisan | RENDAH | GAP-REGISTER.md:3 | Path basis lama `C:\Users\gspen\Videos\Buku` (pra-migrasi) masih tercantum di kepala | Perbarui kepala saat revisi |

**Defect count: 8** (1 TINGGI, 3 SEDANG + 1 SEDANG-metadata, 3 RENDAH). Sinkron CSV (delta D4):
sumber kebenaran = GAP-REGISTER.csv; MD naratif tidak memakai ID GAP-nnn - kondisi, bukan defect
baru. Catatan verifikasi silang objek ini: cetakan occurrence vs baris registri dibedakan basis
(1.3); tidak ada defect BARU yang ditemukan saat perakitan - temuan segar [M] mengonfirmasi
delapan butir di atas apa adanya.

---

## Bagian 7 - Gap register domain (verbatim CSV, terukur ulang [M] 2026-09-30)

```
GAP-001,R1,PUIL / SNI kelistrikan,Kepatuhan instalasi listrik Indonesia,"ELECTRICAL, GROUNDING-LIGHTNING",TINGGI,terbuka,"ANSI/NETA menutup ambang uji, BUKAN kepatuhan hukum Indonesia"
GAP-004,R1,SNI proteksi petir,Kepatuhan proteksi petir,GROUNDING-LIGHTNING,TINGGI,terbuka,Uman mengutip IEC 62305:2006 - usang
```

(baris CSV 2 dan 5. Normalisasi tipografi terdeclare: baris GAP-004 asli memakai satu tanda pisah
panjang (U+2014) sebelum kata "usang" - di objek ini diganti tanda hubung biasa demi gerbang
tipografi A1/A2; byte asli tetap di `GAP-REGISTER.csv:5` dan tidak mengubah makna apa pun.)

GAP-001 = SATU entri registri dua domain (ELECTRICAL + GROUNDING-LIGHTNING): rujukan silang,
BUKAN salinan - begini di CSV, pertahankan (delta D4). GAP-004 khusus domain ini: dasar acuan
petir di rak (Uman) mengutip IEC 62305:2006 yang usang - tingkat proteksi mengikat per edisi
berlaku tetap tidak dapat ditetapkan dari rak (DT-02). Protokol hidup selama kedua gap terbuka:
rantai putus @4 + tiga jalan sah (4.2) - sudah tertulis di rak, tidak diubah. Usulan celah BARU
dari studi ini: TIDAK ADA (kelas-nol sudah terwakili GAP-001/004 + "tidak ada di rak" untuk kelas
impuls); nomor final registri tetap hak controller (V-16).

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Vonis controller LAYAK BERTINGKAT - yang terbit
lapisan BATAS-PENGETAHUAN: kerangka metode ukur + validasi rantai + keabsenan ambang; BUKAN rak
ambang terima dan BUKAN rak kepatuhan hukum Indonesia.

1. **Status rantai apa adanya (tanpa perataan):** RANTAI-D **PUTUS di mata 4** - "Tidak ada
   sumber sah untuk ambang resistansi pembumian di rak ini" (Bagian 4). Terbit APA ADANYA;
   kepala putus wajib ikut setiap turunan (BA, proposal, spesifikasi). Meratakan status = cacat
   proses. "Rantai selesai bila PUIL/SNI dibeli" OVERSTATED - tertutup hanya dasar mata 4 nasional;
   edisi IEC 62305 berlaku tetap milik GAP-004; R4 tetap per proyek; ambang per kasus tetap bisa
   minta penetapan pemilik.
2. **D-C4-01 mengubah cara berbicara, bukan cara mengukur:** praktik lepas-konduktor TETAP
   dijalankan (prasyarat keabsahan hasil untuk elektroda tunggal; tanpa itu yang terukur gabungan
   seluruh sistem - netral, pipa, baja bangunan - dan BA tidak sah), tetapi sebagai INTERPRETASI
   rekayasa berlabel, bukan kutipan [R3]; bahaya pelepasan konduktor (isi kalimat sumber asli)
   wajib ikut masuk prosedur K3 lapangan. Perbaikan label dua arah (rak + skill fleet) lewat
   kurasi.
3. **Tabel 4.1/4.2 Uman:** hanya angka yang terbaca sebagai kalimat yang naik (RD-08/RD-09);
   transkripsi tabel utuh menunggu manusia membuka PDF 89-90 (BT-01/BT-02); ukuran mesh bukan
   pengganti analisis bola gelinding (RD-10).
4. **PDF primer belum dibuka manusia:** vonis halaman = vonis LAPISAN TEKS (pypdf read-only);
   detail visual per halaman wewenang manusia; alamat nyata laci di 1.4 (alamat cermin cacat
   D-C4-03); `ekas/` hanya cermin.
5. **Known-defect wajib ikut terangkut:** D-C4-01..D-C4-08 (bukti 6.2) - penandaan lapis rak
   menunggu kartu FIX berizin; sampai terpasang, vonis rilis domain ditahan. Bentuk lama tidak
   dihapus, hanya ditandai.
6. **Usia bahan:** Joffe & Lock edisi ke-2 2023 (3 th - apa adanya); Uman 2008 (18 th - melampaui
   batas pakai apa adanya di rak; statusnya sudah ditandai "18 th" (berglif peringatan) di rantai)
   DAN mengutip IEC
   62305:2006 yang usang (GAP-004) - umur tidak dihitung ulang dari lapis resume; keduanya R3 -
   tak satu pun berwewenang ambang terima.
7. **Adjacency (rujukan silang, tidak disalin; V-15):** domain ELECTRICAL = pemegang ANSI/NETA
   ATS-2017 [R2] Tabel 100.1/100.14 - guard "Jangan tertukar" rantai ini cukup POINTER, isi kartu
   ELECTRICAL tidak diserap; skill fleet `grounding-lightning-design` = kanonik sejalan rantai
   (tabel rujukan identik) - pointer adjacency saja, dengan catatan D-C4-01 menembusnya (perbaikan
   lewat kurasi dua arah, bukan sunting sepihak).
8. **Sumber dan kebaruan ekstraksi:** seluruh angka dari lapisan teks `ekas/` + teks PDF primer
   diekstrak read-only oleh studi t_87ac1a6e (2026-09-30); pengukuran objek ini = cetakan segar
   `lib/c4-l1-evidence/c4l1_measure.py` -> `c4l1_evidence_measure.json` (2026-09-30), bukan
   ingatan; verifier dapat menjalankan ulang `lib/c4-stu-evidence/c4_stu_final.py` - semua klaim
   Bagian 2-3 studi berasal dari outputnya. Deklarasi basis: baris = wc -l (cetakan studi +1);
   byte Uman = cetakan giliran ini (26.856.687 B; drift 1 byte vs metadata handoff hulu
   26.856.688 B dicatat, tidak mempengaruhi klaim apa pun).

STATUS: needs-review
