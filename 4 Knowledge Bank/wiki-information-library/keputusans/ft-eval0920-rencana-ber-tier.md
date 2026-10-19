---
id: ft-eval0920-rencana-ber-tier
type: keputusan
title: "RENCANA-FT-SWARM: rekomendasi ber-tier 0-3 untuk fleet GSP + empat keputusan gerbang user"
status: active
sumber: docs/2026-09-20-ft-eval-0920/output/RENCANA-FT-SWARM.md
halaman: Part 3 + DECISION BLOCK
tanggal_akses: 2026-09-20
kelas_bukti: sintesis
sensitif: tidak
perkara: ft-eval-0920
tags: [rencana, fine-tuning, tier, roadmap, keputusan-user, ft-eval-0920]
links: [ft-l4-kapan-ft-bukan-jawaban, ft-l2-harga-ft-hosted-2026, ft-l3-kelayakan-qlora-5070ti]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Provenans lengkap (sumber output/RENCANA-FT-SWARM.md + pointer Part 3/DECISION BLOCK; sha16 sumber fab3aa68302842fd terukur ulang cocok). Uji kesetiaan RAW lolos: rentang biaya Tier 1 ($8-45 Fireworks utk 15-90 jt token; $75-450 Vertex tarif 2.5 Flash), dataset 5k-20k, kalibrasi 100-step pengganti faktor derived 0,55, empat keputusan gerbang user, dan larangan lintas-tier semuanya cocok dengan RENCANA baris 52-68; klaim RE-CHECK V2 PASS 19/19 terverifikasi di lajur/V-VERDICT.md L124. YAML valid, title==H1, satu baris status, kelas_bukti sintesis jujur (dokumen keputusan lintas lajur). Dedup bersih: id unik dalam folder, tidak bentrok dengan 118 id vault/riset-sistem-ai-gsp-kam maupun 792 entri wiki. REKOMENDASI: tidak ada perbaikan wajib; saat promosi bawa tanggal akses 2026-09-20 sebagai batas-waktu angka biaya (harga vendor volatile) dan jangan naikkan isi DECISION BLOCK sebagai fakta sebelum user menjawab empat keputusan."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: keputusans/ft-eval0920-rencana-ber-tier.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# RENCANA-FT-SWARM: rekomendasi ber-tier 0-3 untuk fleet GSP + empat keputusan gerbang user

Status objek: USULAN keputusan (belum disahkan user; bagian "DECISION BLOCK FOR THE USER" masih terbuka). Dokumen sumber lolos verifier V2 (RE-CHECK PASS 19/19) dan gerbang naturalisasi doc (sha16 fab3aa68302842fd). Basis bukti: lajur L1-L4 + S0-S2 misi FT-EVAL-0920, semua terukur 2026-09-20.

Rekomendasi ber-tier + syarat pindah:
- TIER 0 (default, tanpa latih, tanpa biaya eksternal): bangun eval harness beku dari ~100 kartu kanban misi selesai; RAG/EKAS retrieval; skill engineering dari kegagalan nyata; memory tiering; Reflexion-style catatan kegagalan. SYARAT pindah Tier 1: eval beku tersedia DAN kegagalan BERULANG bersifat PERILAKU (format/urutan/tool-call) pada tugas yang pengetahuannya SUDAH tersedia di konteks. Kalau kegagalan masih "tidak tahu faktanya" -> perbaiki Tier 0, jangan FT.
- TIER 1 (LoRA hosted, ~$10-100an per eksperimen): dataset perilaku 5k-20k contoh sharegpt dari misi PASS-verdict + transkrip tersanitasi; vendor Fireworks (~$8-45 untuk 15-90 jt token latih pada tarif $0,50/M) atau Vertex (~$75-450 pada tarif 2.5 Flash; rasio char/token = asumsi yang wajib diganti tokenizer nyata); gate: no-regression lintas keluarga + naik >=10 poin target + pass^4 naik; registrasi hasil = 1 entri model_list LiteLLM; shadow seminggu via silent_model lalu canary.
- TIER 2 (LoRA lokal 5070 Ti, data tidak keluar): Unsloth QLoRA Qwen3-8B/14B di WSL2/Docker; serving Ollama/llama.cpp; syarat masuk: kalibrasi 100-step mengganti faktor derived 0,55; guru distilasi hanya open-weight permisif.
- TIER 3 (DPO/RL/continued-PT): hanya bila Tier 2 mentok TERUKUR (delta L-DET jenuh padahal kegagalan masih perilaku) atau kebutuhan reward-verifiable; korpus harus orde miliaran token untuk continued PT.
- Larangan eksplisit semua tier: FT untuk injeksi fakta EKAS; full FT >= 3B di mesin ini; torchtune sebagai fondasi; distilasi dari Claude tanpa izin tertulis; akun Google UNPAID untuk korpus GSP.

Empat keputusan gerbang untuk user: (1) approve Tier 0 sekarang; (2) pilih vendor Tier 1 + budget + persetujuan data keluar, atau langsung Tier 2 privat; (3) pasok satu baris provenance bobot gspthinker180b-finetuned dari server inference (menentukan branch A retrain-incumbent vs branch B train-students); (4) terima/tolak kesimpulan headline "knowledge belongs to retrieval, behavior belongs to weights".

Langkah server-side (step 13) jalan paralel dan butuh user sejak hari pertama. sha16 berkas sumber: fab3aa68302842fd.
