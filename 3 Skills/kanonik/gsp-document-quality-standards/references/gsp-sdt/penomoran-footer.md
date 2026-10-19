# Penomoran, Register & Kepala-Kaki - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §1.4 (C-11..C-17), §1.6 (C-21..C-22), §2.1, §2.4, §5.2.
> Pemilik paket: `gsp-document-quality-standards`; kanal lain pointer.

## 1. Identitas & register dokumen

- **C-11** - Kode dokumen berpola `GSP-SDT[-XXX]-nnn`; XXX = kode rezim: (kosong)=umum,
  `SDTP`, `SDTP-AD`, `SDTP-AU`, `PL`, `CY`, `BIZ`; nnn = nomor urut tiga digit.
- **C-12** - Nomor register `NNN/GSP/KODE/BULAN_ROMAWI/TAHUN` mengikuti Register Induk PT GSP.
  Nomor ketujuh dokumen sistem berstatus **provisional sampai disahkan pada Register Induk
  (ARSIP)** - jangan dikutip sebagai nomor final. Contoh sah: `028/GSP/STD/VIII/2026`.
- **C-13** - Klausul/subklausul desimal maksimum **tiga tingkat** (`6.1`, `6.1.1`); nomor tidak
  pernah dilewati atau dipakai ulang antar revisi.
- **C-14** - Gambar & tabel bernomor **per klausul**: `Gambar k.n`, `Tabel k.n`; setiap
  gambar/tabel **wajib membawa baris SUMBER** yang menyebut asal datanya.
- **C-15** - Setiap kebutuhan diberi `REQ-Kx-nnn` unik sepanjang umur dokumen dan tertaut sampai
  metode verifikasinya.
- Kunci khas rezim (§2.4): PL `BB-nnn` + SHA-256 (barang bukti, selaras KUHAP); CY
  `FND-Kx-nnn (CVSS · ATT&CK)` contoh `FND-K1-007 · 8.8 · T1190`; BIZ `LI-nnn (BOQ)` contoh
  `LI-014 · BOQ-3.2`.

## 2. Pola nomor lembar per rezim (C-16) - WAJIB persis

| Rezim | Pola nomor halaman/lembar | Catatan |
|---|---|---|
| SDT-001 umum (R-1) | `n / mm` (contoh footer `1 / 07`; sumber tercetak R-1 memakai em-dash, dirender '/' per D17) | halaman utuh |
| SDTP pertahanan (R-2) | `SHEET nn OF mm` (dua digit) | wajib tiap lembar, termasuk lembar identifikasi |
| AD (R-3) | `LEMBAR n DARI m` | |
| AU (R-4) | `HAL nn / mm` | T mencakup uji darat & uji terbang |
| PL (R-5) | `HLM n / mm` | Klausul 6.1 hanya menyebut "halaman bernomor utuh"; pakai pola footer PDF yang terbukti |
| CY (R-6) | `n / mm` | footer PDF `n / 06` |
| BIZ (R-7) | `n / mm` | footer PDF `n / 06` |

**C-17** - Tabel/gambar tidak boleh dipenggal antar lembar tanpa penanda lanjutan
("bersambung"). Pada HTML aturan ini jadi aturan pagination print.

## 3. Kepala-kaki terkendali (C-22)

```text
HEADER: <KODE DOKUMEN> · <JUDUL DOKUMEN> · <KLASIFIKASI>
FOOTER: PT GEMILANG SATRIA PERKASA | <KLASIFIKASI> · Terkendali | <NOMOR LEMBAR REZIM>
```

Klasifikasi tercetak pada **kepala, kaki, dan sampul** setiap lembar terkendali (C-08).

## 4. Format minimum (C-21)

Kal penutup Tabel 8.1 di ketujuh dokumen: *"Ketentuan ini adalah bentuk minimum; dokumen boleh
lebih ketat, tidak boleh lebih longgar."* A4 tegak di semua rezim; margin per rezim (mm,
atas/bawah/kiri/kanan): R-1 24/24/22/26, R-2 22/18/22/20, R-3 22/18/22/20, R-4 22/18/22/20,
R-5/R-6/R-7 23/22/21/24. Bingkai: R-2 navy, R-3 ganda hijau, R-4 azure; lainnya tanpa bingkai.
Logo: **dilarang** di R-2/R-3/R-4 (identitas = pita komando + tipografi).

Nilai palet & huruf per rezim tinggal di §2.1 SPEC-DOC dan paket token DS
(`gsp-design-system-grill/references/master-design/`) - **jangan disalin ke sini** (D-TA-7.1).

## 5. Pengendalian revisi (C-24)

Revisi huruf kapital berurut (`Rev A`, `Rev B`, …); baris terbaru di **puncak**; baris lama
tidak pernah diubah/dihapus; pengecualian terhadap acuan dicatat sebagai baris revisi tersendiri.
Tabel riwayat: `Rev | Tanggal | Perubahan | Oleh`.

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
