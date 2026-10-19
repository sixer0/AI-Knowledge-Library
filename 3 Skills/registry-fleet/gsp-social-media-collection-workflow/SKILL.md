---
name: gsp-social-media-collection-workflow
description: "Workflow koleksi data sosial media GSP: routing sumber gratis per platform, tangga eskalasi, referral graph, gerbang L7 scope-filter, eksekusi paralel, normalisasi, dedup, arsip. ALWAYS LOAD untuk agen gsp-social-media-crawler. Gunakan untuk membangun corpus data sosial yang kaya, bersih, dan siap dianalisis."
version: 1.4.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: intelligence
    tags: [social-media, crawler, collection, scraping, corpus, referral-graph, ladder, scope-filter]
---

# GSP Social Media Collection Workflow

> Pipeline koleksi untuk agen social-media-crawler. Target: corpus data sosial yang **kaya
> (bukan sekadar judul/permukaan), bersih (dedup + normalisasi), dan siap analisis**.
> Wajib: jalur gratis (tanpa API berbayar), hormati etika crawling & ToS platform.
> Lapis kendali misi (fase+gerbang lintas-fase) ada di payung `gsp-social-intel-orchestration` v2.0.0 [PATEN-AKHIR-0909].

## Pemicu

User/task meminta: kumpulkan data sosial, crawl percakapan/komentar/posting, bangun corpus
untuk topik/brand/handle/kompetitor, riset platform tertentu.

## Pipeline 6 Tahap

### Tahap 1 - Scope & Etika
1. Definisikan: topik + alias, platform, window waktu, target volume, kedalaman
   (posting saja / + komentar / + metadata penulis).
2. Cek `robots.txt` untuk situs target; tentukan rate limit (default: 1 req / 1-3 detik).
3. Konfirmasi hanya data publik; tidak ada bypass login/captcha; minimalkan PII yang
   dikoleksi. Catat keputusan ini di manifest.

### Tahap 2 - Routing Sumber (per platform, jalur GRATIS)
| Platform | Jalur gratis utama | Fallback |
|---|---|---|
| Reddit | JSON publik `reddit.com/r/<sub>/search.json?q=...&restrict_sr=1`, `old.reddit.com`, sort by relevance/new/top | searxng `site:reddit.com` |
| YouTube | `youtube-content` skill (transkrip), RSS kanal `youtube.com/feeds/videos.xml?channel_id=`, halaman hasil pencarian via firecrawl | yt-dlp (jika terpasang, untuk metadata/komentar publik) |
| X/Twitter | Browser untuk halaman publik; nitter instance publik bila ada; **jangan** login wall | searxng `site:x.com` (metadata dari snippet) |
| TikTok | Browser/firecrawl untuk halaman publik & hashtag; batasi karena anti-bot kuat | searxng `site:tiktok.com` |
| Instagram | Browser/firecrawl untuk profil/posting publik; login wall → batasi | searxng `site:instagram.com` |
| Threads | Browser/firecrawl halaman publik | searxng |
| LinkedIn | Browser/firecrawl halaman publik (rate-limit ketat; banyak login wall) | searxng `site:linkedin.com` |
| Bluesky | API publik atproto: `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=` (tanpa key) | searxng |
| Web/berita | `gsp-searxng` (lokal :8080) + `web_extract` | `gsp-firecrawl` (lokal :3002) untuk JS-heavy |
| Arsip/paywall | Wayback Machine API `archive.org/wayback/available` | `r.jina.ai` free tier |

Prinsip: **kumpulkan konten penuh + metadata + engagement**, bukan hanya snippet.
Jika sebuah platform menghalangi (login wall/anti-bot), catat di manifest sebagai
`platform_limited` dan lanjut ke platform lain - jangan paksakan cara tidak sah.

Kolom "Jalur gratis utama" di atas hanya pintu masuk. Vonis keterbatasan platform TIDAK boleh
dijatuhi dari kolom ini; pakai TANGGA ESKALASI per platform di bawah (L3).

#### NORMA FAN-OUT MULTI-ALAT PARALEL (WF-CRAWL-0911 D-06)

Norma eksplisit ini menggantikan norma implisit (`--jobs`, `HostScheduler`) tanpa mengubah
routing sumber gratis per platform di tabel Tahap 2 (Reddit JSON, atproto, dll tetap); ia hanya
melapis dua hal: mesin mana yang primer, dan batas paralelnya. Revisi D-06 (putusan user
11-09, benchmark crawl4ai lolos rubrik terkunci, vonis IMPROVEMENT_SAH — contract.md §9
docs/2026-09-11-firecrawl-searxng-parallel-enforcement/ + evidence/BENCHMARK-CRAWL4AI.md):
norma dua-mesin menjadi TIGA ALAT HIDUP — akuisisi ekstraksi disebarkan paralel ke
Firecrawl DAN crawl4ai, hasil digabung di lapis DEDUP sebelum analisa.

1. **Pencarian = SearXNG lokal :8080 PRIMER.** `web_search` Hermes pada profil crawler kini
   memakai backend searxng. Fan-out kueri varian dan `engines=` eksplisit lewat HTTP langsung
   mengikuti resep seksi PARALEL + SEBAR ENGINE skill `gsp-searxng` (pointer saja; register
   hidup/mati engine, rekomendasi engine, dan kewajiban membaca `unresponsive_engines` tinggal
   di skill itu - jangan duplikasi di sini).
2. **Ekstraksi/render = Firecrawl lokal :3002 + crawl4ai FAN-OUT PARALEL (tiga alat
   hidup).** Banyak URL sekaligus lewat `/v2/batch/scrape` (async + poll sampai completed)
   dan scrape tunggal untuk satu url, mengikuti resep skill `gsp-firecrawl` (pointer saja);
   crawl4ai jalur library venv produksi `C:/Users/TRIAL/gsp-tools/c4ai` mengikuti resep skill
   `gsp-crawl4ai` §PENGGUNAAN PRODUKSI (pointer saja). Keduanya alat SEJAJAR yang memegang
   slice URL berbeda — BUKAN fallback berjenjang. Lane yang sudah memakai mesin: X8
   (pencarian lewat searxng), T3 dan G1 (render lewat firecrawl; crawl4ai menggantikan
   posisi firecrawl di lane render hanya bila firecrawl mati terbukti).
3. **Plafon paralel lintas-alat**: per-pekerja firecrawl N=4 panggilan serentak DAN
   crawl4ai maks 2 proses browser serentak; per-misi maksimal 8 lane TOTAL lintas-alat
   (firecrawl + crawl4ai + lane searxng dihitung bersama), dirujuk ke kapasitas mesin
   (MAX_CONCURRENT_JOBS=16). Aturan lama `--jobs` (default 4, clamp maks 8; L6 butir 1)
   TETAP berlaku untuk skrip harvest beku `scripts/crawler/`; plafon baru ini berlaku untuk
   panggilan mesin langsung di luar skrip. Sopan-per-host (floor + jitter HostScheduler)
   tetap mengikat pada semua lapis.
4. **Tangga fallback bersyarat-tercatat** (D-TA-2 WF-CRAWL-0911) kini berstatus
   darurat-per-alat: ddgs/keyless/cloud boleh dipakai hanya bila alat terkait mati
   TERBUKTI - status HTTP/timeout dicatat dengan timestamp di `manifest.json`
   (`limitations`) atau baris LADDER; vonis mati berlaku per alat, fan-out sah jalan
   terus untuk alat lain yang hidup. Fallback senyap saat alat lambat atau sekadar tidak
   nyaman = pelanggaran norma.
5. **Lapis DEDUP sebelum analisa**: seluruh berkas harvest multi-alat (kolom
   url,konten,sumber,ts) digabung lewat
   `python skills/gsp-vendor-crawler/scripts/dedup_harvest.py --input <berkas...>
   --out-dir <dir>` (kanonik gsp-vendor-crawler; kunci URL ternormalisasi + sha256
   konten, deterministik+idempoten) -> `unique.jsonl` + report; angka `dup_removed`
   dilaporkan di manifest. Routing per platform tidak berubah; lapis ini TIDAK
   menggantikan hash `canonical_hash` Tahap 4 (level item corpus).

### Tahap 3 - Eksekusi Koleksi
1. Gunakan tool sesuai jalur (web_search/web_extract, browser, terminal untuk curl/yt-dlp).
2. Simpan **setiap** hasil mentah ke `raw/` (html/json) segera, dengan nama file ber-prefix
   platform + timestamp (mis. `reddit_20260821_1200_<id>.json`).
3. Catat engagement (likes/comments/shares/views/reposts) saat koleksi - angka bisa berubah
   seiring waktu.
4. Untuk posting panjang (YouTube, artikel, thread), simpan transkrip/teks penuh.
5. Jalankan mekanik lewat skrip beku `scripts/crawler/` (lihat seksi Perkakas), bukan lewat
   fetch manual per item; paralelkan dengan `--jobs` sesuai tabel kelas jalur di L6.
6. Pada mode fan-out D-06: slice daftar URL kerja antar-alat (firecrawl vs crawl4ai) di
   level URL SEBELUM eksekusi; simpan hasil tiap alat ke berkas harvest terpisah
   ber-prefix alat (mis. `firecrawl_<ts>.jsonl`, `crawl4ai_<ts>.jsonl`; kolom
   url,konten,sumber,ts); jalankan `dedup_harvest.py` (butir 5 norma di atas) SEBELUM
   item naik ke Tahap 4 dan sebelum apapun dianalisa.

### Tahap 4 - Normalisasi & Dedup
1. Petakan tiap item ke skema corpus `gsp-social-media-data-standards` (JSONL).
2. Hitung `canonical_hash = sha256(normalized_text + author_handle + publish_day)`.
3. Dedup: buang duplikat persis (hash sama). Untuk near-duplicate (judul mirip), tandai
   `duplicate_of=<item_id>` - jangan dihapus diam-diam.
4. Normalisasi teks: unescape HTML, hapus whitespace berlebih, pertahankan bahasa asli.
5. Jangan mengubah teks kutipan; simpan `content.text` apa adanya.
6. Sebelum ditulis ke `items.jsonl`, setiap kandidat WAJIB melewati gerbang L7
   (`scope_filter.cek_item`) - tidak ada cabang tulis yang melewatinya.

### Tahap 5 - Arsip & Manifest
Tulis ke `<workspace>/social/<job_id>/`:
- `raw/` - snapshot mentah
- `items.jsonl` - corpus normal
- `graph_edges.jsonl` + `frontier_<platform>.json` + `recount_summary.json` - bahan & hasil
  referral graph (wajib ada bila lane memakai L4)
- `quarantine.jsonl` + `off_platform.jsonl` - register penolakan L7 (bila gerbang aktif)
- `url_kanonik.jsonl` - hasil resolusi shortlink (rantai status lengkap, gagal tercatat)
- `dedup/unique.jsonl` + `dedup/report.md|.json` - hasil lapis KUMPUL->DEDUP lintas-alat
  (wajib ada bila mode fan-out D-06 dipakai; angka dup_removed masuk manifest)
- `manifest.json` - `{job_id, topic, aliases, platforms, window_start, window_end,
  collected_at, methods, total_items, dedup_removed, platform_limited[], limitations,
  ethics_notes, window_anchor}`
- `collection_report.md` - ringkasan per platform: jumlah item, kendala, catatan kualitas,
  tabel LADDER per rung, tabel kontribusi per kelas jalur, delta vs baseline

### Tahap 6 - Handoff
Sampaikan ke analyst/user:
- Path corpus + manifest + report.
- Ringkasan: total item, per platform, dedup, platform yang terbatas, dan saran
  analisis lanjutan.
- Status jujur: `complete` / `partial` (sebutkan apa yang gagal) / `blocked`.

---

## Field-wajib panen (v1.2, misi GAP-FILL-0909 09-09) - akar kekurangan blueprint §1

Akar kekurangan korpus pbw0907 (vonis blueprint `docs/2026-09-09-gap-driven-collection/identification/03_blueprint-gap-fill.md` §1.3, hasil ukur dump raw per lane): field mentah SUDAH ada di payload tapi tidak pernah naik ke items.jsonl karena skema normalisasi tidak punya kuncinya. Empat kelas field kini WAJIB dipanen dan WAJIB punya kolom di items/sidecar lane:

1. **views/tayang** (`view_count` YouTube & TikTok integer; `viewCount` X varian compact TANPA spasi; teks "N views" Threads/IG hanya dengan label `metode="regex-teks"`). Parser wajib `json.load` + coercion int, BUKAN grep; varian compact X terbukti lolos parser bila dibaca utuh. Predikat tercetak: kumulatif saat collected_at, bukan tayangan harian.
2. **reply_to / quote** (`in_reply_to_status_id_str` + `conversation_id_str`, `quoted_status_id_str`, `entities.user_mentions[].id_str` di X; `parent`/`t1_` balasan komentar YouTube; `parent_id`+`name`+`link_id` Reddit). Tepi relasi sah HANYA bila kedua sisi id tersimpan; simpan pasangan id dua sisi, jangan buang sisi kedua.
3. **followers** (`channel_follower_count` yt-dlp; `user.followers_count` payload syndication X; `followersCount` Bluesky; teks "N Followers" IG regex berlabel). Simpan sebagai snapshot per tanggal unduh; lane tanpa kunci mengirim KETERSEDIAAN-alasan, bukan nol.
4. **likes komentar** (skor/ups Reddit, `likeCount` Bluesky, like per komentar YouTube/X bila respons menyediakannya). Rerata likes-komentar adalah bahan formula pengaruh; hilangnya kolom ini membuat blok aktor kosong diam.

Aturan turunan WAJIB **simpan-field-mentah-jangan-dibuang**: setiap kunci numerik/relasional yang hadir di raw payload platform TIDAK BOLEH dibuang saat normalisasi hanya karena skema items belum mengenalnya. Jalur benar: naikkan sebagai field aditif (items extra atau sidecar ber-versi), atau catat di register kegagalan lane dengan alasan enum. Membuang field mentah diam-diam = cacat workflow (empat kelas di atas adalah kerugian nyata hasil audit pbw0907: follower YT 59 bahan + X 6 akun + bsky TERBUANG TOTAL, pohon komentar Reddit TERBUANG TOTAL, viewCount X 6 item TERBUANG, 21 video meta YT tanpa baris item).

Spesimen jalur ekstraksi per platform terinci di lampiran SPEC §2 blueprint GAP-FILL (SPEC-YT/TT/X/IGH/RBS/BRW); pemetaan targetnya ke skema payload v1.2 (AT-803/806/807 + flag `_ketersediaan`) di paten `gsp-sosmed-html-insight` Amandemen v1.2.0 bagian B.

---

## Perluasan Jangkauan (v1.1) - resep CRAWLER-EXPAND-0908

Resep ini berasal dari misi 08-09: vonis lama "platform tipis karena anti-bot" sebagian besar
salah sasaran. Yang mati adalah **discovery**; fetcher per-item (CDN syndication, oEmbed)
hidup dan menghasilkan item penuh. Karena itu aturan induknya: **sebelum menyebut sebuah
platform tipis, habiskan tangga rung dan lead referral graph lebih dulu.**

Perkakas beku (Python 3 stdlib-only, rerun tanpa interaksi, exit 0 = sukses) di
`scripts/crawler/`: `keyword_expander.py` (L1), `referral_harvest.py` (L4 + recount),
`shortlink_resolve.py` (L4), `harvest_per_id.py` (L3 per-item + L7), `ladder_state.py`
(LADDER), `scope_filter.py` (L7) + berkas data `spam_patterns.json`, `topic_tokens.json`,
`official_channels.json`. Urutan pakai per skenario: `scripts/crawler/README_crawler_expansion.md`.

Penomoran lapis terkunci (D-TA4-01): L1 expander kata kunci, L2 snowball, L3 tangga alternatif
per platform, L4 referral graph, L5 ambang anti-berhenti-dini, L6 teknik dasar, L7 gerbang
scope-filter. Sumber kebenaran:
`docs/2026-09-08-crawler-expansion/identification/06_blueprint-crawler-expansion.md`,
`identification/07_addendum-scope-filter.md`, `VERIFICATION.md` (VERIF4 PASS 9/9,
VERIF5 PASS 7/7), `scripts/crawler/README_crawler_expansion.md`.

### L1 - Pelebar kata kunci (`keyword_expander.py`)

Satu kata kunci masuk, `query_plan.json` keluar: minimal 12 varian, minimal 5 kelas terisi,
tiap query bertag kelas + bahasa, panjang <= 100 karakter. Kelas: gelar/jabatan, nama lengkap
dan varian urutan, salah ketik, hashtag, handle resmi, ko-entitas kebijakan, gaul/sarkasme
netral, multi-bahasa.

Aturan: (a) query plan ditulis ke folder misi, tidak mengendap di kepala worker; (b) hanya
query yang bisa langsung dieksekusi yang boleh masuk plan; (c) ko-entitas tidak boleh melebar
ke topik di luar kata kunci asal; (d) anggaran: konsumsi direct-search hasil ekspansi
**<= 25%** anggaran discovery sebuah lane, sisanya untuk L3/L4 (D-TA4-08).

### L2 - Snowball

| Jalur | Cara | Batas | Meteran |
|---|---|---|---|
| Thread balasan/quote X | ikuti field `in_reply_to` / `quoted_tweet` dari respons syndication/oEmbed, fetch id itu juga | 2 level dari root, maks 20 anak/root | >= 50% item X punya pemeriksaan tepi balasan/quote tercatat (ada atau tidak ada) |
| Komentar level-2 | YouTube via yt-dlp (termasuk replies); Reddit JSON bersarang alamiah; Threads hanya yang terlihat render | 1 level balasan | item komentar membawa `parent_thread_url` |
| Author-snowballing | tarik timeline publik author item hasil panen (`timeline-profile` per handle) | 1 hop dari seed, maks 10 author/batch, cooldown >= 45 dtk/handle | >= 3 author baru per misi (meteran M4) |

Hanya simpul publik; tanpa login/pertemanan; author snowball berhenti saat 429 persisten
(vonis per handle, bukan dipaksa).

### L3 - TANGGA ESKALASI per platform

Aturan umum tangga:
1. Tangga WAJIB berjenjang. Vonis mati dijatuhkan **per rung**, dengan status HTTP +
   timestamp di LADDER (`ladder_state.py`), bukan per platform.
2. Vonis "jalur mati" untuk satu platform sah hanya bila semua rung kelas itu terisi.
3. Rung bertanda `[MATI-0907]` sudah divonis dengan bukti: cukup probe ulang SEKALI murah
   per misi (cek harian), tidak wajib mengulang seluruh tangga mati.
4. Kolom "Bukti" di bawah adalah status terakhir terukur; endpoint bertanda HIDUP dijalankan
   lebih dulu karena murah dan terbukti menghasilkan item.

**X/Twitter**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| X1 | `cdn.syndication.twimg.com/tweet-result?id=<id>&token=<t>` per id | 200 JSON teks + likes + `created_at` | 403/404 per id = mati untuk id itu; ganti skema token = vonis rung | HIDUP (21 item) |
| X2 | `publish.twitter.com/oembed?url=` per id | 200 JSON `author_name` + `html` | 400/404 per id; rate limit IP -> backoff | HIDUP |
| X3 | widget `platform.twitter.com` (embed timeline) per handle | payload tweet terlihat | shell kosong/DNS = mati | belum teruji |
| X4 | `syndication.twitter.com/srv/timeline-profile/screen-name/<h>` | 200 JSON ~20 tweet terakhir | 429 persisten setelah 1 retry jeda >= 45 dtk = vonis per handle | HIDUP 4/6 handle |
| X5 | nitter instance hidup-harian (daftar 6-8, probe `/search?f=tweets&q=` sekali per misi) | 200 + tautan status | semua JS-wall/403/DNS dalam satu probe = vonis tercatat ts | MATI-0907 |
| X6 | Wayback CDX pola `x.com/*/status*` per window | daftar snapshot | 200 body kosong = mati untuk window | MATI-0907 |
| X7 | archive.today untuk url status spesifik | halaman terarsip | timeout/403 dua percobaan = mati | belum teruji |
| X8 | mesin pencari (searxng multi-engine + `site:x.com`) untuk status-id | URL status baru | 0 status-id dari >= 8 kueri varian baru = vonis | MATI-0907 untuk real-time; probe ulang hanya dengan varian L1 baru |

**TikTok**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| T1 | yt-dlp metadata per-video (tanpa unduhan) | JSON deskripsi + stats + timestamp | rc1 "No working app info" = mati extractor | HIDUP 16/16 |
| T2 | `tiktok.com/oembed?url=` per url | 200 JSON caption + `author_unique_id` | 400/404 per url | HIDUP; TIDAK membawa tanggal (tanggal dari dekode `id>>32`) |
| T3 | render halaman tag/profil/search UA mobile (firecrawl :3002 atau curl UA pool) | `SIGI_STATE`/`SIGI_BLOCK` berisi video id | shell tanpa data video 2x UA berbeda = vonis | MATI-0907; cek harian 1x |
| T4 | Wayback CDX `tiktok.com/@<u>/video*` dan `/tag/*` | daftar snapshot | 200 kosong = mati window | MATI-0907 |
| T5 | discovery L4: id video datang dari tepi platform lain (`frontier_tiktok.json`) | id baru belum claimed | frontier kosong = vonis "graph tidak menyuplai", BUKAN "tiktok mati" | jalur harapan utama; discovery direct mati |

**Instagram / Threads / Facebook**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| G1 | firecrawl render post/thread per-url | caption + tanggal + likes terbaca | `mdlen=0` / 408 -> 1 retry; mati per-url tercatat | HIDUP (200 x13 lane ig) |
| G2 | mbasic/m.facebook halaman publik (profil/feed/hashtag) | teks pos terlihat | login wall = catat `platform_limited` | sebagian (fb 1 item live-text; permalink butuh login = berhenti) |
| G3 | render profil IG publik akun terkait | caption memuat token entitas | login wall / shell = vonis | HIDUP terbatas |
| G4 | CDX/archive `instagram.com` & `facebook.com` | snapshot | kosong = mati | belum diuji sistematis |
| G5 | Threads dari frontier L4 (tepi `threads.net` dari korpus) | url post baru | frontier habis = vonis suplai | jalur utama threads; dump tag padat 18-35 tautan/halaman |

Routing FB: Facebook nyaris nol rujukan keluar di korpus, jadi FB dicari dari mesin
pencari/CDX (G2/G4), BUKAN dari referral graph.

**Reddit**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| RD1 | `reddit.com/r/<sub>/search.json` + listing `.json`, UA jujur (identitas + kontak `--contact`), backoff eksponensial | 200 JSON posting + komentar | 403/429 persisten setelah backoff 60 dtk = vonis per sub | HIDUP (47 item lane reddit-bluesky) |
| RD2 | pullpush.io / arctic-shift (mirror historis) | 200 JSON | down/rate-limit = catat | BELUM teruji; jangan dikutip sebagai endpoint terbukti hidup |
| RD3 | RSS search (`search.rss`) | XML entri | kosong = mati | belum teruji |

**Bluesky**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| BS1 | `public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=` (tanpa key) + retry backoff | 200 JSON posts | timeout/5xx persisten = vonis sementara (catat ts) | HIDUP |
| BS2 | mirror publik API (instance alternatif) | 200 JSON | mati = catat | belum teruji |
| BS3 | sampling relay firehose tanpa auth (jetstream/relay publik) jendela terbatas, filter token topik | stream event masuk | koneksi ditolak = mati | belum teruji; SAMPLING menit bukan jam, simpan hanya event bertoken |

**Berita/web**

| Rung | Cara | Sinyal hidup | Ambang mati | Bukti 08-09 |
|---|---|---|---|---|
| NW1 | `news-sitemap.xml` portal (kompas, tempo, cnnindonesia, antaranews, detik, kumparan): loc + pubDate | XML URL + tanggal | 404 -> coba varian sitemap index / `news.xml` / `sitemap-news.xml` | sitemap resmi = jalur primer; BELUM teruji di misi ini |
| NW2 | Bing News RSS + Google News RSS per publisher (`site:<domain>`) | 200 XML entri | hasil identik lintas kueri = fallback generik, buang | HIDUP sebagian (36 item); generik = buang |
| NW3 | Wayback CDX per domain harian | snapshot list | kosong = mati hari itu | belum teruji |

### L4 - REFERRAL GRAPH kelas satu

Referral graph adalah jalur produksi utama, bukan pelengkap. Kontribusi terukur pada korpus
pilot 08-09 (diukur ulang sendiri oleh custodian 08-09 atas `items.jsonl`, bukan dikutip):

| Lane | Item | Dari graph | Kelas lain | graph_edges.jsonl |
|---|---|---|---|---|
| pbw0908-pilot/x-tiktok | 172 (x 143, tiktok 29) | 151 | direct 20, snowball 1 | 18.642 baris |
| pbw0908-pilot/ig-threads-fb | 223 (threads 203, instagram 13, fb 7) | 216 | direct 7 | 18.628 baris |
| pbw0908-pcmp/ig-threads-fb | 37 (threads 25, instagram 12) | 33 | snowball 4 | 27.519 baris |

Rekonsiliasi satuan (penting agar tidak salah kutip): angka "33/37" pada lane pcmp memakai
`provenance.path_class` (33 graph + 4 snowball), sedangkan `provenance.path` bernilai
`referral_graph` pada 37/37 item karena kedua kelas itu sama-sama bersumber tepi. Lane pcmp
juga tercatat `via_edge` null pada seluruh itemnya (jejak edge tidak ikut tersimpan di lane
itu) - jangan klaim jejak edge lengkap pada lane tersebut.

Isi resep:

1. **Panen tepi dari SEMUA teks** (`referral_harvest.py --corpus <korpus>`, boleh berulang;
   korpus misi sebelumnya adalah bahan bakar awal). Output `graph_edges.jsonl` dengan kunci
   skema: `edge_id, source_doc, source_platform, ditemukan_di, target_url_raw,
   target_url_kanonik, target_id, platform_target, is_shortlink, ts_scan`. Pola kanonik:
   x/twitter status, tiktok video/v/awards, threads.net|threads.com post, youtube
   watch|shorts|live|youtu.be, instagram p|reel, bsky.app profile/post, facebook
   post/permalink, shortlink (t.co, bit.ly, dlvr.it, buff.ly, rb.gy, s.twimg.co, lnkd.in,
   ow.ly, is.gd, tinyurl, tiny.cc, shorturl.at).
2. **Recount sebelum angka**: `recount_summary.json` (id unik per platform) ditulis ke
   `collection_report.md` SEBELUM angka target/delta apa pun dikutip (D-TA4-05). Angka PoC
   berbasis occurrence (154/379/23/786/282) dicabut dan tidak boleh dikutip lagi; satuan
   occurrence dan id-unik berbeda.
3. **Shortlink wajib di-resolve** (`shortlink_resolve.py`): HEAD lalu GET fallback, ikut
   redirect, rantai status lengkap, jeda >= 1,0 dtk dan <= 4 req/menit per domain shortener.
   GAGAL TERCATAT (status + ts) di `url_kanonik.jsonl`, bukan hilang. Prioritas 1 = sumber
   yang bukan judul Google News (pelajaran: 9/10 shortlink dari judul berita menuju artikel,
   0 menuju posting kanonik). Hasil "artikel berita" dialihkan jadi bahan frontier berita,
   bukan dibuang.
4. **BFS kedalaman 2**: depth 1 = tepi dari dokumen korpus lama; depth 2 = tepi dari item BARU
   hasil panen misi ini (jalankan ulang `referral_harvest.py` dengan `--corpus <out-dir>`).
   Antrian per platform `frontier_<platform>.json`. DEDUP SAAT MASUK frontier (bukan saat
   keluar) dengan kunci `(platform_target, target_id)`; kapasitas 200 id per batch per
   platform, sisa dicatat sebagai frontier tertunda (bukan dibuang).
5. **Jejak asal-usul**: item hasil panen membawa `provenance.path="referral_graph"` dan
   `provenance.via_edge=<edge_id>`. Frontier lama yang sudah dipanen otomatis hilang karena
   claimed terhadap `items.jsonl` lane.
6. **Atribusi dari ISI respons, JANGAN dari path URL** (D-TA4-07). Author dan tanggal SELALU
   dari field respons endpoint (`user.screen_name`, `author_name`, `author_unique_id`,
   `created_at`, `created_utc`). Path user hanya dipakai membentuk URL tampilan. Bukti
   kegagalan preseden: path `/prabowo/status/` mengembalikan author `@sjafriesjams`, dan path
   `/@prabowo/video` mengembalikan `@pojoksatu.id`; keduanya akan salah atribusi bila path
   dipakai sebagai klaim author. Tanggal TikTok dari dekode `id>>32` (oEmbed TikTok tidak
   membawa tanggal), diverifikasi yt-dlp bila alat tersedia. Engagement tak terlihat =
   `null`, bukan 0. Item tanpa tanggal diberi `window="unknown"`, tidak dihitung W1/P1 dan tidak
   naik ke kolom terbit.
7. **Vonis baru (menggantikan vonis lama)**: vonis "tipis/buntu" untuk sebuah platform HANYA
   sah setelah EMPAT kelas jalur dijalankan dan terbukukan di LADDER: (1) direct search,
   (2) alternatif resmi (tangga L3), (3) arsip (CDX/archive.today), (4) referral graph
   (termasuk resolusi shortlink dari sumber yang tersedia). Vonis tanpa keempatnya =
   pelanggaran L5. Kata "tipis" tidak boleh muncul sebagai vonis tanpa LADDER lengkap.

### L7 - GERBANG SCOPE-FILTER (proteksi backlink)

Link yang dipanen dari badan posting dan komentar bisa dispami iklan judi online, farm SEO,
atau tujuan di luar scope. Gerbangnya SATU modul, bukan dua salinan logika.

1. **Satu titik wajib per alur.** `scripts/crawler/scope_filter.py` di-import (tidak disalin)
   oleh `referral_harvest.py` (`saring_edge` saat menulis `frontier_<plat>.json`),
   `shortlink_resolve.py` (`cek_final_url` sebelum menulis rekaman selesai), dan
   `harvest_per_id.py` (`cek_item` sebelum `out_f.write`). Runner lane/BFS memakai fungsi yang
   sama; runner TIDAK boleh menulis frontier atau items lewat jalur lain, dan dilarang
   menyalin logikanya. Whitelist platform diimpor dari `referral_harvest.ALL_PLATFORMS`
   sebagai sumber tunggal (matcher ganda = buta-titik terwarisi).
2. **Dua sumbu ortogonal, dilarang digabung** (D-TA5-01): SCOPE = apakah tujuan termasuk
   whitelist platform; MOTIF = apakah teks/handle/domain bermotif iklan-spam. Blog off-topic
   yang relevan topik = gagal scope tapi lulus motif; akun judi online = gagal motif. Obat dan
   labelnya beda.
3. **Karantina tercatat, non-destruktif** (D-TA5-03/04): setiap penolakan menjadi baris
   `quarantine.jsonl` dengan kode alasan; identitas rekonsiliasi WAJIB berlaku per aliran
   `N_masuk = N_lolos + N_quarantine`. Edge yang ditolak TETAP ada di `graph_edges.jsonl`
   (register bahan mentah). Audit retroaktif TIDAK menulis ulang dan TIDAK menghapus
   `items.jsonl` yang sudah terbit; hasilnya laporan + delta + quarantine, promosi/demosi
   hanya lewat keputusan controller.
4. **Urutan gerbang item tetap** (D-TA5-09): MOTIF, lalu SCOPE/platform, lalu ENTITY, lalu
   TOPIK, lalu TANGGAL. Kode utama adalah kegagalan pertama; kode lengkap disimpan di daftar.
   Kegagalan pada empat gerbang pertama membuat item tidak ditulis dan masuk quarantine,
   sedangkan kegagalan tanggal membiarkan item tetap ditulis dengan `window="unknown"` dan
   flag tidak tayang.
5. **Denylist adalah berkas data** (`spam_patterns.json`, dimuat runtime; AC-13 menolak entri
   tanpa `sumber`). Kondisi terukur 08-09: 4 keluarga, semuanya membawa `motif` + `sumber`,
   `domain_huruf` kosong pada semua keluarga (tidak ada blokir domain sewenang-wenang;
   blogspot memakai mode `scope_bukan_motif` = label farm-seo di register, bukan blokir).
   **Pola huruf untuk domain/nama; pola angka HANYA untuk string berlabel nama/handle**
   (regex angka polos menghasilkan 61 positif-palsu pada id status URL; path/id tidak pernah
   dipolai). Default ketat: `sumber_edge=tidak-diketahui` diperlakukan sama dengan `komentar`
   (butuh 2 sinyal). Gerbang hanya membaca field teks terurai, dilarang memindai byte HTML
   mentah, atribut class, atau blob base64.
6. **Larangan sensor** (D-TA5-08): pemfilteran dibatasi MOTIF IKLAN/OUT-OF-SCOPE. Dilarang
   menyaring karena pandangan politik/opini. Item yang hanya "tidak relevan topik" masuk
   karantina dengan `review_manusia=true`, bukan dihancurkan. Register quarantine/off_platform
   adalah artefak audit internal, bukan kolom terbit.
7. **Template audit = bypass test 4 jalur** (verifier menjalankan sendiri, bukan percaya
   laporan pekerja): (A) frontier manual + panggilan harvest langsung; (B) final_url shortlink
   off-platform; (C) suntik `graph_edges.jsonl` manual lewat jalur audit; (D) host merek judi
   standalone. Uji wajib: `python scripts/crawler/scope_filter.py --selftest` (exit 0, subset
   inti 12/12) dan `--audit <korpus> --out <dir>` (offline, deterministik, byte-identik antar
   run). Presisi penolakan dan recall kelulusan disampel dengan seed tercatat.

### L5 - Ambang anti-berhenti-dini

Gerbang vonis adalah PROSEDUR, bukan angka keras item (D-TA4-03; vonis RT: angka keras memicu
inflasi item). Vonis/partial-handoff sah hanya bila:

1. Semua rung semua kelas jalur dicoba dan terbukukan dengan status HTTP + timestamp di LADDER.
2. Semua lead murah yang sudah ada di `raw/` habis diproses (promosikan kandidat jadi item,
   atau buangkan dengan alasan gerbang, tercatat).
3. Delta terhadap baseline dilaporkan pada satuan yang sama.
4. BFS depth 2 selesai, atau frontier tersisa dicatat jumlahnya.

Angka hanya berperan sebagai FLOOR DELTA keberhasilan (bukan gerbang lapor), misalnya >= 10
item non-direct per lane; controller boleh mengubah floor per misi dengan keputusan tercatat.
Partial-handoff sah hanya bila anggaran riil <= ambang-B LAD ATAU tangga benar-benar habis
dengan LADDER lengkap. Preseden yang dilawan: penutupan x-tiktok dengan W1=4 padahal kuota
longgar, dan vonis "tipis karena anti-bot" yang salah sasaran.

### L6 - Teknik dasar seragam

1. **Paralel sopan**: `--jobs N` (default 4, clamp maks 8) pada `harvest_per_id.py` dan
   `shortlink_resolve.py`. Model: pool worker jalan paralel ANTAR HOST; `HostScheduler`
   menahan laju PER-HOST >= `max(--delay, floor)` dtk + jitter berseed nama host. Paralel
   menaikkan CONCURRENCY antar-host, bukan LAJU per host. `--jobs 1` = jalur serial lama persis.
   Plafon terukur: pada jalur render-proxy SATU host (firecrawl :3002 menuju threads.net) rasio
   nyata jobs=4 vs jobs=1 **1,42x** pada konfigurasi server lama (MAX_CONCURRENT_JOBS=2; subset
   identik 30 url, cache off, 08-09 17:08-17:14; target >=2x tidak tercapai karena antrian render
   internal server). AMANDEMEN 08-09 17:40 (putusan user 'approve improve kinerja firecrawl'):
   konkurensi server dinaikkan (MAX_CONCURRENT_JOBS 2->16, NUM_WORKERS_PER_QUEUE 1->4,
   CRAWL_CONCURRENT_REQUESTS 2->8, BROWSER_POOL_SIZE 2->8; .env.bak-0908 tersimpan) -> benchmark
   klien IDENTIK jobs=4 turun 151,0 dtk -> 53,1 dtk (**2,84x** vs konfigurasi lama; 3,67x vs
   baseline serial 195,0 dtk konfigurasi lama). Vonis lama 'plafon jalur satu host 1,4x' ternyata
   plafon KONFIGURASI, bukan fisika: render cold 6 serentak kini wall 31,2 = render terlambat
   (bukan berjenjang). Multi-host (campuran oEmbed/CDN/syndication/shortener = mayoritas panen
   nyata) tetap untung penuh. Jangan merekayasa angka rasio; laporkan penyebab terukur.
2. Panduan `--jobs` per kelas jalur: render proxy lokal 4-8 (server multi-render TERBUKTI sejak
   08-09; ukur dulu sebelum naik >4); oEmbed/CDN resmi 4; Reddit 1-2 (satu host dominan + rate
   limit sendiri); Bluesky 1-2 (dua request berurutan per post di host sama); shortlink 4
   (floor 15 dtk per domain shortener).
3. **Simpan-leads-dulu**: respons mentah ditulis ke `raw/` SEBELUM parsing; tidak ada data yang
   hanya hidup di memori sesi.
4. **Cache antar batch** `social/_cache/ce/`, TTL selama misi; 429/5xx di-cache negatif 10 menit.
   Kunci cache POST ikut **method + body** (kunci GET tidak berubah) - sebelumnya tabrakan kunci
   pada render firecrawl. Timeout transport render 75 dtk (probe: scrape normal 32 dtk divonis
   `ERR:timeout` palsu oleh timeout 25 dtk).
5. **Determinisme uji**: `--stable-output` mengurutkan batch by key, plus `GSP_FIXED_NOW=<iso-z>`
   untuk jam tertambat, sehingga dua run atas input sama byte-identik.
6. Rotasi UA pool 4-6 string (3 desktop, 2-3 mobile) bergilir per request per host; UA jujur
   wajib untuk Reddit (identitas + kontak) dan Bluesky. Backoff eksponensial 2^n dtk, plafon
   60 dtk, maks 3 retry per URL, kecuali aturan khusus per rung (X4 cooldown 45 dtk per handle).
7. `robots.txt` membatasi CARA, bukan tujuan: hormati larangan pada jalur itu lalu pindah rung
   berikutnya; larangan bukan izin melewatinya, dan bukan pula vonis buntu untuk platformnya.
8. Semua angka laporan dihasilkan skrip Python deterministik (D-TA4-09). Dilarang mengutip
   angka dari ingatan/laporan pihak lain tanpa ukur ulang; backend rg di host ini tidak reliabel
   untuk pola URL bergaris miring.
9. Pola deteksi: huruf untuk domain/nama, angka hanya untuk handle (lihat L7 butir 5).

### Jebakan harness (penyebab false-pass nyata 08-09)

1. **Platform diturunkan dari NAMA berkas frontier**: `frontier_<platform>.json`. Berkas uji
   WAJIB bernama persis (mis. `frontier_threads.json`). Nama lain divonis "rute belum ada" lalu
   dilewati TANPA error, sehingga 0 item menjadi false-pass. Setiap run uji harus memeriksa nama
   berkas terhadap daftar platform yang dikenal skrip.
2. **Baris keluaran = 0 wajib curiga**, bukan dianggap sukses. Selidiki urutan ini sebelum
   melapor: nama berkas frontier, claimed dedup terhadap `items.jsonl`, jendela tanggal, gerbang
   L7, lalu jaringan. Keluaran kosong yang sah selalu punya alasan tertulis (mis. frontier
   sudah claimed).
3. `entity_match=false` tidak boleh naik ke kolom terbit; item tanpa tanggal tidak dihitung
   dalam W1/P1. Label jendela (`W1`/`P1`/`pre-window`/`unknown`) harus dipetakan eksplisit oleh
   skrip metrik; ember `unknown` yang menampung pre-window membuat baseline salah dibaca.
4. `via_edge` boleh kosong pada lane tertentu; jangan melaporkan "jejak edge lengkap" tanpa
   mengukur kehadiran field per item.

## Perkakas (referensi pointer, jangan disalin ke sini)

| Perkakas | Kontrak | Isi |
|---|---|---|
| `keyword_expander.py` | 10.1 | 1 kata kunci -> `query_plan.json` (>= 12 varian, >= 5 kelas) |
| `referral_harvest.py` | 10.2 | korpus -> `graph_edges.jsonl` + `frontier_<platform>.json` + `recount_summary.json` (nol jaringan, deterministik) |
| `shortlink_resolve.py` | 10.3 | shortlink -> `url_kanonik.jsonl` (rantai status lengkap, gagal tercatat) |
| `harvest_per_id.py` | 10.4 | frontier -> `items.jsonl` via rute L3 per platform + ladder rows |
| `ladder_state.py` | 10.5 | catat baris LADDER ke `collection_report.md` (idempoten per rung) |
| `scope_filter.py` | L7 07 seksi 8 | gerbang `saring_edge` / `cek_final_url` / `cek_item` + `--selftest` + `--audit` |
| `README_crawler_expansion.md` | 10.6 | urutan pakai per skenario (pilot, lane pembanding, resume parsial) + tabel `--jobs` |

Format baris LADDER (sama di semua misi): `rung | URL/aksi | status HTTP + timestamp | hasil |
keputusan lanjut`.

## Pitfalls

- Jangan kumpulkan hanya judul/snippet - target konten penuh + metadata + engagement.
- Jangan abaikan `platform_limited` - laporan harus menyebutkan keterbatasan.
- Jangan hapus duplikat tanpa catatan di manifest.
- Jangan menyimpan kredensial atau melewati login wall.
- Jangan flood request - rate limit wajar; gunakan cache lokal antar batch.
- Jangan menulis item tanpa `source_url` - corpus tanpa URL tidak bisa disitasi.
- Jangan memvonis platform dari satu rung. Vonis per rung dengan status + timestamp; vonis
  platform hanya setelah empat kelas jalur terisi di LADDER.
- Jangan memakai path URL sebagai bukti author. Atribusi hanya dari isi respons endpoint.
- Jangan mengutip angka PoC occurrence sebagai jumlah id unik; jalankan recount lebih dulu.
- Jangan menganggap endpoint "belum teruji" sebagai endpoint hidup; kolom bukti menunjukkan
  status terukur terakhir.
- Jangan menulis frontier/items tanpa memanggil gerbang L7; jangan menyalin logika gerbang.
- Jangan menyaring opini politik; karantina dengan `review_manusia=true`, bukan penghancuran.
- Jangan menganggap `--jobs` besar sebagai jaminan kecepatan pada jalur satu host; ukur rasio.
- Jangan berhenti sukarela saat kuota iterasi masih longgar dan leads tersimpan masih ada (kejadian 07-09 misi PRABOWO-SOSMED: x-tiktok menutup dengan W1=4 item + sisa kerja ~20-30 iterasi padahal kuota belum habis; threads 4 < minimum 6). Aturan: sebelum menutup partial-handoff, habiskan dulu leads murah yang sudah tersimpan di `raw/` (promosikan kandidat jadi item penuh); partial-handoff sah hanya bila kuota riil tersisa <= ambang-B LAD ATAU jalur benar-benar habis (bukti LADDER lengkap), bukan karena ganti jalur yang mahal terasa melelahkan.

## Verifikasi

Sebelum selesai: `items.jsonl` >= 1 item valid, semua `source_url` ada, `manifest.json`
lengkap, spot-check 5 URL terbuka, jumlah item per platform tercatat, dan laporan
menyebutkan platform yang terbatas (jika ada).

Bila lane memakai perluasan v1.1, tambahannya:
1. `recount_summary.json` ditulis ke laporan SEBELUM angka target/delta dikutip.
2. LADDER lengkap empat kelas jalur, tiap baris punya status HTTP/rc + timestamp; kata "tipis"
   tidak dipakai sebagai vonis tanpa tangga habis.
3. Tabel kontribusi per kelas jalur (graph/direct/snowball/arsip) cocok dengan hitungan parser
   atas `provenance.path` atau `path_class` (sebutkan satuan yang dipakai).
4. Sampling item panen graph: teks dan author cocok dengan raw payload respons endpoint;
   `via_edge` merujuk `edge_id` nyata (bila lane menyimpannya).
5. Identitas L7 berlaku per aliran (`N_masuk = N_lolos + N_quarantine`); `scope_filter.py
   --selftest` exit 0; bypass test 4 jalur tidak menemukan jalur lolos-diam-diam.
6. Determinisme: dua run atas input sama byte-identik (`--stable-output` + `GSP_FIXED_NOW`).
7. Tabel VERIFIKASI-AKURASI SPK-002 menempel di kartu penutup; rilis hanya bila SALAH-TARGET 0.

## Changelog

- **1.4.0 (2026-09-11, misi WF-CRAWL-0911 kartu t_7387e10f)** - seksi NORMA DUA-MESIN PARALEL
  menjadi NORMA FAN-OUT MULTI-ALAT PARALEL (tiga alat hidup; putusan user D-06, benchmark
  crawl4ai lolos rubrik terkunci): ekstraksi/render disebarkan paralel ke Firecrawl :3002 DAN
  crawl4ai venv produksi (sejajar, bukan fallback berjenjang); plafon per-misi <=8 lane TOTAL
  lintas-alat (firecrawl N=4/pekerja + crawl4ai <=2 proses/pekerja); tangga fallback menjadi
  darurat-per-alat; lapis KUMPUL->DEDUP wajib sebelum analisa lewat skrip kanonik
  `skills/gsp-vendor-crawler/scripts/dedup_harvest.py` (butir 5 norma, butir 6 Tahap 3,
  artefak `dedup/` di Tahap 5). Routing sumber gratis per platform tidak diubah.
- **1.3.0 (2026-09-11, misi WF-CRAWL-0911 kartu t_893fd521)** - seksi NORMA DUA-MESIN PARALEL
  setelah Tahap 2: pencarian primer SearXNG :8080 dan ekstraksi primer Firecrawl :3002 menjadi
  norma eksplisit (pointer ke resep gsp-searxng/gsp-firecrawl, tanpa duplikasi); plafon
  per-pekerja N=4 dan per-misi <= 8 lane firecrawl dirujuk ke kapasitas mesin
  (MAX_CONCURRENT_JOBS=16); `--jobs` clamp maks 8 tetap berlaku untuk skrip harvest beku;
  tangga fallback bersyarat-tercatat (mesin mati terbukti -> ddgs boleh dengan bukti di
  manifest/LADDER; fallback senyap = pelanggaran). Routing sumber gratis per platform tidak
  diubah.
- **1.2.1 (2026-09-09, misi PATEN-AKHIR-0909 kartu t_82b85e36)** - satu revisi tercatat: TAMBAH satu baris pointer lapis kendali ke payung `gsp-social-intel-orchestration` v2.0.0 di blok pembuka; tidak ada norma tangga/L1-L7 yang diubah; snapshot pra-amandemen v1.2.0 tersimpan ber-sha di laporan distribusi DIST (sha256 2f23742e...).
- **1.2.0 (2026-09-09, misi GAP-FILL-0909 kartu t_af1b1084)** - seksi "Field-wajib panen": empat
  kelas field wajib (views/tayang, reply_to/quote, followers, likes komentar) dengan jalur
  ekstraksi dan ambang null per platform; aturan wajib simpan-field-mentah-jangan-dibuang sebagai
  akar kekurangan perbaikan dari vonis kehilangan field blueprint GAP-FILL §1.3 atas korpus pbw0907;
  pointer ke lampiran SPEC §2 dan ke skema payload v1.2 di paten gsp-sosmed-html-insight.
- **1.1.0 (2026-09-08, misi CRAWLER-EXPAND-0908)** - resep perluasan jangkauan dari blueprint
  06 + addendum L7 07 + README perkakas, semua kartu hulu PASS (VERIF4 9/9, VERIF5 7/7):
  seksi L1 pelebar kata kunci, L2 snowball, **TANGGA** eskalasi L3 per platform dengan endpoint
  terbukti hidup dan ambang mati per rung, **REFERRAL GRAPH** L4 kelas satu (panen tepi, recount
  prasyarat, shortlink wajib resolve, BFS depth 2, atribusi dari isi respons, vonis empat kelas),
  **gerbang L7** scope-filter (satu titik wajib per alur, karantina tercatat non-destruktif,
  dua sumbu ortogonal, larangan sensor opini, bypass test 4 jalur sebagai template audit),
  L5 ambang anti-berhenti-dini prosedural, L6 teknik dasar (`--jobs` + HostScheduler per-host,
  plafon render-proxy satu host 1,42x, cache kunci method+body, timeout render 75 dtk), seksi
  jebakan harness (nama berkas frontier, keluaran 0 baris wajib curiga), perluasan seksi
  Verifikasi, dan penambahan berkas wajib di Tahap 5.
- **1.0.x (2026-08-24 s.d. 2026-09-08)** - pipeline 6 tahap, routing sumber gratis per platform,
  normalisasi/dedup, arsip/manifest, handoff; pitfall berhenti-dini ditambahkan 08-09 pasca
  misi PRABOWO-SOSMED-0907.
