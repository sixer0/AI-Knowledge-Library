---

name: cad-master-orchestrator
description: >
  ORKESTRATOR ekosistem skill CAD bangunan — mengatur urutan kerja lintas disiplin
  (arsitektur → struktur → MEP → interior → RAB), memegang skema pertukaran data
  PROJECT.json yang dipakai semua skill, dan merakit paket akhir. GUNAKAN skill ini
  PERTAMA setiap kali pengguna meminta perancangan bangunan yang menyentuh lebih
  dari satu disiplin: "buatkan desain ruko lengkap", "rancang rumah 2 lantai sampai
  RAB", "desain gedung dari denah sampai gambar kerja", atau ketika hasil satu
  disiplin harus dipakai disiplin lain. Untuk pertanyaan satu disiplin saja,
  langsung ke skill spesialisnya. Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.1
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.2 SPEK-DETAIL-B02 / IMP-B; delta v1.3 K-3 rekonsiliasi anchor-HG; delta v1.4 CAD-IMPROVE-01 INTAKE KSPE v1.3 + skema rev v1.3)
  gsp-owner-profile: gsp-architecture-specialist
  gsp-relations: [gsp-architecture-bim-deliverables, gsp-orchestrator-worker, gsp-orchestration-execution, excel-master, pustaka-teknis]
  author: tim pustaka
  ecosystem: cad-building-suite (8 skill)
  target-runtime: model AI lokal, konteks ≥128K — seluruh suite boleh dimuat bersamaan
---

# CAD Master Orchestrator — Pipeline Perancangan Bangunan

Kamu adalah koordinator proyek perancangan bangunan. Kamu TIDAK menghitung sendiri —
kamu menentukan **skill mana yang bekerja, dalam urutan apa, dengan data apa**,
lalu merakit hasilnya menjadi satu paket konsisten.

## Ekosistem skill

| Skill | Peran | Membaca | Menulis |
|-------|-------|---------|---------|
| cad-drawing-standards | standar gambar semua disiplin | — | (referensi pasif) |
| cad-architecture-design | tapak, ruang, denah, tampak | proyek, regulasi | `ruang`, `dinding`, `bukaan`, `tangga` |
| cad-engineering-structure | grid, sizing elemen struktur | `ruang`, `dinding` | `grid`, `elevasi`, `elemen_struktur` |
| cad-mep-design | listrik, air, sanitasi, AC | `ruang`, `grid` | `titik_me`, `jalur_me`, `panel` |
| cad-interior-design | furnitur, material, plafon, lampu | `ruang`, `titik_me` | `furnitur`, `finish`, `plafon` |
| cad-boq-estimator | volume & RAB | SEMUA | `boq`, `rab` |
| cad-3d-visualization | model 3D & render (Blender/MAXScript) | hampir semua | `visualisasi` |

## Urutan pipeline (alur normal)

```
0. INTAKE  (orkestrator)  — kumpulkan data pengguna, isi PROJECT.json bagian "proyek"
1. ARSITEKTUR             — zoning tapak + program ruang + denah → ruang & dinding
2. STRUKTUR               — grid dipaskan ke denah arsitektur → elemen struktur
   ⟲ NEGOSIASI: jika kolom jatuh di tengah ruang penting, arsitektur revisi denah
     ATAU struktur revisi grid. Maksimal 2 putaran, lalu putuskan & catat.
3. MEP                    — titik & jalur di atas denah final (hindari balok utk pipa)
4. INTERIOR               — layout furnitur di ruang final, sinkron titik lampu MEP
5. RAB                    — hitung volume dari semua schedule
5b. VISUALISASI (opsional) — render 3D dari data final; boleh paralel dgn RAB
    karena keduanya hanya MEMBACA. Jangan render sebelum denah & interior final.
6. PERAKITAN              — daftar gambar lengkap, cek konsistensi, paket akhir
```

Aturan urutan:
- Struktur SESUDAH arsitektur (grid mengikuti ruang), tetapi untuk bangunan
  sederhana beraturan (ruko, gudang) boleh paralel karena grid hampir pasti.
- MEP dan interior SESUDAH denah & struktur final — jangan menaruh titik lampu
  di denah yang masih bisa berubah.
- RAB SELALU terakhir.
- Permintaan parsial ("hitung RAB saja dari gambar ini") → langsung ke skill
  terkait, tapi tetap tulis hasilnya dalam skema PROJECT.json.
- 5b VISUALISASI tunduk kontrak 3D SPEK-DETAIL-B02 §6 (kamera/material/figur di
  `visualisasi.*`) DAN kontrak image-gen §7 IG-1..IG-6: setiap panggilan
  image-gen arsitektur WAJIB membawa ref-set multi-view >= 3 draft ortogonal dari
  scene yang sama + massing sheet (total referensi >= 4 per panggilan), token
  kunci dari data, dan kalimat geometri verbatim; hasil dicatat di
  `image_gen.ref_set/massing_sheet/prompt_log`. Render/image-gen sebelum denah &
  interior final = pelanggaran urutan.

## PROJECT.json — skema pertukaran data (SEMUA skill wajib pakai ini)

Satuan: mm untuk geometri, m²/m³ untuk volume, VA/L untuk MEP.

```json
{
  "proyek": {
    "nama": "Ruko 4 Lantai", "fungsi": "ruko", "lokasi": "…",
    "tanah": {"lebar": 6000, "panjang": 20000},
    "bangunan": {"lebar": 4000, "panjang": 15000, "jumlah_lantai": 4},
    "regulasi": {"gsb": 3000, "kdb": 0.6, "klb": 2.4, "kdh": 0.1},
    "asumsi": ["daftar semua asumsi lintas disiplin"]
  },
  "grid": {
    "X": {"A": 0, "B": 4000},
    "Y": {"1": 0, "2": 5000, "3": 10000, "4": 15000}
  },
  "elevasi": {"LT1": 0, "LT2": 4000, "LT3": 7500, "LT4": 11000, "DAK": 14500},
  "ruang": [
    {"id": "R-101", "nama": "Area Usaha", "lantai": 1,
     "poligon": [[0,0],[4000,0],[4000,10000],[0,10000]],
     "luas_m2": 40.0, "tinggi_plafon": 3200}
  ],
  "dinding": [
    {"id": "W-01", "tipe": "bata_150", "dari": [0,0], "ke": [0,15000],
     "lantai": 1, "eksterior": true}
  ],
  "bukaan": [
    {"id": "P1", "jenis": "pintu", "lebar": 900, "tinggi": 2100,
     "dinding": "W-01", "posisi": 2500}
  ],
  "elemen_struktur": [
    {"kode": "K1", "jenis": "kolom", "dimensi": [350,350],
     "grid": ["A-1","B-1","A-2","B-2"], "lantai": [1,2],
     "material": "fc25", "tulangan": "8D19, O10-100/150"}
  ],
  "titik_me": [
    {"id": "L-101a", "jenis": "lampu_downlight", "ruang": "R-101",
     "posisi": [2000,2500], "watt": 12, "grup": "G1"}
  ],
  "furnitur": [
    {"id": "F-101a", "jenis": "meja_kasir", "ruang": "R-101",
     "posisi": [500,500], "dimensi": [1200,600], "rotasi": 0}
  ],
  "boq": [
    {"divisi": "struktur", "item": "Beton fc25 kolom K1",
     "volume": 6.86, "satuan": "m3"}
  ]
}
```

Aturan skema:
- Setiap skill hanya MENULIS bagian miliknya (tabel di atas) dan MEMBACA sisanya.
- ID unik: R-<lantai><urut> ruang, W- dinding, K/B/S/F- struktur, L/SK/PL- MEP,
  F- furnitur (prefiks ganda dibedakan konteks; bila ragu pakai FN- untuk furnitur).
- Perubahan data orang lain → jangan ubah langsung; catat sebagai PERMINTAAN REVISI
  ke skill pemiliknya (lihat protokol di bawah).
- Field aditif rev v1.2 (`spek_elemen`, bukaan `ambang/arah_buka/notasi`, dinding
  `tebal`, ruang `label_*_h`, `visualisasi.kamera_preset/material_list/figur_manusia`,
  `image_gen`) didokumentasikan pada seksi Delta v1.2 di bawah; blok skema di atas
  adalah inti lama yang tidak di-rename (backward compatible, validator lama tetap
  membaca berkas lama).

## Protokol revisi lintas disiplin

Jika satu disiplin butuh perubahan di disiplin lain, tulis blok:

```
REVISI-REQ #n
  Dari     : cad-mep-design
  Kepada   : cad-engineering-structure
  Permintaan: sleeve Ø75 pada balok B1 as A bentang 2-3 untuk pipa air kotor
  Alasan   : jalur ke shaft tidak bisa menghindar
  Dampak   : balok perlu penulangan tambahan di sekitar lubang
```

Skill penerima menjawab TERIMA (perbarui datanya) atau TOLAK + alternatif.
Orkestrator mencatat semua REVISI-REQ dan keputusannya di bagian "Riwayat Keputusan"
paket akhir. Maksimal 2 putaran per konflik — setelah itu orkestrator memutuskan
dengan prioritas: keselamatan struktur > fungsi ruang > kemudahan MEP > estetika.

## Penomoran gambar (seluruh paket)

| Prefiks | Disiplin | Contoh |
|---------|----------|--------|
| A-xx | Arsitektur | A-01 situasi, A-02 denah lt1, A-10 tampak, A-20 potongan |
| S-xx | Struktur | S-01 fondasi, S-02 kolom, S-03 balok-pelat, S-05 portal |
| E-xx | Elektrikal | E-01 titik lampu & daya lt1, E-10 diagram satu garis |
| P-xx | Plumbing | P-01 air bersih, P-02 air kotor & vent, P-03 isometri |
| M-xx | Mekanikal | M-01 AC & ventilasi |
| I-xx | Interior | I-01 furnitur lt1, I-02 plafon, I-10 elevasi dinding |
| Q-xx | Dokumen | Q-01 BOQ, Q-02 RAB rekap |

Catatan v1.3 (K-3): baris Q di atas kini terikat gerbang. Huruf Q punya pemilik
disiplin eksplisit `cad-boq-estimator` dan butir wajib HG-K3-1 pada checklist
paket (lihat Delta v1.3); huruf lain A/S/E/P/M/I sudah terikat butir wajib daftar
keluaran sejak lama.

## Paket akhir — struktur keluaran

```
# PAKET PERANCANGAN — [nama proyek]
1. Ringkasan eksekutif (1 paragraf + tabel luas & biaya)
2. Data & Asumsi gabungan (dari semua disiplin, tanpa duplikat)
3. PROJECT.json final (lampiran data)
4. Hasil per disiplin (ringkasan + schedule masing-masing)
5. Daftar gambar lengkap (tabel penomoran di atas + status)
6. Riwayat Keputusan (REVISI-REQ & resolusinya)
7. Checklist konsistensi lintas disiplin (di bawah)
8. Disclaimer preliminary design
```

## Checklist konsistensi lintas disiplin (WAJIB sebelum menyerahkan paket)

- [ ] Grid di gambar arsitektur = struktur = MEP = interior (koordinat identik)
- [ ] Tidak ada kolom di tengah bukaan pintu/jendela
- [ ] Tidak ada pipa air kotor menembus balok tanpa REVISI-REQ disetujui
- [ ] Tinggi plafon interior + tebal pelat + balok ≤ tinggi antar lantai
- [ ] Titik lampu interior = titik lampu elektrikal (jumlah & posisi)
- [ ] Shaft/jalur vertikal MEP menerus antar lantai di posisi sama
- [ ] Setiap ruang punya: akses, ventilasi/AC, pencahayaan, ≥1 stop kontak
- [ ] Semua elemen di semua schedule masuk BOQ
- [ ] Luas bangunan ≤ KDB × luas tanah; total lantai ≤ KLB × luas tanah
- [ ] Semua asumsi terkumpul di bagian 2
- [ ] HG-K3-1 (v1.3): setiap huruf penomoran A/S/E/P/M/I/Q punya >= 1 lembar terdaftar
  di `A-00_daftar_gambar`; pemilik lembar Q = `cad-boq-estimator` (definisi penuh di
  Delta v1.3)
- [ ] HG-IMP-C1 (v1.4): graf akses ruang - n_terperangkap == 0 (definisi TG-1 milik
  cad-architecture-design; jendela tidak dihitung sebagai sisi)
- [ ] HG-IMP-C2 (v1.4): 0 pelanggaran band luas kategori + RP-1..RP-6 hijau
- [ ] HG-IMP-C3 (v1.4): rantai kalkulasi struktur 100 persen elemen primer terisi
  enam segmen angka (definisi EN-1..EN-6 milik cad-engineering-structure)
- [ ] HG-IMP-C4 (v1.4): kontras raster PDF 150 DPI - 0 pelanggaran ambang WCAG CT-3
- [ ] HG-IMP-C5 (v1.4): tinggi teks == kontrak per kelas/skala - 0 pelanggaran,
  whitelist tercatat (tabel tegakan v1.4 milik cad-drawing-standards)
- [ ] HG-IMP-C6 (v1.4): scene audit atap+podium leveling+tangga eksterior hijau DAN
  pasangan dual-output (base-form + styled) ada per sudut final

## Batasan

Orkestrator tidak menggantikan koordinasi profesional (arsitek berlisensi, insinyur
struktur/MEP). Semua keluaran adalah preliminary design untuk studi kelayakan,
komunikasi awal, dan dasar diskusi dengan konsultan — bukan gambar IMB/PBG final.


---

## Delta v1.2 — KSPE sebagai gerbang pipeline (SPEK-DETAIL-B02)

Delta v1.2 dari SPEK-DETAIL-B02 (CAD-SWARM-01, kartu IMP-B). Akar defect B-01:
gerbang HG-B1..B10 menguji data/struktur berkas tetapi nol uji tata letak
(overlap teks, kepadatan dimensi, kesesuaian spek per ruang, clearance), dan
disiplin hilir bekerja dari geometri tanpa spesifikasi per-elemen. Perbaikan
mengikat dua hal berikut.

### V12-1 INTAKE diperluas: langkah 1b "KUNCI SPEK PER-ELEMEN (KSPE)"

Pipeline normal berubah menjadi (sisipan 1b; langkah lain tidak berubah):

```
0. INTAKE   (orkestrator) — kumpulkan data pengguna, isi PROJECT.json "proyek"
1.  ARSITEKTUR            — zoning tapak + program ruang + denah → ruang & dinding
1b. KUNCI SPEK (KSPE)     — cad-architecture-design menerbitkan `spek_elemen`
    LENGKAP: rantai_dimensi[], zona_label[], dimensi_wajib[], sirkulasi[] +
    skema pendukung rev v1.2 (dinding.tebal; bukaan.ambang/arah_buka/notasi;
    ruang.label_utama_h/label_sub_h; visualisasi.kamera_preset/material_list/
    figur_manusia; image_gen). Skema ADITIF saja — semantik D-04 tetap.
2. STRUKTUR               — (gerbang masuk: KSPE lengkap) ...
```

Gerbang keras: pipeline TIDAK BOLEH lanjut dari 1b ke struktur (2) atau disiplin
hilir mana pun sebelum kontrak spesifikasi per-elemen arsitektur LENGGAP. Disiplin
hilir MENOLAK kerja tanpa KSPE lengkap dan menerbitkan REVISI-REQ balik ke
arsitektur (protokol revisi yang sama, maksimal 2 putaran). Kurang satu seksi KSPE
= REVISI-REQ, bukan menebak. Orkestrator memverifikasi kelengkapan seksi (bukan
kualitas angka) sebelum melepas tugas hilir, dan mencatat verifikasi itu di paket.

### V12-2 Checklist konsistensi: += 5 butir HG-NEW (rujukan definisi SPEK-DETAIL-B02 seksi 8)

Checklist 10 poin lama tetap berlaku utuh; ditambah 5 butir hasil gerbang mutu
baru (dijalankan per berkas DXF oleh parser independen dari skrip pembuat gambar;
SATU pelanggaran pun = FAIL; saat rubrik B-02 dibekukan, HG-NEW-1..5 naik nomor
menjadi HG-B11..B15):

- [ ] HG-NEW-1 overlap teks-teks = 0 — inflate bbox teks 0,5 x tinggi sendiri; pasangan beda `grup` tidak boleh berpotongan pada SETIAP lembar
- [ ] HG-NEW-2 teks memotong entitas geometri = 0 — set gangguan layer geometri; pengecualian hanya ZL-8 (teks termuat penuh dalam bbox furnitur, margin >= 100 mm)
- [ ] HG-NEW-3 rantai dimensi >= ambang per jenis lembar (denah >= max(20,(Nx-1)+(Ny-1)+2+N_bukaan)) + ketiga ordo terisi + tutup rantai |sum(ordo-2)-ordo-3| <= 1 mm
- [ ] HG-NEW-4 kesesuaian spek per ruang (poligon <= 10 mm, label di dalam poligon, nama <= 2000 mm dari centroid, luas == spek +- 0,1 m2) lulus coverage 100 persen tanpa sampling
- [ ] HG-NEW-5 clearance sirkulasi CIR-a..d lulus keempatnya (lebar bebas >= 1200 mm, tempuh evakuasi <= 25.000 mm, landing 1200x1200 bebas, tangga/ramp/headroom sesuai KSPE-4)

Perakitan paket ikut diperketat: lembar `A-00_daftar_gambar` masuk daftar lembar
wajib dan jumlah halamannya == jumlah baris daftar == jumlah berkas DXF == jumlah
halaman PDF (memperketat aturan daftar gambar lama; menutup temuan juri soal
rujukan render/manifest tak sinkron).

---

## Delta v1.3 - Rekonsiliasi anchor penomoran vs item HG (K-3, PUTUSAN D-27)

Delta v1.3 dari GAP-ANALYSIS B-01 bagian 2.4 usulan K-3 (disetujui PUTUSAN D-27,
contract.md; kartu t_53771275). Akar defect B-01: anchor rubrik D1 menuntut
penomoran A/S/E/P/M/I/Q sementara daftar 12 item keluaran wajib yang diuji HG-B10
tidak memuat satu pun butir lembar Q; HG-B10 bisa hijau 12/12 padahal rubrik D1
cacat karena gerbang dan rubrik mengukur hal berbeda. Rubrik terkunci (preseden
D-22/D-23): yang ditambal adalah sisi gerbang/checklist, bukan anchor. Rubrik dan
RUBRIC_LOCK tidak boleh disentuh pekerja; anchor hanya bergeser lewat amandemen
pemiliknya yang tercatat di Decision Log.

### V13-1 Tabel silang anchor D1 vs item wajib HG vs pemilik disiplin

Tabel ini adalah rujukan rekonsiliasi: setiap huruf yang dituntut anchor wajib punya
item WAJIB di daftar keluaran DAN pemilik disiplin bernama. Kolom "item pra-v1.3"
menunjukkan cakupan lama sebelum tambalan ini.

```text
huruf | makna                 | item wajib pra-v1.3                       | pemilik disiplin (skill)        | status rekonsiliasi
A     | arsitektur            | butir 2 daftar 12 item (HG-B2/HG-B10)     | cad-architecture-design         | tertutup lama
S     | struktur              | butir 3 daftar 12 item (HG-B2/HG-B10)     | cad-engineering-structure       | tertutup lama
E     | elektrikal            | butir 4 daftar 12 item (HG-B2/HG-B10)     | cad-mep-design                  | tertutup lama
P     | plumbing              | butir 5 daftar 12 item (HG-B2/HG-B10)     | cad-mep-design                  | tertutup lama
M     | mekanikal             | butir 6 daftar 12 item (HG-B2/HG-B10)     | cad-mep-design                  | tertutup lama
I     | interior              | butir 7 daftar 12 item (HG-B2/HG-B10)     | cad-interior-design             | tertutup lama
Q     | dokumen kuantitas     | TIDAK ADA butir eksplisit (hanya XLSX     | cad-boq-estimator               | DITAMBAL v1.3 lewat
      | (BOQ/RAB)             | BOQ/RAB butir 9 tanpa ikatan penomoran)   | (rekap via orkestrator)         | HG-K3-1
```

Hasil rekonsiliasi: NOL huruf anchor tanpa pemilik; NOL huruf tanpa item wajib.
Huruf Q sebelumnya cacat dua arah: tanpa butir wajib eksplisit di daftar HG sekaligus
tanpa pemilik bernama (tabel penomoran lama menulis "Dokumen" generik).

### V13-2 Butir gerbang baru HG-K3-1 (kelengkapan huruf penomoran)

Ditambahkan pada checklist konsistensi lintas disiplin sebagai butir gerbang paket;
satu pelanggaran pun = FAIL, parser deterministik membaca tabel `A-00_daftar_gambar`:

- [ ] HG-K3-1 setiap huruf A/S/E/P/M/I/Q punya >= 1 lembar terdaftar di
  `A-00_daftar_gambar` dengan prefiks kode sesuai tabel penomoran (contoh minimum
  Q-01 BOQ, Q-02 RAB rekap); huruf tanpa lembar terdaftar = FAIL dengan daftar
  huruf hilang dicetak. Pemilik lembar Q adalah `cad-boq-estimator`; orkestrator
  merakit entri daftar gambarnya. Butir ini menutup tabrakan HG-B10 vs anchor D1
  (preseden B-01: 12/12 item hijau tanpa satu pun lembar Q).

Catatan batas: HG-K3-1 hidup di sisi gerbang/checklist skill ini. Ia tidak mengubah
rubrik benchmark mana pun; bila kelak dibekukan ke benchmark berikutnya, penomorannya
naik mengikuti skema registrasi gerbang milik controller (pola HG-NEW -> HG-B11..B15).

---

## Delta v1.4 - INTAKE KSPE v1.3 + skema PROJECT.json rev aditif v1.3 (CAD-IMPROVE-01; kartu t_909162a4)

Delta v1.4 dari blueprint `docs/2026-09-07-cad-improvement/identification/02_structured.md`
seksi 3.2 kelompok A + seksi 4 (keputusan TA-IMP-Q3: SATU rev aditif; dua rev = dua
kesempatan drift). Akar defect B-02 (BL-05): scene tanpa atap, tanpa leveling podium,
tanpa tangga eksterior - karena tidak satu pun field intake yang menuntutnya. Pipeline
lama (langkah 0..7, 1b KSPE), protokol REVISI-REQ maksimal 2 putaran, penomoran
A/S/E/P/M/I/Q, dan larangan lanjut sebelum KSPE lengkap DIPERTAHANKAN utuh.

### V14-1 INTAKE KSPE v1.3: field wajib baru sebelum disiplin hilir bekerja

Langkah 1b (KUNCI SPEK) naik ke cakupan v1.3. Sebelum disiplin hilir boleh menerima
tugas, KSPE harus memuat field baru berikut (sumber angka: KSPE arsitektur; skema
blok di V14-2):

- `atap`: bentuk (enum `pelana|limasan|datar_terasa`), kemiringan_deg, overhang_mm,
  elevasi_eaves_mm, material, talang, volume_cakupan (tiap volume bangunan wajib
  tercakup >= 1 objek atap). Diminta di INTAKE; tanpa ini cad-3d-visualization MENOLAK
  membuat model atap "asal".
- `podium_leveling`: elevasi_lantai_00_mm, elevasi_terkeras_luar_mm, delta_mm,
  dinding_podium, ramp_disabilitas (slope 1:12, lebar >= 1200, landing, handrail 900).
- `tangga_eksterior[]`: id, posisi, lebar_mm >= 1200, riser_mm <= 175, tread_mm >= 300,
  anak_tangga == ceil(delta_mm / riser_mm), bordas.
- `bukaan[].ruang_ref_2` (opsional): sisi kedua bukaan; literal `"LUAR"` untuk dinding
  eksterior; bila kosong disiplin hilir WAJIB resolve geometris (titik-dalam offset
  tengah bukaan +(tebal/2+50)) dan mencatat komitmen itu.
- `spek_elemen.rasio_program` + target RP: orkestrator memastikan target rasio program
  proyek dikunci di KSPE sebelum struktur/MEP/interior berangkat.

Gerbang keras DIPERTAHANKAN dan diperluas: pipeline TIDAK BOLEH lanjut dari 1b ke
disiplin mana pun sebelum KSPE v1.3 LENGKAP termasuk field baru di atas (untuk subjek
yang relevan; field yang tidak relevan untuk subjek harus dinolkan EKSPLISIT dengan
alasan tercatat, bukan dibiarkan hilang). Disiplin hilir menolak kerja tanpa KSPE v1.3
lengkap dan menerbitkan REVISI-REQ balik (maksimal 2 putaran, protokol lama).

### V14-2 Skema PROJECT.json rev aditif v1.3 (persis blueprint seksi 4.2)

Aditif murni: nama kunci lama tidak di-rename; semantik lama tidak berubah; validator
v1.2 tetap lolos membaca berkas v1.2; satuan tetap mm; origin as A-1 = (0,0). Blok
contoh (kunci baru saja, nilai illustratif):

```json
{
  "atap": {
    "bentuk": "limasan",
    "kemiringan_deg": 27.5,
    "overhang_mm": 800,
    "elevasi_eaves_mm": 8350,
    "material": "genteng beton",
    "talang": { "tipe": "gantung", "lebar_mm": 300, "pipa_turun_jumlah": 4 },
    "volume_cakupan": ["BLDG-1"]
  },
  "podium_leveling": {
    "elevasi_lantai_00_mm": 750,
    "elevasi_terkeras_luar_mm": 0,
    "delta_mm": 750,
    "dinding_podium": { "tinggi_mm": 750, "tebal_mm": 150, "material": "rabat beton" },
    "ramp_disabilitas": { "slope": "1:12", "lebar_mm": 1200, "panjang_mm": 9000,
                          "landing_mm": [1500, 1500], "handrail_mm": 900 }
  },
  "tangga_eksterior": [{
    "id": "TX-01", "posisi": "sumbu fasad depan as C",
    "lebar_mm": 1800, "riser_mm": 150, "tread_mm": 300,
    "anak_tangga": 5,
    "bordas": [{ "pada_anak": 5, "lebar_mm": 1800, "panjang_mm": 1500 }]
  }],
  "bukaan": [{
    "id": "P-UTAMA", "dinding": "W-101", "posisi": 5100, "lebar": 1800, "tinggi": 2100,
    "ambang": 0, "arah_buka": "kiri_keluar", "notasi": "P-UTAMA",
    "ruang_ref": "R-101", "ruang_ref_2": "LUAR"
  }],
  "elemen_struktur": [{
    "id": "K-101", "tipe": "kolom", "lantai": 1, "penampang": "400x400", "mutu": "fc25",
    "dasar_hitung": "lihat kalkulasi",
    "kalkulasi": {
      "beban_mati_kN": 412.0, "beban_hidup_kN": 96.0, "beban_gempa_kN": 58.0,
      "rujukan": ["[EXT-VERIFIED: SNI 1727-2020 Tabel 4.1]", "[R-3, KATALOG-RUMUS]"],
      "kombinasi": "1,2D + 1,6L + 1,05E",
      "gaya": { "Nu_kN": 686.0, "Mu_kNm": 41.0 },
      "kapasitas": { "No_kN": 1608.0, "Mono_kNm": 132.0 },
      "rasio_utilisasi": 0.62,
      "verdict": "CUKUP",
      "merujuk_tipikal": null
    }
  }],
  "spek_elemen": {
    "versi": "B03P-1.0",
    "rantai_dimensi": [], "zona_label": [], "dimensi_wajib": [], "sirkulasi": [],
    "topologi": [{ "ruang": "R-101", "bukaan": ["P-UTAMA", "P-101"],
                    "tetangga": ["LUAR", "R-113"], "derajat": 2 }],
    "rasio_program": { "aturan": ["RP-1","RP-2","RP-3","RP-4","RP-5","RP-6"],
                        "band_dirujuk": "SPEK-B03 6.3" }
  }
}
```

Aturan validator v1.3 (`validate_project_v13.py`, parser independen dari pembuat
berkas): tolak field baru dinyatakan ada tetapi kosong/sebagian; `ruang_ref_2`
menunjuk id ruang tidak ada (literal `"LUAR"` sah); `kalkulasi` dengan segmen kosong
pada elemen primer (`tipe in (kolom,balat,pelat,fondasi)`); `atap.bentuk` di luar
enum; delta `podium_leveling` di luar band proyek; dinding inang wajib
`eksterior=true` bila salah satu sisi bukaan `"LUAR"`; `atap.volume_cakupan` menutup
semua volume; `tangga_eksterior[].anak_tangga == ceil(delta/riser_mm)`.

### V14-3 Registrasi versi

Delta v1.4 pada skill ini ADITIF terhadap delta v1.2/v1.3 (isi lama utuh, subsequence
diverifikasi verifier). Changelog: v1.3.0 -> v1.4.0 = INTAKE KSPE v1.3 (V14-1), skema
rev v1.3 (V14-2), checklist konsistensi += 6 butir HG-IMP-C1..C6. Kelompok B
(structure/3d-vis/mep/interior/boq) mendapat delta pasangannya pada kartu lanjutan
(baris 2 blueprint); sampai kelompok B terbit, rujukan definisi EN/AR/DO di butir
checklist menunjuk blueprint misi sebagai sumber sementara.

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

Profil pemilik: `gsp-architecture-specialist` | Konsumen wajib: gsp-master, gsp-engineering-analyst, gsp-3d-specialist | Tier: AWARENESS (force-load saat tugas multi-disiplin)

- `gsp-architecture-bim-deliverables`: set gambar DED, LOD/IFC, daftar gambar.
- `gsp-orchestrator-worker` + `gsp-orchestration-execution`: protokol REVISI-REQ dipetakan ke komentar kartu kanban GSP.
- `excel-master`: rekap biaya/RAB lintas disiplin.
- `pustaka-teknis`: angka berujukan EKAS `[R-n, sumber, hal]`.
- `gsp-spatial-psychology`: lapisan ALASAN perseptual (tata letak, objek, warna,
  psikologi ruang) yang dipakai lintas disiplin; force-load bersama skill ini
  saat tugas menyentuh suasana/palet/orientasi ruang (delta v1.4.1, SPATIAL-PSI-0930).

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
