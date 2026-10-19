---
record_type: knowledge_card
reference_id: REF-VSS-002
reference_confidence_level: R2
title: "BS EN 62676-1-2"
domain: VIDEO-SURVEILLANCE
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/EN-BS
resume_path: 05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md
---

# REF-VSS-002 — BS EN 62676-1-2

**Tingkat keyakinan:** **R2** · **Status otoritas:** `ACTIVE_WITH_SCOPE_LIMITS`
**Laci sumber:** `R2/EN-BS`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/R2 - BS EN 62676-1-2.md`

---

## 1. Yang dipasok rujukan ini

Persyaratan unjuk kerja transmisi video per security grade

**Halaman jangkar:** PDF 34

## 2. Rumus / metode

```
Tabel 7 — waktu deteksi hilang sinyal 8 / 4 / 2 detik
```

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi

## 4. Batas pemakaian — baca sebelum mengutip

**Bukan ONVIF.** Interoperabilitas perangkat tidak tercakup

**Known-defect VSSKB-0923 (2026-09-23):** angka Tabel 7 8/4/2 detik di atas berkontradiksi dengan bentuk empat nilai 8/4/4/2 pada lapisan teks lain (`R2 - BS EN 62676-1-2.md:45-48`, `KATALOG-RUMUS.md:474-477`); pemetaan per-grade BELUM TERKONFIRMASI terhadap geometri PDF primer (ukur gsp-custodian 2026-09-23). Kartu rujukan ini karena itu TIDAK boleh berdiri sendiri sebagai sandaran ambang terima untuk butir waktu deteksi sampai rekonsiliasi dengan publikasi resmi BSI/IEC dilakukan manusia. Rujukan lengkap: `wiki/catatans/vss-korpus-ekas-0923.md` sub-seksi 'Batas angka Tabel 7'.

## 5. Rantai jaminan

```
REQUIREMENT → REF-VSS-002 (R2) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/VIDEO-SURVEILLANCE/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
