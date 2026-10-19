---
id: electrical-korpus-ekas-0923
type: catatan
title: Korpus ELECTRICAL EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-24
catatan_verifikasi: "VERDICT: terverifikasi || ALASAN: Objek memenuhi 7 dimensi verifikasi custodian: (1) frontmatter valid YAML, title==H1, 16 tags beku, field wajib lengkap; (2) provenans: 17/20 cross-check angka ke rak nyata PASS (>=10 minimal), marker [R-n,sumber,hal] konsisten; (3) kesetiaan hulu: K-1..K-10 predikat/register/gap/R1=0/R4=0/offset ATS+19/N-13 verbatim sesuai studi & rak; (4) anatomi 8 bagian lengkap per skema G-1; (5) BATAS Bagian 8 memuat N-11 apa adanya (rantai terkuat rak R2 NETA+catatan ATS!=MTS, GAP-001/008/014, peringatan usia Gill 18th, known-defect D3-FIXx/D4-FIXx tercatat); (6) konsistensi internal: nomor baris cocok disk pasca D3+D4, tidak ada bentuk lama dihapus diam-diam, kontradiksi ditandai; (7) kebersihan: non-ASCII=0, jalur rak nyata terverifikasi. REKOMENDASI: promosikan ke wiki via librarian."
sumber: "docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md (hulu: 9 berkas ekas/ wajib dibaca penuh + 10 pendukung, terdaftar di Bagian 1 objek)"
halaman: "marker [R-n, sumber, hal] per butir di body: PDF 223, 241, 246 (ANSI/NETA ATS-2017 - Tabel 100.1, 100.14, 100.18; offset cetak +19 teruji 3/3); PDF 142, 144, 145, 659, 928 (Gill - DAR, PI, empat metode, batas tegangan uji, Apendiks A)"
tanggal_akses: 2026-09-24
kelas_bukti: sintesis
sensitif: tidak
perkara: nwskill-0923
tags: [electrical, kelistrikan, isolasi, tahanan-isolasi, pi, dar, polarization-index, dielectric-absorption-ratio, neta-ats, ats-2017, tabel-100.1, tegangan-uji-dc, koreksi-suhu, uji-terima, mts-absen, megger]
links: [ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL, docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, ekas/05_DOMAIN-KNOWLEDGE/THERMAL, ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP, ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING, ekas/05_DOMAIN-KNOWLEDGE/RCM]
defek-terkait: register kontradiksi NWSKILL-0923 K-1..K-10 di docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md Bagian 5; anotasi known-defect hanya-tambah D3-FIXx lalu D4-FIXx terpasang 2026-09-24 di delapan berkas rak (jalur lengkap Bagian 1.1a dan 5 objek ini); K-1 berpredikat CALON DEFECT SUBSTANTIF menunggu putusan manusia, K-3 menunggu adjudikasi PDF 246
penulis: gsp-power-specialist
diajukan: 2026-09-24
domain: ELECTRICAL
created: 2026-09-24
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-24
dipromosikan-ke: catatans/electrical-korpus-ekas-0923.md
catatan_keputusan: "dipromosikan: NWSKILL-0923 D3-L2: gerbang format librarian 10/10 PASS (validator mandiri + red-green), verdict custodian terlampir di catatan_verifikasi, non-sensitif non-dosir; known-defect K-1..K-10 + anotasi D3-FIXx/D4-FIXx tercatat, semua vonis BELUM TERKONFIRMASI terhadap PDF primer"
---

# Korpus ELECTRICAL EKAS - peta, rumus, ambang, dan batas pengetahuan (NWSKILL-0923)

Objek master misi NWSKILL-0923 (id `electrical-korpus-ekas-0923`, type catatan, domain
ELECTRICAL = D3). Muatan = peta rak + rumus + angka acuan + kerangka hitung + ambang terima +
register kontradiksi + celah resmi + batas kemampuan, dalam satu berkas (granularitas SATU
objek master per domain sesuai skema beku G-1 seksi 1).

Provenans: body ini disalin terpadatkan dari SATU sumber,
`docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md` (studi
t_1711b38f status complete, 738 baris, ekstraksi read-only dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) oleh
gsp-power-specialist pada 2026-09-24). Tidak ada pembacaan ulang korpus untuk angka BARU pada
giliran ini; bacaan langsung rak di giliran L1 adalah (a) verifikasi ulang berkas-berkas yang
ditambal D3-FIXx dan D4-FIXx sesudah studi menutup, dan (b) reproduksi aritmetika angka rak
oleh skrip `docs/2026-09-23-nws-knowledge-register/scripts/measure_d3_anchors.py` pada giliran
ini (hasil di Bagian 2.3). Nomor baris di objek ini memakai kondisi DISK TERKINI - pasca DUA
gelombang tambalan; peta pergeseran dua-gelombang ada di Bagian 1.1a.

Kelas bukti objek: sintesis - kekuatan utama R2 (ANSI/NETA ATS-2017 lewat resume) dipasangkan
dengan R3 (Gill 2008 lewat resume); R1 nol dan R4 nol global. Kelas bukti berbeda dicampur
dalam satu berkas; pemisahannya ditegakkan lewat penanda `[R-n, sumber, hal]` per butir dan
blok BATAS PENGETAHUAN di Bagian 8. Yang tidak ada di rak dinyatakan "tidak ada di rak".

## Konvensi tulis objek ini (dinyatakan di depan)

1. **Marker bentuk koma** `[R-n, sumber, hal]` sesuai konvensi D-18 (`pustaka-teknis`). Di
   dalam kutipan literal dari lapis teks rak, penanda rak tampil apa adanya (mis. `[R2]` tanpa
   nama halaman seperti ditulis `RANTAI-JAMINAN.md:68`) - menormalkannya akan merusak kutipan
   verbatim; marker lengkapnya ada di baris penjelas di luar kutipan.
2. **Nol glif non-ASCII** di seluruh berkas (target skema G-1 seksi 10; preseden berkas
   saudari `lib/networking-object-body.md` = 0 non-ASCII). Karena itu glif ditulis ulang TANPA
   mengubah nilai: `M ohm` untuk satuan tahanan isolasi, `derajat C` untuk satuan suhu,
   `delta-T` untuk simbol delta-T, `<=` / `>=` / `<` / `>` untuk operator, `-` untuk sel kosong
   tabel, `1-3` (minus biasa) untuk rentang yang di rak memakai en dash. **ANGKA, SATUAN, dan
   NAMA HALAMAN disalin PERSIS**, desimal koma Indonesia dipertahankan. Substitusi HANYA pada
   glif, tidak pernah pada nilai.
3. **Penanda asal angka** mengikuti wajib kartu pengetahuan (`REF-ELC-001.md:32-33`,
   `REF-ELC-002.md:38-39`): `SOURCE-DERIVED` (tertulis di rak), `PROJECT-DERIVED` (hasil hitung
   dari masukan rak), `OEM-DERIVED` (lembar data pabrikan), `ASSUMPTION`.

## BATAS DOMAIN (N-13) - kalimat wajib, dikutip verbatim dari studi

> **BATAS DOMAIN (N-13, kalimat wajib):** yang terdaftar di domain ELECTRICAL adalah **uji
> instalasi dan peralatan listrik** (ANSI/NETA ATS-2017 untuk ambang uji terima, Gill untuk metode
> dan rasio) - **BUKAN** UPS, baterai, atau genset (domain POWER-BACKUP / Rantai C), dan **BUKAN**
> proteksi petir maupun pembumian (domain GROUNDING-LIGHTNING / Rantai D).

Dasar kalimat: `research/electrical-korpus-detail.md:590-593` (Bagian 6 studi), dengan
penegasan depan di `:98-103`: label awam "Electrical" lebih luas daripada domain rak ini
(`identification/01_translated.md:62` butir K-6, `:142` butir F-5). Pembeda besaran yang wajib
ikut: **tahanan isolasi (M ohm) BUKAN resistansi pembumian (ohm)** - dua besaran berbeda,
sering tertukar (`ekas/01_GOVERNANCE/AUTHORITY-STATUS.md:30`;
`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md:159-161`).

Uji keberadaan batas ini di rak (ukur giliran L1, skrip): kata `interval`, `torque`, `torsi`,
`petir` = **0 kemunculan** di seluruh [`ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/). Kata `UPS` (3x),
`baterai` (1x), `genset` (2x) muncul HANYA di tiga konteks non-muatan: baris "pendamping di
rak" (`R3 - Gill:175` menyebut laci `R3/UPS/` dan `R3/GENSET/`), contoh beban non-linier pada
kualitas daya (`R3 - Gill:78` - UPS disebut sebagai BEBAN yang mengganggu instalasi, bukan
sebagai lingkup uji), dan anotasi K-9 milik tambalan D3-FIXx (`RANTAI-JAMINAN.md:100`). Nol di
antaranya memasok angka atau ambang catu daya/pembumian untuk domain ini.

---

## Bagian 1 - Peta isi

Path memakai NAMA FOLDER NYATA di disk (kontrak jalur G-1 seksi 6). Label katalog berbentuk
`R2/ANSI-NETA/` dan `R3/ELECTRICAL/` adalah label laci, BUKAN path; padanan nyatanya dicantumkan
(butir K-10). Uji keberadaan = baca langsung/ls, bukan glob.

### 1.1 Lapis domain [`ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/) (3 berkas)

| Berkas | Peran | Tingkat R | Ukuran nyata (pasca-tambalan) |
|---|---|---|---|
| `RANTAI-JAMINAN.md` | Rantai E, urutan kerja mata 1-5 uji instalasi listrik; SATU-SATUNYA tempat contoh terhitung domain ini | peta pengetahuan | 125 baris, 8.720 B (studi mengukur 113 baris / 4.703 B sebelum tambalan) |
| `R2 - ANSI-NETA ATS-2017.md` | Resume standar uji terima; penyedia ANGKA AMBANG | R2 | 150 baris, 6.436 B (tidak ditambal; mtime 2026-08-24) |
| `R3 - Electrical Power Equipment Maintenance and Testing.md` | Resume buku Gill; penyedia METODE dan RASIO | R3 | 185 baris, 8.316 B (studi mengukur 182 baris / 7.588 B sebelum tambalan) |

### 1.1a Pergeseran baris akibat tambalan known-defect DUA GELOMBANG (2026-09-24, keduanya hanya-tambah)

Studi D3-STU membaca rak sebelum tambalan dipasang. Gelombang pertama (D3-FIXx, pukul 14:08,
enam berkas) lalu gelombang kedua (D4-FIXx, pukul 14:18, ikut menyentuh berkas yang sama plus
THERMAL) menambah blok anotasi lagi, sehingga sebagian nomor baris bergeser DUA KALI. Semua
jangkar objek ini kini diselaraskan ke kondisi DISK TERKINI (pasca kedua gelombang) dan
diperiksa otomatis oleh validator: tiap jangkar wajib berada dalam rentang berkas nyata DAN
tidak jatuh di baris kosong (Check 11 dan 13). Pasangan titik kunci:

| Jangkar | Nomor studi (prapatch) | Nomor kini (pasca D3+D4, terukur ulang giliran L1b) |
|---|---|---|
| `RANTAI-JAMINAN.md` (ELECTRICAL) rumus PI / DAR / vrutin / contoh / mata 4 / lampiran / status / terbuka | :38 / :44 / :50-51 / :59-71 / :79-83 / :98-107 / :109 / :112-113 | :41 / :47 / :53-54 / :62-74 / :85-89 / :110-119 / :121 / :124-125 (tetap sejak D3; berkas TIDAK ditambal D4) |
| `R3 - Gill` DAR / PI / contoh PI / bebas suhu / batas rutin / tidak ada ambang mutlak / bookmark | :102-103 / :115 / :120-121 / :138-139 / :144-145 / :152-155 / :179 | :102-103 / :115 / :123-124 / :141-142 / :147-148 / :155-158 / :182 (tetap sejak D3) |
| `KATALOG-RUMUS.md` bagian 5: DAR / PI / tegangan rutin | :227-258 | :240-246 / :248-255 / :260-264 |
| `KATALOG-RUMUS.md` 13.1: Tabel 100.1 / 100.14 / 100.18 + caveat konsensus | :430-466 | :455-469 / :474-481 / :486-493 / caveat :469 |
| `KATALOG-RUMUS.md` anotasi K-4 / K-5 / K-10 | (tidak ada prapatch) | :471-472 / :483-484 / :448-449 |
| `KATALOG-RUMUS.md` klaim `_standar/` + seksi "Yang TIDAK ada di rak" | :530, :532, :535 | klaim :444-445; seksi :560-578 (baris M ohm :566, pembumian :567, delta-T :568, standar Indonesia :571) |
| `AMBANG-TERIMA-INDUK.md` tiga baris R2 sah | :15-17 | :15-17 (tetap) |
| `AMBANG-TERIMA-INDUK.md` tiga baris R3 adopsi kontrak (PI / DAR / vrutin) | :55-57 | :61-63 |
| `AMBANG-TERIMA-INDUK.md` bentuk adopsi benar / bentuk dilarang | :63 / :65 | :69 / :71 |
| `AMBANG-TERIMA-INDUK.md` belum ada sumber sah (pembumian / PUIL / MTS) | :75 / :77 | :79 / :81 / :83 |
| `AMBANG-TERIMA-INDUK.md` wajib R4 + "menunggu data pabrikan" | :85-94 | :91-103 |
| `AMBANG-TERIMA-INDUK.md` cara memakai berkas / gate G4 / "metode boleh R3" | (tidak dikutip studi) | :107-113 / :6-7 / :52-53 |
| `ASUMSI-BAKU.md` tidak boleh diasumsikan / tabel gugur / TIDAK gugur | :128-129 / :143-145 / :153-155 | :131-132 / :146-148 / :159-161 |
| `REF-ELC-002.md` yang dipasok / halaman jangkar / boleh ambang? / batas pemakaian | :22 / :24 / :40 / :47 | :22 / :27 / :43 / :50 |
| `REF-ELC-002.md` label penanda / rantai / larangan lompat / gate G0-G7 | :32-33 / :45-47 / :49-51 / :54-56 | :38-39 / :52-55 / :58-59 / :61-65 |
| `REF-ELC-002.md` anotasi K-2 (dua tempat) | (tidak ada prapatch) | :29-30 dan :45-46 |
| `R2 - ANSI-NETA ATS-2017.md` Tabel 100.1 / 100.14 / baris 100.18 | :39-61 / :63-74 / :79-88 | tetap; HANYA peringatan "panduan tindakan" bergeser ke :93-95 |
| `R2 - ...md` tabel rujukan lain / struktur dokumen / pemakaian GSP | :99-108 / :112-121 / :125-135 | :106-117 / :121-130 / :134-144 |
| `R2 - ...md` pairing + batas standar (PUIL / MTS / pabrikan mendahului) | :144-146 / :147-148 / :149-150 | :156-158 / :159-160 / :161-162 |
| `TEMPLATE-BERITA-ACARA.md` bagian 3 / ringkasan sumber ambang / baris delta-T | :105-125 / :244-245, :250 / :201 | :105-131 / :246-261 (baris rasio :254, M ohm :255) / :207 |
| `THERMAL/RANTAI-JAMINAN.md` baris delta-T / lampiran klasifikasi | :70-71 / :93 | :73-74 / :102 |

Cacah blok anotasi known-defect terukur kini (probe baca langsung, giliran L1b):
`RANTAI-JAMINAN.md` ELECTRICAL 4 (D3) ; `R3 - Gill` 1 (D3) ; `REF-ELC-002.md` 3 (1 D4 + 2 D3) ;
`KATALOG-RUMUS.md` 16 (campuran D3, D4, VSSKB, anotasi misi lain) ; `AMBANG-TERIMA-INDUK.md` 4
(2 D4 + 1 D3 + 1 VSSKB) ; `ASUMSI-BAKU.md` 3 (1 D4 + 1 VSSKB + 1 lain) ;
`TEMPLATE-BERITA-ACARA.md` 5 (3 D3 + 2 D4) ; `THERMAL/RANTAI-JAMINAN.md` 4 (D4). Bentuk kedua
gelombang hanya-tambah; isi dan angka rak tidak diubah.

### 1.2 Lapis kartu pengetahuan [`ekas/04_KNOWLEDGE-CARDS/ELECTRICAL/`](../../ekas-lapis-teks/04_KNOWLEDGE-CARDS/ELECTRICAL/) (2 kartu)

| Kartu | R | Status otoritas | Yang dipasok (:22) | Halaman jangkar (:24/:27) | Boleh tetapkan ambang? (:37/:43) | Batas pemakaian (:41/:50) |
|---|---|---|---|---|---|---|
| `REF-ELC-001.md` | R3 | ACTIVE | Empat metode ukur isolasi, batas tegangan uji <= 75% terima / <= 60% pabrik | PDF 142, 144, 145 | **Tidak sendirian** - hanya bila kontrak mengadopsi tertulis | Memberi rasio dan metode, BUKAN ambang M ohm mutlak |
| `REF-ELC-002.md` | R2 | ACTIVE_WITH_SCOPE_LIMITS | 600 V -> 100 M ohm / 5 kV -> 1.500 M ohm / 15 kV -> 5.000 M ohm; delta-T > 15 derajat C antar komponen serupa atau > 40 derajat C terhadap udara | PDF 223, 241, 246 | **Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi | ATS = uji terima, BUKAN pemeliharaan (MTS). BUKAN ambang resistansi pembumian. Standar Amerika - bukan pengganti PUIL |

Kedua kartu memuat blok identik: penanda wajib `SOURCE-DERIVED / PROJECT-DERIVED / OEM-DERIVED /
ASSUMPTION` (`REF-ELC-001.md:32-33`, `REF-ELC-002.md:38-39`), rantai REQUIREMENT -> rujukan ->
keputusan desain -> perhitungan -> uji -> bukti -> terima (`REF-ELC-001.md:45-47`,
`REF-ELC-002.md:52-55`), larangan melompat dari rujukan langsung ke ambang terima
(`REF-ELC-001.md:49-50`, `REF-ELC-002.md:58-59`), dan gate G0-G7 (`REF-ELC-001.md:54-56`,
`REF-ELC-002.md:61-65`).

Kartu R2 kini membawa anotasi known-defect K-2 di dua tempat (`REF-ELC-002.md:29-30,45-46`):
jawaban "Ya" di seksi 3 baru menyebut satu syarat, padahal sumber menambah syarat kedua
(nilai berlaku "bila tidak ada standar konsensus lain"; spesifikasi pabrikan mendahului -
`R2 - ANSI-NETA ATS-2017.md:57-59, :161-162`). Setiap kutipan kartu ini WAJIB membawa caveat.

### 1.3 Lapis bersama (baris terkait kelistrikan/uji isolasi, nomor pasca-tambalan)

| Berkas | Baris | Yang dipasok |
|---|---|---|
| [`ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md`](../../ekas-lapis-teks/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md) (598 baris, 30.272 B) | :41-43 | indeks cepat PI, DAR, tegangan uji rutin (Gill) |
| idem | :53-55 | indeks cepat M ohm minimum, koreksi suhu, delta-T (ATS-2017) |
| idem | :233-262 | bagian 5 "Pengujian instalasi listrik": DAR, PI, batas rutin, empat metode |
| idem | :442-485 | bagian 13.1 ANSI/NETA ATS-2017: Tabel 100.1, 100.14, 100.18 versi katalog |
| idem | :460 | caveat katalog "berlaku bila tidak ada standar konsensus lain; spesifikasi pabrikan mendahului" |
| idem | :554, :556, :559 | "Yang TIDAK ada di rak": M ohm mutlak TERTUTUP, delta-T TERTUTUP, standar Indonesia TIDAK ADA |
| [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) (183 baris, 10.523 B) | :131-132 | ambang resistansi pembumian dan resistivitas tanah = TIDAK BOLEH diasumsikan |
| idem | :146-148 | asumsi yang GUGUR sejak standar masuk: M ohm isolasi, faktor koreksi suhu, delta-T termografi |
| idem | :156-158 | "yang TIDAK gugur": ATS memberi tahanan isolasi, BUKAN resistansi pembumian |
| [`ekas/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md`](../../ekas-lapis-teks/07_VERIFICATION-VALIDATION/ACCEPTANCE-CRITERIA/AMBANG-TERIMA-INDUK.md) (110 baris, 7.595 B) | :6-7 | aturan gate G4: R1/R2 sah; R3 hanya bila kontrak mengadopsi tertulis; R5 tidak pernah |
| idem | :15-17 | tiga baris R2 sah (isolasi M ohm, koreksi suhu, delta-T) |
| idem | :23-24 | anotasi known-defect K-2 atas baris :15 |
| idem | :28-31 | batas cakupan wajib: ATS untuk pemeliharaan = salah (itu MTS) |
| idem | :58-60 | tiga baris R3 perlu adopsi kontrak (PI, DAR, batas tegangan uji rutin) |
| idem | :66 | bentuk adopsi sah: "Ambang PI < 1 mengacu Gill (2008) sebagaimana diadopsi pasal ... kontrak." |
| idem | :68 | bentuk yang DILARANG: "sesuai praktik industri" |
| idem | :78, :80 | belum ada sumber sah: kepatuhan Indonesia (PUIL/SNI), uji pemeliharaan (MTS) |
| idem | :88-97 | daftar wajib R4 + instruksi "menunggu data pabrikan" |
| idem | :101-107 | cara memakai berkas ambang (empat langkah) |
| [`ekas/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md`](../../ekas-lapis-teks/07_VERIFICATION-VALIDATION/TEST-PROCEDURES/TEMPLATE-BERITA-ACARA.md) (269 baris, 12.689 B) | :105-130 | bagian 3 BA uji instalasi listrik (unsur wajib, metode, normalisasi) |
| idem | :207 | ambang lulus delta-T untuk pemeriksaan termal |
| idem | :250-251, :256 | ringkasan sumber ambang: rasio dari Gill, M ohm mutlak dari ATS, termal dari ATS |
| [`ekas/01_GOVERNANCE/AUTHORITY-STATUS.md`](../../ekas-lapis-teks/01_GOVERNANCE/AUTHORITY-STATUS.md) (115 baris, 5.164 B) | :29-31 | tiga baris batas cakupan ATS-2017 (terima vs peliharaan; M ohm vs ohm; Amerika vs PUIL) |
| [`ekas/02_REGISTERS/GAP-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv) (22 baris, 3.228 B) | :2, :9, :15 | GAP-001 (PUIL/SNI, TINGGI), GAP-008 (MTS, MENENGAH), GAP-014 (R4 by-design) |
| [`ekas/02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/MASTER-REFERENCE-REGISTER.csv) | :5-6 | REF-ELC-001 (`no-unless-contract-adopts`), REF-ELC-002 (`yes-if-adopted`) |
| [`ekas/00_START-HERE/README.md`](../../ekas-lapis-teks/00_START-HERE/README.md) (98 baris, 4.112 B) | :34-38, :47 | keadaan rak R1=0 R2=5 R3=24 R4=0 R5=8; alasan R4 by-design |

### 1.4 Lapis laci sumber (keberadaan fisik terukur)

| Laci nyata di pohon [`ekas/`](../../ekas-lapis-teks/) | Isi | Klaim `_ISI.md` | PDF primer sebenarnya |
|---|---|---|---|
| [`ekas/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/`](../../ekas-lapis-teks/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/) | hanya `_ISI.md` | 1 berkas, 3,3 MB (`_ISI.md:3,7`) | ada di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/`, 3.469.354 B = 3,31 MiB (cocok) |
| [`ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/ELECTRICAL/`](../../ekas-lapis-teks/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/ELECTRICAL/) | hanya `_ISI.md` | 1 berkas, 12,4 MB (`_ISI.md:3,7`) | ada di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/ELECTRICAL/`, 13.026.971 B = 12,42 MiB (cocok) |

Ukuran pada `_ISI.md` konsisten dengan byte nyata di laci luar-rak (uji MiB, bukan MB desimal).
**Pohon [`ekas/`](../../ekas-lapis-teks/) sendiri tidak memuat satu pun PDF** - kondisi struktural korpus, bukan cacat
domain ELECTRICAL (lihat Gap G-10; pola sama di domain FIBER-OPTIC).

### 1.5 PDF primer (verifikasi halaman = wewenang manusia; agen bekerja dari lapisan teks)

| Sumber | Edisi/tahun | Klaim lapis teks | Konvensi halaman (beku G-1 seksi 7) |
|---|---|---|---|
| ANSI/NETA ATS-2017, *Standard for Acceptance Testing Specifications for Electrical Power Equipment & Systems* (InterNational Electrical Testing Association) | 2017 | 262 halaman, 3,3 MB (`R2 - ANSI-NETA ATS-2017.md:5`) - TIDAK diverifikasi agen | selisih TETAP cetak + 19 = PDF; teruji internal 3/3 (Bagian 2.3) |
| Paul Gill, *Electrical Power Equipment Maintenance and Testing*, edisi kedua (CRC Press) | 2008 | 1.002 halaman, 12,4 MB (`R3 - Gill:4`) - TIDAK diverifikasi agen | nomor PDF langsung; TIDAK terujiable internal (tidak ada pasangan cetak di resume - lihat Bagian 5 uji b) |

Peringatan nama berkas yang menempel pada resume ATS (`R2 - ANSI-NETA ATS-2017.md:8-15`):
berkas pernah diterima dengan nama "...Maintenance Testing Specifications... ANSI/NETA
MTS-2007" padahal isinya ATS-2017. Bedanya substantif: **ATS = uji terima** (instalasi baru,
sebelum serah terima), **MTS = uji pemeliharaan** (instalasi berjalan). Nama berkas sudah
diperbaiki sesuai isinya.

Domain tetangga yang relevan HANYA sebagai rujukan silang (putusan P-8, tidak disalin):
[`ekas/05_DOMAIN-KNOWLEDGE/THERMAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/) (pemakai Tabel 100.18 - lihat K-3),
[`ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/) (UPS/baterai/genset - di luar D3),
[`ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/) (petir/pembumian - di luar D3),
[`ekas/05_DOMAIN-KNOWLEDGE/RCM/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RCM/) (rumus FFI untuk interval fungsi tersembunyi - lihat 3.6).

---

## Bagian 2 - Rumus dan angka acuan

Setiap rumus dan angka membawa penanda sumbernya sendiri bentuk koma plus jalur baris rak
relatif shared workspace. Tanpa marker = asumsi, custodian menolak.

### 2.1 Rumus inti domain

| # | Rumus | Ambang perhatian | Marker | Jalur baris rak (pasca-tambalan) |
|---|---|---|---|---|
| 1 | `PI = R(10 menit) / R(1 menit)` | PI < 1 | [R3, Gill, PDF 144] | `RANTAI-JAMINAN.md:41`; `R3 - Gill:109-115`; `KATALOG-RUMUS.md:248-255`; `REF-ELC-001.md:29` |
| 2 | `DAR = R(60 detik) / R(30 detik)` | DAR < 1,25 | [R3, Gill, PDF 144] | `RANTAI-JAMINAN.md:47`; `R3 - Gill:96-103`; `KATALOG-RUMUS.md:240-246`; `REF-ELC-001.md:29` |
| 3 | `V(uji rutin) <= 75% x V(uji terima maks)` ATAU `<= 60% x V(uji pabrik)` | - | [R3, Gill, PDF 145] | `RANTAI-JAMINAN.md:53-54`; `R3 - Gill:147-148`; `KATALOG-RUMUS.md:260-264`; `REF-ELC-001.md:22` |
| 4 | `R(terkoreksi 20 derajat C) = R(ukur) x faktor(Tabel 100.14)` | - | [R2, ANSI/NETA ATS-2017, Tabel 100.14, PDF 241] | `RANTAI-JAMINAN.md:57-60,67`; `R2 - ANSI-NETA ATS-2017.md:63-74`; `KATALOG-RUMUS.md:474-481` |
| 5 | `R(ukur) >= ambang Tabel 100.1 per tegangan nominal` | lihat 2.2 A | [R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223] | `RANTAI-JAMINAN.md:68,85`; `R2 - ANSI-NETA ATS-2017.md:39-61`; `KATALOG-RUMUS.md:455-469` |
| 6 | `delta-T antar komponen serupa` dan `delta-T terhadap udara sekitar` -> empat tingkat tindakan | > 15 derajat C / > 40 derajat C | [R2, ANSI/NETA ATS-2017, Tabel 100.18, PDF 246] | `R2 - ANSI-NETA ATS-2017.md:79-95`; `KATALOG-RUMUS.md:486-493`; `AMBANG-TERIMA-INDUK.md:17` |

Rumus 1-3 adalah **rasio** - bebas pengaruh suhu dan ukuran peralatan (`R3 - Gill:141-142`),
sehingga tidak butuh normalisasi. Rumus 4-6 adalah **angka mutlak** yang memerlukan sumber
normatif. Pemisahan ini menentukan cara pakai: rasio tidak dikoreksi suhu, mutlak WAJIB
dikoreksi (`TEMPLATE-BERITA-ACARA.md:124-126`).

### 2.2 Angka acuan per sumber (salinan persis + jalur baris)

**A. Tabel 100.1 - tahanan isolasi minimum** [R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223 /
cetak 204]. Salinan utuh 10 baris dari `R2 - ANSI-NETA ATS-2017.md:44-55`:

| Tegangan nominal peralatan (V) | Tegangan uji DC minimum (V) | Tahanan isolasi minimum (M ohm) | Baris |
|---|---|---|---|
| 250 | 500 | 25 | `:46` |
| 600 | 1.000 | 100 | `:47` |
| 1.000 | 1.000 | 100 | `:48` |
| 2.500 | 1.000 | 500 | `:49` |
| 5.000 | 2.500 | 1.500 | `:50` |
| 8.000 | 2.500 | 2.500 | `:51` |
| 15.000 | 2.500 | 5.000 | `:52` |
| 25.000 | 5.000 | 10.000 | `:53` |
| 34.500 | 5.000 | 100.000 | `:54` |
| 46.000 ke atas | 5.000 | 100.000 | `:55` |

Judul tabel sebagaimana tertulis di `:41-42`: *Insulation Resistance Test Values, Electrical
Apparatus and Systems **Other Than Rotating Machinery***. Catatan standar sendiri (`:57-59`):
nilai disarankan Standards Review Council **bila tidak ada standar konsensus lain**; bila
pabrikan menetapkan nilai sendiri, **nilai pabrikan yang berlaku**. Caveat ini bukan hiasan -
ia syarat pemakaian (lihat K-2).

**B. Tabel 100.14 - faktor koreksi ke 20 derajat C** [R2, ..., Tabel 100.14, PDF 241 /
cetak 222], salinan utuh 6 baris dari `R2 - ANSI-NETA ATS-2017.md:67-74`:

| Suhu (derajat C) | Isolasi terendam minyak | Isolasi padat (bukan mesin berputar) | Baris |
|---|---|---|---|
| -10 | 0,125 | 0,25 | `:69` |
| 0 | 0,25 | 0,40 | `:70` |
| 10 | 0,50 | 0,63 | `:71` |
| **20** | **1,00** | **1,00** | `:72` |
| 25 | 1,40 | 1,25 | `:73` |
| 30 | 1,98 | 1,58 | `:74` |

Nama kolom ketiga mengecualikan mesin berputar secara eksplisit (`:67`) - lihat K-1 dan G-4.

**C. Tabel 100.18 - ambang delta-T termografi** [R2, ..., Tabel 100.18, PDF 246 / cetak 227],
salinan utuh 4 baris dari `R2 - ANSI-NETA ATS-2017.md:83-88`:

| delta-T antar komponen serupa (beban serupa) | delta-T terhadap udara sekitar | Tindakan yang disarankan | Baris |
|---|---|---|---|
| 1-3 derajat C | 1-10 derajat C | kemungkinan cacat; perlu diselidiki | `:85` |
| 4-15 derajat C | 11-20 derajat C | kemungkinan besar cacat; perbaiki bila sempat | `:86` |
| - | 21-40 derajat C | pantau sampai perbaikan dapat dilakukan | `:87` |
| **> 15 derajat C** | **> 40 derajat C** | ketidaksesuaian besar; perbaiki segera | `:88` |

Peringatan yang menempel pada tabel (`:90-92`): spesifikasi suhu berbeda menurut jenis
peralatan; **tabel ini panduan tindakan, bukan batas mutlak.** Kalimat ini wajib ikut setiap
kutipan tabel (lihat K-3).

**D. Angka Gill (rasio dan metode)** [R3, Gill, PDF 142/144/145/659]:

| Butir | Nilai persis di rak | Baris rak |
|---|---|---|
| Ambang DAR | "di bawah 1,25 merupakan alasan untuk penyelidikan dan kemungkinan perbaikan peralatan" | `R3 - Gill:102-103` |
| Ambang PI | "kurang dari 1 menunjukkan peralatan mengalami penurunan mutu" | `R3 - Gill:115` |
| PI menggantikan DA | "Bila uji PI dilakukan, uji DA tidak perlu dilakukan lagi" (motor, PDF 659) | `R3 - Gill:117-118` |
| Contoh PI buku | megohmmeter 900 M ohm menit ke-1, 2.700 M ohm menit ke-10 -> PI = 2.700 / 900 = 3,0 | `R3 - Gill:123-124` |
| Empat metode | short-time reading / time-resistance (DAR) / Polarization Index (PI) / step-voltage | `R3 - Gill:130-135` |
| Syarat short-time | hanya bermakna sebagai tren; wajib dinormalkan ke 20 derajat C + pengaruh kelembapan diperhitungkan | `R3 - Gill:137-139` |
| Keunggulan DAR/PI | bebas pengaruh suhu dan ukuran peralatan -> tidak perlu normalisasi | `R3 - Gill:141-142` |
| Batas tegangan uji rutin | <= 75% V uji terima maksimum ATAU <= 60% V uji pabrik | `R3 - Gill:147-148` |
| Yang TIDAK diberikan buku | ambang mutlak M ohm lulus/tidak lulus; pendekatannya rasio dan tren | `R3 - Gill:155-158` |
| Alat utama | megohmmeter (PDF 48); DAR biasanya terbatas pada megohmmeter engkol tangan | `R3 - Gill:46-47,105` |
| Pintu masuk format BA | Apendiks A "Forms and Reports", PDF 928 | `R3 - Gill:37-38,166-167` |

**E. Status keabsahan per lapis** (angka tidak berubah; yang berubah adalah klaim sahnya):

| Lapis | Isolasi M ohm | PI / DAR | Batas uji rutin | delta-T termografi |
|---|---|---|---|---|
| Rantai E (`RANTAI-JAMINAN.md:85-89`) | R2 | R3 | R3 | R2 |
| Katalog 13.1 / bagian 5 (`KATALOG-RUMUS.md:442-496`, `:233-262`) | R2 | R3 | R3 | R2 |
| Ambang induk (`AMBANG-TERIMA-INDUK.md:15-17`, `:61-63`) | R2 sah (dengan caveat K-2) | R3 perlu adopsi kontrak | R3 perlu adopsi kontrak | R2 sah (dengan caveat K-3) |
| Asumsi baku (`ASUMSI-BAKU.md:146-148`) | gugur sebagai asumsi | (tidak disebut) | (tidak disebut) | gugur sebagai asumsi |
| Kartu (`REF-ELC-001.md:37`, `REF-ELC-002.md:43`) | Ya bila diadopsi + edisi tervalidasi | Tidak sendirian | Tidak sendirian | Ya bila diadopsi |
| BA (`TEMPLATE-BERITA-ACARA.md:111-116`, `:246-261`) | ada di rak | ada di rak | ada di rak | ada di rak |

### 2.3 Uji aritmetika deterministik atas angka rak (dijalankan nyata pada giliran ini)

Skrip `docs/2026-09-23-nws-knowledge-register/scripts/measure_d3_anchors.py` dijalankan pada
giliran L1 ini; hasilnya di bawah adalah cetakan alat, bukan ingatan dari studi.

| Uji | Masukan dari rak | Hasil alat | Vonis |
|---|---|---|---|
| Offset halaman ATS-2017 | 223-204; 241-222; 246-227 | 19; 19; 19 | **LOLOS 3/3** - klaim "tetap +19" (`R2 - ...md:17`) terbukti internal |
| Contoh PI buku Gill | 2.700 / 900 | 3,0 | **LOLOS** - cocok `R3 - Gill:124` |
| Koreksi 62 M ohm @30 derajat C kolom isolasi padat | 62 x 1,58 | 97,96 | Terhitung (PROJECT-DERIVED); rak tidak menuliskan hasilnya |
| Koreksi 62 M ohm @30 derajat C kolom terendam minyak | 62 x 1,98 | 122,76 | Terhitung (PROJECT-DERIVED); rak tidak menuliskan hasilnya |
| Batas rutin dari 1.000 V uji terima | 0,75 x 1.000 | 750 | Kerangka hitung, BUKAN angka rak |
| Batas rutin basis 60% dari 1.000 V | 0,60 x 1.000 | 600 | Kerangka hitung, BUKAN angka rak |
| Ukuran PDF vs klaim `_ISI.md` | 3.469.354 B; 13.026.971 B | 3,31 MiB; 12,42 MiB | **LOLOS** - cocok 3,3 MB dan 12,4 MB |
| Komposisi Tabel 100.1 resume vs katalog | 10 baris vs 9 baris | nilai sama; baris 46 kV tergabung | Lihat K-4 |
| Komposisi Tabel 100.14 resume vs katalog | 6 baris vs 4 baris | nilai sama; baris -10 dan 25 hilang | Lihat K-5 |
| Kemunculan `interval` / `torque` / `torsi` / `petir` di rak ELECTRICAL | - | 0 / 0 / 0 / 0 | Konfirmasi G-7 dan G-8 (bukan dugaan) |
| Direktori bernama `_standar` di pohon [`ekas/`](../../ekas-lapis-teks/) | - | 0 direktori | Konfirmasi K-10 |
| Baris domain ELECTRICAL di TEST/CALCULATION/REQUIREMENT/EVIDENCE-REGISTER.csv | - | 0 / 0 / 0 / 0 | Konfirmasi G-9 |

Nol nilai gagal reproduksi aritmetika. Yang bermasalah adalah **propagasi syarat pemakaian**
antar lapis (Bagian 5), bukan angkanya.

---

## Bagian 3 - Kerangka hitung terapan

### 3.1 Urutan kerja yang rak tetapkan (tidak boleh dibalik)

Dari `RANTAI-JAMINAN.md:22-29` (mata 2 keputusan desain) dan `:62-74` (contoh):

```
1. Pilih metode ukur      -> empat metode Gill (PDF 142); pengukuran sesaat SAJA ditolak
                             untuk peralatan besar karena tidak menampakkan tren
2. Tetapkan tegangan uji  -> batas mata 3; menaikkan tegangan "agar meyakinkan" DITOLAK
                             (merusak isolasi yang diuji)
3. Catat suhu saat ukur   -> koreksi ke 20 derajat C; membandingkan antar-waktu tanpa
                             koreksi DITOLAK (selisih suhu bisa lebih besar daripada degradasinya)
4. Nilai = rasio + mutlak + tren (tiga kriteria, tidak saling menggantikan)
```

Baris kunci: `RANTAI-JAMINAN.md:29` "Kriteria penilaian: **Rasio (PI, DAR) + M ohm mutlak
[R2] + tren** | Salah satu saja ditolak - ketiganya menangkap gejala berbeda"; `:73-74`
"Bila nilai terkoreksi < 100 M ohm -> tidak memenuhi ambang [R2], walaupun PI dan DAR terlihat
baik. Ketiga kriteria itu tidak saling menggantikan."

Penegas rekonsiliasi K-8 (milik objek ini, bukan rak): yang TIDAK SALING MENGGANTIKAN adalah
**rasio vs M ohm mutlak vs tren**. Di DALAM keluarga rasio, PI mengerjakan peran DA
(`R3 - Gill:117-118`, PDF 659), sehingga DAR menjadi opsional bila PI dikerjakan. Rak tidak
pernah menuliskan pembedaan ini eksplisit; pembacaan harfiah kedua kalimat menghasilkan
instruksi bertentangan.

### 3.2 Contoh terhitung rak #1 (satu-satunya di domain ini) + penyelesaiannya

Rak menuliskan soalnya tetapi berhenti sebelum hasil angka (`RANTAI-JAMINAN.md:62-71`):
"Motor 600 V, hasil ukur 62 M ohm pada 30 derajat C" -> langkah 1 "62 M ohm x faktor Tabel
100.14 -> nilai terkoreksi"; langkah 2 bandingkan dengan 100 M ohm.

Penyelesaian dengan angka rak yang tersedia (faktor dari `R2 - ANSI-NETA ATS-2017.md:73-74`):

```
Kolom isolasi padat (bukan mesin berputar):  62 x 1,58 = 97,96 M ohm  -> < 100 M ohm => TIDAK LULUS
Kolom isolasi terendam minyak:               62 x 1,98 = 122,76 M ohm -> > 100 M ohm => LULUS
```

Vonis berbeda tergantung kolom yang dipilih, dan **rak tidak menyediakan kolom yang sah untuk
mesin berputar**: judul Tabel 100.1 mengecualikan *Rotating Machinery*
(`R2 - ANSI-NETA ATS-2017.md:41-42`) dan kolom "isolasi padat" mengecualikan "bukan mesin
berputar" (`:67`). Contoh rak memakai kata "Motor". Ini bukan kekurangan aritmetika - ini cacat
cakupan yang tercatat sebagai **K-1, CALON DEFECT SUBSTANTIF menunggu putusan manusia**.
Angka 97,96 dan 122,76 adalah hasil hitung pekerja dari masukan rak, bertanda
`PROJECT-DERIVED`, BUKAN angka rak.

### 3.3 Contoh terhitung rak #2 (dari resume Gill, lengkap sampai vonis)

`R3 - Gill:123-124`: megohmmeter membaca 900 M ohm pada menit ke-1 dan 2.700 M ohm pada menit
ke-10 -> `PI = 2.700 / 900 = 3,0` -> jauh di atas ambang 1 -> isolasi berperilaku baik.
Aritmetika direproduksi alat pada giliran ini (2.3). Ini contoh **rasio**: tidak butuh koreksi
suhu (`R3 - Gill:141-142`), sehingga bebas dari masalah cakupan di 3.2.

### 3.4 Ambang isolasi per kelas tegangan (cara memilih baris yang rak tetapkan)

Cara memilih baris Tabel 100.1: tegangan **nominal peralatan**, BUKAN tegangan uji. Tiga titik
penekan yang rak tulis eksplisit:

1. Nilai pabrikan mendahului tabel (`R2 - ...md:59`, `:161-162`; `KATALOG-RUMUS.md:469`).
2. Tabel berlaku hanya bila tidak ada standar konsensus lain (`R2 - ...md:57-58`).
3. Tabel tidak berlaku untuk mesin berputar (`R2 - ...md:41-42`) - dan **tidak ada tabel
   penggantinya di rak** untuk mesin berputar (G-4).

Untuk pekerjaan GSP yang nyata (pemilihan baris dari Tabel 100.1, `SOURCE-DERIVED` untuk
nilainya): panel LV 600 V -> uji DC 1.000 V, minimum 100 M ohm; kabel kelas 15 kV -> uji DC
2.500 V, minimum 5.000 M ohm; kabel kelas 25 kV -> uji DC 5.000 V, minimum 10.000 M ohm.
**Kelas 20 kV tidak menjadi baris tabel** (tabel hanya 15.000 dan 25.000,
`R2 - ...md:52-53`); pemilihan baris untuk kelas menengah Indonesia adalah keputusan yang
harus ditulis di berita acara, bukan diimplikasikan (G-6).

### 3.5 Torque (torsi) sambungan listrik - status: TIDAK ADA di rak

Diukur ulang giliran ini: kemunculan `torque` dan `torsi` di [`ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/)
= **0**. Satu-satunya padanan di rak ada di domain lain:
`CIVIL-STRUCTURAL/RANTAI-JAMINAN.md:103` "Torsi baut ... tidak ada di rak | Spesifikasi baut
[R4] + SNI 1729". Kesimpulan: **tidak ada angka torsi sambungan listrik di rak**; nilainya R4
(lembar data pabrikan / spesifikasi sambungan). Jangan dikarang dari pengetahuan umum
(`AMBANG-TERIMA-INDUK.md:96-97`: tulis "menunggu data pabrikan").

### 3.6 Interval uji - status: TIDAK ADA sandaran di rak untuk lingkup ini

Kata `interval` = **0 kemunculan** di seluruh [`ekas/05_DOMAIN-KNOWLEDGE/ELECTRICAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/ELECTRICAL/) (diukur
ulang, 2.3). Alasan struktural: ATS adalah standar **uji terima** (satu kali sebelum serah
terima), sehingga interval berkala bukan bagiannya; yang mengatur interval pemeliharaan adalah
**MTS - tidak ada di rak** (GAP-008, `GAP-REGISTER.csv:9`).

Satu-satunya jalan sah yang tersedia di rak untuk interval fungsi tersembunyi adalah FFI
Moubray milik domain RCM: `FFI = 2 x ketaktersediaan_yang_diizinkan x MTBF_perangkat / ...`
(`ekas/05_DOMAIN-KNOWLEDGE/RCM/RANTAI-JAMINAN.md:60-67`; [R3, Moubray, PDF 198]) - dan ia
butuh sasaran MTBF majemuk dari pemilik (`ASUMSI-BAKU.md:129`). **DILARANG mengimpor interval
dari domain tetangga**: triwulanan IEEE 1188 adalah pemeriksaan BATERAI
(`AMBANG-TERIMA-INDUK.md:19`), bukan uji instalasi listrik.

### 3.7 Hitung yang rak nyatakan TIDAK bisa dikerjakan dari rak

| Keperluan | Pernyataan rak | Jalur |
|---|---|---|
| Ambang M ohm mutlak dari buku Gill | "Buku tidak memberi nilai ambang mutlak ... angkanya harus diambil dari standar yang berlaku (NETA, IEEE, atau PUIL), bukan dari buku ini" | `R3 - Gill:155-158` |
| Faktor koreksi suhu dari Gill | Gill menyebut keharusan normalisasi tanpa memberi angkanya | `R2 - ...md:76-77` |
| Kepatuhan Indonesia | ATS bukan pengganti PUIL | `R2 - ...md:156-158`; `AMBANG-TERIMA-INDUK.md:81` |
| Ambang resistansi pembumian | ATS tidak menyentuhnya; besaran berbeda | `AUTHORITY-STATUS.md:30`; `ASUMSI-BAKU.md:159-161` |
| Program pemeliharaan berjalan | MTS belum ada | `R2 - ...md:159-160`; `GAP-REGISTER.csv:9` |
| Nilai torsi sambungan | tidak ada di rak | 3.5; `AMBANG-TERIMA-INDUK.md:91-103` |

---

## Bagian 4 - Ambang terima NETA ATS-2017 yang hidup di rak

### 4.1 Nilai lulus minimal (yang terpasang di gerbang mutu)

| Uji | Nilai lulus minimal | R | Sah sebagai dasar lulus/tidak? | Jalur |
|---|---|---|---|---|
| Tahanan isolasi, peralatan 250 V | 25 M ohm (uji DC 500 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:46` |
| Tahanan isolasi, 600 V / 1.000 V | 100 M ohm (uji DC 1.000 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:47-48`; `AMBANG-TERIMA-INDUK.md:15`; `REF-ELC-002.md:22` |
| Tahanan isolasi, 2.500 V | 500 M ohm (uji DC 1.000 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:49` |
| Tahanan isolasi, 5 kV | 1.500 M ohm (uji DC 2.500 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:50` |
| Tahanan isolasi, 8 kV | 2.500 M ohm (uji DC 2.500 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:51` |
| Tahanan isolasi, 15 kV | 5.000 M ohm (uji DC 2.500 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:52` |
| Tahanan isolasi, 25 kV | 10.000 M ohm (uji DC 5.000 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:53`; `KATALOG-RUMUS.md:466` |
| Tahanan isolasi, 34,5 kV dan 46 kV ke atas | 100.000 M ohm (uji DC 5.000 V) | R2 | ya, dengan caveat K-2 | `R2 - ...md:54-55`; `KATALOG-RUMUS.md:467` (bentuk tergabung - lihat K-4) |
| Normalisasi hasil ukur | faktor ke 20 derajat C; pada 20 derajat C faktor = 1,00 (kedua kolom) | R2 | ya | `R2 - ...md:72`; `AMBANG-TERIMA-INDUK.md:16` |
| Termografi delta-T | > 15 derajat C antar komponen serupa ATAU > 40 derajat C terhadap udara -> perbaiki segera | R2 | dengan caveat K-3 (panduan tindakan, bukan batas mutlak) | `R2 - ...md:88,90-92`; `AMBANG-TERIMA-INDUK.md:17` |
| Polarization Index | PI < 1 -> selidiki | R3 | HANYA sah bila kontrak mengadopsi tertulis | `AMBANG-TERIMA-INDUK.md:61`; `R3 - Gill:115` |
| Dielectric Absorption Ratio | DAR < 1,25 -> selidiki | R3 | HANYA sah bila kontrak mengadopsi tertulis | `AMBANG-TERIMA-INDUK.md:62`; `R3 - Gill:102-103` |
| Batas tegangan uji rutin | <= 75% V uji terima / <= 60% V pabrik | R3 | HANYA sah bila kontrak mengadopsi tertulis | `AMBANG-TERIMA-INDUK.md:63` |

Predikat per baris tabel di atas (bentuk koma, satu paket dengan jalur baris): baris tegangan
250 V s.d. 46 kV ke atas [R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223]; normalisasi ke 20 derajat C
[R2, ANSI/NETA ATS-2017, Tabel 100.14, PDF 241]; delta-T termografi [R2, ANSI/NETA ATS-2017,
Tabel 100.18, PDF 246]; PI [R3, Gill, PDF 144]; DAR [R3, Gill, PDF 144]; batas tegangan uji
rutin [R3, Gill, PDF 145].

**Cara membaca kolom "Sah?"** (aturan gate G4, `AMBANG-TERIMA-INDUK.md:6-7`): R1/R2 -> sah;
R3 -> hanya bila kontrak mengadopsinya tertulis; R5 -> tidak pernah. Bentuk adopsi yang sah:
"Ambang PI < 1 mengacu Gill (2008) sebagaimana diadopsi pasal ... kontrak" (`:69`). Bentuk yang
DILARANG: "sesuai praktik industri" (`:68`).

**Larangan tampilan yang mengikat objek ini:** PI < 1 dan DAR < 1,25 TIDAK BOLEH disajikan
sebagai ambang mutlak tanpa syarat. Statusnya R3 "perlu adopsi kontrak" DAN membawa caveat K-2
untuk angka mutlak yang berdampingan dengannya. Meratakan R2 dan R3 menjadi "standar"
dilaporkan sebagai cacat (`AMBANG-TERIMA-INDUK.md:49-50`: metode boleh R3; angka
lulus/tidak-lulus yang tidak dihitung tidak boleh R3).

### 4.2 Interval

**Tidak ada sandaran di rak** (3.6, G-1, G-8). Objek ini menyatakan: "interval uji pemeliharaan
instalasi listrik: tidak ada sandaran di rak (MTS absen)". Yang ada di rak hanyalah interval
untuk domain tetangga (IEEE 1188: pemeriksaan baterai triwulanan, `AMBANG-TERIMA-INDUK.md:19`)
yang BUKAN lingkup ELECTRICAL.

### 4.3 Tabel rujukan ATS-2017 lain yang tercatat tapi TIDAK diekstrak angkanya

`R2 - ...md:106-117` mendaftar delapan tabel lain dengan nomor cetak saja, tanpa nilai: 100.2
switchgear withstand (205), 100.5 trafo IR (209), 100.8 instantaneous trip (214), 100.9
instrument transformer dielectric (215), 100.10 vibrasi maksimum (216), 100.13 SF6 (221),
100.15-100.17 high-potential recloser/sectionalizer/busbar (224-226), 100.21 akurasi CT TP IEC
(231). **Angkanya tidak ada di lapisan teks** - hanya keberadaannya. Objek ini karena itu TIDAK
boleh mengklaim cakupan switchgear withstand, vibrasi, SF6, dsb. (Gap G-5).

### 4.4 Struktur dokumen ATS yang tercatat (untuk penelusuran lanjutan)

129 bookmark; bagian utama: General Scope, Applicable References, Qualifications of Testing
Organization and Personnel, Division of Responsibility, Safety and Precautions, Suitability of
Test Equipment, Test Report, Inspection and Test Procedures (bagian terbesar, per jenis
peralatan), Tables (cetak 204 dst.) - `R2 - ...md:121-130`. Pemakaian GSP per keperluan ada di
`:134-144`.

### 4.5 Bukti serah yang rak tetapkan (Rantai E mata 5)

Delapan lampiran wajib, `RANTAI-JAMINAN.md:110-119`: berita acara uji tahanan isolasi; tabel
hasil berisi nilai terukur + **suhu saat ukur** + nilai terkoreksi; ambang Tabel 100.1 yang
berlaku + tegangan nominal peralatan (**sebutkan barisnya, bukan hanya nama standarnya**);
nilai PI dan DAR beserta waktu pembacaan; tegangan uji yang dipakai + dasar pembatasannya;
sertifikat kalibrasi megger; riwayat hasil sebelumnya; kartu kendali rantai.

Catatan rak pada butir suhu (`:113`): "Suhu sering tidak dicatat - hasilnya jadi tidak dapat
dibandingkan." Ini alasan mata 5 ada, bukan formalitas. Kerangka BA-nya:
`TEMPLATE-BERITA-ACARA.md:105-131`.

---

## Bagian 5 - Register kontradiksi / known-defect

Sepuluh butir dari studi, naik UTUH dengan predikat vonisnya masing-masing. Tidak ada **nilai**
yang berbeda antar berkas (uji c studi: nol selisih angka); yang berbeda adalah cakupan, syarat
pemakaian, dan kehadiran baris - kategori cacat yang tidak tertangkap oleh "cek angka sama".
Semua vonis halaman berstatus BELUM TERKONFIRMASI terhadap sumber primer sampai manusia membuka
PDF; bentuk lama tidak dihapus di mana pun, hanya ditandai. Rak sudah dianotasi lewat tambalan
hanya-tambah D3-FIXx lalu D4-FIXx (dua-duanya 2026-09-24; daftar pergeseran dan cacah blok di Bagian 1.1a).

### K-1. Contoh terhitung rantai memakai ambang yang tabelnya mengecualikan mesin berputar - CALON DEFECT SUBSTANTIF, menunggu putusan manusia (TINGGI)

- Rantai: "Motor 600 V, hasil ukur 62 M ohm pada 30 derajat C" lalu "Bandingkan ambang: Tabel
  100.1, 600 V -> minimum 100 M ohm [R2]" - `RANTAI-JAMINAN.md:64,68` (pra-patch `:61,65`).
- Tabel yang dirujuk berjudul *Insulation Resistance Test Values, Electrical Apparatus and
  Systems **Other Than Rotating Machinery*** - `R2 - ANSI-NETA ATS-2017.md:41-42`.
- Kolom koreksi yang tersedia juga mengecualikan: "Isolasi padat (**bukan mesin berputar**)" -
  `R2 - ANSI-NETA ATS-2017.md:67`.
- Dampak: contoh satu-satunya di domain ini mengajari pembaca membandingkan motor dengan angka
  yang cakupan tabelnya tidak mencakup motor. Efek lanjutan: vonis berubah tergantung kolom
  (97,96 vs 122,76 M ohm, 3.2).
- Lapis yang mewarisi: NOL (tidak ada lapis lain yang mengulang contoh). Cacat lokal rantai,
  bukan wabah - tetapi rantai inilah yang dijadikan kerangka BA.
- Anotasi terpasang: `RANTAI-JAMINAN.md:76-77`.
- Keputusan lanjut: **KEPUTUSAN DIBUTUHKAN (controller/manusia)** - ganti contoh menjadi
  peralatan non-berputar (panel 600 V), atau tambahkan kalimat pengecualian di mata 3, atau
  tandai contoh sebagai ilustrasi metode saja. Pekerja tidak mengubah rak (read-only).

### K-2. Caveat "bila tidak ada standar konsensus lain" hilang di lapis hilir - cacat propagasi (TINGGI)

- Ada di sumber: `R2 - ANSI-NETA ATS-2017.md:57-59` dan `:161-162`; `KATALOG-RUMUS.md:469`.
- Tidak ada di: `AMBANG-TERIMA-INDUK.md:15` (baris disajikan dengan kolom "Sah?" centang tanpa
  catatan pabrikan-mendahului), `REF-ELC-002.md:22,43`, `TEMPLATE-BERITA-ACARA.md:113,251`,
  `RANTAI-JAMINAN.md:85`.
- Dampak: gerbang rilis memperlakukan 100 M ohm sebagai ambang mutlak tanpa syarat, padahal
  sumber R2-nya sendiri mensyaratkan "tidak ada standar konsensus lain" dan memberi prioritas ke
  spesifikasi pabrikan. Persis pola pemicu angka salah pada dokumen serah.
- Anotasi terpasang: `AMBANG-TERIMA-INDUK.md:26-27`, `REF-ELC-002.md:29-30,45-46`,
  `TEMPLATE-BERITA-ACARA.md:118-119,266-267`, `RANTAI-JAMINAN.md:92-93`.
- Perlakuan objek ini: klausul caveat **wajib ikut** setiap kali angka Tabel 100.1 tampil
  (diterapkan di 2.2 A, 3.4, 4.1). Usulan tambal permanen di lapis hilir tetap pekerjaan
  controller.

### K-3. Tabel 100.18 dinaikkan jadi "ambang lulus" padahal resume menyebutnya "panduan tindakan, bukan batas mutlak" - cacat propagasi (TINGGI, lintas domain D4)

- Peringatan sumber: `R2 - ANSI-NETA ATS-2017.md:93-95`.
- Hilang di: `AMBANG-TERIMA-INDUK.md:17` ("-> perbaiki segera" tanpa caveat),
  `ASUMSI-BAKU.md:148`, `TEMPLATE-BERITA-ACARA.md:207`, `KATALOG-RUMUS.md:486-493`, dan
  **domain THERMAL**: `THERMAL/RANTAI-JAMINAN.md:73-74` memberi "> 15 derajat C -> perbaiki
  segera" berlabel R2 tanpa caveat; `:102` meminta "klasifikasi terhadap Tabel 100.18" sebagai
  bukti serah.
- Dampak lintas domain: temuan termal bisa divonis "tidak lulus" atas angka yang standarnya
  sendiri sebut panduan. Calon defect yang MELINTASI BATAS DOMAIN - relevan untuk D4 (THERMAL)
  dan harus dikoordinasikan controller agar dua domain tidak menulis vonis berbeda untuk tabel
  yang sama.
- Anotasi known-defect kini SUDAH terpasang di berkas THERMAL: 4 blok D4-FIXx (2026-09-24, pasca
  studi menutup; terukur) - termasuk yang menyatakan tabel ambang THERMAL hanyalah cuplikan dua
  baris dari empat tingkat. Isi dan angka rak tidak diubah tambalan itu; kualifikator "panduan
  tindakan, bukan batas mutlak" tetap hanya ada di resume ATS.
- Keputusan lanjut: adjudikasi oleh manusia terhadap PDF primer (apakah kalimat peringatan itu
  memang ada di PDF 246), lalu tambal lapis hilir termasuk THERMAL.

### K-4. Komposisi Tabel 100.1 berbeda antar lapis: 10 baris vs 9 baris - delta cakupan (RENDAH, terukur)

- Resume: `R2 - ANSI-NETA ATS-2017.md:54` "| 34.500 | 5.000 | 100.000 |" dan `:55`
  "| 46.000 ke atas | 5.000 | 100.000 |".
- Katalog: `KATALOG-RUMUS.md:467` "| 34.500 ke atas | 5.000 | 100.000 |" - baris 46.000 tidak ada.
- Nilai tidak berkontradiksi (keduanya 100.000 M ohm); yang hilang adalah **keberadaan baris
  46 kV sebagai kelas tersendiri**. Grep `46.000` di seluruh [`ekas/`](../../ekas-lapis-teks/) (ukur ulang giliran L1):
  2 berkas = resume ATS + katalog (baris anotasi K-4), jadi populasi angkanya memang dua.
- Dampak rendah untuk praktik GSP (46 kV jarang), tinggi untuk audit "salin persis".
- Perlakuan objek ini: 2.2 A menampilkan bentuk LENGKAP 10 baris (resume = otoritas); katalog
  dinyatakan sebagai ringkasan. Anotasi `KATALOG-RUMUS.md:471-472`.

### K-5. Tabel 100.14 di katalog kehilangan dua baris suhu - delta cakupan (SEDANG, terukur)

- Resume: enam baris suhu -10 / 0 / 10 / 20 / 25 / 30 (`R2 - ...md:69-74`).
- Katalog: empat baris 0 / 10 / 20 / 30 (`KATALOG-RUMUS.md:478-481`) - baris **-10 (0,125 /
  0,25)** dan **25 (1,40 / 1,25)** hilang.
- Dampak nyata: 25 derajat C adalah suhu ruang perangkat yang sangat sering terjadi di
  Indonesia; pengguna yang hanya membuka katalog tidak menemukan faktornya dan berpotensi
  interpolasi liar.
- Anotasi `KATALOG-RUMUS.md:483-484`. Perlakuan objek ini: 2.2 B menampilkan bentuk LENGKAP
  6 baris.

### K-6. "Empat ambang uji tidak punya sumber" tetapi hanya dua yang didaftar - ambiguitas rujukan (RENDAH, tidak teradjudikasi dari teks)

- `R2 - ANSI-NETA ATS-2017.md:24-25` menyebut **empat** ambang tertulis tidak ada di
  `TEMPLATE-BERITA-ACARA.md`; `:27-30` hanya menutup **dua** (M ohm isolasi, delta-T termal).
- Dua sisanya tidak pernah dinamai di berkas mana pun. Pembacaan paling mungkin: kriteria ganti
  baterai (IEEE 1188) dan ventilasi baterai (IEC 62485-2) - keduanya juga masuk rak 19 Agustus
  2026 (`KATALOG-RUMUS.md:444`), tetapi keduanya milik domain POWER-BACKUP, BUKAN ELECTRICAL.
- Status: **calon defect dokumentasi**, tidak dapat diputus dari lapisan teks. **Tidak boleh
  naik ke objek IL sebagai angka** - dan tidak naik; hanya tercatat di sini.

### K-7. Klaim "bookmark bawaan 24 entri" vs 17 entri yang dipetakan - tidak terverifikasi (RENDAH)

- `R3 - Gill:7` dan `:182` mengklaim 24 entri bookmark (bab + apendiks); peta isi `:20-35`
  mendaftar 17 (13 bab + 2 apendiks + bibliography + index).
- Bukan kontradiksi angka (bookmark bisa memuat sub-bagian yang tidak dipetakan), tetapi tidak
  dapat diverifikasi dari teks. Dicatat agar konsumen tidak mengulang angka 24 sebagai fakta
  terverifikasi.

### K-8. "PI menggantikan DA" vs "ketiga kriteria tidak saling menggantikan" - konflik instruksi, bukan angka (SEDANG)

- Sisi A: `R3 - Gill:117-118`, `KATALOG-RUMUS.md:255`, `TEMPLATE-BERITA-ACARA.md:128` - bila
  uji PI dilakukan, uji DA tidak perlu lagi.
- Sisi B: `RANTAI-JAMINAN.md:29` (kriteria rasio + M ohm mutlak + tren) dan `:73-74` ("ketiga
  kriteria itu tidak saling menggantikan").
- Rekonsiliasi sah dari teks: yang tidak saling menggantikan adalah **rasio vs M ohm vs tren**;
  di dalam keluarga rasio, PI menggantikan DA. Rak TIDAK PERNAH menuliskan pembedaan ini
  eksplisit, sehingga pembacaan harfiah menghasilkan instruksi bertentangan (kerjakan DAR atau
  jangan kerjakan DAR).
- Anotasi terpasang: `RANTAI-JAMINAN.md:31-32`, `R3 - Gill:120-121`,
  `KATALOG-RUMUS.md:257-258`, `TEMPLATE-BERITA-ACARA.md:130-131`.
- Eksekusi: penegas resmi ditulis di objek ini (3.1), dengan rujukan PDF 659.

### K-9. Dua cakupan klaim "rantai terkuat" - inkonsistensi frasa, bukan angka (RENDAH)

- `RANTAI-JAMINAN.md:3` "rantai paling kuat di **rak ini**"; `:95` "paling kuat di **seluruh
  rak**". Domain POWER-BACKUP mengklaim UTUH pada baterai/ventilasi [R2] tetapi MENUNGGU R4
  pada genset dan UPS (`POWER-BACKUP/RANTAI-JAMINAN.md:136`), sehingga klaim "seluruh rak"
  bertahan secara substansi.
- Tidak ada angka yang terpengaruh. Anotasi `RANTAI-JAMINAN.md:99-100`.
- Perlakuan objek ini: SATU bentuk klaim, dipakai di Bagian 8 butir 1: "terkuat di rak, dengan
  dua celah normatif: MTS dan PUIL".

### K-10. Lokasi `_standar/` yang dikatalogkan tidak ada di pohon [`ekas/`](../../ekas-lapis-teks/) - cacat penamaan (RENDAH, terukur)

- `KATALOG-RUMUS.md:444-445`: lima standar "disimpan di subfolder `_standar/` dalam folder
  topiknya". Pencarian direktori `_standar` di seluruh [`ekas/`](../../ekas-lapis-teks/) (ukur ulang giliran L1):
  **0 direktori**.
- Kenyataan di disk: `03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/` (sesuai
  `REF-ELC-002.md:8`). Kolom `source_folder` `MASTER-REFERENCE-REGISTER.csv:6` menulis
  "Electrical Maintenance/_standar" - kemungkinan merujuk rak sumber asal (Mac), bukan [`ekas/`](../../ekas-lapis-teks/).
- Dampak: agen yang menuruti katalog mencari path yang tidak ada. Anotasi
  `KATALOG-RUMUS.md:448-449`. Perlakuan objek ini: semua path dinormalisasi ke nama folder nyata
  (Bagian 1 dan 6).

### Ringkasan predikat

| ID | Jenis | Berat | Teradjudikasi dari teks? | Aksi | Status objek ini |
|---|---|---|---|---|---|
| K-1 | Cakupan ambang vs contoh terhitung | TINGGI | Ya (dua jalur baris bertentangan) | Putusan controller/manusia | naik utuh, predikat CALON DEFECT SUBSTANTIF |
| K-2 | Caveat standar hilang di gerbang rilis | TINGGI | Ya | Tambal lapis hilir | caveat ditempel di SEMUA kemunculan angka |
| K-3 | Panduan tindakan dinaikkan jadi ambang lulus | TINGGI (lintas domain D4) | Ya di lapis teks; primernya perlu manusia | Adjudikasi PDF 246 | naik utuh + tanda lintas domain |
| K-4 | Baris 46 kV hilang di katalog | RENDAH | Ya | Sinkronkan bentuk | objek pakai bentuk lengkap 10 baris |
| K-5 | Baris -10 dan 25 derajat C hilang di katalog | SEDANG | Ya | Lengkapi katalog | objek pakai bentuk lengkap 6 baris |
| K-6 | "Empat ambang" vs dua yang didaftar | RENDAH | Tidak | Jangan naikkan angka | tercatat tanpa angka |
| K-7 | Bookmark 24 vs 17 entri | RENDAH | Tidak | Jangan klaim terverifikasi | tercatat sebagai tidak terverifikasi |
| K-8 | PI vs DA: instruksi bertentangan | SEDANG | Sebagian | Tulis penegas di objek IL | penegas ditulis di 3.1 |
| K-9 | "rak ini" vs "seluruh rak" | RENDAH | Ya | Satu bentuk klaim | satu bentuk dipakai di Bagian 8 |
| K-10 | Path `_standar/` tidak ada | RENDAH | Ya | Normalisasi path | semua path = nama nyata |

---

## Bagian 6 - Gap register domain

### 6.1 Celah resmi ber-ID (dari [`ekas/02_REGISTERS/GAP-REGISTER.csv`](../../ekas-lapis-teks/02_REGISTERS/GAP-REGISTER.csv), baris terukur)

| ID | Yang tidak ada | R | Prioritas / status | Isi baris csv | Arti untuk domain ini |
|---|---|---|---|---|---|
| GAP-001 | PUIL / SNI kelistrikan | R1 | TINGGI / terbuka (`:2`) | domain "ELECTRICAL, GROUNDING-LIGHTNING"; catatan: "ANSI/NETA menutup ambang uji, BUKAN kepatuhan hukum Indonesia" | Korpus TIDAK dapat menyatakan kepatuhan hukum Indonesia |
| GAP-008 | ANSI/NETA MTS (uji PEMELIHARAAN) | R2 | MENENGAH / terbuka (`:9`) | domain ELECTRICAL; catatan: "Yang ada ATS = uji TERIMA" | Semua ambang di rak = uji terima; program pemeliharaan berkala tidak bersandar |
| GAP-014 | Seluruh dokumentasi OEM | R4 | PER PROYEK / by-design (`:15`) | domain SEMUA | Tegangan uji pabrik, nilai isolasi yang ditetapkan pabrikan, torsi sambungan = "menunggu data pabrikan" |

### 6.2 Celah hasil sapuan (G-1..G-10, basis bukti bukan dugaan)

| ID | Yang tidak ada | Tingkat | Status register | Bukti di rak | Dampak untuk pemakaian objek ini |
|---|---|---|---|---|---|
| G-1 | **ANSI/NETA MTS** (uji pemeliharaan) | R2 | GAP-008 terbuka, MENENGAH (`GAP-REGISTER.csv:9`) | `RANTAI-JAMINAN.md:16-18,124-125`; `R2 - ...md:159-160`; `AMBANG-TERIMA-INDUK.md:83` | Semua ambang di rak = **uji terima**. Interval dan kriteria pemeliharaan berkala tidak bersandar |
| G-2 | **PUIL / SNI kelistrikan** | R1 | GAP-001 terbuka, TINGGI (`GAP-REGISTER.csv:2`) | `RANTAI-JAMINAN.md:13,102-104,124-125`; `AMBANG-TERIMA-INDUK.md:81`; `AUTHORITY-STATUS.md:31` | Kepatuhan hukum Indonesia BELUM bersandar; ATS bukan pengganti |
| G-3 | **R1 = 0 sumber global; R4 = 0 sumber global** | R1/R4 | by-design untuk R4 (GAP-014) | `ekas/00_START-HERE/README.md:34-38` (R1 0, R2 5, R3 24, R4 0, R5 8) | Rantai "terkuat" sekalipun tidak punya landasan regulasi nasional |
| G-4 | **Ambang tahanan isolasi untuk mesin berputar** | - | TIDAK terdaftar di GAP-REGISTER (gap baru, usulan) | judul Tabel 100.1 `R2 - ...md:41-42`; kolom `:67`; contoh `RANTAI-JAMINAN.md:64` | Turunan K-1. Perlu IEEE 43 atau setara - tidak ada di rak |
| G-5 | **Angka tabel ATS lain** (100.2, 100.5, 100.8, 100.9, 100.10, 100.13, 100.15-100.17, 100.21) | R2 | tidak terdaftar (bagian dari kelengkapan resume) | `R2 - ...md:106-117` - hanya nomor tabel + nomor cetak, tanpa nilai | Objek TIDAK boleh mengklaim cakupan switchgear withstand, vibrasi, SF6, dsb. |
| G-6 | **Kelas tegangan menengah Indonesia (mis. 20 kV) di Tabel 100.1** | - | tidak terdaftar (gap baru, usulan) | tabel hanya 15.000 dan 25.000 (`R2 - ...md:52-53`) | Pemilihan baris untuk 20 kV = keputusan yang ditulis di BA, bukan diimplikasikan |
| G-7 | **Torque sambungan listrik** | R4 | tidak terdaftar (padanan CIVIL-STRUCTURAL: "tidak ada di rak") | grep `torque`/`torsi` di ELECTRICAL = 0 (diukur); `CIVIL-STRUCTURAL/RANTAI-JAMINAN.md:103` | Nyatakan "menunggu data pabrikan"; jangan isi angka umum |
| G-8 | **Interval uji berkala instalasi listrik** | - | implisit di GAP-008 | kata `interval` = 0 kemunculan di `ELECTRICAL/` (diukur ulang) | Jangan impor interval dari domain lain (triwulanan IEEE 1188 = baterai) |
| G-9 | **Contoh pelaksanaan elektrikal (BA nyata, kalkulasi, ITP)** | - | tidak ada artefak | TEST/CALCULATION/REQUIREMENT/EVIDENCE-REGISTER.csv: **0 baris domain ELECTRICAL** (diukur ulang); `08_EVIDENCE/` dan `09_HANDOVER/` tidak memuat berkas elektrikal | Domain ini murni lapisan pengetahuan; belum ada jejak penerapan. Bandingkan FIBER-OPTIC yang punya suite P00 |
| G-10 | **PDF primer tidak ada di pohon [`ekas/`](../../ekas-lapis-teks/)** | - | kondisi struktural korpus | `03_SOURCE-VAULT/.../ANSI-NETA/` dan `.../ELECTRICAL/` hanya berisi `_ISI.md`; PDF di `C:/Users/TRIAL/gsp-ekas/lengkap/` | Verifikasi halaman per angka = tugas manusia; agen berhenti di lapisan teks |

### 6.3 Cara pakai objek ini (empat langkah, mengikuti `AMBANG-TERIMA-INDUK.md:107-113`)

1. Cari jenis ujinya di Bagian 4.1. Bila jenis uji tidak ada di sana, cek Bagian 6 - kalau
   masih tidak ada, ia TIDAK punya sandaran: jangan pakai angka.
2. Salin **angka + sumber + halaman + tingkat R** ke prosedur uji / berita acara. Rujukan yang
   diminta rak: "sebutkan barisnya, bukan hanya nama standarnya" (`RANTAI-JAMINAN.md:114`).
3. Bila jatuh di baris R3 (PI, DAR, batas tegangan uji rutin) - **periksa kontraknya dulu**,
   sebelum uji, dan tulis pasalnya (`AMBANG-TERIMA-INDUK.md:69,111`). Bentuk "sesuai praktik
   industri" ditolak (`:71`).
4. Bila jatuh di "belum ada sumber sah" (PUIL, MTS, resistansi pembumian) - pilih satu dari
   tiga jalan sah dan tulis pilihannya di berita acara (`AMBANG-TERIMA-INDUK.md:79,112-113`).
   Untuk angka melekat produk: tulis "menunggu data pabrikan", tandai `MENUNGGU R4` (`:102-103`).

Tiga aturan pakai tambahan yang spesifik domain ini:

- **Selalu bawa pasangan.** Gill memberi metode/rasio, ATS memberi angka mutlak. Memakai salah
  satu sendirian menghasilkan vonis cacat: Gill tidak memberi ambang M ohm
  (`R3 - Gill:155-158`), ATS tidak memberi metode (`R2 - ...md:32-33`).
- **Selalu bawa caveat.** Tabel 100.1 bersyarat (K-2); Tabel 100.18 adalah panduan tindakan
  (K-3); PI/DAR butuh adopsi kontrak tertulis (R3).
- **Jangan menyeberang batas domain.** Angka baterai/UPS/genset/pembumian tidak dimiliki objek
  ini walau satu rak (BATAS DOMAIN N-13 + Bagian 8 butir 9).

### 6.4 Yang justru KUAT di rak ini (agar objek tidak timpang)

1. **Satu-satunya domain dengan ambang R2 yang sah** (dengan caveat). Ambang induk `:15-17`
   memberi tiga baris R2 centang ya; domain NETWORKING dan STORAGE justru "UTUH pada
   perhitungan, TANPA SANDARAN NORMATIF pada ambang" (`identification/01_translated.md:143`
   butir F-6).
2. **Offset halaman teruji internal** (+19, 3/3 - 2.3). Tidak ada domain lain yang membuktikan
   offset-nya sekuat ini.
3. **Pemisahan peran buku vs standar eksplisit dan konsisten**: Gill terbuka menyatakan tidak
   memberi ambang mutlak (`R3 - Gill:155-158`); ATS terbuka menyatakan dirinya bukan pengganti
   PUIL (`R2 - ...md:156-158`).
4. **Batas cakupan tertulis di tiga lapis sekaligus** (`AUTHORITY-STATUS.md:29-31`,
   `REF-ELC-002.md:50`, `ASUMSI-BAKU.md:159-161`) - termasuk peringatan bahwa NETA sering
   disalahgunakan sebagai dasar ambang pembumian.
5. **Asumsi yang seharusnya sudah gugur didaftar dan digantikan** (`ASUMSI-BAKU.md:146-148`) -
   mekanisme anti-duga berjalan, bukan sekadar imbauan.
6. **Kerangka bukti serah operasional** (`RANTAI-JAMINAN.md:110-119` +
   `TEMPLATE-BERITA-ACARA.md:105-131`) sampai tingkat "sebutkan barisnya, bukan hanya nama
   standarnya".

### 6.5 Higienis laci R4 elektrikal

Laci `R4_OEM-TECHNICAL` kosong secara global (README: R4 = 0 sumber). Untuk domain ini tepat
by-design (GAP-014: angka melekat produk diminta per proyek), tetapi berarti **setiap** angka
tegangan uji khusus pabrikan, nilai isolasi yang ditetapkan pabrikan, dan torsi sambungan
adalah "menunggu data pabrikan" - bukan menunggu riset pustaka.

---

## Bagian 7 - Kata kunci rute (16 token)

Tag beku objek ini (daftar beku G-1 seksi 4, byte-per-byte; frontmatter tetap otoritatif,
bagian ini hanya mirror):

`electrical, kelistrikan, isolasi, tahanan-isolasi, pi, dar, polarization-index,
dielectric-absorption-ratio, neta-ats, ats-2017, tabel-100.1, tegangan-uji-dc, koreksi-suhu,
uji-terima, mts-absen, megger` = 16 token.

| Token | Padanan kerja harian | Jangkar isi |
|---|---|---|
| electrical / kelistrikan | uji instalasi listrik, serah terima panel | seluruh objek |
| isolasi / tahanan-isolasi | "isolasi masih layak atau tidak" | Bagian 2-4; `RANTAI-JAMINAN.md:41,47,68` |
| pi / polarization-index | rasio 10 menit / 1 menit | [R3, Gill, PDF 144]; `R3 - Gill:109-115` |
| dar / dielectric-absorption-ratio | rasio 60 s / 30 s | [R3, Gill, PDF 144]; `R3 - Gill:96-103` |
| neta-ats / ats-2017 | ambang uji terima | [R2, ANSI/NETA ATS-2017]; `R2 - ...md:39-95` |
| tabel-100.1 | M ohm minimum per tegangan nominal | [R2, ANSI/NETA ATS-2017, PDF 223]; 2.2 A |
| tegangan-uji-dc | 500 / 1.000 / 2.500 / 5.000 V uji | [R2, ANSI/NETA ATS-2017, PDF 223]; 2.2 A |
| koreksi-suhu | normalisasi ke 20 derajat C | [R2, ANSI/NETA ATS-2017, PDF 241]; 2.2 B |
| uji-terima | ATS bukan MTS | `AUTHORITY-STATUS.md:29`; `R2 - ...md:13-15` |
| mts-absen | celah program pemeliharaan | GAP-008; `GAP-REGISTER.csv:9`; G-1 |
| megger | alat ukur + sertifikat kalibrasinya | [R3, Gill, PDF 48]; `R3 - Gill:46-47`; `RANTAI-JAMINAN.md:117` |

Catatan jujur: istilah yang sering dipakai praktisi - `termografi`, `delta-t`, `hipot`,
`step-voltage`, `torsi` - TIDAK termasuk daftar beku G-1 untuk D3. Dua di antaranya sengaja
bukan milik domain ini: `termografi` dan `delta-t` dirutekan ke D4
(`thermal-korpus-ekas-0923`, pemilik Tabel 100.18 sebagai ambang aksinya), `torsi` tidak punya
muatan di rak sama sekali (G-7). `hipot` dan `step-voltage` hidup di dalam objek ini sebagai
metode ([R3, Gill, PDF 142]) dan rutenya lewat token `isolasi`. Perubahan daftar tag =
amandemen G-1 lewat kartu + Decision Log, bukan suntingan senyap.

---

## Bagian 8 - BATAS PENGETAHUAN / status rantai

Blok ini wajib ikut terbit bersama angkanya. Objek yang hanya berisi angka enak-dibaca tapi
menyembunyikan celah = gagal maksud registrasi dan menabrak aturan EKAS ("jawab tidak ada di rak
daripada mengarang").

1. **Status rantai apa adanya (tanpa perataan).** `RANTAI-JAMINAN.md:121` mencetak: "Status
   rantai: UTUH. Satu-satunya rantai di rak ini yang ambang, metode, dan koreksinya seluruhnya
   bersandar sumber tertulis - dan dua di antaranya [R2]." Satu bentuk klaim kekuatan yang
   dipakai objek ini (rekonsiliasi K-9): **terkuat di rak, dengan dua celah normatif: MTS dan
   PUIL.** ATS = uji terima, BUKAN MTS pemeliharaan (`AUTHORITY-STATUS.md:29`;
   `R2 - ...md:13-15,159-160`).
2. **R1 = 0 dan R4 = 0 global.** Keadaan rak: R1 = 0, R2 = 5, R3 = 24, R4 = 0, R5 = 8
   [peta rak: `ekas/00_START-HERE/README.md:34-38`]. Arti (README `:41-43`): korpus dapat
   merancang, menghitung, dan menetapkan ambang uji, TETAPI TIDAK dapat menyatakan kepatuhan
   hukum Indonesia dan TIDAK dapat menyebut angka produk tanpa bahan dari luar. R4 tidak perlu
   diadakan (by-design, per proyek); R1 perlu diadakan (`:45-49`).
3. **Angka R2 pun bersyarat.** Tabel 100.1 berlaku "bila tidak ada standar konsensus lain" dan
   spesifikasi pabrikan mendahuluinya (`R2 - ...md:57-59,161-162`) - kehilangan klausul ini di
   lapis hilir adalah K-2. Tabel 100.18 adalah panduan tindakan, bukan batas mutlak
   (`R2 - ...md:93-95`) - penghilangan klausul ini adalah K-3. PI < 1 dan DAR < 1,25 adalah R3
   dan HANYA sah bila kontrak mengadopsinya tertulis (`AMBANG-TERIMA-INDUK.md:61-62,69`).
   Dilarang meratakan R2 dan R3 menjadi "standar" (`:52-53`).
4. **Known-defect yang wajib ikut terangkut.** K-1 (contoh motor vs tabel non-berputar) berstatus
   CALON DEFECT SUBSTANTIF menunggu putusan manusia - anotasi terpasang di
   `RANTAI-JAMINAN.md:76-77`, isi rak TIDAK diubah. K-2 dan K-3 sudah dianotasi di lapis hilir
   (K-2) tetapi K-3 BELUM dianotasi di `THERMAL/RANTAI-JAMINAN.md` (terukur 0 blok) dan
   membutuhkan adjudikasi PDF 246 oleh manusia. K-6 dan K-7 tidak dapat diputus dari teks dan
   tidak menaikkan angka apa pun. Bentuk lama tidak dihapus di mana pun, hanya ditandai.
   Semua vonis halaman berstatus BELUM TERKONFIRMASI terhadap sumber primer (SPK-002 butir 1:
   kesetiaan hulu bukan bukti benar).
5. **GAP register yang mengikat domain:** GAP-001 (PUIL/SNI, TINGGI - NETA menutup ambang uji,
   BUKAN kepatuhan hukum Indonesia), GAP-008 (NETA MTS, MENENGAH - yang ada ATS = uji TERIMA),
   GAP-014 (R4 by-design, angka melekat produk diminta per proyek). Plus tujuh celah hasil
   sapuan G-4..G-10 di Bagian 6.2, semuanya berbasis bukti ukur, bukan dugaan.
6. **Interval uji TIDAK bersandar.** Kata `interval` = 0 kemunculan di rak ELECTRICAL (diukur).
   Jangan mengimpor triwulanan IEEE 1188 (itu baterai, domain POWER-BACKUP). Jalan sah yang
   ada: FFI Moubray [R3, PDF 198] milik domain RCM (`RCM/RANTAI-JAMINAN.md:60-67`), yang
   menuntut sasaran MTBF majemuk dari pemilik (`ASUMSI-BAKU.md:129`).
7. **Peringatan usia buku (F-7).** Gill 2008 = 18 tahun (penanda usia rak ikut dikutip apa
   adanya: `RANTAI-JAMINAN.md:12` menulis tingkat R3 disertai peringatan "18 th"; glif
   peringatan rak ditulis deskripsi agar berkas tetap ASCII). Konsekuensi yang rak nyatakan
   sendiri (`R3 - Gill:183-184`): untuk hal yang mengacu edisi standar lain (NFPA 70E, IEEE),
   periksa apakah ada revisi terbaru SEBELUM mengutip angka batas ke dokumen resmi. ATS-2017
   edisi 2017 = 9 tahun; periksa revisi sebelum kontrak mengadopsi.
8. **Torque dan angka pabrikan: menunggu R4.** Tidak ada angka torsi sambungan listrik di rak
   (G-7); tegangan uji pabrik dan nilai isolasi yang ditetapkan pabrikan adalah R4
   (`AMBANG-TERIMA-INDUK.md:91-103`). Tulis "menunggu data pabrikan", jangan isi angka umum.
9. **Batas cakupan D3 (N-13) dan domain tetangga HANYA rujukan silang, tidak disalin (P-8).**
   Yang terdaftar: uji instalasi dan peralatan listrik (ATS-2017 + Gill). Yang BUKAN:
   UPS/baterai/genset -> [`ekas/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/POWER-BACKUP/) (Rantai C; status rantainya
   sendiri "UTUH pada baterai dan ventilasi [R2]. MENUNGGU R4 pada genset dan UPS",
   `POWER-BACKUP/RANTAI-JAMINAN.md:136`); proteksi petir dan pembumian ->
   [`ekas/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/GROUNDING-LIGHTNING/) (Rantai D; resistansi pembumian tidak punya
   R1 maupun R2 di rak, `AMBANG-TERIMA-INDUK.md:79`). Rujukan silang aktif: THERMAL
   [`ekas/05_DOMAIN-KNOWLEDGE/THERMAL/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/THERMAL/) memakai tabel yang sama (Tabel 100.18) dan vonis K-3
   berlaku untuk keduanya; RCM [`ekas/05_DOMAIN-KNOWLEDGE/RCM/`](../../ekas-lapis-teks/05_DOMAIN-KNOWLEDGE/RCM/) memegang rumus interval (FFI).
   Kata kunci yang TIDAK boleh ditarik oleh slug `#electrical-korpus`: UPS, baterai, genset,
   ventilasi ruang baterai, resistansi pembumian, rolling sphere.
10. **Sumber dan kebaruan.** Seluruh angka berasal dari lapisan teks [`ekas/`](../../ekas-lapis-teks/) diekstrak read-only
    2026-09-24; tidak ada PDF primer yang dibuka - verifikasi per halaman wewenang manusia
    (PDF asli di `C:/Users/TRIAL/gsp-ekas/lengkap/03_SOURCE-VAULT/`). `ekas/`, `vault/`,
    `wiki/`, `profiles/` read-only selama giliran ini - objek ini tidak mengubah rak. Nomor
    baris `RANTAI-JAMINAN.md` (125 baris), `R3 - Gill` (185), `KATALOG-RUMUS.md` (598),
    `AMBANG-TERIMA-INDUK.md` (110), `ASUMSI-BAKU.md` (183), `TEMPLATE-BERITA-ACARA.md` (269)
    memakai versi PASCA-tambalan D3-FIXx; pemetaan ke nomor studi (versi prapatch) ada di
    Bagian 1.1a.

STATUS: complete
