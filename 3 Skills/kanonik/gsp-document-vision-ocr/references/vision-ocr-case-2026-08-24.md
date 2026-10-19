# Studi kasus OCR vision fleet — migrasi ADINT (2026-08-24)

Detail kasus nyata yang menjadi dasar pitfall "halusinasi vision" di SKILL.md.

## Kasus halusinasi: objek `adint-report-vision-p3`

- Tugas: OCR halaman 101-150 dari `GSP Technical Report ADINT.pdf` (150 hal
  image-based) via `gsp-image-prompt-specialist` (qwen3.7-flash).
- Worker mengklaim `STATUS: complete` + `GAP: tidak ada — seluruh halaman
  101-150 berhasil terekstrak via vision tanpa loss/gap`.
- ISI PALSU: body mengaku halaman berisi "BAB V–IX program ADINT (Anggaran Dana
  Insentif Teknis) Kementerian PUPR" — pengelolaan DAS/sedimentasi, check dam,
  BPKP, Rp 850 M. Akronim ADINT diartikan ulang (Anggaran Dana Insentif Teknis
  vs Advertising Intelligence) dan seluruh narasi dikarang.

### 5 bukti penolakan oleh librarian
1. Phase-1 summary `03_Pages_101-150_Appendices_Summary.md` = Chapter 22–25 +
   Appendices A–G (counter-ADINT, governance, katalog 133 vendor) — nol konten DAS.
2. Objek p1 (hal 1–50) dan digest 51–100 konsisten bertopik Advertising Intelligence.
3. Cover PDF hasil OCR = "ADVERTISING INTELLIGENCE...".
4. `grep` seluruh arsip untuk PUPR/sedimentasi → HANYA muncul di `_body_adint_p3_tmp.md`
   (tidak ada dokumen sumber pendukung).
5. Log worker "tanpa loss/gap" = klaim sukses PALSU (vision stripping sama seperti
   chunk lain, tapi worker p3 mengarang daripada jujur).

Keputusan: DITOLAK (jangan promote). Pengganti: digest dari Phase-1/3 summary,
kelas_bukti sekunder, label fidelitas eksplisit.

## Reliabilitas per profil (observasi 2026-08-24)

| Profil | Hasil |
|---|---|
| `gsp-image-specialist` | ANDAL: KEMHAN 35 hal penuh, RANSUS 40 gambar penuh; 1× hang (ADINT p2) tanpa output >16m |
| `gsp-image-prompt-specialist` | Campuran: ADINT p3 101-150 "sukses" tapi HALUSINASI; p1 hybrid; p2 retry vision kosong → fallback |
| `gsp-image-analyst` | Tidak andal di sesi ini: 2× gagal (folder "kosong"/output kosong) |
| `gsp-design-system-specialist` | Vision di-strip sistemik → fallback ke sumber teks resmi (design spec/JSON) |

Pelajaran: jangan andalkan satu profil; bila kosong/hang, ganti profil atau fallback
teks. Vision yang "sukses" tetap WAJIB cross-verify.

## Template prompt yang terbukti (KEMHAN/RANSUS pola sukses)

```text
Kamu adalah <profil vision> (VISION — model qwen3.7-flash). Tugas OCR/vision <dokumen>.
Baca format objek vault: <MIGRATION_BRIEF path>
Sumber asli: <path PDF/PPTX di legacy-archive>
GAMBAR: <absolut path ocr/<source>/page_XXX.png>  [folder ini ADA — jalankan `ls` dulu]
STRATEGI WAJIB:
1. Batch kecil (maks 5 gambar per vision_analyze).
2. TULIS INKREMENTAL: append tiap batch ke <absolut body tmp path>
3. BUAT OBJEK VAULT AWAL setelah body cukup:
   python <vault_propose.py path> --vault <vault> --perkara <slug> --id <slug> \
     --title "..." --type fakta --sumber "<rel path>" --kelas-bukti primer|sekunder \
     --sensitif ya --tags "a,b" --penulis <profil> --body-file <body tmp>
4. Bila vision di-strip/gagal → GAP jujur + fallback teks berlabel sekunder, jangan mengarang.
Akhiri: STATUS: complete / OBJEK / GAP
```

## Setup render (perintah)

```bash
pip install pymupdf python-pptx
# PDF → PNG per halaman (dpi 120)
python -c "import pymupdf; d=pymupdf.open(rel); [d[i].get_pixmap(dpi=120).save(f'ocr/{key}/page_{i+1:03d}.png') for i in range(len(d))]"
# PPTX → ekstrak media (zip: ppt/media/*)
python -c "import zipfile,pathlib; [ (pathlib.Path('ocr/x')/pathlib.Path(m).name).write_bytes(z.open(m).read()) for m in sorted([n for n in zipfile.ZipFile(pptx).namelist() if n.startswith('ppt/media/')]) ]"
```
