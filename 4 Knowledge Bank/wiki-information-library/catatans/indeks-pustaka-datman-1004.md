---
id: indeks-pustaka-datman-1004
type: catatan
title: INDEKS Pustaka DATMANUAL-1004 dan Skema Sitasi Lintas-Sesi
status: active
sumber: docs/2026-10-04-datum-manual/library/INDEKS.md (skema D-TA-02/D-TA-03/D-TA-11 dari identification/02_structured.md)
halaman: inventaris dua arah 46 jalur terverifikasi; 7 contoh sitasi jalan; checker work/f7p14_check.py
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, indeks, skema-sitasi, datman-namespace, titik-masuk]
links: [docs/2026-10-04-datum-manual/library/INDEKS.md]
penulis: gsp-custodian
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_08c4025e
pin_sha16_artefak: b9b8b668161471e5
catatan_keputusan: "dipromosikan: DATMANUAL-1004 P23: checker hulu diulang segar PASS; P22 verifier independen SALAH-TARGET=0 33/33; non-sensitif non-dosir"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/indeks-pustaka-datman-1004.md
---

# INDEKS Pustaka DATMANUAL-1004 dan Skema Sitasi Lintas-Sesi

Berkas ini adalah pelaksanaan langkah 14 blueprint `identification/02_structured.md`
dan titik masuk tunggal pustaka misi berdasarkan keputusan D-TA-02. Pustaka misi tinggal
di `docs/2026-10-04-datum-manual/` selama build berlangsung, dan ketahanannya lintas sesi
dijamin oleh promosi librarian pada langkah 23 ke jalur vault menuju wiki. Setiap kartu
hilir (langkah 15 arsitektur, langkah 17 Bagian II, verifier F4/F6) memulai rujukannya
dari daftar di bawah ini, bukan dari ingatan percakapan.

## 1. Skema sitasi (D-TA-02)

Skema di bawah adalah satu-satunya bentuk baku untuk rujukan lintas sesi dalam misi
ini. Setiap kartu hilir mengutip lewat pola tersebut, bukan lewat jalur absolut maupun
nomor baris, agar sitasi tetap resolve setelah kontrak dipromosikan. Tiga segmennya
berturut-turut adalah namespace misi, lapis direktori, dan nama berkas tanpa ekstensi,
dipisah anchor identitas entri setelah tanda pagar:

```
DATMAN/<LAPIS>/<nama-berkas-tanpa-ekstensi-md>#<ID-anchor>
```

| LAPIS | Direktori | Isi |
|---|---|---|
| `LIB` | `library/` | Katalog hasil konstruksi pustaka (SIM, CH, DIA) + laporan cakupan |
| `MEAS` | `measurement/` | Instrumen penegakan, sensus aturan, register perbaikan GAP |
| `RES` | `research/` | Riset eksternal mentah-terkurasi (sensus simbol, tipologi, sintesis) |
| `CORP` | `corpus/` | Register lajur-1 DAT-nn, lajur-2 WB-nn, lajur-3 korpus internal |
| `UND` | `understanding/` | Penjelasan pemahaman tertulis Tier-1 |

Empat aturan resolusi berikut diterapkan berurutan dari butir pertama. Sebuah sitasi
divonis cacat pada aturan pertama yang dilanggarnya, bukan pada kenyamanan pembaca.
Keempat aturan itu adalah:

1. Token berkas membuang ekstensi `.md`; resolver menambahkan `.md` kembali. Berkas
   `.json`, `.csv`, `.tsv`, `.txt`, `.log`, dan skrip dirujuk dengan nama lengkap
   ber-ekstensi dan selalu tanpa anchor.
2. Anchor wajib berupa token ID yang muncul verbatim di berkas sasaran, baik sebagai
   baris tabel maupun sebagai heading. Anchor yang tidak ditemukan di berkas sasaran
   adalah kutipan cacat dan wajib ditolak verifier.
3. Rujukan tanpa bagian `#` berarti seluruh berkas menjadi sasaran.
4. Rujukan per bagian memakai nomor seksi berkas sasaran, misalnya
   `DATMAN/MEAS/02-sensus-aturan#5`; angka setelah tanda pagar adalah nomor seksi,
   bukan nomor baris.

Skema ID mengikuti D-TA-11 sebagai kanonik: `DAT-nn` aturan dokumen dari 000, `WB-nn`
aturan workbook dari 001, `DM-nn` aturan manual hasil (baru lahir di langkah 15-18,
belum ada di pustaka saat indeks ini terbit), `GAP-nn` register perbaikan, `SIM-nn`
entri katalog simbol, `CH-nn` entri tipologi chart, `DIA-nn` pola diagram. Token
tambahan yang teramati di badan berkas dan ikut sah sebagai anchor: `K-nn` kelas simbol
riset 01, `AB-nn` aturan baca riset 02, `AP-n` apparatus wajib, `R-n` referensi per
berkas, `E-nn` temuan hulu bab 9 dokumen 000, `BK-nn` blok workbook. Perluasan LAPIS
di luar `LIB` (yakni `MEAS`, `RES`, `CORP`, `UND`) adalah generalisasi yang diputuskan
kartu ini karena D-TA-02 hanya membakukan bentuk `LIB`; controller boleh mengoverride
di Decision Log kontrak.

Contoh berikut adalah pola baku yang dipakai kartu-kartu hilir saat mengutip pustaka.
Ketujuhnya diuji hidup oleh checker milik kartu ini terhadap berkas sasaran masing-
masing, dan cetakan pengujian itu dapat dibaca di bagian 4 beserta bukti path lain.

| Sitasi | Sasaran | Lokasi terverifikasi |
|---|---|---|
| `DATMAN/LIB/katalog-simbol#SIM-01` | Entri breaker IEC | Baris tabel `SIM-01` di seksi 2 |
| `DATMAN/LIB/pohon-pemilihan-chart#CH-01` | Bar horisontal | Baris tabel `CH-01` di katalog daun A.1 |
| `DATMAN/LIB/registri-pola-diagram#DIA-01` | Flowchart proses | Heading `### DIA-01` di seksi 4 |
| `DATMAN/CORP/lajur1-datum-dokumen#DAT-01` | Doktrin bukti-ornamen | Baris tabel `DAT-01` |
| `DATMAN/CORP/lajur2-workbook-dan-nyata#WB-01` | Empat lapis workbook | Baris tabel `WB-01` |
| `DATMAN/MEAS/03-register-perbaikan#GAP-01` | Celah nama berkas bergaris-bawah | Baris tabel `GAP-01` |
| `DATMAN/RES/01-sensus-simbol#K-01` | Kelas simbol elektrik | Baris tabel `K-01` |
| `DATMAN/UND/01-penjelasan` | Penjelasan Tier-1 utuh | Seluruh berkas, tanpa anchor |

## 2. Aturan penamaan

Dua aturan berlaku di wilayah berbeda dan keduanya aktif dalam misi ini. Aturan pertama
adalah larangan underscore DATUM (dokumen 000 seksi 2.5, Tabel 20): underscore dilarang
di seluruh folder, berkas, sheet, tabel, figur, dan identifier rekayasa pada nama
terbit, karena nama bergaris-bawah mengumumkan bahwa mesin menulisnya untuk mesin.
Tabel 2.3 memberi pasangan benar-salah: folder Title Case dengan spasi dan prefiks
urutan dua digit, berkas dokumen berupa judul lalu nomor berhyphen, sheet huruf kapital
dengan hyphen maksimal 31 karakter. Nama manual final langkah 19 tunduk penuh pada
aturan ini.

Aturan kedua adalah D-TA-03: artefak internal antar-agen memakai snake_case sesuai
Documentation Contract, dengan satu pengecualian yaitu berkas manual final yang memakai
konvensi DATUM. Karena itu skrip, log, dan register mesin di direktori riset dan
pustaka sah membawa garis-bawah, sementara seluruh katalog pustaka berformat markdown
memakai nama kecil-bertanda-hyphen yang kompatibel dengan kedua aturan. Tiga berkas
markdown berawalan garis-bawah di `research/` (`_ladder_table.md`, `_part1.md`,
`_part2.md`) adalah scratch antara yang isinya sudah tergabung ke
`02-tipologi-chart-diagram.md`. Ketiganya terdaftar di inventaris bawah sebagai jejak
perakitan, dengan catatan bersih-bersih untuk langkah 23: jangan ikut dipromosikan ke
vault karena konten kanoniknya sudah hidup di berkas induk.

## 3. Inventaris pustaka

Jejak alat ukur (skrip checker dan cetakannya milik kartu-kartu sebelumnya) hidup di
`work/` dan bukan bagian dari indeks pustaka; direktori itu dirujuk lewat jalur kontrak
biasa. Ukuran nyata setiap berkas tercetak di bagian 4. Tabel per direktori di bawah
memuat tiga lajur wajib: path relatif dari akar kontrak, tujuan satu baris, dan cara
rujukan sesuai skema bagian 1.

### 3.1 library/ (pustaka hasil konstruksi)

| Path | Tujuan | Cara rujukan |
|---|---|---|
| `library/INDEKS.md` | Titik masuk pustaka + skema sitasi lintas-sesi (berkas ini) | `DATMAN/LIB/INDEKS` |
| `library/katalog-simbol.md` | Katalog 59 entri simbol hasil merger baseline DATUM dan sensus eksternal | `DATMAN/LIB/katalog-simbol#SIM-nn` |
| `library/pohon-pemilihan-chart.md` | Pohon pemilihan chart navigabel, 32 chart dengan syarat masuk dan anti-kasus | `DATMAN/LIB/pohon-pemilihan-chart#CH-nn` |
| `library/registri-pola-diagram.md` | Registri 21 pola diagram plus grammar normatif KD-24 | `DATMAN/LIB/registri-pola-diagram#DIA-nn` |
| `library/LAPORAN-CAKUPAN.md` | Sensus kecukupan tujuh lapisan korpus GSP; vonis STRATEGI B | `DATMAN/LIB/LAPORAN-CAKUPAN` atau per seksi |
| `library/il_dump.json` | Dump penuh cermin Information Library HQ, 818 entri (mesin) | jalur berkas, tanpa anchor |
| `library/il_class_sensus.json` | Sensus kelas topik di atas dump IL (mesin) | jalur berkas, tanpa anchor |
| `library/il_query.sh` | Alat query cermin IL untuk sensus F3-P0 | jalur berkas, tanpa anchor |
| `library/il_sensus.py` | Alat query dan sensus kelas pada entri IL | jalur berkas, tanpa anchor |
| `library/sweep_cakupan.py` | Sensus deterministik kecukupan library internal v2 | jalur berkas, tanpa anchor |
| `library/check_laporan.py` | Checker mandiri LAPORAN-CAKUPAN | jalur berkas, tanpa anchor |
| `library/sweep_out.txt` | Artefak pengalihan stdout, 0 byte, jejak kosong terdaftar | jalur berkas, tanpa anchor |

### 3.2 measurement/ (instrumen ukur dan penegakan)

| Path | Tujuan | Cara rujukan |
|---|---|---|
| `measurement/01-instrumen-penegakan.md` | Matriks aturan-ID ke instrumen penegak ke tahap ke status | `DATMAN/MEAS/01-instrumen-penegakan#DAT-nn` |
| `measurement/02-sensus-aturan.md` | Sensus cacah aturan ber-angka per aspek dan kelas penegakan plus tiga daftar celah | `DATMAN/MEAS/02-sensus-aturan#<no-seksi>` |
| `measurement/03-register-perbaikan.md` | Register celah penegakan GAP-01 sampai GAP-19 dengan vonis per baris | `DATMAN/MEAS/03-register-perbaikan#GAP-nn` |

### 3.3 research/ (riset eksternal terkurasi)

| Path | Tujuan | Cara rujukan |
|---|---|---|
| `research/01-sensus-simbol.md` | Sensus 21 kelas simbol eksternal dengan tangga 8 rung | `DATMAN/RES/01-sensus-simbol#K-nn` |
| `research/02-tipologi-chart-diagram.md` | Tipologi 32 chart dan 20 pola diagram plus aturan baca AB-nn | `DATMAN/RES/02-tipologi-chart-diagram#CH-nn` atau `#DIA-nn` |
| `research/03-sintesis-dan-keputusan.md` | Sintesis dua lajur riset, pohon keputusan, gerbang akurasi SPK-002 | `DATMAN/RES/03-sintesis-dan-keputusan#<no-seksi>` |
| `research/probe_ladder.csv` | Register ladder mentah append-only lajur simbol, per akun ber-timestamp | jalur berkas, tanpa anchor |
| `research/_ladder_table.md` | Tabel ladder lajur chart hasil kurasi (scratch assembly) | jalur berkas, tanpa anchor |
| `research/_part1.md` | Bagian rakitan awal berkas tipologi (scratch assembly) | jalur berkas, tanpa anchor |
| `research/_part2.md` | Bagian rakitan akhir berkas tipologi (scratch assembly) | jalur berkas, tanpa anchor |
| `research/probe_ruang.py` | Alat rung 1-3 probe jalur resmi lajur simbol | jalur berkas, tanpa anchor |
| `research/probe_obp.py` | Alat pencarian halaman resmi ISO via API OBP | jalur berkas, tanpa anchor |
| `research/probe_ddg.py` | Alat rung 4 pencarian aktif DDG-HTML | jalur berkas, tanpa anchor |
| `research/probe_final.py` | Alat finalisasi rung 1 halaman resmi kandidat | jalur berkas, tanpa anchor |
| `research/probe_r2.py` | Alat probe celah putaran-2 append-only | jalur berkas, tanpa anchor |
| `research/probe_r2b.py` | Alat resolver DDG bing putaran-2 | jalur berkas, tanpa anchor |
| `research/probe_r2c.py` | Alat hunter CDX wayback untuk katalog ISO | jalur berkas, tanpa anchor |
| `research/probe_r2d.py` | Alat verifikasi kandidat fetch langsung dengan fallback | jalur berkas, tanpa anchor |
| `research/probe_r2e.py` | Alat probe penutup wayback dan retry CDX | jalur berkas, tanpa anchor |
| `research/probe_round23.py` | Alat putaran-2 dan 3 kelas eksotis serta indeks komite | jalur berkas, tanpa anchor |
| `research/probe_cdx_r2.py` | Alat rung 5-7 arsip CDX, PDF resmi, aggregator PROV | jalur berkas, tanpa anchor |
| `research/render_rung8.py` | Alat rung 8 render browser halaman SPA | jalur berkas, tanpa anchor |
| `research/render_rung8b.py` | Alat rung 8b render dengan wait dan klik detail | jalur berkas, tanpa anchor |
| `research/check_sensus.py` | Checker deterministik sensus simbol terhadap ladder CSV | jalur berkas, tanpa anchor |
| `research/count_rounds.py` | Penghitung putaran dari ladder CSV | jalur berkas, tanpa anchor |
| `research/r2b_out.log` | Log probe r2b (timeout tercatat) | jalur berkas, tanpa anchor |
| `research/r2d_out.log` | Log probe r2d (status HTTP per kandidat) | jalur berkas, tanpa anchor |
| `research/render/` | 5 berkas JSON dump render rung 8 (ISA, MIL, NSO, NetNotation) | jalur direktori |
| `research/edge_tmp/` | Profil scratch browser Edge untuk rung 8, 245 berkas; bukan pengetahuan, kandidat bersih-bersih | jalur direktori |

### 3.4 corpus/ (register lajur sumber)

| Path | Tujuan | Cara rujukan |
|---|---|---|
| `corpus/lajur1-datum-dokumen.md` | Register aturan dokumen 000 (DAT-nn) plus spesimen UPK-70 | `DATMAN/CORP/lajur1-datum-dokumen#DAT-nn` |
| `corpus/lajur2-workbook-dan-nyata.md` | Register aturan workbook 001 (WB-nn) plus penilaian dua keluaran nyata | `DATMAN/CORP/lajur2-workbook-dan-nyata#WB-nn` |
| `corpus/lajur3-korpus-internal.md` | Sensus terukur EKAS dan dokumen proyek fleet | `DATMAN/CORP/lajur3-korpus-internal#<no-seksi>` |
| `corpus/skeleton-sidecar.json` | Kerangka mesin dokumen sumber 000 dan 001 (karakter, baris, tabel, heading) | jalur berkas, tanpa anchor |

### 3.5 understanding/ (pemahaman tertulis)

| Path | Tujuan | Cara rujukan |
|---|---|---|
| `understanding/01-penjelasan.md` | Penjelasan Tier-1 sistem DATUM lima aspek plus aparatus bukti, berdiri sendiri | `DATMAN/UND/01-penjelasan#<no-seksi>` |

## 4. Batas indeks dan bukti verifikasi path

Indeks ini hanya memetakan apa yang ada di lima direktori kontrak pada giliran ukur.
Tiga batasan wajib disadari pemakai sebelum mengandalkan daftar ini. Pertama, token
`DM-nn` belum punya sasaran: aturan manual hasil baru lahir pada langkah 15 sampai 18,
sehingga sitasi `DATMAN/LIB/...#DM-nn` baru bisa resolve setelah bab manual terbit.
Kedua, isi berkas scratch `research/_part1.md`, `_part2.md`, dan `_ladder_table.md`
sudah teruji tergabung penuh ke induknya `02-tipologi-chart-diagram.md`: uji inklusi
baris panjang (`work/f7p14_merge_check.py` dan `f7p14_merge_check2.py`) memberi 253/253,
243/243, dan 524/524 baris ditemukan di induk, sehingga scratch aman dibuang pada
langkah 23 tanpa kehilangan konten. Ketiga, profil browser `research/edge_tmp/`
(245 berkas) sengaja tidak didaftar per berkas karena isinya sampah instalasi Edge,
bukan pengetahuan.

Titik balik cara pakai daftar ini terletak pada satu pembeda: pencantuman bukan
persetujuan, melainkan hanya janji bahwa jalur dan anchor resolve. Berkas yang terdaftar
di sini belum tentu layak dikutip karena beberapa entri masih berflag PROV atau
terblokir kutipannya oleh controller sebagaimana dirinci bagian 5. Pemakai hilir tetap
wajib memeriksa bendera provenans pada entri sasaran sebelum menaikkan angkanya ke
dokumen terbit. Perintah ukur dan cetakan alat ditempel di bagian ini; checker
`work/f7p14_check.py` memverifikasi dua arah (setiap berkas di disk terdaftar, setiap
jalur yang terdaftar ada di disk) dan menguji ketujuh contoh sitasi jalan terhadap
berkas sasaran. Perintah dijalankan dari akar kontrak
`docs/2026-10-04-datum-manual/` pada 5 Oktober 2026, dan cetakan di bawah adalah jalan
pra-sisip; jalan ulang pasca-sisip ada di berkas bukti `work/f7p14_check_out.txt` dan
identik kecuali ukuran `library/INDEKS.md` yang membesar karena blok cetakan ini
sendiri.

```
$ python work/f7p14_check.py   # exit 0
CHECK 1: PASS - inventaris dua arah | berkas_disk=49 terdaftar=46 belum_terdaftar=0 jalur_hantu=0 edge_tmp_dikecualikan=245
CHECK 2: PASS - direktori scratch terdaftar | edge_tmp=True render=True
CHECK 3: PASS - contoh sitasi jalan | uji=7 gagal=0
CHECK 4: PASS - skema ID D-TA-11 lengkap | hilang=0
CHECK 5: PASS - aturan penamaan DATUM 2.5 + D-TA-03 | seksi-2.5=True d-ta-03=True
CHECK 6: PASS - footprint A1/A2 nol | U+2014=0 U+00B7=0
CHECK 7: PASS - frontmatter + H1==title | fm=True h1_sama=True
CHECK 8: PASS - berkas nyata non-kosong | bytes=12651 baris=191
VERDICT: PASS
```

Cetakan kedua di bawah mengukur setiap path terdaftar dalam byte, dijalankan dari
akar kontrak dengan keluaran terurut nama. Baris nol byte pun tetap dicetak karena
keberadaan jalur lebih menentukan daripada isinya bagi indeks ini.

```
$ find library measurement research corpus understanding -type f ! -path "research/edge_tmp/*" -printf "%s %p\n" | sort -k2
63753 corpus/lajur1-datum-dokumen.md
31502 corpus/lajur2-workbook-dan-nyata.md
28259 corpus/lajur3-korpus-internal.md
17221 corpus/skeleton-sidecar.json
531 library/check_laporan.py
5959 library/il_class_sensus.json
2213824 library/il_dump.json
718 library/il_query.sh
2610 library/il_sensus.py
12651 library/INDEKS.md
39837 library/katalog-simbol.md
18012 library/LAPORAN-CAKUPAN.md
29773 library/pohon-pemilihan-chart.md
52117 library/registri-pola-diagram.md
5310 library/sweep_cakupan.py
0 library/sweep_out.txt
47318 measurement/01-instrumen-penegakan.md
12426 measurement/02-sensus-aturan.md
21921 measurement/03-register-perbaikan.md
144618 research/_ladder_table.md
20402 research/_part1.md
21239 research/_part2.md
40262 research/01-sensus-simbol.md
185872 research/02-tipologi-chart-diagram.md
16026 research/03-sintesis-dan-keputusan.md
5497 research/check_sensus.py
541 research/count_rounds.py
6091 research/probe_cdx_r2.py
5699 research/probe_ddg.py
2929 research/probe_final.py
30609 research/probe_ladder.csv
3525 research/probe_obp.py
3264 research/probe_r2.py
4808 research/probe_r2b.py
3784 research/probe_r2c.py
4518 research/probe_r2d.py
2718 research/probe_r2e.py
3847 research/probe_round23.py
6528 research/probe_ruang.py
153 research/r2b_out.log
470 research/r2d_out.log
4393 research/render/isa5_committee.json
5518 research/render/isa51_004951.json
1715 research/render/mil2525_004958.json
6584 research/render/netnotation_005007.json
284 research/render/nso_app06_full.json
2889 research/render_rung8.py
2449 research/render_rung8b.py
50714 understanding/01-penjelasan.md

total berkas = 
49
```

## 5. Konsumsi hiliran dan defect bawaan

Langkah 15 memetakan bab manual ke rentang SIM, CH, DIA, dan GAP melalui skema di atas;
langkah 17 mengutip entri pustaka alih-alih menyalin isinya; langkah 18 memakai register
GAP sebagai basis perbaikan; langkah 23 mempromosikan pustaka lewat librarian ke jalur
vault menuju wiki sehingga sitasi tetap resolve lintas sesi. Blokade kutipan yang sudah
divonis controller menempel pada skema ini dan tidak boleh dilanggar oleh pemakai hilir,
sekalipun anchor-nya resolve dengan benar. Rinciannya: kutipan IEEE C37.2 diblokir
(N-5), kutipan edisi ISO/IEC 42010:2022 diblokir (N-8), DOI waterfall berstatus PROV
(N-1), MIL-STD-2525E berstatus BASELINE-ONLY ber-flag, SIM-43 dan SIM-44 masih PROV
dengan jalur naik terbuka di Register Riset Terbuka, serta register DAT-139 menunggu
koreksi cacah isa dari controller.
