#!/usr/bin/env python3
"""
legacy_knowledge_map.py — peta pengetahuan per proyek dari legacy-archive.

Untuk tiap proyek top-level: struktur 2 tingkat, artefak kunci (final/report/
index/laporan/proposal/masterplan/ringkasan), file terbesar, judul H1 dari
beberapa file md penting. Output markdown ke stdout untuk panduan kurasi.

TIDAK menulis apapun ke vault — hanya analisis (membaca).
"""
import json, re, sys
from pathlib import Path

ROOT = Path("C:/Users/TRIAL/workspace/gsp-hermes/workspace/legacy-archive")
MANIFEST = ROOT / "manifest.json"

KEY_HINTS = ("final", "report", "index", "laporan", "proposal", "masterplan",
             "ringkasan", "summary", "executive", "brief", "00_", "01_",
             "assembled", "translated", "structured", "05_insights", "manifest")

def h1(path: Path, maxlen=200):
    try:
        txt = path.read_text("utf-8", errors="replace")[:4000]
    except Exception:
        return ""
    for line in txt.splitlines():
        if line.startswith("# "):
            return line[2:].strip()[:maxlen]
    return ""

def main():
    files = json.loads(MANIFEST.read_text("utf-8"))
    # kelompok per proyek top-level (sebelum '/')
    proj = {}
    for f in files:
        top = f["rel"].split("/", 1)[0]
        proj.setdefault(top, []).append(f)
    out = []
    for top in sorted(proj, key=lambda t: -len(proj[t])):
        fl = proj[top]
        out.append(f"\n## PROYEK: {top}  ({len(fl)} file, {sum(x['size'] for x in fl)/1e6:.1f} MB)")
        # struktur 2 tingkat
        out.append("### Struktur (2 level)")
        lvl2 = {}
        for f in fl:
            parts = f["rel"].split("/")
            if len(parts) >= 3:
                key = f"{parts[1]}/{parts[2]}"
            elif len(parts) == 2:
                key = parts[1] + "/"
            else:
                key = "(root)"
            lvl2.setdefault(key, []).append(f)
        for k, v in sorted(lvl2.items(), key=lambda kv: -len(kv[1])):
            out.append(f"- `{k}` : {len(v)} file")
        # artefak kunci
        out.append("### Artefak kunci (pola final/report/index/proposal/dll)")
        keyf = [f for f in fl if any(h in f["rel"].lower() for h in KEY_HINTS)]
        for f in sorted(keyf, key=lambda x: -x["size"])[:25]:
            abs = ROOT / f["rel"]
            h = h1(abs) if f["ext"] in (".md", ".markdown") else ""
            extra = f" — “{h}”" if h else ""
            out.append(f"- [{f['size']/1e3:.0f}KB] `{f['rel']}`{extra}")
        # file terbesar
        out.append("### File terbesar")
        for f in sorted(fl, key=lambda x: -x["size"])[:8]:
            out.append(f"- [{f['size']/1e6:.1f}MB] `{f['rel']}`")
    Path(ROOT / "knowledge_map.md").write_text("\n".join(out), "utf-8")
    print(f"knowledge_map ditulis: {ROOT/'knowledge_map.md'}")

if __name__ == "__main__":
    main()
