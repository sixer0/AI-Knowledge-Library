# PAKET TOKEN MASTER_DESIGN (satu-satunya sumber kebenaran token DS GSP)
Dimiliki oleh skill `gsp-design-system-grill` (keputusan D-TA-7 blueprint t_e06f0d9e; disahkan controller D13).
Generator paket: SM-1 t_de708ae3, 2026-09-01. Sumber hulu: `docs/2026-09-01-master-design-adaptasi/study/` (13/13 set terverifikasi cakupan halaman penuh).

## Isi
| berkas | peran |
|---|---|
| [`gsp-ds-sets.json`](gsp-ds-sets.json) | mirror byte-identik `study/DS-batch-ALL.json` - 13 set mesin-baca (palette role->hex, usage_ratio, mood, components, rules, gaps, legenda sumber palet) |
| `gsp-ds-set-<slug>.md` × 13 | kartu token per preset (palet + rujukan halaman, tipografi verbatim, grid, komponen, larangan, GAP jujur) |
| [`GSP-DS-KELUARGA.md`](GSP-DS-KELUARGA.md) | kondensasi konstanta A1–A11, pola bidang B1–B4, meta-rules MR1–MR6 siap-kode |
| [`gsp-font-manifest.md`](gsp-font-manifest.md) | 62 keluarga font × 9 kategori + path zip sumber (NOL bundling biner - D-TA-2) |

## Cara pakai (kanal apa pun: asset / slide / master prompt / HTML)
1. Pilih preset: default **GENERAL**; 12 preset bernama: BNN, BNPT, BUSINESS, CYBER, MILITARY, POLRI, TNI-AD, TNI-AL, TNI-AU, TEKNIK, VISUAL, KEMHAN (slug = nama file kartu).
2. Baca nilai HANYA dari [`gsp-ds-sets.json`](gsp-ds-sets.json) / kartu set - jangan mengarang, jangan menyalin HEX ke berkas skill lain (pointer saja).
3. Terapkan meta-rules MR1–MR6; konflik dua standar mengikuti hierarki D-TA-4 (kanal dokumen -> GSP-SDT menang; kanal visual -> DS menang; HTML -> blok identitas dulu, lalu palet DS).
4. Nilai berlabel `terukur-piksel` = hasil ukur piksel (bukan tercetak dokumen); `estimasi-vision` = perkiraan, BUKAN spesifikasi; `TIDAK_TERBACA` tetap kosong - dilarang mengisi dengan karangan.

## Preset -> domain (pemilihan cepat)
institusional-kepolisian: POLRI, BNN, BNPT, militer-matra: TNI-AD, TNI-AL, TNI-AU, MILITARY, siber: CYBER, bisnis: BUSINESS, engineering: TEKNIK, editorial: VISUAL, pemerintah-pertahanan: KEMHAN, netral/proyek-lain: GENERAL.

## Aturan teks keluaran (D15+D16)

Larangan em-dash (U+2014) MUTLAK (D17): konten keluaran (teks, slide, HTML, prompt, teks dalam gambar) tidak memakai em-dash sama sekali, TANPA pengecualian blok terkendali maupun verbatim (pengecualian verbatim hanya berlaku untuk middle dot). Alternatif saat menulis: koma, titik, titik dua, kurung, atau spasi-hyphen. Saat verifikasi: scan U+2014 pada artefak final, ganti otomatis sampai nol, laporkan jumlah penggantian.

Middle dot (U+00B7) dilarang di konten keluaran. Pengecualian HANYA pada string blok terkendali yang meniru master design verbatim (mis. footer TERBATAS · Terkendali). Alternatif di prosa: koma, garis miring, kurung, atau titik dua. Bullet daftar boleh; marker dan gayanya MENGIKUTI preset master design terpilih (lihat bagian Ikonografi/Komponen di references/master-design/gsp-ds-set-<slug>.md), bukan • generik hiasan di prosa.

Catatan deviasi tipografi (D17): pola footer sumber `n <U+2014> mm` (tercetak R-1) dirender sebagai `n / mm` demi kepatuhan D17, mengikuti preseden pola footer PDF keluarga GSP-SDT `HLM n / mm` (SPEC-DOC-SYSTEM.md R-5); label provenans ikut dirender `[jenis / sumber, hal]`. Ini disengaja, bukan cacat.

STATUS: complete
