#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan SEMUA SKILL.md (registry default + kanonik) menjadi inventaris SUPER DETAIL:
- file tree LENGKAP (semua file: SKILL.md, LICENSE, README, scripts, templates,
  references, assets, __pycache__/*.pyc) dengan ukuran
- deskripsi & When-to-Use PENUH (tanpa potongan)
- hingga 25 perintah/tool utama yang diekstrak dari code fences
- body SKILL.md utuh (untuk lampiran isi penuh)
Output: JSON + dossier markdown + lampiran isi penuh + zip semua file skill.
Usage: python scan_skill_library.py   (sesuaikan ROOTS/OUT di bawah)
"""
import os, re, json, zipfile

ROOTS = {
    "registry": r"C:/Users/TRIAL/AppData/Local/hermes/skills",
    "kanonik": r"C:/Users/TRIAL/workspace/gsp-hermes/skills",
}
BASE_OUT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs"  # sesuaikan per tugas
OUT_JSON = os.path.join(BASE_OUT, "skills_super_raw.json")
OUT_DOSSIER = os.path.join(BASE_OUT, "katalog_skill_super_detail.md")
OUT_FULL = os.path.join(BASE_OUT, "katalog_skill_isi_penuh.md")
OUT_ZIP = r"C:/Users/TRIAL/workspace/Katalog_Skill_Files.zip"


def parse_frontmatter(text):
    fm = {}
    if not text.startswith("---"):
        return fm, text
    parts = text.split("---", 2)
    if len(parts) < 3:
        return fm, text
    lines = parts[1].split("\n")
    body = parts[2]
    cur_key, desc_lines = None, []
    def flush():
        nonlocal cur_key, desc_lines
        if cur_key and desc_lines:
            fm[cur_key] = " ".join(x.strip() for x in desc_lines if x.strip()).strip()
        cur_key, desc_lines = None, []
    for ln in lines:
        if not ln.strip() or ln.strip().startswith("#"):
            continue
        m = re.match(r"^([A-Za-z_][A-Za-z0-9_.]*):\s*(.*)$", ln)
        if m:
            flush()
            key, val = m.group(1), m.group(2).strip()
            if key == "description" and val in ("", ">-", ">", "|", "|-"):
                cur_key = key
            else:
                fm[key] = val
        elif cur_key:
            desc_lines.append(ln)
    flush()
    return fm, body


def extract_sections(body):
    return [(len(h), t.strip()) for h, t in re.findall(r"^(#{1,6})\s+(.+)$", body, re.M)]


def extract_when_full(body):
    m = re.search(r"^##+ (When to Use|Triggers|Kapan Menggunakan|Pemicu)[^\n]*\n(.*?)(?=^##|\Z)", body, re.M | re.S)
    return re.sub(r"^[-*]\s+", "- ", m.group(2), flags=re.M).strip() if m else ""


def extract_commands(body):
    cmds = []
    for block in re.findall(r"```[a-z]*\n(.*?)```", body, re.S):
        for ln in block.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(("#", "//", "<!--")):
                continue
            if re.match(r"^[\w./\\-]+\s+\S", ln) or ln.startswith(("$", "hermes ", "python ", "node ", "npm ", "gh ", "git ", "docker ", "curl ", "pip ", "uv ", "npx ", "soffice", "cargo ")):
                cmds.append(ln[:180])
    if len(cmds) < 15:
        for ln in body.splitlines():
            m = re.search(r"`([^`]{4,120})`", ln)
            if m and re.match(r"^[\w./\\-]+(\s|$)", m.group(1)) and (" " in m.group(1) or m.group(1).endswith((".py", ".sh", ".js", ".mjs", ".ps1"))):
                cmds.append(m.group(1)[:180])
    seen, out = set(), []
    for c in cmds:
        k = c.lower()
        if k not in seen:
            seen.add(k); out.append(c)
        if len(out) >= 25:
            break
    return out


def file_kind(path):
    for prefix in ("references", "templates", "scripts", "assets"):
        if path.startswith(prefix + "/"):
            return prefix
    return "root"


def fmt_size(n):
    return f"{n/1024:.1f} KB" if n >= 1024 else f"{n} B"


def main():
    entries, seen = [], set()
    for root_name, root in ROOTS.items():
        for dirpath, dirnames, filenames in os.walk(root):
            if "SKILL.md" not in filenames:
                continue
            sp = os.path.join(dirpath, "SKILL.md")
            rel = os.path.relpath(sp, root)
            cat = os.path.relpath(dirpath, root).split(os.sep)[0]
            name = os.path.basename(dirpath)
            with open(sp, encoding="utf-8", errors="replace") as f:
                text = f.read()
            fm, body = parse_frontmatter(text)
            files, total = [], 0
            for root2, dirs2, files2 in os.walk(dirpath):
                for fn in sorted(files2):
                    fp = os.path.join(root2, fn)
                    relf = os.path.relpath(fp, dirpath).replace("\\", "/")
                    try:
                        sz = os.path.getsize(fp)
                    except OSError:
                        sz = 0
                    total += sz
                    files.append({"path": relf, "kind": file_kind(relf), "size": sz, "size_hr": fmt_size(sz)})
            files.sort(key=lambda x: (x["kind"] != "root", x["path"]))
            entry = {
                "name": fm.get("name", name), "category": cat, "root": root_name, "relpath": rel,
                "description": fm.get("description", ""), "version": fm.get("version", ""),
                "author": fm.get("author", ""), "license": fm.get("license", ""),
                "platforms": fm.get("platforms", ""), "tags": fm.get("tags", ""),
                "when": extract_when_full(body), "sections": extract_sections(body),
                "commands": extract_commands(body), "files": files, "file_count": len(files),
                "file_total": total, "body": body, "body_chars": len(body),
            }
            key = entry["name"].lower()
            if key in seen:
                continue
            seen.add(key)
            entries.append(entry)
    entries.sort(key=lambda e: (e["category"].lower(), e["name"].lower()))
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=1)

    def cat_order(c):
        return (0 if c == "orchestration" else 1 if c == "gsp" else 2, c.lower())
    cats = {}
    for e in entries:
        cats.setdefault(e["category"], []).append(e)

    # Part A: dossier super detail
    L = ["# KATALOG SKILL SUPER DETAIL - EKOSISTEM BRAHMA GSP", "",
         f"**Total: {len(entries)} skill unik ({len(cats)} kategori).** Semua file per skill dicantumkan (SKILL.md + pendukung).", ""]
    for cat in sorted(cats, key=cat_order):
        L.append(f"## Kategori: {cat} ({len(cats[cat])} skill)")
        L.append("")
        for e in cats[cat]:
            badge = " *(kanonik EKAS)*" if e["root"] == "kanonik" else ""
            L.append(f"### {e['name']}{badge}")
            L.append("")
            L.append(f"- **Kategori:** `{e['category']}`; **Lokasi:** `{e['relpath']}`")
            meta = []
            if e["version"]: meta.append(f"versi {e['version']}")
            if e["author"]: meta.append(f"author {e['author']}")
            if e["license"]: meta.append(f"lisensi {e['license']}")
            if e["platforms"]: meta.append(f"platform {e['platforms']}")
            if meta: L.append(f"- **Metadata:** {', '.join(meta)}")
            if e["tags"]: L.append(f"- **Tags:** {e['tags']}")
            if e["description"]:
                L.append(f"- **Deskripsi lengkap:** {e['description'].replace(chr(10), ' ')}")
            if e["when"]:
                L.append("- **Pemicu / When to Use (penuh):**")
                for wl in e["when"].splitlines()[:25]:
                    L.append(f"  {wl}")
                if len(e["when"].splitlines()) > 25:
                    L.append(f"  _… (total {len(e['when'].splitlines())} baris, lihat isi penuh)_")
            if e["sections"]:
                L.append(f"- **Struktur bagian ({len(e['sections'])}):** " + "; ".join(f"{'#'*lvl} {t}" for lvl, t in e["sections"]))
            if e["commands"]:
                L.append(f"- **Perintah/tool utama ({len(e['commands'])}):**")
                for c in e["commands"]:
                    L.append(f"  - `{c}`")
            L.append(f"- **File lengkap ({e['file_count']}, total {fmt_size(e['file_total'])}):**")
            for fl in e["files"]:
                L.append(f"  - `{fl['path']}` - {fl['size_hr']}")
            L.append(f"- **Ukuran body SKILL.md:** {e['body_chars']} karakter")
            L.append("")
    with open(OUT_DOSSIER, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    # Part B: isi penuh SKILL.md
    F = ["# LAMPIRAN - ISI PENUH SELURUH SKILL.md", "", f"Total {len(entries)} skill, konten asli tanpa potongan.", ""]
    for cat in sorted(cats, key=cat_order):
        F.append(f"## Kategori: {cat}")
        F.append("")
        for e in cats[cat]:
            F.append(f"### {e['name']}")
            F.append("")
            F.append(f"`{e['relpath']}`")
            F.append("")
            F.append("```markdown")
            F.append(e["body"].rstrip())
            F.append("```")
            F.append("")
    with open(OUT_FULL, "w", encoding="utf-8") as f:
        f.write("\n".join(F))

    # Zip semua file skill
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root_name, root in ROOTS.items():
            for dirpath, dirnames, filenames in os.walk(root):
                if "SKILL.md" not in filenames:
                    continue
                rel = os.path.relpath(dirpath, root)
                for fn in filenames:
                    z.write(os.path.join(dirpath, fn), f"skills/{root_name}/{rel}/{fn}")
    print("skills:", len(entries))
    print("dossier:", os.path.getsize(OUT_DOSSIER), "bytes")
    print("full:", os.path.getsize(OUT_FULL), "bytes")
    print("zip:", os.path.getsize(OUT_ZIP), "bytes")


if __name__ == "__main__":
    main()
