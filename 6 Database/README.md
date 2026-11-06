# 6 Database

## Tujuan

Folder ini menyimpan dua rujukan basis data dari host asal. Yang pertama adalah skema
Prisma milik dasbor Headquarter (HQ). Skema ini menunjukkan tabel yang dipakai dasbor dan
bridge untuk login, konten, pemantauan agen, antrean tugas, cerminan wiki, pencarian IL,
dan pengguna WebUI. Yang kedua adalah snapshot papan kanban agen berupa berkas SQLite biner
bertanggal.

Keduanya salinan untuk referensi. Snapshot tidak menjadi basis data layanan yang hidup,
dan skema tidak terhubung ke basis data mana pun di perangkat ini.

## Struktur subfolder

| Lokasi | Isi |
|---|---|
| [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | Skema Prisma teks: blok `generator`, `datasource` (penyedia `postgresql`, alamat dari variabel lingkungan), model, dan satu enum |
| [snapshot/](snapshot/kanban-2026-10-19.db) | Satu berkas SQLite 3 biner, salinan keadaan papan kanban pada tanggal di nama berkas |

## Peta topik

### Model skema per area

Semua model berikut ada di [schema-prisma-hq.prisma](schema-prisma-hq.prisma). Kolom
`Bagian` menyebut baris awal deklarasi model.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Login dasbor (adapter NextAuth): `Account` (akun penyedia OAuth per pengguna beserta token), `Session` (token sesi dan kedaluwarsa), `User` (nama, email, gambar), `VerificationToken` | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 11, 29, 37, 47 |
| Konten media sosial: `Draft` (draf unggahan dengan skor, jadwal, umpan balik, metrik, riwayat edit), `TweetMetric` (metrik per unggahan), `Idea`, `ContentCalendar` (data per minggu), `ContentRequest` (permintaan pembuatan draf) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 55, 95, 107, 121, 278 |
| Konten video dan artikel: `YoutubeIdea` (ide dengan hook, tahap funnel, skor kompetisi), `YoutubeScript` (naskah lengkap dengan cek fakta dan metadata SEO), `YoutubeFeedback`, `LongformScript`, `Article` (artikel per track dengan status dan metrik), `SavedTitle` | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 127, 145, 174, 182, 324, 350 |
| Keadaan agen dan pesan antaragen: `AgentState` (status, tugas berjalan, biaya, aktivitas terakhir per agen), `AgentBusMessage` (pesan dari agen ke agen dengan tanda sudah dibaca), `Mission` (misi per agen dengan status dan prioritas) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 217, 231, 307 |
| Telemetri orkestrasi: `OrchestrationRecord`, satu baris per interaksi terarah antarprofil (jenis delegate, handoff, verify, report, review, gate, dispatch; status; path artefak kontrak dokumentasi) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | Komentar baris 245-248; model baris 249 |
| Penyimpanan umum: `DataStore` (kunci dan JSON; dipakai bridge untuk daftar cron dan kondisi layanan), `Brief` (ringkasan harian per tanggal), `BattleRoyaleBot` (keadaan JSON per id) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 289, 297, 272 |
| Pemantauan klien lewat bot Telegram: `ClientPulseClient` (data klien dan tanggal kontrak), `ClientPulseChat` (obrolan tertaut klien), `ClientPulseMessage` (pesan dengan intent, sentimen, perlu dibalas), `ClientPulseAnalysis` (skor per jendela waktu), `ClientPulseAlert` (peringatan dengan bukti dan tindakan yang dianjurkan) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 362, 384, 402, 426, 451 |
| Bus tugas dasbor dan bridge: `AgentRequest` (asal, peminta, jenis `oneshot`/`kanban`/`chat`/`instant`, profil tujuan, penanda efek samping, status `queued` sampai `rejected`, hasil), `AgentEvent` (log aktivitas), `HermesTask` (cerminan kartu kanban) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | Komentar baris 473-476; model baris 478, 505, 518 |
| Cerminan wiki: `HermesMemory` (entri wiki dengan tipe, status, keyakinan, provenans, tag, tautan, isi, masa berlaku) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | baris 533-534 |
| Indeks pencarian teks penuh IL: `IlSearchDoc` (dokumen dari wiki, workspace, atau vault dengan kolom `tsvector` yang tidak terbaca lewat klien Prisma) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | Komentar baris 554-563; model baris 564 |
| Pengguna WebUI dan peran: enum `Role` (`ADMINISTRATOR`, `USER`), `WebUiUser` (nama pengguna, hash kata sandi, peran, satu profil agen per akun yang ditegakkan unik di tingkat basis data) | [schema-prisma-hq.prisma](schema-prisma-hq.prisma) | Komentar baris 580-583; enum baris 584; model baris 589 |

### Snapshot kanban

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Salinan beku papan kanban agen beserta kontrak tiap kartu. Berkas SQLite 3 biner yang dibuat lewat mekanisme backup saat layanan berjalan | [snapshot/kanban-2026-10-19.db](snapshot/kanban-2026-10-19.db) | Berkas biner; tidak ada bagian teks |
| Kedudukan snapshot dalam arsitektur | [peta-integrasi.md](../5%20Integration/peta-integrasi.md) | Salinan yang tersedia di clone, baris Kanban |

Tabel di dalam snapshot tidak dibuka untuk panduan ini. Isinya hanya diketahui dari
keterangan [INDEKS.md](INDEKS.md) dan peta integrasi.

## Titik masuk

- Skema basis data HQ: [schema-prisma-hq.prisma](schema-prisma-hq.prisma). Untuk alur
  tugas, mulai dari `AgentRequest` (baris 478).
- Cara tabel bus dipakai: [hermes-bridge/README.md](../5%20Integration/hermes-bridge/README.md).
- Inventaris berkas: [INDEKS.md](INDEKS.md).

## Jebakan

- Ada dua basis data yang berbeda. Skema Prisma memakai Postgres milik dasbor, sedangkan
  snapshot adalah SQLite papan kanban agen. Snapshot tidak berisi tabel skema Prisma.
  Hubungan keduanya adalah cerminan: bridge menyalin kartu kanban ke `HermesTask`.
- Snapshot adalah berkas biner. Isinya tidak terbaca pemindai teks dan dapat memuat data
  dari segala kelas. Berkas ini bukan layanan aktif dan tidak mencerminkan keadaan papan
  sesudah tanggal di nama berkasnya.
- Komentar pada `IlSearchDoc` (baris 554-563) menyatakan bahwa struktur tabel itu
  ditentukan oleh migrasi SQL di host asal, bukan oleh skema ini, dan melarang
  sinkronisasi skema langsung pada tabel itu. Skema ini bukan gambaran lengkap
  struktur basis data.
- Komentar skema merujuk dokumen desain dan migrasi pada folder `docs/` host asal. Berkas
  itu tidak ada di clone ini.
- Model `Account` dan `WebUiUser` memuat kolom token dan hash kata sandi. Yang ada di
  skema hanya nama kolom, tanpa nilai.

## Hubungan dengan koleksi lain

- [5 Integration](../5%20Integration/INDEKS.md): dasbor ([hq-server.mjs](../5%20Integration/hq/hq-server.mjs),
  [package.json](../5%20Integration/hq/package.json) dengan skrip Prisma) dan
  [bridge.mjs](../5%20Integration/hermes-bridge/bridge.mjs) adalah pemakai skema ini.
- [4 Knowledge Bank](../4%20Knowledge%20Bank/INDEKS.md): salinan wiki yang menjadi sumber
  `HermesMemory` dan sebagian sumber `IlSearchDoc`.
- [2 Roles](../2%20Roles/INDEKS.md): daftar controller yang menurut kebijakan fleet
  dibangun dari data akun RBAC ([controller-roster.json](../2%20Roles/controller-roster.json)).
- [1 Workflow](../1%20Workflow/INDEKS.md): prosedur harian pustakawan yang memanggil API IL
  dasbor. Kaitan API itu dengan `IlSearchDoc` adalah perkiraan dan belum diperiksa.

## Sensitivitas

Ikuti [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Kelas penanganan"
(baris 13), "Aturan" (baris 30), dan "Menjalankan skrip arsip" (baris 137). Untuk folder
ini, yang terutama berlaku:

- Snapshot adalah wadah campuran basis data (KM-8) dan mengikuti kelas tertinggi isinya.
  Snapshot tidak ikut edisi umum, tidak disalin ke keluaran, dan tidak dibuka kecuali
  tugas tentang pustaka memerlukannya.
- Folder ini tertolak bawaan pada edisi pertama (bagian "Isi edisi umum").
- Skema memuat model tentang klien dan pesan. Data seperti itu tidak dicari di luar
  skema, dan nama tidak disalin.

Disusun 2026-11-06 dari keadaan commit 023082a. Inventaris lengkap: INDEKS.md.
