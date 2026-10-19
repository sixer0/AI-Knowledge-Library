# -*- coding: utf-8 -*-
"""Validator design_master.json (SOP Imagegen 2.1 §13) - gerbang keras pra-serah.

Pakai: python validate_design_master.py <design_master.json> [--refs-base DIR] [--skip-sha]
Exit 0 = PASS (laporan tercetak); exit 1 = FAIL dengan daftar cacat.
"""
import argparse, hashlib, json, os, re, sys

HEX_RE = re.compile(r"#[0-9A-Fa-f]{6}\b")
PLACE_RE = re.compile(r"<[^<>\n]{1,80}>")
# tag referensi SOP (<image1> dst) bukan placeholder; tanpa anchor agar bisa sub dalam teks
IMAGE_TAG_RE = re.compile(r"<image\d+>")
REQ_TOP = ["schema", "brand", "version", "approved_by_user", "language",
           "design_direction", "sources", "references", "brand_rules",
           "deck_blocks", "identity_strings", "archetypes",
           "known_failures", "seed_rule", "changelog"]
ALLOW_EMPTY = {"lexicon_cues"}  # kosong sah; diisi setelah gagal render (SOP)
REQ_RULES = ["background", "palette_in_order", "accent_usage", "title_typography",
             "body_typography", "icon_style", "panels", "logo_description",
             "logo_rules", "voice"]
REQ_BLOCKS = ["block1_opener_prefix", "block2_references", "block3_transitions",
              "block4_style", "block5_footer"]


def deep_placeholders(obj, path="$"):
    out = []
    if isinstance(obj, str):
        s = IMAGE_TAG_RE.sub("", obj)  # tag <imageN> sah, bukan placeholder
        for m in PLACE_RE.finditer(s):
            out.append(f"{path}: placeholder {m.group(0)!r}")
    elif isinstance(obj, dict):
        for k, v in obj.items():
            out += deep_placeholders(v, f"{path}.{k}")
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            out += deep_placeholders(v, f"{path}[{i}]")
    return out


def sha256(path):
    h = hashlib.sha256()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("json_path")
    ap.add_argument("--refs-base", default=None, help="dasar relatif path refs (default: folder json)")
    ap.add_argument("--skip-sha", action="store_true", help="jangan cek sha256 berkas refs")
    args = ap.parse_args()
    d = json.load(open(args.json_path, encoding="utf-8"))
    base = args.refs_base or os.path.dirname(os.path.abspath(args.json_path))
    fails, warns = [], []

    for k in REQ_TOP:
        if k not in d or d[k] in ("", None, {}, []):
            fails.append(f"field wajib hilang/kosong: {k}")
    if d.get("schema") != "design_master_v1":
        fails.append(f"schema harus 'design_master_v1', dapat {d.get('schema')!r}")
    if str(d.get("language", "")).strip().lower() not in ("english", "indonesian"):
        fails.append(f"language harus 'English' atau 'Indonesian', dapat {d.get('language')!r}")

    fails += deep_placeholders(d)

    br = d.get("brand_rules", {})
    for k in REQ_RULES:
        if not str(br.get(k, "")).strip():
            fails.append(f"brand_rules.{k} kosong")
    for k, v in br.items():
        txts = v if isinstance(v, list) else [v]
        for t in txts:
            if isinstance(t, str) and HEX_RE.search(t):
                fails.append(f"brand_rules.{k} memuat HEX ({HEX_RE.findall(t)}) - SOP §13.2 minta warna dalam kata")

    blocks = d.get("deck_blocks", {})
    for k in REQ_BLOCKS:
        v = str(blocks.get(k, "")).strip()
        sisa = IMAGE_TAG_RE.sub("", v)
        if not v or PLACE_RE.search(sisa):
            fails.append(f"deck_blocks.{k} kosong/placeholder")

    refs = d.get("references", {})
    files = refs.get("files", [])
    if not files:
        fails.append("references.files kosong")
    if len(files) > 10:
        fails.append(f"references.files {len(files)} > 10 (plafon request)")
    logo_idx = [i for i, f in enumerate(files) if "logo" in str(f.get("role", "")).lower()]
    if logo_idx and logo_idx[-1] != len(files) - 1:
        fails.append("logo lockup bukan entri TERAKHIR references.files")
    for i, f in enumerate(files):
        fp = f.get("file", "")
        if not fp.lower().endswith(".png"):
            fails.append(f"refs[{i}] bukan .png: {fp}")
            continue
        full = fp if os.path.isabs(fp) else os.path.join(base, fp)
        if not os.path.isfile(full):
            fails.append(f"refs[{i}] berkas tidak ada: {full}")
        elif not args.skip_sha:
            want = str(f.get("sha256", ""))
            got = sha256(full)
            if not want or want.lower() != got:
                fails.append(f"refs[{i}] sha256 tidak cocok ({fp})")
    ident = d.get("identity_strings", [])
    if not [s for s in ident if isinstance(s, str) and s.strip() and not s.startswith("<")]:
        fails.append("identity_strings kosong/placeholder")
    if str(d.get("approved_by_user", "")).startswith("<"):
        warns.append("approved_by_user masih placeholder - sah hanya saat pengajuan approval")

    print(f"== VALIDASI design_master: {os.path.basename(args.json_path)} ==")
    print(f"brand={d.get('brand')} v{d.get('version')} refs={len(files)} "
          f"fails={len(fails)} warns={len(warns)}")
    for x in fails:
        print("  FAIL:", x)
    for x in warns:
        print("  WARN:", x)
    if fails:
        print("VERDICT: FAIL")
        sys.exit(1)
    print("VERDICT: PASS")


if __name__ == "__main__":
    main()
