# Gerbang Objek Terbit (RENDER-GATE) - resep pengukuran docx/pdf terbit

Sumber preseden: misi INDUK-GAYA-VISUAL-1006 (06-10-2026). User memvonis dua kali atas sajian
pedoman visual: (1) 'tidak semua hasil bisa saya buka' - nama berkas ber-spasi di tautan MEDIA;
(2) 'hasilnya masih berantakan' - setelah FIX-SA hijau C16 (lebar gambar), audit render+vision
menemukan cacat lapisan lain (ritme, caption hilang 52 hal, tabel rusak per-huruf, pemenggalan
monospace, penanda dua warna). Keputusan struktural: bangun ulang dengan MESIN KANONIS
datum-house-style v2.0.0 (registry fleet), bukan menambal builder karangan untuk ketiga kalinya.

## Konstanta satuan (hafalkan; salah bagi = salah vonis)

1 inci = 914400 EMU = 1440 dxa/twips = 72 pt; 1 mm = 36000 EMU = 56,69 dxa = 2,8346 pt.
Insiden nyata: pembagi 567 (salah 10x) membuat tabel 128 mm tervonis 12,8 mm. Sebelum
menyatakan akar cacat, cocokkan pembacaan XML dengan RENDER PDF - render adalah arbiter.

## Snippet pengukuran (Python)

```python
# PDF: overflow gambar, tabrakan teks, caption posisi
import pymupdf
d = pymupdf.open(pdf)
TOP, BOT = 70, d[0].rect.height - 60   # zona badan (chrome header/footer di luar)
for i, p in enumerate(d):
    body_imgs = [im for im in p.get_image_info()
                 if TOP < im["bbox"][1] and im["bbox"][3] < BOT]
    blocks = [b for b in p.get_text("blocks") if b[4].strip()]
    body_blocks = [b for b in blocks if b[1] > TOP and b[3] < BOT]
    for im in body_imgs:
        r = pymupdf.Rect(im["bbox"])
        if im["bbox"][2] > p.rect.x1 + 3: print("OVERFLOW", i+1)
        for tb in body_blocks:
            it = r.intersect(pymupdf.Rect(tb[:4]))
            if not it.is_empty and it.get_area() > 0.3*min(r.get_area(), pymupdf.Rect(tb[:4]).get_area()):
                print("TABRAKAN", i+1, tb[4][:30])
    caps = [tb for tb in body_blocks if tb[4].strip().startswith(("Gambar ", "GAMBAR "))]
    if body_imgs and not caps: print("CAPTION HILANG", i+1)

# DOCX: lebar penempatan + lebar kolom tabel
import docx
from docx.oxml.ns import qn
dd = docx.Document(docxf)
bad = [(round(s.width/36000,1), round(s.height/36000,1)) for s in dd.inline_shapes
       if s.width/36000 > 166.5]                      # nominal 128/166mm + toleransi
for t in dd.tables:
    g = t._tbl.find(qn('w:tblGrid'))
    if g is None: continue
    mm = [int(c.get(qn('w:w')))/56.69 for c in g.findall(qn('w:gridCol'))]
    # vonis: tidak ada kolom < 15mm (kecuali terdaftar); total == lebar area cetak
```

```python
# Render bukti utk vision_analyze (red-green)
pix = d[n-1].get_pixmap(dpi=100); pix.save(f"work/sajian_audit/h{n:03d}.png")
```

## Gotcha alat

- Operator `&` (bitwise Rect intersection) dalam heredoc inline DITOLAK parser terminal sebagai
  shell-backgrounding. Tulis skrip ke berkas lalu jalankan, atau pakai `r.intersect(r2)`.
- `fitz` alias deprecated - import `pymupdf`.
- Word COM: `Dispatch` gagal 'Call was rejected by callee' saat Word sibuk worker lain ->
  `win32com.client.DispatchEx("Word.Application")` instance terpisah + `Documents.Open(src,
  ReadOnly=True)`; hitung halaman `ComputeStatistics(2)`; ekspor `ExportAsFixedFormat(dst, 17)`.
- Kompresi ulang PDF (garbage/deflate) tidak menolong bila gambar sudah optimal - bisa membengkak
  (ukur 105%); jangan klaim 'diperkecil' tanpa ukur.
- vision_analyze untuk layout: minta KRITIK TATA LETAK (kolom terurai huruf, caption posisi,
  tabrakan, ritme spasi, elemen terpotong) - bukan ringkasan isi.

## Protokol red-green sebelum klaim 'rapi'

1. Render >= 8 halaman yang DULU rusak (dari temuan audit) + 2 acak -> PNG 100 dpi.
2. vision_analyze tiap render; catat temuan bernama (ini bukti RED alat sendiri, pola short-check D-16).
3. Perbaiki via mesin kanonis; rebuild; render ULANG halaman yang sama; daftar path sebelum/sesudah
   wajib di result kartu.
4. Baru jalankan gerbang deterministik (overflow=0, tabrakan=0, caption>=95%, gridCol wajar) +
   scanner kanal doc + hitung halaman dua alat (Word COM == pymupdf; selisih dibukukan declared).

## Aturan pendamping (dari ledger misi)

- Artefak cacat ditandai `.cacat` / `.cacat-2`, JANGAN dihapus (bukti jejak audit).
- Pin sha16 artefak yang dipegang checker/fixture WAJIB naik serumah kartu dengan suntingannya;
  riwayat pin append-only ber-alasan (kelas drift 3x: J16/SA/F18; verifier menangkap sebagai
  CHECK FAIL, bukan kegagalan objek).
- Nama berkas sajian-MEDIA tanpa spasi (lihat gsp-orchestration-execution Seksi penyajian):
  salinan underscore di serah/ dengan sha identik berkas kanonis.
