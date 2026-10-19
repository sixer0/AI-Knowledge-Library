# Preseden pengawasan 09-10 (PSIKOTES-1008 F4-F5, BUKUV3-MAP/ING-1009)

Enam pola terukur dari giliran vonis controller hari ini; semuanya terbukti di disk, bukan narasi.

## 1. Countersign seed-BERBEDA (bukan replikasi seed pekerja)
Saat memvonis artefak unduhan/inventaris, jangan ulangi seed pekerja — sampling ulang dengan seed milik controller sendiri membuktikan kelulusan bukan kebetulan satu undian.
- Kasus W1a: pekerja uji 30/30 sha256 dengan seed 1009; controller sampel ulang 12 berkas seed 2027 -> 12/12 sha + ukuran cocok. Dua seed berbeda, 42 pembacaan, semua cocok = vonis L2 naik kelas bukti.
- Resep: `random.Random(<seed-baru>).sample(rows, k)` atas manifest CSV, hash ulang berkas lokal, bandingkan kolom sha + ukuran sumber==lokal. Catat kedua seed di jejak vonis.

## 2. Notifikasi `timed_out` = sinyal, bukan vonis; run-1 bisa tetap menghasilkan artefak
- `hermes kanban runs <id>` dulu sebelum aksi apa pun: dispatcher me-retry otomatis (run-2 hidup = jangan bikin kartu baru, jangan reclaim).
- Run yang mati di cap (1814s > 1800s) SUDAH bisa menerbitkan artefak lengkap sebagian (kasus DOCX-1/2: 7 docx terbit). Jalur sah per aturan user 01-09: audit KELENGKAPAN artefak vs kontrak, tempel "catatan gerbang" sebagai komentar ke kartu yang sedang retry (hasil ukur + daftar gerbang sisa + sha sumber terkunci + larangan rebuild buta), lalu tunggu penutupan run-2 untuk vonis.
- Bedakan artefak HIDUP vs basi: `ls --time-style=full-iso` + bandingkan mtime vs waktu mulai run; jangan pakai sha dari ingatan.

## 3. Field `result` bisa None padahal kartu menutup sah (jalur wake/summary)
Kasus L25 dan FIX-7: `show --json` membaca `result: None` sementara notifikasi papan membawa ringkasan penutupan lengkap. Bukan cacat kerja. Vonis wajib bertumpu pada artefak disk + cetakan alat + komentar, BUKAN pada field result; catat sebagai "catatan mesin" di jejak agar tak salah vonis RESULT_ONLY.

## 4. Glif introduced-konverter pada objek terbit (kelas cacat baru docx)
Sumber markdown nol U+00B7, tapi docx hasil konversi memuat 78 middle dot SELURUHNYA di kepala tabel (pola `NOMOR · STATUS · LEVEL`). Kepala tabel BUKAN blok terkendali -> pelanggaran A2 mutlak pada objek terbit. Gerbang: baca `word/document.xml` via zipfile + hitung U+2014/U+00B7 pada lapis teks SEBELUM vonis rilis kanal DOCX; pemisah kepala tabel harus spasi biasa. Kelas ini terpisah dari indikator gaya terwaris genre (D-12/D-15) - yang mutlak tetap pemblokir.

## 5. Pekerja menemukan populasi phantom SEBELUM kerja = jalur benar; controller akui cacat rencana spesifik
Kasus W3a: rencana controller menyebut P0 19 buku; register riil 14. Pekerja melapor lewat komentar rekonsiliasi, mengerjakan 14 riil tanpa fabrikasi. Vonis controller: L2 untuk 14 riil + koreksi rencana tercatat di Decision Log (D-ING-04, kelas T5 controller) + phantom dilacak ke domain sebenarnya via grep register lalu dibebankan ke kartu yang sudah terjadwal (tanpa kartu baru). Pola umum: angka rencana yang tidak cocok ukur disk = cacat hulu controller, bukan alasan menolak artefak pekerja.

## 6. Berkas instruksi terproteksi (AGENTS.md): jalur pekerja-tersumbat -> pemegang-hak-tempel
Sesi headless tidak bisa menambal AGENTS.md (gerbang persetujuan). Jalur sah yang dipakai W2: pekerja menulis `output/W2_AGENTS-PATCH.md` berisi blok OLD/NEW verbatim + deklarasikan penahanan (bukan diam-diam); controller menempelkan dengan uji keunikan `count(OLD)==1`, tulis ulang, verifikasi `OLD tersisa 0 / NEW hadir 1`. Jangan pernah menyuruh worker mem-bypass gerbang proteksi.

## 7. Tagihan turun-temurun WAJIB tertempel di body kartu hilir saat create
Kasus FIX-6 (D-11): tagihan countersign 'pengocokan huruf B' tidak tertempel di body kartu L22 saat create; pekerja merakit urutan-identik secara SAH sesuai kartunya, tagihan baru ketahuan saat vonis pasca-done -> kartu FIX tambahan + pemborosan modal. Preseden naik: grep tagihan verbatim di body saat short-check peluncuran kartu; klaim hasil generator wajib uji-arah-edge (kasus lain hari sama: cetakan redgreen sisi-MERAH disalahbaca sebagai FAIL artefak hidup - baca header varian dulu sebelum menuduh artefak).
