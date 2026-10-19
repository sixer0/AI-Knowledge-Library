# HQ dashboard verification — quick recipe (29-08-2026)

Session notes for verifying Agent HQ (`gsp-datacenter`, https://localhost:9011,
self-signed HTTPS) after code changes. Complements SKILL.md golden rules.

## Skema & cara akses
- HQ SELALU via `https://` + `curl -sk` (HTTP biasa → "Empty reply" palsu;
  jangan salah simpulkan server mati). WebUI 9012 juga HTTPS.
- Dev mode (`npm run dev -- -p 9011 ... --experimental-https` via
  gsp-ecosystem-start.sh) → halaman/API baru LIVE tanpa rebuild, compile
  on-demand saat request pertama.
- Bila satu route gagal compile, dev overlay bisa membuat SEGMEN path lain
  ikut 500 (contoh nyata: duplikat deklarasi `zombieEdges` di
  /api/brahma/dispatch-kpi membuat seluruh /api/brahma/* 500 sementara).
  Banyak-500 mendadak = cek log `~/gsp-ecosystem/hq.err.log` dulu, jangan
  asumsikan DB mati.

## Halaman/API KPI dispatch (ada sejak 29-08)
- `GET /api/brahma/dispatch-kpi` — total, byStatus, review.pending,
  review.selfClaimHistoris (done tanpa decidedAt, pra-review-gate),
  orchestration.zombieEdges (record `running` + parent TIDAK `running`;
  jangan hitung dispatch yang memang berjalan sebagai zombie), multi-hop %.
- Halaman `/dispatch-kpi` + nav "Dispatch KPI" di Overview.
- Kit UI: `Button` hanya punya variant `primary|ghost` (bukan `outline`);
  `Panel/SectionHeader/Pill/Skeleton/EmptyState` ada di `@/components/ui/kit`.
- Nav sidebar: `src/components/sidebar.tsx` (navGroups array) — tambah item
  di sana, bukan layout.tsx.

## Verifikasi PATCH endpoint (review gate)
```
curl -sk -X PATCH 'https://localhost:9011/api/brahma/requests/<id>' \
  -H 'content-type: application/json' \
  -d '{"action":"force-done","note":"..."}'      # → 200, status done
```
- 409 = status tidak actionable untuk aksi itu (guard benar bekerja);
  baca field `error` di body, jangan asumsikan bug.
- Pre-existing repo noise: error compile route lain di hq.err.log
  (`jsonblob`, module-not-found lama) TIDAK berarti patch Anda salah —
  verifikasi route sendiri dengan HTTP code + body.
