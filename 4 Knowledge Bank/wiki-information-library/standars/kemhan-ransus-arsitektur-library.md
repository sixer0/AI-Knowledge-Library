---
id: kemhan-ransus-arsitektur-library
type: standar
title: "Arsitektur Information Library Ransus Intelligent — direktori, taksonomi, template"
status: active
sumber: legacy-archive/KEMHAN -20260824T085136Z-1-001/KEMHAN/outputs/masterplan/01_library_architecture.md
halaman: seluruh berkas (718 baris); Directory Structure, Taxonomy Design, Template Definitions
tanggal_akses: 2026-08-25
kelas_bukti: sekunder
sensitif: tidak
perkara: kemhan-ransus-intelligent
tags: [kemhan-ransus-intelligent, arsitektur-library, taksonomi, template, library-architecture]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/kemhan-ransus-intelligent/2026-08-25_kemhan-ransus-arsitektur-library.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Arsitektur Information Library Ransus Intelligent — direktori, taksonomi, template

Arsitektur library mendukung Path A (Integrasi Data Internal) dari Dual Integration Framework. Hirarki: LIBRARY_INDEX.md + RELATIONSHIPS.md + VOCABULARY.md di root; research/ (8 analisis); masterplan/; domain/ (6 domain internal: dokumen, laporan, isu/kasus, geospasial, monitoring teknis, governance); intelligence_products/ (SITREP, brief, report, summary, briefing); tactical_devices/; templates/ (md/docx/xlsx); scripts/; archive/.

Taksonomi 8 kategori entitas: DOK (Document & Knowledge), RPT (Operational Report), ISS (Issue & Case), GEO (Geospatial & AOI), TEC (Technical Monitoring), GOV (Governance), INT (Intelligence Product), DEV (Tactical Device). Subtipe per kategori (mis. DOK-SOP/DOK-POL/DOK-REF/DOK-HIS; INT-SITREP/INT-BRIEF/INT-IREP/INT-SUMM/INT-OBRF; DEV-REG/DEV-CAP/DEV-INT/DEV-MNT).

8 tipe relationship: REFERENCES, DERIVED_FROM, SUPERSEDES, RELATED_TO, VALIDATES, ASSIGNED_TO, CONTAINS, REQUIRES. Setiap entitas wajib YAML frontmatter: entity_id, title, category, type, status, classification, version, created, updated, tags, summary, ai_queryable; conditional: author/reviewer/approved_by, relationships; classification levels: INTERNAL, CONFIDENTIAL, RESTRICTED, TOP_SECRET.

Template MD: SOP (purpose/scope/prerequisites/procedure/roles/references/revision), Intelligence Product (exec summary/situation/analysis/recommendations/source citations/confidence), Mission Log (objectives/timeline/sensor activity/alerts/issues). Format: MD primary (AI-queryable, git-friendly), DOCX formal distribution, XLSX structured data.

LIBRARY_INDEX.md = entry point Agent Librarian (auto-generated + manual review); RELATIONSHIPS.md = peta cross-entity (REFERENCES/DERIVED_FROM/SUPERSEDES/RELATED_TO/VALIDATES). Flag vocabulary 5 kategori: Document Status, Alert/Issue, Classification, AI Confidence, Capability Governance.


## Domain & project
- Domain registry: defense-intel (kemhan/ransus — mobile command center, electronic warfare)
- Project: kemhan-ransus-intelligent

## Catatan analisa
- Skor: 5 (kepentingan x keandalan — analisa konten folder legacy KEMHAN).
- Sumber: `legacy-archive/KEMHAN -20260824T085136Z-1-001/KEMHAN/outputs/masterplan/01_library_architecture.md` (seluruh berkas; §1 direktori, §2 taksonomi, §3 template, §4 flag vocabulary).
