#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Scan SUPER DETAIL semua SKILL.md: file tree LENGKAP (semua file), deskripsi &
when penuh (tanpa potongan), perintah/tool utama dari body, body utuh.
Output: JSON + katalog dossier (super detail) + lampiran isi penuh SKILL.md."""
import os, re, json, zipfile

ROOTS = {
    "registry": r"C:/Users/TRIAL/AppData/Local/hermes/skills",
    "kanonik": r"C:/Users/TRIAL/workspace/gsp-hermes/skills",
}
OUT_JSON = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/skills_super_raw.json"
OUT_DOSSIER = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/katalog_skill_super_detail.md"
OUT_FULL = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/katalog_skill_isi_penuh.md"
OUT_ZIP = r"C:/Users/TRIAL/workspace/Katalog_Skill_Files_2026-08-24.zip"

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
    if m:
        txt = re.sub(r"^[-*]\s+", "- ", m.group(2), flags=re.M)
        return txt.strip()
    return ""

def extract_commands(body):
    cmds = []
    for block in re.findall(r"```[a-z]*\n(.*?)```", body, re.S):
        for ln in block.splitlines():
            ln = ln.strip()
            if not ln or ln.startswith(("#", "//", "<!--")):
                continue
            if re.match(r"^[\w./\\-]+\s+\S", ln) or ln.startswith(("$", "hermes ", "python ", "node ", "npm ", "gh ", "git ", "docker ", "curl ", "pip ", "uv ", "npx ", "soffice", "cargo ", "npx ")):
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
            files = []
            total = 0
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

    # ── Part A: dossier super detail ─────────────────────────────────────
    def cat_order(c):
        return (0 if c == "orchestration" else 1 if c == "gsp" else 2, c.lower())
    cats = {}
    for e in entries:
        cats.setdefault(e["category"], []).append(e)
    L = []
    L.append("# KATALOG SKILL SUPER DETAIL — EKOSISTEM BRAHMA GSP")
    L.append("")
    L.append("**Sumber:** registry `AppData/Local/hermes/skills` + kanonik `workspace/gsp-hermes/skills` · **Tanggal:** 24 Agustus 2026 · **Total: %d skill unik** (%d kategori) · **Semua file per skill dicantumkan (SKILL.md + pendukung).**" % (len(entries), len(cats)))
    L.append("")
    L.append("> Lampiran isi PENUH setiap SKILL.md ada di `katalog_skill_isi_penuh.md`; salinan semua file skill ada di `Katalog_Skill_Files_2026-08-24.zip`.")
    L.append("")
    # summary table
    L.append("## Ringkasan")
    L.append("")
    L.append("| Kategori | Jml | File | Rata-rata file/skill |")
    L.append("|---|---|---|---|")
    for cat in sorted(cats, key=cat_order):
        items = cats[cat]
        fc = sum(e["file_count"] for e in items)
        L.append(f"| {cat} | {len(items)} | {fc} | {fc/len(items):.1f} |")
    L.append(f"| **Total** | **{len(entries)}** | **{sum(e['file_count'] for e in entries)}** | |")
    L.append("")
    for cat in sorted(cats, key=cat_order):
        L.append(f"## Kategori: {cat} ({len(cats[cat])} skill)")
        L.append("")
        for e in cats[cat]:
            badge = " *(kanonik EKAS)*" if e["root"] == "kanonik" else ""
            L.append(f"### {e['name']}{badge}")
            L.append("")
            L.append(f"- **Kategori:** `{e['category']}` · **Lokasi:** `{e['relpath']}`")
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
                L.append(f"- **Pemicu / When to Use (penuh):**")
                for wl in e["when"].splitlines()[:25]:
                    L.append(f"  {wl}")
                if len(e["when"].splitlines()) > 25:
                    L.append(f"  _… (total {len(e['when'].splitlines())} baris, lihat isi penuh)_")
            if e["sections"]:
                secs = "; ".join(f"{'#'*lvl} {t}" for lvl, t in e["sections"])
                L.append(f"- **Struktur bagian ({len(e['sections'])}):** {secs}")
            if e["commands"]:
                L.append(f"- **Perintah/tool utama ({len(e['commands'])}):**")
                for c in e["commands"]:
                    L.append(f"  - `{c}`")
            L.append(f"- **File lengkap ({e['file_count']}, total {fmt_size(e['file_total'])}):**")
            for fl in e["files"]:
                L.append(f"  - `{fl['path']}` — {fl['size_hr']}")
            L.append(f"- **Ukuran body SKILL.md:** {e['body_chars']} karakter")
            L.append("")
    with open(OUT_DOSSIER, "w", encoding="utf-8") as f:
        f.write("\n".join(L))

    # ── Part B: isi penuh SKILL.md ───────────────────────────────────────
    F = []
    F.append("# LAMPIRAN — ISI PENUH SELURUH SKILL.md (130 SKILL)")
    F.append("")
    F.append("**Sumber:** registry + kanonik · **24 Agustus 2026** · Konten asli tanpa potongan, diurutkan per kategori.")
    F.append("")
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

    # ── ZIP semua file skill ─────────────────────────────────────────────
    with zipfile.ZipFile(OUT_ZIP, "w", zipfile.ZIP_DEFLATED) as z:
        for root_name, root in ROOTS.items():
            for dirpath, dirnames, filenames in os.walk(root):
                if "SKILL.md" not in filenames:
                    continue
                rel = os.path.relpath(dirpath, root)
                for fn in filenames:
                    fp = os.path.join(dirpath, fn)
                    arc = f"skills/{root_name}/{rel}/{fn}"
                    z.write(fp, arc)
    print("skills:", len(entries))
    print("dossier:", os.path.getsize(OUT_DOSSIER), "bytes")
    print("full:", os.path.getsize(OUT_FULL), "bytes")
    print("zip:", os.path.getsize(OUT_ZIP), "bytes")

if __name__ == "__main__":
    main()
