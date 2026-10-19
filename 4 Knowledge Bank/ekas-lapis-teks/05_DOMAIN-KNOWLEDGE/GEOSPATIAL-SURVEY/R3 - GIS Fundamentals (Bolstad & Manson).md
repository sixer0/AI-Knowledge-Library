# GIS Fundamentals — A First Text on Geographic Information Systems

**REF-GEO-001** · **R3** · Domain **GEOSPATIAL-SURVEY** · Paul Bolstad & Steven Manson
**Berkas:** 746 halaman · **tanpa bookmark** · `R3/GEOSPATIAL-SURVEY/`

---

## Untuk apa dipakai di GSP

**Dasar sistem informasi geografis** — model data, proyeksi, datum, dan analisis spasial.
Berguna pada pekerjaan yang memetakan sebaran perangkat, cakupan pengawasan, atau jalur
infrastruktur di atas peta.

## ⚠ Dua cacat berkas yang menentukan cara memakainya

**1. Tanpa bookmark sama sekali** untuk 746 halaman.

**2. Teks rusak akibat OCR.** Contoh nyata dari halaman 41:

> *"Porollels. Eost-West lines of equol IOll!ude"* — seharusnya *"Parallels. East-West lines
> of equal latitude"*
>
> *"Roto-t1on axis at the geographic Nor th Pote"* — seharusnya *"Rotation axis at the
> geographic North Pole"*

**Akibatnya: Ctrl+F akan sering gagal.** Kata kunci teknis tidak dapat diandalkan untuk
menemukan halaman. Buku ini praktis hanya dapat dibaca **berurutan**, bukan dirujuk.

> Ini menurunkan nilai pakainya secara berarti. **Pertimbangkan mencari salinan pengganti**
> yang lapis teksnya bersih — tercatat sebagai kebutuhan pada `GAP-REGISTER`.

## Yang dapat dipakai

Bab 2 membahas **model data** — raster dan vektor — beserta sistem koordinat geografis:
paralel, meridian, dan sumbu rotasi bumi.

Pemahaman **datum dan proyeksi** adalah yang paling penting: peta yang datumnya berbeda akan
menggeser titik puluhan meter, dan itu cukup untuk membuat penempatan kamera meleset.

## Batas pemakaian

Buku pengantar. Tidak memasok ambang ketelitian maupun prosedur uji.

Konteks Amerika Utara. Indonesia memakai **SRGI2013** — tidak ada di rak.

## Menopang

Gate **G2** — dasar penempatan perangkat di atas peta. Dipakai bersama REF-GEO-002.

---

## Catatan koreksi RR3A (2026-10-11, kartu t_bd122a56)

Mode verifikasi-tanpa-duplikasi langkah 18: berkas sudah ada dan status register `ACTIVE`;
seluruh klaim terukur diuji ulang terhadap vault lewat parser (pypdf). Satu klaim dinyatakan
keliru, sisanya terkonfirmasi.

- KOREKSI-RR3A-1: kalimat "tercatat sebagai kebutuhan pada `GAP-REGISTER`" keliru. Cek-silus
  `02_REGISTERS/GAP-REGISTER.md` per 11-10-2026: kebutuhan "salinan pengganti" hanya
  terdaftar untuk Diesel Generator Handbook; tidak ada butir GIS Fundamentals. Kebutuhan
  salinan berlapis teks bersih ini dinyatakan **belum tercatat**; pencatatan resmi di
  GAP-REGISTER bukan wewenang berkas ini (dilaporkan sebagai ISU-LINTAS-OWNER, pemilik
  gerbang register langkah 21).
- Terkonfirmasi segar: 746 halaman, 0 bookmark, dan dua kutipan contoh OCR rusak muncul
  verbatim pada PDF 41 ("Porollels. Eost-West lines of equol IOll!ude"; "Roto-t1on axis at
  the geographic Nor th Pote").
- Konversi halaman: PDF 41 membawa kepala "Chapter 2: Data Models" dengan cetakan 29, jadi
  "halaman 41" pada berkas ini = nomor PDF, bukan nomor cetak (selisih +12 di titik itu).
- Nuansa uji jejak kata: "Parallels" masih ketemu di PDF 40, 134, 138, 142, tetapi
  "Rotation axis" nol hasil karena glif halaman 41 rusak. Vonis "Ctrl+F akan sering gagal"
  tetap berlaku; kegagalannya sporadis per halaman, paling parah pada halaman bergambar.

Tidak ada perubahan daya-ikat: status `ACTIVE`, tingkat R3, dan batas pemakaian tetap;
register induk tidak disentuh (penyatuan status milik langkah 21).
