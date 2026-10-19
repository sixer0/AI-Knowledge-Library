# -*- coding: utf-8 -*-
"""Bandingkan JSON sapuan controller vs rerun verifier (NAT-S20 validasi ulang)."""
import json
import sys

def load(p):
    return json.load(open(p, encoding="utf-8"))

def agg_by_code(payload):
    tot = {}
    for rec in payload["per_store"]:
        for c, n in rec.get("by_code", {}).items():
            tot[c] = tot.get(c, 0) + n
    return dict(sorted(tot.items(), key=lambda kv: -kv[1]))

def core(payload):
    return {k: payload[k] for k in ("window", "scanner_version", "n_requested",
            "min_chars", "stores_total", "samples_total", "channel_counts",
            "abs_hits", "heavy_samples", "heavy_pct", "verdict")}

def main(a, b):
    pa, pb = load(a), load(b)
    print("== inti A (%s) ==" % a)
    print(json.dumps(core(pa), ensure_ascii=False, sort_keys=True))
    print("== inti B (%s) ==" % b)
    print(json.dumps(core(pb), ensure_ascii=False, sort_keys=True))
    print("== by_code A ==", json.dumps(agg_by_code(pa), ensure_ascii=False))
    print("== by_code B ==", json.dumps(agg_by_code(pb), ensure_ascii=False))
    # selisih per store: scanned, abs, heavy
    sa = {r["store"]: r for r in pa["per_store"]}
    sb = {r["store"]: r for r in pb["per_store"]}
    keys = sorted(set(sa) | set(sb))
    diffs = []
    for k in keys:
        ra, rb = sa.get(k), sb.get(k)
        if ra is None or rb is None:
            diffs.append((k, "store hilang di salah satu", ra is not None, rb is not None))
            continue
        t = lambda r: (r["scanned"], r["abs_violations"], r["heavy_violations"])
        if t(ra) != t(rb):
            diffs.append((k, t(ra), t(rb)))
    print("== selisih per store (A vs B) ==")
    for d in diffs:
        print(d)
    print("total store sama:", len(keys), "| store berbeda:", len(diffs))

if __name__ == "__main__":
    main(sys.argv[1], sys.argv[2])
