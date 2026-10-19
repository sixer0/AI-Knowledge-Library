# Anatomi Wajib per Kelas - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §1.3 (C-09, C-10) + §2.3; dokumen sumber Klausul 5 / Tabel 5.1
> masing-masing R. Pemilik paket: `gsp-document-quality-standards` (D-TA-7.4); kanal lain pointer.

## 1. Notasi (C-09)

| Notasi | Arti |
|---|---|
| ● | **wajib** - blok wajib namun KOSONG menggugurkan penerbitan |
| ○ | opsional disarankan |
| – | tidak berlaku |

Urutan blok dokumen = urutan baris tabel dari atas ke bawah. Jangan menata ulang blok wajib.

## 2. Matriks inti - keluarga teknis/pertahanan (identik R-1 SDT-001, R-2 SDTP, R-3 AD, R-4 AU)

| # | Blok | K1 | K2 | K3 | K4 | K5 | K6 | K7 | K8 |
|---|------|----|----|----|----|----|----|----|----|
| 1 | Blok Identifikasi | ● | ● | ● | ● | ● | ● | ● | ● |
| 2 | Ruang Lingkup | ● | ● | ● | ● | ● | ● | ● | ● |
| 3 | Acuan Normatif | ● | ● | ● | ● | ● | ● | ● | ○ |
| 4 | Istilah & Singkatan | ● | ● | ○ | ● | ○ | ● | ○ | – |
| 5 | Isi Teknis | ● | ● | ● | ● | ● | ● | ● | ● |
| 6 | Matriks Ketertelusuran | ● | ● | ○ | ● | ● | ○ | ○ | – |
| 7 | Verifikasi (A/D/I/T) | ● | ○ | ○ | ● | ● | ○ | – | ○ |
| 8 | Klasifikasi & Distribusi | ● | ● | ● | ● | ● | ● | ● | ● |
| 9 | Lampiran Bukti | ○ | ○ | ○ | ● | ● | ● | ● | ● |
| 10 | Pengendalian Revisi | ● | ● | ● | ● | ● | ● | ● | ● |

Sumber: [R-1/R-2/R-3/R-4, Tabel 5.1, keempatnya verbatim sama].

## 3. Delta per rezim non-pertahanan (§2.3)

**R-5 PL** - baris 9 diganti **"Rantai Kustodi & Bukti"** (K1 ○; K2 ○; K3 ●; K4 ○; K5 ●;
K6 ○, K7 –, K8 ●). Pergeseran vs matriks inti: Istilah (K2 ○, K3 ●), Matriks Ketertelusuran
(K2 ○, K3 ●, K4 ○, K6 ●), Verifikasi (K2 ●, K3 ●, K4 ○, K6 ●).

**R-6 CY** - baris 9 = **"Rantai Kustodi & Bukti"** dengan K1 ● (wajib di kelas pentest).
Acuan Normatif opsional di K7 **dan** K8. Matriks Ketertelusuran longgar di K3/K4. Verifikasi
wajib di K2 (asesmen).

**R-7 BIZ** - baris 5 menjadi **"Isi Teknis / Komersial"**; baris 9 diganti **"Ketentuan
Komersial"** (K2 ●, K6 ●, K7 ●, K8 ●); metode verifikasi ditulis **(FAT/SAT)**; satu-satunya
rezim yang membuat **Klasifikasi & Distribusi opsional (○) di K6** (company profile publik);
Matriks Ketertelusuran wajib di K3.

## 4. Cara generator memakai

1. Ambil matriks inti, terapkan delta rezim target → susun heading dokumen persis sebaris tabel.
2. Blok ● yang isinya belum ada = **jangan diterbitkan**; tandai blocker, jangan diisi basa-basi
   (C-03: penyimpangan hanya sah sebagai pengecualian bernomor di Pengendalian Revisi).
3. Blok 1 (Blok Identifikasi) dan 10 (Pengendalian Revisi) ● di semua kelas/rezim - tidak pernah
   boleh absen, termasuk pada lembar kerja XLSX (lihat `anatomi-xlsx.md`) dan HTML
   (`peta-html.md`).
4. Module L tetap mengatur FORMAT penomoran heading & metadata; GSP-SDT mengatur **bentuk dan
   urutan blok** (D-TA-7.5). Bila bertabrakan: FORMAT → Module L; BENTUK/ANATOMI/REGISTER → GSP-SDT.
