---
id: ft-l3-kelayakan-qlora-5070ti
type: fakta
title: "Vonis kelayakan FT lokal RTX 5070 Ti 16GB (Blackwell sm_120): LAYAK QLoRA sampai 14B, TIDAK LAYAK 27-32B/full-FT"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L3-local-ft.md
halaman: seksi 1-3, 7 tabel keputusan F1-F9
tanggal_akses: 2026-09-20
kelas_bukti: sintesis
sensitif: tidak
perkara: ft-eval-0920
tags: [fine-tuning, qlora, unsloth, rtx-5070-ti, blackwell, sm_120, lokal, ft-eval-0920]
links: [ft-l3-pitfall-bnb-sm120-windows]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Uji kesetiaan RAW lolos atas seluruh angka L3 (sha16 072e5480a79c1b55): hardware 16.303 MiB/sm_120/driver 591.86/RAM 127,1 GB/disk bebas 660 GB/CUDA Toolkit 13.3/torch fleet CPU-only; tabel VRAM resmi Unsloth 3B=3,5 s.d. 70B=41 GB; vonis nyaman sampai 8B, layak-disiplin 12-14B, 27-32B tidak layak; PyTorch 2.7.0 April 2025 cu128 + indeks wheel 2.10.0-2.11.0 win_amd64 cu126/cu128/cu130 cp311-cp314 dan 2.12.0-2.14.0 cu126/cu130/cu132; faktor [DERIVED] 0,55 berlabel dengan rumus dan kewajiban kalibrasi 100-step; inference pihak ketiga 66,6/45,5/40,4 t/s; serving Ollama/llama.cpp/vLLM-via-WSL2/TensorRT tidak dipilih; full FT >=3B tidak layak. Ukur ulang custodian 2026-09-20: nama GPU, 16303 MiB, compute 12.0, driver 591.86 identik; RAM total 127,1 GB identik; keenam versi PyPI identik (unsloth 2026.9.7, axolotl 0.19.0, trl 1.13.0, llamafactory 0.9.5, torchtune 0.6.1, vllm 0.29.0). Kelas_bukti sintesis jujur (ukur lokal + riset). REKOMENDASI: klaim state lingkungan bersifat volatile; ukur ulang custodian atas mesin yang sama memberi GPU/RAM/driver identik tetapi disk bebas 658 GB vs 660 GB saat lajur diukur (drift pemakaian normal, bukan salah tulis). Tandai klaim volatile dengan batas waktu 'terukur 2026-09-20' saat promosi agar tidak terbaca tahan-waktu."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: faktas/ft-l3-kelayakan-qlora-5070ti.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Vonis kelayakan FT lokal RTX 5070 Ti 16GB (Blackwell sm_120): LAYAK QLoRA sampai 14B, TIDAK LAYAK 27-32B/full-FT

Hasil ukur + riset lajur L3 misi FT-EVAL-0920 (akses URL 2026-09-20; ladder 8 kelas jalur: 7 dieksekusi penuh, 1 N/A beralasan; 14 URL primer 200 + 7 endpoint API):

1. Hardware terukur lokal: RTX 5070 Ti 16.303 MiB, compute 12.0 (sm_120), driver 591.86; RAM 127,1 GB; disk C: bebas 660 GB; WSL2 Ubuntu-24.04 + Docker tersedia; CUDA Toolkit 13.3; belum ada libs ML (torch fleet = CPU-only).
2. Dukungan sm_120: PyTorch 2.7.0 (April 2025) pertama mendukung Blackwell dengan wheel cu128 (https://pytorch.org/blog/pytorch-2-7/); status indeks wheel resmi https://download.pytorch.org/whl/torch/ per 2026-09-20: torch 2.10.0-2.11.0 menyediakan win_amd64 cu126/cu128/cu130 (cp311-cp314), torch 2.12.0-2.14.0 menyediakan cu126/cu130/cu132. Jalur stabil Windows aktif: torch >= 2.10 + cu130. Perintah: uv pip install torch --index-url https://download.pytorch.org/whl/cu130
3. Tabel VRAM resmi Unsloth QLoRA 4-bit ("absolute minimum", https://unsloth.ai/docs/get-started/fine-tuning-for-beginners/unsloth-requirements, akses 2026-09-20): 3B=3,5GB, 7B=5GB, 8B=6GB, 9B=6,5GB, 11B=7,5GB, 14B=8,5GB, 27B=22GB, 32B=26GB, 70B=41GB. Vonis: nyaman sampai 8B; layak-dengan-disiplin (seq<=4K, batch 1-2, gradient checkpointing) 12-14B; 27-32B TIDAK LAYAK (22-26GB > 16GB efektif).
4. Kasus khusus MoE: openai/gpt-oss-20b (Apache 2.0, diverifikasi dari README model card https://huggingface.co/openai/gpt-oss-20b/raw/main/README.md) - bobot native MXFP4 tidak bergantung bitsandbytes 4-bit; LAYAK-EKSPERIMENTAL. Qwen3-8B/14B Apache 2.0 terverifikasi dari front-matter README (https://huggingface.co/Qwen/Qwen3-14B/raw/main/README.md).
5. Framework: pemenang operasional Unsloth (klaim resmi 2x kecepatan latih, hemat VRAM 70%, konteks 12x; basis uji RTX 5090, blog Blackwell https://unsloth.ai/docs/blog/fine-tuning-llms-with-blackwell-rtx-50-series-and-unsloth); LLaMA-Factory cadangan resmi-Windows (butuh bnb build CUDA 12.8-12.9 khusus RTX 50); TRL cadangan ekosistem HF; Axolotl ditolak untuk single-GPU; torchtune ditolak (rilis beku 0.6.1 sejak 07-04-2025, 17 bulan; sinyal pemeliharaan lemah).
6. Throughput: benchmark publik tokens/sec TRAINING spesifik 5070 Ti TIDAK DITEMUKAN setelah 8 kelas jalur (vonis jenuh ber-angka). Data inference pihak ketiga di kartu persis ini (https://www.hardware-corner.net/gpu-llm-benchmarks/rtx-5070-ti/): gpt-oss-20B 66,6 t/s gen @128K; Qwen3-14B Q4_K 45,5 t/s; Qwen3-8B 40,4 t/s. Faktor komputasi [DERIVED] 5070Ti vs 5090 = 0,55 (aproksimasi kasar rasio core x clock; wajib diganti kalibrasi 100-step).
7. Serving: Ollama LAYAK native (dukungan eksplisit cc 5.0+ termasuk RTX 5070 Ti, driver >= 550; https://docs.ollama.com/gpu); llama.cpp LAYAK (prebuilt Windows+CUDA; resep build MSVC sm_120 issue #22696); vLLM LAYAK-VIA-WSL2 (dok resmi Linux-only, py3.10-3.13); TensorRT-LLM TIDAK DIPILIH (Linux-first). Integrasi LiteLLM: pola custom provider OpenAI-compatible terbukti di fleet.
8. Full fine-tune >= 3B TIDAK LAYAK di mesin ini: bobot BF16 8B sudah 16GB plus optimizer state AdamW fp32 ~2x bobot.

Versi PyPI terukur via API JSON hari ini: unsloth 2026.9.7, axolotl 0.19.0, trl 1.13.0, llamafactory 0.9.5, torchtune 0.6.1, vllm 0.29.0. sha16 berkas sumber: 072e5480a79c1b55.
