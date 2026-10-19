# Varian studi: korpus design-system image-only → spesifikasi token mesin-baca

Kasus nyata 2026-09-01 (kontrak `docs/2026-09-01-master-design-adaptasi/`):
`MASTER_DESIGN/design system/` = 13 set PDF style-guide GSP (BNN, BNPT, Business,
Cyber Security, GENERAL, Millitary, Polri, TNI AD/AL/AU, Teknik, Visual, Kemhan;
10–25 hal per set, total 190) — **0 karakter lapisan teks** (terverifikasi pymupdf).
Tujuan: bukan objek vault, tapi spesifikasi token per set untuk hilir (Skill Manager
meng-improve skill asset/slide/master-prompt/HTML artifact yang SUDAH ADA).

## Alur yang terbukti jalan

1. **Preflight teks** tiap PDF (`pymupdf` get_text per halaman). Nol → vision.
   Campuran dalam satu repo itu biasa: design system = image-only, dokumen sistem
   = berteks lengkap. Jangan dispatch vision untuk yang berteks.
2. **Render SEMUA halaman**, dpi 120, `render_all/<slug_set>/page_NN.png`
   (generator: `scripts/render_pdf_pages.py`). Jangan sampling — halaman tengah/akhir
   justru berisi komponen & aturan.
3. **Partisi set** ≤2 worker profil sama (`gsp-design-system-specialist`), scope per
   worker mutually exclusive. Bridge FIFO 1 request/iterasi, RUN_TIMEOUT 30m →
   kontrak TULIS INKREMENTAL per set supaya progres bertahan lewat timeout.
4. **Kontrak prompt** (template di bawah): path absolut; `ls` dulu sebelum vision;
   batch ≤5 halaman/panggilan `vision_analyze`; nilai tak terbaca = `TIDAK_TERBACA`,
   DILARANG mengarang hex/nama font; output `DS-<slug>.md` per set + ringkasan JSON.
5. **Worker = pembaca murni**: larangan eksplisit "JANGAN membuat/mengedit skill"
   di prompt — penulis perubahan skill adalah hilir (SM pasca-TA), sesuai prinsip
   penulis≠verifikator dan lane pekerja.

## Struktur output DS-<slug>.md (bagian wajib)

```
# Design System: <nama set>
Sumber: <path> (N halaman, OCR vision <tanggal>)
## Identitas & Mood      — kata kunci, sektor, tone
## Warna                 — tabel nama | HEX | peran (primary/aksen/latar/teks) | hlm sumber
## Tipografi             — family terlihat; hierarchy display/H1..H4/body/caption
## Layout & Grid         — margin, kolom, ratio slide, pola komposisi
## Komponen              — tombol, kartu, ikon style, chart, header/footer, logo
## Ikonografi & Ornamen  — gaya garis, simbol khas, watermark/klasifikasi
## Aturan khusus         — klasifikasi Terbatas, larangan eksplisit
## Halaman referensi     — 1 baris per halaman
## GAP                   — apa yang TIDAK_TERBACA/ambigu
```

Skema ringkasan JSON per batch:
`[{set, palette:[{name,hex,role}], fonts:[], mood:[], components:[], rules:[]}]`

## Diffing korpus berteks (CORE vs DELTA) — tanpa LLM

Untuk N dokumen seragam (kasus: 7 dokumen GSP-SDT, 10 klausul identik + varian matra):
ekstrak teks, lalu bandingkan perbendaharaan kata panjang (≥7 huruf):
- irisan semua dokumen = **CORE SHARED** (aturan seragam)
- selisih per dokumen = **DELTA per varian** (mis. AD→Alutsista/Ditajenad,
  AU→Airworthiness/Bhuwana, CY→FND-Kx-nnn/advisory, BIZ→INCOTERMS/anggaran)
Ini memvalidasi klaim "seragam + delta" tanpa membaca penuh tiap dokumen, dan murah.
Filter stopword domain (nama perusahaan, 'terbatas', 'dokumen') sebelum diff.

## Pola skrip diffing (inti)

```python
import re
def words(t): return set(re.findall(r"[A-Za-z][A-Za-z\-]{6,}", t))
common = None
for slug, txt in docs.items():
    w = words(txt); common = w if common is None else common & w
STOP = {"gemilang","perkasa","terbatas","dokumen","teknis","sistem","verifikasi"}
for slug, txt in docs.items():
    delta = sorted(w for w in words(txt) - common if w.lower() not in STOP)
    print(slug, "->", delta[:20])   # identitas khas varian
```

## Verifikasi sebelum lanjut ke hilir
- Jumlah `page_NN.png` per set == jumlah halaman PDF (cetak dari manifest render).
- Tiap `DS-*.md` punya bagian Warna BERHEX atau GAP eksplisit — hex tanpa halaman
  sumber = curiga halusinasi, kembalikan ke worker.
- Ringkasan batch-A + batch-B digabung → satu peta keluarga (konstanta bersama vs
  pembeda) sebelum masuk TA/SM.
