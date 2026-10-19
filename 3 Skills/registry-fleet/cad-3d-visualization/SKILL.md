---

name: cad-3d-visualization
description: >
  Penerjemah rancangan menjadi VISUALISASI 3D — mengubah data PROJECT.json
  (dinding, bukaan, tangga, furnitur, titik lampu, finish material) menjadi model
  3D dan render gambar perspektif, melalui skrip Blender Python (bpy, headless),
  MAXScript (3ds Max), atau ekspor OBJ/glTF. GUNAKAN skill ini setiap kali
  pengguna menyebut: render, 3D, visualisasi, perspektif, "seperti apa jadinya",
  tampilan realistis, material/tekstur 3D, walkthrough, Blender, bpy, 3ds Max,
  MAXScript, V-Ray/Cycles/Eevee, SketchUp, "buatkan gambar 3D interior/eksterior"
  — bahkan bila kata "visualisasi" tidak disebut. Gambar teknik 2D tetap di skill
  disiplin masing-masing; skill ini hanya MEMPERLIHATKAN hasilnya secara 3D.
  Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.1
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.2 SPEK-DETAIL-B02 / IMP-B; delta v1.3 K-1a+K-1b2 CAD-SWARM-01; delta v1.4 CAD-IMPROVE-01 kelengkapan arsitektural AR + dual-output DO)
  gsp-owner-profile: gsp-3d-specialist
  gsp-relations: [pustaka-teknis, gsp-design-system-grill, blender-mcp, gsp-verification-before-completion]
  author: gemilangsatriaperkasa.eng@gmail.com
  ecosystem: cad-building-suite (8 skill) — membaca hampir semua bagian PROJECT.json,
    menulis bagian `visualisasi`
  dependensi: Blender >= 3.6 (gratis, render headless) untuk jalur utama;
    3ds Max opsional untuk jalur MAXScript
---

# CAD 3D Visualization — Dari Data Rancangan ke Render

Kamu adalah asisten visualisasi arsitektur. Tugasmu MENERJEMAHKAN, bukan mendesain
ulang: setiap dinding, pintu, anak tangga, dan lampu di model 3D harus berasal
dari data PROJECT.json yang sudah diputuskan disiplin lain. Jika data kurang
(mis. finish belum ditentukan), terbitkan REVISI-REQ ke skill pemiliknya —
jangan mengarang geometri sendiri.

Prinsip:
1. **Satu sumber kebenaran.** Geometri dari PROJECT.json. Jika render tidak cocok
   dengan denah 2D, yang salah adalah skrip 3D — bukan denahnya.
2. **Satuan.** PROJECT.json memakai mm; Blender memakai METER. Konversi
   `mm / 1000` di SATU fungsi konversi — jangan tebar pembagian di mana-mana.
3. **Origin sama.** (0,0,0) = as A-1 elevasi ±0.00 — konsisten dengan semua DXF.
4. **Jujur soal kualitas.** Hasil otomatis = draft presentasi berbahan material
   dasar/prosedural. Fotorealisme penuh butuh pustaka tekstur & sentuhan manual —
   katakan itu, jangan menjanjikan hasil setara render artis.

## ALUR KERJA 6 TAHAP

### Tahap 1 — Pilih jalur & keluaran

| Jalur | Kapan dipakai | Eksekusi |
|-------|---------------|----------|
| **Blender bpy** (default) | otomatisasi penuh, render tanpa buka aplikasi | `blender -b -P skrip.py` |
| MAXScript | pengguna bekerja di 3ds Max & akan menyunting manual | jalankan dari 3ds Max > Scripting |
| Ekspor OBJ/glTF | hanya butuh model utk dibuka di aplikasi lain | modul `obj` tulis manual / bpy export |

Tanyakan (atau default-kan): target ruang (interior lantai berapa / eksterior),
jumlah sudut kamera (default 2: satu lebar + satu detail), kualitas
(draft Eevee / final Cycles), resolusi (default 1920×1080).

### Tahap 2 — Konversi geometri (aturan per elemen)

Semua fungsi menerima data mentah PROJECT.json (mm) dan mengonversi internal.

| Elemen | Sumber data | Cara bangun |
|--------|-------------|-------------|
| Lantai/pelat | `ruang.poligon` atau bidang lantai | mesh datar di elevasi lantai; tebal 120 mm ke bawah |
| Dinding | `dinding` (dari, ke, tipe→tebal) | box sepanjang segmen: panjang × tebal × tinggi (elevasi lantai s.d. bawah pelat atas) |
| Bukaan | `bukaan` (dinding, posisi, lebar, tinggi) | boolean difference pada dinding; isi kusen = frame box 50 mm + kaca (material glass) utk jendela; pintu = panel 40 mm |
| Tangga | `tangga` (riser, tread, lebar, posisi) | loop box anak tangga: i × (tread, lebar, riser); bordes = box; railing = silinder Ø40 tiap 1 m + handrail |
| Kolom/balok | `elemen_struktur` | box sesuai dimensi & grid — tampilkan bila ekspos; sembunyikan yang tertutup plafon/dinding |
| Plafon | `ruang.tinggi_plafon` | bidang di elevasi plafon; drop/cove = box keliling −400 |
| Furnitur | `furnitur` (jenis, posisi, dimensi, rotasi) | primitif parametrik per jenis — tabel di bawah |
| Titik lampu | `titik_me` jenis lampu | light object + fixture kecil (silinder/emission) |

**Furnitur parametrik** (gabungan primitif — cukup meyakinkan pada jarak kamera normal):

| Jenis | Susunan primitif |
|-------|------------------|
| bed | box kasur (t=250 di atas box dipan 300) + headboard tipis + 2 bantal (box sudut membulat) |
| wardrobe/lemari | box penuh + garis pintu (inset 5 mm) + handle silinder |
| sofa | box dudukan + box sandaran + 2 box lengan |
| meja/kasir/workstation | box top t=30 + 4 kaki box/silinder |
| kursi | box dudukan + sandaran + 4 kaki |
| kitchen set | deret box modul 600 + top beda material + kabinet atas menggantung |
| rak/gondola | rangka box tipis + 3–4 rak papan |
| kloset | silinder + box tangki; wastafel = setengah bola + pedestal |
| tanaman pot (dekor) | kerucut/silinder pot + icosphere daun (material hijau) |

Modifier bevel kecil (5 mm) pada semua furnitur — sudut tajam sempurna terlihat
palsu di render.

### Tahap 3 — Material (mapping dari finish schedule interior)

Gunakan Principled BSDF. Tanpa pustaka tekstur → prosedural; jika pengguna punya
folder tekstur (`assets/`), pakai image texture + UV scale sesuai ukuran nyata
(granit 60×60 → scale 0.6 m).

| Finish (dari cad-interior-design) | Material dasar | Parameter kunci |
|-----------------------------------|----------------|-----------------|
| granit polished | abu terang | roughness 0.15, specular 0.6; noise ringan utk urat |
| keramik matt / R10 | krem | roughness 0.6; checker halus utk nat |
| vinyl SPC / parket | cokelat kayu | roughness 0.4; wave/musgrave utk serat |
| cat dinding | warna palet 60/30/10 | roughness 0.9 |
| kayu oak (furnitur) | oak hangat | roughness 0.45 |
| HPL | sesuai warna | roughness 0.5 |
| kaca | transmission 1.0 | roughness 0.05, IOR 1.45 |
| besi/railing | abu gelap | metallic 0.9, roughness 0.35 |
| beton ekspos | abu | roughness 0.85 + noise |
| rumput/tanah (eksterior) | hijau | particle/geometry nodes bila Cycles; plane hijau kasar utk draft |

Ambil warna dari palet interior (60/30/10) — jangan pilih warna sendiri.

### Tahap 4 — Pencahayaan & kamera

**Pencahayaan:**
- Eksterior: Sun (elevasi 35–55°, azimut dari orientasi tapak; kekuatan 3–5) +
  Nishita sky texture. Jam sore (aszimut barat) memberi bayangan menarik.
- Interior siang: cahaya masuk dari bukaan (sun + portal) + langit; JANGAN
  terangi interior hanya dengan lampu buatan di render siang.
- Interior malam / area tanpa jendela: pakai `titik_me` — tiap downlight = point
  light, kekuatan 300–800 lm ≈ 5–15 W Blender; temperatur warna dari skill
  interior (2700–3000 K hunian → RGB hangat; 4000 K retail → netral).
- Emission kecil pada fixture agar lampunya "terlihat menyala".
- RESEP K-1b2: fixture bermaterial emisi BUKAN sumber cahaya - ia hanya membuat
  bohlam terlihat menyala; uji wajib = ada >= 1 light object nyata per ruang
  tertutup (aturan L1/L2 di K3D-5). Emission tidak pernah menggantikan light
  object sebagai penerang ruang.

**Kamera (preset — pakai ini, jangan asal taruh):**

| Preset | Posisi | Lensa |
|--------|--------|-------|
| Interior eye-level | tinggi 1.5–1.6 m, di sudut ruang menghadap diagonal | 24 mm (ruang sempit) – 35 mm |
| Interior detail | 1.2–1.4 m, 1.5–2 m dari objek (kasir, kitchen set) | 50 mm |
| Eksterior three-quarter | tinggi 1.6 m, jarak ±1.5× tinggi bangunan, sudut 30–45° dari muka | 35 mm |
| Bird eye | di atas, melihat 45° | 50 mm |

WAJIB: `clip_start = 0.01` (ruang sempit), kamera tidak berada DI DALAM dinding/
furnitur, dan vertikal tegak (shift lens, bukan mendongak) untuk eksterior.

### Tahap 5 — Render

| Mode | Engine | Samples | Kapan |
|------|--------|---------|-------|
| Draft | Eevee | — | iterasi cek komposisi (< 10 dtk/frame) |
| Final | Cycles | 128–256 + denoise | presentasi |

Headless: `blender -b -P generate_3d.py` — skrip mengatur semua lalu
`bpy.ops.render.render(write_still=True)`. Simpan `render/<nama>_<preset>.png`.
SELALU render draft dulu, periksa (kamera nabrak dinding? material tertukar?
skala aneh?), baru final.

### Tahap 6 — QA & catat hasil

- [ ] Uji skala: tinggi pintu di render ≈ 2.1 m vs manusia 1.7 m (masukkan
  figur referensi box 1.7 m saat cek, hapus sebelum final)
- [ ] Denah kamera cocok dengan denah 2D (overlay top view vs A-0x)
- [ ] Tidak ada z-fighting (bidang berimpit — offset 1 mm)
- [ ] Semua bukaan berlubang benar (boolean sukses — cek dari dalam & luar)
- [ ] Jumlah & posisi lampu = titik_me (E-01..E-04)
- [ ] Setiap ruang tertutup punya >= 1 light object nyata (bukan hanya fixture
  emisi) - uji resep K-1b2; rinciannya K3D-5
- [ ] Material sesuai finish schedule (granit di lt1, vinyl di KT — bukan tertukar)
- [ ] Tulis ke PROJECT.json bagian `visualisasi`: daftar berkas render, preset
  kamera, engine, dan skrip pembangkitnya

## Kerangka skrip bpy (pola — kembangkan, jangan tulis dari nol)

```python
import bpy, math, json

M = lambda mm: mm / 1000.0                      # konversi mm -> m (SATU tempat)
data = json.load(open("PROJECT.json", encoding="utf-8"))

def clear():
    bpy.ops.object.select_all(action="SELECT"); bpy.ops.object.delete()

def mat(name, color, rough=0.8, metal=0.0):
    m = bpy.data.materials.get(name) or bpy.data.materials.new(name)
    m.use_nodes = True
    b = m.node_tree.nodes["Principled BSDF"]
    b.inputs["Base Color"].default_value = (*color, 1)
    b.inputs["Roughness"].default_value = rough
    b.inputs["Metallic"].default_value = metal
    return m

def box(name, cx, cy, cz, dx, dy, dz, material=None):
    bpy.ops.mesh.primitive_cube_add(location=(M(cx), M(cy), M(cz)))
    o = bpy.context.object
    o.name = name; o.scale = (M(dx)/2, M(dy)/2, M(dz)/2)
    if material: o.data.materials.append(material)
    return o

def wall(seg, tinggi, tebal, z0, m_wall):
    (x1, y1), (x2, y2) = seg["dari"], seg["ke"]
    L = math.hypot(x2-x1, y2-y1)
    o = box(seg["id"], (x1+x2)/2, (y1+y2)/2, z0 + tinggi/2, L, tebal, tinggi, m_wall)
    o.rotation_euler[2] = math.atan2(y2-y1, x2-x1)
    return o

def opening_cut(wall_obj, buk, z0):
    """Boolean lubang bukaan pada dinding (posisi mm dari ujung 'dari')."""
    cut = box("cut_"+buk["id"], 0, 0, 0, buk["lebar"], 400, buk["tinggi"])
    # ...posisikan cut pada dinding sesuai buk["posisi"], lalu:
    mod = wall_obj.modifiers.new("bool", "BOOLEAN")
    mod.operation = "DIFFERENCE"; mod.object = cut
    bpy.context.view_layer.objects.active = wall_obj
    bpy.ops.object.modifier_apply(modifier="bool")
    bpy.data.objects.remove(cut)

def tangga(t, z0, m_step):
    y = t["y0"]
    for i in range(t["riser_jumlah"]):
        box(f"step{i}", t["cx"], y + t["tread"]/2, z0 + (i+1)*t["tinggi_riser"] - t["tinggi_riser"]/2,
            t["lebar"], t["tread"], t["tinggi_riser"], m_step)
        y += t["tread"]

def kamera_interior(x, y, z, target):
    bpy.ops.object.camera_add(location=(M(x), M(y), M(z)))
    cam = bpy.context.object
    cam.data.lens = 24; cam.data.clip_start = 0.01
    # arahkan ke target dgn constraint TRACK_TO ke empty di posisi target
    bpy.context.scene.camera = cam
    return cam

def render(path, final=False):
    sc = bpy.context.scene
    sc.render.engine = "CYCLES" if final else "BLENDER_EEVEE_NEXT"
    if final: sc.cycles.samples = 192; sc.cycles.use_denoising = True
    sc.render.resolution_x, sc.render.resolution_y = 1920, 1080
    sc.render.filepath = path
    bpy.ops.render.render(write_still=True)
```

Catatan versi: Blender 4.x memakai `BLENDER_EEVEE_NEXT`; 3.x memakai
`BLENDER_EEVEE`. Deteksi via `bpy.app.version` bila perlu.

## Jalur MAXScript (alternatif, untuk pengguna 3ds Max)

> **WAJIB** sebelum build via MCP 3ds Max: muat skill `gsp-3dsmax-mcp-modeling`
> (katalog fungsi terbukti-gagal di host ini + resep terbukti-jalan + standar
> detail minimal objek). Jangan uji ulang fungsi yang sudah divonis mati di sana.


Prinsip sama, sintaks beda — hasilkan `.ms` berisi:
`Box length: width: height: pos:[x,y,z]` per elemen (3ds Max default satuan
sesuai System Units — set `units.SystemType = #millimeters` di awal skrip agar
data mm dipakai langsung tanpa konversi), material `PhysicalMaterial`,
`Physical Camera` + `Sun Positioner`. Pengguna menjalankan lewat
Scripting > Run Script, lalu menyempurnakan material/tekstur secara manual —
di sinilah keahlian 3ds Max pengguna melengkapi keluaran otomatis.

## Integrasi ekosistem

- MEMBACA: `proyek`, `grid`, `elevasi`, `ruang`, `dinding`, `bukaan`, `tangga`,
  `elemen_struktur`, `furnitur`, `titik_me`, palet & finish (interior).
- MENULIS: hanya `visualisasi` (daftar render + preset + path skrip).
- Data kurang → REVISI-REQ ke skill pemilik (mis. "furnitur R-201 belum ada"
  → cad-interior-design). Jangan menambah furnitur karangan sendiri.

## Batasan (sampaikan di awal ke pengguna)

- Hasil otomatis = **draft presentasi** berbahan material dasar; fotorealisme
  (tekstur batu alam, rumput 3D, pot bunga detail seperti contoh referensi)
  butuh pustaka aset + penyempurnaan manual di Blender/3ds Max.
- Tidak mencakup: animasi walkthrough (bisa ditambah kemudian — keyframe kamera),
  simulasi pencahayaan fotometrik akurat (ranah kajian pencahayaan), VR.
- Butuh Blender terpasang di mesin eksekusi; tanpa itu, jatuhkan ke jalur
  ekspor OBJ + beri tahu pengguna cara membukanya.


---

## Kontrak 3D & image-gen (v1.2 — SPEK-DETAIL-B02 seksi 6-7)

Delta v1.2 dari SPEK-DETAIL-B02 (CAD-SWARM-01, kartu IMP-B). Temuan B-01:
komposisi kamera benar tetapi eksekusi material/cahaya salah, dan image-gen
inkonsisten massa karena referensi hanya satu sudut. Solusi: kamera dan material
kini DIKUNCI di spesifikasi sebelum build scene; skill ini bekerja HANYA dari KSPE
lengkap (`spek_elemen` + field visualisasi di bawah) — kurang satu seksi =
REVISI-REQ balik ke arsitektur, bukan menebak.

### K3D-1 Spesifikasi kamera per sudut (field wajib `visualisasi.kamera_preset[]`)

Setiap sudut render final ditentukan SEBELUM build scene, minimal 4 sudut
(preseden P-11; menggantikan default lama "2 sudut"). Field WAJIB per kamera:
`nama, jenis, lokasi_mm[3], target_mm[3], lensa_mm, sensor_mm (36),
tinggi_mata_mm, shift_y, clip_start_m (0.01), resolusi [1920,1080],
engine_final (CYCLES)`. Preset dasar (kalibrasi temuan juri B-01):

| Sudut | lokasi | target | lensa | tinggi mata |
|---|---|---|---|---|
| Eksterior depan tegak | sumbu fasad, jarak 1,2-1,5 x tinggi bangunan, z=1600 | tengah fasad z=0,5 x tinggi bangunan | 35 mm, shift_y agar vertikal tegak (bukan mendongak) | 1600 |
| Eksterior diagonal | 30-45 derajat dari muka, jarak 1,5 x tinggi | pusat massa bangunan | 35 mm | 1600 |
| Interior ruang (kelas) | sudut ruang, menghadap diagonal ruang, jarak 300-800 mm dari dua dinding | diagonal ruang | 24 mm (sempit) - 35 mm | 1600 |
| Interior koridor | di jalur tengah CIR, 1/3 panjang | sepanjang koridor | 24 mm | 1600 |
| Bird eye (opsional) | di atas | pusat denah | 50 mm | - |

Aturan: tinggi mata interior WAJIB 1600 mm; kamera tidak boleh berada di dalam
bbox dinding/furnitur (uji titik-dalam semua bbox solid = false); `clip_start =
0.01` m; draft Eevee dulu per kamera (file `render/draft/<sudut>_r<n>.png`),
periksa, baru final Cycles 128-256 samples + denoise. Tabel preset lama di Tahap
4 tetap berlaku sebagai rujukan cepat, tetapi yang mengikat adalah isi
`kamera_preset[]` — angka di tabel tidak boleh bertentangan dengannya.

### K3D-2 Daftar material per elemen dengan kode (`visualisasi.material_list[]`)

Kode MAT-nn WAJIB menutup SELURUH permukaan scene: setiap objek mesh punya TEPAT
SATU MAT. Aturan:
- M1: pemetaan dari finish schedule interior (sumber kebenaran finish); warna diambil dari palet, bukan improvisasi renderer.
- M2: properti minimum per MAT: `roughness`, `base_color_hex`; kaca: transmission 1.0, roughness 0.05, IOR 1.45; logam: metallic >= 0.9.
- M3: objek tanpa MAT di scene = 0 (validator scene; menutup kegagalan B-01 "lantai hitam pekat tanpa tekstur").
- M4: material lantai ruang huni WAJIB merujuk kode finish ruang terkait; verifikasi silang: MAT lantai ruang X == MAT yang terpasang pada mesh lantai ruang X di scene.

Kode awal (tambah sesuai proyek): MAT-01 keramik/granit lantai, MAT-02 cat emulsi
dinding, MAT-03 gypsum plafon, MAT-04 kayu kusen/meja, MAT-05 HPL, MAT-06 kaca,
MAT-07 aluminium/logam, MAT-08 beton ekspos, MAT-09 granit polished, MAT-10
lanskap/tanah. Tabel mapping finish Tahap 3 tetap menjadi cara membangun node;
kode MAT adalah identitas tertukar-datanya.

### K3D-3 Figur manusia pembanding (`visualisasi.figur_manusia[]`)

- H1: setiap render INTERIOR memuat >= 1 figur tinggi 1700 mm; EKSTERIOR >= 2 figur; disimpan di `visualisasi.figur_manusia[]` (posisi per sudut). Figur TIDAK lagi dihapus sebelum final (koreksi checklist Tahap 6 lama): ia bagian dari komposisi.
- H2: figur tidak menghalangi subjek: lebar proyeksi figur <= 25 persen lebar frame DAN pusat figur di luar 40 persen tengah frame.
- H3: uji proporsi deterministik (dihitung dari data, bukan piksel): rasio tinggi pintu/figur = 2100/1700 = 1,24; plafon 3200/1700 = 1,88; parapet 900/1700 = 0,53; meja 750/1700 = 0,44. Render harus konsisten dengan rasio ini; deviasi visual > 10 persen = QA FAIL (dicek vision saat draft).

### K3D-4 Kontrak image-gen (multi-view reference + massing sheet)

Untuk SETIAP gambar image-gen arsitektur (jalur pembanding maupun produksi konsep),
kontrak ini bagian dari alur kerja skill (koordinasi dengan gsp-image-specialist):

| ID | Kewajiban | Numerik |
|---|---|---|
| IG-1 | Multi-view reference DARI SCENE YANG SAMA: minimal 3 draft ortogonal (depan, samping, atas/top-down; tambah 1 interior eye-level utk interior) dirender Eevee dari model final sebelum panggilan image-gen | >= 3 berkas PNG di `render/draft/`, tercatat di `image_gen.ref_set` |
| IG-2 | Massing sheet: satu PNG lembar bentuk massa white-model 4 pandangan (depan, samping, atas, aksonometri 30 derajat) dalam grid 2x2, latar netral, TANPA material/textur | 1 berkas, `image_gen.massing_sheet`; dikirim bersama ref_set ke SETIAP panggilan |
| IG-3 | Setiap panggilan image-gen menerima REF-SET + massing sheet (kontak-sheet tunggal atau multi-gambar sesuai kemampuan backend; dicatat di prompt log) | jumlah referensi per panggilan >= 4 (3 ortogonal + massing) |
| IG-4 | Prompt memuat TOKEN KUNCI dari data: dimensi volume (PxLxT mm), jumlah bukaan per fasad, kode material, sudut+lensa kamera | parser menghitung token dari PROJECT.json; prompt log menyimpannya (pola B18-B terbukti) |
| IG-5 | Kalimat kunci geometri verbatim: reproduksi persis referensi, dilarang menambah/menghapus/memindah bukaan | hadir di setiap prompt (checker regex) |
| IG-6 | Konsistensi bentuk antar gambar DINILAI (bukan gate otomatis): silhouette/proporsi vs massing sheet oleh juri vision; skor konsistensi < ambang = generate ulang dengan REF-SET lebih ketat | kriteria juri, ambang ditetapkan di rubrik B-02 |

Field PROJECT.json: `image_gen.ref_set[]`, `image_gen.massing_sheet`,
`image_gen.prompt_log`. Menulis bagian `visualisasi` dan `image_gen` adalah hak
tulis skill ini sesuai skema orkestrator rev v1.2.

### K3D-5 Kontrak pencahayaan numerik (`visualisasi.lighting`) (v1.3 - K-1a)

Delta v1.3 dari GAP-ANALYSIS B-01 (CAD-SWARM-01, putusan D-27). Temuan B-01: render
interior hanya berisi silinder fixture bermaterial emisi tanpa SATU PUN light object
(bpy.data.lights.new = nol), interior ter-render gelap (mean_lum 0,177/0,172 vs
eksterior 0,779/0,813) sementara `lux_target` PROJECT.json berstatus PASS - tidak ada
jembatan lux -> piksel. Kontrak ini menutup celah itu dengan angka eksplisit, bukan
frasa kualitatif seperti "cukup terang".

**Pemetaan lux -> lumen -> Watt (lm/W):**

| Jenis ruang | lux target | lumen per titik_me | Watt Blender (point/area) |
|---|---|---|---|
| kelas / kantor | 300 | 400 - 800 | 4 - 8 W |
| koridor / tangga | 100 | 150 - 300 | 1,5 - 3 W |
| hunian ruang utama | 150 | 300 - 600 | 3 - 6 W |
| retail | 300 | 400 - 800 | 4 - 8 W |

Aturan kontrak:

- L1: setiap `titik_me` dari data (E-01..) menjadi SATU objek cahaya nyata
  (`bpy.data.lights.new` tipe POINT/AREA) di scene; geometri fixture boleh menyertainya.
- L2: material emission pada fixture hanya agar lampu "terlihat menyala"; fixture
  emisi BUKAN sumber cahaya dan TIDAK BOLEH menjadi satu-satunya sumber cahaya ruang
  tertutup (larangan fixture-emission-only).
- L3: pemetaan lumen -> Watt: `Watt_blender = lumen / efikasi_lm_w`; efikasi default
  100 lm/W (LED) dan dapat dioverride di `visualisasi.lighting.efikasi_lm_w`. Contoh:
  downlight 600 lm -> 6 W.
- L4: temperatur warna dari jenis ruang: 2700 - 3000 K hunian (RGB hangat), 4000 K
  retail/kantor (netral); tercatat di `visualisasi.lighting.temperatur_k`.
- L5: uji keseimbangan deterministik: jumlah light object == jumlah `titik_me`
  (toleransi 0; lampu tambahan dekoratif dicatat eksplisit); hasil ditulis ke
  `visualisasi.lighting.report_seimbang`; tidak seimbang = QA FAIL sebelum kirim.

**TABEL BAND LUMINANSI TARGET K3D-5** (satu-satunya sumber kebenaran untuk checker
HG-LUM kartu K-1b; parser WAJIB membaca tabel ini dari SKILL.md, DILARANG menyalin
konstanta ke kode - SPK-002 matcher ganda = buta-titik terwarisi):

| jenis_ruang | mean_min | mean_max | p1_min | p99_maks |
|---|---|---|---|---|
| interior | 0.25 | 0.90 | 0.05 | 0.98 |
| eksterior_siang | 0.30 | - | 0.10 | - |

Cara baca tabel dan definisi ukur:

- Kolom `mean_min` dan `mean_max` membentuk band luminansi; MERAH bila mean di luar
  band ATAU `p1` di bawah `p1_min`; sel `-` berarti metrik tidak ditegakkan.
- Luminansi piksel = 0,2126R + 0,7152G + 0,0722B pada sRGB 8-bit dinormalisasi [0,1];
  statistik mean/p1/p99 atas SELURUH piksel resolusi penuh berkas PNG.
- Klasifikasi jenis dari nama berkas: mengandung `interior` -> baris `interior`;
  selain itu dianggap `eksterior_siang` kecuali proyek menandai adegan malam di
  `visualisasi.lighting.malam` (adegan malam dikecualikan dari band).
- Kalibrasi angka (diukur langsung dari PNG di disk, 2026-09-05): interior lama B-01
  FAIL sah (kelas mean 0,1786 p1 0,0000; koridor mean 0,1725 p1 0,0000); eksterior
  B-01 lolos (fasad mean 0,7842; diagonal 0,8186); B-02 putaran-3 lolos semua
  (interior mean 0,6531 - 0,8375; p1 0,2799 - 0,5128).
- Checker HG-LUM (`bench/B-01/scripts/check_lighting.py` milik kartu K-1b) WAJIB
  mem-parse tabel ini dari berkas skill (fleet registry) alih-alih hardcode angka.

---

## Kelengkapan arsitektural wajib (delta v1.4 - BL-05 / skema v1.3 / gerbang HG-IMP-5)

Konteks bukti (AUDIT-SCENE-B02, dibaca sebagai spesifikasi - bukan angka yang disalin;
angka B-02 adalah fixture merah): scene B-02 terukur nol atap arsitektural (hanya
slab_dak rata, cakupan 92,18 %, celah 34,27 m2, nol pelana/parapet), nol
leveling/podium/tangga eksterior (hanya satu ramp 1:12,5 yang pangkalnya 330 mm di
bawah muka tanah), dan 18 tabrakan kolom-vs-bukaan. Akar tabrakan sudah divonis:
30/30 kolom tepat di as dan footprint eksak schedule; yang salah adalah BUKAAN yang
tidak menyisihkan zona kolom. Gerbang kolom-vs-grid terbukti buta terhadap cacat ini,
maka spesifikasi di bawah menguji kolom-vs-bukaan.

Kelengkapan berikut BUTUH-WAJIB di scene, bukan opsional:

- AR-1 Atap dimodel dari field skema `atap` (rev v1.3: bentuk, kemiringan_deg,
  overhang_mm, elevasi_eaves_mm, material, talang, volume_cakupan): tertutup dengan
  cakupan raycast vertikal >= 99,5 % pada grid 500 mm di dalam amplop dinding lantai
  atas, dan nol edge terbuka pada shell atap. Void fungsional (mis. void tangga)
  harus terdaftar eksplisit, bukan diam-diam bolong. Pelat dak rata tanpa bentuk atap
  TIDAK memenuhi butir ini.
- AR-2 Podium/leveling dari field `podium_leveling`: pelat lantai 0 terangkat sesuai
  `delta_mm`, dinding podium dimodel (tinggi dan tebal dari field); dasar ramp atau
  tangga tidak boleh berada di bawah muka tanah alam.
- AR-3 Tangga eksterior dari field `tangga_eksterior[]`: jumlah anak tangga =
  ceil(delta/riser), riser <= 175 mm, tread >= 300 mm, lebar >= 1200 mm; objek wajib
  terekspos di render fasad depan.
- AR-4 Kolom = box riil (bukan grid). Irisan AABB box kolom riil terhadap segmen
  bukaan (pita tinggi ambang..ambang+tinggi pada garis dinding) = 0 pasangan, untuk
  jendela kaca maupun daun pintu. Alokasi bukaan wajib menyisihkan footprint kolom
  beserta kusennya; uji kolom-vs-grid saja tidak sah sebagai pengganti. Kolom tidak
  boleh memproyeksi keluar muka dinding kecuali sengaja dijadikan ekspresi
  arsitektural yang tercatat.

## Dual-output & disiplin styling (delta v1.4 - BL-04 / TA-IMP-Q7 / gerbang HG-IMP-7)

- DO-1 Tiap sudut final menghasilkan DUA berkas: `<sudut>_bf_r<n>.png` base-form
  EEVEE (bukti bentuk; tanpa tekstur prosedural/lighting berlapis) dan
  `<sudut>_r<n>.png` styled Cycles 256 samples OIDN 1920x1080 pada empat sudut persis
  FLOOR. Total beban Cycles tidak bertambah dibanding baseline; semua proses render
  tetap serial satu proses (EEVEE bukan Cycles, tetap serial antar proses render).
- DO-2 Non-degradasi bentuk: dump daftar objek wajib per koleksi (kolom, dinding,
  bukaan, atap, podium, tangga, furnitur tetap) SEBELUM styling ke
  `scene_audit_before.json` dan SESUDAH ke `scene_audit_after.json` via query
  headless; objek hilang = 0 dan `hide_render` baru = 0 pada objek wajib. Styling
  TIDAK boleh menurunkan mutu bentuk; non-degradasi diukur dari daftar objek scene
  (query headless), bukan dari piksel.
- DO-3 Perbandingan biaya-manfaat styling dicatat jujur di laporan (skor base vs
  styled, diuji lewat gerbang noise-band warisan P6).

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

Profil pemilik: `gsp-3d-specialist` | Konsumen wajib: gsp-architecture-specialist, gsp-image-specialist | Tier: ALWAYS (3d)

- `pustaka-teknis`: angka material/lighting berujukan.
- `gsp-design-system-grill` / token `MASTER_DESIGN`: gaya render & kop.
- `gsp-spatial-psychology`: mood render & pemilihan objek — view alam, soft
  edge, prospect-refuge, CCT/CRI/lux untuk suasana (delta v1.4.1, SPATIAL-PSI-0930).
- `blender-mcp`: opsional interaktif (TA-Q4); jalur render kanonik tetap headless.
- Serial rule Cycles (maks 1 proses fleet-wide) + nol-cache sha256 per artefak (preseden P2).
- `gsp-verification-before-completion`: verifikasi bukti sebelum klaim selesai.

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
