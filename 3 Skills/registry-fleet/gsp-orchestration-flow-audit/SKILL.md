---
name: gsp-orchestration-flow-audit
description: >-
  Use to audit fleet orchestration flow and recurring work.
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, orchestration, audit, fleet-state]
    category: orchestration
---

# Audit Alur Orkestrasi & Peta Pekerjaan Berulang

Kelas tugas: **review read-only atas keadaan orkestrasi fleet** (bukan menjalankan misi).
Pemicu: user minta "tinjau alur orkestrasi", "petakan pekerjaan yang berulang", atau
vonis kesehatan ritus fleet. Keluaran = laporan ber-angka yang diukur langsung dari
sumber hari itu, bukan kutipan laporan lama (aturan angka-laporan = cetakan alat pada
giliran itu).

## Sumber kebenaran yang wajib diukur

| Sumber | Cara baca | Yang didapat |
|---|---|---|
| Papan kanban | `hermes kanban --board default list --json` (ribuan kartu; parse via Python/execute_code, jangan dibaca mentah) | status distribution, assignee distribution, umur kartu `blocked` (field `created_at`/`started_at`/`completed_at` = epoch detik), klasifikasi judul per regex |
| Cron fleet | **bukan** `cronjob action=list` — lihat PITFALL. Baca `jobs.json` utama + glob per profil | daftar job, schedule, enabled, no_agent vs agent-run, script |
| Folder misi | `docs/` shared ws: hitung `contract.md`, `identification/`, `PHASE-REPORTS.md`, pola nama berulang (sync-email-nas-*, gateway-*, draf-v*, triase*) | ritus yang dibayar ulang tiap giliran |
| Skrip fleet | `gsp-hermes/scripts/` + isi folder misi terbaru | skrip sekali-pakai yang lahir ulang per giliran vs modul tetap |

Jalankan `scripts/fleet_state_census.py` untuk sensus lengkap sekali jalan
(kanban buckets + cron inventory + docs census). Sesuaikan regex bucket judul
dengan kelas misi yang sedang aktif.

## PITFALL terukur (sesi audit 30-09)

- **`cronjob action=list` mengembalikan 0 padahal belasan job aktif.** Tool itu hanya
  menampilkan cron profil aktif/session ini. Untuk inventaris fleet WAJIB baca
  berkas: `$LOCALAPPDATA/hermes/cron/jobs.json` + glob
  `$LOCALAPPDATA/hermes/profiles/*/cron/jobs.json`. Tiap entri punya
  `name|schedule|enabled|no_agent|script`; `no_agent=True` = tanpa LLM (beban
  rendah), agent-run interval = beban tersembunyi terbesar.
- **Assignee mati tidak error, diam-diam orphan.** Setelah rebrand/migrasi profil,
  kartu ber-assignee profil yang foldernya sudah tidak ada di
  `$LOCALAPPDATA/hermes/profiles/` (mis. `brahma`, `default`, kosong/None) tak akan
  pernah diklaim dispatcher. Sensus: `ls "$LOCALAPPDATA/hermes/profiles/"` lalu
  cross-check kolom assignee. Temuan ini jejak historis, bukan pekerjaan hidup —
  laporkan begitu, jangan disarankan "kerjakan ulang".
- **Umur `blocked` dihitung dari epoch detik** di field JSON kartu; bandingkan vs
  tenggat gerbang 48 jam (aturan 10 `gsp-orchestration-execution`). Jangan pakai
  mtime berkas.
- **Kebijakan uji-window bisa menggantung tanpa vonis.** Kelas temuan: pola yang
  berstatus "opt-in selama jendela uji N hari" (mis. fast-lane DAG pre-built) tapi
  jendelanya sudah lewat dan tidak ada Decision Log naik-default/revert di docs.
  `grep -rl "<nama-kebijakan>" docs/` + cek DECISION-LOG sebelum menyimpulkan.
- **Klasifikasi judul kartu berbasis regex = pendekatan.** Laporkan sebagai
  "RT-like/TA-like ... berbasis pola judul, bisa meleset beberapa persen"; angka
  deterministik (jumlah kartu, umur blocked, jumlah folder) boleh diklaim keras.
- **`ls -d profiles/*/ | sed ...` menghasilkan nama kosong di git-bash** untuk
  direktori profil; pakai `ls` polos pada direktori profiles.

## Struktur laporan (kanal chat, tunduk gerbang naturalisasi)

1. **Alur saat ini** — urutan fase yang berjalan, diverifikasi dari artefak
   (identification/01+02, kartu kontrak, PHASE-REPORTS), plus subseksi
   "yang menyimpang dari desain" berisi temuan terukur.
2. **Peta berulang tiga kelas**: (Kelas 1) berulang via cron terotomasi —
   tabel protokol|frekuensi|beban; (Kelas 2) ritus orkestrasi yang belum
   terotomasi (RT+TA templated, perakitan kartu, closeout, audit insidental);
   (Kelas 3) defect-prone ritual (skrip sekali-pakai per giliran, assignee mati,
   rollout-skrip-per-kebijakan).
3. **Usulan prioritas bernomor** — tutup dengan pertanyaan apakah salah satu
   ditugaskan jadi misi berkartu. Jangan buat kartu/delegasi tanpa persetujuan.

Gerbang serah (wajib, preseden 30-09): tulis draf ke
`docs/<YYYY-MM-DD>-<slug>/draf-jawaban.md` → jalankan
`python "$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/scripts/scan_ai_footprint.py" --channel chat <berkas>` →
laporkan VERDICT + exit code bersama jawaban. FAIL = naturalisasi ulang dulu.

## Batas klaim

Laporan ini membaca keadaan, bukan memvonis penyebab. Untuk tiap butir usulan,
akar-nya (kenapa ritus berulang) butuh traceroot terpisah per misi bila user
menugaskannya.

## Riwayat
- 1.0.0 (2026-09-30): lahir dari misi tinjauan alur orkestrasi 30-09
  (3.313 kartu disensus, 514 folder docs, 17 job cron lintas 8 profil).
