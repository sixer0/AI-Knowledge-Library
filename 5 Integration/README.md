# 5 Integration

## Tujuan

Folder ini menyimpan salinan referensi arsitektur integrasi fleet di host asal: kode
dasbor Headquarter (HQ), kode bridge yang menghubungkan dasbor dengan CLI agen, contoh
variabel lingkungan dasbor yang telah disanitasi, dan peta komponen. Gunanya untuk
memahami bagaimana komponen saling terhubung, terutama bagaimana tugas dikirim dari
dasbor ke agen dan bagaimana hasilnya kembali.

Kode di sini tidak lengkap untuk dijalankan, dan layanannya tetap berada di host asal.
Panduan ini tidak mengajarkan penyiapan.

## Struktur subfolder

| Lokasi | Isi |
|---|---|
| [peta-integrasi.md](peta-integrasi.md) | Dua tabel: salinan komponen yang ada di clone dan kedudukannya, serta lokasi dan peran komponen di host asal |
| [hermes-bridge/](hermes-bridge/README.md) | Kode bridge (`bridge.mjs`) beserta README-nya |
| [hq/](hq/hq-server.mjs) | Pembungkus server produksi dasbor (`hq-server.mjs`), manifest paket Node (`package.json`), dan contoh variabel lingkungan yang disanitasi (`env-contohsaniter.txt`) |

## Peta topik

### Komponen dan hubungannya

Ringkasan dari [peta-integrasi.md](peta-integrasi.md) dan
[hermes-bridge/README.md](hermes-bridge/README.md):

- **Dasbor HQ** adalah aplikasi web Next.js untuk memantau dan mengendalikan tugas fleet.
  Datanya disimpan di Postgres dengan skema Prisma (lihat `6 Database`).
- **Postgres bersama** berfungsi sebagai bus pesan. Dasbor menulis permintaan ke tabel
  `AgentRequest` dan membaca hasil cerminan dari `HermesTask`, `AgentEvent`, dan
  `DataStore`.
- **Bridge** berjalan di mesin agen. Bridge hanya membutuhkan koneksi keluar ke Postgres
  dan CLI agen lokal, tanpa membuka layanan.
- **Kanban** adalah papan tugas SQLite milik agen. Bridge mencerminkannya ke `HermesTask`.
  Salinan beku papan ini ada di `6 Database/snapshot`.
- **Wiki IL** adalah pustaka terbit yang dicerminkan bridge ke `HermesMemory`. Salinannya
  ada di `4 Knowledge Bank/wiki-information-library`.
- **WebUI percakapan** tidak disertakan di clone ini. Hubungannya dengan dasbor hanya
  terlihat dari model `WebUiUser` dan kelompok variabel RBAC.

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Daftar komponen yang tersedia di clone dan kedudukannya (salinan kode, snapshot beku, pustaka lokal, tidak disertakan) | [peta-integrasi.md](peta-integrasi.md) | Salinan yang tersedia di clone |
| Peran tiap komponen di host asal dan catatannya (cara login dasbor, batas waktu bridge, letak papan dan wiki) | [peta-integrasi.md](peta-integrasi.md) | Lokasi pada host asal |
| Diagram aliran dua arah dasbor, Postgres, bridge, CLI | [hermes-bridge/README.md](hermes-bridge/README.md) | Paragraf pembuka dan diagram (baris 5-11) |

### Cara bridge mengirim tugas

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Fungsi pull (cermin papan, cron, kondisi layanan, aktivitas) dan push (menjalankan permintaan berstatus `queued` atau `approved`; `awaiting_approval` tidak dijalankan) | [hermes-bridge/README.md](hermes-bridge/README.md) | Fungsi |
| Nama variabel lingkungan bridge dan artinya | [hermes-bridge/README.md](hermes-bridge/README.md) | Konfigurasi variabel lingkungan |
| Asumsi bentuk argumen CLI, tulis SQL langsung tanpa Prisma, persetujuan pengguna lewat Approval Inbox | [hermes-bridge/README.md](hermes-bridge/README.md) | Catatan dan asumsi |
| Perbedaan salinan dengan sumber: nilai batas waktu di README berbeda dari konstanta di kode; dua berkas pendukung tidak disertakan | [hermes-bridge/README.md](hermes-bridge/README.md) | Batas salinan ini |
| Ringkasan dua tugas bridge dan variabel yang dibutuhkan | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Komentar kepala, baris 2-18 |
| Konstanta konfigurasi yang dibaca dari lingkungan | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Baris 30-47 |
| Pembuatan, pemantauan, dan penutupan kartu kanban untuk permintaan yang ditujukan ke profil | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | `createKanbanCard`, `closeKanbanCard`, `awaitCardCompletion` (baris 234-362) |
| Cerminan papan, cron, biaya, kondisi layanan, dan wiki ke Postgres | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Blok "PULL" (mulai baris 363) dan "Memory Wiki" (mulai baris 481) |
| Pembuatan ringkasan harian otomatis | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Blok "Chief-of-staff daily brief" (mulai baris 556) |
| Eksekusi satu permintaan: telemetri orkestrasi, aturan satu kartu satu eksekutor (kartu ber-assignee diserahkan ke dispatcher), pemotongan hasil yang menjaga JSON tetap valid | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Blok "PUSH", `runRequestClaimed` (mulai baris 618) |
| Dua jalur antrean: jalur utama satu permintaan per iterasi dengan klaim atomik, dan jalur cepat paralel untuk permintaan seketika | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | `processQueue`, `askLane` (baris 823-861) |
| Pemulihan permintaan dan edge orkestrasi yang tertinggal berstatus berjalan setelah restart, urutan startup | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | `recoverZombies`, `main` (baris 873-918) |

### Dasbor HQ

| Kebutuhan / topik | Berkas | Bagian |
|---|---|---|
| Pembungkus server produksi Next.js: membaca port dan daftar antarmuka dari lingkungan, memakai TLS bila berkas sertifikat ada, riwayat keputusan bind pada komentar kepala | [hq/hq-server.mjs](hq/hq-server.mjs) | Komentar baris 1-8; kode baris 14-43 |
| Kerangka aplikasi: Next.js, NextAuth dengan adapter Prisma, klien Postgres, bot Telegram, Google API, uji vitest | [hq/package.json](hq/package.json) | `scripts`, `dependencies`, `devDependencies` |
| Kelompok variabel lingkungan dasbor: inti wajib (basis data, sesi, login OAuth, daftar email yang diizinkan), Hermes dan bridge (termasuk rahasia rute internal dan cron), penyedia AI opsional, YouTube, X, Notion, Client Pulse, radar trading, RBAC antara dasbor dan WebUI, gerbang dev-bypass | [hq/env-contohsaniter.txt](hq/env-contohsaniter.txt) | Judul kelompok bergaris pada baris 13, 50, 84, 101, 110, 116, 122, 130, 136, 152 |

[hq/env-contohsaniter.txt](hq/env-contohsaniter.txt) adalah contoh variabel lingkungan
yang disanitasi. Panduan ini hanya merujuk judul kelompoknya; nilai di dalamnya tidak
disalin dan tidak dipakai.

## Titik masuk

- Cara bridge mengirim tugas: [hermes-bridge/README.md](hermes-bridge/README.md), bagian
  Fungsi, lalu [bridge.mjs](hermes-bridge/bridge.mjs) blok PUSH untuk rinciannya.
- Peta komponen: [peta-integrasi.md](peta-integrasi.md).
- Tabel yang dipakai sebagai bus: `AgentRequest`, `AgentEvent`, `HermesTask` pada
  [skema Prisma](../6%20Database/schema-prisma-hq.prisma).
- Inventaris berkas: [INDEKS.md](INDEKS.md).

## Jebakan

- Tabel variabel README bridge menyebut nilai bawaan batas waktu pelaksanaan yang berbeda
  dari konstanta di kode (baris 34). README salinan sendiri mengakui ini pada bagian
  "Batas salinan ini".
- `bridge.mjs` mengimpor modul gerbang yang tidak ada di folder ini, dan berkas layanan
  latar yang disebut README juga tidak disertakan. Kode tidak lengkap.
- README bridge menggambarkan penyiapan di satu jenis mesin, sedangkan kode juga memuat
  penanganan proses sistem operasi lain. Lokasi di `peta-integrasi.md` juga milik host
  lain. Path, port, dan alamat pada salinan ini tidak menggambarkan perangkat pembaca.
- Komentar `hq-server.mjs` dan [INDEKS.md](INDEKS.md) menyebut port dan antarmuka jaringan
  host asal. Keduanya bukan endpoint harness ini (AP-16).
- Schema Prisma dasbor memakai Postgres, sedangkan papan kanban memakai SQLite. Snapshot
  di `6 Database` adalah papan kanban, bukan basis data dasbor.
- Bagian penyiapan README bridge memuat perintah pemasangan dan menjalankan layanan.
  Perintah itu tidak dijalankan (AP-11, AP-12).

## Hubungan dengan koleksi lain

- [6 Database](../6%20Database/INDEKS.md): [schema-prisma-hq.prisma](../6%20Database/schema-prisma-hq.prisma)
  mendefinisikan tabel yang dibaca dan ditulis dasbor serta bridge, dan
  [snapshot kanban](../6%20Database/snapshot/kanban-2026-10-19.db) adalah salinan beku papan
  yang dicerminkan bridge.
- [4 Knowledge Bank](../4%20Knowledge%20Bank/INDEKS.md): salinan wiki yang dicerminkan
  bridge ke `HermesMemory`.
- [1 Workflow](../1%20Workflow/INDEKS.md): job cron yang memantau dasbor dan WebUI, serta
  prosedur harian pustakawan yang memanggil API IL dasbor.
- [7 Tools](../7%20Tools/INDEKS.md): arsip skrip fleet, termasuk skrip yang membangun
  daftar controller dari data RBAC.
- Akses lintas harness: [HARNESS.md](../HARNESS.md).

## Sensitivitas

Ikuti [KEBIJAKAN-SENSITIVITAS.md](../KEBIJAKAN-SENSITIVITAS.md), bagian "Kelas penanganan"
(baris 13), "Aturan" (baris 30), dan "Menjalankan skrip arsip" (baris 137). Untuk folder
ini, yang terutama berlaku:

- `bridge.mjs`, `hq-server.mjs`, dan `package.json` adalah kode arsip (KM-7). Kode ini
  dibaca tanpa dijalankan, dan dependensinya tidak dipasang.
- Rincian host, port, dan antarmuka jaringan pada berkas ini termasuk KM-4 dan tidak
  disalin ke keluaran.
- `env-contohsaniter.txt` dibaca sebatas nama kelompok dan nama variabel. Contoh nilai
  bukan pola yang ditiru, dan nilai kredensial tidak dicari di berkas lokal (AP-15).

Disusun 2026-11-06 dari keadaan commit 023082a. Inventaris lengkap: INDEKS.md.
