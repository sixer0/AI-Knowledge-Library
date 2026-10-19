# -*- coding: utf-8 -*-
"""
EPUB -> PDF memakai PyMuPDF, sekaligus memindahkan daftar isi EPUB
menjadi bookmark PDF.

EPUB bersifat reflowable (tanpa halaman tetap), jadi tata letaknya
DIBENTUK ULANG saat dikonversi — bukan disalin. Ukuran halaman dan
ukuran huruf ditetapkan di sini.

Jalankan:  python epub_ke_pdf.py "berkas.epub" [...]
Opsi   :   --lebar N --tinggi N --huruf N
"""
import io, os, sys, time

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass

import fitz

# A4 dalam titik (72 dpi)
LEBAR, TINGGI, HURUF = 595, 842, 11


def ambil(bendera, baku):
    if bendera in sys.argv:
        return int(sys.argv[sys.argv.index(bendera) + 1])
    return baku


def konversi(src):
    nama = os.path.basename(src)
    if not os.path.exists(src):
        print("TIDAK ADA:", nama)
        return None
    dst = os.path.splitext(src)[0] + ".pdf"
    if os.path.exists(dst):
        print("SUDAH ADA, dilewati:", os.path.basename(dst))
        return dst

    t0 = time.time()
    print("Membuka  :", nama[:70])
    print("  ukuran :", "%.1f MB" % (os.path.getsize(src) / 1048576.0))

    doc = fitz.open(src)
    doc.layout(width=LEBAR, height=TINGGI, fontsize=HURUF)
    print("  halaman setelah tata letak:", doc.page_count)

    toc = doc.get_toc()
    print("  daftar isi:", len(toc), "entri")

    print("  mengubah ke PDF...")
    pdfbytes = doc.convert_to_pdf()
    doc.close()

    out = fitz.open("pdf", pdfbytes)
    if toc:
        # entri di luar jangkauan halaman akan ditolak set_toc — disaring dulu
        bersih = [t for t in toc if 1 <= t[2] <= out.page_count]
        dibuang = len(toc) - len(bersih)
        if bersih:
            out.set_toc(bersih)
        print("  bookmark dipasang:", len(bersih),
              ("(%d di luar jangkauan, dibuang)" % dibuang) if dibuang else "")

    out.save(dst, garbage=4, deflate=True)
    out.close()

    print("  keluaran:", os.path.basename(dst))
    print("  hasil   : %.1f MB · %.0f detik" % (
        os.path.getsize(dst) / 1048576.0, time.time() - t0))
    print()
    return dst


if __name__ == "__main__":
    LEBAR = ambil("--lebar", LEBAR)
    TINGGI = ambil("--tinggi", TINGGI)
    HURUF = ambil("--huruf", HURUF)
    berkas = [a for a in sys.argv[1:] if a.lower().endswith(".epub")]
    if not berkas:
        print(__doc__)
        sys.exit(1)
    print("Tata letak: %d x %d titik, huruf %d pt" % (LEBAR, TINGGI, HURUF))
    print("=" * 66)
    for b in berkas:
        konversi(b)
