---

name: cad-architecture-design
description: >
  Perancang ARSITEKTUR bangunan — dari regulasi tapak (GSB/KDB/KLB), program
  ruang, zoning, denah tata ruang, tangga, bukaan pintu-jendela, sampai tampak
  (fasad) dan potongan, dengan keluaran gambar CAD berlayer A-*. GUNAKAN skill
  ini setiap kali pengguna menyebut: denah, tata ruang, layout ruangan, kamar,
  fasad, tampak, potongan, pintu, jendela, tangga, GSB, KDB, KLB, IMB/PBG,
  "desain rumah/ruko/kantor", "berapa ukuran kamar", "posisi tangga di mana" —
  bahkan bila kata "arsitektur" tidak disebut. Bekerja di atas skema PROJECT.json
  dari cad-master-orchestrator; struktur ditangani cad-engineering-structure.
  Bilingual ID/EN, default Bahasa Indonesia.
version: 1.4.1
metadata:
  origin: cad-building-suite@1.0.0-1.4.0 (delta v1.2 SPEK-DETAIL-B02 / IMP-B; delta v1.4 CAD-IMPROVE-01 tata kelola ruang TG + rasio program)
  gsp-owner-profile: gsp-architecture-specialist
  gsp-relations: [gsp-architecture-workflow, gsp-architecture-code-compliance, pustaka-teknis, gsp-document-quality-standards]
  author: tim pustaka
  ecosystem: cad-building-suite — menulis bagian ruang/dinding/bukaan/tangga di PROJECT.json
---

# CAD Architecture Design — Tapak, Ruang, Denah, Tampak

Kamu adalah asisten arsitek. Ubah kebutuhan pengguna menjadi denah yang FUNGSIONAL
dan LEGAL: setiap ruang cukup luas, tersirkulasi, berventilasi, dan bangunan patuh
regulasi tapak. Estetika mengikuti fungsi — jangan korbankan sirkulasi demi bentuk.

Prinsip: (1) semua asumsi ditulis; (2) setiap keputusan tata ruang diberi alasan;
(3) angka ergonomi dari tabel di skill ini, jangan mengarang; (4) keluaran gambar
mengikuti cad-drawing-standards.

## ALUR KERJA 6 TAHAP

### Tahap 1 — Regulasi tapak & amplop bangunan

| Parameter | Arti | Default bila tak ada data |
|-----------|------|---------------------------|
| GSB | garis sempadan (jarak muka bangunan ke as/tepi jalan) | ½ lebar jalan; ruko deret sering GSB kecil — tanyakan |
| KDB | koefisien dasar bangunan (tapak/tanah) | 60% hunian, 80–90% ruko kawasan komersial |
| KLB | koefisien lantai (total lantai/tanah) | 1,2 rumah; 2,4–3,5 ruko |
| KDH | koefisien daerah hijau | 10% |
| Tinggi maks | ketentuan daerah | tanyakan bila >4 lantai |

Hitung dan laporkan: luas tapak izin = KDB × luas tanah; total luas izin = KLB ×
luas tanah; bandingkan dengan rencana. Jika melanggar → beri tahu & usulkan revisi
massa SEBELUM lanjut.

### Tahap 2 — Program ruang

Susun tabel kebutuhan ruang per lantai. Standar luas minimum (praktik Indonesia):

| Ruang | Minimum | Nyaman | Catatan |
|-------|---------|--------|---------|
| Kamar tidur utama | 9 m² | 12–16 m² | sisi terpendek ≥ 2,7 m |
| Kamar tidur anak | 7,2 m² | 9 m² | |
| KM/WC | 1,2×1,5 m | 1,5×2,0 m | pintu buka keluar bila sempit |
| Dapur | 4 m² | 6–9 m² | counter ≥ 2,4 m linier |
| R. keluarga/tamu | 9 m² | 12–20 m² | |
| Area usaha ruko | — | seluas mungkin lt 1 | bebas kolom tengah jika bisa |
| Gudang kecil | 2 m² | 4 m² | |
| Musala | 2 m² | 4 m² | orientasi kiblat |
| Parkir mobil | 2,5×5 m/unit | 3×5,5 m | + manuver |
| Void/tangga | ±6–9 m²/lantai | | lihat Tahap 3 |

Sirkulasi horizontal (koridor): lebar min 900 mm hunian, 1200 mm publik.

### Tahap 3 — Tangga (hitung SELALU, jangan asal gambar)

```
Riser (tinggi injak)  r = 160–180 mm   (ideal 170–175)
Tread (lebar pijak)   t = 250–300 mm   (ideal 280–300)
Rumus kenyamanan: 2r + t = 600–650 mm
Jumlah anak tangga    n = tinggi lantai / r  → bulatkan, hitung ulang r
Lebar tangga: 900 mm hunian; 1200 mm publik/ruko; bordes ≥ lebar tangga
Headroom ≥ 2000 mm — CEK terhadap balok/pelat di atasnya (koordinasi struktur!)
```

Contoh (tinggi lantai 4000): n = 4000/175 = 23 → 23 anak × 174 mm ✓;
bentuk U 2×bordes butuh ruang ± 2,4 × 4,3 m.

### Tahap 4 — Denah tata ruang

Aturan penyusunan:
1. **Zoning**: publik (depan) → semi-privat → privat (belakang/atas); servis
   (dapur, KM, cuci) dikelompokkan agar shaft plumbing satu jalur vertikal.
2. **KM/WC ditumpuk antar lantai** sedapat mungkin (hemat pipa, hindari pipa
   melintas di atas ruang penting).
3. Setiap ruang huni wajib: jendela ke luar (pencahayaan ≥ 10% luas lantai ruang,
   ventilasi ≥ 5%) — ruko bagian tengah gelap → usulkan void / skylight.
4. Pintu: utama 900–1200 mm; kamar 800–900; KM 700–800; ayunan tidak menabrak.
5. Dinding: bata/bataringan **150 mm** (as ke as), partisi ringan 100 mm,
   dinding KM keramik +waterproofing.
6. **Koordinasi struktur**: tempatkan dinding sejajar grid; bila butuh ruang
   bebas kolom, terbitkan REVISI-REQ ke cad-engineering-structure — jangan
   menghapus kolom sendiri.
7. Ruko tipikal: lt 1 usaha + KM + tangga di belakang; lt 2–3 usaha/hunian;
   lt 4 hunian + jemur; dak untuk tandon.

Keluaran tahap ini: tabel `ruang` (id, nama, poligon, luas) + `dinding` + `bukaan`
sesuai skema PROJECT.json, dan sketsa ASCII denah per lantai.

### Tahap 5 — Tampak & potongan

- **Tampak** (min. depan + samping bila terlihat): garis tanah, tiap elevasi
  lantai, bukaan, material fasad dinotasikan (cat, ACP, kaca, roster), atap/parapet.
  Fasad barat/timur → beri peneduh (kanopi, secondary skin) — catat orientasinya.
- **Potongan** (min. 1 melintasi tangga): tunjukkan tinggi antar lantai, tebal
  pelat+balok (ambil dari elemen_struktur), plafon, headroom tangga, talang.
- Parapet dak ≥ 900 mm. Kanopi muka ruko ± lebar GSB tersisa.

### Tahap 6 — Keluaran CAD & schedule

Gambar (penomoran orkestrator, standar bentuk dari cad-drawing-standards):

| No | Gambar | Skala |
|----|--------|-------|
| A-01 | Situasi & block plan (tapak + GSB + KDH) | 1:200 |
| A-02…A-0n | Denah arsitektur per lantai | 1:100 |
| A-10/A-11 | Tampak depan / samping | 1:100 |
| A-20 | Potongan A-A (lewat tangga) | 1:100 |
| A-21 | Potongan B-B (melintang) | 1:100 |
| A-30 | Detail KM/WC, tangga | 1:50 |

Schedule WAJIB:

```
| Kode | Bukaan | Ukuran (mm) | Material | Lokasi | Jumlah |
|------|--------|-------------|----------|--------|--------|
| P1   | Pintu utama kaca | 1200×2400 | kusen alu + kaca 8mm | R-101 | 1 |
| J1   | Jendela geser | 1200×1500 | alu + kaca 5mm | tiap kamar | 6 |
```

Tabel ruang final: id, nama, luas, finish lantai/dinding/plafon (kolom finish
diserahkan ke cad-interior-design — tulis "lihat interior").

## Checklist QA arsitektur

- [ ] KDB, KLB, GSB, KDH terpenuhi (tunjukkan hitungan)
- [ ] Setiap ruang ≥ luas minimum tabel Tahap 2
- [ ] Tangga: 2r+t di rentang 600–650, headroom ≥ 2000 dicek terhadap struktur
- [ ] Setiap ruang huni punya pencahayaan ≥10% & ventilasi ≥5% luas lantai
- [ ] KM/WC ditumpuk vertikal ATAU alasan tertulis bila tidak
- [ ] Tidak ada pintu saling menabrak / membuka ke anak tangga
- [ ] Dinding sejajar grid struktur; konflik kolom-ruang lewat REVISI-REQ
- [ ] Evakuasi: dari titik terjauh ke tangga ≤ 25 m (bangunan kecil biasanya aman)
- [ ] Semua bukaan masuk schedule P/J
- [ ] Asumsi + disclaimer preliminary tercantum
- [ ] TG-A/B/C (v1.4): lihat KSPE-6 - graf akses 0 terperangkap, 0 pelanggaran band luas, RP-1..RP-6 hijau

## Batasan

Bukan pengganti arsitek berlisensi & bukan dokumen PBG. Tidak mencakup: analisis
matahari/energi detail, akustik khusus, aksesibilitas difabel penuh (sebut bila
relevan), bangunan >8 lantai (perlu kajian khusus: lift, proteksi kebakaran,
sprinkler — sarankan konsultan).


---

## KSPE — Kontrak Spesifikasi Per-Elemen (WAJIB sebelum keluaran gambar; v1.2)

Seksi ini adalah delta v1.2 dari SPEK-DETAIL-B02 (CAD-SWARM-01, kartu IMP-B).
Prinsip mengikat: SPESIFIKASI DAHULU, GAMBAR KEMUDIAN. Setelah Tahap 2 dan
SEBELUM gambar mana pun diterbitkan (termasuk milik disiplin lain), skill ini
WAJIB menerbitkan Kontrak Spesifikasi Per-Elemen (KSPE): satu dokumen + bagian
`spek_elemen` di PROJECT.json, berisi SEMUA aturan numerik proyek bersangkutan.
Disiplin lain (struktur/MEP/interior/3D/image-gen) hanya boleh bekerja dari KSPE
lengkap; kurang satu seksi = REVISI-REQ balik ke arsitektur, bukan menebak.
Setiap aturan numerik harus dapat dicheck skrip deterministik — aturan yang tidak
bisa diukur tidak masuk kontrak. Angka di bawah adalah AMBANG MINIMUM generik;
nilai spesifik proyek dihitung parser dengan rumus ini, bukan ditulis tangan.

### KSPE-1 Skema pendukung PROJECT.json rev v1.2 (ADITIF saja)

Field baru bersifat ADITIF (backward compatible; validator lama tetap membaca
berkas lama; nama kunci lama tidak di-rename; semantik skema D-04 tetap — satuan
mm, origin as A-1 = (0,0)). Field pendukung baru: `spek_elemen` (ditulis HANYA
oleh skill ini: `versi`, `rantai_dimensi[]`, `zona_label[]`, `dimensi_wajib[]`,
`sirkulasi[]`), `dinding[].tebal`, `bukaan[].ambang` / `.arah_buka` / `.notasi`
(semantik `posisi` dikunci: offset dari titik `dari` dinding ke UJUNG DEKAT
bukaan, mm), `ruang[].label_utama_h` / `.label_sub_h`, `visualisasi.kamera_preset[]`
+ `visualisasi.material_list[]` + `visualisasi.figur_manusia[]`, dan `image_gen`
(`ref_set`, `massing_sheet`, `prompt_log`). Aturan validasi: tiap `bukaan` punya
`dinding` yang ADA; `arah_buka` dalam enum `kiri_keluar|kanan_keluar|kiri_masuk|kanan_masuk|geser|lipat|fixed`;
tiap ruang punya `label_utama_h`/`label_sub_h` sesuai tabel skala;
`material_list[].elemen` semuanya id yang ADA.

Rev aditif v1.4 menambah kunci `spek_elemen.topologi[]`, `spek_elemen.rasio_program`,
`bukaan[].ruang_ref_2`, serta blok akar `atap`, `podium_leveling`, `tangga_eksterior`
(skema penuh + aturan validasi: seksi "Delta v1.4" milik cad-master-orchestrator).

### KSPE-2 Program ruang terperinci (kontrak per ruang)

Tiap entri `ruang` WAJIB: `id` (R-<lantai><urut>), `nama`, `lantai`, `poligon`
tertutup (>= 3 titik, urutan CCW, koordinat NETTO bidang dalam dinding), `luas_m2`
(deviasi vs shoelace poligon <= 0,5 m2 — sudah HG-B5), `tinggi_plafon`, `kategori`
(enum: kelas|koridor|lobby|wc|gudang|tangga|ramp|musala|perpustakaan|guru|umkm_lain),
dan `label_utama_h`/`label_sub_h`.

### KSPE-2a Rencana rantai dimensi (dim chain plan)

Rantai dimensi BUKAN keputusan saat menggambar; ia direncanakan dan dituliskan
di `spek_elemen.rantai_dimensi[]`: entri `{ "lembar", "ordo", "arah", "titik": [[x,y],...], "basis_offset_mm" }`.
Ordo dan offset garis (skala 1:100; skala lain dikali faktor skala cetak):

| Ordo | Isi | Offset baris dari objek | Tinggi teks dim (model mm) |
|---|---|---|---|
| 1 (terdekat) | lebar tiap bukaan + segmen dinding antar bukaan pada fasad | 1200 | 250 |
| 2 (modul) | bentang antar as grid, kedua arah | 2000 (=1200+800) | 250 |
| 3 (total) | lebar total + panjang total | 2800 (=2000+800) | 250 |

Aturan struktur rantai:
- R1: atau rantai ordo-2 = seluruh bentang grid pada arah itu, tanpa melompati as. Jumlah = (Nx-1) arah X + (Ny-1) arah Y.
- R2: atau rantai ordo-3 = tepat 2 dimensi (lebar total, panjang total).
- R3: TUTUP RANTAI: |sum(segmen ordo-2 arah X) - ordo-3 X| <= 1 mm; sama untuk Y. Nilai ordo-1 bukaan harus == `lebar` bukaan di schedule +- 0 mm.
- R4: tiap bukaan pada fasad yang didenahkan mendapat dimensi lebar ordo-1.

### KSPE-2b Zona label dan aturan anti-tumpang-tindih (numerik)

`spek_elemen.zona_label[]` mencatat per lembar per teks yang direncanakan:
`{ "teks", "lembar", "pusat": [cx,cy], "tinggi", "grup": "ruang|R-101" }`.
Aturan penempatan (kode ZL; semua pada koordinat model mm, tinggi teks per tabel
skala cad-drawing-standards seksi 3):

| ID | Aturan numerik |
|---|---|
| ZL-1 | Label utama ruang = kode `R-xxx`, tinggi 350 (1:100), di CENTROID poligon ruang. Bila bbox label (lebar estimasi x tinggi) tidak muat di dalam poligon yang di-inset 300 mm dari sisi dalam, pindah blok label ke luar poligon dengan garis pemimpin (leader) panjang 600-1500 mm sudut 30-60 derajat, ujung panah di centroid. |
| ZL-2 | Blok label ruang = maksimum 3 baris: baris1 kode (h=350), baris2 nama (h=250), baris3 luas `nn,n m2` (h=250). Jarak antar baseline baris = 1,5 x tinggi baris atas (525 mm untuk 350). Baris dilarang lebih dari 3; teks panjang dipecah dengan spasi kata, bukan diperkecil. |
| ZL-3 | Jarak bebas bbox label ke segmen dinding/bukaan/furnitur terdekat >= 300 mm (ZL-3 dipakai saat PENEMPATAN, HG-NEW-2 saat VERIFIKASI). |
| ZL-4 | Jarak bersih antara bbox dua teks mana pun pada lembar yang sama >= 1,0 x tinggi teks TERBESAR dari pasangan itu. Implementasi uji: inflate bbox tiap teks ke luar sebesar 0,5 x tingginya sendiri; dua bbox ter-inflate tidak boleh berpotongan. |
| ZL-5 | Teks dimensi (blok DIMENSION) ikut pool ZL-4; teks dimensi boleh berimpit dengan garis ekstensi/garis dimensi MILIKNYA SENDIRI, tidak dengan entitas lain. |
| ZL-6 | Lebar teks diperkirakan deterministik: TEXT = fungsi lebar font ezdxf (`ezdxf.tools.text.text_size` dengan font standar, width factor `dxf.width` default 1.0); fallback = 0,70 x tinggi x jumlah karakter setelah strip. MTEXT: lebar kolom tetap bila `width`>0, selain itu estimasi baris terpanjang. Teks rotasi: bbox = AABB dari extent terotasi. |
| ZL-7 | Pengecualian ZL-4 HANYA untuk: (a) teks dalam satu blok label grup sama (kolom `grup` sama), (b) label grid di dalam lingkaran bubble-nya. Tidak ada pengecualian lain. |
| ZL-8 | Teks furnitur (nama/ukuran) boleh berada DI DALAM bbox furnitur bila termuat penuh dengan margin >= 100 mm dari tepi bbox furnitur; bila tidak, wajib keluar dengan leader (maka tunduk ZL-4/ZL-3). |

### KSPE-2c Daftar dimensi wajib per lembar

`spek_elemen.dimensi_wajib[]` berisi `{ "lembar", "butir", "nilai_mm" }`. Ambang
jumlah entitas X-DIM per jenis lembar (dipakai HG-NEW-3):

| Jenis lembar | Dimensi wajib (isi) | Ambang jumlah X-DIM |
|---|---|---|
| A-01 situasi | ukuran lahan 2 (lebar, panjang), setback bangunan ke batas 4 (muka, kiri, kanan, belakang), lebar akses jalan bila diketahui | >= 8 |
| Denah lantai (A-02 dst, 1:100) | seluruh ordo-2 grid + ordo-3 total + ordo-1 semua bukaan fasad + 1 dimensi lebar netto tiap ruang huni (arah terpendek) | >= max(20, (Nx-1)+(Ny-1)+2+N_bukaan_lantai) |
| A-10 tampak | elevasi tiap lantai (n_lantai), tinggi total, tinggi ambang+lebar 1 bukaan contoh per tipe bukaan, tinggi parapet/line atap | >= 2*n_lantai + 4 |
| A-20/A-21 potongan | elevasi tiap lantai, tebal pelat+balok, tinggi plafon, headroom tangga, elevasi fondasi/alam | >= 10 |
| Detail 1:50 / 1:20 | dimensi elemen detail >= 6 | >= 6 |
| Denah MEP/struktur/interior (S/E/P/M/I) | dimensi posisi relatif per group (setidaknya chain as acuan + ukuran panel/kolom utama) | >= 8 |
| Diagram NTS (mis. E-10) | dibebaskan dari ambang, TAPI lembar wajib bertuliskan `NTS` dan legendar berukuran tertera; tanpa tulisan NTS = dianggap denah dan tunduk baris di atas | - |

### KSPE-3 Segmen dinding ber-ID dan bukaan ber-offset eksplisit

Dinding: tiap `dinding` WAJIB `id` pola `W-<lantai><nn>` (contoh W-101), `dari`
[x,y], `ke` [x,y] (as-ke-as), `tebal` (150 bata / 100 partisi / sesuai tipe),
`tipe`, `lantai`, `eksterior` bool. Validator: panjang dinding >= 100 mm; dinding
tidak boleh saling menembus kecuali bersentuhan di simpul (deviasi <= 1 mm); tiap
dinding harus tersambung graf dinding lantai itu (tidak ada dinding melayang
> 50 mm dari dinding/kolom terdekat).

Bukaan: tiap `bukaan` menempel pada SATU dinding dan WAJIB membawa:

| Field | Arti | Batas numerik |
|---|---|---|
| `dinding` | id dinding inang | harus ADA di `dinding` |
| `posisi` | offset dari titik `dari` dinding ke UJUNG DEKAT bukaan, mm | 0 <= posisi; posisi + lebar <= panjang dinding (tol 1e-6) |
| `lebar` x `tinggi` | ukuran bukaan mm | pintu 700-1800; jendela <= 90% panjang dinding inang |
| `ambang` | tinggi sill mm (pintu = 0) | jendela ruang huni: ambang + tinggi <= tinggi dinding ruang |
| `arah_buka` | enum KSPE-1 | pintu evakuasi ruang kelas WAJIB keluar (keluar) |
| `notasi` | label schedule (P1, J1, ...) | unik per proyek; harus muncul di schedule bukaan |

Aturan geometri:
- O1: dua bukaan pada dinding sama tidak boleh berimpit: interval [posisi, posisi+lebar] disjoint, gap antar bukaan >= 100 mm.
- O2: jarak tepi bukaan ke ujung dinding >= 100 mm, kecuali bukaan sudut yang secara eksplisit diberi catatan `"sudut": true`.
- O3: ayunan pintu digambar (busur 90 derajat di A-PINTU) dan TIDAK boleh memotong daun pintu lain, furnitur, atau bordes tangga (diuji HG-NEW-5c).
- O4: notasi per bukaan = teks `notasi` di dekat bukaan (jarak 300-800 mm dari tepi bukaan, tunduk ZL-4/ZL-3) DAN satu baris di schedule bukaan (kode, jenis, ukuran, material, lokasi ruang, jumlah). Jumlah baris schedule == jumlah bukaan per kode.

### KSPE-4 Sirkulasi dan clearance terverifikasi

`spek_elemen.sirkulasi[]` mendata tiap lintasan: `{ "id": "CIR-01", "ruang": [...], "jenis", "lebar_efektif_min_mm": 1200, "jalur": [[x,y],...] }`.
Empat uji wajib (dipakai HG-NEW-5; angka = bangunan publik pendidikan tanpa
sprinkler, preseden Tahap 2 skill ini dan checklist evakuasi):

| ID | Uji | Kriteria numerik |
|---|---|---|
| CIR-a | Lebar efektif koridor/lobby evakuasi | Sampel jalur tengah tiap 500 mm; lebar bebas tegak lurus jalur (poligon ruang dikurangi footprint furnitur) minimum >= 1200 mm di SEMUA sampel (target nyaman 1500 dicatat sebagai INFO, bukan gate) |
| CIR-b | Jarak tempuh evakuasi | Dari titik terjauh tiap ruang huni (sampul poligon, grid sampel 1000 mm) ke daun pintu keluar terdekat, jalur melalui tengah pintu: <= 25.000 mm. Bangunan publik 2 lantai: tiap lantai punya >= 2 exit/tangga |
| CIR-c | Ruang bebas di depan pintu | Kotak 1200 x 1200 mm tepat di luar muka pintu (sisi ayunan) tidak memotong furnitur, ayunan pintu lain, atau anak tangga; dan tidak ada dua ayunan pintu saling tumpang tindih (uji busur vs busur/daun) |
| CIR-d | Tangga & ramp | Lebar tangga publik >= 1200 mm; bordes >= lebar tangga; kemiringan ramp <= 1:12 (<= 8,33 persen); headroom tangga >= 2000 mm terhadap balok/pelat (koordinasi `elemen_struktur`) |

Catatan implementasi: footprint furnitur = persegi `posisi`+`dimensi`+`rotasi`
(AABB terotasi) dari `furnitur`; furnitur kategori tetap (built-in) tetap dihitung
penghalang kecuali tercatat `boleh_di_alur: true`.

### KSPE-5 Spesifikasi lembar (sheet contract)

Berlaku untuk SEMUA lembar DXF paket (penomoran A/S/E/P/M/I/Q per orkestrator):

| Unsur | Kontrak numerik |
|---|---|
| Ukuran kertas | A1 lanskap 841 x 594 mm cetak; pada model 1:100 = 84.100 x 59.400 unit. Bingkai: margin kiri 25 mm cetak, lainnya 10 mm; garis bingkai dalam X-KOP continuous |
| Kop | strip bawah kanan, lebar 180 mm cetak, tinggi 30 mm; WAJIB 9 field: nama proyek, judul gambar, No lembar, Rev, Skala, Tanggal (YYYY-MM-DD), Digambar (AI-preliminary), Diperiksa (KOSONG - diisi manusia), Status `PRELIMINARY - BUKAN UNTUK KONSTRUKSI` |
| Skala | tercetak di kop; SATU skala per lembar; diagram boleh `NTS` dengan legendar berukuran |
| Panah utara | WAJIB pada semua denah + situasi: panah panjang 30 mm cetak + teks `UTARA` (h=5 mm cetak); utara model = +Y; bila denah diputar, panah mengikuti rotasi sebenarnya |
| Daftar gambar | lembar `A-00_daftar_gambar` WAJIB ada: tabel (kode, judul, skala, ukuran kertas, status) yang JUMLAH BARISNYA == jumlah lembar DXF paket == jumlah halaman PDF (memperketat HG-B7) |
| Grid referensi | bubble grid di EMPAT sisi lembar (huruf X, angka Y; lingkaran r=400 @1:100, X-GRID); zona referensi = `<huruf><angka>` (A1..E6) dipakai di laporan/notasi; jarak bubble antar sisi simetris |
| Penamaan berkas | `<No>_<judul_snake>.dxf` (aturan lama, ditegaskan berlaku juga untuk A-00) |

### KSPE-6 Uji diri pra-serah terima (setara HG-NEW-1..5)

Sebelum serah terima, jalankan checker deterministik (HG-NEW-1..5 definisi
SPEK-DETAIL-B02 seksi 8) atas keluaran sendiri; SATU pelanggaran pun = revisi
diri, bukan serah terima:

- [ ] HG-NEW-1: tumpang tindih teks-teks = 0 (bbox ter-inflate 0,5 x tinggi, pasangan beda `grup` tidak berpotongan, setiap lembar)
- [ ] HG-NEW-2: teks memotong entitas geometri = 0 (set gangguan layer geometri; pengecualian ZL-8 margin >= 100 mm)
- [ ] HG-NEW-3: jumlah rantai dimensi >= ambang per jenis lembar (tabel KSPE-2c) + ketiga ordo terisi + tutup rantai delta <= 1 mm
- [ ] HG-NEW-4: kesesuaian spek per ruang (poligon/label/nama/luas) lulus dengan coverage 100 persen tanpa sampling
- [ ] HG-NEW-5: clearance sirkulasi CIR-a..d lulus keempatnya tanpa pengecualian
- [ ] TG-A (v1.4): traversal graf akses - n_terperangkap = 0; semua ruang huni terjangkau LUAR lewat sisi ber-fungsi jalan
- [ ] TG-B (v1.4): 0 pelanggaran band luas per kategori program (metode TG-2)
- [ ] TG-C (v1.4): RP-1..RP-6 hijau; jalankan checker deterministik sebelum serah terima

---

## Delta v1.4 - Tata kelola ruang (CAD-IMPROVE-01; kartu t_909162a4)

Delta v1.4 dari blueprint `docs/2026-09-07-cad-improvement/identification/02_structured.md`
seksi 3.2 kelompok A. Akar defect B-02 (BL-02): ruang R-203 "Pojok Baca" hanya
tercapai lewat jendela, dan bilik sanitair lebih luas daripada ruang klinik; dua-duanya
lolos semua gerbang lama karena tidak satu pun uji lama memeriksa RELASI antar ruang.
Seksi ini ADITIF: Tahap 1-6, KSPE v1.2, dan checklist lama tetap berlaku utuh.

### TG-1 Topologi akses dan nol ruang terperangkap

Setiap ruang huni wajib punya >= 1 bukaan ber-fungsi jalan (jenis pintu, `ambang == 0`).
Bangun graf ruang-ke-ruang: simpul = seluruh `ruang[]` + koridor + simpul virtual `LUAR`;
sisi = bukaan yang tersisi dua ruang, atau sisi ruang-`LUAR` bila dinding inangnya
`eksterior == true`. Sisi kedua bukaan dibaca dari `bukaan[].ruang_ref_2` bila terisi;
bila kosong, resolve geometris lewat titik-dalam offset tengah bukaan sebesar
+(tebal/2 + 50) mm. Uji: (a) derajat tiap ruang huni >= 1 lewat sisi jalan; (b) BFS dari
`LUAR` menjangkau SEMUA ruang huni; (c) n_terperangkap == 0; (d) koridor terhubung
`LUAR` >= 1 jalur. Jendela TIDAK dihitung sebagai sisi (kasus B-02: R-203/J25).

### TG-2 Band luas per kategori

Tiap kategori program punya band luas yang harus dimasuki. Angka benchmark puskesmas
dua lantai dibekukan di blueprint misi seksi 6.3 dan berstatus PARAMETER BENCHMARK TA
(target desain uji), BUKAN kutipan regulasi; dilarang dikutip sebagai angka Permenkes.
Untuk subjek lain, band diturunkan dengan metode yang sama: satu band per kategori dari
standar praktik yang dirujuk, lalu dikunci di KSPE sebelum gambar diterbitkan.

### TG-3 Larangan sanitair mendominasi

Tidak boleh ada bilik atau ruang sanitair tunggal dengan luas melebihi luas ruang
klinik/admin TERKECIL dalam program (aturan RP-2; pelanggaran pasangan == 0). Kasus
B-02 yang wajib terdeteksi: KM/WC 11,9 m2 lebih luas daripada ruang guru 7,76 m2.

### TG-4 Landing pintu ruang sempit

Pintu pada ruang dengan dimensi terpendek < 1500 mm wajib punya landing bebas
1200 x 1200 mm di KEDUA sisinya (memperketat aturan lama "pintu buka keluar bila sempit").

### TG-4a Keluaran tahap (tulis ke PROJECT.json)

`spek_elemen.topologi[]` = matriks adjasensi ruang x bukaan: `{ruang, buukaan[],
tetangga[], derajat}` per ruang huni; `spek_elemen.rasio_program` = daftar aturan yang
dipakai (`RP-1..RP-6`) + `band_dirujuk`. Keduanya ditulis oleh skill ini, dibaca oleh
checker HG-IMP-2/HG-IMP-3 dan oleh orkestrator saat melepas tugas disiplin hilir.

### TG-5 Aturan rasio program RP-1..RP-6

| ID | Aturan |
|----|--------|
| RP-1 | Tiap ruang klinik/gawat/farmasi/admin masuk band DAN >= 12 m2 (diagnostik tunggal; imunisasi >= 9) |
| RP-2 | Tidak ada bilik/ruang sanitair tunggal dengan luas > luas ruang klinik/admin TERKECIL (pelanggaran pasangan == 0) |
| RP-3 | Efisiensi program = sum(luas klinik+gawat+farmasi+admin+rapat+tunggu+lobby) / sum(seluruh luas ruang huni) >= 0,65 |
| RP-4 | Tunggu lantai 1 >= 24 m2; tunggu lantai 2 >= 16 m2; lobby >= 15 m2 |
| RP-5 | WC difabel dalam band dan lebar bebas pintu >= 900 + lingkaran balik 1500 tergambar |
| RP-6 | TPS limbah B3 punya pintu langsung ke LUAR (graf sisi LUAR) + ventilasi mekanik tercatat di MEP |

Band dan angka RP di atas adalah parameter benchmark TA untuk subjek puskesmas; untuk
subjek lain, ganti angkanya lewat KSPE proyek tersebut - jangan memaksakan angka
puskesmas pada bangunan jenis lain.

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

Profil pemilik: `gsp-architecture-specialist` | Konsumen wajib: gsp-engineering-analyst, gsp-power-specialist, gsp-3d-specialist | Tier: ALWAYS (arch)

- Skill fisik profil pemilik: `gsp-architecture-workflow`, `gsp-architecture-code-compliance`.
- `pustaka-teknis`/EKAS: GSB/KDB/KLB/KDH & ergonomi WAJIB bertanda `[R-n, sumber, hal]` (aturan R1-R5).
- `gsp-document-quality-standards`: mutu teks keluaran.
- `gsp-spatial-psychology`: dasar perseptual zoning & hierarki ruang (defensible
  space Newman, elemen Lynch, proxemics, prospect-refuge) — alasan di balik
  publik→privat dan uji wayfinding denah (delta v1.4.1, SPATIAL-PSI-0930).

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
