---
id: fleet-test-pelajaran-design-system-css
type: pelajaran
title: "Pelajaran design system: audit CSS - token, spacing, tipografi, kontras WCAG"
status: active
sumber: docs/2026-08-24_fleet_test/gsp-design-system-specialist/design_review.md
halaman: hal. 1-6 (Skor per Prinsip; Ringkasan Skor)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: fleet-test-2026-08-24
domain: digital
writer: gsp-librarian
tags: [design-system, css, wcag, aksesibilitas, token, pelajaran, ui]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/fleet-test-2026-08-24/2026-08-25_fleet-test-pelajaran-design-system-css.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---
# Pelajaran design system: audit CSS - token, spacing, tipografi, kontras WCAG


Audit 5 selector CSS (sample_style.css: .card, .card-title, .btn-primary, .btn-primary:hover, .text-muted) terhadap 4 prinsip design system [sumber — design_review.md hal. 1-6]:
Skor total 2.0/4 = LEMAR (tiap prinsip 0.5/1). Kode belum siap dipakai di proyek berbasis design system tanpa refactoring.

1) Token & konvensi warna FAIL: hex literal langsung (#2563eb -> #1d4ed8 hover) tanpa CSS custom properties; selector berorientasi posisi, bukan semantik.
2) Spacing konsistensi WARN: padding 10px/18px pecah kelipatan 4; card radius 8px vs button 6px tanpa token.
3) Hierarchy tipografi FAIL: 3 ukuran font (18/16/13px) tanpa skala rasio (1.125-1.5); tanpa line-height dan font-family eksplisit.
4) Aksesibilitas kontras FAIL: .text-muted #6b7280 di #fff ≈ 2.95:1 GAGAL WCAG AA (4.5:1); .btn-primary ≈ 4.6:1 lolos AA gagal AAA; .card-title ≈ 15.3:1 lolos AA+AAA.

Rekomendasi: definisikan :root tokens (--color-*, --space-xs..xl, --radius-*, --text-*, line-height); ganti hex literal ke var(--*); fix .text-muted (gelapkan #374151 ≈ 6.3:1 ATAU perbesar >= 18px); tambah :focus-visible ring; min-height 44px touch target; pertimbangkan prefers-color-scheme: dark.

Prioritas: TERTINGGI .text-muted (2.95:1), TINGGI focus state .btn-primary, RENDAH button menuju AAA.
Kelas bukti: primer (audit langsung file CSS; kontras dihitung rumus luminansi relatif W3C WCAG 2.x).
