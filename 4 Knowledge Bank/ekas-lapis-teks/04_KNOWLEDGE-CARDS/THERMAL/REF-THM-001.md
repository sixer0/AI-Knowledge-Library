---
record_type: knowledge_card
reference_id: REF-THM-001
reference_confidence_level: R3
title: "Infrared Thermal Imaging"
domain: THERMAL
authority_status: ACTIVE
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/THERMAL
resume_path: 05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md
---

# REF-THM-001 — Infrared Thermal Imaging

**Tingkat keyakinan:** **R3** · **Status otoritas:** `ACTIVE`
**Laci sumber:** `R3/THERMAL`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md`

---

## 1. Yang dipasok rujukan ini

Delapan parameter wajib kamera, aturan IFOV

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-9 (seksi 'Yang dipasok' di atas): kartu MENYEMPITKAN cakupan buku. Resume Vollmer juga memasok fisika emisivitas (Bab 1, PDF 22), pantulan dan Fresnel (PDF 33, 250), definisi NETD/resolusi/IFOV (PDF 128), SWIR (PDF 467), bangunan (PDF 497), deteksi gas (PDF 580), industri termasuk panel listrik (PDF 663) - lihat `05_DOMAIN-KNOWLEDGE/THERMAL/R3 - Infrared Thermal Imaging.md`. Halaman jangkar kartu (PDF 25, 128) ikut sempit. Label 'Laci sumber: R3/THERMAL' di kepala kartu = tingkat, bukan path (path benar sudah ada di frontmatter vault_path; register K-5).

**Halaman jangkar:** PDF 25, 128

## 2. Rumus / metode

```
ΔT_serupa · ΔT_udara
```

> **CATATAN DEFECT (NWSKILL-0923/D4-FIXx, 2026-09-24):** known-defect dari studi NWSKILL-0923 (register: docs/2026-09-23-nws-knowledge-register/research/thermal-korpus-detail.md, Bagian 5). Vonis sementara lapis teks; status BELUM TERKONFIRMASI sampai manusia membuka PDF primer.
> K-9 (rumus di atas): SALAH ATRIBUSI. Kedua bentuk ΔT_serupa/ΔT_udara hanya ada di rantai F (`05_DOMAIN-KNOWLEDGE/THERMAL/RANTAI-JAMINAN.md` bagian Perhitungan ΔT), BUKAN di buku Vollmer - resume tidak memuat rumus itu; satu-satunya ΔT di resume adalah kalimat anti-klaim 'Yang tidak ada di buku ini'. Orang yang memverifikasi rumus ini ke buku R3 tidak akan menemukannya. Tulis atribusinya sebagai definisi kerja rantai F, bukan pasokan rujukan R3 (register K-9).

Setiap angka yang diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.

## 3. Boleh menetapkan ambang terima?

**Tidak sendirian.** Hanya bila kontrak mengadopsinya secara tertulis

## 4. Batas pemakaian — baca sebelum mengutip

**Buku fisika, bukan standar pemeliharaan.** Ambang ΔT dari NETA [R2]

## 5. Rantai jaminan

```
REQUIREMENT → REF-THM-001 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain lengkap: `05_DOMAIN-KNOWLEDGE/THERMAL/RANTAI-JAMINAN.md`

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
