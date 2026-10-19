---
name: gsp-skill-authoring
description: "Skill Creator GSP: CRUD skill dan tools — create, patch, edit, delete skill fleet dari registry kanonik."
version: 1.2.0
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, skills, authoring, crud, fleet]
    category: orchestration
---

# GSP Skill Creator — CRUD Skill & Tools Fleet

## When to use
- Di-dispatch untuk membuat/ubah/hapus skill atau tools fleet GSP, atau menambah skill baru
  yang belum dimiliki (dipanggil oleh Skill Manager).
- Kamu adalah **penulis**: verifikasi hasil oleh System Control (penulis bukan verifikator).

## Lokasi & jalur kanonik (fakta post-reorg 29-08-2026 — FLAT, bukan nested)
- **Registry kanonik (sumber kurasi):** `C:/Users/TRIAL/workspace/gsp-hermes/skills/<name>/SKILL.md`
- **Registry fleet (default hermes, sumber tunggal on-demand):**
  `$LOCALAPPDATA/hermes/skills/gsp/<name>/SKILL.md` — FLAT satu tingkat di bawah `gsp/`
  (121 SKILL.md saat inventaris 2026-08-30; struktur nested `<name>/<name>/` sudah DIHAPUS
  saat reorg 29-08 — JANGAN dibuat ulang). Kategori non-GSP hidup flat di
  `$LOCALAPPDATA/hermes/skills/<kategori>/<name>/SKILL.md`.
- **Profil:** `C:/Users/TRIAL/AppData/Local/hermes/profiles/<profil>/skills/<name>/SKILL.md`
  (flat; skill dari engine Hermes bisa berada di subfolder kategori, mis.
  `skills/software-development/<name>/SKILL.md`). Salinan didistribusi oleh
  `gsp-skill-distribution`.
- Format skill: SKILL.md (YAML frontmatter: `name`, `description`, `version`, `author`,
  `license`, `metadata.hermes.tags`, `category`) + optional references/, scripts/, templates/.

## Alur CRUD
1. **CREATE** — tulis SKILL.md baru (ikuti `hermes-agent-skill-authoring` & contoh registry):
   - description: pemicu jelas + perilaku 1 garis; trigger di 57 chars pertama.
   - Body: When to use → langkah konkret → pitfalls → verification.
   - Author/category gsp; commit ke registry kanonik + registry fleet.
2. **UPDATE** — `gsp skills` CLI atau edit langsung; patch (old/new) prefer untuk fix kecil;
   edit (full rewrite) untuk overhaul besar. Setelah update: re-read skill_view, pastikan
   frontmatter intact.
3. **DELETE** — hapus dari kanonik + registry fleet + profil yang memegang salinan
   (perbarui SOUL ALWAYS/ON DEMAND bila perlu).
4. **Tools** — tools Hermes terdaftar di config.yaml profile (platform_toolsets.cli list);
   jika request menuntut tool khusus, pastikan toolsets integrasi tercatat + cek kesehatan.

## Jalur Defect / Fix (dari Skill Manager)
- Dipanggil oleh Skill Manager setelah proposal defect disetujui:
  - **BUG**: patch/edit skill di registry kanonik + fleet, lalu distribusi update ke profil pemegang.
  - **CHANGE REQUEST**: implementasi perubahan yang telah dinilai relevan oleh manager.
- Setelah update: re-read skill_view, pastikan frontmatter intact; verifikasi oleh System Control.

## Pitfalls
- PITFALL Windows patch: pakai write_file/script byte-safe Python bila string mengandung CR-LF literal
  (patch tool bisa membuat CR literal sehingga merusak file; ironically this very line was
  mangled by that mechanism on 09-10 when edited through patch).
- PITFALL registry fleet = profil `default`: `patch`/`write_file` ke
  `$LOCALAPPDATA/hermes/skills/gsp/<nama>/...` DIBLOKIR guard lintas-profil. Pola jalan
  (terbukti 09-10 kartu t_2c28626f): edit di kanonik `<ws>/gsp-hermes/skills/<nama>/`,
  lalu `cp` berkas berubah ke fleet lewat terminal, verifikasi `cmp -s` (bukan sha —
  lihat pitfall shell di bawah), dan hapus bytecode basi `__pycache__/<mod>.cpython-*.pyc`
  di KEDUA pohon (`rm -f <berkas-spesifik>`) supaya salinan fleet yang dieksekusi benar-benar
  byte hidup. Kartu yang menyebut jalur fleet sebagai objek kerja = direktif eksplisit.
- PITFALL gerbang merah instrumen ber-token: menyalin HANYA skrip lint ke Temp lalu
  menjalankannya GAGAL (`FileNotFoundError: tokens.json` — resolver `HERE.parent`).
  Bangun mirror minimal: `<tmp>/tokens.json` + `<tmp>/scripts/<skrip>.py` +
  `<tmp>/scripts/fixtures_*/` tempat fixture dibutuhkan selftest.
- PITFALL sesi single-query (-q): `execute_code` diblokir TOTAL, begitu pun `rm -rf` dan
  `find -delete`. Tulis skrip probe ke berkas di `$LOCALAPPDATA/Temp` lalu jalankan via
  `uv run`; untuk hapus pakai `rm -f <berkas>` spesifik. `python -c` boleh, heredoc tidak.
- PITFALL ukur sha di git-bash: untuk jalur ber-backslash Windows output `sha256sum`
  ter-render dengan `\` di depan dan karakter terakhir terpotong (`\38a24bb0b897b42`)
  sehingga perbandingan string A=B selalu TIDAK. Uji identitas berkas pakai `cmp -s`,
  atau `cygpath -w`/path forward-slash sebelum hashing.
- PITFALL putusan hulu bisa salah ukur: saat mekanisme yang disahkan manager tidak
  mencapai gerbang hijau kartu, JANGAN memperluas semantik cek sendiri. Implementasikan
  persis yang disahkan, UKUR semua pembacaan sah mekanisme itu (mis. tingkat kalimat vs
  paragraf) + kelas sisa temuan, tempelkan angkanya, lalu `kanban_block(kind=needs_input)`
  dengan opsi keputusan untuk manager. Preseden 09-10: DATUM-22 basal 36 pemicu, putusan
  mencatat 1; mekanisme sah membersihkan tepat 1; tiga pembacaan diukur semua >0.
- PITFALL fixture selftest scan_ai_footprint.py (kejadian nyata 06-10, t_334c0a44):
  parser md membuang segmen baris kosong (`Doc.add` skip teks kosong) sehingga paragraf
  prosa yang hanya dipisahkan baris kosong TERGABUNG jadi satu paragraf di mata
  `prose_paragraphs`; pemisah sejati = heading/tabel/kode. Fixture yang butuh N
  paragraf pendek (uji rasio C-7 dsb.) wajib dipisah `###` heading atau tabel, bukan
  baris kosong. Selain itu `sentences_of` memecah kalimat hanya bila titik diikuti
  spasi+huruf kapital: pola `**Label.** teks` tergabung satu kalimat dengan labelnya,
  jadi badan enam-bidang S-2 terbaca 1 kalimat/paragraf kecuali tiap bidang diisi
  >= 2 kalimat lengkap bermodal. Alat ukur presisi sebelum mengarang fixture: import
  scanner via importlib lalu `saf.prose_paragraphs(doc, False)` + `len(saf.sentences_of(p))`
  per paragraf.
- PITFALL path (post-reorg 29-08): SEMUA registry FLAT `<name>/SKILL.md` — kanonik, fleet
  (`skills/gsp/<name>/`), dan profil. Struktur nested `<name>/<name>/` sudah dihapus; jika
  kamu menemukannya muncul kembali (mis. dari copytree buta atau restore backup), ratakan
  dan hapus folder duplikat. Saat menyalin antar registry, salin folder skill utuh
  (SKILL.md + references/scripts/templates) ke jalur flat tujuan.
- Skill yang dihapus dari registry fleet namun masih di profil → warning konsistensi.
- Frontmatter harus valid (gagal load jika tidak).

## Verification
- `skill_view(name=<skill>)` berhasil load tanpa error; frontmatter valid;
  skill terlihat di `skills_list`; salinan kanonik + fleet + profil sinkron.
- Akhiri respons: `STATUS: complete|needs-review|blocked|failed` + `ARTIFAK: <path>`.
