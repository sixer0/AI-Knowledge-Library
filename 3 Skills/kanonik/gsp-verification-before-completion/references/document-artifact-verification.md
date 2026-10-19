# Verifikasi Artefak Dokumen (.xlsx/.docx) - GERBANG VERIF-GATE 04-09

Prosedur ini wajib dijalankan setiap kali objek verifikasi adalah berkas Excel atau Word yang memuat tabel, angka turunan, atau daftar URL, karena ketiga kelas cacat F1/F2/F3 berasal dari lapisan berkas yang tidak terbaca oleh mata. Provenansinya adalah misi VERIF-GATE-0904 melalui kontrak `docs/2026-09-04-improvement-gate-verifikasi/contract.md`, blueprint D-TA-01..D-TA-12, serta keputusan gerbang `identification/SKILL-DECISION.md` berstatus APPROVE bersyarat C-01..C-11 yang terbit sebelum implementasi dimulai. Pelaksana teknisnya adalah skrip `scripts/doc_gate_check.py` pada skill yang sama dengan fixture red-green di `scripts/fixtures/document-gate/`, sementara standar induk yang dilayaninya adalah SPK-002-GSP-IX-2026 tentang akurasi data mutlak pada field beban-rilis. Dokumen ini adalah resep operasional yang diwajibkan oleh checklist SKILL.md agar verifikator memanggil parser dan probe alih-alih menilai tabel dengan mata belaka.

## Kapan prosedur ini wajib

| Kondisi objek verifikasi | Tindakan |
|---|---|
| `.xlsx` atau `.docx` dengan tabel, angka turunan (total, subtotal, persentase), atau daftar URL | WAJIB menjalankan `doc_gate_check.py`; vonis mata atas kelas cacat F1/F2/F3 tidak diterima tanpa keluaran skrip |
| Berkas dokumen tanpa tabel dan tanpa URL (prosa murni) | Prosedur ini tidak wajib; Iron Law skill induk tetap berlaku penuh |
| Keluaran verifikasi akan dirilis ke manusia (kolom terbit, lampiran kontrak, etalase) | Berlapis ganda: `doc_gate_check.py` untuk keutuhan artefak, lalu `gate_accuracy_100.py` untuk gerbang akurasi field beban-rilis populasi penuh sesuai SPK-002 butir 5 |

Alasan kelas cacat ini tidak bisa dibaca dengan mata bersifat struktural dan berlapis, sebab kesalahan aritmetika sel baru terlihat setelah nilai direka ulang dari baris penyusunnya, rel hyperlink rusak hanya tampak di lapisan XML `.rels`, dan URL yang hidup tetapi nyasar ke entitas lain hanya terbaca setelah halaman di-probe lalu judulnya dibandingkan dengan nama barisnya. Preseden nyata 04-09 membuktikan hal itu karena workbook expo26 dan PROPOSAL-SWMS.docx lolos pemeriksaan visual berulang sebelum parser menemukan temuan yang sama.

Survey korpus `docs/**/*.docx` pada hari yang sama menemukan nol berkas Word dengan objek hyperlink sehingga klaim cakupan uji wajib ditulis per-kaki dan bukan per-format. Angka presisi alamat temuan seperti `docx:tabel10!r6/c2` pada laporan gate berasal dari kebutuhan itu, yaitu manusia harus bisa membuka ulang sel yang dituduh tanpa menebak.

## Prosedur lima langkah (peta ke CHECK skrip)

Langkah satu adalah dump terstruktur yang dikerjakan CHECK 1 F1a dan CHECK 5 F2a. Parser membuka semua sheet dan tabel termasuk yang tersembunyi, merekam setiap baris-kolom ke `evidence_tables.jsonl`, mendeteksi baris header serta kolom nama dan URL secara heuristik bila flag tidak diberikan, lalu membandingkan jumlah rekaman hasil ekstraksi dengan jumlah tag hyperlink mentah di XML supaya tidak ada sumber URL yang lolos dari pembacaan. Langkah dua adalah rekalkulasi yang dikerjakan CHECK 2 F1b, CHECK 3 F1c, dan CHECK 4 F1d secara beruntun.

Setiap angka turunan dihitung ulang dari baris penyusunnya mencakup total kolom, subtotal per blok, dan persentase terhadap basisnya, duplikat dicari pada kolom kunci, lalu placeholder rusak seperti `None`, `#REF!`, `[object Object]`, dan sentinel kosong ditandai sebagai temuan. Aritmetika dijalankan per satuan tabel sehingga rujukan antar-tabel wajib diuji semantiknya lebih dulu sebelum divonis cacat nyata. Khusus uji total kolom sejak keputusan controller D-03 (04-09, kartu t_39db5b93): label-total dibagi dua tier, label generik seperti `Total`, `Total Biaya`, `SUBTOTAL`, atau `Total (netto)` berlaku sebagai penjumlah penuh, sedangkan label berbentuk nama seksi enumerasi seperti `Total enam sheet pendalaman` (preseden B10 expo26 yang agregatnya lintas-sheet) masuk tier ambigu; komponen dijumlah ke arah bawah dulu lalu ke arah atas memakai toleransi `close_enough` yang sama, kecocokan satu arah tetap sah tanpa vonis, ketidakcocokan pada label generik dengan blok bersih tetap FAIL pemblokir (kontrol mutasi wajib terdeteksi), sementara ketidakcocokan pada label ambigu atau blok yang kedua kandidatnya memuat baris lintasan tanpa angka di kolom ini (jeda/kolom campur) turun menjadi CATATAN `NEEDS_REVIEW` non-pemblokir di `notes_register.csv` dengan alasan tercetak, bukan FAIL senyap maupun pemblokir.

Langkah tiga adalah rel utuh yang dikerjakan CHECK 6 F2b terhadap seluruh sumber URL. Ekstraksi meliputi sel ber-hyperlink, rel eksternal pada part `*.rels`, dan URL polos pada teks terbaca, kemudian setiap rel diuji punya target non-kosong, tanpa spasi, dengan `TargetMode="External"` bila bersifat eksternal. Rel dangling atau target ber-spasi termasuk cacat struktur yang memblokir rilis karena workbook semacam itu bisa ditolak aplikasi saat dibuka pengguna. Langkah empat adalah probe hidup yang dikerjakan CHECK 7 F2c dengan disiplin satu probe per URL unik.

Setiap respons dikirim dengan header `Accept-Encoding: gzip, deflate` lalu didekompresi sebelum dibaca isinya, sementara status HTTP, final URL, rantai redirect, `content_encoding`, serta panjang mentah dan hasil dekompresi dicatat ke `evidence_urls.jsonl`. Berkas bukti itu sekaligus menjadi cache resume karena URL yang sudah tercatat pada run sama tidak diprobe ulang ketika run dihentikan lalu dilanjutkan.

Langkah lima adalah entity-match yang dikerjakan CHECK 8 F3 memakai logika warisan `gate_accuracy_100.py` secara verbatim termasuk STOP-list, `name_tokens`, `abs_url`, dan `dom_of`. Token nama entitas pada baris dicocokkan dengan sinyal host, judul `<title>`, Open Graph, sekuens nama, dan kemunculan di body halaman tujuan. Ambang warisan berlaku utuh yaitu minimal dua sinyal berarti BENAR dan nol sinyal berarti SALAH-TARGET, sementara tepat satu sinyal berarti NEEDS_REVIEW dengan bukti, bukan lulus diam-diam. CHECK 9 kemudian menguji bahwa bukti benar-benar ada di disk dengan membaca ulang laporan gate serta berkas evidence, dan CHECK 10 menguji kesesuaian manifest terhadap deteksi hanya saat flag `--expect` diberikan.

## Cara memanggil skrip

```text
C:/Users/TRIAL/AppData/Local/hermes/bin/uv run --python 3.11 --no-project \
  --with openpyxl --with python-docx python \
  "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-verification-before-completion/scripts/doc_gate_check.py" \
  --target "<berkas.xlsx>" --outdir "<dir-bukti>" \
  --sheet PD-EUROSATORY-PARIS --sheet PD-WAIC-SHANGHAI \
  --header-row 5 --name-col Exhibitor --url-col Website --key-col No \
  --workers 10 --timeout 18
```

Pola jalan terverifikasi fleet memakai interpreter nyata via uv karena perintah `python` di PATH git-bash adalah stub WindowsApps yang gagal jalan tanpa pesan jelas, dan flag inti kontrak D-TA-02 terdiri atas `--target`, `--outdir`, `--mode gate|fixture`, `--expect fixture_expected.json`, `--config kolom.json`, `--sheet` yang boleh berulang, `--all-sheets`, `--header-row N`, `--name-col`, `--url-col`, `--key-col` yang boleh berulang, `--timeout`, `--workers`, `--skip-network`, `--whitelist CSV`, dan `--keep-body`. Alias warisan kartu C1 tetap diterima supaya perintah lama tidak rusak, yaitu `--out` sama dengan `--outdir`, `--no-probe` sama dengan `--skip-network`, dan `--entity-col` sama dengan `--name-col`.

Seluruh path dan kolom datang dari argumen atau config JSON sehingga tidak ada konstanta satu misi di dalam skrip dan skrip yang sama dipakai lintas proyek. Uji fixture red-green memakai `--mode fixture --expect scripts/fixtures/document-gate/fixture_expected.json` atau harness `scripts/run_fixture_suite.py` untuk seluruh fixture sekaligus.

Keluaran stdout berupa baris `CHECK n: PASS|FAIL|NEEDS_REVIEW - nama` untuk CHECK 1 sampai CHECK 9, ditambah CHECK 10 hanya saat `--expect` diberikan, dan ditutup satu baris `VERDICT: PASS|FAIL|NEEDS_REVIEW`. Exit code menurut D-TA-05 adalah 0 untuk PASS, 2 untuk FAIL, 3 untuk NEEDS_REVIEW, dan 1 untuk error atau crash. Crash tidak pernah keluar dengan kode 0 sehingga kegagalan alat tidak bisa menyamar sebagai kelulusan verifikasi. Pada mode fixture dengan `--expect`, exit 0 hanya terjadi bila deteksi sama dengan manifest dan arahnya benar, artinya fixture cacat wajib FAIL dan baseline wajib PASS.

## Artefak bukti di --outdir (D-TA-06)

| Berkas | Isi |
|---|---|
| `gate_report_<ts>.txt` | Baris CHECK dan VERDICT final hasil run |
| `evidence_tables.jsonl` | Dump rekaman baris-kolom penuh hasil langkah satu |
| `evidence_urls.jsonl` | Per URL unik: lokasi sumber (sheet!sel atau part#rId), status HTTP, final URL, rantai redirect, transport (encoding, panjang mentah dan decoded), vonis entity beserta sinyal per kolom; berfungsi juga sebagai cache resume |
| `notes_register.csv` | CATATAN tidak memblokir: MATI, HTTP4XX, KOSONG, REDIRECT-SILANG, entity-context tidak tersedia |
| `failures.csv` | Seluruh temuan pemblokir dengan alamat presisi seperti `Sheet!C7` atau `docx:tabel10!r6/c2` |

## Aturan vonis (D-TA-04, turunan Decision Log D-02)

Pemblokir yang menghasilkan VERDICT FAIL dan menahan rilis adalah temuan F1 apa pun mencakup baca tidak utuh, aritmetika salah, duplikat kunci, dan placeholder rusak, kemudian cacat struktur rel F2b, SALAH-TARGET F3 lebih dari nol, serta crash. Catatan register tidak memblokir tetapi wajib tetap dibukukan per SPK-002 mencakup MATI, HTTP4XX, KOSONG, REDIRECT-SILANG, dan entity-context yang tidak tersedia, sehingga pada artefak nyata VERDICT PASS boleh disertai register catatan selama kolom terbit bersih dari pemblokir. NEEDS_REVIEW dengan exit 3 menunggu keputusan manusia atau controller karena bukan kegagalan sekaligus bukan kelulusan, dan contoh sah status itu adalah probe yang dilewati lewat `--skip-network` sehingga vonis jaringan belum terbukti, atau entity-match dengan tepat satu sinyal.

Batas klaim menurut syarat C-07 perlu diulang di sini supaya tidak ada yang melebihkan perangkat ini, karena checklist hanya mewajibkan pelaksanaan dan skrip hanya membuktikan kelas cacat pada run tertentu dengan bukti mentah di disk, tanpa klaim bahwa gerbang ini wajib secara teknis maupun bahwa nol cacat lolos sefleet. Keterbatasan bawaannya juga perlu disebut terang-terangan: vonis entity-match bergantung pada kualitas nama entitas di baris sumber, probe jaringan bergantung pada lingkungan saat run berlangsung, dan aritmetika lintas-tabel bisa keluar sebagai positif palsu parser sampai semantiknya diuji manual. Vonis alat atas artefak nyata pun diputus oleh verifikator independen, bukan oleh penulis skrip maupun oleh pekerja yang menyerahkan berkas.

## Pitfall

Hyperlink ber-spasi merusak workbook karena menulis target hyperlink yang memuat spasi atau karakter kontrol melalui openpyxl dapat menghasilkan berkas yang ditolak Excel saat dibuka pengguna. Fixture `xlsx_f2_defects.xlsx` mengunci kelas ini lewat rel target ber-spasi plus rel dangling supaya regresi tertangkap otomatis oleh suite. Bila perlu memperbaiki berkas korban, tulis ulang rel melalui XML lalu validasi dengan buka-simpan, jangan menambal di tampilan saja. False-DEAD terjadi karena user-agent atau timeout, sebab server yang menolak UA bot atau menjawab lambat menghasilkan catatan MATI yang palsu padahal entitasnya sah dan situsnya hidup.

Sebelum mencatat MATI sebagai fakta, probe ulang dilakukan dengan UA netral `GSP-DocGate/1.0 (+kontak ops@gspsp.co.id)` dan `--timeout` yang lebih besar lalu hasilnya dibandingkan dengan register run sebelumnya, dan selisih MATI atau KOSONG yang besar antar-run wajib dijelaskan sebagai perbedaan UA atau timeout sesuai preseden syarat C-08, bukan didiamkan.

Redirect nyasar menipu vonis karena status 200 tidak menjamin halaman milik entitas, mengingat final URL bisa berpindah ke domain lain lewat rantai redirect yang panjang. Vonis entity-match memakai final URL dan isi hasil dekompresi, sementara REDIRECT-SILANG dicatat sebagai flag untuk pemeriksaan ulang oleh verifikator. Fidelity bukan truth, sebab angka yang konsisten dengan berkas sumber belum tentu benar di dunia sehingga sumber warisan wajib diuji ulang terhadap sumber primer untuk setiap field yang terbit sesuai SPK-002 butir 1. Entity-match adalah gerbang kelas ini karena URL hidup yang token namanya tidak muncul di host, judul, Open Graph, maupun isi body divonis SALAH-TARGET tanpa kompromi.

URI namespace XML bukan URL dokumen, sebab menghitung kemunculan `http` pada `word/document.xml` mentah menangkap URI namespace elemen akar, dan kejadian nyata 04-09 menemukan 13 kemunculan pada PROPOSAL-SWMS.docx yang semuanya `schemas.microsoft.com/...` serta bukan tautan. Hitung URL hanya dari lapisan terbaca berupa teks `w:t`, objek hyperlink, dan rel `TargetMode="External"` supaya register tidak tercemar angka tanpa bukti warisan parser. Kelas cacat preseden F-58 (06-10, RAFIFUNITY G-FINAL-58 t_507778e0): **kurung pada DOI nama keluarga** (`https://doi.org/10.1002/(SICI...` dan `.../0749-5978(85)...`) termakan parser ekstraksi era hulu sehingga rel Target keluar TERPOTONG dan 404 hidup - lolos dari SEMUA sensor sebelumnya karena rel ada, hyperlink ada, dan entity-match baris tidak mewajibkan kelengkapan format.

Wajib: validasi FORMAT tiap rel Target dengan regex URL utuh (tanpa karakter terkurung menggantung) sebelum probe; dan **anchor internal prosa** diuji sebagai `w:hyperlink w:anchor=` menuju bookmark tujuan (bukan sekadar cacah bookmarkStart - Ed3 punya 487 bookmark tapi rujukan silang 'See section' 255/255 POLOS sementara Ed2 1.217 anchor-link aktif; pembanding-edisi adalah cara satu-satunya menangkap kelas regresi tautan-hulu ini). Positif palsu parser muncul pada rujukan antar-tabel karena total yang mengacu ke tabel lain tidak cocok dengan penjumlahan satu-tabel dan bisa keluar sebagai temuan F1b, seperti kejadian nyata 04-09 pada tabel 10 PROPOSAL-SWMS.docx yang diserahkan hilir sebagai temuan T-1.

Saat audit FAIL, dump baris yang gagal lalu klasifikasikan checker-defect versus data-defect lebih dulu sebelum vonis cacat nyata, mengikuti pola [`data-collection-audit-discipline.md`](data-collection-audit-discipline.md).

Run besar menabrak batas waktu bila dibiarkan satu proses, sehingga untuk workbook ribuan URL jalankan pass fixture lebih dulu, probe dengan `--workers 10`, manfaatkan resume otomatis dari `evidence_urls.jsonl`, dan pecah run per sheet saat mendekati batas 1800 detik. Baseline hidup pun bisa mati karena lingkungan mengingat fixture baseline hanya memakai domain IANA stabil `example.com` dengan nama entitas yang cocok token host dan judulnya. Bila suatu hari baseline MATI karena jaringan, catatnya adalah ENV-NOTE dari tester, bukan regresi kode, sesuai D-TA-10. Pemisahan dua kategori pencatatan itu menjaga suite merah-hijau tetap berarti bagi pekerja berikutnya yang membaca log tanpa memegang konteks misi.

## Verifikasi prosedur ini sendiri

Setiap perubahan skrip atau fixture diuji dua arah sebelum dipercaya siapa pun, dimulai dari regenerasi fixture dua kali yang wajib menghasilkan SHA-256 identik pada seluruh berkas. Delapan fixture harus searah manifest, artinya enam fixture cacat keluar FAIL dengan CHECK bernomor beralamat presisi dan dua baseline keluar PASS, dibuktikan lewat `run_fixture_suite.py`. Berkas rusak harus keluar dengan exit 1 dan bukan PASS supaya crash tidak pernah hijau di depan verifier, dan perintah beserta hasilnya dibukukan di laporan kartu kerja sebagai jejak audit. Penulis skrip bukan verifikator keluarannya sesuai D-TA-12. Riwayat versi referensi ini bermula di 1.0.0 tanggal 04-09-2026 bersama misi VERIF-GATE-0904 kartu t_2ecdceed.
