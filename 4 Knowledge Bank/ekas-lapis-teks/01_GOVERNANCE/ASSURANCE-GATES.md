# Gate Jaminan G0 – G7

Gate adalah **titik yang tidak boleh dilewati** tanpa syaratnya terpenuhi. Bukan tahap
laporan; bukan formalitas administrasi. Sebuah butir pekerjaan yang melewati gate tanpa
syaratnya **akan gagal di gate berikutnya** — hanya lebih mahal.

---

## Delapan gate

### G0 — Sumber tervalidasi

**Syarat:** judul, edisi, tahun, dan halaman sumber dapat ditelusuri. Tingkat R ditetapkan.
Status otoritas ditetapkan.

**Gagal bila:** rujukan disebut tanpa edisi, atau halamannya tidak dapat dibuka.

> Gate ini yang paling sering dianggap sepele. Kutipan "menurut IEC 62305" tanpa nomor
> edisi tidak dapat diverifikasi — dan edisi 2006 yang dikutip Uman **sudah usang**.

---

### G1 — Kebutuhan dibekukan

**Syarat:** kebutuhan proyek tertulis dan disetujui. **Keputusan yang milik pemilik sudah
diambil pemilik** — secara tertulis.

**Empat hal yang harus ditetapkan pemilik, bukan perancang:**

| Hal | Mengapa |
|---|---|
| Sasaran MTBF kegagalan majemuk | Menyatakan risiko yang bersedia ditanggung |
| Sasaran pengamatan video (FI/FR) | Menentukan biaya dan kemampuan sistem secara mendasar |
| Ambang resistansi pembumian | Berasal dari standar atau persyaratan pemilik |
| Resistivitas tanah | Harus diukur — tidak ada penggantinya |

**Gagal bila:** perancang mengisi salah satunya diam-diam. Seluruh biaya sistem kemudian
berdiri di atas angka yang tidak pernah disetujui siapa pun.

---

### G2 — Desain disetujui

**Syarat:** tiap keputusan punya catatan (`TPL-01`) berisi rujukan, alasan, dan
**alternatif yang ditolak beserta alasan penolakannya**.

**Gagal bila:** kolom alternatif kosong. Keputusan tanpa alternatif tidak dapat dinilai —
tidak ada yang bisa diperiksa selain selera perancangnya.

---

### G3 — Perhitungan diverifikasi

**Syarat:**
1. Rumus punya sumber bertingkat.
2. **Tiap masukan bertanda** `SOURCE-DERIVED` / `PROJECT-DERIVED` / `OEM-DERIVED` /
   `ASSUMPTION`.
3. Tiap `ASSUMPTION` punya **sensitivitas** dan **rencana penggantian data**.
4. **Diperiksa orang kedua.**

**Gagal bila:** ada masukan tanpa tanda, atau hanya satu orang yang pernah melihat
hitungannya.

> Butir 4 bukan birokrasi. Kesalahan hitung yang paling merugikan bukan rumus yang salah,
> melainkan **satuan yang tertukar** — dan itu hampir selalu tertangkap oleh mata kedua.

---

### G4 — Metode uji ditetapkan

**Syarat:** metode, alat, jumlah sampel, dan **ambang beserta sumbernya** disetujui
sebelum uji dimulai.

**Pemeriksaan tingkat wajib di gate ini:**

```
Ambang bersumber R1 atau R2  →  sah
Ambang bersumber R3          →  HANYA sah bila kontrak mengadopsinya tertulis
Ambang bersumber R5          →  tidak sah
Ambang belum ditetapkan      →  uji tetap boleh jalan, TETAPI hasil dilaporkan
                                tanpa pernyataan lulus/tidak lulus
```

**Gagal bila:** ambang ditetapkan setelah hasil ukur keluar. Itu bukan pengujian — itu
penyesuaian.

---

### G5 — Uji lulus dengan bukti mentah

**Syarat:** hasil memenuhi ambang G4, **dan** bukti mentahnya tersimpan: bacaan alat,
kondisi uji, kalibrasi yang **masih berlaku pada tanggal uji**, dan penyaksi.

**Gagal bila:** hanya ada ringkasan hasil tanpa bukti mentah, atau kalibrasi alat sudah
kedaluwarsa saat pengukuran dilakukan.

---

### G6 — Bukti serah lengkap

**Syarat:** daftar periksa `TPL-05` terpenuhi seluruhnya, termasuk dua baris yang paling
sering hilang:

- **Daftar asumsi yang masih terbuka**
- **Daftar butir yang masih menunggu data OEM [R4]**

**Gagal bila:** paket terlihat lengkap tetapi menyembunyikan asumsi. Pekerjaan boleh
diserahkan dengan asumsi terbuka — **asalkan tertulis.** Yang tidak boleh adalah asumsi
yang tidak terlihat.

---

### G7 — Diterima

**Syarat:** pemberi kerja atau penyaksi menyetujui hasil secara tertulis.

---

## Aturan yang mengikat seluruh gate

**1. Gate tidak boleh dilompati.**
Tidak ada jalan dari **rujukan langsung ke ambang terima**. G1 sampai G5 harus dilalui.

**2. Gate boleh ditutup dengan status "menunggu" — asalkan tertulis.**
Butir yang menunggu surat pabrikan [R4] dapat melewati G3 dengan tanda `ASSUMPTION` +
sensitivitas, selama tanggal permintaannya tercatat. Yang tidak sah adalah angka umum
tanpa asal-usul.

**3. G4 tidak dapat ditutup selama G3 terbuka — bila ambangnya berasal dari hitungan sendiri.**
Ini ketergantungan yang tidak terlihat dari urutan gate. Bila ambang uji **dihitung**
(anggaran rugi serat, kapasitas RAID, kVA genset), maka ITP **tidak dapat disetujui**
sebelum hitungan itu diperiksa orang kedua — ambang yang belum diverifikasi bukan ambang.

Ambang yang berasal dari **R1/R2** tidak terkena aturan ini: ia sudah sah sejak G0.

**4. Mundurnya satu gate menarik mundur seluruh gate sesudahnya.**
Bila sumber berubah status (misalnya edisi standar diganti), G0 terbuka kembali — dan
seluruh butir yang bersandar padanya harus ditinjau ulang sampai G7.

Hal yang sama berlaku bila **NCR menemukan bahwa ambangnya yang keliru**: yang dibuka
kembali adalah G3, bukan pekerjaan yang dibongkar. Lihat `TPL-09` bagian 3.

---

## Kaitan dengan rantai jaminan

| Mata rantai | Gate |
|---|---|
| ① Rujukan | G0 |
| ② Keputusan desain | G1, G2 |
| ③ Perhitungan | G3 |
| ④ Pengujian | G4, G5 |
| ⑤ Bukti serah | G6, G7 |

Rincian tiap mata: [`ASSURANCE-WORKFLOW.md`](ASSURANCE-WORKFLOW.md)
Rantai lengkap per domain: `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md`

---

## Contoh: rantai yang sengaja berhenti di G4

**Uji pembumian.** Rak ini tidak memiliki sumber sah untuk ambang resistansi pembumian —
tidak R1, tidak R2. Karena itu rantai D **tidak dapat melewati G4** dengan cara biasa.

Tiga jalan sah:

1. **Pemilik menetapkan ambang tertulis** → G4 terbuka, surat penetapan jadi lampiran.
2. **Kontrak menyebut standar tertentu** → peroleh salinannya, ambang naik ke R1/R2.
3. **Laporkan hasil ukur tanpa pernyataan lulus** → G5 dan G6 tetap dapat dilewati; yang
   ditangguhkan hanya penilaiannya.

Yang **tidak** sah: mengisi "< 5 Ω" karena angka itu sering terdengar.

---

## Contoh kedua: rantai yang putus lebih luas

**Keamanan siber (rantai J).** Berbeda dari pembumian yang kehilangan **satu** ambang,
domain ini **tidak punya satu pun sumber R1 atau R2** — UU ITE, Perban BSSN, ISO/IEC 27001,
NIST SP 800-86, ISO/IEC 27037, seluruhnya tidak ada di rak.

Akibatnya tiga hal **tidak dapat diuji sama sekali**: kepatuhan ISO 27001, kriteria audit
BSSN, dan keterterimaan bukti di pengadilan.

**Yang tetap boleh dilakukan:** menjalankan pekerjaan dengan kerangka R3 (proses forensik
empat tahap Alsmadi, integritas jejak audit Anderson) dan panduan R5 — **asalkan gate G6
memuat pernyataan batas kepatuhan** yang menyebut standar mana yang belum dapat dibuktikan.

**Yang tidak boleh:** menuliskan "sesuai ISO/IEC 27001" dalam proposal tanpa memiliki
salinan standarnya. Itu menjanjikan sesuatu yang GSP sendiri tidak dapat memeriksanya.
