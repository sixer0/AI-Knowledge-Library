> # ⚠ CONTOH — BUKAN PEKERJAAN NYATA
>
> Kode proyek **`P00` dicadangkan untuk contoh**. Proyek sungguhan memakai `P25`, `P26`,
> dan seterusnya. **Seluruh angka di berkas ini karangan** untuk menguji perangkat gate —
> jangan disalin ke dokumen pelanggan.

# ITP-P00 — Inspection & Test Plan

**Gate G4** · Disetujui sebelum uji dimulai · 21 Agustus 2026

| # | Butir | Metode | Sumber metode | Ambang | Sumber ambang | Penyaksi |
|---|---|---|---|---|---|---|
| 1 | Kontinuitas & polaritas tiap core | VFL | R3 REF-FO-001 PDF 98 | Semua core menyala, polaritas benar | Praktik | Pengawas |
| 2 | **Rugi kabel referensi** | FOTP-171 | R3 REF-FO-001 | **≤ 0,5 dB** | R3 REF-FO-001 | Pelaksana |
| 3 | **Rugi sisipan per core @1310** | Dua ujung, one-cord | **R2 REF-FO-003 PDF 17** | **≤ 6,40 dB** | CALC-P00-001 | Pengawas |
| 4 | **Rugi sisipan per core @1550** | idem | **R2** | **≤ 5,96 dB** | CALC-P00-001 | Pengawas |
| 5 | Jejak OTDR + daftar peristiwa | OTDR | R3 REF-FO-002 | 6 sambungan terlihat, tak ada peristiwa tak dikenal | Rancangan | Pengawas |
| 6 | Rugi tiap sambungan (dari OTDR) | OTDR | R3 | Dicatat — **menggantikan asumsi 0,3 dB** | — | Pelaksana |
| 7 | Rekaman berjalan 24 jam | Pengamatan VMS | — | Tanpa bingkai hilang | REQ-P00-007 | Pengawas |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: ambang 5,96 dB @1550 yang dikutip di lapis ini TIDAK reproducible dari masukan CALC-P00-001.md:31-36. Alpha tersirat 5,96 tepat = 0,3625 dB/km (tidak muncul di FOA/rantai/katalog/kartu); kandidat rak memberi 5,60 dB (a=0,25), 5,76 dB (a=0,3), 6,40 dB (a=0,5); brute force 1.120 kombinasi menuntut n_sambungan 8/10 (bertentangan n=6 di DDR-P00-001.md:19) atau rugi konektor 0,5/1,0 (bukan 0,75). Rincian uji: register Bagian 2.3 dan K-2. Induk anotasi: CALC-P00-001.md:48. Nilai P00 berlabel 'angka karangan' (contoh); tidak ada dokumen serah nyata yang tercemar. Keputusan koreksi (5,76 / 6,40 / catatan ilustrasi-tanpa-rincian) milik controller-manusia.

## Prasyarat sebelum uji

- ☐ Kalibrasi OLTS dan OTDR **berlaku pada tanggal uji**
- ☐ Kabel referensi sudah diuji (butir 2) — **hasilnya menentukan keabsahan butir 3–4**
- ☐ CALC-P00-001 **sudah diperiksa orang kedua** ⚠ *belum*

> ⚠ **Prasyarat ketiga belum terpenuhi.** ITP ini belum boleh dijalankan untuk butir 3 dan 4,
> karena ambangnya berasal dari hitungan yang belum diverifikasi.
