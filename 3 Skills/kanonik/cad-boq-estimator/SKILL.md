---

name: cad-boq-estimator
description: >
  Penghitung VOLUME pekerjaan (BOQ/Bill of Quantities) dan penyusun RAB (Rencana
  Anggaran Biaya) bangunan — beton, besi, bekisting, pasangan dinding, plester-aci,
  finishing lantai/dinding/plafon, pintu-jendela, titik MEP, sanitair — dari
  schedule semua disiplin dalam PROJECT.json. GUNAKAN skill ini setiap kali
  pengguna menyebut: RAB, BOQ, bill of quantity, volume pekerjaan, kubikasi
  beton, kebutuhan besi, jumlah bata, "berapa biaya bangun", "hitung materialnya",
  "butuh semen berapa", estimasi biaya konstruksi, harga per m² — bahkan bila
  hanya satu item yang ditanya. SELALU jalankan TERAKHIR dalam pipeline (setelah
  arsitektur, struktur, MEP, interior final). Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.0
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.4 CAD-IMPROVE-01 divisi BOQ atap/podium/tangga/ramp/TPS B3/genset-tandon)
  gsp-owner-profile: gsp-engineering-analyst
  gsp-relations: [excel-master, construction-estimator, gsp-architecture-bim-deliverables]
  author: gemilangsatriaperkasa.eng@gmail.com
  ecosystem: cad-building-suite — membaca SEMUA schedule, menulis bagian boq/rab di PROJECT.json
---

# CAD BOQ Estimator — Volume & Rencana Anggaran Biaya

Kamu adalah asisten quantity surveyor. Prinsip: (1) setiap volume DITELUSURI ke
elemen schedule asalnya — tidak ada angka yatim; (2) rumus ditunjukkan; (3) harga
satuan adalah INPUT dari pengguna/daerah — bila tak ada, pakai placeholder
`[Rp ...]` dan beri rentang indikatif dengan disclaimer; (4) waste factor selalu
diterapkan dan disebut.

## ALUR KERJA 5 TAHAP

### Tahap 1 — Inventarisasi sumber

Kumpulkan semua schedule: elemen_struktur (S), bukaan P/J (A), ruang & dinding (A),
finish schedule (I), furnitur built-in (I), titik ME (E/P/M). Laporkan schedule
yang KOSONG — item yang tidak ter-schedule tidak bisa dihitung; minta lengkapi
atau nyatakan eksklusi secara eksplisit.

### Tahap 2 — Rumus volume per kategori

**Struktur beton** (per tipe elemen, lalu × jumlah):
```
Kolom   : b × h × tinggi bersih × jumlah          → m³
Balok   : b × (h − tebal pelat) × bentang bersih  → m³   (h penuh bila konservatif — sebutkan pilihanmu)
Pelat   : luas panel × tebal                      → m³
Fondasi : B × L × tebal (telapak) + kolom pedestal → m³
Sloof   : b × h × panjang total                   → m³
```

**Besi tulangan** — dua metode, pilih & sebutkan:
1. *Rasio praktis* (preliminary): pelat 110–150 kg/m³, balok 150–200,
   kolom 200–250, fondasi 100–150, sloof 120–160.
2. *Hitung batang* (bila tulangan schedule lengkap): panjang × berat/m
   (D10=0,617 · D13=1,042 · D16=1,578 · D19=2,226 · D22=2,984 kg/m)
   + panjang penyaluran & tekukan ±15%.
   Waste besi **+7%**, dibulatkan ke batang 12 m.

**Bekisting** (m² permukaan cetak):
```
Kolom: keliling × tinggi · Balok: (2 sisi h + dasar b) × bentang
Pelat: luas bawah · Fondasi: keliling × tebal
```

**Pasangan & finishing**:
```
Dinding bata  : panjang × tinggi − luas bukaan (P/J)        → m²
  Bata merah ±70 bh/m² · bataringan ±8,3 bh/m² (60×20) — waste +5%
Plester+aci   : 2 × luas dinding (dua muka; 1 muka utk dinding batas) → m²
Cat           : luas plester − dinding keramik; 1 L ≈ 10–12 m² /lapis ×2 lapis
Lantai        : luas ruang per jenis finish (dari finish schedule)  → m² — waste keramik +5% (pola diagonal +10%)
Plafon        : luas ruang + drop/cove aktual                → m²
Waterproofing : luas KM + dak + 300 mm naik dinding          → m²
```

**MEP & lainnya** (satuan titik/unit/m):
```
Titik lampu / saklar / kotak kontak : per titik (dari schedule E)
Pipa per jenis-ukuran               : panjang jalur + 10%    → m
Sanitair (kloset, wastafel, FD, kran): per unit
AC, pompa, tandon, septic, panel    : per unit
Pintu/jendela                       : per unit sesuai schedule P/J
Kitchen set / built-in              : m lari (bawah & atas terpisah)
```

**Rumus volume divisi baru v1.4** (dipetakan ke divisi Romawi di blok Tahap 3):
```
Atap genteng     : luas proyeksi × faktor kemiringan (1/cos α)          → m²
                   talang gantung/beton : panjang keliling eaves         → m
                   pipa turun           : per titik
Podium/leveling  : pelat podium luas × tebal → m³; dinding podium
                   keliling × tinggi → m² pasangan / m³ rabat
Tangga eksterior : anak tangga & bordes per unit; beton bordes+kaliber → m³
Ramp disabilitas : panjang × lebar permukaan rabat                       → m²
                   handrail dua sisi : panjang miring                    → m
TPS limbah B3    : per unit ruang (finishing + exhaust mekanik per titik)
Genset + ATS     : per unit; kabel power genset                          → m
Tandon           : tandon atap / reservoir bawah / pompa per unit
```

### Tahap 3 — Struktur divisi RAB (urutan baku)

```
I.    Persiapan (bowplank, mobilisasi, air & listrik kerja)
II.   Tanah (galian fondasi, urugan kembali, urugan peninggian, buang tanah)
III.  Fondasi (lantai kerja, telapak, sloof — beton/besi/bekisting terpisah)
IV.   Struktur atas (kolom, balok, pelat, tangga — per lantai)
V.    Dinding (pasangan, plester, aci)
VI.   Kusen, pintu & jendela
VII.  Atap / dak (waterproofing, screed)
VIII. Plafon
IX.   Lantai & dinding finish
X.    Pengecatan
XI.   Sanitair & plumbing
XII.  Elektrikal
XIII. Mekanikal (AC, exhaust)
XIV.  Interior built-in (opsional, sering kontrak terpisah)
XV.   Lain-lain (septic, resapan, pagar, akhir/pembersihan)
```

### Divisi tambahan skema v1.3 (delta v1.4 - B-03P)

Baris BOQ baru berikut WAJIB tertelusur (kolom Sumber menunjuk elemen schedule atau
field skema v1.3), dipetakan ke divisi Romawi di atas tanpa mengubah urutan baku:

```text
VII.    Atap: pelana/limasan per m2 bidang atap + talang gantung per m + pipa turun
        per titik            (sumber: field atap, volume_cakupan)
II/III. Podium: rabat per m2/m3 + dinding podium per m2
        (sumber: podium_leveling.dinding_podium)
IV.     Tangga eksterior: anak tangga per unit + bordes per unit
        (sumber: tangga_eksterior[])
VI.     Ramp disabilitas per m2 + handrail per m dua sisi
        (sumber: podium_leveling.ramp_disabilitas)
XV.     TPS limbah B3 (ruang + ventilasi mekanik tercatat), genset + panel ATS,
        tandon atap + reservoar bawah tanah
        (sumber: program ruang + field MEP)
```

Ambang jumlah baris: paket benchmark B-03P menuntut >= 150 baris BOQ tertelusur 100 %
(naik dari floor lama 124). Baris tanpa Sumber yang menunjuk elemen schedule tidak
dihitung memenuhi ambang.

### Tahap 4 — Format keluaran

**BOQ (Q-01)** — tanpa harga, murni volume:

```
| No | Uraian pekerjaan | Volume | Sat | Sumber (elemen) |
|----|------------------|--------|-----|-----------------|
| IV.1 | Beton fc'25 kolom K1 350×350 | 6,86 | m³ | S: K1 ×8, lt1–2 |
| IV.2 | Besi tulangan kolom K1 (rasio 220 kg/m³) | 1.509 | kg | S: K1 |
```

**RAB (Q-02)** — BOQ × harga satuan:

```
| No | Uraian | Vol | Sat | Harga satuan (Rp) | Jumlah (Rp) |
...
Rekap per divisi → Subtotal → Overhead & profit kontraktor (10%) →
PPN 11% → TOTAL → dibulatkan.
Tampilkan juga: biaya per m² luas total lantai (sanity check:
rumah menengah 2025 ± Rp 5–8 jt/m²; ruko struktur 4 lt ± Rp 4,5–7 jt/m² — 
INDIKATIF, wajib dikalibrasi harga daerah).
```

Bila diminta berkas: hasilkan **xlsx** (satu sheet BOQ, satu sheet RAB, satu
sheet rekap; rumus Excel hidup: Jumlah = Vol × Harga, rekap = SUM divisi) —
gunakan skill excel-master/xlsx bila tersedia di lingkunganmu.

**AHSP**: bila pengguna meminta analisis harga satuan, pecah item ke koefisien
AHSP/SNI (bahan + upah + alat) — minta daftar harga bahan & upah daerah;
tanpa itu, JANGAN mengarang harga — pakai placeholder.

### Tahap 5 — Rekonsiliasi & sanity check

- Cross-check beton: total m³ vs (luas lantai × 0,30–0,40 m³/m² untuk ruko beton) —
  selisih > 25% → periksa ulang.
- Besi/beton keseluruhan 130–180 kg/m³ — di luar itu, periksa.
- Bata: luas dinding / luas lantai biasanya 1,0–1,6 untuk hunian bersekat.
  PENGECUALIAN: bangunan pipih memanjang (ruko 4–5 m lebar, dinding samping
  masif setinggi bangunan) wajar mencapai 2,0–2,5 — jangan tandai salah,
  cukup jelaskan penyebab geometrinya.
- Semua item schedule tercakup? Jalankan daftar silang: setiap kode schedule
  (K1, B1, P1, L1, FN-01…) harus muncul ≥1 baris BOQ atau tercatat di EKSKLUSI.

## Checklist QA BOQ/RAB

- [ ] Setiap baris BOQ punya kolom Sumber yang menunjuk elemen schedule
- [ ] Waste factor diterapkan & disebut (besi 7%, bata 5%, keramik 5–10%, pipa 10%)
- [ ] Volume bukaan dikurangkan dari dinding
- [ ] Daftar EKSKLUSI eksplisit (apa yang TIDAK dihitung: izin, tanah, furnitur lepas, dll.)
- [ ] Harga = input pengguna atau placeholder — tidak ada harga karangan
- [ ] Rekap: overhead 10% + PPN 11% + pembulatan
- [ ] Sanity check m³ beton/m², kg besi/m³, Rp/m² dilaporkan
- [ ] Disclaimer: estimasi preliminary, bukan penawaran kontraktor

## Batasan

Estimasi kelayakan — bukan RAB tender. Akurasi tipikal ±15–25% pada tahap
preliminary. Harga sangat bervariasi antar daerah & waktu; selalu kalibrasi
dengan harga setempat terkini. Tidak menghitung: eskalasi, bunga, perizinan,
biaya tak terduga (sarankan kontingensi 5–10%).

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

Profil pemilik: `gsp-engineering-analyst` | Konsumen wajib: gsp-pm-analyst, gsp-pm-writer, gsp-master | Tier: AWARENESS

- `excel-master` WAJIB: workbook teraudit konvensi ASUMSI-BAKU/TPL-02.
- `construction-estimator` (registry): silang rujukan saja, hindari duplikasi isi.
- `gsp-architecture-bim-deliverables`: struktur RAB/RKS.
- SPK-002: gerbang rilis 100% untuk field beban-rilis (angka rupiah bersumber).

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
