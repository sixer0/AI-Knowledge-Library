# AI Knowledge Library GSP

Pustaka pengetahuan dan perkakas operasional PT. Gemilang Satria Perkasa (GSP).
Edisi sumber dibuat pada 19 Oktober 2026 dari host Swarm untuk NAS UGREEN
(192.168.0.90, share GSP-DATA), melalui kartu SKL-NAS-1019.
Salinan ini dikelola dalam [repositori GitHub privat](https://github.com/sixer0/AI-Knowledge-Library).

## Cara menggunakan pustaka

Pilih folder sesuai topik, baca `INDEKS.md`, lalu buka berkas yang dibutuhkan.
Indeks menjelaskan isi folder dan mencantumkan lokasi berkas. Path dan nama teknis
mengikuti sumber asal agar rujukannya tetap dapat ditelusuri.

| Folder | Isi | Berkas isi, di luar INDEKS.md |
|---|---|---:|
| [1 Workflow](1%20Workflow/INDEKS.md) | Prosedur kerja, standar penataan dan metadata, pemeriksaan harian pustaka, serta jadwal otomatis (cron). | 8 |
| [2 Roles](2%20Roles/INDEKS.md) | Tugas dan kewenangan agen, daftar profil aktif, serta controller yang terikat pada akun pengguna (RBAC). | 49 |
| [3 Skills](3%20Skills/INDEKS.md) | Sumber skill yang dikurasi (`kanonik`) dan salinan yang digunakan fleet (`registry-fleet`). | 2320 |
| [4 Knowledge Bank](4%20Knowledge%20Bank/INDEKS.md) | Wiki Information Library, lapisan teks EKAS, indeks pengetahuan, dan katalog dokumen. | 1292 |
| [5 Integration](5%20Integration/INDEKS.md) | Hubungan antarkomponen Hermes, bridge pengiriman tugas, Headquarter pada port 9011, dan WebUI pada port 9012. | 6 |
| [6 Database](6%20Database/INDEKS.md) | Skema Prisma HQ dan salinan keadaan basis data kanban pada tanggal edisi. | 2 |
| [7 Tools](7%20Tools/INDEKS.md) | Skrip pemantauan, audit, pengelolaan tugas, utilitas repositori, dan contoh prompt historis. | 743 |

## Istilah yang digunakan

Controller adalah agen koordinator; worker adalah agen pelaksana. Dispatch berarti
pengiriman tugas. Gatekeeper berarti penanggung jawab kurasi atau pemeriksaan. Registry adalah daftar rujukan skill atau profil. Kanonik berarti
sumber acuan yang ditetapkan, sedangkan mirror adalah salinannya. Provenans adalah
catatan asal-usul sumber; attest adalah pengesahan hasil kurasi. Snapshot adalah
salinan keadaan data pada waktu tertentu.

## Kedudukan salinan ini

Layanan, papan kanban aktif, dan wiki produksi tetap berada pada host asal. Berkas di
repositori ini menjadi referensi pengetahuan dan arsitektur. Bahasa pada salinan lokal
disunting dalam audit 19 Oktober 2026; penyuntingan tersebut tidak memperbarui layanan,
profil agen, atau berkas NAS secara otomatis.

Menurut catatan edisi sumber, nilai rahasia pada konfigurasi contoh telah disamarkan
sebelum disalin. Audit bahasa ini tidak menyatakan telah melakukan audit keamanan.
Snapshot basis data dibuat melalui mekanisme backup SQLite saat layanan berjalan.

Proses pembangunan ulang salinan pada host asal menggunakan `build_staging.py`,
`upload_nas.py`, dan `verify_roundtrip.py`. Catatan sumber menempatkan skrip tersebut di
`docs/2026-10-19_swarm-knowledge-library-nas/scripts`; folder itu tidak disertakan di
repositori ini.

## Audit bahasa dan riwayat perubahan

[Laporan audit per folder](outputs/audit-bahasa-2026-10-19/README.md) menjelaskan perubahan,
contoh sebelum–sesudah, hasil pemeriksaan, dan batas audit. Versi awal tersimpan pada
commit `8785880`. Setiap folder memiliki commit perbaikan tersendiri; commit pemeriksaan
akhir mencatat koreksi lintas folder.

Untuk meninjau perubahan di GitHub, buka **Commits**, pilih commit folder, lalu baca
**Files changed**. Daftar berkas beserta hash sebelum dan sesudah tersedia pada laporan.

## Pemeriksaan keutuhan

`MANIFEST.csv` mencatat path relatif, ukuran byte, dan SHA-256 untuk 4.428 berkas pustaka
asli, termasuk README dan tujuh indeks. Manifest tidak mencatat dirinya sendiri,
metadata Git, `.gitignore`, atau laporan audit dalam `outputs/`.

Manifest diperbarui mengikuti isi salinan yang disunting. Manifest edisi awal tetap
tersedia pada commit awal, sehingga kedua keadaan dapat dibandingkan. Saat membandingkan
salinan NAS dengan repositori ini, gunakan manifest untuk edisi yang sesuai.
