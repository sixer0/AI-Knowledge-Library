---
id: temuan-audit-f1-f12
type: fakta
title: Temuan Audit Ekosistem GSP 24-08-2026 (F1-F12)
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 14
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [audit, temuan, risiko, gap]
links: [rekomendasi-peningkatan-kapabilitas-a-e]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Tabel F1-F12 identik kajian §14 baris 521-532 (12 baris; tingkat Tinggi x2, Sedang x6, Rendah x4 cocok persis); bukti 2 kartu blocked t_c26ab80f & t_0359aecc cocok §9.6 baris 426; RAW kedua ringkasan eksekutif §1 baris 37-40 mengonfirmasi temuan utama F1-F4. || Rekomendasi: Non-blocking: tidak ada."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/temuan-audit-f1-f12.md
---

# Temuan Audit Ekosistem GSP 24-08-2026 (F1-F12)

12 temuan audit ekosistem GSP 24-08-2026 (kajian §14):

| # | Temuan | Dampak | Tingkat |
|---|---|---|---|
| F1 | Roster mismatch `gsp-vendor-crawler-orchestrator` (roster) vs `gsp-crawler-orchestrator` (disk) | Dispatch via roster id salah sasaran/gagal | Tinggi |
| F2 | Gateway fleet mati saat audit; watchdog cron terakhir error | Profil tidak siap delegasi; perlu start ulang | Tinggi |
| F3 | Komentar ROSTER "43 statis" tidak sinkron (aktual 41) | Kebingungan inventaris | Rendah |
| F4 | 2 kartu kanban blocked belum direkonsiliasi (guard brief, fleet test image) | Jejak orkestrasi menggantung | Sedang |
| F5 | 2 AgentRequest failed + 1 rejected tanpa analisis lanjut | Kemungkinan bookkeeping vs agent failure | Sedang |
| F6 | Roster belum memuat user01-style dynamic dengan benar (1 dari 2 WebUiUser) | Visibilitas user access parsial | Rendah |
| F7 | PID file gateway memakai PID MSYS — tidak andal | Status online/offline misleading | Sedang |
| F8 | Kategori skill kanonik terpecah (kanonik EKAS 12 vs registry 128 vs per-profil) | Duplikasi & drift salinan skill | Sedang |
| F9 | Webstack: hanya 5 agen extract_backend=firecrawl; sisanya keyless ring | Kualitas ekstraksi tidak merata | Sedang |
| F10 | EKAS rantai jaminan PUTUS (GROUNDING/CYBERSECURITY/CIVIL) + R1 kosong | Batas jaminan domain tsb | Sedang |
| F11 | Wiki tersebar: folder wiki + HermesMemory + IL (3 sumber kebenaran) | Drift metadata | Rendah |
| F12 | Infrastruktur adjacent (n8n, open-webui, crawler-admin, ops autocrawl) tidak terkelola | Kebisingan & risiko resource | Rendah |

Sumber: `kajian_ekosistem_brahma.md` bab 14 (tabel Temuan, Risiko & Gap).

# Bukti

- Rekomendasi penanganan di §15 (lihat unit `rekomendasi-peningkatan-kapabilitas-a-e`).
- 2 kartu blocked: t_c26ab80f (guard brief), t_0359aecc (FleetTest
  gsp-image-analyst) — kajian §9.6.

# Catatan

- F1 & F2 adalah prioritas tinggi: konsolidasi identitas roster↔profil dan
  hidupkan ulang gateway fleet via watchdog.
