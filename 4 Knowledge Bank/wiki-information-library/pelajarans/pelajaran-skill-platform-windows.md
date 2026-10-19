---
id: pelajaran-skill-platform-windows
type: pelajaran
title: "Pelajaran: skill gsp-library-workflow & gsp-library-data-standards tidak termuat via skill_view di Windows"
status: active
created: 2026-08-25
sumber: docs/2026_08_24_kurasi_ekas/README.md
halaman: n/a (dokumen teks tanpa paginasi)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kurasi-ekas
domain: library
writer: gsp-librarian
tags: [pelajaran, windows, skill_view, python, platform]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/kurasi-ekas/2026-08-25_pelajaran-skill-platform-windows.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran: skill gsp-library-workflow & gsp-library-data-standards tidak termuat via skill_view di Windows

Saat kurasi EKAS 2026-08-24, skill `gsp-library-workflow` dan
`gsp-library-data-standards` ber-`platforms: [macos, linux]`, sehingga
`skill_view` menolak memuatnya di Windows.
[sumber: docs/2026_08_24_kurasi_ekas/README.md, dokumen teks tanpa paginasi —
bagian "Blocker / catatan"]

## Workaround yang terbukti

1. Baca konten skill langsung dari `SKILL.md` (bukan lewat `skill_view`).
2. Jalankan helper (mis. `vault_propose.py`, `vault_promote.py`) dengan
   `python` — bukan `python3` (python3 tidak tersedia di host; python 3.11 ada).
   [README.md, "Blocker / catatan"; status.md, "Blocker"]

## Pelajaran

- Sebelum menjalankan alur kurasi di Windows, cek frontmatter `platforms` pada
  skill yang wajib dimuat; bila tidak mencakup windows, akses lewat file
  langsung.
- Helper GSP berbasis Python dapat dipanggil dengan `python` di host ini;
  `python3` tidak tersedia.

## Asumsi

Tidak ada asumsi. Kondisi platform (python 3.11, python3 missing) sesuai catatan
dokumen sumber dan pengamatan sesi ini.
