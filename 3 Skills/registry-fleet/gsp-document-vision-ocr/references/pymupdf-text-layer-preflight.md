# Preflight lapisan teks PDF — pymupdf sebelum OCR vision

## Kasus nyata (2026-08-24, dokumen ADINT)

- File: `GSP_Technical_Report_ADINT.pdf` (150 hal, 13,6 MB, producer
  "macOS Quartz PDFContext").
- `read_file` gagal: *"document extraction failed — UnsupportedError:
  unsupported input: PDF has no extractable text (TextBased, 150 pages):
  OCR is required."* → seolah-olah image-based, seolah-olah wajib OCR vision.
- Fakta: pymupdf mengekstrak **426.885 karakter** dari 150 halaman dengan
  **0 halaman kosong** (<50 char). PDF punya lapisan teks penuh.

## Pelajaran

1. Pesan "no extractable text" dari konverter dokumen (`read_file`) tidak
   selalu benar. Selalu probe lapisan teks langsung dengan pymupdf sebelum
   memutuskan jalur OCR vision (mahal, lambat, rawan halusinasi).
2. Kasus ADINT p3 sebelumnya (halusinasi vision "Anggaran Dana Insentif
   Teknis PUPR") kemungkinan diperparah oleh asumsi "image-based" yang
   salah pada dokumen yang sebenarnya punya teks.

## Perintah probe

```bash
python -c "import pymupdf; d=pymupdf.open('FILE.pdf'); t=[len(d[i].get_text().strip()) for i in range(len(d))]; print('total_chars',sum(t),'empty_pages',sum(1 for x in t if x<50))"
```

Interpretasi:
- total_chars >> 0, empty_pages ≈ 0 → **ekstrak teks, jangan OCR**.
- total_chars ≈ 0 di hampir semua halaman → benar-benar scan → jalur OCR vision.

## Ekstraksi teks dengan penanda halaman (untuk sitasi per-halaman)

```bash
python -c "
import pymupdf
doc = pymupdf.open('FILE.pdf')
with open('OUT.md','w',encoding='utf-8') as f:
    for i in range(doc.page_count):
        f.write(f'\n\n<!-- ===== PAGE {i+1} ===== -->\n\n')
        f.write(doc[i].get_text())
"
```

Catatan: modul `fitz` (API lama) memberi deprecation warning; gunakan
`import pymupdf`. Setelah ekstraksi, baca file .md penuh baris per baris
(proposal 150 hal = ~8.200 baris / ~450 KB) untuk pendalaman "tanpa ada
yang terlewatkan".
