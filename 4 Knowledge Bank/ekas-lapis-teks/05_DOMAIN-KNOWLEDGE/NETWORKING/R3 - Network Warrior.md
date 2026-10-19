# Resume — Network Warrior

**Penulis:** Gary A. Donahue · **Edisi:** kedua · **Penerbit:** O'Reilly Media, 2011
**Berkas:** `Gary A. Donahue - Network Warrior (2nd Edition, 2011).pdf` — 785 halaman, 8,1 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF.** Bookmark bawaan 526 entri sampai tingkat
> sub-bagian sudah tersedia.

Buku **praktik lapangan jaringan Cisco**, ditulis dari pengalaman kerja bukan dari kurikulum.
Posisinya di rak: di antara Kurose (teori) dan CCNA (sertifikasi) — ini yang menjelaskan
**apa yang sebenarnya terjadi di perangkat** dan mengapa hal yang seharusnya bekerja ternyata
tidak.

Ciri khasnya: tiap topik disertai keluaran perintah sungguhan dan cerita kasus yang pernah
ditemui penulis.

---

## Peta isi

| Bab | Judul | PDF | | Bab | Judul | PDF |
|---|---|---|---|---|---|---|
| 1 | What Is a Network? | 27 | | 14 | Route Maps | 223 |
| 2 | Hubs and Switches | 31 | | 15 | Switching Algorithms in Cisco Routers | 233 |
| 3 | **Autonegotiation** | 45 | | 16 | Multilayer Switches | 247 |
| 4 | **VLANs** | 51 | | 17 | Cisco 6500 Multilayer Switches | 257 |
| 5 | **Trunking** | 63 | | 18 | Cisco Nexus | 291 |
| 6 | VLAN Trunking Protocol | 75 | | 19 | Catalyst 3750 Features | 343 |
| 7 | **Link Aggregation** | 89 | | 20 | Telecom Nomenclature | 367 |
| 8 | **Spanning Tree** | 107 | | 21 | T1 | 381 |
| 9 | Routing and Routers | 131 | | 22 | DS3 | 401 |
| 10 | Routing Protocols | 145 | | 23 | Frame Relay | 413 |
| 11 | Redistribution | 173 | | 24 | MPLS | 435 |
| 12 | Tunnels | 193 | | 25 | **Access Lists** | 441 |
| 13 | **First Hop Redundancy** | 207 | | 26 | **Authentication in Cisco Devices** | 463 |

Bab-bab sesudahnya membahas topik operasional lain — desain jaringan, penelusuran gangguan,
IP telephony, dan praktik kerja sehari-hari.

---

## Bagian yang paling sering dipakai

### A. Autonegotiation (Bab 3, PDF 45)

Bab pendek tetapi menyelesaikan salah satu keluhan paling sering di lapangan: tautan menyala
tetapi lambat, banyak error, atau putus-nyambung. Penyebab tersering **duplex mismatch** —
satu sisi dipaksa, sisi lain otomatis.

Relevan untuk instalasi kamera IP dan perangkat lapangan yang port switch-nya sering
dikonfigurasi manual "supaya aman", justru menimbulkan masalah.

### B. VLAN dan trunking (Bab 4–6, PDF 51–75)

Dasar pemisahan jaringan pengawasan dari jaringan kantor pelanggan — pemisahan yang hampir
selalu disyaratkan dalam dokumen teknis sistem pengawasan. Termasuk VTP dan risikonya.

### C. Spanning Tree (Bab 8, PDF 107)

Sumber gangguan yang paling sulit didiagnosis dan paling merusak bila salah: badai siaran,
topologi yang berubah sendiri, jaringan yang lumpuh setelah satu kabel ditambahkan.
Bab ini menjelaskan perilakunya dan cara mengendalikannya.

### D. Agregasi tautan (Bab 7, PDF 89)

EtherChannel/LAG untuk menaikkan kapasitas uplink — dipakai pada tautan ke NVR dan penyimpanan
yang menampung banyak aliran video sekaligus.

### E. Redundansi hop pertama (Bab 13, PDF 207)

HSRP, VRRP, GLBP. Dipakai saat merancang gateway redundan pada instalasi yang tidak boleh
terputus.

### F. Access list dan autentikasi perangkat (Bab 25–26, PDF 441 dan 463)

Pengendalian akses dan pengamanan perangkat jaringan itu sendiri — bagian yang sering diminta
pemeriksa pada instalasi instansi.

### G. Nomenklatur telekomunikasi (Bab 20–24, PDF 367–435)

T1, DS3, Frame Relay, MPLS. Sebagian sudah usang untuk instalasi baru, tetapi masih ditemui
pada jaringan warisan pelanggan — dan MPLS masih dipakai layanan operator.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menelusuri tautan lambat / banyak error | Bab 3, PDF 45 (duplex mismatch) |
| Merancang pemisahan VLAN jaringan pengawasan | Bab 4–6, PDF 51–75 |
| Menangani badai siaran / jaringan lumpuh | Bab 8, PDF 107 |
| Uplink berkapasitas besar ke NVR/penyimpanan | Bab 7, PDF 89 |
| Gateway redundan | Bab 13, PDF 207 |
| Pengamanan perangkat jaringan | Bab 25–26, PDF 441 dan 463 |
| Memahami jaringan warisan pelanggan | Bab 20–24, PDF 367–435 |

**Pendamping di rak:** `R3/NETWORK/` (Kurose) untuk dasar teori,
`R3/NETWORK/` (Fall & Stevens) untuk penelusuran tingkat paket, `R3/NETWORK/` (CCNA 2024)
untuk penyiapan sertifikasi personel.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 526 entri sangat rinci.
- Terbitan 2011 dan **berorientasi Cisco**. Perintah dan perilaku dasarnya masih berlaku,
  tetapi platform yang dibahas (6500, 3750) sudah tidak dijual — dan sebagian teknologi WAN
  (Frame Relay, T1) sudah jarang untuk instalasi baru. Pakai untuk **prinsip dan pola
  gangguan**, bukan untuk memilih perangkat.
- Isinya tidak pernah diubah, jadi tidak ada cadangan `_asli/`.
