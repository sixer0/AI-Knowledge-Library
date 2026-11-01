---
title: "Standar Organisasi Information Library GSP (v1.1.0)"
type: standar
status: active
created: 2026-08-25
updated: 2026-10-31
writer: brahma
editor: pemelihara-pustaka
version: 1.1.0
domain: library
project: information-library
tags: [standar, organisasi, information-library, struktur, gsp]
kelas_bukti: sintesis
---

# Standar Organisasi Information Library GSP (v1.1.0)

> Dokumen hidup. Kanonik: `docs/standards/01_ORGANIZATION-STANDARD.md`.
> Pasangan wajib: `02_METADATA-STANDARD.md` (metadata), `03_LIBRARIAN-DAILY-PROCEDURE.md` (runbook harian),
> `04_DAILY-TASK-PROMPT.md` (prompt dispatch harian). Revisi standar: bump `version`, tulis
> `updated` + `editor`, catat riwayat di bagian bawah.

## 1. Tujuan

Standar ini menetapkan dua kewajiban:

1. **Antarmuka Information Library (IL) mudah ditelusuri.** Setiap entri memiliki judul yang jelas, tipe yang benar, dan keterangan sumber yang terstruktur.
2. **Ruang kerja tertata.** Setiap berkas berada di folder yang tepat, memakai nama sesuai konvensi, memiliki metadata lengkap, dan dapat dilacak sepanjang siklus hidupnya.

Standar ini berlaku untuk **semua** lapisan IL: wiki (terbit), vault (staging), dan workspace (RAW).
Siapa pun yang menulis/memindahkan/mengubah artefak IL wajib mematuhinya.

## 2. Prinsip jangka panjang

| # | Prinsip | Arti operasional |
|---|---------|------------------|
| P1 | **Struktur di atas kecepatan** | Folder & nama menjelaskan isi. Penelusuran manusia didahulukan daripada kecepatan menulis. |
| P2 | **Satu sumber kebenaran** | Pengetahuan kanonik ada di wiki (sudah disahkan); draft di docs; usulan di vault. Tidak ada duplikat kanonik. |
| P3 | **Perubahan selalu tercatat** | Setiap perubahan (pemindahan, penggantian nama, atau penyuntingan metadata) dicatat di `CHANGES.md` pelaksanaan harian. Tidak ada penghapusan. |
| P4 | **Konservatif** | Jika ragu, jangan ubah berkas. Tandai di laporan sebagai `flagged` agar dapat diputuskan oleh manusia atau pada pelaksanaan berikutnya. |
| P5 | **Path stabil** | Path yang dirujuk dokumen lain tidak berubah tanpa migrasi tercatat (old → new di CHANGES.md). |
| P6 | **Data berkala dan pengetahuan** | Data berkala (log, snapshot, artefak tugas) memakai tanggal di nama & tidak di-versioning semver. Pengetahuan yang tetap berguna naik ke wiki. |

## 3. Topologi IL (3 tingkat)

```
WIKI   C:/Users/TRIAL/AppData/Local/hermes/wiki          → pengetahuan terbit, kanonik, di-attest (DB HermesMemory via bridge)
VAULT  <ws>/vault/<perkara>/<YYYY-MM-DD>_<slug>.md       → staging/usulan, siapa pun boleh usul
RAW    <ws> = C:/Users/TRIAL/workspace/gsp-hermes/workspace → data kerja
```

- **Wiki**: ditulis **hanya** lewat `vault_promote.py` (gateway librarian). Struktur folder: `<type>s/<slug>.md`
  (`catatans/`, `faktas/`, `keputusans/`, `pelajarans/`, `proyeks/`, `standars/`). Taksonomi tipe: `catatan,
  fakta, keputusan, pelajaran, proyek, standar` (+ tipe vault `vendor, produk, dosir` bila terbit).
- **Vault**: tidak diubah oleh pelaksanaan harian kecuali kurasi basi (lihat 03). Format objek: `gsp-library-data-standards`.
- **RAW**: zona + aturan (subbab 4-5).

## 4. Struktur RAW (shared workspace)

```
<ws>/
├── AGENTS.md                     [PROTEKSI — jangan dipindah/diubah run harian]
├── MEMORY.md                     [PROTEKSI]
├── memory/                       [time-series: YYYY-MM-DD_log_<slug>.md, refs/, tasks/ — isi jangan diubah run harian]
├── docs/                         [dokumen kerja — area utama organisasi]
│   ├── standards/                [standar hidup 01-04 ini]
│   ├── 00_INDEX/                 [indeks & katalog kurasi: katalog-skill, bagan, peta, matrix]
│   ├── 01_DOMAIN/<domain>/       [pengetahuan per domain of expertise — lihat registry §6]
│   ├── 02_PROJECT/<project>/     [artefak per project (bukan folder tugas harian)]
│   ├── 03_REFERENCE/             [referensi umum lintas domain]
│   ├── _inbox/                   [file lepas/tak jelas menunggu triase — bukan tempat menumpuk permanen]
│   └── <YYYY-MM-DD>_<task-slug>/ [folder tugas Documentation Contract (aktif) — snake_case]
├── vault/                        [staging — dikecualikan dari scan workspace IL (scope=vault)]
├── ekas/                         [PROTEKSI — korpus EKAS, struktur kanonik tetap]
└── legacy-archive/               [arsip beku: <domain>/ atau <project>/; tetap ter-scan IL]
```

### 4.1 Aturan folder

1. **`docs/` root tidak boleh ada file lepas** — kecuali file indeks yang memang ditetapkan di
   `00_INDEX/`. File lepas → `_inbox/` (bila belum jelas) atau folder yang sesuai.
2. **Nama folder tugas**: `YYYY-MM-DD_<task-slug>` snake_case (huruf kecil, `_`, angka).
   DILARANG: `t_<hash>`, tanggal tanpa slug, `Untitled`, spasi, huruf kapital.
3. **Siklus hidup folder tugas**: aktif di `docs/` → setelah **selesai + berumur ≥ 30 hari** dipindah ke
   `legacy-archive/`. Folder berumur < 7 hari **jangan** dipindah (masih bisa dirujuk task aktif).
4. **Folder arsip** boleh menyusun sub-struktur `<domain>/` atau `<project>/` agar tetap bisa ditelusuri.
5. **`_inbox/` adalah zona transit**, bukan gudang: item di _inbox > 14 hari → dipindah ke folder tepat
   atau ditandai untuk keputusan manusia.

## 5. Konvensi penamaan

| Objek | Konvensi | Contoh |
|-------|----------|--------|
| Folder tugas | `YYYY-MM-DD_<task-slug>` snake_case | `2026-08-24_kurasi_ekas` |
| File artefak tugas | `YYYY-MM-DD_<slug>.md` | `2026-08-24_status-kurasi.md` |
| File pengetahuan stabil | `<kebab-slug>.md` | `katalog-skill-gsp.md` |
| File memory harian | `YYYY-MM-DD_log_<slug>.md` | `2026-08-24_log_librarian_kurasi_vault.md` |
| Objek vault | `vault/<perkara>/<YYYY-MM-DD>_<slug>.md` | `vault/contoh-vendor-research/2026-08-24_index.md` |
| Entri wiki | `<type>s/<slug>.md` | `proyeks/contoh-vendor-research-index.md` |

Aturan umum: huruf kecil; tanpa spasi; tanpa karakter khusus selain `-` `_` `.`; tanggal ISO `YYYY-MM-DD` (pengecualian: arsip memori `memory/refs/<profil>/<YYYY_MM_DD>_<slug>.md` menurut skill `gsp-memory-tiering` dan `gsp-memory-lookup` memakai garis bawah; arsip lama tidak diganti nama);
slug deskriptif (2-5 kata). **DILARANG** akhiran versi di nama (`_v2`, `_final`, `_FINAL2`) — versi ada di
frontmatter (`version`), bukan di nama file.

## 6. Daftar bidang keahlian

Domain adalah taksonomi **terkontrol** (bukan bebas). Nilai awal:

| Domain | Sub-domain | Contoh isi |
|--------|-----------|------------|
| `engineering` | vss, fiber, power, grounding, security-cctv, infrastructure | perhitungan, desain, spesifikasi |
| `defense-intel` | perkara instansi pertahanan | riset vendor, ekspo, intelijen publik |
| `corporate` | vendor, procurement, finance, hr | profil vendor, kontrak |
| `digital` | ai-systems, software, data, social-media | riset AI, otomasi, analisis sosmed |
| `operations` | delivery, fleet, quality | status proyek, smoke-test |
| `library` | kurasi, standards | katalog, standar, indeks |

Domain baru ditambahkan lewat **update standar ini** (bukan inline di file). Sub-domain boleh lebih
spesifik di nama folder (`01_DOMAIN/engineering/vss/`).

## 7. Versi dan siklus hidup artefak

- Setiap artefak pengetahuan punya `version` semver (`X.Y.Z`, default `1.0.0`). Perubahan isi yang
  berarti → naikkan versi minor; perubahan editorial → patch.
- Siklus hidup (frontmatter `status`):
  - Workspace docs: `draft` → `active` → `superseded` → `archived`
  - Wiki: `active` → `superseded` → `archived` (dikelola `vault_promote.py`)
- Garis keturunan dicatat dengan `supersedes: <id>` dan `superseded-by: <id>` (id = slug stabil).
- Snapshot dan data berkala TIDAK memakai versi semver — tanggal di nama adalah versinya.

## 8. Larangan (jangan pernah)

1. Menghapus file — selalu pindah (ke `_inbox/`, folder tepat, atau `legacy-archive/`).
2. Mengubah isi dokumen orang lain — pelaksanaan harian hanya boleh menyentuh **metadata/frontmatter & path**.
3. Menyentuh [`ekas/`](../../4%20Knowledge%20Bank/ekas-lapis-teks/), `AGENTS.md`, `MEMORY.md`, isi `memory/`, semantik `vault/`.
4. Menulis wiki di luar `vault_promote.py`.
5. Memindah folder berumur < 7 hari atau folder yang dirujuk dokumen aktif (cek referensi; bila ragu, tandai untuk ditinjau).
6. Menamai ulang file yang id/slug-nya dirujuk entri wiki/IL tanpa mencatat migrasi di CHANGES.md.

## 9. Verifikasi kepatuhan (dijalankan tiap pelaksanaan harian, lihat 03)

- [ ] Tidak ada file lepas di `docs/` root (selain indeks resmi)
- [ ] Tidak ada folder `t_*`/cryptic di `docs/`
- [ ] Semua folder tugas bernama `YYYY-MM-DD_<slug>` snake_case
- [ ] Semua dokumen punya frontmatter valid (cek 02)
- [ ] Tidak ada duplikat judul/id aktif
- [ ] `_inbox/` tidak menumpuk > 14 hari
- [ ] CHANGES.md run terakhir tercatat & konsisten (old → new)
- [ ] IL API (`scope=all`) menampilkan judul manusiawi, tanpa entri sumber tak dikenal

## 10. Riwayat revisi

| Versi | Tanggal | Perubahan | Editor |
|-------|---------|-----------|--------|
| 1.0.0 | 2026-08-25 | Standar awal | brahma |
| 1.1.0 | 2026-10-31 | Contoh folder tugas memakai tanggal ISO; pengecualian tanggal untuk arsip memori `refs/` | pemelihara-pustaka |
