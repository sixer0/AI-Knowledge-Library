---
name: koridor-dokumen
version: 1.1.0
updated: 2026-08-31
status: active
source_of_truth: skills/gsp/gsp-document-quality-standards/SKILL.md (Module L)
---
# Koridor Dokumen GSP - teks blok kanonik

> **Fungsi.** Berkas ini adalah SATU-SATUNYA sumber teks blok `## Koridor Dokumen GSP`
> yang disisipkan ke skill penghasil dokumen fleet (keputusan D1, blueprint
> `docs/2026-08-31-standar-dokumen-fleet/identification/02_structured.md`).
> Isi di bawah baris marker disisipkan **VERBATIM** - dilarang mengarang varian lokal.
> Spesifikasi lengkap dan rationale: **Module L** di skill anchor.
> Tier-3 (skill code/tech-doc) memakai varian pointer: `koridor-dokumen-tier3.md`.

<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

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
