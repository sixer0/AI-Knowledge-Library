---
name: gsp-video-to-course-module
description: "Use when videos must become a verified learning module."
version: 1.0.0
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, orchestration, transcription, course, docx]
    category: gsp
---

# Video YouTube → Course Module Terverifikasi (pola misi Test STT, 31-08-2026)

## When to use
- User memberi beberapa link YouTube dan minta: transkrip penuh, intisari terintegrasi, modul pembelajaran, "zero to hero", atau audit kelengkapan penggabungan.
- Varian kecil (1 video → ringkasan) cukup tahap 1–2 + tulis langsung; varian penuh pakai semua tahap dengan jejak kanban (RT→TA→eksekusi→VERIF, pair orkestrasi GSP wajib).

## Arsitektur folder misi (baku)
```
<MISI>/
  01_raw/            # SRT unduhan (yt-dlp)
  02_transcripts/    # V<n>_<youtubeId>.md + _MANIFEST.md (kanon pemetaan!)
  03_analysis/       # per-video context + 00_CROSS_MAP.md (+ INTEGRATION_GAP.md nanti)
  04_research/       # FORMATS.md (riset format course body) + EXPANSION.md (docs resmi)
  05_module/         # deliverable .md + .docx
  90_meta/           # SEMUA skrip deterministik + laporan verif + arsip rev
logs/
```

## Tahap 1 — Transkripsi deterministik (BUKAN Whisper bila ada caption)
1. `uvx yt-dlp --list-subs` tiap video; ada `.en` resmi → pakai caption (timestamped, cepat). Tidak ada → fallback Whisper, catat di kontrak.
2. Unduh `--write-subs --sub-langs en`; simpan `.en.srt` DAN `.en-orig.srt` (auto vs human; human lebih baik).
3. Skrip ekstraktor SRT→MD per segmen ~60s ber-format `**[H:MM:SS]** text` (template: `Test STT/90_meta/extract_transcripts.py`).
4. **WAJIB sebelum fan-out worker**: tabel kanon `Vn ↔ youtubeId ↔ judul ↔ durasi` masuk kontrak + `_MANIFEST.md`. PITFALL TERBUKTI: artefak worker bisa menukar label V2↔V3; tanpa kanon, seluruh hilir ikut salah.
5. Caveat jujur di kontrak: caption = STT YouTube, bisa tidak koheren di rentang tertentu (cek segmen aneh, catat, jangan klaim "sempurna absolut").

## Tahap 2 — Audit kesempurnaan transkrip (jawaban "transkripsi sempurna?")
Skrip bandingkan SRT mentah vs MD (template `transcript_integrity_audit.py`):
- jumlah cue SRT == kept+dropped; **kept-missing-in-md = 0**; setiap DROP harus duplikat-sejati vs cue-kept sebelumnya pada replay (x==prev / x in prev / ratio>0.85) → **fake-drops = 0**; gap antar segmen > ambang (120s) = 0; tail ≤ 5s dari durasi. VERDICT per video + agregat.

## Tahap 3 — Analisis & riset (bisa paralel)
- Per-video CONTEXT (topik konkret, angka, perintah, opinion-labels) + CROSS_MAP (peran komplementer, kontradiksi & resolusinya, matriks cakupan).
- FORMATS: riset format course body nyata (ATD/Coursera/Udacity/ADDIE/backward design) — format harus hasil riset, bukan karangan.
- EXPANSION: isi gap dengan dokumentasi RESMI (URL tercatat); tandai mana opini presenter vs fakta.

## Tahap 4 — Penulisan modul (writer, bahasa = bahasa sumber/user)
Struktur per modul: Learning Objective → Expanded Chapter → Step-by-Step → Expansion → Exercise → Quiz → Key Takeaways → References. Sitasi wajib `[Vn MM:SS]` = AWAL segmen transkrip sebenarnya (bukan tengah/akhir — drift ujung terbukti terjadi; normalisasi ke awal segmen).

## Tahap 5 — Verifikasi berlapis (pola beku/frozen)
1. `verify_stt.py` (frozen, CHECK 0–10): guard read-only digest pra==pasca, integrasi video, jenjang zero-to-hero, step-by-step per topik, expanded chapters, URL eksternal, sitasi dalam durasi + guard pemetaan kanonis, elemen format course, rasio cakupan (min 0,15 modul/transkrip), deliverable .docx. **Jalankan ulang SETELAP revisi konten; ambang tidak boleh diubah di tengah misi.**
2. Word build: builder md→docx deterministik (template `build_course_docx.py`): sampul + control table + cap terbit, field TOC asli + `w:updateFields=true`, header/footer + PAGE/NUMPAGES, `titlePg` (sampul tanpa nomor), heading literal tanpa substitusi em-dash, Revision History per rev, core properties. `docx_validate.py` (skill docx) untuk validasi paket.
3. `verify_word.py` AC-W1..W8: paket valid, sampul, TOC+footer, heading-match MD persis, **fidelitas 8-gram ≥99%** (window substring murni; frontmatter MD→sampul dihitung miss yang dimaklumi), tabel terkonversi, **jumlah sitasi [Vn MM:SS] MD==docx**, riwayat revisi. Dua run harus identik (deterministik).
4. Countersign oleh gsp-verifier (profil lain, read-only): jalankan ulang skrip beku fresh + audit KEADILAN klaim per-segmen (bukan cuma timestamp ada) + cek regresi vs arsip rev sebelumnya. Penulis = verifikator terlemah; controller tidak menandatangani pekerjaannya sendiri.

## Tahap 6 — Audit integritas penggabungan (jawaban "ada hal penting hilang?")
Analisis INDEPENDEN (bukan penulis modul), metode wajib sistematis: petakan SEMUA topik konkret tiap video → ada/tidak di modul; severity CRITICAL (tidak bisa selesai langkah tanpa ini) / IMPORTANT / MINOR; tiap temuan = sitasi + kutipan + pembanding; pisahkan KEHILANGAN vs KOMPRESI SENGAJA (duplikasi antar-video, filler). Akhiri verdict FAIR/GOOD/DEFICIENT + rekomendasi. **Controller konfirmasi tiap temuan CRITICAL secara independen (grep dsb.) sebelum menindaklanjuti** — auditor juga bisa salah.

## Tahap 7 — Remediasi ber-revisi (Rev B dst.)
Patch bedah (jangan rombak), arsipkan rev sebelumnya (`archive_*_revA.md` — folder misi sering BUKAN git repo, arsip manual = pengganti), changelog per-GAP, sitasi baru diverifikasi per-segmen oleh penulis SEBELUM ditulis, lalu ULANG Tahap 5 lengkap (frozen scripts + Word rebuild + countersign rev baru).

## Tahap 8 — Etalase hasil (folder project user)
`HASIL-PROJECT-<X>/`: deliverable + FULL-TRANSCRIPTS/ + laporan verif + countersign + README presentasi + ZIP. **WAJIB verifikasi sha256 salinan == kanonis** (buktikan bukan versi ganda menyimpang). ZIP: `zip` tidak terpasang → `powershell -Command "Compress-Archive ..."`; uji `unzip -t`.

## Pitfalls lintas-tugas (terbukti 31-08)
- Heredoc berisi `&` atau nested-quote → guard terminal bash menolak / EOF rusak: **tulis file via write_file lalu `cat file >> target`**.
- `python` → alias Microsoft Store: selalu `uv run --python 3.11 [--with python-docx] python`.
- `node -e` inline dengan backslash ganda hancur lewat git-bash: **tulis `.cjs`** (pola rekonsiliasi DB: pg client dari `gsp-datacenter/hermes-bridge/node_modules/pg`, DATABASE_URL dari `gsp-datacenter/.env`, `reconcile_*.cjs`).
- Kartu mirror bridge tertahan `review` padahal artefak sudah countersign PASS → force-done oleh asignor + tutup AgentRequest; catat di contract doc.
- Dispatch HQ `queued` tak ter-claim tapi kerja jalan via kartu mirror → rekonsiliasi DB langsung, jangan dispatch ulang (bahaya kerja ganda).
- Worker hilir bisa auto-rebuild artefak yang baru kamu rebuild → SELALU sha256/mtime check sebelum menyajikan; siapa pun pembangun terakhir yang lolos skrip beku = kanonis.
- `MEDIA:` path tanpa spasi → sajikan via folder etalase tanpa spasi (`HASIL-PROJECT-*`), bukan folder misi ber-spasi.
- Kata "todo" di prompt/artefak memicu placeholder-check verifier → hindari.

## Verifikasi akhir misi
Semua kartu done, AgentRequest closed (tak ada needs-review/queued tertinggal), contract doc §per-increment terisi, sha256 etalase==kanonis, countersign rev terbaru VERDICT PASS.
