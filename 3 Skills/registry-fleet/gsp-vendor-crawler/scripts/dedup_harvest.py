#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""dedup_harvest.py - lapis KUMPUL -> DEDUP norma FAN-OUT MULTI-ALAT (WF-CRAWL-0911 D-06).

Deterministik dan idempoten (stdlib saja). Input: satu atau lebih berkas harvest
JSONL (satu objek per baris) atau JSON (list objek) dengan kolom url, konten,
sumber, ts. Normalisasi URL: host lowercase, fragment dibuang, parameter utm_*
dibuang, trailing slash path dibuang. Kunci unik = (url ternormalisasi,
sha256(markdown ternormalisasi whitespace)). Output di --out-dir:
  unique.jsonl - satu baris per kunci unik; rekaman terpilih = sumber pertama
                 (ts terkecil, lalu urutan baca); kolom `sumber` = sumber terpilih,
                 `sumber_kembar` = daftar semua sumber pada grup (termasuk terpilih).
  report.md    - laporan duplikat: jumlah + contoh grup.
  report.json  - laporan mesin (salin ke manifest/LADDER).
Idempoten: run ulang dengan input sama menulis byte identik; bila isi output
sudah sama, file tidak disentuh (mtime utuh) dan laporan menyebut unchanged.
Urutan output ditentukan kunci (bukan waktu): tidak memakai clock maupun seed acak.
Exit: 0 sukses; 2 tidak ada baris sah pada input.
"""
import argparse
import hashlib
import json
import os
import sys
import unicodedata
from urllib.parse import urlsplit, urlunsplit, parse_qsl, urlencode

UTM_PREFIX = "utm_"


def load_records(path):
    """Baca JSONL (baris objek) atau JSON (list objek). Return list dict."""
    with open(path, "r", encoding="utf-8") as fh:
        text = fh.read()
    stripped = text.lstrip()
    if stripped.startswith("["):
        data = json.loads(text)
        if not isinstance(data, list):
            raise ValueError("%s: JSON root bukan list" % path)
        return [r for r in data if isinstance(r, dict)]
    recs = []
    for i, line in enumerate(text.splitlines(), 1):
        line = line.strip()
        if not line:
            continue
        try:
            obj = json.loads(line)
        except json.JSONDecodeError as exc:
            raise ValueError("%s:%d baris tidak valid: %s" % (path, i, exc))
        if isinstance(obj, dict):
            recs.append(obj)
    return recs


def normalize_url(url):
    """Host+scheme lowercase, fragment dibuang, utm_* dibuang, trailing slash path dibuang."""
    parts = urlsplit(str(url).strip())
    scheme = parts.scheme.lower()
    netloc = parts.netloc.lower()
    path = parts.path
    if path.endswith("/"):
        path = path.rstrip("/")
    query_pairs = [(k, v) for (k, v) in parse_qsl(parts.query, keep_blank_values=True)
                   if not k.lower().startswith(UTM_PREFIX)]
    query = urlencode(query_pairs)
    return urlunsplit((scheme, netloc, path, query, ""))


def canonical_text(content):
    """NFC + whitespace collapse (newline/spasi ganda/tab -> satu spasi, strip tepi)."""
    s = unicodedata.normalize("NFC", str(content))
    return " ".join(s.split())


def content_hash(content):
    return hashlib.sha256(canonical_text(content).encode("utf-8")).hexdigest()


def rep_key(item):
    """Urutan penentu sumber pertama: ts (lexicografis ISO), lalu (file, seq)."""
    rec, fi, seq = item
    ts = str(rec.get("ts") or "")
    return (ts, fi, seq)


def build(inputs):
    """KUMPUL -> grup per kunci unik -> entri unique + statistik. Deterministik."""
    files = sorted(os.path.abspath(p) for p in inputs)
    groups = {}
    stats = {"inputs": [], "total_records": 0, "parse_errors": 0}
    for fi, path in enumerate(files):
        n_ok = 0
        try:
            recs = load_records(path)
        except (ValueError, json.JSONDecodeError) as exc:
            sys.stderr.write("ERROR %s\n" % exc)
            stats["parse_errors"] += 1
            stats["inputs"].append({"file": os.path.basename(path), "records": 0,
                                    "error": str(exc)})
            continue
        for seq, rec in enumerate(recs):
            url = str(rec.get("url") or "").strip()
            if not url:
                continue
            n_ok += 1
            nurl = normalize_url(url)
            chash = content_hash(rec.get("konten", ""))
            groups.setdefault((nurl, chash), []).append((rec, fi, seq))
        stats["inputs"].append({"file": os.path.basename(path), "records": n_ok})
        stats["total_records"] += n_ok

    unique_entries = []
    dup_groups = []
    for (nurl, chash), items in groups.items():
        items_sorted = sorted(items, key=rep_key)
        rec0, fi0, seq0 = items_sorted[0]
        src_list = []
        for rec, fi, seq in items_sorted:
            src = str(rec.get("sumber") or "unknown")
            if src not in src_list:
                src_list.append(src)
        entry = {
            "url": nurl,
            "url_asal": str(rec0.get("url") or ""),
            "content_sha256": chash,
            "sumber": src_list[0],
            "sumber_kembar": src_list,
            "ts": rec0.get("ts"),
            "konten": rec0.get("konten", ""),
        }
        unique_entries.append(((nurl, chash), entry))
        if len(items_sorted) > 1:
            dup_groups.append({
                "url": nurl,
                "content_sha256": chash,
                "n_rekaman": len(items_sorted),
                "sumber_kembar": src_list,
                "sumber_terpilih": src_list[0],
                "file_asal": sorted({files[fi] for _, fi, _ in items_sorted}),
            })
    unique_entries.sort(key=lambda kv: kv[0])
    dup_groups.sort(key=lambda g: (g["url"], g["content_sha256"]))
    stats["unique"] = len(unique_entries)
    stats["dup_removed"] = stats["total_records"] - stats["unique"]
    stats["dup_groups"] = dup_groups
    return unique_entries, stats


def render_report_md(stats):
    lines = []
    lines.append("# LAPORAN DEDUP HARVEST (dedup_harvest.py)")
    lines.append("")
    lines.append("| Metrik | Nilai |")
    lines.append("|---|---|")
    lines.append("| Berkas input | %d |" % len(stats["inputs"]))
    lines.append("| Baris tidak sah (parse error) | %d |" % stats["parse_errors"])
    lines.append("| Total rekaman dibaca | %d |" % stats["total_records"])
    lines.append("| Unik (keluaran unique.jsonl) | %d |" % stats["unique"])
    lines.append("| Duplikat dibuang | %d |" % stats["dup_removed"])
    lines.append("| Grup kembar (>1 rekaman) | %d |" % len(stats["dup_groups"]))
    lines.append("")
    lines.append("## Berkas input")
    lines.append("")
    for inp in stats["inputs"]:
        err = (" ERROR: " + inp["error"]) if inp.get("error") else ""
        lines.append("- `%s`: %d rekaman%s" % (inp["file"], inp["records"], err))
    lines.append("")
    lines.append("## Grup duplikat (contoh maks 10)")
    lines.append("")
    if not stats["dup_groups"]:
        lines.append("(tidak ada duplikat)")
    for g in stats["dup_groups"][:10]:
        lines.append("- `%s` sha256=%s... x%d | sumber=%s | terpilih=%s" % (
            g["url"], g["content_sha256"][:12], g["n_rekaman"],
            ",".join(g["sumber_kembar"]), g["sumber_terpilih"]))
    lines.append("")
    return "\n".join(lines)


def write_if_changed(path, data_bytes):
    """Tulis hanya bila beda dari yang ada di disk -> idempoten, mtime utuh."""
    if os.path.exists(path):
        with open(path, "rb") as fh:
            if fh.read() == data_bytes:
                return "unchanged"
    tmp = path + ".tmp"
    with open(tmp, "wb") as fh:
        fh.write(data_bytes)
    os.replace(tmp, path)
    return "written"


def main(argv=None):
    ap = argparse.ArgumentParser(
        description="KUMPUL+DEDUP hasil harvest multi-alat (norma WF-CRAWL-0911 D-06).")
    ap.add_argument("--input", nargs="+", required=True,
                    help="daftar berkas harvest JSONL/JSON (kolom url,konten,sumber,ts)")
    ap.add_argument("--out-dir", required=True,
                    help="direktori output unique.jsonl + report.md + report.json")
    args = ap.parse_args(argv)

    os.makedirs(args.out_dir, exist_ok=True)
    unique_entries, stats = build(args.input)

    jsonl_text = "".join(
        json.dumps(entry, ensure_ascii=False, sort_keys=True) + "\n"
        for _, entry in unique_entries)
    report_json = {
        "tool": "dedup_harvest.py",
        "inputs": stats["inputs"],
        "parse_errors": stats["parse_errors"],
        "total_records": stats["total_records"],
        "unique": stats["unique"],
        "dup_removed": stats["dup_removed"],
        "dup_group_count": len(stats["dup_groups"]),
        "dup_groups": stats["dup_groups"],
    }
    targets = [
        (os.path.join(args.out_dir, "unique.jsonl"),
         jsonl_text.encode("utf-8")),
        (os.path.join(args.out_dir, "report.md"),
         render_report_md(stats).encode("utf-8")),
        (os.path.join(args.out_dir, "report.json"),
         (json.dumps(report_json, ensure_ascii=False, sort_keys=True, indent=2)
          + "\n").encode("utf-8")),
    ]
    statuses = {}
    for path, blob in targets:
        statuses[os.path.basename(path)] = write_if_changed(path, blob)

    print("inputs=%d total=%d unique=%d dup_removed=%d dup_groups=%d parse_errors=%d" % (
        len(stats["inputs"]), stats["total_records"], stats["unique"],
        stats["dup_removed"], len(stats["dup_groups"]), stats["parse_errors"]))
    for name in ("unique.jsonl", "report.md", "report.json"):
        print("%s: %s (%s)" % (name, statuses[name], os.path.join(args.out_dir, name)))
    if stats["total_records"] == 0:
        sys.stderr.write("ERROR: tidak ada baris sah pada input\n")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
