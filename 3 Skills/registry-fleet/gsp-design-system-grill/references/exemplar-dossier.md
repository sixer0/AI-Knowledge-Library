# Exemplar Dossier - Metrik Terukur Standar Rumah

> **Bukti terukur**, bukan preferensi. Berkas ini memuat hasil reverse-engineering
> lima dokumen rujukan mutakhir perusahaan (2 xlsx, 1 docx, 2 pptx) sampai
> tingkat nilai mentah: hex warna, ukuran titik pecahan, letter-spacing dalam
> dua-puluhan titik, cell margin per konteks, modul lebar kolom, dan tier lebar
> gambar. Dipakai oleh `design-system-grill` pada **Calibration Pass (G0)**
> sebagai baseline kalibrasi, dan oleh Module K `document-quality-standards`
> sebagai sumber angka normatifnya.
>
> **Cara membaca:** tiap sub-seksi memuat **MEASURED** (nilai mentah dari file)
> lalu **RULE** (aturan yang bisa dipindahkan ke proyek lain). Yang wajib
> diwariskan adalah RULE; MEASURED adalah bukti dan titik awal, bukan nilai yang
> boleh disalin buta ke proyek dengan brand berbeda.

---

## 0. Ringkasan Temuan

Lima dokumen itu bukan lima desain; satu sistem yang diterjemahkan ke empat
medium. Yang membedakannya dari keluaran generik bukan satu keputusan besar,
melainkan sekitar dua ratus keputusan kecil yang semuanya **tidak berada pada
nilai bawaan aplikasi**.

| # | Temuan struktural | Konsekuensi bagi design system |
|---|-------------------|-------------------------------|
| T-01 | Tidak ada satu pun ukuran huruf bilangan bulat "aman" (10/11/12). Yang dipakai: 6.5, 7.0, 7.5, 8.0, 8.2, 8.5, 8.6, 9.0, 9.5, 10.5, 11.0, 13.0, 16.0, 23.0 | Skala tipografi wajib memuat pecahan; lihat §4.1 |
| T-02 | Empat keluarga huruf dengan pembagian peran ketat (serif prosa, sans condensed judul/label, mono angka/kode, sans reguler antarmuka data) | TYPE.* wajib per-peran, bukan per-level |
| T-03 | Letter-spacing eksplisit pada seluruh label caps (12–30 dalam satuan 1/20 pt) | Token TYPE.TRACK.* baru |
| T-04 | Leading ditulis **eksak dalam titik**, bukan kelipatan (13.5 / 11.5 / 11.0 / 9.0 / 20.0) | SPACE.LEAD.* wajib nilai pt |
| T-05 | `space_after` paragraf = 0; ritme vertikal dibangun dari **paragraf kosong ber-tinggi eksak** (3 / 5 / 6 pt) | Token SPACE.SPACER.* baru |
| T-06 | Cell margin tabel **asimetris dan berbeda per konteks** (start 0; end 5.65–12.75; top/bottom 3.1–7.35) | SPACE.CELLPAD.* per peran tabel |
| T-07 | Lebar kolom tabel seluruhnya kelipatan **5.669 pt (0,2 cm)** | LAYOUT.GRID.MODULE baru |
| T-08 | Tabel dan gambar memakai tiga tier lebar (77 %, 88 %, 100 % dari measure) | LAYOUT.MEASURE.* baru |
| T-09 | Tabel tanpa fill, tanpa garis vertikal; hanya tiga bobot garis horizontal (1.25 / 0.625 / 0.5 pt) | Membatalkan default I.10.2 |
| T-10 | Dua palet berdampingan: dingin untuk badan, hangat untuk sampul dan pembuka bab | COLOR.* wajib dua trek |
| T-11 | Slide diproduksi sebagai **citra full-bleed** hasil render, bukan susunan shape PowerPoint | Arsitektur turunan slides berubah total; §6 |
| T-12 | Gambar dalam sel spreadsheet ditengahkan dengan **hitungan EMU eksak**, bukan kira-kira | SPACE.IMGFIT.* baru |
| T-13 | Kosakata glif provenans (■ ◈ ◇ △ → ≥ ≤) dipakai konsisten sebagai kolom data | AAM.GLYPH.* baru |
| T-14 | Angka turunan tidak pernah diketik; seluruhnya rantai formula, ditutup lembar uji LULUS/GAGAL | AAM.PROVENANCE - bukan sekadar visual |

---

## 1. Korpus yang Diperiksa

| Kode | Berkas | Medium | Peran dalam sistem |
|------|--------|--------|--------------------|
| X-1 | Daftar Kuantitas dan Harga `[NOMOR]/GSP/RAB/[TAHUN]` | xlsx, 14 lembar | **Kanonik** - gaya rumah spreadsheet |
| X-2 | RAB Final [Proyek N] | xlsx, 3 lembar | Varian kepatuhan format pemberi kerja; pemegang pola gambar-dalam-sel |
| D-1 | Kajian Teknis Komprehensif `[NOMOR]/GSP/KT/[TAHUN]` | docx, 2 section, 105 tabel, 46 gambar | **Kanonik** - gaya rumah dokumen naratif |
| P-1 | Paparan [Sistem Intelijen N] | pptx, 23 slide | **Kanonik** - gaya rumah paparan |
| P-2 | Paparan [Sistem Tata Kelola N] | pptx, 14 aset | Konfirmasi bahwa P-1 adalah sistem, bukan sekali pakai |

Catatan penting tentang X-2: berkas ini memakai Aptos Narrow 10 pt dengan
kotak garis penuh - **bukan** gaya rumah. Ia dipertahankan karena pemberi kerja
mensyaratkan bentuk RAB baku, dan karena ia menyimpan satu pola yang tetap
kanonik: penempatan gambar di dalam sel (§5.6). Perlakukan X-2 sebagai
**compliance skin**: struktur data gaya rumah, kulit visual mengikuti
persyaratan lembaga. Warna tab lembar pada X-2 sudah memakai ink rumah
`#101418`, menandakan skin diterapkan di atas basis yang sama.

---

## 2. Sistem Warna

### 2.1 Trek dingin - badan dokumen dan data

**MEASURED** (docx D-1 dan xlsx X-1, identik lintas medium):

| Token usulan | Hex | Muncul sebagai |
|--------------|-----|----------------|
| `COLOR.INK` | `#101418` | Judul lembar, header tabel (fill), angka bertekanan, tab lembar |
| `COLOR.BODY` | `#2B3640` | Seluruh prosa badan, teks sel non-angka |
| `COLOR.MUTED` | `#6B7783` | Label mikro, nomor seksi, teks SUMBER, header tabel (teks) |
| `COLOR.RULE.HAIR` | `#C3CBD1` | Garis baris tabel, garis bawah header halaman, garis TOC |
| `COLOR.BAND` | `#EFF2F4` | Fill baris kelompok pada spreadsheet - satu-satunya fill di trek dingin |
| `COLOR.PAPER` | `#FFFFFF` | Teks pada fill INK |

**RULE.** Trek dingin memakai lima langkah nilai yang jaraknya melebar
(`#101418` → `#2B3640` → `#6B7783` → `#C3CBD1` → `#EFF2F4`): dua langkah gelap
berdekatan untuk hierarki teks, satu langkah tengah untuk keterangan, dua
langkah terang untuk garis dan pita. Jangan gunakan abu-abu netral murni;
seluruh langkah bergeser ke biru (komponen B > R pada tiap langkah).

### 2.2 Trek hangat - sampul, pembuka bab, penandaan

**MEASURED** (docx D-1, halaman sampul dan pembuka bab):

| Token usulan | Hex | Muncul sebagai |
|--------------|-----|----------------|
| `COLOR.WARM.INK` | `#14110F` | Judul sampul 23 pt |
| `COLOR.WARM.BODY` | `#33302C` | Subjudul sampul, serif italic 10.5 pt |
| `COLOR.WARM.MUTED` | `#7A756E` | Baris alamat dan baris penerima pada sampul |
| `COLOR.WARM.RULE` | `#C4BEB4` | Garis pemisah pada sampul |
| `COLOR.SEAL` | `#6E1420` | Kicker sampul; fill pita klasifikasi |
| `COLOR.SEAL.ON` | `#F6E9E9` | Teks di atas fill `#6E1420` |
| `COLOR.ALERT` | `#9B1C1C` | Kata "RAHASIA" pada header halaman |
| `COLOR.MARK` | `#B45309` | Eyebrow pembuka bab; garis kiri kotak derivasi; glif bullet |

**RULE.** Dua trek hidup berdampingan dalam satu dokumen dan **tidak boleh
dicampur dalam satu blok**. Trek hangat memiliki wilayah tetap: sampul, pembuka
bab, penandaan klasifikasi, kotak derivasi. Badan dokumen sepenuhnya dingin.
Perpindahan trek menjadi penanda hierarki tertinggi - pembaca merasakan
pergantian bab sebelum membaca kata pertamanya.

### 2.3 Warna semantik

**MEASURED.** `#2F6F6B` (teal gelap) pada sel putusan `LULUS/GAGAL` di X-1.
Hanya satu warna semantik hijau; **tidak ada merah untuk GAGAL** - sel gagal
memakai warna yang sama, yang membedakan hanyalah kata.

**RULE.** Status disampaikan lewat **kata**, warna hanya menandai bahwa sel itu
sel putusan. Ini kebalikan dari konvensi hijau/merah, dan itulah alasannya
dipertahankan: menghindari kesan dashboard otomatis.

### 2.4 Palet paparan

**MEASURED** (P-1, P-2 - hasil pengambilan sampel piksel):

| Peran | Nilai terukur | Catatan |
|-------|---------------|---------|
| Latar slide dalam | `#FDFDFD` (11–22 % piksel) | Putih hangat, bukan `#FFFFFF` |
| Latar sampul | gradien `#F5F0EE` → `#F1EBE9` | Sedikit lebih hangat dari slide dalam |
| Crimson tampilan | rumpun `#5A0000`–`#6E0A0B` | Sekeluarga dengan `COLOR.SEAL` `#6E1420` |
| Tint kutipan | `#F5ECED` / `#F6EDEE` | Fill blok pull-quote |
| Ink judul | mendekati `#000000` murni | Baris pertama judul dua nada |

**RULE.** Latar paparan tidak pernah `#FFFFFF`. Aksen paparan adalah anggota
keluarga `COLOR.SEAL` yang sama dengan dokumen cetak - satu identitas, dua
medium. Tint kutipan diperoleh dari aksen pada opacity rendah di atas latar
hangat, bukan dari abu-abu merah muda yang dipilih terpisah.

---

## 3. Keluarga Huruf dan Pembagian Peran

**MEASURED** (D-1 dan X-1):

| Keluarga | Dipakai untuk | Tidak pernah dipakai untuk |
|----------|---------------|---------------------------|
| IBM Plex Serif | Prosa badan; kolom keterangan dalam tabel | Judul, label, angka |
| IBM Plex Sans Condensed | Judul bab, judul seksi, header tabel, caption, eyebrow, wordmark footer | Prosa badan |
| IBM Plex Mono | Nomor seksi, seluruh angka dalam tabel, isi kotak derivasi, baris meta dokumen, glif bullet | Prosa |
| IBM Plex Sans (reguler) | Seluruh teks spreadsheet non-angka | Dokumen naratif |

**RULE.** Peran menentukan keluarga, bukan level. Satu baris tabel D-1 memuat
tiga keluarga sekaligus: kolom kunci Mono 7 pt, kolom nilai Mono 7.5 pt, kolom
keterangan Serif 8 pt. Pembagian ini adalah penanda anti-generik terkuat dalam
sistem, karena keluaran otomatis hampir selalu memakai satu keluarga untuk
seluruh tabel.

**RULE.** Superfamily tunggal dengan empat potongan (serif / sans / condensed /
mono) lebih disukai daripada empat keluarga tak berkerabat: metrik yang sama
membuat baris campuran tetap sejajar.

---

## 4. Skala Tipografi

### 4.1 Ukuran

**MEASURED - docx D-1:**

| Peran | Keluarga | pt | Warna | Tracking (1/20 pt) |
|-------|----------|----|-------|--------------------|
| Judul sampul | Sans Cond bold | 23.0 | `#14110F` | - |
| Judul bab | Sans Cond bold | 16.0 | `#101418` | - |
| Subjudul sampul | Serif italic | 10.5 | `#33302C` | - |
| Judul seksi (H2) | Sans Cond bold | 11.0 | `#101418` | - |
| Prosa badan | Serif | 9.5 | `#2B3640` | - |
| Judul entri TOC | Sans Cond | 8.5 | `#101418` | - |
| Nomor seksi | Mono | 8.0 | `#6B7783` | - |
| Nilai numerik tabel | Mono | 7.5 | `#101418` | - |
| Keterangan tabel | Serif | 8.0 | `#2B3640` | - |
| Kunci tabel | Mono | 7.0 | `#6B7783` | - |
| Nomor entri TOC | Mono | 7.5 | `#6B7783` | - |
| Label caption | Sans Cond bold caps | 7.0 | `#101418` | **16** |
| Teks caption | Sans Cond | 7.5 | `#2B3640` | - |
| Kicker sampul | Sans Cond bold caps | 7.0 | `#6E1420` | **30** |
| Baris alamat sampul | Sans Cond | 7.0 | `#7A756E` | - |
| Eyebrow bab | Sans Cond bold caps | 6.5 | `#B45309` | **28** |
| Header halaman | Sans Cond | 6.5 | `#6B7783` | - |
| Header tabel | Sans Cond bold | 6.5 | `#6B7783` | **12** |
| Label SUMBER | Sans Cond bold | 6.5 | `#6B7783` | **12** |
| Teks SUMBER | Sans Cond | 6.5 | `#6B7783` | - |
| Judul kotak derivasi | Sans Cond bold | 6.5 | `#B45309` | **22** |
| Pita klasifikasi | Sans Cond bold | 6.0 | `#F6E9E9` | - |

**MEASURED - xlsx X-1:**

| Peran | Keluarga | pt |
|-------|----------|-----|
| Judul lembar | Sans bold | 13.0 |
| Nilai sampul | Sans | 9.5 |
| Total besar | Mono bold | 9.5 |
| Subtotal | Mono bold | 8.6 |
| Sel data | Sans / Mono | **8.2** |
| Header tabel | Sans bold | 8.0 |
| Baris kelompok | Sans bold | 8.0 |
| Eyebrow perusahaan | Sans bold | 7.5 |
| Baris meta | Mono | 7.5 |
| Label sampul | Sans bold | 7.5 |
| Catatan SUMBER | Sans | 7.0 |

**RULE - anti-round-number.** Skala **wajib** memuat sedikitnya tiga nilai
pecahan yang tidak jatuh pada 0.0 atau 0.5 dari nilai bulat lazim. `8.2` untuk
badan spreadsheet dan `8.6` untuk subtotal adalah kunci: keduanya tidak dapat
dihasilkan oleh pemilih ukuran mana pun tanpa diketik. Satu keluarga dokumen
tanpa satu pun ukuran pecahan otomatis gagal cek anti-AI.

**RULE - badan kecil.** Ukuran badan berada di **9.5 pt untuk cetak naratif**
dan **8.2 pt untuk spreadsheet**, jauh di bawah default 11–12 pt. Ini
dimungkinkan karena leading dinaikkan (§5.1) dan measure dipersempit (§5.4).
Menaikkan ukuran badan ke 11 pt tanpa mengubah leading dan measure akan
merusak seluruh sistem.

### 4.2 Letter-spacing

**MEASURED.** Seluruh label all-caps memakai `w:spacing` eksplisit; tidak ada
label caps tanpa tracking.

| Konteks | pt | Tracking (1/20 pt) | Rasio em |
|---------|----|--------------------|----------|
| Header tabel | 6.5 | 12 | 0.092 em |
| Label SUMBER | 6.5 | 12 | 0.092 em |
| Judul kotak derivasi | 6.5 | 22 | 0.169 em |
| Eyebrow bab | 6.5 | 28 | 0.215 em |
| Label caption | 7.0 | 16 | 0.114 em |
| Kicker sampul | 7.0 | 30 | 0.214 em |

**RULE.** Tracking naik seiring naiknya "kejauhan" label dari badan teks:
label fungsional yang menempel pada data (header tabel, SUMBER) 0.09 em;
label semi-otonom (caption, judur kotak) 0.11–0.17 em; label pembuka yang
berdiri sendiri di halaman (eyebrow bab, kicker sampul) 0.21 em. Tiga tingkat
ini adalah token: `TYPE.TRACK.TIGHT`, `TYPE.TRACK.MID`, `TYPE.TRACK.WIDE`.

**RULE.** Teks all-caps tanpa tracking dilarang. Teks non-caps tidak diberi
tracking.

---

## 5. Ruang, Ritme, dan Ukuran Bidang (DOCX)

### 5.1 Leading

**MEASURED.** Leading selalu ditulis eksak dalam titik (`w:line` dengan
`lineRule="exact"`), tidak pernah sebagai kelipatan.

| Peran | Ukuran | Leading | Rasio |
|-------|--------|---------|-------|
| Prosa badan | 9.5 | **13.5** | 1.42 |
| Baris tabel | 7.0–8.0 | **11.5** | 1.44–1.64 |
| Baris TOC | 7.5–8.5 | **11.0** | 1.29–1.47 |
| Caption | 7.0–7.5 | **11.0** | 1.47–1.57 |
| Header tabel | 6.5 | **9.0** | 1.38 |
| Teks SUMBER | 6.5 | **9.0** | 1.38 |
| Judul bab | 16.0 | **20.0** | 1.25 |
| Judul sampul | 23.0 | **27.0** | 1.17 |
| Judul seksi | 11.0 | **13.5** | 1.23 |

**RULE.** Rasio leading turun saat ukuran naik: 1.42–1.44 pada teks kecil,
1.23–1.25 pada judul, 1.17 pada judul sampul. Kurva ini adalah tanda tangan
tipografi; leading tetap (1.15 atau 1.5 untuk semuanya) adalah tanda keluaran
otomatis.

**RULE.** Prosa badan dan judul seksi berbagi leading yang sama (13.5 pt)
meski ukurannya berbeda 1.5 pt - ini yang membuat judul "duduk" di grid baris
yang sama dengan badan.

### 5.2 Ritme vertikal - paragraf spacer

**MEASURED.** `space_after` seluruh paragraf badan = **0.0**. Ritme dibangun
dari paragraf kosong ber-tinggi eksak:

| Tinggi spacer | Jumlah kemunculan | Fungsi |
|---------------|-------------------|--------|
| 5.0 pt | 87 | Jeda antar-paragraf standar |
| 3.0 pt | 15 | Jeda rapat (di dalam kelompok terkait) |
| 6.0 pt + `sa` 12.0 | 1 | Jeda sampul bawah |
| 6.0 pt + `sa` 22.0 + garis bawah | 1 | Pemisah sampul |
| 1.0 pt + `sa` 18.0 | 1 | Jeda mikro sampul |

**RULE.** Jeda vertikal **tidak** dikendalikan oleh `space_after` seragam.
Tiga tinggi spacer (rapat / standar / longgar) memberi kendali per-tempat, dan
menghasilkan ritme yang tidak dapat dicapai oleh satu setelan paragraf. Token:
`SPACE.SPACER.TIGHT` (3 pt), `SPACE.SPACER.BASE` (5 pt), `SPACE.SPACER.OPEN`
(6 pt, dipasangkan dengan `space_after` tambahan).

**RULE.** Spacer bukan pengganti struktur. Rasio spacer terhadap paragraf isi
di D-1 kira-kira 1 : 1.2 - bila melebihi 1 : 1, dokumen kehilangan kepadatan.

### 5.3 Spacing per peran paragraf

**MEASURED:**

| Peran | space_before | space_after | leading | keep_with_next |
|-------|--------------|-------------|---------|----------------|
| Prosa badan | 0 | 0 | 13.5 | - |
| Judul seksi | **13.5** | **4.0** | 13.5 | ya |
| Caption | **6.0** | **2.4** | 11.0 | ya |
| Eyebrow bab | 0 | 4.0 | 9.0 | ya |
| Judul bab | 0 | **7.0** | 20.0 | ya |
| Blok SUMBER | 0 | 0 | 9.0 | - (garis atas) |

**RULE - anti-round-number pada spacing.** `2.4` pt pada caption adalah nilai
kunci yang sama pentingnya dengan `8.2` pt pada ukuran huruf. Sedikitnya satu
nilai spacing dalam sistem harus berada di luar kelipatan 0.5.

**RULE.** `space_before` judul seksi (13.5 pt) tepat sama dengan satu baris
badan. Judul mengambil satu baris kosong dari grid, bukan jarak sembarang.

### 5.4 Halaman dan measure

**MEASURED** (D-1, A4 210 × 297 mm):

| Elemen | Nilai | cm |
|--------|-------|-----|
| Margin kiri | 0.945 in | 2.40 |
| Margin kanan | 0.787 in | 2.00 |
| Margin atas | 1.024 in | 2.60 |
| Margin bawah | 0.945 in | 2.40 |
| Jarak header | 0.512 in | 1.30 |
| Jarak footer | 0.512 in | 1.30 |
| **Measure penuh** | **6.538 in = 470.6 pt** | 16.60 |

**RULE.** Margin **asimetris** pada empat sisi berbeda. Kiri > kanan (binding),
atas > bawah (ruang untuk header). Empat margin identik adalah tanda setelan
bawaan. Standar lama I.8.3 (2,5/2,5/3,0/2,5 cm) digantikan bila design system
berlaku.

### 5.5 Tier lebar - tabel dan gambar

**MEASURED.** Seluruh tabel dan gambar sejajar pada tiga (kadang lima) lebar:

| Tier | pt | in | % measure | Dipakai untuk |
|------|-----|-----|-----------|---------------|
| `NARROW` | **362.8** | 5.039 | 77.1 % | Tabel dua–empat kolom; mayoritas gambar; kotak derivasi; baris TOC; daftar bullet |
| `MID` | **413.8** | 5.750 | 87.9 % | Tabel lima–tujuh kolom |
| `WIDE` | 391.1 / 385.4 | 5.43 / 5.35 | 83 % | Dua tabel tujuh dan enam kolom yang tak muat di MID |
| `FULL` | **470.6** | 6.538 | 100 % | Pita klasifikasi sampul; blok identitas dokumen; tiga gambar besar |

**RULE.** Tabel **tidak** direntangkan ke lebar halaman secara default. Tier
NARROW adalah default; naik ke MID hanya bila jumlah kolom memaksa; FULL
disediakan untuk elemen sampul dan gambar yang butuh dampak. Konsekuensinya:
kolom kanan halaman memiliki ruang kosong yang konsisten - bukan margin tak
sengaja, melainkan bidang catatan visual.

**RULE.** Lebar gambar mengambil nilai tier yang sama dengan tabel; tinggi
bebas mengikuti rasio aslinya. Tercatat 46 gambar di D-1: 29 pada tier NARROW
berupa garis grafis tipis (362.8 × 6.8 pt, rasio 53:1 - satu per pembuka bab),
sisanya gambar isi pada NARROW / FULL / 425.2 pt (15 cm) / 306.1 pt (10.8 cm,
potret).

### 5.6 Modul lebar kolom

**MEASURED.** Seluruh lebar kolom pada 105 tabel D-1 adalah kelipatan bulat
dari **5.669 pt (0,2 cm = 113,4 twip)**:

```
17.0(3)  39.65(7)  45.35(8)  51.0(9)   56.7(10)  62.35(11) 68.0(12)
73.7(13) 79.35(14) 85.05(15) 90.7(16)  96.35(17) 102.05(18) 107.7(19)
113.4(20) 119.05(21) 124.7(22) … 362.85(64) 413.8(73) 470.6(83)
```

**RULE.** Lebar kolom dipilih dari modul 0,2 cm, bukan dari pembagian rata
lebar tabel. Akibatnya kolom-kolom **tidak** berjumlah bulat persen dan tidak
pernah terlihat "auto-fit". Token: `LAYOUT.GRID.MODULE = 5.669 pt`.

**RULE.** Modul terkecil yang dipakai adalah 3 unit (17 pt) untuk kolom glif
bullet; kolom data terkecil 7 unit (39.65 pt).

### 5.7 Cell padding per konteks

**MEASURED.** Tidak ada satu nilai padding untuk seluruh dokumen.

| Konteks tabel | top | bottom | start | end |
|---------------|-----|--------|-------|-----|
| Header tabel data | **5.10** | 5.10 | **0.0** | 7.05 |
| Baris tabel data | **4.50** | 4.50 | **0.0** | 7.05 |
| Baris TOC | **3.10** | 3.10 | **0.0** | 5.65 |
| Pita klasifikasi sampul | **4.25** | 4.25 | 7.05 / 0.0 | 7.05 |
| Kotak derivasi | **7.35** | 7.35 | **12.75** | 0.0 |
| Baris bullet | 0 | 0 | 0 | 0 |

**RULE - inset kiri nol.** Kolom pertama tabel memakai `start = 0` sehingga
teksnya rata sempurna dengan prosa badan. Tabel tampak "tertanam" dalam teks,
bukan mengambang di atasnya. Ini kebalikan dari default Word (0,19 cm kiri dan
kanan) dan merupakan salah satu perbedaan visual paling langsung terasa.

**RULE - padding naik seiring bobot.** Header (5.1) > baris data (4.5) > baris
TOC (3.1). Kotak derivasi mendapat padding terbesar (7.35 vertikal, 12.75 kiri)
karena ia satu-satunya blok yang berdiri terpisah dari aliran teks.

**RULE.** `end` padding selalu ada dan selalu lebih besar dari `start`,
menghasilkan talang kanan antar-kolom. Nilai 7.05 pt dan 5.65 pt keduanya
berada pada modul 0,2 cm (1.24 dan 1.0 unit).

### 5.8 Garis tabel

**MEASURED:**

| Garis | val | sz (1/8 pt) | pt | Warna |
|-------|-----|-------------|-----|-------|
| Atas header | single | 10 | **1.250** | `#101418` |
| Bawah header | single | 5 | **0.625** | `#6B7783` |
| Bawah tiap baris | single | 4 | **0.500** | `#C3CBD1` |
| Bawah baris TOC | single | 4 | 0.500 | `#C3CBD1` |
| Bawah header halaman | single | 4 | 0.500 | `#C3CBD1` |
| Kiri kotak derivasi | single | 10 | 1.250 | `#B45309` |
| Atas blok SUMBER | single | 4 | 0.500 | `#C3CBD1` |
| Pemisah sampul | single | 4 | 0.500 | `#C4BEB4` |

**RULE.** Tiga bobot saja: **1.25 / 0.625 / 0.5 pt**. Tidak ada garis vertikal.
Tidak ada fill pada baris tabel. Tidak ada alternating row. Bobot 0.625 pt
(sz 5) adalah nilai yang tak tersedia di antarmuka Word - hanya bisa ditulis
lewat XML, dan itu sebabnya ia bekerja sebagai penanda.

**RULE.** `sz` ganjil (5) wajib muncul sedikitnya sekali. Seluruh garis genap
(4 / 8 / 12) adalah tanda pemilihan lewat menu.

### 5.9 Pola komponen DOCX

**MEASURED - pembuka bab** (4 paragraf berurut, 29 kali):

```
p1  eyebrow    Sans Cond 6.5 bold caps  #B45309  track 28   ls 9.0   sa 4.0  kwn
p2  (kosong)                                                ls 1.0   sa 4.0  kwn
p3  judul bab  Sans Cond 16.0 bold      #101418             ls 20.0  sa 7.0  kwn
p4  (kosong)                                                ls 1.0   sa 2.4  kwn
p5  gambar garis 362.8 × 6.8 pt
```

**MEASURED - caption** (78 kali, satu paragraf dua run):

```
run1  "Tabel 1.1   "  Sans Cond 7.0 bold caps  #101418  track 16
run2  "Angka pokok…"  Sans Cond 7.5            #2B3640  tanpa track
para  sb 6.0  sa 2.4  ls 11.0  keep_with_next
```

Tiga spasi antara nomor dan teks, bukan titik atau em-dash.

**MEASURED - blok SUMBER** (28 kali):

```
para  garis atas single sz4 #C3CBD1  ls 9.0  sb 0  sa 0
run1  "SUMBER  "   Sans Cond 6.5 bold  #6B7783  track 12
run2  isi          Sans Cond 6.5       #6B7783
```

**MEASURED - daftar bullet** (tabel 2 kolom, 15 kali):

```
kolom 1  17.0 pt    "·"  Mono 8.0 bold  #B45309
kolom 2  345.85 pt  isi  Serif 9.5 justify  ls 13.5
cell margin seluruhnya 0
```

Bullet dibuat sebagai tabel, bukan daftar bernomor Word. Konsekuensinya:
gantung baris kedua presisi ke titik, dan glif bullet dapat diberi warna dan
keluarga huruf sendiri.

**MEASURED - kotak derivasi** (tabel 1 kolom, 9 kali):

```
tabel  lebar 362.85 pt  garis KIRI saja single sz10 #B45309  tanpa fill
cell   tcMar top/bottom 7.35  start 12.75  end 0
p0     "Derivasi 7.1 · …"  Sans Cond 6.5 bold #B45309 track 22  ls 9.0  sa 2.0
p1..n  isi perhitungan     Mono 7.0 #101418  ls 11.5
```

Kotak tanpa fill, tanpa kotak penuh - satu garis kiri berwarna trek hangat.

**MEASURED - header halaman:**

```
paragraf  garis bawah single sz4 #C3CBD1  tab RIGHT @ 470.55 pt (= measure penuh)
run1  "PT … · Divisi … · [judul dokumen]"  Sans Cond 6.5      #6B7783
run2  "\tRAHASIA"                          Sans Cond 6.5 bold #9B1C1C
```

Footer kosong. Nomor halaman tidak dipakai di badan - penomoran ditangani
melalui blok identitas dokumen dan pita "SALINAN 01 DARI 04".

**MEASURED - pita klasifikasi sampul** (tabel 2 kolom, 235.3 pt masing-masing):

```
fill #6E1420 pada kedua sel
teks Sans Cond 6.0 bold #F6E9E9
kiri  "KLASIFIKASI · RAHASIA"      rata kiri
kanan "SALINAN 01 DARI 04 · …"     rata kanan
tcMar top/bottom 4.25; start 7.05 (kiri) / 0.0 (kanan); end 7.05
```

---

## 6. Spreadsheet (XLSX)

### 6.1 Kerangka lembar

**MEASURED** (X-1, 14 lembar): `COVER; PETUNJUK; KOORDINAT; HITUNG-KABEL;
HITUNG-GALIAN, NERACA-POSKO, HITUNG-OPTIK, HITUNG-REKAM, HARGA-KAMERA,
RAB, REKAPITULASI, SYARAT, REGISTER-ASUMSI, KENDALI`

**RULE.** Urutan lembar mengikuti **rantai penalaran**, bukan urutan penyajian:
sampul → petunjuk membaca → data mentah → lembar hitung → lembar harga → daftar
kuantitas → rekapitulasi → syarat → register asumsi → lembar kendali. Nama
lembar seluruhnya huruf besar dengan tanda hubung, maksimum dua kata.

**RULE - lembar wajib.** Sedikitnya empat lembar tata kelola harus ada dan
tidak boleh diringkas: `PETUNJUK` (cara membaca), `SYARAT` (persyaratan
mengikat), `REGISTER-ASUMSI` (asumsi bernomor + dampak bila gugur), `KENDALI`
(uji konsistensi berformula dengan putusan LULUS/GAGAL). Empat lembar ini
adalah bagian dari design system, bukan tambahan opsional.

### 6.2 Kepala lembar (identik di 14 lembar)

**MEASURED:**

| Sel | Isi | Huruf | pt | Warna | Tinggi baris |
|-----|-----|-------|-----|-------|--------------|
| A1 | Nama perusahaan | Sans bold | 7.5 | `#6B7783` | 15.0 |
| A2 | Judul lembar | Sans bold | 13.0 | `#101418` | 20.0 |
| A3 | Baris meta | **Mono** | 7.5 | `#6B7783` | default |
| A3:n3 | - | garis bawah **medium** `#101418` | | | |
| 4 | kosong | | | | default |
| 5 | Header tabel | | | | 26.0 |

Pola baris meta: `NOMOR · REV A · DD-BULAN_ROMAWI-YYYY · KLASIFIKASI X ·
<deskripsi isi lembar dalam huruf kecil>`.

**RULE.** Kepala tiga baris + satu baris kosong + header tabel pada baris 5
diulang **identik** di setiap lembar; freeze pane ditaruh tepat di bawah header
(`A6`). Baris meta memakai Mono agar terbaca sebagai metadata mesin, bukan
judul.

### 6.3 Sel dan tabel

**MEASURED:**

| Peran | Huruf | pt | Warna | Fill | Border bawah | Align |
|-------|-------|-----|-------|------|--------------|-------|
| Header tabel | Sans bold | 8.0 | `#FFFFFF` | solid `#101418` | thin `#101418` | kiri/atas, kanan/tengah untuk kolom angka |
| Baris kelompok | Sans bold | 8.0 | `#101418` | solid `#EFF2F4` | hair `#C3CBD1` | kiri/tengah |
| Sel teks | Sans | **8.2** | `#2B3640` | - | hair `#C3CBD1` | kiri/atas, wrap |
| Sel angka | **Mono** | **8.2** | `#101418` | - | hair `#C3CBD1` | kanan/tengah |
| Sel turunan | Mono | 8.2 | `#6B7783` | - | hair `#C3CBD1` | kanan/tengah |
| Subtotal | Mono bold | **8.6** | `#101418` | - | hair `#C3CBD1` | kanan/tengah |
| Total | Mono bold | **9.5** | `#101418` | - | hair `#C3CBD1` | kanan/tengah |
| Sel putusan | Sans | 8.2 | `#2F6F6B` | - | hair `#C3CBD1` | kiri/atas |
| Catatan SUMBER | Sans (label bold) | 7.0 | `#6B7783` | - | **top** thin `#6B7783` | kiri/atas |

**RULE.** Hanya dua fill di seluruh buku kerja: `#101418` untuk header dan
`#EFF2F4` untuk baris kelompok. Baris data tidak pernah diberi fill, termasuk
tanpa alternating row. Garis hanya `hair` di bawah tiap baris - tidak ada garis
vertikal, tidak ada kotak.

**RULE.** `showGridLines = False` di seluruh lembar. Struktur dibaca dari
tipografi dan garis rambut, bukan dari kisi bawaan.

**RULE.** Angka naik ukuran seiring naik agregasi: sel 8.2 → subtotal 8.6 →
total 9.5. Kenaikan 0.4 pt tidak akan terbaca sebagai "lebih besar", tapi
terbaca sebagai "lebih berat" - itulah yang diinginkan.

### 6.4 Format angka

**MEASURED:**

```
[$-421]#,##0          nilai rupiah dan cacah
[$-421]#,##0.00       panjang dalam meter, dua desimal
[$-421]#,##0.0        panjang, satu desimal
[$-421]0.000000       koordinat lintang/bujur
[$-421]0.000          hasil hitung optik
[$-421]0.0%           porsi rekapitulasi
```

**RULE.** Awalan locale `[$-421]` (Indonesia) **wajib** pada setiap format
angka, bukan hanya pada mata uang. Ini yang membuat pemisah ribuan titik dan
desimal koma tampil benar di mesin mana pun, dan ia tidak muncul bila format
dipilih dari menu.

**RULE.** Presisi desimal mengikuti sumber pengukuran, bukan keseragaman: enam
desimal untuk koordinat, tiga untuk optik, dua untuk panjang, nol untuk rupiah.

### 6.5 Lebar kolom dan tinggi baris

**MEASURED - lebar kolom (X-1):**

| Lembar | Kolom |
|--------|-------|
| COVER | A 4.0, B 46.0, C 30.0 |
| PETUNJUK | A 4.0, B 76.0 |
| KOORDINAT | A 9.285, B 10.0, C–D 13.0, E–F 9.0, G 10.285, H 10.426 |
| HITUNG-* | A 46.0, B 8.0, C–D 13.0, E 26.0 |

**RULE.** Kolom A pada lembar bertata-letak sampul dipakai sebagai **talang
4.0** - bukan kolom data. Pada lembar hitung, kolom A justru kolom terlebar
(46) karena memuat kalimat besaran. Lebar bukan hasil auto-fit: nilai bulat
(4, 8, 13, 26, 30, 46, 76) untuk kolom yang dirancang, nilai pecahan
(9.285, 10.285, 10.426) hanya pada kolom yang lebarnya diikat ke isi.

**MEASURED - tinggi baris:**

```
baris 1  15.0     baris 2  20.0    baris 5 (header)  26.0
baris data  17.0 (rapat), 24.0 (berjeda)
baris SUMBER  28.0
lembar sampul: baris genap 26.0, baris ganjil default → pola label-nilai berselang
lembar PETUNJUK: 70, 84, 56, 42, 42 → tinggi mengikuti panjang teks
```

**RULE - baris selang-seling pada lembar sampul.** Pasangan label/nilai
diletakkan pada baris genap dengan tinggi 26, sedangkan baris ganjil dibiarkan
kosong sebagai spacer. Ini padanan spreadsheet dari paragraf spacer §5.2.

**RULE.** Tinggi baris pada lembar teks panjang **tidak seragam** - 70, 84, 56,
42, 42 mengikuti panjang paragraf masing-masing. Tinggi seragam pada lembar
berisi paragraf adalah tanda keluaran otomatis.

### 6.6 Gambar di dalam sel

**MEASURED** (X-2, lembar SPESIFIKASI TEKNIS, 28 gambar):

- Kolom gambar tunggal (kolom F), lebar piksel efektif **180 px**.
- Tinggi baris gambar: **85 pt** standar; 90 / 135 / 165 pt untuk gambar lebih besar.
- Lebar gambar bervariasi 56–160 px; tinggi 29–232 px - **rasio asli dipertahankan**.
- Anchor `TwoCellAnchor` di dalam **satu sel** (from.col = to.col, from.row = to.row).
- `colOff` selalu = `(180 − lebar_gambar) / 2` piksel, dikonversi ke EMU (× 9525).

Verifikasi pada enam sampel:

| Lebar gambar (px) | colOff terukur (EMU) | colOff / 9525 | (180 − w)/2 |
|-------------------|----------------------|---------------|-------------|
| 160 | 95 250 | 10 | 10 |
| 152 | 133 350 | 14 | 14 |
| 148 | 152 400 | 16 | 16 |
| 137 | 209 550 | 22 | 21.5 |
| 116 | 304 800 | 32 | 32 |
| 56 | 590 550 | 62 | 62 |

**RULE.** Gambar dalam sel **dihitung**, tidak diseret. Posisi horizontal =
tengah eksak; posisi vertikal = tengah dengan toleransi ≤ 2 px. Lebar maksimum
= lebar kolom − 20 px (talang 10 px di kedua sisi). Token: `SPACE.IMGFIT.GUTTER
= 10 px`, `SPACE.IMGFIT.ROW = 85 pt`.

### 6.7 Cetak

**MEASURED:** margin `0.5 / 0.5 / 0.6 / 0.7` in (kiri/kanan/atas/bawah), header
dan footer 0.5 in; `fitToHeight = 0`; orientasi per-lembar (potret untuk lembar
hitung, lanskap untuk KOORDINAT); footer `&A · lembar &P dari &N`.

X-2 memakai `0.55 / 0.55 / 0.6 / 0.7` dengan `scale = 73`, `fitToHeight = 2`.

**RULE.** Margin cetak spreadsheet juga asimetris (bawah > atas > kiri/kanan)
untuk memberi ruang footer. `fitToWidth` dibiarkan kosong dan `fitToHeight = 0`
agar lembar panjang mengalir alami alih-alih diperas.

---

## 7. Paparan (PPTX)

### 7.1 Arsitektur berkas

**MEASURED:**

| Aspek | P-1 | P-2 |
|-------|-----|-----|
| Ukuran slide | 12 192 000 × 6 858 000 EMU = 13.333 × 7.5 in (16:9) | sama |
| Jumlah slide | 23 | 14 aset |
| Bentuk per slide | 1 gambar full-bleed + 1 lencana sudut | sama |
| Resolusi aset slide | 1672 × 941 px (≈ 125 ppi) dan 1485–1890 px | sama |
| Teks native PowerPoint | **nyaris nol** (2 run) | nol |

Geometri yang berulang:

```
gambar latar   L 0.004, T 0.0, W 13.326, H 7.5   (13 dari 23 slide)
               varian: L 0.0, T 0.006–0.084, W 13.333, H 7.333–7.488
lencana sudut  L 12.727, T 0.0, W 0.603, H 0.603 (11 slide)
lencana sampul L 0.0, T 0.0, W 0.896, H 0.896
lencana penutup L 0.687, T 0.202, W 1.121, H 1.121
```

**RULE - arsitektur render.** Slide diproduksi sebagai **citra tunggal
full-bleed** hasil render dari sumber desain (HTML/SVG), lalu ditempel ke
PowerPoint. Ini keputusan sistem, bukan kebetulan, dan konsekuensinya besar:
seluruh tipografi, komposisi, dan efek bebas dari batasan mesin layout
PowerPoint. Turunan `design slides` karenanya harus menspesifikasikan **kanvas
render**, bukan master slide.

**RULE.** Lencana sudut kanan-atas berukuran tetap 0.603 in pada `x = 12.727`
(= 13.333 − 0.603 − 0.003) - menempel presisi ke tepi. Sampul dan penutup
memakai ukuran lencana berbeda (0.896 dan 1.121) sebagai penanda halaman
khusus.

**RULE - offset yang tidak nol.** Nilai `L 0.004` dan `T 0.006/0.011/0.084`
menunjukkan gambar ditempatkan manual, bukan lewat "fit to slide". Pertahankan;
offset sub-milimeter ini secara halus mematahkan kesan template.

### 7.2 Tata bahasa slide

Terbaca dari inspeksi visual P-1 dan P-2 (konsisten di kedua dek):

| Komponen | Spesifikasi terbaca |
|----------|---------------------|
| Lencana bab | Kotak sudut-tumpul `COLOR.SEAL`, angka dua digit putih, condensed bold, ± 0.55 in |
| Eyebrow | All-caps tracked di kanan lencana; hitam pada dek 1, crimson pada dek 2 |
| Judul dua nada | Baris 1 mendekati hitam, **baris 2 crimson**; condensed heavy; dua baris, tanpa titik pada baris 1 |
| Deck (paragraf pengantar) | Sans reguler, rata kiri-kanan, 3–5 baris, satu atau dua paragraf |
| Blok kutipan | Fill `#F5ECED`, garis kiri crimson, glif kutip besar, teks crimson miring |
| Rel kanan bernomor | Lingkaran crimson bernomor putih dihubungkan garis vertikal; ikon + judul + keterangan dua baris |
| Kartu mengambang | Putih, sudut tumpul, garis rambut, bayangan halus; judul mikro caps + 3–4 baris keterangan |
| Strip bawah | Deret kartu kecil (logo/regulasi) + satu kartu lebar `EXECUTIVE TAKEAWAY` |
| Footer | Segel + wordmark tracked caps; garis rambut panjang; **segmen crimson pendek di ujung kanan** |
| Hero | Render 3D metalik/kaca dengan cahaya crimson; posisi dan ukuran **berbeda tiap slide** |

**RULE - judul dua nada.** Pemecahan warna pada baris kedua judul adalah tanda
tangan utama dek. Pemecahan mengikuti makna (klausa kedua), bukan pemenggalan
baris otomatis.

**RULE - garis footer terpisah.** Garis footer terdiri dari dua segmen: garis
rambut panjang netral lalu segmen pendek `COLOR.SEAL` di ujung kanan. Detail
kecil ini muncul di seluruh slide kedua dek dan merupakan pengenal termurah
untuk direplikasi.

**RULE - hero tidak pada grid.** Posisi, skala, dan sudut hero berubah tiap
slide. Rel kiri (lencana → judul → deck → kutipan → footer) tetap; sisi kanan
dikomposisi ulang per slide. Inilah "ruang gambar yang berbeda-beda" yang harus
dipertahankan: konsistensi ada pada rel kiri, variasi ada pada bidang kanan.

**RULE - kepadatan.** Tiap slide memuat tepat satu gagasan dominan, satu hero,
satu blok kutipan, dan paling banyak satu deret kartu. Tidak ada slide dengan
dua diagram setara.

---

## 8. Arsitektur Isi yang Menyertai Visual

Temuan yang tidak visual namun tidak terpisahkan dari sistem - tanpa ini,
dokumen yang tampak benar tetap terbaca sebagai keluaran otomatis.

### 8.1 Kosakata glif provenans

**MEASURED** (X-1, kolom "Prov." dan lembar PETUNJUK):

| Glif | Arti | Frekuensi |
|------|------|-----------|
| `■` | terukur dari dokumen atau instrumen | 1 |
| `◈` | diturunkan dengan perhitungan | 16 |
| `◇` | diasumsikan, tercatat di register asumsi | 38 |
| `△` | perlu pembuktian lapangan | 1 |
| `→` `≥` `≤` `-` `–` | operator dalam kalimat teknis | 4 / 9 / 1 / 11 / 2 |

**RULE.** Setiap baris data membawa penanda provenans. Legendanya ditulis di
lembar `PETUNJUK`, bukan di catatan kaki. Glif dipilih dari satu keluarga
geometris (kotak/belah ketupat/segitiga) sehingga terbaca sebagai sistem.

### 8.2 Rantai formula hidup

**MEASURED.** Tidak satu pun nilai turunan di X-1 diketik sebagai angka.
Contoh rantai: `KOORDINAT!G6` (Haversine dari lintang/bujur) →
`KOORDINAT!$G$76` (keliling) → `HITUNG-KABEL!C13` → `RAB!G66` (nilai pekerjaan)
→ `KENDALI!B6` (uji terhadap pagu).

Lembar `KENDALI` memuat dua belas uji berbentuk
`=IF(ABS(B−C)<=0.05,"LULUS","GAGAL")` atau `=IF(B>=C,"LULUS","GAGAL")`.

**RULE.** Design system spreadsheet **wajib** menetapkan bahwa nilai turunan
hidup sebagai formula dan bahwa ada lembar kendali berisi uji berputusan.
Toleransi uji ditulis eksplisit (`±0,05`), bukan tersirat.

### 8.3 Register asumsi

**MEASURED.** Enam asumsi bernomor `ASM-01`…`ASM-06`, masing-masing dengan
kolom **"Dampak bila gugur"**.

**RULE.** Setiap asumsi tercatat bersama konsekuensinya. Kalimat penutup lembar
di X-1 merangkumnya: tidak ada asumsi yang tersembunyi di dalam angka.

### 8.4 Syarat mengikat dan pembuktiannya

**MEASURED.** `S-01`…`S-06` (syarat rancangan) dan `U-01`…`U-05` (pembuktian
lapangan), masing-masing dengan kolom rujukan silang ke lembar atau mata
pembayaran yang membuktikannya.

**RULE.** Penomoran berprefiks per jenis (`ASM-` `S-` `U-` `N-`) dan rujukan
silang eksplisit. Tanpa ini, bagian syarat menjadi daftar tanpa jangkar.

### 8.5 Baris SUMBER

**MEASURED.** 28 blok di D-1, 12 di X-1 - setiap tabel dan setiap lembar
ditutup baris `SUMBER` bergaris atas, memuat asal data dan metode.

**RULE.** Setiap tabel dan setiap lembar berakhir dengan blok SUMBER. Blok ini
memakai ukuran terkecil dalam sistem (6.5 pt docx / 7.0 pt xlsx) dan warna
`COLOR.MUTED` - hadir, tapi tidak bersaing.

---

## 9. Daftar Nilai untuk Kalibrasi Cepat

Ringkasan angka yang paling sering dibutuhkan saat menyusun design system baru
dari baseline ini. Nilai berikut adalah **titik awal terkalibrasi**, bukan
konstanta: sesuaikan ke brand proyek, tetapi pertahankan **pola**-nya (pecahan,
asimetri, tiga bobot garis, tiga tier lebar).

```
GRID.MODULE            5.669 pt   (0,2 cm)
MEASURE.NARROW       362.8   pt   (77,1 % measure)
MEASURE.MID          413.8   pt   (87,9 %)
MEASURE.FULL         470.6   pt   (100 %)

LEAD.BODY             13.5   pt   pada 9.5 pt  → 1.42
LEAD.TABLE            11.5   pt   pada 7–8 pt
LEAD.MICRO             9.0   pt   pada 6.5 pt
LEAD.TITLE            20.0   pt   pada 16 pt   → 1.25

SPACER.TIGHT           3.0   pt
SPACER.BASE            5.0   pt
SPACER.OPEN            6.0   pt

CELLPAD.HEAD           5.10 / 5.10 / 0.00 / 7.05   (t/b/s/e)
CELLPAD.BODY           4.50 / 4.50 / 0.00 / 7.05
CELLPAD.INDEX          3.10 / 3.10 / 0.00 / 5.65
CELLPAD.CALLOUT        7.35 / 7.35 / 12.75 / 0.00

RULE.STRONG            1.250 pt   (sz 10)
RULE.MID               0.625 pt   (sz 5)
RULE.HAIR              0.500 pt   (sz 4)

TRACK.TIGHT           12/20 pt    ≈ 0.09 em
TRACK.MID          16–22/20 pt    ≈ 0.11–0.17 em
TRACK.WIDE         28–30/20 pt    ≈ 0.21 em

PAGE.MARGIN         2.40 / 2.00 / 2.60 / 2.40 cm  (L/R/T/B)
PAGE.HDRFTR         1.30 cm

XLSX.SIZE.CELL         8.2 pt     XLSX.SIZE.SUBTOTAL  8.6 pt
XLSX.SIZE.TOTAL        9.5 pt     XLSX.SIZE.HEAD      8.0 pt
XLSX.ROWH.TIGHT       17 pt       XLSX.ROWH.OPEN     24 pt
XLSX.ROWH.HEAD        26 pt       XLSX.ROWH.SOURCE   28 pt
XLSX.NUMFMT.PREFIX     [$-421]

SLIDE.CANVAS        13.333 × 7.5 in  (16:9), render ≥ 125 ppi
SLIDE.BADGE          0.603 in @ x 12.727
SLIDE.BG             #FDFDFD (dalam), #F5F0EE (sampul)
```

---

## 10. Batas Keberlakuan

1. Nilai pada dossier ini diukur dari satu keluarga proyek. Ia **baseline
   kalibrasi**, bukan identitas wajib. Yang wajib diwariskan adalah RULE di tiap
   sub-seksi dan pola dalam §9.
2. X-2 adalah compliance skin, bukan gaya rumah - jangan mengambil Aptos Narrow
   10 pt dan kotak garis penuh sebagai rujukan, kecuali untuk pola gambar dalam
   sel (§6.6) dan tab lembar berwarna ink.
3. Nama proyek, nomor dokumen, nama lembaga, dan nilai anggaran dalam contoh di
   atas adalah konteks pengukuran; jangan dibawa ke design system proyek lain.
4. Bila proyek baru mengganti keluarga huruf atau warna, **rasio dan pola tetap
   berlaku**: kurva leading (§5.1), tiga tingkat tracking (§4.2), tiga bobot
   garis (§5.8), tiga tier lebar (§5.5), padding per konteks (§5.7).

---

*Exemplar Dossier v1.0 - hasil reverse-engineering 5 dokumen rujukan
(2 xlsx, 1 docx, 2 pptx), 2026-08-10. Dipakai oleh `design-system-grill`
Calibration Pass (G0) dan Module K `document-quality-standards`.*

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
