# -*- coding: utf-8 -*-
"""judge.py — delegasi penilaian ke gsp-image-analyst (vision terbukti). Bandingkan referensi vs render 3D multi-sudut.
Pakai: python judge.py <ref_png> <render_png> [konteks_varian]
Output: JSON {score, pass, critique, fix_hint} pada baris terakhir."""
import subprocess, json, re, sys, os
WS = r"C:\Users\TRIAL\workspace\comfyui-check\satellite"

ref, rend = sys.argv[1], sys.argv[2]
ctx = sys.argv[3] if len(sys.argv) > 3 else ""
Q = (
"Kamu adalah juri objektif kualitas aset 3D. Gambar 1 = REFERENSI 2D satelit (acuan bentuk). "
"Gambar 2 = RENDER multi-sudut dari MESH 3D hasil generate. " + ctx + " "
"Nilai kesesuaian mesh terhadap referensi, skala 0-5 per kriteria: "
"dish (parabola cekung utuh), panel (planar tipis, jumlah benar, biru), boom (lengan penghubung ramping), "
"body (sferoid/blok koheren, bukan blob), detail (horn/strut/modul), clean (tanpa fragmen menggantung/noise tekstur). "
"WAJIB format jawaban persis:\n"
"KRITERIA: dish=.., panel=.., boom=.., body=.., detail=.., clean=..\n"
"TOTAL: <jumlah>/30\n"
"VERDIK: PASS atau FAIL\n"
"CATATAN: <2-3 kalimat cacat utama>\n"
"FIX: <satu instruksi konkret untuk iterasi berikutnya: seed lain / threshold / resolusi / ganti input, atau NONE>"
)
cmd = ["uv","run","--python","3.11","python",WS+r"\ask_vision.py",ref+";"+rend,Q] if False else None
import os
env=dict(os.environ); env["HERMES_PROFILE"]="gsp-image-analyst"
# rute cepat: kilocode langsung (ask_vision) — image-analyst CLI terlalu lambat utk 2 gambar
r=subprocess.run(["uv","run","--python","3.11","python",os.path.join(WS,"ask_vision.py"),ref+";"+rend,Q],capture_output=True,text=True,timeout=600,cwd=WS)
out=(r.stdout or "")+(r.stderr or "")
m=re.search(r"TOTAL:\s*(\d+)\s*/\s*30",out); total=int(m.group(1)) if m else -1
p=re.search(r"VERDIK:\s*(PASS|FAIL)",out); verd=p.group(1) if p else "UNKNOWN"
f=re.search(r"FIX:\s*(.+)",out); fix=f.group(1).strip() if f else "?"
c=re.search(r"CATATAN:\s*(.+)",out); cat=c.group(1).strip() if c else out[-300:]
k=re.search(r"KRITERIA:\s*(.+)",out); krit=k.group(1).strip() if k else ""
print(json.dumps({"score":total,"pass":verd=="PASS","kriteria":krit,"critique":cat,"fix_hint":fix,"raw_tail":out[-200:]},ensure_ascii=False))
