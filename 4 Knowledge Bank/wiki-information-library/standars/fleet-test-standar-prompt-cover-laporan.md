---
id: fleet-test-standar-prompt-cover-laporan
type: standar
title: "Prompt set cover slide laporan GSP - 3 gaya (korporat formal, modern vibrant, minimalis elegan)"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-image-prompt-specialist/prompts.md
halaman: hal. 1-5 (Ringkasan Prompt 1-3; Perbedaan Utama; Catatan Teknis)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [image-prompt, cover, design-system, prompt, standar, slide]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-standar-prompt-cover-laporan.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Prompt set cover slide laporan GSP - 3 gaya (korporat formal, modern vibrant, minimalis elegan)


Prompt set 3 gaya cover slide "Laporan Kinerja Q3 2026" GSP [sumber — prompts.md hal. 1-5; prompt-cover-korporat-formal.md; prompt-cover-modern-vibrant.md; prompt-cover-minimalis-elegan.md]:
1) Korporat formal — navy #1A2744 solid (gradient ke #0F1A30), gold #C8A951, Playfair Display Bold, diamond accent, golden ratio layout.
2) Modern vibrant — navy base 60% + gradient mesh overlay (ungu #6B3FA0, magenta #E84393, teal #20C997) max 25% opacity, glassmorphism panel, badge "Q3" teal solid.
3) Minimalis elegan — warm white #F5F3EF solid, Swiss International Style, Playfair Regular (bukan Bold!), satu garis emas 1px + satu diamond 8x8, max 2 chromatic colors.

Token master konsisten lintas gaya: COLOR.PRIMARY #1A2744, SECONDARY #2E5090, ACCENT #C8A951, SURFACE #F5F3EF, TEXT_PRIMARY #FFFFFF/#1A1A1A, TEXT_SECONDARY #B0A89A.
Format: 1920x1080 px, 16:9, PNG 24-bit sRGB, grid 12 kolom / gutter 24 px.

Kualitas: struktur 11 seksi; self-check IR-1..IR-7 PASS; sibling variance (J.4) — ketiga prompt tidak identik; data spesifik (tahun 2026, hex, koordinat pixel, ukuran font) terpenuhi.
Eksekusi: Midjourney + --v 6 --ar 16:9 --style raw; DALL-E 3 prompt asli; Stable Diffusion + negative prompt standar anti-AI.

Kelas bukti: primer (file prompt itu sendiri).
