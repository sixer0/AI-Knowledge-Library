# 02 — Rantai hitung lintas proyek (serah antar-buku)

> Kanonik: `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/RANTAI-JAMINAN.md` (12 rantai) — rantai lengkap
> ① Rujukan → ② Keputusan desain → ③ Perhitungan → ④ Pengujian → ⑤ Bukti serah.
> Di bawah ini lima rantai lintas-buku yang sering dipakai utuh; untuk satu domain, baca
> rantai domainnya dulu — rantai memberi urutan, resume memberi rincian.

## A. VSS (video surveillance)

1. Sasaran pengamatan FI/FR → keputusan **pemilik** (ASUMSI-BAKU §E)
2. Lensa: `f = pD × d × s / ph` [R3, Damjanovski PDF 240]; pD FI 250 / FR 125 pix/m
3. Bitrate (nyatakan skenario gerak: sedang & tinggi) → `Mb/s = MB/s × 8`
4. Kapasitas rekaman `GB = Mb/s ÷ 8 × 3600 × jam × hari × kamera ÷ 1000`
5. Waktu deteksi hilang sinyal per grade: 8/4/2 detik [R2, BS EN 62676-1-2 PDF 34]
6. BA §2–3 TEMPLATE-BERITA-ACARA

## B. Jalur serat optik

1. Konfigurasi jalur: panjang, jumlah konektor (patch panel = sepasang), sambungan, λ uji
2. Loss budget: serat (SM premises **1,0** / OSP **0,5** dB/km) + konektor (**0,75** dB batas
   TIA) + sambungan fusi (0,1–0,3) [R3, Hayes PDF 129]
3. **Ambang lulus = kolom terburuk** [R3, Hayes PDF 145]; bandingkan dengan anggaran daya
   transceiver (R4)
4. Uji: OLTS/LSPM **wajib** (OTDR pelengkap), kabel referensi ≤ 0,5 dB; metode IEC 61280-4-2
   [R2]; ORL Annex E; RTM untuk perselisihan
5. BA §1 + rincian hitungan dilampirkan

## C. Catu daya & cadangan (UPS/baterai/genset)

1. Profil beban → faktor daya 0,8 (asumsi baku) → kVA/kW
2. Kapasitas baterai `Ah = I × t ÷ DoD` + koreksi C-rate [R3, Crompton PDF 104, 117];
   DoD timbal-asam 50%, litium dari lembar data (R4)
3. Rugi UPS `P × (1÷η − 1)` → beban pendinginan [R3, Emadi PDF 20]; efisiensi dari lembar data
4. Genset: derating (suhu/ketinggian/kelembapan) — kerangka Mahon [R3 PDF 40–42], **angkanya R4**
5. Ventilasi ruang baterai `Q = v × q × s × n × I_gas × C_rt × 10⁻³` [R2, IEC 62485-2 PDF 21]
6. Interval uji fungsi tersembunyi `FFI` [R3, Moubray PDF 198]; kriteria ganti baterai
   [R2, IEEE 1188 PDF 17]
7. BA §5–6

## D. Pemeriksaan termal (termografi)

1. Parameter kamera termal (8 parameter, kalibrasi berlaku) [R3, Vollmer PDF 25]
2. NETD/IFOV: **R4 dari lembar data kamera**
3. Ambang ΔT: **> 15 °C antar komponen serupa · > 40 °C terhadap udara ambien**
   [R2, ANSI/NETA ATS-2017 Tabel 100.18 PDF 246] — bukan asumsi
4. BA §8

## E. Program pemeliharaan (RCM)

1. Konteks operasi ditetapkan **pertama** (dilarang menyalin program proyek lain)
2. Klasifikasi konsekuensi; 89% moda kegagalan tidak terkait umur [R3, Moubray PDF 31]
3. Tugas: on-condition (interval ½ P-F) → restorasi → pembuangan → failure-finding (FFI)
4. Sasaran MTBF kegagalan majemuk = **keputusan pemilik**
5. Rantai RCM utuh: `ekas/05_DOMAIN-KNOWLEDGE/RCM/RANTAI-JAMINAN.md`

## Daftar 12 rantai domain (per domain: buka file-nya)

CIVIL-STRUCTURAL · CYBERSECURITY · ELECTRICAL · FIBER-OPTIC · GROUNDING-LIGHTNING ·
NETWORKING · POWER-BACKUP · PROJECT-QUALITY · RCM · STORAGE · THERMAL · VIDEO-SURVEILLANCE
— semua di `ekas/05_DOMAIN-KNOWLEDGE/<DOMAIN>/RANTAI-JAMINAN.md`.

> ⚠ Tiga rantai PUTUS (ambang tidak ada di rak): **GROUNDING-LIGHTNING** (ambang resistansi
> pembumian), **CYBERSECURITY** (seluruh R1/R2), **CIVIL-STRUCTURAL** (4 SNI struktur).
> Metode boleh dihitung; menyatakan lulus tidak — kecuali sumber sah diperoleh (lihat
> `references/03-batas-dan-celah.md`).