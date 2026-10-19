# Resume — Reference Guide to Fiber Optic Testing, Volume 1

**Penulis:** J. Laferriere, G. Lietaert, R. Taws, S. Wolszczak · **Penerbit:** JDS Uniphase (JDSU), 2007
**Berkas:** `J. Laferriere et al. - Reference Guide to Fiber Optic Testing Vol 1 (2007).pdf` — 146 halaman, 6,1 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Konversi halaman.** Selisih **tetap +7**: halaman cetak + 7 = halaman PDF
> (cetak 1 = PDF 8). Bookmark 89 entri (4 bab + 20 sub-bab + 65 sub-sub-bab) dipasang
> 19 Agustus 2026.

Buku tipis tetapi padat, ditulis oleh pembuat alat ukur. Fungsinya di rak: **pasangan lanjut
dari FOA Reference Guide**. FOA memberi dasar dan prosedur; buku ini masuk jauh lebih dalam
ke **pengukuran** — terutama OTDR, dispersi kromatik, dan PMD.

Kalau pertanyaannya "bagaimana cara mengukur dan bagaimana membaca hasilnya", ini bukunya.

---

## Peta isi

| Bab | Judul | Cetak | PDF |
|---|---|---|---|
| 1 | **Principles of Light Transmission on a Fiber** | 1 | 8 |
| 2 | **Insertion Loss, Return Loss, Fiber Characterization** | 37 | 44 |
| 3 | **Optical Time Domain Reflectometry** | 65 | 72 |
| 4 | **Using an OTDR** | 89 | 96 |

Bookmark turun sampai tingkat seperti `1.5.3 Optical Return Loss`, jadi topik pengukuran
tertentu bisa dituju langsung.

Rincian Bab 1 yang sering dipakai: jenis serat (1.4), transmisi cahaya (1.5) yang mencakup
**atenuasi**, **dispersi**, **optical return loss**, dan **efek non-linier**, lalu standar
dan rekomendasi sistem serat optik (1.6, cetak 32 / PDF 39).

---

## Bagian yang paling sering dipakai

### A. Rugi sisipan dan rugi balik optik (Bab 2, cetak 37 / PDF 44)

Dua besaran yang muncul di hampir setiap berita acara uji serat optik:

- **Insertion Loss (IL)** — rugi total yang dialami sinyal
- **Optical Return Loss (ORL)** — daya yang dipantulkan balik ke sumber

Bab ini juga membahas **fiber characterization** — rangkaian pengukuran lengkap yang dipakai
untuk mensertifikasi jalur, bukan sekadar memastikan nyambung.

### B. OTDR: prinsip (Bab 3, cetak 65 / PDF 72)

Cara kerja OTDR dan pembacaan jejaknya. Termasuk **dead zone** — daerah tepat setelah
peristiwa pantulan di mana OTDR tidak dapat mengukur. Dead zone yang tidak dipahami adalah
sumber kesalahan pembacaan paling umum, terutama pada jalur pendek dalam gedung.

### C. OTDR: pemakaian (Bab 4, cetak 89 / PDF 96)

Bagian paling praktis: penyetelan instrumen, pemilihan lebar pulsa dan rentang, pemakaian
**launch cable**, serta cara mengeluarkan hasil terbaik dari alat.

Sejalan dengan peringatan FOA (yang lebih tegas): jangan memakai fungsi *autotest* sebelum
teknisi yang paham menyiapkan instrumen dan memverifikasi hasilnya.

### D. Dispersi kromatik dan PMD (Bab 1 bagian 1.5, sekitar cetak 21 dan 13 / PDF 28 dan 20)

Dua besaran yang menjadi pembatas pada jalur **panjang dan berkecepatan tinggi** — tidak
relevan untuk jalur dalam gedung, tetapi menjadi penting pada tautan antar-lokasi berjarak
jauh. FOA hanya menyinggung; buku ini membahasnya dengan cara pengukurannya.

### E. Standar dan rekomendasi (bagian 1.6, cetak 32 / PDF 39)

Standar internasional, nasional, standar serat optik, dan standar uji-ukur — dikelompokkan
rapi. Berguna saat menyusun daftar acuan pada dokumen teknis.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menyusun berita acara uji serat optik | Bab 2 (IL, ORL) + Bab 4 |
| Membaca dan menafsirkan jejak OTDR | Bab 3 dan 4, cetak 65 dan 89 / PDF 72 dan 96 |
| Menjelaskan pembacaan janggal pada jalur pendek | Dead zone, Bab 3 |
| Sertifikasi jalur, bukan sekadar uji kontinuitas | Fiber characterization, Bab 2 |
| Tautan antar-lokasi berjarak jauh | Dispersi kromatik dan PMD, bagian 1.5 |
| Daftar acuan standar pada dokumen | Bagian 1.6, cetak 32 / PDF 39 |

**Pendamping di rak:** `R3/FIBER-OPTIC/` (FOA, Hayes) — pasangan wajib. FOA untuk
dasar, prosedur, loss budget, dan kualifikasi teknisi; buku ini untuk pengukuran lanjut.

---

## Catatan mutu berkas

- Teks dapat dicari, mutu ekstraksi baik.
- Bookmark 89 entri dipasang 19 Agustus 2026 dari halaman daftar isi buku (PDF 4–7).
  Judul bab yang melipat dua baris sempat membuat dua bab tidak terbaca dan sudah dikoreksi.
- Terbitan 2007 dan bersifat **panduan produk pabrikan** (JDSU) — prinsip pengukurannya
  netral dan tetap berlaku, tetapi contoh instrumen yang ditampilkan sudah tidak dijual.
- Cadangan sebelum bookmark: `_asli/FO Testing Vol1 JDSU [ASLI sebelum bookmark].pdf`
