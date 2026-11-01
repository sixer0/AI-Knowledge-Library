---
title: "Standar Metadata Information Library GSP (v1.0.0)"
type: standar
status: active
created: 2026-08-25
updated: 2026-08-25
writer: brahma
editor: gsp-librarian
version: 1.0.0
domain: library
project: information-library
tags: [standar, metadata, frontmatter, information-library, gsp]
kelas_bukti: sintesis
---

# Standar Metadata Information Library GSP (v1.0.0)

> Dokumen hidup. Kanonik: `docs/standards/02_METADATA-STANDARD.md`.
> Berlaku untuk semua dokumen markdown di workspace, vault, dan wiki. Frontmatter YAML satu baris per key.

## 1. Tujuan

Setiap dokumen IL harus dapat dibaca manusia dan diproses mesin. Riwayatnya harus jelas: siapa penulis dan penyuntingnya, kapan dibuat dan diubah, versi yang berlaku, sumbernya, serta status dokumen dalam siklus hidupnya.

## 2. Skema frontmatter (wajib + opsional)

Semua nama kolom memakai huruf kecil dengan format snake_case. Tulis satu kolom per baris. Contoh lengkap:

```yaml
---
title: "Judul manusiawi — SAMA dengan H1 pertama"
type: catatan|fakta|keputusan|pelajaran|proyek|standar|vendor|produk|dosir|indeks|inbox
status: draft|active|superseded|archived        # wiki: active|superseded|archived
created: YYYY-MM-DD                             # tanggal dibuat
updated: YYYY-MM-DD                             # terakhir diubah (di-refresh oleh editor)
writer: <profil-gsp>                            # penulis
editor: <profil-gsp>                            # editor/peninjau terakhir
version: X.Y.Z                                  # semver; default 1.0.0
domain: <domain-dari-registry>                  # lihat 01_ORGANIZATION-STANDARD §6
project: <slug-project>                         # bila bagian dari project
tags: [kata, kunci, terkait]
sumber: <path-relatif|url>                      # WAJIB untuk klaim/angka
halaman: <hal atau rentang>                     # untuk dokumen berhalaman
tanggal_akses: YYYY-MM-DD                       # untuk sumber yang berubah (web/pasar)
kelas_bukti: primer|sekunder|tersier|sintesis
links: [id-wiki, path-vault, url]               # referensi silang
supersedes: <id>                                # entri/versi yang digantikan
superseded-by: <id>                             # entri/versi pengganti
---
```

Key opsional khusus vault/wiki (dari `gsp-library-data-standards`): `id`, `sensitif: ya|tidak`,
`perkara`, `catatan_keputusan`, `di-attest-oleh`, `di-attest-pada`, `dipromosikan-ke`,
`persetujuan-ref`, `verifikasi-oleh`.

## 3. Aturan integritas (wajib)

| # | Aturan | Akibat jika dilanggar |
|---|--------|------------------------|
| M1 | `title` di frontmatter **sama** dengan H1 pertama (UI IL membaca H1) | Entri tampil dengan judul ganda/aneh di IL |
| M2 | `created` & `updated` format ISO `YYYY-MM-DD` | Tak bisa disortir/dilacak waktu |
| M3 | `writer` memakai nama profil/akun GSP (`gsp-<peran>`, `gsp-librarian`, `user-<nama>`), **bukan** nama model | Asal-usul kepenulisan tidak dapat dilacak |
| M4 | Setiap angka/klaim kuat wajib `sumber` + `halaman`; tanpa itu angka dianggap **asumsi** | Fakta tak terverifikasi masuk IL |
| M5 | `type` mengikuti taksonomi; `status` mengikuti siklus hidup (lihat 01 §7) | Tak bisa difilter/dikelola |
| M6 | `editor` memperbarui `updated` setiap kali dokumen diubah | Riwayat edit tak tercatat |
| M7 | `kelas_bukti` jujur: primer=asli, sekunder=laporan turunan, tersier=ringkasan pihak lain, sintesis=analisis lintas sumber | Nilai bukti salah tafsir |
| M8 | Dokumen tanpa frontmatter valid = pelanggaran; pelaksanaan harian mengisi metadata dasar tanpa mengubah isi & mencatat di CHANGES.md | Dokumen yatim di IL |

## 4. Metadata per lapisan

| Lapisan | Key wajib | Keterangan |
|---------|-----------|------------|
| Workspace docs (draft) | title, type, status, created, writer, domain, tags | `updated`/`editor`/`version` wajib bila sudah pernah direvisi |
| Vault (usulan) | id, type, title, status, sumber, kelas_bukti, sensitif, diajukan | Lihat `gsp-library-data-standards`; angka wajib sumber+halaman |
| Wiki (terbit) | id, type, title, status, sumber, kelas_bukti, penulis, diajukan, di-attest-oleh, di-attest-pada | Ditulis `vault_promote.py`; pelaksanaan harian TIDAK menulis langsung |
| Memory harian | (konvensi log) `YYYY-MM-DD_log_<slug>.md` | Ikut aturan penamaan; isi tidak disentuh pelaksanaan harian |

## 5. Contoh frontmatter buruk vs baik

**Buruk** (ditemukan di lapangan — ini yang diperbaiki pelaksanaan harian):

```yaml
---
title: Untitled
---
```

```yaml
---
judul: sesuatu
tanggal: 24/08/26
author: AI
---
```

**Baik**:

```yaml
---
title: "Katalog Skill GSP — Inventaris Lengkap"
type: indeks
status: active
created: 2026-08-24
updated: 2026-08-25
writer: gsp-document-analyst
editor: gsp-librarian
version: 1.2.0
domain: library
project: information-library
tags: [katalog, skill, inventaris]
kelas_bukti: sintesis
---
```

## 6. Verifikasi metadata (tiap pelaksanaan harian)

- [ ] 100% dokumen workspace (di luar zona proteksi) punya frontmatter valid: title, type, status, created, writer
- [ ] Tidak ada `title: Untitled` / H1 kosong
- [ ] Tidak ada nama kolom salah eja (`judul`, `author`, `tanggal` non-ISO)
- [ ] `writer`/`editor` memakai identitas GSP
- [ ] Dokumen berisi angka tanpa `sumber`/`halaman` → ditandai di laporan (bukan dihapus)
- [ ] Entri wiki dengan metadata menyimpang → ditandai untuk kurasi lewat alur promote (bukan diedit langsung)

## 7. Riwayat revisi

| Versi | Tanggal | Perubahan | Editor |
|-------|---------|-----------|--------|
| 1.0.0 | 2026-08-25 | Standar awal | brahma |
