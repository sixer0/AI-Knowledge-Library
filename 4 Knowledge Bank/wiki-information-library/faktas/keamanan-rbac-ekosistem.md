---
id: keamanan-rbac-ekosistem
type: fakta
title: Keamanan & RBAC Ekosistem GSP
sumber: docs/2026_08_24_kajian_ekosistem/kajian_ekosistem_brahma.md
halaman: bab 12
tanggal_akses: 2026-08-25
kelas_bukti: primer
sensitif: tidak
perkara: kajian-ekosistem-brahma
domain: operations
writer: gsp-librarian
tags: [keamanan, rbac, secrets, tailscale]
links: [temuan-audit-f1-f12]
penulis: dashboard
diajukan: 2026-08-25
updated: 2026-08-25
editor: gsp-librarian
direvisi-oleh: gsp-librarian
direvisi-pada: 2026-08-25
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-03
catatan_verifikasi: "Riwayat: Verdict awal (gsp-custodian, 2026-08-25): perlu_revisi. Revisi Wave B 2026-08-25 oleh gsp-librarian: fix-h1. Status kembali usulan untuk verifikasi ulang custodian.. Verdict: terverifikasi || Alasan: Seluruh klaim §12 tertelusur utuh ke kajian_ekosistem_brahma.md baris 489-497 (RBAC USER/ADMINISTRATOR, pitfall _rbac_user, HQ NextAuth+Approval Inbox, secrets tanpa nilai, Tailscale); RAW kedua contract doc 2026-08-24-kajian-ekosistem.md mengonfirmasi audit read-only tanpa membaca nilai secret; rujukan §15.E.13-15 cocok baris 558-561. Dedup: tidak ada entri wiki serupa (732 berkas diperiksa). YAML safe_load PASS, satu baris status, title==H1. sensitif=tidak wajar: body eksplisit tanpa nilai secret. || Rekomendasi: Saat promosi, catat untuk kurator: field penulis=dashboard berbeda dari writer=gsp-librarian (sistemik se-folder, bukan fabrikasi); pertahankan batas 'tanpa nilai secret' pada revisi berikutnya."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-03
dipromosikan-ke: faktas/keamanan-rbac-ekosistem.md
---

# Keamanan & RBAC Ekosistem GSP

Keamanan & RBAC ekosistem GSP (kajian §12):

- **WebUI Brahma (9012):** HTTPS TLS self-signed; auth username/password
  (WebUiUser); RBAC via `api/rbac.py`:
  - USER: panel chat/tasks/skills/memory/workspaces/todos; deny
    settings-write, escape, profiles-switch.
  - ADMINISTRATOR: full access.
  - Signout via `.rail` (desktop; `.sidebar-nav` hidden ≥641px).
  - Pitfall: state per-request `_rbac_user` wajib di-clear di
    `reset_trusted_auth_request_state`.
- **HQ (9011):** HTTPS self-signed; NextAuth Google OAuth + ALLOWED_EMAILS;
  INTERNAL_API_SECRET + CRON_SECRET untuk API internal; Approval Inbox untuk
  aksi side-effecting (bridge tidak pernah mengeksekusi `awaiting_approval`).
- **Roster dinamis:** user WebUI signup otomatis muncul di /api/agents
  (level 3, group controller).
- **Secrets:** KILOCODE_API_KEY di Hermes home .env (dibaca launch-bridge.sh);
  profil gsp-* punya .env masing-masing; audit ini TIDAK membaca nilai secret.
- **Jaringan:** tidak ada komponen terbuka ke internet; bridge hanya akses
  keluar ke Postgres + CLI lokal; akses remote via Tailscale.

Sumber: `kajian_ekosistem_brahma.md` bab 12.

# Bukti

- Rekomendasi E (§15.E.13-15): rotasi & minimalkan secret; pastikan .env
  tidak ter-commit; ganti TLS self-signed dengan cert internal CA;
  tinjau RBAC batasi role USER dari endpoint admin HQ; audit firewall.

# Catatan

- Sensitif: rincian secret TIDAK tercantum di sini (nilai dirahasiakan).
