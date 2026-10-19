# Supervisor: Pin Dua-Era, Determinisme Lintas-Waktu, Sensor Pra-Tayang (06-11 sesi enam-papan)

Preskripsi untuk pengawas/countersigner pada papan dengan koridor revisi-berulang (healing loop) dan kartu builder berat. Semua pola terverifikasi pada misi GAYA-AHLI-1005 revD→revG, RAFIFUNITY-1004 mata-remediasi D-88, VISUAL-1005 O3/O4/O4-fix + R11, PROMANUAL-V2 RW-gave-up.

## 1. Determinisme alat diuji LINTAS-WAKTU, bukan dua-run satu sesi

Klaim "renderer/skrip deterministik" hanya terbukti bila hasil proses BARU (giliran lain, jam lain) identik byte dengan aset beku era sebelumnya. Resep: jalankan ulang selftest instrumen dengan dependensi RESMI yang terdokumentasi di laporan pekerja (baca dulu bagian "perintah jalan" — panggilanku tanpa `--with` mencetak FAIL palsu CHECK dependensi), lalu `cmp` file-per-file terhadap `assets/awal/`. Pitfall sensor: flag `--out` bisa diperlakukan DIREKTORI oleh skrip (output mendarat sebagai folder berisi berkas+report) — `cmp` langsung ke path berkas akan BEDA/PermissionError; baca struktur dulu sebelum menuduh non-determinisme. Uji tambahan kuat untuk PDF: bandingkan sha per-aset di report vs cetakan beku pekerja (tiga jalur satu angka).

## 2. Pin dua-era saat healing loop berjalan (norma "vonis menempel byte")

Objek yang disunting kartu healing BERGESER pin di antara giliran ukur pengawas (terukur: outline 7a9866ff → af99be74 pertengahan → 84415982 final; BM2 Ed3 c05d0835 → f7dc08b5 pasca-59A; revF→revG). Aturan:
- Vonis/countersign SELALU menyebut sha16 objek yang diukurnya, dan menyebut status era ("vonis menempel X; objek hidup kini Y — healing evidently berjalan").
- Hilir WAJIB mengulang instrumen atas pin hidup, dilarang mewarisi agregat era-lama (tagihan eksplisit saat O4-fix: jangan warisi 15/1/1).
- Rantai arsip lengkap tiap era adalah prasyarat vonis-lepas (revD tervonis sempat TIDAK terarsip — tagihan S24; pemulihan via rekonstruksi ber-assert sampai sha cocok, lalu salin ke `_arsip/`). Vonis yang menunjuk byte yang tak bisa dibuka = cacat audit-trail.
- Kelas "pin-komentar vs artefak-hidup": komentar pengalihan/controller yang mem-pin build lama lalu build baru lahir tanpa update-pin = deadlock; normakan pin sah = result kartu terakhir (SERAH GAYA memvonis FAIL sha sendiri dengan benar — contoh verifier yang menegakkan norma).

## 3. Sensor pra-tayang untuk teks pengawas sendiri (pelajaran-ke-9..12)

- Angka dalam countersign hanya dari CETAKAN yang sudah dipetik pada giliran itu — draf yang menulis "VERDICT PASS" sebelum ujian hidup selesai tertangkap justru oleh aturan sendiri; koreksi terjadi di DRAF, bukan komentar-koreksi (pelajaran-ke-12, lebih murah daripada tertayang).
- Peta papan ("N done / M running") wajib dari sensus `kanban list | awk` pada giliran pasang, bukan ingatan sensus awal (dua kali meleset dalam satu sesi: C4 7→6, PDF-55 110→111).
- Koreksi typo: grep ke TEKS TAYANG (`kanban show | grep -c <frasa>`) sebelum mengklaim sudah betul — skrip pra-kirim bisa sudah memperbaiki dua dari tiga typo yang "kukoreksi".
- Redeliver notifikasi kartu yang sudah divonis: guard `grep -c "Countersign pengawas"` di show SEBELUM aksi; =1 → tanpa komentar, cukup konfirmasi ringkas ke user.

## 4. Peta-sisa pasca-timeout/gave-up kartu builder berat

Kelas terukur lintas-fleet: kartu "N seksi + M figur" berbentuk satu mati identik di jendela bridge (1814–1820 dtk) — 14 instances (DOKPDF, RAKIT-54, SERAH, SPEC4×2, RWA×2, RWB–RWE×2). Vonis pengawas yang berguna bukan "pekerja lambat" melainkan PETA SISA dari disk per kartu: sensus naskah per-bab (ada/ukuran/mtime/ekor/glif/CR), figur target (png/svg lahir?), register+istilah beku — lalu tagihan resmi: jangan resep ketiga; kartu pecah per-bab menunjuk bekal beku; AMBANG-B parsial-berformat. Aset beku menumpuk antar-giliran = sehat; nol artefak-final-parsial-bernama-final = sehat. Ekor bab lahir "selesai" wajib dipetik sebelum dinobatkan (non-kosong+LF+glif-nol), predikat final tetap butuh cek struktur-vs-blueprint.

## 5. Rundown positif-palsu parser pengawas (terulang, semua dikoreksi sebelum vonis)

- CSV register EKAS ber-pemisah PIPE (`delimiter='|'`) — DictReader default koma mencetak "1558 baris kosong".
- Path dengan SPASI dalam nama berkas ("James F. Kurose...pdf") terpotong oleh regex `[^\s|]+` — "0 ADA" palsu; probe ulang dengan pemotongan kolom/tabel.
- Backtick penempel path (`path.md\``) merusak `os.path.exists` — strip karakter pembungkus.
- Filter substring untuk URL cacat (mis. "(SICI" dalam href) = positif-palsu; uji BENTUK UTUH atau pola terpotong-sejati (`\([^)]*$`).
- GOTO PDF: hitung total lalu uji WILAYAH halaman (dest di luar rentang TOC = rujukan prosa hidup; nol di luar TOC = defect nametable Word/bookmark XML-langsung) — `d.dests` saja menipu (487 dest ≠ 487 tautan aktif).
- `--text <string-path>` mengukur STRING PATH bukan isi berkas (akar F-25-1): sapuan sah = argumen posisi berkas.
- Byte-disk mentah ≠ konten LF: selisih == jumlah CR = koheren CRLF (V3 30.504 vs klaim 30.329) — nyatakan dua konvensi, jangan tuduh salah hitung.

## 6. Transfer norma antar-papan baru

Papan baru (EKASLAP, VISUAL, PROMANUAL-V2) mengadopsi pola dalam hitungan jam bila jejaknya eksplisit: shortcheck ber-cetakan (C2/C4), register-per-ID + lampiran-unit (C4 138/138 literal menjawab catatan traceability C2), block kind=dependency + bukti ls (O4 run pertama, KAL3), partial-handoff AMBANG-B berformat (PDF-55B), jalur token spine dengan nol-placeholder-divalidasi (C3). Tagihan cross-bab yang kubeberukan dan terbukti dipakai: normalisasi sitasi satu konvensi sebelum rakit, normalisasi CR/LF di gerbang spine (C3 CRLF-only), gerbang rakit NOL token `{{...}}` tak-terikat saat final (C1 94 token by-design — placeholder lolos ke buku = cacat rilis kelas DOI-terpotong), dan pembanding-edisi sebagai cara satu-satunya menangkap regresi fitur hulu (Ed2 1.217 anchor vs Ed3 0).
