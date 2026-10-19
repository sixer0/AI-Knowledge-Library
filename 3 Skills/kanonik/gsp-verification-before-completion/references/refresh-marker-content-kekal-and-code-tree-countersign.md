# Countersign Pengawas: Refresh/Marker Konten-Kekal, Pohon Kode/API Ledger, Disiplin Instrumen Sendiri

Preskripsi giliran sore 05-10 (RAFAI MARKER-C10, PROMANUAL REFR/MUTU, RAFIFUNITY KOMPILASI-API/REVIEW-KODE/QC-FIGUR). Tiga kelas objek + satu blok disiplin diri.

## 1. Countersign kartu REFRESH/MARKER pada artefak raksasa (konten-kekal harfiah)

Objek: suntingan kecil atas master/rakitan >1 MB yang mengklaim "hanya kendali".
- **Arsip-dahulu-bukti:** hash ulang berkas arsip pra-sunting pekerja; sha16-nya WAJIB == pin rantai yang kupegang dari vonis sebelumnya (build->vonis->MUTU->REFR). Cocok = rantai pin utuh; tidak cocok = STOP, jangan vonis.
- **Diff penuh independen** (difflib.SequenceMatcher antar splitlines): cetak `baris hilang/baris baru` + sampel OLD/NEW. Vonis konten-kekal hanya bila SEMUA delta adalah teks kendali yang dikutip literal (baris riwayat, status tabel, paragraf marker). Satu delta angka = gagal klaim.
- **Register tak tersentuh tiga bukti:** sha16 per register == pin refreeze, mtime < tanggal kerja, cacah baris tidak turun.
- **Marker:** jalankan scanner sendiri dengan `--require-marker`; PASS harus tercetak di dua format (docx-paragraph + pdf-text). Untuk PDF: ekstrak teks per halaman dan kutip baris marker.
- **Suntik-tanggal:** hitung penanda `@<tanggal terbit>` di master - refresh yang benar mengisi nilai TANPA mengganti stempel tanggal register (0 sisipan = benar).
- Tetapkan pin pasca-sunting baru di vonis sebagai acuan kartu hilir (GRILIS/DOKPDF).

## 2. Countersign gerbang pohon kode / API ledger / aset proyek (tanpa runtime)

Objek: ledger konsistensi API, review kode listing, QC figur generator deterministik.
- **Sensus ulang sendiri:** jumlah baris JSON ledger == klaim; glob `Assets/**/*.cs` + hitung baris total == klaim (922/16 di preseden).
- **Baterai grep pemanggil** (pola "deklarasikan tanpa pakai"): `\.Get\(\)|\.Release\(\)|ItemPool\.`, `\bhud\.`, `\.Show\(\)`, `Time.timeScale = 0` vs `= 1` (set=0 tanpa pemulihan = game-freeze), `"isPartOfComposite": true` vs `"isComposite": true` (komposit yatim). 0 hits = bloker terkonfirmasi dari sisi pengawas.
- **Bukti "belum ada fix masuk":** `git rev-list --count HEAD` + HEAD sha == sha yang dilaporkan; cocokkan jumlah commit tahap vs klaim (16 tahap + 1 MANIFEST = 17).
- **Provenance bukti mentah:** SENTUH byte setiap berkas raw yang dikutip laporan - halaman simpanan bisa berupa stub `Not found` 9 B; pembanding nyata mungkin berkas .txt daftar resmi. Vonis tetap sah bila token dihitung ulang vs berkas yang BENAR, tapi catat: stub mati jangan disimpan tanpa label, URL laporan di-probe ulang saat kartu fix.
- **Profil vision tanpa terminal (QC figur):** metode sah = dimensi piksel dari loader + `savefig(dpi=300)` + `figsize` cm di sumber, dengan batas metode dinyatakan eksplisit. Reproduksi temuan KRITIS lewat vision QA sendiri: bandingkan JANJI caption/MANIFEST dengan teks yang terlihat di wajah figur (kotak rumus hilang = mismatch dua arah). Fix bersifat mekanik bila generator deterministik: "ubah koordinat, rerun, QC ulang" - syarat vonis fix: dua-run idempoten + registry sha + vision QA + baris Riwayat.
- Pemisahan predikat yang benar dan layak dipuji: "signature 0 dari 51 karangan" (kode konsisten dokumen) ≠ "pohon proyek belum koheren fungsional" (cacat integrasi) - dua klaim berbeda, jangan dicampur; MISMATCH-BLOKER baris = tersandung cacat B-x, bukan salah signature.

## 3. Disiplin instrumen pengawas sendiri (sumber positif-palsu terbesar)

- **Ukur draf vonis SEBELUM kirim:** panjang byte (terpotong 229 B terdeteksi begini) + scan glif U+2014/U+00B7 + regex CJK pada vonis sendiri (satu CJK tak sengaja tertangkap pra-kirim).
- **Angka peta = cetakan-alat terakhir sebelum kirim.** Bila board berubah antara draf dan pasang (88->92, todo 4->3): JANGAN sunting komentar lama; kirim komentar `KOREKSI PETA vonis ...` TERPISAH. Substansi vonis tidak berubah.
- **Notifikasi ganda kartu sama:** vonis hanya sekali; `kanban show | grep -c "<penanda unik vonis>"` = 0 sebelum pasang. Frasa kunci yang sudah ada di RESULT pekerja bisa membuat grep-1 menipu - gunakan penanda milik vonis sendiri.
- **Attribusi temuan silang-lajur:** potongan laporan (variansi "T1" ternyata T3) - sentuh berkas laporan penuh dan cocokkan konteks heading SEBELUM membekukan atribusi di catatan retry.
- **Jendela regex sempit = pembacaan palsu:** probe Lampiran D dengan slice 2.500 char sempat membaca "selisih sinkron" padahal D konsisten; baca lajur laporan penuh sebelum memvonis klaim orang lain (dan tulis koreksi itu di vonis).
- **Guard terminal `&`:** heredoc python inline yang memuat `&` (mis. `mods & official`) ditolak sebagai backgrounding - tulis skrip via write_file lalu jalankan `uv run --python 3.11 python C:/...skrip.py`.
- **Lubang cakupan vonis tulis:** 22 vonis bab menguji anatomi+KL+glif tapi TIDAK menguji rentang kuota ordinal (Tujuan belajar 3-6, Uji pemahaman 3-8) - baru terjatuh di MUTU pasca-rakit sebagai cacat turunan kelengkapan. Wariskan CHECK kuota ordinal ke instrumen vonis tulis misi berikutnya sejak bab pertama; vonis tulis tidak boleh mengklaim "bersih total", hanya "bersih per cakupan instrumen".
- **Scanner fleet wajib `--channel <kanal>`** (panggilan polos = kanal default -> false-FAIL C-7; baca `--help` dulu). Beda definisi detektor (slug luas 22 / kanonis-berpasangan 20 / longgar 28) direkonsiliasi dengan mereproduksi angka verifier memakai DEFINISI dia, bukan menuntut angka sama.
