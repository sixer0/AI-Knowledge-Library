# -*- coding: utf-8 -*-
"""Analisis gambar via gateway kilocode (qwen3.8-flash) - jalur vision cadangan yang terbukti."""
import sys, json, base64, urllib.request, os
def b64(p):
    return base64.b64encode(open(p,"rb").read()).decode()
imgs = sys.argv[1].split(";")
q = sys.argv[2]
key = os.environ.get("KILOCODE_API_KEY") or [l.split("=",1)[1].strip().strip('"') for l in open(r"C:\Users\TRIAL\AppData\Local\hermes\.env",encoding="utf-8",errors="ignore") if l.startswith("KILOCODE_API_KEY")][0]
content = [{"type":"text","text":q}]
for p in imgs:
    content.append({"type":"image_url","image_url":{"url":"data:image/png;base64,"+b64(p)}})
body = {"model":"qwen/qwen3.8-flash","messages":[{"role":"user","content":content}],"max_tokens":1200,"temperature":0.1}
req = urllib.request.Request("https://api.kilo.ai/api/gateway/chat/completions", data=json.dumps(body).encode(), headers={"Authorization":"Bearer "+key,"Content-Type":"application/json"})
r = json.loads(urllib.request.urlopen(req, timeout=180).read())
print(r["choices"][0]["message"]["content"])
