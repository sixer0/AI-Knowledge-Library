# -*- coding: utf-8 -*-
"""Penghasil snapshot progres ingestion BUKUV3-ING-1009 (dipakai cron monitor).
Output STABIL: hanya berubah bila state ledger/papan benar-benar berubah."""
import io, os, sys, csv, subprocess, json, hashlib
from collections import Counter

try: sys.stdout.reconfigure(encoding="utf-8")
except Exception: pass

LED = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace\docs\2026-10-09_bukuv3-mapping-korpus\evidence\INGEST-LEDGER.csv"
rows = list(csv.DictReader(io.open(LED, encoding="utf-8"), delimiter=";"))
per = Counter((r["kelas"], r["state"]) for r in rows)
tot = Counter(r["state"] for r in rows)
print("LEDGER BUKUV3-ING-1009 total=%d" % len(rows))
for s in sorted(tot): print("  %-18s %4d" % (s, tot[s]))
for k in sorted({k for k, _ in per}):
    print("  %s: %s" % (k, ", ".join(f"{s}={per[(k,s)]}" for s in sorted({sk for kk, sk in per if kk == k}))))
try:
    out = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                         capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=60).stdout
    cards = [t for t in json.loads(out) if "BUKUV3" in (t.get("title") or "")]
    cs = Counter(t.get("status") for t in cards)
    print("BOARD: " + " ".join(f"{k}={v}" for k, v in sorted(cs.items())))
    for t in cards:
        if t.get("status") == "running":
            print("  RUNNING:", t["id"], (t.get("title") or "")[:60])
except Exception as e:
    print("BOARD: error", e)
