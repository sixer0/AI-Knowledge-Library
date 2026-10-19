# SKOP PATEN jalur generasi: lokal vs OpenAI (D-11 BAKU-IMGW, 04-09)

> **AMANDEMEN 24-09-2026 (user keputusan; STANDAR IMAGEGEN-2.1):** vonis
> "banyak teks / brosur / slide TIDAK LAYAK lokal" berlaku untuk rantai lama
> **Endpoint A/B/C ComfyUI (Qwen-Image-2512)**. Kelas itu kini **LAYAK lokal**
> lewat rantai baru **Imagegen 2.1** (Qwen-Image-2.1, resep A4, layanan
> `gsp-imagegen21.service` di inference-kaytus :8040 via tunnel ssh) dengan
> bukti terukur: 40 string/1.202 char -> identity 7/7, primary 33/35, scene 5/5
> (`C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md`, SOP v2).
> Routing yang berlaku: ikon/hero non-slide tetap Endpoint A :11400;
> **slide/gambar teks padat -> Imagegen 2.1**; teks sangat padat tanpa batas
> jumlah string -> OpenAI tetap cadangan. Tabel di bawah dipertahankan sebagai
> jejak historis vonis lama.

Sumber keputusan: `docs/2026-09-04-baku-image-workflow/contract.md` baris
113-115 (keputusan user D-11, update 04-09 15:45), path relatif workspace
bersama `C:/Users/TRIAL/workspace/gsp-hermes/workspace/`. Dievaluasi Skill
Manager di kartu t_4357c0d1 (CHANGE REQUEST, APPROVE penuh) dan dieksekusi
lewat tiket kurasi t_8e71ddd9. Model image-gen lokal: Qwen-Image-2512 pada
Endpoint A/B/C server ComfyUI GSP.

## Tabel SKOP PATEN

| Kelas keluaran | Lokal (A/B/C) | Jalur bila tak mampu |
|---|---|---|
| Ikon (tanpa teks dalam gambar) | LAYAK - sheet grid @12-16 step cfg 3,5, negative anti-teks, seed tercatat | - |
| Hero image | LAYAK - mode kualitas 28-32 step cfg 4,5, maks 1664x928 | - |
| Hyper-realistic image | LAYAK | - |
| Bahan attachment dokumen profesional | LAYAK sebagai bahan (bukan teks final) | - |
| Gambar banyak teks / teks kecil | TIDAK LAYAK | OpenAI (gpt-image) |
| Brosur | TIDAK LAYAK | OpenAI (gpt-image) |
| Slide presentasi profesional kompleks | TIDAK LAYAK | OpenAI (gpt-image) |

## Aturan routing

1. Sebelum menyusun prompt, klasifikasikan kelas keluaran terhadap tabel di atas.
2. Kelas TIDAK LAYAK: jangan pakai rantai prompt lokal (Endpoint A/B/C);
   serahkan ke jalur OpenAI (gpt-image) atau hybrid2.
3. Kelas LAYAK: seed wajib tercatat + negative anti-teks; teks pada aset hanya
   lewat komposit deterministik (mis. PIL), bukan teks generatif.

## Prosedur hybrid2 (baku)

1. Generate aset visual secara lokal (Endpoint A): hero, backdrop, strips,
   radar, dsb. Tiap aset: seed tercatat + negative anti-teks.
2. Serahkan aset sebagai referensi ke OpenAI (gpt-image) untuk merakit slide
   final.
3. Arsipkan aset, slide final, dan strip banding vs benchmark. Contoh nyata:
   `output/hybrid2/` (4 aset lokal seed tercatat + 3 slide final OpenAI) plus
   `BANDING-slide-0{1,2,3}-benchmark-vs-hybrid2.jpg`.

## Bukti (diukur ulang langsung di disk oleh Skill Manager, t_4357c0d1)

- P1: `docs/2026-09-04-baku-image-workflow/verification/PROBE-ASET-IKON-TEKS.md`
  (6589 B): ejaan generatif VARIAN-A 2/6, galat non-deterministik, reseed percuma.
- P2: `docs/2026-09-04-baku-image-workflow/verification/PROBE-ASET-IKON-TEKS-B3.md`
  (4838 B): komposit deterministik PIL 6/6; kualitas ikon factory 4/5 (sebab ikon
  tetap LAYAK lokal).
- E5: `docs/2026-09-04-baku-image-workflow/verification/MUTU-OBJEKTIF-UJI.md`
  (14424 B): scene terlalu gelap-datar, #050a14 mendominasi 97,4% area, hasil
  2,3-3,1x lebih gelap dari benchmark.
- E6b: `docs/2026-09-04-baku-image-workflow/output/E3-LAPORAN.md` seksi 11
  (35935 B): rakitan komponen butuh banyak iterasi, hasil akhir masih jauh dari
  benchmark.
- hybrid2: `docs/2026-09-04-baku-image-workflow/output/hybrid2/` +
  `BANDING-slide-0{1,2,3}-benchmark-vs-hybrid2.jpg`.

## Catatan SOP-1 / Endpoint B

SOP-1 (jalur slide teks-padat via Endpoint B) tetap tersedia untuk kasus khusus
yang diputuskan controller (arsip sidang F), namun keputusan baku mengikuti
D-11: slide presentasi profesional kompleks lewat OpenAI/hybrid2.
