---
name: datum-house-style
description: "Bangun/lint dokumen standar DATUM: token gaya tunggal, register angka datumbind, lint 38+23 cek, builder docx/xlsx/pptx, audit+embed font, pustaka chart+simbol, baterai figur ENH-E. v2.5.2 (C22-PLURAL 16-10)."
version: 2.5.2
author: GSP (rebuild GAP-09 DHS-RB-01..05; integrasi daftar instrumen DHS-DIST-05; ENH-A/C/D/E/F konsolidasi manual terpadu 08-10)
license: MIT
metadata:
  hermes:
    tags: [gsp, datum, docx, house-style, tokens]
    category: gsp
---

# DATUM House Style v2.1.0 — inti token + instrumen lengkap

Paket gaya rumah DATUM untuk membangun dan mengaudit dokumen standar DATUM
(manual, proposal, laporan, workbook, deck, diagram). Muat skill ini setiap kali
tugas menyebut "bangun dokumen standar DATUM", "lint dokumen DATUM", "token
DATUM", "register kuantitas", atau nama spesifikasi `000/001/002-GSP-STD`.

## Status versi (WAJIB BACA)

Ini REBUILD lini baru **v2.0.0** (putusan GAP-09 05-10; kartu DHS-RB-01
t_0a8c6635 inti, DHS-RB-02 t_60780c73 lint berkas, DHS-RB-03 t_f9ae0289 lint
buku, DHS-RB-04 t_446765d6 diagram, DHS-RB-05 t_28d93e3c builder/render,
integrasi daftar instrumen DHS-DIST-05 t_30fb208e), BUKAN restorasi mesin
v1.8 Rev J. Mesin Rev J dan tokens.json 1.8 tidak ada di disk (vonis probe
05-10: 0 hit pada lima root). Setiap butir paket menunjuk sumbernya sendiri
(lihat kolom Provenans pada DAFTAR INSTRUMEN di bawah): spesifikasi 000/001
RevA, register ukur M01, garis builder DATMANUAL terbukti, atau arsip legacy
(hanya [`datumbind.py`](datumbind.py)). DILARANG mengklaim "restorasi Rev J" pada keluaran
mana pun. Sampai v2.0 lulus verifikasi independen (kartu DHS-VER-06), otoritas
sementara lapis aturan tetap IL `standars/manual-datum-002-datman-1004`
(vonis F22-REV4 PASS). Petakan 75 aturan -> instrumen adalah GAP-10, milik
controller misi (putusan D-6), BUKAN lingkup paket ini.

## RULE RAIL-BUKTI-DUA-MODA (marker RAIL-1008; kebijakan 08-10-2026, direktif user)

Pemilihan moda layout interior DATUM bersifat MEKANIS, bukan selera: builder menghitung
sitasi per paragraf dari naskah. ADA provenans per paragraf -> MODA A: kolom 128 mm +
rail bukti 32 mm (pgMar kanan 58 mm) dan rail WAJIB TERISI chip (peran token
`evidence_rail`: mono 5,9 pt upper ink400; mekanisme pPr/w:framePr w=1814 twips,
hAnchor=margin, offset x=7597, wrap=none - chip menempel paragraf host dan berpindah
halaman bersamanya; sitasi PINDAH lapis dari prosa, konten-kekal). TIDAK ADA -> MODA B:
margin kanan 20 mm, teks lebar penuh 166 mm. Keadaan "rail dialokasikan, chip nol"
DILARANG - preseden cacat EKASLAP-1006, EOSADINT-RevB, ADINPROP-RevA (pgMar 58 mm,
framePr=0 = pita mati; keluhan user 08-10). ASSERT byte jadi wajib di setiap builder:
G-RAIL-1 jumlah framePr body == jumlah sitasi pindah; G-RAIL-2 pola sitasi di w:t prosa
badan == 0 (aparatus SUMBER figur/tabel/lampiran dikecualikan); G-RAIL-3 konsistensi
dua-arah pgMar kanan 58 <=> chip>0, 20 <=> chip=0. Gagal = build exit nonzero (R-11.0).
BENTUK BYTE KANONIS UKUR (v2.3.1, kartu t_fcdd32ac): assert byte-jadi membandingkan
terhadap bentuk PASCA round-trip Word, bukan bentuk pra-save helper —
`<w:framePr w:w="1814" w:wrap="none" w:hAnchor="margin" w:x="7597"/>`
(konstanta `datum_docx.RAIL_FRAMEPR_POST`, token-driven). Word menormalkan CT_FramePr
saat repaginate+Save: `hRule`/`yAlign` dihapus karena memang nilai default dan urutan
atribut ditulis ulang; nilai makna (`hAnchor="margin"`, offset) kekal. Nama atribut sah
ECMA-376 adalah `w:hAnchor` - `w:anchorH` bukan anggota skema dan dibuang Word lalu
ditulis default `hAnchor="text"` (akar defect CTXWIN-1009; jangan pakai ulang).
Tambalan instrumen (helper rail_chip() di datum_docx + cek datum_lint) lewat jalur
defect->proposal gsp-skill-manager; sampai ditambal, gerbang jalan per-misi di ASSERT
builder. Speks: <ws>/docs/2026-10-08-adint-proposal-1008/SPEKS-RAIL-1008.md.

## DAFTAR INSTRUMEN (final v2.1.0)

Semua instrumen token-driven: palet/wajah/grid dibaca dari [`tokens.json`](tokens.json) lewat
resolver `datumbind.tokens_path()` — tidak ada heks/nama font hardcoded di modul
(checked oleh selftest). Interpreter nyata host ini: pola `uv` di bawah.

| # | Instrumen | Fungsi | Cara pakai | Provenans (sumber) | Gerbang jalan |
|---|---|---|---|---|---|
| 1 | [`tokens.json`](tokens.json) | Token palet/tipografi/grid TUNGGAL; bila prosa dan token bertentangan, token menang | dibaca lewat `tokens_path()`, jangan hardcode | builder DATMANUAL (build_manual_datum.py baris 42-67), build_contoh_datum_docx.py baris 29-46, spec 000 RevA Tabel 3.2-3.5; provenans per seksi di dalam berkas | DHS-RB-01; regex nol-hex selftest_builder CHECK G1 |
| 2 | [`datumbind.py`](datumbind.py) | Register / Derivation / audit_docx / audit_retired + resolver `tokens_path()` | CLI: `uv run --python 3.11 --with python-docx python datumbind.py "Register Kuantitas.json" "<dok>.docx"` (exit 0 semua angka tertelusur; exit 1 stray tercetak); import sebagai modul | promosi verbatim arsip legacy sha `5e7bca7f…652e54` (260 baris) + komentar provenans + limit E-12 + resolver lokal (satu-satunya butir ber-arsip) | [`selftest_datumbind.py`](selftest_datumbind.py) dua arah 13 CHECK |
| 3 | [`scripts/datum_lint.py`](scripts/datum_lint.py) | Lint berkas .docx rilis: 38 cek DATUM-01..38 (tahap file 27, build 7, eye 4; build/eye tercetak NOT-RUN jujur dengan pemilik tahapnya) | `uv run --python 3.11 --with python-docx python scripts/datum_lint.py <dok.docx>`; uji diri: `... datum_lint.py --selftest`; exit 0 bersih / 1 FAIL / 2 salah pakai | daftar cek = M01 `docs/2026-10-04-datum-manual/measurement/01-instrumen-penegakan.md` §2.1 (salinan Tabel 8.1 spesifikasi 000 RevA, 38 ID unik); rebuild DHS-RB-02 | `--selftest` dua arah: RED basal rusak ([`scripts/fixtures_lint/basal_rusak.docx`](scripts/fixtures_lint/basal_rusak.docx)) exit!=0 + GREEN exit 0 |
| 4 | [`scripts/datumbuku.py`](scripts/datumbuku.py) | Lint workbook .xlsx: 23 cek W01..W23 (W19 peringatan, tidak menahan terbit; tiga batas lint §11.3 melekat) | `uv run --python 3.11 --with openpyxl python scripts/datumbuku.py BERKAS.xlsx [--json] [--silent]`; uji diri: `--selftest`; exit 0 bersih / 1 temuan penahan / 2 berkas tak terbaca | Standar_Workbook_DATUM_001-GSP-STD-X-2026_RevA §11.1 (Tabel 11.2) + Lampiran A; arsip bukukerja.py dibaca read-only sebagai contoh bentuk, bukan sumber logika; kalibrasi nol temuan pada spesimen RAB_..._RevA.xlsx; rebuild DHS-RB-03 | `--selftest` dua arah atas [`scripts/fixtures_buku/`](scripts/fixtures_buku/) (bersih + 22 rusak + 1 peringatan) |
| 5 | [`datum_diagram.py`](datum_diagram.py) | Engine diagram/infografik: spek JSON -> SVG mm; 9 keluarga/7 mesin layout, 10 bentuk simpul, 6 jenis konektor, geometri terkunci kisi token, apparatus page/figure, penolakan sumber Mermaid | `uv run --python 3.11 python datum_diagram.py spec.json -o out.svg`; flag `--schema --list --estimate --release --json`; exit 1 bila DIAGRAM DEFECT | 000 RevA bab 6 (penanda P1..P7 di header berkas: Tabel 6.1-6.4 baris 656-734, penolakan Mermaid 6.5), M01 2.1 baris 92-105 (cek build DATUM-24..37), register temuan E-08/E-17/E-19/E-20; rebuild DHS-RB-04 | [`selftest_datum_diagram.py`](selftest_datum_diagram.py) dua arah 20 CHECK + [`fixtures_diagram/`](fixtures_diagram/) |
| 6 | [`datum_docx.py`](datum_docx.py) | Builder DOCX token-driven: cover, heading, para, table, derivation, figure; save ber-guard N1 + updateFields + properti inti | import: `from datum_docx import DatumDocx` (tidak ada build saat import, limit E-04); pola pemakaian di docstring berkas | garis builder DATMANUAL terbukti (build_manual_datum.py penghasil docx 100 hal lolos VERIF-final-4 CHECK 1-14; helper diadaptasi verbatim-struktur) + build_contoh_datum_docx.py; kelas builder DHS-RB-05 | [`selftest_builder.py`](selftest_builder.py) (guard + build nyata + audit COM) |
| 7 | [`datum_xlsx.py`](datum_xlsx.py) | Builder workbook token-driven: pita klasifikasi dua blok TANPA merged cell, eyebrow thin-space, blok identitas pasangan label-mono, kunci glif rich-text | import: `from datum_xlsx import DatumWorkbook`; nama lembar dicek N1 saat save | pola chrome build_contoh_datum_xlsx.py terbukti + kontrak STD-SAJI-001 (BLD_saji_check.py G-SAJI-1..8); lint 23 cek tetap milik datumbuku.py; kelas builder DHS-RB-05 | [`selftest_builder.py`](selftest_builder.py) |
| 8 | [`datum_pptx.py`](datum_pptx.py) | Builder deck presentasi token-driven: title/content slide, bullet, table_slide | import: `from datum_pptx import DatumDeck` | KELAS BARU — probe 05-10: 0 builder pptx DATUM terbukti di disk; chrome mengikuti pola DOCX terbukti + tokens.json + 000 RevA Tabel 3.2-3.4; dinyatakan jujur sebagai bukan-pewaris; DHS-RB-05 | [`selftest_builder.py`](selftest_builder.py) |
| 9 | [`datumcheck.py`](datumcheck.py) | Guard situs-panggil G1-G3+N1 + cek ulang 03/04/09/10/16 saat objek dibuat (dipanggil datum_docx) + audit berkas jadi: A1 halaman nyata Word COM, A2 tautan aktif-terlihat (SPK-002 butir 8), A3 em dash U+2014 nol, A4 properti inti, A5 updateFields | audit CLI: `uv run --python 3.11 --with python-docx [--with pywin32] python datumcheck.py <dok.docx> [--pages-com]`; guard di-import pemanggil | 000 RevA tabel 8.2 (D000:L937 lewat M01 §2.2 yang diukur ulang 05-10: 4 guard); limit lebar 128/166 mm dari token grid_mm; pola checker garis check_contoh_datum_short.py + verif_datum_ver04.py; DHS-RB-05 | [`selftest_builder.py`](selftest_builder.py) 42 CHECK dua arah |
| 10 | [`embed_fonts.py`](embed_fonts.py) | Langkah font DATUM: probe registry trio Plex, instal per-user tanpa admin, embed TrueType ke DOCX via Word COM; `ensure_fonts()` hard-fail sebelum build apa pun | `python embed_fonts.py check` / `install` / `embed <dok.docx>`; import `ensure_fonts` | pola instal dipindah utuh dari pitfalls terwaris paket ini (validated DEMS-DATUM-0925); sumber ttf fleet `workspace/EXPO [2026]/Font_DATUM/` + `gsp-canvas-design/canvas-fonts/`; DHS-RB-05 | [`selftest_builder.py`](selftest_builder.py) + audit pasca-embed (font_part nyata di zip) |
| 11 | [`pustakachart.py`](pustakachart.py) + [`pustakachart_data.py`](pustakachart_data.py) | Pustaka chart GSP (ENH-A): render deterministik galeri katalog VCTL (74 PNG, keluarga bar/column/threshold/komposisi/sebaran/hubungan/geospasial/aliran/kinerja) dalam palet+tipografi DATUM; palet baca runtime dari tokens.json, kanvas hanya 128/166 mm, teks terkecil diukur per figur | `uv run --python 3.11 --no-project --with matplotlib --with numpy python pustakachart.py --out <dir> [--check-min-pt]`; dua run berurutan WAJIB byte-identik (terbukti 08-10: 74 PNG, selisih 0); blok warisan datum_chart_buku opsional | promosi toolkit `docs/2026-10-07-vctl-chart-catalog/scripts/render_chart_examples.py` rev0 (VCTL-1007, kontrak D-03 + G-REND-1); resep gambar tidak diubah | gerbang promosi 08-10: determinisme byte-identik + `--check-min-pt` (min 5,8 pt >= lantai DATUM-28 5,5 pt) |
| 12 | [`datumsimbol.py`](datumsimbol.py) | Pustaka simbol DATUM (ENH-F): 41 simbol empat dialek (iec 16, isa 12, sec 7, mil 6) sebagai SVG milimeter token-driven + lembar per dialek berpaginasi blok 247 mm | `uv run --python 3.11 --no-project python datumsimbol.py --list` / `--dialect iec --sheet out.svg` / `--symbol iec:breaker --out s.svg` | normatif (makna/edisi/larangan) TIDAK diduplikasi: satu rumah di `docs/2026-10-04-datum-manual/library/katalog-simbol.md` (SIM-nn); geometri konvensional, SM-12 hormati (berkas berbayar tidak disalin) | menutup E-11 (id tanda hubung) dan E-18 (paginasi 247 mm); SM-03 tercetak di kepala lembar sec; uji render dua putaran 08-10 (round-2 juri mata: label utuh, empat switching berbeda) |
| 13 | [`datum_figur.py`](datum_figur.py) | Baterai figur ENH-E: ukur objek terbit PDF (F1 overflow, F2 caption<=40pt, F3 overlap level KATA, F4 void>25%) + pengecualian sampul DT-14 dan void dideklarasikan | `uv run --python 3.11 --with pymupdf python datum_figur.py BERKAS.pdf [--allow-void 46,57] [--cover-pages 1]`; exit 0 bersih / 1 cacat / 2 tak terbaca; terpanggil otomatis sebagai CHECK A6 [`datumcheck.py`](datumcheck.py) bila padanan PDF ada | sensor ditambal dari lesson 08-10: dedup xref-per-halaman, ambang 57x23pt, hitung kata bukan blok | dua arah 08-10: MERAH EOSADINT RevB (6 cacat, 5 halaman overlap terkonfirmasi kata), HIJAU repro pasca-ENH-C + katalog VCTL (void dideklarasikan) + manual terpadu |

Berkas uji pendamping: [`selftest_datumbind.py`](selftest_datumbind.py), [`selftest_datum_diagram.py`](selftest_datum_diagram.py),
[`selftest_builder.py`](selftest_builder.py), [`scripts/fixtures_lint/`](scripts/fixtures_lint/) (+ `make_fixture.py` pembangun
fixture), [`scripts/fixtures_buku/`](scripts/fixtures_buku/), [`fixtures_diagram/`](fixtures_diagram/). Vonis akhir hidup-tidaknya
mesin milik kartu verifikasi independen DHS-VER-06 (writer-is-not-verifier),
bukan milik penulis paket.

## Generator chart lama: status depresiasi (ENH-B, 08-10)

`gbr_gaya.py` (toolkit misi editorial Rafif) dan `datum_chart_buku.py` (toolkit
PROMANUAL-V2) DILARANG untuk keluaran baru: heks dipaku di kode (aksen biru,
abu netral), kanvas 125/176 mm bukan token DATUM, huruf 9 pt di luar skala.
Rumah kanonis chart fleet kini [`pustakachart.py`](pustakachart.py) (instrumen 11 paket ini).
Misi lama yang sudah terbit tidak diedit retroaktif; pemakai berikutnya
dimigrasikan, dan blok warisan [`pustakachart.py`](pustakachart.py) tetap menyediakan padanan
threshold untuk perbandingan sebelum-sesudah.

## Kompatibilitas gerbang naturalisasi (WAJIB, ENH 08-10)

Keluaran DATUM dibaca manusia dan wajib memenuhi gerbang naturalisasi fleet
(`gsp-output-naturalization`, scanner kanal standar/doc). Builder dan instrumen
paket ini wajib menghasilkan berkas yang lolos tanpa penambalan pasca-terbit:

1. **U+2014 nol mutlak di semua lapisan** termasuk chrome (cap terbit, string
   punggung). Preseden buruk: manual terpadu RevA gagal C-1 di cap terbitnya
   sendiri. Builder tidak memancarkan U+2014 (tokens.json nol; diverifikasi
   08-10); naskah yang mengutip tanda pisah panjang harus memakai hubung.
2. **Penanda D16 wajib ditanam** pada setiap dokumen DATUM-format yang mencetak
   tanda tengah U+00B7 sebagai aparatus (pita klasifikasi, kepala halaman, blok
   register, baris sumber). Satu paragraf deklarasikan cukup (skop per berkas);
   preseden hijau: STD-VISUAL revD dan manual 002. Tanpa penanda, C-2 menembak
   ratusan temuan sah.
3. **Kotak centang memakai U+25A1**, bukan U+2610 (scanner menghitung U+2610
   sebagai emoji, C-3). Glif provenans ■◈◇△ tetap aman (di luar rentang emoji).
4. **Namespace aturan (DT/CH/SM/SG/REQ/ASM) boleh di prosa** — dihitung INFO
   berlabel oleh C-13; identifier modul bergaris bawah di prosa tetap dilarang
   (naikkan ke tabel berlabel manusia).
5. **Baterai figur (datum_figur.py) adalah gerbang ENH-E**: dokumen TERBIT/SERAH
   dengan gambar wajib DEFECTS=0 sebelum serah; void hanya sah bila
   dideklarasikan eksplisit; pemeriksaan mata pada SEMUA halaman berfigur.
6. **Tabrakan ambang yang menunggu putusan controller**: lint DATUM-03
   mengizinkan <=3 tanda pisah panjang/1.000 kata sementara A1 naturalisasi
   menuntut nol. Rekomendasi ENH: turunkan DATUM-03 ke nol (belum dieksekusi,
   bukan wewenang paket ini).

## Perubahan v2.1.0 (ENH-C/D, 08-10)

- `datum_docx.py figure()`: blok gambar kini `line_rule=auto` + keepNext
  (sebelumnya `line exact` setinggi gambar; memaksa Word menggambar meluber ke
  atas dan menimpa paragraf sebelumnya — cacat terproduksi EOSADINT RevB
  hlm 11/15/29, repro dua arah 08-10). Perilaku lama untuk paragraf teks tidak
  berubah.
- [`datumcheck.py`](datumcheck.py): CHECK A6 baru (baterai figur pada padanan PDF; SKIP jujur
  bila PDF atau pymupdf belum ada).
- `datum_diagram.py layout_flow()`: kunci opsional `per_row` membungkus rantai
  panjang jadi baris (E-30 ditutup; kapasitas kolom dibatasi lebar minimum 3
  kisi agar tidak pernah meluap 166 mm; tanpa `per_row` perilaku lama identik).
- E-29 diverifikasi ulang sudah hijau di mesin v2.0.0 (stadium rect+rx,
  cylinder path berlabel) dan diregistrasi sebagai CHECK 22 selftest diagram.
- E-17 ditutup (putusan user 08-10, fixture nyata good_sld.json): stub target
  rute kini arah-balik dari batas simpul, dan sambungan rel berada pada GARIS rel
  (tengah blok), bukan tepi bawah blok; probe dua arah: sebelum 2/3 edges
  menggantung, sesudah 0. CHECK 23 selftest diagram.
- E-08 ditutup dua lapis: guard titik-panggil `px_guard` (DATUM-39, tolak
  sumber <150 dpi efektif saat figure() dibangun) + F5 di baterai figur
  (ukur px-per-inci cetak pada PDF terbit). Uji dua arah 08-10: 500px untuk
  128mm (99 dpi) ditolak, 300 dpi diterima.
- DATUM-03 ambang turun 3 -> 0 sesuai putusan user 08-10 (selaras A1
  naturalisasi nol mutlak); selftest lint tetap PASS dua arah.
- Putusan T-09 caption (user 08-10): DT-15 caption DI ATAS menang untuk
  SEMUA dokumen DATUM; STD-VISUAL wajib ikut saat revisi berikutnya.
- Selftest diagram naik 20 -> 23 CHECK; selftest builder tetap 40 PASS pasca
  tambalan.

## Perubahan v2.2.1 (PUTUSAN-HEUR-1009, 09-10; kartu t_2c28626f)

Dua false-positive heuristik di [`scripts/datum_lint.py`](scripts/datum_lint.py) ditambal sesuai mekanisme
yang disahkan manager di `docs/2026-10-09_ddv-heur-evaluasi/PUTUSAN-HEUR-1009.md`.
Tidak ada ambang/limit cek lain yang diubah (limit DATUM-18 dan DATUM-22 tetap 0).

- **DATUM-18** (`c18`): pencocokan skema klasifikasi tidak lagi memakai
  `body_text.upper()` yang menghapus informasi kapital. Helper baru
  `classification_marks()` memindai kasus-abdi lalu menerapkan dua gerbang: token
  seluruh kapital (`\bRESTRICTED\b`) dihitung marking, DAN kemunculan apa pun dalam
  radius kata penanda kelas (`KLASIFIKASI|CLASSIFICATION|SECURITY|KEAMANAN`, peka
  batas kata) pada kalimat yang sama ikut dihitung; selain itu = kata prosa. Frasa
  prosa huruf kecil ("a restricted arithmetic of ratios", artefak DDV Rev A Annex B)
  tidak pernah menaikkan temuan. Marking sah di badan dokumen tetap terbaca —
  mekanisme TIDAK dibatasi ke header/footer/cover (revisi manager atas usulan asal).
- **DATUM-22** (`c22`): helper baru `strip_document_deictic()` membuang kalimat yang
  dibuka subjek deiksis dokumen sebelum penilaian. Daftar tertutup `DOC_DEIXIS`:
  EN `This/These + standard|document|procedure|specification|policy|report|manual|
  form|checklist`, ID `(Standar|Dokumen|Prosedur|Spesifikasi|Laporan|Formulir) ini`.
  Hanya kalimat itu yang keluar dari kelas klaim eksternal; subjek pihak ketiga tetap
  dinilai penuh — kontrol wajib `"This vendor's datasheet states 45 %"` tetap FAIL.
- **Selftest**: `--selftest` bertambah 8 baris fixture dua arah (`_selftest_heur_1009`,
  CHECK 4..11): H18-a positif-palsu lepas, H18-b RAHASIA+RESTRICTED kapital tetap
  jatuh, H18-c radius penanda kelas aktif, H18-d cabang sampul tanpa penanda utuh,
  H22-a deiksis sampul lepas, H22-b kontrol vendor tetap jatuh, H22-c padanan ID
  lepas, H22-d kalimat pihak ketiga di paragraf sama tetap jatuh. Baris lama
  (CHECK 1 RED / CHECK 2 GREEN / CHECK 3 registry) tidak diubah.
- **Catatan lingkup**: butir 3 PUTUSAN-HEUR-1009 (C-13 monospace) bukan milik paket
  ini — tiket `gsp-output-naturalization` (kartu t_d9d918a6).

## Perubahan v2.3.0 (FIX-DATUM-ENGINE, 09-10; kartu t_9b9494b6, vonis DIST-2 F-1 & F-4)

Dua cacat kelas "dua builder beda perilaku" ditutup di engine, bukan di builder hilir.

- **F-1 pemisah caption (Decision Log):** `DatumDocx.__init__` kini menerima
  `caption_sep` dengan **default baru ASCII `" - "`** — deviasi dari byte lama
  DISETUJUI hulu: vonis manager DIST-2 butir F-1 (`skill_distribution_DIST-2.md`
  §F) mengamanatkan eksplisit "parameter pemisah, default aman ASCII". Efek:
  slug caption `table()` tidak lagi menyuntik U+00B7 ke zona badan meski naskah
  nol glif (preseden rantai DDV 09-10: EOSRAY badan=0 vs DDV 21 dot). Edisi lama
  yang membeku dengan glif warisan direproduksi byte-asalnya lewat
  `caption_sep=" \u00b7 "` (dibuktikan regresi: parts zip identik kecuali cap
  waktu `docProps/core.xml`). Chrome sampul/kepala/kaki (baris copies, pita
  klasifikasi, kepala berjalan) BUKAN lingkup tiket ini — sah per deklarasi D16.
  Builder hilir dilarang menambal slug engine lagi (DEF-QA-2 jadi tambalan
  sementara yang bisa dicabut penerima).
- **F-4 DATUM-09 satuan wajib di emitter:** `Register.emit` menolak besaran
  `unit=None`/kosong dengan `BindDefect` ("tanpa satuan ... daftarkan satuannya").
  Preseden DDV Rev A: bobot dimensi terpancar `unit=null` -> tabel register nilai
  telanjang. Perbaikan kelas di emitter sesuai vonis QA-FINAL baris 54, bukan
  label tangan di builder. Konsumen lama yang memancarkan entri tanpa satuan kini
  WAJIB mengisi satuan (mis. `"poin bobot"`, `"%"`, `"rasio"`) — breaking change
  minor yang disengaja dan disahkan.
- **Selftest dua arah:** [`selftest_builder.py`](selftest_builder.py) +CHECK B7 (default ASCII, U+00B7
  nol di slug) & B8 (jalur legacy memulihkan glif warisan); [`selftest_datumbind.py`](selftest_datumbind.py)
  +CHECK 2b (emit tanpa satuan ditolak) & 2c (satuan terpancar sesuai spec rev B).
  Red-green terbukti di cermin pra-patch: SEP/LEGACY/UNIT FAIL sebelum sunting,
  PASS sesudah; entri bersatuan KEKAL identik sejak basal.
- **Regresi dokumen hidup (09-10):** DDV (konsumen slug engine): zona badan
  U+00B7 18 -> 4 (sisa = penanda D16 + pita sampul sah), delta tepat 14 token
  slug caption, konten-kekal PASS modulo pemisah, hanya `word/document.xml`
  berubah. EOSRAY (konsumen `apparatus=True`): parts zip identik kecuali cap
  waktu core.xml — tidak terpengaruh, sesuai vonis rantai. Scanner kanal doc
  `--channel doc` VERDICT PASS tercetak atas artefak pasca (kedua dokumen).

## Perubahan v2.3.1 (CTXWIN-DEFECT-FIX, 09-10; kartu t_fcdd32ac, vonis APPROVE-BUG t_c4219901)

Satu cacat lapis byte ditutup di engine: `rail_chip()` menulis nama atribut yang tidak
ada dalam skema OOXML, sehingga niat anchor margin tidak pernah aktif di artefak terbit
dan register hash tidak stabil antar jalur build.

- **Akar causa:** `fr.set(qn("w:anchorH"), "margin")` - `anchorH` BUKAN atribut sah
  `CT_FramePr` (yang sah: `hAnchor`, `vAnchor`, `hRule`, `yAlign`, `w`, `x`, `wrap`,
  dst per ECMA-376). Saat repaginate (jalur `pages_measure`/COM), Word membuang atribut
  tak dikenal lalu menulis bentuk minimalnya dengan default `hAnchor="text"`. Byte
  pra-save != pasca-save; bukti P1-P5 di
  `<ws>/docs/2026-10-09_ctxwin-defect-framepr/` (P3 mereproduksi mutasi dari keluaran
  helper murni; P4 membuktikan `hAnchor="margin"` bertahan round-trip; P5 membuktikan
  posisi render chip identik ketiga varian, x=469,9 pt).
- **Tambalan:** `datum_docx.rail_chip()` kini menulis `w:hAnchor="margin"` (`hRule` /
  `yAlign` dipertahankan sebagai default eksplisit). Builder hilir TETAP dilarang
  merakit `framePr` sendiri (RAIL-1008 tak berubah). Semantik G-RAIL-1..3 tidak disentuh.
- **Bentuk byte ukur dibakukan:** konstanta baru `datum_docx.RAIL_FRAMEPR_POST`
  (token-driven dari `_GRID`) = `<w:framePr w:w="1814" w:wrap="none"
  w:hAnchor="margin" w:x="7597"/>`. Assert byte-jadi builder membandingkan terhadap
  bentuk PASCA-save ini, bukan bentuk pra-save helper. Standarkan yang diukur, jangan
  lawan normalisasi default Word.
- **Selftest dua arah:** [`selftest_builder.py`](selftest_builder.py) +CHECK H1 (helper memuat `w:hAnchor`,
  nol `w:anchorH`; deterministik tanpa COM), H2 (konstanta token-driven == nilai ukur),
  H3 (round-trip Word idempoten atas bentuk kanonis; bersyarat pywin32, SKIP tanpa FAIL
  bila COM tak tersedia). Red-green terbukti di cermin pra-patch: H1/H2/H3 FAIL sebelum
  sunting (H3 mereproduksi `hAnchor="text"`), PASS sesudah; VERDICT keseluruhan PASS.
- **Regresi konsumen hidup (09-10):** rebuild fixture rail rev B (ADINPROP-1008
  `scripts/build_rakit.py`, salinan Temp agar basal terbit tak tersentuh) lewat engine
  pasca-tambal - ASSERT pra-embed lolos PENUH (G-RAIL-1/1c/2/3a/3b/3c + pgSz + em dash)
  dan posisi chip hasil render PDF dibandingkan basal rev C (pola `evidence/probe5.py`):
  multiset (x,y,teks) chip IDENTIK 85/85, geser nol; banding pasca-embed dua mesin
  (pra-patch vs pasca-tambal) pun IDENTIK. Efek layout serahan CTXWIN-1009 tetap nihil
  sesuai vonis P5.
- **Efek samping lapis byte yang TERUKUR (v2.3.1):** dengan anchor margin akhirnya AKTIF,
  Word memecah run chip terpanjang (47 karakter, melewati lebar kolom frame) menjadi dua
  `w:r` saat round-trip embed - deterministik (2/2 pengulangan), paras-level konten kekal
  (teks utuh == manifest.upper()), posisi PDF tak bergeser. Uji A/B atas byte pre-embed
  identik membuktikan kausalitas nilai anchor: `margin` -> split, `text` -> tidak. Konsumen
  yang membandingkan teks chip di LEVEL RUN terhadap manifest (mis. G-RAIL-1c jalur
  pasca-embed) wajib membandingkan di LEVEL PARAGRAF (gabung semua `w:t` paragraf framePr)
  agar tidak positif-palsu. Perbaikan gerbang konsumen = usulan terpisah ke manager
  (batas kartu: semantik G-RAIL-1..3 tidak diubah dari sisi instrumen).
- **Distribusi:** kanonik + registry fleet byte-identik pasca-tambal; sensus salinan
  fisik profil = 0 (LEAN FLEET) sehingga penerima grants junction ikut otomatis, tanpa
  re-sync.

## Perubahan v2.5.2 (C22-PLURAL, 16-10; kartu t_65fb51b1; putusan manager t_0a75080c Vonis 3)

Change request disetujui atas under-detection bawaan DATUM-22: kata kunci klaim
eksternal `\b(datasheet|vendor|manufacturer|brosur)\b` lolos bentuk jamak
("Vendors state 900 W output at 40 C." terukur LEPAS di instrumen basal, probe
`plural_probe.py` pada verifikasi/ticket-ins-c22).

- **Perluasan KW c22** menjadi `\b(?:datasheets?|vendors?|manufacturers?|brosur(?:-brosur)?)\b`:
  -s opsional per token EN + reduplikasi ID pada 'brosur'. Tidak ada perubahan lain
  pada mekanisme (DOC_DEIXIS, ambang, sub-traksi paragraf tak tersentuh).
- **Kontrol selftest baru `_selftest_heur_1009` H22-e..H22-l** (CHECK 12..19): tiga
  probe jamak, K1 "The vendor named in the annex states 900 W output at 40 C.", K2
  "The manufacturer published 900 W at 40 C in its leaflet.", K3 preseden H22-b,
  reduplikasi ID "Brosur-brosur mitra menyebut 900 W...", plus kontrol dua arah
  H22-l (deiksis Indonesia subjek jamak tetap lepas).
- **Red-green terukur**: ketiga probe jamak basal=LEPAS -> pasca=FALL; kontrol lepas
  (H22-a/c dan deiksis jamak) identik basal vs pasca; artefak bersih pin GREEN tetap
  exit 0 (CHECK 2). `--selftest` VERDICT PASS exit 0 dari kanonik DAN registry fleet;
  kedua sisi byte-identik sha256[:16] ada80878d323fd46.
- **Distribusi**: sensus salinan fisik profil `datum-house-style` = hanya arsip
  `profiles/gspuser02/skills/datum-revl/` (bukan target, vonis t_0a75080c), sehingga
  nol re-sync penerima (LEAN FLEET).

## Perubahan v2.5.1 (BUG-DIAG-ROWPACK, 09-10; kartu t_787b26a9; bekal desain t_b932e7ba + vonis FIGUR-2 t_df828abe)

Sisa-known yang sengaja ditinggalkan t_ef103378 kini ditutup di mesin:
**tumpuan antar simpul satu baris saat dua kolom graph bertetangga berbagi
baris** (`x_i + w_i > x_(i+1)`). Akar: `_graph_column_pos` lama menguji pitch
seragam hanya terhadap TEPI KANAN (p_cap dari kolom terakhir) sehingga tidak
ada yang menguji lebar simpul per baris. Terukur pada figuran RAFIF-MF-1009:
5 tumpuan pada 3 spek graph (G3.1 satu @10,67 mm, G7.3 tiga @10,67..21,33 mm,
G11.2 satu @10,67 mm); simpul terpotong clamp senyap `build_svg` dan konektor
kehilangan jangkar sah (kelas yang dilaporkan needs-review FIGUR-2).

- **Mekanik baru `_graph_column_pos` (+ helper `_graph_min_width`, `snap_ceil`),
  deterministik dan token-driven:** (1) posisi seragam lama -> uji tumpuan PER
  BARIS; bersih = kembalikan posisi rumus lama PERSIS (nol regresi geometri —
  diverifikasi: 26 dari 29 spek figuran byte-identik SVG pra vs post); (2) ada
  tumpuan -> relaksasi kolom ke kanan sampai celah >= 1 kisi (snap_ceil,
  monotik); (3) tangga strategi ketat-berurutan center+gap1 -> center+gap0 ->
  left+gap1 -> left+gap0 (margin kiri = memakai kanvas penuh, sah karena pusat
  hanya kosmetik); tiap anak tangga boleh merapatkan simpul satu kisi per putar
  sampai batas kebutuhan teks mentah (`_graph_min_width`, tetap kelipatan kisi);
  (4) sungguh tak muat setelah semua daya-ikat habis -> DITOLAK `DATUM-37/ROWPACK`
  bernama, bukan digambar bertumpuk / clamp senyap (preseden t_ef103378:
  rapatkan sampai muat, tolak hanya keadaan tak muat). Statistik penataan
  dilaporkan lewat `sheet.rowpack` (baseline_hits, rounds, strategy, pitch_mm).
- **selftest_datum_diagram.py CHECK 28..30** (gerbang dua arah): 28 repro
  dua-kolom-serah-baris bebas-tumpuan+muat+tanpa-clamp (FAIL di cermin PRA
  dengan tumpuan terukur `kiri>kanan=32.00`, PASS POST); 29 kontrol nol-regresi
  — spek sehat wajib sama persis dengan rumus pitch lama dan TIDAK menyentuh
  jalur rowpack (hijau di kedua pohon = bukti tambalan tidak melebar); 30
  tak-muat-sejati ditolak ROWPACK bernama (ukuran fixture dipilih lewat probe:
  tiap simpul muat sendiri, jumlah tiga baris tidak; FAIL PRA "tidak ada
  penolakan", PASS POST). Cermin PRA exit 1, kanonik POST exit 0.
- **Regresi sapuan 29 spek figuran RAFIF-MF-1009 (cermin PRA vs POST):** error
  BARU 0, error hilang 0, SHA berubah HANYA pada 3 id terdampak (G3.1, G7.3,
  G11.2), 26 id byte-identik, tumpuan 5 -> 0. Gerbang fontTools
  gerbang_geometri.py pada sampel: G7.3 8->2 cacat, G11.2 20->11, sisanya tidak
  bertambah (sisa cacat = kelas lain milik tiket terpisah, termasuk
  G7-pita-hapus-garis-lain akar `_label_knockout` — BUKAN lingkup kartu ini).
  Determinisme dua-run lintas-proses 5/5 sampel byte-identik. Selftest paket
  lain (builder/chip_para/datumbind/datum_lint/datumbuku) exit 0 semua.
- **Distribusi:** KANONIK sha16 mesin 63515916c87f2c69 (selftest aa17cfaa14fd7930,
  tokens.json da95cb7b202e7e69 dan datumbind c7955516bbad1fcd tidak berubah);
  sinkron fleet menyusul sebagai kartu lanjutan manager (pola SYNC-DHS-250) —
  kartu ini TIDAK menyentuh [`$LOCALAPPDATA/hermes/skills/gsp/`](../../registry-fleet/).

## Perubahan v2.5.0 (BUG-DATUM-DIAGRAM, 09-10; kartu t_ef103378; laporan FIGUR-1 t_559f107b + FIGUR-2 t_a3146011 + steer operator mid-run)

Tiga cacat MESIN [`datum_diagram.py`](datum_diagram.py) ditambal di KANONIK SAJA (larangan sync fleet
mid-run demi determinisme FIGUR-2; distribusi menyusul jalur biasa). Basis repro
wrapper pemanggil `work/figur1_diagwrap.py` dan `work/datum_diagram_hopfix.py`.

- **C1 kaki apparatus ber-reserve:** blok kaki (caption/KEY/SUMBER apparatus figure;
  KEY apparatus page ber-legend) digambar pada foot=H-2*LATTICE_Y tanpa reserve
  tinggi -> garis dasarnya berada di dalam simpul baris terakhir pada SEMUA
  diagram ber-legend (tabrakan terukur 13 dari 23 figur figuran RAFIF-MF-1009).
  `Sheet` kini punya medan `foot`; `build_svg` mengisi `sheet.foot =
  _foot_reserve_mm(spec)` (= jumlah baris kaki x LATTICE_Y) sebelum `height()`.
  Spek tanpa legend/page-tanpa-KEY tidak berubah tinggi (hindari inflasi DATUM-33).
- **C2 layout_graph uji muat kanvas:** pitch tetap col*4*LATTICE_X tanpa uji
  x+w<=sheet.W -> kolom kanan melebar keluar kanvas lalu DIAM-DIAM dipersempit
  clamp DATUM-37 (teks meluap kotak; G3.1). `col` kini slot berurutan dari kolom
  yang HADIR: pitch 4*LX selama muat, dirapatkan (snap_floor) + dipusatkan bila
  tidak; tetap tidak muat (pitch < lebar minimum simpul 3*LX) = DITOLAK DATUM-37
  bernama. Jalur lama dipertahankan utuh untuk kolom tunggal / kolom selebar
  lembar / anchor jauh di luar lembar (basal merah DATUM-32 dinding & DATUM-37
  col=20 tetap merah). SISA-KNOWN sengaja TIDAK ditambal (tiket terpisah, mesin
  penataan per-baris): tumpuan antar simpul dalam SATU baris saat dua kolom
  bertetangga berbagi baris dan jumlah lebarnya melewati pitch.
- **C3 crash crossing-hop:** baris render hop `paths[i]["edge"]["kind"]["colour"]`
  meng-index STRING nama jenis sebagai dict -> TypeError SETIAP kali ada hop nyata
  (crash terbukti G10.3/G12.2; worker menyelamatkan diri dengan salinan
  hopfix). Nama token kini lewat `EDGE_KINDS[kind]["colour"]`. Terukur pada
  sapuan figuran: crash hilang di G10.3 dan G12.2 (keduanya kini ter-render);
  G10.2 tidak tersentuh tambalan ini - ia sudah vonis DATUM-33 nyata (247,65 mm
  > 247 mm) identik pra/post karena legend kosong sehingga cadangan kaki nol;
  cacat tingginya milik hulu spek (sudah terdaftar di SISA_KERJA FIGUR-2).
- **Kelas label tepi (vonis visual controller kartu induk, akar di berkas sama):**
  label tepi (YA/TIDAK/kind) dulu selalu di titik tengah segmen terpanjang tanpa
  uji hambatan -> garis menembus teks / teks di atas judul simpul. `_label_pos`
  memilih titik tengah segmen terpanjang yang di luar kotak simpul (dibesarkan
  setengah kotak label); semua kandidat bertabrakan = posisi lama. Urutan render
  diubah: SEMUA path+hop dulu, lalu tiap label dengan pita knockout kertas
  (`_label_knockout`, fill token PAPER - bukan warna baru, DATUM-25 membuang
  kertas dari hitungan) baru teksnya -> nol garis tercetak di atas teks label.
- **selftest_datum_diagram.py CHECK 24..27** (gerbang regresi dua arah, merah
  terbukti atas cermin pra-tambal, hijau pasca): kaki ber-reserve page+figure;
  muat graph tanpa clamp senyap + col jauh tetap DATUM-37; hop nyata tanpa
  TypeError + pola indeks-lama 0 hit di sumber; setiap label tepi ber-knockout.
- **Regresi sapuan figuran RAFIF-MF-1009 (29 spek ber-family, cermin PRA vs POST):**
  error BARU 0; error hilang 2 (TypeError G10.3,G12.2); tabrakan kaki 13->0;
  determinisme dua render byte-identik 9/9 sampel; selftest paket 4/4 exit 0.
  Tinggi figur ber-legend naik tepat 1*LATTICE_Y (4,76 mm) = reserve KEY satu
  baris; figur tanpa legend tidak berubah.
- **Distribusi:** KANONIK saja (sha16 mesin pasca-tambal 767b35a8d15c03d7);
  fleet TIDAK disentuh sesuai larangan kartu (pra 3f123a3f881f58b5) sampai
  FIGUR-2 t_a3146011 selesai; sinkron menyusul lewat gsp-skill-distribution.

## Perubahan v2.4.0 (CTXWIN-FOLLOWUP-1, 09-10; kartu t_be1b447e, putusan manager t_618c93d4)

- **Helper kanonis lapis baca chip rail:** fungsi modul `chip_texts_para(body_xml)`
  mengembalikan list teks gabungan per PARAGRAF ber-`w:framePr` (satu entri per chip,
  sudah di-strip). Builder masa depan WAJIB memanggilnya untuk assert konten-kekal
  G-RAIL-1c alih-alih merakit pembacaan per-`w:r` sendiri - lapis run positif-palsu saat
  Word merepaginasi chip melewati lebar frame (`hAnchor="margin"`, efek samping terukur
  v2.3.1). Menerima bytes XML, str XML, path `.docx`, atau file-like. Semantik
  G-RAIL-1..3 TIDAK diubah: hanya penyeragaman lapis pembacaan.
- **selftest_chip_para.py:** gerbang dua arah helper - arah hijau (basal bersih; byte
  terbelah-dua-run tetap bersih di lapis paragraf; sensor per-run tandingan WAJIB jatuh
  tepat 1) dan arah merah (chip dihapus -> hilang=1 terdeteksi; input non-XML ->
  TypeError; modus bytes == modus path). Jalan VERDICT PASS exit 0; replikasi independen
  atas byte post-embed asli uji A/B (attr-margin/attr-minmargin JEBOL-run OK-paragraf,
  attr-text kontrol OK kedua lapis) cocok dengan tabel putusan manager.
- **Distribusi:** kanonik + fleet byte-identik; sensus salinan fisik profil skill ini = 0
  (LEAN FLEET) sehingga tidak ada penerima fisik yang perlu re-sync.


## Lokasi & distribusi

Pasang FLAT `<name>/` (jangan nested): kanonik
[`C:/Users/TRIAL/workspace/gsp-hermes/skills/datum-house-style/`](./) dan registry
fleet [`$LOCALAPPDATA/hermes/skills/gsp/datum-house-style/`](../../registry-fleet/datum-house-style/). Sensus 05-10:
kedua lokasi byte-identik (43 berkas unik di luar `__pycache__`; sha256 penuh
di `docs/2026-10-05-gap09-datum-recovery/MANIFEST-DHS-DIST-05.md`). Profil
pekerja TIDAK memegang salinan fisik (kebijakan LEAN FLEET 29-08: AWARENESS,
registry fleet = sumber tunggal on-demand); akses per tugas lewat kartu
`gsp-skill-manager`, bukan salinan manual.

## Perintah eksekusi (per interpreter)

Mesin nyata di host ini bukan `python` di PATH (stub WindowsApps gagal jalan). Pola andal:

```
# Lint berkas docx (38 cek):
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with python-docx python scripts/datum_lint.py <dok.docx>

# Lint workbook (23 cek):
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with openpyxl python scripts/datumbuku.py BERKAS.xlsx

# Render diagram (spek JSON -> SVG):
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 python datum_diagram.py spec.json -o out.svg

# Build/import builder (docx+xlsx+pptx sekali jalan):
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with python-docx --with openpyxl --with python-pptx python <skrip-build>.py

# Audit berkas jadi (+halaman nyata Word COM, Windows saja):
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with python-docx --with pywin32 python datumcheck.py "<dok>.docx" --pages-com

# Render PDF via Word COM:
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with pywin32 --with pypdf python <render>.py

# Audit bind sebuah docx selesai terhadap register:
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --with python-docx python datumbind.py "Register Kuantitas.json" "<dokumen>.docx"
# exit 0 = seluruh angka tertelusur; exit 1 = ada stray (daftar tercetak).

# Import sebagai modul dari skrip builder mana pun:
import sys; sys.path.insert(0, r"C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/datum-house-style")
from datumbind import Register, Derivation, tokens_path
TOK = json.load(open(tokens_path(), encoding="utf-8"))
```

Register kuantitas dipancarkan rantai perhitungan sebagai langkah terakhir
(`Register.emit`), tidak pernah ditulis tangan; tiap besaran wajib bertanda asal
TERUKUR/DITURUNKAN/PEMASOK/ASUMSI (glif ■◈◇△, DATUM §8). Dua lintasan build untuk
dokumen yang mencetak jumlah halaman total (sampul/kaki): render pertama dengan
tebakan, lalu bangun ulang dengan angka halaman sebenarnya (preseden 007 Rev A:
`KJ_NPAGES=100` lalu `KJ_NPAGES=84`).

## Pitfalls terwaris (dipindah dari datum-docx-render-pipeline, validated DEMS-DATUM-0925)

- **Word COM export**: `Documents.Open(..., ReadOnly=True)` lalu `ExportAsFixedFormat`
  GAGAL ("can't save, read-only"). Buka dengan `ReadOnly=False, AddToRecentFiles=False`;
  tetap `doc.Close(False)` agar berkas sumber tidak berubah. Pakai `DispatchEx` untuk instance sendiri.
- **PDF basi**: hapus PDF target sebelum re-export; kalau tidak, "sukses" bisa dilaporkan atas byte lama.
- **PAGE/NUMPAGES fields**: setelah `Repaginate()`, update field per seksi footer
  (`sec.Footers(i).Range.Fields.Update()`), Repaginate lagi, baru `ComputeStatistics(2)`.
- **Font IBM Plex tidak terpasang default** di host ini. Pola instal per-user (tanpa admin):
  salin ttf ke `%LOCALAPPDATA%\Microsoft\Windows\Fonts`, tulis value `"<Family> <Style> (TrueType)"`
  -> filename di HKCU `...\CurrentVersion\Fonts` (KEY_WOW64_64KEY), lalu `AddFontResourceExW(path,0,0)`
  + broadcast `WM_FONTCHANGE`. Sumber ttf fleet: `workspace/EXPO [2026]/Font_DATUM/` dan
  [`gsp-hermes/skills/gsp-canvas-design/canvas-fonts/`](../gsp-canvas-design/canvas-fonts/); SansCondensed *Bold* hanya dari
  google/fonts raw `ofl/ibmplexsanscondensed/IBMPlexSansCondensed-Bold.ttf` (file SemiBold
  = family terpisah, Word tidak mensintesis bold-match).
- **Glif ■◈◇△ tidak punya glyph di IBM Plex**: Word fallback ke Courier/CambriaMath saat
  render (sama seperti eksemplar sumber CONTOH-DATUM). Pertahankan run token MONO AMBER di
  XML — JANGAN tukar font.
- **`&` di document.xml** muncul sebagai `&amp;` — unescape sebelum grep string verbatim.
- **ensure_fonts() hard-fail**: cek registry untuk "plex serif"/"plex sans condensed"/"plex mono"
  sebelum build; raise, jangan diam-diam fallback.
- **Batas baris tabel**: kontrak dump = body rows hair bawah sz5 murni; jangan tambahkan
  border penutup karangan sendiri (deviasi = anti-drift FAIL).
- **Limit E-12 (datumbind)**: `_known()` hanya mengenal 0-3 desimal; nilai register ber-dec=4
  (mis. 0,0201 kg/kg) dilaporkan stray dan wajib diizinkan manual lewat `allow=(...)`.
  Jangan ubar-semantik mesin tanpa putusan tercatat.
- **Word COM membuang `w:updateFields` saat save `EmbedTrueTypeFonts=True`** (temuan
  DHS-RB-05): jalankan mitigasi pasca-proses zip dari [`embed_fonts.py`](embed_fonts.py) setelah embed,
  urutan skema CT_Settings menuntut `updateFields` sebelum `w:compat`; audit A5
  [`datumcheck.py`](datumcheck.py) memverifikasi hasil akhir.

## Verification (short check pekerja)

1. Paket flat terbaca di kedua registry: `ls $LOCALAPPDATA/hermes/skills/gsp/datum-house-style/` dan kanonik.
2. Sensus sha256 dua lokasi (kecuali `__pycache__`) = 0 defect; bandingkan terhadap MANIFEST distribusi.
3. [`tokens.json`](tokens.json) valid JSON (`uv run --python 3.11 python -c` lewat berkas skrip, atau jq/python).
4. Gerbang eksekusi (preseden t_a21e89ab): JALANKAN selftest sungguhan dari salinan
   fleet, catat exit code mentah; minimal satu dua arah diuji RED dulu (basal rusak
   wajib exit != 0) sebelum klaim GREEN. `compile()` saja bukan gerbang. Empat gerbang:
   `scripts/datum_lint.py --selftest`, `scripts/datumbuku.py --selftest`,
   [`selftest_datum_diagram.py`](selftest_datum_diagram.py) (23 CHECK), [`selftest_builder.py`](selftest_builder.py) (42 CHECK); gerbang ENH: [`datum_figur.py`](datum_figur.py) dua arah (merah EOSADINT/hijau repro) dan [`pustakachart.py`](pustakachart.py) dua run byte-identik.
5. Builder konsumen membaca token hanya lewat `tokens_path()` — grep jalur root Linux
   peninggalan mesin lama (awalan home root absolut) di skrip baru harus 0 hit.
5a. Bangunan baru WAJIB disimpan ulang lewat Word COM sebelum lint (buka
   non-read-only, Repaginate, Save): tanpa jejak `lastRenderedPageBreak` dari Word,
   sensor halaman lint (DATUM-14) buta dan menghitung seluruh dokumen sebagai satu
   halaman (terbukti 08-10 uji dogfood EOSADINT-REBUILD; pola render_uji.py menanam
   47 jejak lalu lint setara lantai). Simpan juga memperbarui medan NUMPAGES.
6. Daftar instrumen di atas harus cocok 1:1 dengan berkas nyata di disk (verifier DHS-VER-06 menguji ini).
