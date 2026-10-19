# Spot-Check Register JSONL Pekerja Ekstraksi (tervalidasi 2026-09-16, misi MWSKILL-0916)

Kartu ekstraksi korpus (document-reader/analyst) menutup dengan klaim bentuk
"register N baris ber-kutipan-verbatim, X dokumen, nol scan-only". Controller
sahkan dengan SATU skrip python inline (uv run --python 3.11) terhadap berkas
di disk, bukan membaca laporan. Resep:

```python
import json
rows=[json.loads(l) for l in open(REGISTER,encoding='utf-8') if l.strip()]
print('rows',len(rows))                                   # == klaim kartu?
print('tanpa_kutipan',sum(1 for r in rows if not (r.get('kutipan') or '').strip()))
src={}                                                    # sebaran per dokumen
for r in rows: src[r.get('dokumen','?')]=src.get(r.get('dokumen','?'),0)+1
bad=[r.get('id') for r in rows if not r.get('nilai') or not r.get('satuan')]
print('tanpa_nilai_satuan',len(bad),bad[:6])              # daftar id utk ditagih
```

## Interpretasi yang benar (terukur 16-09)

- **Baris tanpa nilai/satuan: lihat POLA, bukan hanya angka.** EX-D punya tepat 2
  baris tanpa nilai/satuan, dan keduanya adalah butir TIDAK-ADA-DI-KORPUS yang
  SENGAJA dibuat sebagai bahan soal jebakan penjurian (id EX-D-209/210 = dua
  baris itu) -> sah, bahkan diinginkan. Register lain (EX-F) punya 3 baris tanpa
  nilai/satuan tanpa penjelasan -> wajib jadi catatan terbuka ke verifier hilir
  ("butir kualitatif sah atau cacat field?"), bukan vonis sepihak controller.
  Bedanya: klaim kartu menyebut kelas khusus + id-nya cocok dengan kelas itu =
  konsisten; tidak = tagih.
- **Cakupan halaman: angka 'halaman terbaca < total' bukan kegagalan bila rinci.**
  Pekerja sah menulis 460/480 bila 20 sisanya dirinci (9 blank verso + 11 grafik
  vektor dekoratif, bukan teks hilang). Tolak klaim 'nol scan-only' tanpa rincian
  per halaman.
- **Cross-check verify report pekerja:** register biasanya punya `<kartu>_verify_report.txt`
  sendiri (`baris=N lolos=N gagal=0 VERDICT PASS`). Angka di laporan pekerja HARUS
  sama dengan hasil ukur controller; beda = eskalasi, bukan rounding.
- **Agregasi lintas register belum teruji di lapis ini:** duplikat antar-kartu
  (dua ekstraktor menyentuh dokumen sama) baru tertangkap di gerbang F4/V-SUSUN;
  jangan klaim "register global bersih" dari spot-check per-kartu.

## Gerbang RT_BYPASS pada blueprint TA

Blueprint TA sah bila `grep -c "01_translated" 02_blueprint.md` > 0 (sitasi nyata,
mis. 3 titik) dan ekor `STATUS: complete`. Ukuran berkas + jumlah baris dari klaim
kartu dicek `ls -la` + `wc -l` pada giliran yang sama.
