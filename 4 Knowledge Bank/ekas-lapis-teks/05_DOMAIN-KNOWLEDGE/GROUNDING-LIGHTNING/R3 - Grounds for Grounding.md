# Resume — Grounds for Grounding: A Handbook from Circuits to Systems

**Penulis:** Elya B. Joffe, Kai-Sang Lock · **Edisi:** kedua · **Penerbit:** Wiley-IEEE Press, 2023
**Berkas:** `Elya B. Joffe, Kai-Sang Lock - Grounds for Grounding (2nd Edition, 2023).pdf` — 1.216 halaman, 133,1 MB
**Disusun:** 19 Agustus 2026, dari teks buku ini

> **Rujukan halaman memakai nomor PDF**, karena nomor cetak buku ini tidak konsisten
> terbaca oleh ekstraksi teks. Bookmark bawaan berkas sangat rinci — **979 entri** sampai
> tingkat sub-sub-bagian — jadi navigasi paling cepat lewat panel daftar isi.

Buku pembumian paling lengkap di rak ini, dan salah satu yang paling lengkap yang ada.
Ditulis dua praktisi EMC (Joffe dari IEEE EMC Society), pendekatannya **dari rangkaian ke
sistem**: bukan sekadar "berapa ohm", melainkan mengapa pembumian berperilaku berbeda pada
frekuensi rendah dan tinggi, dan apa akibatnya pada desain fasilitas.

Kekuatan khasnya: satu bab penuh membongkar **mitos pembumian** yang beredar luas di
lapangan — berguna saat harus menolak permintaan pelanggan atau konsultan yang tidak
berdasar.

---

## Peta isi

| Bab | Judul | PDF |
|---|---|---|
| — | Foreword · Preface edisi kedua | 25 · 27 |
| 1 | Overview | 31 |
| 2 | Fundamental Concepts | 39 |
| 3 | **The Grounds for Grounding** (pembongkaran mitos) | 167 |
| 4 | **Fundamentals of Grounding Design** | 201 |
| 5 | Bonding Principles | 331 |
| 6 | Grounding in Power Transmission and Distribution | 395 |
| 7 | **Grounding for Generators, UPSs, VSDs** | 429 |
| 8 | **Grounding for Lightning Protection Systems** | 455 |
| 9 | Integrated Facility and Mobile/Transportable Systems | 479 |
| 10 | **The Earth Connection** (elektroda & pengukuran) | 553 |
| 11 | Grounding in Wiring Circuits and Cable Shields | 589 |
| 12 | Grounding of Terminal Protection Devices | 693 |
| 13 | Grounding on Printed Circuit Boards | 727 |
| 14 | **Testing and Troubleshooting Grounding Problems** | 1031 |

### Apendiks — bagian yang paling langsung terpakai

| Apendiks | Isi | PDF |
|---|---|---|
| A | Glosarium istilah grounding/earthing/bonding | 1055 |
| B | Akronim | 1071 |
| C | Simbol | 1075 |
| D | Nilai sifat dasar bahan | 1077 |
| E | Standar terkait pembumian | 1079 |
| F | Percobaan praktis untuk peragaan | 1101 |
| **G** | **Daftar periksa dan prosedur verifikasi pembumian** | **1111** |
| **H** | **Isi dokumentasi pembumian** | **1149** |
| I | Kesetaraan Hukum Ohm dan … | 1151 |
| J | Arus balik frekuensi rendah | 1155 |
| K | Ikhtisar parameter S | 1175 |
| L | Contoh analisis "common-impedance" | 1187 |
| M | Soal periksa pemahaman | 1197 |
| — | Indeks | 1207 |

**Apendiks G dan H adalah pintu masuk tercepat untuk pekerjaan lapangan** — G memberi daftar
periksa verifikasi, H memberi daftar isi dokumen pembumian yang harus diserahkan. Keduanya
bisa langsung dijadikan kerangka berita acara dan dokumen serah.

---

## Bagian yang paling sering dipakai

### A. Mitos pembumian (Bab 3, PDF 167)

Bab ini menyebut satu per satu keyakinan yang beredar dan menunjukkan di mana salahnya.
Beberapa yang dikutip di halaman pembuka bab (PDF 32):

- "Elektroda bumi (rod) yang mencegah kita tersengat"
- "Supaya aman, tambah saja jumlah ground rod"
- "Menyambung netral dan ground di banyak titik itu bagus"

Yang perlu dipahami dari bab ini (PDF 182): gagasan **permukaan ekipotensial berimpedansi
nol** itu fiktif — sering dianggap benar karena hanya dinilai dari perilaku DC-nya. Pada
frekuensi tinggi, konduktor pembumian berperilaku sebagai impedansi, bukan sebagai
hubung-singkat.

### B. Titik tunggal vs banyak titik (PDF 175–181)

Perdebatan klasik *single-point* vs *multipoint grounding*. Ringkasan sikap buku:

- Distribusi listrik rumah modern **tidak lagi mengikuti** pembumian titik tunggal (PDF 175)
- Untuk lingkungan dengan transien — misalnya di bawah lantai akses ruang komputer —
  **multipoint bonding ke seluruh baja bangunan yang tersedia umumnya yang terbaik** (PDF 181)

Ini rujukan saat merancang pembumian ruang server dan pusat kendali, dan saat menjawab
konsultan yang bersikeras pada pembumian titik tunggal untuk semua kasus.

### C. Impedansi grid dan mesh (PDF 212)

Bidang logam pejal memberi unjuk kerja optimal, khususnya pada frekuensi tinggi. Grid dan
mesh kawat merupakan pendekatan praktisnya, dengan konsekuensi induktansi. Bagian 4.1.3.1.5
membahas impedansinya — dipakai saat menentukan rapat mesh pembumian ruang peralatan.

### D. Sambungan ke bumi dan pengukurannya (Bab 10, PDF 553)

**Resistivitas tanah** dan pengaruhnya pada tegangan langkah dan sentuh dibahas dengan
contoh terhitung (PDF 402): untuk berat badan 70 kg, resistivitas tanah 100 Ω·m tanpa
lapisan permukaan, dan durasi gangguan 3 detik, diperoleh batas tegangan langkah yang dapat
ditoleransi.

**Dua metode pengukuran yang dipakai di lapangan:**

| Metode | Isi | PDF |
|---|---|---|
| **Wenner** | Empat elektroda berjarak sama dalam satu garis; rasio V/I memberi resistansi | 579 |
| **Fall-of-potential** (tiga pasak) | Metode paling populer untuk mengukur resistansi elektroda bumi terpasang | 580 |

Dua metode ini yang dipakai menyusun berita acara uji pembumian. Perhatikan: pengukuran
menuntut **konduktor penghubung dilepas dari elektroda** lebih dulu (PDF 580) — langkah yang
sering dilewat sehingga hasil ukurnya tidak sah.

### E. Pembumian genset, UPS, dan VSD (Bab 7, PDF 429)

Langsung relevan untuk instalasi catu daya pelanggan: pembumian sumber terpisah, sistem
peralihan, dan interaksi dengan penggerak berkecepatan variabel. Dipakai bersama
`R3/GENSET/` dan `R3/UPS/` di rak.

### F. Pembumian untuk proteksi petir (Bab 8, PDF 455)

Menjembatani buku ini dengan `R3/LIGHTNING/` (Uman). Uman membahas fisika dan sistem
proteksinya; bab ini membahas **sisi pembumiannya** — bagaimana sistem proteksi petir
terhubung ke bumi tanpa menimbulkan masalah pada peralatan elektronik di dalamnya.

### G. Fasilitas terpadu dan sistem bergerak (Bab 9, PDF 479)

Bab untuk shelter, kontainer, kendaraan, dan sistem yang dipindah-pindah — konfigurasi yang
sering muncul pada pekerjaan lapangan GSP dan jarang dibahas buku pembumian lain.

### H. Pengujian dan penelusuran gangguan (Bab 14, PDF 1031)

Prosedur menemukan sumber masalah pembumian pada sistem terpasang. Dipakai saat menangani
keluhan gangguan yang diduga berasal dari pembumian — dering, derau pada video, perangkat
yang berulang mati.

---

## Perhitungan siap pakai

Diambil langsung dari buku dengan nomor persamaannya. Angka yang masuk dokumen serah tetap
harus disertifikasi `veritas`.

### 1. Resistivitas tanah — metode Wenner (PDF 579–580, Pers. 10.17 dan 10.18)

Empat elektroda berjarak sama dalam satu garis lurus. `a` = jarak antar elektroda
bersebelahan, `b` = kedalaman penancapan, `R = V/I` = resistansi terukur (Ω).

**Bentuk lengkap (Pers. 10.17):**

```
                    4 π a R
ρ  =  ──────────────────────────────────────
        1 + 2a/√(a²+4b²) − a/√(a²+b²)
```

**Bentuk praktis (Pers. 10.18)** — berlaku bila kedalaman `b` dibuat jauh lebih kecil
daripada jarak `a`, yang memang praktik lapangannya:

```
ρ  =  2 π a R
```

> Hasilnya adalah **resistivitas rata-rata tanah sampai kedalaman ± a** (PDF 580).
> Jadi jarak antar elektroda menentukan kedalaman yang tersurvei — bukan sekadar
> ketelitian pengukuran.

*Contoh ilustrasi:* jarak elektroda a = 3 m, alat membaca R = 5,3 Ω
→ ρ = 2 × 3,1416 × 3 × 5,3 ≈ **99,9 Ω·m**, mewakili tanah sampai kedalaman ± 3 m.

**Untuk profil tanah berlapis:** ulangi pengukuran pada beberapa nilai `a` (mis. 1, 2, 4,
8, 16 m). Kenaikan atau penurunan ρ terhadap `a` menunjukkan lapisan tanah yang berbeda —
inilah dasar penentuan kedalaman penancapan elektroda (PDF 561–562).

**Keterbatasan yang dicatat buku (PDF 580):** pada jarak `a` besar, tegangan antara dua
elektroda dalam turun cepat dan **mungkin tidak terukur teliti oleh instrumen murah**.
Untuk kasus itu buku menyarankan susunan **Schlumberger-Palmer**.

### 2. Pengukuran resistansi elektroda — fall-of-potential (PDF 580)

Metode tiga pasak, yang paling umum dipakai untuk mengukur resistansi elektroda terpasang.

> **Prasyarat yang sering dilewat:** konduktor penghubung **harus dilepas dari elektroda
> bumi** sebelum diukur. Bila tidak, yang terukur adalah gabungan seluruh sistem, bukan
> elektroda yang dimaksud — dan hasilnya tidak sah dijadikan dasar berita acara.

### 3. Prinsip dasar yang menentukan hasil

Buku menegaskan (PDF 562): **nilai resistansi pembumian berbanding lurus dengan
resistivitas medium** tempat elektroda dipasang. Karena itu urutan kerjanya selalu:

```
ukur resistivitas tanah (Wenner)
        ↓
tentukan jenis, jumlah, dan kedalaman elektroda
        ↓
pasang
        ↓
ukur resistansi terpasang (fall-of-potential)
```

Membalik urutan ini — memasang dulu lalu berharap angkanya tercapai — adalah penyebab
tersering pekerjaan pembumian harus diulang.

### Yang tidak ada di buku ini

Buku **tidak menetapkan angka ambang resistansi pembumian** (mis. "harus di bawah 5 Ω").
Pendekatannya berbasis kebutuhan sistem, bukan angka tunggal. Bila dokumen tender menuntut
ambang tertentu, angkanya diambil dari standar yang berlaku atau dari persyaratan pemilik
sistem — bukan dari buku ini.

---

## Pemakaian di GSP

| Keperluan | Bagian |
|---|---|
| Desain pembumian ruang server dan pusat kendali | Bab 4 + PDF 175–181 (titik tunggal vs multipoint) |
| Pembumian shelter, menara, sistem bergerak | Bab 9, PDF 479 |
| Pembumian genset dan UPS pelanggan | Bab 7, PDF 429 |
| Pembumian sistem proteksi petir | Bab 8, PDF 455 — bersama buku Uman |
| Berita acara uji pembumian | Wenner PDF 579 · Fall-of-potential PDF 580 · Apendiks G PDF 1111 |
| Daftar isi dokumen serah pembumian | Apendiks H, PDF 1149 |
| Menolak permintaan tak berdasar | Bab 3, PDF 167 (pembongkaran mitos) |
| Penelusuran gangguan derau/dering | Bab 14, PDF 1031 |
| Rujukan standar | Apendiks E, PDF 1079 |
| Penyeragaman istilah dokumen | Apendiks A, PDF 1055 |

**Pendamping di rak:** `R3/LIGHTNING/` (Uman) untuk sisi proteksi petir,
`R3/ELECTRICAL/` (Gill) untuk pembumian sistem tenaga dan pengujiannya,
`R3/UPS/` dan `R3/GENSET/` untuk sisi catu daya.

---

## Catatan mutu berkas

- Teks dapat dicari; bookmark bawaan 979 entri sangat rinci dan tidak perlu diperbaiki.
- Simbol Ω dan sebagian karakter khusus kadang terbaca sebagai `?` saat teks disalin —
  tampilan halaman tetap normal.
- Berkas 133 MB, salah satu yang terbesar di rak; wajar karena 1.216 halaman bergambar padat.
- Tidak ada cadangan `_asli/` untuk buku ini karena isinya tidak pernah diubah.
