# Komponen CSS kanonik GSP DS + gerbang render
Carrier aturan (D-TA-7 pointer-only): dokumen ini menunjuk paket token; nilai HANYA dibaca dari
[`skills/gsp/gsp-design-system-grill/references/master-design/gsp-ds-sets.json`](../../../../registry-fleet/gsp-design-system-grill/references/master-design/gsp-ds-sets.json) + kartu preset.
Muatan ini menyerap blueprint langkah 10 (engine `creative/claude-design` READ-ONLY, keputusan D14).
Generator: SM-1 t_de708ae3 2026-09-01.

## 1. Blok token (`:root`) - bentuk baku
```css
/* preset: <SLUG> - token dari gsp-ds-sets.json, jangan hardcode hex di tempat lain */
:root{
  --gsp-bg: <role bg>;            --gsp-surface: <role surface>;
  --gsp-text-primary: <...>;      --gsp-text-secondary: <...>;
  --gsp-primary: <...>;           --gsp-secondary: <...>;
  --gsp-accent: <role accent_single>;            /* ≤10% pemakaian (MR2) */
  --gsp-positive: <...>; --gsp-warning: <...>; --gsp-critical: <...>; --gsp-information: <...>;
  --gsp-space-1:8px; --gsp-space-2:16px; --gsp-space-3:24px; --gsp-space-4:32px;
  --gsp-space-6:48px; --gsp-space-8:64px;   /* basis 8pt (MR5) */
}
```
Aturan: SELURUH stylesheet merujuk var(); nol HEX lepas di luar blok token (AC5). Nama peran = dari JSON.

## 2. Kelas tipografi 9 peran (MR5)
`.t-display .t-h1 .t-h2 .t-h3 .t-lead .t-body .t-data .t-label .t-caption` - ukuran/leading dari kartu
preset bila tercetak (mis. Cyber p6 72/88→11/16); `.t-data{font-variant-numeric:tabular-nums}`;
display condensed ALL-CAPS, body grotesk; keluarga via manifest/pengganti sistem (D-TA-2/GAP-5).

## 3. Grid
12 kolom, gap 20–24px, padding luar 120px (skala penuh) / proporsional viewport kecil; breakpoint menurunkan
margin tapi mempertahankan rasio & urutan hierarki (A1).

## 4. Komponen kanonik (bahasa grafis 8 elemen, A8/MR6)
| komponen | spesifikasi | sumber |
|---|---|---|
| `.gsp-pill-classification` | pil label klasifikasi; warna netral + teks (status TIDAK pernah hanya warna, MR3); sticky di header kanal laporan | slot MR4 |
| `.gsp-strip-stats` | strip statistik cover: angka `.t-data` tabular + label caps kecil | BNN/Polri/Kemhan |
| `.gsp-evidence-tag` | border putus-putus: SOURCE / REFERENCE / STATUS / REV | BNN hal 14 |
| `.gsp-prov-icon` | ikon provenans nilai: ■ terukur ◈ diturunkan ◇ pemasok △ asumsi (+ tooltip sumber) | SPEC aparatur MR4 |
| `.gsp-page-number` | `NN/TOTAL` pojok kanan bawah (layar & print) | A5 |
| `.gsp-kicker` | header "NN / NAMA SISTEM" + garis aksen pendek ≤64px | A5/A8 |

## 5. Gerbang render-lokal sebelum menyerahkan (diserap dari langkah 10)
- [ ] render lokal (buka/parse HTML) - tidak ada elemen overflow/tumpang tindih
- [ ] `grep` HEX di luar blok `:root` = 0 (AC5)
- [ ] status memakai warna+label+ikon; aksen ≤10% area
- [ ] negatives-list MR6 nihil (no neon HUD/glassmorphism/3D chart)
- [ ] kontras teks ≥ 4.5:1 pada preset terang (satu-satunya angka rak: Polri hal 4)

STATUS: complete
