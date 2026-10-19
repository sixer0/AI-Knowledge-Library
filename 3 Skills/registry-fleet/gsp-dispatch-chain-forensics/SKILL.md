---
name: gsp-dispatch-chain-forensics
description: Use when auditing delegation handoff or gate verdicts.
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, orchestration, kanban, verification]
    category: gsp
---

# Forensik Rantai Dispatch & Vonis Instrumen

Kelas kerja: memvonis keluhan "hasil kerja tidak kembali ke asignor", membaca papan
kanban.db secara read-only, menginterpretasikan keluaran gerbang fleet
(wave-lock-guard, deleg-watch, wake-scan), dan membuktikan sebuah tambalan benar-benar
hidup sebelum mengklaimnya. Norma kebijakan tetap milik `gsp-orchestration-execution`
(registry fleet; tulis hanya via kanal gsp-skill-manager). Skill ini alat ukurnya.

## Kapan dipakai
- Keluhan serah-terima/handoff ke profil yang salah, PARKED massal, ACK oleh pihak keliru.
- Controller perlu angka basal atau bukti pasca-tambal (distribusi created_by, rasio ACK).
- Sebuah gerbang memvonis FAIL/PASS dan kamu belum yakin vonisnya mengukur kenyataan.
- Klaim "perbaikan sudah terpasang" atas proses yang panjang umur (bridge/gateway/dashboard).

## Resep 1: ukur papan tanpa menyetel kaki di atasnya
Buka `sqlite3.connect("file:<path>?mode=ro", uri=True)`. Peta kolom yang menyesatkan
(ukur 14-10):
- `tasks.created_at` / `started_at` / `completed_at` = EPOCH int (bukan string ISO; filter
  string tanggal menghasilkan nol baris senyap). Konversi `datetime.fromtimestamp`.
- `parents` BUKAN kolom `tasks` = baca dari tabel `task_links(child_id, parent_id)`.
- Cursor langganan = kolom `last_event_id` di `kanban_notify_subs` (bukan cursor_event_id).
- Board nyata hidup di `<HERMES_HOME>/kanban.db`; `<HERMES_HOME>/kanban/kanban.db` bisa
  kosong (jebakan: query "no such table" berarti salah berkas, bukan papan rusak).
- Ruang id `task_comments` dan `task_events` terpisah; bandingkan SELALU lewat waktu.
Alat siap pakai: `scripts/rantai_ukur.py --tenant <KODE>` (distribusi created_by, done,
PARKED, pembanding basal).

## Resep 2: vonis PARKED/ACK jangan dipindah ke masa lalu
`gsp_deleg_watch.py ack-post <TID>` MENOLAK penulis non-owner kecuali `--proxy`. Kartu
yang lahir sebelum tambalan created_by punya owner kolom 'user' selamanya: jalur sah =
controller bayar `ack-post --by default --proxy`, dan itu perilaku benar, bukan cacat.
Vonis sehat per kartu: ACK ber-author == created_by = owner sah; PROXY-ACK = warisan
pra-tambal; MISMATCH tanpa tag = cacat protokol. Jangan menormalisasi massal created_by
kartu lama.

## Resep 3: klaim 'tambalan hidup' wajib adu umur proses
Patch di disk TIDAK berarti berlaku pada proses panjang-umur. Prosedur: baca
`CreationDate` proses (PowerShell `Get-CimInstance Win32_Process`) dan bandingkan dengan
mtime berkas / waktu commit. Proses lebih tua dari tambal = bawa kode lama di memori.
Kelas proses: CLI fresh-per-panggilan (langsung berlaku), bridge/gateway/dashboard
long-lived (butuh restart = wewenang user; jangan pernah me-restart sendiri, dan jangan
vonis PASS jalur ini dari kode disk saja - labeli NEEDS_REVIEW + kartu resume
needs_input yang menunggu unblock pasca-restart).
Jebakan kembar pohon: runtime CLI hidup di `<HERMES_HOME>/hermes-agent` yang merupakan
repo TERPISAH dari pohon pengembangan (mis. `gsp-agent/engine`). Commit di pohon dev
tidak mengubah perilaku sampai diport ke pohon runtime; cek dua-duanya sebelum klaim,
dan grep titik tambal spesifik (mis. baris default argparse) di pohon runtime.

## Resep 4: vonis instrumen bukan kenyataan (tiga mode kegagalan)
1. **FAIL literal**: gerbang yang mencocok TOKEN literal (mis. penanda bypass rantai)
   akan FAIL bila artefak HANYA MEMBAHAS token itu dalam prosa (termasuk kalimat
   penyangkalan). Obat: tulis ulang artefak tanpa string literal token (parafrase);
   JANGAN melonggarkan gerbangnya. Konsekuensi desain: artefak identifikasi tidak boleh
   mengutip literal token penjaga yang membacanya.
2. **PASS hampa**: `VERDICT: PASS` dengan baris "0 kartu terparse" = gerbang tidak
   mengukur apa pun. Penyebab terukur: parser menuntut kolom terakhir header persis
   'LOCK' (varian 'PERAN+LOCK' tak cocok) dan split sel pada pipe tanpa mengenali pipe
   ter-escape. Obat controller: verifikasi independen partisi LOCK dengan mem-parse
   body kartu terbit (regex bebas, bandingkan lintas kartu DAN vs kartu hidup misi lain),
   tempel hasilnya di kontrak. Jangan klaim lock-guard PASS atas 0 kartu sebagai hijau.
3. **Negatif senyap**: query filter tanggal string pada kolom epoch = 0 baris tanpa
   error. Selalu cetak total mentah berdampingan dengan hasil terfilter.

## Resep 5: kartu buku-kerja controller jangan dibiarkan 'ready' ber-assignee
Kartu kontrak ber-assignee profil yang diklaim dispatcher (status ready) akan di-spawn
menjadi SESI KEMBAR yang mengerjakan misi yang sama paralel dengan controller: menimpa
blueprint, menerbitkan kartu, menutup kontrak. Preseden ukur 14-10 (sesi src=kanban
menimpa 02_structured versi TA, sha berubah di tengah giliran). Pencegahan: kartu kerja
sendiri tanpa assignee (dispatcher tidak mengklaimnya) atau langsung dikerjakan sampai
done. Pemulihan bila terlanjur: JANGAN batalkan keluaran sesi kembar secara refleks -
vonis rekonsiliasi = ukur ulang independen semua gerbang atas keluarannya; sah = adopt
sebagai keadaan kanonis (nol duplikasi, nol kerja ulang), catat insiden di kontrak
(kelas T5-lingkungan), koreksi cacat kecil via komentar kartu, bukan suntingan diam-diam.

## Pitfall mekanik (terukur, jalan di sesi ini)
- Penanda `HERMES_DELEGATED_CHILD_CONTEXT` menetes ke shell terminal controller setelah
  batch subagen; semua `hermes kanban` CLI menolak jalan ("delegate_task child contexts
  cannot mutate"). Jalur sah: `unset HERMES_DELEGATED_CHILD_CONTEXT` prefix tiap perintah
  papan.
- `hermes kanban block <id> --kind X "reason ber-spasi"` menolak pada build ini; urutan
  yang diterima: reason positional dulu, opsi `--kind` belakangan (atau tanpa --kind).
- `lad_card.py` menolak `--json`; output sukses baris "Created t_xxxx".
- Notifikasi batch async mendarat sebelum komentar/hasil pekerja terbaca papan: selalu
  ukur ulang DB/komentar pada giliran setelahnya, jangan kutip ringkasan notifikasi.

## Batas klaim
Angka skill ini adalah cetakan alat pada giliran ukur. Distribusi created_by basal
(170/180 'user' era 11-13/10) sudah DIAMBIL oleh tambal engine (default None +
_profile_author diperketat, port runtime 14-10): kartu baru dari shell berprofil mencatat
profilnya; 'user' kini hanya untuk shell tanpa profil dan kartu warisan. Jangan kutip
basal sebagai keadaan hidup tanpa re-ukur `scripts/rantai_ukur.py`.
