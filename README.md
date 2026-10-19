# SWARM Knowledge Library

Pustaka pengetahuan dan perkakas operasional PT. Gemilang Satria Perkasa (GSP),
dicermin dari host Swarm ke NAS UGREEN (192.168.0.90, share GSP-DATA).
Edisi dasar dibangun 2026-10-19 (kartu kanban SKL-NAS-1019).

## Cara pakai

Cari topik -> buka seksi terkait -> baca `INDEKS.md` seksi itu -> buka berkas.
Setiap berkas punya entri di `MANIFEST.csv` (path, byte, sha256) untuk uji keutuhan.

## Tujuh seksi (direktif user 19-10-2026)

| Seksi | Isi | Berkas |
|---|---|---|
| `1 Workflow` | Prosedur dan kebijakan cara kerja Swarm: standar organisasi/metadata, prosedur harian pustakawan, kebijakan lean fleet, definisi tugas terjadwal (cron). | 8 |
| `2 Roles` | Definisi peran agen (berkas peran fleet pasca PROF-MERGE-1010), registri profil hidup, dan roster controller RBAC. | 49 |
| `3 Skills` | Seluruh skill GSP: sumber kanonik (repo gsp-hermes/skills) dan mirror registry fleet ($LOCALAPPDATA/hermes/skills/gsp). | 2320 |
| `4 Knowledge Bank` | Bank pengetahuan: wiki Information Library (hasil attest librarian), korpus teks EKAS, indeks pengetahuan terstruktur (unit/kemampuan/domain), dan katalog dokumen standar. | 1292 |
| `5 Integration` | Titik integrasi ekosistem: bridge dispatch Hermes, server Headquarter (port 9011), WebUI (9012), dan catatan API internal (tanpa nilai rahasia). | 6 |
| `6 Database` | Skema dan snapshot basis data: skema Prisma HQ, salinan hangat kanban.db (sqlite backup, bukan file hidup), dan ekspor konfigurasi terjadwal. | 2 |
| `7 Tools` | Perkakas operasi fleet: skrip watchdog/audit/monitor profil controller dan skrip utilitas repo gsp-hermes. | 743 |

## Batas dan kekekalan

- Ini **cermin pengetahuan**, bukan sumber eksekusi. Layanan, papan kanban hidup,
  dan wiki produksi tetap berjalan di host; salinan NAS dibekukan pada tanggal edisi.
- Nilai rahasia (secret/token/password/API key) **tidak pernah** ikut naik; berkas
  konfigurasi contoh disamarkan sebelum disalin.
- Basis data naik sebagai **snapshot hangat** (sqlite backup), bukan berkas hidup.
- Regenerasi: jalankan `build_staging.py` lalu `upload_nas.py` + `verify_roundtrip.py`
  (skrip tersimpan di folder misi docs/2026-10-19_swarm-knowledge-library-nas/scripts).

## Manifest

`MANIFEST.csv` = daftar semua berkas (relatif terhadap root library) dengan ukuran
dan sha256. Uji keutuhan: bandingkan sha256 berkas NAS (MDTM/RETR) terhadap manifest.
