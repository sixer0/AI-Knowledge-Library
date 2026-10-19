# Aturan Master Prompt DESIGN SYSTEM (kanal image + slide)
Dimuat oleh `gsp-image-prompt-specialist` saat proyek memakai design system GSP.
Sumber kebenaran token: [`skills/gsp/gsp-design-system-grill/references/master-design/`](../../../../registry-fleet/gsp-design-system-grill/references/master-design/)
(gsp-ds-sets.json mesin-baca; kartu per preset; GSP-DS-KELUARGA.md MR1–MR6; gsp-font-manifest.md).
Generator: SM-1 t_de708ae3 2026-09-01. Bahasa aturan ID, nama field/token EN (D-TA-6).

## 1. Urutan blok prompt WAJIB (tidak boleh dibalik/dilompati)
1. **identitas_set** - preset terpilih (default GENERAL; 12 preset: BNN BNPT BUSINESS CYBER MILITARY POLRI TNI-AD TNI-AL TNI-AU TEKNIK VISUAL KEMHAN) + mood/positioning dari kartu preset.
2. **palet** - salin pasangan `role → hex` dari preset di `gsp-ds-sets.json` + `usage_ratio` + label sumber tiap nilai (tercetak / terukur-piksel / estimasi-vision). Nilai `null` TIDAK_TERBACA dilarang diisi karangan.
3. **tipografi** - peran DISPLAY..CAPTION + ukuran/leading tercetak preset bila ada; tanpa angka tercetak → nyatakan PERAN saja (display-condensed / body-grotesk / data-tabular), bukan nama font karangan (D-TA-2, GAP-5).
4. **komposisi** - kanvas 1920×1080 (atau format lain dari kartu), grid 12 kolom margin 120 gutter 20–24 basis 8pt, pola split sah (FULL; 8/4, 6/6, 4/4/4), hierarki 70/20/10 satu focal point (MR3/MR5).
5. **larangan_dekorasi** - negatives-list keluarga MR6 ditempel utuh: cyberpunk/neon HUD, gaming aesthetics, camouflage/busy background, flashy saturated colors, heavy ornament, gradient/glow berlebihan, 3D chart, stock-hacker cliché.

## 2. Token-lock IR
IR-1..IR-7 skill ini DIISI dari preset paket - bukan dari nol, bukan dari intuisi.
Satu preset per deck/job; ganti preset = job baru (IR-6 exception protocol tetap berlaku).
Setiap angka yang muncul di prompt harus dapat ditelusuri ke kartu preset + halaman sumber (AC8).

## 3. Muatan slide (diserap dari blueprint langkah 8 - engine `productivity/powerpoint` READ-ONLY, keputusan controller D14)
Prompt slide wajib memuat blok tambahan:
- **footer**: nomor halaman `NN/TOTAL` kanan bawah + baris identitas sistem + kata kunci dipisah "•" (A5).
- **slot `classification_label`**: teks klasifikasi dari konteks proyek; label formal tidak ada di rak (MR4) - jangan mengarang skema sendiri.
- **EvidenceTag**: border putus-putus berisi SOURCE / REFERENCE / STATUS / REV (BNN hal 14) untuk klaim berbasis bukti.
- **ONE SLIDE ONE DECISION** (MR3): satu keputusan/focal point per slide; sisanya support quiet.
- **tema python-pptx**: saat prompt dieksekusi agen pemakai `powerpoint`, warna tema & font dipetakan dari preset (role→hex; display/body/data) - panduan eksekusi hidup di prompt, bukan di skill engine.

## 4. Kanal image
Hero memakai 4 treatment kanonik FULL FRAME / CONTAINED / CUTOUT / ENVIRONMENTAL (A7);
"imagery as evidence not decoration" (BNPT p7); ikon line-art stroke seragam (A9).

## 5. Gerbang sebelum serah
- [ ] 5 blok wajib berurutan lengkap
- [ ] semua nilai berasal dari preset + rujukan halaman; nol HEX lepas dari paket
- [ ] negatives-list tercantum; status = warna+label+ikon (MR3)
- [ ] budget baris kanal terpenuhi (slide ≥715, image ≥640 non-blank)

STATUS: complete
