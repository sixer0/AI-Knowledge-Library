---
id: promanual-korpus-register-1004
type: catatan
title: "Register Beku Pengetahuan PROMANUAL-1004: silsilah pin, cacah KL/NEG, gerbang rilis akhir"
status: active
sumber: docs/2026-10-04-prompt-manual/research/{R1,R2,R3,R4}/register-beku.md; docs/2026-10-04-prompt-manual/research/REFREEZE-LOG.md; docs/2026-10-04-prompt-manual/verification/gerbang-rilis-v4.md
halaman: register R1 207 brs, R2 333 brs, R3 434 brs, R4 430 brs (terukur giliran ini; basis split-newline+1, wc -l memberi 206/332/433/429; master 11.107 brs basis splitlines)
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: promanual-1004
tags: [promanual-1004, register-beku, silsilah-pin, gerbang-rilis, koreksi-append-only]
links: [docs/2026-10-04-prompt-manual/output/manual-master.md]
penulis: gsp-librarian
diajukan: 2026-10-05
misi: PROMANUAL-1004
kartu: t_c42af89f
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-05
catatan_verifikasi: "Verdict: terverifikasi. Alasan: sampling provenans lolos penuh pada giliran ukur custodian 2026-10-05 23:3x WIB. Pin sha16 lima berkas (R1 6d72c018bd10dee5, R2 54cc5ffe2824458a, R3 7a959ee9d65ee368, R4 6c131ccdb5189339, master f43fcf284adbeec3) dicocokkan ulang byte-level sha256[:16] dan identik dengan tercetak; ukuran 53.839/101.731/146.284/151.934/2.013.079 B cocok; cacah baris KL ber-anchor 151/229/331/334, NEG 10/49/61/46, KD 0/0/0/7 cocok, total 1.045+166+7 konsisten cetakan FIXD (REFREEZE-LOG baris 225: KL 1.045, URL primer 968, TERUKUR 952); rantai pin D-15 (2026-10-04 22:16, 59 diperiksa 59 diterima 0 ditolak) sampai run-4, run-5 FINAL, FIXD dengan guard difflib tepat 1 baris berubah + 1 sisipan terverifikasi di REFREEZE-LOG baris 196-219; gerbang rilis v4 CHECK 1-17 PASS, CHECK 8 NR delegasi DOKPDF, CHECK 18 NR tertutup PUTUSAN D-31 jalur (ii) terverifikasi di verification/gerbang-rilis-v4.md dan CONTRACT.md baris 259; refresh 13 butir, nol angka kolom terbit berubah, 11 terkonfirmasi ulang penuh ber-timestamp terverifikasi di research/refresh-sebelum-terbit.md baris 16-18; gerbang resweep kolom MCP dan prosedur citation_title N-08..N-10 terverifikasi di research/R3-vonis-lajur.md baris 74-75. Rekomendasi kurator (non-blocking, tanpa mengubah nilai): nyatakan basis cacah baris saat promosi karena 207/333/434/430 memakai konvensi split-newline-plus-satu sementara wc -l memberi 206/332/433/429, dan master 11.107 memakai splitlines; cukup tambah keterangan alat."
riwayat-catatan-verifikasi: "Verdict: terverifikasi. Alasan: sampling provenans lolos penuh pada giliran ukur custodian 2026-10-05 23:3x WIB. Pin sha16 lima berkas (R1 6d72c018bd10dee5, R2 54cc5ffe2824458a, R3 7a959ee9d65ee368, R4 6c131ccdb5189339, master f43fcf284adbeec3) dicocokkan ulang byte-level sha256[:16] dan identik dengan tercetak; ukuran 53.839/101.731/146.284/151.934/2.013.079 B cocok; cacah baris KL ber-anchor 151/229/331/334, NEG 10/49/61/46, KD 0/0/0/7 cocok, total 1.045+166+7 konsisten cetakan FIXD (REFREEZE-LOG baris 225: KL 1.045, URL primer 968, TERUKUR 952); rantai pin D-15 (2026-10-04 22:16, 59 diperiksa 59 diterima 0 ditolak) sampai run-4, run-5 FINAL, FIXD dengan guard difflib tepat 1 baris berubah + 1 sisipan terverifikasi di REFREEZE-LOG baris 196-219; gerbang rilis v4 CHECK 1-17 PASS, CHECK 8 NR delegasi DOKPDF, CHECK 18 NR tertutup PUTUSAN D-31 jalur (ii) terverifikasi di verification/gerbang-rilis-v4.md dan CONTRACT.md baris 259; refresh 13 butir, nol angka kolom terbit berubah, 11 terkonfirmasi ulang penuh ber-timestamp terverifikasi di research/refresh-sebelum-terbit.md baris 16-18; gerbang resweep kolom MCP dan prosedur citation_title N-08..N-10 terverifikasi di research/R3-vonis-lajur.md baris 74-75. Rekomendasi kurator (non-blocking, tanpa mengubah nilai): nyatakan basis cacah baris saat promosi karena 207/333/434/430 memakai konvensi split-newline-plus-satu sementara wc -l memberi 206/332/433/429, dan master 11.107 memakai splitlines; cukup tambah keterangan alat."
catatan_keputusan: "dipromosikan: PROMANUAL-1004 ILPRO t_c42af89f: custodian verdict terverifikasi; pin register 4/4 terukur ulang; non-sensitif non-dosir; dedup wiki+IL 0"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: catatans/promanual-korpus-register-1004.md
---

# Register Beku Pengetahuan PROMANUAL-1004: silsilah pin, cacah KL/NEG, gerbang rilis akhir

Objek ini adalah titik masuk (entry point) ke korpus pengetahuan misi PROMANUAL-1004:
empat register klaim beku yang menjadi sumber seluruh isi "Manual Komprehensif AI Prompting
dan Lingkungan Pengembangan" (nomor dokumen PMN-1004/REV-1). Semua angka pada berkas ini
diukur ulang sendiri oleh gerbang librarian pada 2026-10-05 23:2x WIB (alat: hash sha256[:16]
byte berkas + cacah baris regex ber-anchor), bukan salinan laporan hulu.

## 1. Keadaan beku final (terukur di disk)

| lajur | isi | sha16 terukur | bytes | baris KL | baris NEG | baris KD |
|---|---|---|---|---|---|---|
| R1 | mekanisme model, tokenizer, sampling, batas konteks | 6d72c018bd10dee5 | 53.839 | 151 | 10 | 0 |
| R2 | teknik prompt (dokumen vendor + studi empiris) | 54cc5ffe2824458a | 101.731 | 229 | 49 | 0 |
| R3 | sensus kapabilitas frontier + harga/limit bertanggal | 7a959ee9d65ee368 | 146.284 | 331 | 61 | 0 |
| R4 | API/SDK, kerangka agen, MCP, alat eval/observability | 6c131ccdb5189339 | 151.934 | 334 | 46 | 7 |

Total populasi: 1.045 baris KL + 166 baris register negatif + 7 baris kedaluwarsa (R4).
Cocok persis dengan cetakan agregat hulu FIXD (KL 1.045; URL primer 968; TERUKUR 952).

## 2. Silsilah pin (rantai empat mata, append-only)

Basis D-15 (refreeze 2026-10-04 22:16, 59 baris addendum diperiksa 59 diterima 0 ditolak)
-> run-4 -> run-5 FINAL (pasca-fix akurasi) -> FIXD (koreksi TEMU-RG3-01, satu-satunya
perubahan pasca-FINAL = lajur R2: +1 baris koreksi KL-R2-229 + penanda DICABUT-SEBAGIAN di
kolom catatan KL-R2-112; guard difflib tepat 1 baris berubah + 1 sisipan). Mekanik register:
append-only, nilai lama tidak pernah dihapus in-place.

## 3. Objek turunan dan gerbang rilis

- Master rakit: docs/2026-10-04-prompt-manual/output/manual-master.md sha16 f43fcf284adbeec3,
  2.013.079 B, 11.107 baris (terukur ulang giliran ini; cocok dengan laporan FIXD dan vonis RGRILIS-v4).
- Vonis rilis pengikat: verification/gerbang-rilis-v4.md (kartu RGRILIS-v4 t_b8f81a1d):
  CHECK 1-17 PASS atas pin f43fcf284adbeec3; CHECK 8 NEEDS_REVIEW (uji tampil delegasi ke DOKPDF);
  CHECK 18 NEEDS_REVIEW tertutup PUTUSAN CONTROLLER D-31 (jalur (ii): mode verbatim-mesin di
  sensor C-14, isi Lampiran J tetap verbatim). Nol SALAH-TARGET, nol cacat objek tersisa.
- Refresh pra-terbit (research/refresh-sebelum-terbit.md): 13 butir agenda, nol angka kolom
  terbit berubah, 11 butir terkonfirmasi ulang penuh ber-timestamp.
- Sisa terbuka yang jujur (bukan cacat): lajur R4 berlabel JENUH-PARTIAL-CAPPED per putusan
  controller D-09/D-10 dengan ledger residu dan resweep terjadwal; matriks R3c kolom MCP punya
  gerbang resweep mengikat (prosedur citation_title N-08..N-10 wajib ikut entri benchmark).

## 4. Cara memakai register ini

Setiap klaim yang naik ke perpustakaan wajib menyebut id KL-nn atau NEG-nn beserta sha16
register sumber di atas. Field dinamis (jendela konteks, harga, limit) adalah snapshot
bertanggal potong 2026-10-04 dan wajib diambil ulang sebelum dipakai sebagai persyaratan
kontrak; jangan mengutipnya sebagai angka tetap.
