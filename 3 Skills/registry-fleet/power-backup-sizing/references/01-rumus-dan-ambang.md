# 01 — Rumus & ambang catu daya cadangan

## 1. Kapasitas baterai [R3 — Crompton PDF 104, 117]

```
Ah = I × t ÷ DoD        lalu koreksi C-rate (kurva pabrikan, R4)
```

- DoD timbal-asam: 50% (asumsi baku; sensitivitas linier terhadap Ah).
- DoD litium: **dari lembar data (R4)** — bukan asumsi.
- C-rate efektif: dihitung dari beban & kapasitas; kapasitas nyata ≠ nominal.

## 2. Rugi daya UPS & beban pendinginan [R3 — Emadi PDF 20]

```
Rugi (kW) = P × (1÷η − 1)
```

η dari lembar data produk (R4). Beban pendinginan ruang = rugi UPS + beban lain.

## 3. Ventilasi ruang baterai [R2 — IEC 62485-2 PDF 21]

```
Q = v × q × s × n × I_gas × C_rt × 10⁻³     (m³/jam)
```

v = volume per unit, q = laju gas, s = faktor keselamatan, n = jumlah sel,
I_gas = arus gas (float), C_rt = konstanta suhu/tipe. Detail simbol: buka PDF 21.

## 4. Derating genset [kerangka R3 — Mahon PDF 40–42; angka R4]

Suhu ambien, ketinggian, kelembapan menurunkan output. **Kerangka di buku; angka
derating di lokasi dari surat pabrikan (R4).** Bab 11 Mahon (emergency & standby)
**hilang dari rak** — topik itu tidak tersedia.

## 5. Interval uji fungsi tersembunyi [R3 — Moubray PDF 193, 195, 198]

UPS & genset darurat = fungsi tersembunyi (kegagalan tidak terlihat sampai dibutuhkan).
Interval uji: `FFI ≈ 2 × M_perangkat × M_terproteksi ÷ M_majemuk` (sederhana) atau bentuk
lengkap PDF 198. Sasaran MTBF kegagalan majemuk = **keputusan pemilik**.

## 6. Ambang dari standar (bukan asumsi)

| Butir | Ambang | Sumber |
|---|---|---|
| Ganti baterai VRLA | < 90% rating · turun > 10% · 85% umur layan → uji tahunan | IEEE 1188-2005 PDF 17 |
| Pemeriksaan berkala | Triwulanan | IEEE 1188-2005 PDF 15 |
| Koreksi suhu hasil uji | Faktor KT | IEEE 1188-2005 PDF 19 |
| Ventilasi ruang baterai | Q per rumus IEC 62485-2 | IEC 62485-2 PDF 21 |

> IEEE 1188 untuk **VRLA saja** — baterai vented = IEEE 450 (tidak ada di rak).
> IEC 62485-2 memberi keselamatan instalasi DC + ventilasi.

## 7. Asumsi baku domain (ASUMSI-BAKU §D)

Faktor daya 0,8 · arus start beban terbesar (data pabrikan motor/beban — sering menentukan
ukuran) · margin pertumbuhan 20% · MTBF genset gagal start (pengalaman/unit sejenis, ditandai
ASSUMPTION + sensitivitas).