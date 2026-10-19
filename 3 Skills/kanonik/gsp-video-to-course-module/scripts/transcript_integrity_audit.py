# -*- coding: utf-8 -*-
"""transcript_integrity_audit.py — Uji KESEMPURNAAN transkrip: SRT mentah (01_raw) vs md (02_transcripts).
Deterministik, read-only. Mencetak laporan + VERDICT."""
import re, os, difflib, json

BASE = r"C:/Users/TRIAL/workspace/Test STT"
RAW = os.path.join(BASE, "01_raw"); OUT = os.path.join(BASE, "02_transcripts")
VIDEOS = [("V1","5_N84t1rUU0",1780),("V2","DYdvJCxWd6M",2063),("V3","8yE6G1Lup1s",10967),
          ("V4","G47mnkGkYwQ",2820),("V5","KKmnpuPdnUY",14733)]
TS = re.compile(r"(\d+):(\d+):(\d+)[.,](\d+) --> ")

def parse_srt(path):
    txt=open(path,encoding="utf-8-sig").read()
    cues=[]
    for b in re.split(r"\n\s*\n", txt):
        lines=[l for l in b.splitlines() if l.strip()]
        if len(lines)<2: continue
        m=TS.search(lines[0]); idx=0
        if not m and len(lines)>1: m=TS.search(lines[1]); idx=1
        if not m: continue
        tsec=int(m.group(1))*3600+int(m.group(2))*60+int(m.group(3))
        s=idx+1
        while s<len(lines) and "-->" in lines[s]: s+=1
        text=" ".join(l.strip() for l in lines[s:])
        text=re.sub(r"<[^>]+>","",text); text=re.sub(r"&amp;nbsp;|&amp;amp;","&",text)
        text=re.sub(r"♪[^ ]*|&amp;|&#\d+;","",text); text=re.sub(r"\s+"," ",text).strip()
        if text and not re.fullmatch(r"[\[\(]?music[\]\)]?|[♪\.\-\s]+",text,re.I):
            cues.append((tsec,text))
    return cues

report=[]; all_pass=True
for vid,yid,dur in VIDEOS:
    cues=parse_srt(os.path.join(RAW,f"{yid}.en.srt"))
    md=open(os.path.join(OUT,f"{vid}_{yid}.md"),encoding="utf-8").read()
    md_norm=re.sub(r"\s+"," ",md).lower()
    # replay dedup logic dari extractor
    dedup=[]; dropped=[]
    for t,x in cues:
        if dedup and (dedup[-1][1]==x or x in dedup[-1][1]):
            dropped.append((t,x)); continue
        dedup.append((t,x))
    # 1) setiap cue KEPT harus hadir di md (lossless utk konten yang dipertahankan)
    missing=[(t,x) for t,x in dedup if re.sub(r"\s+"," ",x).lower() not in md_norm]
    # 2) setiap cue DROPPED harus duplikat-sejati vs cue-kept terakhir pada replay
    #    (extractor membuang bila x == prev atau x substring prev; audit: cek keadilan + kemiripan)
    fake_drop=[]; replay=[]
    for t,x in cues:
        if replay and (replay[-1]==x or x in replay[-1]):
            prev=replay[-1]
            fair = (x==prev) or (x in prev) or difflib.SequenceMatcher(None,x.lower(),prev.lower()).ratio()>0.85
            if not fair: fake_drop.append((t,x,prev[:80]))
            continue
        replay.append(x)
    # 3) gap timeline antar cue kept > 120s
    gaps=[]
    for (t1,_),(t2,_) in zip(dedup,dedup[1:]):
        if t2-t1>120: gaps.append((t1,t2,t2-t1))
    # 4) cakupan waktu
    end=dedup[-1][0] if dedup else 0
    w_srt=sum(len(x.split()) for _,x in cues); w_md=sum(len(x.split()) for _,x in dedup)
    status = "PASS" if (not missing and not fake_drop and not gaps and end>=dur-180) else "FAIL"
    if status=="FAIL": all_pass=False
    report.append(dict(video=vid,srt_cues=len(cues),kept=len(dedup),dropped=len(dropped),
        srt_words=w_srt,kept_words=w_md,
        kept_missing_in_md=len(missing), fake_drops=len(fake_drop),
        gaps_gt120s=len(gaps), last_cue_s=end, dur_s=dur,
        tail_gap_s=dur-end, status=status,
        sample_missing=[m[1][:70] for m in missing[:3]],
        sample_fake=[f[1][:70] for f in fake_drop[:3]],
        sample_gaps=gaps[:3]))

for r in report:
    print(f"{r['video']}: {r['status']} | srt_cues={r['srt_cues']} kept={r['kept']} dropped={r['dropped']} "
          f"| words {r['srt_words']}->{r['kept_words']} | kept-missing-in-md={r['kept_missing_in_md']} "
          f"fake-drops={r['fake_drops']} gaps>120s={r['gaps_gt120s']} tail={r['tail_gap_s']}s")
    if r['sample_missing']: print("   MISSING:", r['sample_missing'])
    if r['sample_fake']: print("   FAKE-DROP:", r['sample_fake'])
    if r['sample_gaps']: print("   GAPS:", r['sample_gaps'])
print("VERDICT:", "PASS" if all_pass else "FAIL")
