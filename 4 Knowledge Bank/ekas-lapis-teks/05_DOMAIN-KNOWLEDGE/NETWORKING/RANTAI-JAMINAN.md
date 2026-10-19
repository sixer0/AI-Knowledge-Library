# Rantai I — Jaringan IP untuk sistem terpasang

**Ambang terima berasal dari:** hitungan rancangan + kesepakatan kontrak ·
**tidak ada standar normatif di rak**

> Rantai ini menangani **jaringan yang menopang sistem** — pengawasan video, bukti digital,
> kendali. Untuk **penyimpanan dan BDP transfer jarak jauh**, lihat rantai **H**.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Odom, *CCNA 200-301* (2024) | **R3** | VLAN & trunking · spanning tree · redundansi gateway | PDF 51–75 · 107 · 207 |
| Kurose & Ross (2017) | **R3** | Antrean, tundaan, dasar unjuk kerja jaringan | PDF 113 · 217 |
| Fall & Stevens, *TCP/IP Illustrated* (2012) | **R3** ⚠14 th | Perilaku protokol · BDP · window scaling | PDF 655–664 · 766 · 770 |
| Donahue, *Network Warrior* (2011) | **R3** ⚠15 th | Pola gangguan · uplink kapasitas besar | PDF 89 |
| Limoncelli dkk. (2017) | **R3** | **Proses perubahan** & praktik operasional | PDF 618 |
| **TIA-568 / TIA-942** | **R2** | Perkabelan terstruktur & pusat data | ❌ **TIDAK ADA** |
| Lembar data switch, PBX, AP | **R4** | Kapasitas switching · anggaran PoE · batas sesi | ✅ `R4/NETWORK/` — 28 berkas |

> **CATATAN DEFECT (NWSKILL-0923/D1-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/networking-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3 (baris Odom di tabel sumber): angka "PDF 51-75", "107", "207" atas nama Odom adalah jangkar halaman Network Warrior milik Donahue, bukan CCNA Odom. Peta Donahue: Bab 4 VLANs = 51, Bab 6 VTP = 75, Bab 8 Spanning Tree = 107, Bab 13 First Hop Redundancy = 207 (lihat `R3 - Network Warrior.md`, daftar isi). Resume CCNA Odom hanya memuat jangkar Vol 1 = PDF 9 dan Vol 2 = PDF 1936. Bentuk tandingan: `R3 - Network Warrior.md`. Dampak: verifikasi klaim VLAN/STP/redundansi gateway yang membuka CCNA pada halaman itu mendarat di materi yang salah.
> K-1/K-2 (baris Fall & Stevens di tabel sumber): "766" dan "770" pada baris ini adalah kutipan bab tetangga kendali kemacetan. Bentuk kanonik hasil adjudikasi offset cetak+39: BDP = PDF 769, window scaling = PDF 647. Bentuk tandingan: `STORAGE/RANTAI-JAMINAN.md:47,53`; `KATALOG-RUMUS.md:397,400`; `REF-NET-004.md:24`; `R3 - TCP-IP Illustrated Vol 1.md:122,147`.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Pemisahan VLAN** jaringan pengawasan dari jaringan kantor | Odom PDF 51–75 | Satu VLAN datar **ditolak** — lalu lintas video membanjiri jaringan kantor, dan kamera terjangkau dari mana saja |
| Topologi & **redundansi gateway** | Odom PDF 207 | Gateway tunggal ditolak untuk sistem yang harus terus merekam |
| **Spanning tree** dan pencegahan lup | Odom PDF 107 | Membiarkan setelan bawaan ditolak — akar STP bisa jatuh ke switch akses |
| Kapasitas uplink ke NVR/penyimpanan | Hitungan mata ③ + Donahue PDF 89 | Uplink sama besar dengan port akses **ditolak** — uplink memikul seluruh aliran rekaman |
| **Anggaran PoE** per switch | **R4 wajib** | Menghitung dari jumlah port ditolak — **daya total catu hampir selalu lebih kecil** daripada jumlah daya maksimum semua port |
| Segmentasi & kendali akses ke perangkat | Anderson [R3] · lihat rantai **J** | Kamera dengan kata sandi bawaan **ditolak** |

> **CATATAN DEFECT (NWSKILL-0923/D1-FIXx, 2026-09-24):** known-defect atribusi pada tiga baris dasar di atas ("Odom PDF 51-75", "Odom PDF 207", "Odom PDF 107"): nomor halaman itu milik Network Warrior (Donahue), bukan CCNA Odom (butir K-3 studi NWSKILL-0923; rincian di catatan seksi rujukan). Vonis sementara lapis teks; BELUM TERKONFIRMASI sampai manusia membuka PDF primer. Keputusan desainnya tidak dibatalkan; yang dicacatkan adalah alamat halamannya.

> **Keputusan yang paling sering keliru: anggaran PoE.** Switch 24 port PoE+ tidak berarti
> sanggup memberi 30 W ke 24 port sekaligus. Angkanya dari lembar data **[R4]**, bukan dari
> perkalian.

---

## ③ Perhitungan

### Kebutuhan lebar pita agregat

```
Mb/s_total = Σ (bitrate per kamera) × faktor_puncak
```

Bitrate per kamera dari rantai **B**; nilai nyatanya **[R4]** atau hasil ukur instalasi
percobaan. **Faktor puncak** diperlukan karena rekaman berkorelasi — gerakan di satu area
menaikkan bitrate beberapa kamera sekaligus.

### Anggaran PoE

```
P_total_dibutuhkan = Σ (daya per perangkat × faktor_rugi_kabel)
harus ≤ anggaran PoE switch  [R4]
```

Rugi kabel bertambah pada jarak mendekati 100 m. Perangkat yang menarik daya di ambang
kelasnya akan **gagal menyala** pada ujung jauh meski switch tampak sanggup.

### Bandwidth-Delay Product — [R3, Fall & Stevens PDF 770]

```
BDP = RTT × kapasitas_penyempit
```

**Window scaling wajib bila BDP > 64 kB** [PDF 766]. Rincian di rantai **H**.

> **CATATAN DEFECT (NWSKILL-0923/D1-FIXx, 2026-09-24):** known-defect dua sitasi halaman pada subseksi ini (butir K-1 dan K-2 studi NWSKILL-0923). "PDF 770" untuk rumus BDP dipertanyakan: bentuk kanonik = PDF 769 (cetak 730 + 39; uji offset lolos 20/20 baris peta bab); PDF 770 = cetak 731 = rumusan Jacobson tentang kendali kemacetan (`R3 - TCP-IP Illustrated Vol 1.md:72`). "PDF 766" untuk aturan window scaling dipertanyakan: bentuk kanonik = PDF 647 (cetak 608, bagian 13.3.3); PDF 766 = cetak 727 = awal Bab 16 kendali kemacetan. Bentuk tandingan: `STORAGE/RANTAI-JAMINAN.md:47,53`; `KATALOG-RUMUS.md:397,400`; `REF-NET-004.md:24`; `R3 - TCP-IP Illustrated Vol 1.md:122,147`. Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer 766/769/770.

### Contoh terhitung

40 kamera, bitrate sedang 4 Mb/s, faktor puncak 1,5:

```
Mb/s_total = 40 × 4 × 1,5 = 240 Mb/s
```

→ uplink 1 Gb/s memadai untuk aliran rekam, **tetapi** periksa juga aliran pemutaran ulang
serentak: tiap operator yang memutar rekaman menambah beban ke arah sebaliknya.

---

## ④ Pengujian

| Butir | Ambang | Sumber |
|---|---|---|
| Lebar pita pada uplink saat **puncak** | Di bawah kapasitas rancangan | Hitungan mata ③ |
| **Daya PoE terpakai per switch** | Di bawah anggaran lembar data | **R4** |
| Perangkat menyala pada **ujung jauh** (mendekati 100 m) | Menyala & stabil | R4 + praktik |
| Peralihan gateway redundan | Beralih tanpa kehilangan rekaman | Kontrak |
| Pemulihan setelah lup / cabut kabel | Jaringan pulih dalam waktu yang ditetapkan | Kontrak |
| Pemisahan VLAN | Jaringan pengawasan **tidak terjangkau** dari VLAN kantor | Kontrak |
| Tundaan & kehilangan paket | Sesuai kebutuhan sistem video | Rantai **B** — BS EN 62676-1-2 [R2] |
| **Perkabelan terstruktur** | ⚠ **tidak ada sandaran standar di rak** | TIA-568 — `GAP-011` |

> **Uji yang paling sering dilewati: cabut kabel.** Redundansi yang dibayar hanya terbukti
> bekerja bila diuji dengan mencabut — bukan dengan membaca konfigurasi.

Waktu deteksi hilangnya sinyal video punya **ambang normatif [R2]**: 8 / 4 / 2 detik menurut
security grade — BS EN 62676-1-2 PDF 34. Itu satu-satunya ambang jaringan di rantai ini yang
tidak berasal dari kontrak.
> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** ambang 8 / 4 / 2 detik di atas berstatus known-defect - berkontradiksi dengan bentuk empat nilai 8/4/4/2 di `../VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md:45-48`; pemetaan per-grade BELUM TERKONFIRMASI terhadap PDF primer (ukur gsp-custodian 2026-09-23). Blok penuh: `R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'.


---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Diagram topologi as-built | ✅ | `09_HANDOVER/AS-BUILT/` |
| Tabel VLAN, alamat IP, dan port | ✅ | Termasuk penomoran port fisik |
| **Cadangan konfigurasi + versi firmware** | ✅ | `09_HANDOVER/CONFIGURATION-BACKUP/` |
| Pengukuran lebar pita saat puncak | ✅ | Bukan rata-rata |
| **Laporan daya PoE terpakai per switch** | ✅ | Terhadap anggaran lembar data |
| Hasil uji cabut kabel & peralihan gateway | ✅ | Bukti redundansi bekerja |
| Bukti pemisahan VLAN | ✅ | Percobaan jangkau dari VLAN kantor — harus gagal |
| Lembar data switch/AP | ✅ **[R4]** | `R4/NETWORK/` |
| **Catatan perubahan konfigurasi** | ✅ | Limoncelli PDF 618 — proses perubahan |
| Kartu kendali rantai | ✅ | Satu per besaran |

---

## Status rantai

**UTUH pada perhitungan · TANPA SANDARAN NORMATIF pada sebagian besar ambang.**

Seluruh ambang kecuali waktu deteksi hilang sinyal berasal dari **hitungan rancangan dan
kontrak**. Itu sah — tetapi berarti ambangnya **hanya sekuat kesepakatan tertulisnya**.
Pastikan angka lebar pita, waktu pemulihan, dan pemisahan jaringan **masuk kontrak**, bukan
hanya proposal.

**Celah yang masih terbuka:** **TIA-568** (perkabelan terstruktur) dan **TIA-942** (pusat
data) — `GAP-011`, prioritas menengah.

**Peringatan usia:** Fall & Stevens (2012) dan Donahue (2011) melewati 14–15 tahun.
Perilaku protokol dan pola gangguan tetap berlaku; **platform dan perintah yang disebut
Donahue sudah tidak dijual**. Odom (2024) yang paling mutakhir untuk praktik perangkat.
