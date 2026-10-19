# Register Rujukan — seluruh sumber, terklasifikasi R1–R5

**Bagian dari:** EKAS · **Disusun:** 20 Agustus 2026 · **Jumlah sumber:** 29 resume + 2 indeks

Register ini menjawab satu pertanyaan: **"angka ini boleh dipakai untuk apa?"** — dengan
melihat tingkat sumbernya, bukan judulnya.

Definisi tingkat: `01-TINGKAT-KEYAKINAN-RUJUKAN.md`

---

## R1 — Regulasi dan standar nasional mengikat

**Tidak ada di rak. Nol.**

| Yang dibutuhkan | Untuk apa | Status |
|---|---|---|
| **PUIL / SNI kelistrikan** | Kepatuhan instalasi listrik Indonesia | ❌ belum ada |
| **UU 11/2008 (ITE) + perubahannya** | Dasar hukum bukti elektronik | ❌ belum ada — hanya disebut lewat R5 |
| **Peraturan BSSN No. 4/2021** | Kriteria audit keamanan siber instansi | ❌ belum ada — hanya disebut lewat R5 |
| **SNI proteksi petir** | Kepatuhan proteksi petir | ❌ belum ada |
| Perkap / Permen sektoral | Sesuai instansi pemberi kerja | ❌ belum ada |

> **Konsekuensi:** setiap dokumen GSP yang menyatakan "sesuai peraturan yang berlaku"
> saat ini **tidak dapat dibuktikan dari rak ini**. Kalimat itu harus disandarkan pada
> salinan regulasi yang diperoleh terpisah, atau tidak ditulis sama sekali.

---

## R2 — Standar internasional · 5 standar, 4 resume

| Standar | Tahun | Folder | Yang ditetapkan | Halaman kunci |
|---|---|---|---|---|
| **ANSI/NETA ATS-2017** | 2017 | `R2/ANSI-NETA/` | Ambang tahanan isolasi (Tabel 100.1) · koreksi suhu (100.14) · ΔT termografi (100.18) | PDF 223 · 241 · 246 |
| **IEEE 1188-2005** | 2005 | `R2/IEEE/` | Kriteria penggantian baterai VRLA · interval pemeriksaan | PDF 15 · 17 · 19 |
| **IEC 62485-2:2010** | 2010 | `R2/IEEE/` | Ventilasi ruang baterai · keselamatan instalasi | PDF 14 · 21 |
| **BS EN 62676-1-2:2014** | 2014 | `R2/EN-BS/` | Waktu deteksi hilangnya sinyal video per security grade | PDF 34 |
| **IEC 61280-4-2:2014** | 2014 | `R2/IEC/` | Empat metode uji redaman serat singlemode · RTM · ORL | PDF 14 · 17 · 43 |

**Peringatan usia:** ATS-2017 masih dalam rentang aman. **IEEE 1188-2005 sudah 21 tahun** —
prinsip dan kriterianya masih dipakai luas, tetapi periksa apakah ada revisi sebelum
dijadikan ambang mengikat dalam kontrak baru.

**Batas cakupan yang sering disalahpahami:**

| Standar | **Tidak** mencakup |
|---|---|
| ANSI/NETA **ATS** | Uji **pemeliharaan** — itu ranah **MTS**, tidak ada di rak. ATS = uji **terima** |
| **IEEE 1188** | Baterai **vented** — itu IEEE 450, tidak ada di rak. 1188 = **VRLA** saja |
| **BS EN 62676-1-2** | Interoperabilitas perangkat — itu **ONVIF**, tidak ada di rak |
| **IEC 61280-4-2** | **Multimode** — itu IEC 61280-4-1, tidak ada di rak |
| **ANSI/NETA ATS** | Kepatuhan Indonesia — standar Amerika, **bukan pengganti PUIL** |

---

## R3 — Buku teks dan handbook · 24 buku

Diurut menurut lini kerja, bukan abjad — supaya terlihat mana yang menopang pekerjaan mana.

### Rekayasa terapan — dipakai untuk hitungan

| Buku | Penulis | Tahun | Dipakai untuk | Usia |
|---|---|---|---|---|
| **CCTV: From Light to Pixels** | Damjanovski | 2014 | Lensa, kerapatan piksel, bitrate, kapasitas rekaman | ✅ |
| **FOA Reference Guide to Fiber Optics** | Hayes | 2019 | Loss budget, ambang uji, metode | ✅ |
| **Reference Guide to Fiber Optic Testing Vol 1** | JDSU | 2007 | OTDR, ketidakpastian ukur | ⚠ 19 th |
| **Grounds for Grounding** | Joffe & Lock | 2023 | Wenner, fall-of-potential, bonding | ✅ |
| **The Art and Science of Lightning Protection** | Uman | 2008 | Rolling sphere, tingkat proteksi | ⚠ 18 th — kutip IEC 62305:2006 |
| **Electrical Power Equipment Maintenance & Testing** | Gill | 2008 | PI, DAR, batas tegangan uji | ⚠ 18 th |
| **RCM II** | Moubray | 1997 | P-F, FFI, FMEA, konsekuensi | ⚠ 29 th — metodologinya tetap acuan |
| **Battery Reference Book** | Crompton | 2000 | Ah, DoD, C-rate — **kerangka saja** | ⚠ 26 th |
| **UPS and Active Filters** | Emadi dkk. | 2004 | Rugi daya, beban pendinginan | ⚠ 22 th |
| **Diesel Generator Handbook** | Mahon | 2004 | Derating, kVA, kelas rating | ⚠ 22 th · **Bab 11 hilang** |
| **Storage Networks Explained** | Troppens dkk. | 2009 | Kapasitas RAID, risiko rekonstruksi | ⚠ 17 th |
| **TCP/IP Illustrated Vol 1** | Fall & Stevens | **2012** (ed. 2) | BDP, window scaling | ⚠ 14 th |
| **Infrared Thermal Imaging** | Vollmer & Möllmann | **2018** (ed. 2) | Parameter kamera termal, IFOV | ✅ |
| **Shigley's Mechanical Engineering Design** | Budynas & Nisbett | **2021** | Perhitungan mekanik | ✅ |

### Kerangka berpikir dan proses — tidak memasok angka

| Buku | Penulis | Tahun | Dipakai untuk |
|---|---|---|---|
| **Security Engineering** | Anderson | 2020 | Kerangka keamanan sistem |
| **The NICE Cyber Security Framework** | Alsmadi | 2019 | **Proses forensik 4 tahap + rantai kustodi** (PDF 268) |
| **Protecting Critical Infrastructures** | Johnson (ed.) | 2015 | Objek vital — satu-satunya di rak |
| **The Practice of System and Network Administration** | Limoncelli dkk. | **2017** (ed. 3) | Praktik operasional TI |
| **Maintenance and Reliability Best Practices** | Gulati | **2021** (ed. 3) | Tata kelola & KPI pemeliharaan |
| **Maintenance Planning, Coordination and Scheduling** | **Nyman & Levitt** | **2010** (ed. 2) ⚠ 16 th | Perencanaan kerja pemeliharaan |
| **Computer Vision: Algorithms and Applications** | Szeliski | 2022 | Dasar analitik video |
| **Computer Networking: A Top-Down Approach** | Kurose & Ross | **2017** (ed. 7) | Dasar jaringan |
| **CCNA 200-301 Official Cert Guide** | Odom | 2024 | Praktik jaringan terkini |
| **Network Warrior** | Donahue | 2011 | Pola gangguan jaringan ⚠ 15 th |

---

## R4 — Dokumentasi teknis pabrikan

**Tidak ada di rak, dan memang seharusnya tidak.** R4 melekat pada produk yang dipilih;
rak berisi pengetahuan yang berlaku lintas produk.

**Daftar angka yang WAJIB dari R4 — tidak boleh diambil dari R3 mana pun:**

| Angka | Mengapa harus R4 | Buku yang sering disalahpakai |
|---|---|---|
| Faktor derating genset di lokasi | Berbeda tiap mesin | Mahon PDF 40–42 memberi **kerangka**, bukan angkanya |
| Efisiensi UPS | Berubah drastis sejak 2004 | Emadi memberi **prinsip** |
| DoD & umur siklus baterai | Bergantung kimia dan produk | Crompton hanya timbal-asam lama |
| Kurva laju (C-rate) baterai | Kurva pabrikan | Crompton memberi **contoh**, bukan produk Anda |
| Unjuk kerja tulis RAID | Beda antar pengendali meski aras RAID sama | Troppens memberi **konsep** |
| NETD & rentang kamera termal | Spesifikasi produk | Vollmer memberi **fisika** |
| Redaman & reflektansi konektor terpasang | Bergantung produk & mutu terminasi | Hayes memberi **batas standar TIA** |

> **Ini titik paling rawan.** Angka R3 yang terlihat spesifik (misalnya "derating 3% per
> 300 m") sangat mudah dikutip seolah-olah angka produk. Bila akibatnya mengikat,
> angka itu **harus** diganti surat pabrikan.

---

## R5 — Sumber sekunder · 3 resume + 21 makalah

| Sumber | Jenis | Menunjuk ke | Yang harus dikutip sebenarnya |
|---|---|---|---|
| Tesis Ayubi Wirara (UI) | Tesis | **UU 11/2008 (ITE)** | Pasal UU-nya — **R1** |
| Tesis Ivan Bashofi (UI) | Tesis | **Peraturan BSSN No. 4/2021** | Perban-nya — **R1** |
| Joint CSI (2024) — panduan log | Buku putih badan | Praktik pencatatan log | Boleh dirujuk sebagai praktik, **bukan ambang** |
| 21 makalah IEEE | Makalah | Berbagai | Sumber primer masing-masing |

**Empat makalah IEEE ditandai berpotensi relevan** (forensik otomotif, forensik VxWorks,
deteksi deepfake, ransomware ATT&CK) — berguna sebagai penunjuk literatur, **belum cukup
menjadi sandaran dokumen**.

---

## Ringkasan — sebaran dan artinya

```
R1  ░░░░░░░░░░░░░░░░░░░░  0      ← tidak ada dasar hukum Indonesia di rak
R2  ███░░░░░░░░░░░░░░░░░  5      ← seluruh ambang uji yang sah berasal dari sini
R3  ████████████████████  24     ← kekuatan rak: metode, rumus, penalaran
R4  ░░░░░░░░░░░░░░░░░░░░  0      ← selalu dari pabrikan, per proyek
R5  ██░░░░░░░░░░░░░░░░░░  3+21   ← penunjuk, bukan sandaran
```

**Rak ini kuat pada R3 dan cukup pada R2. Kosong pada R1 dan R4.**

Artinya: GSP dapat **merancang dan menghitung dengan baik** dari rak ini, dapat
**menetapkan ambang uji** untuk lima jenis pengujian, tetapi **tidak dapat menyatakan
kepatuhan hukum Indonesia** dan **tidak dapat menyebut angka produk** tanpa bahan dari luar.

Dua kekosongan itu ditangani berbeda:

- **R4 tidak perlu diadakan** — diminta per proyek dari pabrikan yang dipilih.
- **R1 perlu diadakan** — dan berada di urutan teratas `DAFTAR-PENGADAAN-BAHAN.md`.
