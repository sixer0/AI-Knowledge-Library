#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Bagan interaksi antar skill + matriks pemetaan skill (skill × profil, mode ALWAYS/ON DEMAND).

Sumber:
- skills_super_raw.json (130 skill: nama, kategori, body, file)
- SOUL.md semua profil (default + 40 gsp-* + user01): daftar ALWAYS LOAD / ON DEMAND
- direktori skills per-profil (universe skill lengkap)

Output:
- interaksi_skill.json / bagan_interaksi_skill.md (mermaid + deskripsi) / bagan_interaksi_skill.png
- matriks_pemetaan_skill.xlsx / .md / .csv
"""
import os, re, json, csv, glob

BASE = r"C:/Users/TRIAL/AppData/Local/hermes"
PROFILES = r"C:/Users/TRIAL/AppData/Local/hermes/profiles"
RAW = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem/skills_super_raw.json"
OUTDIR = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026_08_24_kajian_ekosistem"

with open(RAW, encoding="utf-8") as f:
    skills = json.load(f)
by_name = {s["name"].lower(): s for s in skills}

# ── Universe skill: registry/kanonik + per-profil ─────────────────────────
universe = {}   # name -> {"category": ..., "registry": bool}
for s in skills:
    universe[s["name"]] = {"category": s["category"], "registry": True, "body": s["body"]}
profile_dirs = sorted([d for d in os.listdir(PROFILES) if os.path.isdir(os.path.join(PROFILES, d))])
for pd in profile_dirs:
    sk = os.path.join(PROFILES, pd, "skills")
    if os.path.isdir(sk):
        for sd in os.listdir(sk):
            if sd not in universe:
                universe[sd] = {"category": "per-profil", "registry": False, "body": ""}

def get_skills(profile_dir):
    sk = os.path.join(profile_dir, "skills")
    return set(os.listdir(sk)) if os.path.isdir(sk) else set()

def valid_skill_name(s):
    s = s.strip()
    return bool(re.fullmatch(r"[a-z0-9][a-z0-9-]{1,}", s)) and "skill_view" not in s and "name=" not in s and "(" not in s

def extract_skill_lists(soul_text):
    """Kembalikan (always, ondemand) dari SOUL.md."""
    always, ondemand = [], []
    # cari blok ALWAYS LOAD ... (sampai bagian berikutnya atau akhir)
    m = re.search(r"ALWAYS LOAD[^\n]*\n(.*?)(?=\n## |\Z)", soul_text, re.S | re.I)
    if m:
        always = [s for s in re.findall(r"`([^`]+)`", m.group(1)) if valid_skill_name(s)]
    m = re.search(r"ON DEMAND[^\n]*\n(.*?)(?=\n## |\Z)", soul_text, re.S | re.I)
    if m:
        ondemand = [s for s in re.findall(r"`([^`]+)`", m.group(1)) if valid_skill_name(s)]
    return always, ondemand

# ── Pemetaan skill × profil ───────────────────────────────────────────────
profiles = []
souls = [("default", os.path.join(BASE, "SOUL.md"))]
for pd in profile_dirs:
    souls.append((pd, os.path.join(PROFILES, pd, "SOUL.md")))

skill_profile = {}  # skill -> {profile: mode}
for pname, spath in souls:
    if not os.path.exists(spath):
        continue
    with open(spath, encoding="utf-8", errors="replace") as f:
        soul = f.read()
    always, ondemand = extract_skill_lists(soul)
    profiles.append({"profile": pname, "always": always, "ondemand": ondemand,
                     "skills_dir": sorted(get_skills(os.path.join(PROFILES, pname) if pname != "default" else BASE))})
    for s in always:
        skill_profile.setdefault(s, {})[pname] = "ALWAYS"
    for s in ondemand:
        skill_profile.setdefault(s, {})[pname] = "ON DEMAND"

# ── Edge interaksi antar skill ────────────────────────────────────────────
def norm(n):
    return n.lower().strip()

names = {norm(n): n for n in universe}
edges = {}  # (a,b) -> {"types": set, "weight": int}

def add_edge(a, b, etype, weight=1):
    if a == b:
        return
    key = tuple(sorted([norm(a), norm(b)]))
    d = edges.setdefault(key, {"types": set(), "weight": 0})
    d["types"].add(etype)
    d["weight"] += weight

for s in skills:
    a = norm(s["name"])
    body = s["body"]
    # 1) related_skills dari frontmatter (parsing ulang sederhana)
    m = re.search(r"related_skills:\s*\[([^\]]*)\]", s.get("body", ""))
    if not m:
        m = re.search(r"^related_skills:\s*(\[[^\]]*\]|[^\n]+)", s["body"], re.M)
    if m:
        for rn in re.findall(r"[\w-]+", m.group(1)):
            r = norm(rn)
            if r in names and r != a:
                add_edge(a, r, "related")
    # 2) mention dalam backtick
    for span in re.findall(r"`([^`]+)`", body):
        t = norm(span.strip())
        if t in names and t != a:
            add_edge(a, t, "mention")
        else:
            # coba awalan: e.g. `skill_view(name='gsp-x')`
            mm = re.search(r"skill_view\(\s*name\s*=\s*['\"]([\w-]+)['\"]", span)
            if mm and norm(mm.group(1)) in names and norm(mm.group(1)) != a:
                add_edge(a, norm(mm.group(1)), "mention")
    # 3) nama gsp-* di body (pola khas)
    for gn in re.findall(r"\b(gsp-[\w-]+)\b", body):
        g = norm(gn)
        if g in names and g != a:
            add_edge(a, g, "gsp-ref")
    # 4) pola skill_view(name=...) di baris biasa
    for mm in re.finditer(r"skill_view\(\s*name\s*=\s*['\"]([\w-]+)['\"]", body):
        g = norm(mm.group(1))
        if g in names and g != a:
            add_edge(a, g, "gsp-ref")

# ── Simpan JSON interaksi ──────────────────────────────────────────────────
edge_list = []
for (a, b), d in edges.items():
    edge_list.append({"a": names.get(a, a), "b": names.get(b, b),
                      "types": sorted(d["types"]), "weight": d["weight"]})
edge_list.sort(key=lambda e: -e["weight"])
interaction = {"nodes": [{"name": n, "category": universe[n]["category"],
                          "registry": universe[n]["registry"],
                          "profiles": len(skill_profile.get(n, {}))} for n in universe],
               "edges": edge_list,
               "profile_usage": {k: v for k, v in sorted(skill_profile.items())}}
with open(os.path.join(OUTDIR, "interaksi_skill.json"), "w", encoding="utf-8") as f:
    json.dump(interaction, f, ensure_ascii=False, indent=1)

# ── Matriks (data) ─────────────────────────────────────────────────────────
rows = []
for sname, usage in sorted(skill_profile.items()):
    cat = universe.get(sname, {}).get("category", "?")
    always = sorted([p for p, m in usage.items() if m == "ALWAYS"])
    od = sorted([p for p, m in usage.items() if m == "ON DEMAND"])
    rows.append({"skill": sname, "kategori": cat, "jml_profil": len(usage),
                 "always": always, "ondemand": od,
                 "jml_always": len(always), "jml_od": len(od)})

# CSV long-format
csv_path = os.path.join(OUTDIR, "matriks_pemetaan_skill.csv")
with open(csv_path, "w", newline="", encoding="utf-8") as f:
    w = csv.writer(f)
    w.writerow(["skill", "kategori", "profil", "mode"])
    for sname, usage in sorted(skill_profile.items()):
        for p, m in sorted(usage.items()):
            w.writerow([sname, universe.get(sname, {}).get("category", "?"), p, m])

# XLSX
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill
wb = Workbook()
hdr_fill = PatternFill("solid", fgColor="1F3A5F")
hdr_font = Font(bold=True, color="FFFFFF")
def style_header(ws, ncols):
    for c in range(1, ncols + 1):
        cell = ws.cell(row=1, column=c)
        cell.fill = hdr_fill; cell.font = hdr_font

ws1 = wb.active; ws1.title = "Skill_x_Profil"
ws1.append(["skill", "kategori", "profil", "mode"])
for sname, usage in sorted(skill_profile.items()):
    for p, m in sorted(usage.items()):
        ws1.append([sname, universe.get(sname, {}).get("category", "?"), p, m])
style_header(ws1, 4)

ws2 = wb.create_sheet("Profil_x_Skill")
ws2.append(["profil", "jml_always", "jml_od", "always", "ondemand"])
for pr in profiles:
    ws2.append([pr["profile"], len(pr["always"]), len(pr["ondemand"]),
                ", ".join(pr["always"]), ", ".join(pr["ondemand"])])
style_header(ws2, 5)

ws3 = wb.create_sheet("Skill_Aset")
ws3.append(["skill", "kategori", "registry", "jml_profil", "jml_always", "jml_od",
            "file_count", "total_bytes", "templates", "scripts", "references", "body_chars"])
for s in sorted(skills, key=lambda x: x["name"].lower()):
    kinds = {}
    for fl in s["files"]:
        kinds[fl["kind"]] = kinds.get(fl["kind"], 0) + 1
    ws3.append([s["name"], s["category"], s["root"], len(skill_profile.get(s["name"], {})),
                sum(1 for p, m in skill_profile.get(s["name"], {}).items() if m == "ALWAYS"),
                sum(1 for p, m in skill_profile.get(s["name"], {}).items() if m == "ON DEMAND"),
                s["file_count"], s["file_total"], kinds.get("templates", 0),
                kinds.get("scripts", 0), kinds.get("references", 0), s["body_chars"]])
style_header(ws3, 12)

ws4 = wb.create_sheet("Ringkasan")
ws4.append(["metrik", "nilai"])
ws4.append(["total skill (universe)", len(universe)])
ws4.append(["skill direferensikan profil", len(skill_profile)])
ws4.append(["profil", len(profiles)])
ws4.append(["edge interaksi skill", len(edge_list)])
ws4.append(["edge bertipe related", sum(1 for e in edge_list if "related" in e["types"])])
ws4.append(["edge bertipe mention/backtick", sum(1 for e in edge_list if "mention" in e["types"])])
ws4.append(["edge bertipe gsp-ref", sum(1 for e in edge_list if "gsp-ref" in e["types"])])
style_header(ws4, 2)
xlsx_path = os.path.join(OUTDIR, "matriks_pemetaan_skill.xlsx")
wb.save(xlsx_path)

# ── Markdown matriks ───────────────────────────────────────────────────────
M = ["# MATRIKS PEMETAAN SKILL — EKOSISTEM BRAHMA GSP", "",
     f"**Total skill (universe):** {len(universe)} · **Skill dipakai profil:** {len(skill_profile)} · **Profil:** {len(profiles)} · **Edge interaksi:** {len(edge_list)}", "",
     "> Data lengkap (long-format) ada di `matriks_pemetaan_skill.csv` & `matriks_pemetaan_skill.xlsx` (sheet Skill_x_Profil, Profil_x_Skill, Skill_Aset, Ringkasan).", "",
     "## Skill → Profil (peringkat pemakaian)", "",
     "| Skill | Kategori | Jml profil | ALWAYS (profil) | ON DEMAND (profil) |",
     "|---|---|---|---|---|"]
for r in sorted(rows, key=lambda x: (-x["jml_profil"], x["skill"].lower())):
    M.append(f"| `{r['skill']}` | {r['kategori']} | {r['jml_profil']} | {', '.join(r['always'])[:120] or '—'} | {', '.join(r['ondemand'])[:120] or '—'} |")
M += ["", "## Profil → Skill (rangkuman)", "", "| Profil | ALWAYS (jml) | ON DEMAND (jml) |", "|---|---|---|"]
for pr in sorted(profiles, key=lambda x: x["profile"]):
    M.append(f"| `{pr['profile']}` | {len(pr['always'])} | {len(pr['ondemand'])} |")
M += ["", "## Edge interaksi terkuat (top 30)", "", "| Skill A | Skill B | Tipe | Bobot |", "|---|---|---|---|"]
for e in edge_list[:30]:
    M.append(f"| {e['a']} | {e['b']} | {', '.join(e['types'])} | {e['weight']} |")
md_path = os.path.join(OUTDIR, "matriks_pemetaan_skill.md")
with open(md_path, "w", encoding="utf-8") as f:
    f.write("\n".join(M))

# ── Bagan interaksi (mermaid) ──────────────────────────────────────────────
# pilih hub: skill dengan profil terbanyak + top edges
top_skills = sorted(skill_profile, key=lambda s: -len(skill_profile[s]))[:35]
tset = {norm(s) for s in top_skills}
B = ["# BAGAN INTERAKSI ANTAR SKILL — EKOSISTEM BRAHMA GSP", "",
     "**Node:** skill (warna = kategori) · **Edge:** referensi silang (related/mention/gsp-ref) antar skill.", "",
     "> Bagan penuh (130 node) ada di `bagan_interaksi_skill.png`; berikut versi fokus 35 skill terhubung (hub):", "",
     "```mermaid", "graph TD"]
cat_color = {"orchestration": "#F4A261", "gsp": "#E76F51", "productivity": "#2A9D8F",
             "creative": "#E9C46A", "software-development": "#457B9D", "database": "#1D3557",
             "research": "#6D6875", "github": "#264653", "mlops": "#8ECAE6", "autonomous-ai-agents": "#A8DADC"}
for sname in top_skills:
    s = norm(sname)
    cat = universe.get(sname, {}).get("category", "?")
    col = cat_color.get(cat, "#999999")
    B.append(f"    {s}[{sname}]:::c{cat.replace('-','')}")
seen = set()
for e in edge_list:
    a, b = norm(e["a"]), norm(e["b"])
    if a in tset and b in tset:
        if (a, b) in seen:
            continue
        seen.add((a, b))
        lbl = "related" if "related" in e["types"] else ("mention" if "mention" in e["types"] else "gsp-ref")
        B.append(f"    {a} -->|{lbl}| {b}")
B += ["", "classDef core fill:#FFF3E0,stroke:#E76F51", "classDef analysis fill:#E3F2FD,stroke:#1D3557",
      "classDef execution fill:#E8F5E9,stroke:#2E7D32", "classDef verification fill:#FCE4EC,stroke:#C2185B",
      "classDef utility fill:#F3E5F5,stroke:#7B1FA2", "classDef knowledge fill:#FFF8E1,stroke:#F9A825",
      "```", ""]
# deskripsi interaksi
B += ["## Jenis Interaksi", "",
      "1. **related** — deklarasi `related_skills` di frontmatter (mis. docx ↔ pdf/xlsx/powerpoint).",
      "2. **mention** — skill dirujuk dalam body (umumnya di dalam backtick / contoh perintah).",
      "3. **gsp-ref** — referensi skill `gsp-*` dalam body (pola khas fleet GSP).",
      "4. **shared-context** — dua skill dimuat bersama oleh profil yang sama (ALWAYS/ON DEMAND) → lihat matriks pemetaan.", ""]
bagan_md = os.path.join(OUTDIR, "bagan_interaksi_skill.md")
with open(bagan_md, "w", encoding="utf-8") as f:
    f.write("\n".join(B))

# ── PNG (matplotlib) ───────────────────────────────────────────────────────
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import networkx as nx
G = nx.Graph()
for n in universe:
    G.add_node(n)
for e in edge_list:
    G.add_edge(e["a"], e["b"], weight=min(e["weight"], 5), etype=", ".join(e["types"]))
pos = nx.spring_layout(G, seed=42, k=0.42, iterations=60)
plt.figure(figsize=(22, 16))
cats = {}
for n in universe:
    cats.setdefault(universe[n]["category"], []).append(n)
cat_palette = ["#E76F51", "#2A9D8F", "#E9C46A", "#457B9D", "#1D3557", "#6D6875", "#264653",
               "#8ECAE6", "#A8DADC", "#F4A261", "#2B2D42", "#D62828", "#003049", "#5A189A",
               "#7B2CBF", "#9D4EDD", "#FFB703", "#606C38", "#BC6C25"]
for i, (cat, nodes) in enumerate(cats.items()):
    nx.draw_networkx_nodes(G, pos, nodelist=nodes, node_size=420,
                           node_color=cat_palette[i % len(cat_palette)], alpha=0.92, label=cat)
edge_colors = []
for a, b, d in G.edges(data=True):
    edge_colors.append("#E76F51" if "related" in d["etype"] else "#B0BEC5")
nx.draw_networkx_edges(G, pos, edge_color=edge_colors, alpha=0.35, width=0.8)
nx.draw_networkx_labels(G, pos, font_size=7, font_color="#111")
plt.legend(fontsize=11, loc="upper left", frameon=True)
plt.title("Bagan Interaksi Antar Skill — Ekosistem Brahma GSP (130 skill, %d edge)" % G.number_of_edges(), fontsize=16)
plt.axis("off")
plt.tight_layout()
png_path = os.path.join(OUTDIR, "bagan_interaksi_skill.png")
plt.savefig(png_path, dpi=110, bbox_inches="tight")
print("OK edges:", len(edge_list), "| nodes:", len(universe), "| profile usage:", len(skill_profile), "| profiles:", len(profiles))
print("png:", os.path.getsize(png_path), "bytes")
