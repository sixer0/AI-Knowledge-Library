# Paritas gerbang kartu tulis + persist-first kelas builder (RAFIF-REVB-1010, 10-10)

Tiga mekanika terbukti satu misi tulis-massa 27 bab + gelombang figur, semua dari pengukuran disk controller.

## 1. Paritas gerbang: VERIFY kartu = gerbang penerimaan vonis

Kartu tulis gelombang W menaruh VERIFY = `work/pack/ukur_pack.py` (irama) saja, TANPA
`scan_ai_footprint.py --channel <kanal artefak>` di badan kartu. Hasilnya terukur:
lima kartu (W1b/W2/W4/W5/W6) menutup `STATUS: complete` dengan klaim 'lolos gerbang rasa
terukur' padahal berkasnya MERAH di gerbang penerimaan controller (C-8b angka tanpa
batasan, C-24 nol momen pembalik, C-14 salinan gagasan). Pekerja PATUH pada gerbang yang
disuruh; vonis controller jatuh di sensor yang tidak pernah diminta ke pekerja.

Aturan turun-temurun:
- SETIAP kartu tulis/fix memuat SEMUA sensor penerimaan final di blok VERIFY-nya sejak
  dicetak: scan kanal artefak per berkas (VERDICT PASS) + instrumen sekunder (irama/dsb)
  + format result (VERDICT + sha16 + ukuran per berkas).
- Komentar vonis/steer TIDAK terjamin terbaca run yang sudah berjalan - steer hanya
  efektif untuk run BERIKUTNYA; jangan pakai komentar sebagai mekanisme penambalan gerbang
  kartu hidup, tempel di badan bila kartu belum diklaim (`hermes kanban edit` hanya
  menyentuh result - badan tidak bisa ditambal pasca-create, jadi benar sejak awal).
- Pelanggaran format penutupan berikutnya = request-changes, bukan komentar saja.

## 2. Instrumen wajib membuktikan ia membaca sasaran

`work/pack/ukur_pack.py` exit 0 pada berkas revb TANPA membaca berkas itu sama sekali
(skrip kalibrasi korpus era sebelumnya). Exit 0 dari alat yang buta-sasaran = bukti kosong.
Gerbang: sebelum menerima angka instrumen, uji alat pada dua input berbeda yang hasilnya
HARUS beda (red-green mini), atau baca sumbernya untuk pastikan path sasaran dipakai.
Temuan sejenis: bandingkan pin dengan FUNGSI HASH YANG SAMA - `sha1sum | cut -c1-16` vs
pin sha256[:16] memberi 'pin bergeser' palsu (kasus bab-03, tertangkap saat audit susulan).

## 3. Putusan vonis butuh pemilik hidup di giliran yang sama

Putusan D-R2/D-R3 controller (kanonisasi rujukan RULER + tambal lab bab-03) ditulis di
komentar vonis UJI-RASA dengan pemilik 'W9' dan 'W1b'. Audit byte berjam kemudian: bab-03
masih persis pin sampel (mtime tak bergeser) - W1b sudah done saat putusan lahir, W9 belum
dibebani butir itu. Tidak ada yang mengeksekusi.
Aturan: setiap butir putusan controller WAJIB langsung menemukan kartu HIDUP pemiliknya di
papan pada giliran yang sama (komentar bekal + edge tercatat di kontrak); bila pemiliknya
kartu yang sudah tutup, tempel bekal ke pengganti SAAT ITU JUGA, dan tulis siapa pemegang
butirnya. Putusan tanpa pemilik = hutang jejak, bukan keputusan.

## 4. Persist-first untuk kartu kelas builder (coder figur/build)

Pola kegagalan jendela 30 mnt pada gsp-coder-execution: run habis di debat/perancangan,
nol byte ke disk. Terukur satu papan: FG4 run-1 menulis builder 39 KB di detik-terakhir
lalu mati sebelum render; FG1 run-1 hampir lengkap (builder 40 KB + 24 PNG workspace) lalu
timeout; FG2 dan FG3 run-1 KOSONG TOTAL (FG3 crash + timeout, retry habis, nol berkas).
Steer yang terbukti membalik keadaan (FG4 run-2 -> partial-handoff tertib, 16 id tayang,
sensus 33 berkas tertutup aritmetika, 8 id merah DITAHAN tidak terselundup):
1. Persist-first: tulis bagian builder ke berkas SEBELUM render; pecah per-bab/per-id.
2. Publish INCREMENT per id begitu lolos gerbang - jangan kumpulkan di akhir (timeout
   berikutnya tidak menghapus hasil; terbukti: folder figur menayang 33 berkas saat run
   masih jalan).
3. Jalankan modal apa adanya, DILARANG bangun ulang; audit modal vs daftar id dulu.
4. Cadangkan >=8 menit terakhir untuk result penutup format penuh; partial-handoff jujur
   dengan peta sisa per id > complete palsu atau mati senyap.
5. Triger eskalasi TERDOKUMENTASI di kontrak (bukan improvisasi): bila run berikutnya
   timeout lagi TANPA persist pertama (steer diabaikan) -> split per-bab ATAU pindah
   penerima (preseden kelas tugas selesai di profil lain). Jangan pindah penerima selama
   profil masih produktif di kartu lain - bedakan 'steer belum terbaca run' dari
   'profil salah'.

## 6. Catatan mekanik kartu (lad_card.py)

Flag sah: `--est --shape --parents --tenant --body-file`; `--cap` BUKAN flag (cap dibaca
otomatis dari profil; saran bentuk R-1/R-2/R-3 muncul di output). `--parent` salah,
`--parents` benar. Edge susulan via `hermes kanban link <kartu> <target>`; unlink milik
sendiri sah untuk koreksi edge salah tempel.

## 5. Visus controller sebagai pembanding independen

Vonis figur sah dua lapis: mekanik (fontTools + 3 uji kontinuitas konektor eksplisit) DAN
visus enam butir tertulis per id. Klaim pekerja 'bersih' tanpa jawaban enam butir ditolak
(preseden v1.0 3/3 jatuh). Koreksi atas vonis sendiri (understate pin W7: 3 berkas
bergeser, bukan 1) lewat KOMENTAR TERPISAH, bukan sunting komentar lama.
