# Repair gaya-bahasa ke suara ahli-manusia (preseden GAYA-AHLI-1005, 05-10)

## Inti metode (D-05; koreksi user kelas T3 — WAJIB dibaca sebelum blueprint)

- Keluhan "bertele-tele / terasa AI / susunan konteks / kosakata AI" TIDAK ditambal dengan ambang statistik atau pengacakan ritme kalimat. Metode = PELAJARI cara manusia profesional menulis genre sasaran (proposal teknis, buku, surat, chat kerja): anatomi seksi, peran tiap paragraf, alur argumen, kosakata yang benar-benar dipakai ahli.
- Metrik deterministik turun jabatan: alat bantu DIAGNOSIS, bukan sumber aturan. Aturan yang hanya punya dasar angka dan nol pola diamati = cacat; verifier menolak.
- Tiap aturan manual wajib membawa >=2 kutipan VERBATIM tulisan manusia nyata dengan path + halaman/sel/baris. Contoh karangan hanya sah berlabel CONTOH-ILUSTRATIF dan tidak pernah mengisi bidang bukti.
- Meniru manusia bukan menyalin kalimatnya: yang dipelajari anatomi, peran paragraf, alur argumen, kosakata.
- Penahan kambuh: bila hilir tergoda "mengejar p90/ritme/angka", tolak eksplisit sebagai kontradiksi D-05 dan kembalikan ke metode pola-manusia. Tulis penahan ini di blueprint supaya hilir punya pegangan.

## Resep forensik sebelum vonis (F0)

1. Ekstraksi TEKS PENUH: python-docx — paragraf DAN semua sel tabel (`uv run --with python-docx`). Simpan corpus.json + .txt per dokumen.
2. Ukur deterministik (bekukan SATU metrics.py per misi, semua baseline pakai alat sama): mean klausa/kalimat, % kalimat >=4 koma, titik-koma/1000 kata, 'yang'/100 kata, ritme panjang kalimat (stddev, p90, maks), paragraf >150 kata, rasio pembuka kalimat berbeda.
3. Sapu ulang scanner kanonis `scan_ai_footprint.py` di [`$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/scripts/`](../../../registry-fleet/gsp-output-naturalization/scripts/) pada ekstrak penuh. Catatan distribusi: skill `gsp-output-naturalization` tidak selalu ter-load via skill_view di semua profil, tapi jalur skrip registry selalu terjangkau.
4. Temuan kunci: LULUS gerbang token saat rilis TIDAK menjamin lolos suara — 3/3 dokumen yang dulu lolos rilis FAIL saat disapu ulang teks penuh (paragraf+sel tabel). Gerbang token lama menangkap em-dash/frasa, buta terhadap struktur kalimat, aparatus internal telanjang, dan arsitektur konteks. Vonis awal user = kelas T2 (cacat sistem gerbang), bukan T1.

## Cek-silang kutipan anti-fabrikasi (gerbang controller sebelum promosi sintesis)

- Sampel acak BERSEED tercatat (mis. seed=1005), minimal 20 kutipan >=8 kata dari register hasil sintesis.
- Normalisasi NFC + lowercase + buang tanda kutip + rapikan spasi, lalu substring-match terhadap gabungan berkas sumber lajur + dump korpus manusia.
- MISS sekecil apapun = buang entri itu, jangan pertahankan. Hasil HIT/n dicetak di kolom bukti tabel kontrak.

## Skema manual yang terbukti (S-1..S-8 blueprint TA)

- Lapis tetap: L0 pembaca / L1 arsitektur / L2 paragraf / L3 kalimat / L4 kata / L5 suara ahli / L6 gerbang. Penomoran `SG-<lapis>-<nn>`; L0 min 4 aturan, sisanya min 5.
- Enam bidang wajib per aturan: (1) pernyataan satu kalimat perintah; (2) fungsi bagi pembaca; (3) BUKTI MANUSIA >=2 kutipan verbatim ber-path/halaman; (4) kontras fleet verbatim dari korpus keluaran sendiri; (5) predikat verifikasi (angka hanya di sini, wajib menyebut pola latarannya); (6) instrumen penegak (scanner/juri/manusia).
- L6 disusun dari rekomendasi gerbang forensik + batas positif-palsu yang diketahui.
- Rubrik juri: tiga dimensi sesuai sasaran user (mudah dipahami / kesan mendalam / struktur matang) skala 1-5 ber-deskriptor anchor + dimensi penjaga "kesesuaian dengan pola manusia" (menutup jalan pintas mengejar angka). Juri buta, skor per dimensi terpisah, alasan wajib mengutip frasa teks dinilai.
- Kesan mendalam dilarang dari retorika: sumbernya apparatur bukti (angka bersumber, alasan teknis, batasan diakui) — doktrin DATUM "represent, bukan claim" + SPK-002.
- Manual baru = pelengkap rujukan-silang SPK-002/DATUM/GSP-SDT, bukan standar bersaing; aspek bentuk dan institusional tidak diambil alih.

## Pitfall mekanika kartu yang kena di misi ini

- `lad_card.py` menolak assignee bukan folder profil nyata: TIDAK semua profil berprefiks `gsp-` (contoh nyata: `agentriset`). Cek `ls "$LOCALAPPDATA/hermes/profiles"` sebelum create; grep penyaring output bisa MENYEMBUNYIKAN baris ERROR pembuatan kartu — tampilkan tail penuh saat membuat kartu, lalu verifikasi papan.
- Heredoc panjang berisi campuran tanda kutip Indonesia/Inggris memicu hardline parser terminal. Resep: body kartu ditulis via write_file ke `work/card_*.md` lalu `--body-file`; komentar kartu panjang lewat `subprocess.run([...argv])` dalam python, bukan shell inline.
- Worker `timed_out` (limit bridge 1800s) SETELAH substansi selesai (ekor artefak `STATUS: complete`, struktur utuh): controller MENGUKUR sendiri artefak (wc -lc, daftar heading, ekor), lalu `complete --force` dengan bukti terukur di result — jangan kerjakan ulang, jangan biarkan blocked. Dasar normatif: aturan 10 (gerbang tanpa tuan).
- Watcher gelombang: skrip polling `hermes kanban list --json` difilter id misi, exit saat ALL-TERMINAL, `notify_on_complete=true`. Ganti gelombang = RESTART watcher dengan daftar id baru (watcher berjalan tidak membaca perubahan berkas id di disk).
- Kartu hilir wajib `parents=` saat create (edge susulan tidak menahan promosi); edge antar-langkah sintesis→diagnosis dipasang `link` segera setelah kedua kartu lahir.

## Angka jejak (untuk kalibrasi, bukan ambang umum)

Korpus fleet terukur 05-10: rantai >=4 koma 8-23%, titik-koma/1000 kata 11-33, identifier mesin telanjang 46 temuan, kode internal di badan teks 547 temuan, satu kalimat 583 kata, paragraf >150 kata hingga 125 butir. Korpus manusia pembanding ada di `<proyek>/01 Masukan/Dokumen Awal/` (authored instansi), blok kutipan vendor pada work/VENDOR-V1x.txt, textbook di ekas + SOURCE-VAULT/R3.
