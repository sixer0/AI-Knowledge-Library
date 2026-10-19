# Rantai F — Pemeriksaan termal (termografi)

**Ambang terima berasal dari:** **ANSI/NETA ATS-2017 Tabel 100.18 [R2]**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| **ANSI/NETA ATS-2017** | **R2** | **Ambang ΔT lulus/tidak** (Tabel 100.18) | PDF 246 |
| Vollmer & Möllmann, *Infrared Thermal Imaging* (2018) | **R3** | Parameter wajib kamera, aturan IFOV, fisika pengukuran | PDF 25, 128 |
| Gill, *Electrical Power Equipment Maintenance* | **R3** | Konteks pemeliharaan kelistrikan | Bab 12 |
| Lembar data kamera termal | **R4** | NETD, rentang suhu, IFOV nyata | per proyek |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-3 (baris Gill pada tabel rujukan di atas): arah rujukan menyesatkan, terukur di lapis teks. Pointer 'Bab 12' tidak memuat satu pun ambang termal - resume Gill nol kemunculan 'termal/termograf/inframerah/infrared' (grep -i = 0 hasil) dan judul Bab 12 adalah 'Power Quality, Harmonics, Predictive Maintenance' PDF 754 (`ELECTRICAL/R3 - Electrical Power Equipment Maintenance and Testing.md` peta isi). Kriteria ΔT yang dipakai rak berasal dari NETA [R2], bukan Gill. Judul buku di baris ini pun tidak lengkap ('Maintenance' tanpa 'and Testing') dan tanpa nomor PDF padahal jangkarnya tersedia. Angka tidak berubah; yang dicacatkan arah rujukan (register K-3).

> **Perhatikan pembagian peran.** Vollmer adalah **buku fisika**, bukan standar
> pemeliharaan — ia menjelaskan mengapa pengukuran bisa keliru, tetapi tidak menetapkan
> berapa ΔT yang berarti cacat. Angka itu dari NETA [R2].

---

## ② Keputusan desain

Termografi jarang "dirancang", tetapi tetap ada keputusan yang harus tertulis:

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Titik yang diperiksa | Peralatan bertegangan & bersambungan | Pemeriksaan acak ditolak — cacat sambungan tidak tersebar merata |
| **Beban saat pemeriksaan** | Harus mendekati beban operasi | Pemeriksaan pada beban rendah **ditolak** — cacat resistif tidak muncul |
| Sudut pandang & jarak | Aturan IFOV mata ③ | Memotret dari jarak nyaman ditolak bila objek tidak menutupi cukup piksel |
| Cara membandingkan | Antar-komponen serupa **atau** terhadap udara sekitar | Membandingkan komponen tak sejenis ditolak — emisivitas dan beban berbeda |

---

## ③ Perhitungan dan prasyarat ukur

### Delapan parameter wajib — [R3, Vollmer PDF 25]

Salah satu saja keliru, hasil suhunya keliru:

```
emisivitas · jarak · ukuran objek · kelembapan
suhu lingkungan · suhu atmosfer · suhu optik eksternal · transmisi optik eksternal
```

### Aturan IFOV — [R3, Vollmer PDF 128]

Objek harus menutupi **beberapa piksel**, bukan satu. Bila tidak → dekati, atau pakai lensa
tele. Objek sub-piksel menghasilkan suhu **rata-rata dengan latarnya** — lebih rendah dari
yang sebenarnya, sehingga **cacat justru terlewat**.

### Uji pantulan

Ubah sudut pandang. Bila titik panas **ikut berpindah**, itu **pantulan**, bukan panas.
Langkah ini yang memisahkan temuan nyata dari temuan palsu.

### Perhitungan ΔT

```
ΔT_serupa  = T_komponen − T_komponen_sejenis_pada_beban_serupa
ΔT_udara   = T_komponen − T_udara_sekitar
```

---

## ④ Pengujian

| Butir | Ambang | Sumber |
|---|---|---|
| **ΔT antar komponen serupa** | **> 15 °C → perbaiki segera** | **R2** — ATS-2017 Tabel 100.18 PDF 246 |
| **ΔT terhadap udara sekitar** | **> 40 °C → perbaiki segera** | **R2** — PDF 246 |
| Delapan parameter kamera | Tercatat seluruhnya | R3 — Vollmer PDF 25 |
| Aturan IFOV terpenuhi | Objek menutupi beberapa piksel | R3 — PDF 128 |
| Uji pantulan dilakukan | Untuk tiap temuan | R3 |
| Beban saat pemeriksaan | Tercatat, mendekati operasi | Praktik |


> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1a..d (tabel ambang di atas hanya memuat dua baris 'perbaiki segera'): cuplikan, bukan tabel lengkap. Sumber primer lapis teks adalah Tabel 100.18 EMPAT tingkat + kualifikator + syarat beban - utuh di `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92` dan `KATALOG-RUMUS.md` seksi 13.1. Hilir yang membaca tabel di atas saja akan menggolongkan ΔT udara 25 °C sebagai 'tidak ada aturan' (rak menamainya 'Pantau sampai perbaikan dapat dilakukan') dan ΔT serupa 2 °C sebagai aman (rak menamainya 'Kemungkinan cacat; perlu diselidiki'). Kualifikator 'panduan tindakan, bukan batas mutlak' hilang di lapis ini; syarat 'beban serupa' pulih hanya di prosa setelah tabel. Uji petahan: angka > 15 / > 40 seragam di tujuh lapis - cacatnya kelengkapan propagasi, bukan angka (register K-1a..d).
> **Ambang ini menuntut disiplin pencatatan.** ΔT hanya bermakna bila emisivitas dan suhu
> udara tercatat — dan Tabel 100.18 mensyaratkan pembandingnya jelas: komponen sejenis pada
> **beban serupa**, atau udara sekitar. Membandingkan komponen bersebelahan yang bebannya
> berbeda menghasilkan ΔT yang tidak berarti apa-apa.

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-8 (lingkup pemakaian ambang di atas): ambang yang dipakai mata ④ rantai ini berasal dari ANSI/NETA **ATS-2017 (uji terima)**, sementara kegunaan utama rantai F di rak adalah pemeriksaan instalasi listrik BERJALAN pada beban operasi - wilayah **MTS** yang TIDAK ada di rak (`AMBANG-TERIMA-INDUK.md:77`; peringatan wajib `:25-28`). Terukur sebelum anotasi ini: `grep -i MTS` pada folder THERMAL ini = 0 hasil. Bukan salah angka; salah lingkup. Putusan sah/tidaknya ambang dipakai di lapangan = keputusan controller-manusia (register K-8).

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara pemeriksaan termal | ✅ | Kerangka bagian 7 |
| **Citra termal + citra tampak** tiap titik | ✅ | Berpasangan — citra termal saja sulit ditafsirkan kemudian |
| **Delapan parameter kamera** untuk tiap pengukuran | ✅ | Tanpa ini suhunya tidak dapat diverifikasi ulang |
| **Beban saat pemeriksaan** | ✅ | Menentukan apakah hasil "aman" bermakna |
| Suhu udara sekitar | ✅ | Pembanding untuk ΔT_udara |
| Tabel ΔT + klasifikasi terhadap Tabel 100.18 | ✅ | **Sebutkan nomor tabelnya** |
| Catatan uji pantulan | ✅ | Menunjukkan temuan sudah disaring |
| Sertifikat kalibrasi kamera | ✅ | — |
| Kartu kendali rantai | ✅ | — |

**Status rantai: UTUH.** Ambang normatif [R2], prasyarat ukur terjelaskan [R3].

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-7 (klaim UTUH di atas): berlaku untuk ambang [R2] dan prasyarat ukur [R3]; BUTIR R4 rantai ini belum bisa dikutip. NETD/IFOV nyata wajib lembar data per proyek. `R4-STATUS.md` menyebut butir F 'TERTUTUP' tetapi artinya hanya 'lembar data calon sudah masuk laci CAMERA/' - nol angka NETD/IFOV produk naik ke lapis teks mana pun (register K-7). Jangan promosikan 'tertutup' menjadi angka; tulis 'menunggu data pabrikan' sesuai aturan `AMBANG-TERIMA-INDUK.md` bagian Wajib R4.

**Yang harus dijaga:** godaan melaporkan angka suhu mutlak tanpa parameter. Suhu mutlak dari
kamera termal **bukan pengukuran suhu** dalam arti metrologi — ia hasil hitungan dari
delapan masukan. Tanpa masukannya tercatat, angka itu tidak dapat dipertahankan.
