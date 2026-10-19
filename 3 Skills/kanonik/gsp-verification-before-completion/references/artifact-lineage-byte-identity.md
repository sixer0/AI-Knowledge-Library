# Forensik lineage artefak & kekekalan byte (preseden RAFIF-MF-1009 09-10/10-10)

Aturan induk: vonis L2 hanya dari pengukuran disk pada giliran itu. Berkas ini menambahkan kelas ukur yang terbukti diperlukan saat objek jadi DOCX/PDF rakitan.

## 1. Lineage byte pada objek rakit (docx/pdf) — jangan percaya atribusi sidecar

- Buka objek terbit sebagai ZIP, hash tiap `word/media/*`, bandingkan dengan PNG kanal figuran per id:
  `sha256(z.read(n))[:16] == sha256(figuran/GX.Y.png)[:16]`.
- Ini menangkap dua hal yang laporan pekerja tidak bisa: byte ber-vonis-MERAH yang tersisip ke build
  (kasus G11.1 daa58d02 masuk objek b91f2082 padahal QC menjatuhkannya 44 menit sebelum run), dan
  byte lama yang dikira sudah diganti.
- Cek komplementer wajib di gerbang builder: sidecar yang id-nya masih ber-vonis merah di
  verification/QC-*.md = TOLAK sisip (bukan hanya cek atribusi kartu).
- PDF: hitung anotasi `/URI` mentah per varian sebagai bukti tautan hidup; docx: `TargetMode="External"`
  di `word/_rels/document.xml.rels` vs jumlah token `http(s)` di teks. Ketiganya harus saling sama
  (preseden F-A: 1.372 token URL teks tapi 0 rel eksternal + 0 /URI = tautan mati, rilis diblokir).

## 2. Kekekalan byte klaim-vs-akhir

- Setelah event `completed`, mtime artefak BISA bergeser (suntingan pasca-tutup). Bandingkan sha16
  artefak dengan angka yang dikutip result/komentar vonis lama; beda kecil (belasan byte) = catat
  sebagai catatan administrasi, vonis konten tidak berubah bila blok wajib utuh. Pitfall append-only pin:
  kunci byte saat vonis, bukan saat tulis.
- Replay-guard: vonis sudah tayang + sha artefak == cetakan vonis => notifikasi ulang = REPLAY, tanpa aksi papan.

## 3. Gerbang pola teks wajib pada TEKS GABUNGAN lintas-run

- Token bisa terpecah antar `<w:t>` (mis. `[KL-R2-101...]` lolos regex per-run, kena saat w:t digabung).
  Semua sensor pola di lapisan terbit: gabungkan teks lintas-run dulu, baru cari pola.
- Glif krom vs badan: middle dot di baris klasifikasi/salinan = blok terkendali sah bila konsisten
  exemplar induk; hitung terpisah dari badan.

## 4. Pencocokan nama berkas saat mengaudit cakupan register

- Register sering menyebut berkas TANPA ekstensi (`bab-07` vs `bab-07.md`). Pola pencocokan ketat
  menghasilkan cakupan-palsu (7/19 padahal 19/19). Sebelum memvonis "cacat artefak", uji dua pola
  pencocokan dan cocokkan dengan daftar disk. Ini varian lokal dari aturan 'konfirmasi dulu artefak
  mana yang diuji alat'.

## 5. Pair dengan disiplin visus figur

Adjudikasi koordinat endpoint-SVG vs border rect sebelum vonis melayang/menempel:
lihat `visual-qc-connector-discipline.md` (tiga preseden ilusi perioda dash, dua menimpa sensor controller).
