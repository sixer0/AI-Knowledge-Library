# Menggunakan pustaka dari harness di perangkat

Pustaka dapat ditelusuri dari clone lokal pada macOS, Linux, atau Windows. Buka folder
hasil clone sebagai konteks kerja harness, lalu baca panduan ini. Lokasi berkas
ditentukan dari root clone melalui [library.json](library.json), sehingga tidak
bergantung pada drive, nama pengguna, atau direktori kerja proses.

Panduan ini berlaku untuk Codex, Claude Code, dan harness lain yang dapat membaca
berkas lokal. Tidak diperlukan pemasangan profil Swarm atau akses ke host asal
untuk membaca koleksi. Jika memakai alat bantu Python di bawah, gunakan Python 3.10
atau lebih baru; alat tersebut hanya memakai pustaka standar.

## Pilih koleksi

| Kebutuhan | Titik masuk lokal |
|---|---|
| Prosedur kerja | [1 Workflow/INDEKS.md](1%20Workflow/INDEKS.md) |
| Peran dan kewenangan | [2 Roles/INDEKS.md](2%20Roles/INDEKS.md) |
| Skill sumber kurasi | [3 Skills/kanonik](3%20Skills/kanonik/) |
| Skill versi registry | [3 Skills/registry-fleet](3%20Skills/registry-fleet/) |
| Pengetahuan dan sumber | [4 Knowledge Bank/INDEKS.md](4%20Knowledge%20Bank/INDEKS.md) |
| Aturan penggunaan EKAS | [Panduan EKAS](4%20Knowledge%20Bank/ekas-lapis-teks/00_START-HERE/README.md) |
| Daftar unit dan kemampuan | [Indeks pengetahuan](4%20Knowledge%20Bank/indeks-pengetahuan/) |
| Arsitektur integrasi | [5 Integration/INDEKS.md](5%20Integration/INDEKS.md) |
| Skema dan snapshot | [6 Database/INDEKS.md](6%20Database/INDEKS.md) |
| Arsip perkakas | [7 Tools/INDEKS.md](7%20Tools/INDEKS.md) |

Buka SKILL.md atau berkas peran yang sesuai dengan tugas. Instruksi, layanan, tool,
nama profil, serta perintah host yang disebut dalam koleksi dapat membutuhkan
adaptasi pada harness aktif. Teks sumber tersebut tidak otomatis menjadi konfigurasi
perangkat ini. Jangan menjalankan skrip arsip hanya untuk mencari pengetahuan.

## Aturan tautan dan path

- Tautan Markdown relatif dihitung dari folder dokumen yang memuatnya. Spasi pada tujuan tautan ditulis sebagai `%20`.
- Path pada library.json relatif terhadap root clone. Alias seperti `ekas/` dan `roles/` diterjemahkan oleh resolver sesuai peta tersebut.
- Rujukan lokal yang tersedia menggunakan tautan langsung ke berkas di clone. Tidak diperlukan URL GitHub untuk membacanya.
- URL publik untuk sumber, atribusi, dan riwayat commit tetap eksternal. Alat lokal tidak mengambil URL tersebut secara otomatis.
- Alamat localhost, IP privat, Tailscale, dan path mesin pada catatan lama menggambarkan lingkungan sumber. Alamat itu tidak menetapkan endpoint harness ini.
- Metadata sumber, kutipan, CSV indeks, dan kode historis mempertahankan path aslinya. Resolver membantu menelusurinya jika salinannya tersedia.

## Menemukan rujukan lama

Jalankan contoh berikut dari root clone:

```sh
python3 tools/library.py resolve "ekas/00_START-HERE/README.md" --json
python3 tools/library.py resolve "roles/gsp-task-architect.md" --json
python3 tools/library.py resolve "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-ekas-knowledge-index/SKILL.md" --json
```

Untuk rujukan relatif yang dibaca dari dokumen tertentu, berikan konteks dokumennya:

```sh
python3 tools/library.py resolve "references/INDEKS-UNIT.csv" --from "3 Skills/kanonik/gsp-ekas-knowledge-index/SKILL.md" --json
```

Saat memanggil alat dari direktori lain, gunakan path menuju tools/library.py di
clone. Resolver tetap menemukan root melalui lokasi skripnya. Nilai `--from` selalu
relatif terhadap root clone, atau berupa path absolut dokumen di dalam clone.

| Status | Arti dan tindakan |
|---|---|
| `local` | Berkas atau folder tersedia; buka `absolute_path` pada perangkat saat ini. `fragment` menyimpan jangkar bila diberikan. |
| `external` | URL sumber atau layanan eksternal; akses hanya jika diperlukan tugas dan tersedia izin serta alatnya. |
| `missing` | Berkas tidak disertakan, path host belum dipetakan, atau jangkar tidak ditemukan. Nyatakan keterbatasannya. |
| `ambiguous` | Ada beberapa pemetaan yang sama kuat. Periksa rujukan sumber sebelum memilih. |
| `invalid` | Rujukan tidak valid atau mengarah ke luar clone. Perbaiki rujukannya. |

Resolver tidak memilih berkas hanya karena nama akhirnya mirip. Snapshot kanban
tidak diperlakukan sebagai basis data layanan aktif. PDF sumber dan dokumen misi
yang tidak disertakan tidak diganti dengan ringkasan yang berbeda.

Sebagian baris indeks EKAS masih menunjuk digest dari folder misi `sweep/` yang
tidak disertakan. Gunakan status resolver untuk membedakan sumber yang tersedia
dari sumber yang masih harus disediakan. Tingkat bukti dan batas penggunaan angka
tetap mengikuti dokumen EKAS.

## Memeriksa clone

```sh
python3 tools/library.py check
python3 -m unittest discover -s tests
```

Perintah pertama memeriksa alias, pintu masuk, tautan indeks, dan ukuran serta hash
manifest. Perintah kedua menguji resolver, termasuk pemindahan clone dan pemanggilan
dari direktori kerja yang berbeda. Keduanya tidak menjalankan skrip operasi arsip.

Laporan perubahan rujukan tersedia di [laporan portabilitas](outputs/portabilitas-harness-2026-10-19/README.md).
Audit bahasa sebelumnya berlaku pada commit `6e31e8b`; hasil hash audit tersebut
merupakan catatan sebelum penyesuaian tautan ini. Gunakan pemeriksaan clone di atas
untuk keadaan repositori saat ini.
