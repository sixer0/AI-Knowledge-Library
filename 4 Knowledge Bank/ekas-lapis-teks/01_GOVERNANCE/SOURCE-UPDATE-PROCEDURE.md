# Prosedur Menambah Buku ke Rak

**Lokasi rak:** `C:\Users\gspen\Videos\Buku` · **Disusun:** 19 Agustus 2026

Prosedur baku agar buku baru **masuk rak dalam keadaan siap pakai**, bukan sekadar tersimpan.
Disusun dari pengalaman membenahi 23 buku — supaya pekerjaan yang sama tidak perlu diraba
ulang.

**Perkiraan waktu:** 1–3 jam per buku, tergantung apakah perlu OCR dan apakah daftar isinya
dapat diurai otomatis.

---

## Langkah 0 — Periksa dulu apa yang dibutuhkan

Sebelum mengerjakan apa pun, jalankan pemeriksaan ini terhadap berkas baru:

```python
import fitz, os
f = r'<jalur berkas>'
d = fitz.open(f)
n = d.page_count
probe = [max(1, int(n*r)) for r in (0.15, 0.4, 0.7)]
chars = sum(len(d[p-1].get_text().strip()) for p in probe)
print('halaman   :', n)
print('ukuran    : %.1f MB' % (os.path.getsize(f)/1048576))
print('bisa dicari:', chars > 200)
print('bookmark  :', len(d.get_toc()))
print('ukuran hal:', {tuple(round(v) for v in p.rect[2:]) for p in list(d)[:20]})
```

Hasilnya menentukan langkah mana yang perlu dijalankan:

| Kondisi | Tindakan |
|---|---|
| `bisa dicari` = False | **Langkah 1** — OCR |
| `bookmark` = 0 | **Langkah 2** — bangun daftar isi |
| Judul bookmark berupa nama berkas/kode | **Langkah 2b** — perbaiki judul |
| Keduanya sudah ada | Lompat ke **Langkah 3** |

---

## Langkah 1 — OCR (bila belum bisa dicari)

**Cadangkan lebih dulu.** Tanpa kecuali.

```bash
mkdir -p "<folder>/_asli"
cp "<berkas>" "<folder>/_asli/<nama> [ASLI sebelum OCR].pdf"
```

Verifikasi cadangan dengan SHA-256 sebelum melanjutkan — jangan hanya percaya perintah
salin berhasil.

Lalu jalankan:

```bash
python "C:/Users/gspen/Videos/Buku/GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/90_TOOLS/ocr_book.py" "<sumber.pdf>" "<keluaran.pdf>" 300
```

Alat ini: merender tiap halaman ke 300 dpi untuk OCR, menjalankan Tesseract, lalu menanam
hasilnya sebagai **lapisan teks tak terlihat** di atas gambar halaman aslinya. **Gambar
halaman disalin apa adanya** — tidak dikompresi ulang, sehingga mutu tampilan tidak berubah.
Bookmark dan metadata sumber dipertahankan.

### Pilihan dpi

| Resolusi sumber | dpi OCR | Alasan |
|---|---|---|
| Rendah (≈120 dpi, teks digital diratakan) | **300** | Merender di atas resolusi asli membantu ketepatan Tesseract |
| Tinggi (≈600 dpi, pindaian) | **300** | Cukup; lebih tinggi hanya memperlambat tanpa menambah ketepatan |

### Bila berkas perlu dikecilkan juga

Periksa dulu **apakah ada yang bisa dihemat**. Pengalaman rak ini:

- **RCM II**: 88 halaman ternyata teks murni yang tersimpan sebagai JPEG 600 dpi.
  Dibinerkan ke CCITT G4 → 135 MB menjadi 16,6 MB, resolusi tetap 600 dpi.
- **FOA**: sudah 123 dpi dan JPEG-nya efisien. Uji kompresi ulang hanya menghemat 10%
  sambil menurunkan mutu baca → **dibatalkan**.

**Kaidah:** jangan mengompresi sebelum mengukur. Bila penghematannya di bawah ± 30%,
biarkan saja.

> **Peringatan dari pengalaman:** saat membinerkan halaman, **periksa apakah ada area abu
> seragam** (latar kepala tabel, arsiran diagram). Binarisasi polos menghapusnya jadi putih.
> Penanganannya: deteksi area abu, lalu *dither* hanya di area itu — teks tetap diambang
> tegas.

---

## Langkah 2 — Bangun daftar isi

Urut dari yang paling andal:

### 2a. Bila buku punya halaman daftar isi

Uraikan barisnya dengan koordinat kata, bukan teks polos:

```python
ws = page.get_text('words')     # (x0, y0, x1, y1, kata, blok, baris, urutan)
```

Kelompokkan per baris menurut `y`, urutkan per `x`. Untuk **daftar isi dua kolom**, pisahkan
dulu menurut `x` — cari batas kolomnya dari sebaran koordinat, jangan asal setengah lebar
halaman.

**Tiga jebakan yang sudah terbukti muncul:**

1. **Judul melipat dua baris** → baris di atasnya menelan entri di bawahnya. Pada TCP/IP dan
   Lightning Protection ini sempat menghilangkan Bab 1 seluruhnya.
   **Penangkal:** jangan gabungkan baris bila baris berikutnya sendiri membuka entri baru
   (`^Chapter \d+`, `^\d+\.\d+`, `^Appendix`).

2. **Digit nomor halaman hilang** → "31" terbaca "3". Terjadi bila nomor rata kanan dan
   digit terakhir terpotong.
   **Penangkal:** manfaatkan sifat monoton daftar isi — nomor halaman tidak pernah mundur.
   Rekonstruksi digit yang hilang, lalu **kunci tiap bab ke halaman pembukanya di badan
   buku**.

3. **Selisih halaman cetak ke PDF tidak selalu tetap.** Periksa di beberapa titik.
   Bila tidak tetap, **pakai nomor PDF saja** di seluruh rujukan.

### 2b. Bila buku tidak punya halaman daftar isi

Bangun dari **header berjalan** tiap halaman — cara ini dipakai untuk CCTV (Damjanovski).
Ambil judul yang paling sering muncul per bab sebagai judul kanonis, lalu cari halaman
pembuka tiap bab.

### 2c. Bila bookmark ada tapi judulnya rusak

| Gejala | Penanganan |
|---|---|
| Judul berupa kode berkas, halaman **benar** | Ambil judul asli dari **teks berukuran font terbesar** di halaman tujuan |
| Outline asli terkubur di bawah lapis pembungkus | Kupas lapisnya, naikkan tingkat sisanya |
| Akhiran `.pdf` / awalan `N-` | Bersihkan dengan regex |
| Outline sampah seluruhnya | Buang, bangun ulang dari 2a atau 2b |

### 2d. Verifikasi wajib sebelum menyimpan

```
✓ Urutan monoton (halaman tidak mundur)
✓ Tidak ada halaman di luar jangkauan
✓ Tiap bab dicocokkan ke isi halaman tujuannya
✓ Sampel acak sub-bab diuji
```

Simpan dengan `doc.set_toc(toc)` lalu `doc.save(path, incremental=True,
encryption=fitz.PDF_ENCRYPT_KEEP)` — penyimpanan inkremental tidak menyentuh isi halaman.

---

## Langkah 3 — Nama berkas dan folder

**Pola nama:** `Penulis - Judul (Edisi, Tahun).pdf`

- Buang embel-embel unduhan (`- libgen.li`) dan nama seri dalam kurung siku
- Kembalikan urutan nama penulis ke bentuk wajar
- Hindari karakter `/ \ : * ? " < > |` — ganti `TCP/IP` menjadi `TCP-IP`
- Ejaan nama penulis dipertahankan apa adanya, termasuk diakritik (Möllmann)

**Folder:** satu folder per topik, nama tanpa spasi ganda.

### Subfolder menurut jenis bahan (berlaku sejak batch 2, 19 Agustus 2026)

Buku diletakkan langsung di folder topiknya. **Bahan yang bukan buku dipisahkan** supaya
jelas bobot rujukannya:

| Subfolder | Isi | Boleh dikutip di dokumen resmi? |
|---|---|---|
| *(langsung di folder topik)* | Buku teks dan buku pegangan | Ya — sebutkan tahun terbit bila tua |
| `_standar/` | Standar terbitan badan resmi: IEC, IEEE, BS EN, ANSI/NETA | **Ya — ini rujukan berbobot tertinggi di rak** |
| `_tesis/` | Tesis, disertasi, makalah akademik | **Tidak langsung.** Dipakai sebagai **penunjuk** ke sumber primernya; yang dikutip regulasi/standar aslinya |
| `_panduan/` | Panduan praktis, buku putih, materi vendor | Untuk kerangka kerja, bukan untuk angka ambang |

> **Pembedaan ini yang paling menentukan.** Tesis di `R5/THESIS/` menyebut
> UU 11/2008 dan Perban BSSN 4/2021 — berguna untuk menemukan pasalnya, **tetapi yang masuk
> dokumen serah harus regulasi aslinya.** Mengutip tesis sebagai dasar hukum akan
> dipersoalkan saat diperiksa.

**Penamaan standar:** `<Badan> <Nomor>-<Tahun> - <Judul>.pdf` — mis.
`IEEE 1188-2005 - Recommended Practice for Maintenance of VRLA Batteries.pdf`.

> ⚠ **Periksa isi berkas terhadap namanya.** Pada batch 2 ditemukan satu berkas bernama
> *NETA MTS-2007* yang isinya ternyata **ATS-2017** — standar yang berbeda peruntukannya
> (uji terima vs uji pemeliharaan). Buka halaman judulnya sebelum menamai.

---

## Langkah 4 — Tulis resume

Simpan sebagai `RESUME - <judul ringkas>.md` di folder bukunya.

### Kerangka baku

```
1. Kepala      : penulis, edisi, penerbit, berkas, jumlah halaman, ukuran, tanggal susun
2. Konversi halaman : selisih cetak↔PDF; bila tidak tetap, nyatakan "pakai PDF saja"
3. Posisi buku : untuk apa buku ini dipakai, apa bedanya dari buku lain di rak
4. Peta isi    : tabel bab + nomor halaman + untuk apa dipakai
5. Perhitungan siap pakai   ← hanya bila buku memang punya isi hitungan
6. Bagian yang paling sering dipakai
7. Pemakaian di GSP  : tabel keperluan → bagian
8. Pendamping di rak : buku lain yang dipakai berpasangan
9. Catatan mutu berkas : cacat OCR, halaman hilang, peringatan usang
```

### Aturan isi

- **Digali dari teks bukunya**, bukan dari pengetahuan umum
- **Tiap klaim metodologis menyebut halaman**
- Bagian **"Yang tidak ada di buku ini"** wajib ada bila ada angka yang sering diminta
  tetapi tidak dibahas — ini yang mencegah orang mengutip angka yang tidak pernah ada
- Bila buku terbitan lama, tulis **peringatan usang** beserta bagian mana yang masih sahih

### Verifikasi rujukan

```python
# tiap "PDF <n>" harus dalam jangkauan, dan halamannya benar memuat yang dikutip
```

---

## Langkah 5 — Sambungkan ke sistem

Empat berkas yang harus ikut diperbarui — **tanpa ini, buku baru tidak akan ditemukan
siapa pun**:

| Berkas | Yang ditambahkan |
|---|---|
| **KATALOG-RUMUS.md** | Baris di indeks cepat + bagian domain (bila ada rumus); perbarui "Peta resume"; tambahkan ke "Yang TIDAK ada di rak" bila menutup celah |
| **TEMPLATE-BERITA-ACARA.md** | Jenis uji baru, bila buku memberi dasar ambang terima |
| **ASUMSI-BAKU.md** | Asumsi baru yang kini punya sandaran — dan **asumsi lama yang gugur** karena standarnya masuk |
| **PETA-CELAH-KOLEKSI.md** | Coret celah yang tertutup |
| **DAFTAR-PENGADAAN-BAHAN.md** | Tandai bahan yang sudah tertutup atau tertutup sebagian |

**Berkas rujukan skill juga ikut basi** — ini yang paling sering terlewat. Bila buku baru
menutup celah, berkas berikut akan tetap berkata "tidak ada di rak" sampai diperbaiki:

| Skill | Berkas |
|---|---|
| `pustaka-teknis` | `references/01-indeks-rumus.md`, `references/03-batas-dan-celah.md` |
| `power-backup-sizing` | `references/04-batas-dan-peringatan.md` |
| `fiber-link-design` | `references/02-uji-dan-berita-acara.md` |
| `grounding-lightning-design` | `references/03-verifikasi-dan-telusur.md` |
| `rcm-analysis` | `references/` — periksa bila bahan menyentuh keandalan |

Cara memeriksa cepat — cari penanda standar baru di seluruh berkas sistem:

```bash
grep -rlL "ATS-2017\|IEEE 1188\|62485" "C:/Users/gspen/Videos/Buku"/*.md "C:/Users/gspen/.claude/skills"/*/references/*.md
```

Berkas yang **tidak** memuat penandanya adalah calon berkas basi — periksa satu per satu.

Lalu perbarui katalog .docx:

```bash
python "C:/Users/gspen/Videos/Buku/GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/90_TOOLS/buat_katalog_docx.py"
```

Alat ini **mengukur ulang jumlah halaman, ukuran, status OCR, dan bookmark langsung dari
berkas**, jadi angkanya tidak pernah basi. Tambahkan entri buku baru pada senarai `BOOKS`
di dalamnya (folder, judul, penulis, penerbit, cakupan isi, pemakaian).

Lalu bangun ulang paket Markdown untuk model lokal:

```bash
python "C:/Users/gspen/Videos/Buku/GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/90_TOOLS/buat_paket_markdown.py"
```

> ⚠ Alat ini mengumpulkan resume lewat pola glob. Saat batch 2 masuk, resume di subfolder
> `_standar/` **terlewat** karena polanya terlalu sempit. Setelah menjalankannya, **hitung
> jumlah berkas dalam .zip** dan bandingkan dengan jumlah resume yang ada.

**Terakhir:** perbarui `RENCANA-KERJA.md` sebagai catatan riwayat.

---

## Langkah 6 — Skill, bila lini kerjanya jalan

Buat skill hanya bila buku itu menopang **lini pekerjaan yang benar-benar berjalan** —
jangan membuat skill untuk buku yang jarang dipakai.

Pola yang sudah terbukti (`rcm-analysis`, `fiber-link-design`, `power-backup-sizing`,
`grounding-lightning-design`):

```
SKILL.md
├─ frontmatter : name, description dengan pemicu ID/EN + DISAMBIGUASI
├─ Sumber      : buku, folder, aturan kutipan halaman
├─ Mode        : 4–6 mode operasi
├─ Alur wajib  : urutan yang tidak boleh dibalik
├─ Gerbang mutu: daftar periksa sebelum pekerjaan dinyatakan selesai
└─ Perangkaian : ke skill lain
references/
├─ 01-<inti>.md
├─ 02-<penerapan>.md
└─ 03-batas-dan-celah.md   ← wajib: apa yang TIDAK ada di buku
```

**Disambiguasi wajib ditulis tegas** — sebutkan skill mana yang memegang apa, supaya tidak
tumpang tindih dengan 45 skill yang sudah terpasang.

Skill baru terbaca setelah sesi Claude Code dimulai ulang.

---

## Daftar periksa akhir

```
[ ] Cadangan dibuat dan diverifikasi SHA-256 (bila berkas diubah)
[ ] Teks dapat dicari
[ ] Bookmark terpasang, urutan monoton, halaman diverifikasi
[ ] Nama berkas dan folder mengikuti pola
[ ] Resume ditulis, rujukan halaman diverifikasi
[ ] Bagian "yang tidak ada di buku ini" ditulis
[ ] Peringatan usang ditulis bila terbitan lama
[ ] KATALOG-RUMUS.md diperbarui
[ ] Katalog .docx dibangun ulang
[ ] PETA-CELAH-KOLEKSI.md diperbarui
[ ] RENCANA-KERJA.md dicatat
[ ] Skill dibuat/diperbarui bila perlu
```

---

## Perkakas

| Berkas | Fungsi |
|---|---|
| `_tools/ocr_book.py` | OCR: sisipkan lapisan teks tak terlihat, gambar tidak diubah |
| `_tools/buat_katalog_docx.py` | Bangun ulang katalog .docx, angka diukur dari berkas |

**Prasyarat:** Python dengan PyMuPDF, Pillow, numpy, python-docx · Tesseract OCR
(terpasang di `C:\Program Files\Tesseract-OCR`) · Microsoft Word (hanya untuk memeriksa
tampilan .docx).
