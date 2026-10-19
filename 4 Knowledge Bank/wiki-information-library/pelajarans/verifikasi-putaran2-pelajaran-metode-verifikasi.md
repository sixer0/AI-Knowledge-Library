---
id: verifikasi-putaran2-pelajaran-metode-verifikasi
type: pelajaran
title: "Pelajaran — metode verifikasi fleet GSP tanpa membocorkan secret"
status: active
sumber: docs/2026_08_24_verifikasi_putaran2/status.md
halaman: baris 19-61
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: verifikasi-putaran2
domain: digital
writer: gsp-librarian
tags: [verifikasi, metode, keamanan, pelajaran, fleet]
links: [verifikasi-putaran2-verdict]
penulis: gsp-librarian
diajukan: 2026-08-25
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-08-25

dipromosikan-dari: vault/verifikasi-putaran2/2026-08-25_verifikasi-putaran2-pelajaran-metode-verifikasi.md
dipromosikan-oleh: gsp-librarian
dipromosikan-pada: 2026-08-26
---

# Pelajaran — metode verifikasi fleet GSP tanpa membocorkan secret

Pelajaran metode verifikasi fleet GSP dari verifikasi putaran 2 (2026-08-24):

1. Audit env tanpa membocorkan secret: `env_check.py` read-only hanya melaporkan PANJANG nilai (mis. len=268) — nilai secret tidak pernah dibaca/dicetak; bandingkan panjang antar profil vs baseline home `.env` untuk deteksi missing/mismatch [status.md baris 28-30].
2. Deteksi proses tunggal saat wmic/pgrep tidak tersedia di host: gunakan psutil + tasklist; hitung kemunculan CommandLine spesifik (mis. `node bridge.mjs`) bukan semua node.exe [status.md baris 22].
3. Verifikasi proses/kode: `node --check bridge.mjs` (syntax) + pemeriksaan log (`err.log` kosong, `out.log` merekam eksekusi nyata) [status.md baris 24-25].
4. Verifikasi guard lintas-restart: bandingkan DataStore `generatedAt` (sumber kebenaran persisten) dengan counter AgentEvent — pembuktian "tidak re-fire" memakai counter yang tidak bertambah walau restart 5× [status.md baris 38-40].
5. Watchdog read-only saat sehat: jalankan `--verbose`, pastikan output berisi N baris `[running]` sesuai jumlah profil dan TIDAK ada aksi start/stop — bukti kesehatan tanpa mutasi [status.md baris 33-34].
6. Bukti sumber: file pendukung verifikasi (proc_check.py, env_check.py, db_check2.cjs, db_diag.cjs, db_final.cjs, db_queue.cjs, output watchdog --verbose, curl SearXNG) tercatat read-only di workspace kanban t_ed00e226 [status.md baris 57-61].

Rujukan silang: keputusan verdict `verifikasi-putaran2-verdict`. Pelajaran ini = sintesis metode yang terbukti dari verifikasi independen (kelas_bukti primer).
