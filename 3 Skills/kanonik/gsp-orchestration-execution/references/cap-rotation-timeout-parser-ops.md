# Rotasi cap, triase timeout, dan audit parser — pola teruji misi mobile / HDKCOMP / misi visual (29-09)

## 1. Timeout → retry dispatcher = penyelamat modal (jangan re-dispatch buta, jangan pecah kartu dini)
Siklus terbukti berulang pada kartu bridge ber-plafon ~30 menit: run-1 timeout MENINGGALKAN modal
parsial di disk (CSV/manifest/berkas kerja sudah tertulis, tinggal fase laporan/penutupan), dispatcher
retry otomatis, run-2 mengaudit modal lalu menutup. Kasus: V03, V07, A1, A4, L16-C, STY-B.

Triage wajib sebelum vonis apa pun:
1. Cari jejak modal di disk (manifest/CSV/berkas target + scratch/cache per-lane).
2. Klasifikasi:
   - modal penuh, tinggal tutup → tunggu retry, NOL aksi manual;
   - modal parsial (mis. CSV yatim tanpa laporan) → tetap tunggu retry; ambang pecah kartu adalah
     **timeout KEDUA tanpa artefak** (preseden W12: beban baca 16 berkas → pecah sumber per-bab);
   - nol modal dua kali → pecah lingkup (kartu anak separuh cakupan, parent = kartu asal).
3. Jangan pernah memvonis "stuck" dari notifikasi timeout saja; ukur dulu.

## 2. Parser benar sebelum vonis — cacat alat ukur menghasilkan false defect
Tiga kasus satu sesi, semua salah di PEMISAH atau POLA, bukan di artefak:
- CSV lane: delimiter TAB vs pipe berbeda antar berkas (A2/A4 pipe, A3 TAB, A1 pipe). Deteksi dari
  baris kepala, jangan meniru berkas tetangga.
- awk -F',' pada CSV berkutipan → "URL-MATI" palsu; pakai csv.DictReader.
- Sel multi-URL ("a ; b") diprober sebagai satu string → InvalidURL massal palsu; linkcheck WAJIB
  per-URL, vonis mati hanya bila SEMUA URL dalam sel gagal (hasil sejati 47/48 hidup).
- Pola kode: `rcParams({...})` vs aktual `rcParams.update({...})`; pola nama FIG huruf besar vs
  aktual huruf kecil (`ge-fig-01-*.png`).
Aturan: angka final HANYA dari cetakan parser yang sudah dikoreksi dan cocok terhadap sampel mentah;
laporkan koreksi alat secara eksplisit (rekaman metode), jangan diam-diam.

## 3. Cap konkurensi = rem pelepasan kartu BARU, bukan kill-switch kerja berjalan
Ketika dispatcher memajukan lebih banyak kartu daripada maks per tipe profil (mis. 4 collector paralel):
- JANGAN block/stop kartu yang sehat dengan modal bertambah di disk (memutus kerja sehat membakar modal);
- BEKUKan pelepasan kartu baru sampai komposisi kembali ≤ cap;
- unblock antrean bertahap per terminal (pesan block menyebut pemicunya eksplisit).
Pitfall: `hermes kanban block` menolak kartu status `todo` (hanya `ready`) — kartu todo tertahan rantai
dependensi memang tidak perlu dan tidak bisa diblock.

## 4. Mirror artefak misi ke repo (kebijakan standing user) — hemat & non-destruktif
- Cache mentah (research/raw, _probe*, __pycache__, *.apk, file >2 MB) dikecualikan dari commit —
  preseden misi panduan GEN-2; utuh tetap di workspace lokal, nyatakan pengecualian ke user.
- Terlanjur staged? `git diff --cached --name-only | grep pola > daftar.txt` lalu
  `xargs -a daftar.txt git restore --staged --` (non-destruktif). Percobaan `rm -rf` cache di mirror
  kena gerbang persetujuan — jangan diulang lewat jalan tikus; unstage sudah cukup.
- Log kunci hasil (*.log) sering kena gitignore repo; force-add HANYA log bukti (UTILISASI, DG-RERUN)
  dan laporkan keputusan itu.
- Scan secret pada staged diff: pola api[_-]?key|ghp_|sk-|AKIA|password= — angka 0 wajib sebelum commit.
- Push + verifikasi `git ls-remote origin HEAD` == `git rev-parse HEAD` (dua hash dicetak).

## 5. Sisip CHANGELOG CRLF-safe lewat skrip python
Terminal inline dengan `$(...)`+sed+grep panjang bisa kena hardline blocklist
'oversized/unparseable payload'. Resep: skrip python baca bytes → `split(b'\r\n')` → sisip baris entri
baru setelah header `|------|` → tulis bytes. Jangan pakai patch tool pada berkas CRLF besar
(old_string multi-baris gagal cocok karena representasi line ending).

## 6. Uji tandingan klaim generator/builder
Klaim 'rcParams ditempel identik dari D1' diverifikasi dengan mengekstrak blok kanonik D1 §3.4 lalu
membandingkan pasangan kunci:nilai per skrip generator (28/28 identik) — bukan percaya klaim kartu.
Pola umum: setiap klaim konsistensi lintas-berkas diuji dengan ekstraktor yang sama terhadap semua pihak.

## 7. Instantiate gelombang dari WAVE-MAP blueprint (HDKCOMP-V terbukti)
Baca peta gelombang dari berkas blueprint (regex baris tabel), buat kartu per gelombang via lad_card.py
dengan body yang menempel: path batch CSV, SCHEMA kolom, aturan entity-match/CER-001,
syarat jejak VERIFIKASI-AKURASI+ladder, LIMIT-AWARE (anggaran + AMBANG-B), WAKE-ORKESTRATOR.
Langsung block gelombang di luar cap puncak dengan pesan pemicu unblock. Variasi penamaan jejak antar
gelombang (hasil-Vnn.md / hasil-Vnn-VERIFIKASI.md / VERIFIKASI-Vnn.md) itu normal — normator agregat
harus mencocokkan pola longgar, bukan satu nama kaku.
