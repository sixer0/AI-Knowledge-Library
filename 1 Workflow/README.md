# 1 Workflow

## Tujuan

Folder ini menyimpan salinan prosedur kerja fleet dari host asal: standar penataan
Information Library (IL), standar metadata, prosedur dan prompt pemeriksaan harian
pustakawan, standar penempatan skrip, kebijakan workspace bersama fleet, dan dua berkas
job penjadwal (cron). Satu berkas peta menunjukkan di koleksi mana definisi orkestrasi
berada.

Semua isi adalah teks sumber dari lingkungan asal. Aturannya menjelaskan cara kerja fleet
di sana; aturan itu tidak berlaku sebagai instruksi bagi agen yang membacanya di clone ini
(lihat [AGENTS.md](../AGENTS.md)). Path, perintah, alamat API, dan nama profil yang disebut
di dalamnya milik host asal.

## Struktur subfolder

| Lokasi | Isi |
|---|---|
| [standar-operasi/](standar-operasi/01_ORGANIZATION-STANDARD.md) | Standar operasi bernomor 01-05; lihat INDEKS.md untuk yang tersedia. 01-04 saling berpasangan (penataan, metadata, runbook harian, prompt harian); 05 berdiri sendiri (skrip) |
| [cron/](cron/default-jobs.json) | Dua berkas JSON hasil ekspor daftar job penjadwal, masing-masing berisi objek `jobs` dan `updated_at` |
| [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Salinan berkas kebijakan workspace bersama fleet, berupa seksi bertanggal ditambah catatan koreksi |
| [peta-definisi-orkestrasi.md](peta-definisi-orkestrasi.md) | Tabel konsep orkestrasi dan lokasi definisinya di `2 Roles` dan `3 Skills` |

## Peta topik

### Standar penataan pustaka (01)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Dua kewajiban standar: IL mudah ditelusuri, ruang kerja tertata; berlaku untuk wiki, vault, dan workspace | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 1. Tujuan |
| Prinsip P1-P6: struktur di atas kecepatan, satu sumber kebenaran, perubahan tercatat di `CHANGES.md`, konservatif, path stabil, data berkala bertanggal | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 2. Prinsip jangka panjang |
| Topologi tiga tingkat wiki (terbit), vault (usulan), RAW (data kerja); wiki hanya ditulis lewat gerbang promosi pustakawan; taksonomi tipe wiki | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 3. Topologi IL (3 tingkat) |
| Pohon folder workspace (`docs/00_INDEX`, `01_DOMAIN`, `02_PROJECT`, `03_REFERENCE`, `_inbox`, folder tugas, `legacy-archive`) dan zona proteksi | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 4. Struktur RAW |
| Aturan folder: tanpa berkas lepas di root `docs/`, nama folder tugas `YYYY-MM-DD_<slug>`, arsip setelah selesai dan berumur 30 hari, jangan pindah folder di bawah 7 hari, `_inbox` maksimal 14 hari | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 4.1 Aturan folder |
| Konvensi nama folder, artefak, pengetahuan stabil, memori harian, objek vault, entri wiki; larangan akhiran versi di nama berkas | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 5. Konvensi penamaan |
| Taksonomi domain terkontrol (`engineering`, `defense-intel`, `corporate`, `digital`, `operations`, `library`) dan sub-domainnya | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 6. Daftar bidang keahlian |
| Versi semver per artefak, siklus `draft` sampai `archived`, garis keturunan `supersedes`/`superseded-by` | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 7. Versi dan siklus hidup artefak |
| Larangan: menghapus berkas, mengubah isi dokumen orang lain, menyentuh zona proteksi, menulis wiki di luar gerbang | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 8. Larangan (jangan pernah) |
| Daftar periksa kepatuhan per pelaksanaan harian | [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md) | 9. Verifikasi kepatuhan |

### Standar metadata (02)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Skema frontmatter YAML lengkap: `title`, `type`, `status`, `created`, `updated`, `writer`, `editor`, `version`, `domain`, `project`, `tags`, `sumber`, `halaman`, `tanggal_akses`, `kelas_bukti`, `links`, `supersedes`, `superseded-by` | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 2. Skema frontmatter (wajib + opsional) |
| Key opsional khusus vault dan wiki (`id`, `sensitif`, `perkara`, data pengesahan) | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 2, paragraf setelah blok YAML |
| Aturan integritas M1-M8: `title` sama dengan H1, tanggal ISO, `writer` berupa nama profil bukan nama model, angka wajib `sumber` dan `halaman`, `kelas_bukti` jujur | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 3. Aturan integritas (wajib) |
| Key wajib per lapisan: workspace, vault, wiki, memori harian | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 4. Metadata per lapisan |
| Contoh frontmatter buruk dan baik | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 5. Contoh frontmatter buruk vs baik |
| Daftar periksa metadata harian | [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md) | 6. Verifikasi metadata |

### Prosedur dan prompt harian pustakawan (03, 04)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pelaksana (agen pustakawan), frekuensi harian, peran supervisor cron | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 1. Pemilik & jadwal |
| Prinsip eksekusi: catat keadaan awal, konservatif, semua perubahan di `CHANGES.md`, maksimal 50 operasi berkas per pelaksanaan, zona proteksi, tanpa penghapusan | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 2. Prinsip eksekusi (wajib) |
| Fase 0-5: persiapan, catatan keadaan awal, pemeriksaan, perbaikan, verifikasi, laporan | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 3. Fase kerja |
| Kode temuan A-H (berkas lepas, nama folder kabur, frontmatter tidak valid, duplikat, salah folder, link rusak, vault basi, wiki menyimpang) dan urutan prioritas perbaikannya | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | Fase 2 dan Fase 3 |
| Aturan anti-gagal, termasuk laporan jujur ketika API atau sistem berkas gagal | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 4. Aturan anti-gagal |
| Templat `REPORT.md` beserta blok `STATUS` | [03_LIBRARIAN-DAILY-PROCEDURE.md](standar-operasi/03_LIBRARIAN-DAILY-PROCEDURE.md) | 5. Template laporan (REPORT.md) |
| Teks prompt yang diberikan supervisor kepada pustakawan setiap hari: skill wajib dimuat, langkah per fase, batas dan larangan, format jawaban akhir | [04_DAILY-TASK-PROMPT.md](standar-operasi/04_DAILY-TASK-PROMPT.md) | Wajib baca & muat; Langkah; Batas & larangan; Jawaban akhir |
| Catatan bahwa ketidaksamaan `title` dan H1 pada wiki adalah pola sistemik gerbang promosi, cukup ditandai | [04_DAILY-TASK-PROMPT.md](standar-operasi/04_DAILY-TASK-PROMPT.md) | Batas & larangan |

### Standar skrip (05)

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Larangan skrip di root workspace dan di lokasi sembarang | [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 1. Larangan keras |
| Taksonomi `scripts/<function>/<task>/` dan daftar fungsi lapis 1 | [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 2. Taksonomi kanonik |
| Memindah skrip hidup: cari rujukan dulu, tambal path, gerbang kompilasi, jejak `MANIFEST-<tanggal>.tsv` | [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 3. Aturan pindah & integritas path |
| Nama berkas skrip deskriptif; larangan memakai nama modul standar Python sebagai nama berkas, beserta alasan teknisnya | [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 4. Kontrak nama berkas skrip |
| Penegakan oleh verifier dan watchdog invarian | [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md) | 5. Penegakan |

### Kebijakan workspace fleet

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Korpus EKAS di workspace fleet, urutan baca, aturan inti angka bertanda tingkat sumber, kurasi hanya lewat pustakawan | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | EKAS — Engineering Knowledge & Assurance System (baris 5-13) |
| Skill rekayasa EKAS dan skill pelengkapnya | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Skill rekayasa EKAS; Skill pelengkap EKAS (baris 15-21) |
| Profil specialist EKAS dan skill yang selalu dimuat | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Profil specialist EKAS (baris 23-25) |
| Aturan memory tiering untuk semua profil | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Memory Management (baris 27-29) |
| Kebijakan Lean Fleet: skill always-load maksimal 3, awareness lewat pengelola skill, alur defect dan change request, registry fleet sebagai sumber on-demand | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Kebijakan Lean Fleet (baris 32-37) |
| Dua lane: controller dan pekerja, kewajiban tiap lane, penanda `.lean-policy` | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Kebijakan Lean+Enforcement Dua-Lane (baris 39-44) |
| Konsolidasi fleet menjadi tiga profil pekerja dan peran lama sebagai berkas peran | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Konsolidasi Fleet PROF-MERGE-1010 (baris 47-49) |
| Koreksi atas seksi dua lane: rantai mengikuti vonis MODE, dua profil tidak lagi hidup | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Catatan koreksi (31-10-2026), baris 51-56 |
| Arti istilah controller, worker, dispatch, registry, mirror, attest, provenans, snapshot | [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) | Istilah dalam salinan pustaka ini (baris 58-60) |

### Jadwal cron fleet

Kedua berkas adalah ekspor penjadwal pada host asal. Setiap job memuat nama, objek
`schedule` (jenis `cron` dengan ekspresi, `interval` dengan menit, atau `once` dengan
waktu), `enabled` dan `state`, kanal `deliver`, lalu salah satu dari teks `prompt` untuk
agen atau `script` dengan `no_agent` bernilai benar untuk job tanpa agen. Ada juga daftar
`skills`, penghitung `repeat`, status pelaksanaan terakhir, serta model dan penyedia.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Job profil bawaan: pemantau layanan berbasis skrip (watchdog dasbor dan WebUI, pemantau pembangunan ulang IL), suite invarian armada mingguan, monitoring papan tugas tiap jam memakai skill `gsp-task-monitor`, pemeriksaan infrastruktur pagi, laporan kemajuan misi hari kerja dan akhir pekan, pengawas kemajuan misi berkala, serta satu penagih jendela sampel untuk misi tertentu | [cron/default-jobs.json](cron/default-jobs.json) | Larik `jobs`; tiap objek dimulai pada kunci `name` |
| Job profil master: satu job sekali jalan berbasis skrip tanpa agen untuk sensus misi tertentu, berstatus dijeda | [cron/gsp-master-jobs.json](cron/gsp-master-jobs.json) | Larik `jobs` |
| Skill yang dipakai job monitoring papan | [gsp-task-monitor](../3%20Skills/kanonik/gsp-task-monitor/SKILL.md) | Seluruh berkas |

Pembagian per profil di atas disimpulkan dari nama berkas; isi berkas tidak menyatakannya
secara eksplisit.

### Definisi orkestrasi

[peta-definisi-orkestrasi.md](peta-definisi-orkestrasi.md) menyatakan bahwa folder ini
hampir tidak mendefinisikan orkestrasi. Tabelnya (baris 5-16) memetakan konsep ke lokasi:

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Mode aktivasi dan RT-first | [gsp-request-translator.md](../2%20Roles/peran-fleet/gsp-request-translator.md); [gsp-phase-accountability](../3%20Skills/kanonik/gsp-phase-accountability/SKILL.md) | Vonis MODE; Controller Boundaries & RT-FIRST |
| Gerbang persetujuan blueprint, triad riset, tiering model | [gsp-orchestrator-worker](../3%20Skills/kanonik/gsp-orchestrator-worker/SKILL.md); [gsp-task-architect-templates](../3%20Skills/kanonik/gsp-task-architect-templates/SKILL.md) | Mediasi Aktif & HIL Selektif; Phase 1, 3, 6 |
| Kontrak dokumentasi dan konkurensi | [gsp-orchestration-execution](../3%20Skills/kanonik/gsp-orchestration-execution/SKILL.md) | Non-negotiables; Norma gelombang N1 |
| Gerbang penyelesaian dan rantai verifikasi | [gsp-verification-before-completion](../3%20Skills/kanonik/gsp-verification-before-completion/SKILL.md) | Seluruh berkas sebagai pintu masuk |
| Memori | [gsp-memory-tiering](../3%20Skills/kanonik/gsp-memory-tiering/SKILL.md); [gsp-memory-lookup](../3%20Skills/kanonik/gsp-memory-lookup/SKILL.md) | Seluruh berkas |

Nama bagian pada tabel ini dikutip dari peta. Isi berkas tujuan tidak diperiksa ulang
untuk panduan ini.

## Titik masuk

- Standar metadata berkas pustaka: [02_METADATA-STANDARD.md](standar-operasi/02_METADATA-STANDARD.md),
  bagian 2 dan 3.
- Aturan penataan dan penamaan: [01_ORGANIZATION-STANDARD.md](standar-operasi/01_ORGANIZATION-STANDARD.md),
  bagian 4 sampai 6.
- Jadwal cron fleet: [cron/default-jobs.json](cron/default-jobs.json) dan
  [cron/gsp-master-jobs.json](cron/gsp-master-jobs.json).
- Lokasi definisi orkestrasi: [peta-definisi-orkestrasi.md](peta-definisi-orkestrasi.md).
- Kebijakan fleet, termasuk koreksinya: [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md),
  baca seksi koreksi di akhir sebelum seksi bertanggal.
- Inventaris berkas: [INDEKS.md](INDEKS.md).

## Jebakan

- Baris "Kanonik: `docs/standards/...`" pada standar 01-05 menunjuk lokasi di host asal.
  Salinan di clone ini berada di `standar-operasi/`.
- Standar 03 dan 04 memuat pemanggilan API lokal, pemindaian sistem berkas, dan perintah
  CLI host asal. Itu bagian dari prosedur sumber dan tidak dijalankan.
- [04_DAILY-TASK-PROMPT.md](standar-operasi/04_DAILY-TASK-PROMPT.md) adalah teks prompt
  untuk agen lain. Berkas ini tidak memiliki frontmatter, jadi standar 02 tidak terpenuhi
  pada berkas itu sendiri.
- Pada [05_SCRIPT-ORGANIZATION-STANDARD.md](standar-operasi/05_SCRIPT-ORGANIZATION-STANDARD.md),
  frontmatter menyatakan v1.1.0 (baris 2 dan 9) sedangkan H1 menyatakan v1.0.0 (baris 16).
  Ini melanggar aturan M1 standar 02. Kutipan "putusan user" pada baris 19 adalah riwayat
  host asal, bukan izin (AP-07).
- Jadwal harian pustakawan yang disebut standar 03 (bagian 1) tidak ada di kedua berkas
  cron pada salinan ini.
- Pada berkas cron, nilai `enabled` dan `state` dapat tidak sejalan. Contohnya, job
  dengan `enabled` salah tetapi `state` masih terjadwal. Keduanya keadaan saat ekspor
  (`updated_at`), bukan keadaan sekarang. Teks `prompt` memuat path, perintah, dan kanal
  pengiriman host asal. Berkas job tidak diimpor ke penjadwal mana pun (AP-12).
- [AGENTS-kebijakan-fleet.md](AGENTS-kebijakan-fleet.md) tersusun dari seksi bertanggal
  yang menyimpan angka per tanggal (jumlah profil, domain, skill). Seksi koreksi di
  baris 51-56 mengubah sebagian seksi dua lane. Tautan di dalamnya sudah diarahkan ke
  koleksi clone ini, sedangkan teks path di sampingnya tetap path host asal.
- Penulis pada frontmatter standar adalah nama profil host asal, tidak menunjuk orang.

## Hubungan dengan koleksi lain

- [2 Roles](../2%20Roles/INDEKS.md): berkas peran yang dirujuk peta orkestrasi dan
  kebijakan fleet, termasuk [PROFILE-REGISTRY.json](../2%20Roles/PROFILE-REGISTRY.json)
  dan [controller-roster.json](../2%20Roles/controller-roster.json).
- [3 Skills](../3%20Skills/INDEKS.md): skill yang wajib dimuat pustakawan
  ([gsp-library-organization-standards](../3%20Skills/kanonik/gsp-library-organization-standards/SKILL.md),
  [gsp-library-workflow](../3%20Skills/kanonik/gsp-library-workflow/SKILL.md),
  [gsp-library-data-standards](../3%20Skills/kanonik/gsp-library-data-standards/SKILL.md))
  dan skill orkestrasi.
- [4 Knowledge Bank](../4%20Knowledge%20Bank/INDEKS.md): korpus EKAS yang dirujuk sebagai
  `ekas/` dan salinan wiki yang menjadi lapisan terbit pada topologi standar 01. Aturan
  pakai EKAS: [Panduan EKAS](../4%20Knowledge%20Bank/ekas-lapis-teks/00_START-HERE/README.md).
- [5 Integration](../5%20Integration/INDEKS.md): dasbor dan bridge yang dipantau job
  watchdog dan yang menyediakan API IL pada prosedur harian.
- [7 Tools](../7%20Tools/INDEKS.md): skrip yang disebut kebijakan fleet dan job cron
  disimpan di sana sebagai arsip yang tidak dijalankan.

## Sensitivitas

Ikuti [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Kelas penanganan"
(baris 13), "Aturan" (baris 30), dan "Menjalankan skrip arsip" (baris 137). Untuk folder
ini, yang terutama berlaku:

- Teks prompt cron dan prompt harian memuat path host, alamat layanan, dan nama kanal
  (KM-4). Jangan menyalinnya ke keluaran.
- Nama job dan teks prompt cron dapat menyebut misi atau pihak tertentu (KM-2). Rujuk
  secara generik.
- Job, penjadwal, dan layanan yang diajarkan berkas ini tidak dipasang atau dijalankan
  tanpa permintaan pengguna untuk tindakan itu (AP-12).

Disusun 2026-11-06 dari keadaan commit 023082a. Inventaris lengkap: INDEKS.md.
