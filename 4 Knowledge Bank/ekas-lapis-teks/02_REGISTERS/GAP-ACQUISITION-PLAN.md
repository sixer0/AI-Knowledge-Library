# Daftar Pengadaan Bahan — menutup celah rak

**Lokasi rak:** `C:\Users\gspen\Videos\Buku` · **Disusun:** 19 Agustus 2026

Prioritas 4 pada rencana kerja tidak dapat dikerjakan sekarang: **bahannya belum ada di
komputer ini.** Pemeriksaan pada 19 Agustus 2026 terhadap **507 berkas PDF** di Downloads,
Documents, Desktop, dan Videos tidak menemukan satu pun dari empat bahan yang dibutuhkan.

Berkas ini menetapkan **apa yang perlu diperoleh, mengapa, dan apa yang akan terbuka
begitu bahannya ada** — supaya pengadaannya terarah, bukan sekadar "cari buku standar".

Begitu satu bahan masuk, ikuti `PROSEDUR-TAMBAH-BUKU.md`.

---

## 🔄 Status setelah batch 2 (19 Agustus 2026, malam)

Tujuh puluh lima berkas masuk rak sore itu. **Tidak satu pun dari empat bahan di bawah
tertutup penuh**, tetapi dua celah **berkurang** dan beberapa celah lain **tertutup**:

| # | Bahan | Status | Keterangan |
|---|---|---|---|
| 1 | ONVIF | ⬜ **masih terbuka** | Yang masuk **BS EN 62676-1-2** — standar **transmisi** video, bukan interoperabilitas perangkat. Berguna, tetapi bukan pengganti ONVIF |
| 2 | PUIL / SNI | ⬜ **masih terbuka** | Yang masuk **ANSI/NETA ATS-2017** — standar Amerika. Menutup celah **ambang uji**, bukan celah **kepatuhan hukum Indonesia** |
| 3 | Penanganan bukti digital | 🟡 **sebagian** | Alsmadi (*NICE Framework*) memberi **proses empat tahap + rantai kustodi** (PDF 268). NIST SP 800-86 dan ISO/IEC 27037 tetap perlu — Alsmadi meringkas, bukan menormakan |
| 4 | ISO/IEC 27001 | ⬜ **masih terbuka** | Tesis di `R5/THESIS/` menyebut UU 11/2008 dan Perban BSSN 4/2021 — **rujukan sekunder**; regulasi aslinya tetap harus dikutip langsung |

**Celah yang tertutup penuh oleh batch 2** (tidak ada di daftar ini sebelumnya karena
dianggap prioritas menengah): ambang tahanan isolasi, faktor koreksi suhu, ambang ΔT
termografi, kriteria penggantian baterai, ventilasi ruang baterai, dan metode uji redaman
serat singlemode.

**Prioritas pengadaan tidak berubah.** Keempatnya tetap urut seperti semula — batch 2
mengurangi tekanan pada nomor 3, tidak menghapusnya.

**Yang bertambah ke daftar prioritas menengah:** **ANSI/NETA MTS** (uji *pemeliharaan*;
yang ada di rak ATS = uji *terima*) dan **IEEE 450** (uji baterai vented; IEEE 1188 hanya
VRLA).

---

## Urutan prioritas

| # | Bahan | Menutup celah | Mendesak karena |
|---|---|---|---|
| 1 | **Standar video atas IP (ONVIF)** | Interoperabilitas VSS | Muncul di hampir tiap spesifikasi tender VSS |
| 2 | **PUIL / SNI kelistrikan** | Kepatuhan hukum | Seluruh buku listrik di rak berbasis AS/Inggris |
| 3 | **Penanganan bukti digital** | Lini DEMS | Isi inti proposal penegak hukum, tanpa sandaran pustaka |
| 4 | **ISO/IEC 27001 & 27002** | Syarat tender | Sering diminta sebagai syarat atau nilai tambah |

Tiga teratas menutup celah yang **berulang muncul di dokumen yang sudah pernah disusun**,
bukan celah teoretis.

---

## 1. Standar video atas IP — ONVIF

**Yang dicari**

- **Spesifikasi profil ONVIF** — Profile S (streaming), Profile G (perekaman),
  Profile T (streaming lanjut, H.265), Profile M (metadata/analitik)
- Dokumen inti: *ONVIF Core Specification* dan *Profile Specification* per profil
- Sumber resmi: onvif.org — **tersedia bebas**, tidak perlu dibeli

**Mengapa mendesak**

Spesifikasi VSS untuk instansi hampir selalu menyebut profil ONVIF, dan pertanyaan
*"apakah perangkat A benar-benar bisa dipakai dengan VMS B"* muncul di hampir tiap proyek.
Saat ini hanya bisa dijawab dari dokumen vendor — yang berkepentingan.

Damjanovski membahas kompresi dan jaringan video, tetapi **tidak membahas interoperabilitas
sebagai standar**.

**Yang terbuka begitu ada**

- Resume ONVIF: peta profil, apa yang dijamin dan apa yang tidak
- Bagian pada `KATALOG-RUMUS.md`: fitur wajib per profil
- Jenis uji baru pada `TEMPLATE-BERITA-ACARA.md`: **uji interoperabilitas** — sekarang belum ada
- Kemungkinan skill `onvif-interop` bila lini kerjanya cukup sering

---

## 2. Standar instalasi listrik Indonesia — PUIL / SNI

**Yang dicari**

- **PUIL** (Persyaratan Umum Instalasi Listrik) — edisi berlaku
- SNI terkait pembumian dan proteksi petir, bila terpisah
- Sumber: BSN, atau penerbit resmi

**Mengapa mendesak — ini celah kepatuhan, bukan sekadar teknis**

Seluruh buku kelistrikan di rak berbasis **Amerika dan Inggris**: NEC, NFPA 70E, IEEE, BS.
Yang **mengikat secara hukum di Indonesia adalah PUIL**.

Untuk pekerjaan yang diserahkan ke instansi pemerintah, mengutip NFPA tanpa merujuk PUIL
adalah celah yang dapat dipermasalahkan pemeriksa — dan itu bukan soal mutu teknis,
melainkan keabsahan dokumen.

**Yang terbuka begitu ada**

- **Empat ambang yang sekarang bertanda ❌** pada `TEMPLATE-BERITA-ACARA.md` sebagian
  memperoleh sumbernya: ambang resistansi pembumian dan ambang tahanan isolasi
- `ASUMSI-BAKU.md`: beberapa asumsi berubah menjadi ketentuan
- Resume PUIL yang memetakan pasal ke pekerjaan GSP
- Rujukan silang dari resume Gill dan Joffe: mana yang dipakai untuk apa

---

## 3. Penanganan bukti digital

**Yang dicari**

- **NIST SP 800-86** — *Guide to Integrating Forensic Techniques into Incident Response*
  (tersedia bebas dari NIST)
- **ISO/IEC 27037** — pedoman identifikasi, pengumpulan, dan pengawetan bukti digital
- Pelengkap: ISO/IEC 27041, 27042, 27043

**Mengapa mendesak**

GSP mengerjakan sistem manajemen bukti digital untuk penegak hukum. Rantai kustodi,
integritas bukti, dan keterterimaan di pengadilan adalah **isi inti proposalnya** — dan
saat ini **tidak punya sandaran pustaka di rak sendiri**.

Anderson (*Security Engineering*) membahas keamanan sistem dan integritas catatan secara
umum, tetapi tidak membahas penanganan bukti sebagai prosedur.

**Yang terbuka begitu ada**

- Resume yang memetakan tahapan penanganan bukti ke rancangan sistem
- Sandaran untuk skill `digital-forensics-evidence-system` dan
  `dems-polri-proposal-architect` yang sudah terpasang — keduanya kini bekerja tanpa
  rujukan pustaka di mesin ini
- Jenis uji baru: **verifikasi integritas dan rantai kustodi**

---

## 4. ISO/IEC 27001 dan 27002

**Yang dicari**

- **ISO/IEC 27001** — persyaratan sistem manajemen keamanan informasi
- **ISO/IEC 27002** — panduan kendali

**Mengapa perlu**

Sering diminta sebagai syarat atau nilai tambah pada tender instansi. Tanpa rujukan, bagian
SMKI pada proposal disusun dari pengetahuan umum.

**Yang terbuka begitu ada**

- Resume yang memetakan kendali ke pekerjaan GSP
- Rujukan silang dengan Anderson (kerangka berpikir) dan Limoncelli (praktik operasional)

---

## Prioritas menengah — dicatat, belum mendesak

| Bahan | Menutup |
|---|---|
| **TIA-568** | Perkabelan terstruktur |
| **TIA-942** | Perancangan pusat data |
| Buku keamanan perimeter (sensor pagar, radar, fusi sensor) | Perimeter di luar kamera |
| Buku infrastruktur AI/ML produksi (penyajian model, GPU) | Menjalankan analitik di produksi |
| Buku manajemen proyek teknis | Tidak terwakili sama sekali |

---

## Bukan pengadaan bahan baru — memperbaiki yang ada

**Diesel Generator Handbook (Mahon, 2004)** — berkas di rak **kehilangan ± 55 halaman**:
Bab 11 *"Emergency and standby"* seluruhnya dan awal Bab 12.

Bab 11 justru yang paling relevan untuk pekerjaan genset cadangan. **Perlu salinan
pengganti yang utuh**, bukan buku baru. Penanda sudah dipasang di daftar isi berkas dan
tercatat di resume serta `power-backup-sizing`.

---

## Yang harus dilakukan saat bahan tiba

1. Ikuti `PROSEDUR-TAMBAH-BUKU.md` dari Langkah 0
2. Perbarui berkas ini — coret yang sudah tertutup
3. Perbarui `PETA-CELAH-KOLEKSI.md`
4. Perbarui `TEMPLATE-BERITA-ACARA.md` bila bahan itu memberi dasar ambang terima —
   terutama untuk empat baris yang sekarang bertanda ❌

> **Catatan cara pengadaan.** ONVIF dan NIST SP 800-86 tersedia bebas dari sumber resminya.
> PUIL dan ISO/IEC berbayar melalui penerbit resmi (BSN, ISO). Pengadaannya di luar
> jangkauan pekerjaan teknis ini — daftar ini menetapkan **apa** dan **mengapa**, bukan
> **dari mana memperolehnya**.
