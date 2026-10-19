---
id: resep-comfyui-asset-factory
type: pelajaran
title: Resep final dan pitfall operasional ComfyUI Asset Factory (September 2026)
status: active
sumber: docs/2026-09-02-asset-factory/improve/04_delta-analysis.md
halaman: sec.3-4
tanggal_akses: 2026-09-03
kelas_bukti: sintesis
sensitif: tidak
perkara: asset-factory
tags: [comfyui, asset-factory, resep, pitfall, upscale, cutout]
links: [vault/precision-3d-factory, verification/threshold-lock.txt, comfyui-check/assetfactory/ledger.json]
penulis: gsp-librarian
diajukan: 2026-09-03
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Terverifikasi penuh tujuh dimensi. Provenans lolos pada semua spot-check: sha rubrik 1524afc0 cocok sha256sum nyata rubric_thresholds.md dan rubric_bytes 20343 serta re-lock-2 di threshold-lock.txt, sha ledger 6a7ac8e7 cocok sha256sum nyata comfyui-check/assetfactory/ledger.json dengan tepat 7 entri lapisan AF-*, tabel median per lapisan (U1 28 dan 30, U2 27, U3 29, U4 26 jalur rantai dengan jalur lama 25 kriteria warna 2, U6 6 vs baseline 7) identik dengan 04_delta-analysis.md sec.3 termasuk klasifikasi LULUS_AMBANG dan FAIL_REPRODUKSI, execution_cached 0,06 dtk dan cache-lru 16 cocok contract A7, flag chain2 dan PYTORCH_CUDA_ALLOC_CONF cocok D-TA-5 verbatim, KOREKSI-3 pointer bobot dan D-TA-9 cocok, kesimpulan U8-alt FLUX.2-klein tidak dibutuhkan cocok A9, OOM hang dan Pitfall 13-15 cocok improve/06, LayerStyle MIT api.github cocok sheet-U9 U9-6. Konsistensi internal terjaga termasuk batas klaim tanpa IMPROVEMENT_SAH yang sama sumbernya dengan sec.1 delta; metadata YAML valid, title sama H1; dedup bersih dua arah di vault dan wiki; kelas sintesis jujur; tidak sensitif bukan dosir; rujukan R-1 sampai R-9 terdefinisi dan terpakai semua. Catatan kurator minor tanpa pengaruh verdict: butir A13 secara fisik berada di contract sec.6.3 bukan sec.5 saat promosi nanti."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/resep-comfyui-asset-factory.md
catatan_keputusan: "dipromosikan: P-V-34 langkah 34; custodian terverifikasi, recount docs/2026-09-03_custodian-verify-pv34/recount-report.txt"
---

# Resep final dan pitfall operasional ComfyUI Asset Factory (September 2026)

## 1. Ringkasan

Objek ini merekam resep final dan pitfall operasional dari misi Asset Factory ComfyUI (jalur aset slide: t2i, img2img, cutout, upscale; video ditunda gate Q1; 3D dialihkan ke misi precision), yang ditutup 2026-09-03 dengan vonis akhir FAIL terklasifikasi (nol regresi kualitas lapisan produksi; FAIL berasal dari penutupan kontrak dan bentuk artefak, bukan mutu) [R-1 contract.md sec.5 A10/A13; R-2 verification/report_final.md VERDICT]. Rubrik mutu terkunci sha256 `1524afc09c9e16c1074ca3d0229825b098a5a330ac6a0c688bcd70f571635907` (20343 byte, re-lock-2) dicocokkan ulang dari disk pada run promosi ini; ambang lulus = median-3 >= 24/30 + hard-gate + no-krit <= 2, noise band 3 [R-3 verification/threshold-lock.txt; verifikasi run ini sha256sum identik].

## 2. Resep final per lapisan (klasifikasi taksonomi rubrik, bukan klaim improvement)

| Lapisan | Resep | Median-3 | Klasifikasi |
|---|---|---|---|
| U1 t2i (hero) | Z-Image Turbo int8_convrot, graph z_image_turbo_t2i.json, CLIPLoader type=lumina2 (jawaban memo R4), parameter mentah dari lembar resep | 28 (run 28,28,27) | LULUS_AMBANG |
| U1 t2i varian teks pendek | sama; terbukti sanggup render teks uppercase pendek siap-pakai (16/16 karakter benar, keputusan manusia vision) | 30 (run 30,30,30) | LULUS_AMBANG |
| U2 img2img | z_image_img2img.json rantai dari keluaran U1 | 27 (run 26,27,27) | LULUS_AMBANG |
| U3 cutout | birefnet_cutout.json + InvertMask (polaritas; amandemen HG-3.2 AM-1: tengah >=250 DAN keempat sudut ==0) | 29 (run 29,27,30) | LULUS_AMBANG (restate) |
| U4 upscale ber-alpha | rantai kanonis birefnet_upscale_chain.json: link IMAGE internal U3->U4 (tanpa round-trip file) + re-join alpha pasca-upscale; hard-gate baru HG-ALPHA-4x | 26 (run 25,26,26) | LULUS_AMBANG (jalur lama FAIL sah, median 25 tetapi kriteria warna median 2) |
| U6 3D (TRELLIS) | resep terkunci loop-20x (threshold 0.5, cfg 3.0, res 1024 wajib); default graph menyimpang (threshold 0.6 cfg 7.5) = HG-6.2 FAIL bila submit default | 6 (run 7,5,6) vs baseline historis 7/30 | FAIL_REPRODUKSI, tanpa improvement; kelas konsep saja |

Batas klaim penting: empat lapisan lulus berhak atas `LULUS_AMBANG` tetapi TIDAK berhak atas klaim `IMPROVEMENT_SAH` terhadap praktik lama, karena tidak pernah ada run kontrol graph skill lama pada seed sama (baseline U1-U4 := ambang itu sendiri). Hanya U6 punya baseline numerik historis [R-2 report_final.md; R-4 improve/04_delta-analysis.md sec.1, sec.3, sec.4]. Kesimpulan U8-alt jalur A: kebutuhan logo/judul pendek terjawab Z-Image existing; unduhan FLUX.2-klein 8-12 GB TIDAK dibutuhkan (belum diuji teks panjang/dekoratif) [R-1 contract.md A9].

## 3. Pitfall wajib (berlaku umum untuk semua operasi ComfyUI GSP)

1. Nol-cache graph unik per run: cache LRU ComfyUI (`--cache-lru 16`) menetralkan run beruntun identik (terukur `execution_cached` 0,06 dtk pada AF-S1). Wajib graph unik per run dan angka final dari sesi bersih [R-5 contract.md A7 lesson ledger].
2. Repro salin parameter mentah: submit wajib memakai parameter yang disalin persis dari lembar resep (contoh nyata: default graph TRELLIS menyimpang dari resep terkunci; submit default = hard-gate FAIL) [R-6 research/R-matrix.md K-6].
3. OOM maka restart server: setelah OOM berat bisa terjadi driver-level hang pada nvidia-smi dengan pemulihan kill; pola chain2 = kill -> start -> run -> kill [R-7 improve/06_patch_skill_t_6c893e07.md R5 Pitfall 13-15].
4. GPU serial mutlak (D-TA-5): maksimal 1 kartu GPU aktif, satu model per sesi, server-per-sesi pola chain2.sh dengan `--highvram --disable-dynamic-vram --cache-lru 16` + `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True`; batasan fisik mengalahkan batas paralel fleet [R-8 identification/02_structured.md D-TA-5].
5. Hilang alpha pada upscale model: UpscaleWithModel hanya RGB; round-trip file membuang kanal alpha sehingga latar transparan menampakkan foto asli (GAP-5/BF-2). Obat struktural: link IMAGE internal + JoinImageWithAlpha pasca-upscale [R-1 contract.md A8].
6. Pointer bobot basi: workflow bisa menunjuk berkas yang tidak ada di rak (z_image bf16 diminta, int8_convrot yang ada). Cek disk sebelum submit; perbaikan pointer = fase khusus, bukan diselundupkan ke smoke (D-TA-9) [R-1 contract.md A5 KOREKSI-3].
7. Ledger satu penulis: satu berkas ledger kanonis, kartu lanjutan menambah setelah kartu induk done; salinan liar diarsipkan (preseden rekonsiliasi t_5999a3ff) [R-1 contract.md A9].
8. Gerbang improvement D-TA-8: improvement sah = median > baseline DAN >= 2/3 run > baseline DAN selisih di atas noise band; tie = catatan ledger, BUKAN patch skill [R-8 D-TA-8; R-4 sec.1].

## 4. Temuan terbuka (bukan keputusan)

Steering A11 komposisi majemuk (multi-object, layering latar+depan, teks di atas scene) belum terjawab bukti: seluruh smoke memakai brief objek tunggal; ini lubang cakupan, bukan hasil buruk. LayerStyle (MIT) diajukan ke whitelist Q3 HANYA bila kebutuhan font merek muncul; alternatif nol-node = teks dirender di lapisan vektor luar ComfyUI [R-4 sec.5; R-9 research/sheet-U9-composition.md U9-6]. Lane riset known-open: CHECK 2/5 bentuk artefak milik pemilik lane R [R-1 sec. penutup STATUS].

## Rujukan

- [R-1] docs/2026-09-02-asset-factory/contract.md (sec.5 A7-A13, sec.6)
- [R-2] docs/2026-09-02-asset-factory/verification/report_final.md
- [R-3] docs/2026-09-02-asset-factory/verification/threshold-lock.txt (sha dicocokkan ulang run ini)
- [R-4] docs/2026-09-02-asset-factory/improve/04_delta-analysis.md
- [R-5] docs/2026-09-02-asset-factory/contract.md sec.5 A7 (lesson cache LRU, tercatat di ledger)
- [R-6] docs/2026-09-02-asset-factory/research/R-matrix.md (baris U6 + konflik K-6)
- [R-7] docs/2026-09-02-asset-factory/improve/06_patch_skill_t_6c893e07.md
- [R-8] docs/2026-09-02-asset-factory/identification/02_structured.md (D-TA-1..14)
- [R-9] docs/2026-09-02-asset-factory/research/sheet-U9-composition.md
- Ledger kanonis: comfyui-check/assetfactory/ledger.json (sha256 6a7ac8e732d6e339f3ddc7ea479b4bfd59171b351efe4c3c97d1746e091f1f3d, dicocokkan ulang run ini; 7 lapisan AF-*, tidak ditulis oleh run ini)
