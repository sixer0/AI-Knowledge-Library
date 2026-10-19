---
name: gsp-deterministic-drafting
description: Use when drawing dimensioned plans or fixing dimensions.
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, architecture, drafting, verification]
    category: engineering
---

# Deterministic Drafting — Gambar Kerja Presisi dari Data

Kelas tugas: denah, tampak, potongan, detail, tabel ruang, situasi tapak — keluaran
yang memuat ANGKA DIMENSI. Preseden (07-09, rumah 10x15 3 lantai 6 kamar): iterasi 1
memakai image generator untuk denah + blueprint diketik manual → user vonis "banyak
sekali kesalahan dalam perhitungan dimensi". Akar: program ruang 308,75 m2 vs tapak
150 m2, tanpa satu pun uji penutupan. Iterasi final lolos setelah geometri digambar
parser dari data dengan assertion.

## Aturan inti (WAJIB)

1. **Image generator HANYA untuk estetika/render konsep.** Denah, tampak, potongan,
   detail, dan tabel dimensi WAJIB digambar dari data model oleh skrip. Label dimensi
   pada gambar AI tidak bisa dipercaya dan terbaca sebagai angka sungguhan oleh user.
2. **Sumber kebenaran = data model, bukan narasi.** Setiap ruang = rect (x1,y1,x2,y2)
   dalam dict per lantai. Gambar, tabel, dan laporan semuanya dibaca dari struktur sama.
3. **Semua angka terbit dihitung parser** (SPK-002 butir 6): luas, keliling dinding,
   KDB/KLB/KDH, rumus tangga — bukan diketik.
4. Bila user menuntut "cari materi relevan": gali korpus internal dulu (paket skill
   CAD di workspace, EKAS) — mesin pencari umum untuk kueri arsitektur niche
   menghasilkan noise; catat sumber yang benar-benar dipakai.

## Gerbang numerik yang ditegakkan assertion (WAJIB sebelum render)

| Gerbang | Uji |
|---|---|
| Penutupan lantai | sum luas ruang == target massa per lantai (mis. 110,00 m2), toleransi 1e-6 |
| Overlap | irisan pairwise antar rect == 0 |
| Kamar | luas >= 9 m2 dan sisi terpendek >= 2,70 m (standar Indonesia; cad-architecture-design) |
| Akses | pasangan ruang bertetangga wajib berbagi tepi dengan irisan >= 0,80 m (daun pintu); ruangkan akses dideklarasikan eksplisit per lantai → cacat akses harus 0. Pola sah: hall-transit (tangga/hall sebagai pintu masuk ruang lain), jangan andalkan "sentuh-sudut" |
| Tangga | 2r+t dalam 600-650 mm; run flight+bordes <= rongga shaft; HEADROOM >= 2,00 m diuji terhadap pelat — bila gagal (mis. 1,62 m), solusi desain = VOID potongan pelat di atas flight, digambar di denah lantai atas + potongan, bukan diklaim |
| Tapak | KDB <= 80 %, KDH >= 10 %, KLB vs jumlah lantai; tampilkan BATAS benar (KDH `>=`, bukan `<=`) |

## Aturan tata letak label (hasil 3 putaran QA visual)

- Ruang sempit (sisi terpendek < 1,6 m): label dibaca VERTIKAL (rotation=90) mengikuti
  sisi panjang; label horizontal akan melewati dinding dan menabrak ruang tetangga.
- Semua label teks diberi mask `bbox=dict(boxstyle="square",fc="white",alpha=1.0)` agar
  tidak tertimpa arsir garis tangga.
- Di ruang tangga: gambar arsir + panah DULU, lalu blok label ditaruh di zona atas
  ruang (di atas garis anak tangga pertama), panah naik di tepi kiri, jangan diagonal
  memotong teks.
- Label VOID kecil di TENGAH kotak void (anchor center), jangan di sudut (menimpa
  garis dinding).
- Kop gambar: pakai `fig.text` di margin luar + `fig.add_axes` eksplisit, bukan
  koordinat transAxes negatif (rawan menabrak tabel/objek saat bbox_inches=tight).
- Setelah render PNG: QA independen via vision_analyze ("ADA/TIDAK tabrakan teks +
  lokasi"), perbaiki generator (bukan gambarnya), render ulang, verifikasi ulang.
  Vonis visual user = pulih-sistem (D-INT-11), jangan tambal gejala.

## Resep teknis

- Runner: `uv run --python 3.11 --with matplotlib --with ezdxf python gen.py`
  (pitfall: `python` lepas bisa jatuh ke alias Store; paket wajib disebut eksplisit).
- matplotlib: `matplotlib.use("Agg")`, `ax.set_aspect("equal")`, `axis("off")`,
  simpan dpi>=170 `bbox_inches="tight"`.
- DXF: warna layer ezdxf harus INTEGER ACI (mis. 7), bukan string "7" → TypeError
  validator. Satu modelspace per lantai, layer WALL/ROOM/DIM/TITLE.
- f-string: jangan sarang kutip/ekspresi kompleks di dalam f-string tabel — bug
  SyntaxError nyata terjadi di sini; hitung dulu ke variabel.
- Format angka Indonesia: `f"{v:.2f}".replace(".",",")`.

## Urutan kerja kelas tugas ini

1. Dump brief → data model per lantai (rect + tipe) + parameter tapak.
2. Tulis skrip generator berisi `verify()` dengan assertion di atas; JALANKAN dulu,
   fail = perbaiki data, baru render.
3. Render PNG lembar (situasi, denah/lantai, tampak, potongan, detail, tabel ruang +
   rekap gerbang) + DXF editable.
4. vision_analyze QA loop sampai tabrakan teks = 0.
5. Laporan MD: tabel gerbang terukur + register asumsi + status PRELIMINARY (bukan
   dokumen PBG; struktur prabayakan, wajib uji tanah).
6. Gerbang naturalisasi keluaran user (U+2014=0, U+00B7=0) sebelum serah; taut MEDIA.

## Pitfall warisan

- Blueprint diketik manual = sarang inkonsistensi; selalu konversi ke data dulu.
- `done` visual tanpa uji akses = denah tak bisa dihuni; gerbang akses menemukan
  foyer-terputus yang lolos dari mata.
- Jangan restart dari nol tiap iterasi: ubah data model, render deterministik ulang.

## Support files

- `references/session-2026-09-07-rumah-10x15.md` — angka final terverifikasi + recipe
  perbaikan headroom/akses sebagai contoh terapan.
- `templates/gen_drawing_skeleton.py` — kerangka generator (data model + verify +
  plan/elev/section/label rules) siap disalin per misi.
