# Cap rotasi gelombang + triase timeout + echo notifikasi (pola controller teruji 29-09)

Dua misi membuktikan pola ini berulang: HDKCOMP-0929 (12 gelombang verifikasi V) dan
RAFIF-VISUAL-0929 (4 segmen aset + 6 generator figur). Sumber kebijakan: cap di blueprint TA
(puncak running ≤5; maks 2 paralel per tipe profil) + aturan standing user (dispatch failed
tapi artefak ada -> JANGAN re-dispatch buta; audit kelengkapan dulu).

## 1. Cap rotasi — cara menegakkan
- Saat instantiate gelombang N kartu serentak (mis. V01..V12 dari WAVE-MAP): lepas hanya yang
  muat di cap (mis. V01-V04 = 2 crawler + 2 collector); sisanya `hermes kanban block <id>` dengan
  pesan berisi ALASAN + pemicu unblock eksplisit ('saat ada kartu bertipe X terminal').
- Tiap kali satu kartu terminal (done), unblock tepat satu penerus yang slot tipenya longgar.
  Hitung ulang dari papan SETIAP giliran (list --json + Counter status per assignee) — jangan
  pakai ingatan giliran lalu.
- Tafsir cap yang terbukti benar: cap = REM PELEPASAN kartu baru, BUKAN kill-switch kerja berjalan.
  Dispatcher kadang memajukan kartu melewati cap tipe (kasus GD/GC RAFIF-VISUAL); kalau modalnya
  terbukti sehat di disk (figur/manifest mengalir), biarkan terminal sendiri dan stop melepas
  baru. Memutus kerja sehat = membakar modal; ini preseden L9/L17 yang dikonfirmasi ulang.
- Kartu `todo` tertahan rantai dependensi TIDAK bisa dan tidak perlu diblock ('cannot block' dari
  kernel) — rem hanya untuk kartu `ready`.

## 2. Echo notifikasi — jangan bereaksi dua kali
Notifikasi `blocked; needs attention` yang isinya persis pesan cap yang BARU kamu pasang sendiri =
gema, bukan kejadian. Prosedur: ukur papan (status Counter + daftar running per tipe), konfirmasi
keadaan = desain, laporkan 'tidak ada aksi sah', JANGAN unblock dini (melanggar cap sendiri) dan
jangan buat kartu baru. Notifikasi `completed` yang sudah kamu proses lebih dulu dari papan
(baca hasil via list/show sebelum notifikasinya tiba) juga gema — cukup koreksi kronologi, tanpa
kerja ulang.

## 3. Triase timeout — tangga keputusan
1. `dispatcher will retry` = retry otomatis naik; JANGAN manual-retry.
2. Ukur MODAL di disk sebelum vonis: berkas hasil sebagian? cache scratch? register defek?
   - Modal ADA (mis. A1: manifest 666 baris + audit + remediasi; V03/V07: CSV yatim; L16-C: 18
     probe mentah) -> retry biasanya hanya memverifikasi + menutup. Amati satu giliran; tidak ada
     aksi.
   - Modal NOL artefak DAN beban baca kartu besar (kasus W12: body memerintahkan buka 16 berkas
     ±600 KB) -> akar = desain kartu, bukan worker. Pecah lingkup: kartu anak dengan SUMBER
     dibatasi (bab bukan research), rantai parent-child, tutup induk dengan komentar traceroot.
3. Ambang pecah kartu = timeout KEDUA tanpa modal. Timeout pertama dengan modal tidak pernah
   memicu pecah kartu di semua kasus 29-09 (V03, V07, A1, A4 semua selamat via take-over run-2).
4. Run-2 yang baik memanen modal run-1 dan MENAMBAH jejak (bukti: md V07 naik ±600 B dari ukuran
   triase) — cek delta ukuran untuk membedakan 'menutup' vs 'sekadar klaim'.

## 4. Langkah-0 penyegelan bahan (instruksi TA 'ganti placeholder sha pasca langkah 0')
Sebelum melepas kartu hilir yang menyitasi bahan (integrasi/build): controller SENDIRI menghitung
sha12 bahan sumber di disk (kitab beku, manifest gabungan, berkas FIG), membukukan ke contract.md
(Decision Log / seksi Langkah-0), lalu menempelkan pin + putusan register lewat `kanban comment`
STEER ke kartu yang SUDAH running (re-dispatch tapi belum sempat baca body lama). Ini menutup race
placeholder-vs-nyata tanpa menghentikan pekerja.

## 5. Audit klaim pekerja wajib pakai artefak
'Verdified on disk' di result kartu tetap diuji: buka berkasnya, ukur byte/baris/kolom dengan
parser sungguhan, cocokkan angka klaim. Variasi penamaan jejak antar-pekerja (hasil-Vnn.md vs
VERIFIKASI-Vnn.md vs hasil-Vnn-VERIFIKASI.md; FIG besar vs fig kecil; manifest pipe vs tab) adalah
NORMAL — normator hilir harus mencocokkan pola, bukan satu nama baku. Lihat juga
gsp-verification-before-completion/references/parser-correction-before-verdict.md.
