# -*- coding: utf-8 -*-
"""Extract clean timestamped transcripts from yt-dlp SRT files -> 02_transcripts/*.md
Deterministic, no LLM. Segments grouped to ~60s blocks with [MM:SS] markers."""
import re, os, json

BASE = r"C:\Users\TRIAL\workspace\Test STT"
RAW = os.path.join(BASE, "01_raw")
OUT = os.path.join(BASE, "02_transcripts")
os.makedirs(OUT, exist_ok=True)

VIDEOS = [
    ("V1", "5_N84t1rUU0", "Hermes Agent Fundamentals In 29 Minutes", "Tina Huang", 1780),
    ("V2", "DYdvJCxWd6M", "Hermes Agent - Full Tutorial & Setup Guide (For Beginners)", "Metics Media", 2063),
    ("V3", "8yE6G1Lup1s", "HERMES AGENT FULL COURSE 3 HOURS: Build & Sell (2026)", "Samin Yasar", 10967),
    ("V4", "G47mnkGkYwQ", "100 hours of Hermes Agent lessons in 46 minutes", "David Ondrej", 2820),
    ("V5", "KKmnpuPdnUY", "Master HERMES AGENT IN 4 HOURS", "Mani Kanasani", 14733),
]

TS = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+) --> ")

def parse_srt(path):
    with open(path, encoding="utf-8-sig") as f:
        txt = f.read()
    blocks = re.split(r"\n\s*\n", txt)
    cues = []
    for b in blocks:
        lines = [l for l in b.splitlines() if l.strip()]
        if len(lines) < 2:
            continue
        m = TS.search(lines[0])
        if not m:
            m = TS.search(lines[1] if len(lines) > 1 else "")
            if not m:
                continue
            tsec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            text_lines = lines[2:]
        else:
            tsec = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
            start_idx = 1
            # skip timing continuation lines
            while start_idx < len(lines) and "-->" in lines[start_idx]:
                start_idx += 1
            text_lines = lines[start_idx:]
        text = " ".join(l.strip() for l in text_lines)
        # strip inline tags & music markers
        text = re.sub(r"<[^>]+>", "", text)
        text = re.sub(r"&amp;nbsp;|&amp;amp;", "&", text)
        text = re.sub(r"♪[^ ]*|&amp;|&#\d+;", "", text)
        text = re.sub(r"\s+", " ", text).strip()
        if text and not re.fullmatch(r"[\[\(]?music[\]\)]?|[♪\.\-\s]+", text, re.I):
            cues.append((tsec, text))
    # dedupe consecutive identical (auto-subs rollup artifact)
    dedup = []
    for t, x in cues:
        if dedup and (dedup[-1][1] == x or x in dedup[-1][1]):
            continue
        dedup.append((t, x))
    return dedup

def fmt(sec):
    h, r = divmod(sec, 3600)
    m, s = divmod(r, 60)
    return (f"{h}:{m:02d}:{s:02d}" if h else f"{m}:{s:02d}")

manifest = []
for vid, youtube_id, title, channel, dur in VIDEOS:
    srt = os.path.join(RAW, f"{youtube_id}.en.srt")
    if not os.path.exists(srt):
        manifest.append({"id": vid, "file": None, "error": "missing srt"})
        continue
    cues = parse_srt(srt)
    # group into ~60s segments
    segs = []
    cur_start, cur_text = None, []
    for t, x in cues:
        if cur_start is None:
            cur_start = t
        if t - cur_start >= 60 and cur_text:
            segs.append((cur_start, " ".join(cur_text)))
            cur_start, cur_text = t, [x]
        else:
            cur_text.append(x)
    if cur_text:
        segs.append((cur_start, " ".join(cur_text)))
    words = sum(len(s[1].split()) for s in segs)
    cover_end = segs[-1][0] if segs else 0
    out = os.path.join(OUT, f"{vid}_{youtube_id}.md")
    with open(out, "w", encoding="utf-8") as f:
        f.write(f"# {vid}: {title}\n\n"
                f"- YouTube: https://www.youtube.com/watch?v={youtube_id}\n"
                f"- Channel: {channel} | Duration: {fmt(dur)} ({dur}s) | Language: en\n"
                f"- Transcript source: YouTube English captions via yt-dlp (extracted 2026-08-31)\n"
                f"- Coverage: captions run to {fmt(cover_end)} of {fmt(dur)} | {words:,} words | {len(segs)} segments\n\n---\n\n")
        for t, text in segs:
            f.write(f"**[{fmt(t)}]** {text}\n\n")
    manifest.append({"id": vid, "youtube_id": youtube_id, "title": title, "channel": channel,
                     "duration_s": dur, "file": os.path.basename(out), "words": words,
                     "segments": len(segs), "caption_end_s": cover_end,
                     "coverage_pct": round(100.0 * cover_end / dur, 1)})

with open(os.path.join(OUT, "_MANIFEST.md"), "w", encoding="utf-8") as f:
    f.write("# Transcript Manifest — Test STT mission (2026-08-31)\n\n")
    f.write("| ID | Title | Channel | Duration | Words | Segments | Coverage% |\n|---|---|---|---|---|---|---|\n")
    for m in manifest:
        f.write(f"| {m['id']} | {m.get('title')} | {m.get('channel')} | {fmt(m.get('duration_s',0))} | "
                f"{m.get('words',0):,} | {m.get('segments',0)} | {m.get('coverage_pct','?')} |\n")
print(json.dumps(manifest, indent=1))
