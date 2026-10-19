---
name: gsp-docx-business-report
description: Use when building GSP business DOCX reports.
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, document, docx, report, naturalization]
    category: document
---

# GSP DOCX Business Report

Kelas tugas: "buatkan laporan dokumen docx standar bisnis profesional" atas hasil analisa/riset/akuisisi; output wajib lolos gerbang naturalisasi kanal `doc`. Resep terverifikasi 23-09 (laporan analisa korespondensi vendor, 47 KB, VERDICT PASS setelah 2 siklus FAIL->fix->PASS).

## Struktur wajib (Module A Business Documents + STD-SAJI-001)

1. Sampul: nama org, judul, subjudul, nomor dokumen (format `LAP-<PROG>/<MMYYYY>/<NN>`), tanggal, klasifikasi (mis. TERBATAS), kolom persetujuan.
2. Daftar isi tabel (Bagian | Judul).
3. Ringkasan Eksekutif - angka populasi + kelompok keputusan + item tenggat kritis.
4. Latar Belakang dan Metodologi - langkah bernomor.
5..N Temuan (tabel padat per kelompok prioritas), Rekapitulasi Angka, Rekomendasi Langkah.
Terakhir: Blok Verifikasi ber-banner ("BUKTI VERIFIKASI ... dihitung alat, bukan ingatan") berisi hash sumber, ukuran NAS==lokal, dan BATAS KLAIM.
Footer: judul pendek + nomor halaman (fldSimple PAGE). Kepala tabel navy `0F2A4A` teks putih bold, zebra baris genap `C0C0C0`, label kolom manusiawi, lebar kolom per-isi.

## RESEP GERBANG NATURALISASI KANAL `doc` (paling penting; scan_ai_footprint.py)

Scanner DOCX memperlakukan SEMUA paragraf berurutan (termasuk heading dan baris sampul) sebagai grup prosa; sel tabel = ORIGIN_TABLE dan dikecualikan dari metrik panjang. Konsekuensi yang terukur:
- C-7 (B2): paragraf < 3 kalimat boleh maksimal 1 per dokumen (revisi NAT-C7 27-09; semula < 4). Baris sampul, heading telanjang, dan daftar bullet/list-number adalah pembunuh senyap - render ketiganya sebagai TABEL (sampul = tabel 1 kolom; daftar isi = tabel; daftar prosedur = tabel 2 kolom Langkah|Prosedur).
- C-6 (B1): rata-rata >= 25 kata/kalimat pada lapisan prosa. Gabungkan narasi per seksi menjadi SATU paragraf panjang multi-kalimat (target 4-6 kalimat, 25-40 kata/kalimat); hasil terukur PASS di 35.3.
- C-8b (B8): wajib ADA angka spesifik DAN kata pengakuan batasan. Sisipkan leksikon scanner: `batasan`, `keterbatasan`, `belum terverifikasi`, `tidak termasuk`, `asumsi` - paling natural di seksi Blok Verifikasi ("Status ... belum terverifikasi oleh alat kami karena ...").
- C-9 hedging (`dapat`, `mungkin`, `berpotensi`, `diprediksi`, `cenderung`) <= 3 per 1.000 kata - ganti dengan konstruksi faktif ("wajib", "perlu", "harus", atau kalimat langsung).
- D-TA-09 agregasi: >= 2 indikator berat terpicu = FAIL total; perbaiki semua berat sekaligus, bukan satu-satu.
- C-1/C-2: em dash U+2014 dan middle dot U+00B7 harus 0 (juga di dalam sel tabel).

## Loop verifikasi sebelum serah (urutan wajib)

1. Build via `uv run --python 3.11 --with python-docx python build_report_docx.py`.
2. Baca-balik berkas tersimpan dengan python-docx: cetak HEADINGS, jumlah baris/kolom tiap tabel, hitung U+2014/U+00B7 pada gabungan paragraf+sel, dan probe daftar fakta kunci (assert per butir, mis. angka populasi, nama vendor).
3. Scan ARTEFAK NATIF: `python "$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/scripts/scan_ai_footprint.py" <file>.docx --channel doc` - JANGAN scan teks hasil flatten manual (sel tabel ikut tercampur ke prosa -> FAIL C-7 palsu; preseden 23-09). Tampilkan baris VERDICT utuh, tanpa pipe tail.
4. Upload ke NAS (koneksi FTP baru, `TYPE I`), lalu buktikan `ftp.size()` == `os.path.getsize()`.
5. Laporkan jejak cek (VERDICT + angka metrik) bersama artefak ke user.

## Pitfalls

- Helper `make_table(...)` harus meneruskan `font_size` ke `style_table`; lupa = TypeError saat tabel densitas tinggi (preseden 23-09).
- `patch` yang menghapus baris kosong terakhir (old_string berakhir `\n`, new_string tidak) bisa menggabungkan `]` dengan baris berikut -> SyntaxError. Setelah patch penghapusan baris, cek lint output; bila error, perbaiki di patch berikutnya.
- Sel banner merged: buat baris pertama tabel lalu `cells[0].merge(cells[1])` SEBELUM menambah baris data; pola merge pasca-add_row menghasilkan baris tambahan yang tidak diinginkan.
- Istilah asing jangan masuk narasi Indonesia ("rather than" terselip = jejak mesin; probe baca-balik menangkapnya).
- Peringatan `fontTools is required` dari pypdf saat ekstraksi PDF = benign; teks tetap terekstrak penuh. Tambahkan `--with fontTools` bila perlu presisi encoding.

## Template

`templates/build_report_docx.py` - kerangka builder generik (sampul tabel, TOC tabel, H/P/make_table/banner verifikasi/footer PAGE) siap salin-modifikasi.
