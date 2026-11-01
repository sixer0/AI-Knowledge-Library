# Forensik Spot-Check Klaim Pekerja (tervalidasi 2026-09-11, misi WF-CRAWL-0911)

Konteks: controller mensahkan hasil kartu pekerja satu per satu (giliran notifikasi
kanban). Pola di bawah menyelamatkan dari vonis palsu tiga arah: klaim pekerja benar
tetapi cap waktunya bohong, sensus hash saya sendiri yang salah vonis, dan klaim API
yang cuma bisa diuji tanpa menjalankan library.

## 1. Urutan anti-blind dibuktikan MTIME disk, bukan kepala dokumen

- Fakta nyata: dokumen rubrik menulis "dikunci 16:20 WIB", laporan benchmark menulis
  "eksekusi 16:25-16:40", padahal jam dinding saat audit baru 15:43. Cap naratif
  mundur/terbalik terhadap disk.
- Yang sah: rantai mtime `rubrik 15:34:00 -> output mentah 15:39:23 -> laporan
  15:39:51` membuktikan urutan rubrik-sebelum-hasil TETAP benar; yang cacat hanya
  labelnya.
- Resep: `ls -la --time-style=full-iso <file bukti...>` + `date +%H:%M:%S` pada giliran
  yang sama. Vonis tidak diubah oleh cacat label, tetapi temuan wajib ditempel sebagai
  komentar ke kartu verifier hilir dengan instruksi: koreksi cap waktu dokumen,
  DILARANG menyunting bukti mentah.

## 2. Pitfall backslash MSYS pada sensus sha256 (BEDA palsu)

- Gejala: sensus hash kanonik-vs-fleet-vs-profil menampilkan SEMUA baris BEDA padahal
  10 karakter pertama hash terlihat identik secara visual. Sebab: shell git-bash/MSYS
  menyisipkan `\` di depan hash saat path argumen bergaya Windows, sehingga
  perbandingan string `[ "$h" = "$c" ]` gagal sistematis.
- Tambal: normalkan keluaran sebelum bandingkan, mis.
  `h=$(sha256sum "$f" | tr -d '\\' | cut -c1-10)` lalu bandingkan; atau pakai path
  forward-slash murni.
- Aturan vonis: sebelum menyatakan distribusi GAGAL, ulangi perbandingan ternormalkan.
  Sensus 11-09: 7/7 salinan profil sebenarnya cocok; BEDA adalah artefak alat ukur.
  Laporkan kejujuran ini apa adanya (membuktikan sensus dibaca mentah, bukan disalin).

## 3. Uji klaim API/pitfall library lewat introspeksi signature (tanpa eksekusi)

Pekerja menulis "`cache_buster` BUKAN argumen sah CrawlerRunConfig di versi ini".
Uji murah terhadap venv PRODUKSI (bukan venv uji pekerja):

```
<venv>/Scripts/python.exe -c "import inspect; from crawl4ai import CrawlerRunConfig as C; s=inspect.signature(C.__init__).parameters; print('cache_buster' in s, 'cache_mode' in s)"
```

Cocok untuk SETIAP resep skill yang mengklaim argumen hidup/mati: introspeksi
signature menjawab dalam detik tanpa memanggil jaringan/browser.

## 4. Uji determinisme+idempoten skrip dedup/agregasi dengan fixture sendiri

- Buat fixture SENDIRI (jangan pakai fixture pekerja): minimal kasus duplikat
  lintas-alat, variasi utm/fragment/trailing-slash, dan whitespace konten.
- Jalankan dua kali dengan URUTAN input dibalik; bandingkan sha keluaran
  (`unique.jsonl`) -> harus identik (deterministik + idempoten terhadap urutan).
- Cek juga non-match yang SENGAJA tidak boleh tergabung: path URL case-sensitive
  (`p/One` vs `p/one`) wajib tetap dua entitas (benar secara RFC); host lowercase,
  utm, fragment, trailing slash wajib dinormalkan.

## 5. Kontrol merah/hijau HTTP mandiri untuk norma bentuk body

Norma "build menolak maxDepth" diuji ulang controller tanpa membaca laporan verifier:
`curl -X POST /v2/crawl -d '{"url":...,"maxDepth":1}'` wajib 400 unrecognized_keys;
`{"url":...,"limit":1}` wajib success. Setiap norma bentuk-API di skill = dua panggilan
curl (merah + hijau) sebagai spot-check sah.

## 6. Giliran notifikasi kartu: urutan kerja tetap

Notifikasi = input status, BUKAN perintah dekomposisi. (1) list board --json + parse
id terkait (hati-hati: kartu bisa dibuat sesi/user lain dengan tenant turunan, mis.
WFCRAWL-0911-D06 - cek parents/children sebelum membuat apa pun); (2) verifikasi
klaim di disk (grep baris, versi, sha); (3) spot-check independen (butir 1-5);
(4) vonis + komentar ke kartu hilir bila ada temuan; (5) watchdog hanya bila masih
ada kartu non-terminal.

## 7. Payload inline besar kena hardline block

Satu baris terminal yang terlalu panjang (git add multi-path + grep + heredoc
sekaligus) ditolak parser blocklist TANPA regard ke isi operasi. Hanya bila perintahnya baca-saja dan penolakan karena bentuk: tulis
skrip .sh/.py via write_file lalu `bash <file>`; selain itu berhenti dan lapor. Payload yang diblok tersimpan di
`hermes/cache/blocked-scripts/` untuk ditelaah; jangan retry inline yang sama.
