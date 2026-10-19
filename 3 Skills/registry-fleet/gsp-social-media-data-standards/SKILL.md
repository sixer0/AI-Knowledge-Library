---
name: gsp-social-media-data-standards
description: "Standar pengelolaan data sosial media GSP: provenance, citable corpus, dedup, arsip, etika. ALWAYS LOAD untuk agen social-media-analyst & social-media-crawler. Gunakan sebelum mengumpulkan/menganalisis data sosial untuk memastikan insight akurat dan dapat disitasi."
version: 1.0.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux]
metadata:
  gsp:
    category: intelligence
    tags: [social-media, data-governance, provenance, citation, corpus, ethics]
---

# GSP Social Media Data Standards

> Standar wajib pengelolaan data sosial media di lingkungan GSP. Tujuannya satu:
> **setiap insight harus akurat, dapat diaudit, dan dapat disitasi** — bukan opini model,
> bukan middle-information. Terapkan standar ini di SELURUH siklus data: koleksi, arsip,
> analisis, pelaporan.

## Prinsip Inti

1. **Data asli dipertahankan.** Jangan pernah meringkas/menafsirkan data mentah tanpa menyimpan
   salinan aslinya (teks, URL, tanggal, metrik engagement, penulis).
2. **Sitasi wajib.** Setiap klaim dalam laporan harus bisa ditelusuri ke sumber: URL + kutipan
   persis + platform + tanggal publikasi + tanggal koleksi.
3. **Tanpa metrik karangan.** Tidak boleh mengarang angka engagement, follower, atau volume.
   Jika data tidak tersedia → nyatakan "tidak tersedia" / "blocked", jangan estimasi diam-diam.
4. **Konteks lebih penting dari angka.** Engagement ≠ kebenaran. Volume ≠ sentimen. Sampel ≠ sensus.
5. **Jalur gratis dulu.** Gunakan resource GSP lokal (searxng, firecrawl, browser, API publik
   gratis) sebelum API berbayar.

## Skema Item Corpus (wajib untuk tiap item)

Simpan sebagai JSONL dengan field berikut (snake_case):

```json
{
  "item_id": "sha256 pendek dari canonical_hash",
  "platform": "reddit|youtube|tiktok|instagram|threads|linkedin|x|bluesky|pinterest|web|other",
  "source_url": "URL kanonik publik",
  "author": {"handle": "...", "display_name": "...", "profile_url": "..."},
  "published_at": "ISO8601 UTC",
  "collected_at": "ISO8601 UTC",
  "content": {"text": "...", "lang": "id|en|...", "media_refs": ["..."]},
  "engagement": {"likes": 0, "comments": 0, "shares": 0, "views": 0, "reposts": 0},
  "sentiment": null,
  "topic_labels": [],
  "canonical_hash": "sha256:...",
  "raw_payload_path": "relative/path/ke/arsip/mentah",
  "collection_job": "job_id",
  "provenance": "searxng|firecrawl|browser|reddit_json|yt_rss|atproto|manual"
}
```

- `sentiment` diisi oleh ANALISIS (bukan kolektor) dan harus menyertakan skema label:
  `-1..+1` atau `negative|neutral|positive|mixed` + `sentiment_confidence`.
- `canonical_hash` = `sha256(normalized_text + author_handle + publish_day)` untuk dedup.

## Standar Koleksi

- **Publik saja & patuh ToS:** hanya data yang bisa diakses publik tanpa autentikasi.
  Jangan menembus login wall, captcha, atau anti-bot dengan cara tidak sah.
- **Robots & rate-limit:** hormati `robots.txt`, beri jeda antar request, batasi kedalaman.
- **Jangan over-koleksi PII:** hindari menyimpan data pribadi yang tidak relevan dengan topik.
- **Sensus vs sampel:** label kan setiap corpus apakah census (semua posting dalam window)
  atau sampel (sebutkan kriteria sampling). Jangan pernah menyajikan sampel sebagai sensus.
- **Freshness:** simpan `collected_at` dan `published_at` terpisah. Insight "sekarang" harus
  memakai data ≤ 7 hari kecuali konteks menyatakan lain.

## Standar Arsip

Setiap job koleksi menghasilkan folder kerja dengan struktur:

```
<workspace>/social/<job_id>/
├── raw/                    # snapshot mentah: html/json (per platform, per sumber)
├── items.jsonl             # corpus normal (skema di atas)
├── manifest.json           # metadata job: topik, platform, window, metode, batasan, jumlah item
└── collection_report.md    # ringkasan koleksi + kendala
```

`manifest.json` minimal: `{job_id, topic, aliases, platforms, window_start, window_end,
collected_at, methods, total_items, dedup_removed, limitations, ethics_notes}`.

## Standar Analisis & Sitasi

- **Rantai bukti:** klaim → (item_id / source_url) → kutipan persis → platform + tanggal.
- **Triangulasi:** temuan lintas-platform (≥2 sumber independen) = confidence tinggi;
  temuan 1 platform = label "single-platform"; temuan 1 item = "anecdotal".
- **Caveat wajib:** sebutkan ukuran sampel, window waktu, bias platform, kemungkinan bot/
  inorganik, dan perbedaan komunitas. Jangan merata-rata sentimen antar komunitas yang
  sangat berbeda tanpa caveat.
- **Format kutipan posting:**
  `[Platform] @handle, "kutipan persis…", <URL>, dipublikasikan <tanggal>, diakses <tanggal koleksi>`
- **Gate kualitas sebelum laporan:** ceklis QA (lihat gsp-social-media-analysis-workflow):
  corpus cukup?, URL valid?, kutipan persis?, metrik asli?, caveat tercantum?

## Pitfalls

- Jangan menyebut hasil pencarian web sebagai "semua yang ada di platform X".
- Jangan mengganti angka yang gagal diambil dengan angka dari sumber lain tanpa label.
- Jangan menghapus konteks negatif agar laporan terlihat baik — laporan harus netral.
- Jangan menyimpan data sosial di luar struktur `social/` tanpa manifest.

## Verifikasi

Sebelum menyatakan pekerjaan selesai: `items.jsonl` valid JSONL, semua `source_url` dapat
dibuka (spot-check), `manifest.json` terisi lengkap, dan setiap klaim laporan punya
`item_id` atau `source_url` yang tercantum di corpus.
