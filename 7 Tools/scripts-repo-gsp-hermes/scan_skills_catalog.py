#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan semua SKILL.md (registry default + kanonik EKAS) dan ekstrak detail lengkap:
frontmatter, description, linked files (templates/scripts/references/assets), section outline.
Output: JSON terstruktur untuk kompilasi katalog."""
import os, re, json, sys

ROOTS = {
    "registry": r"C:/Users/TRIAL/AppData/Local/hermes/skills",
    "kanonik": r"C:/Users/TRIAL/workspace/gsp-hermes/skills",
}
OUT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/skills_catalog_raw.json"

def parse_frontmatter(text):
    """Tolerant YAML frontmatter parser for SKILL.md."""
    fm = {}
    if not text.startswith("---"):
        return fm, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fm, text
    yaml_block = parts[1]
    body = parts[2]
    lines = yaml_block.split("\n")
    i = 0
    # description may be a folded block (>- or >) or plain; track current key
    cur_key = None
    desc_lines = []
    def flush_desc():
        nonlocal cur_key, desc_lines
        if cur_key and desc_lines:
            fm[cur_key] = " ".join(x.strip() for x in desc_lines if x.strip()).strip()
        cur_key = None
        desc_lines = []
    for ln in lines:
        if not ln.strip() or ln.strip().startswith("#"):
            continue
        if re.match(r"^[A-Za-z_][A-Za-z0-9_.]*:", ln):
            flush_desc()
            m = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*):\s*(.*)$", ln)
            key, val = m.group(1), m.group(2).strip()
            if key == "description" and (val in ("", ">-", "|", ">-", ">", "|-")):
                cur_key = key
            else:
                fm[key] = val
        elif cur_key:
            desc_lines.append(ln)
        elif ln.startswith("- "):
            # list item under previous key — handle tags inline lists only
            pass
    flush_desc()
    # nested metadata: metadata.hermes.tags / category
    return fm, body

def extract_sections(body):
    return re.findall(r"^(#{1,6})\s+(.+)$", body, re.M)

def extract_when(body):
    """Ambil teks bagian pemicu (When to Use / Triggers) — maks 500 char."""
    m = re.search(r"^##+ (When to Use|Triggers|Kapan Menggunakan|Pemicu)[^\n]*\n(.*?)(?=^##|\Z)", body, re.M | re.S)
    if m:
        txt = re.sub(r"^[-*]\s+", "", m.group(2), flags=re.M)
        txt = re.sub(r"\s+", " ", txt).strip()
        return txt[:600]
    return ""

def file_kind(name):
    for prefix in ("references", "templates", "scripts", "assets"):
        if name.startswith(prefix + "/") or name.startswith(prefix + "\\"):
            return prefix
    return "root"

def main():
    entries = []
    seen = set()
    for root_name, root in ROOTS.items():
        for dirpath, dirnames, filenames in os.walk(root):
            if "SKILL.md" not in filenames:
                continue
            sp = os.path.join(dirpath, "SKILL.md")
            rel = os.path.relpath(sp, root)
            cat = os.path.relpath(dirpath, root).split(os.sep)[0]
            name = os.path.basename(dirpath)
            # skip nested category folder itself named 'gsp' etc with no own SKILL.md
            with open(sp, encoding="utf-8", errors="replace") as f:
                text = f.read()
            fm, body = parse_frontmatter(text)
            linked = []
            for root2, dirs2, files2 in os.walk(dirpath):
                for fn in files2:
                    if fn == "SKILL.md":
                        continue
                    fp = os.path.join(root2, fn)
                    relf = os.path.relpath(fp, dirpath).replace("\\", "/")
                    try:
                        sz = os.path.getsize(fp)
                    except OSError:
                        sz = 0
                    linked.append({"path": relf, "kind": file_kind(relf), "size": sz})
            linked.sort(key=lambda x: x["path"])
            sections = extract_sections(body)
            when = extract_when(body)
            desc = fm.get("description", "")
            entry = {
                "name": fm.get("name", name),
                "category": cat,
                "root": root_name,
                "relpath": rel,
                "description": desc,
                "version": fm.get("version", ""),
                "author": fm.get("author", ""),
                "license": fm.get("license", ""),
                "platforms": fm.get("platforms", ""),
                "tags": fm.get("tags", ""),
                "when": when,
                "sections": sections,
                "linked": linked,
                "body_chars": len(body),
            }
            key = entry["name"].lower()
            if key in seen:
                continue
            seen.add(key)
            entries.append(entry)
    entries.sort(key=lambda e: (e["category"].lower(), e["name"].lower()))
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)
    from collections import Counter
    cats = Counter(e["category"] for e in entries)
    print("total skills:", len(entries))
    print("categories:", len(cats))
    for c, n in cats.most_common():
        print(f"  {c}: {n}")
    wt = sum(1 for e in entries if any(x["kind"] == "templates" for x in e["linked"]))
    ws = sum(1 for e in entries if any(x["kind"] == "scripts" for x in e["linked"]))
    wr = sum(1 for e in entries if any(x["kind"] == "references" for x in e["linked"]))
    print(f"dengan templates: {wt}, scripts: {ws}, references: {wr}")

if __name__ == "__main__":
    main()
