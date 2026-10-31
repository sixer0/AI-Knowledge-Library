# Panduan akses edisi umum

Panduan ini untuk pengguna yang ingin agen dari proyek lain membaca pustaka. Edisi umum adalah turunan pustaka yang hanya memuat berkas pada daftar izin. Clone penuh adalah repositori sumber yang lengkap, tempat edisi dibangun. Contoh di sini memakai `{{EDITION_PATH}}` untuk path absolut edisi pada perangkat Anda.

## 1. Status

Panduan ini hanya menunjuk edisi umum. Tidak ada yang terpasang otomatis: tidak ada alat, skrip, atau langkah build pustaka yang menulis ke konfigurasi harness. Semua langkah di bawah dilakukan pengguna. Membaca edisi tidak memerlukan Python, proses, atau symlink.

Yang perlu diketahui tentang isi edisi:

- **Edisi pertama sengaja dipersempit.** Edisi dapat dibaca harness dan penyedia apa pun, jadi kehilangan isi dinilai lebih murah daripada kebocoran. Berkas yang diragukan dikeluarkan. Koleksi yang tidak tercantum pada `README.md` edisi tidak tersedia.
- **Pengetahuan teknis EKAS tidak ikut.** Dari EKAS, hanya templat, verifikasi, bukti, dan serah terima yang ikut. Sisanya ditunda ke edisi berikutnya.
- **Tidak ada klaim bersih.** Pemindaian pola saat build adalah batas bawah. Nama tanpa gelar dan isi yang maknanya peka tetapi tanpa kata kunci tidak terdeteksi, jadi build yang lulus bukan bukti bahwa isi sudah bersih.
- **`approval` pada daftar izin diberikan AI atas pelimpahan pemilik.** Itu bukan hasil tinjauan pemilik. Tinjauan AI melihat baris yang ditunjuk pemindaian, bukan seluruh berkas.
- **Teks tidak menegakkan apa pun.** Penunjuk, stempel, dan kebijakan hanya berpengaruh pada agen yang membaca dan mematuhinya (bagian 7).

## 2. Pemeriksaan edisi

Sebelum memasang penunjuk, pastikan:

1. Folder `{{EDITION_PATH}}` ada. Nama folder yang dianjurkan `ai-knowledge-library-edisi-umum`, di luar clone penuh dan sebaiknya bukan saudara clone penuh.
2. `{{EDITION_PATH}}/library.json` memuat blok `edition` dengan `id` bernilai `edisi-umum`.

Bila salah satunya tidak ada, berhenti. Jangan menunjuk clone penuh sebagai gantinya. Pemilik membangun edisi dari clone penuh dengan `python3 tools/build_edition.py build --output "{{EDITION_PATH}}"`. Alat itu dan berkas pola lokalnya tidak ikut edisi.

## 3. Penunjuk

Salin blok dari [TEMPLAT-PENUNJUK.md](TEMPLAT-PENUNJUK.md), lalu isi path. Blok itu tidak memakai variabel, awalan `@`, atau tautan, dengan alasan berikut:

- Harness yang hanya membaca berkas tidak dapat mengekspansi variabel, jadi path harus absolut.
- Awalan `@path` pada sebagian harness mengimpor isi ke setiap sesi, sehingga isi pustaka mengalir ke penyedia model pada tugas yang tidak terkait.
- `library.json` dibaca pertama karena ketiadaan blok `edition` menandakan repositori penuh. Inilah satu-satunya pemeriksaan yang tersedia bagi pembaca berkas polos.

Penunjuk memberi tahu agen, tetapi tidak memberi izin baca. Izin ada pada kelas 2.

## 4. Kelas harness

Satu harness dapat memerlukan kelas 1 dan kelas 2 sekaligus. Kolom dasar menyatakan asal keterangan; kolom status menyatakan hasil uji pada pustaka. Tautan sumber ada pada bagian 9.

### Kelas 1: harness dengan berkas instruksi tingkat pengguna

Rekatkan blok terisi ke berkas pengguna.

| Harness | Tempat penunjuk | Dasar | Status |
|---|---|---|---|
| Claude Code | `~/.claude/CLAUDE.md` | Dokumentasi resmi | `belum diuji` |
| Codex | `~/.codex/AGENTS.md`, atau di bawah `CODEX_HOME`. `AGENTS.override.md` dibaca lebih dulu, dan hanya berkas non-kosong pertama yang dipakai | Dokumentasi resmi | `belum diuji` |
| opencode | `~/.config/opencode/AGENTS.md`. Bila tidak ada, `~/.claude/CLAUDE.md` dibaca sebagai cadangan, jadi penunjuk di sana ikut mencapai opencode | Dokumentasi resmi | `belum diuji` |
| Kilo Code | Berkas pilihan pengguna di luar repositori, didaftarkan pada `instructions` di `~/.config/kilo/kilo.jsonc`. Path absolut pada `instructions` belum dipastikan | Dokumentasi resmi | `belum diuji` |
| Gemini CLI, Antigravity CLI | `~/.gemini/GEMINI.md`. Dokumentasi Gemini CLI mungkin usang | Dokumentasi resmi | `belum diuji` |
| Cursor | User Rules di pengaturan aplikasi, bukan berkas | Dokumentasi resmi | `belum diuji` |

### Kelas 2: izin direktori tambahan atau direktori eksternal

Aturan untuk semua harness: **izinkan folder edisi saja, tidak pernah induknya.** Bila induk itu juga memuat clone penuh, mengizinkan induk sama dengan mengizinkan keduanya.

| Harness | Mekanisme | Catatan | Status |
|---|---|---|---|
| Claude Code | `--add-dir`, `/add-dir`, atau `permissions.additionalDirectories` pada pengaturan pengguna | Direktori itu terbaca tanpa prompt, dan penyuntingan mengikuti mode izin, jadi kata "baca-saja" pada penunjuk bukan penegakan. `CLAUDE.md` di sana tidak dimuat secara bawaan, dan variabel pelonggarnya tidak perlu diaktifkan | `belum diuji` |
| opencode | `permission.external_directory`, misalnya `"{{EDITION_PATH}}/**": "allow"`. Bawaan `ask` juga cukup: setiap pembacaan meminta persetujuan | | `belum diuji` |
| Gemini CLI | `/directory add`, `--include-directories` | Mekanisme terdokumentasi; pembacaan tanpa itu tidak dikonfirmasi | `belum diuji` |
| Antigravity CLI | Tidak dinyatakan. Pakai kelas 3 | Akses di luar proyek belum diperiksa | `belum diuji` |
| Codex | **Jangan pakai `--add-dir` untuk pustaka.** Sumber menyatakan flag itu memberi akses tulis. Pakai kelas 3 | Pembacaan di luar workspace tidak dikonfirmasi | `belum diuji` |
| Kilo Code | Tidak dinyatakan sampai ada hasil uji. Pakai kelas 3 | Keterangan yang ada hanya hipotesis | `belum diuji` |
| Cursor | Tidak dinyatakan. Pakai kelas 3 | Perilaku di luar workspace hanya dari forum | `belum diuji` |

### Kelas 3: pembaca berkas polos

Untuk harness tanpa berkas instruksi tingkat pengguna, atau yang tidak dapat membaca di luar workspace. Dua cara, keduanya tanpa adapter dan tanpa Python:

1. **Sebagai pesan pertama.** Rekatkan blok terisi pada awal sesi. Cara ini berlaku selama harness dapat membaca path itu.
2. **Sebagai workspace.** Buka folder edisi sebagai konteks kerja. Cara ini selalu tersedia. Batasnya: sesi itu bekerja pada pustaka, bukan pada proyek lain, sehingga isi perlu dibawa manual antarsesi. Multi-root tidak dijadikan jalan keluar, karena perilakunya pada Cursor hanya dari forum.

Urutan baca tetap: `library.json`, `HARNESS.md`, lalu katalog koleksi. Semuanya berkas teks.

## 5. CLI opsional

`tools/library.py` ikut edisi, hanya untuk rujukan lama dan pemeriksaan. Tidak ada subperintah pencarian; agen memakai pencarian harnessnya.

```text
python3 "{{EDITION_PATH}}/tools/library.py" resolve "<rujukan>" --json
python3 "{{EDITION_PATH}}/tools/library.py" check
```

Path selalu dikutip. Root ditentukan dari lokasi skrip, jadi direktori kerja tidak berpengaruh. Hasil `check` yang lulus membuktikan keutuhan terhadap manifest edisi, bukan kesegaran terhadap sumber.

Tanpa Python, status resolver tidak tersedia. Agen membaca peta alias pada `library.json` dan menyatakan bahwa rujukan tidak terverifikasi. Rujukan yang tidak terbuka tidak diganti dengan berkas bernama mirip.

## 6. Bila penunjuk tidak ada

Agen tanpa penunjuk belum membaca teks apa pun dari pustaka, jadi panduan ini tidak dapat mewajibkan perilakunya. Baris berikut adalah keadaan yang diharapkan, bukan jaminan.

| Keadaan | Yang diharapkan | Teks yang mencapainya |
|---|---|---|
| Tidak ada penunjuk, tugas tidak terkait pustaka | Agen tidak mengetahui pustaka dan tidak membukanya. Ini keadaan tertutup yang benar, bukan kegagalan | Tidak ada |
| Tidak ada penunjuk, pengguna menyebut pustaka tanpa path | Pustaka tidak menyediakan cara menemukan dirinya. Pengguna memberi path edisi, dan sesi itu menjadi kelas 3 | Hanya panduan ini, yang dibaca pengguna |
| Agen diberi path edisi tanpa penunjuk, atau mendarat dari pencarian | Batas tetap sampai lewat `AGENTS.md`, `HARNESS.md`, dan stempel pada salinan | Stempel, `AGENTS.md` |
| Penunjuk ada, path tidak ada atau tidak terbaca | Agen melapor dan lanjut tanpa pustaka, tanpa memindai disk | Baris terakhir penunjuk |
| Penunjuk ada, tetapi menuju clone penuh | Agen berhenti setelah `library.json`, karena blok `edition` tidak ada, lalu melapor. Isian seperti ini dilarang | Langkah 1 penunjuk |
| Penunjuk ada, pembacaan ditolak harness | Agen melapor dan meminta pengguna mengizinkan folder edisi saja, atau membukanya sebagai workspace, tanpa beralih ke shell | Baris terakhir penunjuk |

Agen yang membuka clone penuh sebagai workspace tanpa penunjuk berada di luar panduan ini. Clone penuh hanya untuk harness dan penyedia yang disebut namanya oleh pemilik, menurut `HARNESS.md` pada clone itu.

## 7. Batas clone penuh

> Edisi umum mencegah pendaratan tanpa sengaja pada materi terbatas. Edisi tidak menghentikan harness berizin baca luas untuk membuka clone penuh yang berada di disk yang sama. Teks, stempel, dan penanda tidak menegakkan apa pun; yang mencegah pembacaan hanya ketiadaan berkas pada jangkauan harness.

1. Penunjuk mencegah **pendaratan tanpa sengaja**, bukan pembacaan. Harness berizin baca luas tetap dapat membuka clone penuh dan `work/` bila keduanya ada di perangkat itu.
2. Yang benar-benar mencegah pembacaan hanyalah ketiadaan berkas pada jangkauan harness.
3. Pilihan pemilik per perangkat ada pada tabel tingkat di bawah.

**Jangan meluncurkan harness dari folder induk bersama.** Sesi yang diluncurkan dari folder yang memuat edisi dan clone penuh, termasuk folder home, menjangkau keduanya. Memisahkan lokasi hanya mengurangi peluang, tidak menutupnya.

### Kapan `permissions.blockReadsOutsideWorkingDirectories` berlaku

Khusus Claude Code, v2.1.257 atau lebih baru. Nilai bawaan tidak disetel. Tabel ini berasal dari dokumentasi resmi, belum diuji pada pustaka (bagian 9).

| Keadaan | Hasil | Akibat bagi pustaka |
|---|---|---|
| `true` pada berkas pengaturan mana pun, clone penuh di luar semua direktori kerja, alat `Read`, `Grep`, `Glob`, atau `LSP` | Ditolak, pada semua mode, termasuk `bypassPermissions` | Inilah cakupan penegakannya |
| Perintah shell pembaca berkas yang dikenali, menuju luar direktori kerja | Tidak ditolak; meminta persetujuan, juga pada mode auto dan `bypassPermissions` | Bukan batas bila pengguna menyetujui |
| Perintah shell yang tidak dapat ditelusuri parser, misalnya subshell | Meminta persetujuan, kecuali berjalan dalam sandbox yang menegakkan blokir | Sama |
| Skrip yang membuka berkas sendiri, misalnya Python | Tidak dinyatakan pada halaman blokir ini | Diperlakukan sebagai belum tertutup tanpa sandbox |
| Perintah `git` atas clone penuh, misalnya `cat-file` dan `grep` | Tidak disebut halaman di atas. Jalur ini menjangkau seluruh blob | Diperlakukan sebagai belum tertutup; `belum diuji` |
| Sandbox aktif | Blokir mencakup perintah bersandbox. Pengecualian: `sandbox.filesystem.disabled`, `allowManagedReadPathsOnly`, dan path direktori awal yang memuat karakter glob | Satu-satunya bentuk yang mencapai tingkat OS; kombinasi ini `belum diuji` |
| Clone penuh di dalam direktori kerja: sesi diluncurkan di sana atau di induknya, atau ditambahkan lewat `--add-dir`, `/add-dir`, `additionalDirectories` | Tidak berlaku | Tidak ada perlindungan |
| Edisi ditambahkan lewat flag, perintah, atau pengaturan pengguna atau managed | Dihitung direktori kerja, jadi edisi terbaca | Inilah cara memasangnya |
| Edisi ditambahkan hanya pada pengaturan repositori | Tidak dihitung, jadi edisi ikut ditolak | Jangan memakai cara ini |
| Berkas yang diperlukan harness di bawah `~/.claude/`, seperti skill dan rules | Tetap terbaca | Inferensi: tautan skill menuju clone penuh dapat melewati pagar ini. Jangan membuat symlink ke pustaka |
| Harness lain | Tidak berlaku | Tidak ada padanan yang dikonfirmasi. opencode punya `external_directory` bawaan `ask`, yang bergantung pada jawaban pengguna |

Tanpa pengaturan ini, pada mode auto, pembacaan di luar direktori kerja berjalan tanpa prompt selain satu pertanyaan pada pembacaan pertama. Pada `-p` dan sesi latar, pertanyaan itu pun tidak ada. Jadi pada mode tersebut clone penuh dapat terbaca, dan izin kelas 2 bukan pagar.

**Efek samping.** Pengaturan ini mengubah konfigurasi harness, jadi panduan hanya menjelaskannya dan pengguna yang menyetelnya. Bila disetel pada pengaturan pengguna, pembacaan di luar direktori kerja ditolak pada **semua proyek**, bukan hanya pustaka. Pilihan "No, and block" pada prompt mode auto menulis nilai yang sama secara diam-diam, sehingga edisi yang belum ditambahkan ikut tertolak. Mencabutnya berarti menghapus kunci dari setiap berkas yang menyetelnya, lalu memulai sesi baru.

Contoh, bila Anda memilihnya:

```json
{
  "permissions": {
    "additionalDirectories": ["{{EDITION_PATH}}"],
    "blockReadsOutsideWorkingDirectories": true
  }
}
```

### Pilihan pemilik per perangkat

| Tingkat | Keadaan | Yang tercegah | Yang tersisa |
|---|---|---|---|
| 1 | Clone penuh ada, tanpa pembatasan | Pendaratan tanpa sengaja saja | Pembacaan oleh harness berizin luas |
| 2 | Clone penuh ada, harness dibatasi. Saat ini terdokumentasi hanya Claude Code | Alat berkas pada harness itu | Shell yang disetujui, harness lain |
| 3 | Clone penuh tidak ada pada perangkat, hanya edisi | Semua pembacaan salinan lokal clone penuh pada perangkat itu; bukan pengambilan lewat kredensial Git | Kredensial Git yang mencapai repositori, isi edisi yang mengalir ke penyedia model, dan instruksi berisiko pada materi umum |

Pencegahan pembacaan lokal menuntut clone penuh tidak ada di perangkat itu, atau harness dibatasi ke direktorinya. Kredensial Git yang mencapai repositori tetap dapat mengambilnya kembali. **Sebelum mengandalkan tingkat 3, periksa kredensial perangkat itu:** `git config --get-all credential.helper`, akun Git yang masih masuk, dan kunci yang tersimpan. Pembatasan kredensial per repositori masih hipotesis, jadi jangan diandalkan.

### Yang tidak dilindungi rancangan

1. **Teks tidak menegakkan apa pun.** Penunjuk, stempel, kebijakan, `HARNESS.md`, dan panduan ini hanya mengubah perilaku agen yang membaca dan mematuhinya.
2. **Harness berizin baca luas dapat membuka clone penuh pada disk yang sama,** termasuk `work/`, arsip zip, `docs/`, dan object database.
3. **Pengaturan blokir hanya berlaku sejauh tabel di atas,** dan hanya pada satu harness.
4. **Sesi dari induk bersama menjangkau keduanya.** Tidak ada kontrol yang menahannya.
5. **Clone penuh yang sudah ada tetap memuat semua blob.** Riwayatnya tidak ditulis ulang, dan remote juga tetap memuatnya.
6. **Tingkat 3 hanya menutup pembacaan lokal.** Perangkat tanpa clone penuh yang kredensial Git-nya mencapai repositori dapat mengambilnya kembali.
7. **Isi edisi mengalir ke semua penyedia yang dipakai harness Anda.** Retensi, pelatihan, dan yurisdiksi tidak diperiksa.
8. **Pemindaian tidak menemukan yang polanya tidak kenal,** termasuk nama tanpa gelar dan isi yang maknanya peka tetapi tanpa kata kunci.
9. **Stempel tidak menyertai baris `grep`, pembacaan offset, atau berkas non-Markdown.** Instruksi berisiko tingkat sedang tetap dapat dibaca dan diikuti.
10. **Turunan tidak tercakup:** ringkasan, kutipan pada keluaran, memori harness, transkrip, dan berkas sementara.
11. **Pemilik yang memasang penunjuk ke clone penuh atau mengizinkan induknya tidak dicegah.** Pemeriksaan blok `edition` hanya bekerja bila agen mengikutinya.
12. **Izin berbagi di layanan penyimpanan awan, kredensial di luar repositori, dan konektor harness tidak tercakup.**
13. **Perubahan keadaan tidak terdeteksi otomatis.** Tidak ada hook, jadwal, atau layanan, jadi perubahan izin, penunjuk, atau lokasi tetap senyap.

## 8. Perangkat lain

| Jalur | Status | Catatan |
|---|---|---|
| Salin folder edisi oleh pengguna, lalu periksa dengan `check` atau bandingkan dengan `MANIFEST.csv` edisi | Dapat dipakai sekarang | Tanpa repositori baru. Pembaruan manual |
| Repositori privat kedua khusus edisi | Menunggu konfirmasi terpisah dari pemilik | Tindakan keluar; agen tidak melakukannya |
| Clone penuh di perangkat itu, lalu bangun edisi | Tidak dianjurkan | Membawa clone penuh ke perangkat (tingkat 1), dan pemindaian tidak dapat diulang karena berkas pola lokal tidak dilacak Git |
| Penunjuk ke clone penuh | **Dilarang** | Panduan dan penunjuk hanya menuju edisi umum |

Path dan pemisahnya pada Windows `belum diuji`. Claude Code tidak menerima sebagian besar path jaringan sebagai direktori kerja, jadi edisi perlu berada di disk lokal atau drive yang dipetakan.

## 9. Status uji

Panduan ini terbit sebelum sesi uji harness dijalankan. **Semua harness `belum diuji`.** Keterangan pada bagian 4 dan 7 berasal dari dokumentasi, dan hasil uji dapat mengoreksinya. Status berubah hanya setelah sesi nyata tercatat.

| Harness | Status | Sumber yang dibaca, 2026-10-31 |
|---|---|---|
| Claude Code | `belum diuji` | https://code.claude.com/docs/en/permissions, https://code.claude.com/docs/en/settings-reference, https://code.claude.com/docs/en/permission-modes, https://code.claude.com/docs/en/memory |
| Codex | `belum diuji` | https://learn.chatgpt.com/docs/agent-configuration/agents-md, https://learn.chatgpt.com/docs/cli/reference |
| opencode | `belum diuji` | https://opencode.ai/docs/rules/, https://opencode.ai/docs/permissions/ |
| Kilo Code | `belum diuji` | https://kilo.ai/docs/customize/custom-rules |
| Gemini CLI | `belum diuji` | https://geminicli.com/docs/cli/gemini-md/, https://geminicli.com/docs/reference/commands/ |
| Antigravity CLI | `belum diuji` | https://antigravity.google/docs/cli/gcli-migration |
| Cursor | `belum diuji` | https://cursor.com/docs/context/rules |

## 10. Melepas

Hapus teks penunjuk dari berkas instruksi dan izin direktori yang Anda tambahkan. Bila Anda menyetel pengaturan blokir pada bagian 7, cabut seperti tertulis di sana. Tidak ada sisa pemasangan lain, karena tidak ada yang dipasang. Turunan yang sudah ada, seperti memori harness dan transkrip, tidak ikut terhapus.

Bila edisi dicabut atau ditemukan bocor, lepas penunjuk lebih dulu.

## 11. MCP

Tidak ada server MCP. Stdio berarti subproses per sesi, pendaftaran mengubah konfigurasi harness, dukungan resources berbeda antarharness, dan pembaca berkas polos tidak terbantu.

Peninjauan ulang hanya bila kedua syarat ini benar:

1. Pengguna mengizinkan perubahan konfigurasi harness.
2. Pengguna membutuhkan akses berperan pada satu edisi.

MCP tidak menghapus batas pada bagian 7, karena harness yang sama tetap dapat membuka berkas langsung bila izinnya ada.
