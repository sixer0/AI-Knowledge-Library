---
id: ft-l4-taksonomi-8-jalur-improvement
type: pelajaran
title: "Taksonomi 8 jalur peningkatan kapabilitas agen AI (T-a..T-h): apa yang diubah tiap jalur dan biayanya"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L4-methodology.md
halaman: seksi 1 tabel taksonomi
tanggal_akses: 2026-09-20
kelas_bukti: sintesis
sensitif: tidak
perkara: ft-eval-0920
tags: [taksonomi, fine-tuning, rag, sft, dpo, rl, tool-use, metodologi, ft-eval-0920]
links: [ft-l4-kapan-ft-bukan-jawaban, ft-l4-honest-eval-harness-gsp]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Delapan jalur T-a..T-h cocok tabel L4 seksi 1 butir demi butir, termasuk angka: QLoRA latih 65B di satu GPU 48GB (C-06); IT ~100K pasangan vs continued PT ~20B token (C-07); ToolBench 16.464 API 49 kategori (C-13); xLAM pernah peringkat 1 Berkeley Function-Calling Leaderboard (C-14); Reflexion tanpa update bobot (C-11); Voyager bypasses the need for model parameter fine-tuning (C-12). Klaim register 42 baris terukur ulang dengan grep deterministik: tepat 42 baris register C-nn di L4 seksi 8. Peta GSP (pengetahuan ke T-a/T-b, perilaku ke T-d/T-f/T-h) adalah pembacaan langsung paragraf penutup tabel sumber. Kelas_bukti sintesis jujur. REKOMENDASI: tidak ada; bawa serta rujukan register [C-nn] saat promosi agar pembaca wiki dapat membuka sumber per jalur."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: pelajarans/ft-l4-taksonomi-8-jalur-improvement.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Taksonomi 8 jalur peningkatan kapabilitas agen AI (T-a..T-h): apa yang diubah tiap jalur dan biayanya

Sumbu pembeda: APA yang diubah sebuah jalur (pengetahuan vs bentuk/perilaku vs kemampuan pakai-alat vs memori episodik) dan SEBERAPA MAHAL mengubahnya. Ringkasan per jalur dengan rujukan klaim primer [C-nn] lajur L4 (semua URL terverifikasi entity-match oleh verifier CHECK 2; akses 2026-09-20):

- T-a Memory/skill engineering (prompt, AGENTS.md, skill library, refleksi): konteks & prosedur, bobot tak sentuh. Bukti: Reflexion memperbaiki agen lewat umpan balik verbal TANPA update bobot [C-11, arXiv 2303.11366]; Voyager menyimpan skill library kode, menyebut jalur ini "bypasses the need for model parameter fine-tuning" serta "alleviates catastrophic forgetting" [C-12, arXiv 2305.16291]. Biaya ~0.
- T-b RAG/pencarian konteks: sumber jawaban saat inferensi. Bukti: Ovadia dkk. RAG konsisten mengalahkan unsupervised FT untuk pengetahuan lama maupun baru [C-03, arXiv 2312.05934]; Zhang dkk. SIGIR-AP: untuk entitas paling jarang, RAG melampaui FT "by a large margin" [C-04, arXiv 2403.01432].
- T-c Long-context langsung: window lebih besar. Bukti: Hsieh dkk. long-context mengalahkan RAG rata-rata bila sumber daya cukup, tapi RAG jauh lebih murah; hibrida Self-Route menekan biaya [C-05, arXiv 2407.16833].
- T-d SFT (instruction tuning) penuh/LoRA: bentuk/kelakuan keluaran, BUKAN gudang fakta. Bukti: Gekhman dkk. contoh pengetahuan baru dipelajari jauh lebih lambat dan menaikkan halusinasi secara linear [C-01, arXiv 2405.05904]; QLoRA latih 65B di satu GPU 48GB [C-06, arXiv 2305.14314].
- T-e Continued pretraining: pengetahuan/statistik dasar; domain jauh + korpus miliaran token; paling mahal. Bukti: Biderman dkk. regimes IT ~100K pasangan vs continued PT ~20B token [C-07, arXiv 2405.09673].
- T-f DPO/preference tuning: preferensi perilaku (chosen/rejected). Bukti: DPO alternatif RLHF tanpa reward model [C-07b, arXiv 2305.18290]; Tulu 3 resep terbuka SFT+DPO+RLVR [C-08, arXiv 2411.15124].
- T-g RL/RFT outcome-based: strategi generalisasi lintas varian; tugas berverifikator objektif. Bukti: "SFT Memorizes, RL Generalizes" [C-09, arXiv 2501.17161].
- T-h Tool-use tuning: keandalan pemanggilan fungsi/API. Bukti: Toolformer self-supervised [C-10, arXiv 2302.04761]; ToolLLM ToolBench 16.464 API 49 kategori [C-13, arXiv 2307.16789]; xLAM pernah peringkat 1 Berkeley Function-Calling Leaderboard [C-14, arXiv 2409.03215]; AgentTuning AgentInstruct ringan tanpa merusak kemampuan umum [C-15, arXiv 2310.12823].

Peta untuk fleet GSP: masalah "great knowledge and deep technical expertise" = campuran (i) pengetahuan domain EKAS/dokumen -> wilayah T-a/T-b, dan (ii) keandalan perilaku agen -> wilayah T-d/T-f/T-h. Bukti ilmiah memisahkan keduanya: jangan pakai T-d untuk (i). Register sitasi lengkap 42 baris [C-nn] di berkas sumber seksi 8. sha16 berkas sumber: b6aa2417f2f47219.
