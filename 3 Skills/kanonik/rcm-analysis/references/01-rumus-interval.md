# 01 — Rumus interval & uji kelayakan RCM

> Sumber: Moubray, *RCM II* (1997) [R3] — resume lengkap di
> `ekas/05_DOMAIN-KNOWLEDGE/RCM/R3 - RCM II (John Moubray).md`.

## 1. Interval pemeriksaan on-condition [PDF 164]

```
interval = ½ × interval P-F
```

**Syarat kelayakan tugas on-condition** [PDF 166]:

```
nett P-F > waktu yang dibutuhkan untuk bertindak
```

(nett = interval P-F dikurangi waktu yang dibutuhkan mengambil tindakan sebelum kegagalan.)

## 2. Interval failure-finding — bentuk sederhana [PDF 195]

```
FFI ≈ 2 × M_perangkat × M_terproteksi ÷ M_majemuk
```

## 3. Interval failure-finding — bentuk lengkap [PDF 198] — LEBIH BAIK dipakai

```
FFI = M_perangkat × (M_terproteksi ÷ M_majemuk) × (1 − FFI_awal) ...
```

Gunakan bentuk lengkap bila data mendukung; bentuk sederhana bila hanya estimasi.
Keduanya **metode [R3]** — bila dipakai untuk ketentuan kontraktual, sebutkan pasal
kontrak yang mengadopsinya.

## 4. Uji kelayakan tugas (dua tahap, wajib)

1. **Layak secara teknis** — apakah tugas mencegah/mendeteksi moda (kemampuan, efek, uji):
   - On-condition: ada P-F interval yang dapat diamati; alat tersedia.
   - Restorasi: batas umur/kerusakan ditemukan sebelum gagal; siklus konsisten.
   - Discard: batas umur/kerusakan ditemukan sebelum gagal; siklus konsisten.
   - FF: kondisi gagal "tersembunyi" dan dapat diuji; proteksi pengganti tersedia.
2. **Berharga** — apakah tugas mengurangi risiko ke tingkat yang bersedia ditanggung.

## 5. Catatan angka penting

| Angka | Sumber |
|---|---|
| **89% moda kegagalan tidak terkait umur** — jangan otomatis overhaul berkala | R3 — Moubray PDF 31 |
| Interval uji perangkat proteksi (mis. genset darurat) = fungsi TERSEMBUNYI → FFI | R3 — Moubray PDF 193, 195, 198 |
| MTBF gagal start genset (contoh asumsi) = 5 th → interval jadi ~9–36 hari tergantung MTBF majemuk | contoh ASUMSI-BAKU §A |
| Sasaran MTBF kegagalan majemuk = keputusan PEMILIK (bukan asumsi) | ASUMSI-BAKU §A / gate G1 |

## 6. Yang BOLEH diasumsikan (dengan tanda ASSUMPTION + sensitivitas)

MTBF perangkat proteksi (data pabrikan/pengalaman unit sejenis), MTBF fungsi terproteksi
(data historis lokasi), interval P-F (rentang Apendiks 4 Moubray / pabrikan alat).
Semua dengan: nilai, dasar, sensitivitas (½× dan 2×), rencana penggantian (log pengujian
12 bulan).