---
id: expo-2026-intel
type: catatan
title: "Dataset EXPO-INTEL-2026: 325 expo 2026, 5 region, 19 klaster, tier T1-T5"
sumber: collection/expo2026/finalisasi/master-final-v3.csv
tanggal_akses: 2026-09-02
kelas_bukti: sintesis
sensitif: tidak
perkara: expo-intel-2026
tags: [expo, 2026, intel, katalog, tier]
links: [collection/expo2026/expo-intel-2026.xlsx, collection/expo2026/library-proposal.md]
penulis: gsp-librarian
diajukan: 2026-09-03
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
status: active
catatan_verifikasi: "Verdict terverifikasi, 7 dimensi lolos. Provenans dan angka terlacak: 23 cek rekalkulasi independen langsung dari master-final-v3.csv cocok semua, yaitu 325 baris EXPO-001 sampai EXPO-325, region USA 125 Europe 90 Asia 53 China 42 Australia 15, tier T1 2 T2 18 T3 20 T4 78 T5 207, penghuni T1 EXPO-083 WAIC skor 91 dan EXPO-132 Eurosatory skor 87 keduanya Estimasi=no, status 169 lewat 156 mendatang nol batal-tunda, estimasi 105 yes 220 no, versi 269 v1 35 v1-patch 16 v2-baru 5 v3-baru, 19 klaster dengan minimum K13 sebanyak 6 baris, tag T-DEF 31 INFRA-DATA 16 INFRA-QT 2, 732 URL unik sama dengan 732 baris sheet Sources, aritmetika skor dan pemetaan tier 0 salah dari 325 baris, nol Estimasi=yes di T1, workbook 186348 byte sha256 berawalan 71430bbaee341752 dengan 4 sheet urut. Anti-karangan: lima berkas RAW dibuka langsung (master-final-v3.csv, verify-report.txt, f2-verify-report.txt, countersign.md, f2-methodology-export.txt) plus pengukuran ukuran 10 artefak tabel seksi 5, semuanya cocok di disk dan seluruh locator [R-n] terbukti ada isinya, tidak ada klaim karangan. Metadata: yaml.safe_load lulus, nilai tidak terpotong kelas dua, title sama persis dengan H1 pertama, satu baris status, field taksonomi lengkap. Dedup bersih, id dan judul unik di antara 1568 objek vault dan nol temuan di wiki 727 berkas. Grouping perkara expo-intel-2026 sesuai isi dokumen. Gate non-sensitif dan non-dosir tepat, sehingga verifikasi kualitas ini tidak menggantikan gerbang attest librarian. Catatan untuk kurator dan bukan cacat objek, field opsional domain dan halaman absen padahal 1068 dari 1568 objek vault lain memakainya, dan halaman memang tidak berlaku karena sumber berupa CSV tanpa halaman; skrip l29_stats.py yang dikutip seksi 4 tersimpan di workspace kartu t_302f4c70 bukan di shared workspace sehingga jejak hitungnya tidak bisa dibuka pembaca wiki, sebaiknya disalin ke collection/expo2026/finalisasi saat promosi; kolom Bukti_ukuran kosong pada 181 baris termasuk anchor T1 EXPO-083 walau Estimasi=no, kolom itu bukan klaim objek ini tetapi layak masuk daftar keterbatasan."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: catatans/expo-2026-intel.md
---

# Dataset EXPO-INTEL-2026: 325 expo 2026, 5 region, 19 klaster, tier T1-T5

Ekstraksi verbatim seksi 1 sampai 6 proposa library-proposal.md (task_ref t_302f4c70); kunci rujukan [R-n] didefinisikan pada tabel di akhir seksi 5. Dataset penuh tidak disalin ke vault; objek ini adalah rekaman rujukan.

## 1. Ringkasan usulan

Objek yang diusulkan adalah satu entri indeks dataset dengan id stabil `expo-2026-intel` bertipe `catatan`, yaitu rekaman rujukan terhadap hasil akhir misi EXPO-INTEL-2026 berupa katalog 325 acara pameran dan konferensi tahun 2026 lintas lima region dan 19 klaster bidang [R-8] yang dilengkapi skor rubrik empat dimensi serta tier T1 sampai T5. Alternatif tipe `fakta` tetap terbuka bagi kurator karena taksonomi library bersifat skema diamati, sehingga penyesuaian tipe dinilai dari isi objek dan bukan dari daftar tipe mati.

Yang dipromosikan ke vault hanyalah rekaman ringkas ini beserta provenans, metodologi, statistik, dan rujukan path, sedangkan dataset penuh sengaja tidak disalin ke vault sesuai instruksi kartu L29 dan prinsip vault sebagai lapisan rujukan untuk artefak besar. Klasifikasi gerbang objek ini adalah non-sensitif karena seluruh isinya merupakan data acara publik yang bersumber dari web resmi, dan bukan perkara dosir, sehingga setelah verifikasi custodian objek dapat langsung di-attest tanpa approval-ref maupun verification-by.

Karena aturan gatekeeper melarang librarian meng-attest tulisannya sendiri untuk klaim kuat, proposa yang disusun oleh gsp-librarian ini wajib melewati verifikasi custodian lebih dulu sebelum promosi berjalan.

## 2. Provenans

Misi penghasil dataset adalah EXPO-INTEL-2026 dengan kontrak orkestrasi tercatat pada `docs/2026-09-02-expo-intel-2026/contract.md`, yang bertujuan melakukan penelusuran recall-maksimal expo 2026 yang sudah lewat maupun mendatang di region USA, Europe, Asia, China, dan Australia untuk 19 klaster bidang, lengkap dengan klasifikasi rubrik empat dimensi dan sajian workbook Excel profesional [R-6]. Tanggal akses seluruh sumber seragam pada 2 September 2026 sebagai hari-H laporan misi, kolom Sumber pada master membawa stempel akses per URL, dan sheet Sources mendaftarkan 732 URL unik hasil dedup lintas baris [R-1][R-2].

Metode pengumpulannya berupa pengumpulan web terstruktur gelombang B1 sampai B7 oleh 18 kartu pengumpul yang dibagi per bucket tema lalu per region lewat jalur sumber gratis, dengan ddgs backend bing dan probe curl ke situs resmi penyelenggara sebagai ujung tombak serta direktori pihak ketiga hanya sebagai penanda verifikasi [R-6]. Alur hilirnya adalah konsolidasi tanpa duplikat pada fase K21, skor rubrik pada K22, tinjau ulang analis kedua pada K23, penguncian identitas EXPO-001 sampai EXPO-304 pada K24, pengisian celah oleh kartu G1, G2, dan G3 serta kalibrasi oleh E1 dan E2, lalu finalisasi F1 yang menghasilkan master-final-v2.csv sebanyak 320 baris dan finalisasi F2 yang menghasilkan master-final-v3.csv sebanyak 325 baris berikut rebuild workbook [R-6][R-7 bagian 2 dan 8].

Rantai verifikasinya tertutup rapat: skrip deterministik `docs/2026-09-02-expo-intel-2026/verify_expo26.py` atas v3 menghasilkan sembilan CHECK PASS dengan baris akhir VERDICT PASS pada laporan `finalisasi/verify-report.txt` pukul 23:40, validasi build F2 pada `finalisasi/f2-verify-report.txt` PASS enam CHECK, verifier naratif V27 memvonis PASS, dan countersign V28 oleh gsp-pm-verifier menyatakan AGREE penuh atas seluruh vonis dengan penghitungan ulang independen atas region, klaster, aritmetika skor, serta enam sampel baru di luar sampel V27 [R-3][R-4][R-5].

Kelas bukti objek ini adalah sintesis, yaitu analisis lintas sumber web resmi, direktori, dan berita dengan penanda estimasi per baris, sementara sumber primer tiap baris tetap tercatat pada kolom Sumber dan sheet Sources.

## 3. Metodologi rubrik

Penilaian memakai empat dimensi setara tanpa pembobotan karena keempat kriteria diminta setara oleh pemilik misi, yaitu Popularitas P, Ukuran U, Eksposur E, dan Eksibitor X, masing-masing bernilai 0 sampai 25 dalam lima band (21-25, 14-20, 7-13, 1-6, 0), dan jumlahan keempatnya menentukan tier T1 pada rentang 85 sampai 100, T2 pada 70 sampai 84, T3 pada 50 sampai 69, T4 pada 25 sampai 49, serta T5 pada 1 sampai 24 [R-7 bagian 5 dan 9-12].

Aturan anti-estimasi melarang angka tanpa sumber masuk skor, mewajibkan nilai perkiraan atau turunan edisi sebelumnya diberi tanda tilde sehingga barisnya berstatus Estimasi=yes, membatasi dimensi yang seluruh buktinya estimasi pada skor maksimal 20 sesuai cap TA-D5, dan melarang baris berestimasi menempati tier T1, dengan nol pelanggaran pada seluruh 325 baris saat validator F2 memeriksa ulang [R-7 bagian 3-4][R-4 CHECK 5]. Kelas Status memakai patokan hari-H 2 September 2026 sehingga pemisahan acara lewat dan mendatang bersifat deterministik: acara lewat mengambil bukti ukuran dari halaman hasil atau siaran pers pasca-acara, sedangkan acara mendatang memakai halaman edisi 2026 atau angka edisi sebelumnya yang wajib bertanda est-dari-edisi-sebelumnya [R-7 bagian 13].

Definisi masuk dan keluar expo dengan lima tipe masuk E1 sampai E5 dan lima tipe keluar X1 sampai X5, aturan dedup, serta enum region mengikat mengikuti SCHEMA misi yang dipublikasikan controller [R-9].

## 4. Statistik cakupan

Seluruh statistik di bawah dihitung ulang langsung dari master-final-v3.csv pada 2 September 2026 pukul 23:57 WIB memakai skrip `l29_stats.py`, bukan disalin dari handoff, dan hasilnya cocok dengan laporan verifier [R-1][R-3]. Total baris unik ada 325 dengan identitas EXPO-001 sampai EXPO-325, tersebar atas USA 125 baris, Europe 90 baris, Asia 53 baris, China 42 baris, dan Australia 15 baris [R-1][R-3 CHECK 1]. Komposisi tier mencatat T1 dua baris, T2 18 baris, T3 20 baris, T4 78 baris, dan T5 207 baris, dengan dua penghuni T1 yaitu EXPO-083 WAIC 2026 World Artificial Intelligence Conference berskor 91 dan EXPO-132 Eurosatory 2026 berskor 87 yang keduanya berstatus Estimasi=no [R-1][R-3].

Distribusi status mencatat 169 baris lewat dan 156 baris mendatang dengan nol batal-tunda, distribusi estimasi mencatat 105 baris yes dan 220 baris no, sedangkan distribusi versi mencatat 269 baris v1, 35 baris v1-patch hasil kalibrasi E1 dan E2, 16 baris v2-baru dari F1, dan 5 baris v3-baru dari F2 [R-1]. Sembilan belas klaster K01 sampai K19 seluruhnya berada di atas ambang tiga baris dengan minimum K13 Simulasi dan pelatihan sebanyak 6 baris, disertai tag tambahan T-DEF pada 31 baris, INFRA-DATA pada 16 baris, dan INFRA-QT pada 2 baris [R-1][R-3 CHECK 2].

Kolom Sumber memuat 732 URL unik yang cocok satu banding satu dengan 732 baris sheet Sources workbook, dan workbook itu sendiri berukuran 186.348 byte dengan awalan sha256 71430bbaee341752 serta empat sheet berurutan Master, Ranking_Tier, Methodology, dan Sources [R-1][R-2][R-4].

## 5. Rujukan path artefak

Tabel pertama di bawah membekukan artefak kanonik yang dirujuk objek vault, semua path relatif terhadap shared workspace `C:/Users/TRIAL/workspace/gsp-hermes/workspace/`, dengan ukuran yang terverifikasi di disk pada sesi ini melalui listing berkas dan fungsi pengukur ukuran. Objek vault akan menautkan berkas-berkas ini apa adanya tanpa menyalin isinya, karena substrat dataset terlalu besar untuk lapisan vault dan tetap dapat dibangun ulang dari RAW. Kunci rujukan berformat [R-n] yang dipakai seluruh dokumen ini dijelaskan pada tabel kedua setelah daftar artefak. Pembaca wiki cukup memakai kedua tabel ini untuk menelusuri setiap klaim angka kembali ke berkas asalnya tanpa dokumen pendamping.

| Artefak | Path (relatif shared workspace) | Ukuran | Peran |
|---|---|---|---|
| Master final v3 | collection/expo2026/finalisasi/master-final-v3.csv | 316.924 B | dataset kanonik 325 baris x 28 kolom |
| Workbook | collection/expo2026/expo-intel-2026.xlsx | 186.348 B | sajian profesional 4 sheet |
| Laporan verifikasi deterministik | collection/expo2026/finalisasi/verify-report.txt | 1.139 B | VERDICT PASS 9 CHECK |
| Laporan validasi build F2 | collection/expo2026/finalisasi/f2-verify-report.txt | 892 B | VERDICT PASS 6 CHECK |
| Countersign V28 | collection/expo2026/verification/countersign.md | 9.909 B | AGREE penuh vonis V27 |
| Methodology workbook (teks) | collection/expo2026/finalisasi/f2-methodology-export.txt | 37.990 B | prosa metodologi 19 bagian |
| Kontrak misi | docs/2026-09-02-expo-intel-2026/contract.md | 12.020 B | provenans orkestrasi dan decision log D-01 sampai D-13 |
| Taksonomi RT | docs/2026-09-02-expo-intel-2026/identification/01_translated.md | 39.935 B | 19 klaster kanonik, definisi, jendela waktu |
| Blueprint TA | docs/2026-09-02-expo-intel-2026/identification/02_structured.md | 30.306 B | rubrik, schema, DAG |
| SCHEMA pengumpul | collection/expo2026/SCHEMA.md | 5.716 B | aturan kolom, region, dedup |

Adapun berkas `collection/expo2026/master-final.csv` berisi 304 baris dan `finalisasi/master-final-v2.csv` berisi 320 baris adalah artefak pra-finalisasi yang disuperseded dan tidak boleh lagi dirujuk sebagai kanonik. Kartu L29 menyebut master-final.csv sebagai input karena kartu tersebut dibuat sebelum fase F1 dan F2 berjalan, sehingga berkas kanonik ketika proposa ini ditulis sudah bergeser ke v3. Selisih itulah sebabnya proposa ini membeku master-final-v3.csv dan seluruh statistik seksi 4 dihitung ulang darinya, bukan dari master-final.csv. Penamaan versi pada kolom `versi` memungkinkan pembaca memilah baris asli, hasil kalibrasi, dan baris pengisian celah tanpa membuka dokumen lain.

| Kode | Sumber |
|---|---|
| R-1 | collection/expo2026/finalisasi/master-final-v3.csv (dihitung ulang skrip l29_stats.py, 2026-09-02 23:57 WIB) |
| R-2 | collection/expo2026/expo-intel-2026.xlsx |
| R-3 | collection/expo2026/finalisasi/verify-report.txt |
| R-4 | collection/expo2026/finalisasi/f2-verify-report.txt |
| R-5 | collection/expo2026/verification/countersign.md |
| R-6 | docs/2026-09-02-expo-intel-2026/contract.md |
| R-7 | collection/expo2026/finalisasi/f2-methodology-export.txt (penomoran bagian mengikuti berkas) |
| R-8 | docs/2026-09-02-expo-intel-2026/identification/01_translated.md |
| R-9 | collection/expo2026/SCHEMA.md |

## 6. Batas dan keterbatasan

Penilaian ini berbasis bukti terdokumentasi per tanggal akses dan bukan pengukuran lapangan, dan inilah keterbatasan utama dataset yang wajib ikut terbit bersama entri wiki: ketiadaan bukti tidak kami artikan sebagai ketiadaan aktivitas pameran, dan skor baris berestimasi dapat bergeser setelah katalog resmi edisi 2026 terbit [R-7 bagian 18]. Pengecualian region ditetapkan tegas lewat keputusan D-05 kontrak sehingga dataset ini bukan daftar global utuh: kawasan Teluk keluar beserta IDEX, UMEX, WATE, GITEX Dubai, dan Intersec, Selandia Baru keluar karena region Australia dihitung sebagai negara Australia saja, Turki masuk Asia, Hong Kong dan Makau masuk China, sementara event Taiwan masuk Asia dengan nilai Negara Taiwan [R-6][R-9].

Temuan terbuka yang dibawa dari countersign V28 tidak membatalkan vonis tetapi wajib dicatat: header v3 memuat kolom `versi` dua kali sehingga berkas membawa 29 medan versus 28 kolom terdokumentasi yang bersifat kosmetik, akhir rentang I/ITSEC berbeda antar direktori dengan master memakai 3 Desember, `cakupan-gap.md` belum disegarkan ke v3, tautan EXPO-167 Bucharest mati 404 sebagai satu-satunya mati dari 37 probe CHECK 7, dan keputusan reviewer masih terbuka untuk anchor T1 EXPO-132 berskor 87 yang deviasi dari contoh anchor blueprint serta dua baris tepat di batas skor 50 [R-3][R-5].

Bila pemilik misi suatu saat menginginkan kawasan Teluk atau Selandia Baru, jalur yang sah adalah amandemen lingkup disertai misi pengumpulan baru, bukan perluasan sepihak atas dataset yang sudah dikunci ini [R-7 bagian 18].
