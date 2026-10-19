# Status R4 — butir "menunggu data pabrikan" terhadap laci yang kini terisi

**Dibangun 20 Agustus 2026** setelah penyerapan 95 dokumen pabrikan dari mesin ini.

Laci `R4_OEM-TECHNICAL/` semula kosong **secara rancangan** — R4 melekat pada produk dan
diminta per proyek. Triase korpus menemukan dokumen produk yang **sudah ada di mesin ini**
tetapi belum pernah masuk rak.

| Laci | Berkas |
|---|---|
| `NETWORK/` | **28** |
| `SERVER-STORAGE/` | **18** |
| `CAMERA/` | **15** |
| `VMS-NVR/` | **6** |
| `UPS/` | **1** |
| `GENSET/` | **0** |
| `TEST-EQUIPMENT/` | **0** |
| `_PERLU-DIPERIKSA/` | **27** ⚠ belum boleh dikutip |

---

## Butir yang kini TERTUTUP

| Rantai | Butir yang dulu "menunggu R4" | Ditutup oleh |
|---|---|---|
| **C** — catu daya | **Efisiensi UPS** — Emadi (2004) tidak boleh dipakai | **Riello UPS General Catalogue**, 190 hal · `UPS/` |
| **B** — video | Bitrate, sensitivitas, batas kanal kamera | 15 lembar data kamera — PTZ 4K UH4500/4501/6200/7000/7100, UNV IPC2318, RP-PC464A1 dwi-spektrum + GNSS · `CAMERA/` |
| **F** — termografi | **NETD & IFOV kamera termal** | `LC014-56X-4MP-TH640-F75` (termal 640) · `CAMERA/` |
| **B/H** — VMS | Batas kanal & unjuk kerja server analitik | UNV Uniphues5732@PI · UNV UG-I500-H16 · Unicorn CS VMS · `VMS-NVR/` |
| **H** — jaringan | Kapasitas switch, PoE budget, PBX | 28 lembar data · `NETWORK/` |

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-7 (baris F-termografi di atas): 'TERTUTUP' di tabel ini berarti LEMBAR DATA sudah ada di laci `CAMERA/` - BUKAN angka NETD/IFOV sudah bisa dikutip. Nol nilai NETD/IFOV produk terekstraksi ke lapis teks mana pun (diukur pada giliran studi); kedua kandidat (`LC014-56X-4MP-TH640-F75`, `RP-PC464A1`) belum dibuka isinya. `AMBANG-TERIMA-INDUK.md` tetap mencantumkan butir ini sebagai wajib R4 tanpa catatan tertutup - kontradiksi status antar register (register K-7). Promosi 'tertutup' ke objek IL tanpa ekstraksi = angka hantu.

---

## Butir yang MASIH TERBUKA — tidak dapat ditutup dengan menyaring

| Rantai | Butir | Mengapa masih terbuka |
|---|---|---|
| **C** | **Faktor derating genset di lokasi** | `GENSET/` **kosong**. Tidak ada satu pun lembar data genset di mesin ini. Mahon [R3] hanya memberi kerangka |
| **C** | **DoD, umur siklus, kurva C-rate baterai** | Tidak ada lembar data baterai. Crompton (2000) [R3] tidak mewakili produk masa kini |
| **H** | **Unjuk kerja tulis & waktu rekonstruksi RAID** | Ada lembar data **SSD/NVMe** (Kingston NV3, Apacer industrial), **bukan pengendali RAID**. Keduanya berbeda — waktu rekonstruksi ditentukan pengendali |
| **A** | Redaman & reflektansi konektor terpasang | Tidak ada lembar data konektor/kabel serat |
| **A/E/D** | Spesifikasi alat uji (OTDR, OLTS, megger, earth tester) | `TEST-EQUIPMENT/` **kosong**. Dibutuhkan untuk kolom "ketelitian alat" pada berita acara |

**Kelimanya harus diminta ke pabrikan atau penyedia alat saat proyek berjalan.** Itu memang
cara kerja R4 — bukan kegagalan sistem.

---

## Peringatan pemakaian

> **Penempatan laci adalah tebakan mesin, bukan penetapan.** Berkas diklasifikasi dari nama
> dan daerah judul. Sebelum angka dari sebuah berkas masuk dokumen serah, **buka berkasnya**
> dan pastikan model serta versinya sama dengan yang benar-benar terpasang.

Dua kekeliruan yang sudah dikoreksi tangan pada putaran ini:

- **Corsair RM850e** (catu daya PC) sempat masuk `UPS/` — dipindah ke `SERVER-STORAGE/`.
  Catu daya ATX bukan UPS.
- **Honeywell Voyager 1472G** (pemindai kode batang) sempat masuk `UPS/` karena kata
  "battery" di manualnya — dipindah ke `_PERLU-DIPERIKSA/`.

Sebelum koreksi, laci `UPS/` berisi 14 berkas; **13 di antaranya bukan UPS.** Penyebabnya
pencocokan kata di seluruh isi halaman — kata "battery" pada manual telepon adalah
keterangan aksesori, bukan produknya. Alat kini menimbang kata di **daerah judul** tiga kali
lebih berat.

## Laci `_PERLU-DIPERIKSA/` — 27 berkas

Sebagian besar manual seri **KT-\*** dan **KC-\*** hasil pindaian **tanpa lapis teks**,
sehingga mesin tidak dapat membaca judulnya. Yang terbaca sebagian tampak sebagai perangkat
siar/AV — *video switcher*, *tally light*, *switchboard control panel*.

**Berstatus `INTAKE_ONLY`. Belum boleh dikutip.** Buka, tentukan lacinya, lalu pindahkan.
Bila ternyata di luar lingkup teknik GSP, hapus dari laci ini.

---

**Perkakas:** `90_TOOLS/triase_korpus.py` (pemindai) · `90_TOOLS/serap_r4.py` (penyerap).
Keduanya dapat dijalankan ulang kapan saja; duplikat dibuang otomatis berdasarkan sidik jari isi.
