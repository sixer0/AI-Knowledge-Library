---
name: gsp-searxng
description: "Use when searching web via GSP's local self-hosted SearXNG (JSON API, parallel fan-out, engine spread)."
license: MIT
version: 1.1.0
author: GSP

metadata:
  hermes:
    tags: [gsp, searxng, search, selfhost, metasearch]
    category: devops
  category: search
---

# GSP SearXNG Self-Hosted

SearXNG self-hosted milik GSP berjalan lokal di `http://localhost:8080` —
metasearch engine (agregasi 70+ engine pencarian) tanpa API key, tanpa rate
limit. Dipakai sebagai backend `web_search` Hermes, paralel dengan DDGS
(cadangan) dan Firecrawl lokal (extract).

## When to Use
- Pencarian web untuk pipeline crawler/research/enrichment via API SearXNG
  lokal GSP (`localhost:8080`).
- Saat agen perlu tahu endpoint JSON, cara filter kategori (general/news/
  science), atau integrasi `web_search` Hermes dengan SearXNG.
- Saat butuh fan-out kueri paralel dan/atau sebar engine eksplisit — baca
  seksi PARALEL + SEBAR ENGINE di bawah (plafon, register, known-limit plugin).
- Fallback ke DDGS: `hermes config set web.search_backend ddgs` (atau
  `hermes -p <profil> config set ...`) kalau SearXNG bermasalah — hanya tangga
  darurat bersyarat-tercatat (sebab+bukti dicatat di laporan misi).

## Fakta Instalasi (aktual, diverifikasi `docker inspect` 11-09-2026)

| Item | Nilai |
|---|---|
| Lokasi | `C:/Users/TRIAL/searxng` (mesin Windows ini; image `searxng/searxng:latest`) |
| Endpoint | `http://localhost:8080` (UI + JSON API; binding riil `8080->8080/tcp`) |
| Settings | `C:/Users/TRIAL/searxng/settings.yml` — `use_default_settings: true`, `search.formats: [html, json]`, `server.limiter: false`, `server.public_instance: false`; engine tambahan aktif: `bing` (weight 2), `mojeek`, `qwant`, `yep`, `presearch` |
| Container | `searxng`, restart `unless-stopped`, dibuat 24-08-2026; bind riil `/c/Users/TRIAL/searxng:/etc/searxng:rw` (satu folder utuh, tanpa volume cache terpisah) |
| Catatan drift | `docker-compose.yml` di disk memetakan `8888:8080` + mount `settings.yml` tingkat-file `:ro` — TIDAK sama dengan kontainer berjalan. Jangan `docker compose up -d` dari berkas itu tanpa menyelaraskannya dulu: port akan berpindah ke 8888 dan `SEARXNG_URL` profil ikut mati. Sumber kebenaran = `docker inspect searxng`. |

> Catatan historis (Mac-era, sudah lewat): teks lama menyebut `~/searxng`,
> Colima, dan dua volume (`./searxng:/etc/searxng` + `./data:/var/cache/searxng`).
> Instalasi bermigrasi ke Windows 24-08-2026; baris di atas yang berlaku.

## Start / Stop / Cek

```bash
docker ps --filter name=searxng           # status (container `searxng`)
curl -s -o /dev/null -w "%{http_code}\n" http://localhost:8080/   # UI → 200
```

Container ditahan hidup oleh restart policy `unless-stopped` (Docker Desktop).
Kalau perlu create ulang, selaraskan dulu `docker-compose.yml` dengan bind/port
riil (lihat Catatan drift) atau recreate manual dengan `-p 8080:8080 -v
/c/Users/TRIAL/searxng:/etc/searxng` — jangan mentah-mentah dari compose lama.

## API JSON (curl langsung)

```bash
# Pencarian umum (default engine/category)
curl -s "http://localhost:8080/search?q=hermes+agent&format=json"
# Filter kategori: general, news, science, images, videos, dll
curl -s "http://localhost:8080/search?q=expo+jarkarta&format=json&categories=news"
# Pagination
curl -s "http://localhost:8080/search?q=xyz&format=json&pageno=2"
# Sebar engine EKSPLISIT (nama engine dari register — lihat seksi PARALEL)
curl -s "http://localhost:8080/search?q=xyz&format=json&engines=bing"
```

Respons: `{"query": ..., "results": [{"title", "url", "content", "engine", ...}],
"unresponsive_engines": [["<engine>", "<alasan>"], ...], ...}`. Field
`unresponsive_engines` WAJIB dibaca dan dicatat pada SETIAP kueri (bukan
opsional — lihat aturan di bawah). Build ini tidak menaruh field `engine` di
root respons; identitas engine dibaca dari field `engine` per item hasil.

## PARALEL + SEBAR ENGINE

Tiga lapis paralel (standar WF-CRAWL-0911; rujukan `identification/02_structured.md`
§Semantik Paralel, K-05/K-09/K-15/D-TA-4):

| Lapis | Isi | Aturan |
|---|---|---|
| P-1 | Fan-out kueri varian oleh pekerja (N request serentak) | Plafon per-pekerja **N=4**; mesin dipakai bersama fleet |
| P-2 | Sebar engine satu kueri via `engines=` EKSPLISIT | Hanya engine HIDUP di register; `unresponsive_engines` wajib dibaca tiap kueri |
| P-3 | Paralel internal mesin (agregasi SearXNG) | Hormati plafon per pemanggil; jangan saturasi instance bersama |

### Known-limit plugin Hermes (K-15)
Provider searxng Hermes (`hermes-agent/plugins/web/searxng/provider.py:68-88`,
dicek ulang 11-09) hanya mengirim parameter `q`, `format`, `pageno` dengan
`timeout=15` hardcoded. Konsekuensi: `web_search` native TIDAK PERNAH bisa
mengirim `engines=` (juga tidak `categories=`) dan selalu memakai sebar default.
Sebar engine menuntut HTTP langsung / skrip seperti resep di bawah — klaim
"multi-engine" dari `web_search` native tidak pernah sah.

### Register engine (satu-satunya sumber rekomendasi)
- Register merah-hijau: `docs/2026-09-11-firecrawl-searxng-parallel-enforcement/evidence/register-engine.md`
  (workspace bersama `C:/Users/TRIAL/workspace/gsp-hermes/workspace/`).
- Vonis 11-09-2026 (uji `engines=` eksplisit, 2 putaran): **HIJAU hanya `bing`**.
  MERAH: `mojeek` (degradasi senyap: 200 tapi 0 hasil di 4 kueri, access denied
  intermiten), `qwant` & `yep` (Suspended: access denied), `presearch` (timeout
  4.02s identik). Status `Suspended` bersifat backoff sementara — vonis ulang
  dengan menjalankan ulang `evidence/probe_engine_register.py`, bukan dari ingatan.
- Rekomendasi saat ini: `engines=bing` saja; `mojeek` kandidat observasi bila
  pulih. **DILARANG mengklaim multi-engine** sebelum register berubah. Perbaikan
  `settings.yml`/tambah engine = operasi terpisah (putusan D-TA-4), bukan aksi
  diam-diam dari skill ini.

### Resep P-1+P-2: fan-out kueri paralel dengan `engines=` eksplisit
(teruji terhadap `:8080` hidup 11-09-2026; bukti `evidence/s3_skill_recipe_check.py`
+ `.jsonl`, VERDICT PASS):

```python
# Fan-out varian kueri, plafon per-pekerja N=4, engines eksplisit dari register.
import json, urllib.parse, urllib.request
from concurrent.futures import ThreadPoolExecutor

BASE = "http://localhost:8080/search"
ENGINES = "bing"  # register 11-09: hanya bing HIJAU; cek register-engine.md sebelum ganti

def search(q, engines=ENGINES):
    url = BASE + "?" + urllib.parse.urlencode(
        {"q": q, "format": "json", "engines": engines})
    with urllib.request.urlopen(url, timeout=30) as r:
        d = json.loads(r.read().decode("utf-8"))
    unresp = d.get("unresponsive_engines", [])
    if unresp:                      # WAJIB dibaca + dicatat tiap kueri
        print(f"[unresponsive] {q}: {unresp}")
    return d.get("results", [])

queries = ["kueri-a", "kueri-b", "kueri-c", "kueri-d"]
with ThreadPoolExecutor(max_workers=4) as ex:   # plafon N=4 per pekerja
    out = dict(zip(queries, ex.map(search, queries)))
for q, res in out.items():
    print(q, len(res), {it.get("engine") for it in res})
```

Catat `unresponsive_engines` tiap kueri ke laporan/evidence misi. Kalau semua
engine selain yang diharapkan mati: laporkan **CAPPED-with-evidence** (register +
timestamp), bukan fallback diam-diam.

### Aturan: paralel bing-only TANPA sebar engine tidak dianjurkan
Terukur 11-09 (kontrak §1, kueri tanpa `engines=` = sebar default penuh):
paralel-4 = 8183 ms vs serial-4 = 5735 ms, SEMUA hasil tetap dari bing — rugi
murni. Ukur ulang segar 11-09 dengan `engines=bing` dipatok (skrip di atas):
paralel-4 wall 0.49 s vs serial-4 1.59 s — kerugian K-05 ternyata bersumber dari
kontensi sebar default (engine mati/lambat ikut diantri), bukan dari fan-outnya.
Meski begitu pasokan tetap bing-only (tanpa nilai tambah keragaman), sehingga
norma bertahan: **nilai tambah paralel SearXNG baru terbukti bila sebar engine
hidup**; kerja yang melaporkan "paralel sesuai norma" wajib menyertakan bukti
register engine hidup, bukan sekadar waktu.

## Integrasi Web Tools Hermes

1. `.env` profile (`~/.hermes/.env` atau `~/.hermes/profiles/<id>/.env`):
   ```
   SEARXNG_URL=http://localhost:8080
   ```
2. Config: `web.search_backend=searxng` (via `hermes config set` /
   `hermes -p <id> config set`). Extract tetap `web.extract_backend=firecrawl`
   (SearXNG search-only).
3. Berlaku di proses agent berikutnya (restart gateway/sesi).

SearXNG = **search-only**: `web_extract` TETAP butuh provider extract
(firecrawl/tavily/exa/parallel).

## Pitfall

- **403 Forbidden pada format=json** = format JSON belum diaktifkan di
  settings (`search.formats` + restart container).
- **Degradasi senyap**: HTTP 200 + 0 hasil + `unresponsive_engines` kosong ≠
  engine sehat (kasus mojeek 11-09: ditolak upstream tanpa flag konsisten).
  Vonis engine hanya lewat uji `engines=` per engine, bukan dari kueri default.
- **Error engine di log (wikidata, brave rate-limit, ddg timeout)** = normal
  untuk metasearch; engine yang sehat tetap memberi hasil. 0 hasil hanya jika
  SEMUA engine gagal — coba query lain/kategori lain.
- **Limiter butuh Redis/Valkey** — di lokal kita `server.limiter: false`.
  Kalau mau aktifkan, tambah service valkey + set redis URL.
- **Jangan expose publik** tanpa auth/reverse proxy + limit (Caddy/nginx).
- **DDGS timeout** (rate-limit DuckDuckGo): Hermes otomatis fallback ke keyless
  ring (exa/tavily/dll) untuk call itu saja, lalu kembali ke backend utama.
- Efek env/config baru aktif di proses baru (restart gateway).
- `python3` di PATH git-bash mesin ini stub WindowsApps (gagal jalan) — skrip
  uji pakai interpreter nyata (`AppData/Roaming/uv/python/...`) atau `uv run`.

## Verifikasi Cepat

```bash
curl -s "http://localhost:8080/search?q=test&format=json" | grep -o '"url":' | wc -l
# hitung jumlah hasil tanpa python; > 0 = hidup
# Dari sisi Hermes: hermes chat -q "web_search test" → cek log container:
docker logs searxng --since 2m 2>&1 | tail -20
```

## Changelog
- **1.1.0 (11-09-2026, t_bb010e1e / WF-CRAWL-0911 S3)** — tambah seksi PARALEL +
  SEBAR ENGINE (P-1/P-2/P-3, plafon N=4, `engines=` eksplisit ber-register,
  kewajiban `unresponsive_engines`, aturan anti paralel bing-only K-05); catat
  known-limit plugin K-15; sinkronkan fakta instalasi ke Windows (compose drift
  8888 vs 8080 didokumentasikan); teks Mac-era jadi catatan historis; semua resep
  diuji ulang terhadap `:8080` hidup (VERDICT PASS).
- **1.0.0** — versi awal (era Mac/Colima).
