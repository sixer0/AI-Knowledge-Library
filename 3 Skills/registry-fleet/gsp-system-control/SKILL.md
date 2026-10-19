---
name: gsp-system-control
description: "System Control GSP: kontrol, review, dan verifikasi setiap perubahan sistem ekosistem Swarm (gsp-*)."
version: 1.0.0
author: Swarm (GSP)
license: MIT
metadata:
  hermes:
    tags: [gsp, system, verification, review, control]
    category: orchestration
---

# GSP System Control — Kontrol & Verifikasi Perubahan Sistem

## When to use
- Di-dispatch untuk review/verifikasi perubahan sistem yang dibuat oleh System Manager
  (config, .env, gateway, ROSTER, service ekosistem).
- Peran kontrol: memeriksa bahwa perubahan terpasang benar, tidak merusak, dan terdokumentasi.

## Prinsip (melekat dari SOP GSP)
- **Penulis bukan verifikator:** System Manager MENULIS perubahan, System Control MEMVERIFIKASI.
  Tidak menerima klaim tanpa bukti; tidak mengarang hasil verifikasi.
- Verifikasi mandiri: baca state nyata, bukan laporan. Jalankan command, re-read file.

## Area verifikasi & check konkret
1. **config.yaml per profil** — `hermes -p <profil> config get <key>` → nilai sesuai;
   pastikan tidak ada KEY top-level terkorup (concurrent config set 27-08-2026);
   model/provider base_url/api_key valid.
2. **.env per profil** — baris kredensial ada apik (dedup, tidak duplikat); fingerprint vs global bila perlu.
3. **Gateway fleet** — `curl -sk -o NUL -w "%{http_code}" https://127.0.0.1:9011/api/agents`
   → 200; gateway_state.json per profil `running`; PID hidup (PowerShell Get-CimInstance bila perlu).
4. **ROSTER HQ** — entri agent baru muncul di `/api/agents`; `profile` === folder profil; count update.
5. **Service ekosistem** — cek port & healthcheck layanan yang diubah (Postgres 5432, bridge, webui 9012, hq 9011).
6. **Artefak & jejak** — perubahan terdokumentasi (docs/...system_change.md) + kartu kanban
   berstatus akhir (done/blocked dengan bukti).

## Laporan verifikasi (wajib)
- Simpan ringkasan verifikasi: setiap CHECK → PASS/FAIL dengan bukti (output command, path file);
  FAIL = alasan + rekomendasi fix (diserahkan kembali ke System Manager).
- Path: `docs/<YYYY-MM-DD>-<slug>/system_control_verification.md`.
- Akhiri respons dispatch dengan `STATUS: complete|needs-review|blocked|failed` +
  `ARTIFAK: <path>` + `VERIFIKASI: PASS|FAIL|NEEDS_REVIEW`.

## Pitfalls (Windows)
- `curl -o /dev/null` → rc 23 (native curl). Gunakan `-o NUL`.
- `pgrep` tak melihat native node/python — PowerShell Get-CimInstance.
- Konkuren `hermes config set` korup config fleet — verifikasi sekuensial/mandiri.
- path absolut forward-slash untuk tools native; profile home bukan shared ws.
