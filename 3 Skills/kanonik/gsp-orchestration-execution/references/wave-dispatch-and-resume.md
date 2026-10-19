# Wave Dispatch & Resume Cards for Large Fan-out Missions (terverifikasi 02-09, EXPO-INTEL-2026)

Konteks: blueprint menghasilkan >4 kartu pengumpul (misi EXPO: 18 kartu kumpul + 9 hilir).
Bridge mengklaim SETIAP kartu ready ber-assignee gsp-* (lihat hq-dispatch-bridge-quirks.md),
jadi mendaftar 18 kartu datar = 18 worker menyerbu gateway sekaligus. Resep di bawah membuat
dispatcher mematuhi batas konkurensi (maks 5 per misi, tanpa batas per jenis; norma user 03-09B, kap host 20) TANPA polling gate manual.

## 1. Wave chaining lewat multi-parent edges

- Registrasi kartu per gelombang; tiap kartu wave N+1 diberi SEMUA id kartu wave N sebagai
  parents. Wave 1 ber-parent kartu blueprint/TA yang sudah done.
- CLI: `hermes kanban create --parent <id>` repeatable; `lad_card.py --parents id1,id2,...`
  menerima multi-parent (pisahkan koma).
- Efek: wave berikutnya baru jadi ready saat wave sebelumnya terminal → antrean tertib,
  tidak ada kartu menembus batas paralel, tidak ada edge yang perlu di-reclaim.
- Audit wajib setelah registrasi (pelajaran 02-09): baca field `parents` di LEVEL ATAS JSON
  `show --json` (bukan di dalam objek task), pastikan nol kartu yatim. Simpan `cards.map`
  (kode kartu -> id kanban) sebagai register actor.
- Rantai hilir bercabang normal: merge-card (mis. dedup) boleh punya banyak parents
  (EXPO: K21 dengan 18 parents); percabangan {K25, A26} dari K24 lalu join di V27 sah
  selama DAG tanpa siklus.

## 2. Body kartu dirender generator, bukan diketik tangan

- Tulis satu skrip python (mis. `gen_bodies.py`) yang mengekstrak blok aturan/keyword
  VERBATIM dari artefak kanonik hilir-hulu (mis. regex `^### K\d{2}[^\n]*$` atas
  `01_translated.md` seksi keyword) dan me-render body per kartu dari template.
- Tabel kartu (id, bucket, klaster, region, path tulis, E, assignee, kriteria verif) hidup
  sebagai SATU sumber kebenaran di dalam generator; output: `bodies/<cid>.txt` + baris
  `cards.map`. Jaminan: tidak ada keyword/rule hilang karena transkripsi tangan; diff body
  bisa diaudit.
- Skrip generator = infra/ops controller (pengecualian sempit G-2), bukan kerja substantif.
- Prasyarat read-only bersama (mis. `SCHEMA.md` untuk semua pengumpul) juga sah ditulis
  controller sebagai salinan deterministik dari RT/TA, lalu dianggap memenuhi langkah
  blueprint tersebut (catat di Decision Log).

## 3. Kartu lanjutan (resume) dari partial-handoff — resep isi

Worker menutup `STATUS: partial-handoff` = penutupan sah; JANGAN re-dispatch buta.
Resume card (parents=[kartu asal], mata ke-2 dari maks 3) WAJIB memuat:
1. SISA_KERJA bernomor sesuai urutan prioritas dari laporan worker.
2. METODE TERBUKTI dari catatan parent (disalin eksplisit, mis. "backend ddgs tunggal bing
   via skrip + probe curl user-agent browser ke situs resmi").
3. LARANGAN mengulang jalur mati yang sudah didokumentasikan parent.
4. Batas batch per panggilan tool (mis. <= 10 query per panggilan eksekusi) agar tidak
   mati kena timeout tool di tengah batch.
5. Aturan append-not-overwrite untuk artefak parsial yang sudah ada di disk (jangan hapus
   baris valid existing; header harus sama).
6. Target kuantitatif kartu induk tetap disebut (mis. total >= 15 baris) + verifikasi diri
   dengan skrip pola sama.

## 4. QA controller di tengah gelombang (saat wave berikutnya jalan)

- Jalankan skrip QA deterministik kecil atas artefak wave awal: kesamaan set header, enum
  kolom (Region/Status), skema URL dan nol spasi di URL, hitung baris per direktori.
- Kolom ekstra yang tidak berbahaya: SAH, jangan blokir worker. Legitimasi pemetaannya ke
  kartu konsolidasi lewat KOMENTAR kartu (mis. "kolom Catatan ekstra dipetakan ke Catatan
  master saat merge; nilai 'Kota Negara' bertumpuk -> pisahkan saat dedup"). Kartu kanban
  adalah kanal instruksi hilir yang benar, bukan re-dispatch.
- Sampling acak beberapa baris per berkas (nama/tanggal/sumber) untuk cek kewarasan isi.

## 5. Watcher satu proses untuk seluruh misi

- Satu skrip python latar (notify_on_complete=true): poll status tiap kartu tiap ~90 detik,
  cetak HANYA transisi status, keluar saat semua terminal atau melewati deadline, lalu
  cetak inventaris artefak (path, byte, jumlah baris CSV).
- Chat turn tidak pernah memblokir menunggu worker; progres user dijawab dari log watcher +
  audit langsung board saat diminta ("cek progres" -> tabel status + angka baris nyata).

## Pitfalls yang terlihat nyata di misi ini

- `--shape` lad_card yang berbeda dari saran bentuk hanya WARN (keputusan operator sah);
  rantai resume pakai `rantai-N` agar jejak mata rantai terbaca.
- Membuat berkas body via heredoc terminal yang isinya mengandung '&' ditolak guard shell
  ("uses '&' backgrounding") -> buat dengan write_file, baru dirujuk `--body-file`.
- Alias `python` Windows bisa jatuh ke stub Microsoft Store (pesan 'Python was not found');
  jalankan skrip via `uv run --python 3.11 python <skrip>`.
