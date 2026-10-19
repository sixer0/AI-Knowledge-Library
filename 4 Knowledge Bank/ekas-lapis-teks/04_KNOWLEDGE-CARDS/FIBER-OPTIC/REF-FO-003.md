---
record_type: knowledge_card
reference_id: REF-FO-003
reference_confidence_level: R2
title: "IEC 61280-4-2"
domain: FIBER-OPTIC
authority_status: ACTIVE_WITH_SCOPE_LIMITS
vault_path: 03_SOURCE-VAULT/R2_INTERNATIONAL-STANDARDS/IEC
resume_path: 05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/R2 - IEC 61280-4-2.md
---

# REF-FO-003 — IEC 61280-4-2

**Tingkat keyakinan:** **R2** · **Status otoritas:** `ACTIVE_WITH_SCOPE_LIMITS`
**Laci sumber:** `R2/IEC`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/R2 - IEC 61280-4-2.md`

---

## 1. Yang dipasok rujukan ini

Empat metode: one-cord · three-cord · two-cord · OTDR. RTM penyelesai perselisihan. ORL Annex E Method A

**Halaman jangkar:** PDF 14, 17, 20, 43

## 2. Rumus / metode

```
Reflectance = 10 × log₁₀ (Pr ÷ Pin)
```

> **CATATAN DEFECT (NWSKILL-0923/D2-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/fiber-optic-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-9: rumus di atas ditulis tanpa pembatas cakupan. Sumbernya membatasi definisi reflektansi pada KOMPONEN DISKRET DALAM KABEL (`R2 - IEC 61280-4-2.md:55-58`, definisi PDF 14), dan tidak ada satu pun lapis teks yang menjelaskan hubungan arah tanda antara reflectance (dB negatif) dan ORL (dB positif) padahal keduanya dijanjikan bersama di `RANTAI-JAMINAN.md:13,78`. Risiko salah pakai nyata: rumus komponen dipakai untuk ORL jalur. Kelas 'rujukan melebihi isi'. Rekosiliasi butuh PDF IEC (definisi 3.1.7).

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Ya**, bila standar diadopsi kontrak dan edisinya tervalidasi

## 4. Batas pemakaian — baca sebelum mengutip

**Singlemode saja.** Multimode → IEC 61280-4-1, belum ada. Tidak memberi angka ambang lulus

## 5. Rantai jaminan

```
REQUIREMENT → REF-FO-003 (R2) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/FIBER-OPTIC/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
