# Mengukur Pengulangan Antar-Delegasi DALAM Satu Misi (level-2 audit)

Preseden ukur: 30-09, kelas misi riset/kajian teknis multi-lajur. Bahan: rantai
kartu nyata FTDEEP-0921 (30 kartu, lajur W1-W5), CCTV-DP-0923 (7 kartu, lajur
L1-L6), FT-EVAL-0920 (15 kartu). Semua angka di bawah adalah hasil ukur
deterministik atas body kartu di papan + artefak docs pada giliran itu.

## Kapan resep ini dipakai

Bila user menanyakan "pengulangan pekerjaan" dan menyebut KELAS TUGAS spesifik
("riset dan kajian teknis", "misi multi-lajur", "dalam multi delegasi"), ia
memaksudkan level-2: titik mana pekerjaan terulang antar kartu dalam SATU misi,
bukan ritus lintas giliran. Jawaban level-1 (cron/siklus) ditolak dengan "sepertinya
kamu miss" (kejadian nyata 30-09).

## Resep ukur (semua via execute_code + `hermes kanban --board default list --json`)

### 1. Salinan instruksi antar-layer (RT -> TA -> kartu lajur)
Split body kartu jadi kalimat (`re.split(r"[.;\n]", b)`), bandingkan himpunan
kalimat antar pasangan layer. Hasil preseden: 22/49 kalimat RT (45%) muncul utuh
di TA; 22/73 kalimat kartu W1 (30%) identik dengan TA.

### 2. Boilerplate antar-kartu se-gelombang
Split body per paragraf (`\n\s*\n`, panjang >40), normalisasi whitespace, potong
120 char pertama sebagai kunci, hitung Counter kemunculan lintas kartu. Kunci
muncul di >=4 dari 5 kartu = blok tempelan. Preseden: ±460-480 char identik per
kartu lajur (blok RULE PRESISI-HASIL, LIMIT-AWARE, WAKE-ORKESTRATOR, aturan
tempel). Body kartu lajur riset kelas ini: 5.500-6.900 karakter.

### 3. Fetch ganda antar-lajur (biasanya temuan termahal)
Regex `https?://...` atas SEMUA berkas lajur (`docs/<misi>/lanes|lajur/**/*.md|.log|.json`),
normalize (strip protokol/www/trailing punct/lowercase), petakan URL -> himpunan nama
lajur. URL di >=2 lajur = kandidat fetch ganda. Preseden FTDEEP: 78 dari 457 URL
unik (17%) lintas-lajur; teratas arxiv.org 38, docs.together.ai 10,
docs.firecrawl.ai 5. Kontrapreseden CCTV-VQI-0926: 61 URL, 0 tumpang tindih —
pemisahan lingkup yang rapi menekan metrik ini tanpa alat; laporkan keduanya agar
tidak overclaim.

### 4. Rasio kartu remediasi per kelas cacat
Kelompokkan judul kartu misi berdasar pola (RT|TA|L\d|W\d|V\d|F\d|DEFECT|SK-*).
Preseden: FT-EVAL 4 kartu remediasi dari 15 (27%) untuk 2 temuan verifier sejenis
(pasangan fix+recheck per temuan); FTDEEP memakai pola sehat DEFECT -> SK-CREATE ->
SK-DIST -> SK-CR sekali jalan menular ke norma. Vonis: temuan sistematis harus
tambal-templat-sekali, bukan per-lajur.

### 5. Aktivitas vs watchdog hidup
Untuk tiap job cron watchdog interval, cocokkan tenant/prefiks judul misi di papan:
`status` distribution + max(completed_at|started_at|created_at). Semua kartu done +
aktivitas terakhir berhari-hari lalu = watchdog menjaga misi mati. Preseden 30-09:
5 watchdog agent-run interval, seluruh misinya 100% done (HARGA-DEMS 34/34, RING
223/223, EXPO26 126/126, dst.), total ±44 run agen/hari untuk kerja deterministik.

## Koreksi yang wajib dilakukan sebelum klaim umur kartu

Umur kartu `blocked` dihitung dari field `created_at` (epoch DETIK) di JSON papan,
bukan dari kolom lain. Preseden kesalahan 30-09: laporan pertama menyebut "6-9 hari"
dari pembacaan epoch yang salah; ukur ulang benar = 0-29 hari dan sebagian kartu
dibuat ulang <24 jam oleh triase. Aturan gerbang: >48 jam tanpa komentar triase =
cacat (aturan 10 gsp-orchestration-execution). Bila laporan awal keliru, koreksi
eksplisit di jawaban berikutnya (kelas T5 claim-gap: akui spesifik).

## Format keluaran level-2

Tabel peringkat `dampak x frekuensi`: kode | pengulangan | bukti ukur | frekuensi |
perbaikan tersedia (rujuk norma/obat yang SUDAH ada di doktrin fleet, mis.
pipeline-kanonis-v1 untuk fetch-sekali, R-01 register beku untuk sintesis, R-10
kesegaran korpus). Tutup dengan catatan batas: butir mana diukur penuh vs sebagian.
