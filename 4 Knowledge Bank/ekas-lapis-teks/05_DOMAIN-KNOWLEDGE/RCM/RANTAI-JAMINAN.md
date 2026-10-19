# Rantai G — Keandalan dan program pemeliharaan

**Ambang berasal dari:** hitungan RCM [R3] + **sasaran risiko yang ditetapkan pemilik** ·
menjadi mengikat hanya melalui **adopsi kontrak**

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Moubray, *RCM II* (1997) | **R3** ⚠29 th | Tujuh pertanyaan, P-F, FFI, konsekuensi, pola kegagalan | PDF 31, 164, 166, 193, 195, 198 |
| Gulati, *Maintenance & Reliability Best Practices* (2021) | **R3** | Tata kelola, KPI, organisasi | — |
| Nyman & Levitt, *Maintenance Planning* (2010) | **R3** ⚠16 th | Perencanaan dan penjadwalan kerja | — |
| Riwayat kegagalan aset pelanggan | — | MTBF nyata | ❌ **per proyek — sering tidak tersedia** |
| Lembar data & manual pabrikan | **R4** | Interval yang disyaratkan garansi | per proyek |

> Usia RCM II tidak menurunkan bobotnya — metodologinya masih menjadi acuan lintas industri.
> Yang perlu diwaspadai adalah **contoh dan konteks industrinya**, bukan penalarannya.

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| **Konteks operasi** | Wajib ditetapkan **pertama** | Menyalin program dari proyek lain **ditolak** — fungsi yang sama pada konteks berbeda menghasilkan tugas berbeda |
| Fungsi + standar unjuk kerja **terukur** | Kesepakatan dengan pemilik | "Berfungsi dengan baik" **ditolak** — tidak dapat diuji |
| Klasifikasi konsekuensi | Keselamatan · lingkungan · operasi · biaya · **tersembunyi** | Memperlakukan semua kegagalan sama **ditolak** |
| Jenis tugas | On-condition → restorasi → pembuangan → failure-finding | Overhaul berkala sebagai pilihan baku **ditolak** — **89% moda kegagalan tidak terkait umur** [R3 PDF 31] |
| **Sasaran MTBF kegagalan majemuk** | ⚠ **Keputusan pemilik** — menyatakan risiko yang bersedia ditanggung | Ditetapkan perancang **ditolak** |

> **Penemuan yang paling sering mengubah keputusan:** 89% moda kegagalan **tidak terkait
> umur**. Artinya penggantian berkala berdasarkan jam operasi seringkali **tidak menurunkan
> kegagalan sama sekali** — hanya menambah biaya dan memasukkan kegagalan dini akibat
> pekerjaan pemasangan.

---

## ③ Perhitungan

### Interval pemeriksaan on-condition — [R3, Moubray PDF 164]

```
interval = ½ × interval P-F
```

**Syarat kelayakan tugas** [PDF 166]:

```
nett P-F > waktu yang dibutuhkan untuk bertindak
```

Bila tidak terpenuhi, tugas on-condition **tidak layak** — sekalipun secara teknis dapat
dilakukan. Mendeteksi kegagalan yang tidak sempat ditindaklanjuti tidak menghasilkan apa pun.

### Interval failure-finding — bentuk sederhana [R3, PDF 195]

```
FFI = 2 × ketaktersediaan_yang_diizinkan × MTBF_perangkat
```

### Interval failure-finding — bentuk lengkap [R3, PDF 198] — **lebih baik dipakai**

```
        2 × M_perangkat × M_terproteksi
FFI = ──────────────────────────────────
              M_kegagalan_majemuk
```

Bentuk lengkap bertolak dari **sasaran risiko**, bukan dari ketersediaan perangkat — sehingga
angkanya dapat dipertanggungjawabkan kepada pemilik: *"interval ini menghasilkan kegagalan
majemuk sekali per N tahun, sesuai sasaran yang Bapak/Ibu tetapkan."*

### Contoh terhitung

Lihat rantai C — genset standby, FFI ≈ 18 hari.

---

## ④ Pengujian dan verifikasi

Domain ini berbeda dari yang lain: yang "diuji" bukan perangkat keras, melainkan
**keputusan pemeliharaan**.

| Butir | Kriteria | Sumber |
|---|---|---|
| Konteks operasi tertulis sebelum analisis | Ada / tidak ada | R3 |
| Standar unjuk kerja **terukur** | Dapat diuji dengan alat / pengamatan | R3 |
| Tiap moda kegagalan punya konsekuensi terklasifikasi | Lengkap | R3 |
| Tiap tugas **layak secara teknis dan berharga** | Dua uji terpisah — Decision Diagram | R3 |
| Uraian tugas **dapat dikerjakan orang lapangan** | Terbaca sebagai perintah kerja | R3 |
| Interval berasal dari hitungan, bukan kebiasaan | Ada perhitungannya | R3 |
| **Sasaran kegagalan majemuk disetujui pemilik** | Tertulis | ⚠ pemilik |
| Tugas failure-finding punya **proteksi pengganti** saat pelaksanaan | Ada / tidak | R3 — PDF 193 |

> **Titik kritis pada mata ini:** hasil analisis RCM menjadi **kewajiban kontraktual** hanya
> bila kontrak mengadopsinya. Interval yang dihitung dari Moubray [R3] tidak dengan
> sendirinya mengikat siapa pun. Bila GSP terikat memenuhi interval itu, ia harus **tertulis
> dalam kontrak** — dengan angkanya, bukan dengan menyebut "sesuai RCM".

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| **Information Worksheet** | ✅ | Fungsi → kegagalan fungsional → moda → akibat |
| **Decision Worksheet** | ✅ | Konsekuensi → tugas → interval |
| Pernyataan konteks operasi | ✅ | Yang membuat hasilnya sah hanya untuk sistem ini |
| **Sasaran kegagalan majemuk yang disetujui pemilik** | ✅ | Tertulis, bertanda tangan |
| Perhitungan interval per tugas | ✅ | Beserta masukan MTBF dan asal-usulnya |
| Daftar asumsi bertanda | ✅ | MTBF yang belum ada datanya — lihat `ASUMSI-BAKU.md` |
| **Rencana penggantian asumsi dengan data nyata** | ✅ | Kapan ditinjau ulang, dari log apa |
| Uraian tugas siap pakai | ✅ | Termasuk langkah pengembalian ke keadaan siaga |
| Kartu kendali rantai | ✅ | Tandai tiap MTBF yang masih asumsi |

**Status rantai: UTUH sebagai metode, BERGANTUNG PEMILIK pada sasaran risiko, dan
MENUNGGU ADOPSI KONTRAK untuk menjadi mengikat.**

Tiga hal itu harus dinyatakan bersama. Program pemeliharaan yang diserahkan tanpa
menyebutkan bahwa intervalnya berdiri di atas **asumsi MTBF** dan **sasaran risiko yang
belum disetujui** adalah dokumen yang terlihat kuat tetapi tidak bertahan saat pertama kali
dipersoalkan.
