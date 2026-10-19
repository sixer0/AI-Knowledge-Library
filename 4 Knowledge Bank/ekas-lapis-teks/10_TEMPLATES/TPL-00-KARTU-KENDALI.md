# Kartu Kendali Rantai — lembar isian

**Bagian dari:** EKAS · Satu kartu per besaran yang masuk dokumen serah terima.

Kartu ini yang menjawab pertanyaan pemeriksa **tanpa harus membongkar ulang perhitungan.**
Disimpan bersama berita acara, bukan terpisah.

---

## Lembar kosong

```
════════════════════════════════════════════════════════════════
KARTU KENDALI RANTAI JAMINAN                    No. ...........
Proyek     : .................................................
Rantai     : ☐A serat  ☐B video  ☐C daya  ☐D bumi
             ☐E isolasi ☐F termal ☐G keandalan ☐H simpan
════════════════════════════════════════════════════════════════

BESARAN    : .................................................
NILAI      : ................................. satuan ........

──── ① RUJUKAN ────────────────────────────────────────────────
Tingkat    : ☐R1 regulasi  ☐R2 standar  ☐R3 buku
             ☐R4 pabrikan  ☐R5 sekunder
Judul      : .................................................
Halaman    : ..........  Tahun terbit : ..........
Peringatan usia (>15 th)?   ☐ tidak  ☐ ya → dinyatakan di dok.

──── ② KEPUTUSAN DESAIN ───────────────────────────────────────
Yang ditetapkan      : .......................................
Alternatif ditolak   : .......................................
Alasan penolakan     : .......................................

──── ③ PERHITUNGAN ────────────────────────────────────────────
Rumus      : .................................................
Sumber rumus         : [R__] ................. hal. .........
Masukan    :
   ...................  = ..........  [R__]  ☐ terukur ☐ asumsi
   ...................  = ..........  [R__]  ☐ terukur ☐ asumsi
   ...................  = ..........  [R__]  ☐ terukur ☐ asumsi
Hasil      : .................................................
Kepekaan   : bila masukan kritis ±50% → hasil menjadi ........

──── ④ PENGUJIAN ──────────────────────────────────────────────
Metode     : .................................................
Sumber metode        : [R__] ................. hal. .........
Alat       : merek/tipe ............ no. seri ...............
             kalibrasi berlaku s.d. ..........
AMBANG     : .................................................
Sumber ambang        : [R__] ................. hal. .........
   ⚠ Bila sumber ambang = R3, apakah diadopsi kontrak?
     ☐ ya, pasal ..........   ☐ belum → RANTAI PUTUS
Penyaksi   : .................................................

──── ⑤ BUKTI SERAH ────────────────────────────────────────────
Berita acara no.     : .......................................
Lampiran   : ☐ hasil ukur   ☐ rekaman alat   ☐ citra
             ☐ sertifikat kalibrasi          ☐ perhitungan
             ☐ surat pabrikan [R4]           ☐ .............

════════════════════════════════════════════════════════════════
STATUS RANTAI
  ☐ UTUH — kelima mata terisi, ambang bersumber sah
  ☐ MENUNGGU R4 — sah; surat pabrikan sudah diminta tgl ......
  ☐ MENUNGGU PENETAPAN PEMILIK — surat permintaan tgl ........
  ☐ PUTUS di mata ___  — alasan: ............................

Disusun ......................  Diperiksa ....................
Tanggal ......................  Tanggal ......................
════════════════════════════════════════════════════════════════
```

---

## Aturan pengisian

**1. Satu besaran, satu kartu.** Jangan menggabung beberapa besaran — yang digabung akan
kehilangan jejak saat salah satunya dipersoalkan.

**2. Mata ③ — tandai tiap masukan.** Kolom `☐ terukur ☐ asumsi` yang membuat kartu ini
berguna. Masukan bertanda *asumsi* wajib punya baris kepekaan.

**3. Mata ④ — periksa peringatan R3.** Bila ambang berasal dari buku teks dan kontrak belum
mengadopsinya, **rantai putus**. Ini bukan kesalahan pengisi; ini temuan yang harus
disampaikan sebelum berita acara disusun, bukan sesudah.

**4. Status "menunggu" adalah status yang sah** — asalkan tanggal permintaannya tertulis.
Yang tidak sah adalah kartu berisi angka umum tanpa asal-usul.

**5. Kartu berstatus PUTUS tidak menghentikan pekerjaan.** Ia menentukan **cara menulis
berita acaranya**: hasil ukur dilaporkan, pernyataan lulus/tidak lulus ditangguhkan sampai
ambang ditetapkan. Lihat `rantai/D-pembumian-petir.md` untuk tiga jalan sah menutupnya.

---

## Contoh terisi — uji tahanan isolasi

```
BESARAN    : Ambang minimum tahanan isolasi, motor 600 V
NILAI      : 100 MΩ (setelah koreksi ke 20 °C)

① RUJUKAN  : [R2] ANSI/NETA ATS-2017, Tabel 100.1, PDF 223 · 2017
             peringatan usia: tidak

② KEPUTUSAN: kriteria penilaian = MΩ mutlak + rasio + tren
             ditolak: rasio saja — tidak menangkap isolasi yang
             seragam buruk sejak awal

③ HITUNGAN : nilai_terkoreksi = nilai_ukur × faktor(T)
             sumber rumus : [R2] Tabel 100.14, PDF 241
             nilai ukur   = 62 MΩ    [terukur]
             suhu         = 30 °C    [terukur]
             faktor       = Tabel 100.14  [R2]

④ UJI      : metode      : megger, 4 metode Gill PDF 142 [R3]
             AMBANG      : 100 MΩ
             sumber      : [R2] Tabel 100.1 — adopsi kontrak
                           tidak diperlukan, sumber R2
             tegangan uji : ≤75% V uji terima  [R3] Gill PDF 145

⑤ BUKTI    : BA-LIS-014 · lampiran: hasil ukur, suhu, sertifikat
             kalibrasi megger, tabel koreksi yang dipakai

STATUS     : ☑ UTUH
```

Perhatikan mata ④ pada contoh ini: karena ambangnya **R2**, tidak diperlukan adopsi kontrak.
Bandingkan dengan interval pemeliharaan pada rantai G — ambangnya R3, sehingga kotak
"diadopsi kontrak" **wajib** dicentang sebelum dinyatakan mengikat.
