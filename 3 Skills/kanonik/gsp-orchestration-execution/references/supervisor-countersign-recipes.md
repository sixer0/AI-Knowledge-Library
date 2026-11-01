# Resep countersign/vonis pengawas (beku dari gelombang misi buku 04-10 / misi manual 04-10 / GAYA-AHLI-1005, 05–06-10-2026)

Aturan induk: notifikasi `completed/timeout/blocked/gave up/superseded` = KLAIM pekerja. Vonis sah hanya dari artefak dibuka + pengukuran + reproduksi independen + komentar jejak. Pengawas BUKAN dispatcher: tidak membuat kartu/graf, tidak reopen, tidak force-done, tidak promosi.

## 1. Redeliver & duplikat notifikasi
- Notifikasi ganda kartu sama (timeout lalu completed; blocked lalu superseded): PROSES SEKALI. Sebelum kirim komentar: `hermes kanban show <id> | grep -c "<frasa-pembeda-vonis>"` harus 0; setelah kirim harus 1.
- Laporan status blocked yang baru diterima sering SUDAH tersolusikan board-mover (status kini done/running). Cek `status:` + event `blocked {reason}` + komentar controller SEBELUM menyusun vonis; vonis boleh jadi 'dicatat untuk jejak, bukan aksi'.
- `hermes kanban comments <id>` TIDAK selalu mengembalikan isi komentar; pakai `show` lalu potong segmen via skrip Python (subprocess) bila guard shell menolak inline panjang.

## 2. Pin lineage & rekonsiliasi hash
- Bekukan pin pengawas SHA256[:16] per artefak; catat SETIAP suntingan sah sebagai transisi pin lama->baru ber-alasan (garis keturunan, bukan pengganti diam-diam).
- Alias hash antar-agen: klaim worker bisa SHA1-16 padahal pengawas ukur SHA256-16. Sebelum vonis mismatch, probe multi-algoritma (md5/sha1/sha256) dan bekukan KEDUA nilai (konvensi NIT dua-algoritma berasal dari kasus CH04/RM-3).
- Repo yang rentan rewrite git: pin TREE-HASH (`rev-parse HEAD^{tree}` + sha256 konten), bukan commit-hash.
- Pin diukur SETELAH verify terakhir (hukum FIXA: run-4 PROMANUAL mati karena register ditulis ulang 39 detik SETELAH VERIFY tercetak; VERIFY.out tertinggal satu langkah). Verifikasi urutan mtime: sunting -> scan -> verify -> laporan; microfix WAJIB memicu rescan+reverify sebelum klaim AFTER.

## 3. Verifikasi angkut/carry byte-level
- `difflib.SequenceMatcher` vs berkas sumber beku: hitung blok/baris beda; bandingkan dengan 'tepat N suntingan terdaftarkan' + posisi baris. Cocok == nol-siluman terbukti mata kedua.
- Angkut-utuh lapis beku: `cmp` byte lapis buku kartu turunan vs beku kartu induk (lapis tak boleh bergeser saat rakit-meta), lalu string-match N cuplikan lapis ke naskah final (lapis tak dibuang).
- Disposisi: sensus ID worklist vs naskah; BEDAKAN sumbu 'disposisi fisik' vs 'butir rentang-agregat' (W30 agregat mengacaukan hitung naif); cek format ID NYATA dulu (`nn-Wn` vs polos) sebelum vonis 0 temuan.

## 4. Instrument blindness (paling sering berulang)
- Instrumen yang PASS padahal batch-review menemukan cacat SEMANTIK di berkas sama = buta kelas. Tes: apakah instrumen menguji PEMETAAN klausul-per-glif / konsistensi antar-prosa, atau hanya keberadaan/string-utuh/himpunan? Vonis: instrumen yang tak bisa MERAH jangan dipakai memvonis HIJAU.
- Protokol merah-hijau: sebelum suntingan, instrumen baru WAJIB mencetak FAIL atas state cacat kini (bekukan MERAH-BEFORE sebagai BEFORE sah). Run lanjutan DILARANG re-instrumentasi (ulang baseline = pembunuh anggaran kelas FIXA/CH12/FIX-BATCH-3).
- CRLF blindness: Python mode teks memakai universal-newlines (`\r\n` -> `\n`) sehingga CR>0 tak pernah terlihat. Sensor ujung-garis WAJIB mode byte (`newline=''` / `rb`). Deteksi lewat selisih byte-disk vs len konten LF == jumlah CR.
- Ambang per-kanal: probe pengawas WAJIB memakai kanal/ambang SAMA dengan artefak uji (C-6 >=18 prosa-umum vs P1a <=20 kanal kitab; salah kanal = FAIL palsu). Register ambang-per-kanal sah dua arah.
- Sensor format-first: 0 temuan = curigai instrumen dulu (prefiks regex longgar menangkap rujukan silang; heading nyata `### POLA-Lx-nn`; DOTALL melahap kutipan bersarang antar-blok -> pakai parsing per-baris).

## 5. Koreksi jejak
- Vonis terkirim tidak disunting; koreksi = KOMENTAR TERPISAH. Meta-pelajaran: koreksi juga wajib ukur segar sebelum dikirim - koreksi yang tak diukur menambah kesalahan (rantai 3 koreksi kasus 'workdir kosong vs direktori nihil': fakta final = direktori ADA, nol entri).
- Angka laporan = cetakan alat giliran itu: jangan kutip angka dari ingatan/laporan pihak lain; placeholder peta diisi cetakan `kanban list` terakhir sebelum kirim.

## 6. Penutupan superseded/partisi
- Uji klaim 'nol mutasi jalur terbit': cetak pin semua berkas sasaran vs baseline putusan - STATIS identik == superseded jujur. Aset beku run mati (verify teruji-merah, MERAH-BEFORE, kandidat, backup) = warisan sah mata berikutnya; vonis interim menyebut 'modal resume, bukan sampah'.
- Partisi capability-split sah atas eskalasi berulang (D-54: 3A/3B di bawah separuh anggaran yang terbukti habis). Tagih: pemenang kembar WAJIB mewarisi scratch bernilai kartu blocked.

## 7. Timeout parsial - klasifikasi & arahan
Klasifikasi state: (a) mati sebelum pena (nol artefak), (b) badan lahir gerbang belum (CH04/CH07/S9), (c) kandidat hijau belum diterapkan (D4/GEL3), (d) sebagian bab PASS + pin statis anti-sentuh (D2). Arahan run-2 selalu: kunci isi->verify->scanner->laporan; jadwal terikat-menit; AMBANG-B wajib ditulis sebelum menit terakhir; larangan baca-di-luar-worklist; split bersyarat bila timeout lagi (bukti akhir: resep-vs-kontensi condong ke 'orientasi bebas tanpa kerangka' - pasangan CH12/CH13 dispatch menit sama, hanya yang berpola resep menutup).

## 8. Kelas tiket scanner terpetakan (untuk adjudikasi FAIL, bukan tambal naskah)
- A4/C-4 substring TANPA batas kata: 'such as an aisle name' -> 'as an ai' positif-palsu (putusan M-05; fixture red-green wajib).
- C-8b LIMITATION_WORDS hanya EN: klausa batasan Inggris nyata ('as it were on 5 October 2026...') tak dikenali - terkonfirmasi 5x lintas papan; obat = patch scanner, bukan sunting naskah.
- C-6 rata-rata kalimat rendah = PROPERTI GENRE carry Ed2 (kasus 1-5: ch05/ch01/ch15/ch16/ch19) - memvariasi = khianati angkut-verbatim.
- C-14 stem: git-config, 'Retrieved', judul Hoober, stem sitasi API (RigidbodyType2D x3 = tiga sitasi berbeda), STEM SKEMA ENAM BIDANG itu sendiri (label bidang diulang by-design 25x) - whitelist struktural M-04.
- C-13 identifier subjek-konten API (shared_prefs/best_score/save_game/TTS Asli) = kelas allow-list controller.
- C-15 maks kalimat ekstrem = blok register H.2.1 (kelas FM).
- CJK tersesat di keluaran agen ('决定性' di laporan QC + body kartu + bahkan draf komentar PENGAWAS sendiri) - sensor CJK=0 wajib jalan bahkan untuk teks pengawas.
- Vision QA = satu-satunya penangkap kelas SEMANTIK figur (penanda-vs-elemen, desinkron caption, glyph-fallback mathtext '$'); hash stabil + margin hijau BUKAN bukti kebenaran visual. Gerbang deterministik baru (containment J, mathtext pre-render) berasal dari temuan vision - siklus mesin<->mata saling konfirmasi dua arah.

## 9. Gotchas alat
- Komentar panjang ber-apostrof: tulis ke berkas temp, kirim `$(cat berkas)`; rangkai perintah dengan `;` bukan `&&`.
- `uv run --python 3.11 python skrip.py` untuk analisis (python bisa jatuh ke alias Store). Inline loop/`&` memicu guard hardline - berhenti dan lapor; jangan memindahkan perintah ke skrip atau menjalankan ulang isi cache/blocked-scripts tanpa izin.
- Skrip append kontrak: grep penutup WAJIB dijalankan; 'grep 0' pasca-append = jalankan ulang SEKALI (dua kasus transient), jangan dobel-kirim.
- json.load dict: jangan `eval()`; bandingkan `before==after` sebagai dict. Multi-blok JSON ber-header = `json.loads` gagal 'Extra data' - parse regex per-blok.
