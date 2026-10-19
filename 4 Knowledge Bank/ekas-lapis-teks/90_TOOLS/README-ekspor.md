# Pustaka Teknis GSP — Korpus Markdown

**Diekspor:** 19 Agustus 2026 · **Isi:** 55 berkas Markdown, ± 8.000 baris
**Sumber:** rak buku teknis PT Gemilang Satria Perkasa, `C:\Users\gspen\Videos\Buku`

Korpus ini adalah **sari pati 22 buku teknis (20.079 halaman)** beserta prosedur kerja yang
dibangun di atasnya. Ditujukan untuk dipakai model bahasa lokal saat mengerjakan tugas
teknis GSP tanpa akses ke berkas PDF aslinya.

---

## ⚠ Batasan yang harus dipahami lebih dulu

**Berkas PDF bukunya TIDAK disertakan dalam ekspor ini.**

Akibatnya:

| Hal | Status |
|---|---|
| Rumus, ambang, dan angka acuan | **Ada** — sudah digali dan diverifikasi |
| Rujukan halaman (mis. "PDF 240") | **Ada sebagai penunjuk**, tetapi **tidak dapat diverifikasi** dari korpus ini |
| Isi penuh buku | **Tidak ada** |
| Tabel yang berupa gambar di buku | **Tidak ada** — mis. Tabel 4.1 rolling sphere |

**Aturan pemakaian yang mengikuti:**

1. Rujukan halaman **tetap dikutip** dalam dokumen keluaran — supaya dapat diperiksa oleh
   orang yang memegang bukunya
2. Bila sebuah angka **tidak ada di korpus ini**, jangan mengarang. Periksa bagian
   "Yang tidak ada di rak" pada `00-inti/KATALOG-RUMUS.md` — kemungkinan besar memang
   tidak ada di bukunya juga, dan sumbernya sudah disebutkan di sana
3. Bila sebuah pertanyaan menuntut isi buku yang tidak diringkas di sini, **nyatakan bahwa
   berkas PDF-nya perlu dibuka** — jangan menebak isinya

---

## Susunan

```
00-inti/          Rumus, ambang, aturan kerja — dibaca lebih dulu
01-resume/        Sari pati 22 buku, satu berkas per buku
02-skill/         Prosedur kerja per domain (lima skill)
03-tata-kelola/   Celah koleksi, prosedur pemeliharaan rak, riwayat
```

### 00-inti — mulai dari sini

| Berkas | Isi |
|---|---|
| **KATALOG-RUMUS.md** | **Indeks pertanyaan → rumus → buku → halaman.** Pintu masuk utama |
| **ASUMSI-BAKU.md** | Cara memperlakukan data yang tidak tersedia; empat hal yang tidak boleh diasumsikan |
| **TEMPLATE-BERITA-ACARA.md** | Kerangka berita acara delapan jenis uji + tabel sumber ambang |

### 01-resume — sari pati per buku

22 berkas, dinamai `<folder rak> — <judul>.md`. Tiap resume memuat peta isi dengan nomor
halaman, bagian yang paling sering dipakai, tabel pemakaian di GSP, buku pendamping, dan
catatan mutu berkas.

**Dua belas di antaranya punya bagian "Perhitungan siap pakai"** berisi rumus, tabel nilai,
dan contoh terhitung.

### 02-skill — prosedur kerja

| Skill | Domain |
|---|---|
| `pustaka-teknis` | **Lapisan sumber** — cara memanggil angka berikut rujukannya |
| `rcm-analysis` | Keandalan: FMEA, konsekuensi, interval pemeliharaan |
| `fiber-link-design` | Serat optik: loss budget, uji, OTDR |
| `power-backup-sizing` | UPS, baterai, genset, interval uji |
| `grounding-lightning-design` | Pembumian dan proteksi petir |

Tiap skill: `SKILL.md` (mode, alur wajib, gerbang mutu) + berkas referensi.

### 03-tata-kelola

Peta celah koleksi, daftar pengadaan bahan, prosedur menambah buku, dan riwayat pengerjaan.
Diperlukan hanya bila pekerjaan menyangkut pemeliharaan rak, bukan pekerjaan teknis
sehari-hari.

---

## Cara memakai — routing berdasarkan tugas

| Tugas | Baca |
|---|---|
| Butuh satu angka atau rumus | `00-inti/KATALOG-RUMUS.md` → indeks cepat |
| Merancang sistem pengawasan video | `01-resume/CCTV VSS…` + `01-resume/Storage RAID NVR…` + `02-skill/pustaka-teknis/references/02-rantai-hitung-proyek.md` (rantai A) |
| Merancang jalur serat optik | `02-skill/fiber-link-design/` |
| Menentukan kapasitas UPS/baterai/genset | `02-skill/power-backup-sizing/` |
| Merancang pembumian atau proteksi petir | `02-skill/grounding-lightning-design/` |
| Menyusun program pemeliharaan | `02-skill/rcm-analysis/` |
| Menyusun berita acara uji | `00-inti/TEMPLATE-BERITA-ACARA.md` |
| Data pelanggan tidak lengkap | `00-inti/ASUMSI-BAKU.md` |
| Menelusuri gangguan jaringan | `01-resume/TCP IP…` + `01-resume/Network Troubleshooting…` |
| Menilai klaim produk analitik video | `01-resume/Video Analytics…` + `01-resume/CCTV VSS…` |

**Rantai hitung lintas buku** ada di
`02-skill/pustaka-teknis/references/02-rantai-hitung-proyek.md` — lima rantai: VSS, serat
optik, catu daya, pemeriksaan termal, dan program pemeliharaan. Ini yang menunjukkan **titik
serah antar-buku**, hal yang tidak terlihat bila resume dibaca satu per satu.

---

## Aturan kerja yang berlaku di seluruh korpus

Aturan ini bukan formalitas — inilah yang membuat keluaran dapat dipertahankan saat
diperiksa panitia atau auditor.

1. **Tiap angka teknis menyebut sumbernya.** Format: *(Damjanovski, CCTV: From Light to
   Pixels, PDF 240)*
2. **Jangan mengarang angka yang tidak ada.** Empat ambang yang sering diminta memang tidak
   ada di rak — ambang resistansi pembumian, ambang MΩ tahanan isolasi, ambang ΔT termal,
   dan standar instalasi listrik Indonesia. Semuanya tertulis di `KATALOG-RUMUS.md`
   beserta sumber yang seharusnya
3. **Bedakan rumus buku dari penyusunan sendiri.** Bila sebuah langkah disusun sendiri,
   tandai sebagai penyusunan, bukan kutipan
4. **Bawa peringatan usang.** Tujuh buku bertanda usang — angka dari buku itu perlu
   diperiksa terhadap sumber mutakhir sebelum masuk dokumen serah
5. **Nyatakan asumsi.** Nilai, dasar, sensitivitas, dan rencana penggantiannya
6. **Keputusan diambil dari kondisi terburuk**, bukan tipikal
7. **Urutan kerja tidak boleh dibalik** — ukur sebelum merancang, hitung sebelum menetapkan
   ambang

---

## Catatan cacat berkas yang perlu diketahui

| Buku | Cacat | Akibat |
|---|---|---|
| **Diesel Generator Handbook** | **Kehilangan ± 55 halaman** — Bab 11 "Emergency and standby" seluruhnya | Materi genset darurat **tidak tersedia**; perlu sumber lain |
| **CCTV (Damjanovski)** | Ligatur `fi` terbaca `¿` pada PDF asli | Hanya memengaruhi pencarian di PDF, bukan korpus ini |
| **Shigley** | Bookmark hanya sampai tingkat "Part" | Resumenya tidak memuat rujukan halaman — disengaja |

---

## Ringkasan angka

| | |
|---|---|
| Buku diringkas | 22 (20.079 halaman) |
| Resume | 22, seluruhnya berujukan halaman terverifikasi |
| Rujukan halaman | 342, seluruhnya diperiksa dalam jangkauan |
| Buku dengan rumus siap pakai | 12 |
| Contoh terhitung | 14, seluruhnya dihitung ulang — nihil meleset |
| Skill | 5 |
| Rantai hitung lintas buku | 5 |
| Jenis berita acara | 8 |

---

## Paket kedua: batch 2 saja

```bash
python "C:/Users/gspen/Videos/Buku/GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/90_TOOLS/buat_paket_batch2.py"
```

Menghasilkan `Pustaka-Teknis-GSP-Batch2.zip` — **12 berkas, 26 KB** — berisi hanya bahan
yang masuk 19 Agustus 2026: 4 standar, 2 tesis/panduan, 2 buku baru, 2 indeks koleksi
non-teknis, plus `README.md` dan `DELTA-SISTEM.md`.

**Kapan memakai yang mana:**

| Keperluan | Paket |
|---|---|
| Model lokal butuh seluruh rak | `Pustaka-Teknis-GSP-Markdown.zip` (induk, 63 berkas) |
| Meninjau *apa yang berubah* pada batch 2 | `Pustaka-Teknis-GSP-Batch2.zip` |

Isinya **tumpang tindih** — paket batch 2 bukan tambahan atas induk, melainkan irisannya.
Jangan memuat keduanya ke satu indeks; resume yang sama akan terhitung dua kali.

---

## Paket ketiga: Engineering Knowledge & Assurance System

```bash
python "C:/Users/gspen/Videos/Buku/GSP-ENGINEERING-KNOWLEDGE-ASSURANCE-SYSTEM/90_TOOLS/buat_paket_ekas.py"
```

Menghasilkan `Engineering-Knowledge-Assurance-System.zip` — **77 berkas, 236 KB**.
Seluruh rak (batch 1 + 2) disusun ulang menurut **rantai jaminan** dengan setiap sumber
bertanda **tingkat keyakinan R1–R5**.

| Keperluan | Paket |
|---|---|
| Model lokal — seluruh rak, susunan perpustakaan | `Pustaka-Teknis-GSP-Markdown.zip` (63 berkas) |
| Meninjau perubahan batch 2 saja | `Pustaka-Teknis-GSP-Batch2.zip` (12 berkas) |
| **Pekerjaan proyek — rujukan sampai bukti serah** | `Engineering-Knowledge-Assurance-System.zip` (77 berkas) |

**EKAS adalah superset paket induk** — memuat seluruh isinya plus 13 berkas sistem baru
(`00-sistem/` dan `01-rantai-jaminan/`). Untuk pemakaian baru, **pakai EKAS**; dua paket
lain dipertahankan supaya tautan lama tidak putus.

> ⚠ Berkas sistem EKAS berada di `_sistem/` pada rak, **bukan** di akar. Alat pembangkit
> paket induk (`buat_paket_markdown.py`) sengaja **tidak** memuatnya — bila keduanya dimuat
> ke satu indeks, rantai jaminan akan terbaca dua kali.
