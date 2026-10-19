---
name: gsp-crawl4ai
description: "Web crawling and scraping tool with LLM-optimized output. 网页爬虫爬取工具 | Web crawler, web scraper, spider. DuckDuckGo search, site crawling, dynamic page scraping. 智能搜索爬取 | Free, no API key required."
version: 1.2.0
author: Lancelin
license: MIT-0
repository: https://github.com/lancelin111/crawl4ai-skill
homepage: https://github.com/lancelin111/crawl4ai-skill
pypi: crawl4ai-skill
issues: https://github.com/lancelin111/crawl4ai-skill/issues
tags:
  - web-scraping
  - web-crawling
  - crawler
  - scraper
  - spider
  - search
  - markdown
  - llm
  - token-optimization
  - duckduckgo
  - crawl
  - scrape
  - 爬虫
  - 爬取
  - 网页抓取
requires:
  bins:
    - crawl4ai-skill
---

# Crawl4AI Skill - Web Crawler & Scraper

STATUS PERAN (WF-CRAWL-0911 D-06, 11-09): alat akuisisi SEJAJAR dalam fan-out multi-alat paralel. Kelas workflow koleksi menyebarkan akuisisi ke semua alat yang hidup serentak - SearXNG (pencarian), Firecrawl dan crawl4ai (ekstraksi/crawl) - hasil digabung di lapis KUMPUL lalu DEDUP (kunci URL ternormalisasi + hash konten) sebelum analisa. Berlaku sejak putusan user D-06 setelah benchmark lolos rubrik terkunci: rujukan kontrak §9 docs/2026-09-11-firecrawl-searxng-parallel-enforcement/contract.md + evidence/BENCHMARK-CRAWL4AI.md (vonis IMPROVEMENT_SAH). Status lama 'fallback historis' dicabut.

**Web Crawling 网页爬虫 | Web Scraping 网页爬取 | LLM 优化输出**

智能网页爬虫和爬取工具，支持搜索、全站爬取、动态页面抓取。Free web crawler and scraper with LLM-optimized Markdown output.

## 核心功能 | Core Features

- 🔍 **Web Search 网页搜索** - DuckDuckGo search, 免 API key
- 🕷️ **Web Crawling 网页爬虫** - Site crawler, spider, sitemap 识别
- 📝 **Web Scraping 网页抓取** - Smart scraper, data extraction
- 📄 **LLM-Optimized Output** - Fit Markdown, 省 Token 80%
- ⚡ **Dynamic Page Scraping** - JavaScript 渲染页面爬取

---

## 快速开始 | Quick Start

### 安装 | Installation

```bash
pip install crawl4ai-skill
```

### Web Search | 网页搜索

```bash
# Search the web with DuckDuckGo
crawl4ai-skill search "python web scraping"
```

### Web Scraping | 单页爬取

```bash
# Scrape a single web page
crawl4ai-skill crawl https://example.com
```

### Web Crawling | 全站爬虫

```bash
# Crawl entire website / spider
crawl4ai-skill crawl-site https://docs.python.org --max-pages 50
```

---

## PENGGUNAAN PRODUKSI (WF-CRAWL-0911)

Jalur produksi = library Python (bukan CLI `crawl4ai-skill`) lewat venv permanen:
interpreter `C:/Users/TRIAL/gsp-tools/c4ai/Scripts/python.exe` (crawl4ai 0.9.3, Playwright Chromium ms-playwright).

Resep teruji (self-check pembuat 11-09 terhadap venv ini: 3/3 sukses termasuk halaman JS-only, 2,81 s):

```python
import asyncio
from crawl4ai import AsyncWebCrawler, CrawlerRunConfig, CacheMode

async def main(urls):
    cfg = CrawlerRunConfig(cache_mode=CacheMode.BYPASS)
    async with AsyncWebCrawler() as crawler:
        results = await crawler.arun_many(urls, config=cfg)
    return results

asyncio.run(main(["https://example.com", "https://quotes.toscrape.com/js/"]))
```

- PITFALL: `cache_buster` BUKAN argumen sah `CrawlerRunConfig` di versi ini (terukur TypeError 11-09). Untuk bypass cache pakai `cache_mode=CacheMode.BYPASS`.
- Render JS terbukti: `https://quotes.toscrape.com/js/` memuat marker kutipan+Einstein di markdown keluaran (konten hasil render, bukan shell kosong).
- Keunggulan atas firecrawl build lokal: depth crawl penuh dengan kontrol maxDepth (build firecrawl lokal menolak depth/maxDepth, terukur 11-09) dan ekstraksi markdown LLM-free.

### Plafon operasi
- Maksimal 2 proses crawler serentak per pekerja (Chromium berat; browser ms-playwright dipakai bersama proses lain).
- Ikut plafon misi: <= 8 lane total lintas-alat (firecrawl N=4/pekerja + crawl4ai + SearXNG).

### Benchmark ringkas (rubrik terkunci sebelum hasil, 11-09; bukti penuh evidence/BENCHMARK-CRAWL4AI.md)

| Metrik | crawl4ai | firecrawl :3002 | Rasio |
|---|---|---|---|
| scrape paralel-4 wall | 596 ms | 1275 ms | 0,47x (lebih cepat) |
| scrape serial-4 wall | 1818 ms | 2656 ms | 0,68x (lebih cepat) |
| sukses URL | 4/4 | 4/4 | setara |
| render JS (quotes/js/) | OK, marker hadir | OK | setara fungsi |

Biaya disk: venv ~572 MB; ms-playwright ~1,4 GB (browser dipakai bersama). Vonis rubrik: IMPROVEMENT_SAH (A-1..A-3 LULUS).

---

## 使用场景 | Use Cases

### 场景 1：Web Crawler for Documentation | 文档站爬虫

```bash
# Crawl documentation site with spider
crawl4ai-skill crawl-site https://docs.fastapi.com --max-pages 100
```

**爬虫效果 | Crawler Output:**
- ❌ 移除：导航栏、侧边栏、广告
- ✅ 保留：标题、正文、代码块
- 📊 **Token：50,000 → 10,000（-80%）**

### 场景 2：Search + Scrape | 搜索+爬取

```bash
# Search and scrape top results
crawl4ai-skill search-and-crawl "Vue 3 best practices" --crawl-top 3
```

### 场景 3：Dynamic Page Scraping | 动态页面抓取

JavaScript 渲染的页面爬取（雪球、知乎等）：

```bash
# Scrape JavaScript-heavy pages
crawl4ai-skill crawl https://xueqiu.com/S/BIDU --wait-until networkidle --delay 2
```

---

## 命令参考 | Commands

| 命令 Command | 说明 Description |
|------|------|
| `search <query>` | Web search 网页搜索 |
| `crawl <url>` | Web scraping 单页爬取 |
| `crawl-site <url>` | Web crawling 全站爬虫 |
| `search-and-crawl <query>` | Search + scrape 搜索并爬取 |

### 常用参数 | Common Options

```bash
# Web Search 搜索
--num-results 10          # Number of results

# Web Scraping 爬取
--format fit_markdown     # Output format
--output result.md        # Output file
--wait-until networkidle  # Wait strategy for dynamic pages
--delay 2                 # Additional wait time (seconds)
--wait-for ".selector"    # Wait for specific element

# Web Crawling 爬虫
--max-pages 100          # Max pages to crawl
--max-depth 3            # Max crawl depth
```

---

## 输出格式 | Output Formats

### fit_markdown（推荐 Recommended）

智能提取，节省 80% Token。Smart extraction, save 80% tokens.

```bash
crawl4ai-skill crawl https://example.com --format fit_markdown
```

### raw_markdown

保留完整结构。Preserve full structure.

```bash
crawl4ai-skill crawl https://example.com --format raw_markdown
```

---

## 为什么选择这个爬虫？| Why This Crawler?

✅ **免费爬虫 Free Crawler** - 无需 API key，开箱即用  
✅ **智能爬取 Smart Scraper** - 自动去噪，提取核心内容  
✅ **全站爬虫 Site Crawler** - 支持 sitemap，递归爬取  
✅ **动态爬取 Dynamic Scraping** - JavaScript 渲染页面支持  
✅ **搜索集成 Search Integration** - DuckDuckGo 搜索内置  

---

## Changelog

- 1.2.0 (2026-09-11, WF-CRAWL-0911 D-06): STATUS PERAN menjadi alat akuisisi sejajar dalam fan-out multi-alat paralel (putusan user D-06, benchmark lolos rubrik terkunci); seksi baru PENGGUNAAN PRODUKSI (venv permanen + resep AsyncWebCrawler/CacheMode.BYPASS + pitfall cache_buster + plafon 2 proses/pekerja + tabel benchmark + biaya disk).
- 1.1.1 dan sebelumnya: status 'fallback historis' (pra-D-06).

---

## 链接 | Links

- 📦 [PyPI](https://pypi.org/project/crawl4ai-skill/)
- 💻 [GitHub](https://github.com/lancelin111/crawl4ai-skill/)
- 🦞 [ClawHub](https://clawhub.com/skills/crawl4ai-skill)
