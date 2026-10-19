# Asumsi Baku — yang wajib dinyatakan bila data tipis

**Lokasi rak:** `C:\Users\gspen\Videos\Buku` · **Disusun:** 19 Agustus 2026

Pada hampir setiap pekerjaan, sebagian data yang dibutuhkan perhitungan tidak tersedia dari
pelanggan. Berkas ini menetapkan **cara memperlakukannya** supaya pekerjaan tetap berjalan
tanpa menyembunyikan ketidakpastian.

---

## Tiga aturan

**1. Asumsi dinyatakan, tidak disembunyikan.**
Angka asumsi ditandai jelas dalam dokumen — bukan dicampur seolah data terukur. Panitia dan
auditor tidak keberatan pada asumsi; mereka keberatan pada asumsi yang tidak terlihat.

**2. Tiap asumsi disertai sensitivitasnya.**
Tunjukkan apa yang berubah bila asumsi meleset — biasanya cukup dua skenario: setengahnya
dan dua kali lipatnya. Ini membedakan asumsi yang tidak penting dari yang menentukan.

**3. Tiap asumsi punya jalan keluar.**
Sebutkan **data apa yang akan menggantikannya** dan kapan. Asumsi yang tidak pernah diganti
data akan menjadi kesalahan permanen.

Format yang dianjurkan dalam dokumen:

> **Asumsi A-3.** MTBF genset gagal start = 5 tahun.
> *Dasar:* pengalaman lapangan pada unit sejenis; data pelanggan belum tersedia.
> *Sensitivitas:* bila MTBF 2,5 tahun → interval uji menjadi 9 hari; bila 10 tahun →
> 36 hari.
> *Penggantian:* dicatat dari log pengujian selama 12 bulan pertama, ditinjau pada
> tinjauan tahunan.

---

## Daftar asumsi menurut domain

### A. Keandalan dan interval pemeliharaan

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| **MTBF perangkat proteksi** | Data pabrikan, atau pengalaman pada unit sejenis | **Linear** — interval uji berbanding lurus | Log pengujian 12 bulan |
| **MTBF fungsi terproteksi** (mis. laju padam PLN) | Data historis lokasi; bila tidak ada, data wilayah | Linear terhadap interval | Catatan pemadaman |
| **Sasaran MTBF kegagalan majemuk** | **Ditetapkan pemilik sistem, bukan diasumsikan** | Linear terbalik | Kesepakatan tertulis |
| Interval P-F | Rentang dari Apendiks 4 Moubray atau pabrikan alat | Menentukan interval pemeriksaan | Pemantauan aktual |

> Buku menegaskan (Moubray cetak 261 / PDF 279): catatan riwayat di kebanyakan industri
> **jarang cukup lengkap** untuk jadi dasar tunggal. Tipisnya data bukan alasan menunda —
> justru alasan menjalankan RCM dengan pengetahuan orang yang mengoperasikan aset.

### B. Serat optik

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| **Rugi sambungan (splice)** | Ambil dari spesifikasi pelaksana; bila belum ada, pakai batas kontrak | Kecil per sambungan, besar bila jumlahnya banyak | Hasil ukur OTDR saat pelaksanaan |
| **Redaman serat** | **Pakai batas standar**, bukan angka terbaik pabrikan | Menentukan pada jalur panjang | Hasil ukur OLTS |
| **Jumlah konektor** | Hitung dari gambar; tiap patch panel = sepasang | Linear | Gambar terpasang (as-built) |
| Anggaran daya perangkat | Lembar data transceiver | Menentukan lulus/tidak | Lembar data resmi |

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-5: baris rugi sambungan di atas sengaja tanpa angka, tetapi lapis rantai fiber punya rentang 0,1-0,3 dB (`ekas/05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/RANTAI-JAMINAN.md:44`, R3 + R4 bila alat menyebut lain) yang tidak terdaftar di sini maupun di `KATALOG-RUMUS.md` seksi 2. Gap konsistensi antar-lapis (butir K-5 studi NWSKILL-0923).

> Aturan buku (Hayes PDF 145): **jangan memakai spesifikasi terbaik.** Bila ragu, ambil
> yang lebih buruk — margin itu yang menyelamatkan saat pelaksanaan tidak sempurna.

### C. Pembumian

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| **Resistivitas tanah** | ⚠ **Jangan diasumsikan** — survei Wenner wajib | Sangat besar; menentukan seluruh desain | Survei sebelum desain |
| Struktur lapisan tanah | Dari survei beberapa jarak `a` | Menentukan kedalaman vs jumlah elektroda | Survei multi-jarak |
| Ambang resistansi | Dari standar/pemilik | Menentukan lulus/tidak | Kesepakatan tertulis |

> Ini satu-satunya domain di mana **asumsi tidak dapat diterima**. Resistansi pembumian
> berbanding lurus dengan resistivitas medium (Joffe PDF 562); mendesain tanpa mengukur
> berarti menebak seluruh hasil.

### D. Catu daya

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| **Faktor daya beban** | 0,8 bila beban campuran belum terinci | Linear terhadap kVA | Pengukuran beban aktual |
| **Arus start beban terbesar** | Data pabrikan motor/beban | **Sering menentukan ukuran**, bukan beban tunak | Lembar data beban |
| **Efisiensi UPS** | Lembar data produk — **bukan buku 2004** | Menentukan rugi dan beban pendinginan | Lembar data |
| **DoD baterai** | Timbal-asam 50%; **litium dari lembar data** | Linear terhadap Ah | Lembar data pabrikan |
| **C-rate efektif** | Dihitung dari beban dan kapasitas | Menentukan kapasitas nyata | Kurva pabrikan |
| **Faktor derating genset** | **Minta ke pabrikan** untuk kondisi lokasi | Besar di lokasi panas/tinggi | Surat pabrikan |
| Margin pertumbuhan | 20% bila belum ditetapkan | Linear | Kesepakatan pemilik |

> Tiga buku sumber domain ini terbit 2000–2004. **Angka produk masa kini wajib dari lembar
> data**; buku dipakai untuk kerangka hitung dan prinsip.

> **Dua hal di sini tidak lagi perlu diasumsikan** (sejak 19 Agustus 2026):
> **kriteria penggantian baterai** ada di **IEEE 1188-2005** (PDF 17) dan **laju ventilasi
> ruang baterai** ada di **IEC 62485-2** (PDF 21). Keduanya di `R2/IEEE/`.
> Kutip standarnya, jangan menuliskannya sebagai asumsi.

### E. Sistem video

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| **Bitrate per kamera** | Dari codec + resolusi + tingkat gerak; **nyatakan tingkat geraknya** | Linear terhadap kapasitas dan lebar pita | Pengukuran pada instalasi percobaan |
| **Sasaran pengamatan** (FI/FR) | ⚠ **Ditetapkan pemilik, bukan diasumsikan** | Menentukan seluruh pemilihan lensa | Kesepakatan tertulis |
| Jam rekaman per hari | 24 jam bila belum ditetapkan | Linear | Kesepakatan |
| Retensi (hari) | Dari ketentuan yang mengikat pelanggan | Linear | Ketentuan tertulis |
| Faktor gerak/aktivitas | Nyatakan skenario: rendah, sedang, tinggi | Besar — bisa 2–3 kali lipat | Pengukuran aktual |

> **Bitrate adalah asumsi paling berisiko** pada proyek VSS: salah menaksir berlipat
> langsung ke kapasitas penyimpanan dan lebar pita. Sajikan **dua skenario** — sedang dan
> tinggi — jangan satu angka.

### F. Penyimpanan

| Besaran | Bila tidak ada data | Sensitivitas | Penggantian |
|---|---|---|---|
| Aras RAID | Ditetapkan bersama pemilik | Kapasitas terpakai berubah besar | Kesepakatan |
| Waktu rekonstruksi | Dari pabrikan pengendali | Menentukan risiko kegagalan kedua | Uji cabut-cakram |
| Unjuk kerja tulis | **Diperiksa kasus per kasus** — bervariasi antar produk meski aras RAID sama | Menentukan jumlah kanal per mesin | Uji unjuk kerja |

---

## Asumsi yang TIDAK boleh dipakai

Empat hal yang **harus ditetapkan, bukan diasumsikan** — karena keputusannya milik pemilik
sistem, bukan perancang:

| Hal | Mengapa |
|---|---|
| **Sasaran MTBF kegagalan majemuk** | Menyatakan tingkat risiko yang bersedia ditanggung pemilik |
| **Sasaran pengamatan video (FI/FR)** | Menentukan biaya dan kemampuan sistem secara mendasar |
| **Ambang resistansi pembumian** | Berasal dari standar atau persyaratan pemilik |
| **Resistivitas tanah** | Harus diukur; tidak ada penggantinya |

Bila keempatnya belum ditetapkan, **pekerjaan perancangan belum dapat diselesaikan** —
sajikan pilihan beserta konsekuensinya, lalu minta keputusan tertulis.

---

## Asumsi yang GUGUR karena standarnya sudah ada di rak

Masuk 19 Agustus 2026. **Bila hal berikut masih ditulis sebagai asumsi, itu keliru** —
angkanya sudah punya sandaran standar dan harus dikutip, bukan ditaksir.

| Yang dulu diasumsikan | Kini dikutip dari | Halaman | Lokasi |
|---|---|---|---|
| Ambang MΩ tahanan isolasi | **ANSI/NETA ATS-2017** Tabel 100.1 | PDF 223 | `R2/ANSI-NETA/` |
| Faktor koreksi suhu hasil ukur isolasi | **ANSI/NETA ATS-2017** Tabel 100.14 | PDF 241 | idem |
| ΔT yang dianggap cacat pada termografi | **ANSI/NETA ATS-2017** Tabel 100.18 — > 15 °C antar komponen serupa, > 40 °C terhadap udara | PDF 246 | idem |
| Kapan baterai dianggap habis umur | **IEEE 1188-2005** — < 90% rating · turun > 10% · 85% umur layan | PDF 17 | `R2/IEEE/` |
| Laju ventilasi ruang baterai | **IEC 62485-2** — `Q = v × q × s × n × I_gas × C_rt × 10⁻³` | PDF 21 | idem |
| Waktu deteksi hilangnya sinyal video | **BS EN 62676-1-2** Tabel 7 — 8 / 4 / 2 detik | PDF 34 | `R2/EN-BS/` |
> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** baris asumsi Tabel 7 di atas (8 / 4 / 2 detik) berkontradiksi dengan bentuk empat nilai 8/4/4/2 di `R2 - BS EN 62676-1-2.md:45-48` dan `KATALOG-RUMUS.md:474-477`; pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF primer (ukur gsp-custodian 2026-09-23). Asumsi ini tidak boleh naik ke dokumen serah sebagai ambang terima tanpa rekonsiliasi BSI/IEC oleh manusia. Blok penuh: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'.

| Metode uji redaman serat singlemode | **IEC 61280-4-2** — empat metode | PDF 17 | `R2/IEC/` |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1a..d (baris ΔT termografi di tabel di atas): yang dikutip hanya ambang 'perbaiki segera' (> 15 / > 40). Tabel 100.18 sumbernya EMPAT tingkat dan membawa kualifikator 'panduan tindakan, bukan batas mutlak' plus syarat 'beban serupa' - utuh di `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92`. Saat mengadopsi angka ini ke dokumen, salin tabel utuh + kualifikator + syarat, bukan cuplikan dua angka (register K-1a..d). Catatan K-8: sumbernya ATS uji terima; pemakaian untuk pemeliharaan berjalan butuh MTS yang tidak ada di rak.

> **Perhatikan yang TIDAK gugur.** ATS-2017 memberi ambang **tahanan isolasi**, bukan
> **resistansi pembumian** — yang terakhir tetap masuk daftar "tidak boleh diasumsikan" di
> atas. Dua besaran berbeda; sering tertukar.

---

## Cara menyajikan dalam dokumen

Satu bagian tersendiri, tidak disebar di catatan kaki:

```
BAB X — ASUMSI PERANCANGAN

Tabel: nomor · besaran · nilai asumsi · dasar · sensitivitas · rencana penggantian

Ditutup satu paragraf:
"Seluruh angka pada bab-bab berikut disusun atas asumsi di atas. Bila salah satu
berubah, angka yang terpengaruh ditandai pada tabel sensitivitas dan akan ditinjau
ulang."
```

**Untuk workbook (`excel-master`):** asumsi ditempatkan pada **sheet terpisah**, dirujuk
sel-sel perhitungan. Rumus hidup, bukan angka diketik — sehingga perubahan asumsi langsung
terlihat dampaknya di seluruh hitungan.

---

**Berkas terkait:** `KATALOG-RUMUS.md` · `TEMPLATE-BERITA-ACARA.md` · `PETA-CELAH-KOLEKSI.md`
