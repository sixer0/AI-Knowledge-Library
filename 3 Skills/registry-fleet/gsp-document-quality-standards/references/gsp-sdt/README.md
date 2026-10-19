# Paket Referensi GSP-SDT (lapisan bentuk dokumen)

Pemilik tunggal: `gsp-document-quality-standards` (keputusan D-TA-7 / D13). Skill kanal lain
HANYA menunjuk direktori ini - jangan menyalin isinya ke SKILL.md konsumen (anti-drift).

Hulu spesifikasi: `docs/2026-09-01-master-design-adaptasi/study/SPEC-DOC-SYSTEM.md`
(25 butir CORE C-01..C-25 + 6 kelompok DELTA, dari 7 dokumen sistem GSP-SDT Rev A, 27 AGU 2026).

| Berkas | Isi | Pemakai utama |
|---|---|---|
| [`kelas-dokumen.md`](kelas-dokumen.md) | Kelas K1–K8 × rezim: nama, klasifikasi awal, bobot verifikasi (67 vs 66) | semua jalur |
| [`anatomi-per-kelas.md`](anatomi-per-kelas.md) | Matriks blok wajib ●/○/– per kelas + delta PL/CY/BIZ | docx, html |
| [`penomoran-footer.md`](penomoran-footer.md) | Pola `GSP-SDT(-XXX)-nnn`, register, klausul ≤3 tingkat, `Gambar k.n`+SUMBER, REQ-ID, pola nomor lembar per rezim, kepala-kaki C-22, revisi C-24 | docx, xlsx, html |
| [`blok-identitas.md`](blok-identitas.md) | Blok identitas dua bentuk (kisi 6×4 pertahanan / strip profesional) + frontmatter tambahan | docx, xlsx, html |
| [`provenans.md`](provenans.md) | Provenans angka ■◈◇△, A/D/I/T, rantai kustodi SHA-256, padanan medium | semua jalur |
| [`checklist-pra-terbit.md`](checklist-pra-terbit.md) | Checklist gerbang 22 butir (≤25) siap-tempel + cara eksekusi | gerbang semua jalur |
| [`delta-matra.md`](delta-matra.md) | Ringkasan delta 6 kelompok per rezim (umum/kelas/anatomi/aparatus/acuan/gerbang) | semua jalur |
| [`snippet-docx.py`](snippet-docx.py) | python-docx: blok identitas, header/footer klasifikasi, nomor lembar per rezim, tabel revisi, label provenans | gsp-report-format, gsp-word-report-deliverable |
| [`snippet-xlsx.py`](snippet-xlsx.py) | openpyxl: sheet identitas, kolom Provenans wajib, kunci REQ/LI/BB/FND + validator, sheet revisi (subset §3.2 / D-TA-5) | excel-master |

## Hierarki aturan (D-TA-4 + D-TA-7.5 - tidak boleh diputuskan ulang)

1. Kanal dokumen terkontrol (docx, xlsx, HTML-laporan): **GSP-SDT menang** atas estetika DS;
   DS hanya lapisan tipografi/palet yang tidak melanggar klausul (C-21: boleh lebih ketat,
   tidak lebih longgar).
2. Resolusi konflik fleet: FORMAT → Module L; **BENTUK/ANATOMI/REGISTER dokumen → GSP-SDT
   (paket ini)**; GAYA presisi → Module H/K.
3. HTML artifact: blok identitas + klasifikasi header/footer WAJIB dulu, baru palet/tipografi DS.

## Batas paket

- Nilai palet/huruf TIDAK ada di sini - milik paket token DS
  (`gsp-design-system-grill/references/master-design/`).
- Nomor register contoh bersifat provisional sampai Register Induk (ARSIP).
- Engine skills (`productivity/docx`, `productivity/xlsx`) READ-ONLY (keputusan controller D14):
  muatan mereka diserap ke carrier gsp-* yang memakainya.


## Aturan teks keluaran (D15+D16)

Larangan em-dash (U+2014) MUTLAK (D17): konten keluaran (teks, slide, HTML, prompt, teks dalam gambar) tidak memakai em-dash sama sekali, TANPA pengecualian blok terkendali maupun verbatim (pengecualian verbatim hanya berlaku untuk middle dot). Alternatif saat menulis: koma, titik, titik dua, kurung, atau spasi-hyphen. Saat verifikasi: scan U+2014 pada artefak final, ganti otomatis sampai nol, laporkan jumlah penggantian.

Middle dot (U+00B7) dilarang di konten keluaran. Pengecualian HANYA pada string blok terkendali yang meniru master design verbatim (mis. footer TERBATAS · Terkendali). Alternatif di prosa: koma, garis miring, kurung, atau titik dua. Bullet daftar boleh; marker dan gayanya MENGIKUTI preset master design terpilih (lihat bagian Ikonografi/Komponen di references/master-design/gsp-ds-set-<slug>.md), bukan • generik hiasan di prosa.

Catatan deviasi tipografi (D17): pola footer sumber `n <U+2014> mm` (tercetak R-1) dirender sebagai `n / mm` demi kepatuhan D17, mengikuti preseden pola footer PDF keluarga GSP-SDT `HLM n / mm` (SPEC-DOC-SYSTEM.md R-5); label provenans ikut dirender `[jenis / sumber, hal]`. Ini disengaja, bukan cacat.
