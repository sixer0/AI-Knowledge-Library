# Structural Analysis

**REF-CIV-001** · **R3 — buku teks rekayasa** · Domain **CIVIL-STRUCTURAL**
**Penulis:** Russell C. Hibbeler · **Terbit:** 2017, Pearson
**Berkas:** 736 halaman · 274 bookmark · `R3/CIVIL-STRUCTURAL/`
**Disusun:** 21 Agustus 2026, dari daftar isi dan isi buku ini

---

## Untuk apa buku ini dipakai di GSP

**Menghitung gaya dalam pada rangka yang menopang perangkat** — menara antena, tiang kamera,
rangka atap ruang perangkat, dudukan panel surya. Selama ini rak sama sekali tidak punya
sandaran untuk pekerjaan itu; setiap pertanyaan "kuat atau tidak" hanya bisa dijawab
"tanyakan ahli struktur".

Buku ini menjawab **berapa gaya yang bekerja**, bukan **bahan apa yang dipakai** — untuk
yang kedua, lihat REF-CIV-003 (baja) dan REF-CIV-002 (beton).

## Susunan

| Bab | Isi | PDF |
|---|---|---|
| 1 | Jenis struktur · **beban** · perancangan struktur | **15** |
| 1.3 | **Beban** — mati, hidup, angin, gempa, salju | **21** |
| 2 | Idealisasi struktur · jalur beban · **determinasi & kestabilan** | **47** |
| 2.5 | **Determinacy and stability** — apakah struktur dapat dihitung | **63** |
| 3 | **Rangka batang (truss)** — metode simpul & potongan | **95** |
| 3.3 | Metode simpul | **108** |
| 3.5 | Metode potongan | **114** |
| 3.8 | **Rangka ruang (space truss)** — menara | **128** |
| 4 | Gaya dalam pada balok & portal | **151** |

Bab 3 dan 3.8 yang paling langsung berlaku: **menara antena adalah rangka ruang.**

## Yang dapat dipakai langsung

- **Bab 1.3 — jenis dan besaran beban.** Titik awal setiap perhitungan: beban mati
  perangkat, beban angin pada antena/kamera, beban pemasangan.
- **Bab 2.5 — determinasi dan kestabilan.** Menjawab apakah sebuah rangka **dapat**
  dihitung dengan statika sederhana atau menuntut analisis tak tentu.
- **Metode simpul dan potongan** — cara memperoleh gaya batang tanpa perangkat lunak.
- Diagram gaya lintang dan momen untuk balok penopang.

## Batas pemakaian

> **Buku ini memberi metode analisis, bukan ambang lulus.** Berapa tegangan yang boleh
> ditahan sebuah batang **bukan** dari sini — itu dari standar bahan (AISC untuk baja, ACI
> untuk beton) atau **SNI**, yang **tidak ada di rak**.

⚠ **Konteksnya Amerika.** Beban angin dan gempa mengacu ASCE 7. **Indonesia memakai SNI
1727 (beban) dan SNI 1726 (gempa)** — keduanya **tidak ada di rak** dan angkanya berbeda.
Untuk pekerjaan di Indonesia, **metode** dari buku ini boleh dipakai; **angka bebannya
tidak**.

**Perhitungan struktur yang menanggung keselamatan orang harus ditandatangani ahli
bersertifikat.** Buku ini membuat GSP mampu memeriksa dan berdiskusi, bukan menggantikan
tanda tangan itu.

## Menopang

| Rantai / gate | Bagaimana |
|---|---|
| **G2** | Alternatif konfigurasi dudukan beserta alasan penolakannya |
| **G3** | Hitungan gaya batang — ditandai `PROJECT-DERIVED`, diperiksa orang kedua |
| Rantai **D** (pembumian & petir) | Menara yang dihitung di sini juga membawa terminal udara |

**Celah yang tersisa:** SNI 1726 & 1727, AISC, ACI — seluruhnya R1/R2, **tidak ada di rak**.
