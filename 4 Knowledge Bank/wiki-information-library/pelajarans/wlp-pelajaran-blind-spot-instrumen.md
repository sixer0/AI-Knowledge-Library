---
id: wlp-pelajaran-blind-spot-instrumen
type: pelajaran
title: "Blind spot instrumen ukur: deklarasi tanpa evaluasi + semantik klasifikasi permintaan (misi WLP, DEV-F19-2)"
status: active
sumber: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F19-walk.md
halaman: §2; CP-F23 §2; CP-F15 §2-§3
tanggal_akses: 2026-09-07
kelas_bukti: primer
sensitif: tidak
perkara: wlp
tags: [instrumen, alat-ukur, playwright, klasifikasi, wlp, brahma]
links: [wlp-resep-ukur-performa, wlp-pelajaran-objek-vs-content]
penulis: gsp-librarian
diajukan: 2026-09-07
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-07
catatan_verifikasi: "Verdict: terverifikasi. Alasan spesifik: DEV-F19-2 tercetak utuh di CP-F19 par.2 (RENDER_WRAP diimpor tanpa dievaluasi; INIT_SCRIPT wlp_lib.py:47 hanya mendefinisikan longtasks/sse/renders_pre; TypeError identik 6/6 attempt; preseden benar f17_smoke.py:116). Perbaikan semantik walk_reqs/idx_reqs dan bukti evaluasi wrap terverifikasi LANGSUNG di research/raw/wlp-f23/f23_agg.txt: tiap record mencetak wrap=wrapped dan baris klasifikasi 'walk_reqs=1 idx_reqs=1 bare_reqs(warisan)=0 segmented(warisan)=2'. Preseden discard F9 45% cocok kepala CP-F15; rentang 40-60% cocok DEV-F9-2 di CP-F9-testfull.md; F15 valid 7/7 nol discard cocok CP-F15 par.3. Rekomendasi konkret: tidak ada perubahan isi; objek ini layak dipromosikan berdampingan dengan objek resep (yang terakhir butuh revisi kecil pada label kelas XL, bukan pada lesson ini)."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-07
dipromosikan-ke: pelajarans/wlp-pelajaran-blind-spot-instrumen.md
---

# Blind spot instrumen ukur: deklarasi tanpa evaluasi + semantik klasifikasi permintaan (misi WLP, DEV-F19-2)

1. Dua buta-titik instrumen yang terbukti

1.1 Deklarasi tanpa evaluasi. Harness f17_walk.py mengimpor `RENDER_WRAP` dan memakai `window.__wlp.renders.length` padahal INIT_SCRIPT hanya mendefinisikan `window.__wlp = {longtasks, sse, renders_pre}`; `RENDER_WRAP` tidak pernah dipanggil sehingga `renders` undefined -> TypeError di 6/6 attempt. Sebab akar: skrip belum pernah dieksekusi siapa pun sejak ditulis. Preseden benar ada di saudaranya (f17_smoke.py:116 memanggil `page.evaluate(RENDER_WRAP)` sebelum memakai renders) [R-1]. Pelajaran: setiap field/dependensi yang DINYATAKAN dipakai oleh alat ukur wajib dievaluasi nyata dan tercetak di record keluaran; pada rerun F23 field `wrap=wrapped` tercetak di tiap record sebagai bukti evaluasi [R-2].

1.2 Semantik klasifikasi permintaan. Predikat warisan menghitung request bermotif `msg_limit` sebagai segmented, sehingga request indeks (`msg_limit=1&questions=1`) ikut terhitung sebagai halaman walk. Perbaikan: klasifikasi SEMANTIK baru - walk = bermotif `msg_before=`; refresh indeks (`msg_limit=1&questions=1`) direkam terpisah (idx_reqs) dan tidak dihitung sebagai segmented; field warisan tetap direkam agar banding baris-per-baris mungkin [R-2][R-3].

2. Resep pencegahan (generalisasi)

2.1 Alat ukur yang belum pernah jalan = alat yang belum ada. Sebelum dipakai membuktikan apa pun, jalankan sekali dengan keluaran kosong/sintetis dan pastikan semua sensor terisi (bukan hanya terimpor).

2.2 Klasifikasi harus atas makna motif URL, bukan atas token yang kebetulan muncul di banyak endpoint; bila semantik diperbaiki, pertahankan field lama berdampingan supaya rekaman historis tetap terbandingkan.

2.3 Laju discard instrumentasi adalah sinyal mutu instrumen: preseden F9discard 45% (switch-not-landed) vs F15 tertambal 7/7 nol discard menunjukkan polling-kondisi+grace mengalahkan settle berbasis-waktu [R-4].

3. Register rujukan

- R-1: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F19-walk.md §2 (DEV-F19-2, pesan error identik, wlp_lib.py:47, f17_walk.py:85, preseden f17_smoke.py:116).
- R-2: checkpoints/CP-F23-rewalk.md §2 (klasifikasi semantik walk_reqs/idx_reqs; wrap dievaluasi nyata).
- R-3: research/raw/wlp-f23/f23_agg.txt (rekaman `wrap=wrapped` per record; baris `walk_reqs=1 idx_reqs=1 bare_reqs(warisan)=0`).
- R-4: checkpoints/CP-F15-instr.md kepala + §2-§3 (diagnosis cap, T1-T5, 7/7 valid nol discard; CP-F9-testfull.md DEV-F9-2 laju discard 40-60%).

4. Batas berlaku

4.1 Preseden discard-rate dan polling-kondisi diukur pada pergantian sesi WebUI dengan pemuatan lambat (chrome + playwright, mesin tunggal); ambang grace/poll spesifik berkas f15_bench.py bukan angka portabel. Kesimpulan "alat belum pernah jalan = alat belum ada" berlaku umum sebagai prosedur, tetapi tidak menjamin ketiadaan cacat instrumen lain yang baru termanifestasi di beban berbeda.
