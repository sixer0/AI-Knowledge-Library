---
record_type: knowledge_card
reference_id: REF-CVI-002
reference_confidence_level: R3
title: "Richard Hartley, Andrew Zisserman - Multiple View Geometry in Computer Vision (2003, Ca..."
domain: COMPUTER-VISION
authority_status: PENDING_VERIFICATION
vault_path: 03_SOURCE-VAULT/R3_TEXTBOOK-HANDBOOK/COMPUTER-VISION
resume_path: '05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/R3 - Multiple View Geometry (Hartley & Zisserman).md'
---

# REF-CVI-002 — Richard Hartley, Andrew Zisserman - Multiple View Geometry in Computer Vision (2003, Ca...

**Tingkat keyakinan:** **R3** · **Status otoritas:** `PENDING_VERIFICATION` (P-5 — naik ke
`ACTIVE` hanya lewat resume ber-halaman + verifier, gelombang W3)
**Laci sumber:** `R3_TEXTBOOK-HANDBOOK/COMPUTER-VISION`
**Resume lengkap:** `05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/R3 - Multiple View Geometry (Hartley & Zisserman).md` (W3a, berpenanda halaman PDF; menunggu verifier)
**Bukti byte:** sha256[:16] `7ba0104075b51152` — diverifikasi vault==staging pada W1b (gerbang 4/8 PASS)

---

## 1. Yang dipasok rujukan ini

Multiple View Geometry Hartley/Zisserman — kalibrasi kamera, epipolar.

**Halaman jangkar:** terpasang per butir di resume W3a (`resume_path` di kepala kartu, nomor halaman PDF). Angka hanya boleh dikutip ke dokumen serah bila menunjuk penanda `[R3, …, PDF n]` di resume itu.

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
- Multiple View Geometry Hartley/Zisserman — kalibrasi kamera, epipolar. — cakupan detail per bab belum diverifikasi manusia.
- Edisi/tahun terbit: ikuti judul berkas di laci; waspadai usia >15 th untuk angka produk
  (wajib R4 lembar data, bukan buku).
- Dilarang memakai kartu ini sebagai bukti "sudah ada di rak" untuk angka spesifik
  sebelum resume W3 menambat halamannya.

## 5. Rantai jaminan

```
REQUIREMENT → REF-CVI-002 (R3) → KEPUTUSAN DESAIN → PERHITUNGAN → UJI → BUKTI → TERIMA
```

Dilarang melompat dari **rujukan langsung ke ambang terima** tanpa catatan keputusan dan
bukti verifikasi. Rantai domain: `05_DOMAIN-KNOWLEDGE/COMPUTER-VISION/RANTAI-JAMINAN.md` (masih berbanner belum berantai penuh).

## 6. Gate minimum sebelum ditutup

G0 sumber tervalidasi · G1 kebutuhan dibekukan · G2 desain disetujui ·
G3 hitungan diperiksa orang kedua · G4 metode uji disetujui · G5 uji lulus dengan bukti mentah ·
G6 bukti serah lengkap · G7 diterima pemberi kerja

Rincian: `01_GOVERNANCE/ASSURANCE-GATES.md`
