# Supervisor: engine-pin lintas-kartu, determinisme semantik, audit tabrakan & closeout remote (2026-10-06 era sore, PROMANUAL-V2 + VISUAL-1005)

Pola terverifikasi saat pengawas men-countersign gelombang REND/SPES6B/RAKIT/LINTFIX/GCERPOP/GDESAIN/GAKUR (V2) dan A19/A19B/F17/F18/F19/F19B/F20/F21 (VISUAL). Semua contoh di bawah adalah kejadian nyata dengan angka tercetak pada giliran ukur.

## 1. Bekukan ENGINE/toolkit sebagai pin, lalu re-probe identitas di tiap kartu hilir

Ketika artefak render/vonis menyentuh engine yang bisa disunting agen lain di tengah misi:
- Petik `sha256[:16] + ukuran + mtime` engine pada giliran pengawas, tulis sebagai pin di komentar kontrak ("ENGINE KUBEKUKAN SEKARANG").
- Pada kartu berikutnya, re-probe dan nyatakan jumlah kecocokan ("IDENTIK pin beku-ku - ketiga kalinya lintas kartu"). Ini satu-satunya cara membuktikan "engine tidak disunting diam-diam" saat tidak ada kartu bernama untuk suntingan engine.
- **Akar via urutan waktu**: `mtime engine > mtime artefak` = artefak berasal dari engine pra-tambal. Bukti waktu ini yang membuat vonis FAIL F2 SPEC6 sah tanpa membuka isi engine; dan sebaliknya, engine yang sama + artefak baru = jalur rebuild sah.
- Pitfall companion: konstanta assert yang diklaim "sudah di engine" bisa nihil di badan engine (grep `11906` = 0) - assert itu milik jalur verifikasi pasca-render, bukan guard internal. Nyatakan declared supaya pekerja giliran berikutnya tidak mengira guard sudah aktif.

## 2. Verifikasi klaim verifikator dengan alat sendiri, bukan skrip mereka

Saat kartu verifier/reporter mengklaim FAIL/PASS per-butir pada DOCX/PDF, bukti ulang kelas cacat langsung dari berkas dengan stdlib+pymupdf, tanpa memakai instrumen mereka:
```python
import zipfile, re
xml = zipfile.ZipFile(docx).read('word/document.xml').decode('utf-8','ignore')
pg = re.findall(r'<w:pgSz[^/]*w:w="(\d+)"[^/]*w:h="(\d+)"', xml)
mm = [(int(w)*25.4/1440, int(h)*25.4/1440) for w,h in pg]   # twips->mm
# kebocoran YAML front matter: grep 'source_refs:'/'task_ref:' di badan xml
# kolofon: xml.count('NIB'); glif peran: hitung U+25A0/U+25C8/U+25B3/U+25C7
import pymupdf; d = pymupdf.open(pdf); len(d)  # halaman nyata
d[-1].get_text()  # footer 'N DARI M' - regex longgar: r'(\d+\s+(?:DARI|dari|OF)\s+\d+)'
```
Konversi kunci: A4 = 11906x16838 twips = 210,0x297,0 mm; kertas raksasa 53519x37306 = 944x658 mm. Bila footer regex-mu tak menancap karena format, nyatakan pemisahan tegas: "halaman 534 kubuktikan langsung; footer N tetap cetakan pekerja yang koheren" - jangan digeneralisasi jadi semua terverifikasi.

## 3. Determinisme dua-jalanan: bandingkan SEMANTIK, bukan teks mentah

Klaim "dua run identik" pada berkas JSON amplop bisa salah-dibaca dua arah:
- Diff baris mentah menipu (urutan kunci + field amplop): GCERPOP mencetak **121 baris beda** padahal inti identik.
- Bandingkan payload inti per-target: `(exit_code, cetakan_meter tanpa baris 'JSON ditulis: <path>')` → **0 beda dari 33 target** = klaim substantif TERBUKTI.
- Residu wajib dideklarasikan bentuknya: runA memperkaya field `pages_nyata`, runB tidak - "dua varian skrip pembungkus, satu meter". Rumus vonis: **identik hasil ukur, bukan identik berkas amplop**.

## 4. Audit tabrakan hotspot dua-kartu-satu-berkas (kelas B18 vs RWG-R18)

Gejala: dua kartu menunjuk berkas yang sama ke profil yang sama, satu run masih menulis. Penanganan pekerja yang BENAR (vonis SAH): dua sensus berjarak membuktikan berkas tumbuh (33.891→33.911 B), petik `frontmatter task_ref:` sebagai bukti kepemilikan run saudara, lalu **balik cakupan kartu menjadi verifikasi fungsional** (rerun gerbang + audit KL), bukan menimpa. Yang wajib dilakukan pengawas:
- Verifikasi byte FINAL == pin countersign kartu induk sebelumnya (state tulis-menengah era-tengah wajar, jangan vonis dari sha antar-sensus).
- **Traceroot ke hulu-dispatch**: yang mengecek tabrakan adalah pekerja, dispatcher tidak. Pelajaran untuk controller: cek task_ref/lock sebelum menerbitkan kartu micro ke berkas rantai induknya.
- Redeliver notifikasi kartu yang sudah kubevonis: guard `grep -c "Countersign pengawas"` == 1 + re-probe pin stabil => TANPA komentar kedua.

## 5. Closeout git: vonis hanya remote-side, dan blob besar dibuktikan ukurannya

- `git ls-remote origin main` == HEAD klaim + `git log --oneline origin/main` memuat SEMUA hash dilaporkan = "terdorong, bukan lokal-saja".
- Artefak puluhan MB yang diklaim ikut versioned: `git cat-file -s $(git rev-parse "origin/main:<path>")` dan cocokkan dengan ukuran yang PROBE-PENGAWAS-MANDIRI catat pada kartu build (F19: 14.901.519 B == probe F18 persis). Ukuran lokal != bukti remote.
- Pin repo rentan rewrite riwayat: tree-hash/HEAD remote tetap rujukan utama (aturan lama), commit message yang memuat kode temuan (F-21a/F-21b) = rantai sebab-akibat vonis→perbaikan masuk riwayat git.

## 6. Kartu re-vonis wajib menempel byte baru

Setelah remediasi mengganti artefak (REND→spesimen baru; LINTFIX→buku rebuild), vonis berikutnya harus menyebut pin BARU (>0 kemunculan) dan pin LAMA tidak dipakai sebagai terdakwa (0 kemunculan di posisi vonis). Sensor: `tt.count('199b0f3e')` vs `tt.count('5addeec4')` di berkas vonis. Stabilitas objek: re-probe sha+mtime==petikan kartu sebelumnya (nol mutasi pra-vonis). Ledger pin aktif dipegang pengawas: setiap ganti byte, tulis "Pin AKTIF utk hilir: X (era-Y tergantikan - jangan warisi diam-diam)".

## 7. Parser adjacency = sumber positif-palsu pengawas (R14B)

Uji "caption di bawah gambar" dengan aturan baris-bersebelahan mencetak 0/0 padahal kelima caption benar - pemisah baris kosong. Koreksi: baca PETA BARIS nyata (`L78 gambar -> L80 caption`) sebelum vonis; instrumennya yang salah, artefaknya benar (pelajaran-ke-11 varian adjacency).

## 8. Resep micro terbukti kuantitatif (untuk peta sisa pengawas)

RWA-MICRO run-2 selesai **282 detik** setelah run-1 timeout, vs 4x1813 dtk kartu induk cakupan 3-seksi. Ketika pengawas memetakan "sisa = 1 berkas" dari disk, rekomendasi pecah-per-berkas bukan opini - ia punya angka pembanding. Tempelkan di catatan timeout. Sensus agregat multi-kartu sekali jalan (satu skrip, komentar penuh di kartu pertama + pointer di kartu lain) menghemat giliran dan menjaga satu sumber angka.

## 9. Gerbang permukaan-terbit vs meter bahan (F-GAKUR-01)

Duplikasi kata-satuan `{u()}+satuan` (326 lokasi, cacah pengawas == laporan persis) tak tertangkap meter naskah karena meter membaca `.md` dan cacat lahir saat rakit menyatu di `.docx`. Vonis pengawas: gerbang pada ARTEFAK RAKIT wajib ada (alasan keberadaan SPEC6/GAKUR); akar builder-side punya resep sembuh terpreseden (DATUM-30: tambal builder + rebuild resep matang), dan "placeholder 0" di build berarti teresolusi-padanan, BUKAN terkunci-ke-register - dua kelas berbeda, jangan saling menutupi di promosi.
