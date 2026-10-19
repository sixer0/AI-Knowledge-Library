---
name: diffusion-model-sourcing
description: Use when picking local image/video/3D models for ComfyUI.
version: 1.0.0
tags: [comfyui, image-generation, model-selection, licensing, slides]
metadata:
  hermes:
    category: creative
    related_skills: [comfyui, powerpoint, excalidraw]
---

# Diffusion Model Sourcing & Slide Stack

Class of task: "find the best/latest model we can run" for local ComfyUI (or similar), and composing multi-capability stacks (photoreal + text + diagram + 3D + animation, e.g. slide generation). The failure mode this skill prevents is recommending from blog claims — every number must be verified live.

## Verification recipe (MANDATORY before any recommendation)

1. **Real file sizes** — HF tree API, not blog prose:
   `curl -s "https://huggingface.co/api/models/<org>/<repo>/tree/main?recursive=true"`
   Sum `.safetensors` > ~50 MB per needed variant (fp8/nvfp4/int8 differ hugely).
2. **License** — `curl -s "https://huggingface.co/api/models/<org>/<repo>"` → `cardData.license`.
   `apache-2.0`/`mit` = commercial-safe. `other` = read the card; traps seen: FLUX.2-klein **9B non-commercial but 4B Apache-2.0**; Krea-2 custom Community License; LTX-2 / HunyuanImage-3.0 = `other`. For a company (GSP) that bills clients, non-commercial = reject.
3. **Node support on the LIVE server** — `GET /object_info` is megabytes: save to a file first (`curl -o object_info.json`), then filter class_types in Python (`EmptyFlux2LatentImage`, `TextEncodeZImageOmni`, `Krea2ImageNode`, `EmptyQwenImageLayeredLatentImage`, `EmptyTrellis2LatentStructure`, `SeedVR2*`...). ComfyUI ≥ 0.34 ships core nodes natively for Z-Image / Qwen-Image(-2512/Layered) / FLUX.2 / Krea-2 / TRELLIS / Wan / LTXV.
4. **Search fallback:** niche technical queries via Hermes web_search/SearXNG are often geo-poisoned junk → use `ddgs` (`uv run --python 3.11 --with ddgs python <script>`), then confirm against official docs.comfy.org tutorials pages (they list exact split_files download paths).

## Slide-generation stack pattern (verified 2026-09-01)

Multi-need requests ("image + diagram + text + 2D + 3D + animation + realistic") = **layers, never one model**:

| Layer | Model | License | Size (16 GB-variant) |
|-------|-------|---------|----------------------|
| Photoreal fast daily | Z-Image-Turbo (6B, 8-step) | Apache-2.0 | ≈ 18 GB (bf16 12.31 + TE fp8 5.63 + VAE .34) |
| Premium realism / text-in-image | Qwen-Image-2512 fp8_e4m3fn | Apache-2.0 | ≈ 30 GB |
| Layered assets (bg/object/text separate → editable) | Qwen-Image-Layered fp8mixed | Apache-2.0 | ≈ 21 GB |
| Animation | Wan2.2 TI2V-5B fp16 | Apache-2.0 | 10 GB (umt5-xxl TE often already on disk — reuse!) |
| 3D → GLB | TRELLIS.2-4B | MIT | ≈ 10 GB |
| Upscale | SeedVR2 / ESRGAN 4x | — | small |

**Hard rule: precise diagrams and body text are NOT diffusion jobs.** Vector path only: HTML/SVG/Mermaid/Excalidraw → PNG (`powerpoint`, `excalidraw`, `gsp-canvas-design`, `sketch` skills). Diffusion supplies visuals/3D/animation; deck composition merges them. Pipeline: prompt → visual → (animate|3D) → vector diagram/text → compose PPTX/HTML → upscale → export.

## Pitfalls

- **Blog VRAM/size claims are wrong often** (e.g. "Flux.2 Dev fits 24GB quantized" vs HF tree showing fp8 at 32 GB+). Always step 1.
- **Same model family, different licenses per size** — check the exact repo you will download (klein 9B vs 4B).
- **object_info dump blows context** if piped raw — file + Python filter.
- **Text-encoder reuse**: Wan2.1/2.2 share umt5-xxl; Qwen-family share VAE/TEs. Inventory `models/{text_encoders,diffusion_models,vae}` before downloading — often half the stack exists.
- **Blackwell GPUs (RTX 50-series)**: prefer nvfp4/int8-convrot variants for tight VRAM; torch cu130 handles them.
- Do NOT present rejected models as options without the license caveat — a commercial user can be legally burned.

## GSP environment notes (verify before trusting — re-check with recipe above)

ComfyUI at `C:/Users/TRIAL/Documents/comfy/ComfyUI` v0.34, own `.venv` (no comfy-cli): start `./.venv/Scripts/python.exe main.py --port 8188 --listen 127.0.0.1`; log `user/comfyui_8188.log` doubles as activity audit. RTX 5070 Ti 16 GB, RAM 64 GB (CPU offload fine for 20–30 GB models), disk ~460 GB free. On-disk: SDXL base, Wan2.1 T2V 1.3B, umt5_xxl fp16 TE. Not in autostart. Contract doc of the founding session: `workspace/gsp-hermes/workspace/docs/2026-09-01-cek-comfyui-image-generation.md`.

## See also

- `comfyui` (bundled — curator-managed; report gaps to user for `hermes curator adopt`, don't patch directly from background runs) — execution scripts, setup paths, workflow `_comment` pitfall.
