# Peta Integrasi Ekosistem Swarm

Dibekukan: 2026-10-19 (kartu SKL-NAS-1019)

## Salinan yang tersedia di clone

| Komponen | Rujukan lokal | Kedudukan |
|---|---|---|
| Headquarter | [hq/hq-server.mjs](hq/hq-server.mjs) | Salinan kode referensi |
| Hermes Bridge | [hermes-bridge/bridge.mjs](hermes-bridge/bridge.mjs) | Salinan kode referensi; dependensi host dijelaskan pada README bridge |
| Kanban | [Snapshot basis data](../6%20Database/snapshot/kanban-2026-10-19.db) | Keadaan beku pada tanggal edisi; tidak menjadi basis data layanan aktif |
| Wiki IL | [Salinan wiki](../4%20Knowledge%20Bank/wiki-information-library/) | Pustaka lokal untuk ditelusuri |
| WebUI Hermes | Tidak disertakan | Alamat layanan lama bukan endpoint harness ini |

Untuk penggunaan lintas harness, baca [HARNESS.md](../HARNESS.md).

## Lokasi pada host asal

Tabel berikut merekam arsitektur sumber. Path, port, dan alamat tersebut tidak
menentukan lokasi clone atau konfigurasi layanan pada perangkat pembaca.

| Komponen | Lokasi host | Peran | Catatan |
|---|---|---|---|
| GSP Agent HQ | C:/Users/TRIAL/gsp-datacenter (node hq-server.mjs) | Dasbor pemantauan dan pengendalian tugas, port 9011 | Login WebUiUser, cookie HMAC |
| WebUI Hermes | port 9012 via Tailscale | Antarmuka percakapan dengan agen fleet | Restart = wewenang user |
| Hermes Bridge | C:/Users/TRIAL/gsp-datacenter/hermes-bridge/bridge.mjs | Antrean pengiriman tugas lintas profil | RUN_TIMEOUT_MS=1800s; worker-2 cadangan |
| Kanban | C:/Users/TRIAL/AppData/Local/hermes/kanban.db | Papan tugas beserta kontrak setiap kartu (SQLite) | Salinan basis data saat layanan berjalan tersedia di 6 Database |
| Wiki IL | C:/Users/TRIAL/AppData/Local/hermes/wiki | Pustaka pengetahuan yang telah diterbitkan | Salinan di 4 Knowledge Bank |

Berkas di bagian ini merupakan salinan referensi untuk memahami arsitektur. Layanan tetap dijalankan dari lokasi aslinya pada host. Nilai rahasia (SECRET/TOKEN/PASSWORD/KEY) sudah
disamarkan dari berkas konfigurasi contoh.
