# -*- coding: utf-8 -*-
"""build_deck.py — SM-11: mini-deck PPTX >=3 slide dari aset hasil generate.
Slide 1: judul (vektor tipografi) · Slide 2: hero+cutout+chart (combine) · Slide 3: keyframe strip (animasi).
Usage: uv run --python 3.11 --with python-pptx --with pillow python build_deck.py <out.pptx> \
   --hero H.png --cutout C.png --chart G.png --keyframes DIR [--headline PNG]
"""
import argparse, glob, os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN

NAVY = RGBColor(0x0B, 0x2D, 0x5C); GRAY = RGBColor(0x44, 0x44, 0x44); GOLD = RGBColor(0xF2, 0xA9, 0x00)

def blank(prs): return prs.slides.add_slide(prs.slide_layouts[6])

def txt(slide, x, y, w, h, text, size, bold=False, color=None, align=PP_ALIGN.LEFT):
    box = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = box.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.text = text; p.font.size = Pt(size); p.font.bold = bold
    if color: p.font.color.rgb = color
    p.alignment = align
    return tf

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out"); ap.add_argument("--hero"); ap.add_argument("--cutout")
    ap.add_argument("--chart"); ap.add_argument("--keyframes"); ap.add_argument("--headline")
    a = ap.parse_args()
    prs = Presentation(); prs.slide_width = Inches(13.333); prs.slide_height = Inches(7.5)

    # --- slide 1: judul (tipografi vektor riil; opsi banner hasil generate)
    s = blank(prs)
    if a.headline and os.path.exists(a.headline):
        s.shapes.add_picture(a.headline, 0, 0, width=prs.slide_width)
    else:
        r = s.shapes.add_shape(1, 0, 0, prs.slide_width, prs.slide_height)
        r.fill.solid(); r.fill.fore_color.rgb = NAVY; r.line.fill.background()
    txt(s, 0.9, 2.6, 11.5, 1.4, "Keamanan Cerdas, Dimulai dari Aset yang Tepat", 40, True, RGBColor(0xFF,0xFF,0xFF))
    ln = s.shapes.add_shape(1, Inches(0.95), Inches(4.0), Inches(2.2), Inches(0.07))
    ln.fill.solid(); ln.fill.fore_color.rgb = GOLD; ln.line.fill.background()
    txt(s, 0.9, 4.3, 11.0, 0.8, "GSP Swarm HQ — pipeline slide-stack ComfyUI multi-model", 20, False, RGBColor(0xDB,0xE7,0xF5))

    # --- slide 2: combine hero + cutout + chart
    s = blank(prs)
    txt(s, 0.6, 0.4, 7.5, 0.9, "Cakupan Kapabilitas", 28, True, NAVY)
    if a.hero: s.shapes.add_picture(a.hero, Inches(7.0), Inches(0.5), height=Inches(4.2))
    if a.cutout: s.shapes.add_picture(a.cutout, Inches(0.6), Inches(1.6), height=Inches(3.0))
    if a.chart: s.shapes.add_picture(a.chart, Inches(0.6), Inches(4.9), height=Inches(2.2))
    txt(s, 4.0, 1.9, 2.9, 2.6, "Hero & aset produk dihasilkan Z-Image-Turbo; cutout transparan via BiRefNet; diagram angka via jalur vektor deterministik.", 13, False, GRAY)

    # --- slide 3: keyframe strip (bukti lapisan animasi)
    s = blank(prs)
    txt(s, 0.6, 0.4, 9.0, 0.9, "Storyboard Klip — Keyframe Konsisten", 28, True, NAVY)
    if a.keyframes:
        frames = sorted(glob.glob(os.path.join(a.keyframes, "*.png")))[:3]
        for i, f in enumerate(frames):
            s.shapes.add_picture(f, Inches(0.6 + i*4.2), Inches(1.7), width=Inches(4.0))
            txt(s, 0.6 + i*4.2, 4.1, 4.0, 0.5, f"Shot {i+1}", 14, False, GRAY)
    txt(s, 0.6, 6.6, 12.0, 0.6, "Keyframe = img2img dari aset kanonik (seed lock, denoise 0.4) → Wan2.2 i2v per shot → concat.", 13, False, GRAY)

    prs.save(a.out); print("SAVED", a.out)

if __name__ == "__main__":
    main()
