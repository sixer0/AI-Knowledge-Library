# Rencana Kerja — Perpustakaan Teknis

**Lokasi:** `C:\Users\gspen\Videos\Buku`
**Tanggal audit:** 19 Agustus 2026
**Isi koleksi:** 23 berkas PDF · 22 folder topik · 20.079 halaman · 1,04 GB

Dokumen ini menjawab satu pertanyaan: **apa yang dikerjakan lebih dulu.**
Urutan disusun dari hambatan terbesar (isi buku tidak bisa dicari) menuju
pekerjaan kosmetik (penamaan berkas).

---

## Ringkasan temuan audit

| Temuan | Jumlah | Dampak |
|---|---|---|
| Tidak bisa dicari (belum OCR) | ~~2~~ → **0 buku** — ✅ tuntas | — |
| Tanpa bookmark sama sekali | ~~5~~ → **0 buku** — ✅ tuntas | — |
| Bookmark rusak / nama berkas mentah | ~~4~~ → **0 buku** — ✅ tuntas | — |
| Judul duplikat (2 edisi CCNA) | ~~1 pasang~~ → **0** — ✅ diarsipkan | — |
| Nama berkas mentah "libgen.li" | ~~23~~ → **0 berkas** — ✅ tuntas | — |
| Berkas terlalu besar (> 100 MB) | 3 buku | Lambat dibuka, berat disalin |

---

## P0 — Prioritas pertama: isi buku harus bisa dicari

Selama dua buku ini belum di-OCR, keduanya hanya berupa gambar. Tidak bisa
di-Ctrl+F, tidak bisa disalin, tidak bisa dikutip ke dokumen GSP.

### T1. OCR + kompresi — RCM II (John Moubray) — ✅ SELESAI 19 Agustus 2026
- **Hasil:** `Reliability-centered Maintenance (RCM II) - John Moubray [OCR].pdf`
- **Cadangan:** `_asli/RCM II - John Moubray [ASLI sebelum OCR].pdf` (SHA-256 diverifikasi identik dengan berkas asli)
- **Capaian:** 186,7 MB → **89,5 MB** · 972.301 karakter teks (159.352 kata) · 444 halaman utuh · 600 dpi dipertahankan
- **Cara:** Tesseract 5.4 (eng) pada render 300 dpi, hasilnya ditanam sebagai lapisan teks tak terlihat; gambar tidak ikut diproses ulang
- **Kompresi:** 339 hal. G4 asli disalin apa adanya (lossless) · 17 hal. berisi abu/warna tetap JPEG asli (lossless) · 88 hal. teks murni dibinerkan ke G4 pada 600 dpi (135 MB → 16,6 MB), area isian abu di-dither agar latar abu kepala tabel worksheet tidak hilang
- **Catatan target:** target < 60 MB tidak tercapai tanpa menurunkan resolusi teks. 51,3 MB berasal dari 339 halaman G4 yang sudah lossless-minimum; menekan lebih jauh berarti menurunkan 600 dpi ke 400 dpi. Diputuskan mempertahankan mutu.
- **Bonus:** daftar isi (butir T3) sekaligus dipasang — 100 bookmark, 26 tingkat bab + 74 sub-bagian

### T2. OCR — FOA Reference Guide to Fiber Optics (Jim Hayes) — ✅ SELESAI 19 Agustus 2026
- **Hasil:** `Fiber Optic Fundamental/Jim Hayes - FOA Reference Guide to Fiber Optics (2019).pdf`
- **Cadangan:** `Fiber Optic Fundamental/_asli/FOA Reference Guide - Jim Hayes [ASLI sebelum OCR].pdf` (SHA-256 diverifikasi)
- **Capaian:** 452.500 karakter teks (73.496 kata) · **seluruh 214 halaman bertext, nihil halaman kosong** · 14 bookmark dipertahankan
- **Ukuran:** 51,8 MB → 52,0 MB (naik 0,2 MB oleh lapisan teks)
- **Target ukuran turun 60% DIBATALKAN, dan itu keputusan sadar.** Halaman buku ini bukan pindaian kertas melainkan teks digital yang diratakan jadi gambar **123 dpi** — resolusinya sudah rendah dan JPEG-nya sudah efisien. Uji kompresi ulang hanya menghemat 10% (q72) sambil menurunkan mutu baca. Gambar dibiarkan apa adanya, stream JPEG asli disalin lossless.
- **Nama berkas** sekaligus disesuaikan ke pola T6.
- **Resume:** `RESUME - FOA Reference Guide to Fiber Optics.md` di folder yang sama

---

## P1 — Prioritas kedua: navigasi

Buku 500–1.000 halaman tanpa bookmark praktis hanya bisa dibaca berurutan.
Ini yang paling sering menghambat saat butuh rujukan cepat di tengah kerja.

### T3. Bangun bookmark untuk 5 buku tanpa daftar isi — ✅ SELESAI 19 Agustus 2026

**389 bookmark baru terpasang.** Tiap berkas dicadangkan lebih dulu ke `_asli/` folder masing-masing.

| Buku | Halaman | Bookmark | Sumber judul |
|---|---|---|---|
| TCP/IP Illustrated Vol. 1 | 1.059 | **207** (18 bab + 187 sub-bab + glosarium + indeks) | Halaman daftar isi PDF 12–26 |
| CCTV: From Light to Pixels | 595 | **21** (14 bab + 4 apendiks + indeks + muka) | Header berjalan tiap halaman — buku ini tidak punya halaman daftar isi |
| The Art and Science of Lightning Protection | 255 | **72** (14 bab + 56 sub-bab + muka + indeks) | Halaman daftar isi PDF 8–10 |
| Reference Guide to Fiber Optic Testing Vol. 1 | 146 | **89** (4 bab + 20 sub-bab + 65 sub-sub-bab) | Halaman daftar isi PDF 4–7 |
| RCM II (Moubray) | 444 | **100** — selesai bersama T1 | Halaman daftar isi, di-OCR ulang 500 dpi |

**Tiga masalah teknis yang ditemukan dan diatasi:**

1. **Digit hilang.** Pada TCP/IP, ekstraksi teks menjatuhkan digit terakhir sebagian nomor halaman bab (mis. "31" terbaca "3"). Diperbaiki memakai sifat monoton daftar isi untuk merekonstruksi digit, lalu tiap bab dikunci ke halaman pembukanya yang sebenarnya di badan buku. Empat bab meleset satu halaman dan terkoreksi.
2. **Judul terpotong.** Judul bab yang melipat ke baris berikutnya membuat baris di atasnya menelan entri di bawahnya — pada TCP/IP dan Lightning Protection hal ini sempat menghilangkan Bab 1 seluruhnya. Diatasi dengan aturan: jangan gabungkan baris bila baris berikutnya sendiri membuka entri baru.
3. **Tanpa daftar isi sama sekali.** CCTV tidak memuat halaman daftar isi di berkasnya. Bookmark dibangun dari header berjalan tiap halaman, lalu tiap bab diverifikasi ke halaman pembukanya.

Seluruh 389 bookmark diperiksa: urutan monoton, tidak ada halaman di luar jangkauan, seluruh halaman tujuan dapat dibuka. Sampel acak 40 sub-bab TCP/IP diuji dan semuanya mendarat tepat.

### T4. Perbaiki bookmark yang isinya nama berkas mentah — ✅ SELESAI 19 Agustus 2026

| Buku | Sebelum | Sesudah |
|---|---|---|
| Security Engineering (Anderson) | 31 entri `SEv3-ch1-7sep` … | **31 entri** dengan judul bab asli (29 bab) |
| Diesel Generator Handbook (Mahon) | **2.377 entri sampah** (`page1`, `images`, `tableN`), banyak menunjuk halaman −1 | **21 entri bersih** (15 bab + 4 apendiks + muka + indeks) |
| UPS and Active Filters (Emadi dkk.) | 238 entri di bawah 2 lapis pembungkus `3035_cNN.pdf` | **218 entri** berjenjang 5 tingkat, sampai sub-sub-bagian |
| Storage Networks Explained (Troppens dkk.) | 21 entri berakhiran `.pdf` | **20 entri** (13 bab dalam 2 Part + glosarium + apendiks + indeks) |

**Cara kerja berbeda per buku**, tergantung apa yang bisa diselamatkan:
- *Security Engineering*: halaman tujuan sudah benar, hanya judulnya rusak. Judul asli diambil dari tiap halaman tujuan dengan memilih teks berukuran font terbesar.
- *UPS*: outline aslinya ternyata utuh dan benar, hanya terkubur di bawah dua lapis pembungkus nama berkas. Cukup dikupas dan dinaikkan dua tingkat.
- *Storage Networks*: struktur benar, hanya akhiran `.pdf` dan awalan `N-` yang perlu dibersihkan.
- *Diesel Generator Handbook*: outline lama tidak ada yang bisa dipakai. Dibangun ulang dari daftar isi mini yang ada di halaman pembuka tiap bab.

> ### ⚠ Temuan: Diesel Generator Handbook tidak lengkap
> Saat menyusun ulang outline-nya ketahuan berkas ini **kehilangan sekitar 55 halaman**: nomor halaman cetak melompat dari 394 (PDF 388) langsung ke 450 (PDF 391). Yang hilang adalah **Bab 11 "Emergency and standby" seluruhnya dan bagian awal Bab 12 "Fuels and lubricating oils"**. Penyebabnya terlihat dari outline lama: berkas ini dirakit dari potongan `1.pdf`–`13.pdf` dan potongan `10.pdf` tidak ikut.
>
> Bookmark tidak bisa memperbaiki isi yang tidak ada. Sebagai gantinya dipasang entri penanda di posisi terputusnya, supaya pembaca langsung tahu. **Tindak lanjut: cari salinan pengganti buku ini bila Bab 11 diperlukan.**

Seluruh 290 bookmark keempat buku diperiksa: nihil judul sampah, nihil halaman di luar jangkauan, seluruh halaman tujuan dapat dibuka.

---

## P2 — Prioritas ketiga: kebersihan koleksi — ✅ SELESAI 19 Agustus 2026

### T5. Duplikat CCNA — selesai
Edisi 2024 (3.292 hal.) tetap di `Networking/` sebagai rujukan utama. Edisi 2019
(1.813 hal.) dipindahkan ke `Networking/_arsip/` — **tidak dihapus**.

### T6. Penamaan berkas — selesai
Seluruh 22 berkas kini memakai pola **`Penulis - Judul (Edisi, Tahun).pdf`**.
Embel-embel `- libgen.li`, nama seri dalam kurung siku, dan penulisan nama penulis
yang terbalik sudah dibersihkan. Nama penulis dikembalikan ke urutan wajar
(mis. `Chalup, Strata R._Hogan...` menjadi `Thomas Limoncelli, Christina Hogan, Strata Chalup`).

### T7. Struktur folder — selesai
| Sebelum | Sesudah |
|---|---|
| `CCTV  VSS` (spasi ganda) | `CCTV VSS` |
| `Mechanical  Structure` | `Mechanical Structure` |
| `Storage  RAID  NVR` | `Storage RAID NVR` |
| `TCP ip` | `TCP IP` |
| `RCM/Reliability Centered Maintenance/` (bersarang) | isi dinaikkan ke `RCM/` |

> **Sisa kecil:** folder kosong `RCM/Reliability Centered Maintenance/` belum bisa dihapus —
> masih dipegang proses lain (kemungkinan jendela Explorer yang sedang membukanya). Isinya
> sudah kosong dan tidak mengganggu; hapus manual kapan saja setelah jendela itu ditutup.

Berkas yang jalurnya berubah dan ikut diperbarui: `SKILL.md` skill `rcm-analysis`,
`RESUME - RCM II (John Moubray).md`, dan `Resume Perpustakaan Teknis.docx`.

---

## P3 — Nilai tambah, setelah P0–P2 beres

### T8. Katalog induk — ❌ TIDAK DIPERLUKAN (keputusan 19 Agustus 2026)
Bentuk `.xlsx` yang bisa disortir dan difilter dinyatakan tidak diperlukan.
Fungsi katalog sudah dijalankan oleh `Resume Perpustakaan Teknis.docx`, yang angkanya
diukur ulang dari berkas setiap kali dokumen dibuat sehingga tidak bisa basi.

### T10. Resume isi buku — ✅ SELESAI SELURUHNYA 19 Agustus 2026

**22 dari 22 folder buku kini punya resume.** Disimpan sebagai `RESUME - <judul>.md` di
folder bukunya masing-masing.

Tiap resume memuat: peta isi dengan nomor halaman, bagian yang paling sering dipakai beserta
angka dan rumusnya, tabel pemakaian di GSP, buku pendamping di rak, dan catatan mutu berkas
termasuk peringatan bila isinya sudah usang.

**342 rujukan halaman diperiksa otomatis** terhadap jumlah halaman berkas yang dituju —
nihil yang di luar jangkauan. Untuk delapan buku inti, isi rujukannya juga diperiksa satu
per satu terhadap teks halaman tujuan.

Catatan: resume Shigley tidak memuat rujukan halaman karena bookmark buku itu hanya sampai
tingkat "Part" tanpa penanda halaman bab yang dapat dikutip; navigasinya diarahkan ke panel
bookmark bertingkat.

Peringatan usang yang tercatat pada resume masing-masing: Battery (2000) untuk kimia litium
modern, UPS (2004) untuk efisiensi dan topologi masa kini, Storage Networks (2009) untuk
SSD/NVMe dan penyimpanan objek, Network Warrior (2011) untuk pemilihan perangkat, dan
Lightning Protection (2008) untuk nomor edisi standar.

---

### T11. Jembatan rak ke skill — ✅ SELESAI 19 Agustus 2026

Temuan yang mendasari: dari **45 skill yang terpasang, tidak satu pun menyebut rak buku ini**.
`cctv-system-designer` misalnya punya perhitungan optiknya sendiri, tetapi tidak tahu rumus
Damjanovski beserta halamannya ada terverifikasi di mesin ini. Akibatnya angka pada dokumen
GSP bersandar pada pengetahuan umum, bukan halaman buku yang bisa ditunjuk.

**Dua artefak yang menutup celah itu:**

| Artefak | Lokasi | Isi |
|---|---|---|
| **KATALOG-RUMUS.md** | akar rak | Indeks pertanyaan → rumus → buku → halaman; 12 domain; daftar "yang TIDAK ada di rak" |
| **Skill `pustaka-teknis`** | `~/.claude/skills/` | SKILL.md + 3 referensi: indeks rumus, rantai hitung lintas buku per jenis proyek, batas & peringatan usang |

**Rantai hitung lintas buku** (referensi 02) menutup kelemahan resume yang berdiri sendiri —
satu proyek VSS menembus enam buku berurutan, dan berkas itu menunjukkan titik serah
antar-bukunya. Lima rantai tersedia: VSS, jalur serat optik, catu daya & cadangan,
pemeriksaan termal, dan program pemeliharaan.

**Aturan yang ditegakkan skill:** tiap angka teknis menyebut buku dan halamannya; angka yang
tidak ada di rak dinyatakan tidak ada beserta sumber seharusnya, bukan diisi diam-diam;
peringatan usang ikut dibawa bila angkanya dipakai.

Skill ini **lapisan sumber, bukan perancang** — `cctv-system-designer`,
`perimeter-security-designer`, `hw-sw-config-master`, dan `rcm-analysis` tetap memegang
perancangannya; `pustaka-teknis` memasok angka dan rujukannya.

---

### T12. Tiga skill perancangan berbasis rak — ✅ SELESAI 19 Agustus 2026

Prioritas 2. Ketiganya menyandarkan angka ke `KATALOG-RUMUS.md` lewat `pustaka-teknis`,
sehingga tidak mengulang penggalian buku.

| Skill | Bersandar pada | Berkas |
|---|---|---|
| **fiber-link-design** | Hayes (FOA) + JDSU | SKILL.md + 3 referensi — 377 baris |
| **power-backup-sizing** | Emadi + Crompton + Mahon + Moubray | SKILL.md + 4 referensi — 465 baris |
| **grounding-lightning-design** | Joffe & Lock + Uman | SKILL.md + 3 referensi — 428 baris |

Ketiganya memuat: mode operasi, alur wajib, gerbang mutu, perangkaian ke skill lain, dan
bagian **"yang tidak ada di rak"** supaya angka tidak dikarang.

**Tiga hal yang ditegakkan lintas ketiganya:**
- **Urutan kerja tidak boleh dibalik** — loss budget sebelum ambang uji; survei resistivitas
  sebelum desain elektroda; profil beban sebelum kapasitas
- **Keputusan diambil dari kondisi terburuk**, bukan tipikal
- **UPS dan genset diperlakukan sebagai fungsi tersembunyi** — intervalnya dihitung dengan
  FFI, bukan ditebak

Skill personal kini 5 buah, total 2.630 baris: `pustaka-teknis`, `rcm-analysis`,
`fiber-link-design`, `power-backup-sizing`, `grounding-lightning-design`.

---

### T13. Template berita acara dan asumsi baku — SELESAI 19 Agustus 2026

Prioritas 3. Rantai hitung lintas buku sudah lebih dulu masuk `pustaka-teknis`
(referensi 02); dua sisanya diselesaikan di sini sebagai dokumen tingkat rak.

| Artefak | Isi |
|---|---|
| **TEMPLATE-BERITA-ACARA.md** | Rangka umum + delapan jenis uji: serat optik, pembumian, tahanan isolasi, kapasitas baterai, komisioning genset, terima sistem video, pemeriksaan termal, penyimpanan/RAID |
| **ASUMSI-BAKU.md** | Tiga aturan penyajian asumsi + daftar asumsi per domain, masing-masing dengan sensitivitas dan rencana penggantiannya |

**Temuan yang membentuk keduanya:** dari delapan jenis uji, **empat ambang terimanya tidak
ada di rak** — pembumian, tahanan isolasi MΩ mutlak, kapasitas baterai, dan ΔT termal.
Keempatnya berasal dari standar atau kontrak, bukan dari buku. Tabel "Ringkasan sumber
ambang" menandainya supaya tidak dikarang.

**Empat hal yang dinyatakan tidak boleh diasumsikan sama sekali**, karena keputusannya milik
pemilik sistem: sasaran MTBF kegagalan majemuk, sasaran pengamatan video (FI/FR), ambang
resistansi pembumian, dan resistivitas tanah. Bila keempatnya belum ditetapkan, perancangan
belum dapat diselesaikan.

Keduanya disambungkan ke `pustaka-teknis` sebagai aturan pokok butir 6 dan 7, sehingga
berlaku untuk seluruh skill yang memanggilnya.

---

### T14. Prioritas 4 — disiapkan, menunggu bahan (19 Agustus 2026)

**Prioritas 4 tidak dapat dikerjakan sekarang: bahannya belum ada di komputer ini.**
Pemeriksaan terhadap **507 berkas PDF** di Downloads, Documents, Desktop, dan Videos tidak
menemukan satu pun dari empat bahan yang dibutuhkan (ONVIF, PUIL/SNI, ISO 27037,
ISO 27001).

Yang dikerjakan sebagai gantinya adalah **menyiapkan agar integrasinya cepat begitu bahan
tiba**:

| Artefak | Isi |
|---|---|
| **PROSEDUR-TAMBAH-BUKU.md** | Prosedur enam langkah dari berkas mentah sampai tersambung ke skill, lengkap dengan tiga jebakan yang sudah terbukti muncul saat membangun daftar isi |
| **DAFTAR-PENGADAAN-BAHAN.md** | Empat bahan prioritas: apa yang dicari, mengapa mendesak, dan apa yang terbuka begitu ada |
| **_tools/ocr_book.py** | Alat OCR: sisipkan lapisan teks, gambar tidak diubah |
| **_tools/buat_katalog_docx.py** | Bangun ulang katalog .docx, angka diukur dari berkas |

**Kedua alat sebelumnya hanya ada di folder sementara** dan akan hilang saat sesi berakhir.
Sekarang tersimpan permanen di `_tools/` sehingga pekerjaan berikutnya tidak perlu menyusun
ulang pipeline-nya.

**Temuan sampingan:** Downloads berisi 393 PDF — brosur vendor, lembar spesifikasi produk,
proforma invoice, dan dokumen kerja GSP sendiri (ATLAS, Cetak Biru Agung, Asbuild Command
Center, manual VMS ARSENAL POMAL) — seluruhnya tidak tertata. Itu jenis pustaka berbeda
dari rak buku ini, dan bila perlu ditata, pendekatannya juga berbeda.

---

### T15. Batch 2 Lapis 1 — lima standar masuk rak — SELESAI 19 Agustus 2026

Dari `New folder` (75 berkas, 289 MB) yang diserahkan. Seluruhnya diperiksa: **0 rusak,
0 terkunci, hanya 2 perlu OCR** — jadi secara teknis semua dapat diproses. Yang dikerjakan
hanya **Lapis 1**, sesuai pembagian tiga lapis yang disetujui.

| Standar | Ditempatkan | Halaman |
|---|---|---|
| **ANSI/NETA ATS-2017** | `Electrical Maintenance/_standar/` | 262 |
| **BS EN 62676-1-2:2014** | `CCTV VSS/_standar/` | 62 |
| **IEC 61280-4-2:2014** | `FO Test Advanced/_standar/` | 162 |
| **IEC 62485-2:2010** | `Battery/_standar/` | 80 |
| **IEEE 1188-2005** | `Battery/_standar/` | 44 |

Ditempatkan di subfolder `_standar/` — bukan bersebelahan langsung dengan bukunya — supaya
alat pembangun katalog .docx yang mengambil satu PDF per folder tidak salah memilih.

**Empat resume standar ditulis** (dua standar baterai dijadikan satu berkas).

> ### Temuan: nama berkas NETA menyesatkan
> Diterima sebagai *"Maintenance Testing Specifications ANSI/NETA MTS-2007"*. Isinya
> **ANSI/NETA ATS-2017** — *Acceptance Testing*, edisi sepuluh tahun lebih baru. Bedanya
> menentukan: **ATS untuk uji terima**, MTS untuk uji pemeliharaan. Untuk pekerjaan GSP yang
> menyerahkan instalasi baru, ATS yang berlaku. Nama sudah diperbaiki sesuai isinya.

> ### Satu berkas dikeluarkan
> `IEEE Recommended Practice... vented lead-acid` ternyata hanya **contoh catatan redline
> 5 halaman**, bukan standarnya. Ditinggal di `New folder`.

**Dampak langsung — empat ambang yang selama ini bertanda ❌ kini punya sumber:**
tahanan isolasi MΩ, ΔT termografi, kapasitas baterai, dan ventilasi ruang baterai.
`KATALOG-RUMUS.md` bertambah Bagian 13, `TEMPLATE-BERITA-ACARA.md` diperbarui pada empat
jenis uji, `PETA-CELAH-KOLEKSI.md` mencatat celah yang tertutup.

**Lapis 2 dan 3 belum dikerjakan** — menunggu keputusan lanjutan.

---

### T16. Batch 2 Lapis 2 — tesis dan panduan keamanan siber — SELESAI 19 Agustus 2026

Delapan berkas masuk `Cybersecurity/`, perlakuan ringan (resume gabungan, tanpa skill).

| Kelompok | Isi | Lokasi |
|---|---|---|
| **4 tesis UI** (430 hal) | Forensik pesan instan (NIST 800-101) · forensik Android · Cyber Kill Chain + Elastic · kriteria audit BSSN | `Cybersecurity/_tesis/` |
| **4 panduan** (238 hal) | AD compromises (ASD-CISA 2024) · event logging (Joint CSI 2024) · NIST SP 800-50r1 · ITSECBuzz | `Cybersecurity/_panduan/` |

**Temuan yang paling bernilai: konteks hukum Indonesia.** Seluruh buku keamanan di rak
berbasis luar negeri. Keempat tesis justru menerapkan kerangka internasional ke regulasi
Indonesia dan menyebut dasar hukumnya — **UU 11/2008 (ITE)** sebagai dasar sahnya bukti
elektronik, dan **Peraturan BSSN No. 4 Tahun 2021** sebagai dasar audit keamanan instansi.

Keduanya dicatat di `KATALOG-RUMUS.md` sebagai 🟡 **penunjuk** — bukan tertutup penuh, karena
**yang dikutip dalam dokumen resmi harus regulasi aslinya, bukan tesisnya**.

**Dua buku ditahan.** Dari kelompok "Cyber Security Books", dua berkas sebenarnya buku utuh
yang pantas perlakuan penuh: *The NICE Cyber Security Framework* (366 hal) dan
*Cybersecurity: Protecting Critical Infrastructures* (346 hal) — yang kedua relevan untuk
objek vital. Menunggu keputusan.

Tiga berkas lain (dua quantum, satu sejarah kriptografi) tidak menyentuh lini kerja berjalan.

---

### T17. Batch 2 Lapis 3 — dua buku diproses, koleksi non-teknis dipisah — SELESAI 19 Agustus 2026

**Dua buku naik ke perlakuan penuh**, masing-masing diberi folder topik baru:

| Buku | Folder baru | Hal | Nilai |
|---|---|---|---|
| Alsmadi — *The NICE Cyber Security Framework* | `Cyber Operations` | 366 | **Bab 11: proses forensik 4 tahap + rantai kustodi** |
| Johnson (ed.) — *Protecting Critical Infrastructures* | `Critical Infrastructure` | 346 | Satu-satunya buku objek vital di rak |

Bab 11 Alsmadi menutup **sebagian** celah penanganan bukti digital — kerangka prosesnya ada
(collection, examination, analysis, reporting), meski NIST SP 800-86 dan ISO/IEC 27037
sendiri masih belum.

**Koleksi non-teknis dipisah ke `_koleksi-lain/`** — 60 berkas, 221 MB, dengan README dan
indeks, tanpa resume per judul:

| Folder | Berkas | Isi |
|---|---|---|
| `Ebook Pak Makmur` | 25 | Sejarah militer, kekuatan udara, geopolitik |
| `Makalah IEEE` | 21 | Makalah penelitian + `INDEKS-MAKALAH.md` |
| `Quantum dan Kriptografi` | 13 | Komputasi dan kriptografi kuantum |

Empat makalah IEEE ditandai 🟡 berpotensi relevan (forensik otomotif, forensik VxWorks,
deteksi deepfake, ransomware ATT&CK) — berguna sebagai penunjuk literatur, belum cukup jadi
sandaran dokumen.

**`New folder` habis dan dihapus.** Fragmen IEEE 5 halaman dipindah ke `_koleksi-lain` dengan
nama bertanda, tidak dihapus.

**Rak teknis kini 24 folder topik, 20.791 halaman, 0,96 GB.**

---

### T18. Rambatan batch 2 ke seluruh berkas sistem — SELESAI 19 Agustus 2026

Setelah tiga lapis batch 2 selesai, dilakukan **pemindaian kebasian**: mencari penanda lima
standar baru (`ATS-2017`, `IEEE 1188`, `62485`, `62676`, `61280`) pada 12 berkas sistem.

**Hasilnya: 8 berkas basi — dan lima di antaranya berkas rujukan skill.** Ini bentuk
kebasian yang paling berbahaya, karena skill akan tetap berkata *"ambang tidak ada di rak,
ambil dari standar berlaku"* padahal standarnya sudah ada di rak — orang lalu mencari ke
luar sesuatu yang sudah dimiliki.

| Berkas | Yang diperbaiki |
|---|---|
| `pustaka-teknis/01-indeks-rumus.md` | Tabel baru "Ambang dari standar" — 8 baris |
| `pustaka-teknis/03-batas-dan-celah.md` | Empat baris "tidak ada" → ✅ ADA; ONVIF & ISO 27001 ditegaskan **masih** terbuka |
| `pustaka-teknis/02-rantai-hitung-proyek.md` | Rantai termografi langkah 4: "TIDAK ADA di Vollmer" → NETA Tabel 100.18 |
| `pustaka-teknis/SKILL.md` | Empat baris standar pada tabel domain + kaidah *standar didahulukan atas buku teks* |
| `power-backup-sizing/04-batas-dan-peringatan.md` | Bagian 7 baru: IEEE 1188, IEC 62485-2, NETA |
| `fiber-link-design/02-uji-dan-berita-acara.md` | Bagian 6b: IEC 61280-4-2, empat metode, RTM, ORL |
| `grounding-lightning-design/03-verifikasi-dan-telusur.md` | Peringatan **jangan tertukar** — NETA memberi ambang isolasi, **bukan** resistansi pembumian |
| `ASUMSI-BAKU.md` | Bagian baru "Asumsi yang GUGUR" — 7 besaran kini dikutip, bukan ditaksir |
| `DAFTAR-PENGADAAN-BAHAN.md` | Status batch 2: tak satu pun dari 4 bahan tertutup penuh; nomor 3 jadi 🟡 sebagian |
| `PROSEDUR-TAMBAH-BUKU.md` | Konvensi `_standar/_tesis/_panduan` + daftar berkas rujukan skill yang wajib ikut diperiksa |

**Tiga hal yang sengaja dipertahankan sebagai celah terbuka**, supaya tidak terlihat
tertutup padahal bukan:

1. **ONVIF ≠ BS EN 62676-1-2.** Yang masuk standar *transmisi*, bukan interoperabilitas perangkat.
2. **PUIL ≠ ANSI/NETA.** NETA menutup celah *ambang uji*, bukan celah *kepatuhan hukum Indonesia*.
3. **Tesis ≠ regulasi.** Tesis di `_tesis/` adalah penunjuk ke UU 11/2008 dan Perban BSSN
   4/2021 — yang dikutip dalam dokumen resmi tetap harus regulasi aslinya.

**Dua pelajaran yang dimasukkan ke prosedur** supaya tidak terulang:

- Menambah buku **tidak selesai di rak** — berkas rujukan skill ikut basi dan tidak ada yang
  memberi tahu. Prosedur kini memuat daftar berkasnya beserta perintah `grep` pemeriksanya.
- Nama berkas standar **wajib dicocokkan dengan isinya**. Pada batch 2 ada berkas bernama
  *NETA MTS-2007* yang isinya ATS-2017 — peruntukannya berbeda (uji pemeliharaan vs uji terima).

**Paket Markdown dibangun ulang:** 63 berkas, 424 KB mentah → 200 KB terkompresi,
integritas OK.

---

### T19. Rak diubah menjadi Engineering Knowledge & Assurance System — SELESAI 20 Agustus 2026

Perpustakaan menjawab *"di buku mana?"*. Sistem jaminan menjawab *"bagaimana angka ini
sampai ke berita acara, dan apakah ia bertahan saat diperiksa?"* — isinya sebagian besar
sama, **arahnya yang berbeda**.

**Yang ditambahkan — tidak ada sebelumnya:**

| Berkas | Isi |
|---|---|
| `_sistem/01-TINGKAT-KEYAKINAN-RUJUKAN.md` | Tingkat **R1–R5**, aturan pemakaian per jenis keluaran, empat larangan, penurunan mutu karena usia |
| `_sistem/02-REGISTER-RUJUKAN.md` | Seluruh 29 sumber terklasifikasi + **batas cakupan tiap standar** |
| `_sistem/03-RANTAI-JAMINAN.md` | Lima mata rantai ①→⑤ dan aturan tingkat pada tiap mata |
| `_sistem/04-KARTU-KENDALI.md` | Lembar isian per besaran + contoh terisi |
| `_sistem/rantai/A–H` | **Delapan rantai lengkap** dari rujukan sampai lampiran berita acara |

**Temuan pokok dari klasifikasi R1–R5:**

```
R1  0      ← tidak ada dasar hukum Indonesia di rak
R2  5
R3  24     ← kekuatan rak
R4  0      ← selalu dari pabrikan, per proyek
R5  3 + 21 makalah
```

Dua kekosongan itu berbeda sifatnya, dan itu yang membuat klasifikasi ini berguna:
**R4 tidak perlu diadakan** — melekat pada produk yang dipilih, diminta per proyek.
**R1 perlu diadakan** — dan sudah di urutan teratas daftar pengadaan.

**Status delapan rantai:** lima utuh (A, B, C, E, F), **satu putus** (D — pembumian),
dua bersyarat (G perlu adopsi kontrak, H tanpa sandaran normatif).

**Rantai D sengaja diterbitkan dalam keadaan putus.** Tidak ada sumber sah untuk ambang
resistansi pembumian, dan menyamarkannya lebih berbahaya daripada menyatakannya. Berkasnya
memuat tiga jalan sah untuk menutupnya per proyek — penetapan pemilik, adopsi standar
kontrak, atau melaporkan hasil ukur tanpa pernyataan lulus.

**Satu peringatan baru yang ditemukan saat menyusun rantai D:** rak punya ambang **tahanan
isolasi** [R2] tetapi **bukan** ambang **resistansi pembumian**. Dua besaran berbeda —
MΩ terhadap Ω — dan mudah tertukar. Peringatannya masuk ke rantai D dan ke berkas rujukan
skill `grounding-lightning-design`.

**Paket baru:** `Engineering-Knowledge-Assurance-System.zip` — **77 berkas, 236 KB**,
integritas OK. Pembangkit: `_tools/buat_paket_ekas.py`.

---

### T20. Struktur direktori EKAS dibangun — SELESAI 20 Agustus 2026

Rak diubah dari **paket .zip** menjadi **struktur direktori kerja**:
`GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/` — **186 berkas, 115 map, 3 MB**.

| Map | Berkas | Isi |
|---|---|---|
| `00_START-HERE` | 4 | README, peta sistem, kendali dokumen, riwayat |
| `01_GOVERNANCE` | 6 | R1–R5, status otoritas, alur jaminan, gate G0–G7, kebijakan AI, prosedur sumber |
| `02_REGISTERS` | 12 | 8 CSV (2 terisi: 30 rujukan, 14 celah) + 3 penjelas |
| `03_SOURCE-VAULT` | 39 | 22 laci berisi manifest; **PDF belum dipindah** |
| `04_KNOWLEDGE-CARDS` | 30 | Satu kartu per rujukan, 12 domain |
| `05_DOMAIN-KNOWLEDGE` | 38 | 30 resume + 8 rantai jaminan |
| `06`–`09` | 29 | Map kerja proyek, tiap map beraturan sendiri |
| `10_TEMPLATES` | 8 | TPL-00 s.d. TPL-07 |
| `90_TOOLS` `95` `99` | 20 | Perkakas, rekaman impor, arsip |

**Dua koreksi yang ditemukan saat mencocokkan `tree.txt`:**

1. **Tujuh tahun terbit di register EKAS keliru**, termasuk satu salah penulis —
   `Maintenance Planning` tertulis *Palmer 2019*, sebenarnya **Nyman & Levitt 2010**.
   Penyebabnya register disusun dari ingatan, bukan dari berkasnya. Resume aslinya benar.
   Kejadian ini dicatat dalam `AI-USAGE-POLICY.md` sebagai alasan mengapa verifikasi
   halaman dan satuan tidak dapat ditawar.

2. **Bundel `Cybersecurity/_panduan`** menyeret **NIST SP 800-50r1** turun ke R5 karena
   dibundel dengan majalah. Tercatat sebagai butir terbuka; sementara ini bila mengutip
   isinya, **rujuk dokumen aslinya terpisah**.

**Yang belum dikerjakan — sengaja:**

**37 berkas PDF (993 MB) belum dipindahkan** ke `03_SOURCE-VAULT/`. Jalur lamanya dirujuk
oleh 30 resume, 5 skill, dan seluruh katalog; memindahkan tanpa memperbarui rujukan akan
memutus semuanya. `90_TOOLS/migrasi_sumber.py` sudah siap — baku uji coba, sungguhan dengan
`--jalankan`. Uji coba menghasilkan `LAPORAN-MIGRASI.csv` berisi daftar berkas .md yang
perlu disunting setelah pindah.

**EKAS saat ini cermin, bukan pengganti rak.** Berkas asli masih di tempatnya.

---

### T21. Migrasi tuntas — rak lama dibubarkan — SELESAI 20 Agustus 2026

**EKAS berhenti menjadi cermin dan menjadi rak itu sendiri.**

| Tahap | Hasil |
|---|---|
| 37 PDF sumber → `03_SOURCE-VAULT/` | 22 laci · R2:5 · R3:24 · R5:8 |
| 3 PDF arsip → `99_ARCHIVE/` | 2 pra-OCR (239 MB) + 1 edisi lama (39 MB) |
| 24 folder topik + 7 subfolder | **dihapus** setelah 30 resume diverifikasi bersalinan |
| 323 penyebutan jalur di 89 berkas | disunting mengikuti pemindahan |

**Tiga kekeliruan yang tertangkap saat mengerjakan, dan cara memperbaikinya:**

1. **Penggantian buta menyeret kode domain.** Token `` `RCM` `` pada daftar kode domain di
   `DOCUMENT-CONTROL.md` ikut berubah jadi jalur. Dipulihkan.

2. **Catatan riwayat sempat ikut disunting.** Tabel penamaan folder pada T6/T7 dan daftar
   lokasi standar pada T15–T16 berubah menunjuk laci vault — padahal keduanya merekam
   keadaan **saat peristiwa itu terjadi**. 31 penggantian dipulihkan.
   **Kaidah baru: catatan riwayat tidak ikut dimutakhirkan jalurnya.** Catatan riwayat yang
   jalurnya diperbarui berhenti menjadi catatan riwayat.

3. **Jalur penuh merusak keterbacaan kalimat.** `` `03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/RCM/` ``
   di tengah kalimat naratif tidak terbaca, dan dua buku berbeda yang selaci menjadi
   terlihat kembar. Seluruh jalur dipendekkan ke bentuk `` `R3/RCM/` ``, dan satu kalimat
   yang menjadi ganda ditulis ulang menyebut nama bukunya.

**Rak lama tidak ada lagi.** Akar `Buku/` kini berisi `GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/`,
`_koleksi-lain/`, `_sistem/`, `_tools/`, berkas tata kelola akar, dan paket ekspor.

---

### T22. Triase korpus — laci R4 terisi — SELESAI 20 Agustus 2026

**Mempercepat pencarian korpus bukan dengan mencari ke luar, melainkan menyaring yang sudah
ada di mesin ini.** Dua perkakas baru:

| Alat | Fungsi |
|---|---|
| `90_TOOLS/triase_korpus.py` | Memindai 761 kandidat di 6 folder, mengklasifikasi **R1–R5 + 20 kategori teknik**, mengintip halaman judul berkas bernama tidak jelas |
| `90_TOOLS/serap_r4.py` | Menyalin dokumen pabrikan ke `R4_OEM-TECHNICAL/`, menimbang kata di daerah judul 3× lebih berat |

**Hasil pindai:** 761 kandidat → 454 dibuang → **307 masuk antrean**
(R1:1 · R2:7 · R3:151 · R4:133 · R5:15). **95 dokumen pabrikan diserap** ke 6 laci, 648 MB.
Vault kini **132 PDF**.

**Butir "menunggu R4" yang tertutup:** efisiensi UPS (Riello, 190 hal), bitrate & sensitivitas
kamera (15 lembar data), NETD kamera termal, batas kanal server analitik, kapasitas jaringan.

**Yang tidak dapat ditutup dengan menyaring:** derating genset, DoD & umur siklus baterai,
unjuk kerja pengendali RAID, redaman konektor serat, spesifikasi alat uji. Laci `GENSET/`
dan `TEST-EQUIPMENT/` **kosong**. Kelimanya harus diminta ke pabrikan saat proyek berjalan.

**Temuan yang menegaskan celah R1:** dari 761 berkas, hanya **satu** yang bertingkat R1 —
Peraturan Kejaksaan 2024, bukan teknis. **PUIL dan SNI benar-benar tidak ada di mesin ini.**
Empat celah R1 tidak dapat ditutup dengan menyaring.

**Empat kesalahan klasifikasi yang tertangkap saat menyetel, dan sebabnya:**

1. "G**emi**lang" cocok pola `EMI` → masuk pembumian. "**Perka**sa" cocok pola peraturan →
   masuk R1. "Tindak **Pid**ana" cocok `PID` → masuk instrumentasi. **Sebab: singkatan
   pendek tanpa batas kata.**
2. 32 lembar data produk terbaca **R2** karena menyebut "sesuai IEC 60950" di kaki halaman.
   **Kepatuhan bukan standarnya.** R4 kini diperiksa sebelum R2.
3. Laci `UPS/` sempat berisi 14 berkas, **13 bukan UPS** — kata "battery" pada manual telepon
   adalah keterangan aksesori. **Sebab: mencocokkan kata di seluruh isi halaman.** Alat kini
   menimbang daerah judul 3×; hasilnya turun ke 1 berkas, dan yang satu itu sahih.
4. Satu berkas bernama `CATGENX0Y17IREN.pdf` hampir terlewat — ternyata **Katalog Umum
   Riello UPS, 190 halaman**. **Nama berkas tidak dapat dipercaya; halaman judul harus
   dibuka.**

**27 berkas ditahan di `_PERLU-DIPERIKSA/`** — sebagian besar hasil pindaian tanpa lapis
teks. Berstatus `INTAKE_ONLY`, belum boleh dikutip. Sistem sengaja **tidak menebak** laci
untuk berkas yang tidak dapat dibacanya.

Rincian: `02_REGISTERS/R4-STATUS.md` · `02_REGISTERS/INTAKE-RINGKAS.md`

---

### T23. Penyaringan R3 — lima laci baru, kategori naik ke 17 — SELESAI 20 Agustus 2026

Triase menandai **133 nama unik** sebagai R3. Setelah diperiksa, **hanya 12 yang benar-benar
buku rujukan.**

| Laci baru | Buku | Membuka |
|---|---|---|
| **CIVIL-STRUCTURAL** | Hibbeler · Darwin/Dolan/Nilson · Segui · Mamlouk | **Menara, dudukan antena, pondasi** — sebelumnya tanpa sandaran sama sekali |
| **GEOSPATIAL-SURVEY** | Bolstad & Manson · Kavanagh & Mastin | Pengukuran lapangan, koordinat, datum |
| **PROJECT-QUALITY** | Nicholas & Steyn · Siegel · Rumane ×2 | **ITP, inspeksi, audit mutu** — menopang gate G4–G7 |
| **HVAC-BUILDING** | Grondzik & Kwok | Pendinginan ruang perangkat |
| **SOFTWARE-DATA** | *Deep Learning* | Dasar analitik video & ASR |

**Rak kini 21 laci R3** (semula 16), **146 PDF di vault**, kategori teknik aktif naik dari
12 ke 17. Seluruh buku baru berstatus `INTAKE_ONLY` — sudah di laci, **belum diresume**.

**Yang dilewati dan alasannya:** AutoCAD Electrical (236 MB) — tutorial perangkat lunak,
tidak memasok rumus/ambang/metode uji. 76 berkas < 5 MB — fragmen, bukan buku.

**Daftar serap R3 ditulis tangan, bukan hasil tebakan mesin.** Alasannya ada di temuan berikut.

### ⚠ Temuan struktural: 38 dokumen kerja GSP tidak punya rumah

**579 MB** — Kajian Teknis Arsenal, Laporan Audit Log (6 keluaran), Kajian Pemeliharaan IDS
(5 revisi), Laporan Pelatihan, paparan Geospatial & DEMS, Technical Report ADINT — tertangkap
triase sebagai "R3", padahal **keluaran GSP sendiri, bukan sumber rujukan**.

**Tidak dimasukkan ke `03_SOURCE-VAULT/`, dan itu disengaja.** Menaruh keluaran sendiri di
laci sumber membuat pekerjaan GSP terlihat seperti sandaran eksternal — kesalahan yang
paling sulit diperbaiki kemudian, karena sekali dikutip sebagai rujukan, jejaknya menyebar
ke dokumen turunan.

Tetapi dokumen ini berharga dan **tidak punya tempat di EKAS**: map `06`–`09` untuk proyek
**berjalan**, `99_ARCHIVE/` untuk yang **tidak berlaku**, `03_SOURCE-VAULT/` untuk sumber
**eksternal**. Ketiganya tidak cocok.

**Diusulkan map baru `96_PROJECT-PRECEDENT/`** — bersifat **preseden, bukan sumber**: boleh
dipakai melihat bagaimana kajian pernah disusun, tetapi angkanya tetap harus ditelusuri ke
sumber aslinya. **Belum dibuat** — penambahan map tingkat atas adalah keputusan pemilik rak.

Rincian: `02_REGISTERS/R3-STATUS.md`

---

### T24. `New folder` diserap — lini konstruksi & gambar teknik dibuka — SELESAI 21 Agustus 2026

Dua EPUB AutoCAD Electrical dikonversi ke PDF (PyMuPDF, A4/11 pt, daftar isi jadi bookmark:
390 dan 435 entri). Pemeriksaan folder menemukan **25 PDF**, sebelas di antaranya sudah
diserap pada T23 — **14 sisanya diserap sekarang, 948 MB.**

| Laci baru | Buku |
|---|---|
| **CONSTRUCTION** | Peurifoy *Construction Planning, Equipment & Methods* (1.282 hal) · Holm *Construction Cost Estimating* · Mubarak *Construction Project Scheduling and Control* |
| **DRAWING-CAD** | Madsen *Engineering Drawing and Design* (1.104 hal) · Ching *Architectural Graphics* · *Professional Practice of Architectural Working Drawings* · AutoCAD Electrical ×2 · AutoCAD Civil 3D |
| **BUILDING-CONSTRUCTION** | Ching *Building Construction Illustrated* · Sacks *BIM Handbook* · Ching & Winkel *Building Codes Illustrated* |
| **PROJECT-QUALITY** (+2) | *Construction Quality Management* · Watts *Engineering Documentation Control Handbook* |

**Rak R3 kini 50 berkas · 24 laci · 2,3 GB.** Register induk **56 baris**.
Seluruh yang baru berstatus `INTAKE_ONLY` — di laci, **belum diresume**.

**Tiga peringatan yang ditulis ke `_ISI.md` laci masing-masing:**

1. **Tiga berkas AutoCAD adalah tutorial perangkat lunak.** Ia mengajarkan memakai alat,
   **tidak memasok rumus, ambang, maupun metode uji.** Tidak boleh dikutip sebagai sandaran
   teknis. Diserap karena diminta, dengan penanda jelas.
2. **Dua AutoCAD Electrical berasal dari EPUB.** EPUB tidak berhalaman tetap — nomor
   halamannya hasil pembentukan ulang pada A4/11 pt dan **tidak cocok dengan edisi cetak
   mana pun**. Kutip nomor PDF saja; bila ukuran hurufnya diubah, penomorannya bergeser.
3. **Building Codes Illustrated berbasis IBC Amerika.** Berguna memahami penalaran kode,
   **tidak dapat dipakai menyatakan kepatuhan di Indonesia.** Celah R1 tidak berkurang.

**Cacat berkas yang tercatat:** *BIM Handbook* dan *GIS Fundamentals* tanpa bookmark;
*GIS Fundamentals* teksnya rusak akibat OCR — Ctrl+F akan sering gagal.

---

### T25. Pemeriksa keutuhan + akar rak dibereskan — SELESAI 21 Agustus 2026

**Dua perbaikan yang paling menahan pembusukan sistem.**

#### 1. `90_TOOLS/periksa_ekas.py` — pemeriksa keutuhan

Delapan pemeriksaan: register ↔ berkas · kartu ↔ register (termasuk kecocokan domain) ·
manifest laci ↔ isi sebenarnya · salinan ganda dalam vault · berkas yatim tak terdaftar ·
jalur yang tidak dapat diselesaikan · kutipan halaman melebihi jumlah halaman (`--halaman`) ·
sumber kebenaran ganda di luar EKAS.

Keluar dengan **kode 1 bila ada GALAT** — dapat dipakai sebagai gerbang otomatis.

**Jalan pertama menemukan 11 GALAT.** Dua di antaranya salah lapor dari pemeriksanya
sendiri (nama berkas `.pdf` terbaca sebagai jalur map) — diperbaiki. Sembilan sisanya nyata:

- **11 kartu pengetahuan menunjuk `RANTAI-JAMINAN.md` yang tidak ada** pada domain
  NETWORKING, CYBERSECURITY, CRITICAL-INFRASTRUCTURE, MECHANICAL. Kartu kini menyatakan
  terus terang bahwa rantainya **belum disusun**, bukan menunjuk berkas hantu.
- **97 berkas R4 tidak terlihat register sama sekali.** Ditambahkan 6 baris kumpulan
  (`REF-OEM-*`) beserta 5 kartu pengetahuan yang menyebut batas pemakaiannya.
- Satu ketidakcocokan domain antara kartu dan register.

**Keadaan sekarang: GALAT 0.**

#### 2. Akar rak dibereskan — sumber kebenaran ganda dihapus

Sampai hari ini **30 berkas ada dua salinan** — akar dan EKAS. Bila salah satu disunting,
tidak ada yang menyatakan mana yang berlaku. Ini kelas kegagalan yang sama dengan 24 folder
topik yang dihapus pada T21, dan masih tersisa di akar.

Perbandingan dilakukan **menurut isi, bukan nama** — sembilan berkas berganti nama saat
masuk EKAS (`PETA-CELAH-KOLEKSI.md` → `GAP-REGISTER.md`, `_sistem/rantai/*` →
`RANTAI-JAMINAN.md`, dan seterusnya). Hasilnya: **30 identik, 0 berbeda** — aman dihapus.

| Tindakan | Jumlah |
|---|---|
| Berkas akar/`_sistem`/`_tools` dihapus (bersalinan) | **30** |
| Perkakas yang hanya ada di luar, disalin masuk | 2 |
| Rujukan jalur akar diperbarui di dokumen & skill | **14 di 6 berkas** |
| EKAS lama di akar dihapus (arsipnya di `99_ARCHIVE/LEGACY-EKAS`) | 203 berkas |
| `tree.txt` diarsipkan sebagai rekaman struktur sebelum migrasi | 1 |

**Akar rak kini berisi empat hal saja:** `BACA-INI.md`, `GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/`,
`_koleksi-lain/` (non-teknis, sengaja di luar vault), dan `New folder/` (belum disaring).

`BACA-INI.md` memuat tabel "dulu di akar → sekarang di mana", supaya tautan lama tetap
dapat ditelusuri.

---

### T26. Dua puluh enam buku diresume — tidak ada lagi `INTAKE_ONLY` — SELESAI 21 Agustus 2026

Tiga batch, 25 berkas resume, 26 kartu pengetahuan. **Peringatan pemeriksa turun 27 → 1.**

| Batch | Domain | Buku |
|---|---|---|
| 1 | PROJECT-QUALITY | Rumane ×2 · Watts · Nicholas & Steyn · Siegel · Construction Quality Mgmt |
| 2 | CIVIL-STRUCTURAL · CONSTRUCTION | Hibbeler · Segui · Darwin · Mamlouk · Peurifoy · Holm · Mubarak |
| 3 | DRAWING-CAD · BUILDING · GEOSPATIAL · HVAC | Madsen · Ching ×3 · Bakhoum · AutoCAD ×3 · Sacks · Kavanagh · Bolstad · Grondzik |

**Register: 49 ACTIVE · 9 terbatas · 3 pointer · 1 intake** (laci tahanan R4).

#### Temuan yang paling berarti

**1. Seluruh buku sipil & bangunan berbasis standar Amerika.** ASCE 7, AISC, ACI 318, ASTM,
IBC, ADA, ASHRAE, NEC, NFPA — **tidak satu pun padanan Indonesianya ada di rak**. Tujuh
celah baru dicatat: `GAP-015` … `GAP-021` (SNI 1727, 1726, 1729, 2847, AHSP, ASTM/SNI uji
bahan, buku teks pembelajaran mesin).

Akibatnya ditulis ke tiap kartu: **metodenya boleh dipakai, angka dan pasalnya tidak.**
Contoh paling nyata — tabel profil baja Segui adalah profil W/HP/HSS Amerika, bukan
WF/H-beam SNI; **tidak dapat dipakai langsung meski terlihat mirip.**

**2. `Deep-learning.pdf` ternyata makalah, bukan buku.** Tinjauan *Nature* sembilan halaman
(LeCun, Bengio & Hinton 2015) — dinilai R3 pada T23 **dari nama berkas tanpa membukanya**.
Dikoreksi ke R5 `POINTER_ONLY`. **Laci `R3/SOFTWARE-DATA/` kini kosong.**

**3. Tiga judul CAD adalah tutorial perangkat lunak**, ditandai tegas: tidak memuat rumus,
ambang, maupun metode uji, dan **tidak boleh dikutip sebagai sandaran teknis**. AutoCAD
Civil 3D 2011 bahkan sudah 15 tahun — diusulkan `SUPERSEDED`.

**4. Empat cacat berkas tercatat:** bookmark Watts rusak (390 entri pengenal ScienceDirect);
*GIS Fundamentals* tanpa bookmark **dan teks rusak OCR** sehingga Ctrl+F sering gagal;
*BIM Handbook* tanpa bookmark; *Building Construction Illustrated* hanya 18 bookmark untuk
515 halaman.

**5. Peringatan yang ditulis ke setiap kartu sipil:** perhitungan struktur yang menanggung
keselamatan orang **wajib ditandatangani ahli bersertifikat**. Rak ini membuat GSP mampu
memeriksa dan berdiskusi — bukan menggantikan tanda tangan itu.

#### Skill diperbarui

`pustaka-teknis` — enam baris domain baru pada tabel, dan tiga bagian pertanyaan→halaman
di `01-indeks-rumus.md`: proses & mutu (8 pertanyaan), struktur & konstruksi (14),
bangunan & gambar (9). `03-batas-dan-celah.md` mencatat status dan cacat berkas.

---

### T27. Rantai I dan J disusun — NETWORKING & CYBERSECURITY — SELESAI 21 Agustus 2026

Dua domain yang **paling lama pincang**: bukunya ada sejak awal, resumenya lengkap, tetapi
**tidak pernah punya rantai jaminan**. Rak kini punya **10 rantai dari 22 domain**.

#### Rantai I — Jaringan IP sistem terpasang

Dibedakan dari rantai H: H menangani penyimpanan dan BDP transfer jarak jauh, I menangani
jaringan yang menopang sistem pengawasan dan bukti digital.

**Keputusan yang paling sering keliru — anggaran PoE.** Switch 24 port PoE+ tidak berarti
sanggup memberi 30 W ke 24 port sekaligus; **daya total catu hampir selalu lebih kecil**
daripada jumlah daya maksimum semua port. Angkanya dari lembar data **[R4]**, dan
`R4/NETWORK/` sudah berisi 28 lembar data.

**Uji yang paling sering dilewati — cabut kabel.** Redundansi hanya terbukti bekerja bila
diuji dengan mencabut, bukan dengan membaca konfigurasi.

Satu-satunya ambang normatif di rantai ini: **waktu deteksi hilangnya sinyal video**,
8/4/2 detik menurut security grade [R2, BS EN 62676-1-2 PDF 34]. Sisanya dari hitungan dan
kontrak.

#### Rantai J — Keamanan siber & bukti digital · ⚠ PUTUS

**Rantai kedua yang putus, dan putusnya lebih luas daripada D.** Pada D satu ambang hilang;
pada J **seluruh sumber R1 dan R2 tidak ada** — UU ITE, Perban BSSN, ISO/IEC 27001,
NIST SP 800-86, ISO/IEC 27037.

Tiga hal **tidak dapat diuji sama sekali**: kepatuhan ISO 27001, kriteria audit BSSN, dan
keterterimaan bukti di pengadilan. Ketiganya justru yang paling sering diminta pada tender
DEMS dan sistem keamanan instansi.

Rantai memuat tabel **"yang boleh dan tidak boleh dikatakan"** — misalnya boleh menulis
*"mengikuti proses penanganan bukti empat tahap [R3, Alsmadi PDF 266–268]"*, **tidak boleh**
menulis *"memenuhi ISO/IEC 27037"*.

**Butir wajib baru pada gate G6 domain ini: pernyataan batas kepatuhan** — menyebut standar
mana yang belum dapat dibuktikan. Menyatakannya sejak awal jauh lebih kuat daripada menunggu
pemeriksa menemukannya.

**Jalan tercepat menutup:** NIST SP 800-86 tersedia **bebas dari NIST** — satu unduhan
menaikkan lini DEMS dari R3 ke R2.

---

### T28. Rantai K dan M disusun — struktur & mutu — SELESAI 21 Agustus 2026

**Dua belas rantai dari 22 domain.** Empat rantai disusun hari ini (I, J, K, M).

#### Rantai K — Struktur penopang perangkat · ⚠ PUTUS

**Rantai ketiga yang putus.** Empat buku memberi **seluruh metode** — dari beban sampai
sambungan — tetapi **tidak ada satu pun SNI struktur di rak**: `GAP-015` sampai `GAP-018`.

**Peringatan yang membedakan rantai ini dari D dan J:** struktur yang gagal **menjatuhkan
perangkat dan bisa menimpa orang**. Ini bukan soal dokumen yang dipersoalkan auditor.

Karena itu tiga jalan sah pada rantai D **tidak seluruhnya berlaku di sini**. Jalan ke-3
(melaporkan hasil ukur tanpa pernyataan lulus) **dilarang** untuk menara, dudukan di
ketinggian, atau apa pun yang dapat jatuh menimpa orang — hanya jalan 1 (standar dari
kontrak) dan 2 (tanda tangan ahli bersertifikat) yang sah.

Dua hal teknis yang ditekankan:

- **Langkah "periksa determinasi & kestabilan" sering dilewati, dan itu fatal.** Rangka
  tidak stabil **tidak menghasilkan gaya batang yang bermakna** — perangkat lunak tetap
  memberi angka, tetapi angkanya tidak berarti apa-apa. [Hibbeler PDF 63]
- **Beban angin hampir selalu menentukan** pada dudukan antena dan kamera di ketinggian,
  bukan berat perangkatnya. Antena parabola kecil dapat menghasilkan gaya angin beberapa
  kali berat sendirinya.

**Satu-satunya baris yang tidak putus:** uji tarik angkur — kapasitasnya dari lembar data
pabrikan **[R4]**, satu-satunya tingkat sah yang tersedia di domain ini.

#### Rantai M — Mutu, audit, kendali dokumen

**Bentuknya berbeda dari sebelas rantai lain.** Ia tidak menelusuri satu besaran teknis;
ia **melingkupi rantai lain** — yang dijaga bukan "berapa", melainkan apakah rantai lain
benar-benar dijalankan dan buktinya bertahan diperiksa.

"Pengujian" pada rantai ini berupa **audit internal sebelum serah** — supaya temuan
ditemukan sendiri, bukan oleh pemberi kerja.

Memuat tabel kaitan ke dua belas rantai lain: apa yang diperiksa rantai M pada masing-masing.
Tiga di antaranya bertanda ⚠ karena putus — **rantai M yang memastikan putusnya dinyatakan,
bukan disembunyikan.**

Ukuran kemajuan yang paling jujur menurut rantai ini: **baris `TPL-06` yang kolom
`EVIDENCE-ID`-nya kosong belum selesai**, sekalipun pekerjaan fisiknya sudah rampung.
Angka itu tidak dapat dinegosiasikan.

#### Ringkasan status rantai

| Utuh (7) | Bersyarat (2) | ⚠ Putus (3) |
|---|---|---|
| A serat · B video · C daya · E isolasi · F termal · I jaringan · M mutu | G keandalan (perlu adopsi kontrak) · H penyimpanan (tanpa sandaran normatif) | **D** pembumian · **J** siber · **K** struktur |

Sepuluh domain masih tanpa rantai — seluruhnya bernilai lebih rendah:
BUILDING-CONSTRUCTION, CONSTRUCTION, DRAWING-CAD, GEOSPATIAL-SURVEY, HVAC-BUILDING,
MECHANICAL, CRITICAL-INFRASTRUCTURE, SOFTWARE-DATA, STORAGE-DATACENTER, PERLU-DINILAI.

---

### T29. Daftar rujukan skill dibangkitkan dari register — SELESAI 21 Agustus 2026

**Pemeriksaan cakupan skill menemukan 18 rujukan tidak disebut skill mana pun** — termasuk
empat dari lima standar R2. Resumenya ada, kartunya ada, tetapi **tidak terjangkau** dari
lapisan yang dipakai sehari-hari.

Diperbaiki dengan `90_TOOLS/bangun_daftar_skill.py` yang membangkitkan
`pustaka-teknis/references/04-daftar-rujukan-lengkap.md` **langsung dari register** —
seluruh 62 rujukan, dikelompokkan per domain, lengkap dengan tingkat R, status otoritas,
laci, dan status rantai domainnya.

**Dibangkitkan, bukan ditulis tangan.** Daftar yang disunting tangan akan menyimpang dari
rak begitu satu sumber ditambah; daftar yang dibangkitkan tidak bisa.

#### Dua klaim usang yang ikut diperbaiki

`pustaka-teknis/SKILL.md` masih menyebut **"22 buku"** di dua tempat, termasuk pada
deskripsi pemicu skill. Angka itu benar pada 19 Agustus dan salah sejak 20 Agustus.
Diganti: **62 rujukan / 160 berkas**.

#### Satu ketidakcocokan angka yang dijelaskan, bukan disembunyikan

Register punya **62 baris** tetapi vault berisi **160 berkas**. Bedanya disengaja dan kini
tertulis pada daftar:

- **REF-BAT-002 mewakili dua standar** — IEEE 1188-2005 dan IEC 62485-2 berbagi satu resume
  karena menjawab pertanyaan yang sama.
- **Enam baris `REF-OEM-*` mewakili 97 lembar data** — dokumen produk didaftar per **laci**,
  bukan per berkas.

Karena itu tabel sebaran menunjukkan **R2 = 4 baris** walau standarnya lima, dan
**R4 = 6 baris** walau berkasnya 97. Tanpa penjelasan, dua angka itu akan terbaca sebagai
kesalahan register.

---

### T30. Uji coba P00 — perangkat gate dipakai untuk pertama kalinya — SELESAI 21 Agustus 2026

Satu lingkup kecil — **jalur serat optik 3,2 km, 8 core** — dijalankan melewati **G0–G6**
memakai seluruh perangkat: kartu kendali, tujuh templat, enam register, rantai **A**.
Sampai hari ini semuanya **belum pernah dipakai sekali pun**.

Kode **`P00` dicadangkan untuk contoh**; tiap berkas diawali kotak peringatan bahwa angkanya
karangan. Uji coba **sengaja tidak diselesaikan sampai semua centang hijau** — yang berguna
justru melihat bagaimana gate yang belum terpenuhi *terlihat* pada berkas.

#### Lima temuan

**1. ⭐ Gate G4 bergantung pada G3, dan itu tidak pernah dinyatakan.** Ambang uji rugi
sisipan **berasal dari hitungan**, jadi ITP tidak dapat disetujui sebelum hitungannya
diperiksa orang kedua. Pada uji coba, prasyarat itu **memblokir dua butir uji terpenting**.
Aturannya kini masuk `ASSURANCE-GATES.md` sebagai aturan nomor 3 — dengan pengecualian:
ambang dari R1/R2 tidak terkena, karena sudah sah sejak G0.

**2. Dua templat yang dituntut gate ternyata tidak ada.** `07_.../ITP/` dan
`07_.../NON-CONFORMANCE/` punya map dan disebut gate, tetapi **tidak ada `TPL` untuk
mengisinya** — ITP-P00 terpaksa disusun dari nol. Dibuat **`TPL-08-ITP`** dan **`TPL-09-NCR`**.

**3. `TPL-02` tidak menampung hasil lebih dari satu.** Anggaran rugi menghasilkan **dua
ambang** (1310 nm dan 1550 nm) karena rugi serat berbeda menurut panjang gelombang; templat
hanya punya satu baris Hasil. Diberi tabel hasil per kondisi.

**4. Penomoran berita acara tidak konsisten** — `DOCUMENT-CONTROL.md` mencontohkan
`BA-FO-014` tanpa nomor proyek sementara seluruh awalan lain memakainya. Diselaraskan.

**5. Kartu kendali dan lembar perhitungan saling menyalin** — sekitar 60% isi kartu adalah
salinan CALC. **Belum diperbaiki; ini keputusan, bukan cacat.** Saran: pertahankan kartu
(agar dapat dibaca sendiri saat dilampirkan BA) tetapi **dibangkitkan dari CALC**, bukan
diketik ulang. Alatnya belum ada.

#### Yang ternyata bekerja baik

**Penandaan `ASSUMPTION` langsung berguna.** Satu masukan bertanda asumsi — rugi sambungan
0,3 dB — memaksa kolom kepekaan diisi, dan kepekaan itu memunculkan hal yang tidak terduga:
**rugi konektor menyumbang 3,00 dB dari 6,40 dB**, hampir separuh anggaran hanya dari empat
konektor. Tanpa penandaan, perhatian akan tertuju ke sambungan yang jumlahnya lebih banyak.

**`TPL-06` memberi angka yang tidak dapat dinegosiasikan** — 7 dari 7 baris kolom
`EVIDENCE-ID` kosong. Tidak ada ruang menyatakan "hampir selesai".

**Pemeriksaan tingkat pada G4 menangkap hal nyata** — ambang bermetode R3 sah hanya karena
kontrak pasal 7.3 mengadopsi IEC 61280-4-2. Tanpa pasal itu rantai putus, dan kotak centang
`TPL-03` memaksa hal itu diperiksa.

#### Yang masih belum terbukti

Uji coba berhenti di **G6** karena tidak ada bukti mentah. `EVIDENCE-REGISTER` dan
`ASSET-REFERENCE-REGISTER` tetap kosong — **bagian G5–G7 hanya dapat diuji pada pekerjaan
sungguhan.**

Rincian: `00_START-HERE/TEMUAN-UJI-COBA-P00.md`

---

### T9. Petakan celah koleksi — ✅ SELESAI 19 Agustus 2026

Hasilnya dituangkan pada berkas terpisah: **`PETA-CELAH-KOLEKSI.md`**.

Ringkas temuannya:
- **Delapan lini kerja sudah tertutup rapat**, tiga di antaranya sangat kuat (jaringan,
  pembumian, pengawasan video).
- **Empat celah prioritas tinggi**: standar video atas IP (ONVIF), standar kelistrikan
  Indonesia (PUIL/SNI), penanganan bukti digital, dan ISO/IEC 27001. Tiga yang pertama
  menutup celah yang **berulang muncul di dokumen yang sudah pernah disusun**, bukan celah
  teoretis.
- **Sembilan dari 22 buku terbit sebelum 2012.** Sebagian besar tidak bermasalah karena
  membahas hal yang tidak berubah, tetapi tiga perlu diwaspadai saat dikutip: Battery (2000),
  UPS (2004), dan Electrical Maintenance (2008) — isi prinsipnya sahih, **angka batas dan
  rujukan standarnya** yang perlu diperiksa terhadap edisi terbaru.

---

## Urutan eksekusi yang disarankan

```
T1 (OCR RCM)  →  T2 (OCR FOA)  →  T3 (bookmark 5 buku)  →  T4 (perbaiki bookmark 4 buku)
                                                                      ↓
                                    T8 (katalog induk)  ←  T5, T6, T7 (dedup, penamaan, struktur)
```

**Status 19 Agustus 2026: P0, P1, dan P2 TUNTAS.** Tersisa P3 — T8 katalog induk dan T9 pemetaan celah koleksi, keduanya butuh keputusan bersama.

**Yang dikerjakan lebih dulu: T1.** RCM II adalah satu-satunya buku di rak ini
yang tidak punya salinan lain — berkas SWF sumbernya sudah tidak ada — sekaligus
berkas terbesar dan satu-satunya yang tidak bisa dicari **dan** tidak punya
bookmark. Satu pekerjaan menyelesaikan tiga masalah sekaligus.

---

## Prioritas pemanfaatan menurut lini kerja GSP

Kalau yang dimaksud "dikerjakan dulu" adalah **buku mana yang dibaca dulu**,
urutannya mengikuti lini pekerjaan yang sedang berjalan:

| Lini kerja | Buku inti | Pendukung |
|---|---|---|
| Sistem pengawasan video | CCTV: From Light to Pixels | Computer Vision (Szeliski), Storage Networks Explained |
| Jaringan & infrastruktur TI | TCP/IP Illustrated Vol. 1 | Network Warrior, CCNA 200-301 (2024), Computer Networking (Kurose) |
| Kabel serat optik | FOA Reference Guide | Reference Guide to Fiber Optic Testing Vol. 1 |
| Catu daya & kelistrikan | Electrical Power Equipment Maintenance | UPS and Active Filters, Battery Reference Book, Diesel Generator Handbook |
| Proteksi & pembumian | Grounds for Grounding | The Art and Science of Lightning Protection |
| Keandalan & pemeliharaan | RCM II (Moubray) | Maintenance and Reliability Best Practices, Maintenance Planning |
| Keamanan siber | Security Engineering (Anderson) | The Practice of System and Network Administration |
| Struktur & mekanik | Shigley's Mechanical Engineering Design | Infrared Thermal Imaging |
