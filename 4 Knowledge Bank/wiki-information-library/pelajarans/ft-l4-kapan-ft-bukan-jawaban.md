---
id: ft-l4-kapan-ft-bukan-jawaban
type: pelajaran
title: "Evidence stack 13 sumber primer: FT menambah halusinasi untuk fakta baru; RAG menang untuk pengetahuan langka/internal"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L4-methodology.md
halaman: seksi 2 (evidence stack) + seksi 8 register C-01..C-22
tanggal_akses: 2026-09-20
kelas_bukti: sintesis
sensitif: tidak
perkara: ft-eval-0920
tags: [fine-tuning, halusinasi, rag, pengetahuan-baru, bukti-ilmiah, ft-eval-0920]
links: [ft-l4-taksonomi-8-jalur-improvement]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: 13 butir evidence stack cocok verbatim dengan L4 seksi 2 termasuk kutipan bersandaran (struggle to acquire new factual knowledge; learned significantly slower; linearly increase the model's tendency to hallucinate; RAG consistently outperforms; RAG surpasses FT by a large margin) dan pemetaan C-nn ke register seksi 8 (C-01 2405.05904, C-03 2312.05934, C-04 2403.01432, C-02 2404.00213, C-16 2402.05119, C-17 2305.11383, C-18 Anyscale, C-19 Meta, C-20 2601.07054, C-21 2607.08393, C-22 2604.15574, C-23 LIMA, C-24 sama dengan C-07). Catatan negatif terverifikasi (judul persis Lin et al tidak ada di arXiv per 2026-09-20) cocok L4 baris 191 dan menaikkan kejujuran objek. Vonis sintesis diberi label sebagai vonis (RENCANA 2.1), bukan fakta primer. REKOMENDASI: tidak ada; pertahankan catatan negatif saat promosi agar pekerja berikutnya tidak mencari judul yang terbukti tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: pelajarans/ft-l4-kapan-ft-bukan-jawaban.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# Evidence stack 13 sumber primer: FT menambah halusinasi untuk fakta baru; RAG menang untuk pengetahuan langka/internal

Temuan independen yang saling menguatkan, diverifikasi 2026-09-20 dari halaman abstrak/berkas primer (mentah di raw/L4/, kutipan di abstracts.txt):

1. [C-01] Gekhman dkk., arXiv 2405.05904 (Mei 2024): dalam closed-book QA terkontrol, "large language models struggle to acquire new factual knowledge through fine-tuning"; contoh dengan pengetahuan baru "learned significantly slower" dan setelah pun terpelajari "they linearly increase the model's tendency to hallucinate". Kesimpulan penulis: FT mengajarkan model memakai pengetahuan pretraining lebih efisien, bukan menambah fakta.
2. [C-03] Ovadia dkk., arXiv 2312.05934: "RAG consistently outperforms [unsupervised fine-tuning], both for existing knowledge encountered during training and entirely new knowledge".
3. [C-04] arXiv 2403.01432 (SIGIR-AP 2024): 12 LM diuji; FT menaikkan performa lintas popularitas entitas, tetapi "RAG surpasses FT by a large margin particularly for least popular factual knowledge". Kasus persis korpus GSP: dokumen internal = pengetahuan frekuensi nol di pretraining.
4. [C-02] Mecklenburg dkk., arXiv 2404.00213: injeksi pengetahuan via SFT punya keterbatasan terdokumentasi.
5. [C-16] arXiv 2402.05119 + [C-17] arXiv 2305.11383: instruction tuning memasang bentuk respons, bukan pengetahuan.
6. [C-18] Anyscale "Fine Tuning Is For Form, Not Facts" (2023; hidup 2026) + [C-19] Meta AI blog "To fine-tune or not to fine-tune": panduan resmi vendor searah.
7. [C-20] arXiv 2601.07054 (2026): FT vs RAG untuk multi-hop QA dengan pengetahuan baru.
8. [C-21] arXiv 2607.08393 (2026): fakta yang tampak terhafal gagal tergeneralisasi ke penalaran ("Knowing-Using Gap").
9. [C-22] arXiv 2604.15574 (2026): mengapa FT mendorong halusinasi dan cara perbaikan.
10. [C-23] LIMA arXiv 2305.11206: ~1.000 contoh kurasi membentuk perilaku 65B - arah solusi yang benar untuk target PERILAKU.
11. [C-24] = C-07 Biderman dkk. LoRA Learns Less and Forgets Less: guard catastrophic forgetting; LoRA-vs-full-FT trade-off learn/forget.

Vonis sintesis (RENCANA-FT-SWARM 2.1): permintaan "great knowledge" milik lapisan retrieval/skill (Tier 0), BUKAN bobot; yang sah dilatih = perilaku (format, urutan kerja, kepatuhan gerbang, pola tool-use) setelah eval harness berdiri. Larangan eksplisit semua tier: FT untuk injeksi fakta EKAS.

Catatan negatif terverifikasi (supaya tidak dicari ulang): judul persis "Fine-tuning updates form not knowledge" (Lin et al.) TIDAK ada di arXiv per 2026-09-20; padanan sahih yang dipakai: C-18, C-23, C-01, C-17. sha16 berkas sumber: b6aa2417f2f47219.
