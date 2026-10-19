---
id: pelajaran-pitfall-operasional-ekosistem
type: pelajaran
title: Pitfall Operasional Historis Ekosistem GSP (PID, brief ganda, vision)
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 6.4, 7.4, 10.2, 1
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [pelajaran, pitfall, ops, gateway, daily-brief]
links: [temuan-audit-f1-f12]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-document-writer
direvisi-pada: 2026-09-03
status: active
verifikasi-oleh: gsp-custodian
verifikasi-putaran: 2
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Verdict: terverifikasi (custodian PUTARAN 2, 2026-09-03, re-challenge penuh 7 dimensi atas suntingan gsp-document-writer). Alasan: re-challenge PUTARAN 2: suntingan putaran 1 terverifikasi. Catatan penutup dikoreksi menjadi '#2-#4 diperbaiki (6.4); #1 hanya dimitigasi fallback PowerShell dan tetap temuan F7 tingkat Sedang dengan rekomendasi 15.B.4 belum dieksekusi; #5-#7 risiko terbuka' - F7 Sedang diverifikasi di kajian baris 527, fallback PowerShell di 10.2 baris 446; butir pitfall 1-8 tidak diubah, sesuai instruksi putaran 1. || Rekomendasi: objek siap lanjut ke lane librarian - sunting status 'terverifikasi' menjadi 'ditinjau' sebelum memanggil vault_promote.py (aturan I1); cek YAML kelas I5 dan klasifikasi dosir manual tetap prosedurnya. Tidak ada perubahan lain yang diperlukan penulis. Sensitif: tidak; dosir: tidak ada tema perkara hukum (kompensasi klasifikasi manual lane librarian, temuan I2). || Riwayat PUTARAN 1 (custodian 2026-09-03, perlu_revisi): Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: perlu_revisi || Alasan: Pitfall 1-8 semuanya tertelusur ke kajian (baris 246, 261-267, 351, 446, 521-527); NAMUN catatan penutup 'Pitfall #1-#4 sudah diperbaiki pada saat audit' keliru untuk #1 (PID MSYS): F7 tetap temuan terbuka tingkat Sedang (baris 527) dan rekomendasi §15.B.4 (ganti mekanisme PID) belum dieksekusi - yang ada hanya mitigasi fallback PowerShell (§10.2 baris 446). #2-#4 memang diperbaiki per §6.4. || Rekomendasi: Revisi catatan penutup menjadi: '#2-#4 sudah diperbaiki; #1 dimitigasi fallback PowerShell namun tetap menjadi temuan F7 dengan rekomendasi §15.B.4; #5-#7 risiko terbuka/rekomendasi.' Jangan ubah butir 1-8."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: pelajarans/pelajaran-pitfall-operasional-ekosistem.md
catatan_keputusan: "dipromosikan: subset lolos re-challenge RC-9 putaran 2 (9/9 terverifikasi); angka snapshot dibaca sebagai snapshot audit 24-08-2026 (objek terkait sudah membawa seksi Batas)"
---

# Pitfall Operasional Historis Ekosistem GSP (PID, brief ganda, vision)

Pelajaran operasional historis ekosistem GSP: pitfall yang sudah dibayar
mahal (kajian §6.4, §7.4, §10.2, §1):

1. **PID file MSYS vs Windows tidak andal** (§10.2, F7): PID dari `process.pid`
   di MSYS tidak bisa dicek hidup lintas proses Windows; fallback PowerShell
   di versi WebUI/HQ; rekomendasi: pakai state Hermes native
   (`hermes -p <p> gateway status`) bukan `process.kill(pid,0)`.
2. **Daily brief ganda setelah restart bridge** (§6.4): diperbaiki dengan
   guard persist harian via DataStore `hermes-briefing.generatedAt`.
3. **ReferenceError `kanbanCardId is not defined`** (24-08-2026, §6.4):
   scope variabel diperbaiki; pelajaran: bookkeeping failure ≠ agent failure:
   jika AgentRequest `failed` tapi `result` terisi, rekonsiliasi ke `done`.
4. **Dispatch berat timeout >4 menit** (§6.4): RUN_TIMEOUT_MS dinaikkan ke
   30 mnt; instruksi sub-task fokus+sempit <15 mnt.
5. **Profil vision tanpa terminal salah simpulkan "file hilang"** (§7.4):
   `search_files` default root = profile home; instruksi wajib path eksplisit.
6. **qwen3.7-flash rawan halusinasi detail gambar** (§7.4, smoke test
   24-08-2026).
7. **Roster mismatch `gsp-vendor-crawler-orchestrator` vs
   `gsp-crawler-orchestrator`** (§1 temuan F1): dispatch via roster id akan
   gagal; pakai nama folder profil.
8. **Daily brief ganda / kanbanCardId / timeout** adalah contoh perbaikan
   terdokumentasi; pelajaran umum: verifikasi lintas tool, jangan percaya
   status report agen.

Sumber: `kajian_ekosistem_brahma.md` bab 6.4, 7.4, 10.2, 1 (temuan), 14 (F1,
F7), 15 (rekomendasi B).

# Bukti

- Semua pitfall tercatat di source/kode auditor (bug historis §6.4) dan tabel
  temuan §14.
- Smoke test vision 24-08-2026 (#6) dari audit langsung.

# Catatan

- Pitfall #2–#4 sudah diperbaiki pada saat audit (§6.4); #1 (PID MSYS) hanya
  dimitigasi fallback PowerShell dan tetap menjadi temuan F7 tingkat Sedang
  dengan rekomendasi §15.B.4 yang belum dieksekusi; #5–#7 masih berupa risiko
  terbuka/rekomendasi.
