# -*- coding: utf-8 -*-
"""build_deck_html.py — SM-12: mini-deck HTML >=3 <section>, src gambar wajib ADA (relatif).
Usage: uv run --python 3.11 python build_deck_html.py <out.html> --hero H.png --keyframes DIR --diagram D.png
"""
import argparse, glob, os, shutil

def rel(outdir, p):
    if not p or not os.path.exists(p): return None
    dst = os.path.join(outdir, "assets", os.path.basename(p))
    if os.path.abspath(p) != os.path.abspath(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True); shutil.copyfile(p, dst)
    return f"assets/{os.path.basename(p)}"

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--hero"); ap.add_argument("--keyframes")
    ap.add_argument("--diagram"); ap.add_argument("--headline")
    a = ap.parse_args()
    outdir = os.path.dirname(os.path.abspath(a.out))
    hero = rel(outdir, a.hero); dia = rel(outdir, a.diagram); head = rel(outdir, a.headline)
    kf = [rel(outdir, f) for f in sorted(glob.glob(os.path.join(a.keyframes, "*.png")))[:3]] if a.keyframes else []
    kf_html = "".join(f'<figure><img src="{k}"><figcaption>Shot {i+1}</figcaption></figure>' for i, k in enumerate(kf) if k)
    hero_tag = f'<figure><img src="{hero}" alt="hero"></figure>' if hero else ""
    dia_tag = f'<figure><img src="{dia}" alt="diagram"></figure>' if dia else ""
    head_tag = f'<img src="{head}" alt="banner">' if head else "<h1>Keamanan Cerdas, Dimulai dari Aset yang Tepat</h1>"
    html = f"""<!doctype html><html lang="id"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Mini Deck — GSP slide-stack</title>
<style>
 body{{margin:0;font-family:'Segoe UI',Arial,sans-serif;background:#0B2D5C;color:#fff}}
 section{{min-height:100vh;display:flex;flex-direction:column;justify-content:center;padding:6vh 8vw;box-sizing:border-box;border-bottom:2px solid #F2A900}}
 h1{{font-size:clamp(28px,5vw,56px);margin:0 0 12px}} h2{{color:#9DB6D4;font-size:clamp(18px,2.4vw,28px)}}
 img{{max-width:100%;border-radius:10px}} .row{{display:flex;gap:16px;flex-wrap:wrap;align-items:center}}
 figure{{margin:0;flex:1 1 280px}} figcaption{{color:#9DB6D4;font-size:14px;margin-top:6px}}
</style></head><body>
<section>{head_tag}<h2>GSP Swarm HQ — pipeline slide-stack ComfyUI multi-model</h2></section>
<section><h1>Hero & Diagram</h1><div class="row">{hero_tag}{dia_tag}</div></section>
<section><h1>Storyboard Klip</h1><div class="row">{kf_html}</div><h2>Keyframe kanonik → Wan2.2 i2v → concat</h2></section>
</body></html>"""
    open(a.out, "w", encoding="utf-8").write(html)
    print("SAVED", a.out)

if __name__ == "__main__":
    main()
