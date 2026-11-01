# Registrasi Fan-out Besar dengan Gating Wave (terverifikasi 02-09, misi fan-out besar)

Pola untuk mendaftarkan banyak kartu worker sekaligus (18 kartu kumpul + 9 hilir) tanpa
menembus batas konkurensi (maks 5 per misi, tanpa batas per jenis; norma user 03-09B, kap host 20) dan tanpa kartu yatim yang jalan
mendahului upstream.

## 1. Gating wave lewat parents antar-wave (bukan prioritas urutan)

Dispatcher menghormati edge `parents_not_done`, jadi **edge DAG adalah pengatur
konkurensi yang sebenarnya**. Jangan mengandalkan urutan wave sebagai niat lisan saja:

- Semua kartu wave 1: `--parents <id-TA-done>`.
- Semua kartu wave 2: `--parents <id1>,<id2>,<id3>` (SEMUA kartu wave 1).
- dst. Wave N+1 orangtuanya = seluruh kartu wave N. Akibatnya wave N+1 baru siap
  claiming setelah wave N terminal.
- Kartu konsolidasi hilir (mis. dedup master) boleh ber-parent banyak sekaligus
  (terverifikasi: K21 dibuat dengan 18 parent, semua diterima).
- Cabang paralel aman: dari satu parent bisa bercabang (K24 -> {K25, A26}), lalu
 汇聚 di verifier (V27 parents = K25,A26).

CLI dasar mendukungnya: `hermes kanban create --parent` bersifat repeatable, dan
`lad_card.py --parents` menerima daftar dipisah koma. Satu-satunya batasan praktis:
body kartu jangan disisipkan inline lewat shell bila memuat `&` (guard terminal
menafsirkannya sebagai backgrounding, dan heredoc ber-`&` juga ditolak) — tulis body
ke file via write_file, lalu `--body-file`.

## 2. Render body kartu dari dokumen RT/TA lewat generator (jangan salin tangan)

Untuk misi yang aturan pencariannya panjang (keyword multi-bahasa, enum, format kolom),
buat skrip `gen_bodies.py` yang:

1. Membaca `identification/01_translated.md` dari disk dan mengekstrak blok keyword
   per klaster secara utuh (regex heading `### KNN ...`), lalu
2. Merender body per kartu dari TEMPLATE dengan slot (bucket, region, path tulis,
   bahasa pencarian, target baris minimal, verifikasi diri), dan
3. Mencetak manifest JSON per kartu (card, assignee, est, body path, title) yang
   dipakai loop registrasi.

Manfaat: keyword TIDAK pernah disingkat (syarat blok W blueprint), body konsisten
antar 18 kartu, dan perubahan aturan cukup regenerasi + recreate. Verifikasi isi
dengan `wc -c bodies/*.txt` (kisaran 4-6 KB per kartu adalah tanda blok keyword utuh).

## 3. Audit edge wajib sebelum gelombang jalan (ulang pelajaran 02-09)

Segera setelah register, jalankan audit kecil yang membaca `show --json` tiap kartu dan
melaporkan `(status, len(parents))`. `parents` ada di LEVEL ATAS JSON (bukan di dalam
objek `task`). Kartu dengan `parents=0` = cacat: link sekarang juga. Di EXPO26 audit
menunjukkan semua 27 kartu punya 1-18 parent, nol yatim, wave 1 saja yang `running`.

Catatan toolchain: `python` di shell ini bisa jatuh ke alias Microsoft Store (output
buntu "Python was not found" dengan exit_code 0 — berbahaya karena terlihat sukses).
Selalu `uv run --python 3.11 python script.py` untuk skrip audit.

## 4. Watcher rantai panjang (fan-out + hilir)

Untuk misi 25+ kartu dengan durasi jam, watcher python lebih baik dari loop bash:
poll `show --json` per kartu tiap ~90 detik, **emit hanya saat status berubah**
(baris `CID ? -> running`), exit saat semua terminal atau deadline (7 jam), lalu
tutup dengan laporan artefak (walk direktori collection: ukuran + jumlah baris CSV).
Jalankan via terminal background=true + notify_on_complete=true. Ini memberi jejak
progres per-kartu yang bisa dijawab saat user minta "cek progres" tanpa polling ulang.

## 5. Gerbang naturalisasi pada artefak ANTARA (putusan controller 02-09)

`scan_ai_footprint.py --channel doc` menandai gaya dokumen kerja (tabel padat, paragraf
pendek) sebagai FAIL C-6/C-7/C-12 pada artefak antara seperti `01_translated.md` dan
`02_structured.md`. Keputusan yang sah dan tercatat di Decision Log (D-06/D-07 misi
EXPO26): artefak antara internal DITERIMA dengan catatan (selama C-1/C-2 = 0), dan
gerbang penuh ditegakkan di deliverable user-visible (prosa Methodology/Catatan xlsx,
laporan handoff) lewat AC verifikasi (AC6) — bukan memaksa RT/TA menulis prosa panjang
yang justru merusak kegunaan dokumen kerjanya.

## 6. SCHEMA read-only sebagai prasyarat kolektif (pengecualian G-2 sempit)

Saat blueprint menugaskan "publikasi SCHEMA.md" sebagai langkah worker TAPI ia adalah
prasyarat read-only seluruh gelombang dan isinya hanya salinan deterministik dari
RT/TA, controller boleh menerbitkannya sendiri sebagai infra/ops (kartus + bukti di
contract doc, D-08). Yang tetap dilarang: kerja substantif milik worker (risi, skor,
konsolidasi, penulisan deliverable).
