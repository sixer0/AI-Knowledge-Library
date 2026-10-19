# Blok Identitas Dua Bentuk (C-25) - Paket GSP-SDT

> Sumber: SPEC-DOC-SYSTEM.md §1.6 (C-25), §5.1. Pemilik paket: `gsp-document-quality-standards`.
> Generator WAJIB memilih bentuk sesuai rezim target. Letakkan di halaman pertama (DOCX),
> sheet pertama (XLSX), atau elemen pertama `<body>` (HTML).

## 1. Bentuk (a) - kisi 6×4 keluarga pertahanan (R-2 SDTP, R-3 AD, R-4 AU)

Dua belas field, dua kolom per baris:

```text
DOK NO      <GSP-SDTP[-XX]-nnn>    REVISI      <A>
REGISTER    <NNN/GSP/STD/VIII/TAHN> TANGGAL     <DD MON YYYY>
KLASIFIKASI <BIASA|TERBATAS|RAHASIA|SANGAT RAHASIA>  STATUS  <BERLAKU|...>
DISUSUN     <divisi/penyusun>      KUSTODIAN   <kode-kustodian>
DIPERIKSA   <pemeriksa>            DISETUJUI   <penyetuju>
LEMBAR      <nn DARI mm>           MATRA       <Darat (AD)|Udara (AU)>   # R-2 memakai BAHASA
```

Catatan sumber: blok identitas R-2 berfield `BAHASA`, bukan `MATRA` (teks R-2 tidak menyebut
matra; berkas sumber berlabel "AL" - perlakukan payung pertahanan sampai konfirmasi).

## 2. Bentuk (b) - strip 1×4 keluarga profesional (R-1 SDT-001, R-5 PL, R-7 BIZ)

```text
DOKUMEN <GSP-SDT[-XX]-nnn> | REGISTER <NNN/GSP/STD/VIII/TAHN> | REVISI <A> · <DD MON YYYY> | STATUS Berlaku · Direktur & Tim GSP
```

Varian R-6 CY: slot keempat diganti `INTEGRITAS: SHA-256 · diisi saat terbit`.

## 3. Versi Markdown/frontmatter (untuk naskah sumber sebelum ekspor)

```yaml
---
title: "<judul - sama dengan H1>"
date: YYYY-MM-DD
author_profile: <profil-gsp-penulis>
status: complete|blocked|needs-review|failed
task_ref: <id-kanban|slug>
source_refs: [R-1, ...]
# --- GSP-SDT (lapisan bentuk dokumen; tambahan di atas enam key Module L.2) ---
gsp_sdt_rezim: SDT|SDTP|AD|AU|PL|CY|BIZ
gsp_sdt_kelas: K1..K8
dok_no: GSP-SDT[-XXX]-nnn
register: NNN/GSP/KODE/BULAN_ROMAWI/TAHUN   # provisional sampai Register Induk
revisi: A
klasifikasi: TERBATAS
status_dokumen: Berlaku
lembar: "nn dari mm"
---
```

Enam key pertama adalah kontrak Module L.2 - JANGAN diubah namanya; key `gsp_sdt_*` adalah
tambahan lapisan bentuk. Saat ekspor DOCX/XLSX/HTML, field ini menjadi isi blok identitas.

## 4. Snippet siap-pakai

- DOCX (python-docx): `snippet-docx.py` - tabel identitas + header/footer klasifikasi + nomor
  lembar per rezim + tabel revisi.
- XLSX (openpyxl): `snippet-xlsx.py` - sheet identitas, kolom Provenans, kunci REQ/LI, sheet revisi.
- HTML: lihat pointer `gsp-frontend-design/references/gsp-sdt/blok-identitas-html.md` (carrier
  kanal HTML; muatan tetap menunjuk paket ini).

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
