---
name: nas-ftp-file-ops
description: Use when reading or writing files on the GSP UGREEN NAS.
version: 1.0.0
metadata:
  hermes:
    tags: [nas, ftp, ugreen, file-transfer, xlsx, verification]
---

# NAS FTP File Ops (UGREEN UGOS Pro)

Kelas tugas: ambil/ubah/kembalikan berkas master di NAS UGREEN GSP (host LAN
192.168.0.90, akun service GSP-NAS) dan pola tulis-aman-terverifikasi untuk berkas
kerja tim (xlsx master). Teruji end-to-end 09-09: update master korespondensi vendor
saat jalur browser (login Google via CDP) mentok.

## Peta jalur NAS (ukur 29-08 s/d 09-09)
- **FTP 21 = jalur utama yang terbukti**: login GSP-NAS OK, root = `/home` + `/GSP-DATA`.
- Panel HTTPS 9443 / portal https://ug.link/gspnas = aplikasi UGREENlink (SPA, butuh
  aplikasi UGOS) — jangan dihabiskan waktu di sana bila tujuan hanya baca/tulis berkas.
- SMB 445 terbuka tetapi share tidak terekspos (error 67) — jangan jadi jalur utama.
- Struktur map: `/GSP-DATA/Adint/Korespondensi/` (master xlsx korespondensi vendor),
  `/GSP-DATA/GSP Vendor/{Katalog,Meeting}/`, `/GSP-DATA/Swarm/{Workspace,Codebase}/<akun>/`
  (backup ekosistem per akun WebUiUser).

## Resep FTP (pitfall server UGOS)
1. `ftplib.FTP(host)` → login → **`f.voidcmd("TYPE I")` SEBELUM `SIZE`/`MDTM`**:
   di mode ASCII, `SIZE` pada file biner melempar 500/550 dan walker salah menyimpulkan
   file sebagai folder (preseden 09-09: semua PDF tampil `[dir]`).
2. **MLSD tidak didukung** (`501 OPTS command is not defined for MLST`). Jelajah pakai
   `nlst` + probe `size()` (file) vs `cwd()` (dir). Skrip siap pakai:
   `scripts/nas_walk.py`.
3. Sandi lewat variabel lingkungan sementara (`NASPASS=...` saat invoke), JANGAN ditulis
   literal ke skrip/berkas repo. Berkas env privat hanya boleh berisi placeholder
   teredaksi. Sanitasi jejak: `grep -rl <sandi>` workspace sebelum tutup misi.
4. Nama path ber-spasi aman lewat ftplib (parameter string), tapi hati-hati di `LIST`.

## Pola tulis-aman (WAJIB, teruji byte-presisi 09-09)
1. RETR berkas asli → simpan sebagai `nas_master.xlsx`; catat size + MDTM + sha256.
2. Uji kesegaran basis: bila sumber lain mengklaim salinan (mis. ekspor Google), diff
   seluruh sel dengan openpyxl dulu — `TOTAL_DIFF_CELLS == 0` baru sah jadi basis.
3. Edit lokal dengan openpyxl. Untuk tulis baris per entitas: **gerbang entity-match**
   (assert kolom nama == yang diharapkan) sebelum menulis; satu baris bergeser =
   salah-target.
4. STOR cadangan dulu dengan sufiks eksplisit (`..._backup-sebelum-update-<tgl>.xlsx`)
   di folder yang sama, lalu STOR menimpa berkas utama.
5. **Roundtrip verify di sesi FTP baru**: RETR ulang → sha256 == sha256 lokal →
   jalankan verifier yang sama pada hasil unduhan (bukan pada berkas lokal).
6. Gerbang penuh untuk xlsx data: uji titik sel terencana + diff seluruh sel vs
   recompute independen (rebuild dari cadangan) + hitung ulang angka agregat dari data
   aktual dan cocokkan dengan yang tertulis di dashboard. Tabel VERIFIKASI-AKURASI
   menempel di kartu penutup (standar SPK-002).

## Pivot lane (aturan turun dari misi 09-09)
Bila jalur tulis butuh sesi login yang tidak bisa diselesaikan di jendela kendali
(lihat `cdp-browser-session-ops`) dan objek target tersedia sebagai berkas di NAS:
tawarkan ke user alih jalur ke berkas NAS, dan setelah rilis sukses **nyatakan mana
sumber kebenaran** serta salinan mana yang kini tertinggal (Google Sheets 09-09
tertinggal dari NAS sampai user memutuskan sinkron).

## Gerbang anti-sesi-kembar (preseden 09-09 malam + 17-09, teruji)
Sebelum STOR master: RETR segar + assert sha256 == basis yang dibaca saat rencana disusun.
Bila kartu sudah `done` dan MDTM NAS lebih baru dari rilis sendiri = sesi kembar sudah
menulis: JANGAN timpa. Alih mode: (1) countersign independen rilis kembar (diff-planned,
entity-match, recount dashboard); (2) naikkan delta milik sendiri sebagai tambalan bertahap
di atas rilis kembar (backup r3/r4 tiap tahap, gerbang basis per tahap); (3) audit cakupan
hulu-vs-hilir (mis. semua surat vs COMM LOG) untuk menangkap yang dilewatkan kedua sesi.
Hasil 09-09: rilis kembar abd72810 lolos 13/13; tambalan menaikkan COMM LOG 37->42; sha
final e014386b; unplanned-diff 0; cakupan 100%.
Pola 17-09 (kembar MASIH HIDUP saat run berjalan): basis bisa bergeser DUA kali di tengah
audit (r1 00:10, r2 00:22). Jalur: audit + countersign pada salinan lokal r1, lalu SEBELUM
STOR re-fetch dan pindahkan basis tambalan ke versi terbaru (re-derive cacat yang masih ada;
cacat yang sudah ditambal kembar drop dari daftar). Assert sha == basis-tambalan tepat sebelum
STOR adalah satu-satunya penahan; skrip countersign sebaiknya diparameterkan
(basis + unduhan via argv) agar bisa dipakai ulang untuk r2/r3.
Forensik penulis: baca `docProps/app.xml` dalam zip xlsx — `Microsoft Excel` = sunting manual
user (sah jadi basis, jangan digugat), `Openpyxl` = rilis agen. `dcterms:modified` core.xml
memberi waktu UTC build. Preseden 17-09: basis kartu e1b630cd sudah digantikan sunting manual
user (094134ed) — bekerja dari basis riil, bukan basis kartu.

## Pitfall
- **Hyperlink target vs nilai sel = dua objek berbeda di openpyxl** (preseden 10-09: rilis
  menulis teks Zoom baru ke sel MEETING E7 tapi objek hyperlink lama masih menunjuk Meet
  lama; klik pengguna menuju alamat SALAH meski teks terlihat benar; verifier yang hanya
  membandingkan `cell.value` tidak menangkapnya). Gerbang wajib pada verifikasi tautan:
  untuk setiap sel ber-teks `http*`, assert `cell.hyperlink.target` cocok dengan teks;
  dan setiap sel nama entitas baru wajib hyperlink + gaya (warna FF0563C1 + underline
  single) disalin dari baris rujukan.
- **MDTM berzona UTC: bandingkan dengan `datetime.now(timezone.utc)`, jangan jam lokal naif** (preseden 13-09: sweep cron memakai `datetime.utcnow()`-naif vs now lokal WIB membuat umur backup terbaca +7 jam lebih tua (0,99 d jadi 1,28 d) sehingga dua berkas terhapus ±20 menit sebelum ambang 1 hari terlampaui; lane pembanding yang parse MDTM `tzinfo=utc` menemukan selisihnya). Ambang umur = `(now_utc - mdtm_utc)`, dan vonis hapus dicetak bersama kedua timestamp mentah agar audit bisa menghitung ulang.
- **Listing `#recycle` melempar `UnicodeDecodeError` pada ftplib default utf-8** (preseden 15-10 SYNCNAS-1014M: byte 0xa1 pada nama .tmp/ber-aksara aneh) -> buka sesi TERPISAH dengan `ftplib.FTP(host, encoding="latin-1")` untuk konfirmasi DELE memindahkan berkas ke recycle; jangan campur ke sesi verifikasi utama (jalur kandidat dalam satu sesi juga rawan memutus kontrol saat error).
- **Ambang recount verifier WAJIB diukur dari populasi riil basis, bukan disalin dari preseden** (preseden 15-10: ambang `nb==306` warisan giliran lama padahal kolom E basis sudah 313 -> FAIL ALAT; vonis delta +8 tetap benar). Ukur dulu, baru bekukan angka di checker; FAIL ALAT ditambal di checker, artefak rilis tidak disentuh, kejadian dicatat di kontrak.
- **`SIZE` gagal pada berkas besar** (550 "too large" pada mp4 1,2 GB) dan probe `cwd()`
  bisa ikut gagal -> walker yang mengandalkan size/cwd salah vonis dan MELEWATKAN berkas.
  Untuk inventaris (mis. sweep backup), pakai `f.dir(path)` (LIST) dan parse kolom pertama
  `d`/`-` sebagai penentu dir/file; MDTM tetap per berkas.
- **Menghitung entri sheet bertabel**: tabel objek membentang A1:?300 berisi baris kosong —
  `iter_rows` penuh menghasilkan 299 "entri". Hitang entri dari kolom identitas (nama
  vendor / kategori), bukan kolom mana pun non-empty.
- `retrbinary(..., cur.append)` dengan `cur=b""` melempar TypeError ('bytes' object ...
  interpreted as integer) dan `bytearray().append(bytes)` salah tipe: kumpulkan ke LIST
  lalu `b"".join(chunks)`.
- Path MSYS `/c/...` pada program natif: tetap pakai path Windows forward-slash
  (`C:/Users/...`) untuk berkas lokal (berlaku juga ke skrip FTP ini).
- Heredoc besar lewat terminal bisa terpotong: tulis skrip via write_file, jalankan
  `uv run --python 3.11 [--with openpyxl] python <skrip>`.
- Listing `#recycle` muncul di root share — abaikan, jangan di-walk (dalamnya salinan terhapus).
- **DELE path absolut membalas `550 permission denied` tetapi kadang TETAP dieksekusi async** (preseden 12-09: berkas hilang dari folder aktif dan muncul di `#recycle/<share>/...` meski balasan gagal; probe ulang "No such file" mengonfirmasi). Jangan vonis gagal dari balasan saja — verifikasi dengan LIST. Jalur andal: `cwd(folder)` lalu `DELE <nama relatif>` dengan jeda ±2 detik antar perintah (balasan 250 konsisten). Penghapusan lewat FTP memindahkan berkas ke #recycle per-share (bukan lenyap total); pemulihan via panel Files.
- **Jangan persempit ref table object saat menambah baris** (preseden 12-09: tblComm A1:K300 sempat dikecilkan ke A1:K85 = melanggar struktur sumber; tabel basis punya ruang tumbuh). Verifier wajib mengassert ref == basis.
  terhapus).
- Folder berisi file ber-ekstensi aneh (mis. BUKUv3) tampil `[dir]` sebelum TYPE I —
  jangan vonis struktur dari listing mentah.

## See also
- `scripts/nas_walk.py` — jelajah direktori FTP (nlst+TYPE I) siap jalan.
- `cdp-browser-session-ops` — lane browser yang skill ini gantikan saat gerbang login mentok.
- `gsp-verification-before-completion` — gerbang klaim untuk hasil tulis.
