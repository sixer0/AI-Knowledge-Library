# Resume — TCP/IP Illustrated, Volume 1: The Protocols

**Penulis:** Kevin R. Fall, W. Richard Stevens · **Edisi:** kedua · **Penerbit:** Addison-Wesley / Pearson, 2012
**Berkas:** `Kevin R. Fall, W. Richard Stevens - TCP-IP Illustrated Vol 1 The Protocols (2nd Edition, 2012).pdf` — 1.059 halaman, 11,4 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Konversi halaman.** Berbeda dengan CCTV dan FOA, selisih di buku ini **tetap**:
> **halaman cetak + 39 = halaman PDF**. Contoh: TIME_WAIT ada di halaman cetak 618 = PDF 657.
> Ditulis `cetak 618 / PDF 657`. Bookmark 207 entri (18 bab + 187 sub-bab) sudah dipasang.

Buku rujukan tingkat paket. Dipakai bukan untuk belajar konsep dari nol — untuk itu ada
Kurose & Ross di `R3/NETWORK/` — melainkan **saat ada gangguan yang tidak
terjelaskan di lapisan atas** dan harus dibuktikan dari tangkapan paket. Ciri khasnya:
tiap mekanisme ditunjukkan dengan jejak paket sungguhan, bukan diagram teori.

Edisi kedua ini ditulis ulang Kevin Fall dari karya asli W. Richard Stevens, dan sudah
mencakup **IPv6 sejajar dengan IPv4** di sepanjang buku — bukan sebagai bab tambahan.

---

## Peta isi

| Bab | Judul | Cetak | PDF |
|---|---|---|---|
| 1 | Introduction | 1 | 40 |
| 2 | The Internet Address Architecture | 31 | 70 |
| 3 | Link Layer | 79 | 118 |
| 4 | ARP: Address Resolution Protocol | 165 | 204 |
| 5 | The Internet Protocol (IP) | 181 | 220 |
| 6 | System Configuration: DHCP and Autoconfiguration | 233 | 272 |
| 7 | Firewalls and Network Address Translation (NAT) | 299 | 338 |
| 8 | ICMPv4 and ICMPv6 | 353 | 392 |
| 9 | Broadcasting and Local Multicasting (IGMP, MLD) | 435 | 474 |
| 10 | UDP and IP Fragmentation | 473 | 512 |
| 11 | Name Resolution and DNS | 511 | 550 |
| 12 | TCP: The Transmission Control Protocol (Preliminaries) | 579 | 618 |
| 13 | TCP Connection Management | 595 | 634 |
| 14 | TCP Timeout and Retransmission | 647 | 686 |
| 15 | TCP Data Flow and Window Management | 691 | 730 |
| 16 | TCP Congestion Control | 727 | 766 |
| 17 | TCP Keepalive | 793 | 832 |
| 18 | Security: EAP, IPsec, TLS, DNSSEC, DKIM | 805 | 844 |
| — | Glossary of Acronyms | 933 | 972 |
| — | Index | 963 | 1002 |

Tiap bab ditutup bagian **Attacks Involving …** — ringkasan serangan yang mengeksploitasi
protokol yang baru dibahas. Bagian ini berguna langsung saat menyusun bagian keamanan pada
kajian teknis.

---

## Bagian yang paling sering dipakai

### A. TIME_WAIT dan 2MSL (cetak 618 / PDF 657)

Penyebab keluhan lapangan yang paling sering salah didiagnosis: "port habis", "server tidak
bisa menerima koneksi baru padahal beban rendah".

> **TIME_WAIT** disebut juga **2MSL wait state** — TCP menunggu selama **dua kali Maximum
> Segment Lifetime (MSL)**. Setiap implementasi memilih sendiri nilai MSL-nya.

Yang menutup koneksi lebih dulu (*active close*) yang masuk TIME_WAIT — dan **kedua sisi bisa
melakukan active close**, tidak selalu klien. Ini penting saat menelusuri mengapa justru
server yang menumpuk soket TIME_WAIT.

Diagram transisi status TCP lengkap ada di bagian 13.5 (cetak 616–625 / PDF 655–664),
termasuk FIN_WAIT_2, simultaneous open/close, dan konsep quiet time.

### B. Kendali kemacetan (Bab 16, cetak 727 / PDF 766)

Dua algoritma inti — **slow start** dan **congestion avoidance** — berlandaskan asas
*packet conservation* dan *ACK clocking*, dirumuskan Jacobson (cetak 731 / PDF 770).

Bab ini menelusuri evolusinya sampai algoritma modern: NewReno, SACK, FACK, rate halving,
limited transmit, congestion window validation, sampai varian seperti CUBIC dan Compound TCP.

**Kegunaan praktis:** menjelaskan mengapa throughput satu aliran TCP pada tautan jarak jauh
tidak pernah mencapai kapasitas nominal — dan mengapa menambah bandwidth sering tidak
menyelesaikan masalah bila latensi dan kehilangan paketnya yang jadi pembatas.

### C. Fragmentasi IP dan Path MTU (Bab 10, cetak 473 / PDF 512; PMTU cetak 148 / PDF 187)

Sumber gangguan klasik pada tautan berterowongan (VPN, GRE) dan jaringan dengan MTU tidak
seragam: koneksi terbentuk, paket kecil lewat, tetapi transfer besar menggantung.

Bab 10 membahas fragmentasi UDP/IPv4, batas ukuran datagram, timeout perakitan ulang, dan
**interaksi fragmentasi dengan ARP/ND** — kombinasi yang sering luput saat menelusuri
gangguan. Path MTU Discovery untuk TCP dibahas di bagian 13.4 (cetak 612 / PDF 651).

### D. Firewall dan NAT (Bab 7, cetak 299 / PDF 338)

Perilaku NAT dibahas rinci — bukan hanya konsep: penerjemahan alamat dan port, perilaku
penyaringan, server di belakang NAT, **hairpinning/NAT loopback**, NAT editor, dan
teknik menembus NAT (STUN, TURN, ICE, hole punching).

Ini bagian yang dipakai saat merancang akses jarak jauh ke NVR atau perangkat lapangan di
belakang NAT pelanggan, dan saat menjelaskan mengapa sebagian skema akses jarak jauh
bekerja di satu lokasi tetapi tidak di lokasi lain.

### E. DHCP dan konfigurasi otomatis (Bab 6, cetak 233 / PDF 272)

Format pesan, opsi, operasi protokol, **DHCPv6**, pemakaian dengan relay, autentikasi DHCP,
dan rekonfigurasi. Dipakai saat menyiapkan pengalamatan perangkat lapangan dalam jumlah
besar dan saat menelusuri konflik alamat.

### F. DNS (Bab 11, cetak 511 / PDF 550)

Termasuk dynamic update, zone transfer, NOTIFY, sort list, round-robin, split DNS, DNS64,
LLMNR/mDNS, dan serangan terhadap DNS. Relevan untuk sistem yang mengandalkan nama, bukan
alamat tetap.

### G. Keamanan (Bab 18, cetak 805 / PDF 844)

EAP, IPsec, TLS, DNSSEC, dan DKIM dalam satu bab. Ditambah bagian **Attacks Involving …**
di tiap bab lain — misalnya SYN flood dibahas di konteks retransmisi TCP
(cetak 640 / PDF 679).

---

## Perhitungan siap pakai

### 1. Bandwidth-Delay Product (BDP) — cetak 730 / PDF 769

Besaran yang menjelaskan mengapa satu aliran TCP tidak pernah memenuhi kapasitas tautan
jarak jauh.

```
BDP  =  RTT  ×  kapasitas tautan penyempit (bottleneck)
```

Menurut buku, BDP adalah **jumlah data yang dapat tersimpan di jaringan dalam perjalanan
menuju penerima**, dan jendela TCP `W` sebaiknya disetel **kira-kira sebesar BDP** — disebut
juga *optimal window size*. Kapasitas yang dipakai adalah kapasitas **tautan terkecil**
sepanjang jalur pengirim ke penerima, bukan kapasitas nominal langganan.

*Contoh ilustrasi:* tautan 100 Mb/s antar-kota dengan RTT 40 ms
→ BDP = 100.000.000 ÷ 8 × 0,040 = **500.000 byte ≈ 500 kB**.

Bila jendela TCP yang berlaku hanya 64 kB (batas tanpa window scaling), throughput satu
aliran terhenti di sekitar 64 kB ÷ 0,040 s ≈ **1,6 MB/s ≈ 13 Mb/s** — jauh di bawah
kapasitas 100 Mb/s, meski jaringannya sehat.

> **Ini penjelasan untuk keluhan yang sering muncul:** "bandwidth sudah 100 Mb/s tapi
> transfer tetap lambat". Penyebabnya jendela, bukan kapasitas. Penyelesaiannya
> **Window Scale option** (bagian 13.3.3), bukan menambah langganan.

### 2. Kapan Window Scale diperlukan — cetak 608 / PDF 647

Buku menyatakan opsi ini paling relevan saat TCP dipakai untuk **transfer data besar pada
jaringan ber-BDP besar** — yaitu jaringan dengan hasil kali RTT dan bandwidth yang relatif
besar.

Aturan praktis yang mengikuti: **bila BDP melebihi 64 kB, window scaling wajib aktif**
di kedua ujung, atau throughput akan terbatas berapa pun kapasitas tautannya.

### 3. Interval failure-finding jaringan? Bukan di sini

Buku ini **tidak memuat rumus perancangan kapasitas jaringan** (jumlah kamera per uplink,
oversubscription ratio, dan sejenisnya). Cakupannya perilaku protokol, bukan perencanaan
kapasitas. Untuk kebutuhan bitrate video, lihat resume `R3/CCTV-VSS/`.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Menelusuri gangguan dari tangkapan paket | Seluruh buku; mulai dari bab protokol yang dicurigai |
| Soket TIME_WAIT menumpuk, port habis | Bagian 13.5.2, cetak 618 / PDF 657 |
| Transfer besar menggantung di tautan VPN | Bab 10 + Path MTU, cetak 148 / PDF 187 |
| Akses jarak jauh ke perangkat di belakang NAT | Bab 7, cetak 299 / PDF 338 |
| Throughput jauh di bawah kapasitas tautan | Bab 16, cetak 727 / PDF 766 |
| Pengalamatan massal perangkat lapangan | Bab 6, cetak 233 / PDF 272 |
| Bagian keamanan pada kajian teknis | Bab 18 + bagian "Attacks Involving" tiap bab |
| Penyeragaman singkatan dalam dokumen | Glossary of Acronyms, cetak 933 / PDF 972 |

**Pendamping di rak:** `R3/NETWORK/` (Kurose & Ross) untuk dasar teori,
`R3/NETWORK/` (Network Warrior) untuk sisi perangkat Cisco,
`R3/NETWORK/` (CCNA 2024) untuk sertifikasi personel.

---

## Catatan mutu berkas

- Teks dapat dicari, mutu ekstraksi baik.
- **Sebagian gambar diagram tidak ikut terbaca sebagai teks** — sebagian halaman gambar
  menghasilkan karakter acak bila disalin. Yang terbaca adalah badan teksnya; diagram tetap
  tampil normal saat dilihat.
- Bookmark 207 entri dipasang 19 Agustus 2026 dari halaman daftar isi buku (PDF 12–26).
  Empat nomor halaman bab sempat terbaca kurang satu digit oleh ekstraksi teks dan sudah
  dikoreksi dengan penguncian ke halaman pembuka masing-masing bab.
- Cadangan sebelum bookmark: `_asli/TCP-IP Illustrated Vol 1 [ASLI sebelum bookmark].pdf`
