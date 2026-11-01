---
title: "Standar Penempatan & Kerapian Skrip GSP (v1.1.0)"
type: standar
status: active
created: 2026-09-21
updated: 2026-09-28
writer: swarm (gsp-master)
editor: gsp-master
version: 1.1.0
domain: workspace-ops
project: workspace-hygiene
tags: [standar, skrip, organisasi, workspace, gsp, globak]
kelas_bukti: norma-user
---

# Standar Penempatan & Kerapian Skrip GSP (v1.0.0)

> Dokumen hidup. Kanonik: `docs/standards/05_SCRIPT-ORGANIZATION-STANDARD.md`.
> Aturan ini PUTUSAN USER 21-09-2026: "jadikan aturan global kedepannya semua
> script harus terorganisir dengan baik." Berlaku untuk SEMUA agen fleet GSP.

## 1. Larangan keras

1. **DILARANG membuat skrip di root workspace** (`C:/Users/TRIAL/workspace/`).
   Root hanya boleh berisi folder proyek/fungsi, bukan `_tmp.py`, `e4_x.py`,
   `check_*.ps1`, dsb.
2. **DILARANG menaruh skrip sekali-pakai di lokasi sembarang.** Setiap skrip wajib
   dibuat langsung di bawah `scripts/<function>/<task>/`, bukan menunggu dirapikan
   belakangan.
3. DILARANG meninggalkan `__pycache__`/log/data sementara di root; ikut masuk ke
   folder task yang sama.

## 2. Taksonomi kanonik (`scripts/<function>/<task>/`)

Fungsi (lapis 1) — pilih salah satu:

| Fungsi | Isi |
|---|---|
| `research/` | pengumpulan/panen data web, crawler, parser halaman |
| `documents/` | pembuat/pembaca/verifikasi dokumen (docx/xlsx/pptx/pdf) |
| `kanban/` | audit, dump, rekonsiliasi papan tugas |
| `fleet-ops/` | dispatch fleet, watchdog, cek proses/bridge, RBAC |
| `hq-testing/` | uji E2E/UI HQ & WebUI (playwright, verify_*) |
| `media/` | pemrosesan/penskoringan citra & audio |
| `cad/` | skrip CAD/DXF/render |
| `data/` | transformasi/ETL dataset umum |
| `misc/` | hanya bila tak ada fungsi lain yang cocok (hindari) |

Task (lapis 2) — slug pendek per misi/tema, contoh `univ-uk-eu`, `ads-intel-e4`,
`katalog-expo`, `instansi-surat`. Satu misi = satu folder task. Artefak data
pendamping (JSON/log yang dibaca skrip relatif) ikut ke folder task yang sama.

## 3. Aturan pindah & integritas path

1. Sebelum memindah skrip hidup: grep referensi (cron, bridge, launcher, skrip
   lain, proses berjalan). Bila ada rujukan, perbarui rujukannya di commit yang
   sama.
2. Setelah pindah: tambal path absolut/internal yang rusak (`sys.path.insert`,
   `open(r"...")`) agar skrip tetap jalan dari lokasi baru.
3. Gerbang wajib sebelum menutup kerja: `python -m compileall -q scripts/` exit
   0, dan smoke import/rute untuk skrip berantai impor.
4. Tulis `MANIFEST-<tanggal>.tsv` (asal → tujuan → ukuran) sebagai jejak audit.

## 4. Kontrak nama berkas skrip

- Bahasa Indonesia/Inggris bebas, tapi deskriptif: `harvest_fees.py`,
  `verify_upload_limit.py`. Hindari `_t1.py`, `_hc_b.py`, `e4_id17.py` (nomor
  buta tanpa makna). Saat merapikan warisan, nama lama boleh dipertahankan bila
  direferensikan; nama baru WAJIB deskriptif.
- Skrip sekali-pakai yang terbukti usang: pindahkan ke `scratch/` (jangan hapus
  tanpa putusan user), beri prefiks tanggal.
- **DILARANG memakai nama modul standar Python sebagai nama berkas skrip**
  (`inspect.py`, `json.py`, `random.py`, `types.py`, `email.py`, `test.py`,
  dst. — uji dengan `python -c "import sys; print(fn[:-3] in
  sys.stdlib_module_names)"`). Aturan ini berlaku di SEMUA folder tempat skrip
  bisa dijalankan, termasuk folder scratch/Temp. Penyebab: direktori kerja
  paling depan di `sys.path`, sehingga `inspect.py` di akar Temp membayangi
  modul standar dan merusakkan import library pihak ketiga dari folder itu
  (preseden 27-09: misi harga-proyek menaruh `inspect.py` di akar `%TEMP%`;
  seluruh import pymupdf dari folder itu mati dengan error menyesatkan;
  kontrak remediasi `docs/2026-09-28-stdname-shadow-fix/`).

## 5. Penegakan

- Verifier/reviewer misi WAJIB menolak (FAIL) kartu implementasi yang
  meninggalkan skrip di root workspace.
- Cron watchdog invarian (kelas INV) dapat menambah cek "root workspace bersih
  dari skrip" sebagai jaring pengaman.

## Riwayat

- v1.0.0 (2026-09-21): dibuat atas perintah user; diiringi perapian 174 skrip root
  ke taksonomi ini (lihat `scripts/MANIFEST-2026-09-21.tsv`, kontrak misi
  WUI-IMP-0921 kartu O1 `t_73549c50`).
