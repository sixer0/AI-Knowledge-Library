# Rantai D — Pembumian dan proteksi petir

## ⚠ RANTAI INI PUTUS DI MATA ④

**Tidak ada sumber sah untuk ambang resistansi pembumian di rak ini.**
Diterbitkan dalam keadaan putus **dengan sengaja**, supaya kelemahannya terlihat sebelum
dipakai — bukan setelah dipersoalkan pemeriksa.

---

## ① Rujukan

| Sumber | Tingkat | Memasok | Halaman |
|---|---|---|---|
| Joffe & Lock, *Grounds for Grounding* (2023) | **R3** | Wenner, fall-of-potential, bonding, daftar periksa verifikasi | PDF 562, 579–580, 1111, 1149 |
| Uman, *The Art and Science of Lightning Protection* (2008) | **R3** ⚠18 th | Rolling sphere, tingkat proteksi | PDF 89–90 |
| **PUIL / SNI pembumian** | **R1** | **Ambang resistansi yang mengikat** | ❌ **TIDAK ADA** |
| **SNI / IEC 62305 edisi berlaku** | **R1/R2** | Tingkat proteksi petir yang mengikat | ❌ **TIDAK ADA** — Uman mengutip edisi **2006**, sudah usang |
| Persyaratan pemilik sistem | — | Ambang yang disepakati | per proyek |

---

## ② Keputusan desain

| Yang ditetapkan | Dasar | Alternatif yang ditolak |
|---|---|---|
| Konfigurasi elektroda (batang / mesh / ring) | Profil resistivitas tanah dari mata ③ | Menambah batang tanpa survei ditolak — bila lapisan dalam justru lebih resistif, penambahan tidak menurunkan apa pun |
| Skema bonding | Kebutuhan ekipotensial | Pembumian terpisah per subsistem **ditolak** — menciptakan beda potensial |
| Tingkat proteksi petir & radius bola gelinding | Penilaian risiko | Level IV (60 m) sebagai pilihan baku ditolak tanpa penilaian risiko |
| Proteksi surja internal | Kerentanan perangkat | Proteksi eksternal saja **ditolak** — kerusakan berulang setelah petir umumnya berasal dari ketiadaan proteksi internal |
| **Ambang resistansi yang dituju** | ⚠ **Harus ditetapkan pemilik atau standar mengikat** | Angka "< 5 Ω" tanpa sumber **ditolak** |

> **Urutan kerja yang benar** [R3, Joffe PDF 562]: survei tanah **dahulu**, baru
> konfigurasi. Merancang elektroda sebelum mengetahui profil resistivitas adalah menebak.

---

## ③ Perhitungan

### Resistivitas tanah — metode Wenner [R3, Joffe PDF 579–580]

```
ρ = 2 π a R
```

`a` = jarak antar-elektroda (m) · `R` = resistansi terbaca alat (Ω) · `ρ` dalam Ω·m

Ukur pada **beberapa nilai `a`** — tiap `a` menyelidiki kedalaman berbeda, sehingga
menghasilkan **profil**, bukan satu angka. Profil itu yang menentukan apakah elektroda
dalam bermanfaat.

### Rolling sphere — [R3, Uman PDF 89–90]

| Tingkat proteksi | Radius bola |
|---|---|
| Level IV | **60 m** |
| Level I–III | Tabel 4.1 — tersimpan sebagai **gambar tabel**, buka PDF 89–90 langsung |

⚠ **Peringatan mesh** [R3, PDF 90]: ukuran mesh bukan pengganti analisis bola gelinding.

---

## ④ Pengujian — ⚠ MATA YANG PUTUS

| Butir | Ketentuan | Sumber ambang |
|---|---|---|
| **Metode ukur resistansi terpasang** | Fall-of-potential (tiga pasak) | ✅ R3 — Joffe PDF 580 |
| **Prasyarat wajib** | **Konduktor penghubung dilepas dari elektroda sebelum diukur** | ✅ R3 |
| **Ambang lulus resistansi** | ❌ **TIDAK ADA SUMBER SAH DI RAK** | **PUIL/SNI [R1] atau persyaratan pemilik tertulis** |
| Verifikasi bonding & ekipotensial | Daftar periksa Apendiks G | ✅ R3 — PDF 1111 |
| Verifikasi zona lindung petir | Terhadap rancangan bola gelinding | ✅ R3, ⚠ edisi standar usang |

> ### Prasyarat yang paling sering dilewat
> **Konduktor penghubung harus dilepas dari elektroda bumi sebelum diukur.** Bila tidak,
> yang terukur adalah **gabungan seluruh sistem** — termasuk jalur balik lewat netral, pipa,
> dan baja bangunan. Angkanya akan terlihat bagus tetapi **tidak sah dijadikan dasar berita
> acara**, dan baru ketahuan saat terjadi gangguan.

### ⚠ Jangan tertukar

Rak ini **punya** ambang **tahanan isolasi** dari ANSI/NETA ATS-2017 [R2]. Itu **bukan**
ambang **resistansi pembumian**. Dua besaran berbeda:

| | Tahanan isolasi | Resistansi pembumian |
|---|---|---|
| Mengukur | Mutu isolasi antar-konduktor | Hubungan elektroda ke massa bumi |
| Satuan lazim | MΩ (juta ohm) | Ω (satuan ohm) |
| Sumber ambang | ✅ **NETA Tabel 100.1 [R2]** | ❌ **belum ada** |

Menukar keduanya menghasilkan berita acara yang menyebut standar yang tidak mengatur hal
yang diuji — kesalahan yang langsung terlihat oleh pemeriksa yang paham.

---

## ⑤ Bukti serah

| Lampiran | Wajib | Catatan |
|---|---|---|
| Berita acara uji pembumian | ✅ | Kerangka bagian 2 |
| Data survei Wenner: `a`, `R`, `ρ` per titik | ✅ | Profil, bukan satu angka |
| Konfigurasi terpasang: jenis, jumlah, kedalaman elektroda | ✅ | Sesuai penomoran gambar |
| **Pernyataan konduktor penghubung telah dilepas** | ✅ | Satu baris yang menentukan keabsahan seluruh hasil |
| Sertifikat kalibrasi alat | ✅ | — |
| **Ambang yang dipakai + SUMBERNYA** | ✅ | ⚠ **Bila belum ditetapkan pemilik, tulis begitu** |
| Daftar periksa Apendiks G | ✅ | Dapat dipakai apa adanya — PDF 1111 |
| Isi dokumentasi menurut Apendiks H | ✅ | Daftar isi dokumen serah — PDF 1149 |
| Kartu kendali rantai | ✅ | **Status: putus di mata ④** sampai ambang ditetapkan |

---

## Cara menutup rantai ini pada pekerjaan nyata

Selama R1 belum ada di rak, tersedia **tiga jalan sah** — pilih satu dan nyatakan:

1. **Pemilik sistem menetapkan ambang secara tertulis.** Paling cepat. Cantumkan surat
   penetapannya sebagai lampiran berita acara.
2. **Kontrak menyebut standar tertentu.** Peroleh salinannya, kutip pasalnya. Ambang naik
   menjadi R1 atau R2.
3. **Nyatakan hasil ukur tanpa pernyataan lulus/tidak lulus** — berita acara memuat angka
   terukur dan metode, dengan catatan bahwa penilaian menunggu penetapan ambang.

Yang **tidak** sah: mengisi "< 5 Ω" karena angka itu sering terdengar. Angka tanpa sumber
tidak dapat dipertahankan, dan pada pekerjaan pembumian ia justru mudah dipersoalkan karena
setiap pemeriksa berpengalaman tahu angkanya bergantung kebutuhan sistem.

**Penutupan celah ini ada di urutan kedua `DAFTAR-PENGADAAN-BAHAN.md` — PUIL/SNI.**
