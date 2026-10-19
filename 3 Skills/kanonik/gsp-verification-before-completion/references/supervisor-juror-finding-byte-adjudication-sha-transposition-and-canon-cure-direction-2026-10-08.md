# Juror-finding byte adjudication, sha-transposition forensics, canon-cure direction (GAYAMANUAL-1007 V9/H11a, 2026-10-08)

Tiga resep penutup papan keenam, semua terverifikasi lintas-tangan pengawas.

## 1. Verifikator mengadili temuan juri DI BYTE sebelum memvonis (GM-V9 `t_91e376df`)

Pola baru yang layak jadi prosedur baku lane verifikasi akhir: sebelum menulis VERDICT,
verifier menjalankan probe khusus (`gmv9_probeE.py`) yang **mereproduksi setiap temuan
named juri pada byte terbit**. Hasil: semua temuan kedua kursi juri terverifikasi ada di
docx/PDF ("nol halusinasi juri" menjadi klaim terukur, bukan asumsi). Urutan yang benar:
juri menemukan -> verifier mengadili temuan di byte -> vonis akhir menyebut temuan yang
sudah tersokong. Jangan memvonis-ulang dari nol (buang anggaran) dan jangan menelan
temuan juri mentah-mentah (saksi bukan alat ukur).

Konsekuensi gerbang yang sama papan ini: **gerbang-rakit 12-CHECK bisa PASS sementara
verifikasi-independen 10-gerbang FAIL** (TOC mati: string 'No table of contents entries
found.' nyata di docx + halaman-2 kedua PDF + bookmark=0; tak ada CHECK-TOC-HIDUP di
gerbang rakit). Aturan turun-temurun: setiap cacat yang tertangkap oleh JURI atau
VERIFIKASI AKHIR tapi lolos gerbang-hulu = wajib ditambal sebagai CHECK BARU di gerbang
hulu (pola VP-2 'daftar isi hidup: PAGEREF terisi' papan VCTL), bukan hanya disunting
kontennya - tanpa itu rerak bisa hijau lagi dengan cacat yang sama. Tagihan serupa:
CHECK-backtick-terrender-ke-PDF (F2, 11 kepala aturan Bab 7).

## 2. Forensik beda 'typo transkripsi sha' vs 'mutasi pasca-klaim' (GM-H11a `t_71efbbe1`)

Klaim pekerja menyebut fig-25 sha16 `eddec3e8b25ca8ad`; disk mencetak `eedec3e8b25ca8ad`.
Resep adjudikasi (jangan langsung vonis dua-era/mutasi senyap):
1. Bandingkan prefiks vs sufiks hash: dua karakter AWAL terttranspose, ekor-14 identik
   = signature kesalahan ketik manusia; mutasi nyata mengubah SELURUH hash.
2. Cek jam: mtime berkas (05:49:06) LEBIH TUA dari komentar yang mengklaim (05:51) =
   tidak ada jendela tulis-ulang.
3. Vonis: typo-transkripsi-laporan, artefak tunggal; nyatakan PIN KANON dari alat
   (`eedec3e8...`) declared di jejak supaya hilir tidak memilih dari laporan.
Ini sepupu kelas 37.659 (TA-INDUK mengutip byte state-tulis-menengah): angka laporan vs
cetakan alat - yang menang selalu alat, tetapi bedakan dulu sebab selisihnya (race baca,
typo, atau mutasi) sebelum menuduh era.

## 3. Arah penyembuhan 'bukti yang tidak tersedia': klaim disesuaikan ke bukti, bukan sebaliknya (BTN-07 veto, GM-H11a)

Satu-satunya veto kursi-1 (D4=1): prosa buku mengklaim contoh muncul di "empat tempat
berbeda" padahal bukti grep hanya 4 kemunculan identik BERDERET di satu berkas. Obat yang
dipakai H11a dan layak dibakukan: **turunkan klaim prosa ke ukuran sokongan sebenarnya**
("empat baris beruntun dalam satu berkas") + kutipan bukti TETAP terpajang + catatan
aparatus label SOURCE. Yang dilarang dua arah: menghapus kutipan demi hijau, atau
melebar-lebarkan bukti demi cocok klaim. Ini bentuk SPK-002-butir-3 ("kosong lebih baik
daripada salah") di lapis narasi: klaim boleh mengecil, fakta tidak boleh mengarang.

## 4. Field sidecar yang tidak ter-print: ground truth = permukaan TERBIT (H11a catatan skop)

Sunting kata terlarang di sidecar YAML figur menyentuh `judul-pesan`+`alt-text` (yang
dibaca builder jadi caption) tapi meninggalkan field `isi` (tidak ter-print). Vonis
pengawas: non-isu bila field memang tidak naik ke dokumen, TAPI jangan berdebat dari
struktur sumber - **cek string di docx TERBIT pasca-rerak** sebagai ground truth; gerbang
daftar-larang yang sudah ada cukup direrun. Generalisasi: saat menilai kepatuhan lapis
sajian, yang mengikat adalah cetakan permukaan terbit, bukan kelengkapan suntingan
di semua lapis hulu.

## 5. Sensor pengawas yang terpakai giliran ini
- Heuristik fence-utuh (baris dalam fence berakhir tanpa titik) mereplikasi klaim
  '17 fence digabung' -> 0 fragmen tersisa dari 29 fence: proxy cepat validasi
  penggabungan mekanis konten-kekal.
- Regex-ketat '(`C-nn`)' mencetak 8 vs klaim 11 kepala: beda definisi paragraf-vs-pola,
  declare dua-definisi, jangan vonis kontradiksi (pelajaran-ke-11 berulang).
- Payung skop dua-arah: yang bocor di prosa kita disunting; kutipan kanonis dalam fence
  dan kepala aturan SG TIDAK boleh disentuh - cek 'tersisa-1-di-fence' sebagai bukti
  suntingan tidak kebablasan.
