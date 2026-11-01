# AI-Footprint Sweep: matriks scan jejak AI di artefak keluaran
(validated 2026-09-01, misi master-design adaptasi; keputusan user D15-D17)

## Standar GSP (ditegakkan dua sisi: creation + verification)
> Penanda Kebijakan: materi ajar menyebut bentuk terlarang sebagai aturan internal, t_ec8bfdab
- Em dash U+2014: DILARANG MUTLAK, tanpa pengecualian blok terkendali (footer sumber
  master design `N — MM` dirender `N / MM`; deviasi tipografi dicatat eksplisit di paket,
  bukan cacat). Preseden pola footer keluarga sendiri: `HLM n / mm` (SPEC R-5).
- Middle dot U+00B7: dilarang KECUALI string blok terkendali yang mengutip master design
  verbatim (mis. footer `<kelas> · Terkendali`, pola header, glyph Mono dossier); retensi
  ditandai `> Penanda D16:` / `# D16:` dan diverifikasi grep ke arsip sumber `extracted/`.
- Bullet: tidak dilarang; marker/gaya mengikuti preset master design terpilih, bukan • generik.
- Aturan creation hidup di DUA rumah paket saja: README
  `gsp-design-system-grill/references/master-design/` (kanal visual) + README
  skill standar mutu dokumen, `references/gsp-sdt/` (kanal dokumen); skill generator
  lain hanya pointer 1 baris (jangan duplikasi rumus).

## Matriks scan per format (verification-side)
> Penanda Kebijakan: materi ajar menyebut bentuk terlarang sebagai aturan internal, t_ec8bfdab
| Format | Metode | Catatan |
|---|---|---|
| .md/.txt/.json/.py | per baris, hitung literal | json/.py: cek juga bentuk escape |
| .html | per text node (HTMLParser) + raw | decode entity via html.unescape |
| .pptx | per-run (python-pptx) + seluruh XML part | termasuk core properties |
| .docx/.xlsx | seluruh XML part | termasuk entity `&#8212;` `&#183;` `&#x2014;` |
| .pdf | lapisan teks (pypdf) | footer cetak ikut terhitung |
| .png/biner | tidak di-scan; scan .md pendampingnya | |

## Snippet runtime emitter (paling sering lolos)
> Penanda Kebijakan: materi ajar menyebut bentuk terlarang sebagai aturan internal, t_ec8bfdab
Berkas .py di paket yang MERENDER dokumen (mis. snippet-docx.py) bisa bersih secara
literal tapi memancarkan U+2014 via escape `\u2014` saat dijalankan. Wajib:
1. grep semua .py/.html/.md/.json paket: literal + `\u2014` + entity HTML;
2. JALANKAN snippet, scan XML output hasil render (em=0 wajib);
3. kontrol merah-hijau: jalankan scanner terhadap backup pra-fix, HARUS mendeteksi
   (membuktikan gerbang tidak mati). Arsip pra-patch disimpan di workspace kartu.

## Aturan penggantian (menjaga makna, bukan hyphen menempel)
> Penanda Kebijakan: materi ajar menyebut bentuk terlarang sebagai aturan internal, t_ec8bfdab
| Konteks | Sebelum | Sesudah |
|---|---|---|
| sisipan dalam kalimat | `X — Y` | `X, Y` |
| rentang/jarak | `4 — 10` | `4-10` atau `4 - 10` |
| pola footer sumber | `N — MM` | `N / MM` (catat deviasi tipografi) |
| label provenans | `[jenis — sumber, hal]` | `[jenis / sumber, hal]` |
| guard/normalizer | — | spasi-em-dash→koma, sisanya→hyphen; en dash U+2013 lihat aturan sempit D-TA-04 di bawah |

> Catatan resolusi D-TA-04 (misi naturalisasi-output 02-09, kartu t_3a5f473b): aturan lama
> yang menyamakan en dash dengan em dash (ikut nol lolos tanpa pengecualian) DICABUT karena
> menyangkal Module H.7.1 (`SKILL.md:920` pada skill standar mutu dokumen, yang mewajibkan
> U+2013 untuk rentang tahun).
> Aturan berlaku: U+2013 SAH hanya dalam pola rentang angka/tahun yang diapit dua digit,
> regex scanner `(?<=\d)\u2013(?=\d)` (lihat `gsp-output-naturalization/scripts/scan_ai_footprint.py`,
> dilaporkan INFO bukan FAIL); di luar pola itu U+2013 tetap nol lolos (pelanggaran).

## Laporan wajib
Tabel per-berkas (sebelum → sesudah, WAJIB 0), kategori verbatim dipertahankan
terklasifikasi, final_gate `VERDICT: PASS`, arsip mentah (study/extracted) TIDAK
disentuh (bukti mtime), dan klaim cakupan jujur ("fleet-wide 0" tidak ditegaskan bila
skill di luar cakupan masih memuat pelanggar, catat sebagai tindak lanjut terpisah).
