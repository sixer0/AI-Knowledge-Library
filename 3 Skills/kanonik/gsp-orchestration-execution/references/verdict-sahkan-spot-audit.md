# Controller Sahkan Vonis Verifier: Spot-Uji Mandiri + Audit Mtime (validated WF-CRAWL-0911, 11-09)

Aturan 8 (claim ladder) menuntut "controller's own independent artifact
measurement" sebelum L2. Lima pola yang terbukti bekerja di misi WFCRAWL-0911:

## 1. Spot-uji mandiri atas gerbang deterministik verifier
Jangan telan `VERDICT: PASS` bulat-bulat; ulang SENDIRI sebagian kecil CHECK
kunci terhadap keadaan hidup, lalu laporkan kecocokannya. Yang diuji controller
(gate CS-1..CS-8 verifier PASS 8/8):
- KONTROL MERAH API: `POST /v2/crawl {"url":...,"maxDepth":1}` -> harus 400
  `unrecognized_keys` (bukti norma "body ditolak" nyata, bukan tulisan skill saja)
- KONTROL HIJAU: body `{url, limit}` -> success true + id async
- CS config: `grep search_backend|extract_backend` langsung di config.yaml 2 profil
- CS register engine: `engines=mojeek` -> 0 hasil (konsisten vonis MERAH senyap)
Skrip spot cukup 1 berkas .py/.sh di Temp; tempel hasilnya di Decision Log §5
kontrak, bukan hanya chat.

## 2. Run verifier yang cacat alat = INVALID berlabel, bukan FAIL artefak
Run-1 verifier WFCRAWL FAIL palsu di CHECK 1/3 karena bug PARSER ALATNYA
sendiri (regex blok YAML menyantap newline; regex seksi berhenti di fence
code-block sebelum payload). Jalur benar yang dijalankan verifier (jadikan
norma di prompt kartu verifikasi): tambal alat, jalankan ulang, ARSIPKAN
run-1 dengan prefix `INVALID-run1-alat-cacat-` + catatan kepala kenapa tidak
sah; vonis resmi = run berikutnya. Controller: cek laporan INVALID ada di disk
dan alasannya masuk akal - kegagalan alat bukan cacat artefak, dan jejaknya
tidak boleh dihapus diam-diam. Beda kelas dengan FAIL artefak (-> kartu FIX
scoped).

## 3. Audit klaim anti-blind pakai MTIME DISK, bukan cap waktu naratif
Standar user 02-09: rubrik/ambang dikunci SEBELUM hasil. Klaim seperti
"rubrik dikunci 16:20, eksekusi 16:25-16:40" WAJIB diuji dengan
`ls -la --time-style=full-iso` atas rubrik, output mentah, dan laporan:
- urutan sah bila mtime(rubrik) <= mtime(bukti mentah) <= mtime(laporan)
- WFCRAWL: rubrik 15:34:00 < bench.out 15:39:23 < BENCHMARK.md 15:39:51 = SAH
- Temuan nyata: cap waktu NARATIF di kepala dokumen bisa mundur/terbalik dari
  jam dinding (dokumen menulis 16:20/16:30 padahal dinding 15:43). Vonis tidak
  berubah karena urutan terbukti mtime, tapi ini cacat label: tempel ke kartu
  verifier berikutnya (komentar papan) agar dokumen dikoreksi capnya TANPA
  menyentuh bukti mentah. Include instruksi "uji urutan pakai mtime, bukan
  klaim kepala dokumen" di badan kartu verifikasi kelas benchmark.

## 4. Verifikasi klaim pitfall library lewat introspeksi signature
Bila skill/resep mengklaim argumen tertentu TIDAK sah di versi terpasang
(case: `cache_buster` bukan argumen `CrawlerRunConfig` crawl4ai), uji langsung
di venv produksi: `inspect.signature(Kelas.__init__).parameters` -> cek key
ada/tidak. Murah, deterministik, dan membuktikan tulisan skill terhadap versi
yang benar-benar terpasang (bukan versi PyPI terbaru).

## 5. Sensus distribusi versi lewat jalan-penuh
Sebelum sahkan kartu distribusi: `find "$LOCALAPPDATA/hermes/profiles" -path
"*/<skill>/SKILL.md"` + grep `^version` per salinan + sha256 tiga lapis
(kanonik/fleet/profil) harus identik. Jangan pakai glob `profiles/*/skills/gsp*/`
saja - struktur salinan bervariasi (ada `skills/gsp/<skill>`, ada `skills/<skill>`);
find penuh adalah alat ukurnya.
