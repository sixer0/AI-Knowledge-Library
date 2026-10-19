# -*- coding: utf-8 -*-
"""OCR buku PDF berbasis gambar: sisipkan lapisan teks tak terlihat, gambar tidak diubah.

Pemakaian:
    python ocr_book.py <sumber.pdf> <keluaran.pdf> [dpi_ocr]

Kebijakan:
  - Tiap halaman harus berisi tepat satu gambar penuh; stream gambarnya disalin apa adanya
    (lossless, tanpa kompresi ulang).
  - OCR dijalankan pada render halaman di dpi yang diminta (default 300) — untuk pindaian
    resolusi rendah, render di atas resolusi asli membantu ketepatan Tesseract.
  - Bookmark dan metadata dari berkas sumber dipertahankan.
"""
import os, sys, io, csv, zlib, time, subprocess
from concurrent.futures import ThreadPoolExecutor
import fitz
from PIL import Image

Image.MAX_IMAGE_PIXELS = None
TESS = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
WORKERS = 10
LANG = 'eng'


# ---------------------------------------------------------------- OCR
def run_tess(png):
    base = png[:-4]
    if os.path.exists(base + '.tsv'):
        return base + '.tsv'
    r = subprocess.run([TESS, png, base, '-l', LANG, '--psm', '3',
                        '-c', 'preserve_interword_spaces=1', 'tsv'],
                       capture_output=True, text=True,
                       creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    if r.returncode != 0:
        raise RuntimeError('tesseract gagal: %s' % r.stderr[-300:])
    return base + '.tsv'


def read_words(tsv):
    out = []
    with open(tsv, encoding='utf-8', errors='replace', newline='') as f:
        rd = csv.reader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        next(rd, None)
        for row in rd:
            if len(row) < 12 or row[0] != '5':
                continue
            txt = row[11].strip()
            if not txt:
                continue
            try:
                conf = float(row[10])
                l, t, w, h = int(row[6]), int(row[7]), int(row[8]), int(row[9])
            except ValueError:
                continue
            if conf < 0 or w <= 0 or h <= 0:
                continue
            out.append((l, t, w, h, txt))
    return out


# ---------------------------------------------------------------- PDF
def esc(s):
    return s.replace('\\', r'\\').replace('(', r'\(').replace(')', r'\)')


def text_layer(words, iw, ih, pw, ph):
    """Teks tak terlihat (Tr 3) memakai Courier; Tz disetel agar lebar kata pas."""
    sx, sy = pw / iw, ph / ih
    buf = ['BT', '3 Tr']
    for l, t, w, h, txt in words:
        n = len(txt)
        fs = max(h * sy, 1.0)
        natural = 0.6 * fs * n
        if natural <= 0:
            continue
        tz = max(1.0, min(1000.0, 100.0 * (w * sx) / natural))
        buf.append('/F1 %.2f Tf' % fs)
        buf.append('%.1f Tz' % tz)
        buf.append('1 0 0 1 %.2f %.2f Tm' % (l * sx, ph - (t + h) * sy))
        buf.append('(%s) Tj' % esc(txt.encode('cp1252', 'replace').decode('cp1252')))
    buf.append('ET')
    return '\n'.join(buf)


class PDF:
    def __init__(self, path):
        self.f = open(path, 'wb')
        self.off = [None]
        self.f.write(b'%PDF-1.5\n%\xe2\xe3\xcf\xd3\n')

    def new(self):
        self.off.append(None)
        return len(self.off) - 1

    def obj(self, num, body, stream=None):
        self.off[num] = self.f.tell()
        self.f.write(('%d 0 obj\n' % num).encode())
        if stream is None:
            self.f.write(('<< %s >>\n' % body).encode())
        else:
            self.f.write(('<< %s /Length %d >>\nstream\n' % (body, len(stream))).encode())
            self.f.write(stream)
            self.f.write(b'\nendstream\n')
        self.f.write(b'endobj\n')

    def close(self, root, info):
        n = len(self.off)
        xref = self.f.tell()
        self.f.write(('xref\n0 %d\n' % n).encode())
        self.f.write(b'0000000000 65535 f \n')
        for i in range(1, n):
            self.f.write(('%010d 00000 n \n' % self.off[i]).encode())
        self.f.write(('trailer\n<< /Size %d /Root %d 0 R /Info %d 0 R >>\n'
                      'startxref\n%d\n%%%%EOF\n' % (n, root, info, xref)).encode())
        self.f.close()


CS = {'DeviceRGB': '/DeviceRGB', 'DeviceGray': '/DeviceGray', 'DeviceCMYK': '/DeviceCMYK'}


def main():
    src, dst = sys.argv[1], sys.argv[2]
    dpi = int(sys.argv[3]) if len(sys.argv) > 3 else 300
    work = os.path.join(os.path.dirname(os.path.abspath(__file__)),
                        'ocrwork_' + os.path.splitext(os.path.basename(dst))[0][:20])
    os.makedirs(work, exist_ok=True)

    doc = fitz.open(src)
    N = doc.page_count
    t0 = time.time()

    print('tahap 1/3  render %d halaman @ %d dpi' % (N, dpi), flush=True)
    pngs = []
    for i in range(1, N + 1):
        p = os.path.join(work, 'p%04d.png' % i)
        if not os.path.exists(p):
            doc[i - 1].get_pixmap(dpi=dpi, colorspace=fitz.csGRAY).save(p)
        pngs.append(p)
        if i % 50 == 0:
            print('   %d/%d  %.0fs' % (i, N, time.time() - t0), flush=True)

    print('tahap 2/3  OCR %d halaman' % N, flush=True)
    done = [0]

    def job(p):
        r = run_tess(p)
        done[0] += 1
        if done[0] % 25 == 0:
            print('   %d/%d  %.0fs' % (done[0], N, time.time() - t0), flush=True)
        return r

    with ThreadPoolExecutor(max_workers=WORKERS) as ex:
        tsvs = list(ex.map(job, pngs))

    print('tahap 3/3  menyusun PDF', flush=True)
    pdf = PDF(dst)
    cat, pages, info, font = pdf.new(), pdf.new(), pdf.new(), pdf.new()
    pdf.obj(font, '/Type /Font /Subtype /Type1 /BaseFont /Courier /Encoding /WinAnsiEncoding')
    kids, nwords, skipped = [], 0, []

    for i in range(1, N + 1):
        page = doc[i - 1]
        pw, ph = page.rect.width, page.rect.height
        imgs = page.get_images(full=True)
        if len(imgs) != 1:
            skipped.append(i)
        xref = imgs[0][0]
        w = int(doc.xref_get_key(xref, 'Width')[1])
        h = int(doc.xref_get_key(xref, 'Height')[1])
        filt = doc.xref_get_key(xref, 'Filter')[1].strip('/')
        cs = doc.xref_get_key(xref, 'ColorSpace')[1].strip('/')
        bpc = doc.xref_get_key(xref, 'BitsPerComponent')[1]
        stream = doc.xref_stream_raw(xref)
        extra = '/ColorSpace %s /BitsPerComponent %s /Filter /%s' % (
            CS.get(cs, '/DeviceRGB'), bpc, filt)
        dp = doc.xref_get_key(xref, 'DecodeParms')
        if dp[0] != 'null':
            extra += ' /DecodeParms ' + dp[1]

        imgn = pdf.new()
        pdf.obj(imgn, '/Type /XObject /Subtype /Image /Width %d /Height %d %s' % (w, h, extra),
                stream)

        words = read_words(tsvs[i - 1])
        nwords += len(words)
        with Image.open(pngs[i - 1]) as oim:
            ow, oh = oim.size
        cont = pdf.new()
        cs_txt = ('q %.2f 0 0 %.2f 0 0 cm /Im0 Do Q\n' % (pw, ph)) + \
                 text_layer(words, ow, oh, pw, ph)
        pdf.obj(cont, '/Filter /FlateDecode', zlib.compress(cs_txt.encode('cp1252', 'replace'), 9))

        pg = pdf.new()
        pdf.obj(pg, '/Type /Page /Parent %d 0 R /MediaBox [0 0 %.2f %.2f] '
                    '/Resources << /XObject << /Im0 %d 0 R >> /Font << /F1 %d 0 R >> >> '
                    '/Contents %d 0 R' % (pages, pw, ph, imgn, font, cont))
        kids.append(pg)
        if i % 50 == 0:
            print('   %d/%d  %.1f MB' % (i, N, pdf.f.tell() / 1048576), flush=True)

    pdf.obj(pages, '/Type /Pages /Count %d /Kids [%s]'
            % (len(kids), ' '.join('%d 0 R' % k for k in kids)))
    pdf.obj(cat, '/Type /Catalog /Pages %d 0 R' % pages)
    md = doc.metadata or {}

    def esc_s(s):
        return esc(str(s or '')).encode('cp1252', 'replace').decode('cp1252')

    pdf.obj(info, '/Title (%s) /Author (%s) /Producer (Tesseract OCR text layer)'
            % (esc_s(md.get('title')), esc_s(md.get('author'))))
    pdf.close(cat, info)

    toc = doc.get_toc()
    doc.close()
    if toc:
        out = fitz.open(dst)
        out.set_toc(toc)
        out.save(dst, incremental=True, encryption=fitz.PDF_ENCRYPT_KEEP)
        out.close()

    if skipped:
        print('PERINGATAN: halaman dengan gambar != 1:', skipped[:20])
    print('kata ter-OCR: %d' % nwords)
    print('bookmark dipertahankan: %d' % len(toc))
    print('keluaran: %s  (%.1f MB, sumber %.1f MB)'
          % (dst, os.path.getsize(dst) / 1048576, os.path.getsize(src) / 1048576))
    print('waktu %.0f detik' % (time.time() - t0))


if __name__ == '__main__':
    main()
