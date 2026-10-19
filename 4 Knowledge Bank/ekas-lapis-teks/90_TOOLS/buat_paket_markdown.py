# -*- coding: utf-8 -*-
"""Bangun paket ekspor Markdown untuk dipakai model lokal."""
import os, glob, zipfile, io, shutil, re

RAK = r'C:\Users\gspen\Videos\Buku'
SK = r'C:\Users\gspen\.claude\skills'
SCRATCH = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.join(RAK, 'Pustaka-Teknis-GSP-Markdown.zip')

INTI = ['KATALOG-RUMUS.md', 'ASUMSI-BAKU.md', 'TEMPLATE-BERITA-ACARA.md']
TATA = ['PETA-CELAH-KOLEKSI.md', 'DAFTAR-PENGADAAN-BAHAN.md',
        'PROSEDUR-TAMBAH-BUKU.md', 'RENCANA-KERJA.md']

isi = []   # (jalur_arsip, jalur_asli)

# README
isi.append(('README.md', os.path.join(SCRATCH, 'README-ekspor.md')))

# 00-inti
for f in INTI:
    isi.append(('00-inti/' + f, os.path.join(RAK, f)))

# 01-resume — beri awalan nama folder supaya berkasnya menjelaskan diri
#             termasuk resume standar di subfolder _standar/
for p in sorted(glob.glob(os.path.join(RAK, '*', 'RESUME*.md'))
                + glob.glob(os.path.join(RAK, '*', '_*', 'RESUME*.md'))):
    dr = os.path.dirname(p)
    folder = os.path.basename(os.path.dirname(dr) if os.path.basename(dr).startswith('_') else dr)
    judul = os.path.basename(p).replace('RESUME STANDAR - ', 'STANDAR ').replace('RESUME TESIS - ', 'TESIS ').replace('RESUME PANDUAN - ', 'PANDUAN ').replace('RESUME - ', '').replace('.md', '')
    nama = '%s - %s.md' % (folder, judul)
    isi.append(('01-resume/' + nama, p))

# 02-skill
for sk in sorted(os.listdir(SK)):
    d = os.path.join(SK, sk)
    if not os.path.isdir(d):
        continue
    for r, _, fs in os.walk(d):
        for f in sorted(fs):
            if not f.endswith('.md'):
                continue
            rel = os.path.relpath(os.path.join(r, f), d).replace(os.sep, '/')
            isi.append(('02-skill/%s/%s' % (sk, rel), os.path.join(r, f)))

# 03-tata-kelola
for f in TATA:
    isi.append(('03-tata-kelola/' + f, os.path.join(RAK, f)))

hilang = [a for a, b in isi if not os.path.exists(b)]
if hilang:
    raise SystemExit('berkas sumber hilang: %s' % hilang)

if os.path.exists(OUT):
    os.remove(OUT)
with zipfile.ZipFile(OUT, 'w', zipfile.ZIP_DEFLATED, compresslevel=9) as z:
    for arsip, asli in isi:
        z.write(asli, arsip)

# verifikasi
with zipfile.ZipFile(OUT) as z:
    rusak = z.testzip()
    daftar = z.namelist()
    total = sum(i.file_size for i in z.infolist())

print('keluaran : %s' % OUT)
print('berkas   : %d' % len(daftar))
print('mentah   : %.1f KB' % (total / 1024))
print('terkompresi: %.1f KB (%.0f%%)' % (os.path.getsize(OUT) / 1024,
                                         100 * os.path.getsize(OUT) / total))
print('integritas: %s' % ('RUSAK: ' + str(rusak) if rusak else 'OK'))
print()
per = {}
for n in daftar:
    k = n.split('/')[0] if '/' in n else '(akar)'
    per[k] = per.get(k, 0) + 1
for k in sorted(per):
    print('  %-16s %2d berkas' % (k, per[k]))
