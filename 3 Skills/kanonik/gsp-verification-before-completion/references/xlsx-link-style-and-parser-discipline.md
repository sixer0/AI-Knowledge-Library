# XLSX tautan-gaya: letak benar + disiplin koreksi parser (HDKCOMP X1/X2, 29-09)

## Faktanya: openpyxl menulis gaya tampil-tautan TIDAK di styles.xml
- Preseden 04-09 (SPK-002 butir 8): sel URL wajib hyperlink AKTIF + gaya tautan (warna tegas + underline); defect >0 memblokir rilis.
- Kasus 29-09: spot-check controller membaca `xl/styles.xml` (cellXfs/fonts) menemukan 0 blok `<u>` -> dugaannya "defect rilis". Vonis verifier X2 membantah dengan bukti: openpyxl menulis gaya biru+underline sebagai **rich-text run `rPr` inline pada XML sheet** (`xl/worksheets/sheetN.xml`), bukan di cellXfs/dxfs. Sensus penuh run rPr: 663 bergaya, defect 0. `styles.xml` boleh bersih `<u>` pada xlsx yang sah.
- Resep gerbang ganda (pakai keduanya, jangan satu lapis):
  1. Lapis objek: `openpyxl` — tiap sel ber-URL: `cell.hyperlink.target` harus http/https.
  2. Lapis XML mentah: unzip zip xlsx, sensus `<r>`/`rPr` pada sheetN.xml untuk warna+underline; hitung defect per sel.
- Reprobe acak ber-seed (catat seed) terhadap sampel URL: hidup, atau kegagalan sudah tercatat sebagai residu di laporan.

## Disiplin koreksi parser (berulang kali menyelamatkan vonis hari ini)
Empat false-positive alat ukur controller dalam satu hari, semua karena pola pertama salah:
- `awk -F','` pada CSV dengan koma-dalam-kutipan -> "URL-MATI" palsu. Fix: `csv.DictReader`.
- Manifest segmen beda delimiter (pipe vs TAB antar kartu generator) -> "OK 0" palsu. Fix: deteksi delimiter dari baris kepala sebelum parse.
- Cari figur pola `FIG-*` kapital -> 0 hasil; nama nyata `ga-fig-01-*.png` kecil. Fix: pola longgar dulu, persempit.
- Regex `<sheet name="` tanpa atribut lain -> "SHEETS 0" palsu; fix: `<sheet[^>]*name="([^"]+)"`.
Aturan kerja: **vonis hanya dari parser yang sudah terbukti membaca format nyata berkas; laporkan koreksi metode secara eksplisit** ("angka final dari parser yang benar, bukan yang pertama"). Jangan pernah menutup/membuka kartu atas angka parser pertama yang belum divalidasi terhadap sampel kepala berkas.

## Rekonsiliasi spot-check controller vs instrumen verifier
- Steer controller ke kartu verifier (komentar terstruktur: temuan + uji eksplisit yang diminta) lebih baik daripada membuka kartu FIX sendiri. Kalau verifier membuktikan lokasi bukti berbeda dan PASS ber-sensus penuh, controller menerima vonis ber-bukti dan mencatat dugaannya sendiri sebagai false positive — bukan memaksa rework.
