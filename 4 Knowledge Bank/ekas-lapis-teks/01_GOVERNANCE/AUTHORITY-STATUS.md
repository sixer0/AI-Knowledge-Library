# Status Otoritas Sumber

Tingkat **R1–R5** menyatakan *kelas penerbitnya*. **Status otoritas** menyatakan *apakah
sumber itu boleh dipakai sekarang, dan sejauh mana*. Dua hal berbeda: sumber R2 bisa
berstatus `SUPERSEDED`, dan sumber R3 bisa berstatus `ACTIVE` penuh.

---

## Enam status

| Status | Arti | Boleh dipakai? |
|---|---|---|
| `ACTIVE` | Berlaku penuh dalam lingkupnya | ✅ |
| `ACTIVE_WITH_SCOPE_LIMITS` | Berlaku, **tetapi ada hal di luar cakupannya yang sering disangka tercakup** | ✅ — batasnya wajib dibaca |
| `POINTER_ONLY` | Hanya penunjuk ke sumber primer | ⚠ bukan sandaran |
| `INTAKE_ONLY` | Sudah masuk rak, **belum diresume dan belum dinilai** | ❌ belum boleh |
| `SUPERSEDED` | Digantikan edisi atau dokumen lebih baru | ❌ arsip |
| `WITHDRAWN` | Ditarik karena keliru | ❌ |

---

## Yang berstatus `ACTIVE_WITH_SCOPE_LIMITS`

Kelima sumber R2 di rak ini **seluruhnya** berstatus terbatas. Bukan karena mutunya rendah,
melainkan karena masing-masing punya batas cakupan yang mudah dilampaui tanpa sadar.

| Sumber | Berlaku untuk | **TIDAK** berlaku untuk |
|---|---|---|
| **ANSI/NETA ATS-2017** | Uji **terima** instalasi baru | Uji **pemeliharaan** → itu MTS, tidak ada di rak |
| **ANSI/NETA ATS-2017** | Ambang **tahanan isolasi** (MΩ) | Ambang **resistansi pembumian** (Ω) — besaran berbeda |
| **ANSI/NETA ATS-2017** | Praktik Amerika | **Kepatuhan hukum Indonesia** — bukan pengganti PUIL |
| **IEEE 1188-2005** | Baterai **VRLA** | Baterai **vented** → itu IEEE 450, tidak ada di rak |
| **IEC 62485-2:2010** | Keselamatan & ventilasi baterai stasioner | Penentuan kapasitas |
| **BS EN 62676-1-2:2014** | **Transmisi** video | **Interoperabilitas perangkat** → itu ONVIF, tidak ada di rak |
| **IEC 61280-4-2:2014** | Serat **singlemode** terpasang | **Multimode** → itu IEC 61280-4-1, tidak ada di rak |
| **IEC 61280-4-2:2014** | *Cara mengukur* | *Berapa batasnya* — ambang tetap dari hitungan rancangan |

> **Empat baris pertama tabel ini adalah kesalahan yang paling mudah terjadi** dan paling
> mudah terlihat oleh pemeriksa: menyebut NETA sebagai dasar ambang pembumian, atau menyebut
> ATS pada pekerjaan pemeliharaan.

---

## Yang berstatus `POINTER_ONLY`

| Sumber | Menunjuk ke | Yang harus dikutip |
|---|---|---|
| Tesis Ayubi Wirara (2021) | **UU 11/2008 (ITE)** | Pasal UU-nya — R1 |
| Tesis Ivan Bashofi (2023) | **Peraturan BSSN No. 4/2021** | Perban-nya — R1 |
| Bundel panduan `_panduan/` | NIST SP 800-50r1 · advisori ASD-CISA · Joint CSI | **Dokumen aslinya masing-masing** |

> ### Catatan tentang bundel `_panduan`
> Empat berkas dinilai bersama sebagai satu rujukan R5, karena salah satunya majalah.
> **Akibatnya NIST SP 800-50r1 ikut turun ke R5** padahal terbitan federal AS yang layak
> dinilai sendiri — kemungkinan R2.
>
> **Selama belum dipecah:** bila mengutip isi dari NIST/ASD/CISA, **rujuk dokumen aslinya
> secara terpisah**, jangan mengutip bundelnya. Pemecahan tercatat sebagai butir terbuka di
> `00_START-HERE/DOCUMENT-CONTROL.md`.

---

## Yang berstatus `INTAKE_ONLY`

| Isi | Jumlah | Alasan |
|---|---|---|
| Makalah IEEE di `_koleksi-lain/Makalah IEEE/` | 21 | Terindeks, belum diresume per judul |
| Koleksi kuantum & kriptografi | 13 | Di luar lini kerja teknis GSP |
| Koleksi sejarah militer & geopolitik | 25 | Non-teknis |

**Sistem sengaja tidak mengarang pemetaan desain/hitungan/uji/bukti untuk sumber
`INTAKE_ONLY`.** Sumber yang belum dibaca tidak boleh muncul dalam rantai jaminan seolah
sudah dinilai.

Empat makalah IEEE ditandai berpotensi relevan — forensik otomotif, forensik VxWorks,
deteksi deepfake, ransomware ATT&CK — tetapi **penanda relevansi bukan penilaian**.

---

## Yang berstatus `SUPERSEDED`

| Sumber | Digantikan | Lokasi |
|---|---|---|
| CCNA 200-301 Official Cert Guide (2019) | Edisi 2024 | `Networking/_arsip/` |
| Berkas pra-OCR RCM II dan FOA Reference Guide | Versi ter-OCR | `_asli/` masing-masing |

Arsip **tidak dihapus**. Ia menjawab pertanyaan "dulu angkanya berapa".

---

## Peringatan usia — berlaku pada R2 dan R3

Usia **tidak mengubah status**, tetapi mewajibkan peringatan menyertai kutipan.

| Umur | Perlakuan |
|---|---|
| < 5 tahun | Apa adanya |
| 5–15 tahun | Periksa apakah ada edisi lebih baru **bila menyangkut angka batas** |
| > 15 tahun | Dipakai untuk **prinsip dan metode**; **angka batas dan rujukan standarnya wajib diperiksa ulang** |

Yang melewati 15 tahun di rak ini: Moubray (1997), Crompton (2000), Emadi (2004),
Mahon (2004), Uman (2008), Gill (2008), Troppens (2009), Nyman & Levitt (2010),
Donahue (2011), dan **IEEE 1188-2005** — satu-satunya R2 yang terkena.

> IEEE 1188 tetap dipakai luas dan kriterianya masih menjadi acuan. Tetapi sebelum
> dijadikan **ambang mengikat dalam kontrak baru**, periksa apakah sudah ada revisinya.

---

## Cara mengubah status

Perubahan status **wajib lewat** `10_TEMPLATES/TPL-07-SOURCE-UPDATE-REQUEST.md`, tidak
disunting langsung. Alasannya: perubahan status merambat ke kartu pengetahuan, rantai
jaminan, kriteria terima, dan berkas rujukan skill di luar EKAS. Templat itu memuat daftar
periksa rambatannya.
