---
id: katalog-simbol-datman-1004
type: catatan
title: "Katalog Simbol Pustaka SIM-nn: merger baseline DATUM dan sensus eksternal"
status: active
sumber: "docs/2026-10-04-datum-manual/library/katalog-simbol.md (hulu: research/01-sensus-simbol.md + research/probe_ladder.csv pin sha16 2924434389982290 + baseline 000-GSP-STD-X-2026 RevA Tabel 6.5/6.6)"
halaman: 59 entri SIM; 32 URL terbit ber-register entity-match; VERIFIKASI-AKURASI per seksi 8
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, simbol, iec-60617, isa-5.1, mil-std-2525, iso-1219, iso-7010, house-legend, katalog, spk-002]
links: [docs/2026-10-04-datum-manual/library/katalog-simbol.md, docs/2026-10-04-datum-manual/research/probe_ladder.csv]
penulis: gsp-document-writer
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_08c4025e
pin_sha16_artefak: 53e3aa90aab7818c
catatan_keputusan: "dipromosikan: DATMANUAL-1004 P23: checker hulu diulang segar PASS; P22 verifier independen SALAH-TARGET=0 33/33; non-sensitif non-dosir"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/katalog-simbol-datman-1004.md
---

# Katalog Simbol Pustaka SIM-nn: merger baseline DATUM dan sensus eksternal

MISI DATMANUAL-1004 | F6-P11 | Langkah 11 blueprint `identification/02_structured.md`.
Katalog ini adalah hasil merger dua populasi: 41 simbol baseline DATUM (Tabel 6.6
000-GSP-STD-X-2026 RevA, diverifikasi mesin `datum_symbols.py --list` run 3 Oktober 2026)
[R-1] dan 18 kelas simbol/notasi eksternal dari sensus riset 01 (21 kelas dikurangi
K-01, K-02, K-09 yang sudah terserap sebagai grup baseline, sesuai skema ID D-TA-11
yang melarang ganda lintas lajur) [R-2][R-4]. Total entri katalog adalah 59, bernomor
SIM-01 sampai SIM-59 tanpa lubang dan tanpa ganda. Putusan controller D-09/D-10/D-11
(contract.md 05-10) sudah diterapkan pada teks edisi grup ISA, MIL, dan garis.

## 1. Aturan baca katalog

### 1.1 Anatomi entri

Setiap baris memuat sembilan field beban-rilis sesuai kontrak langkah 11: id SIM-nn,
id simbol pustaka, nama Indonesia, nama Inggris, makna, standar beserta edisi dan
status, tanggal verifikasi, dialek, sumber primer tertaut (hyperlink aktif), mark
verifikasi, dan larangan-pakai [R-4]. Field kosong ditulis eksplisit, bukan dibiarkan
kosong: aturan SPK-002 butir 3 memilih kosong daripada salah [R-6]. Kolom
larangan-pakai bukan hiasan: ia menormakan klaim kemampuan yang melekat pada bentuk
simbol, sehingga pembaca gambar bisa mengaudit maksud pemasang.

### 1.2 Mark verifikasi (label teks, bukan glif)

| Mark | Arti |
|------|------|
| TERUKUR | Fetch langsung 200 dengan entity-match 1 pada register `research/probe_ladder.csv`, akun 2026-10-05 [R-2] |
| PROV | Judul/abstrak dari cuplikan mesin pencari atau listing pihak ketiga; respons tautan primer 403/anti-bot pada giliran ukur [R-2] |
| BASELINE-ONLY | Edisi dikutip dari Tabel 6.5 internal; konfirmasi eksternal belum mendarat (register negatif dibukukan) [R-1][R-2] |
| HOUSE-LEGEND | Tidak ada standar; legenda rumah GSP dengan kewajiban publikasi legenda di lembar yang sama (cek 34) [R-1] |

Glif peran internal diganti label teks mengikuti GUIDELINE 2026-10-03 par.4, dicatat
riset 01 sebagai D-5 [R-2]. Pemakai katalog wajib menyalin predikat apa adanya ke
figur hilir: menaikkan PROV menjadi TERUKUR tanpa akun register baru adalah cacat
akurasi, dan menurunkan TERUKUR tanpa dasar juga dilarang. Predikat bukan hiasan
tabel, melainkan klaim tentang bukti yang ada di balik setiap baris.

### 1.3 Tanggal verifikasi

Kolom Verif memakai dua lapis tanggal: verifikasi internal skill DATUM 2026-08-02
(Tabel 6.5 000) [R-1] dan verifikasi lapangan eksternal 2026-10-05 WIB (register
per akun `probe_ladder.csv`) [R-2]. Edisi regulasi wajib diperiksa ulang tahunan dan
diverifikasi lagi sebelum dikutip ke klien (DAT-138) [R-5]. Tanggal pada sel katalog
ini adalah tanggal ukur, bukan tanggal salin.

## 2. Grup IEC - simbol elektrik dan daya (SIM-01 sampai SIM-16)

Standar grup: IEC 60617 DB, database daring; judul resmi terfetch hari ini
"IEC 60617:2026 DB" sehingga tahun edisi 2026 kini sah dikutip (penutupan D-4) [R-2].
Dialek grup: empat perangkat switching berbagi satu konstruksi dan berbeda hanya oleh
tanda pada kontak tetap; ATS adalah kontak pindah plus fungsi kendali; UPS adalah blok
fungsi yang dinamai oleh designasinya (Tabel 79, DAT-140) [R-1][R-5].
Sumber primer grup: [IEC 60617:2026 DB, webstore IEC](https://webstore.iec.ch/en/publication/2723)
(TERUKUR, entity-match 1, 2026-10-05 00:38:49; CDX 3 snapshot) [R-2].

| SIM | id simbol | Nama (ID) | Nama (EN) | Makna | Standar+edisi (status) | Verif | Dialek | Sumber primer | Mark | Larangan-pakai |
|-----|-----------|-----------|-----------|-------|------------------------|-------|--------|---------------|------|----------------|
| SIM-01 | iec:breaker | Pemutus daya | circuit breaker | Circuit-breaker; tanda silang pada kontak tetap | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Tanda silang adalah klaim kemampuan memutus arus hubung singkat; jangan dipakai untuk perangkat tanpa kemampuan itu |
| SIM-02 | iec:disconnector | Pemisah | disconnector | Isolasi tanpa kemampuan memutus arus gangguan | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Disconnector bukan breaker: menggambarnya sebagai pemutus mengklaim pemutusan hubung singkat yang tidak ada (Tabel 79) |
| SIM-03 | iec:contactor | Kontaktor | contactor | Kontak tertutup oleh kumparan | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bukan alat isolasi: kontak dapat lepas saat kehilangan kumparan |
| SIM-04 | iec:switch | Sakelar | switch, general | Sakelar umum tanpa klaim kemampuan khusus | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bila jenis perangkat diketahui, pakai simbol spesifik; jangan berhenti di bentuk umum |
| SIM-05 | iec:changeover | Kontak pindah | changeover contact | Kontak pindah; cara ATS digambar | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | ATS = kontak pindah PLUS fungsi kendali; kontak pindah saja bukan ATS (DAT-140) |
| SIM-06 | iec:fuse | Sekring | fuse, general | Pengaman lebur umum | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC switching | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bukan pengganti pemutus daya yang dapat ditutup ulang |
| SIM-07 | iec:generator | Generator | generator, general | Generator umum | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bentuk umum; varian jenis tanpa dasar standar = mengarang simbol (DAT-137) |
| SIM-08 | iec:motor | Motor | motor, general | Motor umum | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bentuk umum; varian jenis tanpa dasar standar = mengarang simbol (DAT-137) |
| SIM-09 | iec:transformer | Transformator | transformer, two windings | Transformator dua belitan | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Jumlah belitan pada gambar harus sama dengan perangkat nyata |
| SIM-10 | iec:ct | Trafo arus | current transformer | Transformator arus | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Bukan trafo tegangan; beda fungsi ukur = beda simbol |
| SIM-11 | iec:arrester | Penangkap surja | surge arrester | Pembatas tegangan lebih transien | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Jangan tertukar dengan simbol pembumian; fungsi berbeda |
| SIM-12 | iec:earth | Pembumian | earth, general | Pembumian umum | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Jenis pembumian (bersih, chassis, protektif) tidak boleh dikarang; pakai varian baku bila perlu |
| SIM-13 | iec:battery | Baterai | battery or cell | Baterai atau sel | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Jumlah sel pada gambar membawa arti; jangan asal gambar |
| SIM-14 | iec:lamp | Lampu | lamp, general | Lampu indikator umum | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Lampu indikator rangkaian, bukan titik penerangan pada gambar pencahayaan |
| SIM-15 | iec:busbar | Rel daya | busbar | Rel penghantar | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC umum | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Tebal garis mengikuti tata bahasa garis (SIM-42), bukan dekorasi |
| SIM-16 | iec:enclosure | Blok fungsi | functional block item | Item yang dinamai oleh designasinya: UPS, penyearah | IEC 60617:2026 DB (current) | 2026-08-02 internal; 2026-10-05 eksternal | IEC designasi | [webstore.iec.ch/2723](https://webstore.iec.ch/en/publication/2723) | TERUKUR | Jangan mengarang glif khusus UPS; blok fungsi dinamai designasi IEC 81346-1 (SIM-58) |

## 3. Grup ISA - simbol instrumen dan identifikasi P&ID (SIM-17 sampai SIM-28)

Standar grup: ANSI/ISA-5.1-2024. Halaman produk resmi terfetch 200 berjudul
"ANSI/ISA-5.1-2024, Instrumentation and Control - Symbols and Identification"
sehingga edisi berlaku 2024 menurut sumber primer; PUTUSAN controller D-09
(contract.md 05-10 01:45) mengadopsi 2024 di manual (truth di atas fidelity,
SPK-002 butir 1), klaim internal Tabel 6.5 "2022 supersedes 2009" dicatat sebagai
koreksi terbitan pada bab audit manual, bentuk/anatomi kontrak tidak berubah [R-1][R-2][R-7].
Dialek grup: gelembung adalah kode dua-sumbu, bentuk menyatakan fungsi dan garis
horizontal menyatakan lokasi; menghapus garis mengubah indikator ruang kendali menjadi
instrumen lapangan (Tabel 79) [R-1].
Batas hak cipta yang dihormati: katalog ini hanya sitasi identitas dan edisi, tidak
mereproduksi tabel simbol ISA (notice penerbit tercantum di register negatif riset 01) [R-2].
Sumber primer grup: [ANSI/ISA-5.1-2024, halaman produk ISA](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb)
(TERUKUR, entity-match 1, 2026-10-05 00:38:51; render 200 00:49:51) dan
[komite ISA5](https://www.isa.org/standards-and-publications/isa-standards/isa-standards-committees/isa5)
(TERUKUR, 00:50:40) [R-2].

| SIM | id simbol | Nama (ID) | Nama (EN) | Makna | Standar+edisi (status) | Verif | Dialek | Sumber primer | Mark | Larangan-pakai |
|-----|-----------|-----------|-----------|-------|------------------------|-------|--------|---------------|------|----------------|
| SIM-17 | isa:field | Instrumen lapangan | discrete instrument, field mounted | Instrumen diskret pasang lapangan | ANSI/ISA-5.1-2024 (TERUKUR; adopsi putusan D-09, baseline 2022 = koreksi terbitan) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Garis lokasi adalah klaim: jangan menambah/menghapus garis tanpa mengubah maksud pemasangan nyata |
| SIM-18 | isa:primary | Instrumen ruang kendali | primary location instrument | Lokasi utama, dapat diakses operator | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Menghapus garis horizontal mengubah klaim lokasi menjadi instrumen lapangan (Tabel 79) |
| SIM-19 | isa:auxiliary | Instrumen lokasi bantu | auxiliary location instrument | Lokasi bantu, dapat diakses operator | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Beda dari SIM-18 hanya pada kode lokasi; jangan ditukar |
| SIM-20 | isa:inaccessible | Instrumen tak terjangkau | behind-panel instrument | Terpasang di balik panel | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Klaim keteraksesan: jangan dipakai untuk instrumen yang sebenarnya bisa diakses operator |
| SIM-21 | isa:shared | Tampilan bersama | shared display or control | Tampilan atau kendali bersama | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Hanya untuk fungsi yang benar-benar berbagi antar-loop |
| SIM-22 | isa:shared_field | Tampilan bersama lapangan | shared display, field mounted | Tampilan bersama pasang lapangan | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Kombinasi berbagi plus lokasi: dua klaim sekaligus, uji keduanya |
| SIM-23 | isa:computer | Fungsi komputer | computer function | Fungsi komputer | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Jangan dipakai untuk PLC; ada simbol tersendiri (SIM-24) |
| SIM-24 | isa:plc | PLC | programmable logic control | Kendali logika terprogram | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Beda kelas perangkat dari fungsi komputer; jangan saling ganti |
| SIM-25 | isa:valve | Katup kendali | control valve body | Badan katup kendali | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Badan katup tanpa aktuator saja tidak lengkap untuk P&ID operasi |
| SIM-26 | isa:valve_diaphragm | Katup aktuator diafragma | valve with diaphragm actuator | Katup dengan aktuator diafragma | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Tipe aktuator harus sama dengan perangkat nyata; salah aktuator = salah spesifikasi pemeliharaan |
| SIM-27 | isa:valve_motor | Katup aktuator motor | valve with motor actuator | Katup dengan aktuator motor | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Sama seperti SIM-26: aktuator pada gambar adalah klaim perangkat keras |
| SIM-28 | isa:valve_solenoid | Katup aktuator solenoid | valve with solenoid actuator | Katup dengan aktuator solenoid | ANSI/ISA-5.1-2024 (adopsi D-09) | 2026-08-02 internal; 2026-10-05 eksternal | gelembung dua-sumbu | [isa.org produk 5.1-2024](https://www.isa.org/products/ansi-isa-5-1-2024-instrumentation-and-control-symb) | TERUKUR | Sama seperti SIM-26: aktuator pada gambar adalah klaim perangkat keras |

## 4. Grup rumah - legenda keamanan GSP (SIM-29 sampai SIM-35)

Standar grup: tidak ada standar yang dimiliki GSP untuk marka denah keamanan;
Tabel 6.5 menetapkan "none exists: GSP house legend" dengan kewajiban publikasi
legenda [R-1]. Seluruh entri grup ini berbendera HOUSE-LEGEND: setiap gambar yang
memakai marka `sec:` WAJIB mereplikasi legenda pada lembar yang sama (cek 34) dan
DILARANG mengutip IEC 62676 atau EN 50132 sebagai otoritas marka (Tabel 79) [R-1].
Untuk rambu keselamatan nyata (larangan/wajib/larangan), otoritas yang benar adalah
ISO 7010 (SIM-45), bukan legenda ini [R-2].
Sumber primer grup: baseline internal `datum_symbols.py --list` via Tabel 6.6
000 RevA (tanpa tautan eksternal karena memang tidak ada standar; bendera
HOUSE-LEGEND menutup kewajiban sumber per kontrak langkah 11) [R-1].

| SIM | id simbol | Nama (ID) | Nama (EN) | Makna | Standar+edisi (status) | Verif | Dialek | Sumber primer | Mark | Larangan-pakai |
|-----|-----------|-----------|-----------|-------|------------------------|-------|--------|---------------|------|----------------|
| SIM-29 | sec:camera | Kamera tetap | fixed camera with field-of-view cone | Kamera tetap dengan kerucut bidang pandang | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend, replikasi lembar sama (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Kerucut dipurunkan dari panjang fokus nyata, bukan sudut karangan; jangan klaim patuh IEC 62676/EN 50132 |
| SIM-30 | sec:ptz | Kamera PTZ | pan-tilt-zoom camera | Kamera geser-pilih-zoom | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Legenda wajib di lembar yang sama; bukan merek dagang tertentu |
| SIM-31 | sec:pir | Detektor PIR | passive infrared detector | Detektor inframerah pasif | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Jangan dipakai untuk detektor jenis lain (vibration/radar) |
| SIM-32 | sec:fence | Sensor pagar | fence sensor | Sensor pagar | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Menandai sensor, bukan pagar itu sendiri; baca bersama garis pagar |
| SIM-33 | sec:reader | Pembaca akses | access reader | Pembaca akses | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Satu marka untuk satu titik baca; jangan digabung dengan marka barier |
| SIM-34 | sec:barrier | Palang kendaraan | vehicle barrier | Palang kendaraan | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Beda dari gerbang fisik; marka ini mengklaim palang berkendali |
| SIM-35 | sec:mast | Tiang lampu, kamera | lighting or camera mast | Tiang penerangan atau kamera | tidak ada standar: legenda rumah GSP | 2026-08-02 internal | house legend (cek 34) | baseline internal Tabel 6.6 (HOUSE-LEGEND) | HOUSE-LEGEND | Fungsi tiang (lampu versus kamera) dinyatakan di label, bukan di bentuk marka |

## 5. Grup MIL - frame identitas symbology militer (SIM-36 sampai SIM-41)

Standar grup: MIL-STD-2525E. Klaim internal "E, 31 Dec 2022 supersedes D" TIDAK
terkonfirmasi eksternal pada giliran ukur 2026-10-05 (assist.dla.mil 404-shell,
quicksearch DNS-mati, everyspec 404, globalspec 403, jcs.mil 403; hanya arsip
2525D/2525C yang hidup). PUTUSAN controller D-09 menetapkan grup ini BASELINE-ONLY
ber-flag: tidak ada kutipan darinya yang boleh naik sebagai klaim eksternal
terverifikasi; re-check ber-akun dibuka sebagai register known-defect lampiran,
bukan penghalang rilis [R-1][R-2][R-7].
Dialek grup: identitas dibawa BENTUK frame, bukan warna; friend dan neutral hanya
beda aspek (mesin mengukur dalam milimeter); echelon adalah penguat di atas frame
(Tabel 79) [R-1].
Sumber primer grup (arsip hidup, bukan edisi E): [Mil-STD-2525C PDF, arsip NASA
Worldwind](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) (HEAD 200,
entity-match 1, 2026-10-05 00:45:54) dan jejak CDX 3 snapshot ms_2525d.pdf jcs.mil
(2026-10-05 00:45:30) [R-2]. Suplemen non-primer: artikel Wikipedia Joint Military
Symbology (200, 00:39:23) dipakai sebagai pelengkap konsistensi bentuk, bukan otoritas
[SUPLEMEN] [R-2].

| SIM | id simbol | Nama (ID) | Nama (EN) | Makna | Standar+edisi (status) | Verif | Dialek | Sumber primer | Mark | Larangan-pakai |
|-----|-----------|-----------|-----------|-------|------------------------|-------|--------|---------------|------|----------------|
| SIM-36 | mil:friend | Kawan, darat | friend, land | Persegi panjang melebar | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) [SUPLEMEN Wikipedia NJMS](https://en.wikipedia.org/wiki/NATO_Joint_Military_Symbology) | BASELINE-ONLY | Jangan mewarnai friend/hostile sebagai pembeda: bentuk adalah klaimnya |
| SIM-37 | mil:hostile | Lawan, darat | hostile, land | Diamond, titik ke atas | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) | BASELINE-ONLY | Diamond adalah klaim permusuhan; jangan dipakai untuk netral |
| SIM-38 | mil:neutral | Netral, darat | neutral, land | Bujur sangkar | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) | BASELINE-ONLY | Hanya beda aspek dari friend: mesin mengukur milimeter, renderer dilarang menyederhanakan |
| SIM-39 | mil:unknown | Tak dikenal, darat | unknown, land | Quatrefoil | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) | BASELINE-ONLY | Quatrefoil mengklaim ketidaktahuan identitas; jangan jadi hiasan |
| SIM-40 | mil:friend_air | Kawan, udara | friend, air | Dome, terbuka di bawah | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) | BASELINE-ONLY | Domain udara punya frame sendiri; jangan campur frame darat dan udara dalam satu gambar saat satu dialek diberlakukan (cek 35) |
| SIM-41 | mil:hostile_air | Lawan, udara | hostile, air | Pointed arch, terbuka di bawah | MIL-STD-2525E (BASELINE-ONLY ber-flag, putusan D-09) | 2026-08-02 internal; arsip 2026-10-05 | frame bentuk bukan warna | [arsip 2525C NASA](https://worldwind.arc.nasa.gov/milstd2525c/Mil-STD-2525C.pdf) | BASELINE-ONLY | Sama seperti SIM-40: konsisten domain frame |

## 6. Grup eksternal - kelas pustaka simbol/notasi hasil sensus (SIM-42 sampai SIM-59)

Entri grup ini mengisi kelas yang KOSONG di baseline atau melengkapi pustaka
baseline; sumbernya 21 kelas sensus riset 01 dikurangi tiga kelas yang sudah naik
sebagai grup baseline (K-01 ke SIM-01..16, K-02 ke SIM-17..28, K-09 ke SIM-36..41)
sesuai larangan ganda D-TA-11 [R-2][R-4]. Predikat verifikasi mengikuti kolom
Verifikasi tabel sensus 01 seksi 2 [R-2]. Kolom larangan-pakai grup ini memuat
blokir aktif dari putusan controller (ASME, IEEE C37.2) sehingga pembaca tidak bisa
memakai entri tanpa melihat status verifikasinya.

| SIM | Kelas (K-nn) | Nama (ID) | Nama (EN) | Makna / isi kelas | Standar+edisi (status) | Verif | Dialek | Sumber primer | Mark | Larangan-pakai |
|-----|--------------|-----------|-----------|-------------------|------------------------|-------|--------|---------------|------|----------------|
| SIM-42 | K-04 | Tipe garis gambar teknik | basic line conventions | Tipe garis 01.1 tipis, 01.2 tebal, 02.1 putus, 04.1 gores-titik, 05.1 gores-dua-titik (Tabel 80) | ISO 128-2:2020 E1 (adopsi putusan D-09; entri katalog aktif, klaim internal "2022" = koreksi terbitan) | 2026-10-05 (judul terfetch penuh 01:05:11) | garis = tata bahasa, bukan dekorasi | [iso.org/standard/69129](https://www.iso.org/standard/69129.html) | TERUKUR | Tipe 05.1 khusus pekerjaan di luar lingkup kontrak; jangan pakai tipe garis karangan |
| SIM-43 | K-05 | Pen dimensi gambar | dimensioning conventions | Aturan penempatan dimensi pada gambar teknik | ISO 129-1:2018 E2 | 2026-10-05 (cuplikan iso.org 01:04; tautan 403 Cloudflare) | konvensi TC10 | [iso.org/standard/64007](https://www.iso.org/standard/64007.html) (PROV: 403 anti-bot, retry wayback kena 429) | PROV | Jangan dikutip sebagai TERUKUR sebelum retry arsip mendarat (sisa kerja kartu lanjutan) |
| SIM-44 | K-06 | Title block kepala gambar | title blocks and document headers | Isi minimum blok judul dokumen teknik | ISO 7200:2004 E2 | 2026-10-05 (cuplikan iso.org 00:53; tautan 403 Cloudflare) | kelengkapan kepala gambar | [iso.org/standard/35446](https://www.iso.org/standard/35446.html) (PROV: 403 anti-bot, retry wayback kena 429) | PROV | Sama seperti SIM-43: predikat PROV melekat di sel, tidak boleh naik jadi TERUKUR |
| SIM-45 | K-07 | Rambu keselamatan terdaftar | registered safety signs | Rambu larangan/wajib/peringatan berdaftar | ISO 7010:2019 | 2026-10-05 (200 entity-match 1, 00:39:00) | rambu nyata, bukan marka denah | [iso.org/standard/72424](https://www.iso.org/standard/72424.html) | TERUKUR | Marka `sec:` rumah (SIM-29..35) TIDAK boleh diklaim patuh ISO 7010; sebaliknya rambu keselamatan nyata wajib merujuk ISO 7010 |
| SIM-46 | K-08 | Simbol pada peralatan | graphical symbols for use on equipment | Kumpulan glif pada peralatan untuk menginstruksi operasi (mis. indikator panel) | ISO 7000:2019 | 2026-10-05 (200 entity-match 1, 01:05:14) | glif peralatan | [iso.org/standard/78717](https://www.iso.org/standard/78717.html) | TERUKUR | Kandidat formalisasi glif panel untuk `sec:`; selama belum diformalkan, status `sec:` tetap HOUSE-LEGEND |
| SIM-47 | K-21 | Registri rambu keselamatan CN | Chinese national safety sign registry | Jembatan identifikasi nama standar GB (GB 2894 dsb.) | GB 2894 dsb. (entri registri; identifier terbit DITAHAN) | 2026-10-05 (registri openstd 200 judul generik, entity-match 0) | jembatan CER-001 R1, bukan tautan terbit | KOSONG (portal registri pemerintah bukan tautan terbit per SPK-002 butir 10; CER-001 R1 hanya jembatan nama) | PROV | Identifier CN tidak boleh terbit dari portal registri; wajib naik lewat tangga CER-001 (R0 situs resmi penyelenggara atau R2 pencarian Mandarin) |
| SIM-48 | K-03 | Simbol hidrolik/pneumatik | fluid power graphical symbols | Simbol grafis sistem fluida dan diagram sirkuit | ISO 1219-1:2012 + Amd 1:2016 | 2026-10-05 (200 entity-match 1, 00:38:55 dan 00:38:56) | kelas baru, baseline KOSONG terverifikasi | [iso.org/standard/60184](https://www.iso.org/standard/60184.html), [Amd 1:2016](https://www.iso.org/standard/66287.html) | TERUKUR | Baseline tidak punya pustaka hidrolik/pneumatik: sebelum mesin simbol mendukung, gambar memakai blok sederhana WAJIB menyatakan itu terang-terangan (DAT-137) |
| SIM-49 | K-10 | Administrasi identifikasi jaringan | telecommunications administration | Notasi administrasi identitas jaringan/telekomunikasi (label ruang, jalur, sambungan) | ANSI/TIA-606-D | 2026-10-05 (listing akurat 403 dgn token judul; halaman standar TIA render 200 DOM 00:50:07) | keluarga topology Tabel 6.2 | [tiaonline.org/standards](https://www.tiaonline.org/standards/) ; [listing TIA-606-D](https://store.accuristech.com/standards/tia-ansi-tia-606-d?product_id=2594255) (PROV: 403) | PROV | Edisi D dikutip dengan predikat PROV; path lama tiaonline 404 terdokumentasi di register negatif |
| SIM-50 | K-11 | Ikon arsitektur cloud vendor | cloud architecture icon sets | Etalase ikon topologi modern AWS, Azure, Google Cloud | berjalan terus (etalase hidup vendor; BUKAN standar SDO) | 2026-10-05 (ketiganya 200 entity-match 1, 00:40:04 dan 00:51:36-38) | ikon vendor, versi etalase | [AWS icons](https://aws.amazon.com/architecture/icons/), [Azure icons](https://learn.microsoft.com/en-us/azure/architecture/icons/), [Google Cloud icons](https://cloud.google.com/icons) | TERUKUR | Bukan standar SDO: jangan mengklaim konformansi standar; ikon vendor berubah tanpa notifikasi, cantumkan tanggal unduh saat dipakai |
| SIM-51 | K-12 | Notasi proses bisnis dan flowchart | business process notation | BPMN 2.0.2 untuk pool/lane; ISO 5807:1985 untuk bentuk simpul flowchart (stadium, diamond, parallelogram, hexagon pada Tabel 6.3) | BPMN 2.0.2 (OMG); ISO 5807:1985 (masih terbit) | 2026-10-05 (omg 200 00:39:40; iso 11955 200 00:47:16) | bentuk simpul bersumber notasi | [omg.org/spec/BPMN](https://www.omg.org/spec/BPMN/), [iso.org/standard/11955](https://www.iso.org/standard/11955.html) | TERUKUR | Bentuk simpul hanya sah dalam notasi yang dinyatakan di judul gambar; campur BPMN dan flowchart klasik dalam satu gambar melanggar satu-dialek (cek 35) |
| SIM-52 | K-13 | Notasi struktur dan interaksi sistem | UML and SysML | UML 2.5.1 (sequence, component doubled); SysML 2.0 untuk rekayasa sistem | UML 2.5.1; SysML 2.0 (OMG) | 2026-10-05 (omg 200 00:39:41; SysML 2.0 200 00:51:33) | simpul doubled bersumber UML component | [omg.org/spec/UML](https://www.omg.org/spec/UML/), [omg.org/spec/SysML](https://www.omg.org/spec/SysML/) | TERUKUR | Versi spesifikasi wajib disebut di caption; sintaks antar-versi OMG berbeda |
| SIM-53 | K-14 | Arsitektur enterprise | enterprise architecture modeling | Bahasa pemodelan ArchiMate (keluarga layered) | ArchiMate (halaman overview resmi hidup; versi spesifik tidak dikutip karena tidak diukur hari ini) | 2026-10-05 (200 entity-match 1, 00:40:07 dan 00:51:35) | keluarga layered | [opengroup.org archimate-overview](https://www.opengroup.org/archimate-forum/archimate-overview) | TERUKUR | Jangan mengutip nomor versi spesifikasi dari ingatan; edisi hanya dari halaman resmi saat diukur |
| SIM-54 | K-15 | Chart kendali statistik | Shewhart control charts | Tipologi chart kendali (payung perluasan keluarga threshold baseline) | ISO 7870-2:2023 + NIST Engineering Handbook 6.3 | 2026-10-05 (iso 78859 200 00:47:13; nist 200 00:39:45) | aturan sinyal wajib dinyatakan (mis. 3-sigma) | [iso.org/standard/78859](https://www.iso.org/standard/78859.html), [NIST e-Handbook 6.3.2.1](https://www.itl.nist.gov/div898/handbook/pmc/section3/pmc321.htm) | TERUKUR | Chart tanpa aturan sinyal dan n sampel = klaim stabilitas tanpa bukti (AP daun A.3) |
| SIM-55 | K-16 | Diagram pabrik kimia dan petrokimia | diagrams for the chemical industry | Spesifikasi diagram proses lintas bahasa, pelengkap P&ID ISA | ISO 10628-1:2014 | 2026-10-05 (200 entity-match 1, 00:47:14) | P&ID lintas-bahasa | [iso.org/standard/51840](https://www.iso.org/standard/51840.html) | TERUKUR | Untuk figur proses kimia, pasangan ISA-5.1 (SIM-17..28) dan desainasi (SIM-58) ditarik bersamaan |
| SIM-56 | K-17 | Toleransi geometris GD&T | geometrical tolerancing | Simbol toleransi bentuk, orientasi, posisi | ISO 1101:2017 | 2026-10-05 (200 entity-match 1, 00:47:17) | kelas baru, tidak ada baseline | [iso.org/standard/66777](https://www.iso.org/standard/66777.html) | TERUKUR | ASME Y14.5 jangan dikutip dulu: path resmi 404 dan CDX 0 snapshot (register negatif), tunggu jalur katalog baru |
| SIM-57 | K-18 | Simbol las | welding symbolic representation | Representasi simbolis sambungan las pada gambar | ISO 2553:2019 | 2026-10-05 (200 entity-match 1, 00:47:18) | kelas baru, tidak ada baseline | [iso.org/standard/72740](https://www.iso.org/standard/72740.html) | TERUKUR | Kelas struktural-mekanik: hanya dipakai pada gambar fabrikasi, bukan diagram sistem |
| SIM-58 | K-19 | Desainasi referensi dan dokumentasi elektrik | reference designation and documentation | Imbuhan = fungsi, + lokasi, - produk, : terminal (contoh =UPK+PP-Q1); basis join key BoQ dan uji terima | IEC 81346-1:2022 Ed.2.0; IEC 60445:2021; IEC 61082-1:2014 | 2026-10-05 (ketiganya webstore 200 entity-match 1, 00:43:07-19) | designasi = kunci ketertelusuran | [IEC 81346-1:2022](https://webstore.iec.ch/en/publication/64021), [IEC 60445:2021](https://webstore.iec.ch/en/publication/66712), [IEC 61082-1:2014](https://webstore.iec.ch/en/publication/4469) | TERUKUR | Designasi yang sama wajib muncul di baris BoQ dan uji terima; designasi bebas = simbol yatim tanpa harga dan kriteria lulus (DAT-145) |
| SIM-59 | K-20 | Simbol instalasi alarm kebakaran | fire alarm signalling | Simbol perangkat deteksi dan signalling instalasi alarm | NFPA 72 (berjalan; edisi spesifik tidak dikutip dari ingatan) + TIA 72-25-5 terbit | 2026-10-05 (nfpa 200 entity-match 1, 00:40:05; PDF TIA 200 tanpa entity-match, suplemen) | kelas baru, relevan figur deteksi | [nfpa.org/codes-and-standards/nfpa-72](https://www.nfpa.org/codes-and-standards/nfpa-72-standard-development/72) ; [TIA_72_25_5.pdf](https://docinfofiles.nfpa.org/files/AboutTheCodes/72/TIA_72_25_5.pdf) [SUPLEMEN: entity-match 0] | TERUKUR | Nomor edisi NFPA hanya dari halaman resmi saat diukur; reproduksi tabel simbol NFPA dibatasi hak cipta, sitasi identitas saja |

## 7. Rekonsiliasi cacah (parsial = total)

Rekonsiliasi dihitung deterministik oleh `work/f6p11_verify.py` pada giliran ini;
angka di bawah adalah cetakan alat, bukan ingatan (SPK-002 butir 9) [R-6]. Empat
prefiks baseline dijumlahkan lalu ditambah kelas eksternal tersisa, dan hasilnya
diuji sama dengan cacah baris katalog (CHECK 8). Bila salah satu komponen berubah,
CHECK 8 akan FAIL sebelum katalog sempat dipromosikan.

| Komponen | Sumber | Cacah |
|----------|--------|-------|
| Baseline iec: | hitungan baris prefiks `iec:` pada Tabel 6.6 berkas sumber 000 | 16 |
| Baseline isa: | hitungan baris prefiks `isa:` pada Tabel 6.6 | 12 |
| Baseline sec: | hitungan baris prefiks `sec:` pada Tabel 6.6 | 7 |
| Baseline mil: | hitungan baris prefiks `mil:` pada Tabel 6.6 | 6 |
| Subtotal baseline | jumlah empat prefiks | 41 |
| Kelas eksternal baru | 21 kelas sensus 01 dikurangi 3 kelas terserap grup baseline (K-01, K-02, K-09) | 18 |
| TOTAL entri SIM | subtotal baseline + eksternal | 59 |

Temuan rekonsiliasi (dibukukan, tidak mengubah baseline): register lajur-1 DAT-139
menyebut rincian "(iec 16, isa 13, sec 7, mil 6)" yang berjumlah 42, sedangkan
hitungan baris Tabel 6.6 pada berkas sumber menghasilkan 16+12+7+6 = 41 dan judul
tabel juga menyatakan 41 [R-1][R-5]. Selisih ada di prefiks `isa:` (klaim 13 vs
terukur 12). Sumber kebenaran yang dipakai katalog ini: baris nyata Tabel 6.6
(cetakan parser). Register DAT-139 diusulkan dikoreksi ke "isa 12" pada kartu
hilir; putusan mutasi baseline tetap hak controller.

Perintah ukur dan keluarannya dibukukan di `work/f6p11_verify_out.txt` (CHECK 1-8 +
VERDICT), dijalankan 2026-10-05 oleh pekerja sebagai short check; verifikasi penuh
ada di jalur verifier orkestrasi. Skrip yang sama siap dijalankan ulang oleh verifier
tanpa modifikasi karena hanya membaca berkas sumber dan register. Selisih rincian
DAT-139 di atas tidak mengubah angka tabel ini karena parser menghitung baris nyata,
bukan mengutip prosa register.

## 8. VERIFIKASI-AKURASI (SPK-002 butir 5, gerbang rilis 100%)

Uji deterministik seluruh populasi field beban-rilis katalog ini terhadap register
`research/probe_ladder.csv` (bukan sampling): setiap URL terbit harus terdaftar di
register dengan entity-match 1 atau membawa label PROV/SUPLEMEN eksplisit di selnya,
dan setiap bendera harus punya dasar baris sumber. Hasil per gerbang dicetak alat
pada tabel berikut. Gerbang ini meniru prosedur riset 01 Lampiran B agar dua artefak
se-misi bisa dibandingkan verifier dengan alat ukur yang sama.

| Gerbang | Populasi | Hasil cetakan alat |
|---------|----------|--------------------|
| Setiap URL terbit ada di register dengan entity_match=1 ATAU berlabel PROV/SUPLEMEN eksplisit di sel | seluruh URL unik dalam katalog | lihat CHECK 5 `work/f6p11_verify_out.txt` |
| Tidak ada register-negatif yang naik jadi tautan terbit | identifier GB CN, ASME Y14.5, IEEE C37.2 | KOSONG-terdaftar = 0 pelanggaran (identifier GB sengaja KOSONG per CER-001; ASME dan IEEE dilarang dikutip lewat larangan-pakai SIM-56 dan catatan cabang B.4 riset 03) |
| SALAH-TARGET terbit | seluruh tautan | 0 |
| Entri tanpa standar eksplisit berbendera house-legend | 7 entri `sec:` | 7/7 HOUSE-LEGEND dengan kewajiban publikasi legenda (cek 34) |
| Id SIM unik, tanpa ganda lintas lajur (D-TA-11) | 59 id | lihat CHECK 7 |
| Jejak tipografi A1/A2 nol | berkas ini | U+2014 = 0, U+00B7 = 0 (lihat CHECK 6 + laporan scanner) |

Predikat per entri mengikuti register akun riset 01: 16 sumber TERUKUR, 4 PROV
(SIM-43, SIM-44, SIM-49 sebagian, SIM-47), 1 BASELINE-ONLY (grup MIL), 7 HOUSE-LEGEND
(grup rumah), sisanya kelas vendor/arsip dengan predikat terukur per akun [R-2].
Tidak ada identifier register-negatif yang naik menjadi tautan terbit, sesuai
gerbang SALAH-TARGET = 0. Gerbang ini diuji pada SELURUH populasi 32 URL unik
katalog, bukan sampling, dengan parser CSV register yang sama seperti dicetak
di CHECK 5 keluaran alat.

## 9. Register Riset Terbuka yang memengaruhi katalog

Sisa kerja terbuka di bawah DITERUSKAN sebagai Register Riset Terbuka lampiran manual
sesuai PUTUSAN controller D-10 (contract.md): bukan vonis buntu, kutipan dari daun
yang belum terverifikasi diblokir sampai verifikasi mendarat [R-7]. Estimasi iterasi
ikut terbawa agar kartu lanjutan bisa langsung dieksekusi. Butir yang menyentuh
katalog ini bernomor lima, dan semuanya punya jalur aksi konkret, bukan spekulasi.

1. Retry wayback/CDX untuk iso.org/standard/64007 dan /35446 menaikkan SIM-43/SIM-44 dari PROV ke TERUKUR (<=6 iterasi, jeda 429).
2. Jalur ber-akun NSO (APP-6) dan assist.dla.mil (MIL-STD-2525E) menutup re-check grup MIL SIM-36..41 (<=10 iterasi; known-defect register per D-09).
3. ASME Y14.5 path katalog baru (<=8 iterasi) sebelum SIM-56 boleh menyebut padanan ASME; kutipan ASME tetap diblokir sampai terverifikasi.
4. ISO 14617 part lain lewat beranda TC 10 (<=8 iterasi); part 1:2005 sudah punya akun 200 entity-match 1 di register (`iso.org/standard/41838.html`) sebagai calon entri tambahan.
5. IEEE C37.2 (N-5) KOSONG: kutipan diblokir sampai terverifikasi (D-10; riset 03 daun B.4) sehingga grup SLD tetap hanya menarik IEC 60617 (SIM-01..16).

Putusan edisi D-1 dan D-2 tidak lagi terbuka: D-09 sudah mengadopsi ANSI/ISA-5.1-2024
dan ISO 128-2:2020 E1 sebagai teks final kolom standar SIM-17..28 dan SIM-42 [R-7],
sehingga koreksi tersebut tinggal dinormakan pada bab audit manual, bukan di katalog
ini. Butir 1 sampai 5 tetap terbuka dan menjadi bahan kartu lanjutan yang dibuat
orkestrator dari register ini. Setelah butir-butir itu mendarat, hanya kolom Verif
dan Mark yang berubah; struktur katalog tidak perlu disusun ulang.

## Referensi

- R-1: Berkas sumber baseline internal, `C:/Users/TRIAL/workspace/Datum House Style Standard/DATUM_House_Style_Explained_000-GSP-STD-X-2026_RevA.docx.md` baris 743-826 (bab 6.6, Tabel 6.5, Tabel 6.6, Tabel 79, Tabel 80), dibaca langsung 2026-10-05.
- R-2: `docs/2026-10-04-datum-manual/research/01-sensus-simbol.md` (kartu t_77bbeb7d, gsp-data-collector) beserta register `research/probe_ladder.csv` 181 baris.
- R-3: `docs/2026-10-04-datum-manual/research/03-sintesis-dan-keputusan.md` (kartu t_12cf065d, cabang C daun C.1-C.13, apparatus AP-1..AP-10).
- R-4: `docs/2026-10-04-datum-manual/identification/02_structured.md` (KD-25 kontrak desain pustaka simbol; D-TA-11 skema ID; langkah 11 tabel breakdown).
- R-5: `docs/2026-10-04-datum-manual/corpus/lajur1-datum-dokumen.md` (DAT-137, DAT-138, DAT-139, DAT-140, DAT-144, DAT-145).
- R-6: STANDAR-PROSEDUR-AKURASI-DATA SPK-002-GSP-IX-2026, `workspace/docs/2026-09-04-data-accuracy-standard/STANDAR-PROSEDUR-AKURASI-DATA-SPK-002.md`.
- R-7: `docs/2026-10-04-datum-manual/contract.md` putusan D-09/D-10/D-11 (05-10), diterima operator via notifikasi kartu 2026-10-05.
