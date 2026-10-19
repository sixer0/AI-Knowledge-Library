---
record_type: knowledge_card
reference_id: REF-DRW-007
reference_confidence_level: R3
title: "Thomas E. French, Charles J. Vierck. - The fundamentals of engineering drawing and grap..."
domain: DRAWING-CAD
authority_status: PENDING_VERIFICATION
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/DRAWING-CAD
resume_path: '05_DOMAIN-KNOWLEDGE/DRAWING-CAD/R3 - Fundamentals of Engineering Drawing (French Vierck).md'
---

# REF-DRW-007 — Thomas E. French, Charles J. Vierck. - The fundamentals of engineering drawing and grap...

**Tingkat keyakinan:** **R3** · **Status otoritas:** `PENDING_VERIFICATION` (P-5 — naik ke
`ACTIVE` hanya lewat resume ber-halaman + verifier, gelombang W3)
**Laci sumber:** `R3_TEXTBOOK-HANDBOOK/DRAWING-CAD`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/DRAWING-CAD/R3 - Fundamentals of Engineering Drawing (French Vierck).md` (W3c, berpenanda halaman PDF; menunggu verifier)
**Bukti byte:** sha256[:16] `fe19e7b2ba1a37b7` — diverifikasi vault==staging pada W1b (gerbang 4/8 PASS)

---

## 1. Yang dipasok rujukan ini

Dasar gambar teknik dan teknologi grafik French.

**Halaman jangkar:** terpasang per butir di resume W3c (`resume_path` di kepala kartu); jangkar memakai nomor halaman PDF hasil uji-cocok teks (bukti cuplikan: docs/2026-10-09_bukuv3-mapping-korpus/evidence/w3c_anchors-final.json). Kutipan buku ini ke dokumen serah wajib menunjuk penanda `[R3, …, PDF n]` di resume; status tetap pending_verification (P-5) sampai verifier.

## 2. Rumus / metode

```
— (metode level buku; ekstraksi tertambat halaman menunggu resume W3)
```

Setiap angka yang kelak diambil dari sini **wajib ditandai** salah satu dari:
`SOURCE-DERIVED` (dengan kutipan halaman) · `PROJECT-DERIVED` · `OEM-DERIVED` · `ASSUMPTION`.
Cara perolehan kartu ini: **SOURCE-DERIVED tertunda** — berkas PDF asli ada di laci vault
dengan hash tercatat, tetapi kutipan per halaman belum dibuat; sampai W3, kartu ini hanya
menyatakan **keberadaan** sumber, bukan angkanya.

## 3. Boleh menetapkan ambang terima?

**TIDAK.** Dua alasan berlapis: (a) `authority_status` masih `pending_verification`;
(b) R3 tidak pernah menetapkan ambang sendiri — hanya bila kontrak mengadopsinya tertulis.

## 4. Batas pemakaian — baca sebelum mengutip

- Buku teks/handbook (R3): sah untuk **metode dan penalaran**, bukan ambang terima final.
- Dasar gambar teknik dan teknologi grafik French. — cakupan detail per bab belum diverifikasi manusia.
- Edisi/tahun terbit: ikuti judul berkas di laci; waspadai usia >15 th untuk angka produk
  (wajib R4 lembar data, bukan buku).
- Dilarang memakai kartu ini sebagai bukti "sudah ada di rak" untuk angka spesifik
  sebelum resume W3 menambat halamannya.

## 5. Rantai jaminan

```
REQUIREMENT → REF-DRW-007 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain `DRAWING-CAD`: lihat `05_DOMAIN-KNOWLEDGE/DRAWING-CAD/`.

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
