# Template Berita Acara Uji

**Lokasi rak:** `<rak-sumber>` · **Disusun:** 19 Agustus 2026

Kerangka berita acara untuk delapan jenis pengujian yang lazim pada pekerjaan GSP. Tiap
kerangka menunjuk **buku sumber ambang terimanya**, sehingga BA yang dihasilkan bukan
sekadar formulir terisi, melainkan dokumen yang dapat dipertahankan saat diperiksa.

> ### Kaidah yang berlaku untuk semua jenis
>
> **1. Ambang lulus wajib tertulis beserta cara memperolehnya.** Tanpa itu, kata "lulus"
> tidak bermakna — tidak ada yang bisa diperiksa ulang.
>
> **2. Sumber ambang disebut.** Sebagian ambang berasal dari hitungan rancangan, sebagian
> dari standar. **Tidak satu pun boleh dikarang** — lihat kolom "Sumber ambang" tiap bagian.
>
> **3. Identitas alat lengkap:** merek, tipe, nomor seri, **tanggal kalibrasi**. Alat tanpa
> kalibrasi berlaku membuat seluruh hasil ukur dipertanyakan.
>
> **4. Ketidakpastian pengukuran dinyatakan** bila jenis ujinya punya angka itu. Jangan
> menetapkan toleransi lulus lebih ketat daripada ketelitian alat.
>
> **5. Kondisi saat pengukuran dicatat** — suhu, kelembapan, cuaca bila relevan.

---

## Rangka umum — berlaku untuk semua jenis

```
1. IDENTITAS
   ├─ Nama proyek · nomor kontrak · lokasi
   ├─ Tanggal dan waktu pengujian
   ├─ Objek yang diuji (penomoran sesuai gambar rancangan)
   ├─ Pelaksana uji (nama, jabatan, kualifikasi bila disyaratkan)
   └─ Saksi / wakil pemberi kerja

2. DASAR PENGUJIAN
   ├─ Dokumen rancangan yang dirujuk
   ├─ Standar/metode yang dipakai
   └─ Ambang lulus + CARA MEMPEROLEHNYA        ← wajib

3. ALAT UKUR
   └─ Merek · tipe · nomor seri · tanggal kalibrasi

4. KONDISI SAAT PENGUJIAN
   └─ Suhu · kelembapan · cuaca (bila relevan)

5. HASIL UKUR
   └─ Per objek, dengan satuan, dibandingkan ke ambang butir 2

6. KETIDAKPASTIAN PENGUKURAN (bila ada)

7. TEMUAN DAN TINDAK LANJUT

8. KESIMPULAN, TANDA TANGAN, LAMPIRAN
```

Delapan bagian di bawah merinci butir 2, 3, dan 5 sesuai jenis ujinya.

---

## 1. Uji jalur serat optik

**Skill:** `fiber-link-design` · **Buku:** Hayes (FOA) folder `R3/FIBER-OPTIC/`; JDSU folder `R3/FIBER-OPTIC/`

| Unsur | Isi |
|---|---|
| **Ambang lulus** | Total rugi **kolom terburuk** dari loss budget rancangan |
| **Sumber ambang** | Hitungan rancangan — bukan standar. Rinciannya wajib dilampirkan |
| **Metode** | OFSTP-7 (SM) · OFSTP-14 (MM) untuk cable plant · FOTP-171 untuk patchcord |
| **Alat** | OLTS/LSPM **wajib**; OTDR pelengkap |
| **Ketidakpastian** | Lab 0,02–0,05 dB/hari; lapangan lebih besar |

**Data jalur yang dicatat:** jenis serat (OS/OM), panjang, jumlah konektor, jumlah
sambungan, panjang gelombang uji.

**Kabel referensi:** rugi terukur dicatat; syarat **≤ 0,5 dB**.

**Bila OTDR disyaratkan**, catat penyetelannya: λ, lebar pulsa, rentang, averaging, indeks
bias, panjang launch cable dan receive cable. Tanpa itu jejak tidak dapat ditafsirkan ulang.

---

## 2. Uji pembumian

**Skill:** `grounding-lightning-design` · **Buku:** Joffe & Lock folder `R3/GROUNDING/`

| Unsur | Isi |
|---|---|
| **Ambang lulus** | Dari standar berlaku atau persyaratan pemilik sistem |
| **Sumber ambang** | ⚠ **BUKAN dari buku** — Joffe tidak menetapkan angka ambang |
| **Metode survei** | Wenner, beberapa nilai jarak `a` |
| **Metode verifikasi** | Fall-of-potential (tiga pasak) |
| **Rujukan prosedur** | Joffe Apendiks G, PDF 1111 · isi dokumen: Apendiks H, PDF 1149 |

**Data survei:** jarak `a` yang dipakai, R terukur tiap `a`, ρ hasil hitung `2πaR`, tafsiran
profil tanah.

> **Pernyataan wajib pada butir 5:** *"Konduktor penghubung telah dilepas dari elektroda
> sebelum pengukuran."* Tanpa pernyataan ini hasil ukur tidak sah — yang terukur gabungan
> seluruh sistem, bukan elektroda yang dimaksud.

---

## 3. Uji instalasi listrik (tahanan isolasi)

**Buku:** Gill folder `R3/ELECTRICAL/` · **Formulir rujukan:** Apendiks A, PDF 928

| Unsur | Isi |
|---|---|
| **Ambang rasio** | **DAR < 1,25** → perlu penyelidikan · **PI < 1** → penurunan mutu |
| **Sumber ambang rasio** | Gill, PDF 144 |
| **Ambang MΩ mutlak** | ✅ **ANSI/NETA ATS-2017 Tabel 100.1** (PDF 223) — mis. 600 V → 100 MΩ, 5 kV → 1.500 MΩ |
| **Koreksi suhu ke 20 °C** | ✅ **ANSI/NETA ATS-2017 Tabel 100.14** (PDF 241) |
| **Metode** | Short-time · DAR · PI · Step-voltage (PDF 142) |
| **Batas tegangan uji rutin** | ≤ 75% V uji terima maks · ≤ 60% V uji pabrik (PDF 145) |

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: baris 'Ambang MΩ mutlak' pada tabel di atas (✅ Tabel 100.1, PDF 223) tanpa caveat sumber: nilai berlaku 'bila tidak ada standar konsensus lain' dan spesifikasi pabrikan mendahului (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`). Berita acara yang menyalin baris ini wajib membawa caveat-nya; register NWSKILL-0923 K-2.

**Yang dicatat:** pembacaan pada 30 s, 60 s, 1 menit, 10 menit sesuai metode yang dipakai;
suhu saat pengukuran.

> **Untuk short-time reading:** nilai **wajib dinormalkan ke 20 °C** dan pengaruh kelembapan
> diperhitungkan sebelum dibandingkan dengan hasil sebelumnya. DAR dan PI tidak perlu —
> keduanya bebas pengaruh suhu.

**Bila uji PI dilakukan, uji DA tidak perlu lagi** (PDF 659).

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8: kalimat di atas adalah satu sisi konflik instruksi di rak (register NWSKILL-0923 K-8). `ELECTRICAL/RANTAI-JAMINAN.md:29,:70-71` menetapkan kriteria rasio (PI, DAR) + MΩ mutlak + tren dan 'ketiganya tidak saling menggantikan'. Rekonsiliasi sah: PI menggantikan peran DA di dalam keluarga rasio; MΩ mutlak [R2] dan tren tetap wajib. Jangan pakai kalimat ini untuk menghapus kriteria lain dari bukti serah.

---

## 4. Uji kapasitas baterai

**Skill:** `power-backup-sizing` · **Buku:** Crompton folder `R3/BATTERY/`, Part 3 PDF 320

| Unsur | Isi |
|---|---|
| **Ambang lulus** | ✅ **IEEE 1188-2005** (PDF 17): kapasitas **< 90% rating pabrikan**, atau **turun > 10%** dari uji sebelumnya → penurunan mutu |
| **Pemicu uji tahunan** | Menunjukkan penurunan mutu, **atau** mencapai **85% umur layan** yang diharapkan |
| **Koreksi suhu** | Faktor KT, IEEE 1188 Tabel 1 (PDF 19) |
| **Metode** | Uji pengosongan terkendali pada laju yang ditetapkan |
| **Keselamatan instalasi** | IEC 62485-2 — ventilasi `Q = v × q × s × n × I_gas × C_rt × 10⁻³` (PDF 21) |

**Yang wajib dicatat:** **laju pengosongan (C-rate) saat uji**, tegangan akhir, suhu
lingkungan, Ah yang keluar, dan persentasenya terhadap nominal.

> Tanpa mencatat C-rate, hasil uji tidak dapat dibandingkan — kapasitas yang keluar
> bergantung pada laju pengosongan. Uji pada C/10 dan C/2 memberi hasil berbeda pada
> baterai yang sama.

---

## 5. Komisioning genset

**Skill:** `power-backup-sizing` · **Buku:** Mahon folder `R3/GENSET/`, Bab 13 PDF 397

| Unsur | Isi |
|---|---|
| **Ambang lulus** | Parameter unjuk kerja pada spesifikasi kontrak |
| **Sumber ambang** | Spesifikasi + lembar data pabrikan |
| **Parameter wajib diuji** | Load acceptance · regulasi tegangan & frekuensi (transien dan mantap) · batasan harmonisa (PDF 35) |

**Yang dicatat:** waktu start sampai siap beban, tegangan dan frekuensi pada tiap tahap
beban, suhu air keluar, konsumsi bahan bakar bila disyaratkan, tingkat kebisingan bila
disyaratkan.

**Kondisi lokasi dicatat** — suhu dan ketinggian — karena keduanya memengaruhi daya yang
dapat dihasilkan.

> **Butir penutup wajib:** *"Selektor dikembalikan ke posisi otomatis dan unit dipastikan
> dalam keadaan siaga."* Genset yang tidak start karena selektor tertinggal di manual
> setelah uji adalah kegagalan yang seluruhnya dapat dicegah.

---

## 6. Uji terima sistem video

**Skill:** `cctv-system-designer` (perancangan) · **Buku:** Damjanovski folder `R3/CCTV-VSS/`, Bab 14 PDF 512

| Unsur | Isi |
|---|---|
| **Ambang lulus** | Kerapatan piksel di bidang objek sesuai sasaran: **FI 250 pix/m** atau **FR 125 pix/m** |
| **Sumber ambang** | Damjanovski PDF 237–241 + sasaran pengamatan pada dokumen rancangan |
| **Metode objektif** | Test chart (Bab 14) — bukan penilaian "gambar terlihat jelas" |

**Yang dicatat per kamera:** identitas dan lokasi, lensa terpasang, jarak ke bidang objek
acuan, kerapatan piksel terukur/terhitung, hasil uji test chart, bitrate aktual, laju
bingkai.

**Untuk sisi perekaman:** kapasitas terpasang, aras RAID, kapasitas terpakai setelah RAID,
retensi hari yang tercapai, dan **verifikasi laju transfer** — bukan hanya kapasitas.

> **Ambang berbasis megapiksel saja tidak sah.** Yang menentukan kerapatan piksel di bidang
> objek pada jarak nyata, bukan resolusi sensor.

---

## 7. Pemeriksaan termal

**Buku:** Vollmer & Möllmann folder `R3/THERMAL/`

| Unsur | Isi |
|---|---|
| **Ambang lulus (ΔT)** | ✅ **ANSI/NETA ATS-2017 Tabel 100.18** (PDF 246): ΔT > 15 °C antar komponen serupa, atau > 40 °C terhadap udara sekitar → **perbaiki segera** |
| **Parameter wajib disetel** | Delapan parameter (PDF 25) — **dicatat di BA** |
| **Aturan validitas** | Objek menutupi beberapa piksel (IFOV, PDF 128) |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1a..d (baris ambang pada tabel di atas): BA ini menyalin hanya baris 'perbaiki segera'. Klasifikasi temuan wajib memakai Tabel 100.18 EMPAT tingkat beserta kualifikator 'panduan tindakan, bukan batas mutlak' dan syarat 'beban serupa' - sumber primer `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92` (tabel utuh juga `KATALOG-RUMUS.md` seksi 13.1). ΔT udara 21-40 °C = 'Pantau'; ΔT serupa 1-3 °C = 'Perlu diselidiki' - keduanya bukan 'aman' dan bukan 'tanpa aturan' (register K-1a..d).
> K-7 (baris aturan validitas IFOV pada tabel yang sama): aturan di atas kualitatif [R3]. Nilai IFOV/NETD NYATA alat yang dipakai wajib R4 (lembar data per model); 'TERTUTUP' di `R4-STATUS.md` berarti laci terisi, bukan angka siap dikutip - 0 nilai NETD/IFOV di lapis teks (register K-7). Catat model dan firmware kamera di BA, jangan mengarang angkanya.

**Delapan parameter yang dicatat:** emisivitas objek · jarak · ukuran objek · kelembapan
relatif · suhu lingkungan · suhu atmosfer · suhu optik eksternal · transmisi optik eksternal.

**Uji pantulan dicatat:** pengamatan dari sudut berbeda untuk memastikan titik panas bukan
pantulan.

> Tanpa mencatat emisivitas yang dipakai, angka suhu pada BA tidak dapat diverifikasi ulang.
> Permukaan logam mengkilap terbaca jauh lebih dingin daripada suhu sebenarnya.

---

## 8. Uji penyimpanan / RAID

**Buku:** Troppens dkk. folder `R3/STORAGE/` · **Daftar periksa:** Apendiks B, PDF 556

| Unsur | Isi |
|---|---|
| **Ambang lulus** | Kapasitas terpakai dan retensi sesuai rancangan |
| **Sumber ambang** | Hitungan rancangan (bitrate × kamera × retensi) |
| **Yang diverifikasi** | Kapasitas terpakai setelah RAID · ketahanan kegagalan · unjuk kerja tulis |

**Yang dicatat:** jumlah dan kapasitas cakram, aras RAID, kapasitas terpakai terukur,
hasil uji cabut-cakram (bila disyaratkan), waktu rekonstruksi, dan **unjuk kerja tulis
selama rekonstruksi berjalan**.

> Butir terakhir sering dilewat padahal menentukan: selama rekonstruksi, kemampuan menulis
> rekaman menurun, dan pengendali RAID umumnya tidak menyediakan pengaturan prioritas
> (Troppens PDF 70).

---

## Ringkasan sumber ambang

Tabel ini yang mencegah ambang dikarang.

| Jenis uji | Ambang berasal dari | Ada di rak? |
|---|---|---|
| Serat optik | **Hitungan rancangan** (loss budget terburuk) | ✅ rumusnya ada |
| Pembumian | Standar berlaku / persyaratan pemilik | ❌ **tidak ada di rak** |
| Tahanan isolasi — rasio | Gill PDF 144 (DAR 1,25 · PI 1) | ✅ |
| Tahanan isolasi — MΩ mutlak | **ANSI/NETA ATS-2017 Tabel 100.1** | ✅ **ada di rak** |
| Kapasitas baterai | **IEEE 1188-2005** + kontrak | ✅ **ada di rak** |
| Genset | Spesifikasi + lembar data | ❌ |
| Sistem video — kerapatan piksel | Damjanovski PDF 237–241 + sasaran rancangan | ✅ |
| Sistem video — transmisi | **BS EN 62676-1-2 Tabel 7** | ✅ **ada di rak** |
| Termal (ΔT) | **ANSI/NETA ATS-2017 Tabel 100.18** | ✅ **ada di rak** |
| Penyimpanan | Hitungan rancangan | ✅ |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8 (baris Termal pada tabel di atas): 'ada di rak' benar untuk ambang ΔT, tetapi sandarannya ANSI/NETA **ATS** (uji terima). Untuk pemeriksaan instalasi berjalan - kegunaan BA termal paling umum - doktrin rak sendiri menggolongkannya wilayah **MTS** yang tidak ada di rak (`AMBANG-TERIMA-INDUK.md` peringatan + baris 'Uji pemeliharaan listrik'), dan rantai F THERMAL tidak membawa peringatan itu (grep MTS folder THERMAL = 0 sebelum anotasi). Putusan pemakaian = controller-manusia (register K-8).

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: baris 'Tahanan isolasi - MΩ mutlak' pada tabel di atas ditandai ✅ ada di rak TANPA menyebut caveat 'bila tidak ada standar konsensus lain' (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`). Saat baris ini dijadikan dasar lulus/tidak lulus, bawa caveat-nya. Register NWSKILL-0923 K-2.

**Empat baris bertanda ❌ adalah tempat angka paling sering dikarang.** Bila ambangnya
diminta dan sumbernya belum ada, **nyatakan begitu** dan minta ditetapkan — jangan diisi
dari pengetahuan umum.

---

**Berkas terkait:** `KATALOG-RUMUS.md` (rumus dan halaman) · `ASUMSI-BAKU.md` (asumsi yang
wajib dinyatakan bila data tipis) · `PETA-CELAH-KOLEKSI.md` (celah rak)
