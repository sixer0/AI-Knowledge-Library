---
name: mw-ammunition-storage
description: "Norma gudang amunisi per subsistem, angka berrujukan."
version: 1.0.6
author: GSP (PT. Gemilang Satria Perkasa) - gsp-skill-creator
license: MIT
metadata:
  hermes:
    tags: [gsp, ammunition, storage, iatg, safety, engineering]
    category: gsp
---

# Skill Global: Penyimpanan Gudang Amunisi Militer (mw-ammunition-storage)

Paket pengetahuan per-subsistem ini dirakit dari delapan register ekstraksi (enam partisi hulu plus dua tambalan celah GAP) yang dibekukan di atas korpus 49 berkas pada tanggal baseline, dan setiap angka di dalamnya membawa penanda rujukan yang resolve ke satu baris register beku. Komposisi korpusnya adalah 43 berkas berlabel IATG dengan 40 nomor judul unik, 4 publikasi berlabel NATO yang terverifikasi sebagai publikasi PBB, 1 regulasi ATF Amerika Serikat, serta 1 draf internal GSP yang kelas asalnya dipisahkan secara eksplisit.

Susunan bab mengikuti nomor seri subsistem sumber dan bukan urutan per-dokumen, sehingga satu dokumen dapat terurai ke beberapa bab sesuai topik normanya. Prosa ditulis dalam bahasa Indonesia formal sementara istilah teknis, nomor seri, judul dokumen, dan kutipan verbatim dipertahankan apa adanya agar makna teknis tidak bergeser.

## Cara membaca (routing pembaca)

| Jalur | Untuk siapa | Langkah |
|---|---|---|
| Cepat | butuh keputusan praktik | buka bab subsistem terkait di bawah, baca blok bernomor rujukan |
| Penyusun angka | butuh nilai + satuan + kelas asal | [`references/register.md`](references/register.md) bagian bab, atau grep `reg_id` di [`references/register.jsonl`](references/register.jsonl) |
| Pemeriksa angka | menguji kebenaran satu angka | ambil `reg_id`, cocokkan `dokumen` + `halaman` pada baris itu, buka berkas korpus bila tersedia; tanya-jawab tersering di [`references/qa-pemeriksa.md`](references/qa-pemeriksa.md) |

Telusur wajib berhenti dalam dua langkah karena prosa selalu menutup pernyataan bernilai dengan penanda rujukan, penanda itu menunjuk satu `reg_id`, dan baris register tersebut memuat pasangan berkas serta nomor halaman tempat angka ditemukan. Jalur cepat dipakai untuk keputusan praktik sehari-hari tanpa membuka register, sedangkan jalur penyusun angka dipakai ketika satuan atau kelas asal perlu dipastikan sebelum memasukkan nilai ke perhitungan. Jalur pemeriksa angka dipakai saat ada keberatan atas satu butir tertentu dan memerlukan pembacaan ulang halaman sumbernya. Berkas pendukung lain yang membentuk rantai bukti paket ini adalah silsilah dokumen, tabel manusia register, berkas mesin register, tanya-jawab pemeriksa, batas pengetahuan, dan alat ukur gerbang pada direktori skrip.

## Sebaran tanda asal (hitung ulang dari register beku)

| kelas_asal | Baris | Batas pemakaian |
|---|---|---|
| `TERUKUR-DOKUMEN` | 1279 | default; terbaca langsung dari lapisan teks dokumen |
| `TERUKUR-OCR` | 0 | nol pada baseline ini; tidak ada halaman scan-only |
| `DITURUNKAN` | 11 | wajib isi `turunan_dari`; bukan pengganti nilai sumber |
| `INTERNAL-DRAFT` | 40 | draf internal GSP revisi 5.3.2; dilarang jadi pemutus ambang standar luar |
| `TIDAK-ADA-DI-KORPUS` | 11 | pernyataan ketiadaan; bahan `batas-pengetahuan.md` |

Sebaran di atas dihitung ulang dari register beku pada saat rakit, bukan disalin dari laporan hulu, sehingga angka nol pada satu kelas adalah keadaan benar yang tetap ditampilkan dan bukan kegagalan ekstraksi. Kelas TERUKUR-OCR bernilai nol karena seluruh halaman yang dipakai terbaca pada lapisan teks sehingga tidak ada angka yang bergantung pada pengenalan karakter optik. Kelas DITURUNKAN menuntut kolom asal terisi dan tidak boleh dipakai menggantikan nilai sumbernya pada dokumen luar. Kelas INTERNAL-DRAFT dilarang menaikkan ambang standar luar, dan kelas TIDAK-ADA-DI-KORPUS menjadi bahan baku pernyataan batas pengetahuan alih-alih angka.

## Subsistem dan cakupan

| Bab | Subsistem | Blok prosa | Baris register | Berkas korpus | Berkas referensi |
|---|---|---|---|---|---|
| 01 | Klasifikasi barang berbahaya dan terminologi dasar | 9 | 127 | 5 | `subsystem-01-klasifikasi-barang-berbahaya-dan-terminologi-dasar.md` |
| 02 | Manajemen risiko, mutu, dan kompetensi personel | 8 | 74 | 9 | `subsystem-02-manajemen-risiko-mutu-dan-kompetensi-personel.md` |
| 03 | Penandaan, klasifikasi resmi, dan pengujian bahan peledak | 8 | 139 | 6 | `subsystem-03-penandaan-klasifikasi-resmi-dan-pengujian-bahan-peledak.md` |
| 04 | Penyimpanan, perokaran, dan handling internal | 18 | 160 | 10 | `subsystem-04-penyimpanan-perokaran-dan-handling-internal.md` |
| 05 | Zona bahaya dan jarak pemisah (quantity-distance) | 12 | 123 | 6 | `subsystem-05-zona-bahaya-dan-jarak-pemisah-quantity-distance.md` |
| 06 | Konstruksi dan jenis fasilitas penyimpanan | 4 | 40 | 3 | `subsystem-06-konstruksi-dan-jenis-fasilitas-penyimpanan.md` |
| 07 | Kelistrikan, penyalur petir, dan pembumian | 16 | 186 | 7 | `subsystem-07-kelistrikan-penyalur-petir-dan-pembumian.md` |
| 08 | Bahaya radiasi elektromagnetik (EMR) | 5 | 25 | 1 | `subsystem-08-bahaya-radiasi-elektromagnetik-emr.md` |
| 09 | Keamanan fisik gudang dan CCTV | 7 | 74 | 2 | `subsystem-09-keamanan-fisik-gudang-dan-cctv.md` |
| 10 | Keadaan darurat, PPE, dan pencegahan khusus | 9 | 102 | 8 | `subsystem-10-keadaan-darurat-ppe-dan-pencegahan-khusus.md` |
| 11 | Inspeksi, audit, inventaris, dan akuntabilitas lot | 13 | 155 | 12 | `subsystem-11-inspeksi-audit-inventaris-dan-akuntabilitas-lot.md` |
| 12 | Transportasi dan pergerakan amunisi | 6 | 76 | 1 | `subsystem-12-transportasi-dan-pergerakan-amunisi.md` |
| 13 | Lingkungan, demiliterisasi, dan pembuangan akhir | 6 | 60 | 1 | `subsystem-13-lingkungan-demiliterisasi-dan-pembuangan-akhir.md` |
| Total | tiga belas subsistem | 121 | 1341 | 49 | 13 |

Tiga belas bab tersebut menutup seluruh baris register tanpa sisa, dan kolom berkas korpus pada tabel di atas menyebut jumlah berkas yang menyumbang angka ke bab terkait sehingga satu berkas dapat muncul pada beberapa bab. Pembagian ini dipilih karena norma gudang amunisi tersebar lintas seri dan bukan per berkas, sehingga susunan per-dokumen akan memaksa pembaca menyusun ulang topik yang sama dari beberapa berkas sekaligus. Bab dengan jumlah blok kecil menandakan topik yang memang tipis pada korpus dan bukan bagian yang belum selesai dirakit, dan kekosongan semacam itu dinyatakan pada berkas batas pengetahuan.

## Metode dan gerbang beku model

Model paket ini adalah register kuantitas beku yang disusun ulang menjadi bab per-subsistem, dan syarat pembekuannya adalah setiap baris terverifikasi deterministik muncul pada halaman yang diklaim kartu hulu (EX-A 160, EX-B 153, EX-C 124, EX-D 210, EX-E 210, EX-F 171; total 1028 baris hulu) sebelum rakit ini memberi `reg_id` berbentuk `R-<bab>-<urut>`. Tingkat artefaknya adalah SERAH untuk pemakaian internal swarm dan naik ke distribusi fleet hanya lewat gerbang penjurian misi serta langkah distribusi oleh pengelola skill.

Suntingan setelah beku diperlakukan sebagai revisi baru dengan nomor revisi naik, catatan CHANGELOG yang hanya bertambah, dan sidik jari baru yang dihitung ulang. Mengubah nilai beku tanpa baris CHANGELOG dilarang karena menghapus jejak audit yang menjadi alasan paket ini dipertahankan. Revisi 1.0.5 menambah dua partisi tambalan GAP hasil ekstraksi ulang 23 halaman celah yang lolos verifikasi controller sebelum masuk register beku, dengan 153 baris dari GAP-EX1 dan 153 baris dari GAP-EX2.

Kriteria pemilihan sel tabel besar ditetapkan lebih dulu agar gerbang cakupan jujur: satu baris register dibuat untuk setiap sel kunci yang dipakai keputusan rekayasa dan bukan untuk setiap tabel utuh. Pada tabel jarak seri 02 pilihan jatuh pada tiap sel jarak normatif per kelas penyimpanan pada lampiran E, H, L, N, dan Q berikut koefisien penskalaannya. Ketika lapisan teks tidak memisahkan kolom dengan andal, atribusi per-sel ditahan dan anomalinya dibukukan sebagai baris register sendiri alih-alih ditebak nilainya. Draf internal tidak pernah dipakai menaikkan ambang standar luar, dan angka draf selalu membawa penanda kelas asalnya.

## TEMUAN (diterbitkan, bukan dikubur)

| ID | Temuan | Kelas | Tindakan |
|---|---|---|---|
| T-01 | Enam berkas berlabel 'NATO ST-SG' pada kartu hulu ternyata publikasi PBB (UN Model Regulations Rev.24 Vol I/II; UN Manual of Tests Rev.8 + Amend.1). Tema threat assessment/protection level keamanan gudang NATO tidak ada pada berkas itu. | cacat label hulu | kedudukan dikoreksi di silsilah; klaim ketiadaan dipersempit cakupannya lewat field catatan pada baris R-09-0023 |
| T-02 | Klaim hulu 'harga/unit cost tidak ada di korpus' hanya diuji pada seri 01; korpus memuat angka biaya dalam kerangka EMV seri 02 ([R-02-0066, V3_IATG-02.10_en.pdf, hal 41] dan [R-02-0067, V3_IATG-02.10_en.pdf, hal 42]). | propagasi klaim | baris positif ditambahkan dan terverifikasi halaman; klaim lama dipersempit lewat field catatan pada baris R-02-0013 |
| T-03 | Peta bab blueprint memakai asumsi nomor seri yang bergeser dari judul aktual (mis. 08.10 = Transport, bukan inspeksi/audit; 09.10 = Security; 10.10 = Demil/lingkungan; 11.10 = Accident investigation; 12.x = operasi multinasional/unit kecil). | deviasi desain hulu | bab dipetakan dari judul aktual modul; rekonsiliasi tercatat di silsilah |
| T-04 | Nomor halaman register adalah indeks halaman PDF, bukan nomor cetak (mis. selisih tetap pada ATF). | konvensi pengukuran | cara ukur didefinisikan di seksi verifikasi; verifier memakai indeks PDF |
| T-05 | Draf internal CCTV mengutip ambang IATG 05.20/05.40/06.x/09.10/02.50; sumber primer ambang ada di partisi EX-B/C/D/E. | risiko pemalsu-tier | 40 baris INTERNAL-DRAFT diberi penanda inline 'DRAF INTERNAL GSP bukan norma IATG/NATO' dan dilarang jadi pemutus ambang |
| T-06 | Anomali lapisan teks Lampiran E.1 (16 angka vs 17 label kolom) membuat atribusi per-sel kolom E tidak aman. | cacat ekstraksi hulu | dibukukan sebagai baris register sendiri (R-05-0044); atribusi kolom E tidak diterbitkan |
| T-07 | Simbol derajat pada 06.50 dan 07.30 tergabung dengan angka ('400C' = 40 C); dinormalisasi pekerja hulu dengan catatan per baris. | rendering sumber | dipertahankan dengan catatan; jangan dibaca sebagai 400 derajat |
| T-08 | Koersi senyap pointer lintas lapis: jalur rakit mengubah string nomor bagian DOCX menjadi integer (mis. `Lampiran-C` menjadi 0, `5.3.2.1` menjadi 5) sehingga 42 baris .docx kehilangan alamat aslinya tanpa peringatan. | cacat rakit lintas lapis | 42 baris dipulihkan ke pointer hulu pada revisi 1.0.3; grammar validator A-1 dipasang di CHECK 5 `scripts/skl_gates.py`; uji kesetaraan pointer hulu-vs-beku per baris menjadi gerbang wajib rakit berikutnya |

Delapan temuan di atas adalah cacat yang ditemukan selama rakit dan sengaja diterbitkan bersama artefaknya supaya pemeriksa berikutnya tidak mengulang penemuan yang sama. Tidak ada temuan yang ditutupi dengan menghapus baris register terkait, karena setiap temuan punya baris catatan pada register atau baris pada silsilah dokumen. Temuan kelas hulu seperti label berkas dan geseran nomor seri dicatat sebagai fakta pengukuran dan bukan sebagai kesalahan pribadi pekerja tertentu. Tindakan yang mengubah nilai beku tidak dilakukan pada rakit ini; yang dilakukan hanyalah mempersempit cakupan klaim yang terbukti terlalu lebar.

## CHANGELOG (append-only)

| Revisi | Tanggal | Perubahan | Sidik jari register |
|---|---|---|---|
| 1.0.0 | 2026-09-16 | Rakit pertama dari enam register hulu (1028 baris) + 7 baris rekonsiliasi SKL terverifikasi halaman; sanitasi SR-12 pada 2 kutipan; baseline beku 16-09-2026. | `3b254f275e2e6eb7` |
| 1.0.1 | 2026-09-16 | Suntingan pasca-beaku tanpa mengubah nilai beku: prolog empat berkas referensi ditulis ulang sampai lolos gerbang naturalisasi kanal doc (`scan_ai_footprint.py --channel doc` VERDICT PASS), tabel ketiadaan pada `batas-pengetahuan.md` diregenerasi utuh dari field `catatan` register karena sel sebelumnya terpotong sepihak, dan jumlah baris pada prolog `register.md` dikoreksi dari 1028 (angka hulu) ke 1035 (populasi register ini). Sidik jari register tidak berubah karena `register.jsonl` tidak disentuh. | `3b254f275e2e6eb7` |
| 1.0.2 | 2026-09-16 | Perbaikan pasca-verifikasi S9 butir D-2 (kartu t_fa3860a1): field `catatan` diisi pada dua baris kutipan ATF R-04-0130 dan R-04-0138 dengan keterangan bahwa spasi intra-kata pada lapisan teks ATF hasil justification telah dinormalisasi sehingga kutipan merekonstruksi kata utuh sementara halaman klaim tetap terverifikasi; tidak ada nilai beku, teks kutipan, maupun halaman yang diubah. Sidik jari register naik dari `3b254f275e2e6eb7` menjadi `6ab24ef3f9500336` karena isi berkas mesin berubah; dihitung ulang oleh skl_gates.py CHECK 7 dan dicetak ulang pada prolog `register.md` serta `silsilah-dokumen.md`. | `6ab24ef3f9500336` |
| 1.0.3 | 2026-09-16 | Perbaikan pasca-verifikasi S9 butir D-1 sesuai AMANDEMEN R1 bagian A-1 (kartu t_05e017e5): seluruh pointer baris .docx dinormalkan dari integer terkoersi ke string nomor bagian/penanda blok apa adanya dari hulu EX-F (40 baris INTERNAL-DRAFT pulih ke pointer hulu, termasuk R-09-0021 dan R-09-0022 menjadi `paragraf-38` dan `paragraf-414`; 2 baris ketiadaan .docx menjadi null), jalur koersi tipe dihapus dan diganti uji kesetaraan pointer hulu-vs-beku per baris, kolom Hal `register.md` serta 35 sitasi prosa bentuk `hal <n>` diregenerasi ke bentuk `bagian <pointer>`, dan gerbang paket `scripts/skl_gates.py` CHECK 5 mengikuti teks SR-5 revisi R1. Nilai beku, teks kutipan, jumlah baris, dan sebaran tanda asal tidak berubah. Sidik jari register naik dari `6ab24ef3f9500336` menjadi `bcc7ff296dc152b0`; dihitung ulang oleh skl_gates.py CHECK 7 dan dicetak ulang pada prolog `register.md` serta `silsilah-dokumen.md`. | `bcc7ff296dc152b0` |
| 1.0.4 | 2026-09-16 | Perbaikan pasca-verifikasi S9-REVERIF butir D-4 dan D-5 sesuai vonis kartu t_ab0231bb (eksekusi kartu t_e69871d8): satu sitasi R-02-0001 pada bab 02 diubah dari bentuk lama penanda ketiadaan menjadi `bagian Lampiran-C` agar identik dengan pointer register (grammar SR-6 bentuk `bagian <pointer>`), dua baris R-09-0006 dan R-09-0007 dikoreksi pointer-nya dari `5.1.1` menjadi `paragraf-19` karena kutipan verbatim hanya tercantum di paragraf tersebut (opsi remedi (a) sesuai arahan kartu), field `catatan` kedua baris itu ditambah keterangan koreksi pointer hulu sementara keterangan asal tetap dipertahankan, dan nilai, satuan, maupun teks kutipan kedua baris tidak diubah. Jumlah baris tetap 1035 dan 1033 baris register lain byte-identik terhadap backup pra-tambal. Sidik jari register naik dari `bcc7ff296dc152b0` menjadi `a6f6f35b29b91ce8`; dihitung ulang oleh skl_gates.py CHECK 5 dan CHECK 7 serta dicetak ulang pada prolog `register.md` dan `silsilah-dokumen.md`. | `a6f6f35b29b91ce8` |
| 1.0.5 | 2026-09-16 | Merge tambalan celah cakupan F2 sesuai Decision Log D-08 dan D-09 (kartu t_56f2bda6): 306 baris register GAP digabung ke register beku sehingga populasi naik dari 1035 menjadi 1341 baris tanpa satu pun baris hulu berubah isinya; GAP-EX1 menyumbang 153 baris dari 12 halaman celah dan GAP-EX2 menyumbang 153 baris dari 11 halaman celah, keduanya controller-verified lewat uji silang pymupdf 306/306 kutipan berada di halaman yang dinyatakan; `reg_id` baru menyambung penomoran per bab mengikuti konvensi `R-<bab>-<urut>` dengan urutan pemberian mengikuti urutan partisi sumber lalu urutan baris berkas, field `id` baris tetap memakai prefiks GAP-EX1/GAP-EX2 sebagai jejak asal, field `turunan_dari` dinormalkan dari string kosong ke daftar kosong agar seragam dengan skema basis, dan prosa bab subsistem tidak diubah karena penganyaman sitasi GAP menjadi fase tersendiri; bank soal, kunci, jawaban, grade, dan score tidak disentuh. Sidik jari register naik dari `a6f6f35b29b91ce8` menjadi `d5fc5d8475d2c5ab`; dihitung ulang oleh skl_gates.py CHECK 5 dan CHECK 7 serta dicetak ulang pada prolog `register.md` dan `silsilah-dokumen.md`. | `d5fc5d8475d2c5ab` |
| 1.0.6 | 2026-09-16 | Remediasi D-6 pasca vonis S9-REVERIF3 butir C16 (anti-bocor, eksekusi kartu t_d6e1e959): field `catatan` pada 26 baris bawaan partisi GAP-EX2 memuat penanda kehadiran butir kunci bank soal berbentuk id soal dan seluruhnya dinetralkan di hulu `work/ekstraksi/GAP2_register.jsonl` lewat skrip `work/fix_gap2_d6.py`, dengan catatan yang murni penanda diganti frasa netral tanpa id soal dan klausa penanda yang menempel setelah titik-koma dibuang sementara teks informatif sisanya utuh; field id, dokumen, halaman, kutipan, nilai, satuan, kelas_asal, dan turunan_dari tidak berubah satu byte pun, terbukti dari uji diff field-per-field terhadap register hidup 1.0.5 yang menunjukkan tepat 26 baris beda dan 1315 baris identik. Sidik hulu GAP2 naik dari `1baf3349ff1d298ddc3e7fc476301e8f3b5a0ec274508ae735b0a99bbf4916df` menjadi `2c5f29b71eec56fe5c92bb2d3731818f93bed99c1a42f19be2269e9a53c66754`; merge diregenerasi deterministik dari pristine `evidence/pre_merge/` oleh `work/merge_gap_d6.py` yang kini memuat GERBANG ANTI-BOCOR wajib (pola `Q-(T[1-4]|TRAP)-[0-9]{3}` harus nol di hulu dan di seluruh berkas paket sebelum serah). Populasi tetap 1341 baris, bank soal dan kunci tidak disentuh (exam_key `3397fc0003ff39ed`, exam_questions `065da18bcb95e847`), dan jawaban, grade, score tidak disentuh. Sidik jari register naik dari `d5fc5d8475d2c5ab` menjadi `88eff3876c72a5f9`; dihitung ulang oleh `work/merge_gap_d6.py` dan dicetak ulang pada prolog `register.md`, footer `register.md`, serta `silsilah-dokumen.md`. | `88eff3876c72a5f9` |

## Pernyataan kesegaran (R-10)

Baseline beku 16-09-2026 mengikat seluruh isi paket ini karena korpus yang dipakai adalah mirror lokal 49 berkas pada tanggal tersebut dan edisi lebih baru dari IATG, UN Model Regulations, UN Manual of Tests, maupun regulasi ATF belum dijangkau serta belum diuji sama sekali. Pertanyaan tentang edisi lebih baru dijawab sebagai belum dijangkau baseline ini dan bukan ditebak isinya. Keterbatasan itu juga berlaku untuk regulasi nasional negara mana pun yang memang tidak termasuk korpus, sehingga kebutuhan penerapannya harus dicek pada otoritas yang berwenang. Batas-batas lain yang setara didaftar pada [`references/batas-pengetahuan.md`](references/batas-pengetahuan.md) beserta cara cek yang dipakai untuk memvonisnya.

## Verifikasi dan sidik jari

| Pemeriksaan | Cara ukur | Hasil |
|---|---|---|
| Baris register beku | hitung baris [`references/register.jsonl`](references/register.jsonl) | 1341 |
| `reg_id` unik | skrip `scripts/skl_gates.py` CHECK 5 | lihat laporan gerbang |
| Berkas korpus terwakili | pencocokan `dokumen` ke `corpus/_manifest.json` | 49/49 |
| Sidik jari register sha16 | sha256 byte kanonis (key sorted, LF), 16 karakter pertama | `88eff3876c72a5f9` |
| Sidik jari korpus sha16 | sha256 daftar kanonis `nama|sha256` 49 baris urut alfabetis | `4008721dce6863bd` |
| Jejak tipografi | `scan_ai_footprint.py --channel doc` pada paket | lihat VERDICT scanner |
| Halaman rujukan | indeks halaman PDF (bukan nomor cetak); DOCX memakai nomor bagian/paragraf | konvensi |

Sidik jari pada tabel di atas wajib dikutip oleh laporan penilaian dan laporan penerimaan supaya hasil penjurian mengikat pada artefak yang persis sama. Setelah beku, suntingan apa pun membuat nomor revisi naik dan sidik jari baru dihitung ulang oleh alat ukur gerbang yang ikut dikirim dalam paket ini. Cara ukur halaman memakai indeks halaman PDF dan bukan nomor cetak karena beberapa berkas memiliki selisih tetap antara keduanya, dan pemeriksa yang memakai nomor cetak akan menemukan angka yang tampak bergeser. Sumber akhir seluruh isi paket adalah korpus beku misi MWSKILL-0916 dengan manifest 49 berkas dan sidik jari korpus sha16 `4008721dce6863bd`.
