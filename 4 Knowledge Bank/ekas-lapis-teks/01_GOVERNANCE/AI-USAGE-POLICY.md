# Kebijakan Pemakaian Model Bahasa dalam EKAS

Model bahasa dipakai di sistem ini. Kebijakan ini menetapkan **apa yang boleh
dikerjakannya** dan **apa yang tetap harus dikerjakan manusia** — supaya kecepatan tidak
ditukar dengan angka yang tidak dapat dipertahankan.

---

## Prinsip

> **Model boleh menyusun, menelusuri, dan mengingatkan. Model tidak boleh menjadi sumber.**

Tidak ada angka teknis dalam dokumen GSP yang boleh bersandar pada pengetahuan model.
Setiap angka bersandar pada berkas di `03_SOURCE-VAULT/` beserta halamannya.

---

## Boleh

| Pekerjaan | Catatan |
|---|---|
| Menemukan rujukan dan halaman yang relevan | Hasilnya **diverifikasi manusia** dengan membuka halamannya |
| Menyusun draf keputusan desain, prosedur uji, berita acara | Dari templat di `10_TEMPLATES/` |
| Menghitung dengan rumus yang **sudah ada sumbernya** | Rumus dari katalog, bukan dari ingatan model |
| Memeriksa kelengkapan — gate mana yang belum tertutup | Sangat berguna; model jarang lupa butir |
| Menemukan ketidakkonsistenan antar-dokumen | Mis. angka berbeda di dua berkas |
| Merangkum sumber yang sudah dibaca | |
| Menandai berkas yang menjadi basi setelah sumber baru masuk | |

## Tidak boleh

| Larangan | Alasan |
|---|---|
| **Mengisi angka yang tidak ada di rak** | Angka tanpa sumber tidak dapat dipertahankan |
| **Menetapkan ambang terima** | Ambang berasal dari R1/R2/kontrak, bukan dari model |
| **Menaksir angka produk** (derating, efisiensi, DoD, unjuk kerja) | Wajib R4 |
| **Menyatakan kepatuhan regulasi** | Rak tidak memiliki R1 |
| **Menyimpulkan dari sumber `INTAKE_ONLY`** | Sumber yang belum dinilai tidak boleh masuk rantai |
| **Menjadi pemeriksa kedua pada gate G3** | Verifikasi hitungan menuntut tanggung jawab manusia |
| **Menandatangani atau menyetujui apa pun** | |

---

## Aturan penandaan

Setiap angka yang masuk dokumen membawa **dua penanda**:

```
[R2, ANSI/NETA ATS-2017, Tabel 100.1, PDF 223]   ← tingkat + letak
SOURCE-DERIVED                                     ← cara diperoleh
```

Empat cara diperoleh:

| Tanda | Arti |
|---|---|
| `SOURCE-DERIVED` | Langsung dari R1/R2/R3 dengan kutipan halaman |
| `OEM-DERIVED` | Dari R4, terkait model dan versi tertentu |
| `PROJECT-DERIVED` | Hasil hitung dari masukan proyek, metodenya dapat ditelusuri |
| `ASSUMPTION` | Belum terbukti — **wajib** ada sensitivitas dan rencana penggantian |

**`ASSUMPTION` tidak boleh menjadi ambang terima final** tanpa persetujuan tertulis.

---

## Bila model tidak menemukan sumbernya

Jawaban yang benar adalah **"tidak ada di rak"**, bukan angka dari pengetahuan umum.

Bentuk jawaban yang diharapkan:

> *"Ambang resistansi pembumian tidak tersedia di rak ini. Joffe & Lock [R3] memberi metode
> pengukurannya, bukan ambangnya. Ambang harus ditetapkan pemilik sistem secara tertulis
> atau diambil dari PUIL/SNI [R1] — yang belum ada di rak. Lihat GAP-001."*

Bentuk yang **dilarang**:

> ~~"Umumnya ambang resistansi pembumian adalah 5 Ω."~~

Kalimat kedua terdengar membantu dan justru paling berbahaya: ia terlihat seperti fakta,
tidak membawa sumber, dan akan disalin ke dokumen serah oleh orang yang tidak tahu asalnya.

---

## Konflik antar-sumber

Bila dua sumber berbeda, **model tidak memilih diam-diam.** Konflik dicatat di
`06_ENGINEERING/DESIGN-DECISIONS/` memakai `TPL-01` bagian 5, lalu diputuskan manusia.

Urutan yang dipakai bila keputusan harus diambil:

1. Kontrak yang sah + **R1** yang berlaku — tidak boleh dilanggar
2. **R2** untuk metode dan ambang, sesuai lingkupnya
3. **R4** untuk parameter, kompatibilitas, dan batas keselamatan produk aktual
4. **R3** untuk metode rekayasa dan penalaran
5. **R5** untuk menemukan sumber primernya

---

## Yang wajib diperiksa manusia, tanpa kecuali

1. **Nomor halaman.** Model dapat menyebut halaman yang keliru; halaman keliru dalam
   berita acara adalah cacat yang langsung terlihat.
2. **Satuan.** MΩ terhadap Ω, dB terhadap dBm, Ah terhadap Wh.
3. **Lingkup standar.** ATS terhadap MTS, VRLA terhadap vented, singlemode terhadap
   multimode, transmisi terhadap interoperabilitas.
4. **Hitungan pada gate G3.** Mata kedua harus manusia.
5. **Setiap pernyataan kepatuhan.**

---

## Catatan tentang riwayat sistem ini

Register EKAS pernah memuat **tujuh tahun terbit yang keliru** — termasuk satu salah
penulis — karena disusun dari ingatan alih-alih dari berkasnya. Ketahuan saat dicocokkan
dengan daftar berkas sebenarnya.

Kejadian itu tidak dicatat di sini sebagai catatan sejarah, melainkan sebagai alasan
mengapa **poin 1 dan 5 di atas tidak dapat ditawar.** Kesalahan seperti itu tidak terlihat
dari dalam dokumen; ia hanya terlihat ketika dibandingkan dengan sumbernya.
