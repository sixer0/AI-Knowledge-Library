# Kelas Dokumen K1–K8 - Paket GSP-SDT

> Sumber: `docs/2026-09-01-master-design-adaptasi/study/SPEC-DOC-SYSTEM.md` §1.2 (C-05..C-08)
> dan §2.2; dokumen sumber R-1..R-7 Klausul 4 / Tabel 4.1 masing-masing.
> Pemilik paket: `gsp-document-quality-standards` (D-TA-7.4). Kanal lain POINTER saja.

## 1. Aturan inti

- **C-05** - Setiap dokumen masuk satu kelas K1–K8; **bobot verifikasi** = jumlah titik uji
  wajib yang harus terpenuhi sebelum dokumen kelas itu dinyatakan terbit. Bobot menentukan
  kedalaman aparatus (Klausul 7 dan 9).
- **C-07** - Total bobot keluarga teknis/pertahanan (R-1..R-4) = **67**; keluarga non-pertahanan
  (R-5 PL, R-6 CY, R-7 BIZ) = **66**. Generator TIDAK boleh mencampur total 67 dan 66 lintas rezim.
- **C-08** - Klasifikasi empat tingkat menurut penerima: **BIASA / TERBATAS / RAHASIA / SANGAT
  RAHASIA** (notasi B/T/R/SR), tercetak pada kepala, kaki, dan sampul. Penerima menaikkan
  klasifikasi sesuai sensitivitas isi - klasifikasi awal tidak pernah diturunkan sendiri.

## 2. Tabel kelas per rezim (nama, klasifikasi awal, bobot)

| K | SDT-001 umum / SDTP / AD / AU (R-1..R-4, bobot total 67) | PL (R-5, 66) | CY (R-6, 66) | BIZ (R-7, 66) |
|---|---|---|---|---|
| K1 | Spesifikasi Sistem - RAHASIA - 12 | Spesifikasi Teknis Sistem - RAHASIA - 12 | Laporan Uji Penetrasi VAPT - RAHASIA/SR - 12 | Spesifikasi Produk & Solusi - RAHASIA - 11 |
| K2 | Dokumen Antarmuka (ICD) - RAHASIA - 9 | Kajian Teknis & Kelayakan - TERBATAS - 8 | Asesmen Risiko & Kerentanan - RAHASIA - 10 | Proposal Teknis & Penawaran - TERBATAS - 9 |
| K3 | Kajian Teknis - TERBATAS - 8 | **Forensik & Bukti Digital - RAHASIA - 11** | Arsitektur & Desain Keamanan - RAHASIA - 9 | Kajian Kebutuhan & Kelayakan - TERBATAS - 8 |
| K4 | Rencana & Prosedur Uji - RAHASIA - 11 | Kebijakan, Protap & SOP - TERBATAS - 7 | Respons Insiden - RAHASIA - 11 | Rencana & Laporan Uji Terima FAT/SAT - RAHASIA - 12 |
| K5 | Laporan Uji & Verifikasi - RAHASIA - 10 | Rencana & Laporan Uji Terima - RAHASIA - 10 | Audit & Kepatuhan - TERBATAS - 8 | Manual Integrasi & Operasi - TERBATAS - 8 |
| K6 | Manual Operasi & Pemeliharaan - TERBATAS - 7 | Audit & Kepatuhan - TERBATAS - 8 | **Advisory / Buletin Keamanan - BIASA - 5** | Company Profile & Purna Jual - **BIASA** - 7 |
| K7 | Spesifikasi Pengadaan / RAB - TERBATAS - 6 | Spesifikasi Pengadaan / RAB - TERBATAS - 6 | Berita Acara & Serah Terima - TERBATAS - 4 | Kontrak, NDA & Komersial - TERBATAS - 6 |
| K8 | Berita Acara & Serah Terima - TERBATAS - 4 | Berita Acara & Serah Terima - TERBATAS - 4 | Berita Acara & Serah Terima - TERBATAS - 4 | Berita Acara & Serah Terima - TERBATAS - 5 |

Catatan nama per matra (R-3 AD / R-4 AU): nama kelas diberi nuansa materiil - AD: "Spesifikasi
Teknis Materiil", "Buku Petunjuk Pemeliharaan"; AU: "... Materiil Udara", K3 "Kajian Teknis &
Kelaikan Awal", K4 mencakup **uji darat dan uji terbang**, K5 "Laporan Uji & Sertifikat Kelaikan".
Bobot identik dengan R-1. Sumber: [SPEC-DOC §2.2 - R-3/R-4 Tabel 4.1].

**Jebakan makna kode lintas rezim:** di PL, K2 ≠ ICD dan K3 = forensik (bukan kajian); di CY,
K7 = advisory (BIASA); di BIZ, K6 = company profile publik (BIASA). Selalu nyatakan rezim+kelas
bersama-sama, jangan pakai nama kelas lintas rezim.

## 3. Cara generator memakai tabel

1. Tentukan **rezim** target (umum/SDTP/AD/AU/PL/CY/BIZ) lalu **kelas**; baca barisnya sekali -
   nama, klasifikasi awal, dan bobot mengikat bersamaan.
2. Nyatakan `kelas` + `bobot` pada blok identitas / header-metadata (kolom `status` tetap
   `complete|blocked|needs-review|failed` per Module L.2).
3. Sebelum terbit: seluruh titik uji bobot kelas terpenuhi + checklist [`checklist-pra-terbit.md`](checklist-pra-terbit.md)
   (gerbang C-23 - satu butir wajib gagal = TAHAN terbit).
4. Angka total bobot yang dikutip ke dokumen akhir wajib menyebut rezim (67 vs 66) - sumber:
   Tabel 4.1 rezim terkait.
