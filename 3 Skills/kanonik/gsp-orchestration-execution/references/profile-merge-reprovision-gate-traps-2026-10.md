# Reprovisioning kartu yatim pasca-arsip profil + jebakan gerbang (misi manual rev B, 10-10)

Preseden terukur satu giliran: user mengarsipkan profil pekerja (PROF-MERGE-1010) SAAT run berjalan; enam kartu misi crash/gave_up serentak dengan notifikasi `crashed (worker exited)`. Semua bukan kegagalan kerja.

## Tangga penanganan kartu yatim (terbukti menutup 14 kartu satu sweep)

1. **Traceroot dulu, aksi kemudian.** `kanban runs <id>` + `kanban log`: crash <30 dtk tanpa tool call = sebab provider (cek 402); crash SETELAH artefak = klasifikasi crash-pasca-artefak, vonis dari disk; workspace kosong total = nol modal, run baru mulai bersih.
2. **Sensus yatim:** `kanban list --tenant <M>` sapu TANPA head-cut; bandingkan tiap assignee vs `ls $LOCALAPPDATA/hermes/profiles` (arsip bisa di luar folder profil — cek `assignees` juga). Kartu di assignee arsip = yatim.
3. **Reassign ke worker hidup** (`hermes kanban reassign <id> gsp-worker`) + **komentar pointer berkas peran** di SETIAP kartu pindah: `workspace/roles/<profil-lama>.md` dibaca penuh sebelum kerja; identitas, standar, dan skill peran lama berlaku lewat berkas itu. Persona tidak hilang bersama profil.
4. **Unblock dengan alasan traceroot tercatat** (`--reason` ber-spasi diterima pada build 10-10; fallback positional).

## Jebakan provisioning worker (kapabilitas sesi != config profil)

- Worker pengganti bisa memblokir jujur: `block --kind capability` = sesi tanpa terminal/execute_code/vision padahal `config.yaml` profilnya mencantumkan `terminal`. Penyebab dua lapis: (a) **waktu**: dispatcher spawn sesi dengan config SAAT ITU — run yang lahir sebelum tambalan config tetap buta walau config kini lengkap (buktikan: bandingkan mtime config vs `started` run; bila run lebih tua dari patch, blokir sah, cukup unblock untuk sesi baru); (b) **cakupan**: `platform_toolsets.cli` profil hanya memuat subset — tambal dengan nama toolset yang VALID.
- **Gerbang sebelum menulis toolset:** validasi nama terhadap kernel, jangan karang: `python -c "from toolsets import get_toolset_names; ..."` (dari checkout hermes-agent) — `code_execution` dan `vision` sah sebagai entri list (bukan alias `browser`/`delegation` yang ditolak loader dengan peringatan).
- Run berikutnya sesudah patch = sesi toolset lengkap; konfirmasi dari progres nyata di workspace (file baru ber-mtime pasca-patch), bukan dari klaim.

## Deadlock gerbang: kartu reparasi ber-parent kartu blocked

Kartu baru dibuat dengan `parents=[kartu-BLOCKED]` tetap `todo` selamanya (parent tak akan `done` sebelum reparasi selesai; reparasi tak akan `ready` sebelum parent done). Preseden FG5T vs MERGE-FIGUR2 10-10: **lepas edge** (`kanban unlink <blocked> <child>`) agar child jadi `ready`; relasi resmi ditulis di komentar kedua kartu + kontrak misi. Kebalikan dari pitfall late-linked-parents: di sana edge susulan terlalu lambat untuk MENGHENTIKAN; di sini edge awal justru terlalu efektif menghentikan. Aturan: edge `parents` hanya untuk hulu DATA yang akan selesai; gerbang-tutup-dari-kartu-blocked ditegakkan lewat komentar/kontrak, bukan edge.

## Replay guard pasca-notifikasi ganda

Notifikasi completed/blocked bisa masuk ulang setelah vonis tertayang. Prosedur 30 detik: ukur ulang pin artefak kunci (sha16) + mtime + jumlah komentar vonis (`grep -c` penanda vonis). Byte == pin vonis DAN vonis sudah tayang = REPLAY, nol aksi papan, laporkan satu baris. Jangan pernah mengulang vonis atau membuat kartu dari replay.

## Register pin proteksi: baca dari VONIS TERBARU

Sensus "berkas luar cakupan bergeser" memakai register pin cetakan pertama = positif-palsu bila berkas sudah melewati kartu FIX/revisi (preseden bab-07/08 Rev B: pin era merah W2 vs byte FIX-W2, tuduhan drift gugur). Pin proteksi wajib dibaca dari vonis terbaru per berkas; idealnya register hidup dipelihara per klaster di kontrak dan dikutip ulang saat menuduh.
