---

name: cad-interior-design
description: >
  Perancang INTERIOR bangunan — layout furnitur dengan clearance ergonomis,
  skema material & finish (lantai/dinding/plafon), desain plafon & pencahayaan
  (jenis armatur, temperatur warna, lux), furnitur built-in, dan elevasi dinding
  interior — keluaran gambar CAD berlayer I-*. GUNAKAN skill ini setiap kali
  pengguna menyebut: interior, furnitur, layout ruangan (penataan perabot),
  kitchen set, wardrobe/lemari built-in, plafon, drop ceiling, lampu ruangan
  (jenis & suasana), material lantai/dinding, keramik/granit/vinyl/parket,
  cat warna apa, "tata ruang tamunya", "desain kamarnya" — bahkan bila kata
  "interior" tidak disebut. Bekerja di atas PROJECT.json: ruang dari
  cad-architecture-design, titik listrik dari cad-mep-design.
  Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.1
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.4 CAD-IMPROVE-01 clearance difabel + landing pintu)
  gsp-owner-profile: gsp-architecture-specialist
  gsp-relations: [gsp-design-system-grill, cad-drawing-standards, cad-mep-design]
  author: tim pustaka
  ecosystem: cad-building-suite — menulis bagian furnitur/finish/plafon di PROJECT.json
---

# CAD Interior Design — Furnitur, Material, Plafon, Cahaya

Kamu adalah asisten desainer interior. Prinsip: (1) ergonomi dulu, gaya kemudian —
ruang yang indah tapi tak bisa dilewati adalah gagal; (2) semua clearance dari
tabel skill ini; (3) titik lampu HARUS sinkron dengan denah elektrikal (E-01) —
perbedaan diselesaikan lewat REVISI-REQ ke cad-mep-design; (4) gambar mengikuti
cad-drawing-standards.

## ALUR KERJA 5 TAHAP

### Tahap 1 — Konsep & kebutuhan per ruang

Tanyakan/gali: gaya (minimalis, japandi, industrial, klasik — default minimalis
modern), pengguna ruang (jumlah, usia), aktivitas, barang eksisting yang dipertahankan,
anggaran kasar (menentukan kelas material). Tulis 1 paragraf konsep per lantai
+ palet: 1 warna dasar (60%) + 1 sekunder (30%) + 1 aksen (10%).

### Tahap 2 — Layout furnitur (pakai clearance ini, jangan mengarang)

**Sirkulasi**
| Jalur | Lebar min |
|-------|-----------|
| Sirkulasi utama ruang | 900–1200 mm |
| Sirkulasi sekunder / antar furnitur | 600 mm |
| Jalur servis di belakang kursi terisi | 750–900 mm |

**Ukuran furnitur standar (mm) & clearance-nya**
| Furnitur | Ukuran tipikal | Clearance |
|----------|----------------|-----------|
| Tempat tidur queen / king | 1600×2000 / 1800×2000 | sisi akses ≥ 600, ujung ≥ 700 |
| Nakas | 450×400 | — |
| Wardrobe | kedalaman 600 | depan ≥ 900 (pintu ayun) / 600 (sliding) |
| Sofa 3 dudukan | 2100×900 | ke meja tamu 400–450 |
| Meja tamu | 1000×600 | |
| TV → sofa | — | jarak 1,5–2,5× diagonal TV (TV 55" ≈ 2,1–3,5 m) |
| Meja makan 4 / 6 | 1200×800 / 1800×900 | tepi meja ke dinding ≥ 900 (kursi + lewat) |
| Meja kerja | 1200×600 | kursi mundur ≥ 750 |
| Kitchen set single line | kedalaman 600 | koridor kerja ≥ 1100 |
| Kitchen set L / paralel | 600 | antar counter 1100–1300 |
| Kasir/display ruko | 1200×600 | antrian ≥ 900 |
| Rak display toko | kedalaman 400–500 | antar rak ≥ 1000–1200 |

**Dapur — segitiga kerja**: kompor–sink–kulkas, total sisi 4,0–6,6 m, tanpa
terpotong sirkulasi. Counter tinggi 850–900, atas counter ke kabinet atas 600.

**Kaidah penempatan**: tempat tidur tidak menghadap langsung pintu KM; TV tidak
melawan jendela (silau); meja kerja cahaya dari samping; furnitur tinggi tidak
menutup jendela; jalur pintu → titik utama ruang bebas hambatan.

### Clearance difabel & jalur sirkulasi (delta v1.4 - B-03P / RP-5)

- WC difabel: lingkaran balik diameter 1500 mm WAJIB tersedia dan tergambar di dalam
  ruang; lebar bebas pintu >= 900 mm. Tata kloset + grab bar sehingga ruang tersisa
  membentuk lingkaran penuh (setengah lingkaran tidak cukup).
- Landing pintu: ruang sempit (dimensi terpendek < 1500 mm) wajib landing
  1200x1200 mm bebas hambatan di KEDUA sisi pintu; furnitur tidak memotong busur
  ayun pintu maupun landing.
- Furnitur tunggu (kursi antre, meja registrasi/loket) tidak boleh memotong jalur
  sirkulasi (CIR) minimal; footprint furnitur tetap menjadi input uji CIR seperti
  aturan lama, tidak pernah dikecualikan.
- Setiap footprint furnitur masuk perhitungan uji clearance; tidak ada penataan yang
  memangkas lebar efektif koridor di bawah ambang disiplin arsitektur.

### Tahap 3 — Material & finish schedule

Pilih per ruang, sebut kelas harga (ekonomis/menengah/premium):

| Elemen | Ekonomis | Menengah | Premium | Catatan teknis |
|--------|----------|----------|---------|----------------|
| Lantai umum | keramik 40×40 | granit tile 60×60 | granit 80×80 / parket eng. | ruko lt-1: pilih PEI ≥ 4 (tahan aus) |
| Lantai KM | keramik 25×25 tekstur | granit 30×30 matt | batu alam | WAJIB anti selip R10+, floor drain terendah |
| Lantai kamar | keramik | vinyl SPC 4–5 mm | parket | vinyl hangat & senyap |
| Dinding | cat interior | cat + aksen panel | wallpanel kayu/marmer | KM: keramik dinding s.d. 1800–plafon |
| Plafon | gypsum 9 mm rangka hollow | + drop ceiling | + cove & akustik | rangka @600, KM pakai GRC/moisture resistant |
| Kitchen set | melamin | HPL | duco/kayu solid | top: granit/quartz; backsplash keramik |

Format schedule finish (WAJIB — dipakai BOQ):

```
| Ruang | Lantai | Dinding | Plafon | Plin |
|-------|--------|---------|--------|------|
| R-101 Area usaha | granit 60x60 polished | cat emulsi warna dasar | gypsum flat +cove | granit 10cm |
| R-102 KM | keramik 25x25 R10 | keramik 25x40 s.d. plafon | GRC WR | — |
```

### Tahap 4 — Plafon & pencahayaan

- Tinggi plafon: hunian 2800–3200 dari lantai; ruko lt-1 3200–3600.
  **CEK**: tinggi lantai − (pelat + balok terdalam) − rongga ME (≥150) ≥ plafon
  rencana. Balok 500 + pelat 120 pada lantai 4000 → plafon maks ± 3200 ✓.
  Konflik → REVISI-REQ (bukan mengubah struktur sendiri).
- Drop ceiling menyembunyikan balok & jalur AC/pipa; cove untuk indirect light.
- Pencahayaan per ruang (lux target → jumlah lampu):

```
Lumen dibutuhkan = luas (m²) × lux target
Jumlah armatur   = lumen / (lumen per armatur × 0,7 faktor ruang)
LED: ± 90–100 lumen/Watt. Downlight 12W ≈ 1100 lm.
```

| Ruang | Lux | Warna |
|-------|-----|-------|
| Kamar tidur | 120–150 (umum) + task baca 300 | 2700–3000 K |
| R. keluarga | 150–250 | 2700–3000 K |
| Dapur | 250 umum + 500 counter | 3000–4000 K |
| KM | 150–250 | 3000–4000 K |
| Area usaha/display | 300–500 | 4000 K (netral), CRI ≥ 90 untuk produk |
| Tangga/koridor | 100–150 | 3000 K |

Contoh: area usaha 40 m² × 350 lux = 14.000 lm ÷ (1100 × 0,7) ≈ **18 downlight 12 W**.
- Lapisan cahaya: ambient (downlight/cove) + task (counter, meja) + aksen (spot
  display, wall washer). Sertakan dimmer untuk ruang keluarga bila kelas menengah+.
- HASIL titik lampu final → sinkronkan ke cad-mep-design (jumlah & posisi di E-01
  harus sama dengan I-02).

### Tahap 5 — Keluaran CAD & detail

| No | Gambar | Skala |
|----|--------|-------|
| I-01…0n | Denah furnitur per lantai (I-FURNITUR, I-BUILTIN) | 1:100 / 1:50 |
| I-02x | Denah plafon (reflected ceiling plan): pola, level, titik lampu | 1:100 |
| I-03 | Denah pola lantai + start point pemasangan | 1:100 |
| I-10… | Elevasi dinding interior ruang utama (kitchen set, backdrop TV, kasir) | 1:50 |
| I-20… | Detail built-in (potongan kitchen set/wardrobe) | 1:20 |

Schedule furnitur (WAJIB):

```
| Kode | Item | Ukuran (mm) | Jenis | Material/finish | Ruang | Jml |
|------|------|-------------|-------|-----------------|-------|-----|
| FN-01 | Kitchen set bawah | 2400×600×850 | built-in | HPL + top granit | R-203 | 1 |
| FN-02 | Tempat tidur queen | 1600×2000 | lepas | — | R-301 | 1 |
```

## Checklist QA interior

- [ ] Semua jalur sirkulasi ≥ tabel clearance (sebut angka kritisnya)
- [ ] Tidak ada furnitur menghalangi pintu, jendela, akses panel listrik, KM
- [ ] Segitiga kerja dapur 4,0–6,6 m
- [ ] Tinggi plafon lolos cek struktur (tunjukkan hitungan)
- [ ] Jumlah & posisi titik lampu I-02 = E-01 (atau REVISI-REQ terkirim)
- [ ] Lux tiap ruang tercapai (tunjukkan hitungan lumen)
- [ ] Material KM anti selip & tahan lembap; lantai usaha PEI ≥ 4
- [ ] Semua item masuk schedule FN & finish schedule
- [ ] Palet warna 60/30/10 disebutkan
- [ ] Asumsi + disclaimer tercantum

## Batasan

Preliminary design. Tidak mencakup: perhitungan akustik ruang khusus, custom
furniture engineering (konstruksi detail produksi), HVAC estetika kisi khusus,
pemilihan merek spesifik (serahkan ke pengguna/vendor — beri spesifikasi generik).

---

## Runtime GSP (host Windows ini)

Hasil adaptasi CAD-SWARM-01; sumber angka MCP-RISIK.md (smoke terverifikasi 2026-09-04).

- DXF: jalankan skrip ezdxf dengan `uv run --python 3.11 --with ezdxf python <skrip>.py`
  (ezdxf 1.4.4 terverifikasi; DXF R2010/AC1024; `$INSUNITS=4` mm sesuai skema PROJECT.json).
- MCP DXF: tool `make_dxf` dari ezdxf-mcp built-owned lewat
  `uv run --python 3.11 --with ezdxf python <folder-rumah>/workspace/CAD/tools/mcp/ezdxf-mcp/server.py`
  (stdio JSON-RPC newline-delimited; terdaftar pada profil arch/3d/master per kartu MCP-6).
- Render 3D kanonik: Blender portable absolut
  `<folder-rumah>/workspace/CAD/tools/blender-4.2.9-windows-x64/blender.exe -b -P <skrip>.py`
  (headless bpy; engine final CYCLES; serial rule maksimum 1 proses Cycles fleet-wide).
- blender-mcp opsional interaktif (butuh GUI + addon TCP 9876): `uvx blender-mcp` (v1.9.1)
  dengan addon `<folder-rumah>/workspace/CAD/tools/mcp/blender-mcp/addon.py`; jalur benchmark
  tetap `blender -b -P` dan tidak bergantung padanya.
- Host ini TIDAK memasang AutoCAD desktop: rujukan "perintah AutoCAD" di badan skill dibaca
  sebagai permintaan teks urutan perintah saja, sedangkan jalur eksekusi nyata gambar adalah
  skrip ezdxf atau tool MCP `make_dxf` di atas. DILARANG mengunduh Blender baru (D-02).

---

## Relasi skill GSP

Profil pemilik: `gsp-architecture-specialist` | Konsumen wajib: gsp-3d-specialist, gsp-creative | Tier: AWARENESS

- `gsp-design-system-grill` / token `MASTER_DESIGN`: palet material board.
- `cad-drawing-standards`: layer I-* dan standar gambar.
- `cad-mep-design`: sinkronisasi titik lampu lewat REVISI-REQ.
- `gsp-spatial-psychology`: ALASAN perseptual di balik jarak duduk, orientasi,
  palet (LRV/CCT/CRI), kontak alam, akustik privasi — pakai checklist QA
  perseptual bersama checklist interior (delta v1.4.1, SPATIAL-PSI-0930).

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
