# Kelas buta-sensor figur baru (RAFIF-REVB-1010, 10-10) + uji cermin manifest

Sumber: supervisi controller misi tulis-buku Rev B; semua resep di bawah SUDAH dijalankan pada giliran itu dan menjatuhkan vonis yang benar. Dua kelas cacat figur lolos dari SEMUA sensor mekanik yang ada (fontTools GG, konektor GK, dua-run byte-identik, cermin manifest) dan hanya tertangkap oleh visus + penggaris piksel. Pelajaran induk: mata dan penggaris piksel tidak bisa dihapus dari rantai, betapapun hijaunya sensor.

## Kelas #4: tabrakan marker-vs-anotasi pada chart (preseden G9.3)

- Gejala: titik ulangan (repetisi) atau marker lain menimpa teks label nilai sampai digit/desimal tertutup (contoh: titik abu pusat (875,247) berada di dalam pita teks '8.3' y232-252). Label lain bisa aman (gap 15px) - jadi vonis WAJIB per elemen teks, bukan per figur.
- Buta bagi: GG/GK (tidak ada konektor), determinisme, dpi, min_pt. Visus pekerja mengklaim bersih; visus controller menjatuhkan.
- Deteksi murah: crop resolusi penuh zona label (PIL `im.crop` per region, threshold <200) lalu bandingkan bbox piksel gelap marker vs pita teks; atau minta vision menjawab butir (4) secara eksplisit 'tabrakan marker-vs-anotasi' karena model visus cenderung menjawab N/A untuk kelas yang tidak ditanya.
- Tambalan resep: offset label nilai menjauhi titik ulangan (textcoords offset) atau jitter titik; render ulang; visus enam butir sebelum publish.

## Kelas #5: konten terpotong tepi kanvas / margin nol (preseden G26.5, G27.1; warisan lolos-sensor G11.4, G12.1)

- Gejala: blok konten menempel kolom 0 kanvas (stroke simpul terpotong separuh) atau lebih lebar dari kanvas (terpotong dua sisi). Visus melihat 'margin kiri nol vs kanan 110px'.
- Buta bagi: SEMUA sensor era itu termasuk cermin manifest dua arah - FG6 lulus mekanik sempurna tapi 2 dari 5 PNG-nya terpotong.
- Resep uji deterministik populasi (grep-piksel, satu script untuk semua PNG folder terbit):

```python
from PIL import Image
for f in sorted(pngs):
    im = Image.open(f).convert('L'); w,h = im.size; px = im.load()
    c0 = sum(1 for y in range(h) if px[0,y]   < 200)   # kolom kiri
    cw = sum(1 for y in range(h) if px[w-1,y] < 200)   # kolom kanan
    r0 = sum(1 for x in range(w) if px[x,0]   < 200)   # baris atas
    rb = sum(1 for x in range(w) if px[x,h-1] < 200)   # baris bawah
    gagal = any(v > 50 for v in (c0,cw,r0,rb))
```

- Ambang sah: >50 px gelap pada baris/kolom TERAKHIR-1 baris = FAIL. Pola sehat = margin konten >=124 px per sisi (teladan G25.1). Sensus populasi wajib saat merge/rakit, bukan hanya per kartu - id yang lolos sensor kartunya bisa tertangkap sensus folder.
- Aksi: pusat-horizontal blok (margin kiri == kanan), render ulang, publish increment, pin baru dilaporkan.

## Uji cermin manifest DUA ARAH (standar rilis; teladan lulus: manifest FG6)

Manifest figur terbit wajib cermin byte disk, diuji dua arah:
1. manifest -> disk: tiap berkas yang DISEBUT entri (png/svg/spek/sidecar + sha256 + ukuran) harus ADA dan hash-nya cocok. Entri menyebut PNG yang tak ada di disk = ENTRI HANTU (preseden FG2: 4 id ditahan publikasinya tapi manifest mengklaim lahir lengkap dengan sha256 - bahaya fatal untuk RAKIT bind-register). Id tertahan masuk blok 'ditahan' berstatus eksplisit.
2. disk -> manifest: tiap berkas kelas itu di folder terbit harus disebut sebuah entri (nol yatim).
- Pitfall parser pengawas: kunci hash bisa bersarang (`berkas.png.sha256`, `sha256_png`) - asumsi kunci datar menghasilkan '12 hantu' palsu sebelum dibaca struktur sebenarnya. Baca item0 dulu.
- Gerbang RAKIT: manifest-final == cermin byte disk, butir per butir.

## Kanonisasi jalur output saat kartu dicetak (palang dua-folder)

Blueprint yang tidak menetapkan folder terbit membuat kartu paralel berimprovisasi: figurb (steer controller) vs figuran (warisan nama v1.0) - 48 id kolisi, 82 berkas identik, 29 beda-byte, pasangan dash-vs-titik (G10-3 vs G10.3) dalam satu folder. Rezim kanonis: satu folder terbit tunggal; gudang kerja terpisah; merge deterministik sebelum rakit (identik lewati, beda-byte pakai byte tervonis kecuali ada visus LAYAK lebih baru, normalkan dash->titik, manifest cermin). Keputusan jalur WAJIB tertulis di badan kartu sejak dicetak.

## Pitfall alat pengawas (self-corrections giliran ini)

- `sha1sum` di shell vs pin ledger sha256[:16]: memberi kecerokan 'pin bergeser' PALSU pada berkas yang tak tersentuh. Ukur dengan ALGORITME SAMA seperti pin ledger (hashlib.sha256[:16]) sebelum menyimpulkan revisi.
- Mtime + ukuran + pin bersama-sama membuktikan 'berkas tak tersentuh'; salah satu saja bisa menipu.
- Kata 'CAPTIONS' bisa muncul 2x per berkas (blok kanonis + disebut di blok Jejak perakitan yang dibuang saat rakit): gerbang kanal caption menghitung BERKAS blok, bukan kata.
