# Peta Integrasi Ekosistem Swarm

Dibekukan: 2026-10-19 (kartu SKL-NAS-1019)

| Komponen | Lokasi host | Peran | Catatan |
|---|---|---|---|
| GSP Agent HQ | C:/Users/TRIAL/gsp-datacenter (node hq-server.mjs) | Dasbor pemantauan dan pengendalian tugas, port 9011 | Login WebUiUser, cookie HMAC |
| WebUI Hermes | port 9012 via Tailscale | Antarmuka percakapan dengan agen fleet | Restart = wewenang user |
| Hermes Bridge | C:/Users/TRIAL/gsp-datacenter/hermes-bridge/bridge.mjs | Antrean pengiriman tugas lintas profil | RUN_TIMEOUT_MS=1800s; worker-2 cadangan |
| Kanban | C:/Users/TRIAL/AppData/Local/hermes/kanban.db | Papan tugas beserta kontrak setiap kartu (SQLite) | Salinan basis data saat layanan berjalan tersedia di 6 Database |
| Wiki IL | C:/Users/TRIAL/AppData/Local/hermes/wiki | Pustaka pengetahuan yang telah diterbitkan | Salinan di 4 Knowledge Bank |

Berkas di bagian ini merupakan salinan referensi untuk memahami arsitektur. Layanan tetap dijalankan dari lokasi aslinya pada host. Nilai rahasia (SECRET/TOKEN/PASSWORD/KEY) sudah
disamarkan dari berkas konfigurasi contoh.
