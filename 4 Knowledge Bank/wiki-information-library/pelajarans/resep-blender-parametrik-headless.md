---
id: resep-blender-parametrik-headless
type: pelajaran
title: Resep final dan pitfall Blender parametrik headless (Precision 3D Factory, September 2026)
status: active
sumber: docs/2026-09-02-precision-3d-factory/pilot_p1/P1-GATE.md
halaman: sec.1-2
tanggal_akses: 2026-09-03
kelas_bukti: sintesis
sensitif: tidak
perkara: precision-3d-factory
tags: [blender, 3d-parametrik, resep, pitfall, precision-3d-factory]
links: [vault/asset-factory, pilot_p1/P1-GATE.md, research/R-GATE-rekomendasi.md]
penulis: gsp-librarian
diajukan: 2026-09-03
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: Re-verifikasi custodian loop revisi 1 dari maks 3; objek direkonstruksi penuh oleh librarian pasca korupsi all-NUL pada 2026-09-03 sekitar 16:57 lalu diverifikasi ulang penuh tujuh dimensi dari nol terhadap sumber di disk, bukan hanya butir hash. Provenans lolos penuh; hash pengukuran P1 di seksi 3 kini 64 karakter identik byte dengan P1-GATE.md baris 48 dan artefak pilot_p1/out termasuk dim_check.json, roundtrip_measure_glb.json, gate_qa_trimesh.json; median P2 15 plus median_per_kriteria k1=5 k2=0 k3=1 k4=2 k5=3 k6=4 cocok judging_log.md baris 150 dan 156; sha rubrik 1524afc0 dan sha ledger 6a7ac8e7 cocok sha256sum nyata; hash pin blender-mcp f0759291 dan 87e60c9b cocok _LISENSI.tsv baris 12; vonis per resep cocok R-GATE sec.1; gap G-04 sampai G-10 cocok sec.3; kandidat perbaikan P2 cocok countersign.md. Integritas body terbukti; diff terhadap usulan awal body_1_blender.md hanya selisih satu digit 9 pada hash P1 sebagai perbaikan temuan lama, tidak ada perubahan lain. Frontmatter lolos yaml.safe_load dengan 18 kunci lengkap tanpa duplikat dan nilai utuh tidak terpotong, title sama H1 pertama, rujukan R-1 sampai R-13 terdefinisi dan terpakai semua, dedup bersih dua arah vault dan wiki, konsistensi internal antar seksi utuh, kelas sintesis jujur, sensitif tidak dan bukan dosir sehingga tidak menuntut gerbang manusia. Temuan lama hash 63 karakter dinyatakan selesai; jejak verdict lamanya terbaca di docs/2026-09-03_custodian-verify-pv34/recount-report.txt.
catatan_keputusan: "dipromosikan: P-V-34 langkah 34 loop revisi 1; custodian re-verifikasi penuh 7 dimensi pasca rekonstruksi, verdict terverifikasi (recount-recheck-1.txt)"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/resep-blender-parametrik-headless.md
---

# Resep final dan pitfall Blender parametrik headless (Precision 3D Factory, September 2026)

## 1. Ringkasan

Objek ini merekam resep final dan pitfall terverifikasi dari misi Precision 3D Factory (jalur Blender Python API headless untuk aset 3D presisi), hasil langkah 1 sampai 33 blueprint yang ditutup dengan vonis verifikasi deterministik dan countersign agree pada 2026-09-03. Mesin produksi: `blender -b -P script.py` pada Blender 5.2.0 LTS build fbe6228777e7, CPU murni (Cycles CPU + OpenImageDenoise), tanpa GUI, tanpa GPU, tanpa satu pun pemasangan addon baru di luar whitelist [R-1 contract.md sec.2 Q1/Q6; R-2 P1-GATE.md sec.1]. Konvensi satuan: satu Blender unit setara satu milimeter [R-2 P1-GATE.md].

## 2. Resep final yang lolos gerbang (verdict per lembar resep)

| Resep | Verdict | Inti metode | Bukti |
|---|---|---|---|
| (a) Primitif parametrik + modifier bpy | LOLOS (13 uji M5 lulus di 5.2.0 LTS, dua koreksi drift API terdokumentasi) | bangun mesh dari parameter sheet YAML, modifier apply dengan cek return operator | [R-3 recipes/a-parametric-primitives.md baris 15, 148-195] |
| (b) Pengukuran/QA dimensi | LOLOS untuk sisi Blender; QA trimesh pasca-ekspor bergerbang (lapis W1) | `bound_box` x `matrix_world`, pasangan vertex/edge via depsgraph, vertex_groups utk fitur bernama, `bmesh.is_manifold` | [R-4 recipes/b-dim-measurement.md baris 25, 165-172] |
| (c) Ekspor + round-trip GLB/OBJ | LOLOS tanpa butir M gagal; round-trip headless byte-deterministik | io_scene_gltf2 bawaan (Apache-2.0), impor ulang factory-default sebagai pembanding | [R-5 recipes/c-export-roundtrip.md baris 16-43] |
| (d) Material PBR + lighting studio | LOLOS (9/9 CHECK PASS); anggaran render 1080p sekitar 34 detik per frame pada scene balok tunggal | Principled BSDF (Base Color/Metallic/Roughness/IOR), three-point AREA lights, kamera 85mm sensor 36 | [R-6 recipes/d-material-lighting.md baris 27, 231-235] |
| (e) Jembatan MCP | produksi GAGAL-GERBANG (addon menolak mode headless, pemeriksaan `bpy.app.background` di fungsi `start()` kode sumbernya); review visual LOLOS BERSYARAT Q7 | blender-mcp hanya loop review pasca-render, bukan produksi | [R-7 R-GATE-rekomendasi.md sec.1; R-8 contract.md P3 Q7] |

## 3. Hasil pilot (angka terverifikasi, jangan dikutip tanpa rujukan)

- P1 objek SBOX-2624P revisi r01 (enclosure 150x150x65 mm + koordinat lubang mounting, datasheet EKAS R4): gerbang P1 PASS. Hash pengukuran kanonis `cd214125ca3860f8c4aab876570e89df842f4d2c1439f00f4e49bd21c42e1bbd` identik lintas tiga generasi run (dimcheck x2, gate x2, round-trip); GLB byte-identik pada empat proses terpisah; deviasi OBJ maksimum ordo 1,5e-05 mm (rotasi-Z kosmetik importer, tiga orden di bawah toleransi). Toleransi QA: maks(0,5 mm; 0,1% dimensi) [R-2 P1-GATE.md sec.2; R-8 contract.md P3 Q5].
- P2 scene produk realistis: FAIL sah terhadap ambang terkunci 24/30. Median total 15; median per kriteria k1=5, k2=0, k3=1, k4=2, k5=3, k6=4; dictatorship check gagal pada tiga kriteria (k2 material, k3 pencahayaan, k4 komposisi border-line). Akar suara bulat tiga juri: nilai PBR tercatat di scene tetapi tidak terbaca visual sebagai aluminium metalik, dan pencahayaan terbaca datar. Countersign independen menyetujui vonis (agree) dengan aritmetika direkomputasi ulang dari skor mentah. Ambang tidak digeser; anggaran revisi N=3 belum terpakai; keputusan iterasi milik controller [R-9 pilot_p2/judging_log.md baris 150-183; R-10 verification/countersign.md VERDICT].
- Kandidat perbaikan P2 dari countersign (belum dieksekusi): eksposur/cahaya (world strength 1.0 warna 0.05, key 12W fill 4W), bukan nilai PBR, karena socket metallic/roughness terbukti sampai shader (scene.py:150-153, CHECK C8 PASS) [R-10 countersign.md temuan].

## 4. Pitfall wajib (setiap munculnya angka berasal dari artefak yang dirujuk)

1. Inflasi satuan seribu kali pada impor GLB ke scene berskala 0,001: penyebab internal belum dilacak; mitigasi terbukti = sesi verifikasi selalu factory settings [R-11 R-GATE-rekomendasi.md G-04].
2. `modifier_apply` konteks salah mengembalikan `{'CANCELLED'}` tanpa exception; exit code saja tidak menangkap kegagalan. Wajib cek return operator dan `view_layer.objects.active` [R-11 G-05].
3. Drift API nyata di 5.2: namespace `object.primitive_*` hilang (pakai `bpy.ops.mesh.*`), enum wireframe bernama `WIREFRAME` bukan `WIRE`. Dilarang menyalin contoh kode pra-5.2 tanpa uji simbol [R-11 G-06; R-3].
4. Determinisme wajib diukur di level pengukuran/piksel, BUKAN SHA-256 berkas: writer PNG menyisipkan metadata tEXt/eXIf sehingga byte beda walau piksel identik bit [R-11 G-07].
5. Nol-cache versi non-GPU: tiap proses menulis ke direktori keluaran unik agar hasil lama tidak terbaca sebagai hasil baru [R-2 P1-GATE.md sec.2].
6. Repro wajib menyalin parameter mentah dari lembar resep, bukan default graph [R-12 objek pelajaran asset-factory pitfall serupa pada ComfyUI].
7. Render CPU serial: satu proses Cycles pada satu waktu (serial rule D8), jendela render diumumkan di kartu [R-13 02_structured.md Concurrency Notes].

## 5. Batas klaim

Seluruh verdict prosedural-terverifikasi per artefak per tanggal 2026-09-02/03 tanpa klaim fleet-wide (D-TA-10). Lapis P2 masih terbuka untuk iterasi revisi oleh controller; angka P2 di sini adalah baseline lapisan, bukan vonis akhir jalur Blender. Skrip karangan misi berstatus "karangan-sendiri-belum-berlabel" sampai controller menetapkan label internal (gap G-10) [R-11 G-10].

## Rujukan

- [R-1] docs/2026-09-02-precision-3d-factory/contract.md sec.2, sec.7 P3/P6
- [R-2] docs/2026-09-02-precision-3d-factory/pilot_p1/P1-GATE.md
- [R-3] docs/2026-09-02-precision-3d-factory/research/recipes/a-parametric-primitives.md
- [R-4] docs/2026-09-02-precision-3d-factory/research/recipes/b-dim-measurement.md
- [R-5] docs/2026-09-02-precision-3d-factory/research/recipes/c-export-roundtrip.md
- [R-6] docs/2026-09-02-precision-3d-factory/research/recipes/d-material-lighting.md
- [R-7] docs/2026-09-02-precision-3d-factory/research/R-GATE-rekomendasi.md
- [R-8] docs/2026-09-02-precision-3d-factory/contract.md sec.7
- [R-9] docs/2026-09-02-precision-3d-factory/pilot_p2/judging_log.md
- [R-10] docs/2026-09-02-precision-3d-factory/verification/countersign.md
- [R-11] docs/2026-09-02-precision-3d-factory/research/R-GATE-rekomendasi.md sec.3 (gap list G-01..G-14)
- [R-12] vault/asset-factory (objek pelajaran terkait, links)
- [R-13] docs/2026-09-02-precision-3d-factory/identification/02_structured.md (Concurrency & Wave Notes)
