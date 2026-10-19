---
record_type: knowledge_card
reference_id: REF-ELC-002
reference_confidence_level: R2
title: "ANSI-NETA ATS-2017"
domain: ELECTRICAL
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/ANSI-NETA
resume_path: 05_DOMAIN-KNOWLEDGE/ELECTRICAL/R2 - ANSI-NETA ATS-2017.md
---

# REF-ELC-002 — ANSI-NETA ATS-2017

**Tingkat keyakinan:** **R2** · **Status otoritas:** `ACTIVE_WITH_SCOPE_LIMITS`
**Laci sumber:** `R2/ANSI-NETA`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/ELECTRICAL/R2 - ANSI-NETA ATS-2017.md`

---

## 1. Yang dipasok rujukan ini

600 V → 100 MΩ · 5 kV → 1.500 MΩ · 15 kV → 5.000 MΩ. ΔT > 15 °C antar komponen serupa atau > 40 °C terhadap udara

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-1a..d (baris ΔT di seksi 'Yang dipasok' di atas): kartu menyalin hanya ambang 'perbaiki segera' dari Tabel 100.18. Tabel sumbernya EMPAT tingkat + kualifikator 'panduan tindakan, bukan batas mutlak' + syarat 'beban serupa' - utuh di resume `05_DOMAIN-KNOWLEDGE/ELECTRICAL/R2 - ANSI-NETA ATS-2017.md:79-92`. Jangan pakai cuplikan dua angka ini sebagai dasar klasifikasi temuan (register K-1a..d).

**Halaman jangkar:** PDF 223, 241, 246

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: angka-angka di atas dipasok tanpa caveat sumber. R2 mensyaratkan Tabel 100.1 berlaku 'bila tidak ada standar konsensus lain' dan spesifikasi pabrikan mendahului (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`). Kartu ini dikutip lapis hilir (gerbang rilis, BA); sertakan caveat setiap kali mengutip seksi 1.

## 2. Rumus / metode

```
Tabel 100.1 · koreksi suhu Tabel 100.14 · ΔT Tabel 100.18
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi

> **CATATAN DEFECT (NWSKILL-0923/D3-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/electrical-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-2: jawaban 'Ya' di atas baru menyebut satu syarat (adopsi kontrak + edisi). Sumber menambahkan syarat kedua: nilai berlaku hanya 'bila tidak ada standar konsensus lain' dan spesifikasi pabrikan mendahului (`R2 - ANSI-NETA ATS-2017.md:57-59,:149-150`). Register NWSKILL-0923 K-2.

## 4. Batas pemakaian — baca sebelum mengutip

**ATS = uji terima**, bukan pemeliharaan (MTS). **Bukan** ambang resistansi pembumian. Standar Amerika — bukan pengganti PUIL

## 5. Rantai jaminan

```
REQUIREMENT → REF-ELC-002 (R2) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/ELECTRICAL/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
