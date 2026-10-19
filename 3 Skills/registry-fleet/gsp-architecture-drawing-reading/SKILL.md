---
name: gsp-architecture-drawing-reading
description: "Membaca & menafsirkan gambar arsitektur (denah, tampak, potongan, detail, site plan): ekstraksi informasi, QA konsistensi dimensi, verifikasi geometri via vision_analyze + script, dan narasi penjelas. Muat saat ada gambar arsitektur untuk dibaca/diulas/dijelaskan."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: architecture
    tags: [architecture, drawing-reading, plans, vision, qa, dimensions, interpretation]
---

# GSP Architecture Drawing Reading

> Kemampuan membaca & menafsirkan gambar arsitektur: dari gambar raster (foto/scan denah,
> tampak, potongan, detail, site plan) maupun deskripsi/vektor, menjadi informasi terstruktur
> dan narasi yang jelas. Dipakai untuk QA paket gambar, memeriksa konsistensi antar gambar,
> atau menjelaskan desain kepada non-arsitek.

## Alur Membaca Gambar

1. **Siapkan gambar** — identifikasi jenis: site plan / denah / tampak / potongan / detail /
   RCP / jadwal. Tentukan skala & kop gambar bila terlihat.
2. **Baca secara berlapis:**
   - a. **Denah:** dinding (tebal tipis), bukaan (pintu/jendela - arah bukaan), level/elevasi,
     dimensi antar as, grid kolom, perabot (jika ada), label ruang, tangga/ramp/lift/shaft.
   - b. **Tampak:** orientasi fasad, material penutup (notasi), elevasi lantai/atap,
     proporsi bukaan, railing/kanopi, tingkat & overstek.
   - c. **Potongan:** ketinggian lantai-ke-lantai, tinggi plafon, struktur (balok/kolom/plat),
     detail sambungan, profil atap, level tanah ±0.000.
   - d. **Detail:** skala besar (1:20/1:10/1:5), material & lapisan (label), dimensi presisi,
     urutan pemasangan.
   - e. **Site plan:** orientasi utara, sempadan (GSB), akses jalan, drainase, zona hijau,
     hubungan tapak-bangunan.
3. **Ekstrak data kunci** (output wajib bila tersedia): dimensi utama, luas ruang, jumlah
   lantai, material dominan, sirkulasi, jumlah eksit, level/elevasi.
4. **Verifikasi silang:** cek konsistensi antar gambar (denah ↔ potongan ↔ tampak),
   bandingkan luas ruang vs program, cek dimensi tangga (lihat script), cek GSB/sempadan.
5. **Narasi penjelas:** susun penjelasan dalam bahasa user (Indonesia/Inggris) - bentuk,
   organisasi ruang, sirkulasi, sistem struktur, material, kekuatan/kelemahan, saran.

## Menggunakan vision_analyze untuk Gambar Raster

- Toolset `vision` melekat pada profil ini: gunakan `vision_analyze` pada file gambar
  (DENAH_SCAN.png, dsb.) untuk membaca teks/dimensi/notasi yang terbaca.
- **Wajib cross-check:** hasil vision bisa keliru membaca angka/simbol — konfirmasi dengan
  hitungan (mis. luas dari dimensi bertanda) dan konsistensi antar gambar. Jangan pernah
  menuliskan angka dari gambar tanpa menyatakan "terbaca di gambar" + nilai alternatif bila
  meragukan.
- Bila gambar adalah PDF: ekstrak halaman sebagai PNG (pdftoppm) lalu vision_analyze per
  halaman; untuk halaman teks gunakan pdf skill.

## Simbol & Notasi Umum yang Harus Dikenali

| Simbol/Notasi | Makna |
|---------------|-------|
| Garis tebal | dinding terpotong bidang |
| Garis tipis/putus | elemen di luar bidang / tersembunyi |
| Panah dimensi + angka | jarak antar as / ukuran (m/mm) |
| Lingkaran kecil pada dinding | bukaan pintu (busur arah bukaan) |
| Trapesium di dinding | bukaan jendela (atau simbol ganda) |
| Anak panah ke atas/bawah | arah tangga naik/turun (landing ditandai) |
| Kotak dengan salib | kolom struktur / shaft |
| Level ±0.000, +3.200 dst. | elevasi lantai relatif |
| Notasi material (hachure) | bata, beton, kayu, tanah (lihat legenda gambar) |
| Simbol utara (N) | orientasi site plan |
| Label "A-101", "S-201" | nomor lembar disiplin |

## QA Konsistensi Gambar (ceklis)

- [ ] Dimensi denah ↔ potongan: tinggi lantai-ke-lantai konsisten
- [ ] Luas ruang (dari dimensi) ↔ program ruang: selisih wajar (≤ ±5–10%)
- [ ] Tangga: jumlah anak tangga × tinggi/langkah = tinggi antar lantai (script stair_check)
- [ ] Tampak ↔ potongan: ketinggian plafon/atap konsisten
- [ ] Site plan ↔ denah: posisi bangunan terhadap GSB sesuai
- [ ] Eksit: jumlah tangga/exit sesuai okupansi (rujukan gsp-architecture-code-compliance)
- [ ] Pintu/jendela: tanda bukaan konsisten antar denah

## Script `stair_check.py`

Cek geometri tangga dari input: tinggi lantai (floor-to-floor), jumlah anak tangga
(n_tread), tinggi anak tangga (riser) & lebar injakan (tread) bila diberikan.

```bash
python3 stair_check.py --floor_h 3.20 --n 18        # cek riser dari tinggi & jumlah
python3 stair_check.py --riser 0.18 --tread 0.28    # cek 2R+T terhadap pedoman
```
Pedoman praktis: riser ±15–20 cm, tread ±25–30 cm, 2×riser + tread ≈ 60–63 cm; cek juga
standar SNI/permensetempat untuk hunian & bangunan publik (kondisi tangga aman &
aksesibel). Output: status OK/REVIEW + saran.

## Pitfalls

- Jangan menebak angka bila tidak terbaca — tulis "tidak terbaca di gambar" dan usulkan
  verifikasi ke sumber.
- Jangan mengklaim "denah tidak konsisten" tanpa menyebut lembar/posisi persis.
- Notasi material antar drafter berbeda — selalu lihat legenda/kop gambar dulu.
- vision_analyze bukan pengganti pengukuran presisi: untuk angka kritis (lebar exit,
  dimensi struktur) minta file asli/vektor atau konfirmasi.

## Verifikasi

Output pembacaan gambar memuat: jenis & identitas gambar (nomor lembar bila ada), ringkasan
data (dimensi/luas/level/material), hasil QA konsistensi (ceklis + script output), dan narasi
penjelas. Klaim "dibaca dari gambar" selalu menyebut sumber visualnya.