# Resume — The NICE Cyber Security Framework

**Penulis/Editor:** Izzat Alsmadi · **Penerbit:** Springer, 2019
**Subjudul:** *Cyber Security Intelligence and Analytics*
**Berkas:** `Izzat Alsmadi - The NICE Cyber Security Framework (2019).pdf` — 366 halaman, 15,7 MB
**Disusun:** 19 Agustus 2026

> **Rujukan halaman memakai nomor PDF.** Selisih ke nomor cetak **tidak tetap** (+16 sampai
> +18), jadi nomor PDF lebih aman. Bookmark bawaan **458 entri** sampai tingkat sub-bagian.

Buku ini menyusun bahan ajar mengikuti **NICE Framework** — kerangka tenaga kerja keamanan
siber terbitan NIST. Ciri khasnya (PDF 20): NICE **berorientasi pekerjaan, bukan pendidikan**,
dan memakai kompetensi **KSA** (Knowledge, Skills, and Abilities) sebagai ganti capaian
pembelajaran akademik.

Untuk GSP, nilainya ada pada **struktur per fungsi kerja** — tiap bab setara satu peran
dalam operasi keamanan siber, sehingga bisa dipakai memetakan kebutuhan personel dan lingkup
layanan.

---

## Peta isi

| Bab | Judul | PDF | Relevansi GSP |
|---|---|---|---|
| 1 | Introduction | 20 | Kerangka NICE dan KSA |
| 2 | Acquisition Management | 27 | Pengadaan berbasis keamanan |
| 3 | Continuity Planning and Disaster Recovery | 59 | Kelangsungan layanan |
| 4 | Cyber Defense Analysis and Support | 70 | Operasi pertahanan siber |
| 5 | Cyber Intelligence | 91 | — |
| 6 | Cyber Intelligence Analysis | 107 | — |
| 7 | Cyber Operational Planning | 151 | — |
| 8 | Cyber Policy and Strategy Management | 196 | Kebijakan dan tata kelola |
| 9 | Cyber Threat Analysis | 219 | Analisis ancaman |
| 10 | Cyber Security Management | 257 | Tata kelola keamanan |
| **11** | **Forensics Analysis** | **266** | ⭐ **Inti lini DEMS** |
| 12 | Identity Management | 326 | Kendali identitas |
| 13 | Incident Response | 343 | Tanggap insiden |
| — | Index | 359 | — |

---

## Bagian yang paling sering dipakai

### A. Proses forensik digital dan rantai kustodi (Bab 11, PDF 266–268) ⭐

**Bagian paling bernilai untuk GSP.** Bab 11 menguraikan proses forensik digital dasar
(Gambar 11.1) yang terdiri **empat tahap utama**:

```
1. Collection   — pengumpulan
2. Examination  — pemeriksaan
3. Analysis     — analisis
4. Reporting    — pelaporan
```

Dibahas dalam konteks **proses penyitaan dan pengawetan bukti digital, termasuk chain of
custody** (PDF 268).

> Ini kerangka proses yang selama ini **tidak ada sandaran pustakanya di rak**. Celah
> "penanganan bukti digital" pada `PETA-CELAH-KOLEKSI.md` kini **tertutup sebagian** —
> kerangka prosesnya ada, meski **NIST SP 800-86 dan ISO/IEC 27037 sendiri masih belum**.

Dipakai untuk: menyusun bagian metodologi penanganan bukti pada proposal DEMS; memastikan
rancangan sistem menopang keempat tahap, bukan hanya penyimpanan.

**Bertemu dengan** tesis Ayubi Wirara di `R5/THESIS/` yang menerapkan NIST
SP 800-101 pada konteks hukum Indonesia (UU ITE).

### B. Kemampuan tim investigasi (PDF 77)

Buku menegaskan tim investigasi harus punya **keterampilan teknis dan pengetahuan tentang
hukum dan regulasi** — bukan salah satunya saja. Mekanisme audit dan pencatatan log dipakai
untuk mencari bukti.

Berguna saat menyusun persyaratan kualifikasi personel pada dokumen penawaran layanan
forensik.

### C. Tanggap insiden (Bab 13, PDF 343)

Merujuk kumpulan sumber baku termasuk **ISO/IEC** dan publikasi NIST. Dipakai untuk menyusun
prosedur tanggap insiden pada dokumen operasional.

### D. Kelangsungan dan pemulihan bencana (Bab 3, PDF 59)

Perencanaan kelangsungan dan pemulihan — bertemu dengan `R3/STORAGE/` Bab 9
*Business Continuity* dari sisi penyimpanannya.

### E. Kerangka KSA untuk peran kerja (PDF 20)

Karena NICE berorientasi pekerjaan, tiap bab dapat dibaca sebagai **satu peran** beserta
kompetensi yang dituntut. Dipakai untuk:

- Menyusun struktur tim pada usulan layanan keamanan
- Menetapkan persyaratan kualifikasi personel di dokumen tender
- Kerangka program pembinaan internal — bersama NIST SP 800-50r1 di
  `R5/TECHNICAL-GUIDES/`

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| **Metodologi penanganan bukti digital** | **Bab 11, PDF 266–268** |
| Rantai kustodi pada rancangan DEMS | Bab 11, PDF 268 |
| Kualifikasi personel forensik | PDF 77 + kerangka KSA |
| Prosedur tanggap insiden | Bab 13, PDF 343 |
| Struktur tim layanan keamanan | Kerangka KSA, PDF 20 |
| Bagian kebijakan pada proposal | Bab 8, PDF 196 |
| Analisis ancaman | Bab 9, PDF 219 |

**Pendamping di rak:** `R3/SECURITY/` (Anderson) untuk kerangka berpikir keamanan;
`R5/THESIS/` untuk penerapan konteks Indonesia; `R5/TECHNICAL-GUIDES/` untuk
panduan operasional; `R3/CRITICAL-INFRASTRUCTURE/` (Johnson) untuk sisi objek vital.

---

## Batas buku ini

- **Buku ajar, bukan standar.** Untuk persyaratan kontrak, kutip NIST SP 800-86,
  ISO/IEC 27037, atau NICE Framework aslinya — **ketiganya belum ada di rak**.
- Berorientasi konteks Amerika Serikat; pemetaan ke regulasi Indonesia perlu tesis di
  `_tesis/` atau regulasi aslinya.
- Sebagian bab (5–7, intelijen dan perencanaan operasional siber) tidak menyentuh lini kerja
  GSP yang berjalan.
- Selisih halaman cetak–PDF tidak tetap; **selalu pakai nomor PDF**.
