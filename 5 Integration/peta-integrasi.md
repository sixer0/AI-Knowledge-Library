# Peta Integrasi Ekosistem Swarm

Dibekukan: 2026-10-19 (kartu SKL-NAS-1019)

| Komponen | Lokasi host | Peran | Catatan |
|---|---|---|---|
| GSP Agent HQ | C:/Users/TRIAL/gsp-datacenter (node hq-server.mjs) | Dashboard mission control, port 9011 | Login WebUiUser, cookie HMAC |
| WebUI Hermes | port 9012 via Tailscale | Antarmuka chat fleet | Restart = wewenang user |
| Hermes Bridge | C:/Users/TRIAL/gsp-datacenter/hermes-bridge/bridge.mjs | Antrean dispatch lintas profil | RUN_TIMEOUT_MS=1800s; worker-2 cadangan |
| Kanban | C:/Users/TRIAL/AppData/Local/hermes/kanban.db | Papan kontrak kartu (SQLite) | Snapshot hangat di 6 Database |
| Wiki IL | C:/Users/TRIAL/AppData/Local/hermes/wiki | Knowledge Library terbit | Salinan di 4 Knowledge Bank |

Berkas di seksi ini adalah SALINAN REFERENSI untuk pemahaman arsitektur; eksekusi
tetap dari lokasi host aslinya. Nilai rahasia (SECRET/TOKEN/PASSWORD/KEY) sudah
disamarkan dari berkas konfigurasi contoh.
