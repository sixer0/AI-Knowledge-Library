# Auditing Synthesis Integrity — multi-sumber ke satu deliverable (validated 2026-08-31, misi STT Hermes module)

Saat deliverable = sintesis N sumber (transkrip video, korpus dokumen), audit DUA batas sebelum mengklaim lengkap.

## Batas A — raw→extracted LOSSLESS (replay deterministik, bukan kesan)
Jalankan ulang logika dedup/filter extractor terhadap input mentah (mis. SRT cue list vs transkrip md):
- replay rule yang sama; setiap item yang DIBUANG harus terbukti duplikat sejati pada replay (`fake-drops=0`; bandingkan dengan cue-kept TERAKHIR saat replay, bukan pencarian balik di output)
- `kept-missing-in-output=0`, celah jeda maksimum (mis. gap>120s=0), tail coverage (detik terakhir input vs output)
- cetak per sumber: counts + PASS/FAIL + satu baris `VERDICT:` akhir. Skrip read-only, stdlib saja (`difflib.SequenceMatcher` untuk uji kemiripan duplikat).

## Batas B — extracted→synthesis GAP audit (analis independen)
Dispatch analis yang TIDAK menulis deliverable: petakan SEMUA topik/subtopik konkret tiap sumber ke ada/tidaknya di deliverable (grep kata-kunci + baca segmen), severity CRITICAL/IMPORTANT/MINOR. Aturan laporan:
- tiap temuan WAJIB sitasi [sumber timestamp] + kutipan pendek + apa yang deliverable katakan sebagai gantinya (atau 'tidak ada')
- bedakan SENGAJA dikompresi (duplikasi antar-sumber, filler) dari HILANG
- wajib ada seksi penyeimbang "aspek yang terkonfirmasi baik" (mis. rasio sitasi exact, kontradiksi diselesaikan bukan dirata-rata) — laporan tanpa penyeimbang cenderung over-negative
- akhiri tabel ringkasan per sumber + rekomendasi konkret + verdict FAIR/GOOD/DEFICIENT

## Peran controller saat menerima temuan
- JANGAN telan klaim CRITICAL analis bulat-bulat: konfirmasi ulang tiap temuan terhadap artefak aktual (grep/hitung independen). "Penulis = verifikator terlemah" berlaku juga untuk analis.
- Temuan terkonfirmasi → remediasi PATCH BEDAH (bukan rombak; gaya Rev lama dipertahankan), arsipkan artefak lama (folder non-git: `90_meta/archive_*_revA.md`), changelog per-GAP ditulis penulis (`REMEDIATION_LOG.md`).
- Setelah patch: rerun skrip verifier BEKU (ambang tidak diubah), naikkan label rev di builder presentasi (sampul + Revision History baris baru di atas baris lama), rebuild, countersign segar oleh verifier (audit keadilan klaim BARU terhadap sumber, bukan cuma keberadaan timestamp — skrip cek 'sitasi = awal segmen nyata' + spot-check makna).

## Kejujuran mutu sumber
Cacat ASR/caption YouTube (rentang tidak koheren) = caveat pada artefak sumber, bukan bug ekstraksi. Laporkan "lossless TERHADAP SUMBERNYA (caption resmi, bukan Whisper)" — jangan pernah klaim "transkripsi sempurna" absolut.

## Folder etalase / presentasi hasil
- Salinan deliverable ke folder presentasi WAJIB diverifikasi `sha256sum` == artefak kanonis sebelum mengklaim "hasil tersaji"; jangan pindahkan artefak kanonis (etalase = salinan + README).
- ZIP dibangun ulang tiap sinkron: `zip` tidak selalu ada di git-bash → `powershell -Command "Compress-Archive -Path '<dir>\*' -DestinationPath '<out>.zip' -Force"`, validasi balik dengan `unzip -l`.
- README etalase mencantumkan status rev + file verifikasi agar penerima bisa audit sendiri.
