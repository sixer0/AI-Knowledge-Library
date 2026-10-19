# Kalibrasi Noise Juri Independen (terukur 02-09, loop-20x TRELLIS)

Prinsip induk: "Agent said success → verify independently" berlaku juga ke VERIFIER-nya
sendiri. Juri model (vision/LLM) punya noise terukur dan wajib dikalibrasi sebelum
klaim improvement dipakai membuat keputusan.

## Bukti terukur
- Render IDENTIK, rubrik SAMA, 5 penilaian terpisah: 8 → 4 → [6,5,5]. Rentang ±3 poin.
- Repro baseline dengan params PERSIS (v6) di skala juri yang sama: 5 → 3.
  Artinya skor pra-kalibrasi tidak apel-ke-apel dan baseline resmi ikut bergeser.
- Konsekuensi: dua klaim improvement palsu nyaris lolos bila pakai skor tunggal.

## Standar minimum (pakai saat juri = bagian dari gerbang keputusan)
1. Skor = **median 3 run juri** (bukan rata-rata; median tahan outlier 0-vs-6).
2. Improvement sah hanya bila: median > best DAN >=2 run individually > best.
3. Kalibrasi di awal sesi keputusan: repro satu baseline known-good di kondisi juri
   yang sama. Bila tidak kembali ke angka lama, buang angka lama, pakai rentang baru.
4. Ambang improvement HARUS di atas rentang noise pipeline terukur (contoh: noise 3-6
   maka ambang >=7), bukan sekadar "> skor sebelumnya".
5. Juri melihat PASANGAN (referensi vs hasil) dalam satu panggilan, bukan gambar tunggal.
6. Fix-hint juri = HIPOTESIS untuk diuji, bukan instruksi. Bukti nyata: juri menyuruh
   "turunkan threshold ke 40-45" padahal threshold tinggi justru meruntuhkan bagian
   tipis mesh (thr 0,65 menghasilkan skor 2/30); kepatuhan buta = siklus GPU terbuang.

## Pola driver yang terbukti (loop20_driver.py, comfyui-check/satellite)
- judge3() = tiga panggilan judge() lalu statistics.median, simpan runs mentah
  di ledger supaya bisa diaudit.
- Ledger per iterasi: id, axis, params, gen_status, score(median), runs[], detail,
  artefak (glb/render). FAIL juga dicatat sebagai jejak diagnosis, bukan dihapus.
- Gerbang best disimpan di file terpisah (loop20_best.json) agar bisa dikalibrasi
  ulang tanpa edit kode.

## Sinkron dengan
- gsp-comfyui-slide-stack/references/trellis-workflow.md (noise juri + tabel triase OOM)
- gsp-orchestrator-worker (pitfall rantai generation: CHAIN_DONE palsu, struktur varian)
