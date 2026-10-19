# Rantai C — Catu daya cadangan: UPS, baterai, genset

**Ambang terima berasal dari:** **IEEE 1188-2005** dan **IEC 62485-2 [R2]** ·
angka produk dari **lembar data [R4]**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| **IEEE 1188-2005** | **R2** | Kriteria penggantian baterai VRLA, interval pemeriksaan, koreksi suhu | PDF 15, 17, 19 |
| **IEC 62485-2:2010** | **R2** | Ventilasi ruang baterai, keselamatan instalasi DC | PDF 14, 21 |
| Crompton, *Battery Reference Book* (2000) | **R3** ⚠26 th | Kerangka Ah, DoD, C-rate | PDF 104, 109, 117 |
| Emadi dkk., *UPS and Active Filters* (2004) | **R3** ⚠22 th | Rugi daya, beban pendinginan | PDF 20 |
| Mahon, *Diesel Generator Handbook* (2004) | **R3** ⚠22 th · **Bab 11 hilang** | Kerangka derating, kVA | PDF 40–42, 136 |
| Moubray, *RCM II* | **R3** | Interval uji fungsi tersembunyi | PDF 193, 195, 198 |
| **Lembar data pabrikan** | **R4** | Efisiensi, DoD, umur siklus, kurva laju, derating | ❌ per proyek |

> **Tiga buku sumber domain ini melewati 20 tahun.** Kerangka hitungnya tetap sahih;
> **setiap angka produk di dalamnya sudah usang** dan wajib diganti R4.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Topologi UPS (on-line / line-interactive) | Kepekaan beban terhadap gangguan | Line-interactive ditolak untuk beban kritis — ada jeda peralihan |
| Waktu cadangan baterai | Waktu sampai genset mengambil alih + margin | "Sebanyak mungkin" ditolak — biaya dan ruang naik tanpa batas |
| Kimia baterai | Umur, suhu ruang, ruang tersedia | Litium menuntut BMS dan data [R4]; timbal-asam ditolak bila ruang panas |
| **Ventilasi ruang baterai** | **IEC 62485-2 [R2]** — dihitung, bukan ditaksir | Ruang tertutup tanpa ventilasi **ditolak** — VRLA tetap mengeluarkan gas |
| Kapasitas & kelas rating genset | Beban puncak + arus start + derating lokasi | Kelas *standby* ditolak untuk beban terus-menerus |
| Perlakuan sebagai **fungsi tersembunyi** | RCM [R3] | Jadwal "servis tiap 6 bulan" tanpa dasar **ditolak** |

> **Ini titik yang paling sering terlewat.** UPS dan genset hanya bekerja saat sumber utama
> gagal — kegagalannya sendiri **tidak terlihat siapa pun dalam keadaan normal**. Yang
> berbahaya bukan matinya genset, melainkan **kegagalan majemuk**: genset gagal diam-diam →
> PLN padam → beban kritis mati. Karena itu intervalnya **dihitung**, bukan ditebak.

---

## ③ Perhitungan

### Kapasitas baterai — [R3, Crompton PDF 104, 117]

```
Ah = (I × t) ÷ DoD          lalu koreksi terhadap C-rate efektif
```

`DoD` untuk timbal-asam biasanya 0,5 · **untuk litium wajib dari [R4]**

### Rugi daya & beban pendinginan UPS — [R3, Emadi PDF 20]

```
Rugi = P × (1 ÷ η − 1)
```

`η` **wajib dari lembar data [R4]** — angka 2004 tidak mewakili produk masa kini.

### Ventilasi ruang baterai — [R2, IEC 62485-2 PDF 21]

```
Q = v × q × s × n × I_gas × C_rt × 10⁻³      (m³/jam)
```

⚠ **Derating tidak diperbolehkan** oleh standar ini. RCD harus jenis yang sesuai arus DC
[R2, PDF 14].

### Kapasitas genset — [R3, Mahon PDF 136]

```
kVA = (beban puncak ÷ PF) × faktor_derating × margin
```

Faktor derating (suhu, ketinggian, kelembapan) — kerangkanya PDF 40–42, **angkanya dari
surat pabrikan [R4]**.

### Interval uji fungsi tersembunyi — [R3, Moubray PDF 198]

```
        2 × M_perangkat × M_terproteksi
FFI = ──────────────────────────────────
              M_kegagalan_majemuk
```

**Contoh terhitung:** genset dengan MTBF gagal start 5 tahun, pemadaman PLN 2× setahun
(`M_terproteksi` = 0,5 tahun), sasaran kegagalan majemuk sekali per 100 tahun:

```
FFI = (2 × 5 × 0,5) ÷ 100 = 0,05 tahun ≈ 18 hari
```

→ uji beban sekitar dua mingguan sampai bulanan.

---

## ④ Pengujian

| Butir | Ambang | Sumber |
|---|---|---|
| **Uji kapasitas baterai** | **< 90%** rating pabrikan → diganti · turun **> 10%** dari uji sebelumnya → diganti · **85%** umur layan → uji **tahunan** wajib | **R2** — IEEE 1188 PDF 17 |
| Pemeriksaan berkala baterai | Triwulanan | **R2** — PDF 15 |
| Koreksi suhu hasil uji | Faktor KT | **R2** — PDF 19 |
| **Laju ventilasi terpasang** | Hasil hitung mata ③ | **R2** — IEC 62485-2 |
| **Uji beban genset** | ≥ 50% kapasitas, 30 menit; catat tegangan, frekuensi, suhu air keluar, waktu start | R3 + kontrak |
| Interval uji genset | Hasil FFI mata ③ | R3 — **adopsi kontrak diperlukan** bila mengikat |
| Efisiensi UPS terukur | Terhadap lembar data | **R4** |

**Syarat pelaksanaan** [R3, Moubray PDF 193]: bila perangkat proteksi harus dilumpuhkan
untuk diperiksa, **sediakan proteksi pengganti** atau matikan fungsi yang diproteksi selama
pemeriksaan.

**Uraian tugas harus dapat dikerjakan** — bukan "servis genset", melainkan:

> *Uji beban 30 menit pada ≥ 50% kapasitas; catat tegangan, frekuensi, suhu air keluar, dan
> waktu start. Kembalikan ke keadaan siaga dan **pastikan selektor pada posisi otomatis**.*

> Butir terakhir bukan basa-basi. **Kegagalan paling konyol adalah genset yang tidak start
> karena selektornya tertinggal di posisi manual setelah uji.**

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji kapasitas baterai | ✅ | Bagian 4 · **sebutkan IEEE 1188 sebagai sumber ambang** |
| Berita acara komisioning genset | ✅ | Bagian 5 |
| **Perhitungan ventilasi + hasil ukur laju udara** | ✅ | Sering terlewat pada UPS di ruang tertutup |
| Surat pabrikan: derating, efisiensi, DoD, umur siklus | ✅ **[R4]** | Tanpa ini, angka rancangan tetap asumsi |
| Perhitungan FFI + interval yang ditetapkan | ✅ | Beserta sasaran kegagalan majemuk yang dipakai |
| **Pernyataan selektor kembali ke otomatis** | ✅ | Satu baris, mencegah kegagalan majemuk |
| Kartu kendali rantai | ✅ | Tandai tiap masukan yang masih **menunggu R4** |

**Status rantai: UTUH pada baterai dan ventilasi [R2]. MENUNGGU R4 pada genset dan UPS.**

Yang harus dijaga: kartu bertanda "menunggu R4" **dikirim ke pabrikan di awal proyek**, bukan
menjelang serah terima. Ini penghambat paling umum di akhir pekerjaan catu daya.

**Celah yang masih terbuka:** **IEEE 450** (baterai *vented*) — IEEE 1188 hanya mencakup
VRLA. Untuk instalasi baterai basah, ambang uji kapasitas **belum ada sandarannya di rak**.
