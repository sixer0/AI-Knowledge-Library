# Kalibrasi Estimasi LAD dari Laju Nyata (EXPO-OPT 2026-09-02)

Sumber angka: audit misi EXPO-INTEL-2026 (docs/2026-09-02-expo-intel-2026/contract.md
seksi Audit Efisiensi; state.db profil gsp-data-collector dan
gsp-vendor-crawler-specialist, 16 sesi worker, 02-09).

## Konstanta laju nyata (search sehat, jalur ddgs)

| Aktivitas kartu | Laju terukur | Catatan |
|---|---|---|
| 1 query pencarian (ddgs/bing) | 1 iterasi + 15-40 dtk | termasuk baca hasil & seleksi |
| 1 baris tervalidasi sumber primer | 2-4 query | probe situs resmi + ekstraksi + cek tanggal |
| 1 ekstraksi halaman resmi | 1-2 iterasi | dengan extract_char_limit 10000 |
| Kartu kumpul sehat (8-12 query inti + 6-10 pelebar) | 10-18 baris | selesai 13-25 menit |
| Batas anggaran efektif worker (cap 150 iterasi) | ~120 iterasi | sisakan 20% untuk tutup jujur (aturan Ambang) |

## Aturan kalibrasi E (menggantikan asumsi search normal)

1. E kartu kumpul = (perkiraan baris target x 3 query x 1,5 iterasi) + 20 iterasi
   overhead (baca SCHEMA/instruksi, tulis CSV, cek diri). JANGAN pakai asumsi
   1 query per baris; itu penyebab C01/C11 habis anggaran pada 12/50 query.
2. Kartu yang diproyeksikan E > 0,5 x cap dipecah per region lebih dulu, bukan
   dirantai harapan partial-handoff. Satu putaran ulang penuh = +24 menit dan
   baca-ulang seluruh instruksi (kejadian C11b).
3. Ambang evaluasi partial-handoff: worker mengevaluasi di query ke-60% anggaran
   (bukan saat benar-benar habis) supaya SISA_KERJA masih terukur.
4. Bila backend search terdeteksi bermasalah (noise/403 berulang pada 3 query
   pertama), worker berhenti mengejar jalur itu dan langsung pindah curl situs
   resmi atau tandai GAP; jangan membakar 30+ iterasi untuk satu klaster.

## Pembanding after-rollout (diisi saat misi berikutnya)

Baseline 02-09 (searxng rusak, tanpa batas ukuran alat): 27 menit/kartu,
66-94 ribu token/panggilan, cache read 2%, jeda model 17,3 dtk, 248 ribu
token input per baris hasil, 2 dari 10 kartu partial-handoff.
Target pasca P1-P6: <= 18 menit/kartu, <= 25% token/panggilan, 0 partial-handoff
pada kartu yang E-nya sesuai aturan 1.

## Cross-check independen dari kanban DB (02-09, 19 run kartu C01-C18)

Angka di bawah diukur terpisah dari state.db: durasi run dari kolom
`task_runs.started_at/ended_at`, baris dari CSV `collection/expo2026/*/expo-raw.csv`
dan hasil kartu, jumlah query dari laporan metode worker di komentar kartu.

| Metrik | Nilai | Bukti |
|---|---|---|
| Laju sehat (ddgs-bing hidup) | 1 baris / 2-4 query | C07 66q->24br; C16 66q->23br |
| Laju degradasi (noise/403/domain mati) | 1 baris / 4-6 query | C10 60q->11br; C13 40q->10br; C11 12q->2br |
| Waktu per baris (kartu done satu-run) | agregat 1,24 mnt; rentang 1,03-2,09 | 9 kartu, 219 mnt, 177 baris |
| Kendala pengikat | waktu bridge 30 mnt, BUKAN iterasi | semua run mati di 22-31 mnt; 4 partial karena waktu, 0 karena iterasi; satu run melapor pakai ~35 dari cap 150 |
| Biaya putaran ulang penuh | 24-28 mnt + baca ulang instruksi | C07 timeout 30,6m lalu 19,5m; C11 27,6m lalu C11b 25,9m |

Konsekuensi norma: E wajib dua satuan (iterasi DAN menit); bentuk dipilih dari
E_eff = max(E_iter, E_menit). Kartu pengumpul: maks 15 baris target, pencarian
berhenti pada menit ke-20 (sisa 10 mnt untuk tulis artefak + cek + laporan),
evaluasi partial di query ke-60% anggaran. Laju degradasi terdeteksi pada 3
query pertama => seluruh gelombang dirancang pada laju degradasi (target baris
separuh, jumlah kartu naik), bukan worker mengejar target mustahil.
