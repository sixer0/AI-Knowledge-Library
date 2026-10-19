---
name: gsp-limit-aware-delegation
description: "Kebijakan delegasi sadar-limit (LAD): setiap kartu delegasi memuat blok LIMIT dengan anggaran nyata agen target; worker menutup jujur dengan partial-handoff di ambang; bentuk delegasi dipilih lewat estimasi E vs 0.5 x cap. Muat saat membuat/menerima kartu delegasi atau merencanakan bentuk dispatch."
version: 1.5.0
author: GSP (PT. Gemilang Satria Perkasa)
metadata:
  hermes:
    category: orchestration
    tags: [gsp, orchestration, delegation, limit, kanban]
---

# Limit-Aware Delegation (LAD)

Kebijakan fleet keputusan user 02-09-2026. Mengikat untuk SETIAP kartu delegasi
ber-assignee profil Hermes (kartu pribadi tanpa assignee bebas). Tiga pilar:
hulu memberi angka (blok LIMIT), hilir menutup jujur (partial-handoff),
orkestrator menutup loop (kartu lanjutan resume, bukan restart).

## Ambang sadar-limit

| Nama | Rumus | Cap 150 | Cap 500 | Perilaku wajib |
|---|---|---|---|---|
| AMBANG-A (cek jalur) | sisa iterasi <= 50% ATAU jalan >= 15 menit | sisa <= 75 | sisa <= 250 | Stop perluasan lingkup; ambil keputusan sadar: lanjut selesai atau siapkan checkpoint. Tidak wajib lapor. |
| AMBANG-B (tutup jujur) | sisa iterasi <= 25% ATAU sisa waktu <= 8 menit | sisa <= 37 | sisa <= 125 | STOP kerja baru; tulis laporan parsial enam bidang; tutup STATUS: partial-handoff. |

Waktu: plafon efektif adalah kolom `tasks.max_runtime_seconds` per kartu yang
ditegakkan dispatcher; bawaan lad_card.py 3600 detik sejak ratifikasi
AUDIT-DURASI-1010 R1 (kartu t_5e44adad, 10-10) = anggaran profil
run_budget_seconds 2700 + grace; kartu berat boleh minta lebih via
--max-runtime. Jalur lama bridge.mjs 30 menit (grace 10) tidak lagi menjadi
pembunuh utama pada jalur dispatcher. Worker TIDAK punya alat membaca sisa
iterasi miliknya (engine sengaja tanpa peringatan antara, isu #7915);
satu-satunya sumber angka adalah blok LIMIT di kartu, karena itu angka ditulis
absolut, bukan persen.

## Blok LIMIT standar (ditempel OTOMATIS oleh scripts/lad_card.py)

Placeholder diisi dari config profil target saat kartu dibuat (fallback 500
hanya bila profil tak terbaca, dengan peringatan tercetak):

    LIMIT-AWARE (wajib dibaca sebelum mulai; kebijakan LAD 02-09; tutup jujur = selesai sesuai kontrak):
    - ANGGARAN: {cap} iterasi tool (agent.max_turns profil) + {menit} menit plafon run (checkpoint wajib di sepertiga kedua).
    - AMBANG-A (cek jalur): sisa <= {setengah} iterasi ATAU jalan >= {sepertiga} menit -> stop perluasan lingkup; putuskan sadar: lanjut selesai atau siapkan checkpoint.
    - AMBANG-B (tutup jujur): sisa <= {seperempat} iterasi ATAU sisa <= {sepersepuluh} menit -> STOP kerja baru; tulis laporan parsial enam bidang sebagai komentar lengkap, tempel ringkasannya di result, tutup dengan STATUS: partial-handoff.
    - FORMAT LAPORAN: STATUS / ALASAN_LIMIT / SELESAI (path+ukuran nyata di disk) / SISA_KERJA (butir + estimasi iterasi) / BLOCKER / KARTU_LANJUTAN_SARAN.
    - HEMAT: mekanik per-item lewat SATU skrip execute_code (di-refund dari anggaran); gagal identik 2x = ganti pendekatan; file besar dibaca pakai grep/bagian.
    - Parsial berformat BUKAN kegagalan; crash/gave_up tanpa laporan = cacat. Orkestrator membuat kartu lanjutan dari SISA_KERJA (parents kartu ini, maksimal mata ke-3).

setengah = floor(cap/2); seperempat = floor(cap/4). Untuk cap 150: 75 dan 37.
menit = max_runtime // 60 (bawaan 3600 -> 60); sepertiga = menit // 3;
sepersepuluh = menit // 10 — blok LIMIT kini PARAMETRIK mengikuti --max-runtime
sejak ratifikasi AUDIT-DURASI-1010 R1 (10-10), bukan lagi konstanta 30/15/8.

## Bentuk delegasi (estimasi sebelum dispatch)

E = B_baca + (jumlah_item x biaya_per_item) + B_tulis + B_verifikasi, lalu
Buffer = 25% subtotal. Komponen diambil dari daftar nyata dan tabel kalibrasi
(biaya tipikal: RT 15-45; TA 25-50; SM evaluasi 60-120; propagasi fleet-scale
>150 wajib pecah; verifier multi-check fleet-scale wajib dipecah ke countersign
ringan). Tabel kalibrasi diperbarui setiap misi selesai; yang normatif adalah
kewajiban memakai tabel + jejak, bukan nilai spesifiknya.

Estimasi E dihitung dalam DUA satuan, iterasi DAN menit waktu run, lalu bentuk
dipilih dari yang lebih mengikat: E_eff = max(E_iter, E_menit). Untuk kartu riset
pencarian web (kumpul baris bersumber), pakai konstanta laju nyata di
`references/lad-calibration-2026-09.md` (1 baris tervalidasi = 2-4 query;
E = baris x 3 query x 1,5 iterasi + 20 overhead), bukan asumsi 1 query/baris.
Bukti EXPO26 (02-09, 19 run): kendala pengikat kartu pengumpul adalah waktu
bridge 30 menit, bukan anggaran iterasi (empat partial-handoff karena waktu,
nol karena iterasi; satu run melapor cuma memakai sekitar 35 dari cap 150).

| Kode | Kondisi | Bentuk |
|---|---|---|
| R-1 | E <= 0.5 x cap | SATU kartu (jalur normal) |
| R-2 | E > 0.5 x cap DAN output satu artefak koheren | Rantai multi-turn checkpoint-resume; mata = ceil(E / (0.5 x cap)); maksimum 3 mata, mata ke-4 eskalasi manusia |
| R-3 | E > 0.5 x cap DAN item saling bebas | PARALEL cards; tiap kartu <= 0.5 x cap; concurrency maks 5 AKTIF (running) per misi tanpa batas per jenis (norma 03-09B + norma gelombang N1 08-09: kap menghitung kartu running, BUKAN pembuatan batch; sumber normatif: `gsp-orchestration-execution` seksi "Norma gelombang N1"); path output unik |

Ambang 0.5 x cap: worker butuh sekitar 25% anggaran untuk menutup jujur plus
ruang koreksi; menarget cap penuh berarti kartu dirancang mencapai batas maksimum.
Pengecualian: kerja interaktif singkat (chat, tanya-jawab, perbaikan kecil satu
berkas) tidak butuh estimasi; aturan berlaku untuk KARTU DELEGASI.

## Aturan satisfiability kartu tulis/sunting (SAT-1010, ratifikasi t_5e44adad 10-10)

<!-- [SATISFIABILITY-1010] -->
Kartu DELEGASI jenis tulis/sunting berkas (editorial, parafrase, reparasi
figur/dokumen) dengan estimasi E > 40 iterasi WAJIB memenuhi tiga syarat
sebelum dilepas; tanpa salah satunya kartu cacat dan verifier menolak:

1. PECAH-LOKUS: kerja diurai menjadi maksimum 50 lokus kerja per kartu. Lokus
   = satuan sasaran bernama tunggal (berkas#seksi, id figur, rentang baris).
   Bila jumlah lokus melebihi 50, kartu dipecah (rantai/paralel sesuai R-2/R-3),
   bukan plafon dilanggar.
2. PETA-LOKUS: body kartu menyertakan blok `peta-lokus` JSON berisi daftar
   `{id, target, op, est_iter}` — pekerja mengerjakan lokus sesuai peta, boleh
   berhenti di tengah peta dengan partial-handoff yang menyebut lokus terakhir
   selesai, dilarang menulis ulang cakupan dari kepala.
3. LARANGAN-BACA-PENUH: body memuat klausul eksplisit bahwa berkas besar dibaca
   hanya per lokus (grep/bagian/read offset), DILARANG baca-penuh ke konteks.

Dasar terukur (AUDIT-DURASI-1010 §5 R1+R4, misi RAFIF-MF-1009, ukur ulang
kartu t_5e44adad atas DB kanban 10-10): pola menang scoped-lokus FIX-FIGUR2-E5T
(complete) dan FIX-FINAL (complete) versus pola kalah E5S (closed-partial),
E5a (partial stand-down), EDIT-GAYA-G (sesi mati konteks-176k, nol suntingan).
Aturan ini komplementer terhadap R-1/R-2/R-3: sumbu SAT mengukur saturasi
konteks, sumbu R mengukur anggaran waktu/iterasi; kartu wajib lolos keduanya.
<!-- [/SATISFIABILITY-1010] -->

## Penutupan parsial (partial-handoff)

Enam bidang bernama, komentar penuh + result ringkas, tutup dengan
kanban_complete + metadata.partial_handoff=true:

    STATUS: partial-handoff
    ALASAN_LIMIT: iterasi (pakai X dari N, sisa Y) | waktu (menit ke-M dari 30)
    SELESAI: <artefak nyata di disk: path + ukuran/baris + sha256 bila ada>
    SISA_KERJA: <butir tersisa + estimasi iterasi masing-masing>
    BLOCKER: <hambatan atau "tidak ada">
    KARTU_LANJUTAN_SARAN: <judul + assignee + estimasi cap, boleh kosong>

SELESAI wajib merujuk artefak yang benar-benar ada di disk. SISA_KERJA harus
terukur. Parsial berformat tidak menaikkan pencacah kegagalan. kanban_block
hanya untuk sisa kerja yang menunggu keputusan manusia.

## Tindak lanjut orkestrator

Dari setiap partial-handoff, buat kartu lanjutan: (1) body memuat SELESAI dan
SISA_KERJA verbatim lalu instruksi mulai dari butir pertama SISA_KERJA (resume,
bukan restart); (2) parents=[kartu asal] sejak pembuatan, bukan ditautkan
belakangan; (3) blok LIMIT diulang dengan cap sama plus progres awal;
(4) judul berpola sufiks (lanjutan N/M); maksimum 3 mata rantai.

## Guard dan audit

- Semua kartu delegasi dibuat lewat scripts/lad_card.py (menempel blok dari
  config target, memasang --max-runtime bawaan 3600 sejak ratifikasi
  AUDIT-DURASI-1010 R1 10-10; lama 1800, menolak tanpa jejak ESTIMASI
  kecuali flag --interaktif).
- Kontrak wake (kebijakan WK-ORCH-0911): --wake-default mendaftarkan
  notify+wake ke kanal rumah profil aktif dan men-stempel langganan
  'default' secara TERKUNCI (perlindungan D-WKO-1); --wake-chat-id WAJIB
  disertai --wake-notifier-profile=<profil gateway penghost> atau kena WARN
  keras dan wake bisa HILANG SENYAP.
- Gerbang tenant (TA-D8 + amandemen D-05 09-09): lad_card.py menolak kartu
  tanpa tenant dengan exit 2 SEBELUM cabang --dry-run. Jalan sah: (1) --tenant
  MISI-XXXX; (2) --parents kartu bertenant -> tenant diwarisi dari parent
  pertama yang punya tenant (SQL read-only ke task_links/tasks, baris "tenant
  diwarisi dari <id>") sehingga cron watchdog yang membuat kartu resume tanpa
  menyebut tenant tetap jalan; (3) opt-out sadar --no-mission dengan WARN.
  --tenant eksplisit menang atas warisan; kombinasi --tenant + --no-mission
  ditolak. Tenant valid diteruskan sebagai ["--tenant", ...] ke `hermes kanban
  create` dan tercetak di output dry-run; bentuk tidak lazim (pola
  ^[A-Z][A-Z0-9]{1,15}-\d{4}$) hanya WARN.
- Audit deterministik: scripts/lad_audit.py (lihat spesifikasi di kontrak misi).
- Probe concurrency (D-LAD-05): jalankan scripts/lad_audit.py --probe
  [--fixture F.json] [--window-min 15] sebelum gelombang paralel dilepas, dan
  baca keluarannya berupa baris `PROBE: SEHAT|TEKANAN|UNKNOWN` beserta angka
  mentah (kedalaman antrean HQ queued+approved+running serta rasio
  failed-timeout jendela 15 menit) dengan exit 0=SEHAT, 1=TEKANAN, 2=UNKNOWN.
  Konsekuensinya nilai gelombang boleh naik di atas statis 5 per misi tanpa
  batas per jenis (norma 03-09B) hanya saat SEHAT, sedangkan TEKANAN maupun UNKNOWN memaksa statis itu
  karena probe gagal membuktikan jalur dispatch lapang; secret
  INTERNAL_API_SECRET selalu dibaca dari env/config tanpa pernah di-hardcode.
  Fixture uji sintetis tersimpan di scripts/tests/, misalnya fixture_74x.json
  replika fan-out 74x tanggal 01-09 yang wajib terbaca TEKANAN, dan ini
  sekadar replika pola masa lalu sehingga bukan pengganti pengukuran live.
- Batas klaim: kepatuhan perilaku bersifat prosedural-terverifikasi; jangan
  pernah mengklaim fleet-wide nol.

## Riwayat
<!-- [AUDIT-DURASI-1010] -->
1.5.0 (10-10-2026, kartu t_5e44adad ratifikasi gsp-skill-manager atas eksekusi controller AUDIT-DURASI-1010 R1+R4, perintah user 10-10): (a) RATIFIKASI UBAHAN TERPASANG — scripts/lad_card.py DEFAULT_MAX_RUNTIME 1800->3600 + blok LIMIT parametrik mengikuti --max-runtime; dasar ukur ulang DB kanban 10-10: run timed_out seragam @30,2 menit (median populasi timed_out fleet), plafon efektif = kolom tasks.max_runtime_seconds yang ditegakkan dispatcher sementara anggaran profil run_budget_seconds=2700 terpasang di 44 profil tak pernah tercapai; gerbang eksekusi lolos: dry-run default merender 60/20/6 menit dan --max-runtime 5400 merender 90/30/9 (rc=0). SKILL.md diselaraskan dengan kode (prosa lama menyebut bridge 30 menit dan konstanta 30/15/8 yang sudah tidak dirender); help text --max-runtime ikut dikoreksi dari 'default 1800' menjadi nilai aktual. (b) PASANG aturan satisfiability SAT-1010 (blok [SATISFIABILITY-1010]): kartu tulis/sunting E>40 wajib pecah-lokus <=50 + peta-lokus JSON + larangan-baca-penuh; dasar pola menang FIX-FIGUR2-E5T/FIX-FINAL vs kalah E5S/E5a/EDIT-GAYA-G (ukur ulang hasil kartu DB 10-10). Rollback: kembalikan DEFAULT_MAX_RUNTIME="1800", hapus blok [SATISFIABILITY-1010] dan selaraskan kembali prosa; basal pra-edit sha256[:16] SKILL.md be474786d24daed2, lad_card.py 59f6fd770fa720ba (backup C:/Users/TRIAL/AppData/Local/Temp/proposal1010_backup_20261010_133032/).
<!-- [/AUDIT-DURASI-1010] -->
