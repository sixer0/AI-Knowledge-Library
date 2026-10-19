---
id: promanual-uji-dua-rute-1004
type: pelajaran
title: "Uji dua rute lokal T1-T7: efek instruksi bergantung skala model, floor-effect dataset, dan batas CoT sebagai audit"
status: active
sumber: docs/2026-10-04-prompt-manual/uji/hasil-uji-j.md; docs/2026-10-04-prompt-manual/research/R2/register-beku.md baris 38-41, 49, 51-52, 69-72, 84-85, 197
halaman: hasil-uji-j.md 270 baris; checksum dataset beku sha256 per uji tercantum di body
tanggal_akses: 2026-10-05
kelas_bukti: primer
sensitif: tidak
perkara: promanual-1004
tags: [promanual-1004, uji-dua-rute, overthinking, few-shot, ground-only, floor-effect]
links: [promanual-korpus-register-1004]
penulis: gsp-librarian
diajukan: 2026-10-05
misi: PROMANUAL-1004
kartu: t_c42af89f
pin_sha16_register: R2=54cc5ffe2824458a
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-05
catatan_verifikasi: "Verdict: terverifikasi. Alasan: 14 sel vonis T1-T7 kedua model dicocokkan baris-per-baris dengan tabel ringkasan uji/hasil-uji-j.md baris 236-251, semuanya identik; tujuh checksum dataset (16 heks pertama) cocok tabel baris 16-22; setup runtime (llama-server build 10632 commit 11cd98842, RTX 5070 Ti 16 GB, Ollama v0.35.1 WSL Ubuntu-24.04, ctx maks 40960, think:false, temperature 0, tiga ulangan) cocok baris 8-10; token keluaran 183 vs 7 dan rasio ~26x cocok baris 72-73; T5 prompt_tokens 32.002 dan pemotongan diam-diam 20.482 cocok baris 163/174/265; floor-effect T3 (kelima rute 100,0 persen std 0,000; rentang permutasi 0,0..11,1 std 0,052) cocok baris 102-106 dan 122; T6 admits 100 vs 0 persen dan akurasi jawab 25,0 vs 62,5 persen cocok baris 195-196 dan 209-210; SEMUA koordinat register R2 (baris 38-41, 49, 51-52, 69-72, 84-85, 197, 255-258, 264), R1 baris 128, serta NEG lintas lajur (R3 baris 359-365, R4 baris 365-366) menunjuk baris berisi butirnya; pin R2 54cc5ffe2824458a cocok byte; hasil-uji-j.md 270 baris cocok. Rekomendasi kurator (non-blocking): label sitasi 'refusal-aware tuning [R2, KL-R1-110 register R1 baris 128]' salah prefiks, ID dan koordinat benar (KL-R1-110 memang di R1 baris 128), ganti prefiks R2 menjadi R1 saat promosi."
riwayat-catatan-verifikasi: "Verdict: terverifikasi. Alasan: 14 sel vonis T1-T7 kedua model dicocokkan baris-per-baris dengan tabel ringkasan uji/hasil-uji-j.md baris 236-251, semuanya identik; tujuh checksum dataset (16 heks pertama) cocok tabel baris 16-22; setup runtime (llama-server build 10632 commit 11cd98842, RTX 5070 Ti 16 GB, Ollama v0.35.1 WSL Ubuntu-24.04, ctx maks 40960, think:false, temperature 0, tiga ulangan) cocok baris 8-10; token keluaran 183 vs 7 dan rasio ~26x cocok baris 72-73; T5 prompt_tokens 32.002 dan pemotongan diam-diam 20.482 cocok baris 163/174/265; floor-effect T3 (kelima rute 100,0 persen std 0,000; rentang permutasi 0,0..11,1 std 0,052) cocok baris 102-106 dan 122; T6 admits 100 vs 0 persen dan akurasi jawab 25,0 vs 62,5 persen cocok baris 195-196 dan 209-210; SEMUA koordinat register R2 (baris 38-41, 49, 51-52, 69-72, 84-85, 197, 255-258, 264), R1 baris 128, serta NEG lintas lajur (R3 baris 359-365, R4 baris 365-366) menunjuk baris berisi butirnya; pin R2 54cc5ffe2824458a cocok byte; hasil-uji-j.md 270 baris cocok. Rekomendasi kurator (non-blocking): label sitasi 'refusal-aware tuning [R2, KL-R1-110 register R1 baris 128]' salah prefiks, ID dan koordinat benar (KL-R1-110 memang di R1 baris 128), ganti prefiks R2 menjadi R1 saat promosi."
catatan_keputusan: "dipromosikan: PROMANUAL-1004 ILPRO t_c42af89f: custodian verdict terverifikasi; pin register 4/4 terukur ulang; non-sensitif non-dosir; dedup wiki+IL 0"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: pelajarans/promanual-uji-dua-rute-1004.md
---

# Uji dua rute lokal T1-T7: efek instruksi bergantung skala model, floor-effect dataset, dan batas CoT sebagai audit

Temuan empiris hasil eksekusi nyata (bukan kutipan literatur): dua rute runtime lokal memakai
model yang sama dalam tiap blok uji, temperature 0, tiga ulangan per rute, dataset dibekukan
SEBELUM eksekusi. Aturan vonis: selisih akurasi rata-rata < 5 poin DAN di dalam rentang
variasi ulangan = TIDAK BEDA; hasil NEGatif/NULL tetap terbit (TA-D-13). Semua angka di bawah
adalah cetakan laporan uji (uji/hasil-uji-j.md, dihitung ulang oleh scripts/make_report_final.py
dari log mentah per panggilan uji/raw/calls_<T>_<runtime>.jsonl).

## 1. Setup runtime [R-1: hasil-uji-j.md seksi runtime]

- Rute besar: llama.cpp llama-server build 10632 commit 11cd98842, model Qwen3.6-14B-A3B
  finetune GGUF, GPU RTX 5070 Ti 16 GB (-ngl 99), reasoning-effort none (thinking mati,
  terverifikasi smoke test).
- Rute hemat: Ollama v0.35.1 WSL Ubuntu-24.04, qwen3:0.6b Q4_K_M (ctx maks 40960), think:false.
- Checksum dataset beku (sha256, dihitung sebelum eksekusi): T1 9aff3cdc84c21f8c...,
  T2 2f079f515bfa9dbc..., T3 73c3984f97653186..., T4 6e962373c1e092e0..., T5 d68f9a6ae34a52a6...,
  T6 4133abbb2ae3a722..., T7 e11096289dea1d64... (penuh di laporan hulu).

## 2. Vonis lintas uji (14 blok = 7 uji x 2 model)

| uji | topik | 14B | 0,6B |
|---|---|---|---|
| T1 | persona vs tanpa persona | B MENANG (-10,0) | TIDAK BEDA |
| T2 | CoT vs langsung | A MENANG (+8,0) | A MENANG (+22,7) |
| T3 | zero-shot vs 5-shot | TIDAK BEDA (floor) | A MENANG (+100,0) |
| T4 | XML vs Markdown vs prosa | B MENANG (-10,0) | B MENANG (-36,7) |
| T5 | penempatan informasi 32K | TIDAK BEDA | TIDAK BEDA (sama-sama gagal) |
| T6 | ground-only vs tanpa | A MENANG (+8,3) | B MENANG (-11,1) |
| T7 | negasi vs perintah positif | TIDAK BEDA | B MENANG (-10,0) |

## 3. Pelajaran yang naik (dengan dasar)

3.1 EFEK INSTRUKSI BERGANTUNG SKALA MODEL. Ground-only menaikkan akurasi +8,3 poin pada 14B
(100% pertanyaan tak-terjawab dijawab TIDAK TAHU, vs 0% tanpa instruksi) tetapi menurunkan
11,1 poin pada 0,6B (over-application 'TIDAK TAHU' pada pertanyaan yang terjawab: akurasi
jawab 25,0% vs 62,5%). Vonis per blok dilaporkan terpisah, TIDAK dirata-ratakan lintas model
- interaksi ukuran model justru temuannya. Konsisten dengan literatur beku: refusal-aware
tuning [R1, KL-R1-110 register R1 baris 128] dan CoT emergent pada skala [R2, KL-R2-052, baris 70].

3.2 FLOOR-EFFECT DATASET BUKAN BUKTI KESETARAAN. T3 pada 14B: kelima rute 100,0% std 0,000 -
nol variansi adalah artefak kesulitan dataset (klasifikasi POS/NEG dengan jodoh kata eksplisit),
bukan temuan bahwa urutan contoh tidak berpengaruh. Sinyal permutasi hanya hadir di 0,6B
(rentang antar-permutasi 0,0..11,1%, std 0,052) dengan arah mendukung KL-R2-022 (order
sensitivity Lu et al., arXiv 2104.08786): zero-shot 100% mengalahkan semua varian 5-shot.
Implikasi praktik: untuk model >=14B pada tugas klasifikasi sederhana, zero-shot sah dan lebih
hemat; uji transfer-permutasi butuh dataset lebih sulit.

3.3 CoT NAIK AKURASI DENGAN BIAYA BESAR DAN TIDAK SAH SEBAGAI AUDIT. T2: +8,0 poin (14B)
dan +22,7 poin (0,6B), biaya token keluaran 183 vs 7 pada 14B (~26x). Batas interpretasi:
chain-of-thought tidak boleh dipakai sebagai bukti/alasan audit keputusan - penjelasan
plausible bukan penjelasan benar [R2, KL-R2-066, baris 84; sumber arXiv 2305.04388].

3.4 DELIMITER: Markdown/prosa mengalahkan XML pada kedua rute uji ini (-10,0 poin 14B;
-36,7 poin 0,6B) - berlawanan dengan anjuran umum tag XML untuk model Claude [R2, KL-R2-004].
  Temuan lokal dua model uji ini, bukan vonis universal; dokumen vendor tetap otoritatif untuk
modelnya sendiri.

3.5 ADAPTASI PANJANG KONTEKS WAJIB DIBUKUKAN. Target protokol T5 = 32K token. llama.cpp
tercapai (prompt_tokens terukur 32.002); Ollama memotong diam-diam ke 20.482 token di bawah
num_ctx 40960 yang diminta (done=length). Recall 0,0% pada ketiga posisi adalah temuan nyata
pada panjang itu (jawaban halusinasi dari angka pengisi), dan vonis TIDAK BEDA pada nol persen
berarti 'sama-sama gagal' - kesimpulan kurva-U posisi hanya berlaku untuk blok 14B.

3.6 NEGASI ANTI-PATTERN TERUKUR: pada prompt ber-negasi, scaling model BERBALIK (inverse
scaling, semua tipe LM 125M-175B yang diuji) [R2, KL-R2-179, baris 197; arXiv 2209.12711].
T7 lokal konsisten arah pada 0,6B (positif menang +10,0), netral pada 14B.

## 4. Register negatif penting lintas lajur (jejak kegagalan yang menghemat kerja ulang)

- arXiv export API: 429 persisten 3 percobaan + timeout -> jalur HTML abs page sah pengganti
  [R2, NEG-R2-01, register baris 255].
- anthropic resource-library page 404; cookbook.openai.com/examples 404 (pindah domain ke
  developers.openai.com/cookbook) [R2, NEG-R2-03/04, baris 257-258].
- llms.txt platform.openai.com 404 -> varian domain baru developers.openai.com/llms.txt 200
  [R2, NEG-R2-10, baris 264].
- Harga per-token MiniMax/Cohere/ERNIE per-model dan tarif Spark: TIDAK ADA DI RAK per tanggal
  potong (halaman pricing = shell marketing / butuh login) - kosong ber-akun, jangan dicari
  ulang pada jalur yang sama [R3, NEG-R3-04/05/06/10, baris 359-360, 361, 365].
- CDX NOSNAP snaps=0 = bukti tidak ada salinan arsip, bukan kegagalan alat [R3, NEG-R3-07, baris 362].
- Batch API DeepSeek tidak ada di sitemap resmi -> field dikosongkan, bukan diisi [R4, NEG-R4-01, baris 365].
- Siklus-konfirmasi tercatat append-only: vonis mata-1 "Cohere Batch hanya Embedding Jobs"
  DICABUT - API v2 punya resource batches resmi [R4, NEG-R4-02, baris 366].
- ID arXiv tebakan: 8 contoh 200 tapi judul fisika/bio/astro -> entity-match MENOLAK, dibuang
  dari register [R2, NEG-R2-02, baris 256].
