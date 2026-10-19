---
name: gsp-library-bulk-approval
description: "Bulk-approve library promotes via HQ Approval Inbox."
version: 1.0.1
author: GSP (PT. Gemilang Satria Perkasa) — Brahma Orchestrator
license: MIT
platforms: [macos, linux, windows]
metadata:
  hermes:
    tags: [gsp, library, librarian, approval, promote, vault, wiki, approval-inbox]
    category: gsp
  gsp:
    category: library
    tags: [gsp, library, approval, bulk, promote, vault, wiki, agent-hq]
---
# GSP Library — Bulk Approval Promote via Agent HQ

## When to Use

Use this skill when:
- Librarian (gsp-librarian) telah menandai banyak objek vault sebagai
  `menunggu_persetujuan` (sensitif) dan/atau `menunggu_verifikasi` (dosir),
  dan objek-objek itu perlu disetujui user sekaligus.
- Ada batch promote objek library sensitif yang menunggu approval (migrasi,
  kurasi massal, atau backfill knowledge).
- User meminta approval dibundle lewat Approval Inbox HQ (agent HQ) sehingga
  workflow promote + verifikasi lanjutan jalan terotomasi, bukan approval satu
  per satu.

Jangan dipakai untuk: promote tunggal non-sensitif (librarian bisa langsung),
atau objek yang belum melalui kurasi librarian.

Skill ini mengkodifikasi alur **persetujuan massal (bulk) untuk promote objek
library sensitif** lewat **Approval Inbox agent HQ**, dipakai ketika librarian
menandai banyak objek vault `menunggu_persetujuan` (sensitif) dan/atau
`menunggu_verifikasi` (dosir). Orkestrator (Brahma/agent HQ) menyatukannya jadi
**satu request approval**, user menyetujui sekali, lalu workflow promote dan
verifikasi lanjutan berjalan otomatis via agent HQ.

## Mengapa ini ada

Gate Information Library mewajibkan:
- `sensitif: ya`  → WAJIB `--approval-ref` (persetujuan user) sebelum promote.
- `perkara` dosir → WAJIB `--verification-by` (verifikasi manusia) sebelum promote.
- HANYA gsp-librarian yang boleh menjalankan `vault_promote.py` (penulis ≠ verifikator).

Tanpa skill ini, migrasi besar (mis. 46 objek sensitif) akan meminta 46 approval
satu per satu. Dengan bulk request, user cukup menyetujui **satu** kartu di
Approval Inbox, dan approval-ref yang sama dipakai untuk semua objek.

## Prasyarat / komponen

| Komponen | Lokasi |
|---|---|
| Vault root | `~/workspace/gsp-hermes/workspace/vault` (default SHARED_WORKSPACE) |
| Wiki (terbit) | `$HERMES_WIKI` atau `~/AppData/Local/hermes/wiki` (Windows) / `~/.hermes/wiki` (macOS/Linux) |
| Helper vault | profil gsp-librarian: `skills/gsp/gsp-library-workflow/scripts/vault_promote.py`, `skills/gsp/gsp-library-data-standards/scripts/vault_propose.py` |
| Kolektor bulk | `scripts/bulk_approval_collect.py` (skill ini) |
| API Approval Inbox | HQ: `POST /api/brahma/dispatch` (sideEffecting) + `PATCH /api/brahma/requests/:id` |
| Bridge mirror | `hermes-bridge/bridge.mjs` `mirrorWiki()` → HermesMemory → IL scope=wiki (interval `BRIDGE_MIRROR_MS`, default 30s) |

## Alur (wajib, urut)

### Fase 1 — Kurasi librarian menandai
Librarian mengkurasi objek vault (gsp-library-workflow):
- layak & non-sensitif → langsung promote (status wiki `active`).
- `sensitif: ya` → status objek `menunggu_persetujuan` + `catatan_keputusan` berisi alasan.
- dosir/perkara klien → `menunggu_verifikasi` (verifikasi manusia) + sumber dosir.

### Fase 2 — Orkestrator mengumpulkan BULK (agent HQ)
1. Scan vault untuk semua objek berstatus `menunggu_persetujuan`/`menunggu_verifikasi`:
   ```bash
   python scripts/bulk_approval_collect.py \
     --vault "~/workspace/gsp-hermes/workspace/vault" \
     --status menunggu_persetujuan --out approval_batch.json
   ```
   (keluarkan perkara ekas/fleet-test bila bukan bagian batch.)
2. Validasi jumlah & daftar objek (rel path, title, sensitif, perkara). Pastikan
   tidak ada objek yang terlewat (bandingkan dengan daftar kurasi librarian).
3. Buat **satu** request bulk ke Approval Inbox HQ:
   ```bash
   curl -sk https://127.0.0.1:9011/api/brahma/dispatch \
     -H "Content-Type: application/json" \
     -d '{"kind":"oneshot","title":"APPROVAL BULK: promote N objek library sensitif (migrasi ...)","profile":"gsp-librarian","sideEffecting":true,"prompt":"..."}'
   ```
   - `sideEffecting: true` → status `awaiting_approval` (masuk Approval Inbox).
   - Prompt harus self-contained: daftar SEMUA objek (rel path), approval-ref yang
     diusulkan, verification-by yang diusulkan, perintah promote via vault_promote.py.
4. Catat `request.id` yang dikembalikan → ini id approval bulk.

### Fase 3 — User menyetujui (Approval Inbox)
- User melihat kartu bulk di komponen Approval Inbox HQ (polling
  `/api/brahma/requests?status=awaiting_approval`).
- Approve: `PATCH /api/brahma/requests/:id {"action":"approve"}` → status `approved`.
- (Opsional `edit`: user ubah prompt lalu approve.)
- Bridge lalu mengeksekusi request tersebut (oneshot ke gsp-librarian).

### Fase 4 — Promote & verifikasi (lanjutan via agent HQ)
Librarian (hasil eksekusi request) menjalankan per objek:
```bash
python .../vault_promote.py \
  --vault <VAULT> --wiki <WIKI> --object <rel> --by gsp-librarian \
  --approval-ref <approval-ref-bulk> \
  --verification-by <nama-user> \
  --reason "Disetujui user <tanggal> (<konteks batch>)"
```
Lalu verifikasi (jangan klaim sebelum terbukti):
- Setiap entri wiki muncul di `<WIKI>/<type>s/<id>.md` berstatus `active` +
  jejak `di-attest-oleh`, `persetujuan-ref`, `verifikasi-oleh`.
- Setiap objek vault berstatus `dipromosikan`; tidak tersisa `menunggu_persetujuan`.
- Mirror: entri tampil di `curl -sk https://127.0.0.1:9011/api/information-library?scope=wiki` (setelah bridge mirrorTick, ≤ ~1 menit).
- Tulis jejak audit: `docs/<tanggal>_<batch>/persetujuan_user.md` (user, approval-ref, daftar objek).

## Pitfalls

- **Gate menolak tanpa approval-ref** — jangan coba force; promote sensitif tanpa
  approval-ref memang ditolak oleh `vault_promote.py` (fitur, bukan bug).
- **Dosir butuh verification-by** — perkara yang diawali `dosir` memicu gate;
  untuk dosir klien non-`dosir*` (mis. `kemhan-bin`), verification-by tetap
  dijalankan sebagai dokumentasi verifikasi manusia.
- **Satu approval-ref untuk satu batch** — konsisten di semua objek batch agar
  audit trail rapi; jangan menciptakan approval-ref baru per objek.
- **Hanya librarian yang promote** — orkestrator TIDAK menjalankan vault_promote
  sendiri; ia mengirim request (Fase 2/4) ke profil gsp-librarian.
- **Exclude perkara non-batch** — scan bulk harus mengeluarkan `ekas/`, `fleet-test`,
  dan objek yang sudah `dipromosikan` agar tidak di-promote ganda.
- **Bridge mungkin unreachable dari profil** — kalau librarian tidak bisa cek IL
  API dari env-nya, verifikasi mirror dilakukan oleh orkestrator dari env sendiri.
- **Kartu request hang** (proses oneshot >15m): verifikasi artefak mandiri,
  kill proses, tandai request done bila sukses nyata (pola dispatch HQ).
- **Sensitif internal GSP** (dokumen berklasifikasi RAHASIA/strategi) juga wajib
  approval — jangan asumsikan "internal = aman terbit".

## Verification (sebelum klaim selesai)

```
[ ] Jumlah objek di approval_batch.json == jumlah yg dilaporkan librarian (menunggu_persetujuan)
[ ] Semua entri wiki batch berstatus active + punya approval-ref/verification-by
[ ] Tidak tersisa objek menunggu_persetujuan utk perkara batch
[ ] IL scope=wiki menampilkan entri batch (mirror terkonfirmasi)
[ ] persetujuan_user.md terdokumentasi
```
