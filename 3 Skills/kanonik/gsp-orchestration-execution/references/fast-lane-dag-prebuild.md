# SOP Fast-Lane DAG Pre-Built (opt-in, uji mulai 08-09; norma N1 putusan user 08-09)

Status kebijakan: OPT-IN per misi selama 1 minggu uji (mulai 08-09, misi OPT-WF-0907 D-07).
Naik menjadi DEFAULT fleet hanya lewat Decision Log controller setelah kriteria jendela uji
tercapai (lihat bagian "Aturan jendela uji"). Sumber normatif norma gelombang: seksi
"Norma gelombang N1" di SKILL.md skill ini.

## Definisi kunci (Norma N1, putusan user 08-09)

- "Gelombang" = satuan RILIS/PROMOSI serentak kartu, BUKAN satuan pembuatan kartu.
- Pembuatan batch >5 kartu dalam satu giliran SAH, selama kartu AKTIF (running) per misi <=5.
- Promosi tetap digerbangi `parents`: edge hanya ke hulu data nyata (kartu yang outputnya
  dibaca); batas konkurensi ditegakkan lewat prioritas + kapasitas dispatcher, bukan edge semu
  urutan (pitfall "Edge semu antar-gelombang", kejadian EXPO-INTEL 02-09).
- Kap host `kanban.max_in_progress: 20` TETAP (jendela ukur OPT-WF-C4: hingga 4 misi berkap-5).
- Syarat audit per misi: controller MELAPOR jumlah batch kartu dibuat dan puncak running per
  misi, diukur dari event papan/DB (`hermes kanban list --json`, tabel events), bukan narasi.

## SOP langkah 1-7

1. Blueprint final (keluaran TA) dibaca controller; seluruh langkah misi + dependensi data
   nyata sudah eksplisit sebelum satu kartu pun dibuat.
2. Deklarasi opt-in fast-lane dicatat di kontrak misi (baris Decision Log: misi, tanggal,
   pola fast-lane, penanggung jawab SC-G). Tanpa deklarasi = tidak ikut jendela uji.
3. Bangun SELURUH DAG kartu sekali jalan: satu batch create berisi semua kartu fase berikutnya
   dengan `parents=[...]` terisi pada panggilan `kanban_create` itu juga (late-link TIDAK
   menahan promosi; pitfall NAT-S23/S24). CLI setara: `lad_card.py --parents id1,id2,...`.
4. Prioritas menaik per fase (fase hulu prioritas lebih tinggi) supaya antrean dispatcher
   menembus sesuai urutan meski semua kartu lahir `ready` bersamaan.
5. Trace-first: setiap kartu punya body kontrak (output + verify + blok LIMIT-AWARE via
   `lad_card.py`) dan rujukan blueprint; dispatch HQ tercatat sebagai AgentRequest sebelum
   worker diharapkan bergerak.
6. Watcher berjalan: probe `lad_audit.py --probe` sebelum melepas gelombang + pemantau
   puncak-running; jika dispatcher menembus kap aktif, perketat dengan edge HANYA pada kartu
   ke-6 dst. (bukan pada semua kartu).
7. Transisi fase nol-tunggu: begitu kartu hulu `done`, kernel mempromosikan hilir otomatis;
   controller tidak lagi membuat kartu per fase (target bukti awal: transisi 0,5 menit pada
   misi sosmed 0907 vs dasar idle chain 25,2 menit, BASELINE OPT-WF-0907).

## Checklist pra-dispatch (WAJIB, satu giliran sebelum batch create)

```text
[ ] Dispatcher hidup (watchdog/gateway gsp-* aktif; cek proses/health, bukan asumsi)
[ ] Kap host vs beban: estimasi running serentak lintas misi aktif + batch ini <= 20
[ ] Puncak running per misi <= 5 (norma N1; tanpa batas per jenis agen, norma 03-09B)
[ ] Assignee nyata: tiap nama assignee ada foldernya di %LOCALAPPDATA%/hermes/profiles/
    (atau pakai lad_card.py yang menolak nama tak dikenal)
[ ] parents=[...] terisi pada panggilan create itu juga (hanya edge hulu data nyata)
[ ] Trace-first: body kontrak + blok LIMIT-AWARE + jejak ESTIMASI pada tiap kartu
[ ] Watcher/probe siap: lad_audit.py --probe keluaran SEHAT (TEKANAN/UNKNOWN = tahan,
    pakai statis 5 dan evaluasi ulang)
[ ] Anti-kembar: list --json filter judul batch 60 menit terakhir sebelum create
[ ] Deklarasi opt-in + pemilik audit puncak-running tercatat di kontrak misi
```

## Aturan jendela uji (naik-default Q2)

- Jendela: 7 hari kalender sejak 08-09; misi ikut uji hanya bila deklarasinya ada (langkah 2).
- Kriteria naik DEFAULT (dua-duanya wajib, diukur harness OPT-WF C4 `optwf_measure.py`):
  (a) rasio kartu pre-built (kartu dibuat sebelum fase hulu selesai) >= 90% pada misi-misi uji;
  (b) SC-G nol regresi selama 7 hari: outcome changes_requested/crashed/timed_out/blocked/
      gave_up/iteration_budget_exhausted per run tidak memburuk terhadap BASELINE (definisi
      SC-G: measures/README.md misi OPT-WF-0907).
- Vonis ditulis di AFTER.md jendela ukur (kartu D10); keputusan naik/revert lewat Decision Log
  controller. Gagal kriteria = revert ke opt-in, bukan diam-diam lanjut default.
- Selama opt-in, pola non-fast-lane (reaktif per fase) tetap sah untuk misi yang tidak
  mendeklarasikan diri; keduanya tidak bertentangan dengan norma N1.

## Rekonsiliasi dengan rujukan lama

- [`wave-dispatch-and-resume.md`](wave-dispatch-and-resume.md) dan [`wave-registration-large-fanout.md`](wave-registration-large-fanout.md) (02-09) memakai
  multi-parent edges antar-wave sebagai pengatur konkurensi. Di bawah N1 pola itu dibaca
  ulang: edge antar-wave sah bila hilir benar-benar mengonsumsi output hulu; bila tidak,
  ganti dengan prioritas + kap dispatcher (pitfall edge semu). Registrasi massal sekaligus
  kini justru DIANJURKAN (batch creation bebas), yang dibatasi hanya puncak running.
- `gsp-limit-aware-delegation` R-3 memegang pointer ke norma ini; jangan menduplikasi
  definisi di sana.
