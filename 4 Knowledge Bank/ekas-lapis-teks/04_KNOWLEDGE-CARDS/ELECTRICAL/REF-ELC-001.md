---
record_type: knowledge_card
reference_id: REF-ELC-001
reference_confidence_level: R3
title: "Electrical Power Equipment Maintenance and Testing"
domain: ELECTRICAL
authority_status: ACTIVE
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/ELECTRICAL
resume_path: 05_DOMAIN-KNOWLEDGE/ELECTRICAL/R3 - Electrical Power Equipment Maintenance and Testing.md
---

# REF-ELC-001 — Electrical Power Equipment Maintenance and Testing

**Tingkat keyakinan:** **R3** · **Status otoritas:** `ACTIVE`
**Laci sumber:** `R3/ELECTRICAL`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/ELECTRICAL/R3 - Electrical Power Equipment Maintenance and Testing.md`

---

## 1. Yang dipasok rujukan ini

Empat metode ukur isolasi, batas tegangan uji ≤ 75% terima / ≤ 60% pabrik

**Halaman jangkar:** PDF 142, 144, 145

## 2. Rumus / metode

```
PI = R₁₀mnt ÷ R₁mnt (< 1) · DAR = R₆₀dtk ÷ R₃₀dtk (< 1,25)
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis

## 4. Batas pemakaian — baca sebelum mengutip

Memberi **rasio dan metode**, bukan ambang MΩ mutlak

## 5. Rantai jaminan

```
REQUIREMENT → REF-ELC-001 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/ELECTRICAL/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
