---
id: status-lisensi-whitelist-3d-slide
type: fakta
title: Status lisensi whitelist komponen produksi 3D dan aset slide GSP (September 2026)
status: active
sumber: docs/2026-09-02-precision-3d-factory/research/recipes/_LISENSI.tsv
halaman: 32 baris
tanggal_akses: 2026-09-03
kelas_bukti: sekunder
sensitif: tidak
perkara: precision-3d-factory
tags: [lisensi, whitelist, mit, apache, gpl, blender-mcp]
links: [research/R-GATE-rekomendasi.md, contract.md#P6]
penulis: gsp-librarian
diajukan: 2026-09-03
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Terverifikasi penuh tujuh dimensi. Provenans lolos pada seluruh spot-check wajib: _LISENSI.tsv nyata berisi 32 baris kandidat di luar header dan selfcheck 16/16 dua run identik terkonfirmasi di R-GATE-rekomendasi.md baris 28; tabel W0-W3 cocok verbatim dengan R-GATE sec.2 termasuk Apache-2.0 io_scene_gltf2 berkas LICENSE.txt 11.631 B salinan c-lane/c03, MIT trimesh LICENSE.md salinan f-lane/F01, label README CadQuery baris 165-167 dan build123d baris 257-259 dengan berkas LICENSE belum dibuka, serta pin blender-mcp ==1.9.0 hash wheel f0759291b5748c35fcdabd68f89b684cfaae6c61dd475f87d591dddcef63f9fa 95.247 B dan sdist 87e60c9b0b9f4f373231855d8d6ebe82792e598f13cc93ffacaa984cd45a24f2 111.507 B unggah 2026-08-30 pasca insiden 10-08-2026 dengan syarat kumulatif Q7 penuh; daftar DILARANG cocok paragraf DILARANG R-GATE dan baris tsv-nya termasuk license=None lab/blender_mcp isu #42 dan CC-BY-NC-SA Text2CAD; rak ComfyUI cocok AF-R1 baris lisensi Unlicense plus allowCommercialUse, BSD-3-Clause RealESRGAN pada salinan sumber openmodeldb, GPL-3.0 RMBG gerbang G6, MIT LayerStyle api.github 2026-09-02, non-komersial atau community untuk Ideogram-4 dan FLUX.1-dev serta Kontext dan SD3.5 pada AF-R5; dua pengakuan jujur TIDAK TERUJI untuk bobot BiRefNet dan comfyui-videohelpersuite terkonfirmasi sebagai kekosongan nyata di riset misi sehingga bukan klaim karangan. Keputusan manusia W3 DITAHAN dan W1 pin-plus-hash cocok contract precision sec.7 P6, G-10 dan G-12 bimdown-cli cocok gap list R-GATE sec.3. Metadata YAML valid dengan title sama H1, dedup bersih dua arah di vault dan wiki, sensitif tidak dan bukan dosir meski isinya menandai keputusan manusia, rujukan R-1 sampai R-8 terdefinisi dan terpakai semua. Catatan kurator minor tanpa pengaruh verdict; tabel W2 menulis identifier lisensi sebagai Apache-20 tanpa titik yang secara substansi benar sebagai label README saja, dan tanggal_akses frontmatter 2026-09-03 adalah tanggal baca objek sementara body sudah menyatakan masa berlaku status per 2026-09-02."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/status-lisensi-whitelist-3d-slide.md
catatan_keputusan: "dipromosikan: P-V-34 langkah 34; custodian terverifikasi, recount docs/2026-09-03_custodian-verify-pv34/recount-report.txt"
---

# Status lisensi whitelist komponen produksi 3D dan aset slide GSP (September 2026)

## 1. Ringkasan

Objek ini merekam STATUS LISENSI tiap komponen whitelist yang dipakai jalur produksi GSP per 2026-09-03, hasil riset lisensi per-berkas (bukan badge) pada dua misi. Tabel presisi 3D bersumber dari `_LISENSI.tsv` (32 baris kandidat, selfcheck 16/16 dua run identik) dan rekomendasi R-GATE lapis W0-W3 yang disetujui controller (Decision Log P6). Klasifikasi: "teruji per-berkas" = berkas LICENSE dibuka langsung; "label-saja" = hanya badge/README/API label; "TIDAK TERUJI" = berkas tidak memuat footer/section lisensi saat digrep [R-1 _LISENSI.tsv; R-2 R-GATE-rekomendasi.md sec.2; R-3 contract.md precision P6].

## 2. Whitelist presisi 3D (lapis W0-W3)

| Lapis | Komponen | Status lisensi | Keputusan |
|---|---|---|---|
| W0 | Blender 5.2.0 LTS + bpy/bmesh | GNU-GPL-3.0-or-later (biner); skrip pengguna tidak terikat GPL (preseden P-R1 baris CLI); keluaran ekspor bukan turunan GPL | DISETUJUI, nol pasang [R-1 baris 1; R-2 W0] |
| W0 | io_scene_gltf2 (exporter glTF bawaan) | Apache-2.0 TERUJI per-berkas (LICENSE.txt 11.631 B dibuka, salinan c-lane/c03) | DISETUJUI (bawaan) [R-1 baris glTF-Blender-IO] |
| W0 | Exporter OBJ inti + Cycles CPU + OpenImageDenoise | internal Blender (rantai W0) | DISETUJUI, nol pasang [R-2 W0] |
| W1 | trimesh (QA pasca-ekspor, pip Python murni di luar Blender) | MIT TERUJI per-berkas (LICENSE.md dibuka, salinan f-lane/F01) | DISETUJUI dengan pin versi + SHA-256 wheel dicatat kartu pemakai [R-2 W1; R-3 P6] |
| W2 | CadQuery, build123d | Apache-20 label README (baris 165-167 / 257-259); berkas LICENSE per-berkas BELUM dibuka | TUNDA; tidak dibutuhkan pilot; pemakai kelak wajib buka berkas LICENSE sebelum instal [R-1; R-2 W2] |
| W3 | blender-mcp (ahujasid) pin ==1.9.0 | MIT bersandar berkas LICENSE repo + badge README (PyPI info.license kosong, license_expression='MIT', terverifikasi ulang E06). Pin hash wheel f0759291b5748c35fcdabd68f89b684cfaae6c61dd475f87d591dddcef63f9fa (95.247 B) + sdist 87e60c9b0b9f4f373231855d8d6ebe82792e598f13cc93ffacaa984cd45a24f2 (111.507 B), upload 2026-08-30 PASCA insiden pembajakan akun maintainer 10-08-2026 | KONDISIONAL review-only; PEMASANGAN DITAHAN = BUTUH KEPUTUSAN MANUSIA (controller/user). Syarat kumulatif bila disetujui: pin versi+hash, DISABLE_TELEMETRY=true, 16 tool aset eksternal mati, tulis kunci mcp_servers lalu restart agen, smoke Windows dulu [R-1 baris blender-mcp; R-2 W3; R-3 P6] |

Dilarang jadi dependensi (putusan berdasar berkas, bukan selera): lab/blender_mcp (license=None terverifikasi E15, isu #42 OPEN Windows), Sverchok (GPL-3.0 addon; inspirasi kerangka saja), Text2CAD/CC-BY-NC-SA-4.0 gated (haram masuk deliverable klien), DeepCAD/GenCAD/CAD-Recode/Genspex (belum atau gagal diverifikasi), ntriq-x402-blueprint (berbayar per panggilan), freecad-mcp/FreeCAD/OpenSCAD/blender-open-mcp (pembanding di luar gate Q1, sebagian TIDAK TERUJI per-berkas) [R-1; R-2 daftar DILARANG].

## 3. Aset ComfyUI di rak (jalur produksi image)

| Komponen | Status lisensi | Catatan |
|---|---|---|
| Z-Image Turbo (bobot int8_convrot di rak) | Unlicense/domain publik diverifikasi dari LICENSE repo resep hulu; Civitai allowCommercialUse penuh | komersial aman per sumber riset [R-4 AF-R1-image.md baris lisensi] |
| RealESRGAN_x4plus | BSD-3-Clause (katalog openmodeldb, akses 2026-09-02) | [R-5 AF-R2-cutout-up.md baris U4] |
| BiRefNet (bobot birefnet.safetensors rak) | status berkas bobot TIDAK dicatat per-berkas di riset misi; repo ZhengPeng7 diakses sebagai sumber resep | perlu cek berkas sebelum distribusi eksternal; pemakaian internal slide aman-pakai |
| ComfyUI-RMBG (alternatif matting, TIDAK terpasang) | GPL-3.0 | gerbang G6 belum lolos; tidak dipasang [R-6 04_recipe_U3-U4.md] |
| ComfyUI_LayerStyle (kandidat teks, TIDAK terpasang) | MIT (api.github.com 2026-09-02) | keputusan whitelist Q3 = manusia; belum dibutuhkan [R-7 sheet-U9-composition.md U9-6] |
| Ideogram-4 / FLUX.1-dev/Kontext / SD3.5 | non-komersial / community license | TOLAK untuk deliverable komersial GSP [R-8 AF-R5-text-alt.md] |
| comfyui-videohelpersuite (satu-satunya custom node terpasang) | status berkas LICENSE belum diverifikasi per-berkas di riset misi | TIDAK TERUJI; tercatat agar tidak dikira sudah diaudit |

## 4. Item butuh keputusan manusia (penanda untuk kurasi berikutnya)

1. W3 blender-mcp: pasang atau tidak untuk loop review visual P2. Produksi TIDAK bergantung padanya; boleh ditolak tanpa konsekuensi Definition of Failure [R-2 sec.2 implikasi].
2. W1 trimesh: persetujuan lapis sudah diberikan controller (P6); pemasangan aktual + pin versi + hash wheel masih harus tercatat di kartu pemakai bila QA lintas-bahasa dipakai [R-3 P6; R-2 G-01].
3. G-10: skrip karangan misi GSP (resep a-e, driver smoke) berstatus "karangan-sendiri-belum-berlabel"; controller menetapkan bentuk label internal (MIT-0/MIT) sebelum objek turunan dipromosikan lebih jauh [R-2 G-10].
4. LayerStyle (MIT) dan bimdown-cli (MIT-0 skill-card; endpoint publish mengunggah anonim ke bim-claw.com, butuh izin eksplisit user): dorman, aktif hanya bila kebutuhan muncul [R-7; R-2 G-12].

## 5. Batas klaim

Semua status berlaku per tanggal akses 2026-09-02 (presisi) dan 2026-09-02/03 (rak ComfyUI); adopsi dan lisensi wajib ditarik ulang bila dipakai jauh dari tanggal itu (gap G-14). Klaim prosedural-terverifikasi per berkas, tanpa klaim fleet-wide (D-TA-10).

## Rujukan

- [R-1] docs/2026-09-02-precision-3d-factory/research/recipes/_LISENSI.tsv
- [R-2] docs/2026-09-02-precision-3d-factory/research/R-GATE-rekomendasi.md (sec.2 whitelist W0-W3, sec.3 gap list)
- [R-3] docs/2026-09-02-precision-3d-factory/contract.md sec.7 (P6 keputusan controller)
- [R-4] docs/2026-09-02-asset-factory/research/AF-R1-image.md
- [R-5] docs/2026-09-02-asset-factory/research/AF-R2-cutout-up.md
- [R-6] docs/2026-09-02-asset-factory/research/04_recipe_U3-U4.md
- [R-7] docs/2026-09-02-asset-factory/research/sheet-U9-composition.md
- [R-8] docs/2026-09-02-asset-factory/research/AF-R5-text-alt.md
