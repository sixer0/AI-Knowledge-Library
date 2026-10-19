---
record_type: knowledge_card
reference_id: REF-FO-001
reference_confidence_level: R3
title: "FOA Reference Guide to Fiber Optics"
domain: FIBER-OPTIC
authority_status: ACTIVE
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/FIBER-OPTIC
resume_path: 05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/R3 - FOA Reference Guide to Fiber Optics.md
---

# REF-FO-001 — FOA Reference Guide to Fiber Optics

**Tingkat keyakinan:** **R3** · **Status otoritas:** `ACTIVE`
**Laci sumber:** `R3/FIBER-OPTIC`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/R3 - FOA Reference Guide to Fiber Optics.md`

---

## 1. Yang dipasok rujukan ini

Loss budget, batas TIA-568 0,75 dB/konektor, 1 dB/km SM premises · 0,5 dB/km OSP, ambang = kolom terburuk

**Halaman jangkar:** PDF 98, 129, 145

## 2. Rumus / metode

```
rugi = (km × dB/km) + (n_konektor × 0,75) + (n_sambungan × rugi)
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis

## 4. Batas pemakaian — baca sebelum mengutip

OTDR **bukan pengganti** uji rugi OLTS

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-11: kalimat di atas hanya satu sisi. IEC 61280-4-2 (R2) PDF 17 mencantumkan metode OTDR sebagai salah satu empat metode uji redaman (`R2 - IEC 61280-4-2.md:30-35`); ketegangan R2 vs R3 belum teradjudikasi di rak (butir K-11 studi NWSKILL-0923). Jangan meratakan kedua sisi saat mengutip kartu ini.

## 5. Rantai jaminan

```
REQUIREMENT → REF-FO-001 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
