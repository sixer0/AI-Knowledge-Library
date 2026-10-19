# Rantai B — Sistem pengawasan video

**Ambang terima berasal dari:** sasaran pengamatan yang **ditetapkan pemilik** ·
transmisi dari **BS EN 62676-1-2 [R2]**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Damjanovski, *CCTV: From Light to Pixels* | **R3** | Lensa, kerapatan piksel, bitrate, kapasitas | PDF 115, 237–241, 277, 290 |
| **BS EN 62676-1-2:2014** | **R2** | Waktu deteksi hilangnya sinyal per security grade | PDF 34 |
| Szeliski, *Computer Vision* | **R3** | Dasar analitik video | — |
| Lembar data kamera & VMS | **R4** | Sensitivitas, NETD, bitrate nyata, batas kanal | per proyek |
| **ONVIF** | — | Interoperabilitas perangkat | ❌ **tidak ada di rak** |

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Sasaran pengamatan per titik** (identifikasi / pengenalan / deteksi) | ⚠ **Keputusan pemilik, bukan perancang** | Menyeragamkan seluruh titik ke identifikasi ditolak — biayanya berlipat tanpa kebutuhan |
| Panjang fokus & jenis lensa | Hitungan mata ③ | Lensa varifokal "supaya fleksibel" ditolak bila sasarannya sudah pasti — menggeser tanggung jawab ke pemasang |
| Resolusi & ukuran sensor | Kerapatan piksel yang dituntut | Menaikkan resolusi tanpa menaikkan lensa ditolak — tidak menambah kerapatan pada sasaran |
| Codec, laju bingkai, retensi | Kebutuhan + ketentuan mengikat pelanggan | 30 f/d untuk seluruh kamera ditolak — kapasitas naik tanpa manfaat pada titik statis |
| Topologi jaringan & security grade | Tingkat ancaman | — |

> **Sasaran pengamatan adalah keputusan pemilik.** Bila diasumsikan perancang, seluruh
> pemilihan lensa dan biaya sistem berdiri di atas asumsi yang tidak pernah disetujui.
> Mintalah tertulis. [lihat `ASUMSI-BAKU.md` — daftar "tidak boleh diasumsikan"]

---

## ③ Perhitungan

### Panjang fokus lensa — [R3, Damjanovski PDF 240]

```
        pD × d × s
   f = ─────────────
            ph
```

`pD` = kerapatan piksel yang dituntut (pix/m) · `d` = jarak (m) · `s` = lebar sensor (mm)
`ph` = jumlah piksel horizontal

| Ukuran sensor | `s` (mm) |
|---|---|
| 1/4" | 3,2 |
| 1/3" | 4,8 |
| 1/2" | 6,4 |
| 1/2,5" 5 MP | 5,7 |
| 1/2,5" 1080HD | 4,2 |

### Kerapatan piksel sasaran — [R3, PDF 237–241]

| Sasaran | Kerapatan |
|---|---|
| **Identifikasi (FI)** | **250 pix/m** |
| **Pengenalan (FR)** | **125 pix/m** |

### Kapasitas rekaman — [R3, PDF 277, 290]

```
Mb/s = MB/s × 8

GB = (Mb/s ÷ 8) × 3600 × jam × hari × kamera ÷ 1000
```

### Contoh terhitung

Identifikasi wajah pada 12 m, sensor 1/2,5" 1080HD (`s` = 4,2 mm), 1920 piksel horizontal:

```
f = (250 × 12 × 4,2) ÷ 1920 = 12600 ÷ 1920 = 6,56 mm
```

→ pilih lensa **6,5 mm atau lebih panjang**. Lensa 4 mm yang sering dipakai secara baku
hanya mencapai ±150 pix/m pada jarak itu — **cukup untuk pengenalan, tidak untuk
identifikasi**.

> **Bitrate adalah masukan paling berisiko.** Ia bergantung codec, resolusi, dan tingkat
> gerak. Sajikan **dua skenario — sedang dan tinggi** — jangan satu angka. Nilai
> sesungguhnya hanya dari instalasi percobaan atau lembar data [R4].

---

## ④ Pengujian

| Butir | Ketentuan | Sumber |
|---|---|---|
| **Kerapatan piksel di lapangan** | Uji dengan target ukur pada jarak rancangan; bandingkan terhadap sasaran mata ② | R3 + sasaran pemilik |
| **Waktu deteksi hilangnya sinyal video** | **Tabel 7 — 8 / 4 / 2 detik** menurut security grade | **R2** — BS EN 62676-1-2 PDF 34 |
| **Kapasitas rekaman** | Rekam pada beban nyata, ukur pemakaian ruang selama 24 jam, ekstrapolasi | Hitungan mata ③ |
| **Lebar pita** | Ukur pada switch/uplink saat seluruh kamera merekam | Hitungan mata ③ |
| **Laju bingkai & retensi** | Periksa setelan tercatat sesuai rancangan | Kesepakatan |
| **Interoperabilitas perangkat** | ⚠ **belum ada sandaran standar di rak** | ONVIF — celah terbuka |

> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** butir Tabel 7 pada baris 'Waktu deteksi hilangnya sinyal video' di atas memakai bentuk dua nilai 8/4/2, yang berkontradiksi dengan bentuk empat nilai 8/4/4/2 di `R2 - BS EN 62676-1-2.md:45-48` dan `KATALOG-RUMUS.md:474-477`. Pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF primer (ukur gsp-custodian 2026-09-23). Blok penuh + hasil ukur: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) dan `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'. Perlu rekonsiliasi BSI/IEC oleh manusia sebelum angka dipakai sebagai kriteria uji.

> Baris terakhir penting saat menjawab tender: bila spesifikasi menuntut kepatuhan ONVIF,
> **rak ini tidak dapat memasok kriteria ujinya.** Nyatakan bahwa acuannya diambil dari
> dokumen ONVIF terpisah.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji terima sistem video | ✅ | Kerangka bagian 6 |
| **Sasaran pengamatan tertulis dari pemilik** | ✅ | Tanpa ini, "lulus" tidak bermakna |
| Tabel per kamera: jarak, lensa, kerapatan tercapai | ✅ | Bandingkan rancangan vs terukur |
| Cuplikan gambar pada jarak uji | ✅ | Bukti visual kerapatan |
| Hasil uji waktu deteksi hilang sinyal | ✅ | Sebutkan security grade yang dituju |
| Pengukuran kapasitas & lebar pita 24 jam | ✅ | Termasuk tingkat gerak saat pengukuran |
| Kartu kendali rantai | ✅ | Tandai bitrate sebagai asumsi bila belum terukur |

**Status rantai: UTUH pada ambang transmisi, BERGANTUNG PEMILIK pada ambang pengamatan.**

Ini bukan kelemahan sistem — sasaran pengamatan memang bukan keputusan teknis. Yang harus
dijaga: **jangan sampai perancang mengisinya diam-diam** lalu seluruh biaya berdiri di atas
angka yang tidak pernah disetujui siapa pun.
