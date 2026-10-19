# Ambang Terima Induk — beserta tingkat sumbernya

**Berkas ini yang mencegah ambang dikarang.** Tiap baris menyebut angkanya, sumbernya,
tingkat R-nya, dan apakah ia sah dipakai sebagai dasar lulus/tidak lulus.

Kolom **"sah?"** dibaca menurut aturan gate G4:
R1/R2 → sah · R3 → hanya bila kontrak mengadopsinya tertulis · R5 → tidak pernah.

---

## Sah tanpa syarat — bersumber R2

| Uji | Ambang | Sumber | R | Sah? |
|---|---|---|---|---|
| **Tahanan isolasi — MΩ mutlak** | Tabel 100.1: 600 V → **100 MΩ** · 5 kV → **1.500 MΩ** · 15 kV → **5.000 MΩ** | ANSI/NETA ATS-2017, PDF 223 | **R2** | ✅ |
| **Koreksi suhu hasil isolasi** | Tabel 100.14 → acuan **20 °C** | ANSI/NETA ATS-2017, PDF 241 | **R2** | ✅ |
| **Termografi — ΔT** | Tabel 100.18: **> 15 °C** antar komponen serupa · **> 40 °C** terhadap udara → perbaiki segera | ANSI/NETA ATS-2017, PDF 246 | **R2** | ✅ |
| **Kapasitas baterai VRLA** | **< 90%** rating pabrikan → ganti · turun **> 10%** dari uji sebelumnya → ganti · **85%** umur layan → uji tahunan wajib | IEEE 1188-2005, PDF 17 | **R2** | ✅ |
| **Pemeriksaan berkala baterai** | Triwulanan | IEEE 1188-2005, PDF 15 | **R2** | ✅ |
| **Ventilasi ruang baterai** | `Q = v × q × s × n × I_gas × C_rt × 10⁻³` m³/jam — **derating tidak diperbolehkan** | IEC 62485-2, PDF 21 | **R2** | ✅ |
| **Deteksi hilangnya sinyal video** | Tabel 7 per security grade: **8 / 4 / 2 detik** | BS EN 62676-1-2, PDF 34 | **R2** | ✅ |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1a..d + K-8 (baris Termografi di atas): baris ini hanya memuat satu dari empat tingkat tindakan Tabel 100.18, tanpa kualifikator 'panduan tindakan, bukan batas mutlak' dan tanpa syarat 'beban serupa' - keduanya wajib ikut dikutip (sumber primer: `ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92`; tabel utuh juga di `KATALOG-RUMUS.md` seksi 13.1). Batas cakupan: ambang ini milik ATS (uji terima); pemakaian untuk instalasi BERJALAN adalah wilayah MTS yang tidak ada di rak (baris 'Uji pemeliharaan listrik' di bagian Belum ada sumber sah; peringatan di bawah tabel ini) dan butuh putusan controller-manusia (register K-8). Centang ✅ berlaku untuk keberadaan angka di lapis teks, bukan keabsahan pakai lintas lingkup.

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2 (cacat propagasi, TINGGI - sasaran utama butir ini): baris 'Tahanan isolasi - MΩ mutlak' di atas disajikan dengan kolom 'Sah?' = centang TANPA syarat, padahal sumber R2-nya sendiri mensyaratkan nilai Tabel 100.1 berlaku 'bila tidak ada standar konsensus lain' dan spesifikasi pabrikan mendahuluinya (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`; caveat tercetak di `KATALOG-RUMUS.md:454`). Berkas ini adalah gerbang rilis yang dibaca gate G4 sebagai daftar ambang sah; centang R2 pada baris itu tidak mencakup syarat pemakaian tersebut, sehingga 100 MΩ diperlakukan mutlak. Klausul caveat wajib ikut naik ke objek IL dan ke setiap kutipan baris ini. Register: electrical-korpus-detail.md Bagian 5 K-2.
> **CATATAN DEFECT (VSSKB-0923, 2026-09-23):** baris Tabel 7 di atas berstatus known-defect. Lapisan teks korpus membawa DUA bentuk untuk tabel yang sama (deteksi 8/4/2 di lapis ini vs 8/4/4/2 di `R2 - BS EN 62676-1-2.md:45-48`), dan pemetaan per security grade BELUM TERKONFIRMASI terhadap geometri PDF primer (PDF 34 hanya merender TIGA nilai deteksi + DUA nilai durasi; ukur gsp-custodian 2026-09-23). Baris ini TIDAK sah berdiri sendiri sebagai ambang uji serah terima sampai rekonsiliasi dengan publikasi resmi BSI/IEC dilakukan manusia. Centang pada kolom terakhir berlaku untuk keberadaan angka di lapis teks, bukan keabsahan ambang. Blok penuh: `05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md` (CATATAN DEFECT) + `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'. Temuan awal: probe RBAC gspuser01 (verif/rbac/probe-rbac-3-gspuser01.md).


> ⚠ **Batas cakupan wajib dibaca** sebelum memakai baris di atas —
> `01_GOVERNANCE/AUTHORITY-STATUS.md`. Yang paling sering dilampaui: ATS dipakai untuk
> pekerjaan **pemeliharaan** (itu MTS), dan IEEE 1188 dipakai untuk baterai **vented**
> (itu IEEE 450).

---

## Sah — berasal dari hitungan rancangan

Ambang jenis ini tidak berasal dari standar mana pun; ia **hasil perhitungan** dan sah
karena metodenya dapat ditelusuri. Yang wajib: rincian hitungnya ikut dilampirkan.

| Uji | Ambang | Metode | R metode |
|---|---|---|---|
| **Rugi jalur serat optik** | Loss budget **kolom terburuk** | Hayes PDF 129, 145 | R3 |
| **Kerapatan piksel video** | Sasaran pemilik (FI 250 / FR 125 pix/m) | Damjanovski PDF 237–241 | R3 + pemilik |
| **Kapasitas rekaman & lebar pita** | Hasil hitung | Damjanovski PDF 277, 290 | R3 |
| **Kapasitas terpakai RAID** | `(n−1)×C` / `(n−2)×C` | Troppens PDF 46–70 | R3 |
| **kVA genset** | `(puncak ÷ PF) × derating × margin` | Mahon PDF 136 | R3 + **R4** |
| **Kapasitas baterai (Ah)** | `Ah = I × t ÷ DoD`, koreksi C-rate | Crompton PDF 104, 117 | R3 + **R4** |

> **Metode boleh R3.** Yang tidak boleh R3 adalah **angka lulus/tidak lulus** yang tidak
> dihitung — itu beda perkara.

---

## Perlu adopsi kontrak — bersumber R3

| Uji | Ambang | Sumber | R | Sah? |
|---|---|---|---|---|
| **Polarization Index** | **PI < 1** → selidiki | Gill PDF 144 | R3 | ⚠ adopsi kontrak |
| **Dielectric Absorption Ratio** | **DAR < 1,25** → selidiki | Gill PDF 144 | R3 | ⚠ adopsi kontrak |
| **Batas tegangan uji rutin** | ≤ **75%** V uji terima · ≤ **60%** V uji pabrik | Gill PDF 145 | R3 | ⚠ adopsi kontrak |
| **Mutu kabel referensi serat** | rugi **> 0,5 dB** patut dipertanyakan | Hayes | R3 | ⚠ adopsi kontrak |
| **Interval uji perangkat proteksi** | Hasil FFI | Moubray PDF 195, 198 | R3 | ⚠ adopsi kontrak |

Bentuk adopsi yang benar dalam dokumen:

> *"Ambang PI < 1 mengacu Gill (2008) sebagaimana diadopsi pasal … kontrak."*

Bukan: ~~"sesuai praktik industri"~~.

---

## ❌ Belum ada sumber sah

| Uji | Keadaan | Tiga jalan sah |
|---|---|---|
| **Resistansi pembumian** | **Tidak ada R1 maupun R2 di rak.** Joffe [R3] memberi metode, bukan ambang | ① pemilik menetapkan tertulis ② kontrak menyebut standar, peroleh salinannya ③ laporkan hasil ukur **tanpa pernyataan lulus** |
| **Interoperabilitas perangkat video** | ONVIF tidak ada di rak. BS EN 62676-1-2 mengatur **transmisi**, bukan ini | Peroleh dokumen ONVIF terpisah |
| **Kepatuhan instalasi listrik Indonesia** | PUIL/SNI tidak ada. ANSI/NETA **bukan penggantinya** | Peroleh PUIL/SNI |
| **Perkabelan terstruktur** | TIA-568 tidak ada | Peroleh TIA-568 |
| **Uji pemeliharaan listrik** | ANSI/NETA **MTS** tidak ada — yang ada ATS (uji terima) | Peroleh MTS |
| **Kapasitas baterai vented** | IEEE 450 tidak ada — IEEE 1188 hanya VRLA | Peroleh IEEE 450 |
| **Redaman serat multimode** | IEC 61280-4-1 tidak ada — yang ada 4-2 (singlemode) | Peroleh 61280-4-1, atau pakai OFSTP-14 [R3] dan nyatakan |

Seluruh baris ini terdaftar sebagai `GAP-*` di `02_REGISTERS/GAP-REGISTER.csv`.

---

## ❌ Wajib R4 — tidak ada penggantinya

Angka berikut **melekat pada produk** dan tidak dapat diambil dari buku mana pun:

faktor derating genset di lokasi · efisiensi UPS · DoD dan umur siklus baterai ·
kurva laju (C-rate) · unjuk kerja tulis pengendali RAID · waktu rekonstruksi RAID ·
NETD dan IFOV kamera termal · redaman & reflektansi konektor terpasang

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-7 (butir 'NETD dan IFOV kamera termal' di atas): konsisten dengan register lain bahwa butir ini WAJIB R4 dan angkanya BELUM PERNAH ada di lapis teks. `R4-STATUS.md` menulis butir F 'TERTUTUP' - artinya lembar data calon (`LC014-56X-4MP-TH640-F75`, `RP-PC464A1`) sudah masuk laci `CAMERA/`, BUKAN angka NETD/IFOV sudah bisa dikutip (0 nilai terekstraksi; register K-7). Aturan 'menunggu data pabrikan' di bawah tetap berlaku penuh untuk rantai F.

Bila lembar datanya belum ada, tulis **"menunggu data pabrikan"** dan tandai kartu
kendalinya `MENUNGGU R4`. Jangan diisi angka umum.

---

## Cara memakai berkas ini

1. Cari jenis ujinya di salah satu dari lima bagian di atas.
2. Salin **angka + sumber + halaman + tingkat R** ke prosedur uji (`TPL-03`).
3. Bila jatuh di bagian "perlu adopsi kontrak" — **periksa kontraknya dulu**, sebelum uji.
4. Bila jatuh di bagian "belum ada sumber sah" — **pilih satu dari tiga jalan** dan tulis
   pilihannya di berita acara.

**Ambang proyek yang berbeda dari tabel ini** (karena kontrak menetapkan lebih ketat)
ditulis di berkas terpisah dalam map ini, **tidak menimpa berkas induk**.
