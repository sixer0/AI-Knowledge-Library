# Brahma Bridge

Panduan ini merekam penyiapan pada host asal. Untuk menelusuri salinan melalui harness lokal, mulai dari [HARNESS.md](../../HARNESS.md). Kode bridge dan perintah penyiapan di bawah tetap membutuhkan lingkungan serta dependensi sumber.

Bridge menyinkronkan **GSP Agent Headquarter** (situs yang telah dipasang) dengan **Brahma** (agen lokal pada Mac mini) dalam dua arah. Keduanya bertukar pesan melalui Postgres bersama. Bridge hanya memerlukan koneksi keluar ke Postgres dan akses ke CLI `hermes` lokal; bridge tidak membuka layanan ke internet.

```
website  ──insert AgentRequest──▶  Postgres  ◀──poll & run──  bridge ──▶ hermes CLI
website  ◀──read HermesTask/────   Postgres  ◀──mirror───────  bridge ◀── hermes CLI
             AgentEvent/DataStore
```

## Fungsi
- **Pull (Brahma → website):** menyalin papan kanban ke `HermesTask`, menyimpan daftar cron dan kondisi layanan ke `DataStore`, serta mencatat aktivitas di `AgentEvent`.
- **Push (website → Brahma):** menjalankan baris `AgentRequest` berstatus `queued` (aman) atau `approved` (tindakan yang memerlukan persetujuan sudah disetujui pengguna) melalui CLI `hermes`, lalu menyimpan hasilnya. Baris berstatus `awaiting_approval` tidak dijalankan.

## Penyiapan pada Mac mini
1. Salin folder ini ke Mac mini, atau jalankan `git pull` pada repositorinya di sana.
2. Pasang dependensi yang dibutuhkan:
   ```sh
   cd hermes-bridge && npm install
   ```
3. Pastikan `hermes` tersedia melalui PATH. Perintah `which hermes` harus menemukan berkasnya, misalnya `~/.local/bin/hermes`.
4. Jalankan sekali dengan alamat basis data yang akan digunakan:
   ```sh
   DATABASE_URL='postgres://…' HERMES_BOARD=default node bridge.mjs
   ```
   Jika koneksi berhasil, pesan `hermes-bridge up …` muncul dan aktivitas "Bridge connected" tercatat pada situs.
5. Untuk menjalankannya terus-menerus, gunakan launchd:
   ```sh
   # edit the placeholders in ai.gspagenthq.bridge.plist first (path, DATABASE_URL, PATH)
   cp ai.gspagenthq.bridge.plist ~/Library/LaunchAgents/
   launchctl load ~/Library/LaunchAgents/ai.gspagenthq.bridge.plist
   ```
   Lokasi log: `/tmp/hermes-bridge.out.log`, `/tmp/hermes-bridge.err.log`.

## Konfigurasi variabel lingkungan
| Variabel | Nilai bawaan | Keterangan |
|---|---|---|
| `DATABASE_URL` | — (wajib diisi) | Postgres yang juga digunakan situs |
| `HERMES_BOARD` | `default` | slug papan kanban yang akan disalin |
| `HERMES_BIN` | `hermes` | path CLI jika tidak tersedia melalui PATH |
| `BRIDGE_POLL_MS` | `5000` | jeda pemeriksaan permintaan baru, dalam milidetik |
| `BRIDGE_MIRROR_MS` | `30000` | jeda penyalinan kanban, cron, dan kondisi layanan, dalam milidetik |
| `BRIDGE_RUN_TIMEOUT_MS` | `240000` | batas waktu satu pelaksanaan tugas agen, dalam milidetik |

## Catatan dan asumsi
- Bentuk argumen CLI (`hermes kanban create <title>`, `hermes cron create <schedule> <prompt>`) disusun berdasarkan Hermes v0.17.x. Jika versi yang digunakan berbeda, sesuaikan `runRequest()` di [`bridge.mjs`](bridge.mjs).
- Bridge menulis ke Postgres melalui SQL langsung sehingga tidak memerlukan Prisma.
- Pekerjaan yang menimbulkan perubahan harus disetujui pengguna melalui Approval Inbox pada situs sebelum dijalankan oleh bridge.

## Batas salinan ini

Panduan ini mengikuti README sumber untuk Mac mini. Skrip yang disertakan juga memuat penanganan proses Windows. Tabel nilai bawaan waktu tunggu pada README sumber berbeda dari konstanta RUN_TIMEOUT_MS dalam skrip; gunakan nilai dalam skrip ketika menyiapkan layanan. Berkas pendukung gate_transport.mjs dan ai.gspagenthq.bridge.plist tidak tersedia dalam folder salinan ini. Audit bahasa tidak menjalankan penyiapan layanan.
