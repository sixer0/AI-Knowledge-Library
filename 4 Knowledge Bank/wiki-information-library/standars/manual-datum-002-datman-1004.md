---
id: manual-datum-002-datman-1004
type: standar
title: Manual final DATUM Document Manual 002-GSP-STD-X-2026 RevA
status: active
sumber: docs/2026-10-04-datum-manual/manual/ (docx+pdf final, pin sha256 penuh di body)
halaman: 100 halaman ter-render; vonis berantai VERIF-akurasi-representasi.md -> VERIF-ulang.md -> VERIF-final-4.md (PASS)
tanggal_akses: 2026-10-05
kelas_bukti: sintesis
sensitif: tidak
perkara: datmanual-1004
tags: [datman-1004, manual-final, datum-house-style, promosi-lolos, gerbang-librarian]
links: [docs/2026-10-04-datum-manual/manual, docs/2026-10-04-datum-manual/checkpoints/VERIF-final-4.md, docs/2026-10-04-datum-manual/checkpoints/FIX4-selfcheck.md]
penulis: gsp-document-writer
diajukan: 2026-10-05
misi: DATMANUAL-1004
kartu: t_9b06e2a1
pin_sha256_docx: d4939a04e022a0253f9b8c47027457ced50912409dae3f7c91543c539b73945a
pin_sha256_pdf: 76ec696a8f0b94606902dab188becddf886f125982575de47e1114b2f3a02546
riwayat_keputusan: "TAHAN-1 vonis P22 (VERIF-akurasi-representasi.md): A-01 MAJOR SPK-002 butir 8 tanpa tautan aktif+terlihat; A-02 register L.2 N-9 salah klaim token EIA; K-01 empat-vs-enam kolom; K-02 kolom Asal; K-03 aset logo. TAHAN-2 vonis F17-REV (VERIF-ulang.md): CHECK 7 kalimat basi 'belum dibangun ulang' p36/p63; CHECK 9 residu 'Register asumsi 4 kolom' L.6.3; CHECK 10 scanner docx C-12 dua sinyal. FIX3+FIX4 (rebuild controller) lalu vonis F22-REV4 (VERIF-final-4.md): seluruh butir PASS, CHECK 7/14 berbalik PASS, CHECK 1-6/8-13 tidak mundur, scanner naturalisasi dua kanal exit 0"
catatan_keputusan: "dipromosikan: DATMANUAL-1004 F18-PROM2: vonis F22-REV4 PASS (VERIF-final-4.md) atas hash docx d4939a04.../pdf 76ec696a... diukur ulang gerbang; LULUS-PROMOSI controller 11:13 WIB; non-sensitif non-dosir; dedup 0"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: standars/manual-datum-002-datman-1004.md
---

# Manual final DATUM Document Manual 002-GSP-STD-X-2026 RevA

Rekaman objek untuk artefak final manual DATUM misi DATMANUAL-1004 (langkah 19-19b,
promosi F18-PROM2). Berkas biner tidak disalin ke vault; path kanon + pin sha256 penuh:

- DOCX: docs/2026-10-04-datum-manual/manual/DATUM Document Manual 002-GSP-STD-X-2026 RevA.docx (4,947,100 B, sha256 d4939a04e022a0253f9b8c47027457ced50912409dae3f7c91543c539b73945a)
- PDF : docs/2026-10-04-datum-manual/manual/DATUM Document Manual 002-GSP-STD-X-2026 RevA.pdf (1,203,964 B, sha256 76ec696a8f0b94606902dab188becddf886f125982575de47e1114b2f3a02546)

Pin di atas diukur ulang sendiri oleh gerbang librarian pada giliran promosi ini
(certutil SHA256, 05-10 11:2x WIB) dan identik byte-per-byte dengan tabel pin
checkpoints/VERIF-final-4.md, checkpoints/FIX4-selfcheck.md, dan komentar LULUS-PROMOSI
controller di kartu t_9b06e2a1. Rantai build yang melahirkannya (build_manual_datum.py +
fix2_word.py, Word COM, pages=100) dibukukan di checkpoints/FIX4-selfcheck.md.

## Keadaan verifikasi (kutipan vonis pengikat)

Vonis pengikat: checkpoints/VERIF-final-4.md (kartu F22-REV4 t_e56ea1a1, gsp-verifier
independen, 2026-10-05 11:0x WIB): VERDICT PASS. CHECK 7 lama (keadaan-build kepala
Bagian) dan CHECK 14 lama (23/23 rujukan jejak audit ada di disk) berbalik PASS;
CHECK 1-6 dan 8-13 tidak mundur; scanner naturalisasi dua kanal (docx+pdf) VERDICT PASS
exit 0; U+2014=0 pada kedua kanal. Batas klaim vonis: berlaku HANYA untuk sepasang hash
terpin di atas; suntingan sekecil apa pun membatalkan.

Rantai vonis sebelum PASS (dibukukan penuh di field riwayat_keputusan): P22 FAIL ->
FIX1/FIX2 -> F17-REV FAIL -> FIX3 -> F20-REV2/REV3 FAIL/NEEDS_REVIEW -> FIX4 ->
F22-REV4 PASS. Tidak ada promosi tanpa vonis PASS atas hash yang beredar (SPK-002 butir 5).

## Klasifikasi gate librarian

- sensitif: tidak -> tidak butuh persetujuan user (Approval Inbox).
- perkara datmanual-1004 = folder misi, bukan dosir -> tidak butuh verifikasi manusia.
- Dedup: sensus wiki + il_dump (818 entri) atas token 'manual-datum-002' dan
  'DATUM Document Manual' = 0 berkas; tidak duplikat, tidak konflik entri kanonik.
- Intake: jalur usulan manual librarian; scope gerbang ingest 'datmanual-1004' masih
  tertunda registrasi controller (PROMOSI.md seksi 2), sehingga objek ini TIDAK mengklaim
  'sudah tergerbang' produksi (GATE-SPEC 8.2; wewenang promosi librarian tidak berubah).

## Sadar-diri penulis-verifikator

Body rekaman ini dirakit gerbang librarian dari artefak hulu; penulis artefak adalah
gsp-document-writer (lapis md), rebuild oleh controller, dan vonis pengikat oleh
gsp-verifier independen (kartu REV4) - bukan oleh librarian. Attest librarian menutup
kurasi provenans/dedup/gate, menggantikan attestasi diri.

## Catatan minor dibawa terus (dari vonis REV4, tidak memblokir terbit)

- CATATAN-2: named style 'Hyperlink' tak terdefinisi di styles.xml; direct formatting sah.
- CATATAN-3: anotasi URI PDF pecahan multi-baris -> garis bawah sebagian (p63/p77 vonis lama).
- CATATAN-4: hex16 tercetak inline di badan dokumen hanyalah pin FIX2; pin artefak beredar
  ditelusuri lewat checkpoints/FIX3-selfcheck.md dan FIX4-selfcheck.md yang dirujuk dan ada.
- CATATAN-1: seal band 5,30 mm vs token 5,00 dalam toleransi deklaratif +-0,6 (TERIMA).
- Putusan pemilik CHECK10 (Perkap 1/2023 Pasal 79; bentuk kutip PUPR 8/2023) tetap tertunda
  sesuai vonis P22; tidak mengubah keadaan butir rilis yang diuji REV4.
