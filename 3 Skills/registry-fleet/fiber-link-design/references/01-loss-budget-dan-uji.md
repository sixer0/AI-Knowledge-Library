# 01 — Loss budget & metode uji serat optik

## 1. Rumus loss budget [R3 — Hayes PDF 129]

```
Total rugi (dB) = rugi serat + rugi konektor + rugi sambungan
                = (α_serat × L) + (n_konektor × 0,75) + (n_sambungan × 0,1–0,3)
```

| Komponen | Nilai SM | Sumber |
|---|---|---|
| Rugi serat premises | 1,0 dB/km | Hayes PDF 129 |
| Rugi serat outside plant | 0,5 dB/km | Hayes PDF 129 |
| Rugi konektor | 0,75 dB (batas TIA-568) | Hayes PDF 129 |
| Rugi sambungan fusi | 0,1–0,3 dB | Hayes PDF 129 / R4 alat |

> Hitung per panjang gelombang (1310 nm dan 1550 nm) — rugi serat berbeda menurut λ.

**Ambang lulus = total kolom terburuk** [R3 — Hayes PDF 145]. Tidak ada nilai rata-rata.

**Anggaran daya transceiver (R4)**: daya kirim − sensitivitas terima = margin yang tersedia.
Loss budget harus ≤ margin, sisakan margin pelaksanaan.

## 2. Metode uji [R2 — IEC 61280-4-2 PDF 17]

Empat metode reference (single-mode):
1. **One-cord** — referensi tunggal
2. **Three-cord** — tiga kabel referensi (metode penuh)
3. **Two-cord** — dua kabel
4. **OTDR** — metode berbasis OTDR (dengan launch & receive cable)

**Wajib menyebutkan metode yang dipakai** — hasil antar-metode berbeda sistematis.
Penyelesaian perselisihan: **RTM** (Reference Test Method) [R2 — PDF 14].
ORL bila disyaratkan: Annex E Method A, gelombang kontinu [R2 — PDF 43].
Terminasi kelas referensi: [R2 — PDF 20].

## 3. Alat & kabel referensi

| Butir | Syarat | Sumber |
|---|---|---|
| Alat untuk rugi | **OLTS/LSPM wajib** — OTDR bukan pengganti | R3 — Hayes PDF 98 |
| Kabel referensi | Diuji FOTP-171; **rugi > 0,5 dB patut dipertanyakan** | R3 |
| OTDR (pelengkap) | Catat λ, lebar pulsa, rentang, averaging, indeks bias, launch/receive cable | R3 — JDSU PDF 44 |
| Ketidakpastian | Lab 0,02–0,05 dB/hari; lapangan lebih besar | R3 — JDSU |

## 4. Data jalur yang wajib dicatat di berita acara

Jenis serat (OS/OM) · panjang · jumlah konektor · jumlah sambungan · panjang gelombang uji ·
metode (empat pilihan) · alat + tanggal kalibrasi · hasil per λ dibanding ambang.

## 5. Uji coba P00 (contoh nyata terbukti)

Jalur 3,2 km / 8 core: ambang 6,40 dB (1310 nm) dan 5,96 dB (1550 nm). Temuan uji coba:
**rugi konektor menyumbang 3,00 dB dari 6,40 dB** — hampir separuh anggaran hanya dari
4 konektor. Periksa jumlah konektor sebelum menyalahkan sambungan. (Contoh: `CALC-P00-001.md`,
angka karangan — jangan dipakai proyek sungguhan.)