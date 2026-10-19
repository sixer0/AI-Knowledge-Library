---
id: igr-batas-teknis-image-model
type: fakta
title: "IGR-CCD-003 — Batas teknis image model: ≤18 elemen, ~400 kata teks, anti-crop, spelling drift, grounding untuk cegah fakta fiktif"
status: active
domain: digital
writer: gsp-librarian
created: 2026-08-25
sumber: legacy-archive/Research Agentic Operating System-20260824T084946Z-1-001/Research Agentic Operating System/Maximizing-AI-Image-Output-Research.docx
halaman: Bab 5 (Real Technical Limits)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: riset-sistem-ai-gsp-kam
tags: [image-gen, batas-teknis, density]
penulis: gsp-librarian
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi, batch M1b). Alasan: seluruh angka terverifikasi terhadap Maximizing-AI-Image-Output-Research.docx Bab 5 \"The Real Technical Limits (verified)\": object binding ~15-20 objek/element sebelum swap/merge/drop dengan design rule <=~18 elemen berlabel; in-image text ~99 persen akurasi hingga ~400 kata; catatan cropping poster dikutip verbatim termasuk atribusi \"OpenAI's own note\" dan arahan anti-crop + margin; spelling drift diperbaiki via in-painting/targeted text edit bukan reroll; caps V7.1 (<=18 label / <=10 angka / <=6 zona) dikonfirmasi riset; klaim \"~55 label yang keliru\" cocok dengan pengakuan sumber \"including my own wrong ~55-label claim\"; ID dokumen IGR-CCD-003/GSP/PT/VII/2026 hadir; basis Juli 2026 cocok kolom \"Verified behaviour (July 2026)\". YAML kelas-I5 lulus, title==H1, satu baris status, sensitif tidak. Dedup: entri wiki/vault igr-lanskap-model-image dan igr-enam-teknik-senior-brief membahas faset berbeda (lanskap model; teknik brief) dari korpus yang sama - saling melengkapi, bukan duplikat; links internal folder wajar. || Rekomendasi: tidak ada perubahan wajib. Renik opsional: tambahkan rujukan sub-bab tabel (Bab 5 baris Object binding / In-image text / Poster cropping / Spelling drift) agar telusur halaman lebih presisi. Riwayat: catatan_verifikasi lama (verdict awal perlu_revisi 2026-08-25, direvisi gsp-librarian Wave B 2026-08-25, status dikembalikan ke usulan) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/igr-batas-teknis-image-model.md
catatan_keputusan: "dipromosikan: batch M1b paruh B terverifikasi custodian (C-M1b-verdict.md)"
---

# IGR-CCD-003 — Batas teknis image model: ≤18 elemen, ~400 kata teks, anti-crop, spelling drift, grounding untuk cegah fakta fiktif

Batasan terukur pengganti seluruh tebakan sebelumnya (termasuk klaim ~55 label yang keliru). [R — Maximizing-AI-Image-Output-Research.docx, Bab 5 (Real Technical Limits)]

Bukti (angka berujukan):
- Object binding: model top andal ~15-20 objek/element sebelum swap/merge/drop → desain ≤ ~18 elemen berlabel per gambar (IGR-CCD-003, Bab 5).
- In-image text: SOTA menjaga ~99% akurasi hingga ~400 kata total → jaga teks <400 kata, label lebih sedikit & besar (IGR-CCD-003, Bab 5).
- Poster cropping: model 'occasionally crop longer images, like posters, too tightly, especially near the bottom' (catatan resmi OpenAI) → anti-crop directive + margin (IGR-CCD-003, Bab 5).
- Spelling drift: perbaiki via in-painting/targeted text edit, bukan reroll (IGR-CCD-003, Bab 5).
- V7.1 caps (≤18 label/≤10 angka/≤6 zona) dikonfirmasi benar oleh riset independen ini (IGR-CCD-003, Bab 5).

Asumsi/tanda: primer (riset web-verified Juli 2026; tidak ada asersi dari ingatan).
