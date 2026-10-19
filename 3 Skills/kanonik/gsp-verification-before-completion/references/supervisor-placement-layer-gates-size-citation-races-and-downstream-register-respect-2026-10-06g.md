# Supervisor batch G (06-12, PROMANUAL-V2 re-mutu + INDUK gelombang tulis)

## 1. Pelajaran-ke-12: gerbang extent-sumber BUTA terhadap lapis penempatan (koreksi-diri terbuka)

Kasus nyata: sajian STD-VISUAL lolos gerbang F18 (extent manifest dev=0, 162 hal) padahal
53 dari 53 gambar meluber tepi halaman di PDF dan 55 inline extents docx cacat pola
1660/1280 mm = tepat 10x nominal (bug `Cm(w_mm)` vs `Cm(w_mm/10)` di builder). Vonis
pengawas atas 'sajian' yang hanya memakai instrumen extent-sumber ikut buta-titik yang sama.

Aturan naik: **uji gambar wajib di lapis penempatan pada objek terbit**; extent berkas
sumber hanya prasyarat hulu. Resep ukur mandiri (tanpa skrip pekerja):

```python
# DOCX: lebar penempatan inline
import zipfile, re
xml = zipfile.ZipFile(p_docx).read('word/document.xml').decode('utf-8','ignore')
ext = [int(m) for m in re.findall(r'<wp:extent cx="(\d+)"', xml)]
mm = sorted(set(round(e/36000, 1) for e in ext))   # EMU/36000 = mm
# pola raksasa (mis 1660) = bug satuan builder; entri 210x297 = 'Page Ground' latar
# penuh halaman - SAH, adili via descr/nama sebelum cacat (grep segmen XML ±900 char)

# PDF: bbox vs lebar halaman
import pymupdf
d = pymupdf.open(p_pdf); W = d[0].rect.width
bad = sum(1 for pg in d for im in pg.get_image_info(xrefs=True) if im['bbox'][2] > W+1)
```

Metrik mentah wajib diadili sebelum dikutip: '>168mm: 2' teradili = 2 Page Ground sah;
'55 shapes' controller includes 2 sehat -> angka gerbang sejati 53->0. Dua alat dua
definisi = nyatakan arah+besaran, jangan paksa identik.

## 2. Pelajaran-ke-13: sitasi ukuran berkas antar-kartu rawan RACE TULIS

TA menuliskan 01_translated.md sebagai '243 baris, 37.659 B' padahal disk 38.038 B
(tiga formula alternatif pengawas: str 38.010 / utf16 76.020 / baris+karakter 38.253 -
tak satu pun menancap). Hipotesis terkuat: pembacaan pada state tulis-menengah penulis
hulu (mtime 01 = 15:36:48, run TA 15:32-15:39). Aturan: **sitasi antar-kartu wajib
sha16, bukan byte count**; byte boleh pendamping. Baris cocok + byte beda = cacat
paperwork non-blokir bila identitas (path+baris+klasifikasi) benar - adili proporsional.

## 3. Uji-tandingan idem lintas-tangan untuk tambalan collapse builder-side

F-GAKUR-01 (duplikasi-satuan 'kata kata') diverifikasi independen tanpa checklist mereka:
`re.findall(r'\b(\w{3,})\s+\1\b', text_dari_xml, re.I)` atas buku lama = 499 vs buku baru
= 2-60 (sisa = token hash/URL/prosa sah, BUKAN kata-satuan). Runtuh >=88% + sisa
teradili per-token = bukti arah. Declared: regex-cepat definisi-lebar != checklist
unit mereka; dua alat dua definisi.

## 4. Uji K-5 'merujuk bukan menyalin' jadi predikat terukur (resep pengawas)

Jendela geser >=18 kata dari badan DUA standar sumber vs isi blok baru:
```python
words = re.sub(r'\s+',' ', src).split(' ')
for i in range(0, len(words)-18, 40):
    if ' '.join(words[i:i+18]) in blok_norm: hits += 1
```
hits=0 == klaim 'nol salinan badan' terverifikasi lintas-sumur. Murah, deterministik,
bisa dipakai countersign blok tulis mana pun di misi MERUJUK-bukan-menyalin.

## 5. Register REJECTED dihormati hilir TANPA menunggu putusan controller

Pola sehat baru (INDUK L5): blok tulis memuat short-check tabel pin hulu == ledger
countersign pengawas, DAN entri berstatus REJECTED (C-5 f2_juri1.md hantu, vonis L2)
dinyatakan eksplisit 'tidak dikutip sebagai path sah di blok ini' sementara bola
putusan nama kanon tetap tercatat ke controller. Aturan: hilir memilih jalur aman
seketika, putusan penamaan tetap hulu - catat pola ini sebagai target countersign
blok tulis.

## 6. Tagihan jejak: simpan .log scanner PER BLOK

L4 menyimpan `04-rubrik-juri-scan-standar.log` (VERDICT tercetak) - countersign tinggal
grep. L5 mengklaim scanner PASS tanpa log persisten -> pengawas harus mengeksekusi
scanner sendiri atas byte blok (exit 0 PASS, klaim benar, jejak tak kekal). SOP:
setiap klaim scanner wajib meninggalkan `.log` named-per-artefak; tanpa log, vonis
'PASS' diperlakukan sebagai klaim sampai pengawas menjalankan ulang.

## 7. Proporsionalitas alat-atas-kemampuan sesi (deklarasi jujur 2 giliran)

L3 declared scanner TIDAK dijalankan (sesi tanpa eksekutor) -> 'PASS parsial ber-jejak'
+ kewajiban sapuan penuh di langkah hilir; L4 dengan eksekutor menjalankan scanner
sungguhan. Countersign menghargai dua-duanya sebagai SAH selama scope alat dideklarasikan
- jangan menuntut PASS penuh dari sesi tanpa alat, jangan meloloskan tanpa label.

## 8. Redeliver-notifikasi: vonis tayang = cek guard dulu

Beberapa giliran session ini adalah redeliver kartu identik; guard `grep -c
'Countersign pengawas...'` mencetak 0 = vonis BELUM tayang (lanjut pasang), >=1 = sudah
(jangan dobel). Peringatan 'modified since last read' pada write_file temp setelah
sed/python-replace internal = artefak normalisasi sendiri, verifikasi kepala/ekor/len
lalu tayangkan - bukan alasan tulis ulang.

## 9. Catatan peta-papan

Cetakan awk per giliran tetap satu-satunya sumber angka peta; koreksi peta terpasang
SEBELUM tayang lebih murah daripada komentar koreksi sesudah (pelajaran-ke-9 tetap
hidup). Guard `grep -c "Countersign pengawas"` bisa mencocok frasa yang juga muncul di
result/pekerja - gunakan heading penuh vonis-ku sendiri sebagai pola grep anti-duplikat.
