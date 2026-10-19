---
id: wlp-pelajaran-objek-vs-content
type: pelajaran
title: Kelas cacat pembanding identitas mengoper OBJEK bukan CONTENT (misi WLP, DEV-F19-1)
status: active
sumber: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F19-walk.md
halaman: §5; CP-F20 §1-§3; CP-F23 §3
tanggal_akses: 2026-09-07
kelas_bukti: primer
sensitif: tidak
perkara: wlp
tags: [cacat, javascript, regresi, tdd, merah-hijau, wlp, brahma]
links: [wlp-angka-outline-window, wlp-pelajaran-blind-spot-instrumen]
penulis: gsp-librarian
diajukan: 2026-09-07
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-07
catatan_verifikasi: "Verdict: terverifikasi. Alasan spesifik: signature cacat tercetak verbatim di CP-F19 par.5 (baris terserve 446 '_excerptText(win[local]) !== entry.excerpt' vs definisi :90 penerima CONTENT; repr '[object Object]'; pembanding benar :603 '_excerptText(m.content)') dan direplikasi independen oleh controller di CONTRACT.md D-14(1); cermin server routes.py::_question_index_projection :9212 cocok CP-F20 par.2; uji varian populasi penuh 0/10+0/5 lawan 10/10+5/5 cocok CP-F19 par.5 dan CP-F23 par.3; tes merah-hijau tiga tes + guard tetap hijau + regresi 31 passed cocok CP-F20 par.3; grep pola cacat 0 sisa cocok D-15(1); gerbang md5 F21 (47d9b794 vs 4d396b43) cocok CP-F21 par.1; dampak biaya +19,0%/+24,5% cocok CP-F19 par.5 dan terhitung ulang. Batas berlaku ditulis jujur (instance tunggal scoped ke grep saat itu; generalisasi fail-closed ditolak eksplisit). Rekomendasi konkret: tidak ada perubahan isi; saat promosi bawa tautan silang ke wlp-angka-outline-window agar lesson dan bukti biaya terbit satu paket."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-07
dipromosikan-ke: pelajarans/wlp-pelajaran-objek-vs-content.md
---

# Kelas cacat pembanding identitas mengoper OBJEK bukan CONTENT (misi WLP, DEV-F19-1)

1. Signature cacat

1.1 Di WebUI Brahma, gerbang identitas halaman walk segmented membandingkan excerpt baris target dengan excerpt entri outline. Fungsi pembanding `_excerptText(content)` (static/outline.js:90) mengharapkan CONTENT pesan (string atau array part bertipe text), tetapi satu-satunya cabang walk mengoper OBJEK pesan utuh: `if (_excerptText(win[local]) !== entry.excerpt) return null;` (outline.js:446). Cabang non-array `String(content||'')` menghasilkan repr `"[object Object]"` (atau repr dict python pada jalur server) yang tidak pernah sama dengan excerpt entri -> identitas gagal mutlak -> fitur fail-closed diam-diam (DEV-F19-1) [R-1][R-2].

1.2 Pembanding benar ada di berkas yang sama: builder entri warisan memakai `_excerptText(m.content)` (outline.js:603); cermin server `api/routes.py::_question_index_projection` (:9212) juga mengoper `msg.get("content")`. Vonis kelas (find-fix-the-class): instance tunggal, grep pola `_excerptText(win[` tanpa `.content` = 0 sisa setelah tambalan [R-2][R-3].

1.3 Ironi kegagalan: desain fail-closed justru MENYEMBUNYIKAN cacat ini secara fungsional (pendaratan target tetap benar via jalur bare), sehingga hanya terlihat sebagai pemborosan biaya (+19,0%/+24,5%), bukan sebagai error. Fitur yang "aman saat rusak" hanya terdeteksi lewat pengukuran biaya atau uji deterministik gerbangnya [R-1].

2. Cara mendeteksi (resep terverifikasi)

2.1 Uji dua-arah merah-hijau di level logika: harness node vm mengeksekusi outline.js asli terhadap state sintetis; ekspektasi excerpt dihitung INDEPENDEN (bukan oleh fungsi produk). Sebelum tambal: tes merge FAILED (fail-closed ke bare, reproduksi persis); sesudah tambal: PASSED; dua tes guard (byte-honesty >160 baris; mismatch tetap ditolak) tetap hijau -> tambalan tidak membutakan guard [R-2].

2.2 Uji deterministik populasi penuh atas respons HTTP nyata: replika verbatim fungsi pembanding dijalankan ke dua varian argumen (objek vs .content) atas seluruh jendela walk: varian objek 0/10 dan 0/5 cocok; varian .content 10/10 dan 5/5 cocok. Ini memvonis akar tanpa menunggu bug muncul di UI [R-1][R-4].

2.3 Gerbang buka pengukuran: md5 berkas terserve == md5 disk dicetak sebelum mengukur, agar vonis ditujukan ke artefak yang benar (kasus nyata: F21 menutup sah sebagai partial karena md5 terserve masih pra-tambalan 47d9b794, bukan 4d396b43) [R-5].

3. Register rujukan

- R-1: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F19-walk.md §5 (baris terserve, repr "[object Object]", uji varian A/B populasi penuh, dampak biaya).
- R-2: checkpoints/CP-F20-fixdev19.md §1-§3 (diff 1 baris :446, scan kelas, tes merah-hijau 3 tes + regresi 31 passed).
- R-3: CONTRACT.md Decision Log D-15 butir (1) (grep controller: 0 sisa pola cacat).
- R-4: checkpoints/CP-F23-rewalk.md §3 (varian B proved 10/10 + 5/5 atas berkas terserve terverifikasi).
- R-5: checkpoints/CP-F21-reverify.md §1 (gerbang G1 FAIL terukur, md5 47d9b794).

4. Batas berlaku

4.1 Vonis instance tunggal berlaku untuk berkas dan pola panggilan yang di-grep saat itu (outline.js @5d5264d + cermin routes.py); kode pasca-fe71a74 belum diaudit ulang untuk pembanding identitas serupa di modul lain. Generalisasi "semua fail-closed menyembunyikan cacat" terlalu kuat - yang terbukti: fail-closed yang benar hasilnya membuat cacat identitas tidak terdeteksi oleh uji fungsional biasa, sehingga butuh uji deterministik gerbang.
