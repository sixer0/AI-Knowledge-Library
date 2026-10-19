---
record_type: knowledge_card
reference_id: REF-BAT-002
reference_confidence_level: R2
title: "IEEE 1188-2005 dan IEC 62485-2"
domain: POWER-BACKUP
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEEE
resume_path: 05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R2 - IEEE 1188-2005 dan IEC 62485-2.md
---

# REF-BAT-002 — IEEE 1188-2005 dan IEC 62485-2

**Tingkat keyakinan:** **R2** · **Status otoritas:** `ACTIVE_WITH_SCOPE_LIMITS`
**Laci sumber:** `R2/IEEE`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/R2 - IEEE 1188-2005 dan IEC 62485-2.md`

---

## 1. Yang dipasok rujukan ini

Ambang ganti baterai < 90% rating · turun > 10% · 85% umur layan. Ventilasi ruang baterai

**Halaman jangkar:** PDF 15, 17, 19, 21

## 2. Rumus / metode

```
Q = v × q × s × n × I_gas × C_rt × 10⁻³ (m³/jam)
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi

## 4. Batas pemakaian — baca sebelum mengutip

Hanya **VRLA**. Baterai vented → IEEE 450, belum ada di rak. Derating ventilasi tidak diperbolehkan

## 5. Rantai jaminan

```
REQUIREMENT → REF-BAT-002 (R2) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/POWER-BACKUP/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
