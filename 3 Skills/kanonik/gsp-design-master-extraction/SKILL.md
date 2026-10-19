---
name: gsp-design-master-extraction
description: "Ekstraksi system design dari PDF/gambar brand-manual -> design_master.json (SOP Imagegen 2.1), atau susun dari nol setara mutu SOP. Dimuat oleh gsp-design-system-specialist saat user minta design dibuatakan."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: design
    tags: [gsp, design-master, imagegen, ekstraksi, pdf, vision]
  hermes:
    tags: [gsp, design, imagegen21]
---

# GSP Design Master Extraction

Pakai skill ini ketika user meminta **system design DIBUATKAN oleh agent** (jalur B
gerbang 2 di `/create-deck-gsp` / `/create-image-gsp`), dengan atau tanpa materi brand
(PDF manual, gambar, atau tanpa keduanya). Hasil akhir SATU bentuk: berkas
`design_master_<brand>_v<N>.json` yang lolos validator dan siap dipakai pipeline SOP.

Rujukan kanonik: SOP `C:/Users/TRIAL/workspace/handoff/imagegen21_sop_handoff.md` §13
(terutama §13.2 warna-dalam-kata, §13.3 approval user), template
`C:/Users/TRIAL/workspace/handoff/templates/design_master_template.json`, contoh teruji
`C:/Users/TRIAL/workspace/handoff/examples/swarm01_spec.json`, preset token
`gsp-design-system-grill/references/master-design/gsp-ds-sets.json`.

## Tiga jalur masuk

### JALUR E — Ekstraksi dari PDF brand-manual (user melampirkan PDF)
1. Jalankan alat: `python <skill>/scripts/extract_pdf.py <file.pdf> <workdir>/extract [--max-pages 40] [--width 2200]`
   -> `manifest.json` (sha256 berkas + per halaman: PNG, luminansi, tone, warna dominan terukur, kutipan teks).
2. Pilih halaman representatif (cover, halaman palet/tipografi, halaman contoh slide): render PNG-nya jadi
   CALON referensi @512 (latar gelap sesuai SOP; halaman terang = bahan gaya saja, jangan jadikan referensi
   gelap palsu).
3. **Isi dossier dengan VISION, bukan kira-kira**: untuk tiap halaman terpilih, panggil `vision_analyze`
   dan ekstrak token desain persis (judul tipografi, warna palet urut, gaya panel, ikon, komposisi).
   Silangkan dengan angka terukur manifest (tone/dominan) — bila vision dan pengukuran bertentangan,
   ukur ulang crop; jangan menelan salah satu bulat-bulat.
4. Logo: hanya dari BERKAS yang user berikan (halaman PDF yang di-crop juga sah sebagai sumber berkas).
   Crop lockup dengan latar aslinya (jangan transparan), simpan @512, tandai `kind: reproduce_exactly`,
   posisikan TERAKHIR di `references.files`. Tanpa logo sama sekali: `logo_description` = "no logo" dan
   prompt tidak menyebut logo (norma D-03).

### JALUR I — Ekstraksi dari gambar (screenshot/papan gaya/logo PNG)
Langsung ke langkah vision seperti E.3 untuk tiap gambar; hitung sha256 + simpan salinan @512
latar gelap/origonal (jangan keyed transparency). Ukur tone dan warna dominan dengan PIL/numpy
sebelum mendeskripsikan, supaya klaim "dark navy" punya angka.

### JALUR S — Dari nol (user tidak punya materi)
Susun `design_master.json` SETARA MUTU SOP dengan langkah:
1. Tanya (HIL, sudah jadi gerbang perintah): arah (D1..D5 atau preset bernama), bahasa, ada/tidak logo+berkasnya.
2. Bila user menyebut preset MASTER_DESIGN: baca kartu `gsp-ds-set-<slug>.md` + entri `gsp-ds-sets.json`
   sebagai SUMBER TOKEN; konversi wajib: hex -> NAMA WARNA dalam kata + urutan (SOP §13.2 melarang hex
   di brand_rules), `source` preset dicatat di `sources`.
3. Bila arah bebas: pakai default terukur SOP (D1 dark cinematic satu-satunya yang measured) atau nyatakan
   `basis: inferred from a thin brief` + isi `inferred_items` jujur (palet dipilih agent, tipografi dipilih agent).
4. Isi SEMUA field template tanpa sisa `<...>`: `brand_rules` lengkap (background, palette_in_order kata,
   accent_usage, title/body typography, icon_style, panels, logo_description, logo_rules, voice),
   `deck_blocks` 1-5 ditulis penuh dengan slot brand terisi (salin struktur dari
   `templates/deck_prompt_templates.md` blok 1-5), `identity_strings` dari nama brand user,
   `lexicon_cues` kosong boleh (diisi setelah gagal render), `archetypes` salin status registry template,
   `known_failures` salin dari template, `seed_rule` dan `changelog` terisi.

## Gerbang mutu (WAJIB sebelum serahkan)

```
python <skill>/scripts/validate_design_master.py <design_master.json> [--refs-base <dir>]
```
Validator menolak bila: sisa placeholder `<...>`, field wajib kosong, hex muncul di `brand_rules`
(pelanggaran §13.2), referensi >10 / bukan .png / file tidak ada / sha256 tidak cocok, logo bukan
entri terakhir atau tanpa `kind: reproduce_exactly`, `deck_blocks` kehilangan blok 1-5, `language`
tidak valid, `approved_by_user` kosong. Sertakan output PASS validator di penyerahan.

## Penyerahan

Serahkan ke controller/pekerja deck: (1) `design_master_<brand>_v<N>.json`, (2) folder `refs/`
PNG @512 + sha256, (3) hasil validator, (4) tabel bukti per token: sumber (halaman PDF / gambar /
preset / inferred) + angka terukur (tone, luminansi, dominansi warna) — supaya verifier bisa menguji
tanpa membuka materi asli. Approval user (SOP §13.3) adalah gerbang controller, bukan kamu: tandai
status `needs-review` sampai user menyetujui, lalu `approved_by_user` diisi controller dengan tanggal
+ kata-kata user.

## Larangan

- Mengarang token yang tidak terlihat terukur/tersimpan (entity-match: klaim warna harus punya
  bukti piksel atau kartu preset).
- Menaruh hex di `brand_rules` (konversi ke kata; hex hidup hanya di `sources`/catatan preset).
- Menjadikan halaman terang sebagai referensi "latar gelap" dengan rekayasa filter.
- Mengklaim selesai tanpa validator PASS + berkas refs utuh.
