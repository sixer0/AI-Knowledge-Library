# GSP EKAS — paket teks untuk model bahasa lokal

Engineering Knowledge & Assurance System milik PT Gemilang Satria Perkasa.
Dikemas 21 Agustus 2026.

## Apa isi paket ini

**Seluruh lapis teks** sistem: pengetahuan, register, rantai jaminan, kartu rujukan, resume
buku, templat, dan tata kelola.

**Yang TIDAK ikut: berkas PDF sumbernya** — 160 berkas, sekitar 3 GB. Paket ini berisi
**pengetahuan yang sudah diekstrak** dari PDF itu, lengkap dengan nomor halamannya.

Bila sebuah jawaban menuntut membuka halaman aslinya, **itu pekerjaan manusia**, bukan model.
Jalur berkasnya tertulis pada kolom `vault_path` di register.

---

## Aturan yang WAJIB diikuti saat memakai paket ini

### 1. Setiap angka membawa tingkat keyakinan sumbernya

| | Jenis | Boleh menetapkan ambang lulus/tidak lulus? |
|---|---|---|
| **R1** | Regulasi Indonesia / SNI | ✅ ya — mengikat secara hukum |
| **R2** | Standar internasional (IEC, IEEE, BS EN, ANSI/NETA) | ✅ ya bila diadopsi kontrak |
| **R3** | Buku teks / handbook | ⚠ **tidak sendirian** — hanya bila kontrak mengadopsinya tertulis |
| **R4** | Dokumentasi pabrikan (OEM) | ✅ **wajib** untuk angka yang melekat produk |
| **R5** | Tesis, makalah, panduan | ❌ **tidak pernah** — penunjuk saja |

**Sebaran rak ini: R1=0 · R2=4 · R3=49 · R4=6 · R5=3 baris register (160 berkas PDF).**

### 2. R1 kosong — dan itu menentukan banyak jawaban

**Tidak ada satu pun regulasi Indonesia di rak.** Setiap pertanyaan tentang kepatuhan
PUIL, SNI, UU ITE, atau Peraturan BSSN **harus dijawab "tidak ada di rak"**, bukan dijawab
dari pengetahuan umum.

### 3. Bentuk jawaban yang benar saat sumbernya tidak ada

> *"Ambang resistansi pembumian tidak tersedia di rak ini. Joffe & Lock [R3] memberi metode
> pengukurannya, bukan ambangnya. Ambang harus ditetapkan pemilik sistem secara tertulis
> atau diambil dari PUIL/SNI [R1] — yang belum ada di rak. Lihat GAP-001."*

**Yang dilarang:**

> ~~"Umumnya ambang resistansi pembumian adalah 5 Ω."~~

Kalimat kedua terdengar membantu dan justru paling berbahaya: ia terlihat seperti fakta,
tidak membawa sumber, dan akan disalin ke dokumen serah oleh orang yang tidak tahu asalnya.

### 4. Tiga rantai jaminan PUTUS — ambangnya tidak ada

| Rantai | Domain | Yang tidak ada |
|---|---|---|
| **D** | GROUNDING-LIGHTNING | Ambang resistansi pembumian |
| **J** | CYBERSECURITY | **Seluruh R1/R2** — UU ITE, Perban BSSN, ISO 27001, NIST SP 800-86, ISO 27037 |
| **K** | CIVIL-STRUCTURAL | Empat SNI struktur: 1726, 1727, 1729, 2847 |

Pada ketiganya **metode tersedia tetapi ambang tidak**. Menghitung boleh; menyatakan lulus
tidak.

> ⚠ **Rantai K punya batas tambahan:** struktur yang gagal dapat menimpa orang. Perhitungan
> yang menanggung keselamatan **wajib ditandatangani ahli bersertifikat** — rak ini membuat
> mampu memeriksa dan berdiskusi, bukan menggantikan tanda tangan itu.

### 5. Buku berbasis standar Amerika — metodenya boleh, angkanya tidak

Seluruh buku sipil, bangunan, dan sebagian kelistrikan berbasis **ASCE 7, AISC, ACI 318,
ASTM, IBC, NEC, NFPA, ASHRAE**. Padanan Indonesianya tidak ada di rak.

Contoh paling nyata: **tabel profil baja Segui adalah profil W/HP/HSS Amerika**, bukan
WF/H-beam SNI. Dimensinya berbeda — **tidak dapat dipakai langsung** meski terlihat mirip.

---

## Peta isi

| Map | Isi | Mulai dari sini bila… |
|---|---|---|
| [`00_START-HERE/`](00_START-HERE/) | README, peta sistem, kendali dokumen, riwayat, temuan uji coba | …baru pertama memakai |
| [`01_GOVERNANCE/`](01_GOVERNANCE/) | **R1–R5**, status otoritas, alur jaminan, **gate G0–G7**, kebijakan AI | …perlu tahu aturannya |
| [`02_REGISTERS/`](02_REGISTERS/) | Register rujukan · celah · enam register proyek | …mencari daftar |
| [`03_SOURCE-VAULT/`](03_SOURCE-VAULT/) | **Hanya `_ISI.md`** — manifest tiap laci; PDF-nya tidak ikut | …mencari letak berkas |
| [`04_KNOWLEDGE-CARDS/`](04_KNOWLEDGE-CARDS/) | **62 kartu** — satu per rujukan, memuat **batas pemakaian** | …ingin tahu bobot sebuah sumber |
| [`05_DOMAIN-KNOWLEDGE/`](05_DOMAIN-KNOWLEDGE/) | Resume buku + **12 rantai jaminan** | …mengerjakan proyek nyata |
| `06`–`09` | Map kerja proyek + **contoh P00** yang sudah dijalankan | …menyusun dokumen |
| [`10_TEMPLATES/`](10_TEMPLATES/) | TPL-00 … TPL-09 | …butuh bentuk isian |
| [`90_TOOLS/`](90_TOOLS/) | Perkakas — termasuk pemeriksa keutuhan | …ingin tahu apa yang dibangkitkan otomatis |

## Urutan membaca yang disarankan

1. [`01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md`](01_GOVERNANCE/REFERENCE-CONFIDENCE-LEVEL.md) — aturan R1–R5
2. [`01_GOVERNANCE/ASSURANCE-GATES.md`](01_GOVERNANCE/ASSURANCE-GATES.md) — gate G0–G7
3. [`02_REGISTERS/MASTER-REFERENCE-REGISTER.csv`](02_REGISTERS/MASTER-REFERENCE-REGISTER.csv) — daftar seluruh rujukan
4. `05_DOMAIN-KNOWLEDGE/<domain>/RANTAI-JAMINAN.md` — sesuai pekerjaan yang ditanyakan
5. `04_KNOWLEDGE-CARDS/<domain>/<REF-ID>.md` — batas pemakaian sebelum mengutip

## Rantai jaminan yang tersedia (12 dari 22 domain)

- **CIVIL-STRUCTURAL**
- **CYBERSECURITY**
- **ELECTRICAL**
- **FIBER-OPTIC**
- **GROUNDING-LIGHTNING**
- **NETWORKING**
- **POWER-BACKUP**
- **PROJECT-QUALITY**
- **RCM**
- **STORAGE**
- **THERMAL**
- **VIDEO-SURVEILLANCE**

Sepuluh domain lain **belum punya rantai** — bila pertanyaannya menyentuh domain itu,
nyatakan bahwa jalur dari rujukan ke bukti serah **belum disusun**.

## Berkas yang dibangkitkan otomatis — jangan disunting

- `04-daftar-rujukan-lengkap.md` (di skill) ← [`90_TOOLS/bangun_daftar_skill.py`](90_TOOLS/bangun_daftar_skill.py)
- `_ISI.md` tiap laci ← alat serap/migrasi
- `INTAKE-QUEUE.csv`, `INTAKE-RINGKAS.md` ← [`90_TOOLS/triase_korpus.py`](90_TOOLS/triase_korpus.py)

## Pemeriksa keutuhan

[`90_TOOLS/periksa_ekas.py`](90_TOOLS/periksa_ekas.py) memeriksa delapan hal dan keluar dengan kode 1 bila ada **GALAT**.
Keadaan saat pengemasan: **GALAT 0 · PERINGATAN 1**.
