---

name: cad-drawing-standards
description: >
  STANDAR GAMBAR bersama untuk seluruh ekosistem skill CAD bangunan — layer &
  warna semua disiplin (A/S/E/P/M/I), tinggi teks per skala, gaya dimensi, kop
  gambar, penomoran lembar, simbol, dan boilerplate skrip ezdxf yang dipakai
  ulang. GUNAKAN (baca) skill ini SETIAP KALI akan menghasilkan gambar CAD /
  skrip DXF / perintah AutoCAD dari skill disiplin mana pun — jangan mengarang
  layer atau tinggi teks sendiri. Juga gunakan saat pengguna bertanya soal
  standar gambar, layer, kop, skala, atau penamaan berkas gambar.
  Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.0
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.2 SPEK-DETAIL-B02 / IMP-B; delta v1.4 CAD-IMPROVE-01 tema cetak CT + tegakan tinggi teks)
  gsp-owner-profile: gsp-architecture-specialist
  gsp-relations: [gsp-design-system-grill, gsp-architecture-bim-deliverables, ezdxf-mcp:make_dxf, gsp-document-quality-standards]
  author: gemilangsatriaperkasa.eng@gmail.com
  ecosystem: cad-building-suite (7 skill) — dirujuk oleh semua skill penghasil gambar
---

# CAD Drawing Standards — Standar Gambar Bersama

Skill ini adalah SATU-SATUNYA sumber kebenaran untuk bentuk gambar. Skill disiplin
menentukan ISI (apa yang digambar); skill ini menentukan BENTUK (layer, warna,
teks, dimensi, kop). Konsistensi lintas lembar lebih penting daripada selera.

## 1. Aturan dasar

- **Satuan model: milimeter.** 1 unit gambar = 1 mm.
- **Origin (0,0)** = perpotongan grid A-1 (pojok kiri-bawah denah). SEMUA disiplin
  memakai origin yang sama — inilah yang membuat gambar bisa di-overlay (XREF).
- Format DXF: R2010 (`ezdxf.new("R2010", setup=True)`).
- Utara selalu ke atas pada denah; bila tidak, wajib simbol panah utara.
- Satu berkas DXF = satu lembar gambar. Nama berkas = `<No>_<judul_snake>.dxf`,
  contoh `A-02_denah_lantai_1.dxf`.

## 2. Layer standar seluruh disiplin

Format nama: `<DISIPLIN>-<ELEMEN>`. Warna = ACI (AutoCAD Color Index).

### Umum (semua lembar)
| Layer | Isi | ACI | Linetype |
|-------|-----|-----|----------|
| X-GRID | garis as + lingkaran label grid | 8 | CENTER |
| X-DIM | dimensi | 2 | CONTINUOUS |
| X-TEXT | label & notasi | 7 | CONTINUOUS |
| X-KOP | kop & bingkai lembar | 7 | CONTINUOUS |
| X-HATCH | arsiran umum | 8 | CONTINUOUS |

### Arsitektur (A-…)
| Layer | Isi | ACI | Linetype |
|-------|-----|-----|----------|
| A-DINDING | dinding (garis ganda, arsir solid untuk potong) | 7 | CONTINUOUS |
| A-PINTU | daun + ayunan pintu | 4 | CONTINUOUS |
| A-JENDELA | kusen + kaca jendela | 5 | CONTINUOUS |
| A-TANGGA | anak tangga, arah naik | 6 | CONTINUOUS |
| A-SANITER | kloset, wastafel, bak | 5 | CONTINUOUS |
| A-ATAP | garis atap / talang | 30 | DASHED |
| A-BATAS | batas persil, GSB | 1 | PHANTOM |
| A-FURNITUR-REF | furnitur bayangan (referensi) | 8 | CONTINUOUS |

### Struktur (S-…)
| Layer | Isi | ACI | Linetype |
|-------|-----|-----|----------|
| S-KOLOM | penampang kolom (arsir solid) | 1 | CONTINUOUS |
| S-BALOK | tepi balok | 4 | CONTINUOUS |
| S-BALOK-HID | balok tersembunyi di bawah pelat | 4 | HIDDEN |
| S-PELAT | batas & notasi pelat | 3 | CONTINUOUS |
| S-FONDASI | telapak / pile cap | 30 | DASHED |
| S-TULANGAN | tulangan pada detail | 1 | CONTINUOUS |

### Elektrikal (E-…) · Plumbing (P-…) · Mekanikal (M-…)
| Layer | Isi | ACI | Linetype |
|-------|-----|-----|----------|
| E-LAMPU | titik lampu + simbol | 2 | CONTINUOUS |
| E-KOTAK | stop kontak & saklar | 2 | CONTINUOUS |
| E-KABEL | jalur grup / konduit | 2 | DASHED |
| E-PANEL | panel MCB | 1 | CONTINUOUS |
| P-BERSIH | pipa air bersih | 5 | CONTINUOUS |
| P-KOTOR | pipa air kotor & bekas | 6 | DASHED |
| P-VENT | pipa vent | 6 | DOT |
| P-HUJAN | talang & pipa hujan | 4 | DASHDOT |
| M-AC | unit AC + jalur refrigeran | 3 | CONTINUOUS |
| M-VENT | exhaust / fresh air | 3 | DASHED |

### Interior (I-…)
| Layer | Isi | ACI | Linetype |
|-------|-----|-----|----------|
| I-FURNITUR | furnitur lepas | 6 | CONTINUOUS |
| I-BUILTIN | furnitur built-in | 30 | CONTINUOUS |
| I-PLAFON | pola & drop plafon | 8 | DASHED |
| I-LANTAI | pola lantai / start point | 8 | CONTINUOUS |
| I-FINISH | notasi material dinding | 7 | CONTINUOUS |

## 3. Teks & dimensi

Tinggi teks pada MODEL (mm) agar tercetak benar:

| Kegunaan | Cetak | Skala 1:100 | 1:50 | 1:20 |
|----------|-------|-------------|------|------|
| Judul lembar | 5,0 mm | 500 | 250 | 100 |
| Sub-judul / nama ruang | 3,5 mm | 350 | 175 | 70 |
| Label elemen & dimensi | 2,5 mm | 250 | 125 | 50 |
| Notasi kecil | 2,0 mm | 200 | 100 | 40 |

Tegakan kelas tinggi teks (delta v1.4; tabel kelas terkunci blueprint
CAD-IMPROVE-01 seksi 5.6/HG-IMP-6):

- Label utama (nama ruang): 350 pada 1:100 (= 3,5 mm cetak).
- Sub-label / notasi isi / dimensi: >= 250 pada 1:100 (= 2,5 mm cetak).
- Notasi kecil >= 200 HANYA pada layer whitelist: `X-KOP`, `X-LEGEND`,
  `catatan_schedule`.
- 200 mm di layer konten = PELANGGARAN (vonis FAIL, bukan INFO).
- Floor absolut 200 di mana pun; tidak ada teks di bawahnya pada semua kasus.
- Skala selain 1:100: semua angka dikali faktor skala cetak yang dibaca dari kop.
- Pelanggaran == 0; whitelist yang terpakai wajib tercatat eksplisit di laporan
  (target paket baru = 0 whitelist). Distribusi B-02 (200 mm x140) tidak pernah
  dilegalkan kelasnya dan menjadi fixture merah HG-IMP-6.

Gaya dimensi (override ezdxf — WAJIB, memperbaiki faktor skala bawaan):

```python
DIM_OVR = {"dimtxt": 250, "dimasz": 150, "dimexo": 100, "dimexe": 100,
           "dimgap": 60, "dimdec": 0, "dimclrd": 2, "dimclrt": 2, "dimlfac": 1}
```

`dimlfac=1` penting: tanpa ini dimstyle bawaan ezdxf mencetak nilai ×100.
Untuk skala selain 1:100, kalikan dimtxt/dimasz/dimexo/dimexe/dimgap proporsional.

Rantai dimensi denah: baris 1 (terdekat) antar as; baris 2 total. Jarak baris
pertama dari objek ±1200 mm (skala 1:100), antar baris ±800 mm.

## 4. Skala baku per jenis gambar

| Gambar | Skala |
|--------|-------|
| Situasi / block plan | 1:200 – 1:500 |
| Denah, tampak, potongan | 1:100 (bangunan kecil boleh 1:50) |
| Denah per ruang / KM-WC | 1:50 |
| Detail struktur & interior | 1:20 (sambungan 1:10) |
| Diagram (satu garis, isometri, riser) | NTS — tanpa skala |

## 5. Kop gambar (title block)

Letak: strip bawah lembar, tinggi cetak 30 mm. Isi minimum, kiri → kanan:

```
[NAMA PROYEK] | [JUDUL GAMBAR] | No: [A-02] Rev: [0] | Skala: [1:100] |
Tgl: [YYYY-MM-DD] | Digambar: [AI-preliminary] | Diperiksa: [_______] |
Status: PRELIMINARY — BUKAN UNTUK KONSTRUKSI
```

Kolom "Diperiksa" sengaja kosong — diisi manusia. Status wajib tercetak di
setiap lembar; jangan pernah menghilangkannya.

### 5.1 Kontrak lembar v1.2 (SPEK-DETAIL-B02 seksi 5)

Delta v1.2 (kartu FIX-V12): aturan normatif sheet contract berikut mengikat
SEMUA lembar DXF paket dari disiplin mana pun. Aturan lama seksi 1 tentang
panah utara diperkuat menjadi norma penuh di sini.

- Kertas: A1 lanskap 841 x 594 mm cetak; pada model 1:100 = 84.100 x 59.400
  unit. Bingkai: margin kiri 25 mm cetak, lainnya 10 mm; garis bingkai dalam
  pada layer X-KOP continuous.
- Kop: strip bawah kanan, lebar 180 mm cetak, tinggi 30 mm; WAJIB 9 field:
  nama proyek, judul gambar, No lembar, Rev, Skala, Tanggal (YYYY-MM-DD),
  Digambar (AI-preliminary), Diperiksa (KOSONG, diisi manusia), Status
  `PRELIMINARY - BUKAN UNTUK KONSTRUKSI`. Pola cetak di atas hanyalah ringkasan
  susunan 9 field yang sama; tidak ada field yang boleh hilang.
- Panah utara: WAJIB pada semua denah + situasi dengan teks `UTARA` (h=5 mm cetak); panah panjang 30 mm cetak; utara model = +Y; bila denah diputar, panah mengikuti rotasi sebenarnya.
- Daftar gambar: lembar `A-00_daftar_gambar` WAJIB ada; tabel (kode, judul,
  skala, ukuran kertas, status) dengan JUMLAH BARIS == jumlah lembar DXF paket
  == jumlah halaman PDF.
- Grid referensi: bubble grid di EMPAT sisi lembar (huruf arah X, angka arah
  Y; lingkaran r=400 @1:100 pada X-GRID; jarak bubble antar sisi simetris);
  kode zona `<huruf><angka>` (A1..E6) dipakai di laporan dan notasi silang.
- Penamaan berkas: `<No>_<judul_snake>.dxf` (aturan lama) ditegaskan berlaku
  juga untuk A-00.

## 6. Simbol baku

- **Grid**: lingkaran r=400 (1:100) di ujung as; huruf arah X, angka arah Y.
- **Pintu**: garis daun + busur ayun 90°; label P1, P2… dekat bukaan.
- **Jendela**: 3 garis sejajar dalam tebal dinding; label J1, J2…
- **Titik lampu**: lingkaran r=150 dengan silang; downlight = lingkaran ganda.
- **Stop kontak**: setengah lingkaran r=120 di dinding + 1 garis; saklar = "S"
  dengan garis miring (S2 = ganda).
- **Arah naik tangga**: garis putus + panah + teks "NAIK".
- **Potongan**: garis PHANTOM tebal + kepala panah + label lingkaran (mis. A→A).
- **AC indoor**: persegi 800×250 di dinding; outdoor: persegi + kipas.
- **Kloset/wastafel**: pakai blok geometri sederhana (elips + persegi), bukan detail.

## 7. Boilerplate ezdxf (pakai ulang — jangan tulis ulang dari nol)

```python
import ezdxf
from ezdxf.enums import TextEntityAlignment

def new_sheet(layers):
    """layers: list of (name, aci_color, linetype)."""
    doc = ezdxf.new("R2010", setup=True)
    for name, color, lt in layers:
        doc.layers.add(name, color=color, linetype=lt)
    return doc, doc.modelspace()

def text(msp, s, pos, h=250, layer="X-TEXT",
         align=TextEntityAlignment.MIDDLE_CENTER, rotation=0):
    msp.add_text(s, height=h, dxfattribs={"layer": layer, "rotation": rotation}
                 ).set_placement(pos, align=align)

def rect(msp, cx, cy, w, h, layer, hatch=False):
    pts = [(cx-w/2, cy-h/2), (cx+w/2, cy-h/2), (cx+w/2, cy+h/2), (cx-w/2, cy+h/2)]
    msp.add_lwpolyline(pts, close=True, dxfattribs={"layer": layer})
    if hatch:
        hh = msp.add_hatch(dxfattribs={"layer": layer})
        hh.paths.add_polyline_path(pts, is_closed=True)

def draw_grid(msp, grid_x, grid_y, margin=1200):
    xmax, ymax = max(grid_x.values()), max(grid_y.values())
    for g, x in grid_x.items():
        msp.add_line((x, -margin), (x, ymax+margin), dxfattribs={"layer": "X-GRID"})
        msp.add_circle((x, -margin-500), 400, dxfattribs={"layer": "X-GRID"})
        text(msp, g, (x, -margin-500))
    for g, y in grid_y.items():
        msp.add_line((-margin, y), (xmax+margin, y), dxfattribs={"layer": "X-GRID"})
        msp.add_circle((-margin-500, y), 400, dxfattribs={"layer": "X-GRID"})
        text(msp, g, (-margin-500, y))

def dim_chain(msp, points, base_offset, horizontal=True, ovr=None):
    ovr = ovr or {"dimtxt":250,"dimasz":150,"dimexo":100,"dimexe":100,
                  "dimgap":60,"dimdec":0,"dimlfac":1}
    for p1, p2 in zip(points[:-1], points[1:]):
        if horizontal:
            d = msp.add_linear_dim(base=(0, base_offset), p1=(p1, base_offset-1000),
                                   p2=(p2, base_offset-1000), dimstyle="EZDXF",
                                   override=ovr, dxfattribs={"layer": "X-DIM"})
        else:
            d = msp.add_linear_dim(base=(base_offset, 0), p1=(base_offset-1000, p1),
                                   p2=(base_offset-1000, p2), angle=90, dimstyle="EZDXF",
                                   override=ovr, dxfattribs={"layer": "X-DIM"})
        d.render()

def title_block(msp, no, judul, proyek, skala="1:100", x_center=0, y=-3500):
    text(msp, f"{no}  {judul}", (x_center, y), h=400)
    text(msp, f"{proyek} - PRELIMINARY - BUKAN UNTUK KONSTRUKSI - {skala} (mm)",
         (x_center, y-600), h=200)
```

Aturan pemakaian: skill disiplin mengimpor pola ini apa adanya, menambah fungsi
gambar spesifiknya sendiri (pintu, simbol lampu, dst.) di atasnya.

## 8. Kontrol kualitas gambar (cek sebelum menyimpan DXF)

- [ ] Semua entitas berada pada layer yang benar — TIDAK ADA entitas di layer "0"
- [ ] Grid & origin identik dengan gambar disiplin lain di proyek yang sama
- [ ] Ada minimal 2 rantai dimensi (antar-as + total) pada setiap denah
- [ ] Semua elemen berlabel sesuai kode schedule-nya
- [ ] Tinggi teks sesuai tabel skala
- [ ] Kop memuat status PRELIMINARY
- [ ] Nama berkas sesuai pola `<No>_<judul>.dxf`
- [ ] 0 pasangan teks tumpang tindih (definisi HG-NEW-1: inflate bbox teks 0,5 x tinggi sendiri; pasangan beda `grup` tidak boleh berpotongan pada SETIAP lembar)
- [ ] 0 teks memotong geometri (definisi HG-NEW-2: bbox teks tanpa inflate tidak memotong segmen gangguan; pengecualian hanya ZL-8)
- [ ] Rantai dimensi tutup: |sum(ordo-2) - ordo-3| <= 1 mm per arah X dan Y (aturan R3; ordo-1 == lebar bukaan schedule)
- [ ] (v1.4) 0 pelanggaran kelas tinggi teks per skala (tabel seksi 3; whitelist tercatat, target 0)
- [ ] (v1.4) 0 pelanggaran tema cetak CT-1..CT-3: semua layer punya pemetaan warna cetak eksplisit, ColorPolicy konverter eksplisit, latar putih


---

## Seksi 9 — Aturan numerik penempatan teks & rantai dimensi (v1.2)

Delta v1.2 dari SPEK-DETAIL-B02 (CAD-SWARM-01, kartu IMP-B). Seksi ini membuat
aturan yang dulu ad-hoc menjadi terukur; sumber kebenaran penempatan = kontrak
zona label per lembar di `spek_elemen.zona_label[]` (milik cad-architecture-design
KSPE-2b), bukan keputusan saat menggambar.

### 9.1 Jarak bebas teks (ZL-4 dan turunannya)

- ZL-4: jarak bersih antara bbox dua teks mana pun pada lembar yang sama
  >= 1,0 x tinggi teks TERBESAR dari pasangan itu. Implementasi uji: inflate bbox
  tiap teks ke luar sebesar 0,5 x tingginya sendiri; dua bbox ter-inflate tidak
  boleh berpotongan (untuk tinggi sama h ini persis berarti gap >= h).
- ZL-5: teks dimensi (blok DIMENSION) ikut pool ZL-4; teks dimensi boleh berimpit
  dengan garis ekstensi/garis dimensi MILIKNYA SENDIRI, tidak dengan entitas lain.
- ZL-7: pengecualian HANYA (a) teks dalam satu blok label grup sama (kolom `grup`
  sama), (b) label grid di dalam lingkaran bubble-nya. Tidak ada pengecualian lain.
- ZL-3/ZL-8: jarak bebas bbox label ke dinding/bukaan/furnitur terdekat >= 300 mm;
  teks furnitur boleh di DALAM bbox furnitur bila termuat penuh dengan margin
  >= 100 mm dari tepi bbox furnitur.
- Larangan memotong entitas: bbox teks (tanpa inflate) tidak boleh memotong segmen
  gangguan geometri (LINE/LWPOLYLINE/POLYLINE/SPLINE/ARC/CIRCLE, tepi bbox INSERT,
  geometri virtual DIMENSION) pada layer A-DINDING, A-PINTU, A-JENDELA, A-TANGGA,
  A-SANITER, A-ATAP, A-BATAS, S-*, E-*, P-*, M-*, I-FURNITUR, I-BUILTIN, I-PLAFON,
  I-LANTAI, X-DIM, X-KOP. DIKECUALIKAN X-GRID, X-HATCH, A-FURNITUR-REF dan kasus
  ZL-8. Verifikasi oleh gerbang HG-NEW-2; angka target: 0 pelanggaran per lembar.

### 9.2 Estimasi lebar teks deterministik (ZL-6)

TEXT: pakai fungsi lebar font ezdxf (`ezdxf.tools.text.text_size` dengan font
standar, width factor `dxf.width` default 1.0); fallback = 0,70 x tinggi x jumlah
karakter setelah strip. MTEXT: lebar kolom tetap bila `width` > 0, selain itu
estimasi baris terpanjang. Teks rotasi: bbox = AABB dari extent terotasi.

### 9.3 Band offset ordo rantai dimensi

Mengganti aturan dua baris lama (yang tetap benar sebagai kasus ordo 1-2):
ordo-1 offset 1200 mm, ordo-2 offset 2000 mm, ordo-3 offset 2800 mm dari objek
(skala 1:100; skala lain dikali faktor skala cetak; antar baris 800 mm). Tinggi
teks dimensi 250 (model mm @1:100). Klasifikasi entitas hasil ukur: band offset
+-200 mm. Denah wajib punya KETIGA ordo terisi dan rantai tertutup
(|sum(ordo-2) - ordo-3| <= 1 mm per arah).

### 9.4 Ambang jumlah dimensi per jenis lembar

Denah lantai 1:100: >= max(20, (Nx-1)+(Ny-1)+2+N_bukaan_lantai); situasi >= 8;
tampak >= 2*n_lantai + 4; potongan >= 10; detail 1:50 / 1:20 >= 6; denah disiplin
lain (S/E/P/M/I) >= 8; diagram dibebaskan HANYA bila teks `NTS` ada di lembar
disertai legendar berukuran. Isi rinci per jenis: cad-architecture-design KSPE-2c.

### 9.5 Boilerplate helper label-zone (pakai ulang — jangan tulis ulang dari nol)

```python
def est_text_width(s, h, width_factor=1.0):
    """Estimasi lebar TEXT satu baris (fallback ZL-6)."""
    return 0.70 * h * len(s.strip()) * width_factor

def text_bbox(pos, s, h, rotation=0.0, width_factor=1.0):
    """AABB teks: pusat `pos`, lebar estimasi ZL-6, tinggi h; rotasi -> AABB extent."""
    import math
    w = est_text_width(s, h, width_factor)
    if abs(rotation) < 1e-9:
        return (pos[0]-w/2, pos[1]-h/2, pos[0]+w/2, pos[1]+h/2)
    c, s_ = math.cos(math.radians(rotation)), math.sin(math.radians(rotation))
    xs = [pos[0] + (dx*c - dy*s_) for dx, dy in
          ((-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2))]
    ys = [pos[1] + (dx*s_ + dy*c) for dx, dy in
          ((-w/2,-h/2),(w/2,-h/2),(w/2,h/2),(-w/2,h/2))]
    return (min(xs), min(ys), max(xs), max(ys))

def inflate(bb, k):
    """Inflate bbox ke luar sebesar k (ZL-4 memakai k = 0,5 x tinggi teks sendiri)."""
    return (bb[0]-k, bb[1]-k, bb[2]+k, bb[3]+k)

def bbox_overlap(a, b):
    """True bila dua bbox berpotongan (irisan luas > 0)."""
    return not (a[2] <= b[0] or b[2] <= a[0] or a[3] <= b[1] or b[3] <= a[1])

def zl4_violations(items):
    """items: [(id, bbox, tinggi, grup)]. Kembalikan pasangan melanggar ZL-4/ZL-7."""
    inf = [(i, inflate(bb, 0.5*h), g) for i, bb, h, g in items]
    out = []
    for a in range(len(inf)):
        for b in range(a+1, len(inf)):
            if inf[a][2] == inf[b][2]:      # ZL-7 (a): grup sama dikecualikan
                continue
            if bbox_overlap(inf[a][1], inf[b][1]):
                out.append((inf[a][0], inf[b][0]))
    return out
```

Catatan: fungsi ini alat BANTU penempatan saat menggambar; gerbang verifikasi
resmi (HG-NEW-1/HG-NEW-2) memakai parser independen dari skrip pembuat gambar —
jangan memakai helper ini untuk memvonis hasil sendiri.

---

## Seksi 10 - Tema cetak CT (delta v1.4, CAD-IMPROVE-01; kartu t_909162a4)

Delta v1.4 dari blueprint `docs/2026-09-07-cad-improvement/identification/02_structured.md`
seksi 3.2 kelompok A. Akar defect B-02 (BL-01): PDF set gambar B-02 dicetak dengan
warna warisan tema gelap sehingga teks nyaris hilang di atas latar putih. Aturan lama
tetap utuh; seksi ini menutup jalur defect-nya. Kop gambar dan daftar gambar TETAP
seperti kontrak lama (seksi 5 / 5.1) - yang diatur di sini hanya warna cetaknya.

### CT-1 Pemetaan layer -> warna cetak (eksplisit)

Konten dominan HITAM/GELAP di atas latar PUTIH. DILARANG: warna default tema gelap,
ACI terang (7 putih, 6 magenta, 3 hijau neon, dst.) tanpa pemetaan, dan BYLAYER tanpa
pemetaan eksplisit di atas latar putih. Tabel pemetaan wajib ditulis sebelum konversi:

```text
layer (contoh)        | warna cetak | ACI cetak
A-DINDING, S-KOLOM, dll | hitam     | 7->hitam via plot (monochrome) atau ACI 250-256
X-KOP, X-GRID         | hitam       | idem
annotasi teks         | hitam       | 250/7 dipetakan hitam
highlight sengaja     | gelap saja  | merah tua/biru tua, kontras >= ambang CT-3
```

### CT-2 Resep konverter DXF -> PDF

ColorPolicy EKSPLISIT: `MONOCHROME` atau peta warna manual satu-per-satu; latar putih;
jangan mengandalkan style table bawaan. Konverter WAJIB mencatat policy yang dipakai
di log pembuatan PDF.

### CT-3 Uji diri raster sebelum serah terima

Render 1 halaman pada 150 DPI RGB, ukur kontras tiap klaster teks dengan rasio
luminansi WCAG `(L1+0,05)/(L2+0,05)` (L relatif sRGB-linear): teks normal >= 4,5:1;
teks tinggi cetak >= 3,5 mm >= 3,0:1. Lulus = 0 klaster di bawah ambang. Detektor
wajib terkalibrasi MERAH pada PDF asli paket lama yang cacat dan HIJAU pada fixture
bersih sebelum dipakai menilai paket baru.

---

## Runtime GSP (host Windows ini)

Hasil adaptasi CAD-SWARM-01; sumber angka MCP-RISIK.md (smoke terverifikasi 2026-09-04).

- DXF: jalankan skrip ezdxf dengan `uv run --python 3.11 --with ezdxf python <skrip>.py`
  (ezdxf 1.4.4 terverifikasi; DXF R2010/AC1024; `$INSUNITS=4` mm sesuai skema PROJECT.json).
- MCP DXF: tool `make_dxf` dari ezdxf-mcp built-owned lewat
  `uv run --python 3.11 --with ezdxf python C:/Users/TRIAL/workspace/CAD/tools/mcp/ezdxf-mcp/server.py`
  (stdio JSON-RPC newline-delimited; terdaftar pada profil arch/3d/master per kartu MCP-6).
- Render 3D kanonik: Blender portable absolut
  `C:/Users/TRIAL/workspace/CAD/tools/blender-4.2.9-windows-x64/blender.exe -b -P <skrip>.py`
  (headless bpy; engine final CYCLES; serial rule maksimum 1 proses Cycles fleet-wide).
- blender-mcp opsional interaktif (butuh GUI + addon TCP 9876): `uvx blender-mcp` (v1.9.1)
  dengan addon `C:/Users/TRIAL/workspace/CAD/tools/mcp/blender-mcp/addon.py`; jalur benchmark
  tetap `blender -b -P` dan tidak bergantung padanya.
- Host ini TIDAK memasang AutoCAD desktop: rujukan "perintah AutoCAD" di badan skill dibaca
  sebagai permintaan teks urutan perintah saja, sedangkan jalur eksekusi nyata gambar adalah
  skrip ezdxf atau tool MCP `make_dxf` di atas. DILARANG mengunduh Blender baru (D-02).

---

## Relasi skill GSP

Profil pemilik: `gsp-architecture-specialist` | Konsumen wajib: SEMUA penghasil gambar: arch, engineering-analyst, power, 3d | Tier: ALWAYS (arch, 3d)

- `gsp-design-system-grill` + paket token `MASTER_DESIGN`: kop gambar & identitas visual lembar.
- `gsp-architecture-bim-deliverables`: skala-garis-notasi, daftar set gambar.
- MCP `ezdxf-mcp` tool `make_dxf`: jalur produksi DXF di host ini (D-03/D-05).
- `gsp-document-quality-standards`: mutu teks label.

## Hook pelaporan GSP

Saat skill ini dipakai dalam misi GSP, append blok laporan ke
`docs/2026-09-04-cad-swarm-integration/PHASE-REPORTS.md` dengan format
`[FASE] CAD-SWARM-01 | <fase> | <waktu>` plus baris RINGKAS/ARTEFAK/JALUR/RENCANA,
simpan artefak tugas ke `docs/YYYY-MM-DD_<task>/`, dan jangan pernah menulis ke `/output`.

## Gerbang mutu GSP (SPK-002)

- Field beban-rilis (nama entitas, angka, tanggal, tautan, kontak) diverifikasi deterministik
  100% sebelum rilis; hyperlink pada keluaran wajib aktif dan terlihat (warna tegas + garis bawah).
- Kosong lebih baik daripada salah: identifier tak terverifikasi dikosongkan lalu dicatat di register.
- Angka teknis wajib bertanda rujukan EKAS `[R-n, sumber, hal]` lewat `pustaka-teknis` (aturan R1-R5);
  disclaimer preliminary design dari sumber tetap berlaku di semua keluaran disiplin.
