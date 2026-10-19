---
name: gsp-firecrawl
description: "Use when scraping or crawling web via GSP's local Firecrawl."
license: MIT
version: 1.1.0
author: GSP

metadata:
  hermes:
    tags: [gsp, firecrawl, scraping, selfhost, vendor-intelligence]
    category: devops
  category: scraping
---

# GSP Firecrawl Self-Hosted

Firecrawl self-hosted milik GSP berjalan lokal di `http://localhost:3002`
dengan autentikasi server dimatikan (`USE_DB_AUTHENTICATION=false`) — request
tidak butuh API key. Dipakai oleh pipeline web (vendor crawler, enrichment,
research) sebagai mesin scrape/crawl.

## When to Use
- Scraping/crawling halaman web (satu halaman atau multi-URL) via API Firecrawl
  lokal GSP di `localhost:3002`.
- Agent yang bekerja di pipeline web (vendor crawler, enrichment, research)
  membutuhkan endpoint, pola curl, atau integrasi web tools Hermes.
- Operasional stack: start/stop, cek kesehatan, debugging, upgrade.

## Fakta Instalasi (aktual, jangan diubah tanpa verifikasi)

| Item | Nilai |
|---|---|
| Repo | `~/firecrawl` (git tag `v2.11.162`, compose di-patch: image GHCR prebuilt, FoundationDB dinonaktifkan) |
| Endpoint API | `http://localhost:3002` (hanya API yang di-publish ke host) |
| Auth | nonaktif — JANGAN expose ke jaringan tidak tepercaya tanpa auth/TLS |
| Stack | api + playwright-service + redis + rabbitmq + nuq-postgres (network `firecrawl_backend`) |
| Runtime | Docker via Colima (VM 6 CPU / 16 GB / 60 GB, auto-start via brew services, context `colima`) |
| Script helper | `~/firecrawl/start.sh` (start VM+stack), `~/firecrawl/stop.sh` (compose down) |

## Start / Stop

```bash
~/firecrawl/start.sh          # colima start (jika belum) + docker compose up -d
~/firecrawl/stop.sh           # docker compose down
docker compose -f ~/firecrawl/docker-compose.yaml ps   # cek status
```

Cek kesehatan: `curl -s http://localhost:3002/v0/health/readiness` →
`{"status":"ok"}`.

## Scrape Satu Halaman

```bash
curl -sS --max-time 90 -X POST http://localhost:3002/v2/scrape \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "formats": ["markdown"], "timeout": 60000}'
```

Formats umum: `markdown`, `html`, `rawHtml`, `links`, `screenshot`,
`pdf` (tergantung kapabilitas self-hosted). Respons sukses:
`{"success": true, "data": {"markdown": "...", "metadata": {...}}}`.

## Crawl (async, multi-halaman)

```bash
curl -sS --max-time 30 -X POST http://localhost:3002/v2/crawl \
  -H 'Content-Type: application/json' \
  -d '{"url": "https://docs.firecrawl.dev", "limit": 5}'
```

Body HANYA `{url, limit}`. Build ini MENOLAK key `maxDepth`, `formats`, dan
`depth` dengan `400 BAD_REQUEST` (`code: BAD_REQUEST`, `unrecognized_keys`) —
terukur 11-09; jangan pernah tambahkan key itu di body crawl.

Respons awal berisi `id` job + `url` untuk poll status:

```bash
curl -s http://localhost:3002/v2/crawl/<id>
```

ulangi poll sampai `"status": "completed"` (status antara: `scraping`), lalu
ambil halaman hasil di `data[]`.

## Batch Scrape (massal, async) — mekanisme utama ekstraksi massal

```bash
curl -sS --max-time 30 -X POST http://localhost:3002/v2/batch/scrape \
  -H 'Content-Type: application/json' \
  -d '{"urls": ["https://example.com", "https://example.org"], "formats": ["markdown"]}'
```

Respons awal: `{success, id, url, invalidURLs}`. Poll:

```bash
curl -s http://localhost:3002/v2/batch/scrape/<id>
```

ulangi sampai `"status": "completed"` dan `completed == total`. Bentuk hasil:
`data[]` berisi objek `{markdown, metadata}` LANGSUNG per URL (tidak ada
bungkus `success` per item); ikat hasil ke URL asal lewat
`metadata.sourceURL`. Lolos uji 2/2 pada 11-09.

## PARALEL (norma eksekusi)

- **Mekanisme utama ekstraksi massal: `/v2/batch/scrape`** — satu job async,
  fan-out diatur mesin. Puluhan–ratusan URL wajib lewat batch, bukan loop
  scrape tunggal.
- **Kompetisi scrape tunggal (`/v2/scrape`)**: plafon **N=4 request serentak
  per pekerja**, **maksimal 8 lane per misi**. Kapasitas mesin bersama:
  `MAX_CONCURRENT_JOBS=16`, `NUM_WORKERS_PER_QUEUE=4`,
  `CRAWL_CONCURRENT_REQUESTS=8` — mesin dipakai bareng fleet, JANGAN saturasi.
- **Sopan per-host**: satu request aktif per host tujuan pada satu waktu;
  jeda antar request ke host yang sama.
- **Known-limit plugin Hermes**: `web_extract` hanya mengekspos `/v2/scrape`;
  `/v2/batch/scrape` dan `/v2/crawl` TIDAK terekspos tool native. Resep massal
  wajib HTTP langsung (curl/skrip), bukan `web_extract`.

Resep konkuren scrape tunggal (plafon N=4; manfaat terukur 11-09: paralel-4
1275 ms vs serial-4 2656 ms, semua HTTP 200):

```bash
mkdir -p fc_out
for u in https://example.com https://example.org https://httpbin.org/html https://www.iana.org/help/example-domains; do
  curl -sS --max-time 90 -o "fc_out/$(echo "$u" | tr ':/.' '___').json" \
    -w "%{http_code} %{time_total}s $u\n" -X POST http://localhost:3002/v2/scrape \
    -H 'Content-Type: application/json' \
    -d "{\"url\": \"$u\", \"formats\": [\"markdown\"], \"timeout\": 60000}" &
done
wait
```

## Integrasi Web Tools Hermes (profile apa pun)

Agar `web_extract` (dan `web_search`) profile memakai Firecrawl lokal:

1. Di `.env` profile (`~/.hermes/profiles/<id>/.env` atau `~/.hermes/.env`):
   ```
   FIRECRAWL_API_URL=http://localhost:3002
   ```
   (tanpa `FIRECRAWL_API_KEY` — auth server off). Kehadiran var ini membuat
   Hermes otomatis memilih firecrawl sebagai backend default.
2. Di config profile: `web.extract_backend=firecrawl` dan `web.search_backend=searxng`
   (SearXNG lokal GSP di `http://localhost:8080` sudah terpasang — lihat skill
   `gsp-searxng` bila tersedia). DDGS tetap tersedia sebagai backend cadangan:
   `hermes config set web.search_backend ddgs` kalau SearXNG mati.
3. Efek baru aktif di proses agent berikutnya (restart gateway/sesi).

Catatan: perubahan config lewat `hermes -p <id> config set KEY VAL`, `.env`
jangan pernah di-commit.

## Pitfall Runtime

- **RabbitMQ healthcheck lambat**: `docker compose up -d` bisa gagal sekali
  dengan "dependency rabbitmq is unhealthy" (Erlang butuh beberapa detik).
  Solusi: tunggu 10-20 dtk lalu ulangi `docker compose up -d`.
- **Warning env kosong** (`variable is not set`) saat `docker compose config`
  itu normal — variabel opsional (SUPABASE, OPENAI, BULL_AUTH_KEY, dll).
- **`use_gateway=false` & keyless fallback**: di Hermes, jika firecrawl tidak
  terdeteksi, `web_extract` jatuh ke error "search-only backend". Pastikan
  `FIRECRAWL_API_URL` terbaca proses agent.
- **Jangan expose port 3002 ke publik**: tanpa auth, siapa pun bisa scrap.
  Untuk produksi: aktifkan auth + TLS di reverse proxy + persistent volume
  untuk postgres/redis/rabbitmq.
- **Upgrade**: pin tag release di `git checkout v2.<x>` sebelum ganti image;
  cek changelog compose per release (schema/env bisa berubah).

## Verifikasi Cepat Setelah Setup/Perubahan

```bash
curl -s http://localhost:3002/v0/health/readiness          # {"status":"ok"}
curl -sS --max-time 90 -X POST http://localhost:3002/v2/scrape -H 'Content-Type: application/json' \
  -d '{"url": "https://example.com", "formats": ["markdown"], "timeout": 60000}' | head -c 300
# lalu dari sisi Hermes: hermes chat -q "...gunakan web_extract pada https://example.com..."
# dan cek log: docker compose -f ~/firecrawl/docker-compose.yaml logs --since 2m api | grep Scrape
```

## Changelog

- 1.1.0 (2026-09-11, WF-CRAWL-0911): body contoh `/v2/crawl` dikoreksi jadi
  `{url, limit}` saja (build menolak `maxDepth`/`formats`/`depth` — 400
  `unrecognized_keys`, terukur 11-09); seksi Batch Scrape + poll ditulis;
  seksi PARALEL baru (batch/scrape utama, plafon N=4/pekerja & <=8 lane/misi,
  known-limit plugin); semua resep dieksekusi ulang terhadap mesin hidup.
