# Kebijakan DAG Sejati: Edge Data Asli, Konkurensi lewat Kapasitas Dispatcher

Terverifikasi 02-09-2026 (misi EXPO-INTEL-2026 + EXPO-OPT-P3). Berlaku untuk
SETIAP registrasi kartu worker di board kanban. Menggantikan pola lama
"parents antar-wave penuh" yang dirujuk `wave-dispatch-and-resume.md` dan
`wave-registration-large-fanout.md` versi sebelum 02-09 sore.

## 1. Masalah pada pola wave penuh (bukti EXPO26)

Pola lama: kartu wave N+1 diberi SEMUA id kartu wave N sebagai parents.
Efek samping: satu kartu lambat (straggler) menahan SELURUH gelombang berikut
meskipun tidak ada hubungan data. Kejadian nyata: C07 (50 menit) menahan
promosi 4 kartu wave 4 selama 23 menit (D-09 contract EXPO26). Idle kumulatif
per misi skala EXPO: 15-25 menit.

## 2. Aturan kebijakan (WAJIB)

### D-1: Edge = kebutuhan data, bukan penjadwalan

Satu-satunya alasan kartu B ber-parent A adalah: A menghasilkan artefak yang
DIBACA B. Uji diri sebelum memasang edge: "kalau A gagal total, apakah B tetap
bisa dikerjakan dengan bahan lain?" Kalau ya, edge itu semu -> lepas
(`hermes kanban unlink <parent> <child>`). Kartu pengumpul (sumbernya internet,
bukan kartu lain) hanya ber-parent pada gerbang hulu data yang benar
(kartu blueprint/TA atau prasyarat artefak bersama), BUKAN pada sesama
pengumpul.

### D-2: Konkurensi ditegakkan dispatcher, bukan edge semu

Fakta mekanisme dispatcher gateway (dibaca dari kode engine
`hermes_cli/kanban_db.py` fungsi dispatch, audit 02-09):

- Kartu `ready` diurut klaim dengan `ORDER BY priority DESC, created_at ASC`.
- Batas jumlah worker yang hidup ditegakkan HANYA oleh tiga knob config
  `kanban.*`: `max_spawn` (kap total per board), `max_in_progress` (kap total
  lintas board), `max_in_progress_per_profile` (kap per assignee; kartu yang
  melewati dicatat `skipped_per_profile_capped`, tidak hilang).
- PRIORITAS TIDAK MEMBATASI JUMLAH. Prioritas hanya urutan antre; saat ada
  slot, kartu berpriority lebih tinggi diambil lebih dulu. Menaruh "batas
  total / tanpa batas per jenis (norma 03-09)" sebagai perbedaan angka prioritas saja = tidak menegakkan
  apa pun.
- Guard memori otomatis ada (tekanan elevated = maks 1 spawn/tick, critical =
  0) tapi bukan pengganti kap eksplisit.

Konsekuensi kebijakan: kalau misi butuh kap konkurensi (default fleet: 5 per misi,
tanpa batas per jenis, norma user 03-09B; kap host 20 = kapasitas server), controller WAJIB memastikan knob terpasang sebelum gelombang
siap jalan. Saat audit EXPO-OPT 02-09 (norma lama 4/2), `kanban.max_spawn` dan
`max_in_progress_per_profile` KOSONG di config home maupun profil controller,
jadi kap lama selama itu dijaga HANYA oleh edge wave semu. Dua jalur sah
(putusan controller, catat di Decision Log):

- Jalur A (per-misi): dispatcher manual `hermes kanban dispatch --max 5`
  dijalankan controller dengan kartu infra/ops + bukti, atau dispatcher
  gateway dibiarkan jalan dan kap per-tick dijaga lewat `--max` saat controller
  memicu dispatch. Prioritas kartu mengatur URUTAN antre dalam kap itu.
- Jalur B (permanen, wewenang user): set `kanban.max_in_progress: 20` di config (kapasitas server, user 03-09B)
  (`max_in_progress_per_profile` tidak dipakai lagi karena norma 03-09 menghapus
  batas per jenis), restart gateway milik
  user. Controller dilarang restart layanan (aturan user 31-08).

Tanpa salah satu jalur, D-1 tetap dijalankan dan kelebihan worker yang ikut
spawn dilaporkan sebagai temuan (bukan diam-diam kembali ke edge semu).

### D-3: Straggler tidak menahan cabang bebas

Desain DAG yang benar membuat jalur kritis terlihat: kartu hilir hanya
ber-parent pada kartu yang artefaknya benar-benar dibacanya. Merge-card
(dedup/konsolidasi) boleh dan memang harus ber-parent banyak (fan-in nyata),
tapi pengumpul paralel tidak boleh berantai. Rantai resume partial-handoff
(`parents=[kartu asal]`) tetap sah: itu edge data (SISA_KERJA + catatan parent).

### D-4: Registrasi datar + audit, bukan registrasi bergelombang

Daftarkan SEMUA kartu misi sekaligus (datar, tanpa stagger waktu) dengan edge
D-1 + prioritas bernada (mis. hulu=3, pengumpul=2, hilir=1) untuk urutan antre.
Registrasi datar menghilangkan kelas bug "kartu ter-claim saat create tanpa
edge" karena semua edge sudah terpasang saat audit, dan promosi otomatis DAG
menjadwalkan sisanya. Audit edge wajib sesudah register (lihat §3 rujukan lama
- baca field `parents` LEVEL ATAS JSON `show --json`).

### D-5: Jembatan masa transisi (kap dispatcher belum terpasang)

Selama Jalur A/B belum aktif di suatu board, kalau controller tetap butuh
pagar sementara, pakai SATU kartu gerbang wave (bukan edge antar-sesama
pengumpul): satu kartu penampung per-wave yang dibuat controller dan ditutup
done oleh controller saat wave berikutnya boleh jalan. Ini lebih murah dari
edge penuh karena straggler hanya menahan satu gerbang, dan cabang lain yang
tidak menunggu gerbang itu tetap jalan. Tandai sebagai utang teknis di
Decision Log dengan target penghapusan saat kap dispatcher aktif.

## 3. Verifikasi perubahan ini (red-green 02-09)

Smoke board default 02-09 (kartu uji tanpa assignee = non-spawnable, aman;
id: S1 t_0c8af9db, S2 t_317e8fdc, S3 t_f966c5f7):
- `link S1 -> S2`: S2 turun `ready -> todo` (edge menahan promosi); S1 dan S3
  tetap `ready`.
- `unlink S1 -> S2`: S2 kembali `ready` serentak dengan S3 (cabang bebas tidak
  saling menahan).
- Kartu uji diarsipkan (`archive`) setelah hasil dibaca.

## 4. Batas klaim

Kebijakan ini perilaku orkestrator, nol perubahan kode engine. Kap dispatcher
bersifat config; setelah patch ini, klaim "kap 4/2 aktif" hanya sah bila knob
atau jalur A terbukti terpasang (baca-ulang config / output dispatch), bukan
diasumsikan.
