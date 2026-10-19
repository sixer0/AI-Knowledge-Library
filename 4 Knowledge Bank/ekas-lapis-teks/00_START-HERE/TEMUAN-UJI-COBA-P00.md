# Temuan uji coba P00 — apa yang terungkap saat perangkat gate benar-benar dipakai

**21 Agustus 2026.** Satu lingkup kecil — jalur serat optik 3,2 km, 8 core — dijalankan
melewati **G0 sampai G6** memakai seluruh perangkat: kartu kendali, tujuh templat, enam
register, dan rantai **A**.

Sampai hari ini semuanya belum pernah dipakai sekali pun. Uji coba ini yang pertama.

> **Contoh sengaja tidak diselesaikan sampai "semua centang hijau".** Menjalankan sampai
> mulus tidak mengungkap apa pun. Yang berguna justru melihat bagaimana **gate yang belum
> terpenuhi terlihat pada berkas** — dan bahwa pekerjaan tetap boleh berjalan asalkan
> statusnya tertulis.

---

## Lima temuan

### 1. ⭐ Gate G4 bergantung pada G3, dan itu tidak pernah dinyatakan

Ambang uji rugi sisipan **berasal dari hitungan anggaran rugi**. Artinya ITP tidak dapat
disetujui sebelum hitungannya diperiksa orang kedua.

`ASSURANCE-GATES.md` menyusun gate **berurutan** tetapi tidak menyebut bahwa **G4 tidak
dapat ditutup selama G3 terbuka** bila ambangnya berasal dari hitungan sendiri.

Ini bukan urusan teori. Pada uji coba, prasyarat ketiga ITP-P00 tertulis *"CALC sudah
diperiksa orang kedua — **belum**"*, dan itu **memblokir dua butir uji** yang paling penting.

**Diperbaiki:** aturan ketergantungan ditambahkan ke `ASSURANCE-GATES.md`.

### 2. Dua templat yang dituntut gate ternyata tidak ada

| Yang dituntut | Di mana dituntut | Ada templatnya? |
|---|---|---|
| **ITP** — Inspection & Test Plan | Gate G4 · map `07_.../ITP/` | ❌ **tidak ada** |
| **NCR** — laporan ketidaksesuaian | Gate G5 · map `07_.../NON-CONFORMANCE/` | ❌ **tidak ada** |

Keduanya punya map dan disebut gate, tetapi **tidak ada `TPL` untuk mengisinya**. Pada uji
coba, ITP-P00 terpaksa disusun dari nol.

**Diperbaiki:** `TPL-08-ITP.md` dan `TPL-09-NCR.md` dibuat.

### 3. `TPL-02` tidak menampung hasil yang lebih dari satu

Anggaran rugi menghasilkan **dua ambang** — 6,40 dB pada 1310 nm dan 5,96 dB pada 1550 nm —
karena rugi serat berbeda menurut panjang gelombang.

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: ambang 5,96 dB @1550 yang dikutip di lapis ini TIDAK reproducible dari masukan CALC-P00-001.md:31-36. Alpha tersirat 5,96 tepat = 0,3625 dB/km (tidak muncul di FOA/rantai/katalog/kartu); kandidat rak memberi 5,60 dB (a=0,25), 5,76 dB (a=0,3), 6,40 dB (a=0,5); brute force 1.120 kombinasi menuntut n_sambungan 8/10 (bertentangan n=6 di DDR-P00-001.md:19) atau rugi konektor 0,5/1,0 (bukan 0,75). Rincian uji: register Bagian 2.3 dan K-2. Induk anotasi: CALC-P00-001.md:48. Nilai P00 berlabel 'angka karangan' (contoh); tidak ada dokumen serah nyata yang tercemar. Keputusan koreksi (5,76 / 6,40 / catatan ilustrasi-tanpa-rincian) milik controller-manusia.

`TPL-02` hanya punya satu baris **Hasil**. Ini bukan kasus khusus: hampir setiap besaran
teknis punya lebih dari satu kondisi — suhu berbeda, beban berbeda, panjang gelombang
berbeda.

**Diperbaiki:** `TPL-02` diberi tabel hasil per kondisi.

### 4. Penomoran dokumen tidak konsisten

`DOCUMENT-CONTROL.md` memberi contoh `BA-FO-014` — **tanpa nomor proyek** — sementara
seluruh awalan lain memakainya (`CALC-P25-007`). Pada uji coba saya menulis `BA-P00-FO-001`
karena tanpa nomor proyek berita acara tidak dapat dibedakan antar-proyek.

**Diperbaiki:** contoh pada `DOCUMENT-CONTROL.md` diselaraskan menjadi `BA-P25-FO-014`.

### 5. Kartu kendali dan lembar perhitungan saling menyalin

`KARTU-P00-001` mengulang rumus, masukan, kepekaan, dan sumber ambang yang sudah ada di
`CALC-P00-001`. Sekitar **60% isinya salinan**.

**Belum diperbaiki — ini keputusan, bukan cacat.** Dua pilihan:

| Pilihan | Untung | Rugi |
|---|---|---|
| **Pertahankan** | Kartu dapat dibaca sendiri saat dilampirkan ke BA; pemeriksa tidak perlu membuka CALC | Pengisian ganda, dan **dua salinan dapat menyimpang** |
| **Ramping** — kartu hanya menunjuk `CALC-ID` | Sekali tulis | Pemeriksa harus membuka dua berkas |

Saran: **pertahankan, tetapi kartu dibangkitkan dari CALC**, bukan diketik ulang. Belum ada
alatnya.

---

## Yang ternyata bekerja baik

**Penandaan masukan `SOURCE-DERIVED` / `ASSUMPTION` langsung berguna.** Pada CALC-P00-001,
satu-satunya masukan bertanda `ASSUMPTION` — rugi sambungan 0,3 dB — otomatis memunculkan
kolom kepekaan, dan kepekaan itu menunjukkan hal yang tidak terduga: **rugi konektor
menyumbang 3,00 dB dari 6,40 dB**, hampir separuh anggaran hanya dari empat konektor.
Tanpa penandaan, perhatian akan tertuju ke sambungan yang jumlahnya lebih banyak.

**Matriks ketertelusuran `TPL-06` memberi angka yang tidak dapat dinegosiasikan.**
Tujuh dari tujuh baris kolom `EVIDENCE-ID`-nya kosong — pekerjaan belum dilaksanakan.
Tidak ada ruang untuk menyatakan "hampir selesai".

**Pemeriksaan tingkat pada G4 menangkap hal nyata.** Ambang berasal dari hitungan bermetode
R3; karena kontrak pasal 7.3 mengadopsi IEC 61280-4-2, ambangnya sah. Tanpa pasal itu,
rantai akan putus — dan kotak centang pada `TPL-03` memaksa hal itu diperiksa.

---

## Yang tidak terungkap dan perlu uji coba berikutnya

Uji coba berhenti di **G6** karena tidak ada bukti mentah — pekerjaannya tidak nyata.
Akibatnya dua register tetap kosong:

| Register | Mengapa kosong |
|---|---|
| `EVIDENCE-REGISTER.csv` | Bukti baru ada setelah uji dilaksanakan |
| `ASSET-REFERENCE-REGISTER.csv` | Aset baru terdaftar menjelang serah |

**Keduanya hanya dapat diuji pada pekerjaan sungguhan.** Sampai itu terjadi, bagian G5–G7
dari perangkat ini masih belum terbukti.

---

## Berkas uji coba

| Gate | Berkas |
|---|---|
| G1 | `06_ENGINEERING/REQUIREMENTS/REQ-P00-CONTOH.md` |
| G2 | `06_ENGINEERING/DESIGN-DECISIONS/DDR-P00-001.md` |
| G3 | `06_ENGINEERING/CALCULATIONS/CALC-P00-001.md` ⚠ terbuka · `KARTU-P00-001.md` |
| G4 | `07_.../ITP/ITP-P00.md` · `07_.../TEST-PROCEDURES/TEST-P00-001.md` |
| G6 | `09_HANDOVER/BERITA-ACARA/BA-P00-FO-001.md` · `TPL-06-P00-KETERTELUSURAN.md` |

**Kode `P00` dicadangkan untuk contoh.** Proyek sungguhan memakai `P25`, `P26`, dan
seterusnya. Setiap berkas P00 diawali kotak peringatan bahwa angkanya karangan.
