---
name: gsp-comfyui-slide-stack
description: "Use when building decks/slides/clips via ComfyUI models."
version: 1.1.0
author: [GSP Swarm]
license: MIT
tags: [gsp, comfyui, slide, deck, image-generation, video, 3d, orchestration]
related_skills: [comfyui, powerpoint, gsp-canvas-design, excalidraw]
metadata:
  hermes:
    category: gsp
    tags: [gsp, comfyui, slide, deck, image-generation, video, 3d, orchestration]
---

# GSP ComfyUI Slide-Stack -> produksi deck & klip satu pintu

## When to Use
- User meminta deck/slide/brosur dengan visual hasil generate, klip produk, aset 3D,
  atau kombinasi image realistis + diagram + teks + 2D + 3D + animasi.
- Cukup skill `comfyui` bila hanya image generation polos tanpa lapisan slide.

Pipeline **asset-first** berlapis di ComfyUI lokal (`C:\Users\TRIAL\Documents\comfy\ComfyUI`,
v0.34+, server `http://127.0.0.1:8188`). Prinsip: SATU workflow API-JSON per lapisan,
eksekusi berurutan lewat `run_workflow.py`; hasil tahap N jadi input tahap N+1;
verifikasi artefak di SETIAP batas sebelum lanjut. Bukan satu graph raksasa (VRAM 16 GB).

Kebutuhan tercakup: image realistis, diagram, teks, 2D, 3D, animasi -> kombinasi slide/deck/klip.

## Kapan pakai
- Permintaan deck/slide/brosur dengan visual generated, klip animasi produk, aset 3D,
  atau kombinasi: image realistis + diagram + teks + 2D + 3D + animasi.
- Untuk image generation polos saja → cukup skill `comfyui`. Skill ini menambah
  LAYER orkestrasi slide: gerbang aset, konsistensi kanonik, komposisi deck, rantai bukti.

## Mesin & bobot (diverifikasi 2026-09-01)
GPU RTX 5070 Ti 16 GB, RAM 64 GB. Bobot di `models/`:

| Lapisan | File | Folder | Lisensi |
|---|---|---|---|
| Z-Image-Turbo (hero harian, 8 langkah) | `z_image_turbo_bf16.safetensors` + TE `qwen_3_4b_fp8_mixed.safetensors` + VAE `ae.safetensors` | diffusion_models / text_encoders / vae | Apache-2.0 |
| Qwen-Image-2512 (premium + render teks) | `qwen_image_2512_fp8_e4m3fn.safetensors` + TE `qwen_2.5_vl_7b_fp8_scaled.safetensors` + VAE `qwen_image_vae.safetensors` | sama | Apache-2.0 |
| Wan2.2 TI2V-5B (animasi) | `wan2.2_ti2v_5B_fp16.safetensors` + TE `umt5_xxl_fp8_e4m3fn_scaled.safetensors` + VAE `wan2.2_vae.safetensors` | sama | Apache-2.0 |
| TRELLIS.2 (3D→GLB) | `trellis_2_int8_convrot.safetensors` + `trellis_2_shape_vae_bf16` + `trellis_2_texture_vae_bf16` + `dino_v3_vit_l.safetensors` | diffusion_models / vae / clip_vision | MIT; conditioning DINOv3 = lisensi Meta -> **Q7 DISSETUJUI user 2026-09-01: hasil 3D boleh untuk deliverable komersial**. Repack Comfy-Org bisa diunduh anonim (yang gated hanya repo asli `facebook/*`) |
| BiRefNet (cutout) | `birefnet.safetensors` | background_removal | MIT |
| Upscale | `RealESRGAN_x4plus.safetensors` | upscale_models | BSD |

Repo sumber (nama path TERBUKTI, jangan tebak): `Comfy-Org/z_image_turbo`,
`Comfy-Org/Qwen-Image_ComfyUI` (BUKAN `Qwen-Image-2512` -> tidak ada),
`Comfy-Org/Wan_2.2_ComfyUI_Repackaged` (prefiks `split_files/`),
`Comfy-Org/TRELLIS.2` (TANPA prefiks split_files), `ZhengPeng7/BiRefNet` (`model.safetensors`
→ simpan sebagai `birefnet.safetensors`).

## Alur baku (WAJIB berurutan)

### Gerbang A -> Audit Aset (jangan lewati!)
Kualitas output dibatasi kelengkapan input. Sebelum generate apa pun, daftar terhadap brief:
foto produk? logo? maskot? latar? warna/tipografi brand? angka untuk diagram?
→ work-list aset MISSING = pekerjaan L0. Tidak ada produksi sebelum list beres & diverifikasi.

### L0 -> Asset Factory
1. **Kanonik**: satu gambar kanonik per subjek (Z-Image t2i, seed dicatat). Semua varian
   berasal dari sini. Simpan di `ComfyUI/input/canonical.png` (server-side name = path rantai).
2. **Cutout**: [`workflows/birefnet_cutout.json`](workflows/birefnet_cutout.json) → PNG RGBA transparan.
   Butuh upscale aset transparan: JANGAN rantai dua berkas (simpan-muat file membuang
   alpha, lihat pitfall 14). Pakai [`workflows/birefnet_upscale_chain.json`](workflows/birefnet_upscale_chain.json): U3->U4 satu
   graph, link IMAGE internal, alpha di-rejoin pasca-upscale. Bukti GPU: keluaran
   4096x4096 RGBA, alpha tengah 254, keempat sudut 0, lulus hard-gate HG-ALPHA-4x 3/3 run.
3. **Varian shot**: [`workflows/z_image_img2img.json`](workflows/z_image_img2img.json) -> `seed` TETAP (lock), `denoise` default 0.3 (band aman 0.2-0.4; 0.4 = batas atas yang mengubah komposisi) [G-15],
   prompt = subjek sama + instruksi view ("rotated 30 degrees..."). Ini kunci konsistensi.
4. Flat 2D: prompt Z-Image "flat vector illustration, solid colors, thick outlines, no gradients".
5. Banner teks: Qwen-2512, teks ≤4–6 kata dalam tanda kutip, "clean bold sans-serif".

### Deck/brosur
hero (L0) → layout grid 12-kolom + TEKS RIIL (python-pptx) → combine.
Diagram angka & tipografi kaku = **vektor non-difusi** (matplotlib/SVG/HTML→PNG via
msedge headless) -> deterministik, tajam, tak pernah typo.
[`scripts/build_deck.py`](scripts/build_deck.py) (PPTX) / [`scripts/build_deck_html.py`](scripts/build_deck_html.py) (HTML ≥3 section).

### Klip/video
keyframe dari kanonik (L0.3) → [`workflows/wan22_ti2v_5b_i2v.json`](workflows/wan22_ti2v_5b_i2v.json) per keyframe
(1 klip = 1 shot, 49 frame @24fps ≈2 dtk, 1280×704, SATU gerakan kamera per klip)
→ concat ffmpeg. Negative bawaan resmi Wan (bahasa Mandarin) dipertahankan apa adanya.

### 3D
[`workflows/trellis2_img_to_3d.json`](workflows/trellis2_img_to_3d.json): cutout RGBA → structure→shape→upsample→texture→GLB.
**Gerbang Q7**: jangan pakai GLB untuk deliverable klien sebelum user menyetujui DINOv3.

**Status 02-09 (pivot A12)**: jalur 3D generatif dialihkan ke misi
`docs/2026-09-02-precision-3d-factory/` (Blender parametrik + specialist). Resep final TRELLIS
res1024 = 7/30 kelas konsep; reproduksi 02-09 menghasilkan median 6 dengan nol run di atas
baseline, jadi tidak ada klaim mutu produksi dari jalur ini sebelum pilot misi itu selesai.

### Komposisi majemuk (multi-object, layering, teks di atas scene)
Steering user 02-09 mengarahkan produksi ke komposisi majemuk, jadi status tiap jalur dicatat
terpisah antara yang sudah terbukti dan yang masih lubang. Jalur yang matang hari ini: generate
per objek lalu komposit (determinisme seed-lock terbukti piksel-identik intra-lapisan), layering
lewat `ImageCompositeMasked` dengan foreground hasil `RemoveBackground -> InvertMask ->
JoinImageWithAlpha`, dan teks paling akhir via node inti `TextOverlay` (posisi atas/bawah, font
sistem tanpa berkas custom). Urutan WAJIB: komposit, harmonisasi, baru teks; bila dibalik, teks
ikut terharmonisasi dan ejaannya rusak, dan teks kecil yang ikut ter-upscale 4x melembek (kasus
`teks_fine` turun dari 5 ke 4 di lapisan U4). Multi-object dalam SATU prompt dan conditioning
per-wilayah tidak tersedia untuk Z-Image jalur lumina2 tanpa custom node, sehingga gerbang
D-TA-11 menutupnya dan gap G-NG1 tetap terbuka. Catatan jujur: `ImageCompositeMasked` dan
`InvertMask` belum pernah dieksekusi di GPU pada graph gabungan, jadi setiap pemakaian baru wajib
membawa hard-gate polaritas sendiri (alpha tengah >=250 DAN keempat sudut 0), bukan warisan bukti
lapisan U3. Font merek di luar font sistem butuh gerbang whitelist Q3 atau render vektor di luar
ComfyUI.

## Perintah inti (Windows -> path SELALU C:/... forward-slash)
```bash
CC="/c/Users/TRIAL/Documents/comfy/ComfyUI"; VENV="$CC/.venv/Scripts/python.exe"
SK="/c/Users/TRIAL/AppData/Local/hermes/skills/creative/comfyui"
# server: (jika mati) cd "$CC" && ./.venv/Scripts/python.exe main.py --port 8188 --listen 127.0.0.1 &
# bersih VRAM antar-lapisan:
curl -s -X POST http://127.0.0.1:8188/free -H 'Content-Type: application/json' -d '{"unload_models": true,"free_memory": true}'
cd "$SK" && "$VENV" scripts/run_workflow.py \
  --workflow "C:/.../workflows/z_image_turbo_t2i.json" \
  --args '{"prompt":"...","seed":42,"steps":8,"width":1024,"height":1024,"cfg":1.0}' \
  --output-dir "C:/.../smoke" --timeout 300
# img2img rantai: tambah --input-image "image=C:/.../file.png" (injeksi ke field bernama 'image')
```
Workflow siap-pakai tersimpan di [`workflows/`](workflows/) skill ini (API-format, `_meta.title` sah,
tanpa key non-node di level atas).

## Parameter terbukti (dari template resmi Comfy-Org)
- Z-Image: shift 3.0 (`ModelSamplingAuraFlow`), 8 langkah, cfg 1.0, `res_multistep`/`simple`,
  negative = `ConditioningZeroOut`, CLIPLoader **type=lumina2**, native 1024.
- Qwen-2512: shift 3.1, 50 langkah (turbo LoRA: 4–8), cfg 4.0, euler/simple,
  CLIPLoader **type=qwen_image**, native 1328.
- Wan2.2 TI2V: CLIPLoader **type=wan**, 20 langkah cfg 5 `uni_pc`/simple, shift 8
  (`ModelSamplingSD3`), `Wan22ImageToVideoLatent` length 49, CreateVideo fps 24, SaveVideo.
- Z-Image img2img: `denoise` graph kini default 0.3 (resep U2-1 [G-15]); smoke AF-S4 PASS
  median 27 terhadap ambang 24, seed-lock 3 run piksel-identik. Nilai 0.4 lama = batas atas band.
- Teks dalam gambar Z-Image-Turbo int8: teks pendek UPPERCASE lulus ejaan 16/16 karakter pada
  zoom 100% (keputusan manusia vision, misi asset-factory 02-09; median juri 30/30). Belum
  diuji: teks panjang, ukuran kecil, gaya dekoratif. Gerbang zoom 100% + fallback vektor berlaku.

## Pitfall (semua dipukul nyata di misi 2026-09-01)
0. **POLARITAS MASK BiRefNet TERBALIK (akar semua 3D jelek!)** -> `RemoveBackground`
   mengembalikan MASK = **BACKGROUND** (bukan objek). Kalau alpha ini dipakai apa adanya
   di `JoinImageWithAlpha`, hasil RGBA = objek TRANSPARAN, latar OPAK; image-to-3D lalu
   membangun bentuk dari SISA LATAR (blob amorf). WAJIB: `RemoveBackground -> InvertMask ->
   JoinImageWithAlpha`. Cek cepat polaritas: alpha tengah gambar harus 255, sudut 0.
1. **`RemoveBackground` keluaran MASK**, bukan IMAGE -> wajib `JoinImageWithAlpha`
   (image asli + alpha) sebelum `SaveImage`; kalau langsung → HTTP 400 return_type_mismatch.
2. **`ImageScaleToTotalPixels` butuh `resolution_steps`** (required, sering terlupa) -> tanpa ini 400.
3. Workflow API-format: top-level key HARUS node-id saja; catatan di `_meta.title`.
   `_comment` top-level → HTTP 500 di ComfyUI ≥0.34.
4. `run_workflow.py` TIDAK paham path git-bash `/c/...` -> selalu `C:/...`.
5. Nama model exact-case dan file harus ADA di folder yang benar (`folder_paths.py`):
   BiRefNet → `models/background_removal/`, bukan checkpoints.
6. Template resmi (`workflow_templates/templates/*.json`) berformat EDITOR dengan
   **subgraph** (`definitions.subgraphs[].nodes`) -> widget ada di dalam subgraph, bukan top.
   Ekstrak parameter dari sana; jangan pakai template mentah sebagai API-format.
7. Unduhan HF anonim ~1–10 MB/s dan SERING MACET senyap (koneksi hidup, 0 byte).
   Deteksi: `find _stage -name '*.incomplete'` dua kali, bandingkan ukuran.
   Pemulihan: kill → restart `hf_hub_download(..., local_dir=...)` (resume dari `.incomplete`).
   `curl -o /c/...` gagal diam (exit 23) -> path native. File terpotong → ComfyUI error
   "Tensor ... extends past the end of the file" = safetensors korup, unduh ulang utuh.
8. Submit sinkron `POST /prompt` memunculkan error validasi lengkap (node_errors) ->
   pakai itu untuk debug sebelum curiga runner.
9. VRAM 16 GB: JANGAN graph multi-model raksasa; submit per-lapisan + `POST /free`
   antar tahap. Qwen-2512 fp8 offload ke RAM 64 GB aman (lebih lambat).
   **Tapi `/free` TIDAK membebaskan bobot yang di-pin `--highvram --cache-lru`** →
   antar-SESI (beda model) wajib RESTART server. OOM dengan `reserved >> allocated`
   (mis. reserved 14,3 GB, aktif 8,4 GB) = FRAGMENTASI, obat: start server dengan
   `PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True` (terbukti lolos di sesi TRELLIS).
   Bobot 3D wajib varian muat-VRAM: `z_image_turbo_int8_convrot` (6,2 GB), bukan bf16
   (12,3 GB); tekstur bake 2048 mepet, 1024 aman.
10. Klip multi-adegan jangan diharapkan dari 1 submit; rakit di post (ffmpeg concat).
11. Teks dalam gambar: verifikasi zoom 100%; typo → ganti seed maks 3x → fallback layer
    teks vektor. Angka tabel/grafik TIDAK PERNAH lewat difusi.
12. Server ComfyUI terikat sesi yang menyalakannya (bukan autostart) -> cek
    `curl -s http://127.0.0.1:8188/system_stats` sebelum bekerja; nyalakan on-demand.
13. **Cache LRU menetralkan run identik.** Server dengan `--cache-lru` mengembalikan hasil dari
    cache bila graph + parameter identik antar-run beruntun (`execution_cached` terisi, durasi
    ~0,06 dtk, mutu bukan hasil hitung ulang). Angka final WAJIB dari sesi bersih dan SETIAP run
    memakai graph unik (minimal `SaveImage.filename_prefix` beda per run) lalu buktikan
    `execution_cached` kosong (lesson AF-S1; mitigasi terbukti nol-cache di AF-S3/S4/S2b/S5).
14. **Alpha hilang di round-trip file saat upscale.** `UpscaleWithModel` (RealESRGAN) hanya
    RGB; simpan RGBA ke file lalu muat kembali = alpha terbuang, wilayah transparan menampakkan
    foto asli (kriteria `warna` juri jatuh ke median 2 -> FAIL sah AF-S2). Obat: satu graph,
    link IMAGE internal dari cutout ke upscale, alpha dinaikkan `MaskToImage ->
    ImageScaleBy(nearest-exact, 4.0) -> ImageToMask` lalu `JoinImageWithAlpha` pasca-upscale
    (pola `birefnet_upscale_chain.json`).
15. **GPU serial + disiplin repro.** Maksimum 1 kartu GPU aktif dan 1 model per sesi; antar sesi
    RESTART server (pola `scripts/chain2.sh`: kill -> start) karena `/free` tidak melepas bobot
    yang di-pin `--highvram --cache-lru`. OOM = restart server, bukan `/free`. Repro sebuah run
    WAJIB menyalin parameter mentah dari ledger/lembar resep, bukan dari ingatan atau ringkasan.

## Gerbang QA & bukti rantai
- Tiap tahap: artefak diunduh → dicek (dimensi/byte/alpha/teks) → catat `ledger.json`
  (id, workflow, params+seed, exit, oom, input_hash, output_hash, notes).
- Bukti rantai antar-lapisan = `sha256(output N) == sha256(input N+1)` ditulis di
  `SM14_chain_proof.md` (pola fan-out: satu kanonik → banyak konsumen, hash sama).
- Skrip audit: [`scripts/verify_smoke.py`](scripts/verify_smoke.py) (stdlib-only, 18 CHECK + `VERDICT:`;
  teks-dalam-gambar = NEEDS_REVIEW manual, JANGAN palsukan OCR).

## Referensi kontrak misi
`docs/2026-09-01-comfyui-slide-stack/` -> ARCHITECTURE.md (rev B/C),
identification/01_translated.md + 02_structured.md (RT+TA, 14 unit SM),
contract.md (amandemen + decision log Q7), smoke/ (artefak + ledger), verification/.

Misi asset-factory 02-09: `docs/2026-09-02-asset-factory/` -> contract.md (A4-A12, D-TA-1..14),
rubrik terkunci `verification/rubric_thresholds.md` (sha256 tercantum di `threshold-lock.txt`,
noise band 3, gerbang improvement D-TA-8), ledger GPU kanonis
`workspace/comfyui-check/assetfactory/ledger.json` (satu penulis per entri, jangan ditulis
ulang), serta delta dan patch fase I di `improve/`.
