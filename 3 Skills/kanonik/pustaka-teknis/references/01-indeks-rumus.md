# 01 — Indeks cepat rumus (pertanyaan → rumus → buku → halaman)

> **Kanonik:** `ekas/06_ENGINEERING/CALCULATIONS/KATALOG-RUMUS.md` — berkas ini adalah
> salinan indeks cepatnya. Bila beda dengan kanonik, kanonik yang menang.

| Pertanyaan yang muncul di pekerjaan | Rumus / angka | Buku | Halaman |
|---|---|---|---|
| Lensa berapa mm supaya wajah terbaca pada jarak X? | `f = pD × d × s / ph` | Damjanovski | PDF 240 |
| Berapa kerapatan piksel yang disyaratkan? | FI 250 pix/m · FR 125 pix/m | Damjanovski | PDF 237–241 |
| Berapa lebar pita per kamera? | `Mb/s = MB/s × 8` | Damjanovski | PDF 290 |
| Berapa kapasitas rekaman? | `GB = Mb/s ÷ 8 × 3600 × jam × hari × kamera ÷ 1000` | Damjanovski | PDF 277, 290 |
| Berapa rugi total jalur serat? | rugi serat + konektor + sambungan | Hayes (FOA) | PDF 129 |
| Berapa ambang lulus uji serat? | Hasil loss budget kolom terburuk | Hayes (FOA) | PDF 145 |
| Berapa resistivitas tanah di lokasi? | `ρ = 2πaR` (Wenner) | Joffe & Lock | PDF 580 |
| Radius rolling sphere? | Level IV = 60 m; lihat Tabel 4.1 (gambar tabel — buka PDF 89–90) | Uman | PDF 89–90 |
| Isolasi peralatan masih layak? | `PI = R₁₀menit / R₁menit` | Gill | PDF 144 |
| Isolasi perlu diselidiki? | `DAR = R₆₀detik / R₃₀detik` < 1,25 | Gill | PDF 144 |
| Tegangan uji rutin maksimum? | ≤ 75% V uji terima · ≤ 60% V pabrik | Gill | PDF 145 |
| Seberapa sering perangkat proteksi diuji? | `FFI = 2 × M_perangkat × M_terproteksi ÷ M_majemuk` | Moubray | PDF 198 |
| Seberapa sering pemeriksaan on-condition? | `interval = ½ × interval P-F` | Moubray | PDF 164 |
| Apakah tugas on-condition layak? | `nett P-F > waktu yang dibutuhkan bertindak` | Moubray | PDF 166 |
| Kapasitas terpakai setelah RAID? | RAID 5 `(n−1)×C` · RAID 6 `(n−2)×C` | Troppens | PDF 46–70 |
| Berapa Ah bank baterai? | `Ah = I × t ÷ DoD` lalu koreksi C-rate | Crompton | PDF 104, 117 |
| Berapa rugi daya & beban pendinginan UPS? | `Rugi = P × (1÷η − 1)` | Emadi dkk. | PDF 20 |
| Berapa derating genset di lokasi? | Suhu, ketinggian, kelembapan (kerangka) | Mahon | PDF 40–42 |
| Mengapa transfer lambat padahal bandwidth besar? | `BDP = RTT × kapasitas penyempit` | Fall & Stevens | PDF 769 |
| Parameter kamera termal yang wajib disetel? | Delapan parameter | Vollmer & Möllmann | PDF 25 |
| **Berapa MΩ minimum tahanan isolasi?** | **Tabel 100.1 per tegangan nominal** | **ANSI/NETA ATS-2017** | **PDF 223** |
| **Koreksi hasil ukur isolasi ke 20 °C?** | **Tabel 100.14 faktor pengali** | **ANSI/NETA ATS-2017** | **PDF 241** |
| **Berapa ΔT termal yang berarti cacat?** | **Tabel 100.18 — >15 °C antar serupa, >40 °C vs udara** | **ANSI/NETA ATS-2017** | **PDF 246** |
| **Kapan baterai harus diganti?** | **< 90% rating · turun > 10% · 85% umur layan** | **IEEE 1188-2005** | **PDF 17** |
| **Berapa ventilasi ruang baterai?** | `Q = v × q × s × n × I_gas × C_rt × 10⁻³` | **IEC 62485-2** | **PDF 21** |
| **Waktu deteksi hilang sinyal video?** | **Tabel 7 per security grade: 8 / 4 / 2 detik** | **BS EN 62676-1-2** | **PDF 34** |
| **Metode uji redaman SM?** | **Empat metode reference** | **IEC 61280-4-2** | **PDF 17** |

## Yang TIDAK ada di rak (jangan dikarang)

- Ambang resistansi pembumian → PUIL/SNI [R1] atau penetapan pemilik tertulis
- Kepatuhan hukum Indonesia (PUIL, SNI, UU 11/2008, Perban BSSN 4/2021) — R1 kosong
- ONVIF (interoperabilitas perangkat) — yang ada hanya BS EN 62676-1-2 (transmisi)
- ANSI/NETA MTS (uji pemeliharaan) — yang ada hanya ATS (uji terima)
- NIST SP 800-86 / ISO/IEC 27037 (bukti digital) — hanya diringkas Alsmadi [R3]
- ISO/IEC 27001/27002
- Empat SNI struktur: 1726, 1727, 1729, 2847
- Angka produk (R4) apa pun — selalu dari pabrikan per proyek