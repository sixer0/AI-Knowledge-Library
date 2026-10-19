---
name: gsp-fleet-documentation
description: "Document GSP agent fleet mapping: profiles, personas, skills"
version: 1.0.1
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: documentation
    tags: [gsp, fleet, profiles, skills, roster, documentation, mapping, docx, manifest, soul]
---

# GSP Fleet Documentation

> Runbook untuk menghasilkan dokumen profesional perusahaan yang memetakan ekosistem
> profil agen GSP (persona, skill, model, toolsets, roster) **langsung dari data nyata** —
> bukan rekonstruksi manual. Dipakai untuk: inventory fleet, mapping profil×skill,
> dokumentasi arsitektur ekosistem, onboarding, dan audit kesesuaian persona-skill.


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## When to Use

- User minta mendokumentasikan / memetakan ekosistem profil agent GSP dengan persona dan skillnya.
- User minta "duplikasi codebase + dokumentasi mapping" sebagai satu misi.
- Perlu dokumen perusahaan presentable (nomor dokumen, cover page, klasifikasi) tentang fleet.
- Audit kesesuaian: apakah profil terpasang konsisten dengan manifest & ROSTER.

## Prerequisites

- Fleet GSP terinstall: `~/workspace/gsp-hermes/` (manifest.json, scripts/, skills/, workspace/).
- Profil di `~/.hermes/profiles/gsp-*/` (SOUL.md, skills/).
- Dashboard HQ ROSTER: `~/gsp-agent-headquarter/src/app/api/agents/route.ts`.
- Python3 + python-docx (`python3 -c "import docx"`). Pandoc/libreoffice biasanya TIDAK ada — pakai converter bawaan skill ini ([`scripts/md2docx.py`](scripts/md2docx.py)).

## Workflow (data-driven, reproducible)

1. **Duplikasi codebase (bila diminta):** `rsync -a --delete <sumber>/ project/gsp-hermes/`, lalu verifikasi
   `diff -rq <sumber> project/gsp-hermes` → exit 0 = identik. Hati-hati `--delete` (mirror); pastikan arah sumber→target benar.
2. **Ekstrak data ke satu JSON:** `python3 scripts/extract_fleet_data.py` — membaca manifest.json (35 profil,
   5 grup), SOUL.md per profil (seksi `## Persona`), ROSTER `route.ts` (regex), frontmatter deskripsi 65 SKILL.md kanonik.
3. **Generate Markdown:** tulis `gen_doc.py` (template narasi + data dari JSON) → dokumen MD lengkap
   (cover, daftar isi, ringkasan eksekutif, BAB arsitektur, BAB mapping per grup dengan kartu profil,
   katalog skill, matriks relasi, lampiran ROSTER). Simpan generator di `_tools/` di folder docs agar
   dokumen bisa diregenerasi (reproducible artifact).
4. **Konversi ke DOCX:** `python3 scripts/md2docx.py in.md out.docx --title ... --subtitle ... --meta "K=V"` —
   cover page terpisah + heading bertingkat + tabel ber-shading navy + list/bold/italic/code inline.
5. **Verifikasi:** buka DOCX via python-docx, cek jumlah heading H1 == jumlah bab, jumlah tabel, cover metadata.
6. **Distribusi (Documentation Contract GSP):** salin MD+DOCX ke
   `~/workspace/gsp-hermes/workspace/docs/[YYYY_MM_DD]_[task]/` dan append entri ke `workspace/memory/YYYY-MM-DD.md`.

## Struktur Dokumen yang Terbukti (frame untuk mapping)

- Cover page (perusahaan, judul, nomor dokumen, klasifikasi Terbatas—Internal, tanggal, penyusun, versi, status)
- Ringkasan Eksekutif (angka nyata: jumlah profil per grup, model teks vs vision, skill kanonik)
- BAB 1 Pendahuluan (latar, tujuan, ruang lingkup, metodologi, definisi/singkatan)
- BAB 2 Arsitektur Ekosistem (manifest-first, generator, gateway, watchdog, dashboard, shared workspace, kontrak GSP-1..5)
- BAB 3 Pemetaan Profil per Grup (tabel ringkas + kartu per profil: persona SOUL, model, toolsets, ALWAYS/ON DEMAND + deskripsi skill)
- BAB 4 Katalog Skill Kanonik (per domain, dengan aset scripts/templates/references)
- BAB 5 Matriks Relasi Profil×Skill (skill terpakai terbanyak + cakupan per profil)
- BAB 6 Model/Toolset/Kapabilitas (distribusi toolset, profil vision vs teks, kontroler ber-delegation)
- BAB 7 Alur Orkestrasi & Governance (RT-FIRST, Blueprint Approval, Completion Gates, jalur gratis dulu)
- BAB 8 Penutup (jujur: potret pada tanggal terbit; asumsi/limitasi eksplisit)
- Lampiran A ROSTER HQ, B profil terpasang, C struktur codebase

## Pitfalls

- **Pandoc/libreoffice sering tidak ada** → jangan bergantung; [`scripts/md2docx.py`](scripts/md2docx.py) (python-docx) sudah menangani
  heading #..####, tabel pipe, bullet/numbered, bold/italic/code inline, blockquote, code block, dan cover terpisah.
- **ROSTER statis di `route.ts`** — parse dengan regex blok entri `{ id, profile, name, emoji, role, model, level, group }`.
  `profile: "default"` = Brahma (level 1, grup core); level 2 = advisor (request-translator, task-architect); level 3 = spesialis.
  Jumlah ROSTER = 35 gsp + 1 brahma = 36.
- **Persona dari SOUL:** ambil paragraf setelah `## Persona` (bukan baris pertama file — ada header `# SOUL — <id>` dan `## Identitas`).
- **Validasi silang wajib:** manifest == profil terpasang (`~/.hermes/profiles/gsp-*`) == jumlah gsp di ROSTER.
  Cetak `missing SOUL` dan `profil tanpa roster` — kedua daftar harus kosong.
- **Beberapa profil ALWAYS LOAD 0** (explore, data-collector, image-analyst, dll.) — normal; jangan dipaksakan.
- **`rsync --delete`** = mirror penuh; kunci arah benar. Setelah copy jangan tulis file baru ke target sebelum diff selesai,
  agar hasil verifikasi bersih.
- **gsp-image-prompt-specialist** punya skill ALWAYS LOAD bernama sama dengan profilnya — data nyata, pertahankan apa adanya.
- **Grup profil vs grup ROSTER bisa beda label** (manifest `utility` ↔ ROSTER `advisor` untuk RT/task-architect) — sajikan keduanya.

## Support Files

- [`scripts/extract_fleet_data.py`](scripts/extract_fleet_data.py) — ekstraksi data fleet (manifest + SOUL + ROSTER + skill frontmatter) → JSON + ringkasan. Jalankan dulu; hasil dipakai generator.
- [`scripts/md2docx.py`](scripts/md2docx.py) — converter Markdown→DOCX profesional (python-docx), cover page + tabel ber-shading + heading bertingkat.

## Verification

Dianggap berhasil bila: duplikasi `diff -rq` exit 0; ekstraksi mencetak jumlah profil/skill/roster yang cocok dengan
hitungan nyata; dokumen MD terbaca utuh; DOCX terbuka via python-docx dengan jumlah heading H1 == jumlah bab
dan cover metadata benar; artefak tersalin ke shared workspace `docs/` + entri log harian tertulis.
