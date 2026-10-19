---
id: ft-l2-harga-ft-hosted-2026
type: fakta
title: "Tabel harga fine-tuning hosted terverifikasi 2026: Vertex, Fireworks, Together, Bedrock, Azure, Modal, RunPod"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L2-hosted-platforms.md
halaman: seksi 1 tabel komparasi + seksi 2 C-14..C-37
tanggal_akses: 2026-09-20
kelas_bukti: primer
sensitif: tidak
perkara: ft-eval-0920
tags: [fine-tuning, harga, vertex, fireworks, together, bedrock, azure, modal, runpod, litellm, ft-eval-0920]
links: [ft-l2-openai-ft-winding-down, ft-l2-negatif-ft-platform-terverifikasi]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Uji kesetiaan RAW atas SELURUH angka kunci terhadap lajur/L2-hosted-platforms.md (sha16 289ea28bb003c49c): Vertex $0,01/$0,003/$0,025/$0,005/$0,0015 per 1k + Gemma 3 27B $6,83/M + serving 1,5x + batas dataset 100-500 contoh/1GB/10M; Fireworks LoRA $0,50/$3/$6/$10 + Full 2x + DPO 2x + H100/H200 $8 + B200 $13 + B300 $15 + minimum 3 contoh; Together $0,34/$0,84/$4 s.d. GLM-5.2 $40/$100/$60 + Parquet maks 100GB; Bedrock Nova/Claude 3 Haiku us-west-2 + mode ZDR/aws_review/provider_data_share; Azure daftar model + angka statis tidak terverifikasi; Modal $3,95/$4,54/$2,50/$6,25/$7,10; RunPod $2,89/$3,49/$4,59/$7,89; LiteLLM endpoint FT enterprise + jalur model_list. Register 34 SOURCE-DERIVED/1 PROV/2 ASSUMPTION cocok L2 seksi 0; klaim verifier seed 51500 14/14 HTTP 200 SALAH-TARGET 0 cocok V-VERDICT CHECK 2; ladder 18 rung dan raw/L2/ladder.log terverifikasi 136 baris. Kelas_bukti primer jujur; C-18/C-26 berlabel ASSUMPTION dengan rencana penggantian. REKOMENDASI: tidak ada perbaikan wajib; angka adalah daftar harga ber-tanggal sehingga wajib terbit dengan batas-waktu 2026-09-20, dan dua gap (Azure/Bedrock per-token) harus tetap kosong, bukan diisi."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: faktas/ft-l2-harga-ft-hosted-2026.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Tabel harga fine-tuning hosted terverifikasi 2026: Vertex, Fireworks, Together, Bedrock, Azure, Modal, RunPod

Angka daftar harga vendor, semua diakses 2026-09-20 WIB lewat URL primer milik vendor (gerbang entity-match SPK-002; verifier CHECK 2 membuka ulang sampel acak seed 51500: 14/14 HTTP 200, SALAH-TARGET 0). Register lengkap C-01..C-37 (34 SOURCE-DERIVED, 1 PROV, 2 ASSUMPTION).

1. Google Vertex / Gemini Enterprise Agent Platform [C-14..C-17]: AKTIF GA; SFT (teks/dokumen/gambar/audio/video/fn-call), Preference (DPO), RL. Harga per 1k token latih: Gemini 3.5 Flash $0,01; 3.1 Flash-Lite $0,003; 2.5 Pro $0,025; 2.5 Flash $0,005; 2.5 Flash-Lite $0,0015; Gemma 3 27B $6,83 per 1M token. Serving model hasil tuning ditagih 1,5x tarif dasar. Batas dataset: JSONL di Cloud Storage, disarankan 100-500 contoh, maks 1GB/file, maks 10M contoh. Sumber: https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/tuning/supervised-tuning (HTTP 200) + https://cloud.google.com/gemini-enterprise-agent-platform/generative-ai/pricing (HTTP 200, 3.057.539 B).
2. Fireworks AI [C-27..C-30]: AKTIF; SFT/DPO/RFT; LoRA & full-param; minimum 3 contoh; format kompatibel chat OpenAI. Harga per 1M token latih: LoRA SFT <=16B $0,50; 16-80B $3; 80-300B $6; >300B $10; Full SFT 2x LoRA; DPO 2x SFT. GPU on-demand H100/H200 $8/jam, B200 $13/jam, B300 $15/jam. ZDR default inferensi open model; training retensi 30 hari; BYOB + CMEK tersedia. Sumber: https://docs.fireworks.ai/fine-tuning/fine-tuning-models.md + https://fireworks.ai/pricing (HTTP 200).
3. Together AI [C-23..C-25]: AKTIF; LoRA (default) atau Full FT; SFT + DPO; reasoning FT; BYOM dari HF Hub; Parquet pre-tokenized maks 100GB. Harga (LoRA SFT / Full SFT / minimum charge per job): Qwen3.5 0.8B $0,34/$0,84/$4; 27B $1,05/$2,62/$4; Llama 3.3 70B $2,03/$5,08/$4; Llama 4 Maverick $5,60/$14/$16; GLM-5.2 $40/$100/$60. Training-for-other-models OPT-IN default mati; ZDR toggle admin. Sumber: https://docs.together.ai/docs/fine-tuning-overview.md + https://www.together.ai/pricing (HTTP 200).
4. Amazon Bedrock [C-32..C-33]: AKTIF; SFT, RFT (reward via Lambda), Distillation otomatis teacher->student. Model: Nova 2 Lite/Nova Lite/Micro/Pro/Canvas/Titan, Claude 3 Haiku (region us-west-2 saja), Llama 3.1/3.2/3.3. Tagihan latih = token korpus x epoch; inferensi custom model = harga model dasar; angka per-token dirender dinamis (register ketidakterverifikasian). Mode retensi eksplisit: ZDR; aws_review (human review oleh AWS); provider_data_share legacy. Sumber: https://docs.aws.amazon.com/bedrock/latest/userguide/custom-model-fine-tuning.md + data-retention.html (HTTP 200).
5. Azure AI Foundry [C-31]: AKTIF; LoRA untuk SFT/DPO/RFT; model gpt-4o-mini/4o/4.1, o4-mini (RFT), gpt-5 2025-08-07 (RFT GA dengan catatan), Ministral-3B, Qwen-32B, Llama-3.3-70B, gpt-oss-20b. Angka USD per-token TIDAK terverifikasi dari HTML publik (komponen dinamis) - jalur resmi = Azure Pricing Calculator/agreement. Sumber: https://learn.microsoft.com/en-us/azure/ai-foundry/openai/how-to/fine-tuning (HTTP 200, 242.395 B).
6. Modal (DIY) [C-34]: per detik GPU: H100 SXM5 ~$3,95/jam, H200 ~$4,54/jam, A100 80GB ~$2,50/jam, B200 ~$6,25/jam, B300 ~$7,10/jam. Contoh FT resmi: Unsloth, GRPO verl. Sumber: https://modal.com/pricing (HTTP 200).
7. RunPod (DIY) [C-35]: tutorial resmi FT dengan Axolotl; tabel utama H100 PCIe $2,89/jam, H100 SXM $3,49, H200 $4,59, B300 $7,89; tier Community/Secure perlu konfirmasi sebelum dipakai anggaran. Sumber: https://docs.runpod.io/fine-tune + https://www.runpod.io/pricing (HTTP 200).
8. Integrasi LiteLLM [C-36..C-37]: endpoint /fine_tuning + /files = fitur ENTERPRISE LiteLLM; jalur non-enterprise = daftarkan model hasil FT sebagai entri model_list biasa (alias -> api_base endpoint dedikasi vendor); rollback satu baris config. Sumber: https://docs.litellm.ai/docs/fine_tuning (HTTP 200, 69.426 B).

Register ketidakterverifikasian (kosong lebih baik daripada salah): harga statis Azure per 1M token; harga per-token latih Bedrock konkret; SLA waktu latih semua vendor managed. Asumsi C-18 (estimasi biaya korpus 50-500MB = $30-$3.750 dengan sensitivitas rasio char/token) dan C-26 (waktu latih LoRA menit-sampai-jam) berlabel ASSUMPTION, wajib diganti pengukuran.

Provenans berjenjang (AM-G4): ladder 18 rung ber-timestamp di berkas sumber seksi 5; log mentah docs/2026-09-20-ft-eval-0920/raw/L2/ladder.log (136 entri). sha16 berkas sumber: 289ea28bb003c49c.
