# Materials for Civil and Construction Engineering

**REF-CIV-004** · **R3 — buku teks rekayasa** · Domain **CIVIL-STRUCTURAL**
**Penulis:** Michael S. Mamlouk & John P. Zaniewski
**Berkas:** 661 halaman · 412 bookmark · `R3/CIVIL-STRUCTURAL/`
**Disusun:** 21 Agustus 2026, dari daftar isi dan isi buku ini

---

## Untuk apa buku ini dipakai di GSP

**Memahami dan memeriksa bahan** yang dipakai pekerjaan sipil pendukung: beton pondasi,
baja dudukan, agregat, aspal jalan akses, kayu bekisting.

Bermanfaat paling besar saat **memeriksa pekerjaan pihak ketiga**: apa yang harus diuji pada
beton yang datang, apa arti hasil uji tekan, mengapa agregat bermasalah.

## Susunan

| Bab | Isi | PDF |
|---|---|---|
| **1** | **Konsep rekayasa bahan** — tegangan-regangan, kekuatan, keuletan | **22** |
| 2 | Sifat dasar bahan | **77** |
| **3** | **Baja** | **110** |
| 4 | Aluminium | **169** |
| **5** | **Agregat** | **194** |
| 6 | **Semen portland, air pencampur, bahan tambah** | **244** |
| **7** | **Beton semen portland** | **288** |
| 8 | Pasangan (masonry) | **370** |
| 9 | Aspal | **386** |
| 10 | Kayu | **469** |
| 11 | Komposit | **523** |
| — | Apendiks | **553** |

## Yang dapat dipakai langsung

**Bab 1 (PDF 22 dst.)** menjelaskan dasar yang menentukan pembacaan seluruh hasil uji bahan:
diagram tegangan-regangan, dan bahwa **luas di bawah kurva sama dengan kerja per satuan
volume** yang dibutuhkan untuk mendeformasi atau mematahkan bahan (terverifikasi, PDF 40 area).

**Bab 7 — beton.** Perancangan campuran, pengujian, dan apa yang memengaruhi kekuatan.
Dipakai saat menilai hasil uji tekan silinder dari pemasok.

**412 bookmark** — buku dengan navigasi terbaik di laci ini.

## Batas pemakaian

> Buku **sifat bahan**, bukan buku perancangan. Ia menjelaskan **mengapa** bahan berperilaku
> begitu; **berapa** yang boleh dipakai ada di buku perancangan (REF-CIV-002, REF-CIV-003)
> dan pada standar bahan yang **tidak ada di rak**.

Metode uji yang dirujuk **ASTM** — juga tidak ada di rak. Indonesia memakai SNI yang setara
tetapi tidak identik.

## Menopang

Gate **G4** dan **G5** — menetapkan uji bahan apa yang diminta dan bagaimana membaca hasilnya.

---

## Catatan verifikasi RR3A (2026-10-11, kartu t_bd122a56)

Langkah 18 RESUME-R3 berjalan dalam mode verifikasi-tanpa-duplikasi: berkas ini sudah ada,
status register `ACTIVE`, maka isinya diuji ulang terhadap vault lewat parser (pypdf), bukan
ditulis ulang. Hasil ukur segar:

- 661 halaman dan 412 bookmark terkonfirmasi. Vonis "navigasi terbaik di laci ini" masih
  benar: pemegang bookmark kedua tertinggi di laci hanya 277 (ukur 11-10-2026, seluruh PDF
  laci CIVIL-STRUCTURAL).
- Pembuka bab sesuai tabel Susunan: PDF 22 (bab 1), 77 (bab 2), 110 (bab 3), 169 (bab 4),
  194 (bab 5), 244 (bab 6), 288 (bab 7), 370 (bab 8), 386 (bab 9), 469 (bab 10), 523 (bab 11),
  553 (apendiks). Tiap halaman buka diperiksa lewat cetak teks kepala halaman.
- Kutipan "luas di bawah kurva sama dengan kerja per satuan volume" nyata pada PDF 40-41
  (baris teks "work per unit volume" muncul di sana; halaman 40 memuat cetak 39).
- Konversi halaman: nomor cetak = nomor PDF dikurangi 1 (PDF 26 memuat cetakan 25; PDF 40
  memuat cetakan 39). Penanda `[PDF n]` pada berkas ini memakai nomor halaman PDF.

Tidak ada perubahan daya-ikat: status `ACTIVE`, tingkat R3, dan batas pemakaian tetap
sebagaimana terdaftar; register induk tidak disentuh (penyatuan status milik langkah 21).
