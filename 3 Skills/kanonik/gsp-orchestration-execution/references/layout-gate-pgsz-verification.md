# Gerbang Layout Terbitan Dokumen: Ukur pgSz Nyata, Bukan Klaim Build
Preseden: EKASLAP-1006 (06-10), Decision Log D-12. User mengeluh "layout jadi kecil, tdk sesuai standard datum" pada DOCX 51 halaman yang lolos semua gerbang angka.

## Anatomi kegagalan (dua lapis)
1. **Cacat pekerja (T1)**: skrip rakit menulis `pgSz` sendiri sebesar 53519x37306 twips (94,4 x 65,8 cm) pada SEMUA 17 seksi, melewati `_GRID` mesin `datum_docx` (token: A4 210x297 mm = 11906x16838 twips). Type scale ikut menyimpang: run dominan 8,0pt dan 6,0pt, padahal token `type.scale_pt.body.size = 9.5`. Word menampilkan kanvas raksasa dengan zoom-out -> semua teks terlihat kecil.
2. **Cacat instrumen gerbang**: CHECK 12 verifier mencatat "Grid: A4 210x297 ... konsisten tokens.json" tanpa pernah mengukur `pgSz` aktual dari berkas. Vonis grid berbasis klaim jalur build, bukan cetakan alat atas artefak jadi.

Efek silumannya: **inflasi halaman**. "51 halaman" pada kanvas 94 cm setara ~184 halaman A4 riil (kalibrasi: rujukan Manual DATUM 002 = 36.896 kata / 100 hal = 369 kata/hal; objek 67.867 kata -> 184 hal). Gerbang rentang halaman (mis. 50-100) yang tidak memverifikasi ukuran halaman bisa lulus palsu.

## Resep ukur deterministik atas berkas JADI (zipfile, tanpa Word)
```python
import zipfile, re
from collections import Counter
z = zipfile.ZipFile(PATH_DOCX)
doc = z.read('word/document.xml').decode('utf-8')
# 1. Dimensi SEMUA seksi. A4 = 11906 x 16838 twips (567 twips/cm)
sects = re.findall(r'<w:pgSz w:w="(\d+)" w:h="(\d+)"[^/]*/>', doc)
assert sects and all(s == ('11906','16838') for s in sects), sects[:3]
# 2. Margin (A4 DATUM: dalam 24mm=1361, rail 32mm=1814/3288 kanan, luar 20mm=1134)
print(re.findall(r'<w:pgMar[^/]*/>', doc)[-1])
# 3. Distribusi ukuran huruf (w:sz half-points). Token body = 9,5pt = 19
szs = Counter(int(x)/2 for x in re.findall(r'<w:sz w:val="(\d+)"/>', doc))
print(szs.most_common(8))
# 4. Volume riil untuk deteksi inflasi
txt = re.sub(r'<[^>]+>', ' ', doc)
words = len(re.findall(r'\S+', txt)); tables = len(re.findall(r'<w:tbl>', doc))
# 5. Embed font (KD-16): word/fonts/ terisi + settings.xml embedTrueTypeFonts
names = z.namelist()
print(any(n.startswith('word/fonts/') for n in names),
      'embedTrueTypeFonts' in z.read('word/settings.xml').decode())
```
Kalibrasi densitas: bandingkan `kata/halaman` objek terhadap dokumen DATUM rujukan SEJENIS yang sudah lolos gerbang (simpan path + sha16 rujukan di jejak). Estimasi halaman-A4-riil = kata_objek / (kata_rujukan / halaman_rujukan). Bila estimasi menyimpang jauh dari halaman COM terukur -> curigai kanvas salah ukuran atau inflasi.

## Aturan mengikat
- **Kartu verifier dokumen** WAJIB memuat CHECK "pgSz semua seksi == token grid" dan "ukuran run badan == token body" yang diukur dari `word/document.xml` artefak JADI. Klaim engine/build/pekerja BUKAN bukti. Ini perluasan langsung RULE AKURASI DATA butir 9 (angka laporan = cetakan alat) ke dimensi layout.
- **Kartu rakit/build** WAJIB memakai `_GRID`/type scale mesin (mis. `datum_docx` import) TANPA override manual halaman/huruf; deviasi = KD-16/KD-17 FAIL (palet/geometry lokal karangan sendiri dilarang).
- **Keluhan visual user** = vonis sinyal (rule anti-drift butir 4): diff artefak vs dump sumber desain dulu (resep di atas), pulihkan sistem sumber; dilarang tambal gejala dengan kosakata/format baru, dilarang pula langsung menyalahkan persepsi user.
- **Kompresi pasca-koreksi-layout** mengikuti hierarki H-2 blueprint: lampiran per-unit keluar badan ke berkas kerja berindeks -> tabel diringkas ke nilai keputusan -> prosa dipadatkan. Dilarang: memangkas unit pengetahuan, mengecilkan type scale di bawah token, inflate halaman. Register kuantitas TIDAK boleh tersentuh oleh perbaikan layout (sha16 harus tetap) - bila src register yang memicu lint, itu jalur re-freeze terpisah.
- **Lembar kendali append-only**: koreksi layout besar = baris revisi baru (APA/MENGAPA/DAMPAK), bukan suntingan senyap.

## Catatan mekanika papan selama misi panjang
- Loop pengawas latar yang mempoll `hermes kanban list --json` akan sesekali membaca output kosong -> `json.JSONDecodeError`. Bungkus `try/except` dan cetak penanda READ_FAIL lalu lanjut; JANGAN perlakukan gagal-baca sebagai kartu bermasalah (dua alarm palsu terjadi di misi ini sebelum diperbaiki).
- Pitfall "late-linked parents" terulang lagi dengan varian baru: kartu hilir (REVERIF) dibuat SEBELUM kartu hulu perbaikannya lahir -> parents kosong -> ready -> diklaim dispatcher untuk memvonis artefak yang belum ada. Pemulihan sah: `reclaim` -> `block --kind dependency` -> `link` edge nyata. Akar pencegahan: jangan create kartu hilir sebelum hulu fisiknya ada di papan; bila terpaksa, block-dependency di giliran tool yang sama dengan create.
- Kartu arsip karena body memuat angka karangan controller (melanggar angka-cetakan-alat): komentar jejak + kartu pengganti ber-body yang angkanya didefinisikan sebagai "hitung dengan alat", bukan nilai literal.
