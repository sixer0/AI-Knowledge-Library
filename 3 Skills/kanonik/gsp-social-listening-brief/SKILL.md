---
name: gsp-social-listening-brief
description: Use when the user wants a social listening report about what people are saying about a brand, person, product, topic, category, or niche across public social platforms. Produces cited themes, sentiment caveats, notable posts, and recommended actions.
allowed-tools: Bash, Read, Write, WebFetch

version: 1.0.1
author: ScrapeCreators
license: MIT
homepage: https://scrapecreators.com
repository: https://github.com/ScrapeCreators/social-media-research-skills
metadata:
  gsp:
    adapted: true
    note: "Jalur gratis: tidak butuh SCRAPECREATORS_API_KEY. Gunakan resource GSP lokal (searxng, firecrawl, browser) sebagai pengganti."
    tags:
      - social-media
      - research
      - listening
---

# Social Listening Brief


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: [`skills/gsp/gsp-document-quality-standards/SKILL.md`](../../registry-fleet/gsp-document-quality-standards/SKILL.md) **Module L**
(ringkasan: [`skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`](../../registry-fleet/gsp-document-quality-standards/references/koridor-dokumen.md)).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## Overview

Research what people are saying publicly across social platforms. This is useful for brand monitoring, category research, product feedback, reputation checks, and understanding recent conversations.

## When to Use

Use this skill when the user asks:

- what are people saying about X?
- monitor this brand/topic/category
- find complaints or praise about a product
- summarize recent social discussion
- compare sentiment across Reddit, TikTok, YouTube, LinkedIn, Instagram, or Threads

## Useful Sources

> **Jalur gratis GSP (tanpa API berbayar):** gunakan resource lokal berikut sebagai pengganti ScrapeCreators API:
> - **Web search:** `gsp-searxng` (SearXNG lokal `http://localhost:8080`) untuk Google/Bing/Reddit search agregasi.
> - **Ekstraksi halaman:** `gsp-firecrawl` (Firecrawl lokal `http://localhost:3002`) + `web_extract` untuk halaman JS-heavy/anti-bot dasar.
> - **Browser fallback:** tool `browser` untuk halaman yang butuh rendering penuh (TikTok, Instagram, Threads, LinkedIn public pages).
> - **Reddit:** endpoint JSON publik `https://www.reddit.com/r/<sub>/search.json?q=<topic>&restrict_sr=1` + `old.reddit.com` (tanpa auth, rate-limit wajar).
> - **YouTube:** skill `youtube-content` (transkrip), RSS feed kanal `https://www.youtube.com/feeds/videos.xml?channel_id=<id>`, dan `yt-dlp` bila tersedia.
> - **Bluesky:** API publik atproto (tanpa key): `https://public.api.bsky.app/xrpc/app.bsky.feed.searchPosts?q=<topic>`.
> - **Arsip/paywall:** `https://archive.org/wayback/available?url=<u>` dan `r.jina.ai` (free tier) sebagai fallback ekstraksi.

- Reddit search, subreddit search, posts, comments
- TikTok search top/keyword/hashtag dan comments
- YouTube search, transcripts, comments
- Instagram reels search dan hashtag search
- LinkedIn post search
- Threads search
- Google search when platform search is not enough

## Workflow

1. Define topic, aliases, competitor names, and date window.
2. Search multiple relevant sources, not every source blindly.
3. Keep URLs, dates, platform, engagement metrics, and exact quotes.
4. Cluster conversations into themes.
5. Separate positive, negative, neutral, and mixed signals.
6. Highlight representative examples and action items.

## Output Format

```markdown
# Social Listening Brief: {topic}

## Executive Summary
- Main takeaway:
- Conversation volume: Low/Medium/High
- Sentiment: Positive/Neutral/Negative/Mixed
- Confidence: High/Medium/Low

## Top Themes
| Theme | Sentiment | Evidence | Representative quote/source |
|---|---|---|---|

## Notable Posts
- [source](url) — why it matters

## Risks / Opportunities
- ...

## Recommended Actions
1. ...
```

## Common Pitfalls

- Do not pretend this is exhaustive social monitoring. It is public-data research.
- Do not average sentiment across very different communities without caveats.
- Do not use engagement as a proxy for truth.
