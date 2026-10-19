---
id: gsp-dokumen-quality-validasi-selfcontainment
type: standar
title: "Panduan Kualitas Dokumen GSP — Validasi, Self-Containment & Agent Loading"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/document-quality-improvement-guide.md
halaman: Bagian 5-7, Lampiran
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: gsp-document-quality
domain: library
writer: gsp-librarian
tags: [gsp, dokumen, kualitas, standar, validasi, self-contained]
links: [gsp-dokumen-quality-kerangka-keputusan, gsp-dokumen-quality-deteksi-ai]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-document-quality/2026-08-25_gsp-dokumen-quality-validasi-selfcontainment.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Panduan Kualitas Dokumen GSP — Validasi, Self-Containment & Agent Loading

## Ringkasan
Checklist validasi pasca-penulisan (internal, eksternal, kelengkapan informasi, deteksi AI), aturan self-contained & penanganan referensi, matriks loading modul per agent, dan prinsip flexibility layer.

## Bukti (sumber: document-quality-improvement-guide.md, Bagian 5, 6, 7 + Lampiran)
- Internal Quality Checklist 10 poin untuk SEMUA dokumen: tipe sesuai tujuan, struktur sesuai tipe, kedalaman sesuai audiens, klaim ber-evidence, asumsi ditandai, tanpa kontradiksi, tanpa duplikasi info, istilah konsisten, heading/angka/referensi seragam, tanpa bahasa marketing/vague (Bagian 5.1).
- External Quality Checklist 6 poin WAJIB Tier 2+: self-contained, tanpa dependensi tersembunyi, Required References diringkas, Informational ditandai "for further reading", kesimpulan dapat dipahami dari dokumen saja, rekomendasi dapat diinterpretasi independen (Bagian 5.2).
- Information Completeness Check 6 poin: rekomendasi/requirement/keputusan/kеsimpulan berdiri sendiri, tanpa section bergantung pengetahuan internal yang tidak diungkap (Bagian 5.3).
- AI-tell detection 5.4: 10 indikator (paragraf rata-rata <4 kalimat sistemik, kalimat <25 kata, pembuka generik, tanpa angka, tanpa batasan, "dapat/mungkin" berlebih, EN di-italic, tanpa rekam jejak, transisi monoton, kesimpulan datar); 3+ HIGH → WAJIB revisi; C2 exclusion note: satu paragraf pendek disengaja / ritme bervariasi BUKAN AI-tell (Bagian 5.4–5.4.1).
- Required vs Informational References: Required WAJIB diringkas 2–5 kalimat dalam dokumen sebelum dicite; Informational cukup "for further reading" (Bagian 6.1, 6.4).
- Self-contained rule: pembaca TIDAK boleh butuh laporan/riset/catatan rapat/spec/wiki/source repo; hidden information prevention 3 pertanyaan (kesimpulan/rekomendasi/keputusan); golden rule: readers should never be forced to obtain another document (Bagian 6.2–6.5).
- Agent Loading Matrix: document-translator (E, D, H, 3.7–3.9), document-analyst (A, B, C, E, H, J), document-reader (C), document-writer (A, B, D, E, F, H, I, 3.7–3.9), document-reviewer (B, D, G, H, I, 4.7+5.5+6.6), document-controller (A, B, F, H, J), pm-writer (A, B, D, E, F, H, I, 3.7–3.9), content-research-writer (H, 3.7–3.9); semua agents: F (final step), H (creation/editing), I (formatting) (Bagian 7).
- Flexibility layer (Lampiran): paragraf tetap → RANGE 3–8 + VARIANCE; voice split 60/40 kaku → band 60–70%; heading "BAB X" → default per tipe konten; cover page → default formal; em dash >4/halaman → 1–2/halaman; precedent kanonik: "Jangan pernah memaksa template tetap" (Module D.4); fit-vs-novelty guardrail: pola familiar bukan slop bila pilihan paling jelas (Lampiran).

## Catatan
Kelas bukti sekunder. Standar normatif internal GSP; daftar agent (document-writer, pm-writer, dst) adalah peran dalam pipeline orkestrasi GSP.
