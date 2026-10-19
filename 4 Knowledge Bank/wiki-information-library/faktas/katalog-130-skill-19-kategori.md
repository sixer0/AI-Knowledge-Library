---
id: katalog-130-skill-19-kategori
type: fakta
title: Katalog 130 Skill Unik Ekosistem GSP (19 Kategori)
status: active
sumber: docs/2026_08_24_kajian_ekosistem/katalog_skill_lengkap.md
halaman: Ringkasan Katalog & contract doc 2026-08-24-katalog-skill.md
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [skill, katalog, 130, registry]
links: [kategori-skill-gsp-30-dan-orchestration-5]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Semua angka dihitung ulang dari data mentah dan cocok persis: skills_catalog_raw.json berisi 130 entri dengan 19 kategori berbeda; tally kategori identik dengan sebaran di body (gsp 30, productivity 18, creative 16, software-development 11, database 8, autonomous-ai-agents 7, github 7, research 7, mlops 5, orchestration 5, apple 4, media 3, devops 2, email 2, data-science 1, note-taking 1, smart-home 1, social-media 1, yuanbao 1). Jumlah heading H3 katalog_skill_lengkap.md = 130 (satu entri per skill). File pendukung 13 template / 28 script / 48 referensi cocok dengan baris Total Ringkasan Katalog baris 37. Klaim verifikasi docx (150 heading = 20 H1 + 130 H2, 1 tabel, 1418 paragraf) dan kartu t_949c6a74 cocok dengan contract doc 2026-08-24-katalog-skill.md. Tidak ada dimensi yang gagal. Seksi Catatan merekonsiliasi selisih 128 SKILL.md registry (20 kategori, kajian §8.1) vs 130 unik gabungan registry+kanonik - rekonsiliasi yang diperlukan dan sudah benar. Kebijakan dedup salinan per-profil dinyatakan eksplisit sehingga tidak dihitung ganda. || Rekomendasi: Siap dipromosikan. Sunting status `terverifikasi` -> `ditinjau` sebelum promote (aturan I1). Saat promosi sertakan jejak skrip hitung (scan_skills_catalog.py / build_skills_catalog.py) sebagai rujukan agar pembaca wiki dapat membuka bukti mentahnya. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/katalog-130-skill-19-kategori.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Katalog 130 Skill Unik Ekosistem GSP (19 Kategori)

Katalog resmi seluruh skill ekosistem GSP — **130 skill unik, 19 kategori**
(katalog_skill_lengkap.md, Ringkasan Katalog; contract doc 2026-08-24-katalog-skill.md).

- **Sumber inventaris:** registry default `AppData/Local/hermes/skills` +
  kanonik `workspace/gsp-hermes/skills`.
- **Sebaran kategori:** gsp 30 · productivity 18 · creative 16 ·
  software-development 11 · database 8 · autonomous-ai-agents 7 · github 7 ·
  research 7 · mlops 5 · orchestration 5 · apple 4 · media 3 · devops 2 ·
  email 2 · data-science 1 · note-taking 1 · smart-home 1 · social-media 1 ·
  yuanbao 1.
- **File pendukung:** 13 skill punya template, 28 punya script, 48 punya
  referensi.
- **Kebijakan dedup:** skill per-profil (`profiles/gsp-*/skills/`) adalah
  salinan registry/kanonik sesuai ALWAYS/ON DEMAND SOUL.md — tidak dihitung
  ganda; 2 entri kanonik-only tercatat.
- **Sumber kebenaran inventaris:** registry default; kanonik EKAS ditandai
  badge (decision log).
- **Verifikasi:** 130 entri diekstrak (scan rekursif seluruh root, tidak ada
  yang terlewat); docx_validate ok (150 heading: 20 H1 + 130 H2; 1 tabel, 1418
  paragraf).

Sumber: `katalog_skill_lengkap.md` (Ringkasan Katalog + contract doc
2026-08-24-katalog-skill.md §Data Kunci & Verifikasi).

# Bukti

- Data mentah: `skills_catalog_raw.json` (130 skill, 19 kategori — kontrak t_949c6a74).
- Dossier kompilasi 139 KB + Word terverifikasi.

# Catatan

- Kajian ekosistem menyebut 128 SKILL.md registry (20 kategori) + 12 kanonik;
  katalog gabungan = 130 unik (dedup nama registry ↔ kanonik).
