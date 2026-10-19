# Rantai H — Penyimpanan dan jaringan

**Ambang terima berasal dari:** hitungan rancangan · **tidak ada standar normatif di rak**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Troppens dkk., *Storage Networks Explained* (2009) | **R3** ⚠17 th | Kapasitas RAID, risiko rekonstruksi | PDF 46–70 |
| Fall & Stevens, *TCP/IP Illustrated Vol 1* (2012) | **R3** ⚠14 th | BDP, window scaling | PDF 647, 769 |
| Kurose & Ross (2017) · Odom, *CCNA* (2024) | **R3** | Dasar dan praktik jaringan terkini | — |
| Donahue, *Network Warrior* (2011) | **R3** ⚠15 th | Pola gangguan | — |
| **TIA-568 / TIA-942** | **R2** | Perkabelan terstruktur & pusat data | ❌ **TIDAK ADA** |
| Lembar data pengendali RAID & cakram | **R4** | Unjuk kerja tulis, waktu rekonstruksi | per proyek |

> **Buku penyimpanan di rak terbit 2009** — sebelum SSD/NVMe umum, sebelum penyimpanan
> objek dan awan. **Konsep RAID/SAN/NAS-nya tetap sahih**; angka unjuk kerja dan waktu
> rekonstruksinya tidak mewakili perangkat masa kini.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Aras RAID | Toleransi kegagalan vs kapasitas terpakai | **RAID 5 pada cakram besar ditolak** — risiko kegagalan kedua selama rekonstruksi [R3 PDF 67–68] |
| Jumlah & ukuran cakram | Kapasitas hasil mata ③ + waktu rekonstruksi | Cakram terbesar "supaya hemat slot" ditolak — memperpanjang rekonstruksi |
| Cadangan panas (hot spare) | Waktu tanggap penggantian | Tanpa hot spare ditolak bila lokasi jauh dari teknisi |
| Kapasitas & topologi jaringan | Beban puncak + lonjakan | Merancang pada beban rata-rata ditolak — perekaman video berkorelasi, puncaknya bersamaan |
| Ukuran window TCP untuk transfer jarak jauh | BDP mata ③ | Menambah lebar pita tanpa memeriksa BDP **ditolak** — tidak menambah laju |

---

## ③ Perhitungan

### Kapasitas setelah RAID — [R3, Troppens PDF 46–70]

```
RAID 5 : kapasitas_terpakai = (n − 1) × C
RAID 6 : kapasitas_terpakai = (n − 2) × C
```

`n` = jumlah cakram · `C` = kapasitas per cakram

### Bandwidth-Delay Product — [R3, Fall & Stevens PDF 769]

```
BDP = RTT × kapasitas_penyempit
```

**Bila BDP > 64 kB, window scaling wajib** [PDF 647]. Tanpa itu, transfer jarak jauh akan
lambat **walaupun lebar pitanya besar** — gejala yang sering salah didiagnosis sebagai
"jaringan kurang cepat" dan dijawab dengan menambah lebar pita yang tidak menolong.

### Contoh terhitung

Perekaman video 40 kamera, kebutuhan 96 TB mentah, RAID 6 dengan cakram 16 TB:

```
n − 2 = 96 ÷ 16 = 6      →  n = 8 cakram
```

Periksa juga **beban rekonstruksi** [R3 PDF 70]: selama satu cakram dibangun ulang, seluruh
cakram lain dibaca penuh — unjuk kerja turun dan risiko kegagalan kedua meningkat. Waktu
rekonstruksi nyata **hanya dari [R4]**.

---

## ④ Pengujian

| Butir | Ambang | Sumber |
|---|---|---|
| Kapasitas terpakai setelah RAID | Hasil hitung mata ③ | R3 |
| **Uji cabut-cakram** (rekonstruksi nyata) | Selesai dalam waktu yang ditetapkan; sistem tetap melayani | Kontrak + **R4** |
| Unjuk kerja tulis pada beban penuh | Seluruh kanal merekam tanpa bingkai hilang | Hitungan + **R4** |
| Lebar pita pada uplink saat puncak | Di bawah kapasitas rancangan | Hitungan mata ③ |
| Transfer jarak jauh mencapai laju rancangan | Sesuai BDP | R3 |
| Perkabelan terstruktur | ⚠ **tidak ada sandaran standar di rak** | TIA-568 — celah terbuka |

> **Uji cabut-cakram adalah uji yang paling sering dilewati** dan paling sering
> menyelamatkan. Ia satu-satunya cara membuktikan bahwa redundansi yang dibayar benar-benar
> bekerja — dan bahwa unjuk kerja selama rekonstruksi masih memadai untuk perekaman berjalan.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji penyimpanan / RAID | ✅ | Kerangka bagian 8 |
| Perhitungan kapasitas + aras RAID yang dipilih beserta alasannya | ✅ | Termasuk alternatif yang ditolak |
| **Hasil uji cabut-cakram**: waktu rekonstruksi, unjuk kerja selama proses | ✅ | Bukti redundansi bekerja |
| Pengukuran unjuk kerja tulis pada beban penuh | ✅ | Seluruh kanal aktif |
| Pengukuran lebar pita saat puncak | ✅ | Bukan rata-rata |
| Lembar data pengendali & cakram | ✅ **[R4]** | Sumber sah angka unjuk kerja |
| Kartu kendali rantai | ✅ | Tandai unjuk kerja tulis sebagai **menunggu R4** bila belum diuji |

**Status rantai: UTUH pada perhitungan, TANPA SANDARAN NORMATIF pada ambang.**

Seluruh ambang di rantai ini berasal dari **hitungan rancangan dan kontrak**, bukan dari
standar. Itu sah — tetapi berarti ambangnya **hanya sekuat kesepakatan tertulisnya**.
Pastikan angka unjuk kerja dan waktu rekonstruksi yang dijanjikan **masuk kontrak**, bukan
hanya proposal.

**Celah yang masih terbuka:** **TIA-568** (perkabelan terstruktur) dan **TIA-942** (pusat
data) — keduanya di prioritas menengah `DAFTAR-PENGADAAN-BAHAN.md`.
