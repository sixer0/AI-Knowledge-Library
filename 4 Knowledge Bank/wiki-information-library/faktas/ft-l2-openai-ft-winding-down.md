---
id: ft-l2-openai-ft-winding-down
type: fakta
title: "OpenAI self-serve fine-tuning winding-down: GSP tak memenuhi syarat mulai 2026-05-07"
status: active
sumber: docs/2026-09-20-ft-eval-0920/lajur/L2-hosted-platforms.md
halaman: seksi 2 klaim C-01..C-08
tanggal_akses: 2026-09-20
kelas_bukti: primer
sensitif: tidak
perkara: ft-eval-0920
tags: [fine-tuning, openai, platform-hosted, vendor-status, ft-eval-0920]
links: [ft-l2-harga-ft-hosted-2026]
penulis: gsp-librarian
diajukan: 2026-09-20
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-20
catatan_verifikasi: "Verdict: terverifikasi || Alasan: Enam butir cocok verbatim dengan L2 seksi 2 C-01..C-07 (sha16 289ea28bb003c49c): kutipan winding-down + 371.836 B + ts 2026-09-20T14:40+07; linimasa 07-05-2026 / 02-07-2026 / 06-01-2027 + 466.654 B; metode SFT/Vision/DPO/RFT dan daftar model tanpa kelas GPT-5.x; harga o4-mini $100/jam, gpt-4.1 $25, 4.1-mini $5, nano $1,50, gpt-4o $25, 4o-mini $3, FT input $0,80/M vs dasar $0,40/M + pricing.md 23.005 B; minimum 10 contoh + 29.465 B; kebijakan data sejak 01-03-2023 + retensi jobs 30 hari + files until deleted + 603.620 B. Rujukan verifier t_44faa91c cocok peta kartu contract.md (S10) dan re-check V2 19/19 cocok V-VERDICT L124. Implikasi GSP (belum pernah FT = tidak memenuhi syarat) adalah pembacaan langsung tabel C-02. REKOMENDASI: tidak ada; tanggal linimasa wajib utuh saat promosi karena menjadi pemicu kelayakan vendor."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-20
dipromosikan-ke: faktas/ft-l2-openai-ft-winding-down.md
catatan_keputusan: "dipromosikan: FT-EVAL-0920 S13: lolos kurasi librarian + verifikasi custodian 2026-09-20"
---

# OpenAI self-serve fine-tuning winding-down: GSP tak memenuhi syarat mulai 2026-05-07

Vonis lajur L2 misi FT-EVAL-0920 (akses URL 2026-09-20 WIB; diverifikasi silang verifier t_44faa91c CHECK 2 entity-match 14/14 SALAH-TARGET 0, re-check V2 19/19 hijau):

1. Kutipan resmi [C-01, SOURCE-DERIVED]: "OpenAI is winding down the fine-tuning platform. The platform is no longer accessible to new users... existing users... will be able to create training jobs for the coming months. All fine-tuned models will remain available for inference until their base models are deprecated." Sumber primer: https://platform.openai.com/docs/guides/fine-tuning (HTTP 200, 371.836 B, akses 2026-09-20T14:40+07).
2. Linimasa penutupan [C-02, tabel "Update to OpenAI's self-serve fine-tuning"]: 07-05-2026 (dd-mm-yyyy) pembuatan job ditutup untuk organisasi yang belum pernah menjalankan fine-tuning; 02-07-2026 ditutup untuk organisasi tanpa inferensi FT dalam 60 hari terakhir; 06-01-2027 pelanggan aktif pun tidak bisa membuat job baru. Sumber: https://platform.openai.com/docs/deprecations (HTTP 200, 466.654 B). Implikasi GSP: belum pernah FT = TIDAK memenuhi syarat mulai hari pengukuran.
3. Metode terdokumentasi [C-03]: SFT, Vision SFT, DPO, RFT (grader). Model: SFT/Vision gpt-4.1/4.1-mini/4.1-nano + gpt-4o-2024-08-06; DPO keluarga gpt-4.1 + gpt-4o; RFT o4-mini-2025-04-16. Tidak ada model kelas GPT-5.x di daftar self-serve.
4. Harga latih per 1M token [C-04]: o4-mini $100,00/jam; gpt-4.1 $25,00; gpt-4.1-mini $5,00; gpt-4.1-nano $1,50; gpt-4o $25,00; gpt-4o-mini $3,00. Inferensi hasil FT lebih mahal dari dasar (gpt-4.1-mini FT input $0,80/M vs dasar $0,40/M). Sumber: https://platform.openai.com/docs/pricing.md (HTTP 200, 23.005 B).
5. Minimum dataset 10 contoh; format JSONL chat messages; upload POST /v1/files purpose="fine-tune" [C-05]. Sumber: https://platform.openai.com/docs/guides/supervised-fine-tuning.md (HTTP 200, 29.465 B).
6. Kebijakan data [C-07]: sejak 01-03-2023 data API tidak dipakai melatih model OpenAI kecuali opt-in; retensi /v1/fine_tuning/jobs 30 hari tanpa human review; /v1/files retensi "until deleted". Sumber: https://developers.openai.com/api/docs/guides/your-data (HTTP 200, 603.620 B).

Provenans berjenjang (AM-G4): ladder 18 rung ber-timestamp di berkas sumber seksi 5; log mentah 136 entri docs/2026-09-20-ft-eval-0920/raw/L2/ladder.log; gerbang entity-match SPK-002 diterapkan per klaim. sha16 berkas sumber: 289ea28bb003c49c.
