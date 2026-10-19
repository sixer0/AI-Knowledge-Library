#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optwf_measure.py - harness ukur kriteria sukses (SC) misi OPT-WF-0907, sekali-jalan.

Kartu sumber: t_f4087c0c (OPT-WF-C4). Rumus beku dari blueprint 02_structured.md
seksi O-F + 01_request.md seksi 6 (SC-1..SC-6, SC-G). Sumber ad-hoc fase A:
telem1.py..telem7.py (disalin permanen di docs/2026-09-07-opt-orchestration-throughput/harness-src/).

Pemakaian:
  python optwf_measure.py --days 14 [--since ISO] [--until ISO] [--tag NAME]
                          [--kanban-db PATH] [--outdir PATH] [--no-postgres]

Jendela: [since, until]. Bila --since tidak diberi: since = until - days*86400.
Bila --until tidak diberi: until = waktu jalan (parameter jendela, satu-satunya
kebergantungan jam dinding). Semua query memakai epoch integer jendela; tidak ada
now()/CURRENT_DATE di dalam query => determinis untuk jendela yang sama.

Dua cakupan dilaporkan untuk metrik kanban.db:
  window  - peristiwa dalam jendela (dipakai utk AFTER.md pasca-perubahan)
  alltime - seluruh riwayat DB (kompatibel BASELINE: skrip telem fase A sebagian
            besar memang tanpa filter waktu; selisih n terhadap BASELINE = DB tumbuh)

Metrik Postgres (AgentRequest: RT/TA, konkurensi) memakai jendela; bila koneksi
gagal, blok ditandai UNAVAILABLE (tanpa angka karangan).

Output: blok teks per SC ke stdout + JSON ke <outdir>/<tanggal-until>_<tag>.json
(tanggal-until = tanggal UTC akhir jendela, bukan jam dinding).
"""

import argparse
import json
import os
import re
import sqlite3
import statistics
import sys
from datetime import datetime, timezone

DEFAULT_KANBAN_DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
DEFAULT_ENV = r"C:/Users/TRIAL/gsp-datacenter/.env"
DEFAULT_OUTDIR = ("C:/Users/TRIAL/workspace/gsp-hermes/workspace/"
                  "docs/2026-09-07-opt-orchestration-throughput/measures")
HEALTH_MAX_S = 21600  # ambang "sehat" <=6h, sama dgn fase A (telem2/telem7)


# ---------------------------------------------------------------- util
def parse_iso(s):
    s = s.strip()
    if s.endswith("Z") or s.endswith("z"):
        s = s[:-1] + "+00:00"
    dt = datetime.fromisoformat(s)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def iso(epoch):
    return datetime.fromtimestamp(epoch, timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def pct(sorted_vals, p):
    """Nearest-rank seperti fase A: indeks int(n*p) (telem5/telem7), clamp ke n-1."""
    n = len(sorted_vals)
    if n == 0:
        return None
    return sorted_vals[min(int(n * p), n - 1)]


def dist(vals, unit=1.0, extra_gt=None):
    vals = sorted(vals)
    n = len(vals)
    if n == 0:
        return {"n": 0}
    out = {
        "n": n,
        "median": round(statistics.median(vals) / unit, 1),
        "p75": round(pct(vals, 0.75) / unit, 1),
        "p90": round(pct(vals, 0.90) / unit, 1),
        "p95": round(pct(vals, 0.95) / unit, 1),
        "p99": round(pct(vals, 0.99) / unit, 1),
        "max": round(vals[-1] / unit, 1),
    }
    if extra_gt is not None:
        out["gt_%s" % extra_gt[0]] = sum(1 for v in vals if v > extra_gt[1])
    return out


# ---------------------------------------------------------------- DB
def connect_sqlite(path):
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    return con


def env_db_url(env_path):
    txt = open(env_path, encoding="utf-8", errors="ignore").read()
    m = re.search(r'DATABASE_URL="([^"]+)"', txt) or re.search(r"DATABASE_URL=(\S+)", txt)
    if not m:
        raise RuntimeError("DATABASE_URL tidak ditemukan di %s" % env_path)
    return m.group(1)


def connect_pg(env_path):
    import psycopg2  # impor lokal: harness tetap jalan tanpa psycopg2
    return psycopg2.connect(env_db_url(env_path))


# ---------------------------------------------------------------- helpers sqlite
def ev_minmax(con, kind, mode="min"):
    """dict task_id -> min/max created_at event `kind`."""
    fn = "min" if mode == "min" else "max"
    cur = con.execute(
        "SELECT task_id, %s(created_at) t FROM task_events WHERE kind=? GROUP BY 1" % fn,
        (kind,))
    return {r["task_id"]: r["t"] for r in cur.fetchall()}


def links(con):
    return [(r["parent_id"], r["child_id"])
            for r in con.execute("SELECT parent_id, child_id FROM task_links")]


def quantile_report(pairs, lo=None, hi=None):
    """pairs: list (value_seconds). lo/hi: filter inklusif pada value (detik)."""
    vals = [v for v in pairs if v is not None and (lo is None or v >= lo) and (hi is None or v <= hi)]
    return dist(vals, unit=60.0)  # menit


def gate_stats(producers, links_, lo=None, hi=None):
    """idle chain & turunan gate: delta = producer(anak) - producer(induk), non-negatif."""
    spans = []
    for pid, cid in links_:
        pv, cv = producers.get(pid), producers.get(cid)
        if pv is None or cv is None:
            continue
        d = cv - pv
        if d < 0:
            continue
        if lo is not None and not (lo <= cv <= hi):
            continue
        spans.append(float(d))
    return spans


# ---------------------------------------------------------------- SC blocks
def sc1(con, W):
    s, u = W["since"], W["until"]
    claims_all = ev_minmax(con, "claimed", "min")
    lk = links(con)
    return {
        "formula": "claimed anak - claimed induk (menit, nearest-rank int(n*p)), non-negatif",
        "window": quantile_report(gate_stats(claims_all, lk, s, u)),
        "alltime": quantile_report(gate_stats(claims_all, lk)),
    }


def gates_s1(con, W):
    """BASELINE seksi 1: latensi gerbang ambil-tugas."""
    s, u = W["since"], W["until"]
    created_ev = ev_minmax(con, "created", "min")
    promoted = ev_minmax(con, "promoted", "min")
    claimed = ev_minmax(con, "claimed", "min")
    spawned = ev_minmax(con, "spawned", "min")
    completed = ev_minmax(con, "completed", "max")
    lk = links(con)
    parents_of = {}
    for pid, cid in lk:
        parents_of.setdefault(cid, []).append(pid)

    # parent done -> child promoted (anchor = waktu promoted)
    pd2pr = []
    for cid, pids in parents_of.items():
        pd = max((completed[p] for p in pids if p in completed), default=None)
        if pd is None or cid not in promoted:
            continue
        d = promoted[cid] - pd
        if d >= 0:
            pd2pr.append((float(d), promoted[cid]))
    # promoted -> claimed (anchor = claimed)
    pr2cl = [(claimed[t] - promoted[t], claimed[t]) for t in promoted
             if t in claimed and claimed[t] >= promoted[t]]
    # claimed -> spawned
    cl2sp = [(spawned[t] - claimed[t], spawned[t]) for t in claimed
             if t in spawned and spawned[t] >= claimed[t]]
    # kartu tanpa parent: created -> claimed (anchor = claimed)
    tasks_created = {r["id"]: r["created_at"] for r in con.execute(
        "SELECT id, created_at FROM tasks")}
    noparent = []
    for t, c in claimed.items():
        if t in parents_of:
            continue
        ct = tasks_created.get(t, created_ev.get(t))
        if ct is not None and c >= ct:
            noparent.append((float(c - ct), c))

    def a_in(a):
        return W["since"] <= a <= W["until"]

    gt10 = sum(1 for v, a in pr2cl if v > 600 and a_in(a))
    gt10_all = sum(1 for v, a in pr2cl if v > 600)
    cl2sp_vals_w = [v for v, a in cl2sp if a_in(a)]
    return {
        "parent_done__child_promoted_menit": {
            "window": dist(sorted(v for v, a in pd2pr if a_in(a))),
            "alltime": dist(sorted(v for v, a in pd2pr)),
        },
        "promoted__claimed_detik": {
            "window": _secs(sorted(v for v, a in pr2cl if a_in(a))),
            "alltime": _secs(sorted(v for v, a in pr2cl)),
        },
        "claimed__spawned_detik": {
            "window": _secs(sorted(cl2sp_vals_w)),
            "alltime": _secs(sorted(v for v, a in cl2sp)),
            "mean_window": round(statistics.mean(cl2sp_vals_w), 1) if cl2sp_vals_w else None,
            "mean_alltime": round(statistics.mean([v for v, a in cl2sp]), 1) if cl2sp else None,
        },
        "noparent_created__claimed_detik": {
            "window": _secs(sorted(v for v, a in noparent if a_in(a))),
            "alltime": _secs(sorted(v for v, a in noparent)),
        },
        "promoted__claimed_gt10menit_jumlah": {"window": gt10, "alltime": gt10_all},
    }


def _secs(sorted_s):
    n = len(sorted_s)
    if n == 0:
        return {"n": 0}
    return {"n": n,
            "median": round(statistics.median(sorted_s)),
            "p90": round(pct(sorted_s, 0.90)),
            "p95": round(pct(sorted_s, 0.95))}


def sc2(con, W):
    s, u = W["since"], W["until"]
    created_ev = ev_minmax(con, "created", "min")
    claimed = ev_minmax(con, "claimed", "min")
    completed = ev_minmax(con, "completed", "max")
    lk = links(con)
    parents_of = {}
    for pid, cid in lk:
        parents_of.setdefault(cid, []).append(pid)

    def classify(anchor_on_child_created=True):
        pre, react, pre_claim = [], [], []
        for cid, pids in parents_of.items():
            pd = max((completed[p] for p in pids if p in completed), default=None)
            ct = created_ev.get(cid)
            if pd is None or ct is None:
                continue
            d = ct - pd
            if d < 0:
                pre.append((cid, ct))
                if cid in claimed and claimed[cid] >= pd:
                    pre_claim.append(float(claimed[cid] - pd))
            else:
                react.append((cid, ct, float(d)))
        return pre, react, pre_claim

    out = {}
    for scope, (lo, hi) in (("window", (s, u)), ("alltime", (None, None))):
        pre, react, pre_claim = classify()
        if lo is not None:
            pre = [x for x in pre if lo <= x[1] <= hi]
            react = [x for x in react if lo <= x[1] <= hi]
        n = len(pre) + len(react)
        out[scope] = {
            "n_parent_done": n,
            "prebuilt_n": len(pre),
            "prebuilt_pct": round(100.0 * len(pre) / n) if n else None,
            "reaktif_n": len(react),
            "reaktif_pct": round(100.0 * len(react) / n) if n else None,
            "delay_reaktif_menit": dist(sorted(x[2] for x in react), unit=60.0),
            "prebuilt_parentdone__klaim_menit": dist(sorted(pre_claim), unit=60.0),
        }
    out["formula"] = ("prebuilt = child.created_at < parent.completed_at (event); "
                      "delay reaktif = child.created - parent.completed (menit)")
    return out


def sc3(con, W):
    """SC-3 = menit run worker selesai / menit rentang chain, per cakupan.
    Chain = komponen terhubung graph task_links (>=2 kartu). Rentang chain =
    max(ended)-min(started) atas run; busy = durasi run outcome completed sehat."""
    s, u = W["since"], W["until"]
    parent = {}

    def find(x):
        while parent.setdefault(x, x) != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a, b):
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb

    rows = list(con.execute("SELECT task_id, started_at, ended_at, outcome FROM task_runs "
                            "WHERE started_at IS NOT NULL"))
    for pid, cid in links(con):
        union(pid, cid)
    comp = {}
    for r in rows:
        if r["started_at"] is None:
            continue
        root = find(r["task_id"])
        c = comp.setdefault(root, {"tasks": set(), "lo": None, "hi": None,
                                   "runs": []})
        c["tasks"].add(r["task_id"])
        end = r["ended_at"] if r["ended_at"] is not None else r["started_at"]
        if c["lo"] is None or r["started_at"] < c["lo"]:
            c["lo"] = r["started_at"]
        if c["hi"] is None or end > c["hi"]:
            c["hi"] = end
        if (r["outcome"] == "completed" and r["ended_at"] is not None
                and 0 < r["ended_at"] - r["started_at"] < HEALTH_MAX_S):
            c["runs"].append((r["started_at"], r["ended_at"]))
    # komponen multi-kartu saja (chain sejati)
    chains = [c for c in comp.values() if len(c["tasks"]) >= 2]

    def agg(clamp_window):
        busy = 0.0
        span = 0.0
        nch = 0
        for c in chains:
            lo, hi = c["lo"], c["hi"]
            if clamp_window:
                lo = max(lo, s)
                hi = min(hi, u)
            if hi <= lo:
                continue
            nch += 1
            span += (hi - lo)
            for (rs, re_) in c["runs"]:
                if clamp_window:
                    rs, re_ = max(rs, s), min(re_, u)
                if re_ > rs:
                    busy += (re_ - rs)
        return {"n_chain": nch,
                "busy_menit": round(busy / 60.0, 1),
                "span_menit": round(span / 60.0, 1),
                "rasio_pct": round(100.0 * busy / span, 1) if span else None}

    # cakupan window: rentang chain dan run di-clamp ke jendela
    win = agg(True)
    alltime = agg(False)
    cal = (u - s) / 86400.0
    busy_w = con.execute(
        "SELECT COALESCE(SUM(ended_at-started_at),0) FROM task_runs WHERE outcome='completed' "
        "AND started_at BETWEEN ? AND ? AND ended_at BETWEEN ? AND ? "
        "AND ended_at-started_at > 0 AND ended_at-started_at < ?",
        (s, u, s, u, HEALTH_MAX_S)).fetchone()[0]
    return {
        "formula": "menit run worker selesai (completed, sehat <6h) / menit rentang chain "
                   "(komponen task_links >=2 kartu); varian kalender = busy/jam jendela",
        "window": win, "alltime": alltime,
        "varian_kalender_window": {
            "busy_menit": round(busy_w / 60.0, 1),
            "jam_jendela": round(cal * 24, 1),
            "rasio_pct": round(100.0 * busy_w / ((u - s)), 2) if u > s else None,
        },
    }


def sc5(con, W):
    s, u = W["since"], W["until"]
    days = max((u - s) / 86400.0, 1e-9)
    n_w = con.execute("SELECT count(*) FROM tasks WHERE completed_at BETWEEN ? AND ?",
                      (s, u)).fetchone()[0]
    n_a, first = con.execute(
        "SELECT count(*), min(completed_at) FROM tasks WHERE completed_at IS NOT NULL AND completed_at <= ?",
        (u,)).fetchone()
    days_a = max((u - first) / 86400.0, 1e-9) if first else days
    return {
        "formula": "kartu completed_at dalam cakupan / hari cakupan",
        "window": {"hari": round(days, 2), "selesai": n_w, "per_hari": round(n_w / days, 2)},
        "alltime": {"hari": round(days_a, 2), "selesai": n_a, "per_hari": round(n_a / days_a, 2)},
    }


def sc6(con, W):
    s, u = W["since"], W["until"]
    q = ("SELECT ended_at-started_at d FROM task_runs WHERE outcome='timed_out' "
         "AND ended_at IS NOT NULL AND started_at IS NOT NULL")
    vals_w = [r["d"] for r in con.execute(q + " AND ended_at BETWEEN ? AND ?", (s, u))]
    vals_a = [r["d"] for r in con.execute(q)]
    def blk(vals):
        vals = sorted(v for v in vals if v is not None and v > 0)
        return {"n": len(vals),
                "semua_ge_1600dtk": (len(vals) > 0 and all(v >= 1600 for v in vals)),
                "median_detik": round(statistics.median(vals)) if vals else None,
                "p90_detik": round(pct(vals, 0.90)) if vals else None}
    return {"formula": "count outcome=timed_out per cakupan (basis ended_at)",
            "window": blk(vals_w), "alltime": blk(vals_a)}


def sc_g(con, W):
    s, u = W["since"], W["until"]
    def counts(where_s, params):
        row = con.execute(
            "SELECT"
            " SUM(CASE WHEN outcome='changes_requested' THEN 1 ELSE 0 END) crq,"
            " SUM(CASE WHEN outcome='crashed' THEN 1 ELSE 0 END) crash,"
            " SUM(CASE WHEN outcome='timed_out' THEN 1 ELSE 0 END) tmo,"
            " SUM(CASE WHEN outcome='blocked' THEN 1 ELSE 0 END) blk,"
            " SUM(CASE WHEN outcome='gave_up' THEN 1 ELSE 0 END) gu,"
            " SUM(CASE WHEN error LIKE '%Iteration budget exhausted%' THEN 1 ELSE 0 END) itex,"
            " COUNT(*) tot"
            " FROM task_runs WHERE 1=1 " + where_s, params).fetchone()
        return {"verifier_FAIL_changes_requested": row["crq"] or 0,
                "crashed": row["crash"] or 0, "timed_out": row["tmo"] or 0,
                "blocked": row["blk"] or 0, "gave_up": row["gu"] or 0,
                "iteration_budget_exhausted": row["itex"] or 0,
                "total_run": row["tot"] or 0}
    return {"formula": "hitung outcome task_runs per cakupan (basis ended_at; G-a proxy FAIL "
                       "verifier = outcome changes_requested)",
            "window": counts("AND ended_at BETWEEN ? AND ?", (s, u)),
            "alltime": counts("", ())}


def run_duration(con, W):
    """Distribusi durasi run SEHAT (completed, 0<d<6h). p99 WAJIB ada (prasyarat Q1)."""
    s, u = W["since"], W["until"]
    base = ("SELECT ended_at-started_at d FROM task_runs WHERE outcome='completed' "
            "AND started_at IS NOT NULL AND ended_at IS NOT NULL "
            "AND ended_at-started_at > 0 AND ended_at-started_at < %d" % HEALTH_MAX_S)
    vals_w = [r["d"] / 60.0 for r in con.execute(base + " AND ended_at BETWEEN ? AND ?", (s, u))]
    vals_a = [r["d"] / 60.0 for r in con.execute(base)]
    def blk(vals):
        out = dist(sorted(vals), unit=1.0)
        if out.get("n"):
            out["gt_28menit"] = sum(1 for v in vals if v > 28)
            out["gt_40menit"] = sum(1 for v in vals if v > 40)
        return out
    return {"formula": "durasi run outcome=completed, 0<d<6h (menit, nearest-rank)",
            "window": blk(vals_w), "alltime": blk(vals_a)}


def profile_overlap(con, W):
    """BASELINE seksi 4: pasangan run overlap sesama profil."""
    s, u = W["since"], W["until"]
    q = ("SELECT a.profile prof, COUNT(*) n FROM task_runs a JOIN task_runs b "
         "ON a.profile=b.profile AND a.id<b.id "
         "AND a.started_at < COALESCE(b.ended_at, a.ended_at) "
         "AND b.started_at < COALESCE(a.ended_at, b.ended_at) "
         "WHERE a.started_at IS NOT NULL AND b.started_at IS NOT NULL")
    def top(where, params):
        rows = con.execute(q + where + " GROUP BY 1 ORDER BY 2 DESC LIMIT 8", params).fetchall()
        return {r["prof"]: r["n"] for r in rows}
    return {"formula": "pasangan run overlap (interval beririsan) sesama profil, top 8",
            "window": top(" AND a.started_at BETWEEN ? AND ?", (s, u)),
            "alltime": top("", ())}


# ---------------------------------------------------------------- BATCH
# OPT-WF-E13 (t_6b7bb2a7): metrik fraksi multi-call utk mengukur efek putusan
# D-08 (batching) dan D-09 (max_turns 200). Blok baru; blok lama tidak dirombak.
DEFAULT_PROFILES_GLOB = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/*/state.db"


def _batch_scope(con, s=None, u=None, kanban_only=False):
    """Hitung giliran assistant multi-call dalam satu cakupan.

    Giliran = baris messages(role='assistant', tool_calls NOT NULL). Jumlah call
    per giliran = json_array_length(tool_calls). s/u: filter timestamp inklusif
    (None = tanpa filter waktu). kanban_only: pilah via sessions.source='kanban'.
    """
    join = (" JOIN sessions se ON se.id = m.session_id AND se.source='kanban'"
            if kanban_only else "")
    where = ("m.role='assistant' AND m.tool_calls IS NOT NULL"
             " AND json_valid(m.tool_calls)")
    params = ()
    if s is not None:
        where += " AND m.timestamp BETWEEN ? AND ?"
        params = (s, u)
    q = ("SELECT COUNT(k), COALESCE(SUM(k>=2),0),"
         " AVG(CASE WHEN k>=2 THEN k END), MAX(k) FROM ("
         " SELECT json_array_length(m.tool_calls) k FROM messages m" + join +
         " WHERE " + where + ")")
    turns, multi, avg_multi, mx = con.execute(q, params).fetchone()
    return {"giliran": turns or 0,
            "multi_ge2": multi or 0,
            "fraksi_pct": round(100.0 * (multi or 0) / turns, 1) if turns else None,
            "rata_call_per_giliran_multi": round(avg_multi, 2) if avg_multi is not None else None,
            "maks_call_per_giliran": mx}


def _batch_durasi_kanban(con, s=None, u=None):
    """Durasi sesi source='kanban' yang berakhir (menit). Proxy run worker."""
    where = ("source='kanban' AND ended_at IS NOT NULL AND started_at IS NOT NULL"
             " AND ended_at > started_at")
    params = ()
    if s is not None:
        where += " AND started_at BETWEEN ? AND ?"
        params = (s, u)
    vals = [r[0] / 60.0 for r in con.execute(
        "SELECT ended_at-started_at FROM sessions WHERE " + where, params)]
    return dist(sorted(vals), unit=1.0)


def batch_stats(glob_pat, W, min_n):
    """BATCH: fraksi multi-call per profil pekerja dari state.db (HANYA-BACA)."""
    import glob as _glob
    s, u = W["since"], W["until"]
    per, errors = [], []
    for db in sorted(_glob.glob(glob_pat)):
        prof = os.path.basename(os.path.dirname(db)).lower()
        try:
            con = sqlite3.connect("file:" + db.replace("\\", "/") + "?mode=ro",
                                  uri=True)
        except Exception as e:
            errors.append({"profil": prof,
                           "error": "%s: %s" % (type(e).__name__, e)})
            continue
        try:
            rec = {"profil": prof, "db": db}
            for scope in ("window", "alltime"):
                ss, uu = (s, u) if scope == "window" else (None, None)
                rec[scope] = {
                    "semua": _batch_scope(con, ss, uu, kanban_only=False),
                    "kanban": _batch_scope(con, ss, uu, kanban_only=True),
                    "durasi_run_kanban_menit": _batch_durasi_kanban(con, ss, uu),
                }
            rec["below_min_n"] = rec["window"]["semua"]["giliran"] < min_n
            per.append(rec)
        except Exception as e:
            errors.append({"profil": prof,
                           "error": "%s: %s" % (type(e).__name__, e)})
        finally:
            con.close()

    lapor = [r for r in per if not r["below_min_n"]]

    def agregat(scope, sub):
        tg = sum(r[scope][sub]["giliran"] for r in lapor)
        tm = sum(r[scope][sub]["multi_ge2"] for r in lapor)
        fr = [r[scope][sub]["fraksi_pct"] for r in lapor
              if r[scope][sub]["fraksi_pct"] is not None]
        return {"n_profil": len(lapor), "giliran": tg, "multi_ge2": tm,
                "fraksi_pooled_pct": round(100.0 * tm / tg, 1) if tg else None,
                "median_fraksi_per_profil_pct": round(statistics.median(fr), 1) if fr else None,
                "maks_call_tertinggi": max((r[scope][sub]["maks_call_per_giliran"]
                                            for r in lapor
                                            if r[scope][sub]["maks_call_per_giliran"] is not None),
                                           default=None)}

    return {
        "formula": "giliran=messages role=assistant AND tool_calls NOT NULL; "
                   "n_call=json_array_length; fraksi=multi(>=2)/giliran; "
                   "pilah sumber via sessions.source='kanban' (sub-cakupan kanban)",
        "per_profil": per,
        "min_n": min_n,
        "profil_error": errors,
        "agregat": {("%s.%s" % (sc, sb)): agregat(sc, sb)
                    for sc in ("window", "alltime")
                    for sb in ("semua", "kanban")},
        "catatan_keterbatasan": [
            "state.db menyimpan SEMUA percakapan agen pada profil (kanban, cli, "
            "desktop, webui, cron); pemisahan run kanban hanya via sessions.source "
            "dan hanya semampu skema - fraksi cakupan 'semua' tercemar sesi chat.",
            "timestamp pesan epoch REAL; jendela window memakai m.timestamp "
            "(bukan waktu run kanban.db) - batas jendela bisa meleset untuk run "
            "yang melintasi batas.",
            "giliran tanpa tool_calls (jawaban murni) TIDAK dihitung sebagai "
            "penyebut; fraksi = densitas batching di antara giliran ber-tool.",
            "durasi run = ended_at-started_at sesi source=kanban (proxy; sesi "
            "tanpa ended_at / crash tidak terhitung).",
            "DB dibaca mode=ro saat harness jalan; profil aktif menulis - nilai "
            "adalah snapshot, bukan konsistensi titik-waktu.",
        ],
    }


# ---------------------------------------------------------------- Postgres
def pg_blocks(conpg, W):
    s_dt = datetime.fromtimestamp(W["since"], timezone.utc)
    u_dt = datetime.fromtimestamp(W["until"], timezone.utc)
    out = {}
    cur = conpg.cursor()

    def q(sql, params=None):
        cur.execute(sql, params or ())
        return cur.fetchall()

    # RT/TA rantai identifikasi (median durasi kerja, menit)
    rt = {}
    for prof in ("gsp-request-translator", "gsp-task-architect"):
        rows = q('SELECT percentile_cont(0.5) WITHIN GROUP (ORDER BY extract(epoch FROM ("finishedAt"-"startedAt"))/60.0) med, '
                 'count(*) n FROM "AgentRequest" WHERE profile=%s AND status=%s '
                 'AND "startedAt" IS NOT NULL AND "finishedAt" IS NOT NULL '
                 'AND "startedAt" >= %s AND "startedAt" < %s',
                 (prof, "done", s_dt, u_dt))
        med, n = rows[0]
        rt[prof] = {"n": n, "median_menit": round(float(med), 1) if med is not None else None}
    out["rantai_RT_TA"] = {"formula": "median durasi (finishedAt-startedAt) run done per profil, jendela",
                           **rt}

    # konkurensi sehat per menit
    rows = q('WITH b AS (SELECT date_trunc(\'minute\', m) m, count(*) c FROM ('
             'SELECT generate_series(date_trunc(\'minute\',"startedAt"), '
             'date_trunc(\'minute\', COALESCE("finishedAt","startedAt")), interval \'1 minute\') m '
             'FROM "AgentRequest" WHERE "startedAt" IS NOT NULL AND "startedAt" >= %s AND "startedAt" < %s '
             'AND COALESCE(extract(epoch FROM ("finishedAt"-"startedAt")),0) <= 21600) x GROUP BY 1) '
             'SELECT max(c), avg(c)::numeric(6,2), count(*) FILTER (WHERE c=0), count(*) FROM b',
             (s_dt, u_dt))
    pk, av, idle, tot = rows[0]
    out["konkurensi_AgentRequest"] = {
        "formula": "overlap run sehat (<=6h) per menit, jendela",
        "puncak": pk, "rata": float(av) if av is not None else None,
        "menit_kosong": idle, "total_menit_jendela_run": tot}

    # AgentRequest per status + selesai/hari (konteks seksi 5)
    rows = q('SELECT status, count(*) FROM "AgentRequest" WHERE "createdAt" >= %s AND "createdAt" < %s '
             'GROUP BY 1 ORDER BY 2 DESC', (s_dt, u_dt))
    out["AgentRequest_status"] = {r[0]: r[1] for r in rows}
    return out


# ---------------------------------------------------------------- render
def render_batch_table(B):
    """Tabel ringkas stdout utk blok BATCH."""
    L = []
    L.append("profil                          | giliran_w | multi%_w | rataKali_w | maks_w | durasi_run_menit(median) | min-n")
    for r in B["per_profil"]:
        w = r["window"]["semua"]
        d = r["window"]["durasi_run_kanban_menit"]
        L.append("%-31s | %9s | %7s | %10s | %6s | %22s | %s" % (
            r["profil"], w["giliran"],
            "-" if w["fraksi_pct"] is None else "%.1f" % w["fraksi_pct"],
            "-" if w["rata_call_per_giliran_multi"] is None else "%.2f" % w["rata_call_per_giliran_multi"],
            "-" if w["maks_call_per_giliran"] is None else w["maks_call_per_giliran"],
            "-" if not d.get("n") else "%.1f (n=%d)" % (d["median"], d["n"]),
            "YA" if r["below_min_n"] else ""))
    ag = B["agregat"]
    for key in ("window.semua", "window.kanban", "alltime.semua", "alltime.kanban"):
        a = ag[key]
        L.append("AGREGAT %-13s: n=%s giliran=%s multi=%s pooled=%s%% median_per_profil=%s%% maks=%s" % (
            key, a["n_profil"], a["giliran"], a["multi_ge2"],
            a["fraksi_pooled_pct"], a["median_fraksi_per_profil_pct"], a["maks_call_tertinggi"]))
    if B["profil_error"]:
        L.append("profil_error: %s" % json.dumps(B["profil_error"], ensure_ascii=False))
    return "\n".join(L)


def render_text(R):
    L = []
    def blk(title, d):
        L.append("== %s ==" % title)
        L.append(json.dumps(d, indent=2, ensure_ascii=False, sort_keys=True))
        L.append("")
    W = R["_meta"]
    L.append("optwf_measure | jendela %s .. %s (%s hari) | tag=%s" %
             (W["since_iso"], W["until_iso"], W["days"], W["tag"]))
    L.append("kanban.db=%s | postgres=%s" % (W["kanban_db"], W["postgres"]))
    L.append("")
    blk("SC-1 idle chain antar-tahap (menit)", R["SC1_idle_chain"])
    blk("SC-1b gerbang ambil-tugas (BASELINE seksi 1)", R["SC1b_gerbang"])
    blk("SC-2 prebuilt vs reaktif", R["SC2_prebuilt"])
    blk("SC-3 pemanfaatan waktu sistem", R["SC3_utilisasi"])
    blk("SC-5 throughput kartu selesai/hari", R["SC5_throughput"])
    blk("SC-6 timed_out per cakupan", R["SC6_timed_out"])
    blk("SC-G guard non-regresi (hitung outcome)", R["SCG_guard"])
    blk("DURASI RUN SEHAT (p95+p99 utk keputusan Q1)", R["durasi_run_sehat"])
    blk("S4 pasangan overlap sesama profil", R["profil_overlap"])
    if "batch" in R:
        L.append("== BATCH fraksi multi-call per profil (state.db, hanya-baca) ==")
        L.append(render_batch_table(R["batch"]))
        L.append("")
        L.append("catatan keterbatasan BATCH:")
        for c in R["batch"]["catatan_keterbatasan"]:
            L.append("- %s" % c)
        L.append("")
    if "postgres" in R:
        blk("PG AgentRequest (RT/TA, konkurensi)", R["postgres"])
    elif "postgres_error" in R:
        L.append("== PG AgentRequest == UNAVAILABLE: %s" % R["postgres_error"])
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--since", help="ISO UTC, mis. 2026-08-24T14:00:00Z")
    ap.add_argument("--until", help="ISO UTC, mis. 2026-09-07T14:00:00Z")
    ap.add_argument("--tag", default="run")
    ap.add_argument("--kanban-db", default=DEFAULT_KANBAN_DB)
    ap.add_argument("--env", default=DEFAULT_ENV)
    ap.add_argument("--outdir", default=DEFAULT_OUTDIR)
    ap.add_argument("--no-postgres", action="store_true")
    ap.add_argument("--profiles-glob", default=DEFAULT_PROFILES_GLOB,
                    help="glob state.db profil utk blok BATCH")
    ap.add_argument("--min-n", type=int, default=30,
                    help="giliran minimum dlm jendela agar profil dilaporkan di BATCH")
    ap.add_argument("--no-batch", action="store_true",
                    help="lewati blok BATCH (kompatibel pemakai lama)")
    a = ap.parse_args()

    until = parse_iso(a.until) if a.until else int(datetime.now(timezone.utc).timestamp())
    since = parse_iso(a.since) if a.since else until - a.days * 86400
    if since >= until:
        sys.exit("since harus < until")
    W = {"since": since, "until": until,
         "since_iso": iso(since), "until_iso": iso(until),
         "days": round((until - since) / 86400.0, 2)}

    con = connect_sqlite(a.kanban_db)
    R = {"_meta": {"window": W, "since_iso": W["since_iso"], "until_iso": W["until_iso"],
                   "days": W["days"], "tag": a.tag, "kanban_db": a.kanban_db,
                   "postgres": "skip" if a.no_postgres else "coba"}}
    R["SC1_idle_chain"] = sc1(con, W)
    R["SC1b_gerbang"] = gates_s1(con, W)
    R["SC2_prebuilt"] = sc2(con, W)
    R["SC3_utilisasi"] = sc3(con, W)
    R["SC5_throughput"] = sc5(con, W)
    R["SC6_timed_out"] = sc6(con, W)
    R["SCG_guard"] = sc_g(con, W)
    R["durasi_run_sehat"] = run_duration(con, W)
    R["profil_overlap"] = profile_overlap(con, W)
    if not a.no_batch:
        R["batch"] = batch_stats(a.profiles_glob, W, a.min_n)
        R["_meta"]["batch_profiles_glob"] = a.profiles_glob
        R["_meta"]["batch_min_n"] = a.min_n
    if not a.no_postgres:
        try:
            pg = connect_pg(a.env)
            R["postgres"] = pg_blocks(pg, W)
            pg.close()
        except Exception as e:
            R["postgres_error"] = "%s: %s" % (type(e).__name__, e)
    con.close()

    os.makedirs(a.outdir, exist_ok=True)
    date_tag = iso(until)[:10]
    path = os.path.join(a.outdir, "%s_%s.json" % (date_tag, a.tag))
    with open(path, "w", encoding="utf-8") as f:
        json.dump(R, f, indent=2, ensure_ascii=False, sort_keys=True)

    print(render_text(R))
    print("JSON ditulis: %s" % path)


if __name__ == "__main__":
    main()
