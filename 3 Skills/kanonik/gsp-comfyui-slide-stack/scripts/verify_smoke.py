# -*- coding: utf-8 -*-
"""verify_smoke.py — kontrak verifikasi deterministik (TA §4). stdlib-only.
Usage: python verify_smoke.py <folder-misi>
"""
import json, os, re, struct, sys, zipfile, datetime

BASE = os.path.abspath(sys.argv[1] if len(sys.argv) > 1 else ".")
SMOKE = os.path.join(BASE, "smoke")
R = []
def out(n, s, nm):
    R.append((n, s, nm)); print(f"CHECK {n}: {s} — {nm}")

def png_info(p):
    """(w,h,color_type) via IHDR; color_type 6 = RGBA."""
    try:
        with open(p, "rb") as f:
            if f.read(8) != b"\x89PNG\r\n\x1a\n": return None, None, None
            f.read(4)
            if f.read(4) != b"IHDR": return None, None, None
            w, h, bd, ct = struct.unpack(">IIBB", f.read(10))
            return w, h, ct
    except Exception:
        return None, None, None

LED = json.load(open(os.path.join(SMOKE, "ledger.json"), encoding="utf-8"))
def u(i): return next((x for x in LED["units"] if x["id"] == i), None)
def art(i):
    x = u(i)
    p = os.path.join(BASE, x["artifact"]) if x else None
    return p if p and os.path.exists(p) else None

# 1 SM-01
p = art("SM-01")
if p:
    w, h, _ = png_info(p); sz = os.path.getsize(p)
    out(1, "PASS" if sz > 200_000 and w and min(w, h) >= 1024 else "FAIL", f"SM-01 {w}x{h} {sz//1024}KB")
else: out(1, "FAIL", "SM-01 hilang")
# 2 SM-02 RGBA
p = art("SM-02")
if p:
    _, _, ct = png_info(p)
    out(2, "PASS" if ct == 6 else "FAIL", f"SM-02 color-type={ct} (6=RGBA)")
else: out(2, "FAIL", "SM-02 hilang")
# 3 SM-03 teks (review manual dicatat di ledger.notes)
p = art("SM-03"); nt = (u("SM-03") or {}).get("notes", "")
if p:
    w, h, _ = png_info(p)
    st = "PASS" if "TEKS-TERBACA" in nt else ("FAIL" if "TEKS-SALAH" in nt else "NEEDS_REVIEW")
    out(3, st, f"SM-03 {w}x{h}; notes='{nt[:60]}'")
else: out(3, "NEEDS_REVIEW", "SM-03 menunggu bobot Qwen-2512")
# 4 SM-04 + sumber SVG
p = art("SM-04"); sv = os.path.join(SMOKE, "sources", "SM04_diagram.svg")
w, h, _ = png_info(p) if p else (0, 0, 0)
out(4, "PASS" if p and os.path.exists(sv) and w >= 1200 and h >= 600 else "FAIL", f"SM-04 {w}x{h} sumber={'ada' if os.path.exists(sv) else 'HILANG'}")
# 5 SM-05
p = art("SM-05"); w, h, _ = png_info(p) if p else (0, 0, 0)
out(5, "PASS" if p and min(w, h) >= 1024 else "FAIL", f"SM-05 {w}x{h}")
# 6 SM-06 >= 2x SM-01
p1, p6 = art("SM-01"), art("SM-06")
if p1 and p6:
    w1 = png_info(p1)[0]; w6 = png_info(p6)[0]
    out(6, "PASS" if w6 >= 2 * w1 else "FAIL", f"SM-06 {w6}px vs sumber {w1}px")
else: out(6, "FAIL", "SM-06/SM-01 hilang")
# 7 SM-07 >=3 PNG
d = os.path.join(SMOKE, "SM07_keyframes")
kfs = [f for f in os.listdir(d) if f.lower().endswith(".png")] if os.path.isdir(d) else []
out(7, "PASS" if len(kfs) >= 3 else "FAIL", f"SM-07 {len(kfs)} frame")
# 8 SM-08 mp4
p = art("SM-08")
if p and os.path.getsize(p) > 100_000:
    pr = u("SM-08")["params"]
    out(8, "PASS" if pr.get("length") == 49 and pr.get("fps") == 24 else "NEEDS_REVIEW", f"SM-08 {os.path.getsize(p)//1024}KB {pr}")
else: out(8, "NEEDS_REVIEW", "SM-08 menunggu bobot Wan2.2")
# 9 SM-09 GLB
p = art("SM-09")
if p and os.path.getsize(p) > 1_000_000:
    out(9, "PASS" if open(p, "rb").read(4) == b"glTF" else "FAIL", f"SM-09 {os.path.getsize(p)//1024}KB")
else: out(9, "NEEDS_REVIEW", "SM-09 menunggu bobot TRELLIS (gerbang Q7)")
# 10 SM-10 + sumber HTML
p = art("SM-10"); src = os.path.join(SMOKE, "sources", "SM10_headline.html")
out(10, "PASS" if p and os.path.exists(src) else "FAIL", "SM-10 + sumber HTML")
# 11 SM-11 pptx >=3 slide
p = art("SM-11")
if p:
    z = zipfile.ZipFile(p); n = [x for x in z.namelist() if re.fullmatch(r"ppt/slides/slide\d+\.xml", x)]
    out(11, "PASS" if len(n) >= 3 else "FAIL", f"SM-11 {len(n)} slide")
else: out(11, "FAIL", "SM-11 hilang")
# 12 SM-12 html >=3 section, src utuh
p = art("SM-12")
if p:
    html = open(p, encoding="utf-8").read()
    secs = len(re.findall(r"<section", html))
    srcs = re.findall(r'src="([^"]+)"', html)
    broken = [s for s in srcs if not s.startswith("http") and not os.path.exists(os.path.join(os.path.dirname(p), s))]
    out(12, "PASS" if secs >= 3 and not broken else "FAIL", f"SM-12 {secs} section, putus={broken}")
else: out(12, "FAIL", "SM-12 hilang")
# 13 SM-13 concat mp4
p = art("SM-13")
out(13, "PASS" if p and os.path.getsize(p) > 100_000 else "NEEDS_REVIEW", "SM-13" + ("" if p else " menunggu klip"))
# 14 SM-14 chain proof
p = art("SM-14")
if p:
    t = open(p, encoding="utf-8").read()
    batas = len(re.findall(r"BATAS\s+\d+.*?PASS", t))
    out(14, "PASS" if batas >= 3 else "FAIL", f"SM-14 {batas} batas terbukti")
else: out(14, "NEEDS_REVIEW", "SM-14 belum dibuat")
# 15 ledger utuh
units = LED["units"]
orph = [x["id"] for x in units if x.get("exit") == 0 and not art(x["id"]) and not os.path.isdir(os.path.join(BASE, x["artifact"]))]
pend = [x["id"] for x in units if x.get("exit") is None]
out(15, "PASS" if len(units) == 14 and not orph else "FAIL", f"{len(units)} unit; exit0-tanpa-artefak={orph}; belum-jalan={pend}")
# 16 no OOM
oom = [x["id"] for x in units if x.get("oom")]
out(16, "PASS" if not oom else "FAIL", f"OOM={oom}")
# 17 kontrak amandemen + Q7
c = open(os.path.join(BASE, "contract.md"), encoding="utf-8").read()
out(17, "PASS" if ("SALAH" in c and "Q7" in c) else "FAIL", "amandemen+Q7")
# 18 skill
sk_dirs = [r"C:\Users\TRIAL\workspace\gsp-hermes\skills\gsp-comfyui-slide-stack",
           os.path.expandvars(r"%LOCALAPPDATA%\hermes\skills\gsp\gsp-comfyui-slide-stack")]
found = next((d for d in sk_dirs if os.path.exists(os.path.join(d, "SKILL.md"))), None)
if found:
    head = open(os.path.join(found, "SKILL.md"), encoding="utf-8").read(400)
    out(18, "PASS" if head.startswith("---") and "name: gsp-comfyui-slide-stack" in head else "FAIL", f"skill @ {found}")
else: out(18, "FAIL", "skill belum ada")

fails = [r for r in R if r[1] == "FAIL"]; needs = [r for r in R if r[1] == "NEEDS_REVIEW"]
verdict = "FAIL" if fails else ("NEEDS_REVIEW" if needs else "PASS")
print(f"VERDICT: {verdict} ({len(R)-len(fails)-len(needs)}/{len(R)} pass, {len(needs)} review, {len(fails)} fail)")
os.makedirs(os.path.join(BASE, "verification"), exist_ok=True)
rp = os.path.join(BASE, "verification", f"report_{datetime.date.today()}.md")
with open(rp, "a", encoding="utf-8") as f:
    f.write(f"\n## Run {datetime.datetime.now():%Y-%m-%d %H:%M:%S}\n\n")
    for n, s, nm in R: f.write(f"- CHECK {n}: {s} — {nm}\n")
    f.write(f"\n**VERDICT: {verdict}**\n")
print("REPORT", rp)
