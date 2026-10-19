---
record_type: knowledge_card
reference_id: REF-BAT-001
reference_confidence_level: R3
title: "Battery Reference Book"
domain: POWER-BACKUP
authority_status: ACTIVE
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/BATTERY
resume_path: 05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3 - Battery Reference Book.md
---

# REF-BAT-001 — Battery Reference Book

**Tingkat keyakinan:** **R3** · **Status otoritas:** `ACTIVE`
**Laci sumber:** `R3/BATTERY`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R3 - Battery Reference Book.md`

---

## 1. Yang dipasok rujukan ini

Kerangka hitung kapasitas, rentang suhu timbal-asam tersegel −20…+50 °C

**Halaman jangkar:** PDF 104, 109, 117

## 2. Rumus / metode

```
Ah = I × t ÷ DoD, lalu koreksi C-rate
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis

## 4. Batas pemakaian — baca sebelum mengutip

DoD, umur siklus, dan kurva laju **wajib R4** — buku terbit 2000

## 5. Rantai jaminan

```
REQUIREMENT → REF-BAT-001 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
