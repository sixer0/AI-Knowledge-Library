# -*- coding: utf-8 -*-
# Generator fixture uji sintetis probe (BUKAN data live - fixtures untuk regresi ambang).
# fixture_74x.json  : replika pola fan-out 74x (01-09) -> wajib TEKANAN
# fixture_sehat.json: antrean dangkal + rasio timeout nol -> wajib SEHAT
# fixture_tengah.json: pita tengah rasio -> fail-safe TEKANAN
# CATATAN: stempel waktu fixture relatif terhadap saat generate; jendela probe
# hanya 15 menit, jadi jalankan ulang generator ini sebelum pakai fixture lebih
# dari 15 menit setelah ia ditulis (mis. `python gen_fixtures.py` di folder ini).
import json
from datetime import datetime, timedelta, timezone

now = datetime.now(timezone.utc)
def iso(dt): return dt.strftime("%Y-%m-%dT%H:%M:%S.000Z")

def req(i, status, age_min, err=""):
    c = now - timedelta(minutes=age_min)
    f = c + timedelta(minutes=min(age_min, 5))
    return {"id": "fx-%03d" % i, "status": status, "kind": "oneshot",
            "profile": "gsp-worker-fixture", "title": "fixture %d" % i,
            "createdAt": iso(c), "startedAt": iso(c), "finishedAt": iso(f),
            "updatedAt": iso(f), "error": err}

TO = "hermes CLI timeout after 1800000ms: -p gsp-worker-fixture -z ..."

# 74x: 74 dispatch dalam jendela, queue menumpuk, banyak failed-timeout
fx74 = {"fixture": "fan-out 74x 01-09 (sintetis)", "byStatus":
        {"queued": 58, "approved": 0, "running": 16, "done": 188, "failed": 107},
        "requests": []}
i = 0
for k in range(44):
    i += 1; fx74["requests"].append(req(i, "failed", 3 + (k % 12), TO))
for k in range(20):
    i += 1; fx74["requests"].append(req(i, "done", 2 + (k % 13)))
for k in range(10):
    i += 1; fx74["requests"].append(req(i, "running", 1 + k))

fx_sehat = {"fixture": "gelombang kecil sehat (sintetis)", "byStatus":
            {"queued": 0, "approved": 0, "running": 2, "done": 190, "failed": 33},
            "requests": []}
i = 0
for k in range(8):
    i += 1; fx_sehat["requests"].append(req(i, "done", 1 + k))
i += 1; fx_sehat["requests"].append(req(i, "failed", 6, "provider error 500"))
for k in range(2):
    i += 1; fx_sehat["requests"].append(req(i, "running", 1 + k))

fx_tengah = {"fixture": "pita tengah rasio 0.17 (sintetis)", "byStatus":
             {"queued": 2, "approved": 0, "running": 3, "done": 190, "failed": 36},
             "requests": []}
i = 0
for k in range(5):
    i += 1; fx_tengah["requests"].append(req(i, "done", 2 + k))
for k in range(1):
    i += 1; fx_tengah["requests"].append(req(i, "failed", 4, TO))
for k in range(18):
    i += 1; fx_tengah["requests"].append(req(i, "done", 7 + k))

for name, obj in (("fixture_74x.json", fx74), ("fixture_sehat.json", fx_sehat),
                  ("fixture_tengah.json", fx_tengah)):
    json.dump(obj, open(name, "w", encoding="utf-8"), indent=1)
    print("wrote", name, len(obj["requests"]), "rows")
