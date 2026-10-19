# 01 — Proses forensik & rantai kustodi (bahan yang tersedia)

## 1. Proses forensik 4 tahap [R3 — Alsmadi, NICE Framework, Bab 11 PDF 268]

| Tahap | Aktivitas | Keluaran wajib |
|---|---|---|
| **Collection** | Identifikasi & kumpulkan bukti; gambar/salinan forensik (write-blocker) | Daftar media, hash awal, status pengawetan |
| **Examination** | Ekstraksi data dari salinan; jangan mengubah media asli | Artefak terekstrak + hash ulang |
| **Analysis** | Korelasi & rekonstruksi peristiwa; integritas catatan (Anderson) | Temuan + jejak analisis |
| **Reporting** | Laporan untuk pengadilan/pemilik; bahasa yang dapat dipertanggungjawabkan | Laporan + rantai kustodi lampiran |

## 2. Rantai kustodi (chain of custody) — isian minimal per transisi

- Objek (ID unik) · dari siapa → ke siapa · tanggal & waktu · alasan perpindahan
- **Hash SHA-256 sebelum & sesudah** setiap langkah · saksi bila disyaratkan.

## 3. Pengawetan

- Bekerja pada **salinan**, bukan media asli; media asli = bukti prima.
- Write-blocker untuk media fisik; snapshot/imajing tool terdokumentasi (R4 alat).
- Log akses semua penanganan; perubahan hanya via prosedur.

## 4. Regulasi Indonesia — PENUNJUK (R5), bukan dasar

| Sumber penunjuk | Menunjuk ke | Yang harus dikutip (belum ada di rak) |
|---|---|---|
| Tesis Ayubi Wirara (UI) | UU 11/2008 (ITE) — dasar sah bukti elektronik | pasal UU-nya [R1] |
| Tesis Ivan Bashofi (UI) | Peraturan BSSN No. 4/2021 — audit keamanan instansi | Perban-nya [R1] |

## 5. Standar yang BELUM ada di rak (menunggu pengadaan)

NIST SP 800-86 · ISO/IEC 27037 · (pelengkap 27041/27042/27043). Tanpa itu:
**keterterimaan di pengadilan dan kriteria audit BSSN tidak dapat dinyatakan**.