# Kelas berulang controller — hasil GAYA-AHLI-1005 + VISUAL-1005 (06-10)

Kondensasi dua misi ~100 kartu. Tiap kelas: gejala → akar → protokol. Sumber detail: CONTRACT.md + Decision Log kedua misi (docs/2026-10-05-gaya-bahasa-forensik/, docs/2026-10-06-visual-instrument/).

## C1. Worker mati setelah artefak lahir (limit bridge 1800s)
Gejala: kartu timed_out/gave_up ATAU done dengan result kosong, padahal artefak utuh di disk (mtime = menit timeout); yang belum terjadi hanya short-check/penulisan result. Terjadi >=8 kali lintas dua misi.
Protokol:
1. UKUR artefak sendiri dengan parser independen (cacah struktur, bidang wajib, glif, keutuhan ekor) — jangan percaya summary.
2. Hijau → `complete --force` dengan bukti terukur di result; kartu sudah terminal → komentar catatan-controller. JANGAN restart dari nol (menimpa artefak = preseden buruk, lihat pitfall double-run 03-09).
3. Pencegahan di kartu baru: kerja rakit/tulis berat → `--max-runtime 3600`; body wajib memuat "SHORT CHECK DI AWAL sesi"; bebankan pembekuan instrumen/builder di kartu awal agar resume tidak menulis ulang.
4. Resep identik mati dua kali dengan progress sama → PECAH kartu (mata-a build+gerbang / mata-b PDF+serah), bukan percobaan ketiga.

## C2. Drift pin (pin vs artefak hidup)
Gejala: konstanta pin di checker/fixture/komentar pengalihan masih era lama setelah artefak disunting/direbuild; gerbang menolak objek hidup; atau komentar mem-pin build lama sementara result mem-pin build baru. Tiga kambuh dalam satu misi (kelas drift-3) + kasus SERAH.
Protokol:
- Pen-pin-an sah = result kartu TERAKHIR. Rebuild wajib menulis ulang pin result; komentar pengalihan dinyatakan batal saat rebuild.
- Doktrin "pin naik serumah suntingan": siapa pun yang menyunting artefak (termasuk suntingan metadata satu baris) WAJIB di giliran yang sama menaikkan pin di SEMUA konsumen (konstanta checker, pin fixture, notes) + menambah baris RIWAYAT PIN.
- Checker menyimpan PASANGAN LEDGER: pin badan (hash zona aturan) + pin hidup; bukti badan tak bergeser = hash zona konstan lintas transisi metadata. Perubahan pin = ledger sah ber-jejak, BUKAN pelonggaran.
- Byte era lampau hilang: rekonstruksi dari arsip tertua via transformasi bernama, verifikasi sha == pin sebelum mengarsipkan (pola f21b_arsip_revb).
- Whitelist/swa-deklarasi oleh objek yang diukur tetap REJECT (preseden t_eec55819).

## C3. Salah invokasi instrumen → klaim salah (kelas T5)
Kasus nyata: scanner dipanggil `--text <path>` ⇒ yang terukur string path 2 kata, bukan isi berkas; klaim "scanner PASS" menyebar ke vonis-lepas + kontrak, ditangkap verifier independen.
Protokol:
- Sapuan berkas = argumen POSISI (tanpa --text); `--text` hanya untuk cuplikan inline. Bentuk invokasi dicetak di jejak.
- Klaim rilis wajib merujuk run segar atas byte terpin; jejak tidak boleh lebih tua dari objek (selisih era harus dinyatakan eksplisit).
- Saat ketahuan: akui SPESIFIK (baris mana, alat mana), coret rekaman + adendum + akar; vonis akun lain yang tidak bergantung instrumen cacat tetap berdiri.

## C4. Resep tool (Windows / COM / uv / parser)
- Word COM "Call was rejected by callee" (instance dipakai worker lain): `win32com.client.DispatchEx("Word.Application")` (instance terpisah) + `DisplayAlerts=0`; halaman nyata `ComputeStatistics(2)`; ekspor `ExportAsFixedFormat(dst,17)`; PDF selalu dicetak dari docx TERKINI (cek mtime sezaman).
- Runner fixture/render via uv butuh `--with matplotlib,pillow,numpy`; ModuleNotFoundError = kurang dependensi, bukan cacat objek. Verifikasi PDF mandiri lapis dua: pymupdf vs Word COM; selisih alat (mis. 160 vs 162 hal) dibukukan declared.
- Terminal hardline memblokir perintah inline dengan substitusi ganda `$( ... $( ... ) )` atau payload raksasa → berhenti dan laporkan; ganti jalur hanya atas izin pengguna. Payload terblokir tersimpan di cache/blocked-scripts (pulihkan `bash <path>` hanya atas izin pengguna, jangan retry inline).
- `lad_card.py`: `--parents` harus id kartu NYATA (entri ledger non-kartu / id fiktif → create exit 1); `grep -E "Created|ERROR"` bisa menelan pesan saat batch — selalu tail output penuh bila jumlah Created < jumlah kartu.

## C5. Pola akselerasi full-power (norma N1 + penahan berkas)
- Lepas kartu hilir PARALEL dengan kalimat penahan baku ("cek berkas X di disk; kalau belum ada, block kind=dependency jujur; dispatcher klaim ulang otomatis") — terbukti nol tabrakan (review outline jalan sebelum outline lahir).
- Persiapan kiri langkah hilir (daftar kerja, infrastruktur renderer/gerbang) boleh didahului bila hulunya sudah final.
- Controller boleh ambil-alih langkah mekanik deterministik (kemasan DOCX/PDF, ledger) dengan kartu + jejak, lalu ALIHKAN worker yang terlanjur mengklaim menjadi verifikasi independen (jangan bangun ulang).
- Anggaran ukuran diputuskan ALAT (halaman PDF nyata), bukan proksi; plafon yang ternyata estimasi internal (bukan tuntutan user) diadili lewat putusan tercatat + veto user terbuka — completeness vs plafon dilarang diputus diam-diam.
- Vonis dua-juri + reshoot-sempit per-zona-hash (bawa zona tak tersentuh dengan bukti byte-identik) memangkas biaya re-uji tanpa membuka ulang batch.
