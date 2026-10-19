#!/usr/bin/env python3
"""STT-W8 independent verification: citation-token integrity + quote grounding.

Modes:
  seg  Vn ts[,ts...]   dump transcript segment starts (for human reading)
  cites                 every (Vn, ts) token in module == real segment start?
  quotes                hardcoded quote needles found in cited transcript?
Exit 0 only when all checks PASS.
"""
import re, sys, io, os

BASE = os.path.join(os.path.dirname(os.path.abspath(__file__)))
ROOT = os.path.dirname(BASE)
MAP = {"V1": "V1_5_N84t1rUU0.md", "V2": "V2_DYdvJCxWd6M.md",
       "V3": "V3_8yE6G1Lup1s.md", "V4": "V4_G47mnkGkYwQ.md",
       "V5": "V5_KKmnpuPdnUY.md"}
MODULE = os.path.join(ROOT, "05_module", "HERMES-ZERO-TO-HERO.md")

def load(vn):
    with open(os.path.join(ROOT, "02_transcripts", MAP[vn]), encoding="utf-8") as f:
        return f.read()

def to_secs(ts):
    parts = [int(p) for p in ts.split(":")]
    if len(parts) == 2:
        return parts[0] * 60 + parts[1]
    return parts[0] * 3600 + parts[1] * 60 + parts[2]

def fmt(secs):
    h, r = divmod(secs, 3600)
    m, s = divmod(r, 60)
    return f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}"

def starts(vn):
    return {to_secs(m) for m in re.findall(r"\*\*\[(\d{1,2}:\d{2}(?::\d{2})?)\]\*\*", load(vn))}

def norm(text):
    text = re.sub(r"\*\*\[\d{1,2}:\d{2}(?::\d{2})?\]\*\*", " ", text)
    return re.sub(r"\s+", " ", text).lower()

def tokens_in_module():
    """Yield (vn, ts_secs, raw) for every citation timestamp in the module."""
    out = []
    with open(MODULE, encoding="utf-8") as f:
        mod = f.read()
    # bracketed citation groups only (skip prose); includes Appendix rows
    for grp in re.findall(r"\[[^\]\[]*\]", mod):
        if grp.lower().startswith("[http"):
            continue
        cur = None
        for m in re.finditer(r"(V\d)\s*(\d{1,2}:\d{2}(?::\d{2})?)|(\d{1,2}:\d{2}(?::\d{2})?)", grp):
            if m.group(1):
                cur, ts = m.group(1), m.group(2)
            elif cur:
                ts = m.group(3)
            else:
                continue
            if cur in MAP:
                out.append((cur, to_secs(ts), m.group(0).strip()))
    return out

def mode_cites():
    S = {vn: starts(vn) for vn in MAP}
    toks = tokens_in_module()
    uniq = sorted(set((v, s) for v, s, _ in toks))
    bad = [(v, s) for v, s in uniq if s not in S[v]]
    print(f"CHECK 1 citation tokens: total={len(toks)} unique={len(uniq)}")
    if bad:
        for v, s in bad:
            print(f"  FAIL {v} {fmt(s)} — no segment starts at this time")
        print("CHECK 1: FAIL")
        return False
    print("CHECK 1: PASS (every unique (Vn,ts) equals a real segment start)")
    return True

QUOTES = [
    ("V3", "the agent just deleted it"),
    ("V3", "she lost years of emails"),
    ("V1", "if you have the hardware and the ability of doing this"),
    ("V1", "help me use ollama to download open-source models"),
    ("V1", "gives you direct control with the model"),
    ("V1", "took me about like 30 minutes to set up"),
    ("V5", "not the smartest but it will work"),
    ("V5", "free, it's private, it's slower, but it works"),
    ("V5", "start with zero at max 20 bucks a month"),
    ("V5", "you are flying blind"),
    ("V5", "watch the agent actually think in real time"),
    ("V5", "i need my fathom meetings in here"),
    ("V5", "this will drive you nuts"),
    ("V5", "minute time savings here at least"),
    ("V5", "four patches"),
    ("V5", "quarter payment option"),
    ("V5", "green flags"),
    ("V5", "no matter the tool"),
    ("V5", "less than a penny"),
    ("V5", "daily session snapshots"),
    ("V5", "one-on-one coaching"),
    ("V5", "deploy to netlify"),
    ("V5", "signup"),
    ("V2", "restart gateway"),
    ("V2", "hermes doctor"),
    ("V2", "health report"),
    ("V3", "trading bot"),
    ("V3", "voice memo"),
    ("V3", "hud"),
]

def mode_quotes():
    cache = {}
    ok = True
    for vn, needle in QUOTES:
        if vn not in cache:
            cache[vn] = norm(load(vn))
        hit = needle in cache[vn]
        print(f"  {'PASS' if hit else 'FAIL'} [{vn}] \"{needle}\"")
        ok = ok and hit
    print("CHECK 2:", "PASS" if ok else "FAIL")
    return ok

def mode_seg(args):
    vn = args[0]
    want = {to_secs(t) for t in args[1].split(",")}
    text = load(vn)
    for m in re.finditer(r"\*\*\[(\d{1,2}:\d{2}(?::\d{2})?)\]\*\*(.*?)(?=\n\s*\n|\Z)", text, re.S):
        if to_secs(m.group(1)) in want:
            body = re.sub(r"\s+", " ", m.group(2))[:1200]
            print("--- [" + m.group(1) + "] " + body)
    return True

if __name__ == "__main__":
    mode = sys.argv[1]
    if mode == "seg":
        mode_seg(sys.argv[2:])
        sys.exit(0)
    results = []
    if mode in ("cites", "all"):
        results.append(mode_cites())
    if mode in ("quotes", "all"):
        results.append(mode_quotes())
    print("VERDICT:", "PASS" if all(results) else "FAIL")
    sys.exit(0 if all(results) else 1)
