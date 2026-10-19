---
id: penjelasan-datum-datman-1004
type: catatan
title: Penjelasan pemahaman tertulis sistem DATUM (Tier-1)
status: active
sumber: "docs/2026-10-04-datum-manual/understanding/01-penjelasan.md (hulu: D000/STD001/SPC/RAB + corpus lajur1-2 + measurement M01/M02 terdaftar di seksi 0)"
halaman: 142 ID DAT + 24 ID WB dikutip terverifikasi terhadap register hulu; checker work/f5p7_check.py
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, datum-house-style, pemahaman-tier1, lima-aspek, aparatus-bukti]
links: [docs/2026-10-04-datum-manual/understanding/01-penjelasan.md]
penulis: gsp-data-analyst
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_08c4025e
pin_sha16_artefak: fb02b0c98af9726f
catatan_keputusan: "dipromosikan: DATMANUAL-1004 P23: checker hulu diulang segar PASS; P22 verifier independen SALAH-TARGET=0 33/33; non-sensitif non-dosir"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/penjelasan-datum-datman-1004.md
---

# Penjelasan pemahaman tertulis sistem DATUM (Tier-1)

MISI DATMANUAL-1004 | F5-P7 | Langkah 7 (S-5c, I-1). Role: gsp-data-analyst (lane pekerja).

Dokumen ini berdiri sendiri: pembaca tidak perlu membuka artefak lain untuk memahaminya.
Setiap klaim sitasinya memakai ID aturan (DAT-nn dari register lajur-1, WB-nn dari register
lajur-2) atau path+baris berkas sumber. Semua angka sensus dan status instrumen diambil dari
artefak measurement yang dicetak parser pada giliran hulu masing-masing, bukan dari ingatan.

## 0. Peta sumber dan cara membaca

| Alias | Path | Apa |
|---|---|---|
| D000 | C:/Users/TRIAL/workspace/Datum House Style Standard/DATUM_House_Style_Explained_000-GSP-STD-X-2026_RevA.docx.md | Panduan house style dokumen (1.130 baris lapis teks); sumber 179 aturan DAT-nn |
| STD001 | C:/Users/TRIAL/workspace/Datum House Style Standard/Standar_Workbook_DATUM_001-GSP-STD-X-2026_RevA.docx.md | Standar workbook DATUM (1.105 baris); sumber 68 aturan WB-nn (pemetaan 1:1 ke BK-nn) |
| SPC | C:/Users/TRIAL/workspace/Datum House Style Standard/Proposal_Teknis_Spesimen_UPK-70_000-GSP-PT-X-2026_RevA.docx.md | Spesimen proposal UPK-70 (427 baris); tempat workings nyata terlihat bekerja |
| RAB | C:/Users/TRIAL/workspace/Datum House Style Standard/RAB_Spesimen_UPK-70_000-GSP-RAB-X-2026_RevA.xlsx.md | Spesimen workbook RAB UPK-70 (442 baris, 13 sheet); bukti hidup aturan 001 |
| LAJUR1 | docs/2026-10-04-datum-manual/corpus/lajur1-datum-dokumen.md | Register 179 aturan DAT-nn dengan kolom Aspek, Penegakan, Alasan, Sitasi |
| LAJUR2 | docs/2026-10-04-datum-manual/corpus/lajur2-workbook-dan-nyata.md | Register 68 aturan WB-nn + penilaian dua keluaran nyata (DEMS, KAJ) |
| M01 | docs/2026-10-04-datum-manual/measurement/01-instrumen-penegakan.md | Matriks aturan-ke-instrumen-ke-status; inventaris 92 ID instrumen |
| M02 | docs/2026-10-04-datum-manual/measurement/02-sensus-aturan.md | Sensus angka: 247 aturan per aspek dan per kelas penegakan |

Sitasi `D000:L128` berarti baris 1130-baris lapis teks tersebut; `SPC:L38` serupa untuk
spesimen. Nomor baris SPC/RAB dalam dokumen ini diverifikasi ulang terhadap berkas sumber
pada giliran tulis ini lewat pembacaan langsung dan `sed -n`. Konvensi kutipan: tanda pemisah
U+00B7 dan U+2014 pada teks sumber dinormalisasi menjadi ` / ` di dalam kutipan demi aturan
nol-glyph artefak ini; kata dan angka tidak diubah (preseden LAJUR2:L29 dan LAJUR1:L277).

Kerangka cakupan mengikuti putusan TA D-TA-07 (identification/02_structured.md:L157):
lima aspek tersurat yang disebut permintaan (format, gaya tulis, figur, diagram, chart)
ditambah aparatus bukti tujuh sudut (klasifikasi, penomoran, provenance, register, derivasi,
terbilang, reproduksi) karena bab 5 sampai 8 panduan 000 memang mengatur aparatus sebagai
bagian tak terpisahkan dari house style. Sensus M02 menghitungnya sebagai enam bucket:
format 60, gaya 27, figur 8, diagram 24, chart 14, apparatus 114, jumlah 247 aturan dengan
UNMATCHED nol (M02:L55-L64).

## 1. Doktrin inti: apa DATUM itu dan mengapa ia ada

DATUM adalah lapisan bentuk dan pembuktian di bawah skill konten. Yang menentukan nilainya
adalah empat kalimat doktrin:

1. Segala yang ada di halaman adalah bukti atau aparatus yang membuktikan bukti; tidak ada
   ornamen (DAT-01; D000:L128-L133). Bentuk mengikuti fungsi; ornamen adalah sinyal template
   yang tidak bisa diaudit.
2. Setiap tanda pada halaman harus dapat ditelusuri ke fakta terukur, turunan, pasokan, atau
   asumsi (DAT-02; D000:L133 + D000:L510). Nama "datum" membawa dua makna sekaligus: bidang
   referensi geodesi dan fakta yang given.
3. Bila konten datang tanpa sumber atau tanpa tanda provenans, DATUM tidak mengarang; ia
   menandai celah dan mengembalikan kontennya (DAT-05; D000:L141-L143). Penolakan itulah
   seluruh nilai lapisan ini.
4. Kelas rujukannya tulisan teknik instrument-grade (Jane's, IISS, MIL-STD-961E, lembar data
   Hensoldt dan Rohde & Schwarz, sertifikat kalibrasi), bukan deck konsultan premium
   (DAT-03; D000:L134-L137).

DATUM juga memisahkan tanggung jawab secara tegas: pemanggil memasok konten, angka, sumber,
dan institusi penerima; DATUM memasok halaman, aparatus, klasifikasi, blok register, dan lint
(DAT-04; D000:L139-L143). Keputusan konten visual milik PRISMA/gsp-visual-commander, DATUM
hanya merender spec dan tidak boleh menolak spec sah karena selera maupun mengarang gambar
(DAT-06; D000:L150-L153).

### Argumen nilai: apparatus mahal, ornamen murah

Alasan komersial doktrin ini dibukukan eksplisit di panduan (DAT-03; D000:L134-L137): ornamen
murah dan dimiliki semua pesaing; aparatus mahal karena tidak bisa dibuat tanpa mengerjakan
rekayasanya. Siapa pun bisa meniru pita dan warna; tidak ada yang bisa meniru register
kuantitas, rantai derivasi, dan audit binding tanpa benar-benar menghitungnya. Karena itu
setiap aturan DATUM yang tampak keras (garis 0,18 mm, tint hanya 15/30 persen, satu accent per
figur) sebenarnya membeli satu hal: bentuk yang terbit adalah jejak dari pekerjaan rekayasa
yang nyata, bukan lapisan rias di atas angka yang belum diuji.

Bukti pasar dari dua keluaran nyata fleet (LAJUR2 seksi 5, 48 penilaian tercacah skrip
work/count_predicates.py): DEMS Bareskrim patuh furniture halaman (klasifikasi, kepala/kaki,
cap terbit) tetapi nol tanda provenance per angka (0 ■ ◈ ◇ △, 0 kurung derajat; LAJUR2:L246),
sedangkan Kajian SPPT membawa aparatus lengkap dalam varian label teks (88 [TERUKUR], 539
[DITURUNKAN], 215 blok "Turunan D-", dua jalur hitung dengan selisih < Rp 1; LAJUR2:L246-L250).
Vonis lajur-2: furniture bisa ditiru dan sudah ditiru; aparatus per-angka itulah pembedanya
(LAJUR2:L264, L268).

## 2. Aspek 1: Format (60 aturan; DAT 48 + WB 12, M02:L57)

### 2.1 Tiga tier dan apa yang dilepas

Setiap artefak disortir ke tiga tier: NOTA (Markdown lepas, tanpa cover/register/PDF/lint),
TERBIT (docx/xlsx penuh dengan lint wajib), SERAH (aparatus penuh + lint + PDF + audit halaman
dan angka; tidak ada yang dilepas); NOTA adalah default dan naik tier wajib dijustifikasi
(DAT-13; D000:L181-L192). Uji tier satu kalimat: mampukah kamu menyebut seseorang di luar
divisi yang akan membacanya? Bila tidak, itu NOTA (DAT-14; D000:L194). Alasannya ekonomi:
sebagian besar keluaran dibaca sekali oleh satu-dua orang, dan kemasan penuh memakan satu
siklus build penuh tanpa membeli apa pun (kolom Alasan DAT-13, LAJUR1:L49). Yang boleh dilepas
hanya kemasan; tanda provenans dan entri register tetap wajib bahkan di NOTA (DAT-16;
D000:L194). Artefak yang naik tier naik bersama pada satu gerbang dalam satu pass, supaya
tidak ada paket sebagian naik dan sebagian tertinggal menjadi angka basi (DAT-15; D000:L194).

### 2.2 Dua register: wrapper berdaulat, interior instrumental

Dokumen dibangun sebagai dua register: wrapper (cover, lembar kendali, pembatas, tanda tangan,
sampul belakang) membungkus inti teknis (badan, tabel, figur, derivasi, lampiran); wrapper
mendapatkan ruangan, interior mendapatkan kontrak (DAT-32; D000:L262-L274). Alasannya: meniru
struktur dokumen pertahanan nyata, dan audiens berbeda butuh suara berbeda dalam satu berkas
(LAJUR1:L73). Wrapper memakai kertas cream #FBFAF7 dengan maroon state #6E1420 hanya untuk pita
segel dan klasifikasi (DAT-33; D000:L272-L273); interior near-white #FCFCFB dengan amber
#B45309 hanya bermakna (DAT-34; D000:L300). Sejak Rev J semua keluaran GSP berdasar terang dan
ground gelap hanya atas permintaan eksplisit; kata defence/premium/serious bukan instruksi
gelap (DAT-35; D000:L276-L280), mencegah klise "gelap = serius" yang justru menjadi tanda
template.

Spesimen memperlihatkan pembagian ini: halaman 1 sampai kira-kira L50 SPC adalah wrapper
(klasifikasi L2, blok kontrol nomor/revisi/kustodian L13-L16, entitas+NIB+issue stamp L19,
spine string L20, lembar kendali dengan riwayat revisi, rantai verifikasi V1-V3, distribusi
terkendali, tiga bidang tanda tangan L25-L50), sedangkan Bab 1 ke bawah adalah interior dengan
kontrak tabel dan rail (SPC:L89 dst.).

### 2.3 Grid, tipe, dan garis

Halaman terkunci ke grid A4: margin dalam 24 mm, kolom teks 128 mm, gutter 6 mm, rail bukti
32 mm, margin luar 20 mm; judul, baris tabel, tinggi figur adalah kelipatan utuh baseline
13,5 pt (DAT-46; D000:L346-L363). Elemen full-span mencapai 166 mm dan tidak pernah lebih;
measure badan terjaga 66-80 karakter per baris (DAT-47; D000:L348). Kedua engine menolak lebar
selain 128/166 mm, jadi angka ini bukan anjuran melainkan konsekuensi perangkat (kolom Alasan
DAT-46, LAJUR1:L87). Skala tipe terkunci per elemen sebagai token (chapter 16/20, body 9,5/13,5,
tabel 8,2/11,5, dan seterusnya; DAT-44; D000:L327-L344) karena skala adalah token, bukan
improvisasi. Peran tipe tetap: struktural Plex Sans Condensed, baca Plex Serif, data Plex Mono
untuk setiap numeral, ID, satuan, register, rail; fallback keras berturut-turut Segoe UI
Semibold / Georgia / Consolas / Arial Narrow (DAT-40; D000:L312-L320). Calibri, Times New Roman,
Aptos, Arial sebagai body dilarang karena wajah default Office adalah jejak "siapa pun bisa
ini" (DAT-41; D000:L320 + D000:L901).

Bobot garis baku hierarkis tanpa warna: 0,45 mm ink900 untuk garis atas header dan atas total;
0,25 mm ink400 bawah header; 0,20 mm ink200 separator; 0,50 mm revision bar; lantai fotokopi
semua garis 0,18 mm (DAT-48; D000:L365-L373). Tint hanya 15 dan 30 persen karena dua tint
terang menyatu setelah dua kali fotokopi (DAT-49; D000:L373 + D000:L638). Catatan jujur:
baris DAT-48 dan DAT-52 bertanda [teks-penuh-di-000] karena furniture per halaman tidak tampil
utuh di lapis teks sidecar (metode LAJUR1:L23).

### 2.4 Gramatika tabel dan penamaan

Garis horizontal saja; garis vertikal dan header terisi tidak pernah (DAT-62; D000:L436-L450),
karena vertikal dan fill adalah jejak template yang diblokir lint 07/08. Satuan pada kolom
sendiri di kanan angka (DAT-65; D000:L446) karena tabel data tanpa kolom satuan gagal lint 09.
Zebra hanya di atas 12 baris dan tidak pernah di BoQ cetak (DAT-66; D000:L447): zebra dini
menjadi noise dan bertabrakan dengan struktur group. Baris total ditandai garis kuat di atas,
bukan warna (DAT-67; D000:L448).

Kerja folder adalah bagian dari bentuk: garis bawah dilarang di semua folder, berkas, sheet,
dan identifier (DAT-27; D000:L233-L238) karena nama bergaris-bawah mengumumkan tulisan mesin
untuk mesin; satu-satunya pengecualian sempit adalah modul Python lama yang butuh underscore
untuk import (DAT-29; D000:L249-L251). Pola nama dibuat agar pembaca yang tidak hadir di
ruangan menemukan dokumen dengan membaca rak (kolom Alasan DAT-28; D000:L240-L249). Nama
berkas dibangun dari string caption, tidak pernah sebaliknya, sehingga figur berakhir bernama
benar di berkas dan di dokumen sekaligus (DAT-30; D000:L251). Setiap format keluaran punya
produser of record tunggal (docx=datum_docx.py, chart=datumchart.py, dan seterusnya; DAT-21;
D000:L207-L219) supaya cacat bisa dibiayarkan ke satu tahap. Bila prosa dan tokens.json
bertentangan, token menang (DAT-23; D000:L219): satu sumber kebenaran numerik untuk gaya.

### 2.5 Sisi workbook dari format

Empat lapis arsitektur (masukan, hitung, sajian, kendali+keluaran; WB-01; STD001:L198);
konstanta hanya di MASUKAN dan AHS (WB-02, cek W02); satu lembar HITUNG-ranah per ranah
(WB-03); hitung sekali lalu rujuk, ganda hanya di KENDALI (WB-04); urutan tab = urutan baca
(WB-05); rumus mengalir atas-kiri ke bawah-kanan (WB-06); REGISTER wajib bila angka dikutip
dokumen (WB-07). Blok kepala baris 1-6 sama di semua lembar dan beku di A7 (WB-16, cek W12);
tanpa sel gabungan dan tanpa lembar tersembunyi (WB-17; cek W08/W09; selaras larangan merged
di zona komputasi DAT-154 karena merge merusak rujukan dan sort, D000:L859 + D000:L916);
setiap sheet dicetak sebagai dokumen terkendali A4 fit-to-width dengan footer blok register
(WB-59; DAT-155). Kelas sheet tetap delapan nama dengan peran tersurat (COVER Display,
PETUNJUK Control, KENDALI Control, HITUNG-name Calculation sebagai satu-satunya rumah
konstanta; DAT-149; D000:L836-L847).

Contoh workings di RAB spesimen: 13 sheet dengan urutan persis taksonomi itu (COVER,
PETUNJUK, KENDALI, RINGKASAN, REKAPITULASI, RAB, AHS, MASUKAN, HITUNG-BEBAN, HITUNG-LISTRIK,
HITUNG-BUNYI, HITUNG-TERBILANG, REGISTER; LAJUR2:L219), dan blok kepala yang seragam dengan
bendera induk di baris 4 setiap sheet (dibuktikan di 13 lokasi baris; LAJUR2:L221).

## 3. Aspek 2: Gaya tulis (27 aturan; DAT 22 + WB 5, M02:L58)

### 3.1 Angka dan satuan sebagai gaya

Konvensi numeral Indonesia berlaku bahkan di teks Inggris: titik ribuan, koma desimal, spasi
nilai-satuan (contoh panduan: 6.546,2 m; 0,20 mm); DATUM tidak mendefinisikan varian Inggris
(DAT-09; D000:L160) karena satu sistem numeral untuk semua keluaran dan varian ganda adalah
sumber drift (ditegakkan lint 16). Satuan mengikuti BIPM SI dan NIST SP 811: spasi antara nilai
dan satuan, sudut bidang datar tanpa spasi (30° 22′ 8″), pasangan toleransi dikurung atau
satuan diulang ((63,2 ± 0,1) m), dimensi mengulang satuan (51 mm × 51 mm × 25 mm) (DAT-118;
D000:L623-L634). Setiap ± wajib menyatakan artinya (toleransi rancangan, 1 sigma, k = 2);
± telanjang dilarang dan ketidakpastianlah yang menentukan presisi, bukan nilainya (DAT-119;
D000:L630-L631). Workings spesimen: seluruh Turunan memakai bentuk ini, misalnya "arus saluran
43,47 A" dan "susut relatif 0,86 %" (SPC:L304, L317), dan baris catatan Tabel 2.1 menyatakan
terang "Notasi ± menyatakan toleransi rancangan, bukan ketidakpastian pengukuran" (SPC:L142).

Di workbook, format angka mengikuti register dan desimal koefisien AHS tiga digit (WB-28),
rupiah tanpa desimal dengan nol tampil tanda pisah (WB-27), persen dengan spasi sebelum tanda
(WB-29, cek W14), negatif memakai tanda minus dan tanpa warna (WB-30, cek W05); pemisah
ribuan/desimal diserahkan ke pengaturan wilayah dengan PDF dari profil id-ID (WB-31;
STD001:L407-L421).

### 3.2 Warna yang berbicara dan prosa yang terkalibrasi

Prosa badan selalu ink700, tidak pernah hitam murni; ink900 dicadangkan untuk judul, garis
primer, dan seluruh numeral (DAT-37; D000:L308-L309) karena keterbacaan ukuran kecil adalah
pekerjaan utama (preseden Hensoldt). Maksimal lima nilai warna per halaman dan warna yang tidak
mengkodekan apa pun dihapus (DAT-38; D000:L309, ditegakkan lint 14/25). Setiap token warna
punya tepat satu pekerjaan (DAT-36; D000:L282-L306). Pasangan navy+gold dipensiunkan sebagai
pairing premium paling ter-template yang ada (DAT-39; D000:L309); alasannya jujur dicatat:
dilarang eksplisit tetapi tidak ada lint untuknya, hanya ingatan pemelihara. Kotak cream dengan
bar warna kiri (callout) dilarang sebagai penekanan dan digantikan ruled aside bergaris
(DAT-81; D000:L493-L500) karena callout bar adalah tanda tangan kedua paling dikenali dari
tulisan mesin setelah vertikal tabel.

Kalibrasi prosa adalah bagian gaya, bukan etika penulisan: pernyataan forward-looking memakai
tujuh band ICD 203 dengan rentang persen tersurat (hampir tidak mungkin 1-5 % sampai hampir
pasti 95-99 %; DAT-93; D000:L552-L554) karena kata kemungkinan yang tidak terkalibrasi adalah
hedging; istilah kemungkinan tidak pernah dicampur dengan tingkat keyakinan dalam kalimat yang
sama (DAT-94; D000:L553) karena dua sumbu ketidakpastian yang dicampur mengaburkan mana yang
dijamin. Workings spesimen: satu kalimat model ditampilkan bersama label skalanya, "Kemungkinan
besar (55 % hingga 80 %) beban puncak ... lebih rendah dari nilai rancangan" dengan catatan
penutup "Istilah kemungkinan tidak dicampur dengan tingkat keyakinan" (SPC:L112-L114), dan
tabel skala ICD dicetak ulang di lampiran agar terbaca tanpa dokumen lain (SPC:L417-L427;
aturan induknya DAT-92; D000:L548).

Gaya brief ikut diatur: setiap headline adalah klaim bukan topik, satu gagasan per slide, tidak
lebih dari sekitar 55 kata teks badan (DAT-158; D000:L870 + D000:L873-L879); deck menutup pada
keputusan yang diminta dan empat angka yang membenarkannya, tidak pernah pada "Terima kasih"
(DAT-160); daftar negatif larangan deck (animasi, logo berulang, bullet lebih lima, stok foto,
gradien, shadow, accent kedua) dijaga mata presenter, bukan lint berkas (DAT-162; D000:L881-L883).

## 4. Aspek 3: Figur (8 aturan; DAT 8 + WB 0, M02:L59)

Figur adalah objek visual yang disematkan (gambar, foto, sparkline, peta) dan aturannya kecil
jumlahnya tetapi semuanya menagih aparatus. Setiap tabel dan gambar wajib caption di atas dan
baris SUMBER di bawah, keduanya mandatory (DAT-69; D000:L452-L456): tanpa SUMBER tabel tidak
bisa diaudit (lint 10 untuk tabel, lint 29 untuk gambar). Caption dibuka identifier dalam
condensed kapital lalu satu kalimat isi (DAT-70; D000:L454) agar rujukan silang sebaris mungkin.
Caption foto menempatkan kredit lebih dulu dalam kurung, lalu subjek, tempat, bulan, tahun
(DAT-78; D000:L490) karena atribusi foto adalah legal-first. Sparkline ikut Tufte: lebar 14
letterspace, satu tinta, nilai akhir dicetak di kanan, dan band normal wajib didefinisikan dan
diungkapkan di caption (DAT-79; D000:L490) karena sparkline tanpa definisi band adalah klaim
diam-diam. Peta punya seri nomor sendiri (Peta 1.1) agar tidak menyamar sebagai diagram
ber-spek (DAT-80; D000:L490).

Penempatan figur bukan pekerjaan tangan: figur ditempatkan dengan helper figure(), tidak pernah
manual, karena penempatan manual merusak spasi baris dan memotong gambar ke satu baseline
(DAT-22 + DAT-135; D000:L211-L213, D000:L724). Mode aparatus menjamin figur tidak kehilangan
buktinya saat pindah wadah: figur yang ditempatkan di .docx/.pptx mengatur apparatus ke page
sehingga halaman mencetak caption, sumber, dan baris kunci, dan SVG mencatat kewajiban itu
lewat komentar DATUM-APPARATUS-REQUIRED yang dilaporkan lint 36 (DAT-134; D000:L722-L726).
Satu accent per figur, maksimal lima nilai warna, legenda sebagai baris kunci bukan kotak
(DAT-133; D000:L717, lint 25/26).

Workings spesimen: Gambar 4.1 memiliki caption di atas ("Gambar 4.1 Siklus refrigerasi kompresi
uap unit UPK-70, satu sirkuit dua tahap.", SPC:L248) dan baris SUMBER plus PROVENANS di bawah
("SUMBER Bab 3 dokumen ini / KAK-UPK-2026-01 (fiktif) pasal 4 ... PROVENANS kapasitas
[PEMASOK, keandalan C3] / aliran pasok [DITURUNKAN]", SPC:L250). Pola sama berulang di Gambar
4.2 (SPC:L269 + L272), 4.3 (SPC:L279 + L282), 5.1 (SPC:L288 + L290), 6.1 (SPC:L331 + L333).
Catatan cakupan jujur: figur=0, diagram=0, chart=0 di sisi workbook adalah fakta domain
(standar workbook tidak mengatur objek visual; M02:L140-L142), bukan kekosongan regulasi.

## 5. Aspek 4: Diagram (24 aturan; DAT 24 + WB 0, M02:L60)

### 5.1 Prinsip: gambar adalah klaim, bukan styling

Chart punya sumbu; gambar (drawing) punya node dan konektor dan gagal dengan cara berbeda;
routing diperlakukan rekayasa, bukan styling (DAT-121; D000:L645-L648). Setiap kotak adalah
komponen nyata, setiap garis antarmuka nyata, setiap anotasi kuantitas nyata; garis yang
menembus kotak tak terkait mengklaim koneksi yang tidak ada, dan satu klaim palsu menggugurkan
kepercayaan pada sisanya (DAT-122; D000:L647 + D000:L952). Karena itu kegagalan gambar adalah
kegagalan klaim, bukan estetika (kolom Alasan DAT-121).

Pipeline-nya linear dan manusia hanya menyentuh satu berkas: keputusan PRISMA Gate 0-5, lalu
diagram-spec.json (satu-satunya berkas yang disunting manusia), lalu datum_diagram.py
(geometri, routing, simbol, aparatus), lalu SVG, lalu datum_render.py (PNG 300 dpi untuk
.docx), lalu lint sebagai gerbang rilis (DAT-123; D000:L650-L654). Semua figur digambar engine,
tidak pernah sketsa tangan dan tidak pernah Mermaid untuk kirim, karena Mermaid terbaca
mesin-digambar (radius paksa, palet stok, tepi tanpa label) dan gagal lint 31 (DAT-20 +
DAT-136; D000:L206, D000:L737-L741). Permukaan review dibukukan batasnya: Excalidraw tanpa
ruang milimeter; Figma lossless saat impor tetapi export-nya meng-outline teks sehingga
salinan Figma tidak pernah dimakan ulang, dan datum_figma_audit.py mendif node tree terhadap
spec dua arah (DAT-136).

### 5.2 Bahasa bentuk, garis, dan dialek

Vokabular node dengan makna tetap: box komponen/langkah; stadium mulai-selesai sebagai
satu-satunya bentuk boleh radius (ISO 5807); diamond keputusan dengan setiap keluaran berlabel;
parallelogram IO; cylinder data; hexagon persiapan/gateway; doubled subsistem berstruktur
lanjut (UML); shadowed entitas eksternal di luar boundary (DFD); circle junction; busbar stroke
berat (IEC 60617); satu notasi per gambar (DAT-128; D000:L690-L703) karena bentuk adalah bahasa
(lint 23 memblokir sudut membulat di luar terminator). Keluarga diagram tertutup sembilan nama
dengan tujuh layout engine: layered, topology, stack, flow, swimlane, sequence, sld, rack,
graph (DAT-127; D000:L675-L688) karena di luar tipologi itu tidak ada jalur build. Konektor
membawa makna lewat pola garis lebih dulu dan warna kemudian (data solid ink900; control
putus-putus; sync titik; accent satu jalur; alert putus panjang; verify putus-titik) sehingga
makna bertahan di fotokopi (DAT-129; D000:L705-L714). Engine menerapkan tiga konvensi ruang
kantor teknik yang dilewatkan gambar buatan tangan: anchor mengembang, lompat-silang, detours
rintangan, dan lint 32 memblokir konektor menembus kotak asing (DAT-130; D000:L716-L720). Node
snap ke kisi 10,667 mm x 4,7625 mm dan menjaga satu lebar per tier agar satu tier terbaca
sebagai satu jenis hal (DAT-131; D000:L717). Zona kepercayaan digambar lewat closure outline
putus-putus ber-tab tanpa fill karena batas wilayah klaim harus terlihat tanpa warna (DAT-132;
D000:L717).

Aturan yang paling jujur datang terakhir: jangan pernah mengarang simbol baku; bila set
terregulasi berlaku pakai itu, atau nyatakan terang bahwa blok sederhana dipakai, karena tanda
rekaan yang terlihat resmi lebih buruk dari kotak jujur sebab mengklaim konformansi ke standar
yang tidak dipegang (DAT-137; D000:L743-L746). Pustaka simbol wajib diverifikasi edisi berlakunya
(iec IEC 60617 DB; isa ANSI/ISA-5.1-2022 menggantikan 2009; mil MIL-STD-2525E; lines ISO
128-2:2022 karena edisi 2020 ditarik; desig IEC 81346-1:2022) dengan periksa ulang tahunan
(DAT-138; D000:L748-L757); katalognya 41 simbol dalam empat pustaka (iec 16, isa 13, sec 7,
mil 6; DAT-139; D000:L759-L807). Setiap dialek membawa beda-klaimnya sendiri: empat sakelar IEC
berbagi satu konstruksi dan berbeda hanya oleh tanda, sehingga pemisah yang digambar sebagai
pemutus daya mengklaim pemutusan hubung singkat yang tidak ada (DAT-140); bubble ISA adalah kode
dua-sumbu sehingga menjatuhkan garis lokasi mengubah indikator ruang kendali menjadi instrumen
lapangan secara diam-diam (DAT-141); identitas MIL dibawa bentuk bingkai bukan warna karena
warna hilang di fotokopi (DAT-142). Legenda rumah wajib direproduksi pada lembar yang sama
(lint 34) dan dilarang mengutip IEC 62676 atau EN 50132 sebagai otoritas tanda yang tidak
dipegang (DAT-143; D000:L818-L821). Satu gambar satu dialek (DAT-144; lint 35). Designasi
referensi ikut IEC 81346-1 dengan = fungsi, + lokasi, - produk, : terminal, dan designasi yang
sama muncul di baris BoQ dan uji terima sehingga satu simbol dapat ditelusuri sampai ke harga
dan kriteria lulusnya (DAT-145; D000:L824).

### 5.3 Workings diagram di spesimen UPK-70

Tiga workings terlihat langsung. Pertama, blok jujur: "Gambar 4.1 memakai blok sederhana,
karena DATUM belum memiliki dialek simbol HVAC yang terverifikasi" dengan penutup "Blok jujur
lebih baik daripada simbol rekaan" (SPC:L244-L246), persis penerapan DAT-137. Kedua, legenda
garis sebagai baris kunci, bukan kotak: "KETERANGAN garis penuh data / putus-putus perintah /
putus panjang merah pemutusan proteksi / bingkai berbayang entitas luar lingkup" (SPC:L271;
pola DAT-129/DAT-133; penandaan entitas luar sesuai DAT-128). Ketiga, designasi join-key:
"Gambar 5.1 memakai simbol IEC 60617 dengan penanda IEC 81346. Penanda =UPK+PP-Q1 dibaca:
sistem UPK, lokasi panel gedung PP, komponen Q1. Penanda yang sama dipakai pada daftar
kuantitas dan uji terima" (SPC:L293-L294; penerapan DAT-145). Batas lingkup pun digambar:
pekerjaan milik pemilik di luar kontrak memakai garis putus dua titik ISO 128-2 tipe 05.1
"yang mencegah perdebatan lingkup saat serah terima" (SPC:L118; DAT-146; D000:L824). Field
minimum spec (family, id, title, classification, nodes, edges, legend, sources, labels_verified,
width_mm 128 atau 166 saja) terdaftar di DAT-124 (D000:L656-L669) dengan batas mesin yang
dicatat jujur: engine membaca field source, bukan sources[] (DAT-125; D000:L669).

## 6. Aspek 5: Chart (14 aturan; DAT 5 + WB 9, M02:L61)

Chart adalah SVG dengan teks nyata, bukan raster, karena teks raster tidak bisa dibaca ulang
maupun diaudit (DAT-73; D000:L474-L475 + D000:L909). Gramatika chart ditegakkan oleh engine,
bukan oleh imbauan: satu accent pada seri yang berarti, satu baseline, gridline hanya bila nilai
harus dibandingkan, label langsung menggantikan legenda, label nilai mono tanpa kotak, tanpa
judul di dalam plot (DAT-74; D000:L474-L478); datumchart.py tidak menawarkan opsi terlarang,
sehingga penolakan 3-D, bayangan, gradien, ujung bar membulat, bingkai chart, dan label berkotak
berupa penghapusan capability dari engine, bukan daftar larangan di dokumen gaya (DAT-75;
D000:L475). Tipologi tertutup tiga keluarga: bar untuk peringkat, column untuk deret waktu,
threshold untuk nilai terhadap batas tergambar (DAT-76; D000:L477).

Aturan paling bernilai di aspek ini adalah threshold: batas digambar sebagai garis berlabel dan
bar yang melampauinya memakai tinta alert, sehingga gambar melakukan perbandingan, bukan
pembaca (DAT-77; D000:L480-L482), karena chart teknik paling umum dan paling sering digambar
salah. Workings spesimen, Bab 6.1: "KAK membatasi tingkat tekanan bunyi pada 55,0 dB(A) di
titik 3 m dari unit ... Gambar 6.1 menggambar batas itu sebagai garis, sehingga pembaca tidak
perlu membandingkan angka sendiri. Tahap 2 tanpa selubung melampaui batas, dan batang yang
melampaui batas memakai tinta peringatan" (SPC:L325-L329), dengan caption dan SUMBER/PROVENANS
di L331-L333, plus nilai mentahnya [PEMASOK, keandalan C3] 57,5 dB(A) versus batas 55,0 yang
baru terpenuhi setelah selubung pada 51,5 dB(A) (Turunan D-6.1a, SPC:L336-L341).

Sisi chart workbook (9 aturan WB) adalah kelas derivasi kata kunci M02 (jejak per baris di
work/f5p5_census.py seksi H): format angka dalam chart workbook mengikuti register yang sama
dengan badan dokumen, dan angka chart yang keluar ke dokumen wajib lewat register juga (WB-47;
dokumen mengutip angka workbook melalui datumbind, tidak diketik ulang).

## 7. Aparatus bukti (114 aturan; DAT 72 + WB 42, M02:L62)

Ini jantung sistem: tujuh sudut yang ditetapkan D-TA-07. Pembahasan per sudut dengan alasan
dan workings.

### 7.1 Klasifikasi

Kosakata klasifikasi ditetapkan institusi penerima, bukan oleh GSP; memakai skema salah adalah
cacat kepatuhan yang langsung terlihat oleh reviewer yang tahu regulasinya (DAT-98;
D000:L566-L570). Skema per penerima dibukukan: Kemhan/TNI ikut Permenhan 26/2017 Pasal 3 (tanpa
level Terbatas), Polri/Bareskrim/Densus ikut Perkap 1/2023 Pasal 79, Kementerian/BIN/BNPT ikut
Peraturan ANRI 5/2021 Pasal 104-109 (DAT-99; D000:L572-L578). Kode klasifikasi adalah elemen
pertama nomor dokumen (SR, R, T, B) agar kelas terbaca dari nomor tanpa membuka berkas
(DAT-100; D000:L580). Rahasia dan Sangat Rahasia ditandai tinta merah, Terbatas dan Biasa hitam
(DAT-101; D000:L581) karena warna memikul makna, bukan dekorasi. Kelas muncul dalam kapital di
setiap halaman lewat running head dan register block (DAT-102), halaman satu boleh distempel
dan seterusnya wajib diketik (DAT-103), SR dan R berjalan dalam amplop ganda dengan kontrol
salinan bernomor yang dicatat di sel kanan seal band karena rantai kustodi dimulai dari
kemasan (DAT-104; D000:L584). Lantai hukum tidak bisa ditawar permintaan klien: setiap tata
letak situs, register koordinat, atau peta perimeter instalasi militer adalah minimal Rahasia
apa pun yang diminta (UU 14/2008 Pasal 17; DAT-105; D000:L585). Urgensi adalah sumbu terpisah
yang tidak pernah dikacaukan dengan klasifikasi (DAT-106; D000:L586).

Workings: cover dan setiap halaman spesimen membawa "KLASIFIKASI / BIASA" dan sel salinan
"SALINAN 01 DARI 03 / SPESIMEN, BUKAN PENAWARAN" (SPC:L2, L23), baris entitas "PT GEMILANG
SATRIA PERKASA / NIB 9120208940517 / BIASA" (SPC:L19), dan register block kaki dengan nomor
dokumen 000/GSP/PT/X/2026 (SPC:L13). Label furniture ini bertahan bahasa Indonesia bahkan di
dokumen Inggris karena penanda identitas institusi harus dikenali lintas bahasa (DAT-08;
D000:L159).

### 7.2 Penomoran

Nomor GSP berpola urutan/GSP/kode jenis/bulan Romawi/tahun (005/GSP/KT/VIII/2026) dengan dua
representasi satu nomor: slash di dalam dokumen, hyphen di nama berkas (DAT-109; D000:L601-L605);
bulan Romawi adalah aturan Perkap 1/2023, bukan kebiasaan, dan dasar normatifnya disebut agar
tidak hilang sebagai folklore (DAT-110; D000:L603). Daftar kode jenis DATUM dan daftar ARSIP
berbeda dan gap-nya dicatat terbuka (DS tidak ada di daftar ARSIP, cacat E-21; DAT-111;
D000:L603 + D000:L1017). Nomor 000 adalah placeholder dan nomor nyata wajib dialokasikan dari
Register Induk sebelum salah satu berkas diterbitkan karena identitas dokumen adalah milik
ARSIP, bukan DATUM (DAT-12; D000:L163 + D000:L1086). Pembagian kepemilikan hidup berkas tegas:
ARSIP memiliki identitas, LOKUS memiliki tempat, KRONIK memiliki catatan kejadian + SHA-256;
DATUM tidak menyentuh ketiganya dan hanya menjamin nama yang mereka tempuh patuh (DAT-31;
D000:L252-L257).

Kunci join lintas paket adalah penomoran persyaratan: ID REQ-subsystem-nn diberi sekali dan
berjalan tanpa perubahan dari kajian ke proposal, BoQ, jadwal, dan uji terima (DAT-97;
D000:L558). Workingsnya ada dua lapis. Di proposal: delapan REQ hidup dari register persyaratan
Tabel 2.2 (SPC:L150-L160) sampai matriks ketertelusuran Tabel 8.1 yang menghubungkan setiap
persyaratan ke tempat pembuktian, baris BoQ yang membayarnya, dan uji yang memutuskan lulus
atau gagal, dengan aturan "satu nomor yang tidak memiliki baris pada salah satu kolom adalah
celah yang harus ditutup sebelum dokumen diserahkan" (SPC:L388-L400). Di workbook: kode baris
tetap REQ, K, R, BTS, M, AHS, ASM dengan nomor dua angka (WB-12; STD001:L263-L267) terbukti
tersebar di RAB (REQ-UPK-01..08, K-01..09, R-01..05, BTS-01..05, M-01..04, AHS-01..02,
ASM-UPK-01..03; LAJUR2:L227). Nomor derivasi berpola D-bab.klausa-huruf (DAT-89; D000:L533)
dan penandaan komponen ikut IEC 81346-1 (DAT-145) seperti workings =UPK+PP-Q1 (SPC:L293-L294).

### 7.3 Provenance

Empat tanda provenans dengan makna dan warna tetap: ■ TERUKUR (dibaca dari dokumen/instrumen),
◈ DITURUNKAN (dihitung dari masukan terukur dengan derivasi shown), ◇ PEMASOK (klaim lembar
data vendor belum diverifikasi independen), △ ASUMSI (membawa ID dan pernyataan dampak)
(DAT-82; D000:L502-L510); register menolak entri tanpa tanda (DAT-85; D000:L514) karena pembaca
harus tahu berapa berat tiap angka. Angka beban-rilis tanpa mark adalah cacat, bukan pilihan
gaya (DAT-83; D000:L510, incaran lint 11). Klaim eksternal membawa grade Admiralty dua karakter
(NATO AJP-2.1 / STANAG 2511) dengan keandalan sumber A-F dan kredibilitas informasi 1-6 dinilai
terpisah (DAT-90; D000:L546-L550); angka forum tanpa atribusi adalah [F6] dan tidak masuk
proposal (DAT-91; D000:L548) karena itu ambang masuk korpus dan keputusan manusia, bukan regex.
Kedua tabel skala dicetak sekali di lampiran agar tanda seperti [C3] terbaca tanpa dokumen lain
(DAT-92; D000:L548). Bahkan penulis panduan menandai klaimnya sendiri dengan ■/◈/△ (DAT-10;
D000:L161) supaya inferensi tidak pernah terbaca dengan nada fakta.

Workings spesimen: kolom Asal per baris pada Tabel 2.1 kondisi rancangan (■ untuk nilai KAK, △
untuk ASM-UPK-01; SPC:L127-L141) dengan baris SUMBER+PROVENANS di L142; penandaan per blok
("◈ DITURUNKAN" menggantung di blok keputusan rancangan SPC:L97 dan rincian beban SPC:L178);
klaim pemasok berderajat ("kapasitas per tahap adalah klaim Pemasok A [PEMASOK, C3] yang belum
diuji", SPC:L223); lampiran Admiralty dan ICD tercetak penuh (SPC:L406-L427). Di workbook,
provenance dibawa oleh warna huruf numeral: amber signal konstanta ketik-tangan (periksa dan
tantang), verd rujukan sheet lain (ubah di sumbernya), ink900 rumus pada sheet ini (jangan
pernah timpa), merah alert tautan ke luar workbook (verifikasi ulang) (DAT-150; D000:L849-L856;
WB-24 dengan cek W04 yang menghitung warna dari isi sel, STD001:L407-L421) dan kunci warna itu
dideklarasikan di PETUNJUK karena "konvensi yang tidak bisa dibaca siapa pun bukan konvensi"
(DAT-151; D000:L856; WB-55 bagian A; workings: RAB:L34 "A / Kunci warna angka. Warna menyatakan
asal, bukan hiasan"). Setiap masukan workbook bertanda asal plus derajat Admiralty bila sumber
luar plus kolom Sumber (WB-44; STD001:L621-L625) dengan workings 72 parameter MASUKAN
bermark dan berderajat, misalnya baris ke-72 "Toleransi selisih uji silang ... ■ TERUKUR [A1]"
(RAB:L207-L285, L285).

### 7.4 Register

Sejak Rev I setiap angka beban-rilis adalah referensi bernama ke register kuantitas yang ditulis
rantai perhitungan sebagai langkah terakhir (DAT-84; D000:L512-L516), karena koreksi model cukup
satu re-run build, bukan berburu di semua dokumen yang mengutip angka. Urutan build mengikuti
logika ini: nomor (dari ARSIP) paling dulu, lalu register kuantitas, baru prosa dan gambar,
sehingga setiap label dan kalimat bisa memuat ke register (DAT-25; D000:L221-L226). Dua audit
dijalankan di gerbang serah: audit_docx menolak angka tak terlacak di berkas jadi, dan
audit_retired menolak nilai yang sudah ditarik tapi masih hidup di teks, karena nilai lama yang
tertinggal adalah kegagalan paling mahal (DAT-86; D000:L526-L529). Batas binding yang diketahui
ikut dibukukan: audit memformat ulang nilai ke maksimal 3 desimal sehingga rasio lembap 0,0201
kg/kg dilaporkan nyasar dan harus diizinkan manual (known-defect E-12; DAT-87; D000:L527 +
D000:L1008). Dari sisi workbook: REGISTER wajib bila angkanya dikutip dokumen (WB-07), register
memakai nama, desimal, satuan yang sama dengan register dokumen (WB-46), dan dokumen mengutip
angka workbook melalui datumbind, tidak diketik ulang (WB-47; STD001:L621-L625).

Workings: pernyataan metodologi spesimen menyatakan "Setiap angka penting dalam dokumen ini
dihitung oleh rantai perhitungan dan dirujuk dari register kuantitas, bukan diketik" (SPC:L38)
dan rantai verifikasinya V1 (model/hitungupk.py menghitung seluruh beban, aliran, arus, harga,
PPN), V2 (setiap blok turunan diuji datumbind.Derivation terhadap register), V3 (Register.audit_docx
atas berkas jadi) tercatat di lembar kendali (SPC:L34-L36). Di RAB, sheet REGISTER berisi 41
baris besaran dengan header "Nama besaran / Nilai register / Desimal / Satuan / Asal / Sumber"
(RAB:L402 header, data L403-L443; contoh baris pertama "luas lantai 600 0 m² ■ TERUKUR MASUKAN",
RAB:L403; baris terakhir "total 723248250 0 Rp ◈ DITURUNKAN REKAPITULASI", RAB:L443) dengan
keterangan "Setiap angka yang keluar ke dokumen tercantum di sini dengan nama, satuan dan asal.
Dibaca oleh datumbind" (RAB:L401).

### 7.5 Derivasi

Tier SERAH mewajibkan blok derivasi untuk setiap angka beban-rilis, diuji datumbind.Derivation
dan ditutup dengan apa yang terjadi bila asumsinya gagal (DAT-18; D000:L204): aritmetika dijaga
mesin, kalimat penutup dijaga mata. Bentuk bloknya tetap: aritmetika sebenarnya dalam mono di
kiri garis amber 0,45 mm, tiap input dengan mark-nya, kesimpulan dengan vonis toleransi, dan
kalimat penutup (DAT-88; D000:L531-L535) karena datumbind.Derivation menolak build bila
aritmetika tampil tidak cocok dengan hasil hitung. Tier SERAH menambah rute derivasi kedua yang
independen untuk setiap kuantitas yang mencapai rekapitulasi, dengan kedua rute dan selisihnya
ditampilkan, karena koreksi model ketahuan lebih cepat bila dua rute terpisah (DAT-17;
D000:L203). Padanan workbook-nya: uji KENDALI membandingkan nilai dilaporkan dengan turunan
mandiri yang merujuk sel (WB-51, cek W18) dan angka REGISTER direkonsiliasi rute hitung kedua
bila dikutip dokumen (WB-43; STD001:L621-L625, rekonsiliasi 41 besaran dengan selisih relatif
terbesar 5,6 x 10^-12 terdokumentasi di STD001:L655-L699 lewat LAJUR2:L136).

Workings derivasi adalah bagian terpadat spesimen dan layak dikutip apa adanya sebagai contoh
bentuk. D-3.2a udara luar: rumus V = Rp × Pz + Ra × Az = 3,8 × 60 + 0,6 × 600 menghasilkan
588 L/s; Qs = ρ × V × cp × ΔT × 1.000 = 1,2 × 0,588 × 1,006 × 9,0 × 1.000 = 6.389 W; Ql =
1,2 × 0,588 × 2.501 × 0,0099 × 1.000 = 17.443 W; penutup: "Bila bola basah luar naik 1 K,
beban laten udara luar naik 3.245 W (ASM-UPK-01)" (SPC:L199-L210). D-3.3a kapasitas wajib:
59.632 W + margin 10 % = 65.595 W, setara 18,65 TR, terpasang 70,0 kW, cadangan 6,7 %, vonis
"wajib ≤ terpasang 65,6 kW MEMENUHI", penutup menyatakan konsekuensi: "Bila kapasitas nyata
turun lebih dari 6,7 %, REQ-UPK-01 gagal dan unit tidak diterima pada uji kapasitas"
(SPC:L214-L223). D-5.2a arus: I = 25.175 ÷ (1,732 × 380 × 0,88) = 43,47 A, pemutus minimum
1,25 × I = 54,3 A ≤ 63 A MEMENUHI, plus uji sensitivitas asumsi EER 2,8 (SPC:L298-L307).
D-5.3a susut tegangan 0,86 % ≤ 3 % MEMENUHI dengan keputusan desain yang diekspos: penampang
16 mm² ditentukan oleh kuat hantar arus, bukan oleh susut (SPC:L311-L319). D-7.2a PPN: subtotal
Rp 651.575.000, DPP nilai lain 11/12 × subtotal = Rp 597.277.083,33, PPN 12 % = Rp 71.673.250,
total Rp 723.248.250, tarif efektif 11 %, penutup "Bila ketentuan ini berubah sebelum kontrak,
hanya baris PPN dan total yang berubah" (SPC:L367-L373). Setiap blok menutup dengan vonis
MEMENUHI terhadap batas yang disebut, dan setiap angka tengah membawa mark ◈/◇/■.

### 7.6 Terbilang

Setiap rekapitulasi berharga membawa baris terbilang yang dihasilkan kode dari angka total,
tidak pernah diketik, dan total HPS dibulatkan ke bawah (DAT-115; D000:L613 + D000:L949),
karena terbilang ketik-tangan bisa berbeda dari angkanya; kecocokan tetap dicek mata (butir
daftar manual "terbilang cocok dengan angka di atasnya"; DAT-167; D000:L943-L952). Padanan
workbook: terbilang dari rumus HITUNG-TERBILANG dengan rentang valid 0 <= N < 10^14, tidak
pernah diketik, dijaga cek W17 plus uji K-07 (WB-40; STD001:L518-L526; uji 35/35 sama terhadap
Python terdokumentasi di STD001:L606 lewat LAJUR2:L124). Workings: baris SUMBER Tabel 7.2
menuliskan "Terbilang: tujuh ratus dua puluh tiga juta dua ratus empat puluh delapan ribu dua
ratus lima puluh rupiah. Terbilang dihasilkan kode dari angka total, tidak diketik" (SPC:L382)
dan di RAB sheet HITUNG-TERBILANG menghitung per kelompok lalu merekonstruksi (RAB:L370-L384)
dengan hasil yang sama persis muncul di REKAPITULASI (RAB:L135) yang menunjuk sumbernya
"terbilang total, dibulatkan ke bawah ... HITUNG-TERBILANG" (RAB:L135).

### 7.7 Reproduksi

Semua sistem ini harus bertahan dari perlakuan paling kasar yang menanti dokumen tender:
difotokopi dan discan berulang. Karena itu desain untuk fotokopi adalah aturan tingkat pertama,
bukan tips: tidak ada garis lebih tipis 0,18 mm; tint hanya 15 atau 30 persen; fill diagram
adalah arsiran 45° dan 135°, bukan tint abu; setiap perbedaan warna diulang oleh bentuk, label,
pola garis, atau posisi; dan uji terima bersifat fisik: cetak 100 %, fotokopi dua kali, baca
40 cm, apa pun yang hilang gagal (DAT-120; D000:L636-L640). Ini alasan di balik DAT-48, DAT-49,
pola garis DAT-129, dan identitas bingkai MIL DAT-142. Integritas render lintas mesin dijaga
mekanik: .docx meng-embed font (embed_fonts.py), workbook dan deck tidak bisa embed lintas
platform sehingga mengirim assets/fonts + PASANG-DULU.txt, dan PDF selalu embed+subset sehingga
PDF adalah format tender pilihan (DAT-42; D000:L322-L326). Kebenaran jumlah halaman dijaga field
halaman, bukan ketikan: nomor LEMBAR berasal dari field halaman karena sample terbit menunjukkan
"DARI 6" pada berkas 3 halaman, cacat E-06 (DAT-52; D000:L385 + D000:L430 + D000:L1002).
Perbedaan kemampuan platform diakui, bukan dipaksakan: lead Datum Rule tumbuh mengikuti posisi
halaman di PDF sebagai pengukur progres baca, sementara Word tidak bisa memvariasi gambar header
per halaman sehingga .docx memakai lead tetap (DAT-53; D000:L392).

Enam perangkat tanda signature membuat halaman dikenali dari seberang ruangan tanpa mengorbankan
reproduksi: Datum Rule (hairline 0,20 mm + 12 tick), Evidence rail 32 mm (mark, grade Admiralty,
source, REQ, revision bar), Register block empat sel mono, Seal band maroon 5 mm dengan salinan
bernomor di kanan, Spine string mono 6 pt rotated, Issue stamp // YYYYMMDD LANG CLASS (DAT-50;
D000:L375-L389; konvensi dipinjam dari Saab dan Hensoldt). Rail kosong adalah benar: "rail adalah
janji; janji kosong lebih jujur daripada janji palsu", dan mengisinya agar terlihat sibuk gagal
cek manual rail honesty (DAT-51; D000:L391-L393 + D000:L946). Rel bukti harus benar-benar dipakai
di halaman beban-rilis karena rel yang diisi formalitas tanpa isi menghancurkan maknanya (DAT-19;
D000:L205). Workings di spesimen: seal band dan klasifikasi di L2, spine string "Proposal Teknis,
UPK-70, Bahasa Indonesia, rev. A, Oktober 2026" di L20, issue stamp "// 20261003 ID B / TERBITAN 1"
di L19 (pola DAT-56; D000:L388), register block nomor/revisi/LEMBAR di L13-L15 (pola DAT-52).
Cover mengikuti urutan tetap rata kiri margin 24 mm dan tidak pernah center karena center cover
adalah tata letak template yang diblokir lint 06 (DAT-57; D000:L396-L400; workings urutan
SPC:L7-L20). Logo muncul tepat satu halaman karena logo berulang adalah bahan iklan, bukan bukti
(DAT-58; D000:L397 + D000:L950).

## 8. Bagaimana aturan ditegakkan: mesin, mata, dan yang belum ada

Sensus M02 atas 247 aturan (M02:L70-L77): kelas mesin 115, kelas mata 98, kelas tidak-ada 34.
Instrumentasi terinventaris 92 ID tepat sekali (M01 §4): battery DATUM 38 cek dengan tahap 27
file + 7 build + 4 eye (M01 §2.1; D000 Tabel 8.1 L894-L935), guard situs-panggil G1-G3 + N1
(M01 §2.2), sembilan cek mata manual MAT-01..09 (M01 §2.3), lint workbook datumbuku 23 cek
W01-W23 (M01 §2.4; STD001 Tabel 11.2), gerbang mutu dokumen G-DQ 16 butir (M01 §2.5), dan dua
instrumen kebijakan STD-SAJI-001 dan SPK-002 (M01 §2.6).

Filosofi penegakannya konsisten di seluruh register. Lint menangkap dua hal: apa pun yang membuat
dokumen terbaca tulisan mesin dan cacat kepatuhan yang membuat GSP terlihat tidak paham regulasi;
satu kegagalan pun memblokir rilis, karena tanpa blokir gerbang hanyalah saran (DAT-164;
D000:L888-L890). Tiga puluh delapan pemeriksaan dibagi per tahap sesuai di mana cacat bisa dilihat,
dan sejak Rev J banner hanya melaporkan apa yang benar-benar dijalankan skripnya karena banner
yang melebih cakupan adalah klaim palsu (DAT-165; D000:L888-L895 + D000:L935). Guard ditembakkan
di tempat pemanggilan (datumcheck.py menembak cek 03/04/09/10/16 saat tabel dibuat dengan caption
tabel itu dalam pesan, plus G1 jumlah sel, G2 lebar kolom, G3 teks kepanjangan, N1 garis-bawah)
karena dokumen terukur butuh sekitar 4,9 build sebelum guard ini ada; gerbang pasca-ada terlambat
(DAT-166; D000:L937-L941). Gerbang lint melingkar balik ke sumber (spec, register, atau skrip
build), tidak pernah menambal berkas jadi, karena dokumen ini regeneratif dan tambalan pada output
hilang pada build berikutnya (DAT-26; D000:L223). Perilaku gerbang yang bohong atau crash
dicatat sebagai temuan severity tertinggi: datum_lint.py abort pada berkas Word berisi tabel satu
baris tiga sampai lima kolom (E-01) sehingga gerbang dijalankan pada salinan bertambal, dan tiga
pemeriksaan menyala pada konten yang benar (E-09 pada bentuk sah PPN 12 % x DPP) lalu dibersihkan
dengan parafrasa, bukan ubah substansi (DAT-168; D000:L953-L957 + D000:L992). Putusan program
perbaikan mengikuti logika yang sama: perbaiki engine sebelum menambah aturan, karena yang
membatasi DATUM hari ini adalah perkakas sendiri (DAT-171; D000:L986-L990), argumen terkuat lawan
putusan dibukukan bersama falsifiernya (DAT-172; D000:L992), dan cacat gerbang direproduksi dengan
masukan uji minimal serta ditabulasi, merah-hijau, bukan dipercaya (DAT-174; D000:L1039-L1056).

Sensus juga membukukan tiga celah struktural dengan angka (M02 seksi 3-5). Celah 1, aspek tanpa
aturan: NOL, keenam aspek punya aturan dengan bukti dukungan leksikal per aspek (M02:L123-L142).
Celah 2, aturan tanpa instrumen: 55 aturan DAT (34 berkelas tidak-ada ditambah 21 yang mengklaim
mesin tanpa menyebut satu cek/skrip bernama pun; daftar ID lengkap M02:L151-L165). Celah 3,
instrumen tanpa aturan penunjuk: 28 (10 cek battery DATUM yang tidak dirujuk baris register mana
pun, 16 butir G-DQ seluruhnya, plus 2 kebijakan STD-SAJI-001 dan SPK-002; M02:L191-L209). Arah
celah 3 penting untuk pemahaman: gerbang mutu dokumen seutuh 16 butir berdiri tanpa satu pun
aturan register yang menunjuknya, dan dua instrumen satu-satunya yang berstatus HIDUP bernama
tidak ditunjuk aturan mana pun, sehingga tidak ada baris aturan yang bisa divonis patuh melalui
keduanya (M02:L205-L209).

## 9. Batas-batas jujur sistem ini

Sistem ini kuat sebagai norma tertulis dan lemah sebagai mesin hari ini. Enam batas berikut
wajib ikut terbaca agar penjelasan ini tidak menjadi brosur.

1. Skill pemilik perkakas absan. Skill datum-house-style v1.8 Rev J (pemilik datum_lint.py,
   datumcheck.py, datumbuku.py, engine, tokens.json) tidak ada di registry fleet maupun profil
   pada probe disk 2026-10-05 00:50:45 (0 hit; M01 §5 butir 1). Konsekuensi terukur: 27 cek file
   + 7 cek build + 4 guard + 23 cek W = 61 instrumen berskrip berstatus ABSAN, dan 75 dari 247
   aturan (30,4 persen) bermerek mesin tetapi seluruh instrumennya absan; tidak ada satu pun
   aturan berstatus instrumen HIDUP penuh (M02:L119-L121). Hari ini seluruh battery itu adalah
   norma tertulis yang sangat rapi, bukan gerbang yang berjalan.
2. datumbind.py hanya HIDUP-PARSIAL: dua salinan di legacy-archive, 260 baris, fungsi
   Register/Derivation/audit_docx/audit_retired terbukti di file, tetapi berada di arsip, bukan
   di jalur rilis kanonis (M01 §5 butir 2). Klaim spesimen bahwa V2/V3 dijalankan (SPC:L35-L36)
   hanya bisa berarti dijalankan di mesin skill yang kini absan (M01 §5 butir 8).
3. G-DQ baru dieksekusi 3 dari 16 butir (G-DQ-4/11/12 via CHECK 9 verif_datum_ver04.py; M01 §5
   butir 3); belum ada gerbang rilis otomatis 16 butir, dan sebagaimana celah 3, ke-16-nya tidak
   ditunjuk aturan register mana pun.
4. Lapis teks punya batas bukti. Furniture per halaman (running head, register block kaki, seal
   band visual, zebra) tidak tampil utuh di sidecar, sehingga baris DAT-48, DAT-52, DAT-60,
   DAT-61, DAT-101, DAT-120 disitasi ke uraian normatif D000 dengan tanda [teks-penuh-di-000]
   (metode LAJUR1:L23); warna huruf dan ketebalan garis pada RAB/DEMS/KAJ tidak bisa divonis
   dari teks. Enam penilaian keluaran nyata berpredikat TAK-TERKONFIRMASI karena alasan yang sama
   (LAJUR2 seksi 5.1).
5. Spesimen adalah latihan bentuk, bukan pekerjaan nyata: klien, KAK, pemasok, dan harga rekaan;
   fisika, uji aritmetika, dan bentuknya nyata (DAT-11; D000:L162; pernyataan diri di SPC:L11,
   L93). Mark provenans di spesimen merujuk ke sumber rekaan dengan aturan yang sama seperti
   dokumen nyata. Nomor 000/001/NNN masih placeholder sampai Register Induk mengalokasikan
   (DAT-12; LAJUR2:L272).
6. Ada deviasi yang diketahui antara klaim dan implementasi: 32 temuan audit E-01..E-32 terdaftar
   dengan bukti dan perbaikan (DAT-173; D000:L993-L1029), termasuk glyph ■ ◈ ◇ △ yang muncul dalam
   face simbol mesin pembaca sehingga bobotnya tidak stabil (E-32; D000:L1080-L1086 lewat
   DAT-176), enam id simbol masih bergaris-bawah melawan §14 (E-11; DAT-139), dan kedua dokumen
   panduan sendiri belum bernomor sah (DAT-176; D000:L1086). Residual risk lain dibukukan jujur:
   seluruh render memakai LibreOffice dan Word bisa paginate berbeda; Excel desktop tidak tersedia
   saat pengujian 001 (STD001 via LAJUR2:L47).

Selain itu satu catatan metode untuk angka sensus di dokumen ini: aspek WB (dan karena itu
pemisahan chart 9 / format 12 / apparatus 42 di sisi workbook) adalah derivasi kata kunci
berprioritas karena register lajur-2 tidak menyediakan kolom Aspek; tiap asignasi dapat dibantah
lewat tabel jejak per baris di keluaran work/f5p5_census.py seksi H, dan perubahan kosakata wajib
dicetak ulang (M02:L255-L257). Angka-angka M02 adalah cetakan alat pada giliran 2026-10-05
00:56:09 dengan VERDICT PASS 14/14 (M02:L217-L236), bukan hitungan tangan.

## 10. Ringkasan satu paragraf

DATUM adalah sistem di mana bentuk halaman adalah konsekuensi dari kewajiban bukti: grid dan
tipografi (format) memastikan setiap numeral duduk sejajar dan terbaca di fotokopi; kalibrasi
prosa (gaya tulis) memastikan "mungkin" berarti 55-80 persen dan ± berarti sesuatu; caption dan
SUMBER (figur) memastikan setiap gambar bisa ditelusuri; engine dan dialek simbol (diagram)
memastikan setiap garis mengklaim antarmuka yang nyata; tipologi tertutup (chart) memastikan
perbandingan dilakukan gambar, bukan pembaca; dan tujuh sudut aparatus (klasifikasi, penomoran,
provenance, register, derivasi, terbilang, reproduksi) memastikan tidak ada satu pun angka yang
mencapai halaman tanpa diketahui dari mana ia datang, bagaimana ia dihitung, apa yang terjadi
bila asumsinya salah, dan bagaimana bukti itu bertahan difotokopi dua kali. Nilainya terletak
pada aparatus yang tidak bisa dibeli dengan template (DAT-03), dan batas jujurnya hari ini adalah
aparatus penegaknya sendiri sebagian besar absan dari disk (M01 §5, M02 §2.4): standarnya hidup,
mesinnya mayoritas menunggu dipulihkan.

## 11. Verifikasi (cetakan alat, bukan klaim)

Gerbang deterministik dijalankan pada giliran tulis ini lewat skrip
`work/f5p7_check.py` (jejak stdout: `work/f5p7_run.txt`): keberadaan berkas, cakupan enam seksi
aspek/aparatus + tujuh sudut D-TA-07, kehadiran ID DAT/WB yang dikutip di register hulu,
nomor baris SPC/RAB yang dikutip berada dalam batas berkas dan cocok token kunci, densitas
sitasi baris-isian, dan tipografi U+2014 = 0 / U+00B7 = 0. Hasil per CHECK dan VERDICT akhir
dicetak skrip dan direkap di komentar kartu penutup.

STATUS: complete. Artefak: docs/2026-10-04-datum-manual/understanding/01-penjelasan.md (berkas
ini). Konsumsi hilir: langkah 15-16 (manual/01-arsitektur.md, manual/bagian-1.md) memakai
narasi ini sebagai bahan Tier-1 Bagian I; angka sensus tetap diukur ulang dari M02, bukan dari
salinan prosa di sini.
