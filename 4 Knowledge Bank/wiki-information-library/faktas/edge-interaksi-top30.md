---
id: edge-interaksi-top30
type: fakta
title: Edge Interaksi Skill Terkuat (Top 30)
status: active
sumber: docs/2026_08_24_kajian_ekosistem/matriks_pemetaan_skill.md
halaman: bab Edge interaksi terkuat (top 30)
tanggal_akses: 2026-08-25
kelas_bukti: sintesis
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: digital
writer: gsp-librarian
tags: [interaksi, skill, edge, graf]
links: [bagan-interaksi-218-node-69-edge]
penulis: dashboard
diajukan: 2026-08-25
catatan_verifikasi: "Verdict: terverifikasi (custodian 2026-09-03, challenge penuh 7 dimensi). Alasan: Setiap bobot yang dikutip dicocokkan dengan dua sumber sekaligus (tabel matriks_pemetaan_skill.md baris 154-187 = tepat 30 baris, dan interaksi_skill.json): claude-design <-> popular-web-designs 6, <-> design-md 6, <-> sketch 2; gsp-kanban-contract <-> gsp-orchestrator-worker gsp-ref 6; gsp-fleet-profile-operations <-> gsp-orchestration-execution 5; gsp-orchestration-execution <-> gsp-orchestrator-worker 4; gsp-fleet-profile-operations <-> hermes-web-search-stack 3; document-to-action-items <-> ocr-and-documents 3 / pdf 2 / docx 2; ocr-and-documents <-> pdf 3; email-inbox-triage <-> himalaya / google-workspace / weekly-review-planning 2/2/2; meeting-action-items <-> teams-meeting-pipeline 2; blogwatcher <-> competitor-news-monitor 2; gsp-document-vision-ocr <-> gsp-image-prompt-specialist 2, gsp-library-bulk-approval <-> gsp-library-workflow 2, gsp-document-vision-ocr <-> gsp-proposal-deepdive 2; ekor panjang bobot 1 (apple-notes<->obsidian, hermes-home-migration<->to-prd, architecture-diagram<->excalidraw, ascii-art/ascii-video/p5js<->pretext). Tidak ada bobot yang menyimpang. Tidak ada dimensi yang gagal. Body menyebut 'Pola dominan' sehingga tidak mengklaim menyalin 30 baris penuh - jujur. Kelas bukti sintesis tepat (turunan dari JSON + matriks). Definisi bobot di seksi Catatan konsisten dengan metodologi contract doc. || Rekomendasi: Siap dipromosikan. Sunting status `terverifikasi` -> `ditinjau` sebelum promote (aturan I1). Pertahankan tautan ke objek bagan-interaksi agar definisi bobot tidak terbaca menggantung. || Riwayat: catatan_verifikasi sebelumnya (custodian 2026-08-25 perlu_revisi, direvisi librarian Wave B fix-h1) dipertahankan sebagai riwayat."
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/edge-interaksi-top30.md
catatan_keputusan: "dipromosikan: IL-INGEST-01 B1a pilot: verdict custodian terverifikasi (C-B1a-verdict.md), cek YAML kelas-I5 lulus, non-sensitif non-dosir"
---

# Edge Interaksi Skill Terkuat (Top 30)

Edge interaksi antar skill terkuat — top 30 (matriks_pemetaan_skill.md, bab
"Edge interaksi terkuat (top 30)"; data interaksi_skill.json).

Pola dominan:
- **claude-design ↔ popular-web-designs / design-md / sketch** (mention,
  bobot 6/6/2) — cluster desain web kreatif.
- **gsp-kanban-contract ↔ gsp-orchestrator-worker** (gsp-ref, 6) — pasangan
  orkestrasi inti.
- **gsp-fleet-profile-operations ↔ gsp-orchestration-execution** (gsp-ref,
  mention, 5) — operasi fleet ↔ jejak orkestrasi.
- **gsp-orchestration-execution ↔ gsp-orchestrator-worker** (4) — workflow inti.
- **gsp-fleet-profile-operations ↔ hermes-web-search-stack** (mention, 3).
- **document-to-action-items ↔ ocr-and-documents / pdf / docx** (3/2/2).
- **ocr-and-documents ↔ pdf** (3); **email-inbox-triage ↔ himalaya /
  google-workspace / weekly-review-planning** (2/2/2); **meeting-action-items ↔
  teams-meeting-pipeline** (2); **blogwatcher ↔ competitor-news-monitor** (2).
- **GSP library/intel:** gsp-document-vision-ocr ↔ gsp-image-prompt-specialist
  (2), gsp-library-bulk-approval ↔ gsp-library-workflow (2),
  gsp-document-vision-ocr ↔ gsp-proposal-deepdive (2).
- Ekor panjang (1): apple-notes↔obsidian, hermes-home-migration↔to-prd,
  architecture-diagram↔excalidraw, ascii-art/video/p5js↔pretext, dll.

Sumber: `matriks_pemetaan_skill.md` bab Edge interaksi terkuat (top 30);
`interaksi_skill.json`.

# Bukti

- Edge dihitung dari referensi silang body SKILL.md & frontmatter: related /
  mention / gsp-ref (contract doc 2026-08-24-bagan-matriks-skill.md).

# Catatan

- Bobot = jumlah konteks referensi (mention/gsp-ref) antar dua skill;
  shared-context (ko-pemakaian profil) dilacak di matriks, bukan di edge ini.
