---
record_type: knowledge_card
reference_id: REF-PWR-001
reference_confidence_level: R3
title: "Diesel Generator Handbook"
domain: POWER-BACKUP
authority_status: ACTIVE
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/GENSET
resume_path: 05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3 - Diesel Generator Handbook.md
---

# REF-PWR-001 — Diesel Generator Handbook

**Tingkat keyakinan:** **R3** · **Status otoritas:** `ACTIVE`
**Laci sumber:** `R3/GENSET`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3 - Diesel Generator Handbook.md`

---

## 1. Yang dipasok rujukan ini

Kerangka derating lokasi, kelas rating genset

**Halaman jangkar:** PDF 40–42, 136

## 2. Rumus / metode

```
kVA = (puncak ÷ PF) × derating × margin
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis

## 4. Batas pemakaian — baca sebelum mengutip

⚠ **Bab 11 hilang** (± 55 hal). Faktor derating nyata **wajib R4**

## 5. Rantai jaminan

```
REQUIREMENT → REF-PWR-001 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
