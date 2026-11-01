# Figure connector blindness — mechanical gate 0 != pixel fit (figure mission 1009, 2026-10-09/10)

Two independent confirmations in one night that `cacat_gerbang:0` from fontTools-based
diagram gates (gerbang_geometri.py d2734ee7 lineage) does NOT imply the rendered PNG is
technically readable. Both directions of error observed:

- **F2-B / G4.2 (t_904a2817):** run-1 published 6 ids all `cacat_gerbang:0`,
  `deterministik_dua_run:true`, correct machine pin, sidecar attribution clean —
  yet controller independent vision ruled TIDAK-LAYAK: dangling stub segments, a
  connector mis-routed into a foreign column, an arrowhead detached from its node,
  a dashed line crawling along a field border.
- **F1-B / G3.4 + G9.1 (t_421f2836):** after steer-2 added connector gates K1–K4,
  8/10 ids published; controller spot-vision on the two DATUM-33 geometry-change ids
  FAILED BOTH: G3.4 red polyline broken with two floating ends; G9.1 vertical bus
  collinear-overlapping the left borders of two nodes (>3 mm) plus two more floating
  segments. Labels/content intact — pure geometry defect the gate cannot see.

## Residual blind classes after K1–K4 (name them in every figure card)

- **K5 arrow-orientation-vs-border:** an arrowhead may sit exactly on a TOP border yet
  point horizontally (tangent), which reads as detached. Assert marker direction is
  perpendicular (or a deliberate corner-apex entry) relative to the border it lands on.
- **K6 line-through-label-box:** connector passing THROUGH the ink box of a text label
  (not just near it). Knockout-band fixes can create the inverse (band erases foreign
  segments — class G7); assert both: label ink untouched by foreign strokes, and no
  knockout covering non-owned segments.
- **Bus collinearity:** a bus/connector running parallel and <= ~1 mm over a node border
  reads as "border merged with wire". Require >= 3–4 mm separation; measure x-coords of
  vertical bus vs node left/right edges in the SVG, not pixels.
- **Polyline continuity:** gates checking endpoints may still pass a path whose MIDDLE
  segment list has a gap (two polylines that look joined at zoom). Test continuity of the
  full path point sequence against node/bus attachment points.

## Controller vision protocol for figures (six-point, per id, before any L2 vonis)

Run `vision_analyze` on the PUBLISHED PNG asking exactly:
(a) floating/dangling segments without node or bus? (b) every arrowhead landing on the
destination border with perpendicular orientation? (c) any line overlapping a node border
> 3 mm? (d) any label pierced/overlapped by a line or border? (e) all label text complete
and readable (nothing clipped)? (f) content still matches the figure spec (nothing dropped
to achieve the geometry fix)? Verdict LAYAK only if all six pass. Diamond apex entry is
accepted as a corner-entry exception on (b), stated explicitly.

## Worker self-vision claims are the WEAKEST rung

The F2-B worker reported "visus mata CLEAR" for G4.2 while the identical artifact failed
controller vision minutes later. Rule: a worker's own vision pass never closes a figure;
controller (or QC card) re-runs the six-point protocol on the published bytes. When the
worker's mechanical evidence (hashes, determinism, manifest) matches disk but the visual
claim does not survive, vonis = partial: accept the mechanics, convict the id, remediation
card lists the concrete defects WITH coordinates from the controller's own vision output
(gives the next run a targeted repair map instead of a re-debate).

## Steer pattern that worked (timeout/gave_up mid-publish)

Audit disk first (sidecar `kartu` field + manifest sha16 + PNG mtimes distinguish
already-published-by-this-card vs old bytes), then steer: state map (N done, exact sha16,
which ids still old bytes), the specific defect list per failing id with coordinates, the
new mandatory checks (K5/K6 + six-point vision), publish-per-id anti-loss rule, and a
budget-priority order when <50% window remains. Unblock (`hermes kanban unblock`) after
`gave_up` — dispatcher's "will retry" does NOT fire while status=blocked; verify
status=ready in the same turn.

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
1. manifest -> disk: tiap berkas yang DISEBUT entri (png/svg/spek/sidecar + sha256 + ukuran) harus ADA dan hash-nya cocok. Entri menyebut PNG yang tak ada di disk = ENTRI TANPA BERKAS (preseden FG2: 4 id ditahan publikasinya tapi manifest mengklaim lahir lengkap dengan sha256 - bahaya fatal untuk RAKIT bind-register). Id tertahan masuk blok 'ditahan' berstatus eksplisit.
2. disk -> manifest: tiap berkas kelas itu di folder terbit harus disebut sebuah entri (nol yatim).
- Pitfall parser pengawas: kunci hash bisa bersarang (`berkas.png.sha256`, `sha256_png`) - asumsi kunci datar menghasilkan '12 hantu' palsu sebelum dibaca struktur sebenarnya. Baca item0 dulu.
- Gerbang RAKIT: manifest-final == cermin byte disk, butir per butir.

## Kanonisasi jalur output saat kartu dicetak (palang dua-folder)

Blueprint yang tidak menetapkan folder terbit membuat kartu paralel berimprovisasi: figurb (steer controller) vs figuran (warisan nama v1.0) - 48 id kolisi, 82 berkas identik, 29 beda-byte, pasangan dash-vs-titik (G10-3 vs G10.3) dalam satu folder. Rezim kanonis: satu folder terbit tunggal; gudang kerja terpisah; merge deterministik sebelum rakit (identik lewati, beda-byte pakai byte tervonis kecuali ada visus LAYAK lebih baru, normalkan dash->titik, manifest cermin). Keputusan jalur WAJIB tertulis di badan kartu sejak dicetak.

## Pitfall alat pengawas (self-corrections giliran ini)

- `sha1sum` di shell vs pin ledger sha256[:16]: memberi kecerokan 'pin bergeser' PALSU pada berkas yang tak tersentuh. Ukur dengan ALGORITME SAMA seperti pin ledger (hashlib.sha256[:16]) sebelum menyimpulkan revisi.
- Mtime + ukuran + pin bersama-sama membuktikan 'berkas tak tersentuh'; salah satu saja bisa menipu.
- Kata 'CAPTIONS' bisa muncul 2x per berkas (blok kanonis + disebut di blok Jejak perakitan yang dibuang saat rakit): gerbang kanal caption menghitung BERKAS blok, bukan kata.
