---
id: promanual-fakta-frontier-1004
type: fakta
title: "Snapshot frontier 2026-10-04: 41 entri model di 13 penyelenggara, ambang harga konteks, pola jendela servis vs arsitektur"
status: active
sumber: docs/2026-10-04-prompt-manual/research/R3/register-beku.md baris 26, 40, 122, 164, 323, 344; docs/2026-10-04-prompt-manual/research/R4/register-beku.md baris 100, 349, 350, 355
halaman: baris register R3/R4 (koordinat terukur giliran ini)
tanggal_akses: 2026-10-05
kelas_bukti: primer
sensitif: tidak
perkara: promanual-1004
tags: [promanual-1004, frontier, harga, konteks, snapshot-2026-10-04]
links: [promanual-korpus-register-1004]
penulis: gsp-librarian
diajukan: 2026-10-05
misi: PROMANUAL-1004
kartu: t_c42af89f
pin_sha16_register: R3=7a959ee9d65ee368; R4=6c131ccdb5189339
ladder_path: docs/2026-10-04-prompt-manual/research/R3a/ladder.md
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-05
catatan_verifikasi: "Verdict: terverifikasi (re-verifikasi fokus iterasi-2, 2026-10-05 23:46 WIB; audit 7 dimensi tidak diulang dan tidak ada kuantifikasi tambahan sesuai dispatch). Uji tambalan terhadap sumber: body seksi 1 baris 41-44 kini memisahkan dua basis dan keduanya cocok ke sumber primer. CONTRACT.md baris 87 (D-13, PUTUSAN K8) menyatakan Amazon Nova hosted tambahan via Bedrock dan pembilang penyelenggara frontier lingkup sensus TETAP 15; register R3 baris 164 (KL-R3-146) menyatakan pembilang frontier TERTUTUP = 41 entri di 13 penyelenggara beserta daftar per vendor. Kalimat lama yang menggabung dua pembilang tidak bersisa di grup body (grep deterministik baris >25 atas 'tidak mengubah pembilang' dan 'pembilang 13 penyelenggara lingkup': 0 hit, rc=1). Spot-check acak koordinat angka lain di body terhadap register: 8 titik, semuanya cocok, nol selisih. R3 baris 26 (KL-R3-08: context 1.05M token, max output 128K, cutoff Astra/Sol 2026-04-30 dan Luna 2026-05-18); R3 baris 40 (KL-R3-22: Fable 5.1 / Opus 5.5 / Sonnet 5.5 1M, Haiku 4.5 200K); R3 baris 122 (KL-R3-104: OpenAI >272K, xAI >=200k prompt, Google 3.1 Pro >200k, ByteDance Ark segmen (128,256], kelas DITURUNKAN-SINTESIS); R3 baris 323 (KL-R3-305: Gemma-4-31b-it 262.144 dengan sliding_window 1024, Qwen3.8-27B 262.144, Olmo-3-7B-Instruct 65.536, Phi-4 16.384); R3 baris 344 (KL-R3-326 koreksi D-24/CACAT-4: max_position_embeddings 1.048.576 dan sliding_window 128 di lapis ATAS, tanpa text_config maupun 262.144); R4 baris 100 (KL-R4-079: lima vendor 50 persen); R4 baris 349-350 (KL-R4-328/KL-R4-329 kanal pengganti HTTP 200 ber-timestamp dengan ukuran byte); R4 baris 355 (KL-R4-334: token 4K hidup di guides/fim_completion, bukan api/create-completion). Verdict iterasi-1 dipindah utuh ke riwayat-catatan-verifikasi dan tetap jadi jejak temuan; catatan_keputusan librarian konsisten dengan tambalan yang terukur. Gate sensitif/dosir tidak digantikan verifikasiku: sensitif tidak, perkara promanual-1004 tetap lewat gate librarian."
riwayat-catatan-verifikasi: "Verdict: perlu_revisi (satu butir atribusi putusan; seluruh sampel angka lain lolos). Alasan: sampling 10 titik plus SEMUA koordinat baris lolos. R3 baris 26/40/122/164/323/344 dan R4 baris 100/349/350/355 berisi butir yang sesuai klaim; tarif Zhipu GLM-5.1 6/24 dan 8/28 yuan ada di KL-R3-293 baris 311; konversi 555k kata dan 2,5M karakter Unicode ada di KL-R3-23 baris 41; pembilang 41 entri di 13 penyelenggara dihitung ulang dari raw/R3a/frontier_counter.json menghasilkan 41 entri dan 13 penyelenggara dengan daftar per vendor identik; pin R3 7a959ee9d65ee368 dan R4 6c131ccdb5189339 cocok byte; jalur ladder_path R3a/ladder.md ada (36.354 B). SATU cacat: kalimat 'Putusan controller D-13: Amazon Nova berstatus hosted tambahan via Bedrock, tidak mengubah pembilang 13 penyelenggara lingkup' menggabung dua pembilang berbeda; teks CONTRACT.md baris 87 menyatakan pembilang penyelenggara frontier lingkup sensus TETAP 15, sedangkan 13 adalah pembilang frontier tertutup KL-R3-146; kontradiksi hidup di sumber dan objek menyalin satu sisi tanpa penanda basis. Rekomendasi konkret: tulis dua basis terpisah, misalnya 'pembilang penyelenggara lingkup sensus tetap 15 per D-13; pembilang frontier tertutup 13 penyelenggara per KL-R3-146', jangan ubah angka produk mana pun, lalu ajukan ulang untuk promosi."
catatan_keputusan: "dipromosikan: PROMANUAL-1004 ILPRO t_c42af89f: custodian verdict terverifikasi; pin register 4/4 terukur ulang; non-sensitif non-dosir; dedup wiki+IL 0"
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-05
dipromosikan-ke: faktas/promanual-fakta-frontier-1004.md
---

# Snapshot frontier 2026-10-04: 41 entri model di 13 penyelenggara, ambang harga konteks, pola jendela servis vs arsitektur

Fakta produk bertanggal. Seluruh angka adalah snapshot tanggal potong 2026-10-04 dari
dokumentasi resmi penyelenggara (kelas NORMATIF-DOK kecuali disebut lain), terverifikasi
entity-match dan lolos gerbang rilis v4 (SALAH-TARGET 0 dari 759 URL fetch segar).
Wajib ambil ulang sebelum dipakai sebagai persyaratan kontrak.

## 1. Pembilang frontier tertutup [R3, KL-R3-146, register baris 164]

41 entri model frontier di 13 penyelenggara pada tanggal potong, daftar per halaman resmi
(berkas raw/R3a/frontier_counter.json; uji ulang independen vonis lajur: 41/41 terverifikasi
di dumps): OpenAI 4 (gpt-6-astra, gpt-6.1-sol, gpt-6-sol, gpt-6-luna); Anthropic 4
(claude-fable-5.1, opus-5.5, sonnet-5.5, haiku-4.5); Google 3; xAI 3; Mistral 4; Cohere 4;
Moonshot 1 (kimi-k3); Zhipu 4; ByteDance 3; MiniMax 3; DeepSeek-API 2; StepFun 3; Alibaba 3.
Dua pembilang berbeda basis (koreksi iter-1, preseden verdict custodian): putusan controller
D-13 (CONTRACT.md baris 87) menyatakan pembilang penyelenggara frontier LINGKUP SENSUS tetap 15
(Amazon Nova hosted tambahan via Bedrock); pembilang frontier TERTUTUP KL-R3-146 = 41 entri di 13
penyelenggara pada tanggal potong. Kedua angka sah pada basisnya masing-masing.

## 2. Kartu spesifikasi contoh (field dinamis bertanggal)

- GPT-6 (OpenAI, halaman resmi models): context window 1.05M token; max output 128K token;
  knowledge cutoff Astra/Sol 2026-04-30, Luna 2026-05-18 [R3, KL-R3-08, baris 26].
- Lineup Anthropic: Fable 5.1 / Opus 5.5 / Sonnet 5.5 = 1M token; Haiku 4.5 = 200K [R3, KL-R3-22, baris 40].
- Konversi resmi Anthropic: 1M token ~ 555k kata / 2,5M karakter Unicode (tokenizer sejak Opus 4.7).

## 3. Ambang harga konteks panjang (pola lintas provider) [R3, KL-R3-104, baris 122]

Ambang konteks panjang memicu tarif lebih tinggi untuk SELURUH token request, bukan hanya
token di atas ambang. Diturunkan dari 4 sumber resmi independen (DITURUNKAN-SINTESIS):
OpenAI >272K; xAI >=200k prompt; Google 3.1 Pro >200k; ByteDance Ark segmen (128,256].
Pola sama dipakai vendor CN: Zhipu GLM-5.1 <32K = 6/24 yuan, >=32K = 8/28 yuan [R3, KL-R3-293].

## 4. Diskon batch lintas vendor [R4, KL-R4-079, baris 100]

OpenAI 50%, Anthropic 50%, Google 50%, Mistral 50%, Zhipu 50% - kelima terverifikasi dari
halaman resmi masing-masing (sintesis KL-R4a-08/24/32/45/72, tiap sumber primer terdaftar terpisah).

## 5. Jendela servis berbeda dari jendela arsitektur (jebakan baca config)

- DeepSeek-V4-Pro config.json resmi: max_position_embeddings 1.048.576 dengan sliding_window
  128 di lapis ATAS; berkas TIDAK memuat kunci text_config maupun 262.144 - klaim awal
  KL-R3-303 dicabut-sebagian oleh baris koreksi KL-R3-326 (putusan D-24 / CACAT-4) [R3, baris 344].
  Pelajaran yang tetap terdukung: membaca satu field config saja = salah simpul; jendela
  servis (1M) bukan jendela atensi per-sublayer.
- Kelas konteks menengah dari config resmi (TERUJI penuh): Gemma-4-31b-it text_config 262.144
  (sliding_window 1024); Qwen3.8-27B 262.144; Olmo-3-7B-Instruct 65.536; Phi-4 16.384
  [R3, KL-R3-305, baris 323].
- Entri gated HuggingFace (Llama-4-Maverick, Nemotron-3-Ultra-550B, ERNIE-4.5-300B,
  command-r-plus-08-2024) mengembalikan HTTP 401 dan dicatat tanpa menembus - floor legal
  platform, angka konteks keempatnya TIDAK ADA DI RAK via jalur ini [R3, KL-R3-306].

## 6. Kanal rujukan yang mati dan penggantinya (jejak koreksi hidup)

URL dokumentasi ber-under_score mati 404 pada 2026-10-05 (guide .md OpenAI dan Claude):
KL-R4-016 dan KL-R4-025 sumbernya dicabut oleh baris koreksi KL-R4-328/KL-R4-329 yang
memindah kanal ke path hidup ber-entity-match (tools-web-search.md, tools-computer-use.md,
computer-use-tool.md, web-search-tool.md; HTTP 200 ber-timestamp, ukuran byte tercatat)
[R4, baris 349-350]. Nilai '4K' keluaran FIM DeepSeek berasal dari halaman
guides/fim_completion, bukan halaman API reference [R4, KL-R4-334, baris 355].
