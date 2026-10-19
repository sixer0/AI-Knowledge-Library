---
id: registri-diagram-datman-1004
type: catatan
title: "REGISTRI POLA DIAGRAM (DIA-nn): grammar bentuk, konektor, apparatus, contoh-pakai"
status: active
sumber: "docs/2026-10-04-datum-manual/library/registri-pola-diagram.md (hulu: corpus/lajur1-datum-dokumen.md DAT-121..146, research/02-tipologi-chart-diagram.md, research/03-sintesis-dan-keputusan.md, identification/02_structured.md KD-24)"
halaman: 21 pola DIA-01..DIA-21; grammar KD-24 lapis-2; verifikasi work/f7p13_check.py
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, diagram, registri-pola, kd-24, sembilan-keluarga, known-defect-n1-n9]
links: [docs/2026-10-04-datum-manual/library/registri-pola-diagram.md]
penulis: gsp-document-writer
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_08c4025e
pin_sha16_artefak: 4457fb3509b975c2
catatan_keputusan: "dipromosikan: DATMANUAL-1004 P23: checker hulu diulang segar PASS; P22 verifier independen SALAH-TARGET=0 33/33; non-sensitif non-dosir"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/registri-diagram-datman-1004.md
---

# REGISTRI POLA DIAGRAM (DIA-nn): grammar bentuk, konektor, apparatus, contoh-pakai

- Misi: DATMANUAL-1004 | Kartu: t_6a28789b | Pekerja: gsp-document-writer
- Langkah 13 blueprint (fase konstruksi-pustaka). Konsumsi hiliran: langkah 14
  (library/INDEKS.md), langkah 15 (arsitektur manual), Bagian II manual
  (langkah 17), verifier F4/F6.
- Tanggal: 2026-10-05. Cacah dalam berkas ini dicetak alat `work/f7p13_check.py`
  pada giliran ini (jejak di `work/f7p13_check_out.txt`), bukan ingatan.
- Sumber (readonly, tidak diubah lajur ini):
  - R-1 = `corpus/lajur1-datum-dokumen.md` - register DAT-121..DAT-146: kontrak
    spec gambar, 9 keluarga, 10 bentuk node, 6 konektor, routing, trust zone,
    satu aksen, aparatus, permukaan review, pustaka simbol, designasi, tipe garis.
  - R-2 = `research/02-tipologi-chart-diagram.md` - katalog eksternal DIA-01..
    DIA-20 dengan kasus, anti-kasus, aturan baca, dan sitasi ber-ladder; aturan
    baca lintas tipologi AB-01..AB-10; register known-defect N-1..N-9.
  - R-3 = `research/03-sintesis-dan-keputusan.md` - cabang B pohon pembaca
    (daun B.1..B.9), apparatus wajib AP-1..AP-10, gerbang SPK-002.
  - R-4 = `identification/02_structured.md` - KONTRAK-DESAIN KD-09 (lebar figur
    128/166 saja), KD-13 (tata bahasa tabel), KD-20 (matriks ketertelusuran),
    KD-24 (grammar normatif diagram); keputusan D-TA-11 (skema ID tunggal).
  - R-5 = `library/pohon-pemilihan-chart.md` - kartu 12; Gerbang-Akar cabang
    STRUKTUR/ALUR/JADWAL/KETERTELUSURAN dirutekan ke registri ini.
  - R-6 = `contract.md` - putusan controller D-09 (edisi ISA/ISO), D-10 (register
    riset terbuka, blokir kutipan), D-11 (adopsi RTM sebagai perluasan DIA).
- Skema sitasi pustaka (D-TA-02): `DATMAN/LIB/registri-pola-diagram#<ID>` dengan
  ID = DIA-nn atau butir KD/DAT yang dirujuk.

## 1. Cara memakai registri ini

Registri ini menjawab pertanyaan pembaca cabang-B pada pohon keputusan riset:
"diagram apa yang benar untuk struktur, alur, jadwal, koneksi, atau
ketertelusuran saya, dan grammar apa yang wajib melekat padanya?" Pemakaiannya
bertingkat dua lapis, mengikuti cara kartu 12 menata cabangnya sendiri supaya
dua registri saudara dapat dibaca dengan satu kebiasaan. Lapis pertama adalah
grammar normatif pada bagian 2 yang berlaku untuk semua pola tanpa kecuali;
satu pun pelanggarannya membuat gambar cacat walau polanya benar, karena
grammar inilah isi kontrak KD-24 yang dinormakan dari R-1. Lapis kedua adalah
katalog pola pada bagian 4 yang dipilih lewat daun B.1..B.9 pohon pembaca
(R-3 bagian 2) atau tabel keluarga pada bagian 3.

Setelah pola terpilih, keempat field beban-pakai pada entri wajib dibaca semua:
bentuk node, konektor, apparatus, dan contoh-pakai. Nol pola boleh dipakai tanpa
anti-kasus dan contoh-pakai terbaca, mengikuti syarat simpul AP-10 yang sama
dengan kartu 12. Bila tidak ada pola yang cocok, dilarang mengarang diagram di
luar tipologi terdaftar tanpa mencatat GAP-nn; jalur fallbacknya sama dengan
pohon chart (R-5 bagian 7). Waterfall biaya tidak mendapat nomor DIA baru karena
sudah dimiliki lajur chart sebagai CH-16, dan penanganannya dibukukan di
bagian 5 bersama rekonsiliasi RTM serta temuan cacat hulu.

## 2. Lapis grammar normatif (berlaku untuk semua pola; butir KD-24)

### 2.1 Kewajiban kebenaran dan jalur produksi

Setiap kotak adalah komponen nyata, setiap garis adalah antarmuka nyata, setiap
anotasi adalah kuantitas nyata; garis yang menembus kotak tak terkait mengklaim
koneksi yang tidak ada, dan satu klaim palsu menggugurkan kepercayaan pada
seluruh gambar (DAT-122). Chart punya sumbu; gambar punya node dan konektor dan
gagal dengan cara berbeda: kegagalan gambar adalah kegagalan klaim, bukan
estetika (DAT-121). Jalur produksinya adalah Gate PRISMA, lalu
`diagram-spec.json` sebagai satu-satunya berkas yang disunting manusia, lalu
engine geometri, lalu SVG, lalu raster 300 dpi untuk .docx, lalu lint sebagai
gerbang rilis (DAT-123). Field minimum spec memuat family, id dan title
bernomor prefiks bab, classification, nodes[], edges[] dengan empat field wajib
(from, to, kind, label), legend[], notes[], dan sources[] minimal satu dokumen
plus pasal; `labels_verified` false berarti draft dan dilarang kirim (DAT-124).
Batas mesin yang diketahui ikut dibukukan: engine membaca field `source`, bukan
`sources[]` (DAT-125). Setiap string yang dibaca sebagai fakta adalah klaim atas
nama GSP, sehingga label numerik dibangkitkan dari register kuantitas dan gambar
tidak bisa berbeda dari derivasinya (DAT-126; AP-2).

### 2.2 Vokabular bentuk node (sepuluh bentuk, makna tetap)

Bentuk adalah bahasa, dan satu gambar hanya memakai satu notasi (DAT-128).
Engine hanya menawarkan sepuluh bentuk berikut, dan tidak ada bentuk keenam
belas yang boleh muncul dari tangan penulis spec. Pemaknaan tetapnya menjadi
bahan audit pembaca gambar, sebab lint 23 menjaga bentuk terminator dan lint
lainnya menjaga kekhususan busbar:

| # | Bentuk | Makna tetap | Catatan normatif |
|---|--------|-------------|------------------|
| 1 | box | komponen atau langkah | bentuk netral default |
| 2 | stadium | mulai-selesai (terminator) | satu-satunya bentuk boleh radius (ISO 5807); lint 23 memblokir sudut membulat di luar terminator |
| 3 | diamond | keputusan | SETIAP keluaran wajib berlabel |
| 4 | parallelogram | masukan/keluaran data | - |
| 5 | cylinder | data tersimpan | - |
| 6 | hexagon | persiapan atau gateway | - |
| 7 | doubled | subsistem berstruktur lanjut | dialek UML |
| 8 | shadowed | entitas eksternal di luar boundary | dialek DFD |
| 9 | circle | junction atau off-page | - |
| 10 | busbar (stroke berat) | rel daya/sinyal | IEC 60617 |

### 2.3 Vokabular konektor (enam jenis; pola garis dulu, warna kemudian)

Jenis konektor membawa makna lewat pola garis lebih dulu dan warna kemudian,
sehingga makna bertahan di fotokopi hitam-putih (DAT-129; AB-10; uji fisik
reproduksi KD-23). Warna sendiri tidak pernah boleh menjadi satu-satunya
pembeda dua hubungan, karena fotokopi dan buta warna sama-sama menghapusnya.
Tabel berikut mendaftar enam jenis yang ditawarkan engine, beserta padanan tipe
garis ISO 128-2 yang relevan:

| # | Jenis | Pola dan warna | Makna | Tipe garis ISO 128-2 |
|---|-------|----------------|-------|----------------------|
| 1 | data | solid ink900, kepala solid | aliran utama data/daya/material | 01.1 kontinu sempit |
| 2 | control | putus-putus ink700, kepala terbuka | jalur kendali atau pengecualian | 02.1 putus-putus |
| 3 | sync | titik ink400 | sinkronisasi lemah | - |
| 4 | accent | solid signal tebal | satu jalur pesan yang tidak boleh dilewat pembaca; maksimal satu per figur | - |
| 5 | alert | putus panjang warna alert | gagal, penolakan, pengecualian | - |
| 6 | verify | putus-titik verd | uji integritas, atestasi, audit | 04.1 putus-titik-panjang |

Tipe garis tambahan untuk soal lingkup kerja ikut dibukukan di sini: 01.2
kontinu lebar dan 05.1 putus-panjang-dua-titik untuk pekerjaan di luar kontrak.
Yang terakhir itu mencegah perdebatan lingkup saat serah terima, karena mata
langsung melihat mana yang dijanjikan dan mana yang tidak (DAT-146). Kedua tipe
tambahan ini tersedia di engine sehingga penulis spec tinggal memilih, bukan
menggambar diam-diam.

### 2.4 Konvensi routing (tiga konvensi ruang kantor-teknik)

Engine menerapkan tiga konvensi yang biasa dilewatkan gambar buatan tangan,
sehingga penulis spec tidak perlu dan tidak boleh mengulanginya secara manual
(DAT-130). Pertama, anchor mengembang atau fanned anchors: garis keluar satu
kotak pada titik berbeda, bukan menumpuk di satu anchor, sebab dua panah ke satu
anchor terbaca sebagai panah dua-kepala yang tidak pernah digambar (DAT-122).
Kedua, lompat-silang atau crossing hops: run horizontal melompati run vertikal
dengan busur kecil sehingga persilangan tidak ambigu. Ketiga, detours rintangan
atau obstacle detours: rute mengelilingi kotak tak terkait, dan lint 32
memblokir konektor yang menembus kotak asing. Node snap ke kisi 10,667 mm x
4,7625 mm dan menjaga satu lebar per tier sehingga satu tier terbaca sebagai
satu jenis hal (DAT-131).

### 2.5 Zona kepercayaan (trust zone)

Wilayah klaim digambar lewat closure berupa outline putus-putus dengan tab
label, tanpa fill (DAT-132). Batas wilayah klaim harus terlihat tanpa warna,
sebab warna hilang di fotokopi sementara batas tanggung jawab tidak boleh ikut
hilang. Contoh pemakaiannya adalah zona DMZ pada topologi, boundary sistem pada
DFD, dan enclosure loop kontrol pada P&ID; ketiganya memakai konstruksi closure
yang sama agar pembaca belajar satu kebiasaan sekali saja.

### 2.6 Satu aksen dan anggaran warna

Satu accent per figur, dan maksimal lima nilai warna dalam satu figur
(DAT-133; lint 25 per berkas dan lint 26 per build). Legenda adalah baris kunci,
bukan kotak mengelilingi objek. Aturan ini selaras dengan AP-6 yang melarang
gradient, shadow, dan 3-D, karena dekorasi semacam itu mencuri peran yang
seharusnya dipegang struktur gambar.

### 2.7 Apparatus: mode page versus mode figure

Mode aparatus ditentukan oleh permukaan tempat figur hidup (DAT-134). Figur
yang ditempatkan di .docx/.pptx mengatur apparatus ke PAGE sehingga halamanlah
yang mencetak caption, sumber, dan baris kunci, sementara SVG mencatat kewajiban
itu lewat komentar DATUM-APPARATUS-REQUIRED yang dilaporkan lint 36; SVG berdiri
mengatur FIGURE dan membawa aparatusnya sendiri. Apparatus wajib lintas cabang
menempel utuh (R-3 bagian 3): AP-1 caption bernomor di atas figur dengan tanggal
berlaku di judul dan SUMBER di bawah; AP-2 mark provenans berupa label teks;
AP-3 satuan label sumbu ikut ISO 80000-1; AP-6 satu aksen jenuh; AP-7 pola garis
dulu dan tautan dilabeli; AP-9 teks nyata dalam gambar. Untuk Word, SVG dirender
300 dpi pada lebar yang dideklarasikan dan ditempatkan dengan helper yang
melepaskan spasi baris eksak 13,5 pt, yang tanpa itu gambar terpotong ke satu
baseline (DAT-135).

### 2.8 Lebar figur: 128 atau 166 mm saja

Lebar figur hanya 128 mm atau 166 mm, tidak pernah nilai antara; kedua engine
menolak nilai di luar pasangan itu (DAT-124; KD-09; AP-9). Dua angka ini bukan
selera, melainkan konsekuensi grid halaman dan lattice yang sama sejak sumber
desain, sehingga figur selalu duduk rapi pada kolom dokumen. Panduan pemilihan
per pola tercatat pada tiap entri katalog di field Lebar.

### 2.9 Permukaan review yang dilarang jadi keluaran

Mermaid boleh dipakai untuk berpikir, tidak pernah untuk kirim, karena radius
paksa, palet stok, tepi tanpa label, dan tanpa grid terbaca mesin; sumber
Mermaid dalam deliverable gagal lint 31 (DAT-136; AP-9). Excalidraw menjaga
grammar tapi tanpa ruang milimeter, sehingga sah hanya untuk drafting. Figma
mengimpor SVG DATUM lossless sebagai vektor teredit dengan teks nyata pada
96 dpi (166 mm setara 627,4 px dan bolak-balik bersih), tetapi export-nya
meng-outline setiap node teks sehingga salinan Figma adalah artefak review yang
tidak pernah dimakan ulang; audit dua arah terhadap spec dilakukan dengan
datum_figma_audit.py (DAT-136).

### 2.10 Satu dialek simbol dan pustaka simbol ber-edisi

Satu gambar membawa satu dialek simbol saja, dan lint 35 memblokir campur
dialek (DAT-144). Jangan pernah mengarang simbol baku: bila set terregulasi
berlaku maka pakai itu, atau nyatakan terang bahwa blok sederhana dipakai,
karena tanda rekaan yang terlihat resmi mengklaim konformansi ke standar yang
tidak dipegang (DAT-137). Gambar bertanda pustaka rumah (sec:) wajib
mereproduksi legenda pada lembar yang sama lewat lint 34, dan tidak pernah
mengutip IEC 62676 atau EN 50132 sebagai otoritas tanda (DAT-143). Edisi pustaka
yang berlaku dikutip mengikuti putusan controller D-09 yang menegakkan truth di
atas fidelity: ANSI/ISA-5.1-2024 dan ISO 128-2:2020 E1; baseline 000 menyebut
ISA-5.1-2022 dan ISO 128-2:2022 lalu dikoreksi sebagai temuan audit tanpa
mengubah anatomi kontrak (R-6 D-09; bandingkan DAT-138). MIL-STD-2525E tetap
ber-flag BASELINE-ONLY dan dilarang naik sebagai klaim eksternal terverifikasi
(R-6 D-09). Katalog glif per simbol ada di `library/katalog-simbol.md` (SIM-nn,
kartu 11).

### 2.11 Designasi referensi sebagai kunci telus

Designasi referensi ikut IEC 81346-1: tanda sama untuk fungsi, tanda plus untuk
lokasi, tanda minus untuk produk, dan titik dua untuk terminal. Contoh
`=UPK+PP-Q1` berarti sistem UPK, lokasi panel PP, komponen Q1 pemutus feeder.
Designasi yang sama muncul di baris BoQ dan uji terima sehingga satu simbol
dapat ditelusuri ke harga dan kriteria lulusnya (DAT-145); kunci gabung inilah
yang dipakai pula oleh matriks ketertelusuran DIA-21.

## 3. Sembilan keluarga DATUM dan kapan menggambar (DAT-127)

Sembilan nama keluarga dengan tujuh layout engine membentuk tipologi tertutup
(DAT-127). Tabel berikut adalah indeks balik dari katalog bagian 4, sehingga
pembaca yang berangkat dari keluarga engine dapat langsung menemukan polanya.
Arah baca tabel ini satu arah saja: dari keluarga ke pola, bukan sebaliknya,
karena pemilihan pola tetap lewat daun pohon pembaca pada R-3.

| Keluarga | Kapan menggambar | Pola DIA yang dirutekan | Mesin layout |
|----------|------------------|--------------------------|--------------|
| layered | strata, tier, zona | DIA-11, DIA-18 | ya |
| topology | perangkat jaringan dan tautan; setiap tautan dilabeli | DIA-03, DIA-09 | ya |
| stack | daftar berlapis tanpa layout/sample sendiri | DIA-04 | ya |
| flow | prosedur berurutan dengan gerbang keputusan | DIA-01, DIA-02, DIA-08, DIA-15 | ya |
| swimlane | siapa yang beraksi adalah poinnya | DIA-02 | ya |
| sequence | urutan pesan atas waktu | DIA-05 | ya |
| sld | rantai daya/sinyal pada busbar | DIA-14 | ya |
| rack | elevasi rak, posisi U beban-rilis | DIA-13 | ya |
| graph | selain itu, ditempatkan per col/row | DIA-06, DIA-07, DIA-12, DIA-16, DIA-17, DIA-19, DIA-21 | per col/row |

Catatan pemetaan perlu dibaca sebelum tabel dipakai sebagai acuan nomor. DIA-02
terdaftar di dua keluarga (flow dan swimlane) karena memang irisan keduanya.
DIA-05, DIA-10, dan DIA-20 adalah pola lintas keluarga yang tetap punya satu
nomor kanonis, sebab D-TA-11 melarang ganda nomor.

## 4. Katalog pola DIA-01 .. DIA-21

Format tiap entri adalah tabel dua kolom berisi sepuluh field. Empat field
sebelum Sitasi merupakan beban-rilis verifikasi kartu 13, yaitu nol pola tanpa
contoh-pakai, dan keempatnya diuji checker deterministik bagian 7. Nomor,
definisi, kasus, anti-kasus, dan sitasi diwarisi dari R-2 §4 dengan koreksi
rujukan silang yang bergeser (lihat bagian 5.3); grammar bentuk, konektor,
routing, dan apparatus dinormakan dari R-1 sesuai lapis bagian 2.

### DIA-01 Flowchart proses (ISO 5807 / ANSI)

| Field | Isi |
|---|---|
| Keluarga DATUM | flow (DAT-127) |
| Bentuk node + makna | stadium mulai-selesai; box langkah proses; diamond keputusan dengan setiap keluaran berlabel; parallelogram masukan/keluaran (DAT-128) |
| Konektor + pola/warna | data solid ink900 kepala solid untuk alur utama; control putus-putus ink700 untuk jalur pengecualian; label ya/tidak pada cabang; pola garis dulu warna kemudian (DAT-129; AB-10) |
| Routing | arah alur utama kiri-ke-kanan atau atas-ke-bawah; fanned anchors pada diamond bercabang banyak; detour mengelilingi kotak tak terkait (DAT-130) |
| Trust zone | opsional; sub-alur yang dipindah ke halaman lain ditandai circle off-page (DAT-128) |
| Apparatus | mode page di .docx dengan caption atas bernomor prefiks bab, tanggal dalam judul, SUMBER bawah (DAT-134, AP-1); SVG mandiri mode figure dengan komentar DATUM-APPARATUS-REQUIRED |
| Lebar | 128 mm default; naik ke 166 mm bila node lebih dari sekitar 10 atau ada sub-alur paralel (DAT-124; pecah sub-alur bila lebih dari sekitar 25 node) |
| ANTI-kasus | tanggung jawab aktor tidak jelas di sini (pakai DIA-02 swimlane); interaksi pesan antar sistem (pakai DIA-05 sequence); lebih dari sekitar 25 node satu halaman (pecah sub-alur) (R-2 §DIA-01, rujukan dikoreksi 5.3) |
| Contoh-pakai dokumen GSP | prosedur commissioning UPS pada Kajian Teknis UPK (langkah terima, ujicoba, beban purna); alur eskalasi insiden pada SOP pemeliharaan VSS; langkah serah terima dokumen pada bab manajemen proyek proposal teknis |
| Sitasi | R-2 §DIA-01 (rung W2_flow, Z3_flow, WS_5807, Z3_5807 mirror BSI doi.org/10.3403/00099818u); R-1 DAT-127, DAT-128, DAT-129 |

### DIA-02 Cross-functional flowchart / swimlane

| Field | Isi |
|---|---|
| Keluarga DATUM | swimlane, juga irisan flow (DAT-127) |
| Bentuk node + makna | sama dengan DIA-01 di dalam lajur; judul lajur adalah peran, bukan nama orang (R-2 §DIA-02) |
| Konektor + pola/warna | data solid untuk alur; garis handover antar-lajur wajib bersilang tegas tanpa ambiguitas; accent hanya bila satu jalur handover adalah pesan utama (DAT-129, DAT-133) |
| Routing | lompat-silang wajib pada persilangan lajur (crossing hops, DAT-130); lajur snap ke kisi lebar DAT-131 |
| Trust zone | garis lajur itu sendiri adalah partisi; trust zone tambahan hanya untuk pihak eksternal klien (outline putus-putus berlabel, DAT-132) |
| Apparatus | mode page; legenda peran ditulis di kepala lajur sehingga baris kunci tidak berulang di kaki; SUMBER bawah tetap (DAT-134, AP-1) |
| Lebar | 166 mm wajib bila lajur lima atau lebih; lebih dari sekitar 6 lajur pada 128 mm adalah anti-kasus eksplisit (R-2 §DIA-02; DAT-124) |
| ANTI-kasus | satu aktor saja (lajur jadi dekorasi); lebih dari sekitar 6 lajur pada lebar 128 mm (R-2 §DIA-02) |
| Contoh-pakai dokumen GSP | prosedur handover GSP, klien, dan vendor pada pengiriman proyek DEMS; alur persetujuan revisi gambar as-built sebelum masuk lampiran kajian; rantai tanda tangan LEMBAR KENDALI saat divisualkan untuk audiens klien |
| Sitasi | R-2 §DIA-02 (rung Z2_swim_alt; BPMN pool/lane varian formal via rung WS_19510, OM2); R-1 DAT-127 |

### DIA-03 Diagram topologi jaringan

| Field | Isi |
|---|---|
| Keluarga DATUM | topology (DAT-127) |
| Bentuk node + makna | box perangkat; circle junction titik agregasi; ikon vendor hanyalah kelas perangkat dan bentuk tidak bermakna sendiri (R-2 §DIA-03; ikon menjadi kelas SIM dari lajur 8) |
| Konektor + pola/warna | data solid untuk tautan dengan label media, kecepatan, dan ID pada SETIAP tautan (WAJIB, DAT-127); accent satu jalur tulang punggung; control putus-putus untuk tautan cadangan atau logis (DAT-129) |
| Routing | fanned anchors pada perangkat multi-uplink; persilangan dioptimalkan dengan lompat-silang, bukan diacak (DAT-130) |
| Trust zone | segmentasi VLAN dan batas situs digambar closure putus-putus berlabel, tanpa fill (DAT-132) |
| Apparatus | mode page; fisik dan logika tidak dicampur dalam satu gambar sehingga perlu dua gambar bila dua-duanya dibutuhkan; legenda tipe tautan sebagai baris kunci (R-2 §DIA-03; DAT-133) |
| Lebar | 166 mm untuk WAN atau rute fiber multi-situs; 128 mm untuk LAN satu ruang (DAT-124) |
| ANTI-kasus | tanpa label tiap tautan (media, kecepatan, ID); mencampur fisik dan logika dalam satu gambar; simbol vendor non-standar tanpa legenda (R-2 §DIA-03) |
| Contoh-pakai dokumen GSP | arsitektur LAN/WAN situs pada Kajian Teknis SPPT; rute fiber dan segmentasi VLAN kamera-NVR-VMS pada proposal VSS; peta uplink data center pada proposal infrastruktur |
| Sitasi | R-2 §DIA-03 (rung W_net, Z3_net; RFC 8345 rung X_rfc8345, Z2_rfc8345); R-1 DAT-127, DAT-132 |

### DIA-04 Stack diagram (daftar berlapis)

| Field | Isi |
|---|---|
| Keluarga DATUM | stack (DAT-127) |
| Bentuk node + makna | box per lapis dengan label peran lapis (bukan nama produk); tanpa layout geografis (R-2 §DIA-04) |
| Konektor + pola/warna | panah antar-lapis hanya bila interaksi nyata (data solid); larangan panah hias antar semua lapis (DAT-129, DAT-122) |
| Routing | arah lapis atas-bawah konsisten; satu lebar per lapis dijaga kisi (DAT-131) |
| Trust zone | grup lapis keamanan dapat di-closure putus-putus bila klaim berlapisnya yang dijual (DAT-132) |
| Apparatus | mode page; jumlah lapis lebih dari 9 wajib digrup lebih dulu (anti-kasus); keterangan sumber per lapis masuk notes[] bukan tempelan gambar (DAT-124, DAT-134) |
| Lebar | 128 mm default (DAT-124) |
| ANTI-kasus | klaim urutan komunikasi real-time (itu DIA-05); jumlah lapis lebih dari 9 tanpa grup (R-2 §DIA-04, rujukan dikoreksi 5.3) |
| Contoh-pakai dokumen GSP | tumpukan protokol komunikasi perangkat pada proposal integrasi; arsitektur ekosistem 5-lapisan Brahma (contoh internal terkurasi R-2 §DIA-04); security-in-depth CCTV dari kamera sampai VMS pada kajian VSS |
| Sitasi | R-2 §DIA-04 (arc42 building-block rung AR1; contoh internal IL faktas/arsitektur-ekosistem-brahma-5-lapisan); R-1 DAT-127 |

### DIA-05 Sequence diagram (UML)

| Field | Isi |
|---|---|
| Keluarga DATUM | sequence (DAT-127) |
| Bentuk node + makna | objek di kepala lifeline vertikal (box); waktu ke bawah; activation bar menandai eksekusi (R-2 §DIA-05) |
| Konektor + pola/warna | pesan berupa panah horizontal berlabel imperatif plus payload (data solid); balasan kepala terbuka (control); sinkron versus asinkron dibedakan pola garis lebih dulu, sync titik untuk event lemah (DAT-129) |
| Routing | lifeline snap kisi; pesan tidak menembus activation objek lain (detour, DAT-130) |
| Trust zone | lifeline milik sistem pihak ketiga di-closure putus-putus agar batas kendali terlihat (DAT-132) |
| Apparatus | mode page; judul menyebut rentang interaksi yang digambar; waktu absolut tidak dibaca dari jarak gambar dan deklarasi itu masuk catatan kaki gambar (R-2 §DIA-05; AP-1) |
| Lebar | 166 mm bila objek lima atau lebih; lebih dari 7 objek adalah anti-kasus (R-2 §DIA-05; DAT-124) |
| ANTI-kasus | alur keputusan bercabang kompleks (pakai DIA-01; semantik activity UML tidak berdiri sendiri di registri ini); jumlah objek lebih dari 7; waktu absolut diklaim dari jarak gambar (R-2 §DIA-05, rujukan dikoreksi 5.3) |
| Contoh-pakai dokumen GSP | interaksi API VMS dengan NVR dan engine analitik pada proposal sistem pengawasan; handshake BMS dengan SCADA pada kajian gedung; urutan autentikasi pengguna DEMS saat login |
| Sitasi | R-2 §DIA-05 (rung W2_seq, Z3_seq; OMG UML 2.5.1 rung O1, X_omg_uml_pdf); R-1 DAT-127 |

### DIA-06 State diagram / statechart

| Field | Isi |
|---|---|
| Keluarga DATUM | graph, penempatan per col/row (DAT-127) |
| Bentuk node + makna | box state; pseudo-state awal dan akhir lewat circle; self-transition digambar busur; guard dalam kurung siku (R-2 §DIA-06) |
| Konektor + pola/warna | transisi berupa panah berlabel event dengan guard dan aksi (data solid); transisi gagal memakai alert putus panjang warna alert (DAT-129) |
| Routing | penempatan per col/row menjaga level statechart hierarkis terbaca (DAT-131) |
| Trust zone | region paralel di-closure putus-putus berlabel (DAT-132) |
| Apparatus | mode page; daftar state lengkap harus muncul juga sebagai tabel status bila dipakai sebagai spesifikasi penerimaan (AP-1; designasi perangkat ikut DAT-145) |
| Lebar | 128 mm default; 166 mm bila region paralel berdampingan (DAT-124) |
| ANTI-kasus | sistem dengan state tak hingga atau kontinu; dipakai sebagai pengganti flowchart prosedur manusia (R-2 §DIA-06) |
| Contoh-pakai dokumen GSP | mesin status tiket layanan pemeliharaan dari terbuka, ditangani, menunggu suku cadang, sampai selesai; mode operasi UPS normal-degraded-bypass pada kajian power backup; status aset pada aplikasi pendukung kajian |
| Sitasi | R-2 §DIA-06 (rung W3_state, Z3_state; Harel 1987 DOI 10.1016/0167-6423(87)90035-9 rung Z_harel); R-1 DAT-127 |

### DIA-07 ER diagram (entity-relationship)

| Field | Isi |
|---|---|
| Keluarga DATUM | graph (DAT-127) |
| Bentuk node + makna | box entitas; atribut terikat entitas; relasi kata kerja dengan kardinalitas WAJIB di kedua ujung (notasi Chen atau crow's foot) (R-2 §DIA-07) |
| Konektor + pola/warna | sisi relasi solid (data); kardinalitas ditulis di ujung, bukan di legenda warna (DAT-129, AB-10) |
| Routing | penempatan per col/row; hindari silang padat dengan agregasi entitas (DAT-130, DAT-131) |
| Trust zone | sub-skema milik sistem lain di-closure bila model menyentuh perbatasan sistem (DAT-132) |
| Apparatus | mode page; kamus entitas sebagai tabel pendamping di teks, gambar hanya kerangka relasi (AP-1) |
| Lebar | 166 mm bila entitas delapan atau lebih; lebih dari 20 entitas satu kanvas adalah anti-kasus (R-2 §DIA-07; DAT-124) |
| ANTI-kasus | desain fisik tabel atau partisi (pakai skema DDL); entitas lebih dari 20 satu kanvas (R-2 §DIA-07) |
| Contoh-pakai dokumen GSP | model data aset proyek (aset, lokasi rak, posisi U, hasil uji) pada desain aplikasi pendukung kajian; model data kontrak pemeliharaan dengan join key designasi IEC 81346 (DAT-145) |
| Sitasi | R-2 §DIA-07 (Chen 1976 DOI 10.1145/320434.320440 rung O_chen; rung W2_er, Z3_er); R-1 DAT-127 |

### DIA-08 Data-flow diagram (DFD Gane-Sarson / Yourdon)

| Field | Isi |
|---|---|
| Keluarga DATUM | flow atau graph (DAT-127) |
| Bentuk node + makna | proses sebagai kotak Gane-Sarson, datastore cylinder, entitas eksternal shadowed, aliran data berarah (DAT-128; bentuk DFD sudah jadi baseline Tabel 6.3) |
| Konektor + pola/warna | aliran data solid berlabel kata benda; TANPA kontrol atau percabangan karena itu wilayah DIA-01 (DAT-129, R-2 §DIA-08) |
| Routing | penomoran level 0, 1, 2 konsisten; satu proses satu fungsi atomik per level; anak gambar merujuk parent lewat circle off-page (R-2 §DIA-08; DAT-128) |
| Trust zone | boundary sistem digambar closure putus-putus; entitas eksternal selalu di luarnya (DAT-132, DAT-128) |
| Apparatus | mode page; register datastore masuk notes[]; SUMBER bawah menyebut dokumen klien asal aliran (DAT-124, AP-1) |
| Lebar | 166 mm untuk level 1 ke bawah; level 0 cukup 128 mm (DAT-124) |
| ANTI-kasus | kontrol atau percabangan (itu DIA-01); dicampur UML activity dalam satu gambar (R-2 §DIA-08) |
| Contoh-pakai dokumen GSP | analisis sistem informasi klien pada tahap kajian DEMS dari sensor, agregasi, sampai laporan; boundary sistem VMS terhadap jaringan kantor pada kajian keamanan siber fisik |
| Sitasi | R-2 §DIA-08 (rung W2_dfd, Z3_dfd; Chapin 1978 DOI 10.1145/1040730.1040732 dan Gane-Sarson 1981 DOI 10.1145/800175.809823 rung OA_gane); R-1 DAT-127, DAT-128 |

### DIA-09 Deployment diagram (UML)

| Field | Isi |
|---|---|
| Keluarga DATUM | topology atau graph (DAT-127) |
| Bentuk node + makna | node komputasi sebagai doubled (subsistem berstruktur lanjut); artefak software digambar di dalam node; label node adalah perangkat plus lokasi (DAT-128; R-2 §DIA-09) |
| Konektor + pola/warna | konektor antar node solid berlabel protokol atau tautan; control putus-putus untuk jalur manajemen (DAT-129) |
| Routing | fanned anchors pada gateway multi-cabang; detour mengelilingi node tak terkait (DAT-130) |
| Trust zone | zona DMZ dan intranet WAJIB closure putus-putus berlabel; inilah pola trust zone paling sering dipakai keluarga ini (DAT-132) |
| Apparatus | mode page; daftar artefak per node harus bisa dibaca sebagai teks (AP-9); kapasitas daya per node dirujuk ke tabel, bukan digambar di sudut (AP-1) |
| Lebar | 166 mm lazim karena zona dan lokasi (DAT-124) |
| ANTI-kasus | topologi jaringan murni (pakai DIA-03); elevasi rak fisik (pakai DIA-13) (R-2 §DIA-09) |
| Contoh-pakai dokumen GSP | penempatan server VMS, edge recorder, dan gateway DMZ pada proposal infrastruktur data center; topologi penempatan sensor DEMS per gedung dengan artefak firmware di dalamnya |
| Sitasi | R-2 §DIA-09 (rung W3_dep, Z3_dep; OMG UML 2.5.1 sebagaimana DIA-05); R-1 DAT-127, DAT-128, DAT-132 |

### DIA-10 Arsitektur deskripsi multi-view (ISO/IEC/IEEE 42010 + C4 + arc42)

| Field | Isi |
|---|---|
| Keluarga DATUM | lintas keluarga (layered, topology, stack) sebagai payung pemilihan view (R-2 §DIA-10) |
| Bentuk node + makna | mengikuti view terpilih; aturan normatifnya ada di level gambar: satu gambar satu view satu level zoom, judul menyebut view dan level (R-2 §DIA-10) |
| Konektor + pola/warna | mengikuti pola target view (DIA-03, DIA-04, DIA-09, DIA-11); larangan mencampur level zoom dalam satu kanvas (analogi DAT-144 untuk view) |
| Routing | mengikuti pola target view (DAT-130) |
| Trust zone | stakeholder view dapat menutup wilayah tanggung jawab per view (DAT-132) |
| Apparatus | mode page; judul wajib memuat nama view dan level zoom (mis. Container); register asumsi arsitektur masuk Register asumsi 4 kolom dokumen (KD-20; AP-1) |
| Lebar | per view; Context 128 mm lazim cukup, Component naik ke 166 mm (DAT-124) |
| ANTI-kasus | dianggap standar gambar tunggal karena 42010 tidak menormakan notasi visual; C4 dipakai memaksa semua stakeholder membaca level Component (R-2 §DIA-10) |
| Contoh-pakai dokumen GSP | memilih Context view untuk bab ringkasan eksekutif proposal dan Container view untuk lampiran teknis; menjaga konsistensi antar gambar arsitektur saat paket penawaran lintas disiplin (VSS, daya, fiber) |
| Sitasi | R-2 §DIA-10 (c4model.com rung CM1; arc42 rung AR1; 42010:2011 DOI IEEE rung V2_42010; edisi 2022 belum terverifikasi sehingga kutipan edisi 2022 diblokir sampai terverifikasi, N-8 dan R-6 D-10); R-4 KD-20 |

### DIA-11 Layered architecture diagram

| Field | Isi |
|---|---|
| Keluarga DATUM | layered (DAT-127) |
| Bentuk node + makna | strata horizontal box; label lapis adalah peran bukan produk; interaksi hanya antar-lapis bertetangga kecuali digambar eksplisit (R-2 §DIA-11) |
| Konektor + pola/warna | panah dependensi solid searah konsisten; panah lintas banyak lapis tanpa alasan adalah anti-kasus (DAT-129) |
| Routing | satu lebar per lapis (kisi DAT-131); arah dependensi tidak boleh bolak-balik antar lapis |
| Trust zone | lapis yang berada di luar lingkup kontrak diberi garis 05.1 putus-panjang-dua-titik (DAT-146) plus closure bila perlu (DAT-132) |
| Apparatus | mode page; keterangan mekanisme antar-lapis masuk teks, bukan anotasi renik dalam gambar (AP-1, AP-9) |
| Lebar | 128 mm default (DAT-124) |
| ANTI-kasus | semantik waktu karena lapis bukan fase; panah lintas banyak lapis tanpa alasan (R-2 §DIA-11) |
| Contoh-pakai dokumen GSP | tier presentation-service-data aplikasi DEMS pada proposal; stratifikasi keamanan berlapis perimeter-jaringan-host pada kajian VSS; tumpukan proteksi daya genset-UPS-PDU bila digambar sebagai lapis fungsi, sementara rantai elektrikalnya tetap DIA-14 |
| Sitasi | R-2 §DIA-11 (arc42 building-block rung AR1; contoh internal IL arsitektur Brahma 5-lapisan); R-1 DAT-127, DAT-146 |

### DIA-12 Sankey / alluvial (arus proporsional)

| Field | Isi |
|---|---|
| Keluarga DATUM | graph dengan arus proporsional (DAT-127) |
| Bentuk node + makna | simpul sumber, transformasi, dan beban sebagai box sempit; pita pelebar menyandeng besaran aliran karena lebar pita sebanding nilai (R-2 §DIA-12) |
| Konektor + pola/warna | pita solid; warna adalah sumber atau arah, bukan kategori acak; total masuk-keluar diberi label angka (DAT-129, R-2 §DIA-12) |
| Routing | layout hierarkis Sugiyama meminimalkan silang (R-2 §DIA-19 sebagai basis layout); angka kecil tidak boleh dibaca presisi dari lebar |
| Trust zone | aliran di luar boundary sistem ditandai control putus-putus, bukan pita penuh (DAT-129, DAT-132) |
| Apparatus | mode page; neraca masuk-keluar wajib berlabel angka dengan satuan ISO 80000-1 (AP-3); ketidakseimbangan wajib dicatat terang di caption, bukan dibiarkan tampak konservatif (AP-1, R-2 §DIA-12) |
| Lebar | 166 mm hampir selalu perlu karena lebar pita yang harus terbaca (DAT-124) |
| ANTI-kasus | aliran tidak konservatif (masukan tidak sama dengan keluaran) tanpa catatan; lebih dari sekitar 12 simpul; angka kecil dibaca presisi dari lebar (R-2 §DIA-12) |
| Contoh-pakai dokumen GSP | neraca energi situs (pembangkit, beban, rugi) pada kajian power backup; aliran material pada kajian logistik proyek; jembatan konsumsi daya per lantai gedung pada kajian BMS |
| Sitasi | R-2 §DIA-12 (rung W2_sankey, Z3_sankey, Z2_sankey_src; Sugiyama 1981 DOI 10.1109/tsmc.1981.4308636 rung V2_sugi); R-1 DAT-127 |

### DIA-13 Rack elevation

| Field | Isi |
|---|---|
| Keluarga DATUM | rack (DAT-127) |
| Bentuk node + makna | grid unit 1U per baris; perangkat adalah blok pengisi slot; slot kosong WAJIB berlabel kosong, bukan diam (R-2 §DIA-13) |
| Konektor + pola/warna | umumnya tanpa konektor antar-perangkat; jalur PDU atau rail digambar control putus-putus bila diperlukan; label posisi U beban-rilis berupa teks nyata (DAT-129, AP-9) |
| Routing | sumbu U eksplisit 1 sampai 42; setiap slot berisi perangkat ATAU kosong berlabel (R-2 §DIA-13) |
| Trust zone | area sewa versus area milik klien di-closure putus-putus bila satu rak berbagi wilayah (DAT-132) |
| Apparatus | mode page; kapasitas daya per rail dan berat kumulatif jangan dihilangkan dari apparatus meski tidak digambar dalam rak (R-2 §DIA-13); designasi perangkat ikut IEC 81346 agar tertelusur ke BoQ (DAT-145) |
| Lebar | 128 mm untuk satu rak tunggal; 166 mm untuk deret beberapa rak berdampingan (DAT-124) |
| ANTI-kasus | dimensi mekanik mengikat tanpa merujuk EIA-310/TIA; perangkat digambar skala-gambar bukan skala-U (R-2 §DIA-13) |
| Contoh-pakai dokumen GSP | rencana tata letak rak 42U ruang data center pada proposal infrastruktur; audit kapasitas U sisa pada kajian peremajaan; posisi NVR, switch, dan PDU per-U pada lampiran instalasi VSS |
| Sitasi | R-2 §DIA-13 (baseline DAT-127; EIA-310 via mirror BSI doi.org/10.3403/30122102 rung V2_eia310 berupa backs-resolver Crossref, dicatat jujur R-2 §5.4 dan N-9; situs TIA/BICSI langsung mati DNS); R-1 DAT-127, DAT-145 |

### DIA-14 Single-line diagram (SLD) tenaga

| Field | Isi |
|---|---|
| Keluarga DATUM | sld (DAT-127) |
| Bentuk node + makna | busbar stroke berat sebagai rel; simbol peralatan listrik baku pustaka iec berupa glif SIM dari lajur 8, di mana empat sakelar berbagi satu konstruksi dan berbeda hanya tandanya, sebab pemisah yang digambar sebagai pemutus daya mengklaim kemampuan hubung singkat yang tidak ada (DAT-140); satu konduktor boleh mewakili banyak fasa dengan deklarasi di legenda (R-2 §DIA-14) |
| Konektor + pola/warna | rangkaian daya solid (data) orientasi aliran atas-ke-bawah; sirkuit kendali dan interlock memakai control putus-putus; pekerjaan di luar kontrak memakai garis 05.1 (DAT-129, DAT-146) |
| Routing | proteksi digambar urut pada feeder; fanned anchors pada cabang busbar (DAT-130) |
| Trust zone | batas kepemilikan (PLN versus genset milik klien) berupa closure putus-putus berlabel (DAT-132) |
| Apparatus | mode page; deklarasi jumlah fasa dan dasar arus hubung singkat di legenda atau catatan; designasi fungsi-lokasi-produk wajib muncul juga di BoQ dan uji terima (DAT-145; AP-1, AP-3) |
| Lebar | 166 mm untuk distribusi penuh; 128 mm untuk rantai satu feeder (DAT-124) |
| ANTI-kasus | kabel kontrol detail (pakai wiring diagram multi-line, di luar registri ini sampai terverifikasi); SLD dipakai untuk instalasi rumah karena dialek IEC 60617 berbeda (R-2 §DIA-14) |
| Contoh-pakai dokumen GSP | rantai genset, ATS, UPS, dan beban pada Kajian Teknis UPK dan Proposal UPK-70; interlock dual-source pada kajian power backup; satu garis distribusi panel PP ke beban-beban kritis |
| Sitasi | R-2 §DIA-14 (rung W2_sld, Z3_sld; basis simbol IEC 60617 lajur 8; IEEE C37.2 KOSONG karena identifier N-5 sehingga kutipan C37 DIBLOKIR per R-6 D-10; ISA-5.1-2024 untuk instrumen mengikuti putusan D-09); R-1 DAT-127, DAT-140, DAT-145, DAT-146 |

### DIA-15 P&ID (piping and instrumentation diagram)

| Field | Isi |
|---|---|
| Keluarga DATUM | flow dengan simbol ISA (DAT-127; Tabel 6.6) |
| Bentuk node + makna | peralatan proses dan instrumen dengan bubble ISA dua-sumbu, di mana bentuk menyandeng fungsi dan garis horizontal menyandeng lokasi; menjatuhkan garis mengubah indikator ruang kendali menjadi instrumen lapangan secara diam-diam (DAT-141); huruf pertama tag adalah variabel yang diukur (R-2 §DIA-15) |
| Konektor + pola/warna | garis beda media, instrumen, dan sinyal dibedakan POLA garis lebih dulu (data, control, verify) sesuai AB-10 dan DAT-129 |
| Routing | loop kontrol digambar utuh dari sensor ke aktuator; silang antar-loop memakai lompat-silang (DAT-130) |
| Trust zone | enclosure loop kontrol dan batas sistem BMS berupa closure putus-putus (DAT-132) |
| Apparatus | mode page; register tag WAJIB ada sebagai tabel pendamping karena tag adalah kunci jejak sekaligus join key IEC 81346 (DAT-145); tanpa register tag gambar tidak boleh terbit (R-2 §DIA-15) |
| Lebar | 166 mm hampir selalu; area proses luas dipecah per area (DAT-124) |
| ANTI-kasus | alur material non-proses; P&ID tanpa register tag (R-2 §DIA-15) |
| Contoh-pakai dokumen GSP | integrasi sistem SCADA/BMS pada kajian gedung dari loop sensor HVAC ke aktuator; dokumen serah terima plant dengan tag list; dialek ISA juga dipakai untuk instrumen lingkungan ruang server pada kajian daya |
| Sitasi | R-2 §DIA-15 (rung W2_pid, Z3_pid; ISA-5.1 produk resmi isa.org rung isa51 dengan edisi berlaku 2024 per putusan D-09; mirror crossref rung V2_pidstd); R-1 DAT-127, DAT-141, DAT-144 |

### DIA-16 Timeline / roadmap

| Field | Isi |
|---|---|
| Keluarga DATUM | graph atau stack, penempatan per col/row (DAT-127) |
| Bentuk node + makna | sumbu waktu horizontal; milestone sebagai circle atau diamond; peristiwa sebagai box label (kosakata bentuk DAT-128) |
| Konektor + pola/warna | rentang sebagai bar solid netral; accent satu tonggak kunci seperti tanggal serah terima kontrak (DAT-129, DAT-133) |
| Routing | tanggal pada tick, bukan hanya label acara; hari kerja versus kalender dinyatakan (R-2 §DIA-16) |
| Trust zone | segmen di luar lingkup kontrak diberi garis 05.1 (DAT-146) |
| Apparatus | mode page; tahun anggaran ditulis gaya dokumen (TA 2027); skala logaritmik tanpa penanda adalah anti-kasus (AP-1; R-2 §DIA-16) |
| Lebar | 166 mm untuk lintasan multi-tahun; 128 mm untuk satu seri milestone (DAT-124) |
| ANTI-kasus | ketergantungan antar tugas detail (pakai DIA-17); skala waktu logaritmik tanpa penanda (R-2 §DIA-16) |
| Contoh-pakai dokumen GSP | jadwal implementasi bertahap tiga TA pada proposal penyelenggaraan; sejarah insiden besar pada laporan pasca-kejadian; lintasan upgrade firmware armada pada rencana peremajaan |
| Sitasi | R-2 §DIA-16 (rung W3_timeline, Z3_tl); R-1 DAT-127 |

### DIA-17 Gantt chart (jadwal proyek)

| Field | Isi |
|---|---|
| Keluarga DATUM | graph (DAT-127) |
| Bentuk node + makna | bar rentang per aktivitas pada kisi aktivitas-versus-waktu; milestone dibedakan bentuk (diamond atau circle); float dibedakan bentuk (R-2 §DIA-17) |
| Konektor + pola/warna | panah dependensi antar bar (control tipis); bar progres status kini dibedakan tinting, bukan warna acak (DAT-129, DAT-133) |
| Routing | hari ini digaris vertikal eksplisit; tanggal pada skala bulan eksplisit (R-2 §DIA-17) |
| Trust zone | pekerjaan di luar kontrak memakai bar bergaris 05.1 (DAT-146) |
| Apparatus | mode page; progres persen wajib punya dasar pengukuran yang dideklarasikan (AP-1; R-2 §DIA-17); kurva-S turunan menjadi gambar terpisah |
| Lebar | 166 mm; lebih dari 150 baris cetak dipecah per paket pekerjaan (R-2 §DIA-17; DAT-124) |
| ANTI-kasus | lebih dari 150 baris cetak tanpa pecah; ketergantungan implisit tanpa panah; progres persen tanpa dasar pengukuran (R-2 §DIA-17) |
| Contoh-pakai dokumen GSP | jadwal pelaksanaan kontrak pada bab perencanaan proposal teknis sebagai basis kurva-S penagihan termin; jadwal shutdown dan migrasi peremajaan UPS dengan jendela kerja malam; roadmap pengadaan bertahap TA 2026 sampai 2028 pada rencana induk |
| Sitasi | R-2 §DIA-17 (rung W2_gantt, Z2_gantt_prim atribusi via OpenLibrary numFound 22); R-1 DAT-127 |

### DIA-18 Tree diagram / hierarki (WBS, pohon keputusan)

| Field | Isi |
|---|---|
| Keluarga DATUM | layered atau graph (DAT-127) |
| Bentuk node + makna | simpul induk-anak box; daun bernomor mengikuti penomoran dokumen (R-2 §DIA-18) |
| Konektor + pola/warna | garis parent-anak solid tanpa panah bila murni dekomposisi; panah hanya bila ada arah aliran (DAT-129) |
| Routing | tingkat indentasi konsisten; kedalaman lebih dari 5 pada cetak adalah anti-kasus (R-2 §DIA-18) |
| Trust zone | cabang di luar lingkup penawaran diberi closure putus-putus berlabel (DAT-132) |
| Apparatus | mode page; penomoran daun harus bisa dijadikan penomoran bab atau baris BoQ sebagai analogi join key DAT-145 (AP-1) |
| Lebar | 128 mm default; 166 mm untuk WBS dua kolom paralel (DAT-124) |
| ANTI-kasus | silang antar-cabang (itu graph umum DIA-19); kedalaman lebih dari 5 pada cetak (R-2 §DIA-18) |
| Contoh-pakai dokumen GSP | WBS dekomposisi lingkup penawaran per paket pekerjaan pada proposal; taksonomi aset site per gedung pada kajian inventaris; pohon eskalasi kegagalan daya (PLN, genset, UPS, beban) sebagai alat bantu narasi sebelum SLD DIA-14 |
| Sitasi | R-2 §DIA-18 (rung Z3_tree; disambiguasi Tree_diagram tercatat ladder); R-1 DAT-127 |

### DIA-19 Graph umum (network/undirected, Sugiyama DAG)

| Field | Isi |
|---|---|
| Keluarga DATUM | graph, penempatan per col/row (DAT-127) |
| Bentuk node + makna | simpul box bebas constraint layout khusus; arah panah adalah dependensi bukan aliran waktu kecuali dinyatakan (R-2 §DIA-19) |
| Konektor + pola/warna | sisi berarah solid untuk dependensi; agregasi cluster bila edge padat (DAT-129) |
| Routing | DAG hierarkis memakai penempatan lapisan Sugiyama untuk meminimalkan persilangan; crossing dioptimalkan bukan diacak (R-2 §DIA-19; DAT-130) |
| Trust zone | cluster milik sistem berbeda diberi closure putus-putus (DAT-132) |
| Apparatus | mode page; edge lebih dari sekitar 60 tanpa agregasi adalah anti-kasus; tabel adjacency menjadi pendamping teks bila graf dipakai sebagai acuan uji (AP-1) |
| Lebar | 166 mm lazim (DAT-124) |
| ANTI-kasus | edge lebih dari sekitar 60 tanpa agregasi; arah tanpa makna (R-2 §DIA-19) |
| Contoh-pakai dokumen GSP | graf dependensi integrasi multi-situs (VMS pusat, cabang, link WAN) pada kajian arsitektur; peta ketergantungan modul aplikasi DEMS pada lampiran desain |
| Sitasi | R-2 §DIA-19 (Sugiyama 1981 DOI 10.1109/tsmc.1981.4308636 rung V2_sugi; Moradi dkk. 2025 DOI 10.1109/iv68685.2025.00031 rung V2_sugi); R-1 DAT-127 |

### DIA-20 Architecture modeling language (ArchiMate / UML deployment / BPMN)

| Field | Isi |
|---|---|
| Keluarga DATUM | lintas keluarga sebagai aturan dialek (DAT-127, DAT-144) |
| Bentuk node + makna | mengikuti bahasa terpilih; sudut kanan-bawah gambar menandai dialek plus versi (R-2 §DIA-20) |
| Konektor + pola/warna | mengikuti dialek; mencampur dua dialek dalam satu gambar diblokir lint 35 (DAT-144; DAT-129) |
| Routing | mengikuti pola target; engine hanya menjamin satu dialek per gambar (DAT-144) |
| Trust zone | viewpoint ArchiMate dapat menutup wilayah stakeholder (DAT-132) |
| Apparatus | mode page; penanda dialek-plus-versi adalah bagian aparatus, bukan hiasan (AP-1; R-2 §DIA-20) |
| Lebar | mengikuti pola view yang dipilih (DAT-124) |
| ANTI-kasus | mencampur dialek dalam satu gambar; ArchiMate untuk detail teknis perangkat karena salah granularitas (R-2 §DIA-20) |
| Contoh-pakai dokumen GSP | klien mensyaratkan model enterprise ArchiMate pada tender instansi sehingga dipilih viewpoint terdaftar lalu digambar dengan engine; proses bisnis pelayanan BPMN sebagai lampiran proposal DEMS; konsistensi notasi lintas disiplin saat satu paket dikerjakan tim VSS dan tim sipil |
| Sitasi | R-2 §DIA-20 (Open Group rung Z2_opengroup dengan token spesifikasi standar tercetak; OMG rung OM4; ISO 19510 BPMN rung WS_19510); R-1 DAT-144 |

### DIA-21 Matriks ketertelusuran (RTM; adopsi putusan D-11)

| Field | Isi |
|---|---|
| Keluarga DATUM | graph, penempatan per col/row; berstatus matriks dan BUKAN chart, penegasan yang ditegaskan R-2 §5 dan R-3 daun B.9 agar tidak tersesat ke pohon chart |
| Bentuk node + makna | sel matriks dengan baris persyaratan (thread REQ) dan kolom artefak pemenuh (gambar, tabel, uji); isi sel berupa mark ketertelusuran LABEL TEKS seperti "uji", "gambar", "belum", bukan glif peran (AP-2; KD-20 mewajibkan matriks ketertelusuran sebagai bagian register dokumen) |
| Konektor + pola/warna | tidak ada konektor tergambar; hubungan dibawa kunci gabung berupa designasi IEC 81346 dan nomor persyaratan (DAT-145); highlight sel terpenuhi memakai satu accent, sisanya netral (DAT-133) |
| Routing | tidak berlaku untuk garis; keterbacaan ditentukan urutan kolom yang mengikuti urutan bab dokumen induk, bukan alfabetis (aturan tata bahasa tabel KD-13) |
| Trust zone | kolom artefak di luar lingkup kontrak ditandai header bergaris ganda atau catatan kaki, selaras tipe garis 05.1 untuk lingkup (DAT-146) |
| Apparatus | mode tabel dokumen (bukan figur): caption atas bernomor plus tanggal dalam judul, SUMBER bawah, kepala kolom berisi satuan atau peran (KD-13); bila dirender sebagai figur matriks mandiri berlaku mode figure penuh (DAT-134) |
| Lebar | sebagai tabel memakai lebar teks halaman; sebagai figur matriks hanya 166 mm (DAT-124; KD-09) |
| ANTI-kasus | dipakai sebagai bukti ketertelusuran padahal sel berisi glif tanpa label (langgar AP-2); baris persyaratan tanpa owner dan status padahal harus ikut Register asumsi dan thread REQ (KD-20); matriks kotak penuh centang tanpa satu pun sel "belum" yang jujur, sebab kosong lebih baik daripada salah (SPK-002 butir 3) |
| Contoh-pakai dokumen GSP | matriks persyaratan spesifikasi klien ke gambar as-built, hasil uji terima, dan baris BoQ pada dokumen SERAH, di mana join key designasi DAT-145 menutup rantai ini; lampiran kepatuhan tender DEMS yang menghubungkan butir syarat ke pasal jawaban dan buktinya; penelusuran GAP-nn manual ini sendiri memakai bentuk yang sama |
| Sitasi | R-2 §5 baris "(kosong) matriks ketertelusuran, diusulkan untuk kartu 13"; R-3 daun B.9; R-6 putusan D-11 yang mengadopsi RTM sebagai perluasan DIA; R-4 KD-20 yang menempatkan matriks ketertelusuran berpredikat PERSIS dalam anatomi dokumen |

## 5. Rekonsiliasi lintas lajur

### 5.1 Waterfall biaya tetap CH-16, tidak mendapat nomor DIA baru

Blueprint langkah 13 menyebut "waterfall biaya" dalam daftar pola eksternal.
Rekonsiliasinya adalah bahwa waterfall sudah dimiliki lajur chart sebagai CH-16
(jembatan nilai) dan telah dirutekan kartu 12 ke daun A.7 dengan syarat total
tertutup aritmetika dan subtotal bertanda (R-5; R-3 §A.7). Membuat DIA-22 untuk
konsep yang sama melanggar skema ID tunggal D-TA-11 yang menetapkan satu konsep
satu nomor lintas lajur. Yang dinormakan di sini hanyalah sisi diagrammatik
pemakaian biaya, yaitu sumbu nol bersama (AP-4), subtotal berlabel angka
(AP-1 dan AP-3), serta kolom melayang yang wajib menyatakan selisih sebagai
teks nyata (AP-9). Rujukan pemakaiannya adalah jembatan nilai RAB spesimen dari
subtotal per kelompok ke total penawaran (mis. RAB_Spesimen_UPK-70) memakai
CH-16 dengan apparatus ini. Sitasi primer waterfall tetap ikut register N-1
bahwa DOI Wilken dkk. HDSR 2019 KOSONG sehingga sitasinya berlabel PROV tanpa
DOI, per R-2 §6 dan blokir kutipan R-6 D-10.

### 5.2 Status RTM setelah adopsi

RTM tadinya hanya usulan di R-2 §5 dan R-3 daun B.9; putusan controller D-11
mengadopsinya sebagai perluasan DIA (R-6). Karena tidak ada nomor lama yang
menempatinya, registri ini menerbitkannya sebagai DIA-21 sebagai nomor lanjutan,
bukan nomor pinjaman dari lajur chart. Konsekuensi hilirnya adalah langkah 14
(INDEKS) dan langkah 15 (arsitektur manual) menghitung populasi DIA menjadi 21
dan mencabut label "usulan" dari R-3 daun B.9 saat dikutip.

### 5.3 Temuan cacat hulu: rujukan silang R-2 bergeser

Beberapa baris anti-kasus di R-2 §4 merujuk nomor DIA yang bergeser dari katalog
nomornya sendiri. Entri DIA-01 menulis "pakai DIA-05 swimlane" padahal swimlane
adalah DIA-02, lalu menulis "interaksi pesan antar sistem (pakai DIA-06)"
padahal sequence adalah DIA-05; entri DIA-04 menulis "itu DIA-06" untuk urutan
komunikasi real-time padahal yang dimaksud adalah sequence (DIA-05); entri
DIA-05 menulis "DIA-11 activity" padahal DIA-11 adalah layered architecture.
Registri ini memperbaiki rujukan saat menyalin anti-kasus, bukan menambal
gejala, karena definisi, kasus, dan sitasi R-2 lainnya diwarisi verbatim;
temuan dibukukan sebagai known-defect hulu untuk verifier. Sumber riset 02 tidak
diedit oleh lajur ini, mengikuti praktik kartu 12 yang tidak mengubah baseline.

## 6. Uji konsistensi terhadap KD-24 (butir per butir)

KD-24 berbunyi "Kontrak spec gambar + 9 keluarga + 10 bentuk + 6 konektor +
konvensi routing + trust zone + satu aksen + larangan Mermaid + aturan Figma"
dengan predikat kontrak PERSIS, yaitu grammar normatif yang dinormakan manual
karena renderer absen (R-4). Uji butir per butir dilakukan terhadap norma lajur
ini, bukan terhadap spesifikasi controller, mengikuti kaidah bahwa artefak
diukur pada sumber desainnya. Hasil lengkapnya sebagai berikut.

| Butir KD-24 | Dinormakan di | Predikat |
|-------------|---------------|----------|
| Kontrak spec gambar | 2.1 (DAT-123..126) | PERSIS |
| 9 keluarga | 3 (tabel DAT-127, sembilan nama) | PERSIS |
| 10 bentuk node | 2.2 (tabel sepuluh baris DAT-128) | PERSIS |
| 6 konektor | 2.3 (tabel enam baris DAT-129 + tipe garis DAT-146) | PERSIS |
| Konvensi routing (fanned anchors, crossing hops, obstacle detours) | 2.4 (DAT-130..131) | PERSIS |
| Trust zone | 2.5 (DAT-132) plus field per entri | PERSIS |
| Satu aksen | 2.6 (DAT-133; AP-6) | PERSIS |
| Larangan Mermaid | 2.9 (DAT-136; lint 31) | PERSIS |
| Aturan Figma (import lossless, export dilarang jadi keluaran) | 2.9 (DAT-136) | PERSIS |
| Lebar 128/166 saja (KD-09 ikut diuji) | 2.8 plus field Lebar per entri | PERSIS |
| Apparatus page versus figure | 2.7 (DAT-134..135; AP-1..AP-9) | PERSIS |

Tidak ada deviasi tanpa putusan controller pada seluruh tabel di atas. Edisi
simbol mengikuti putusan D-09 dan dibukukan di 2.10 sebagai koreksi fakta
terbitan, bukan perubahan bentuk kontrak. Anatomi grammar tetap utuh sehingga
verifier langkah 20 dapat menguji butir ini langsung terhadap dump sumber
desain tanpa perlu membaca ulang kontrak misi.

## 7. Verifikasi dan known-defect yang diwarisi

Verifikasi deterministik dijalankan lewat `work/f7p13_check.py` dengan jejak
cetakan di `work/f7p13_check_out.txt`. Yang diuji adalah populasi 21 entri tanpa
lubang; nol pola tanpa contoh-pakai dan tanpa tiga field beban-rilis lainnya;
sembilan keluarga lengkap dengan rute; hitung bentuk 10 dan konektor 6 persis;
kelima konvensi lapis-2 hadir; cakupan daun B.1 sampai B.9 penuh 21 ditambah
RTM; jejak A1 dan A2 nol; frontmatter dan H1 konsisten. Known-defect yang
diwarisi dan ditempel di rute pemakaiannya adalah N-5 bahwa identifier IEEE
C37.2 KOSONG sehingga kutipan C37 pada DIA-14 DIBLOKIR (R-6 D-10); N-1 bahwa DOI
waterfall KOSONG sehingga sitasinya berlabel PROV (bagian 5.1); EIA-310 pada
DIA-13 yang merupakan backs-resolver Crossref bukan TERUKUR-direct (dicatat
jujur R-2 §5.4 dan N-9); MIL-STD-2525E yang tetap BASELINE-ONLY ber-flag (2.10,
R-6 D-09); serta N-8 bahwa edisi 42010:2022 belum terverifikasi sehingga
kutipannya diblokir pada DIA-10. Temuan baru lajur ini adalah geseran rujukan
silang R-2 yang dibukukan di bagian 5.3.

## Referensi

| Ref | Berkas dan isi |
|-----|----------------|
| R-1 | `corpus/lajur1-datum-dokumen.md`, register DAT-121..DAT-146 hasil baca mendalam 000-GSP-STD-X-2026 RevA dan spesimen (lajur 1 misi ini) |
| R-2 | `research/02-tipologi-chart-diagram.md`, katalog DIA-01..DIA-20, AB-01 sampai AB-10, tangga ofensif dan LADDER, register N-1..N-9 |
| R-3 | `research/03-sintesis-dan-keputusan.md`, pohon tiga cabang, daun B.1 sampai B.9, AP-1..AP-10, VERIFIKASI-AKURASI SPK-002 |
| R-4 | `identification/02_structured.md`, blueprint, KONTRAK-DESAIN KD-01 sampai KD-32, keputusan D-TA-01..D-TA-12 |
| R-5 | `library/pohon-pemilihan-chart.md`, kartu 12 (CH-nn), Gerbang-Akar dan daun A.1..A.7 |
| R-6 | `contract.md`, Decision Log misi termasuk putusan controller D-09, D-10, D-11 tertanggal 05-10 |
