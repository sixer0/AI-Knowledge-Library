# Simulasi Penjurian: uji pengetahuan skill hasil ingestion (pola MWSKILL-0916, 16-09)

Vonis user: sebuah skill hasil ingestion BELAK terbukti berguna sampai panel buta menjawab soal dengannya dan juri memvonis. Bank soal dan kunci dibuat INDEPENDEN dari skill yang diuji; kandidat hanya boleh membaca paket skill + lembar soal, kunci dan korpus hulu dilarang mutlak. Rubrik terkunci sejak awal; controller dilarang menggesernya saat vonis buruk.

## DAG kanonik (kartu LAD per tahap, parent = tahap sebelumnya)
1. F0 mirror korpus (hitung file/byte) -> F1-RT terjemahan -> F1-TA blueprint + KONTRAK-DESAIN rubrik
2. F2 register ekstraksi (baris TERUKUR-DOKUMEN, kutipan terverifikasi ke PDF) -> F3 bank soal + kunci BEKU: catat sha256 questions dan sha256 key; keduanya tidak boleh berubah sepanjang misi, bukti di tiap gerbang
3. S8 rakit paket skill -> S9 verifier vonis penuh instrumen sendiri (seed tetap), keluaran VERIFICATION.md; FAIL -> kartu FIX scoped-exact ke pekerja (bukan verifier menambal sendiri), lalu REVERIF
4. S10 kandidat paralel (plafon 2 gelombang; kandidat ke-3 edge di belakang kandidat 1): tiap kandidat tulis `<CAND>_answers.jsonl` 66 baris, urutan id persis lembar soal, skema field seragam (cand/id/jawaban/nilai_sebut/rujukan/menyatakan_tidak_ada/skill_dibaca)
5. S13 GRADE: 3 juri, pasangan vonis deterministik via residu `(i-1) mod 3` (J1: 0&1, J2: 0&2, J3: 1&2), tiap juri 44x3 vonis skor 0-3 terhadap kunci resmi, field celah_skill wajib terisi. Controller TIDAK menilai butir per butir (mencemari panel)
6. Arbiter hanya untuk soal |a-b|>1 pada lapis pasangan; hitung dengan skrip setelah semua grade terminal; nol selisih = nol kartu arbiter
7. S14 SCORE skrip deterministik (assigns controller/infra): G1 median skor >= ambang, G2 min >= ambang, G3 kasus terburuk per tipe (T1 skor 3), G4 jebakan/trap (penolakan sah = lulus, fabrikasi = 0), G5 sitasi resolve ke baris register sedokumen-sehalaman kunci. Vonis LULUS_AMBANG atau FAIL
8. Remediasi -> SIMULASI WAJIB DIULANG DARI S10 dengan paket baru (putusan D-09): grade/jawaban lama tidak dipakai lagi, arsipkan utuh ke work/archive_run2/ sebelum gelombang baru menulis nama berkas yang sama
9. S15 distribusi HANYA bila LULUS_AMBANG -> S16 countersign + tabel VERIFIKASI-AKURASI

## Gerbang anti-bocor (C16) - pelajaran FAIL(1) era 1.0.5
Penanda id soal (pola `Q-(T[1-4]|TRAP)-\d{3}`) masuk ke paket rilis lewat field catatan baris register tambalan. Tambal permanen:
- GERBANG grep pola bocor NOL hasil di SEMUA berkas paket, jadi langkah wajib DI DALAM skrip merge (bukan hanya checklist kartu)
- Uji controller atas merge wajib mencakup scan penanda LINTAS FIELD, bukan hanya baris/sidik/kutipan
- Remediasi di hulu (berkas sumber pekerja), lalu merge ulang + sidik baru + reverif penuh

## Pitfall alat controller (semua terbukti menyalakan alarm palsu)
- Nama field: register paket memakai `reg_id` untuk id R-xx (field `id` = id internal EX-/GAP-); cek pertama pakai field salah -> "reg hantu" palsu. Uji field dengan mencetak keys baris pertama SEBELUM klaim defect
- Parser skor run-1 menghukum angka kutipan sah pada jawaban trap padahal rubrik mengizinkan -> vonis run INVALID, arsipkan `score_run1_INVALID.json` utuh, jalankan run-2 resmi; jangan sunting hasil vonis di tempat
- Parser pembanding controller: normalisasi desimal koma vs titik (14,8 vs 14.8) dan unicode, kalau tidak hasil jadi batas bawah menyesatkan; laporkan sebagai pembanding, bukan vonis
- Worker melapor "sha16" yang ternyata awalan SHA-1; hitung ulang sha256 kanonik di jalur merge
- `hermes kanban list --board X --json`: urutan flag penting (`list --json` benar, `--json list` gagal parse senyap -> watchdog berputar tanpa vonis)
- terminal menolak perintah foreground yang memuat karakter `&` bahkan di dalam kode Python heredoc (set intersection) -> pakai `.intersection()` atau tulis skrip ke berkas dulu
- Notifikasi kartu / watchdog ALL_TERMINAL BUKAN bukti artefak: ukur segar disk (ls, sha256, jumlah baris) sebelum laporan; pernah melaporkan lembar run-3 terverifikasi padahal belum ada di disk, lalu harus koreksi eksplisit ke user

## Pola watchdog kartu
Skrip Python kecil: loop `hermes kanban --board default list --json`, peta {card_id: label}, set terminal {done,failed,cancelled,archived}, cetak transisi per poll, keluar `ALL_TERMINAL {...}` saat semua terminal; jalankan background=true notify_on_complete=true. Buat watchdog baru per gelombang (jangan pakai ulang watchdog gelombang lama yang sudah terminal).
