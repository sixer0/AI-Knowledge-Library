# Rantai Jaminan — dari rujukan sampai bukti serah terima

**Bagian dari:** EKAS · **Disusun:** 20 Agustus 2026

Perpustakaan menjawab *"di buku mana?"*. Sistem jaminan menjawab *"bagaimana angka ini
sampai ke berita acara, dan apakah ia bertahan saat diperiksa?"*

Perbedaannya bukan pada isi, melainkan pada **arah**. Perpustakaan disusun menurut buku.
Sistem jaminan disusun menurut **rantai** — dan sebuah rujukan dianggap belum berguna
sampai rantainya sampai ke ujung.

---

## Lima mata rantai

```
  ①  RUJUKAN            "dari mana angkanya"
      [tingkat R1–R5, judul, halaman]
              │
              ▼
  ②  KEPUTUSAN DESAIN   "apa yang ditetapkan karena itu"
      [pilihan + alternatif yang ditolak + alasannya]
              │
              ▼
  ③  PERHITUNGAN        "berapa angkanya"
      [rumus + masukan + asumsi bertanda + hasil]
              │
              ▼
  ④  PENGUJIAN          "bagaimana dibuktikan di lapangan"
      [metode + alat + ambang + siapa menyaksikan]
              │
              ▼
  ⑤  BUKTI SERAH        "apa yang diserahkan sebagai bukti"
      [berita acara + lampiran + rekaman alat + tanda tangan]
```

**Rantai putus bila salah satu mata hilang.** Yang paling sering putus:

| Mata yang hilang | Gejalanya di dokumen | Akibat saat diperiksa |
|---|---|---|
| ① Rujukan | Angka muncul tanpa sumber | *"Dasarnya apa?"* — tidak terjawab |
| ② Keputusan | Hitungan ada, tetapi tidak jelas menetapkan apa | Perancangan terlihat sewenang-wenang |
| ③ Perhitungan | Ambang disebut, cara memperolehnya tidak | Ambang terlihat dikarang |
| ④ Pengujian | Rancangan lengkap, cara membuktikan tidak ada | Tidak ada dasar menyatakan "selesai" |
| ⑤ Bukti | Uji dilakukan, hasilnya tidak terdokumentasi | Pekerjaan sah tetapi **tidak dapat ditagihkan** |

> Mata ⑤ yang paling mahal bila hilang. Pekerjaan yang benar-benar dikerjakan tetapi
> tidak berbukti, secara administrasi sama dengan pekerjaan yang tidak dikerjakan.

---

## Aturan tingkat pada tiap mata rantai

Tingkat R1–R5 tidak berlaku seragam di sepanjang rantai:

| Mata | Tingkat yang dituntut | Catatan |
|---|---|---|
| ① Rujukan | apa adanya — **dicatat**, bukan dinilai | Semua tingkat boleh masuk asalkan bertanda |
| ② Keputusan desain | **R3 cukup** | Keputusan rekayasa memang penilaian; yang penting alasannya tertulis |
| ③ Perhitungan | **R2 atau R3** untuk rumus · **R4 wajib** untuk angka produk | Campuran — tandai per masukan |
| ④ Ambang pengujian | **R1 → R2 → kontrak** | R3 hanya bila kontrak mengadopsinya tertulis |
| ⑤ Bukti serah | — | Bukan soal tingkat; soal kelengkapan dan keterlacakan |

**Konsekuensi yang harus dipahami:** sebuah rantai dapat sepenuhnya sah di mata ①–③ dan
tetap **gagal di mata ④**, karena rumusnya dari R3 tetapi ambangnya juga diambil dari R3.
Contoh nyata di rak ini: interval uji genset dihitung dengan rumus FFI Moubray [R3] —
sah sebagai metode — tetapi bila interval itu dijadikan **kewajiban kontraktual**, ia harus
diadopsi tertulis dalam kontrak, bukan dirujuk ke bukunya saja.

---

## Kartu kendali rantai

Dipakai satu kartu per besaran yang masuk dokumen serah. Bentuk minimum:

```
BESARAN     : ..............................................
NILAI        : ..............................................

① RUJUKAN    : [R_] ......................... hal. .........
② KEPUTUSAN  : yang ditetapkan ..............................
               alternatif ditolak ...........................
③ HITUNGAN   : rumus .......................................
               masukan ......................................
               asumsi [tandai] ..............................
               hasil ........................................
④ UJI        : metode ......................................
               alat + kalibrasi .............................
               AMBANG ....................... sumber [R_] ...
⑤ BUKTI      : berita acara no. ............................
               lampiran .....................................

STATUS RANTAI : ☐ utuh   ☐ putus di mata ___   ☐ menunggu R4
```

Kartu yang berstatus **"menunggu R4"** adalah kartu yang sah — asalkan tertulis. Yang
tidak sah adalah kartu yang diisi angka umum lalu dilupakan asal-usulnya.

---

## Delapan rantai yang sudah tersusun

Ada di `rantai/` — masing-masing lengkap dari ① sampai ⑤:

| Berkas | Domain | Ambang berasal dari |
|---|---|---|
| `A-serat-optik.md` | Jalur serat optik | **Hitungan rancangan** + metode IEC 61280-4-2 [R2] |
| `B-video-pengawasan.md` | Sistem pengawasan video | Sasaran pemilik + BS EN 62676-1-2 [R2] |
| `C-catu-daya-baterai.md` | UPS, baterai, genset | IEEE 1188 & IEC 62485-2 [R2] + lembar data [R4] |
| `D-pembumian-petir.md` | Pembumian & proteksi petir | ⚠ **belum ada sumber sah** — celah R1 |
| `E-uji-instalasi-listrik.md` | Uji tahanan isolasi | ANSI/NETA ATS-2017 [R2] |
| `F-termografi.md` | Pemeriksaan termal | ANSI/NETA ATS-2017 Tabel 100.18 [R2] |
| `G-keandalan-pemeliharaan.md` | Interval & strategi pemeliharaan | Hitungan RCM [R3] + adopsi kontrak |
| `H-penyimpanan-jaringan.md` | Penyimpanan & jaringan | Hitungan rancangan |
| `NETWORKING/RANTAI-JAMINAN.md` | **I** — Jaringan IP sistem terpasang | Hitungan + kontrak · deteksi hilang sinyal **[R2]** |
| `CYBERSECURITY/RANTAI-JAMINAN.md` | **J** — Keamanan siber & bukti digital | ⚠ **PUTUS di mata ④** — celah R1/R2 |
| `CIVIL-STRUCTURAL/RANTAI-JAMINAN.md` | **K** — Struktur penopang perangkat | ⚠ **PUTUS di mata ④** — empat SNI kosong |
| `PROJECT-QUALITY/RANTAI-JAMINAN.md` | **M** — Mutu, audit, kendali dokumen | Melingkupi rantai lain |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-6 PHANTOM POINTER (baris `F-termografi.md` pada tabel di atas): berkas TIDAK ADA di disk - ukur ulang pada giliran tambal: `find ekas -name 'F-termografi.md'` = 0 hasil; seluruh delapan nama berkas per-rantai pada tabel ini (`A-serat-optik.md` sampai `H-penyimpanan-jaringan.md`) = 0 hasil, sedangkan tiga baris terakhir tabel yang sama menunjuk path `*/RANTAI-JAMINAN.md` yang memang ada. Sasaran nyata rantai F = `05_DOMAIN-KNOWLEDGE/THERMAL/RANTAI-JAMINAN.md`. JANGAN merujuk atau menyuruh mengisi `F-termografi.md` (register K-6).

**Rantai D, J, dan K putus di mata ④** dan keduanya sengaja diterbitkan dalam keadaan
putus, supaya kelemahannya terlihat sebelum dipakai — bukan setelah dipersoalkan pemeriksa.

**Rantai J putusnya lebih luas daripada D:** pada D hanya satu ambang yang hilang; pada J
**seluruh sumber R1 dan R2 tidak ada** — empat celah prioritas tinggi sekaligus.

---

## Cara memakai sistem ini pada pekerjaan nyata

1. **Mulai dari rantai domainnya**, bukan dari buku. Buka `rantai/X-*.md` sesuai pekerjaan.
2. **Isi kartu kendali** untuk tiap besaran yang akan masuk dokumen serah.
3. **Tandai kartu yang menunggu R4** dan kirim permintaan data ke pabrikan lebih awal —
   ini yang paling sering menjadi penghambat di akhir proyek.
4. **Periksa mata ④** sebelum menyusun berita acara: apakah ambangnya punya sumber sah?
   Bila R3, apakah kontrak mengadopsinya?
5. **Susun berita acara** dari kerangka di `04-pengujian-bukti/TEMPLATE-BERITA-ACARA.md`.
6. **Simpan kartu kendali bersama berita acara.** Kartu itu yang menjawab pertanyaan
   pemeriksa tanpa harus membongkar ulang perhitungan.

---

## Yang membedakan sistem ini dari daftar rujukan biasa

Daftar rujukan menyatakan **apa yang dimiliki**. Sistem jaminan menyatakan **apa yang dapat
dipertahankan** — dan, sama pentingnya, **apa yang tidak**.

Tiga pernyataan yang hanya mungkin karena sistem ini ada:

1. *"Ambang uji tahanan isolasi pada pekerjaan ini bersandar pada standar internasional
   [R2], bukan pada penilaian pelaksana."*
2. *"Faktor derating genset belum dapat ditetapkan sampai surat pabrikan diterima; angka
   sementara dipakai hanya untuk kajian kepekaan, tidak untuk ambang terima."*
3. *"Ambang resistansi pembumian pada pekerjaan ini belum memiliki sandaran normatif dan
   harus ditetapkan pemilik sistem secara tertulis."*

Ketiganya terdengar seperti kelemahan. Justru sebaliknya — **dokumen yang menyatakan
batasnya lebih sulit dipatahkan** daripada dokumen yang menyamarkannya, karena tidak ada
lagi yang tersisa untuk ditemukan pemeriksa.
