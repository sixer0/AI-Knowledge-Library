---
id: ft-l4-honest-eval-harness-gsp
type: pelajaran
title: "Desain eval harness internal GSP: 3 lapis metrik (L-DET/L-JUDGE/L-OUT), pass^k, dataset beku, verifier-oracle STaR"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L4-methodology.md
halaman: seksi 4 (desain eval) + seksi 3.3 (pipeline sintetis)
tanggal_akses: 2026-09-20
kelas_bukti: sintesis
sensitif: tidak
perkara: ft-eval-0920
tags: [eval-harness, pass-k, reliabilitas, sft, data-sintetis, star, ft-eval-0920]
links: [reliabilitas-pass-k, ft-l4-taksonomi-8-jalur-improvement]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Seluruh angka cocok L4-methodology.md (sha16 b6aa2417f2f47219): GAIA manusia 92% vs GPT-4+plugins 15%; AgentBench tiga penyebab kegagalan agen; tau-bench <50% pass@1 dan pass^8 <25% di retail; MT-Bench kesepakatan >80%; guard forgetting arXiv 2405.09673; LIMA ~1.000 contoh membentuk perilaku 65B; AlpaGasus 9k hasil filter dari 52k + 5,7x lebih cepat; IFD cukup 10%; Secret Recipe 2412.13337; Self-Instruct +33% absolut; Magpie 4 juta pasangan; target 5k-20k dengan batas <1k rapuh dan >50k marginal; rollout shadow silent_model + canary + rollback satu baris. Klaim dedup diverifikasi independen: id reliabilitas-pass-k memang ada di vault/riset-sistem-ai-gsp-kam dengan sumber berbeda (docx KAM) dan vonis pass^k yang sama, sehingga posisi pelengkap-bukan-duplikat benar. Kelas_bukti sintesis jujur (rancangan internal berbasis 13 sumber). REKOMENDASI: tidak ada perbaikan wajib; saat promosi catat bahwa objek reliabilitas-pass-k masih status usulan dan sensitif ya agar link tidak menggantung."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: pelajarans/ft-l4-honest-eval-harness-gsp.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Desain eval harness internal GSP: 3 lapis metrik (L-DET/L-JUDGE/L-OUT), pass^k, dataset beku, verifier-oracle STaR

Rancangan lajur L4 (13 sumber primer; akses 2026-09-20) untuk mengukur peningkatan kapabilitas SEBELUM-SESUDAH apa pun:

1. Filosofi dari benchmark publik: GAIA [arXiv 2311.12983] - manusia 92% vs GPT-4+plugins 15% pada tugas end-to-end; eval harus MISI NYATA, bukan QA artifisial. AgentBench [arXiv 2308.03688] - kegagalan utama agen = long-term reasoning, decision-making, instruction following. tau-bench [arXiv 2406.12045] - agen function-calling SOTA sukses <50% pass@1 dan TIDAK KONSISTEN: pass^8 <25% di retail; pelajaran kunci: ukur RELIABILITY (pass^k), bukan pass-rate satu kali.
2. Tiga lapis metrik GSP: L-DET (persentase gerbang mesin lolos - check_lembar PASS, scanner A1/A2 nol, tabel VERIFIKASI-AKURASI SALAH-TARGET=0); L-JUDGE (rubrik LLM juri, kalibrasi >80% kesepakatan dengan verdict manusia per MT-Bench arXiv 2306.05685, bias posisi/verbosity/self-enhancement dimitigasi randomisasi); L-OUT (pass-rate verifier aktual per profil, retry-count, fallback-rate dari LiteLLM cost tracking).
3. Protokol: dataset kasus DI-FROZEN sebelum model kandidat dilatih (holdout permanen); replikasi k>=4 untuk kasus deterministik (pass^k style); vonis hanya jika L-DET tidak REGRESI di keluarga tugas mana pun (guard forgetting, arXiv 2405.09673) DAN L-OUT naik pada keluarga target; anti-contamination = split per-misi, bukan acak per-baris.
4. Ambang keputusan: Gate-1 fungsional (L-DET naik >=10 poin absolut pada keluarga target, 0 toleransi regresi untuk yang sudah >=95%); Gate-2 reliabilitas (pass^4 naik, variance turun); Gate-3 operasional (masa bayangan: L-OUT kandidat >= baseline pada trafik setara, fallback-rate tidak naik). Semua vonis dicetak script deterministik + countersign verifier (penulis bukan verifikator).
5. Pipeline dataset (kualitas > kuantitas, angka terverifikasi): LIMA ~1.000 contoh membentuk perilaku 65B [arXiv 2305.11206]; AlpaGasus 9k hasil filter dari 52k MENGALAHKAN Alpaca asli + 5,7x lebih cepat latih [arXiv 2307.08701]; IFD cukup 10% data cherry-by-difficulty [arXiv 2308.12032]; Secret Recipe: resep populer (Tulu) dan phased training (Orca) TIDAK universal - validasi per-korpus [arXiv 2412.13337]. Target GSP: 5k-20k contoh perilaku; <1k terlalu rapuh, >50k manfaat marginal hilang di balik noise kualitas.
6. Rejection sampling dengan aset sendiri: STaR [arXiv 2203.14465] loop generate-buang-salah-latih-ulang; Self-Instruct [arXiv 2212.10560] bootstrap instruksi +33% absolut; Magpie [arXiv 2406.08464] 4 juta pasangan query-respons dari template sisi-user; Distilling Step-by-Step [arXiv 2305.02301] rationale guru sebagai supervisi multi-task; Orca [arXiv 2306.02707] peringatan: model kecil meniru GAYA guru tanpa penalarannya - evaluasi harus menguji penalaran. Keunggulan struktural GSP: verifier fleet = oracle gratis (rol yang sama dengan annotator yang harus digaji perusahaan lain).
7. Format data: standar de-facto 2026 = messages {role, content} ala OpenAI; LLaMA-Factory alpaca/sharegpt (openai = kasus khusus sharegpt); TRL standard conversation kompatibel. Transkrip sesi Hermes (state.db) + kartu kanban ber-verdict dapat dikonversi lossless ke sharegpt.
8. Rollout pasca-FT: shadow via LiteLLM traffic mirroring silent_model (menyalin request ke kandidat TANPA memengaruhi respons), canary berbobot, rollback satu baris config (docs.litellm.ai/docs/traffic_mirroring + /docs/routing, HTTP 200 2026-09-20).

Link dedup: objek reliabilitas-pass-k (vault/riset-sistem-ai-gsp-kam) sudah memuat vonis pass^k tau-bench dari kajian KAM lama (sumber berbeda, konklusi sama) - objek ini pelengkap desain operasional, bukan duplikat. sha16 berkas sumber: b6aa2417f2f47219.
