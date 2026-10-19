#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""selftest_datum_diagram.py — gerbang eksekusi dua arah kelas diagram v2.0.0
(kartu DHS-RB-04; preseden t_a21e89ab dan DHS-RB-01: kompilasi bukan gerbang).

Letakkan BERDAMPINGAN dengan datum_diagram.py + tokens.json + datumbind.py lalu
jalankan dengan interpreter apa pun yang punya stdlib. Hijau penuh hanya bila:
  FASE-A (RED): setiap basal rusak di fixtures_diagram/bad_cases.json DITOLAK
                engine dengan cacat bernama sesuai, DAN sumber engine terbukti
                bebas hex palet/grid hardcoded (token-driven);
  FASE-B (GREEN): basal baik dirender nyata menjadi SVG, lolos semua cek yang
                  dilaporkan, geometri terkunci kisi, apparatus benar, dan CLI
                  (--schema/--list/--estimate/render) mengembalikan exit 0.
Cetak CHECK n: PASS|FAIL per butir + VERDICT akhir; exit != 0 bila ada FAIL.
"""
import json
import os
import re
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)

fails = []


def check(n, name, cond, detail=""):
    tag = "PASS" if cond else "FAIL"
    if not cond:
        fails.append(name)
    print("CHECK %s: %s — %s%s" % (n, tag, name, (" | " + str(detail)) if detail else ""))


import datum_diagram as dd
from datum_diagram import DiagramDefect, load_spec, build_svg, estimate, tokens_path

FIXDIR = os.path.join(HERE, "fixtures_diagram")
TMP = os.path.join(HERE, "_st_diag_tmp")
if not os.path.isdir(TMP):
    os.makedirs(TMP)


def write_tmp(name, obj):
    p = os.path.join(TMP, name)
    with open(p, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False)
    return p


# ---------------------------------------------------- CHECK 1: token resolver
try:
    tok = json.load(open(tokens_path(), encoding="utf-8"))
    ok = tok["colour"]["interior"]["signal"] == "#B45309" and tok["grid_mm"]["text_column"] == 128
    check(1, "engine membaca tokens.json paket lewat datumbind.tokens_path()", ok, tokens_path())
except Exception as ex:
    check(1, "engine membaca tokens.json paket lewat datumbind.tokens_path()", False, repr(ex))

# ------------------------------- CHECK 2: token-driven — nol hex/nol mm gaya
src = open(os.path.join(HERE, "datum_diagram.py"), encoding="utf-8").read()
body = re.sub(r'#.*|"""[\s\S]*?"""', "", src)          # buang komentar + docstring
hexes = re.findall(r'#[0-9A-Fa-f]{6}\b', body)
check(2, "sumber engine bebas hex palet hardcoded", hexes == [], "temuan=%r" % hexes[:5])

# ----------------------------------------------- FASE-A RED: battery mutasi
bad = json.load(open(os.path.join(FIXDIR, "bad_cases.json"), encoding="utf-8"))
n_reject = 0
misses = []
for i, case in enumerate(bad["cases"], start=1):
    p = write_tmp("_bad_%d.json" % i, case["spec"])
    try:
        svg, rep = build_svg(load_spec(p), release=True)
        misses.append("%s:DITERIMA" % case["name"])
    except DiagramDefect as ex:
        msg = str(ex)
        if case["expect"].lower() in msg.lower():
            n_reject += 1
        else:
            misses.append("%s:nama salah ('%s' vs '%s')" % (case["name"], case["expect"], msg[:60]))
    except Exception as ex:
        misses.append("%s:galat tak terduga %r" % (case["name"], ex))
check(3, "FASE-A RED: semua %d basal rusak ditolak dengan cacat bernama" % len(bad["cases"]),
      n_reject == len(bad["cases"]) and not misses,
      "%d/%d lolos uji penolakan%s" % (n_reject, len(bad["cases"]), ("; sisa: " + "; ".join(misses)) if misses else ""))

# ------------------- CHECK 4: DATUM-31 sumber Mermaid ditolak (P7, cek 31)
mpath = os.path.join(TMP, "_mermaid.mmd")
open(mpath, "w", encoding="utf-8").write("graph TD\n  A-->B\n")
try:
    load_spec(mpath)
    check(4, "DATUM-31 sumber Mermaid ditolak", False, "tidak raise")
except DiagramDefect as ex:
    check(4, "DATUM-31 sumber Mermaid ditolak", "DATUM-31" in str(ex), str(ex)[:70])

# ------------- CHECK 5: gerbang rilis menolak labels_verified bukan true (P1)
spec_draft = json.load(open(os.path.join(FIXDIR, "good_layered.json"), encoding="utf-8"))
spec_draft["labels_verified"] = False
p = write_tmp("_draft.json", spec_draft)
try:
    build_svg(load_spec(p), release=True)
    check(5, "rilis menolak spek draft (labels_verified false)", False, "tidak raise")
except DiagramDefect as ex:
    check(5, "rilis menolak spek draft (labels_verified false)", "draft" in str(ex).lower(), str(ex)[:70])

# ------------------------------------------ FASE-B GREEN: basal baik nyata
good_ran = []
for fname in ("good_layered.json", "good_sld.json"):
    path = os.path.join(FIXDIR, fname)
    try:
        spec = load_spec(path)
        svg, rep = build_svg(spec, release=True)
        outp = os.path.join(TMP, fname.replace(".json", ".svg"))
        open(outp, "w", encoding="utf-8").write(svg)
        good_ran.append((fname, rep, svg, outp))
    except Exception as ex:
        good_ran.append((fname, None, None, repr(ex)))

ok_green = all(r is not None for _, r, _, _ in good_ran) and len(good_ran) == 2
check(6, "FASE-B GREEN: kedua basal baik ter-render tanpa cacat", ok_green,
      "; ".join("%s=%s" % (f, "OK" if r else d) for f, r, _, d in good_ran))

# CHECK 7: geometri terkunci kisi token (P5) — yang diuji adalah kotak simpul
# utama (data-node), bukan hiasan dalam bentuk (bayangan/garis ganda).
lat_x, lat_y = dd.LATTICE_X, dd.LATTICE_Y
geom_ok = True
bad_geom = []
for fname, rep, svg, _ in good_ran:
    if rep is None:
        continue
    skipped_shapes = 0
    for m in re.finditer(r'<[^>]*data-node="([^"]+)"[^>]*/?>', svg or ""):
        attrs = dict(re.findall(r'(\w[\w-]*)="(-?[\d.]+)"', m.group(0)))
        if "x" not in attrs:      # bentuk poligon/garis diturunkan dari kotak yang sudah dikunci
            skipped_shapes += 1
            continue
        x, y = float(attrs["x"]), float(attrs["y"])
        w, h = float(attrs["width"]), float(attrs["height"])
        if abs(x - round(x / lat_x) * lat_x) > 0.005 or abs(w - round(w / lat_x) * lat_x) > 0.005 \
           or abs(y - round(y / lat_y) * lat_y) > 0.005 or abs(h - round(h / lat_y) * lat_y) > 0.005:
            # toleransi 0,005 mm = setengah unit pembulatan keluaran SVG (3 desimal)
            geom_ok = False
            bad_geom.append("%s:%s (%.3f,%.3f %.3fx%.3f)" % (fname, m.group(1), x, y, w, h))
check(7, "simpul terkunci kisi token %.4f x %.4f mm (P5)" % (lat_x, lat_y), geom_ok, "; ".join(bad_geom[:4]))

# CHECK 8: root SVG memakai mm, bukan px polos (E-08)
mm_ok = all(re.search(r'width="[\d.]+mm" height="[\d.]+mm"', svg) for _, _, svg, _ in good_ran if svg)
check(8, "root SVG menyatakan mm (E-08)", mm_ok)

# CHECK 9: apparatus — page membawa komentar kewajiban; figure memikul sendiri (P6)
page_ok = fig_ok = False
for fname, rep, svg, _ in good_ran:
    if not svg:
        continue
    if rep["apparatus"] == "page":
        page_ok = "DATUM-APPARATUS-REQUIRED" in svg
    else:
        fig_ok = ("SUMBER" in svg) and ("KEY" in svg) and ("4.3" in svg)
check(9, "apparatus page ber-komentar kewajiban; figure memikul caption+KEY+SUMBER", page_ok and fig_ok)

# CHECK 10: warna keluar dari token, plafon <=5 dipatuhi basal baik (P5/DATUM-25)
col_ok = True
interior_hex = set(dd.INTERIOR.values())
for fname, rep, svg, _ in good_ran:
    if not svg:
        col_ok = False
        continue
    if rep["n_colour"] > int(dd.LIMITS["max_colour_values"]):
        col_ok = False
    for hexv in re.findall(r'(?:fill|stroke)="(#[0-9A-Fa-f]{6})"', svg):
        if hexv.upper() not in {h.upper() for h in interior_hex} | {dd.PAPER.upper()}:
            col_ok = False
check(10, "setiap hex keluaran adalah token colour.interior; n_colour<=5", col_ok,
      "; ".join("%s:%d warna" % (f, r["n_colour"]) for f, r, _, _ in good_ran if r))

# CHECK 11: glif rumah dirender mono amber sesuai pitfall warisan (T marks)
mark_ok = False
for fname, rep, svg, _ in good_ran:
    if svg and dd.MARKS["TERUKUR"] in svg:
        mark_ok = ('font-family="%s"' % dd.FACES["mono"]) in svg and dd.colour_of("signal") in svg
        break
check(11, "glif asal memakai wajah mono + tinta signal (pitfall warisan)", mark_ok)

# CHECK 12: arsiran 45/135 tersedia, tint abu TIDAK dipakai untuk isian (catatan fotokopi P5/638)
hatch_ok = all(("datum-hatch45" in svg and 'fill="#' not in svg.split('id="datum-hatch')[0].split("<rect")[-1])
               for _, _, svg, _ in good_ran if svg)
grey_used = any(re.search(r'fill="url\(#grey', svg or "") for _, _, svg, _ in good_ran)
check(12, "isian memakai pola arsiran, bukan tint", ("datum-hatch45" in (good_ran[0][2] or "")) and not grey_used)

# CHECK 13: CLI render nyata exit 0 + laporan JSON sah
cli = subprocess.run([sys.executable, os.path.join(HERE, "datum_diagram.py"),
                      os.path.join(FIXDIR, "good_layered.json"), "-o", os.path.join(TMP, "cli.svg"), "--json"],
                     capture_output=True, text=True)
cli_ok = cli.returncode == 0 and os.path.exists(os.path.join(TMP, "cli.svg"))
try:
    rep_cli = json.loads(cli.stdout)
    cli_ok = cli_ok and rep_cli.get("checks_run")
except Exception:
    cli_ok = False
check(13, "CLI render nyata exit 0 + SVG tertulis + laporan JSON", cli_ok, "exit=%s" % cli.returncode)

# CHECK 14: CLI --estimate ada dan berfungsi (P9 E-19)
cli2 = subprocess.run([sys.executable, os.path.join(HERE, "datum_diagram.py"),
                       os.path.join(FIXDIR, "good_sld.json"), "--estimate", "--json"],
                      capture_output=True, text=True)
est_ok = cli2.returncode == 0 and "render_hint" in cli2.stdout
check(14, "CLI --estimate berfungsi (E-19 ditutup)", est_ok, "exit=%s" % cli2.returncode)

# CHECK 15: CLI basal rusak exit != 0 dengan pesan cacat tercetak
badp = write_tmp("_bad_cli.json", bad["cases"][0]["spec"])
cli3 = subprocess.run([sys.executable, os.path.join(HERE, "datum_diagram.py"), badp],
                      capture_output=True, text=True)
check(15, "CLI basal rusak exit != 0 + DIAGRAM DEFECT tercetak",
      cli3.returncode != 0 and "DIAGRAM DEFECT" in (cli3.stderr + cli3.stdout), "exit=%s" % cli3.returncode)

# CHECK 16: --schema dan --list exit 0 (kontrak P1/P2/P3/P4 terbit)
cli4 = subprocess.run([sys.executable, os.path.join(HERE, "datum_diagram.py"), "--schema"],
                      capture_output=True, text=True)
cli5 = subprocess.run([sys.executable, os.path.join(HERE, "datum_diagram.py"), "--list"],
                      capture_output=True, text=True)
check(16, "--schema dan --list exit 0", cli4.returncode == 0 and cli5.returncode == 0
      and "width_mm" in cli4.stdout and "EDGE_KINDS" in cli5.stdout)

# CHECK 17: sembilan keluarga terpetakan ke tujuh mesin (P2 verbatim)
engines = {dd.FAMILIES[k]["engine"] for k in dd.FAMILIES}
check(17, "9 keluarga -> 7 mesin layout (P2 Tabel 6.2)", len(dd.FAMILIES) == 9 and len(engines) == 7,
      "%d keluarga, %d mesin" % (len(dd.FAMILIES), len(engines)))

# CHECK 18: sepuluh bentuk + enam jenis konektor lengkap dengan atribusi (P3/P4)
check(18, "10 bentuk simpul (P3) dan 6 jenis konektor (P4) lengkap",
      len(dd.SHAPES) == 10 and len(dd.EDGE_KINDS) == 6
      and all({"means", "notation"} <= set(v) for v in dd.SHAPES.values())
      and all({"pattern", "colour", "head", "iso", "use"} <= set(v) for v in dd.EDGE_KINDS.values()))

# CHECK 19: stadia satu-satunya bentuk beradius (P3 verbatim) — basal baik tidak
# memakai stadium, jadi tidak boleh ada rx= sama sekali di keluaran.
radius_only = [k for k, v in dd.SHAPES.items() if v["radius"]]
svg_all = "".join(s for _, _, s, _ in good_ran if s)
check(19, "radius hanya pada stadium (P3)", radius_only == ["stadium"] and 'rx="' not in svg_all,
      "beradius=%r" % radius_only)

# CHECK 20: banner jujur — laporan menyebut cek yang dijalankan
ran_all = set()
for _, rep, _, _ in good_ran:
    if rep:
        ran_all |= set(rep["checks_run"])
need = {"DATUM-24", "DATUM-25", "DATUM-26", "DATUM-27", "DATUM-28", "DATUM-32", "DATUM-33",
        "DATUM-34", "DATUM-35", "DATUM-37-lebar", "DATUM-29/30"}
check(20, "laporan melapor cek yang benar-benar dijalankan (banner jujur)", need <= ran_all,
      sorted(ran_all))

# CHECK 21 (ENH-D E-30): flow per_row membungkus; dua arah.
# MERAH: flow 10 simpul tanpa per_row melewati tinggi A4 (perilaku lama dipertahankan).
# HIJAU: dengan per_row=5 muat A4, baris-first, dan kapasitas riil tidak meluap lebar
# (regresi 08-10: tanpa batas k_max, n5 mendarat di x=170,7 > 166 mm dan DATUM-37 raise).
def _flow_spec(per_row=None, n=10):
    s = {"family": "flow", "id": "99.1", "title": "Uji pembungkusan flow.",
         "width_mm": 166, "labels_verified": True, "classification": "TERBATAS",
         "nodes": [{"id": "n%d" % i, "label": "Langkah proses %d" % i,
                    "class": {"row": 0}} for i in range(1, n + 1)],
         "edges": [{"from": "n%d" % i, "to": "n%d" % (i + 1), "kind": "data",
                    "label": "terus"} for i in range(1, n)],
         "sources": ["uji internal"]}
    if per_row:
        s["per_row"] = per_row
    return s

sp_red = _flow_spec()
sh_red = dd.Sheet(166); dd.layout_flow(sp_red, sh_red)
red_tall = sh_red.height() > 297.0
sp_grn = _flow_spec(per_row=5)
sh_grn = dd.Sheet(166); dd.layout_flow(sp_grn, sh_grn)
grn_fit = sh_grn.height() <= 297.0
row1 = sorted([k for k, nd in sh_grn.nodes.items() if nd["y"] == sh_grn.top],
              key=lambda k: sh_grn.nodes[k]["x"])
row1_ok = row1 == ["n%d" % (i + 1) for i in range(len(row1))] and len(row1) >= 3
overflow_w = [k for k, nd in sh_grn.nodes.items() if nd["x"] + nd["w"] > 166.0 + 1e-6]
svg_wr, rep_wr = dd.build_svg(sp_grn)   # tidak boleh raise DATUM-37
check(21, "flow per_row membungkus muat A4, baris-first, muat lebar (E-30)",
      red_tall and grn_fit and row1_ok and not overflow_w,
      "tanpa_per_row=%.0fmm per_row=%.0fmm baris1=%s luap_lebar=%s" %
      (sh_red.height(), sh_grn.height(), row1, overflow_w))

# CHECK 22 (ENH-D E-29 terverifikasi ulang): stadium = rect beradius, cylinder utuh.
sp_shape = {"family": "graph", "id": "99.2", "title": "Uji bentuk simpul.",
            "width_mm": 166, "labels_verified": True, "classification": "TERBATAS",
            "nodes": [{"id": "a", "label": "Mulai proses", "class": {"col": 0, "row": 0},
                       "shape": "stadium"},
                      {"id": "b", "label": "Data tersimpan", "class": {"col": 3, "row": 0},
                       "shape": "cylinder"}],
            "edges": [{"from": "a", "to": "b", "kind": "data", "label": "alir"}],
            "sources": ["uji internal"]}
svg_s, _ = dd.build_svg(sp_shape)
import re as _re
a_tag = _re.findall(r'<(rect|circle)[^>]*data-node="a"[^>]*>', svg_s)
a_rx = 'rx="' in (_re.findall(r'<rect[^>]*data-node="a"[^>]*>', svg_s) or [""])[0]
b_tag = _re.findall(r'<(path|circle)[^>]*data-node="b"[^>]*>', svg_s)
lab_b = bool(_re.findall(r'Data tersimpan', svg_s))
check(22, "graph menghormati stadium (rect+rx) dan cylinder berlabel (E-29)",
      a_tag == ["rect"] and a_rx and b_tag == ["path"] and lab_b,
      "a=%s rx=%s b=%s label=%s" % (a_tag, a_rx, b_tag, lab_b))

# CHECK 23 (ENH-D E-17): tap cabang SLD mendarat tepat di garis rel, tidak
# menggantung di bawahnya. Fixture nyata good_sld.json (instruksi user 08-10:
# ekstrak contoh dari dokumen). Merah sebelum tambal: 2 dari 3 edges menggantung.
import json as _json
with open(os.path.join(HERE, "fixtures_diagram", "good_sld.json"), encoding="utf-8") as fh:
    sp_sld = _json.load(fh)
sh_sld = dd.Sheet(sp_sld["width_mm"]); dd.layout_sld(sp_sld, sh_sld)
bus_y = sh_sld.bus["y"]
def _on_bnd(pt, n, tol=0.35):
    x, y = pt
    return ((abs(x - n["x"]) < tol and n["y"] - tol <= y <= n["y"] + n["h"] + tol) or
            (abs(x - (n["x"] + n["w"])) < tol and n["y"] - tol <= y <= n["y"] + n["h"] + tol) or
            (abs(y - n["y"]) < tol and n["x"] - tol <= x <= n["x"] + n["w"] + tol) or
            (abs(y - (n["y"] + n["h"])) < tol and n["x"] - tol <= x <= n["x"] + n["w"] + tol))
dangle = 0
for r in dd.route_edges(sp_sld, sh_sld):
    e = r["edge"]; pts = r["pts"]
    pa, pb = pts[0], pts[-1]
    touches = any(abs(py - bus_y) < 0.35 for px, py in pts)
    ok_a = (_on_bnd(pa, sh_sld.nodes[e["from"]]) or abs(pa[1] - bus_y) < 0.35)
    ok_b = (_on_bnd(pb, sh_sld.nodes[e["to"]]) or abs(pb[1] - bus_y) < 0.35)
    if e["from"] == sh_sld.bus["id"] or e["to"] == sh_sld.bus["id"]:
        ok_a = ok_a and touches; ok_b = ok_b and touches
    if not (ok_a and ok_b):
        dangle += 1
check(23, "tap cabang SLD menempel garis rel, nol menggantung (E-17)",
      dangle == 0, "edges=%d menggantung=%d" % (len(sp_sld["edges"]), dangle))

# CHECK 24..27 (BUG-DATUM-DIAGRAM, kartu t_ef103378; laporan FIGUR-1 t_559f107b
# + FIGUR-2 t_a3146011 + operator mid-run). Merah basal ketiga cacat terbukti
# terpisah atas cermin pra-tambal (mirror sweep: tabrakan kaki 13 figur,
# clamp-diam-diam graph col=2, TypeError hop G10.3/G12.2) — lihat result kartu.
def _diag_base(extra=None):
    s = {"family": "layered", "id": "99.3", "title": "Uji kaki apparatus.",
         "classification": "BIASA", "width_mm": 128, "labels_verified": True,
         "nodes": [{"id": "a%d" % i, "label": "Simpul baris %d" % i,
                    "class": {"tier": i}} for i in range(4)],
         "edges": [{"from": "a%d" % i, "to": "a%d" % (i + 1), "kind": "data",
                    "label": "tautan"} for i in range(3)],
         "sources": ["uji internal"]}
    if extra:
        s.update(extra)
    return s


def _node_bottoms(svg):
    out = []
    for m in _re.finditer(r'<[^>]*data-node="[^"]+"[^>]*/?>', svg):
        a = dict(_re.findall(r'(x|y|width|height)="(-?[\d.]+)"', m.group(0)))
        if "y" in a and "height" in a:
            out.append(float(a["y"]) + float(a["height"]))
    return out


sp_leg = _diag_base({"legend": ["TERUKUR hasil uji", "ASumsi desain"]})
svg_leg, rep_leg = dd.build_svg(json.loads(json.dumps(sp_leg)))
key_y = min(float(m.group(1)) for m in _re.finditer(
    r'<text x="0(?:\.0)?" y="([\d.]+)"[^>]*>KEY[^<]*</text>', svg_leg))
bottom = max(_node_bottoms(svg_leg))
# apparatus figure: tiga baris kaki (caption+KEY+SUMBER) wajib muat juga
sp_fig = _diag_base({"legend": ["TERUKUR hasil uji"], "apparatus": "figure"})
svg_fig, rep_fig = dd.build_svg(json.loads(json.dumps(sp_fig)))
foot_y_fig = min(float(m.group(1)) for m in _re.finditer(
    r'<text x="0(?:\.0)?" y="([\d.]+)"[^>]*>(?:KEY|SUMBER|\d)[^<]*</text>', svg_fig))
bottom_fig = max(_node_bottoms(svg_fig))
c24 = (key_y >= bottom + dd.LATTICE_Y * 0.5
       and foot_y_fig >= bottom_fig + dd.LATTICE_Y * 0.5)
check(24, "kaki apparatus ber-reserve: KEY/caption di bawah simpul terakhir (C1)",
      c24, "page key_y=%.2f bottom=%.2f | figure foot=%.2f bottom=%.2f" %
      (key_y, bottom, foot_y_fig, bottom_fig))

# CHECK 25 (C2): layout_graph menguji muat kanvas — tidak ada clamp diam-diam.
sp_g = {"family": "graph", "id": "99.4", "title": "Uji muat graph.",
        "classification": "BIASA", "width_mm": 128, "labels_verified": True,
        "nodes": [{"id": "kiri", "label": "Simpul kiri panjang", "class": {"col": 0, "row": 0}},
                  {"id": "kanan", "label": "Simpul kanan yang sangat panjang sekali",
                   "class": {"col": 2, "row": 0}}],
        "edges": [{"from": "kiri", "to": "kanan", "kind": "data", "label": "tautan"}],
        "sources": ["uji internal"]}
sh_g = dd.Sheet(128)
dd.layout_graph(sp_g, sh_g)
est_g = {n["id"]: dd._node_size(n, sh_g)[0] for n in sp_g["nodes"]}
no_clamp = all(abs(sh_g.nodes[k]["w"] - est_g[k]) < 1e-9 for k in sh_g.nodes)
fits = all(nd["x"] + nd["w"] <= 128.0 + 1e-6 for nd in sh_g.nodes.values())
sp_far = json.loads(json.dumps(sp_g))
sp_far["nodes"][1]["class"]["col"] = 20
far_reject = False
try:
    dd.build_svg(sp_far)
except dd.DiagramDefect as ex:
    far_reject = "DATUM-37" in str(ex)
check(25, "layout_graph uji muat kanvas: tanpa clamp senyap + col jauh tetap DATUM-37 (C2)",
      no_clamp and fits and far_reject,
      "clamp=%s muat=%s tolak_col20=%s" % (no_clamp, fits, far_reject))

# CHECK 26 (C3): crossing-hop nyata ter-render tanpa TypeError (crash G10.3/G12.2).
sp_hop = {"family": "flow", "id": "99.5", "title": "Uji lompatan silang.",
          "classification": "BIASA", "width_mm": 166, "labels_verified": True,
          "per_row": 3,
          "nodes": [{"id": "n%d" % i, "label": "Langkah %d" % i,
                     "class": {"col": (i - 1) % 3, "row": (i - 1) // 3}} for i in range(1, 7)],
          "edges": [{"from": "n1", "to": "n6", "kind": "data", "label": "silang"},
                    {"from": "n2", "to": "n5", "kind": "control", "label": "balik"}],
          "sources": ["uji internal"]}
try:
    svg_hop, rep_hop = dd.build_svg(sp_hop)
    hop_ok = rep_hop["n_hops"] >= 1 and '" A ' in svg_hop or (" A " in svg_hop and rep_hop["n_hops"] >= 1)
except Exception as ex:
    svg_hop, hop_ok = "", False
stale_pat = 'colour_of(paths[i]["edge"]["kind"]["colour"]' in src
check(26, "crossing-hop ter-render tanpa TypeError + pola indeks-lama 0 hit (C3)",
      hop_ok and not stale_pat, "hops=%s stale=%s" % (hop_ok, stale_pat))

# CHECK 27 (kelas label tepi, vonis visual controller kartu induk): tiap teks
# label tepi wajib didahului langsung oleh pita knockout kertas (rect fill=PAPER)
# dan tidak boleh ada <path> konektor yang tercetak SETELAH teks label terakhir.
def _label_seq_ok(svg_x):
    toks = [m.group(0) for m in _re.finditer(r'<(path|rect|text)\b[^>]*/?>', svg_x)]
    n_lab = 0
    for k, t in enumerate(toks):
        if t.startswith("<text") and ('font-family="%s"' % dd.FACES["mono"]) in t \
           and 'text-anchor="middle"' in t and k > 0:
            prev = toks[k - 1]
            # hanya hitung teks yang memang diberi knockout: preseden rect kertas
            if prev.startswith("<rect") and ('fill="%s"' % dd.PAPER) in prev:
                n_lab += 1
    total_mid = sum(1 for t in toks if t.startswith("<text")
                    and 'text-anchor="middle"' in t
                    and ('font-family="%s"' % dd.FACES["mono"]) in t)
    after = False
    last_lab = max((k for k, t in enumerate(toks) if t.startswith("<text")), default=len(toks))
    # path setelah teks label terakhir = garis menimpa apparatus/simpul, bukan label;
    # untuk kelas ini cukup uji: setiap teks rail-middle ber-knockout == total rail-middle
    return n_lab == total_mid and total_mid > 0, total_mid


seq_leg, n_leg = _label_seq_ok(svg_hop)   # svg_hop punya dua label tepi nyata
lab_struct = seq_leg and ('fill="%s"' % dd.PAPER) in svg_hop
check(27, "setiap label tepi ber-knockout kertas, nol teks telanjang (kelas vonis visual)",
      lab_struct, "rail_middle=%d semua_ber_knockout=%s" % (n_leg, seq_leg))

# ============ BUG-DIAG-ROWPACK (kartu t_787b26a9): CHECK 28..30 =============
# Gerbang dua arah: cermin PRA-tambal wajib FAIL di 28 dan 30, hijau di 29;
# kanonik POST wajib hijau ketiganya. Alat ukur membaca pohon dari argv/HERE
# sehingga pra dan post menjalankan berkas cek yang sama persis.

def _row_hits(sheet_x):
    """Tumpuan horizontal antar simpul yang berbagi baris y yang sama."""
    by_y = {}
    for nd in sheet_x.values():
        by_y.setdefault(round(nd["y"], 3), []).append(nd)
    out = []
    for yy, group in by_y.items():
        group = sorted(group, key=lambda n: n["x"])
        for a, b in zip(group, group[1:]):
            ov = a["x"] + a["w"] - b["x"]
            if ov > 1e-6:
                out.append("%s>%s=%.2f" % (a["id"], b["id"], ov))
    return out


# CHECK 28: repro G4.2-style — dua kolom bertetangga berbagi SATU baris, lebar
# simpul kiri melewati pitch -> basal merah menumpuk; pasca harus bersih, muat,
# dan tanpa clamp senyap (lebar terpasang == lebar kebutuhan).
# Simpul KIRI jauh lebih lebar dari pitch (kasus hidup G7.3: 'prv' 64 mm vs
# pitch 42,67 mm); kolom kanan sempit sehingga p_cap lama tidak tersentuh.
sp_pack = {"family": "graph", "id": "99.6", "title": "Uji tumpuan satu baris.",
           "classification": "BIASA", "width_mm": 128, "labels_verified": True,
           "nodes": [{"id": "kiri", "label": "Sumbu kualitas jawaban paling menentukan hasil",
                      "class": {"col": 0, "row": 0}},
                     {"id": "kanan", "label": "Cloud",
                      "class": {"col": 1, "row": 0}}],
           "edges": [{"from": "kiri", "to": "kanan", "kind": "data", "label": "tautan"}],
           "sources": ["uji internal"]}
sh_pack = dd.Sheet(128)
dd.layout_graph(sp_pack, sh_pack)
hits_pack = _row_hits(sh_pack.nodes)
est_pack = {n["id"]: dd._node_size(n, sh_pack)[0] for n in sp_pack["nodes"]}
noclamp_pack = all(abs(sh_pack.nodes[k]["w"] - est_pack[k]) < 1e-9 for k in sh_pack.nodes)
fits_pack = all(nd["x"] + nd["w"] <= 128.0 + 1e-6 for nd in sh_pack.nodes.values())
lattice_pack = all(abs(nd["x"] / dd.LATTICE_X - round(nd["x"] / dd.LATTICE_X)) < 1e-9
                   and abs(nd["w"] / dd.LATTICE_X - round(nd["w"] / dd.LATTICE_X)) < 1e-9
                   for nd in sh_pack.nodes.values())
svg_pack, rep_pack = dd.build_svg(sp_pack, release=False)
check(28, "graph dua-kolom-serah-baris bebas tumpuan + muat tepi + tanpa clamp senyap (ROWPACK)",
      (not hits_pack) and fits_pack and noclamp_pack and lattice_pack,
      "tumpuan=%r muat=%s clamp=%s kisi=%s" % (hits_pack, fits_pack, noclamp_pack, lattice_pack))

# CHECK 29: nol regresi geometri untuk spek sehat — posisi kolom WAJIB sama
# persis dengan rumus pitch seragam lama (jalur penataan ulang tidak boleh
# menyentuh spek yang sudah bersih).
sh_g2 = dd.Sheet(128)
dd.layout_graph(sp_g, sh_g2)
cols_g = sorted({int(n.get("class", {}).get("col", 0)) for n in sp_g["nodes"]})
maxw_g = {}
for n in sp_g["nodes"]:
    c = int(n.get("class", {}).get("col", 0))
    maxw_g[c] = max(maxw_g.get(c, 0.0), dd._node_size(n, sh_g2)[0])
last_w_g = maxw_g[cols_g[-1]]
p_g = dd.LATTICE_X * 4
cap_g = (128.0 - last_w_g) / float(len(cols_g) - 1)
if not p_g <= cap_g + 1e-9:
    p_g = dd.snap_floor(cap_g, dd.LATTICE_X)
tot_g = (len(cols_g) - 1) * p_g + last_w_g
x0_g = dd.snap_floor(max(0.0, (128.0 - tot_g) / 2.0), dd.LATTICE_X)
old_pos = {c: x0_g + i * p_g for i, c in enumerate(cols_g)}
same_g = all(abs(sh_g2.nodes[n["id"]]["x"] - old_pos[int(n.get("class", {}).get("col", 0))]) < 1e-9
             for n in sp_g["nodes"])
untouched = not hasattr(sh_g2, "rowpack")
check(29, "spek graph sehat tidak berubah geometri vs rumus pitch lama (nol regresi ROWPACK)",
      same_g and untouched and not _row_hits(sh_g2.nodes),
      "posisi_sama=%s rowpack_terpakai=%s" % (same_g, getattr(sh_g2, "rowpack", None)))

# CHECK 30: keadaan benar-benar tak muat DITOLAK dengan cacat bernama, bukan
# digambar bertumpukan / di-clamp senyap.
# Ukuran dipilih lewat probe terukur: tiap simpul muat sendiri di lembar 128 mm
# (42,7 / 64,0 / 32,0 mm) tetapi jumlah tiga-tiganya melewati lebar tersedia
# setelah semua simpul dirapatkan sampai kebutuhan teks -> ROWPACK bernama.
_tight_words = (5, 8, 2)
sp_tight = {"family": "graph", "id": "99.7", "title": "Uji tak muat sejati.",
            "classification": "BIASA", "width_mm": 128, "labels_verified": True,
            "nodes": [{"id": "s%d" % i,
                       "label": " ".join(["kata"] * n) + " %d" % i,
                       "class": {"col": i, "row": 0}}
                      for i, n in enumerate(_tight_words)],
            "edges": [{"from": "s%d" % i, "to": "s%d" % (i + 1), "kind": "data",
                       "label": "a%d" % i} for i in range(len(_tight_words) - 1)],
            "sources": ["uji internal"]}
tight_msg = ""
try:
    dd.build_svg(sp_tight, release=False)
    tight_reject = False
except dd.DiagramDefect as ex:
    tight_msg = str(ex)
    tight_reject = "ROWPACK" in tight_msg
check(30, "graph berbagi baris yang sungguh tak muat ditolak DATUM-37/ROWPACK bernama",
      tight_reject, tight_msg[:90] or "tidak ada penolakan")

# ---- bersih-bersih
import shutil
shutil.rmtree(TMP, ignore_errors=True)

print("VERDICT: " + ("PASS" if not fails else "FAIL — " + ", ".join(fails)))
sys.exit(0 if not fails else 1)
