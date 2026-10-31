# Katalog Rumus — Perpustakaan Teknis

**Lokasi rak:** `<rak-sumber>` · **Disusun:** 19 Agustus 2026
**Isi:** seluruh rumus, ambang, dan angka acuan yang sudah digali dan diverifikasi dari
22 buku di rak ini.

Berkas ini adalah **jembatan antara rak dan pekerjaan**. Fungsinya satu: saat sebuah angka
dibutuhkan, di sini terlihat **buku mana, halaman berapa, dan rumus apa** — sehingga angka
yang masuk dokumen GSP selalu punya rujukan yang bisa diperiksa panitia atau auditor.

> **Aturan pemakaian.** Rumus di bawah disalin dari bukunya, bukan dari pengetahuan umum.
> Setiap kali dipakai dalam dokumen, **sebutkan buku dan halamannya**. Bila sebuah angka
> tidak ada di katalog ini, jangan mengarang — cek dulu bagian "Yang tidak ada di rak ini"
> di bagian akhir.
>
> Angka hasil hitung yang masuk dokumen serah disertifikasi `veritas`.

---

## Cara memakai

1. Cari barisnya di **Indeks cepat** menurut pertanyaan yang sedang dihadapi
2. Buka resume buku terkait untuk konteks dan contoh terhitung
3. Bila perlu memastikan, buka halaman PDF yang disebut
4. Kutip dengan format: *"(Damjanovski, CCTV: From Light to Pixels, PDF 240)"*

---

## Indeks cepat — pertanyaan ke rumus

| Pertanyaan yang muncul di pekerjaan | Rumus / angka | Buku | Halaman |
|---|---|---|---|
| Lensa berapa mm supaya wajah terbaca pada jarak X? | `f = pD × d × s / ph` | Damjanovski | PDF 240 |
| Berapa kerapatan piksel yang disyaratkan? | FI 250 pix/m · FR 125 pix/m | Damjanovski | PDF 237–241 |
| Berapa lebar pita per kamera? | `Mb/s = MB/s × 8` | Damjanovski | PDF 290 |
| Berapa kapasitas rekaman yang dibutuhkan? | `GB = Mb/s ÷ 8 × 3600 × jam × hari × kamera ÷ 1000` | Damjanovski | PDF 277, 290 |
| Berapa rugi total jalur serat optik? | `rugi serat + rugi konektor + rugi sambungan` | Hayes (FOA) | PDF 129 |
| Berapa ambang lulus uji serat? | Hasil loss budget kolom terburuk | Hayes (FOA) | PDF 145 |
| Berapa resistivitas tanah di lokasi? | `ρ = 2πaR` | Joffe & Lock | PDF 580 |
| Radius rolling sphere untuk desain proteksi petir? | Level IV = 60 m; lihat Tabel 4.1 | Uman | PDF 89–90 |
| Isolasi peralatan masih layak? | `PI = R₁₀menit / R₁menit` | Gill | PDF 144 |
| Isolasi perlu diselidiki? | `DAR = R₆₀detik / R₃₀detik` < 1,25 | Gill | PDF 144 |
| Tegangan uji pemeliharaan rutin maksimum? | ≤ 75% V uji terima · ≤ 60% V pabrik | Gill | PDF 145 |
| Seberapa sering perangkat proteksi diuji? | `FFI = 2 × M_perangkat × M_terproteksi ÷ M_majemuk` | Moubray | PDF 198 |
| Seberapa sering pemeriksaan on-condition? | `interval = ½ × interval P-F` | Moubray | PDF 164 |
| Apakah tugas on-condition layak? | `nett P-F > waktu yang dibutuhkan bertindak` | Moubray | PDF 166 |
| Kapasitas terpakai setelah RAID? | RAID 5 `(n−1)×C` · RAID 6 `(n−2)×C` | Troppens | PDF 46–70 |
| Berapa Ah bank baterai? | `Ah = I × t ÷ DoD` lalu koreksi C-rate | Crompton | PDF 104, 117 |
| Berapa rugi daya dan beban pendinginan UPS? | `Rugi = P × (1÷η − 1)` | Emadi dkk. | PDF 20 |
| Berapa derating genset di lokasi ini? | Suhu, ketinggian, kelembapan | Mahon | PDF 40–42 |
| Mengapa transfer lambat padahal bandwidth besar? | `BDP = RTT × kapasitas penyempit` | Fall & Stevens | PDF 769 |
| Parameter apa yang wajib disetel di kamera termal? | Delapan parameter | Vollmer & Möllmann | PDF 25 |
| **Berapa MΩ minimum tahanan isolasi?** | **Tabel 100.1 per tegangan nominal** | **ANSI/NETA ATS-2017** | **PDF 223** |
| **Bagaimana mengoreksi hasil ukur ke 20 °C?** | **Tabel 100.14 faktor pengali** | **ANSI/NETA ATS-2017** | **PDF 241** |
| **Berapa ΔT termal yang berarti cacat?** | **Tabel 100.18 empat tingkat tindakan** | **ANSI/NETA ATS-2017** | **PDF 246** |
| **Kapan baterai harus diganti?** | **< 90% rating · turun > 10% · 85% umur** | **IEEE 1188-2005** | **PDF 17** |
| **Berapa ventilasi ruang baterai?** | `Q = v × q × s × n × I_gas × C_rt × 10⁻³` | **IEC 62485-2** | **PDF 21** |
| **Berapa waktu deteksi hilang sinyal video?** | **Tabel 7 per security grade: 8/4/2 detik** | **BS EN 62676-1-2** | **PDF 34** |
| **Metode uji redaman serat singlemode?** | **Empat metode reference** | **IEC 61280-4-2** | **PDF 17** |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1c (baris indeks di atas): janji 'empat tingkat tindakan' hanya ditepati di seksi 13.1; mata ④ rantai F, ambang induk, ASUMSI-BAKU, BA, dan kartu REF-ELC-002 menyalin HANYA baris 'perbaiki segera'. Pembaca yang memakai indeks sebagai daftar periksa akan menemukan tabel 'kurang' di lapis lain (register K-1c).

> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** bentuk dua nilai 8/4/2 pada baris Tabel 7 di atas berkontradiksi dengan bentuk empat nilai 8/4/4/2 di bagian 13.2 (`KATALOG-RUMUS.md:474-477`) dan `R2 - BS EN 62676-1-2.md:45-48`. Pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF primer (ukur gsp-custodian 2026-09-23). Blok penuh: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'.

---

## 1. Optik dan sistem video

**Buku:** Damjanovski, *CCTV: From Light to Pixels* (2014) · folder `R3/CCTV-VSS/`
**Resume:** `RESUME - CCTV From Light to Pixels.md`

### 1.1 Panjang fokus lensa (PDF 240)

```
f = pD × d × s / ph
```

`f` mm · `pD` pix/m · `d` m · `s` mm lebar sensor · `ph` piksel horizontal

| Format sensor | s (mm) |
|---|---|
| 1/4" | 3,2 |
| 1/3" | 4,8 |
| 1/2" | 6,4 |
| 1/2,5" mode 5 MP | 5,7 |
| 1/2,5" mode 1080 HD | 4,2 |

### 1.2 Kerapatan piksel sasaran (PDF 237–241)

| Sasaran | pD |
|---|---|
| **Identifikasi (FI)** | 250 pix/m |
| **Pengenalan (FR)** | 125 pix/m |

Dasar AS4806.2: 86–88 piksel untuk wajah ≈ 344–352 pix/m ≈ 3 mm per piksel.

> Begitu pix/m di bidang objek terpenuhi, **jumlah megapiksel kamera tidak lagi menentukan.**

### 1.3 Lebar pita dan kapasitas rekaman (PDF 277, 290)

```
Mb/s = MB/s × 8
GB   = Mb/s ÷ 8 × 3600 × jam/hari × hari × jumlah kamera ÷ 1000
```

Acuan efisiensi codec (PDF 290): mutu setara 20 Mb/s kompresi per-citra ≈ **4 Mb/s MPEG-2**
(≥ 5× lebih hemat); H.264 lebih hemat lagi.

### 1.4 Laju bingkai (PDF 115)

PAL/CCIR **25 f/d** · NTSC/EIA **30 f/d**

---

## 2. Serat optik

**Buku:** Hayes, *FOA Reference Guide* (2019) · folder `R3/FIBER-OPTIC/`
**Pendamping:** JDSU, *Fiber Optic Testing Vol 1* · folder `R3/FIBER-OPTIC/`

### 2.1 Loss budget (PDF 129 dst.)

```
Total rugi (dB) = rugi serat + rugi konektor + rugi sambungan
```

| Serat | λ | Tipikal | Maksimum EIA/TIA 568 |
|---|---|---|---|
| Multimode | 850 nm | 3 dB/km | 3,5 dB/km |
| Multimode | 1300 nm | 1 dB/km | 1,5 dB/km |
| Singlemode | 1310 nm | 0,4 dB/km | **1 dB/km premises · 0,5 dB/km OSP** |
| Singlemode | 1550 nm | 0,3 dB/km | idem |

| Konektor | Rugi |
|---|---|
| Multimode | 0,2–0,5 dB tipikal |
| SM pabrikan / pigtail fusion | 0,3 dB tipikal |
| **Batas TIA-568** | **0,75 dB** |
| SM terminasi lapangan | 0,5–1,0 dB |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5: seksi 2 ini tidak memuat baris rugi sambungan (splice) padahal rantai fiber menuliskan rentang 0,1-0,3 dB di `RANTAI-JAMINAN.md:44` (R3 + R4 bila alat menyebut lain) dan `CALC-P00-001.md:36` memakai 0,3 dB bertag ASSUMPTION. Gap konsistensi antar-lapis (butir K-5); jangan menyimpulkan 'tidak ada angka rak' dari kekosongan baris ini.

> **Aturan buku (PDF 145):** pakai kolom **terburuk** untuk memutuskan, bukan tipikal.
> Sisakan margin untuk pelaksanaan dan penurunan mutu komponen.

### 2.2 Ambang uji dan ketelitian

- Kabel referensi: rugi **> 0,5 dB patut dipertanyakan**
- Ketidakpastian: lab **0,02–0,05 dB/hari**; lapangan lebih besar
- **Jangan menetapkan toleransi lulus lebih ketat daripada ketelitian alat**

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3: baris ketidakpastian di atas tanpa atribusi buku. Angka 0,02-0,05 dB/hari hanya terbukti tercetak di resume FOA (`R3 - FOA Reference Guide to Fiber Optics.md:125-128`), sementara rantai fiber, kartu REF-FO-002, dan skill fiber-link-design menyandarkannya ke JDSU yang resume-nya nol angka dB. Jangan mengutip baris ini sebagai angka JDSU sebelum manusia membuka PDF primer.

### 2.3 Standar metode uji

| Metode | Standar |
|---|---|
| Satu ujung (patchcord) | FOTP-171 |
| Dua ujung (cable plant) — multimode | OFSTP-14 |
| Dua ujung — singlemode | OFSTP-7 |

---

## 3. Pembumian

**Buku:** Joffe & Lock, *Grounds for Grounding* (2023) · folder `R3/GROUNDING/`

### 3.1 Resistivitas tanah — Wenner (PDF 579–580)

Bentuk praktis, berlaku bila kedalaman `b` ≪ jarak `a` (Pers. 10.18):

```
ρ = 2 π a R
```

Bentuk lengkap (Pers. 10.17):

```
ρ = 4πaR ÷ [ 1 + 2a/√(a²+4b²) − a/√(a²+b²) ]
```

> Hasilnya = resistivitas rata-rata **sampai kedalaman ± a**. Ukur pada beberapa nilai `a`
> (1, 2, 4, 8, 16 m) untuk memperoleh profil tanah berlapis.

**Keterbatasan (PDF 580):** pada `a` besar, tegangan turun cepat dan mungkin tidak terukur
teliti oleh instrumen murah → pakai susunan **Schlumberger-Palmer**.

### 3.2 Resistansi elektroda terpasang (PDF 580)

Metode **fall-of-potential** (tiga pasak).

> **Prasyarat wajib:** konduktor penghubung **dilepas dari elektroda** sebelum diukur.
> Bila tidak, hasilnya tidak sah untuk berita acara.

### 3.3 Urutan kerja yang benar (PDF 562)

```
ukur resistivitas → tentukan elektroda → pasang → ukur resistansi terpasang
```

Resistansi pembumian **berbanding lurus dengan resistivitas medium.**

---

## 4. Proteksi petir

**Buku:** Uman, *The Art and Science of Lightning Protection* (2008) · folder `R3/LIGHTNING/`

### 4.1 Rolling sphere (PDF 89–90)

IEC menetapkan **empat tingkat proteksi**, masing-masing dengan radius bola gelinding.

| Tingkat | Radius | Sumber |
|---|---|---|
| Level IV | **60 m** | Tabel 4.1 |
| Level lain | lihat Tabel 4.1 | PDF 89 |

**Catatan kritis Uman (PDF 90):** dengan dua kurva alternatif lain yang juga ada dalam
literatur, radius Level IV menjadi **54 m atau 48 m**. Angka IEC adalah pilihan model,
bukan besaran fisika pasti.

### 4.2 Peringatan tentang mesh (PDF 90)

Rolling sphere memperkirakan **petir dapat menyambar di dalam mesh mana pun** yang dipasang
langsung di atap, dan **IEC tidak menyajikan teori yang membenarkan nilai ukuran mesh-nya.**

### 4.3 Ketinggian kritis (PDF 89)

Permukaan **di atas 60 m** hampir pasti tersambar pada akhirnya → struktur tinggi butuh
terminal udara pada dinding sisi, bukan hanya atap.

---

## 5. Pengujian instalasi listrik

**Buku:** Gill, *Electrical Power Equipment Maintenance and Testing* (2008) · folder `R3/ELECTRICAL/`

### 5.1 Dielectric Absorption Ratio (PDF 144)

```
DAR = R(60 detik) ÷ R(30 detik)
```

**Ambang: DAR < 1,25 → perlu penyelidikan dan kemungkinan perbaikan.**

### 5.2 Polarization Index (PDF 144)

```
PI = R(10 menit) ÷ R(1 menit)
```

**Ambang: PI < 1 → peralatan mengalami penurunan mutu.**
Bila uji PI dilakukan, **uji DA tidak perlu lagi** (PDF 659).

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8: kalimat di atas satu sisi konflik instruksi (register NWSKILL-0923 K-8): `ELECTRICAL/RANTAI-JAMINAN.md:29,:70-71` menegaskan kriteria rasio + MΩ mutlak + tren tidak saling menggantikan. Rekonsiliasi: PI menggantikan peran DA dalam keluarga rasio; MΩ mutlak dan tren tetap wajib. Jangan pakai kalimat ini untuk memangkas bukti serah.

### 5.3 Batas tegangan uji rutin (PDF 145)

```
V(rutin) ≤ 75% × V(uji terima maks)    atau    ≤ 60% × V(uji pabrik)
```

### 5.4 Empat metode pengukuran tahanan isolasi (PDF 142)

Short-time · DAR · PI · Step-voltage.
DAR dan PI **bebas pengaruh suhu dan ukuran peralatan**; short-time reading harus
**dinormalkan ke 20 °C**.

---

## 6. Keandalan dan interval pemeliharaan

**Buku:** Moubray, *RCM II* · folder `R3/RCM/` · **Skill:** `rcm-analysis`
*(Buku ini memakai selisih tetap: halaman cetak + 18 = halaman PDF)*

### 6.1 Tugas on-condition (cetak 146–148 / PDF 164–166)

```
interval pemeriksaan = ½ × interval P-F
nett P-F             = interval P-F − interval pemeriksaan
kelayakan teknis     : nett P-F > waktu yang dibutuhkan untuk bertindak
```

### 6.2 Interval failure-finding

```
FFI = 2 × ketaktersediaan × MTBF perangkat              (cetak 177 / PDF 195)

      2 × M_perangkat × M_terproteksi
FFI = ────────────────────────────────                  (cetak 180 / PDF 198)
              M_kegagalan_majemuk
```

Koreksi bila pengujian sendiri merusak: kalikan `(1 − p)`; abaikan bila p < 0,05
(cetak 181 / PDF 199).

### 6.3 Pola kegagalan (cetak 13 / PDF 31)

A 4% · B 2% · C 5% · D 7% · E 14% · **F 68%**
→ **89% moda kegagalan tidak terkait umur** → restorasi/pembuangan terjadwal hanya sah
bila ada umur aus teridentifikasi (pola A, B, C).

---

## 7. Penyimpanan

**Buku:** Troppens dkk., *Storage Networks Explained* (2009) · folder `R3/STORAGE/`

### 7.1 Kapasitas terpakai (PDF 46–70)

| Aras | Kapasitas | Cakram boleh gagal |
|---|---|---|
| RAID 0 | `n × C` | 0 |
| RAID 1 / 10 | `n/2 × C` | 1 per pasangan |
| **RAID 5** | `(n − 1) × C` | 1 |
| RAID 6 | `(n − 2) × C` | 2 |

### 7.2 Peringatan RAID 5 (PDF 67–68)

RAID 5 adalah solusi untuk **kegagalan satu cakram**, bukan kelangsungan usaha.
Rekonstruksi membaca seluruh data cakram utuh → **menaikkan peluang sektor rusak muncul
selama rekonstruksi** (MTTDL akibat BER). Tabel 2.1 (PDF 67) memuat probabilitasnya;
asumsi MTBF cakram 1.400.000 jam.

→ Untuk array besar, pertimbangkan RAID 6 atau RAID 10.

### 7.3 Beban rekonstruksi (PDF 70)

Rekonstruksi membebani bus I/O dan cakram **di atas beban normal**, dan pengendali RAID
umumnya **tidak menyediakan pengaturan prioritasnya**. Kemampuan menulis rekaman menurun
selama rekonstruksi berjalan.

---

## 8. Baterai

**Buku:** Crompton, *Battery Reference Book* (2000) · folder `R3/BATTERY/`

```
Ah dibutuhkan = arus beban (A) × waktu cadangan (jam) ÷ DoD yang diizinkan
```

lalu **koreksi terhadap C-rate**: bandingkan arus beban terhadap kapasitas nominal, ambil
kapasitas tersedia pada laju itu dari kurva pabrikan.

Contoh ketergantungan laju (PDF 169, sel tertentu — bukan universal):
C → >50% · C/2 → 80% · C/4 → 100% · C/10 → 100%

Rentang suhu operasi timbal-asam tersegel (PDF 109): **−20 sampai +50 °C**; bila operasi
terus-menerus di ujung rentang, pakai sensor suhu untuk mengoptimalkan pengisian.

> ⚠ Buku terbit 2000 — **kimia litium modern tidak tercakup.** Kerangka hitung tetap
> berlaku; angka DoD, umur siklus, dan kurva laju ambil dari lembar data pabrikan.

---

## 9. UPS

**Buku:** Emadi dkk., *UPS and Active Filters* (2004) · folder `R3/UPS/`

```
Rugi daya (W)     = daya beban (W) × (1 ÷ efisiensi − 1)
Beban pendinginan = rugi daya (seluruhnya menjadi panas)
kVA UPS          ≥ (total beban ÷ faktor daya) × margin pertumbuhan
```

Efisiensi rendah **melekat pada topologi on-line** karena konversi ganda (PDF 20) — rugi
daya muncul dua kali dalam perhitungan: konsumsi listrik dan beban pendinginan.

> ⚠ Terbit 2004 — **angka efisiensi produk masa kini ambil dari lembar data**, bukan buku ini.

---

## 10. Genset

**Buku:** Mahon, *Diesel Generator Handbook* (2004) · folder `R3/GENSET/`

```
kVA ≥ (beban puncak ÷ faktor daya) × faktor derating lokasi × margin
```

dengan pemeriksaan terpisah: **arus start beban terbesar** masih dalam kemampuan
*load acceptance* unit.

**Derating (PDF 40–42):** suhu lingkungan naik, ketinggian naik, kelembapan naik → kerapatan
udara turun → daya turun. Faktor deratingnya diminta dari pabrikan untuk kondisi lokasi
sebenarnya.

**Yang wajib tertulis di spesifikasi (PDF 35–36):** kVA + **kelas rating** + kondisi lokasi
+ load acceptance. Menyebut kVA saja membuat penawaran tidak dapat dibandingkan.

> ⚠ Berkas di rak **kehilangan Bab 11 "Emergency and standby"** — perlu salinan pengganti.

---

## 11. Jaringan

**Buku:** Fall & Stevens, *TCP/IP Illustrated Vol. 1* (2012) · folder `R3/NETWORK/`
*(Selisih tetap: halaman cetak + 39 = halaman PDF)*

```
BDP = RTT × kapasitas tautan penyempit
```

Jendela TCP sebaiknya ≈ BDP (*optimal window size*), memakai kapasitas **tautan terkecil**
sepanjang jalur — bukan kapasitas langganan (cetak 730 / PDF 769).

**Aturan praktis:** bila **BDP > 64 kB**, *Window Scale option* wajib aktif di kedua ujung
(cetak 608 / PDF 647), atau throughput terbatas berapa pun kapasitas tautannya.

---

## 12. Termografi

**Buku:** Vollmer & Möllmann, *Infrared Thermal Imaging* (2018) · folder `R3/THERMAL/`

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 (label folder `R3/THERMAL/` di atas): tingkat, bukan path - direktori `R3` tidak ada di `ekas/05_DOMAIN-KNOWLEDGE/` (terukur). Path lapis teks: `ekas/05_DOMAIN-KNOWLEDGE/THERMAL/`; laci PDF: `ekas/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/THERMAL/` (hanya `_ISI.md`; PDF primer di `<arsip-sumber>/03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/THERMAL/`). Skrip yang me-resolve label ini gagal (register K-5).

**Delapan parameter wajib disetel sebelum mengukur (PDF 25):** emisivitas objek · jarak
kamera–objek · ukuran objek · kelembapan relatif · suhu lingkungan · suhu atmosfer · suhu
optik eksternal · transmisi optik eksternal.

**Aturan IFOV (PDF 128):** objek harus menutupi **beberapa piksel**, bukan satu. Bila lebih
kecil dari IFOV pada jarak itu, nilai terbaca adalah campuran objek dan latar — bukan suhu
objek.

**Emisivitas** adalah sumber kesalahan terbesar: permukaan logam mengkilap **terbaca jauh
lebih dingin** daripada suhu sebenarnya.

**Pantulan:** ubah sudut pandang untuk menguji titik panas — bila titik ikut berpindah,
itu pantulan, bukan panas.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1b (seksi 12 Termografi di atas): seksi ini memuat parameter, IFOV, emisivitas, dan pantulan [R3] tetapi TIDAK memuat tabel ambang ΔT maupun kualifikatornya. Ambang hidup di seksi 13.1 (di bawah) dan sumber primernya `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92` - kutip selalu berpasangan dengan kualifikator 'panduan tindakan, bukan batas mutlak' yang hanya hidup di sana (register K-1b).

---

## 13. Standar — ambang terima

Lima standar masuk rak 19 Agustus 2026, disimpan di subfolder `_standar/` dalam folder
topiknya. **Buku memberi metode dan cara menghitung; standar memberi ambang dan cara
membuktikan.** Keduanya dipakai berpasangan.

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-10 (cacat penamaan path, RENDAH - terukur): klaim 'disimpan di subfolder `_standar/` dalam folder topiknya' di atas tidak cocok dengan pohon `ekas/` - pencarian direktori `_standar` di seluruh `ekas/` = 0 hasil (diukur saat studi; kolom keenam `MASTER-REFERENCE-REGISTER.csv` menulis mis. 'Electrical Maintenance/_standar' yang merujuk rak sumber asal (Mac), bukan `ekas/`). Kenyataan di disk: `03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA/` (sesuai `REF-ELC-002.md:8`). Agen yang menuruti kalimat ini akan mencari path yang tidak ada; normalisasi rujukan ke path `ekas/` nyata saat promosi objek IL (preseden fiber K-12). Register NWSKILL-0923 K-10.

### 13.1 ANSI/NETA ATS-2017 — `R2/ANSI-NETA/`

*Acceptance Testing Specifications.* Selisih halaman **tetap +19** (cetak 204 = PDF 223).

**Tahanan isolasi minimum — Tabel 100.1 (cetak 204 / PDF 223)**

| Tegangan nominal (V) | Tegangan uji DC (V) | Min. tahanan isolasi (MΩ) |
|---|---|---|
| 250 | 500 | 25 |
| 600 | 1.000 | 100 |
| 1.000 | 1.000 | 100 |
| 2.500 | 1.000 | 500 |
| 5.000 | 2.500 | 1.500 |
| 8.000 | 2.500 | 2.500 |
| 15.000 | 2.500 | 5.000 |
| 25.000 | 5.000 | 10.000 |
| 34.500 ke atas | 5.000 | 100.000 |

> Berlaku **bila tidak ada standar konsensus lain**; spesifikasi pabrikan mendahuluinya.

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-4 (delta cakupan, RENDAH - terukur): tabel di atas adalah ringkasan 9 baris. Resume sumber punya 10 baris: kelas '34.500' dan '46.000 ke atas' terdaftar terpisah (`R2 - ANSI-NETA ATS-2017.md:54-55`); di katalog keduanya digabung menjadi '34.500 ke atas'. Nilai tidak berkontradiksi (keduanya 100.000 MΩ); yang hilang adalah keberadaan baris 46 kV sebagai kelas tersendiri (grep '46.000' seluruh `ekas/` = 1 kemunculan, hanya di resume). Dampak rendah untuk praktik (46 kV jarang), tinggi untuk audit 'salin persis': pakai resume sebagai kanonik, nyatakan katalog sebagai ringkasan. Register NWSKILL-0923 K-4.

**Koreksi suhu ke 20 °C — Tabel 100.14 (cetak 222 / PDF 241)**

| Suhu | Isolasi terendam minyak | Isolasi padat |
|---|---|---|
| 0 °C | 0,25 | 0,40 |
| 10 °C | 0,50 | 0,63 |
| **20 °C** | **1,00** | **1,00** |
| 30 °C | 1,98 | 1,58 |

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5 (delta cakupan, SEDANG - terukur): tabel di atas kehilangan dua baris suhu yang ada di resume sumber: '-10 °C (0,125 / 0,25)' dan '25 °C (1,40 / 1,25)' (`R2 - ANSI-NETA ATS-2017.md:69-74` punya enam baris -10/0/10/20/25/30; katalog hanya empat). 25 °C adalah suhu ruang perangkat yang sangat sering terjadi di Indonesia; pengguna yang hanya membuka katalog tidak menemukan faktornya dan berpotensi interpolasi liar. Kanonik enam baris ada di resume; lengkapi katalog saat promosi objek IL. Register NWSKILL-0923 K-5.

**Ambang ΔT termografi — Tabel 100.18 (cetak 227 / PDF 246)**

| ΔT antar komponen serupa | ΔT terhadap udara sekitar | Tindakan |
|---|---|---|
| 1–3 °C | 1–10 °C | Kemungkinan cacat; selidiki |
| 4–15 °C | 11–20 °C | Kemungkinan besar cacat; perbaiki bila sempat |
| — | 21–40 °C | Pantau sampai dapat diperbaiki |
| **> 15 °C** | **> 40 °C** | **Perbaiki segera** |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1b + K-1d (tabel di atas): salinan empat tingkat TETAPI tanpa kualifikator sumber 'Tabel ini panduan tindakan, bukan batas mutlak' (`ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:91-92`) dan tanpa syarat pembanding 'beban serupa' yang ada di kepala kolom sumber (`:83`). Angka tanpa kualifikator dan syarat tidak boleh naik ke dokumen serah sendirian (register K-1b, K-1d).

### 13.2 BS EN 62676-1-2:2014 — `R2/EN-BS/`

*Video surveillance systems — Performance requirements for video transmission.*

**Pemantauan interkoneksi — Tabel 7 (PDF 34)**

| Persyaratan | Grade 1 | Grade 2 | Grade 3 | Grade 4 |
|---|---|---|---|---|
| Maks. durasi perangkat tidak tersedia | 180 s | 180 s | 30 s | 30 s |
| Maks. waktu deteksi hilangnya sinyal | 8 s | 4 s | 4 s | 2 s |

> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** pemetaan per-grade bentuk EMPAT nilai pada tabel ini BELUM TERKONFIRMASI terhadap geometri PDF primer (PDF 34 hanya merender 3 nilai deteksi + 2 nilai durasi; ukur gsp-custodian 2026-09-23). Bentuk dua nilai 8/4/2 hidup di indeks `KATALOG-RUMUS.md:58` dan `RANTAI-JAMINAN.md:95`. Blok penuh: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'. Syarat rekonsiliasi BSI/IEC oleh manusia sebelum angka jadi ambang uji serah terima.

> **Performance class independen dari security grade** (PDF 29) — jangan dicampur dalam
> spesifikasi.

### 13.3 IEC 61280-4-2:2014 — `R2/IEC/`

Empat metode uji redaman singlemode terpasang (PDF 17): **one-cord · three-cord · two-cord ·
OTDR**. Tiga pertama memakai LSPM.

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-11: kalimat 'Tiga pertama memakai LSPM' di atas menegaskan metode keempat (OTDR) tidak memakainya - dan di sinilah letak ketegangan R2 vs R3 yang belum teradjudikasi: FOA/rantai fiber melarang OTDR sebagai pengganti uji rugi OLTS (`RANTAI-JAMINAN.md:75,85-86`; `R3 - FOA Reference Guide to Fiber Optics.md:106-110`) sementara IEC mengakui metode OTDR sebagai metode uji redaman (PDF 17). Butir K-11; simpan kedua sisi saat mengutip seksi ini.

`Reflectance = 10 × log₁₀ (Pr / Pin)` (PDF 14). **RTM** = metode uji untuk menyelesaikan
perselisihan. ORL: Annex E Method A (PDF 43).

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-9: rumus reflektansi di atas dikutip tanpa pembatas cakupan sumber - IEC membatasi definisinya pada komponen diskret dalam kabel (`R2 - IEC 61280-4-2.md:55-58`), dan hubungan arah tanda reflectance vs ORL tidak dijelaskan di lapis mana pun. Butir K-9; BELUM TERKONFIRMASI sampai PDF IEC dibuka manusia.

Sumber ketidakpastian utama: **sambungan test cord ke alat uji** — pakai terminasi kelas
referensi (PDF 20).

### 13.4 IEEE 1188-2005 — `R2/IEEE/`

**Kriteria penurunan mutu dan penggantian (PDF 17):**

| Kondisi | Arti |
|---|---|
| Kapasitas **< 90%** rating pabrikan | Penurunan mutu → uji tahunan wajib |
| Turun **> 10%** dari uji sebelumnya | Penurunan mutu → uji tahunan wajib |
| Mencapai **85%** umur layan diharapkan | Uji tahunan wajib |

Pemeriksaan triwulanan (PDF 15): nilai ohmik internal, suhu terminal negatif, tegangan tiap
sel. Faktor koreksi suhu KT: Tabel 1 (PDF 19).

### 13.5 IEC 62485-2:2010 — `R2/IEEE/`

**Ventilasi ruang baterai (PDF 21):**

```
Q = v × q × s × n × I_gas × C_rt × 10⁻³   (m³/jam)
```

Menjaga konsentrasi hidrogen di bawah batas aman. **Derating tidak diperbolehkan** meski
emisi gas terukur lebih rendah dari asumsi standar.

Proteksi (PDF 14): jarak rambat/bebas per IEC 60664-1 dengan 4.000 V impuls; **RCD harus
yang sesuai untuk arus DC**.

---

## Yang TIDAK ada di rak ini

Penting sama pentingnya dengan yang ada — supaya tidak ada angka yang dikarang.

| Yang sering diminta | Status | Ambil dari mana |
|---|---|---|
| Ambang **MΩ mutlak** tahanan isolasi | ✅ **TERTUTUP** — ANSI/NETA ATS-2017 Tabel 100.1 | Bagian 13.1 |
| Ambang **resistansi pembumian** (mis. < 5 Ω) | **Tidak ada** — Joffe berbasis kebutuhan sistem | Standar berlaku / persyaratan pemilik |
| Ambang **ΔT lulus/tidak** pemeriksaan termal | ✅ **TERTUTUP** — ANSI/NETA ATS-2017 Tabel 100.18 | Bagian 13.1 |
| Nilai **lengkap Tabel 4.1 & 4.2** rolling sphere | Ada di berkas sebagai tabel gambar | Buka PDF 89–90 langsung |
| **Penanganan bukti digital** (chain of custody) | 🟡 **sebagian** — proses 4 tahap: Alsmadi Bab 11 (PDF 268), `R3/SECURITY/` | Standar aslinya belum |
| **Standar instalasi listrik Indonesia** | **Tidak ada di rak** | PUIL / SNI — celah prioritas tinggi |
| Dasar hukum bukti elektronik Indonesia | 🟡 **penunjuk ada** — tesis Ayubi Wirara menyebut **UU 11/2008 ITE** | `R5/THESIS/` · kutip UU-nya |
| Kriteria audit siber instansi | 🟡 **penunjuk ada** — tesis Ivan Bashofi menyebut **Perban BSSN 4/2021** | `R5/THESIS/` · kutip Perban-nya |
| Kebijakan dan mutu pencatatan log | ✅ **Joint CSI (2024)** | `R5/TECHNICAL-GUIDES/` |
| **ONVIF** (interoperabilitas perangkat) | **Masih terbuka** | Celah prioritas tinggi |
| Standar transmisi video | ✅ **TERTUTUP sebagian** — BS EN 62676-1-2 | Bagian 13.2 |
| Rumus **perencanaan kapasitas jaringan** | Tidak ada — Fall & Stevens membahas protokol | Kurose atau sumber perancangan |
| **Bab 11 Genset** (emergency & standby) | **Hilang dari berkas** | Perlu salinan pengganti |

---

## Peta resume

| Domain | Folder | Resume |
|---|---|---|
| Video pengawasan | `R3/CCTV-VSS/` | RESUME - CCTV From Light to Pixels.md |
| Analitik video | `R3/CCTV-VSS/` | RESUME - Computer Vision Algorithms and Applications.md |
| Serat optik dasar | `R3/FIBER-OPTIC/` | RESUME - FOA Reference Guide to Fiber Optics.md |
| Serat optik uji lanjut | `R3/FIBER-OPTIC/` | RESUME - Reference Guide to Fiber Optic Testing Vol 1.md |
| Pembumian | `R3/GROUNDING/` | RESUME - Grounds for Grounding.md |
| Proteksi petir | `R3/LIGHTNING/` | RESUME - The Art and Science of Lightning Protection.md |
| Uji instalasi listrik | `R3/ELECTRICAL/` | RESUME - Electrical Power Equipment Maintenance and Testing.md |
| UPS | `R3/UPS/` | RESUME - Uninterruptible Power Supplies and Active Filters.md |
| Baterai | `R3/BATTERY/` | RESUME - Battery Reference Book.md |
| Genset | `R3/GENSET/` | RESUME - Diesel Generator Handbook.md |
| Keandalan | `R3/RCM/` | RESUME - RCM II (John Moubray).md |
| Perencanaan pemeliharaan | `R3/RCM/` | RESUME - Maintenance Planning Coordination and Scheduling.md |
| Tata kelola pemeliharaan | `R3/RCM/` | RESUME - Maintenance and Reliability Best Practices.md |
| Penyimpanan | `R3/STORAGE/` | RESUME - Storage Networks Explained.md |
| Protokol jaringan | `R3/NETWORK/` | RESUME - TCP-IP Illustrated Vol 1.md |
| Dasar jaringan | `R3/NETWORK/` | RESUME - Computer Networking A Top-Down Approach.md |
| Praktik jaringan Cisco | `R3/NETWORK/` | RESUME - Network Warrior.md |
| Sertifikasi jaringan | `R3/NETWORK/` | RESUME - CCNA 200-301 Official Cert Guide Library.md |
| Keamanan sistem | `R3/SECURITY/` | RESUME - Security Engineering.md |
| Operasional TI | `R3/OPERATIONS/` | RESUME - The Practice of System and Network Administration.md |
| Termografi | `R3/THERMAL/` | RESUME - Infrared Thermal Imaging.md |
| Struktur & mekanik | `R3/MECHANICAL/` | RESUME - Shigley's Mechanical Engineering Design.md |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-4 + K-5 (baris Termografi pada tabel di atas): nama resume 'RESUME - Infrared Thermal Imaging.md' TIDAK ada di disk (ukur ulang giliran tambal: `find ekas -name 'RESUME*'` = 0); nyata: `ekas/05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md`. Label `R3/THERMAL/` pun bukan path (direktori `R3` tidak ada). Kelas sama dengan blok K-12 fiber di bawah tabel ini - di sana divonis dua baris serat; baris THERMAL ini divonis studi termal (register K-4, K-5).

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-12 (khusus dua baris 'Serat optik dasar' dan 'Serat optik uji lanjut' pada tabel di atas): nama resume di tabel di atas tidak sama dengan berkas nyata. Tertulis 'RESUME - FOA Reference Guide to Fiber Optics.md' dan 'RESUME - Reference Guide to Fiber Optic Testing Vol 1.md'; nyata di lapis 05: 'R3 - FOA Reference Guide to Fiber Optics.md' dan 'R3 - Reference Guide to Fiber Optic Testing Vol 1.md'. Label folder 'R3/FIBER-OPTIC/' pun merujuk laci vault, bukan folder domain (`ekas/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/`). Cacat penamaan terukur (preseden identik K-11 jaringan); berdampak pada jalur rute memori dan sitasi objek IL. Catatan cakupan: pola 'RESUME - ' tidak cocok dengan konvensi penamaan nyata di lapis 05 untuk domain lain juga (ukur: 0 berkas berprefiks itu di `ekas/05_DOMAIN-KNOWLEDGE/`) - butir fiber yang divonis di sini; sisanya untuk controller.
