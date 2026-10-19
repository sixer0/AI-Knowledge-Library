---
name: excel-master
description: Use when building engineering calculation workbooks.
version: 1.4.0
author: GSP (PT. Gemilang Satria Perkasa)
license: Proprietary
platforms: [windows, macos, linux]
metadata:
  gsp:
    category: engineering
    tags: [gsp, excel, workbook, perhitungan, asumsi, audit]
  hermes:
    tags: [gsp, excel, calculations]
    related_skills: [pustaka-teknis]
---

# Excel Master - Workbook Perhitungan Engineering yang Dapat Diaudit


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../../registry-fleet/gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../../registry-fleet/gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## GSP-SDT Integration (v1.2.0 - subset spreadsheet §3.2)

Sumber kebenaran bentuk dokumen: [`skills/gsp/gsp-document-quality-standards/references/gsp-sdt/`](../../registry-fleet/gsp-document-quality-standards/references/gsp-sdt/)
(paket GSP-SDT; MERUJUK, jangan menyalin). Konvensi spreadsheet GSP-SDT PENUH dipegang skill
ini - engine `productivity/xlsx` READ-ONLY (keputusan controller D14, menggantikan langkah 20
blueprint). Subset yang mengikat workbook (SPEC-DOC §3.2 / D-TA-5): TIDAK berlaku bingkai
lembar, pita komando, maupun anatomi naratif K1–K8 penuh.

Penerapan di skill ini:
1. **Sheet identitas = blok identitas (C-25)** sebagai sheet PERTAMA (di depan INPUT-ASUMSI):
   DOK NO, REGISTER, KLASIFIKASI, REVISI, STATUS + KELAS/BOBOT - helper
   `snippet-xlsx.py` paket SDT (`sheet_identitas`).
2. **Kolom `Provenans` wajib pada kolom nilai** - angka rupiah K7/RAB adalah angka teknis
   (C-18). Pemetaan label EKAS skill ini ↔ notasi SDT: `SOURCE-DERIVED`=terukur ■,
   `PROJECT-DERIVED`=diturunkan ◈, `OEM-DERIVED`=pemasok ◇, `ASSUMPTION`=asumsi △.
   Satu angka = satu provenans; pakai validator `validate_rows()` dari snippet.
3. **Kunci tertelusur** kolom pertama: `REQ-Kx-nnn` (kebutuhan), `LI-nnn` (BOQ BIZ),
   `BB-nnn` (bukti PL), `FND-Kx-nnn` (temuan CY) - unik seumur workbook (`penomoran-footer.md`).
4. **Klasifikasi** di sel kepala setiap sheet cetak + header/footer cetak (C-08/C-22);
   penamaan sheet mengikuti pola lembar `nn` bila diekspor ke PDF.
5. **Sheet riwayat revisi tersendiri** (di depan/bukan menggantikan AUDIT-TRAIL bila sudah ada;
   baris terbaru di puncak, baris lama tak diubah - C-24): `sheet_revisi`.
6. Gerbang: checklist `checklist-pra-terbit.md` butir universal 1–17 dijalankan sebelum workbook
   dinyatakan selesai, berdampingan dengan verifikasi EKAS skill ini.

Larangan: jangan salin tabel/anatomi ke file ini; jangan terbitkan sheet nilai tanpa kolom
Provenans; jangan duplikat AUDIT-TRAIL jadi dua sumber kebenaran revisi (satu sheet revisi resmi).
Revisi: v1.1.0 (2026-09-01, SM-2 t_4cc4e6b9) - section subset §3.2 + rujukan snippet-xlsx (langkah 19; muatan langkah 20 diserap per D14).
- Em-dash U+2014 DILARANG MUTLAK tanpa pengecualian (D17); middle dot U+00B7 dilarang dengan pengecualian hanya string blok terkendali yang meniru master design verbatim. Berlaku atas seluruh teks keluaran; definisi + prosedur scan: `gsp-document-quality-standards/references/gsp-sdt/README.md` (bagian Aturan teks keluaran D15+D16).

## When to Use

- Menyusun **workbook perhitungan** yang akan menjadi lampiran berita acara / dokumen
  serah (power, fiber, VSS, termal, mekanik, dll.).
- Setiap kali perhitungan menyangkut **ambang lulus** atau angka yang diperiksa auditor.

Kanonik korpus: [`ekas/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/06_ENGINEERING/ASSUMPTIONS/ASUMSI-BAKU.md) (bagian "Untuk workbook
(excel-master)") + [`ekas/10_TEMPLATES/TPL-02-CALCULATION-SHEET.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/10_TEMPLATES/TPL-02-CALCULATION-SHEET.md) +
[`ekas/01_GOVERNANCE/ASSURANCE-GATES.md`](../../../4%20Knowledge%20Bank/ekas-lapis-teks/01_GOVERNANCE/ASSURANCE-GATES.md) (gate G3).

## Aturan pokok (dari EKAS - tidak bisa ditawar)

1. **Asumsi di sheet terpisah** - tidak dicampur dengan perhitungan. Sheet asumsi berisi:
   besaran, nilai, satuan, dasar/sumber (`[R-n - sumber, hal]`), sensitivitas,
   rencana penggantian.
2. **Rumus hidup, bukan angka diketik** - tiap sel perhitungan merujuk sel asumsi/input.
   Perubahan asumsi → dampak terlihat di seluruh hitungan otomatis.
3. **Tiap angka membawa penanda sumber/asal**: `SOURCE-DERIVED`; `PROJECT-DERIVED`;
   `OEM-DERIVED`, `ASSUMPTION`.
4. **Ambang dari R1/R2** (R3 hanya bila kontrak mengadopsi) - dikutip dengan standar +
   baris/tabelnya.
5. **Satuan konsisten & ditulis eksplisit** (MΩ vs Ω, dB vs dBm, Ah vs Wh) - kesalahan
   satuan adalah penyebab paling umum hitungan gagal auditable.
6. **Pemeriksa kedua (G3)** - verifikasi orang kedua wajib; jejak nama + tanggal ada.

## Struktur workbook yang dianjurkan

```
Sheet 1  INPUT-ASUMSI    → semua masukan + sumber + sensitivitas (rumus hidup di sini)
Sheet 2  PERHITUNGAN     → rumus merujuk Sheet 1; tiap kelompok punya judul + satuan
Sheet 3  HASIL-AMBANG    → hasil vs ambang (standar [R1/R2] atau hitungan terverifikasi)
Sheet 4  SENSITIVITAS    → skenario ½× dan 2× untuk tiap ASSUMPTION
Sheet 5  AUDIT-TRAIL     → versi, tanggal, pemeriksa kedua, perubahan
```

## Pitfalls yang paling sering muncul

- **Angka mati (hardcoded)** di tengah perhitungan → melanggar aturan 2; dampak perubahan
  asumsi tidak terlihat.
- **Asumsi tersembunyi** di sel tanpa label/sumber → auditor akan menolak.
- **Ambang tanpa sumber** - menulis "lulus" tanpa menunjukkan standar yang dipakai.
- **Satu sheet campur input+hitung** → sulit diverifikasi ulang.
- Nilai produk (efisiensi, derating, DoD) dari ingatan, bukan R4.

## Verifikasi sebelum workbook dinyatakan selesai

- Sheet asumsi terpisah, semua masukan berlabel + bersumber ✓
- Rumus hidup (tidak ada hardcode untuk masukan) ✓
- Ambang dikutip dari R1/R2 (atau R3+pasal kontrak) ✓
- Sensitivitas untuk tiap ASSUMPTION ada ✓
- Pemeriksa kedua tercatat di audit trail ✓
- Varian (unit test): ubah 1 asumsi → hasil berubah sesuai arah & besaran yang wajar ✓
