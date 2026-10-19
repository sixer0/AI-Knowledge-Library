# Verified Download Manifest — 2026-09-01

All sizes read from `https://huggingface.co/api/models/<repo>/tree/main?recursive=true` on 2026-09-01 (real bytes, not blog claims). Re-verify before download — repos gain variants. Target: RTX 5070 Ti 16 GB / RAM 64 GB / ComfyUI ≥ 0.34.

## Z-Image-Turbo — Apache-2.0 ✅ (Comfy-Org/z_image_turbo)
- `split_files/diffusion_models/z_image_turbo_bf16.safetensors` — 12.31 GB → models/diffusion_models/
- `split_files/text_encoders/qwen_3_4b_fp8_mixed.safetensors` — 5.63 GB (bf16 = 8.04 GB; fp4_mixed = 3.48 GB) → models/text_encoders/
- `split_files/vae/ae.safetensors` — 0.34 GB → models/vae/
- Optional ControlNet: `alibaba-pai/Z-Image-Turbo-Fun-Controlnet-Union` → models/model_patches/ (node `ZImageFunControlnet`)
- Official workflow: workflow_templates `image_z_image_turbo.json`; docs https://docs.comfy.org/tutorials/image/z-image/z-image-turbo

## Qwen-Image-2512 — Apache-2.0 ✅ (Comfy-Org/Qwen-Image_ComfyUI)
- `split_files/diffusion_models/qwen_image_2512_fp8_e4m3fn.safetensors` — 20.43 GB (recommended; bf16 = 40.86 GB)
- `split_files/text_encoders/qwen_2.5_vl_7b_fp8_scaled.safetensors` — 9.38 GB
- `split_files/vae/qwen_image_vae.safetensors` — 0.25 GB
- Optional 4-step accel: `lightx2v/Qwen-Image-Lightning/Qwen-Image-Lightning-4steps-V1.0.safetensors` → models/loras/
- Template `image_qwen_Image_2512.json`; aspect-ratio table on docs page (native res 1328² etc.)

## Qwen-Image-Layered — Apache-2.0 ✅ (Comfy-Org/Qwen-Image-Layered_ComfyUI)
- `split_files/diffusion_models/qwen_image_layered_fp8mixed.safetensors` — 20.53 GB (bf16 40.86 GB)
- `split_files/vae/qwen_image_layered_vae.safetensors` — 0.25 GB; TE shared with Qwen-Image above
- Why: outputs SEPARATE layers (bg/object/text) → assets for editable slides. Node `EmptyQwenImageLayeredLatentImage`.

## Wan2.2 TI2V-5B — Apache-2.0 ✅ (Comfy-Org/Wan_2.2_ComfyUI_Repackaged)
- `split_files/diffusion_models/wan2.2_ti2v_5B_fp16.safetensors` — 10.00 GB
- Needs wan2.2 VAE (small); text encoder umt5-xxl — **GSP disk already has umt5_xxl_fp16.pth (11 GB) from Wan2.1 — reuse**
- 14B variants exist at 14.3 GB fp8 each (high+low noise two-stage = ~29 GB) — tight on 16 GB, prefer 5B

## TRELLIS.2-4B — MIT ✅ (microsoft/TRELLIS.2-4B)
- ckpts: `ss_flow_img_dit_1_3B_64_bf16` 2.58 + `slat_flow_img2shape_dit_1_3B_512_bf16` 2.58 + `slat_flow_imgshape2tex_dit_1_3B_512_bf16` 2.58 + enc/dec pairs ~0.7–0.95 each ≈ 10 GB total
- Nodes present in core ≥0.34: `EmptyTrellis2LatentStructure`, `MeshToFile3D`, `Load3D`

## Krea-2 (June 2026, newest) — ⚠️ Krea Community License (verify before client work) (Comfy-Org/Krea-2)
- `diffusion_models/krea2_turbo_nvfp4.safetensors` — 7.67 GB (best for Blackwell 16 GB); fp8_scaled 13.14; int8_convrot 13.49; bf16 26.28
- `text_encoders/qwen3vl_4b_fp8_scaled.safetensors` — 5.24 GB; `vae/qwen_image_vae.safetensors` — 0.25 GB
- Style LoRAs incl. `krea2_turbo_lora_rank_64_bf16` 0.47 GB; nodes `Krea2ImageNode`, `Krea2StyleReferenceNode`

## FLUX.2 family — license trap
- `black-forest-labs/FLUX.2-klein-4B` — **Apache-2.0 ✅** (521k downloads)
- `black-forest-labs/FLUX.2-klein-9B` — **NON-COMMERCIAL ⚠️** (`flux-2-klein-9b.safetensors` 18.16 GB bf16 — needs quant for 16 GB anyway)
- Comfy-Org repacks: `Comfy-Org/vae-text-encorder-for-flux-klein-9b` (note upstream typo "encorder"), `.../flux-klein-4b`
- FLUX.2 dev = 32B, effectively out of reach (≥ 64 GB fp16); nodes `EmptyFlux2LatentImage`, `Flux2Scheduler` exist regardless

## Rejected (with reason)
- Lightricks/LTX-2 — license `other` (custom); fp4 19.99 GB borderline on 16 GB VRAM
- tencent/HunyuanImage-3.0 — license `other`; 80B-class, needs heavy offload
- Krea-2 for commercial deliverables — pending license-terms check

## Live-server capability probe (verified 2026-09-01, GSP machine)
`/object_info` (saved to file, filtered) confirmed present: EmptyFlux2LatentImage, Flux2Scheduler/ProImageNode, Krea2ImageNode, TextEncodeZImageOmni, ZImageFunControlnet, EmptyQwenImageLayeredLatentImage, TextEncodeQwenImageEdit(+Plus), QwenImageDiffsynthControlnet, EmptyTrellis2LatentStructure, MeshToFile3D, SeedVR2*, CreateVideo/SaveVideo + 136 video nodes, 58 3D nodes. Absent: `UnetLoaderGGUF` (GGUF quant routes need ComfyUI-GGUF custom node).
