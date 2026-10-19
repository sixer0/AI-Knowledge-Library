#!/usr/bin/env python
"""Audit kelengkapan cakupan halaman studi vision per set (GSP fleet).

Pemakaian:
  python page_coverage_audit.py <render_all_dir> <study_dir>

<render_all_dir> : folder berisi subfolder per set dengan page_NN.png hasil pre-render.
<study_dir>      : folder berisi DS-*.md hasil worker vision (bagian '## Halaman referensi').

Laporan per set: OK / PARTIAL (daftar halaman hilang) / MISSING.
Exit code 0 hanya bila SEMUA set lengkap p1..pN — pakai sebagai gerbang sebelum
klaim selesai atau sebelum memutuskan re-dispatch.

Catatan regex (pelajaran 01-09): pola naive `^\W*p(\d{1,2})` kehilangan `p10:`.
Di sini dua pola digabung: token `p<N>` di mana pun + `<N>:` di awal baris.
"""
import sys, os, re, glob


def pages_in(render_dir):
    return len(glob.glob(os.path.join(render_dir, "page_*.png")))


def slug_tokens(name):
    toks = [t for t in re.split(r"[^a-z0-9]+", name.lower()) if len(t) > 2]
    return toks[:2] or toks


def find_study(study_dir, set_name):
    toks = slug_tokens(set_name)
    for f in sorted(glob.glob(os.path.join(study_dir, "DS-*.md"))):
        low = os.path.basename(f).lower()
        if toks and all(t in low for t in toks):
            return f
    return None


def coverage(md_path, expected):
    t = open(md_path, encoding="utf-8").read()
    sec = re.search(r"##\s*Halaman referensi(.*?)(?=\n##\s|\Z)", t, re.S)
    block = sec.group(1) if sec else t  # fallback: whole file bila heading beda
    seen = set()
    for m in re.finditer(r"[Pp](\d{1,3})", block):
        seen.add(int(m.group(1)))
    for m in re.finditer(r"(?m)^\s*(\d{1,3})\s*[:—\-–]", block):
        seen.add(int(m.group(1)))
    return [i for i in range(1, expected + 1) if i not in seen]


def main():
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(2)
    render_root, study_dir = sys.argv[1], sys.argv[2]
    ok = True
    total_src = total_cov = 0
    for d in sorted(os.listdir(render_root)):
        rd = os.path.join(render_root, d)
        if not os.path.isdir(rd):
            continue
        exp = pages_in(rd)
        if not exp:
            continue
        total_src += exp
        f = find_study(study_dir, d)
        if not f:
            print(f"MISSING  {d} (0/{exp} halaman; file studi tidak ada)")
            ok = False
            continue
        missing = coverage(f, exp)
        cov = exp - len(missing)
        total_cov += cov
        if missing:
            ok = False
            print(f"PARTIAL  {d} ({cov}/{exp}) file={os.path.basename(f)} missing={missing}")
        else:
            print(f"OK       {d} ({cov}/{exp}) file={os.path.basename(f)}")
    print(f"\nTOTAL halaman: {total_cov}/{total_src} tercakup")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
