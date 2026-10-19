# KONTRAK-SAJIAN-WORKBOOK-PROFESIONAL (STD-SAJI-001, 22-09-2026)

Sumber kebenaran: dump struktur read-only berkas acuan user
`EXPOWORLD-1026-registri-master.xlsx` (lampiran 22-09, 319.625 B, sha256[:16] ccbff35b30d6453e)
dibandingkan artefak build kita (301.389 B, sha 4bdc0158 - sama data, beda sajian).
Angka token di bawah = cetakan alat (openpyxl, dump_out.txt), bukan kesan visual.
Terapkan pada SEMUA laporan pencarian/akuisisi berikutnya (workbook + tabel MD).

## 1. Token gaya beku (tabel data)

| Elemen | Nilai wajib | Catatan ukur |
|---|---|---|
| Font kepala kolom | Consolas 11 bold, warna FFFFFF | semua sheet data |
| Fill kepala | solid navy gelap `0F2A4A` | satu-satunya warna kepala |
| Kepala: align/tinggi | center/center + wrap; tinggi baris kepala 32-48 | 48 bila label 2 baris |
| Font isi | Consolas 10 (sheet registri); Calibri 10 (sheet agenda/verifikasi) | monospace untuk data padat |
| Zebra baris | baris genap fill solid `C0C0C0`; baris ganjil tanpa fill | selang-seling sejak R2 |
| Border isi | thin horizontal (top+bottom); TANPA border vertikal | grid garis-garis halus, bukan kurung-kurung |
| Align isi | ID/kode/tanggal center; teks panjang left + wrap; semua vertical center | |
| Lebar kolom | PER-KOLOM sesuai isi (ID 12; nama 40-43; venue/keterangan 30-34; bendera 8-10). DILARANG lebar seragam 14 | build lama kita seragam 14 = cacat |
| Tinggi baris isi | seragam 21-30; baris ber-wrap naik 30-45 | jangan biarkan auto |
| Freeze panes | WAJIB per sheet: registri besar bekukan kepala+kolom kunci (mis. F4 / L2); agenda bekukan kepala (A2) | |
| AutoFilter | boleh di sheet kerja (A2:..); opsional di sheet terbit | acuan: terbit tanpa AF, kerja pakai freeze dalam |
| Tautan | warna `0563C1` + underline, satu objek hyperlink per sel; target = URL terverifikasi | defect tampil-tautan 0 (gerbang lama tetap) |
| Tanpa conditional formatting | zebra statis sudah cukup; CF minimal/none | acuan: 0 CF rules |

## 2. Token label kolom (kemanusiawikan header)

Kepala kolom untuk pembaca manusia = label Title-Case manusiawi, BUKAN slug mesin skema:
`ID Expo`, `Nama Resmi`, `Nama Lokal`, `Kategori Utama`, `Tanggal Mulai`, `Venue`, dst.
Slug skema (`nama-resmi`, `tanggal-mulai`) hanya di sheet kerja internal/register negatif.
Pemetaan label <-> kolom skema dibekukan di builder (satu tabel, dipakai semua sheet).

## 3. Anatomi sheet VERIFIKASI (bukti audit yang enak dibaca)

- Baris 1: banner judul merged A:F, navy `0F2A4A`, putih bold 13, tinggi 28
- Blok meta key-value: kolom label bold, kolom nilai reguler, border thin, align left/top wrap
- Baris seksi merged penuh (mis. A7:F7) sebagai pemisah blok audit; freeze di bawah blok pertama
- Klasifikasi dokumen ditulis eksplisit (mis. `TERBATAS`) di baris meta

## 4. Urutan & cakupan sheet (pola baku laporan pencarian)

1. TERBIT (hanya populasi lolos aturan rilis, gaya tabel penuh)
2. KERJA (populasi penuh + flag terbit/alasan eksklusi)
3. VERIFIKASI (banner + blok meta + blok hasil audit + seed)
4. AGENDA/gugus aksi per segmen (sheet terpisah per segmen keputusan user)

## 5. Gerbang gaya (dihitung builder SEBELUM simpan; rilis diblokir bila >0)

- G-SAJI-1: kepala = font bold putih di navy pada 100% kolom terisi
- G-SAJI-2: zebra benar >=99% baris (genap C0C0C0, ganjil kosong)
- G-SAJI-3: border horizontal thin ada; border vertikal 0
- G-SAJI-4: lebar kolom non-seragam (>=80% kolom punya lebar khusus; tak ada blok lebar identik >8 kolom)
- G-SAJI-5: freeze_panes terisi pada semua sheet data
- G-SAJI-6: tautan biru+underline, defect tampil-tautan 0
- G-SAJI-7: label kepala tanpa slug (`grep -c '-' pada kata kecil berpasangan` = 0 di sheet TERBIT/AGENDA)
- G-SAJI-8: tinggi baris kepala dan zebra terbaca alat (bukan default)
Semua cek = pembacaan openpyxl atas berkas SIMPANAN (roundtrip), bukan asumsi memori builder.

## 6. Resep builder (snippet kanonis)

```python
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
HDR_FILL = PatternFill('solid', fgColor='0F2A4A')
HDR_FONT = Font(name='Consolas', size=11, bold=True, color='FFFFFF')
ZEBRA    = PatternFill('solid', fgColor='C0C0C0')
THIN_H   = Border(top=Side('thin'), bottom=Side('thin'))
LINK     = Font(name='Consolas', size=10, color='0563C1', underline='single')
# isi: font Consolas 10; wrap teks panjang; vcenter; zebra idx%2==0; tinggi 21/30/45
# lebar: dict per kolom dari profil isi (max len sampel + margin), bukan konstanta
```

## 7. Penerapan lintas kanal keluaran

- MD/docx: prinsip sama - label kolom manusiawi, tabel tidak lebih lebar dari kebutuhan,
  baris selang-seling bila engine mendukung, tautan aktif bergaya, blok verifikasi ber-banner.
- Notifikasi/chat: ringkas, angka + tautan; tabel hanya <=6 kolom.
- Naturalisasi tetap gerbang terpisah (STD output GSP): kontrak ini mengatur SAJIAN,
  bukan melonggarkan footprint.
