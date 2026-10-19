---
name: gsp-tool-batching
description: "Aturan batching tool call: kirim beberapa tool call independen dalam SATU giliran (reads, pencarian, web_extract multi-URL) dan serialisasi hanya saat ada ketergantungan. Muat saat merencanakan giliran kerja dengan >=2 kemungkinan tool call."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
metadata:
  hermes:
    category: orchestration
    tags: [gsp, workflow, batching, throughput]
---

# Tool Batching - Beberapa Tool Call dalam Satu Giliran

Kebijakan fleet PUTUSAN USER D-08 (misi OPT-WF-0907, 08-09-2026). Runtime engine
sudah mengeksekusi batch tool call secara konkuren (paralel-safe, path-scoped);
pembatas nyata adalah seberapa sering MODEL emisi batch, bukan runtime. Fraksi
dasar giliran multi-call worker saat skill ini ditulis: 18%. Target: naik.

## Aturan inti

Sebelum mengirim giliran, tanya: "apakah hasil call B saya butuhkan untuk
menentukan argumen call A?" Jika TIDAK, keduanya satu giliran. Jika YA, baru
serialisasi.

BATCH dalam satu giliran (independen):
- Baca beberapa berkas berbeda (`read_file` x2-x4 path berbeda).
- Cari beberapa hal berbeda (`web_search` multi-query, `search_files` beberapa pola).
- `web_extract` beberapa URL sekaligus (helper sudah menerima list URL).
- Inspeksi silang dua salinan berkas (kanonik vs registry, profil vs fleet).
- Lookup independen: `skill_view` + `read_file` + `search_files` untuk tiga hal tak terkait.

WAJIB SERIAL (jangan batch):
- Call berikutnya memakai HASIL call sebelumnya (grep dulu, lalu baca file yang ketemu).
- Tulis ke path yang sama/berurutan: `patch`/`write_file` lalu verifikasi isi file itu.
- Perintah terminal destruktif atau stateful (install lalu build, migrate lalu test, rm lalu ls hasil).
- Edit berantai pada SATU file (edit kedua bisa menabrak konteks edit pertama).
- Aksi browser berurutan pada satu halaman (klik lalu baca hasil navigasi).

## Batas

- Maksimal 6 call per batch; 2-4 adalah zona manis. Batch besar memperbesar
  dampak kegagalan satu call dan menyulitkan pembacaan log.
- Hormati barrier bawaan runtime: navigasi + wait_for_load tetap satu paket;
  jangan paksakan parallelisme pada alat yang kontraknya sekuensial.
- Setelah batch selesai, baru ambil keputusan yang bergantung pada gabungan hasilnya.

## Contoh pola (giliran worker nyata)

Pola 1 - audit salinan skill (3 call, 1 giliran):
```text
read_file(kanonik/SKILL.md, limit=15)   # header+versi
read_file(fleet/SKILL.md, limit=15)     # header+versi
read_file(profil/SKILL.md, limit=15)    # header+versi
```
Giliran berikutnya (tergantung hasil): bandingkan versi, lalu patch bila drift.

Pola 2 - riset awal (3 call, 1 giliran):
```text
web_search("topik A")
web_search("topik B")
read_file(notes_eksisting.md)
```
Giliran berikutnya: web_extract URL terpilih dari hasil (URL bergantung hasil, jadi serial).

Pola 3 - pra-edit multi-file (2 call, 1 giliran):
```text
read_file(config.yaml)
read_file(script.py)
```
Lalu serial: patch config -> patch script -> jalankan test (rantai sebab-akibat).

Anti-pola: `web_search` lalu `web_extract` hasil pencarian di giliran yang sama
(argumen extract belum ada); `write_file` lalu `read_file` file yang sama untuk
"verifikasi" di giliran yang sama (verifikasi membaca state pra-commit tool).

## Biaya dan manfaat

Batching tidak mengubah total call kerja yang sama; ia memangkas GILIRAN
(round-trip model), sehingga run lebih cepat dan anggaran iterasi LAD bertahan
lebih jauh. Jangan mengarang call pengisi hanya supaya terlihat batch - setiap
call harus punya tujuan kerja.

## Distribusi (catatan Skill Manager)

Pembaca sasaran: SEMUA lane pekerja. Mekanisme distribusi terpilih: blok pendek
"Tool Batching" di `gsp-verification-before-completion` (skill ALWAYS LOAD fisik
di seluruh profil pekerja) sebagai pointer wajib, skill ini sebagai rujukan
lengkap di registry fleet. Profil yang butuh lebih: minta promosi ALWAYS-LOAD
ke gsp-skill-manager.
