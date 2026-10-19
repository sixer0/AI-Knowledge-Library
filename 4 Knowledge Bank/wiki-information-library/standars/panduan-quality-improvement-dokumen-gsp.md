---
id: panduan-quality-improvement-dokumen-gsp
type: standar
title: "Panduan Quality Improvement Dokumen GSP — Adaptasi Document Quality Standards v1.3 untuk Orkestrasi"
status: active
sumber: legacy-archive/outputs-20260824T085259Z-1-001/outputs/document-quality-improvement-guide.md
halaman: §1–Lampiran (942 baris, 7 bagian)
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: gsp-document-quality
domain: digital
writer: gsp-librarian
tags: [gsp, document-quality, standar, penulisan, anti-ai, claude-vibes, orkestrasi]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/gsp-document-quality/2026-08-25_panduan-quality-improvement-dokumen-gsp.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Panduan Quality Improvement Dokumen GSP — Adaptasi Document Quality Standards v1.3 untuk Orkestrasi

## Ringkasan
Dokumen internal GSP (disusun 2026-08-04, revisi integrasi claude-vibes 2026-08-04,
942 baris) yang mengadaptasi **Module A–J Document Quality Standards v1.3** menjadi
panduan praktis & actionable untuk semua agent dokumen GSP orchestration
(document-translator/analyst/reader/writer/reviewer/controller, pm-writer,
content-research-writer). Sejak revisi 2026-08-04 juga mengintegrasikan lapisan
deteksi AI dari skill `claude-vibes/ai-writing-detection` (vocabulary tell,
structural pattern, model fingerprint, false-positive prevention).

## Bukti (sumber: document-quality-improvement-guide.md)
- **Bagian 1 — Quick Decision Framework** (§1.1–§1.3): decision tree 8 tipe dokumen
  (Research, Information Mapping, Business, Technical, Operational, Planning,
  Analytical, Educational; default General Report); matrix audiens→kedalaman
  (Executive 1–2 hal, Management 5–10, Engineer 10–20, Developer 15–30,
  Researcher 20–50, Customer 3–10, General public 2–5); Independence Tier Checker
  (Tier 1 Internal / 2 External / 3 Customer Delivery).
- **Bagian 2 — Pre-Writing Checklist** (§2.1–§2.3): lima checkpoint wajib sebelum
  delegasi pembuatan dokumen; template spec analysis; penentuan audiens+depth.
- **Bagian 3 — Writing Quality Standards** (§3.1–§3.10): daftar hitam frasa
  AI-typical (mis. "Di era digital/modern ini", "Tidak dapat dipungkinkan bahwa",
  "Dapat disimpulkan bahwa" → klaim langsung) + alternatif; pembuka/penutup
  dilarang; rhythm kalimat (rata-rata 30–45 kata, min 25) & paragraf; active vs
  passive voice; pola "Bukan X, Melainkan Y"; confidence labeling; **claude-vibes
  layer** §3.7 (15+ high-signal vocabulary tell, overused phrases, structural red
  flags), §3.8 model-specific fingerprint, §3.9 false-positive prevention;
  spesifisitas wajib §3.10.
- **Bagian 4 — Formatting Standards** (§4.1–§4.7): number format Indonesia
  (currency, exact vs approximate); heading hierarchy; table formatting;
  cross-reference format (internal/external/citation); cover page template;
  DOCX style map; formatting red flags.
- **Bagian 5 — Post-Writing Validation** (§5.1–§5.6): Internal Quality Checklist
  (10 poin, semua dokumen); External Quality Checklist (6 poin, Tier 2+);
  Information Completeness Check (6 poin); AI-Tell Detection Checklist (10 poin);
  **9-Layer AI-Tell Detection Checklist** §5.5 (metodologi claude-vibes — Layer 1
  Technical Artifacts → FAIL otomatis; Layer 2 Vocabulary; Layer 3 Structural;
  Layer 4 Content; Layer 5 Citation; Layer 6 Formatting; Layer 7 Stylometric;
  Layer 8 Coherence; Layer 9 Confidence Scoring); cara pakai + format pelaporan
  (semua checklist 5.1–5.3 wajib 100% PASS sebelum dokumen selesai).
- **Bagian 6 — Reference & Self-Containment** (§6.1–§6.6): Required vs
  Informational References; Self-Contained Document Rule (pembaca TIDAK boleh
  butuh akses dokumen internal lain); hidden information prevention; citation
  red flags.
- **Bagian 7 — Agent Loading Matrix** (§7): modul DQS yang harus di-load per
  agent (document-writer: A,B,D,E,F,H,I + 3.7–3.9; document-reviewer:
  B,D,G,H,I + 4.7+5.5+6.6; dst.); rekomendasi load di awal sesi.
- **Lampiran — Flexibility Layer** (Lampiran): pelunakan aturan tetap jadi
  range+variance (paragraf 3–8 kalimat; voice band 60–70% active; kuota "bukan X
  melainkan Y" jadi panduan; em dash 1–2/halaman); precedent kanonik Module D.4
  "Jangan pernah memaksa template tetap"; fit-vs-novelty guardrail; catatan
  integrasi claude-vibes (termometer reviewer, bukan pisau pemotong naskah).

## Keterkaitan
- Adaptasi dari standar sumber: skill `gsp-document-quality-standards`
  (Document Quality Standards v1.3, Module A–K) — unit ini adalah turunan praktis
  versi orkestrasi GSP.
- 3 render file identik konten: `document-quality-improvement-guide.md`,
  `document-quality-improvement-guide(1).md` (byte-identical sha256 805c16a1...),
  `document-quality-improvement-guide.docx` (render Word, ekstraksi teks cocok).
- Non-sensitif: dokumen operasional internal tanpa klasifikasi; tidak memuat data
  klien/anggaran/defense.
