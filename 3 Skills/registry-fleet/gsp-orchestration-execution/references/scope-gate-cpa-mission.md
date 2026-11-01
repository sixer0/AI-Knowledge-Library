# Scope-gate mission frame (CP-A) — preseden misi manual AI, 2026-10-04

Kelas misi: user meminta pola dua-gerbang eksplisit, mis. "First define the scope ...
after i agreed - do deep research until saturation". Riset mendalam DILARANG mulai
sebelum persetujuan user tercatat. Frame ini merangkai gerbang itu ke lane CONTROLLER
tanpa pelonggaran RT-first.

## Urutan sah (terbukti jalan penuh pada misi manual AI)

1. **Kontrak dulu, gerbang ditulis eksplisit.** `docs/<tanggal>_<slug>/CONTRACT.md`
   memuat blok "Gerbang misi" dengan CP-A sebagai gate: "gelombang riset BARU dibuka
   setelah CP-A disetujui user". Fase hilir TIDAK dibuat kartunya di muka.
2. **Fase scope = RT + TA paralel** (OPT-WF O-C; tipe misi bertemplat manual/riset).
   Kartu TA memuat kalimat penahan baku `TA: tunggu 01 di docs/.../identification/
   01_translated.md sebelum finalisasi`. Body kartu TA boleh mencontohkan penafsiran
   tetapi WAJIB dilabel "USULAN, bukan kata user" — RT mewajibkan hal ini di catatan
   sinkronisasinya dan TA menuruti status hipotesis sampai CP-A.
3. **Gerbang RT_BYPASS diukur controller**: 02 final menyitasi 01 (frontmatter
   `source_translated_task` + seksi Source Translation menunjuk berkas yang sama);
   cek grep U+2014/U+00B7 = 0 pada kedua artefak; baca result kartu via
   `hermes kanban show <id> --json`.
4. **Usulan scope ke user lewat kanal chat TUNDUK gerbang naturalisasi**: tulis draf
   penuh ke `_work/cpa_draft_*.md`, jalankan
   `scan_ai_footprint.py <berkas> --channel chat`, baru kirim isi yang sama ke chat.
   Jejak PASS dilaporkan bersama artefak (D-07 kontrak).
5. **Persetujuan = form clarify multi-pertanyaan** (scope umum + butir keputusan
   terpisah seperti level-kedalaman dan cakupan). Jawaban form adalah sumber
   kebenaran; sesuai aturan 14, jawaban di kanal chat menutup entri inbox HQ —
   jangan tinggalkan approval ganda.
6. **Catat vonis user VERBATIM di Decision Log kontrak sebelum kartu riset pertama
   dibuat** (mis. D-05: "Setujui semua default D-1..D-6" + timestamp + kanal).
   Tanpa entri ini, seluruh fase riset tidak sah.

## Mekanika rilis DAG riset (batch, satu giliran)

Skrip Python pemanggil `lad_card.py` via subprocess, SATU run untuk seluruh DAG:
- parse `Created t_xxxxxxxx` dari stdout tiap panggilan untuk mendapat id kartu,
  lalu pakai id itu sebagai `--parents` kartu berikutnya dalam run yang sama —
  tidak ada race window antara create dan link (pitfall late-linked parents);
- `--tenant <MISI>` di semua kartu (gerbang tenant lad_card menolak tanpa ini);
- `--wake-default` per kartu;
- simpan register id ke `_work/<fase>_card_ids.json` untuk fase berikutnya;
- edge HANYA ke hulu data nyata (contoh sah: UJI-LOKAL ber-parent ke kartu desk
  yang melahirkan daftar uji; SYN ber-parent ke semua lajur).

## Board-mover per misi + jebakan delivery WebUI

Pola misi buku 04-10 (dipakai ulang misi manual AI): cron `every 15m` dengan
`monitor_script` = skrip digest deterministik (status kartu + path+ukuran artefak,
TANPA timestamp) — agent hanya bangun saat hash digest berubah; prompt mover berisi
tugas rekonsiliasi (ukur artefak sendiri, bukan percaya summary; resume
partial-handoff via lad_card; gerang buka fase berikutnya; tempel [FASE] ke
PHASE-REPORTS; DILARANG klaim selesai ke user / restart server / menulis naskah).
- **Jebakan**: dari sesi WebUI, `deliver: origin` menghasilkan error
  `unknown platform 'webui'` (preseden watchdog misi polish 30-09, last_delivery_error
  terukur). Buat job lalu langsung `update deliver='local'`; laporan fase tetap
  sampai ke user lewat wake-subscribe papan + controller.
- Template digest: `templates/board-mover-watch.py` (ubah TENANT + DOCS).

## Kartu uji-lokal: ukur host dulu, pisahkan klaim fasilitas

Sebelum melepas kartu "buktikan X di hardware ini", controller MENGUKUR host
(`nvidia-smi`, keberadaan runtime). Bila fasilitas yang diklaim user (mis. studio
4x GPU kelas workstation) BUKAN hardware host kendali (host ini: 1x RTX 5070 Ti),
body kartu WAJIB menuliskan: uji nyata hanya pada host (label `[measured]`), angka
untuk fasilitas user dihitung eksplisit dari spesifikasi resmi vendor + hasil
skala-per-GPU (label `[estimate]` dengan rumus terbuka), dan dilarang mengarang
angka fasilitas. Ini perpanjangan SPK-002 butir truth-fidelity ke jalur bukti lokal.

## Pitfall temuan: TA masih memakai batas lama "maks 2 sejenis"

Body kartu TA misi manual AI tidak menyebut norma konkurensi, dan TA menyusun breakdown
dengan "pekerja paralel maks 2" (aturan lama yang SUDAH digusur norma
03-09B: kap 5 AKTIF per misi, tanpa batas per-jenis; kap host 20). TA mengoreksi
dirinya sendiri di catatan run, tetapi controller harus mencegah dari hulu:
**setiap body kartu TA untuk riset multi-lajur menempelkan satu baris norma
konkurensi yang berlaku** (N1 + 03-09B + kap host), dan Decision Log controller
mencatat pembacaan bila ada deviasi (misi manual AI D-06 melepas 1a-1e serentak,
tepat kap 5).
