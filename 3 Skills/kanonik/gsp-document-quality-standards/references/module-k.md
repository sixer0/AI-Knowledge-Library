## Module K: Precision Formatting Layer

> **Kapan berlaku.** Module K berlaku ketika sebuah **design system aktif**
> untuk proyek (artefak `design system - [PROJECT].md` ada). Dalam kondisi itu
> Module K **menggantikan nilai default** pada I.8.1 (Font Recommendations),
> I.8.2 (Paragraph Formatting), I.8.3 (Page Layout), I.10.2 (Table Style), dan
> I.3.3 (Table Width). Aturan **non-numerik** Module I (penomoran, caption,
> klasifikasi, cross-reference, urutan field cover) tetap kanonik dan tidak
> disentuh Module K.
>
> Tanpa design system aktif, Module I tetap berlaku apa adanya.
>
> **Sumber angka.** Nilai baseline dan buktinya hidup di
> `skills/gsp/gsp-design-system-grill/references/exemplar-dossier.md` - Module K memuat
> **aturan**, dossier memuat **pengukuran**. Jangan menyalin tabel pengukuran
> ke sini (J.9 anti-duplication berlaku dua arah).

### K.1 Prinsip: Presisi Terkalibrasi

Perbedaan antara dokumen profesional dan keluaran otomatis jarang terletak pada
satu keputusan besar. Ia terletak pada beberapa ratus keputusan kecil yang
semuanya berada **di luar nilai bawaan aplikasi**. Nilai bawaan itulah yang
dikenali pembaca sebagai "buatan mesin", bukan susunan kalimatnya.

Empat prinsip yang mengikat seluruh Module K:

1. **Setiap nilai numerik dipilih, bukan diterima.** Ukuran huruf, leading,
   padding, lebar kolom, dan bobot garis harus dapat dijelaskan alasannya.
2. **Asimetri adalah default.** Margin empat sisi, padding sel, dan pembagian
   kolom tidak simetris kecuali ada alasan.
3. **Peran menentukan format, bukan level.** Keluarga huruf, ukuran, dan warna
   ditetapkan per peran (kunci, nilai, keterangan, label) - bukan per level
   heading atau per kolom.
4. **Variasi terkendali, bukan variasi acak.** Padding yang berbeda-beda per
   konteks adalah sistem tiga sampai empat nilai bernama, bukan improvisasi.

### K.2 Aturan Anti-Round-Number (WAJIB)

Nilai bawaan aplikasi berkumpul di bilangan bulat lazim: huruf 10/11/12 pt,
spacing 6/12 pt, leading 1.15/1.5, garis 0.5/1.0 pt, margin 2.5 cm. Sebuah
sistem yang seluruh nilainya jatuh di sana akan terbaca sebagai keluaran
otomatis, betapapun baik isinya.

| # | Aturan | Ambang minimum |
|---|--------|----------------|
| K.2.1 | Skala ukuran huruf memuat nilai pecahan yang bukan `.0` dan bukan `.5` | ≥ 2 nilai (mis. tipe `8.2`, `8.6`) |
| K.2.2 | Skala spacing/padding memuat nilai di luar kelipatan 0.5 pt | ≥ 1 nilai (mis. `2.4`, `7.05`, `7.35`) |
| K.2.3 | Leading ditulis **eksak dalam titik**, tidak pernah sebagai kelipatan baris | 100 % paragraf |
| K.2.4 | Bobot garis memuat nilai yang tak tersedia di antarmuka aplikasi | ≥ 1 nilai (mis. `0.625` pt = `sz 5`) |
| K.2.5 | Margin halaman berbeda pada sedikitnya tiga dari empat sisi | wajib |
| K.2.6 | Lebar kolom tabel tidak pernah hasil auto-fit maupun pembagian rata | 100 % tabel |

**Cara verifikasi.** Kumpulkan seluruh nilai numerik dalam spec design system;
bila setiap nilai dapat dicapai dengan dua klik di menu aplikasi, sistem gagal
K.2 dan wajib direvisi sebelum produksi.

### K.3 Sistem Tipografi Berbasis Peran

#### K.3.1 Pembagian keluarga huruf

Sistem memakai **tiga sampai empat keluarga** dengan pembagian peran ketat:

| Peran | Keluarga | Tidak pernah dipakai untuk |
|-------|----------|---------------------------|
| Prosa badan naratif | Serif | Judul, label, angka |
| Judul, header tabel, caption, eyebrow, wordmark | Sans Condensed | Prosa badan |
| Angka, kode, nomor seksi, metadata, isi kotak hitungan | Monospace | Prosa |
| Teks antarmuka data (spreadsheet non-angka) | Sans reguler | Dokumen naratif |

**Aturan.** Satu baris tabel boleh - dan sebaiknya - memuat tiga keluarga
sekaligus (kunci mono, nilai mono, keterangan serif). Satu keluarga untuk
seluruh tabel adalah pola keluaran otomatis.

**Aturan.** Superfamily tunggal berpotongan empat (serif / sans / condensed /
mono) lebih disukai daripada empat keluarga tak berkerabat - metrik yang sama
menjaga baris campuran tetap sejajar.

#### K.3.2 Skala ukuran

- Skala memuat **12–20 langkah**, bukan lima. Dokumen naratif rujukan memakai
  20 langkah dari 6.0 sampai 23.0 pt.
- **Ukuran badan cetak berada di 9.0–9.8 pt**, bukan 11–12 pt. Ini hanya
  bekerja bila leading dinaikkan (K.4.1) dan measure dipersempit (K.5.2).
  Menaikkan ukuran badan tanpa menyesuaikan keduanya merusak sistem.
- **Ukuran sel spreadsheet berada di 8.0–8.4 pt.**
- Angka naik ukuran seiring naik agregasi: sel → subtotal → total, dengan
  kenaikan kecil (0.4 pt) yang terbaca sebagai bobot, bukan sebagai skala.

#### K.3.3 Letter-spacing (tracking) - WAJIB pada all-caps

Setiap teks all-caps memiliki tracking eksplisit. Tiga tingkat bernama:

| Token | Rasio em | Dipakai untuk |
|-------|----------|---------------|
| `TRACK.TIGHT` | 0.08–0.10 | Label fungsional yang menempel pada data: header tabel, label sumber |
| `TRACK.MID` | 0.11–0.17 | Label semi-otonom: caption, judul kotak callout |
| `TRACK.WIDE` | 0.20–0.22 | Label pembuka yang berdiri sendiri: eyebrow bab, kicker sampul |

**Aturan.** Tracking naik seiring naiknya kejauhan label dari badan teks.
All-caps tanpa tracking dilarang. Teks non-caps tidak diberi tracking.

### K.4 Ruang dan Ritme Vertikal

#### K.4.1 Kurva leading

Leading ditulis eksak dalam titik, dan **rasionya turun saat ukuran naik**:

| Rentang ukuran | Rasio leading |
|----------------|---------------|
| Teks mikro dan tabel (6.5–8 pt) | 1.38–1.45 |
| Prosa badan (9–10 pt) | 1.40–1.45 |
| Judul seksi (11–13 pt) | 1.20–1.30 |
| Judul bab (15–17 pt) | 1.22–1.28 |
| Judul sampul (20 pt +) | 1.15–1.20 |

**Aturan.** Leading tetap (1.15 atau 1.5 untuk semua peran) adalah tanda
keluaran otomatis dan tidak diterima.

**Aturan.** Prosa badan dan judul seksi sebaiknya berbagi nilai leading yang
sama meski ukurannya berbeda - inilah yang membuat judul duduk pada grid baris
badan.

#### K.4.2 Ritme lewat paragraf spacer

`space_after` paragraf badan = **0**. Jeda vertikal dibangun dari **paragraf
kosong ber-tinggi eksak** dengan tiga nilai bernama:

| Token | Rentang | Fungsi |
|-------|---------|--------|
| `SPACER.TIGHT` | 2.5–3.5 pt | Jeda di dalam kelompok yang terkait erat |
| `SPACER.BASE` | 4.5–5.5 pt | Jeda antar-paragraf standar |
| `SPACER.OPEN` | 6–8 pt | Jeda antar-blok, dipasangkan dengan `space_after` tambahan |

**Aturan.** Rasio jumlah spacer terhadap paragraf isi tidak melebihi **1 : 1**.
Melebihi itu, dokumen kehilangan kepadatan dan spacer berubah menjadi padding.

**Aturan.** `space_before` judul seksi disetel sama dengan **satu baris badan**
(= nilai leading badan), sehingga judul mengambil satu baris kosong dari grid.

#### K.4.3 Spacing per peran

Setiap peran paragraf memiliki triplet `space_before / space_after / leading`
sendiri. Sedikitnya satu di antaranya berada di luar kelipatan 0.5 pt (K.2.2).

### K.5 Grid, Measure, dan Lebar

#### K.5.1 Modul lebar kolom

Seluruh lebar kolom tabel adalah **kelipatan bulat dari satu modul** (nilai
baseline: 0,2 cm = 5.669 pt = 113 twip).

**Aturan.** Lebar kolom dipilih dari modul, bukan dari pembagian rata lebar
tabel dan bukan dari auto-fit. Akibat yang diinginkan: kolom tidak pernah
berjumlah bulat persen dan tidak pernah terlihat otomatis.

#### K.5.2 Tier measure

Tabel dan gambar sejajar pada **tiga tier lebar** yang dinyatakan sebagai
persen dari measure penuh:

| Tier | % measure | Dipakai untuk |
|------|-----------|---------------|
| `NARROW` | 75–80 % | Default: tabel 2–4 kolom, mayoritas gambar, callout, indeks, daftar |
| `MID` | 85–90 % | Tabel 5–7 kolom yang tidak muat di NARROW |
| `FULL` | 100 % | Elemen sampul, pita klasifikasi, gambar berdampak |

**Aturan.** `NARROW` adalah default. Tabel **tidak** direntangkan ke lebar
halaman kecuali jumlah kolom memaksa. Ruang kosong yang tersisa di kanan adalah
bidang catatan visual yang disengaja, dan konsistensinya lintas halaman adalah
bagian dari identitas.

**Aturan.** Lebar gambar mengambil nilai tier yang sama dengan tabel; tinggi
mengikuti rasio asli. Gambar dengan lebar sembarang dilarang.

#### K.5.3 Margin halaman

Margin berbeda pada sedikitnya tiga dari empat sisi. Pola baseline: kiri >
kanan (binding), atas > bawah (ruang header). Margin cetak spreadsheet juga
asimetris (bawah > atas) untuk memberi ruang footer.

### K.6 Anatomi Tabel

#### K.6.1 Larangan

Bila design system aktif, hal berikut **tidak dipakai** - menggantikan I.10.2:

| Dilarang | Sebagai gantinya |
|----------|------------------|
| Fill berwarna pada header tabel | Garis atas tebal + garis bawah sedang |
| Alternating row shading | Garis rambut di bawah tiap baris |
| Garis vertikal antar-kolom | Talang lewat `end` padding |
| Kotak garis penuh mengelilingi tabel | Tidak ada garis luar sama sekali |
| Padding sel seragam satu nilai | Padding per peran (K.6.3) |

Pengecualian: **compliance skin** - bila pemberi kerja mensyaratkan bentuk tabel
baku (mis. format RAB pemerintah), kulit visual mengikuti persyaratan sementara
struktur data, penomoran, dan arsitektur isi tetap mengikuti design system.
Pengecualian ini dicatat sebagai deviasi eksplisit.

#### K.6.2 Tiga bobot garis

| Token | Rentang | Dipakai untuk |
|-------|---------|---------------|
| `RULE.STRONG` | 1.0–1.5 pt | Garis atas header tabel; garis aksen kotak callout |
| `RULE.MID` | 0.6–0.75 pt | Garis bawah header tabel |
| `RULE.HAIR` | 0.4–0.5 pt | Garis bawah tiap baris; garis header halaman; garis indeks |

**Aturan (K.2.4).** Sedikitnya satu bobot memakai nilai yang tak tersedia di
antarmuka aplikasi - pada DOCX ini berarti `w:sz` bernilai ganjil.

#### K.6.3 Padding sel per konteks

Padding **tidak** seragam. Empat konteks bernama, tiap konteks punya kuartet
`top / bottom / start / end`:

| Konteks | Pola |
|---------|------|
| Header tabel | Vertikal terbesar di antara baris tabel; `start = 0` |
| Baris data | Vertikal sedang; `start = 0` |
| Baris indeks / daftar isi | Vertikal terkecil; `start = 0`; `end` lebih kecil |
| Kotak callout | Vertikal terbesar keseluruhan; `start` besar; `end = 0` |

**Aturan - inset kiri nol.** Kolom pertama memakai `start = 0` sehingga teksnya
rata sempurna dengan prosa badan. Tabel terbaca tertanam dalam teks, bukan
mengambang di atasnya. Ini salah satu perbedaan visual paling langsung terasa
terhadap default aplikasi.

**Aturan.** `end` selalu ada dan selalu lebih besar dari `start`. Nilainya
berada pada modul K.5.1.

#### K.6.4 Baris sumber

Setiap tabel dan setiap lembar ditutup **blok SUMBER** bergaris atas, memuat
asal data dan metodenya. Blok memakai ukuran terkecil dalam sistem dan warna
teks paling redup - hadir, tapi tidak bersaing dengan data.

### K.7 Warna: Dua Trek

Sistem menjalankan **dua trek warna berdampingan** dan tidak mencampurnya dalam
satu blok:

| Trek | Wilayah | Karakter |
|------|---------|----------|
| **Dingin** | Seluruh badan dokumen, seluruh data | 5 langkah dari ink sampai pita, jarak melebar, semua bergeser ke biru |
| **Hangat** | Sampul, pembuka bab, penandaan klasifikasi, kotak callout | Ink hangat, muted hangat, garis hangat, ditambah warna segel |

**Aturan.** Perpindahan trek menjadi penanda hierarki tertinggi - pembaca
merasakan pergantian bab sebelum membaca kata pertamanya.

**Aturan - abu-abu tidak netral.** Setiap langkah abu memiliki bias warna
(dingin ke biru, hangat ke kuning). Abu-abu netral murni (`R = G = B`) tidak
dipakai.

**Aturan - status lewat kata.** Sel putusan menggunakan satu warna semantik
untuk menandai bahwa ia sel putusan; yang membedakan LULUS dari GAGAL adalah
**kata**, bukan hijau versus merah. Konvensi lampu lalu lintas menghasilkan
kesan dashboard otomatis dan tidak dipakai.

### K.8 Presisi Penempatan Gambar

#### K.8.1 Gambar dalam sel spreadsheet

Gambar **dihitung**, tidak diseret:

- `colOff = (lebar_kolom_px − lebar_gambar_px) / 2`, dikonversi ke EMU.
- `rowOff` ditengahkan dengan toleransi ≤ 2 px.
- Lebar maksimum gambar = lebar kolom − 2 × talang (baseline talang 10 px).
- Rasio asli dipertahankan; tinggi baris disetel per gambar, bukan seragam.
- Anchor dua-sel di dalam **satu sel** (`from.col = to.col`, `from.row = to.row`).

#### K.8.2 Gambar dalam dokumen naratif

Lebar mengambil salah satu tier K.5.2. Tinggi bebas. Caption mengikuti pola
label + teks (dua run, keluarga sama, ukuran dan warna berbeda, label ber-tracking).

#### K.8.3 Tinggi baris mengikuti isi

Pada lembar berisi paragraf, tinggi baris mengikuti panjang teks masing-masing
dan **tidak seragam**. Tinggi seragam pada lembar berisi paragraf adalah tanda
keluaran otomatis.

### K.9 Arsitektur Paparan Berbasis Render

Bila design system menetapkan jalur render (baseline house style), paparan
diproduksi sebagai **citra full-bleed hasil render** dari sumber desain
(HTML/SVG), lalu ditempel ke berkas presentasi - bukan disusun dari shape
aplikasi presentasi.

| Aspek | Aturan |
|-------|--------|
| Kanvas | 16:9; render pada ≥ 125 ppi terhadap ukuran slide |
| Isi slide | Satu citra full-bleed + elemen tetap berukuran kecil (lencana sudut) |
| Lencana | Ukuran tetap, menempel presisi ke tepi; sampul dan penutup memakai ukuran berbeda sebagai penanda halaman khusus |
| Offset | Penempatan manual dengan offset sub-milimeter yang tidak nol; hindari "fit to slide" |
| Rel tetap | Satu sisi slide memegang urutan tetap (lencana → judul → pengantar → kutipan → footer) |
| Bidang variasi | Sisi lain dikomposisi ulang tiap slide: posisi, skala, dan sudut visual utama berubah |
| Kepadatan | Satu gagasan dominan, satu visual utama, paling banyak satu deret kartu per slide |

**Konsekuensi bagi spec.** Turunan `design slides` menspesifikasikan **kanvas
render** (ukuran, ppi, rel tetap, bidang variasi, komponen), bukan master slide
aplikasi presentasi.

### K.10 Arsitektur Isi yang Menyertai Format

Empat komponen berikut adalah bagian dari design system, bukan tambahan
opsional. Tanpanya, dokumen yang tampak benar tetap terbaca sebagai keluaran
otomatis karena angkanya tidak dapat ditelusuri.

| Komponen | Aturan |
|----------|--------|
| **Penanda provenans** | Setiap baris data membawa glif provenans dari satu keluarga geometris (mis. terukur / diturunkan / diasumsikan / perlu pembuktian). Legenda ditulis di lembar petunjuk, bukan catatan kaki. |
| **Rantai formula hidup** | Nilai turunan hidup sebagai formula, tidak pernah diketik sebagai angka. Berlaku untuk spreadsheet; untuk dokumen naratif, padanannya adalah kotak derivasi yang menampilkan perhitungannya. |
| **Lembar kendali** | Sekumpulan uji konsistensi berformula dengan putusan lulus/gagal dan **toleransi eksplisit**. Bendera induk menyatakan status seluruh uji. |
| **Register asumsi** | Asumsi bernomor berprefiks, masing-masing dengan kolom dampak bila gugur. Rujukan silang eksplisit ke lembar atau mata pembayaran yang membuktikannya. |

**Aturan penomoran.** Prefiks per jenis (asumsi / syarat / pembuktian / catatan)
dengan nomor urut dua digit, dan setiap entri membawa rujukan silang ke tempat
pembuktiannya.

### K.11 Checklist Kepatuhan Module K (12 Poin)

Dijalankan terhadap **spec design system** sebelum produksi dokumen, dan
terhadap **dokumen jadi** sebelum serah terima.

```
[ ] K.2.1  Skala huruf memuat ≥ 2 nilai pecahan non-.0/.5
[ ] K.2.2  Skala spacing memuat ≥ 1 nilai di luar kelipatan 0.5 pt
[ ] K.2.3  Seluruh leading eksak dalam titik, tidak ada kelipatan baris
[ ] K.2.4  ≥ 1 bobot garis di luar nilai antarmuka aplikasi
[ ] K.2.5  Margin berbeda pada ≥ 3 dari 4 sisi
[ ] K.3.1  3–4 keluarga huruf dengan pembagian peran; ≥ 1 tabel berkeluarga campur
[ ] K.3.3  Seluruh all-caps ber-tracking; 3 tingkat tracking terdefinisi
[ ] K.4.1  Rasio leading turun saat ukuran naik (kurva, bukan konstanta)
[ ] K.4.2  Ritme lewat spacer bernama; rasio spacer : paragraf ≤ 1 : 1
[ ] K.5.1  Seluruh lebar kolom kelipatan modul; tidak ada auto-fit
[ ] K.5.2  3 tier measure terdefinisi; NARROW adalah default
[ ] K.6    Tanpa fill header, tanpa alternating row, tanpa garis vertikal;
           padding per konteks; blok SUMBER di tiap tabel
```

Kegagalan pada K.2.x adalah **blocking** - spec tidak boleh masuk produksi.
Kegagalan pada butir lain dicatat sebagai deviasi eksplisit dengan justifikasi.

---

