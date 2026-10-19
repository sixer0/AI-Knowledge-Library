# -*- coding: utf-8 -*-
"""Ronde cron 15-10 sore: kesegaran heartbeat gateway 3 wajib tanpa WMI (read-only)."""
import json, os, time, datetime

BASE = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "profiles")
REG = json.load(open("C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json", encoding="utf-8"))
wajib = REG["gateway_wajib_hidup"]
now = time.time()
print("=== HEARTBEAT CHECK 3 WAJIB (tanpa WMI) ===")
ok = True
for p in wajib:
    hb = os.path.join(BASE, p, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print(f"  {p:20s} TIDAK ADA berkas heartbeat -> curiga")
        ok = False
        continue
    raw = open(hb, encoding="utf-8", errors="replace").read().strip()
    try:
        d = json.loads(raw)
    except Exception:
        d = {"raw": raw[:120]}
    # bentuk bisa berubah; cari updated_at/pid
    upd = d.get("updated_at") or d.get("ts") or d.get("timestamp")
    pid = d.get("pid")
    age = None
    if isinstance(upd, (int, float)):
        age = now - float(upd)
    elif isinstance(upd, str):
        try:
            t = datetime.datetime.fromisoformat(upd.replace("Z", "+00:00"))
            age = now - t.timestamp()
        except Exception:
            pass
    if age is None:
        print(f"  {p:20s} heartbeat terbaca tapi format tak dikenal: keys={list(d)[:6]}")
        ok = False
    else:
        flag = "SEHAT" if age < 180 else "BASI"
        if age >= 180:
            ok = False
        print(f"  {p:20s} pid={pid} umur_hb={age:.0f}s -> {flag}")
print("VERDIK_HB:", "SEHAT" if ok else "ADA-MASALAH")
