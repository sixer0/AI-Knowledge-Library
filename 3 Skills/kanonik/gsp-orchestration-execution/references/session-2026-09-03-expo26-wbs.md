# Sesi EXPO26-WBS (2026-09-03) - Standard Design Workbook DATUM + Merge Komprehensif

Misi: dua workbook hasil crawling di `EXPO [2026]` (katalog 325 expo + pendalaman 11.620 exhibitor 6 expo) digabung jadi satu workbook komprehensif + standard design acuan + template. TUNTAS: 20 kartu, VERDICT PASS AC-1..AC-18 + countersign SETUJU nol ketidakcocokan; changelog gsp-agent d2fd1e45 pushed. Kontrak: `docs/2026-09-03-expo26-workbook-standard/`.

## Alur yang terbukti bekerja
- RT -> TA -> (audit controller menemukan cacat) -> TA2 amandemen -> build -> reviewer kode -> verifier independen -> fix card -> countersign. Dua amandemen TA (TA2 untuk pasangan katalog, TA3 untuk grammar DATUM yang disuplai user di tengah misi) keduanya lewat kartu, bukan suntingan sepihak controller.
- Gate kekekalan saat restyle visual: ekstrak populasi DATA (locate header dari ISI), diff nilai+number_format+hyperlink terhadap baseline artefak versi lama = 0 beda SEBELUM artefak ditimpa. Pola ini menyelamatkan restyle besar (195.067 sel, 0 beda).
- Determinisme didefinisikan SETINGKAT SEL (bukan byte zip): dua jalan bandingkan nilai/format/hyperlink/urutan sheet/freeze/autofilter.
- Verifier dan countersign memakai TEKNIK BERBEDA (objek gaya openpyxl vs XML mentah sharedStrings) dan hasil silang identik = bukti ganda kuat.

## Temuan substantif
- D-C01: hanya 2 dari 6 expo pendalaman punya baris di katalog (MWC=EXPO-104 Urut_Prioritas 4; WRC=EXPO-086 pd 236). Aturan pasangan jujur: hyperlink silang hanya untuk pasangan sah; 4 lainnya teks "di luar katalog 2026" + blok peta silang berlabel turunan. Dilarang menambah baris katalog karangan (menuntut penilaian rubrik baru = di luar lingkup RT).
- Angka CONTOH di blueprint bisa salah meski aturannya benar (13/291 vs aktual 4/236) dan menular ke dokumen turunan (D1). Verifier wajib menguji ATURAN dengan hitung ulang, bukan menguji angka contoh mentah.

## PITFALL baru (WAJIB dicek di sesi mendatang)
1. **needs-review bridge-tanpa-result berulang** (S1, S4, RA): bridge menutup request `needs-review` dengan result kosong padahal pekerja SELESAI dan artefak ada. Jalur resmi: PATCH force-done oleh asignor (x-internal-secret, dengan izin pemilik atas kredensial itu) HANYA setelah controller mengukur artefak sendiri; jangan pernah percaya summary.
2. **Request `failed` zombie tidak bisa force-done via API** ("cannot force-done a failed request"). Kasus: bridge restart saat proses berjalan -> worker sudah menulis artefak lengkap + kartu kanban done, tapi AgentRequest failed permanen. Rekonsiliasi cukup di contract doc Decision Log + kartu kanban done; jangan dispatch ulang buta (aturan user: audit kelengkapan artefak dulu).
3. **Penghitung baris offset-asumsi memberi false-MISMATCH** pada sheet warisan ber-baris judul (+1). Pola benar: locate baris header dari ISI kolom kunci, lalu hitung non-kosong setelahnya. Salah satu verifier nyaris FAIL artefak karena ini.
4. **Konstanta uji mati pada gerbang terbit KENDALI** membuat bendera "OK TO ISSUE" mati permanen (target 53.138/13.925 tidak bersumber; aktual 52.975/12.270). Aturan: target uji KENDALI WAJIB dihitung skrip dari populasi saat build + assert penjaga, bukan diketik.
5. **Glif/provenans harus run rich text Mono** (CellRichText + InlineFont) bila menyatu prosa; font per-sel saja tidak cukup dan scanner XML membacanya dari sharedStrings. Preseden: perbaikan F1 (contoh) dipakai ulang oleh RF1 (D3).
6. **Whitelist U+00B7/glif harus menyebut POSISI** (baris meta kepala, pita klasifikasi, judul tracked, kolom PROV, legenda PETUNJUK). Salinan legenda di tempat lain (COVER template) tertangkap scanner sebagai pelanggaran - buang duplikatnya, jangan perluas whitelist tanpa keputusan tercatat.
7. **String verbatim DATUM mengandung em dash** (ISSUE "// ... ID T — Terbitan 1", label "TIER 1 — PRIORITAS PUNCAK", bendera "LULUS — OK TO ISSUE"): ini kutipan verbatim dari exemplar user, diizinkan oleh STANDAR DATUM; scanner gerbang naturalisasi wajib memisah populasi "verbatim DATUM" vs prosa baru, dan melaporkan hitungannya (contoh: 5 em dash, semua verbatim).
8. **Body kartu yang disalin dari bacaan read_file membawa nomor baris** "N|" - kalau dipakai menulis ulang berkas, berkas rusak. Selalu tulis ulang dari sumber diketahui, jangan dari render bernomor.
9. **Watcher node inline via terminal() dengan nested quotes sering patah** ("syntax error at end of input") dan pesan redaksi sistem membuat subshell `$(...)` gagal. Pola baku: tulis berkas .cjs di $LOCALAPPDATA/Temp lalu jalankan background.
10. **`git add <direktori>` di repo mirror hermes-home menyapu semua untracked** (03-09: commit RULE SOUL ikut 9.980 berkas Temp/backup/skill yang menggantung di working tree; tidak merusak tapi jejak kotor). Pola baku: `git add -- <path-eksplisit-satu-per-satu>` atau daftar path via file+xargs; cek `git status --short | wc -l` sebelum add. Guard sisip-murni SOUL terbukti: `t2.replace(BLOCK,"",1)==t` (hapus blok = teks asli persis), idempoten (jalankan ulang skip 55).

## Penanda lingkungan
- Font DATUM tidak tertanam di xlsx/docx; mesin pembaca pasang dulu Font_DATUM (PASANG-DULU.txt). Verifikasi token membaca nama font dari XML, tidak bergantung rendering.
- Salinan berkas untuk tautan MEDIA tidak boleh mengandung spasi/[ ] di nama folder: gunakan folder handover tanpa spasi di docs kontrak atau salinan Expo-AI.
