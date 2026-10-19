---
name: gsp-webui-verification
description: "Verify GSP web UIs via headless Chromium, UX-first."
version: 1.0.0
author: Brahma (GSP)
license: MIT
platforms: [windows]
metadata:
  gsp:
    category: gsp
    tags: [gsp, webui, verification, ux, headless, playwright, information-library, https]
---

# GSP WebUI Verification — render-check & UX review (human-first)

Gunakan saat perlu **memverifikasi tampilan/perilaku** halaman GSP web UI —
Agent HQ (`gsp-datacenter`, https://localhost:9011) atau Brahma WebUI
(`gsp-brahma`, https://localhost:9012) — atau saat menilai **UX** sebuah
halaman dashboard/library. Keduanya HTTPS **self-signed**.

## Aturan emas (standar user, non-negotiable)

> **"ASUMSIKAN KAMU MANUSIA, BUKAN MESIN."**

- Nilai dari **apa yang dilihat manusia di halaman pertama**, bukan dari
  "semua API 200".
- **Pengetahuan penting tampil dulu; raw/dump di belakang** — user tidak
  boleh memilah informasi lagi.
- **TIDAK BOLEH ADA JALAN PINTAS**: klasifikasi/knowledge harus berasal dari
  analisa konten konkret, bukan heuristik path/nama folder.
- Pipa IL GSP: **WORKSPACE = raw · VAULT = analisa (skoring/filtrasi/dedup/
  clustering/decompose/metadata/grouping) · WIKI = paling berharga**. Raw
  TIDAK pernah diangkat jadi knowledge tanpa melewati vault→wiki.

## Metode render-check (tanpa daemon browser)

Browser daemon (`browser_exec`) bisa macet di halaman HTTPS self-signed
(timeout 420s). Jangan andalkan daemon untuk HTTPS — pakai **headless
Chromium via Playwright langsung dari terminal**:

1. Browser Playwright sudah ter-install di
   `C:/Users/TRIAL/AppData/Local/ms-playwright/chromium-<rev>/chrome-win64/chrome.exe`.
   Cek dulu `find` untuk dapatkan `<rev>` yang ada (mis. chromium-1228).
2. `pip install playwright` (paket Python kecil; browser TIDAK perlu
   di-download ulang).
3. Launch dengan `executable_path=` menunjuk binary yang ADA — versi pip
   playwright bisa minta build yang beda (mis. minta 1234 padahal ada 1228),
   dan `executable_path` menghindari download/error "Executable doesn't exist".
4. `context(ignore_https_errors=True)` + launch arg `--ignore-certificate-errors`.
5. `goto(wait_until="networkidle")` + `wait_for_timeout(2000)` — cukup untuk
   React client app fetch data.
6. Baca: `page.inner_text("body")`, `page.evaluate` (daftar button/teks),
   `page.screenshot(path=...)` untuk user (MEDIA:C:/path/ke/gambar.png).
7. Untuk interaksi: `page.evaluate` klik elemen pertama yang teksnya cocok,
   tunggu, baca ulang — verifikasi drill-down benar-benar berubah state.

Script siap pakai: `scripts/render_check.py` (dump teks + screenshot).
Catatan Windows: jalankan python dengan path `C:/...`, bukan `/c/...`; file
kerja simpan di workspace (`C:/Users/TRIAL/workspace/`), bukan `/tmp`.

## Checklist UX (verifikasi ala manusia)

- [ ] **Halaman pertama**: yang tampil = knowledge terdistilasi (wiki/vault/
      insight), bukan dump raw (file report/checkpoint/progress agent).
- [ ] **Cari topik** (mis. "ADINT"): hasil dikelompokkan domain→project,
      knowledge wiki muncul pertama; raw hanya via scope Arsip.
- [ ] **Hitung masuk akal**: jumlah "project" mencerminkan folder asli
      (puluhan), bukan ratusan dari inferensi path.
- [ ] **Filter berfungsi**: chip domain→project cascading; status vault
      bisa diklik; clear filters mereset semua; toggle tidak ada yang mati.
- [ ] **Drill-down**: klik domain → project → dokumen benar-benar berubah
      state (cek innerText/DOM, bukan hanya HTTP).
- [ ] **Tidak ada duplikasi klasifikasi**: dokumen dalam project ber-type
      document, bukan fact/decision/lesson.

## Pitfall & pelajaran (dari insiden nyata)

- **Jangan menilai dump legacy sebagai "sampah"** — itu riwayat siklus
  orkestrasi penuh; nilainya muncul SETELAH analisa (vault/wiki), bukan
  dengan disembunyikan. Sembunyikan = jalan pintas; analisa = benar.
- **Jangan buat entri knowledge sintetis dari file raw** (mis. entri "cycle"
  dari classification.json) — itu mengangkat raw tanpa analisa dan melanggar
  pipa IL. Klasifikasi ditulis librarian lewat analisa konten → vault.
- **Jangan hanya perbaiki chip/filter** saat user bilang "standarisasi gagal"
  — akar masalah biasanya model data/klasifikasi, bukan kosmetik.
- Verifikasi via bundle terkompilasi + API nyata + headless render saat
  daemon macet — dan katakan jujur mana yang tidak bisa diverifikasi.

## Referensi

- `references/il-knowledge-first.md` — arsitektur Information Library
  knowledge-first + pola rebuild atomic (dispatching per folder, monitor,
  verifikasi 100% coverage).
