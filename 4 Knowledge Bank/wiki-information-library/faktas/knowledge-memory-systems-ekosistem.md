---
id: knowledge-memory-systems-ekosistem
type: fakta
title: Knowledge & Memory Systems Ekosistem (Workspace, EKAS, Wiki, IL, Kanban)
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 9.1-9.6
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: library
writer: gsp-librarian
tags: [knowledge, ekas, wiki, il, memory]
links: [pipeline-librarian-raw-vault-wiki]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Semua angka cocok kajian §9.1-9.6 baris 388-427: EKAS 270 file/1.7 MB + 430 file/160 PDF/3 GB; wiki 54 file 6 folder; HermesMemory 54 baris; IL 1.996 (fact 56, decision 62, note 1.672, project 206 = 54+1.942); kanban 43+4=47. RAW kedua contract doc independen mengonfirmasi EKAS/IL/DB counts. Seksi Batas jujur menandai angka sebagai snapshot audit. || Rekomendasi: Catatan kurator saat promosi: wiki kini 732 entri (tumbuh sejak audit) - pertahankan angka snapshot, jangan sunting body."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/knowledge-memory-systems-ekosistem.md
---

# Knowledge & Memory Systems Ekosistem (Workspace, EKAS, Wiki, IL, Kanban)

Knowledge & memory systems ekosistem GSP (kajian §9.1–9.6):

- **Shared workspace (Brahma Fleet)** `C:/Users/TRIAL/workspace/gsp-hermes/
  workspace`: AGENTS.md (Hermes-optimized + GSP-1..GSP-5), MEMORY.md + memory/
  (log harian), docs/ (artefak tugas snake_case), vault/ (staging librarian),
  ekas/ (mirror teks korpus, 244 entri IL), legacy-archive/.
- **EKAS** `C:/Users/TRIAL/gsp-ekas/`: model-lokal/ = 270 file teks 1.7 MB;
  lengkap/ = 430 file + 160 PDF sumber 3 GB; struktur 00_START-HERE …
  90_TOOLS; model jaminan R1–R5, gate G0–G7, 12 rantai jaminan, 61 knowledge
  cards, TPL-00..09 (lihat unit `rantai-jaminan-ekas-r1-r5`).
- **Wiki & HermesMemory:** `C:/Users/TRIAL/AppData/Local/hermes/wiki` — 54
  file .md dalam 6 folder (catatans, faktas, keputusans, pelajarans, proyeks,
  standars); dicerminkan ke HermesMemory (54 baris, type=fact semua, status
  active); ditulis via API `/api/brahma/memory` atau bridge memory.write.
- **Information Library (IL):** endpoint `/api/information-library` — total
  1.996 entri saat audit (fact 56, decision 62, note 1.672, project 206) =
  wiki 54 + scan workspace 1.942 file .md; UI scope toggle + badge sumber.
- **Kanban board `default`:** SQLite `AppData/Local/hermes/kanban.db`; 43
  kartu awal (41 done, 2 blocked) + 4 kartu audit = 47; bridge menutup kartu
  otomatis per dispatch.
- **Pipeline librarian (RAW → VAULT → WIKI):** lihat unit
  `pipeline-librarian-raw-vault-wiki`.

Sumber: `kajian_ekosistem_brahma.md` bab 9.1–9.6.

# Bukti

- 1.996 entri IL dihitung via `/api/information-library?scope=all` (kajian
  §9.4; walkMd skip node_modules/.git/.next).
- 54 wiki file tercermin ke HermesMemory 54 baris (kajian §5.4, §9.3).

# Batas

- Jumlah entri IL = snapshot audit 24-08-2026; knowledge baru terus
  bertambah.
