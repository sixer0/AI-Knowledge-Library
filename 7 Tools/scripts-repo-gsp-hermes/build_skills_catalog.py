#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Kompilasi katalog lengkap skill dari skills_catalog_raw.json → markdown."""
import json, os

RAW = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/skills_catalog_raw.json"
OUT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/katalog_skill_lengkap.md"

with open(RAW, encoding="utf-8") as f:
    entries = json.load(f)

# order kategori: orchestration & gsp dulu (inti GSP), lalu alfabetis
def cat_order(c):
    if c == "orchestration": return 0
    if c == "gsp": return 1
    return 2
cats = {}
for e in entries:
    cats.setdefault(e["category"], []).append(e)
ordered = sorted(cats.items(), key=lambda kv: (cat_order(kv[0]), kv[0].lower()))

def fmt_size(n):
    if n >= 1024: return f"{n/1024:.1f} KB"
    return f"{n} B"

def render_entry(e):
    L = []
    badge = " *(kanonik EKAS)*" if e["root"] == "kanonik" and e["category"] == "gsp" else ""
    L.append(f"### {e['name']}{badge}")
    L.append("")
    L.append(f"- **Kategori:** `{e['category']}` · **Lokasi:** `{e['relpath']}`")
    meta = []
    if e.get("version"): meta.append(f"versi {e['version']}")
    if e.get("author"): meta.append(f"author {e['author']}")
    if e.get("license"): meta.append(f"lisensi {e['license']}")
    if e.get("platforms"): meta.append(f"platform {e['platforms']}")
    if meta: L.append(f"- **Metadata:** {', '.join(meta)}")
    if e.get("tags"):
        L.append(f"- **Tags:** {e['tags']}")
    if e.get("description"):
        desc = e["description"].replace("\n", " ")
        L.append(f"- **Deskripsi:** {desc}")
    if e.get("when"):
        L.append(f"- **Pemicu (When to Use):** {e['when']}")
    if e.get("sections"):
        secs = ", ".join(h[1].strip() for h in e["sections"][:14])
        L.append(f"- **Struktur bagian ({len(e['sections'])}):** {secs}{' …' if len(e['sections'])>14 else ''}")
    if e.get("linked"):
        L.append(f"- **File pendukung ({len(e['linked'])}):**")
        for lf in e["linked"]:
            L.append(f"  - `{lf['kind']}/{lf['path'].split('/')[-1]}` — {fmt_size(lf['size'])}")
    L.append(f"- **Ukuran body:** {e['body_chars']} karakter")
    L.append("")
    return "\n".join(L)

lines = []
lines.append("# KATALOG LENGKAP SKILL — EKOSISTEM BRAHMA GSP")
lines.append("")
lines.append("**Sumber:** registry default `AppData/Local/hermes/skills` + kanonik `workspace/gsp-hermes/skills` · **Tanggal:** 24 Agustus 2026 · **Total: 130 skill unik** (19 kategori)")
lines.append("")
lines.append("## Ringkasan Katalog")
lines.append("")
lines.append("| Kategori | Jumlah skill | Dengan template | Dengan script | Dengan referensi |")
lines.append("|---|---|---|---|---|")
tot_t = tot_s = tot_r = 0
for cat, items in ordered:
    t = sum(1 for e in items if any(x["kind"] == "templates" for x in e["linked"]))
    s = sum(1 for e in items if any(x["kind"] == "scripts" for x in e["linked"]))
    r = sum(1 for e in items if any(x["kind"] == "references" for x in e["linked"]))
    tot_t += t; tot_s += s; tot_r += r
    lines.append(f"| {cat} | {len(items)} | {t} | {s} | {r} |")
lines.append(f"| **Total** | **{len(entries)}** | **{tot_t}** | **{tot_s}** | **{tot_r}** |")
lines.append("")
lines.append("> Catatan: skill per-profil (`profiles/gsp-*/skills/`) adalah salinan dari registry/kanonik sesuai daftar ALWAYS LOAD / ON DEMAND di SOUL.md tiap profil; tidak dihitung ganda di katalog ini.")
lines.append("")
for cat, items in ordered:
    lines.append(f"## Kategori: {cat} ({len(items)} skill)")
    lines.append("")
    for e in items:
        lines.append(render_entry(e))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("\n".join(lines))
print("written:", OUT)
print("size:", os.path.getsize(OUT), "bytes")
