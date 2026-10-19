---
name: gsp-word-report-deliverable
description: >-
  Use when producing GSP kajian/audit reports as Word .docx.
version: 1.5.0
author: Brahma (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, docx, report, kajian, audit, catalog, deliverable]
    category: gsp
---

# GSP Word Report Deliverable - kajian/audit/katalog → .docx

Workflow baku untuk menghasilkan **dokumen laporan komprehensif Word (.docx)**
di ekosistem GSP: kajian ekosistem, audit sistem, katalog skill/inventaris,
atau laporan besar lain yang user minta "detail lengkap tanpa ada yang
terlewat". Terbukti dipakai 24-08-2026 untuk Kajian Ekosistem (16 bab) →
Katalog Skill (130 entri) → Katalog Super Detail (semua file + isi penuh).


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../../registry-fleet/gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../../registry-fleet/gsp-document-quality-standards/references/koridor-dokumen.md)).

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
## GSP-SDT Integration (v1.2.0 - deliverable besar patuh bentuk dokumen)

Sumber kebenaran bentuk dokumen: [`skills/gsp/gsp-document-quality-standards/references/gsp-sdt/`](../../registry-fleet/gsp-document-quality-standards/references/gsp-sdt/)
(paket GSP-SDT; MERUJUK, jangan menyalin isinya). Skill ini memegang deliverable Word besar
(kajian/audit/katalog); GSP-SDT menambahkan lapisan bentuk untuk dokumen yang dinyatakan
berkelas K1–K8 / rezim tertentu - kajian internal bebas tetap cukup Module L.

Penerapan di skill ini:
1. **Gerbang pra-terbit WAJIB sebelum ekspor**: jalankan `checklist-pra-terbit.md` GSP-SDT
   (22 butir ≤25) berdampingan dengan checklist verifikasi skill ini (langkah 5 Workflow).
   Satu butir wajib gagal = TAHAN terbit; kegagalan dicatat di dokumen, tidak disembunyikan.
2. **Provenans angka wajib disebut dan benar** untuk setiap angka teknis di badan laporan:
   label `[terukur|diturunkan|pemasok|asumsi - sumber, hal]` + glyph ■◈◇△ (`provenans.md`);
   selaras aturan "klaim dari data live terverifikasi" skill ini - angka hasil tool = terukur,
   hasil hitung = diturunkan, klaim vendor = pemasok, belum diuji = asumsi.
3. Blok identitas + register `GSP-SDT(-XXX)-nnn` + klasifikasi kepala-kaki-sampul + nomor
   lembar pola rezim + tabel revisi (baris terbaru di puncak): lihat `blok-identitas.md`,
   `penomoran-footer.md`; helper `snippet-docx.py` paket SDT dapat dipakai bersama alur
   [`scripts/build_md_to_docx.py`](scripts/build_md_to_docx.py) skill ini (blok identitas disisipkan di awal markdown sumber).
4. Dokumen >8000 kata tetap lewat `gsp-long-document-assembly`; bagian SDT berlaku per bab
   (penomoran klausul per bagian, blok identitas di jilid utama saja).
5. Kelas dokumen kajian umumnya **K3 Kajian Teknis** (bobot 8, TERBATAS) untuk keluarga
   teknis; nyatakan kelas+bobot di blok identitas, penuhi titik ujinya (`kelas-dokumen.md`).

Larangan: jangan salin checklist/anatomi ke file ini; jangan nyatakan `complete` bila gerbang
SDT belum dijalankan; jangan pakai angka provenans "pemasok" sebagai dasar keputusan.
Revisi: v1.1.0 (2026-09-01, SM-2 t_4cc4e6b9) - section GSP-SDT + gerbang pra-terbit (langkah 18).
Revisi: v1.5.0 (2026-09-07, controller DEVNOTES-REV-0709) - pitfalls gerbang bentuk docx (sectPr/grid/Caption/TOC/footer C-22/penanda D16) + scan rahasia tanpa git diff + pemulihan klausa saat hapus paragraf.
- Em-dash U+2014 DILARANG MUTLAK tanpa pengecualian (D17); middle dot U+00B7 dilarang dengan pengecualian hanya string blok terkendali yang meniru master design verbatim. Berlaku atas seluruh teks keluaran; definisi + prosedur scan: `gsp-document-quality-standards/references/gsp-sdt/README.md` (bagian Aturan teks keluaran D15+D16).

## When to Use
- User meminta "kajian komprehensif", "tinjauan lengkap", "audit sistem",
  "uraikan setiap X dengan lengkap", "semua file dan file pendukung",
  "tanpa ada satupun yang tersisa", dan hasil akhir berupa **Word Docs**.
- Inventarisasi apa pun yang harus enumerasi **semua** item + file pendukung.
- Laporan yang butuh tabel besar hasil generate (mis. tabel 40 profil).

## Prinsip user (GSP) - JANGAN ditawar
1. **Kelengkapan total**: jangan potong deskripsi/When-to-Use; cantumkan
   SEMUA file (SKILL.md, LICENSE, README, scripts, templates, references,
   assets, __pycache__/*.pyc) dengan ukuran; lampirkan isi penuh di dokumen
   terpisah bila terlalu besar; arsip zip file asli agar "tidak ada yang
   tersisa".
2. Bahasa Indonesia untuk narasi; istilah teknis tetap Inggris.
3. Klaim harus dari data live terverifikasi (tool output), bukan memori.

## Workflow

### 1. Jejak orkestrasi (WAJIB - gsp-orchestration-execution)
- Buat kartu kanban kontrak per subtask SEBELUM eksekusi:
  `hermes kanban --board default create "<judul>" --body "<output+verify>" --assignee brahma --priority 1 --json` (create mendukung `--json`).
- ⚠️ **PITFALL**: `hermes kanban complete <id> --result "..." --json` **GAGAL**
  (usage error - `complete`/`block` tidak punya flag `--json`). Pakai tanpa
  `--json`: `hermes kanban --board default complete <id> --result "bukti"`.
- Tulis contract doc di `workspace/gsp-hermes/workspace/docs/<YYYY-MM-DD>-<slug>.md`
  berisi tabel kartu (id/title/assignee/dep/status/bukti) + data kunci + verifikasi.

### 2. Pengumpulan data (read-only, langsung)
- Batch perintah independen dalam satu turn (terminal/read/curl).
- Service HQ (9011) & WebUI (9012) **HTTPS self-signed** → `curl -sk`; probe
  http:// tanpa `-k` mengembalikan kosong (JSONDecodeError char 0).
- Dashboard Hermes = `hermes dashboard --port 9010`; cek `hermes profile list`,
  `hermes kanban --board default list --json`, `cronjob list`, `docker ps`,
  `netstat -ano | grep LISTENING`, `tailscale status`.
- DB: query via file skrip (jangan heredoc/one-liner raksasa - parser
  memblokirnya; jika kena blok, jalankan file tersimpan
  `bash .../blocked-scripts/blocked-*.sh`, atau pakai node pg dari
  `gsp-datacenter/hermes-bridge/node_modules`, atau tulis .py kecil).
- Simpan hasil terstruktur ke JSON (mis. `skills_catalog_raw.json`) agar
  kompilasi berikutnya programatik dan tidak hilang di konteks.

### 3. Sintesis markdown (sumber kebenaran)
- Struktur laporan (16 bab, terbukti disukai user):
  Ringkasan Eksekutif → Metodologi → Peta Arsitektur/Diagram → Node Inti →
  Komponen (per sistem: stack, halaman, API, model data, alur) → Fleet/Tabel →
  Skill → Knowledge/Memory → Infrastruktur → Workflow → Keamanan/RBAC →
  Status Live Saat Audit → Temuan/Risiko (tabel #/dampak/tingkat) →
  Rekomendasi (A..E) → Lampiran (perintah verifikasi, inventaris, env keys).
- **Tabel besar yang digenerate** (40 profil, 130 skill): tulis markdown dengan
  placeholder `{{PROFILES_TABLE}}`, lalu inject via script python yang membaca
  data live - jangan mengetik 40 baris manual (rentan salah).
- Sertakan tabel "Status Live" + "Temuan" + "Rekomendasi" - user menilai
  laporan dari bukti nyata.

### 4. Konversi markdown → Word
- Pakai [`scripts/build_md_to_docx.py`](scripts/build_md_to_docx.py) (salinan di skill ini):
  `python build_md_to_docx.py <src.md> <out.docx> "<TITLE>" "<SUBTITLE>" "<META>"`
- Konverter: A4, blok judul custom, mapping heading H2→Heading 1 dan H3→Heading 2
  (H1 markdown = judul, dilewati otomatis), tabel dengan header shaded,
  code block berlatar abu, footer nomor halaman (field PAGE).
- Untuk dokumen raksasa (>1 MB isi penuh): Word memuat dossier/ringkasan;
  lampiran isi penuh tetap di markdown; file asli di zip.

### 5. Verifikasi (WAJIB sebelum klaim selesai)
- `python docx_validate.py <out.docx>` → `{"ok": true}`.
- `python docx_read.py <out.docx> --structure` → cek jumlah heading (H1/H2),
  tabel, paragraf; spot check 1 entri.
- Cross-check jumlah yang diklaim (mis. "130 skill", "160 file zip") dengan
  hitungan programatik - jangan "go with what I have".

### 6. Penyerahan
- Tabel inventaris artefak (docx, markdown, JSON, zip, contract doc, kartu
  kanban) + `MEDIA:<absolut path>` agar docx ter-render di WebUI.
- Tutup kartu kanban dengan bukti; perbarui contract doc.

## Katalog skill super detail (inventarisasi library skill)
- [`scripts/scan_skill_library.py`](scripts/scan_skill_library.py) - scan semua SKILL.md (registry + kanonik):
  frontmatter toleran (termasuk description blok `>-`), file tree LENGKAP
  (semua file + ukuran), When-to-Use penuh, hingga 25 perintah/tool dari code
  fences, body utuh → JSON + dossier + lampiran isi penuh + zip semua file.
- Format entri dossier (terbukti memenuhi "super detail"):
  Kategori/Lokasi, Metadata (versi/author/lisensi/platform), Tags,
  Deskripsi lengkap, Pemicu penuh, Struktur bagian (semua), Perintah/tool
  utama, File lengkap (path + ukuran), Ukuran body.
- Dedup nama antar root (registry vs kanonik) agar 130 bukan 142+; badge
  `*(kanonik EKAS)*` untuk entri kanonik-only.

## Pitfalls
- `hermes kanban complete`/`block` **tanpa** `--json` (lihat Workflow 1).
- Markdown H1 = title block → mapping heading di konverter.
- `curl http://localhost:9011` (tanpa -k/https) → body kosong, jangan salah
  baca sebagai "server down".
- Inline psql/heredoc raksasa diblokir parser terminal → tulis file skrip.
- `git diff --cached` pada stash berisi .docx memicu `astextplain`/docx2txt (tidak terpasang) + timeout → scan rahasia pra-commit pakai skrip Python yang baca berkas staged langsung (`git diff --cached --name-only` + regex), bukan lewat diff.
- Konverter MD→docx polos bisa LOLOS verifikasi isi tapi melanggar bentuk GSP-SDT (preseden DEVNOTES-0709, vonis user 'masih berantakan'): tabel grid > area teks meluber margin, heading tanpa nomor desimal C-13, TOC field tanpa entri cached, blok identitas bukan strip resmi, tanpa tabel revisi C-24, Calibri default. GERBANG BENTUK sebelum serah: probe XML (sectPr vs lebar grid; style Title/H1..H3/Caption terpakai; entri TOC; footer pola C-22). Pola rujukan: docs/2026-09-07-devnotes-revisi/ (process/b2/build_docx_revb.py + process/v2/check_revb.py).
- Style kapitel: semua paragraf 'Tabel ...' tepat sebelum <w:tbl> = style Caption asli Word, SATU aturan untuk kedua jalur render (baris bold MD vs peta penomoran); kalau tidak, sebagian terbit bergaya Body (preseden CHECK 7: 19/24).
- Scanner U+00B7 (C-2): PASS hanya bila 0 temuan ATAU berkas memuat baris 'Penanda D16:' (skop per berkas, terbaca dari lapisan XML docx) - byte dengan separator strip resmi wajib sertakan penanda itu.
- Lebar tabel: area teks = A4 11906 - left 1474 - right 1247 = 9185 twips; grid proporsional <= nilai itu; probe jumlah gridCol > area = defect rilis.
- Menghapus paragraf atas putusan user: sensus dulu klausa unik di dalamnya; bila tidak ada di tempat lain, gabungkan verbatim ke baris SUMBER kapitel terkait (preseden LA.2/LA.3 -> A.2/A.3), jangan biarkan informasi hilang.
- Jangan claim "semua profil punya .env" tanpa cek `os.path.exists` per profil.
- ROSTER HQ menyebut jumlah statis yang bisa kedaluwarsa - hitung dari source.
- Skill per-profil (`profiles/gsp-*/skills/`) adalah SALINAN registry/kanonik -
  jangan dihitung ganda dalam inventaris.

## Verification checklist
```
[ ] Kartu kanban dibuat sebelum eksekusi, ditutup dengan bukti
[ ] Contract doc di shared ws docs/
[ ] Semua klaim angka dari output tool live
[ ] docx_validate ok:true
[ ] docx_read --structure: heading/tabel/paragraf sesuai ekspektasi
[ ] Tidak ada deskripsi/When-to-Use yang terpotong
[ ] Semua file skill tercantum (SKILL.md + pendukung) di dossier
[ ] Lampiran isi penuh + zip untuk konten > ~500 KB
```

## File pendukung
- [`scripts/build_md_to_docx.py`](scripts/build_md_to_docx.py) - konverter markdown→Word (argv-driven).
- [`scripts/scan_skill_library.py`](scripts/scan_skill_library.py) - scanner inventaris skill super detail
  (dossier + isi penuh + zip).
- [`references/report-structure.md`](references/report-structure.md) - kerangka laporan kajian 16 bab + format
  entri super detail + contoh tabel Status Live/Temuan.
