# GSP-DS-KARTU - preset `BUSINESS` (slug: business)
Sumber: `study/DS-business.md` (10 halaman, coverage_verified=True) + `study/DS-batch-ALL.json` (mesin-baca). Generator: SM-1 t_de708ae3 2026-09-01.
Legenda sumber palet: tercetak='HEX dicetak eksplisit di dokumen sumber', terukur-piksel='dominan terukur dari piksel PNG (DS-palet-TERUKUR.json, hasil controller) - dipakai untuk mengisi slot yang TIDAK_TERBACA di file DS', estimasi-vision='perkiraan pembacaan vision, BUKAN nilai spesifikasi'.

## Palet (role → hex; satu-satunya definisi nilai = gsp-ds-sets.json)

| name | hex | role | source |
|---|---|---|---|
| Navy gelap (aksen primer) | `null` | breadcrumb, ikon, header tabel, metrik, footer | TIDAK_TERBACA - tidak ada HEX tercetak |
| Putih dominan | #F0F0F0 | measured dominant 85.37% (latar putih) | terukur-piksel |
| Abu teks/netral | #9090A0 | measured 3.49% | terukur-piksel |
| Abu medium | #A0A0B0 | measured 2.33% | terukur-piksel |
| Hijau indikator positif | `null` | delta positif / status On Track | TIDAK_TERBACA |
| Merah status buruk | `null` | tidak dicontohkan di dokumen | tidak ada di rak (GAP-4) |

**usage_ratio:** visual: ±80% putih, navy satu-satunya aksen kuat, hijau hanya sinyal positif (tanpa angka tercetak)

**Mood / positioning:** profesional · kredibel · disiplin · decision-oriented · anti-dekoratif · gaya konsultan manajemen

## Tipografi (kutipan verbatim dari file DS - angka hanya bila tercetak)

- Typeface: TIDAK_TERBACA (nama font tidak dicetak). Satu keluarga sans-serif grotesk netral di seluruh dokumen; terlihat seperti Helvetica/Arial/Inter-class. Tidak ada serif, tidak ada display face.
- Hierarchy yang teramati (ukuran absolut tidak dicetak; estimasi relatif):
  - Display/halaman-judul: ALL CAPS, weight paling berat (Black/ExtraBold), ±2,5–3× body - contoh "BUSINESS COMMUNICATION SYSTEM" (p1), "FINANCIAL & COMMERCIAL VIEW" (p3).
  - Subjudul tagline: Bold, navy, 1 kalimat, format "[Verb] the [object]..." - selalu ada di bawah judul (p1–p10).
  - H2 bagian: Bold, hitam, UPPERCASE atau Title Case (mis. "REVENUE BRIDGE (Annual, USD)", "KEY TAKEAWAYS").
  - Label komponen/kolom: UPPERCASE kecil, regular/medium, abu atau navy (mis. "REVENUE", "STATUS", "DELIVERABLE").
  - Body: Regular, abu gelap, kalimat pendek 1–3 baris per item.
  - Angka metrik: Bold besar (display angka), sering disertai delta kecil berwarna.
  - Caption/footer: satu kalimat bold navy rata-tengah di dasar halaman; teks sumber ("Source: ...") kecil di dasar slide contoh.
- Aturan tipografi eksplisit dari dokumen: judul slide = kalimat insight penuh ("Revenue grew 18%, driven primarily by recurring contracts."), bukan label topik (p8 footer).

## Layout & Grid

- Kanvas: landscape 16:9-ish, background putih, margin putih lega.
- Pola tulang punggung semua halaman: breadcrumb "NN / GENERAL BUSINESS PRESENTATION SYSTEM" kiri-atas → judul + subjudul + intro kiri → konten grid tengah → footer kalimat penutup tengah-bawah.
- Split kolom yang berulang: kiri 60% / kanan 40% (p1, p2); tiga kolom bawah ±30/35/35 (p3); kiri-list vs kanan-mockup (p4, p8); sidebar kanan "HOW TO READ THIS"/"NEXT 30 DAYS" (p5, p9).
- Komponen grid lain: flow horizontal 4 langkah dengan panah (p1); 5 kolom prinsip dengan divider vertikal (p1); KPI cards 3×2 + 1 kartu lebar (p3); tabel metrik 5 baris × 7 kolom (p5); matriks 4 fase × 5 baris atribut (p9); chevron 5 tahap × 4 baris Owner/Activity/Output/KPI (p10).
- Pemisah: garis abu tipis horizontal & vertikal menggantikan kotak; border tipis pada kartu; header tabel navy dengan teks putih.
- Spes grid numerik (kolom/gutter/px): TIDAK_TERBACA - tidak dicetak.

## Komponen
- breadcrumb 'NN / GENERAL BUSINESS PRESENTATION SYSTEM'
- hero title block + tagline navy
- process flow 4-5 langkah
- callout SO WHAT?
- EXECUTIVE SNAPSHOT box
- KPI card + delta
- waterfall chart
- line chart multi-seri
- tabel header navy
- comparison matrix ✓/⊖/✕
- weighted scorecard
- recommendation box
- timeline milestone + roadmap chevron
- RACI dot-matrix
- footer kalimat penutup (semua halaman)

## Aturan & larangan (negatives-list)
- setiap slide harus menggerakkan diskusi maju (p1)
- judul slide = kalimat insight, bukan label topik (p8)
- anatomi slide 8 elemen wajib termasuk Source (p4)
- hierarki eksekutif Takeaway→Implication→Evidence→Context→Detail (p8)
- 8 layout kanonik; KPI wajib change/target/status/trend (p5, p6)

## GAP (jujur - jangan diisi karangan)
- nol HEX & nol nama font tercetak
- spes grid numerik tidak dicetak
- status negatif tidak dicontohkan
- penomoran slide internal acak vs urutan PDF

STATUS: complete

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
