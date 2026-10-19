#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""optwf_worker_trace.py — OPT-WF-C3: mirror WorkerTrace standalone (tanpa sentuh engine).

Baca event kanban.db (HANYA-BACA, WAL-safe via URI mode=ro) dan cerminkan spawn
worker yang TIDAK punya AgentRequest ber-hermesTaskId sama ke tabel BARU
"WorkerTrace" di Postgres gsp-datacenter (bukan AgentRequest, agar gerbang
review HQ tidak terganggu).

Resolusi akhir-run (dipakai cermin DAN pengukur dispatcher, satu sumber kebenaran):
  1. event terminal (completed/blocked/crashed/timed_out/reclaimed) setelah
     'spawned' pada run_id yang sama -> tutup di sana;
  2. tanpa terminal tapi run itu adalah run aktif kartu (tasks.current_run_id
     == run_id dan status 'running') -> tetap terbuka ('running'); heartbeat
     terakhir dicatat sebagai progress;
  3. tanpa terminal dan bukan run aktif -> tutup di event terakhir run itu
     (heartbeat/archived/dll; worker minimal hidup sampai jejak terakhirnya).

Subperintah:
  backfill [--days 14]   sekali-jalan; jendela awal N hari (default 14)
  once                   satu siklus sinkronisasi (jendela --days ke belakang)
  daemon [--interval 10] polling terus-menerus (default 10 dtk)
  measure [--hours 3]    konkurensi AgentRequest vs AgentRequest+WorkerTrace
                         vs running dispatcher pada jendela sama (lapor %)

Keras: tidak menulis apa pun ke kanban.db maupun berkas engine hermes-agent.
"""
import argparse
import os
import re
import sqlite3
import sys
import time
import urllib.parse
from datetime import datetime, timedelta, timezone

KANBAN_DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
HQ_ENV = r"C:/Users/TRIAL/gsp-datacenter/.env"

SPAWN_KIND = "spawned"
HEARTBEAT_KIND = "heartbeat"
TERMINAL_KINDS = ("completed", "blocked", "crashed", "timed_out", "reclaimed")

# Konvensi HQ: kolom timestamp AgentRequest = naive waktu server DB
# (Asia/Bangkok, UTC+7, tanpa DST — diverifikasi via SHOW timezone, 08-09).
# Semua nilai WorkerTrace ditulis/dibaca dalam bingkai yang sama.
TZ_LOCAL = timezone(timedelta(hours=7))


def now_local():
    return datetime.now(TZ_LOCAL).replace(tzinfo=None)


def dt(epoch):
    """epoch -> naive UTC+7 (bingkai timestamp HQ)."""
    return datetime.fromtimestamp(epoch, TZ_LOCAL).replace(tzinfo=None) \
        if epoch is not None else None


DDL = '''
CREATE TABLE IF NOT EXISTS "WorkerTrace" (
  id         text PRIMARY KEY,
  task_id    text NOT NULL,
  profile    text,
  started_at timestamp without time zone,
  ended_at   timestamp without time zone,
  outcome    text,
  source     text NOT NULL DEFAULT 'mirror'
)
'''
DDL_IDX = 'CREATE INDEX IF NOT EXISTS "WorkerTrace_task_id_idx" ON "WorkerTrace" ("task_id")'


# ---------------------------------------------------------------- pure logic
def group_events(events):
    """(event_id, task_id, run_id, kind, ts) -> {(task_id, run_id): [(kind, ts)...]}."""
    g = {}
    for (_eid, tid, rid, kind, ts) in events:
        g.setdefault((tid, rid or 0), []).append((kind, ts))
    for k in g:
        g[k].sort(key=lambda x: x[1])
    return g


def resolve_run(evs, is_live):
    """evs terurut utk satu (task,run); is_live True bila run ini run aktif kartu.
    Kembalikan (spawn_ts, end_ts|None, outcome) atau None bila tak ada spawn."""
    si = next((i for i, (k, _) in enumerate(evs) if k == SPAWN_KIND), None)
    if si is None:
        return None
    spawn_ts = evs[si][1]
    after = evs[si + 1:]
    term = next(((k, ts) for (k, ts) in after if k in TERMINAL_KINDS), None)
    if term:
        return (spawn_ts, term[1], term[0])
    if is_live:
        return (spawn_ts, None, "running")
    last_ts = max([ts for (_, ts) in after if ts > spawn_ts], default=spawn_ts)
    return (spawn_ts, last_ts, "ended")


def build_run_rows(events, liveness):
    """liveness: dict task_id -> (status, current_run_id).
    Kembalikan list (task_id, run_id, spawn_ts, end_ts|None, outcome)."""
    out = []
    for (tid, rid), evs in sorted(group_events(events).items()):
        st, cur_rid = liveness.get(tid, (None, None))
        is_live = (st == "running" and (cur_rid or 0) == (rid or 0))
        r = resolve_run(evs, is_live)
        if r:
            out.append((tid, rid, r[0], r[1], r[2]))
    return out


def build_mirror_rows(events, assignee, covered, liveness):
    """Baris cermin utk (task_id, run_id) ber-spawn tanpa AgentRequest yang relevan.
    events: (event_id, task_id, run_id, kind, created_at_epoch).
    covered: dict task_id -> {'open': bool, 'last_end': datetime|None} dari
      AgentRequest; sebuah run dikecualikan hanya bila AR-nya masih terbuka ATAU
      spawn-nya <= penutupan AR (+toleransi 5 mnt). Re-dispatch setelah AR tutup
      (mis. kartu yang dijalankan ulang pasca crash/zombie) TETAP dicerminkan —
      kalau tidak, run keduanya tak terukur sama sekali (preseden 08-09).
    liveness: lihat build_run_rows."""
    rows = []
    for (tid, rid, s, e, outcome) in build_run_rows(events, liveness):
        cov = covered.get(tid)
        if cov:
            if cov["open"]:
                continue
            le = cov["last_end"]
            if le is None or dt(s) <= le + timedelta(minutes=5):
                continue  # run ini terwakili oleh AR-nya
        rows.append({
            "id": f"mirror-{tid}-r{rid}",
            "task_id": tid,
            "run_id": rid,
            "profile": assignee.get(tid) or "unknown",
            "started_at": s,
            "ended_at": e,
            "outcome": outcome,
            "source": "mirror",
        })
    return rows


# ------------------------------------------------------------------ readers
def open_kanban_ro():
    con = sqlite3.connect(f"file:{KANBAN_DB.replace(os.sep, '/')}?mode=ro",
                          uri=True, timeout=5)
    con.execute("PRAGMA busy_timeout=3000")
    return con


def fetch_events(con, since_epoch=None):
    """Event spawn+terminal + heartbeat TERAKHIR per run (agregasi, ringan)
    + assignee + liveness (status, current_run_id) per task."""
    kinds = (SPAWN_KIND,) + TERMINAL_KINDS
    ph = ",".join("?" * len(kinds))
    sql = (f"SELECT id, task_id, run_id, kind, created_at FROM task_events "
           f"WHERE kind IN ({ph})")
    args = list(kinds)
    # batas bawah juga menyertakan run yang lahir sebelum jendela namun masih
    # relevan: ambil semua spawn sejak batas; heartbeat diagregasi per run.
    if since_epoch is not None:
        sql += " AND created_at >= ?"
        args.append(since_epoch)
    evs = con.execute(sql, args).fetchall()
    hb_sql = ("SELECT MAX(id), task_id, run_id, 'heartbeat', MAX(created_at) "
              "FROM task_events WHERE kind='heartbeat'")
    hb_args = []
    if since_epoch is not None:
        hb_sql += " AND created_at >= ?"
        hb_args.append(since_epoch)
    hb_sql += " GROUP BY task_id, run_id"
    evs += con.execute(hb_sql, hb_args).fetchall()
    tids = list({e[1] for e in evs})
    assignee, liveness = {}, {}
    for i in range(0, len(tids), 500):
        chunk = tids[i:i + 500]
        ph2 = ",".join("?" * len(chunk))
        for tid, prof, st, crid in con.execute(
                f"SELECT id, assignee, status, current_run_id FROM tasks"
                f" WHERE id IN ({ph2})", chunk):
            assignee[tid] = prof
            liveness[tid] = (st, crid)
    return evs, assignee, liveness


def load_database_url():
    for line in open(HQ_ENV, encoding="utf-8", errors="ignore"):
        if line.startswith("DATABASE_URL="):
            return line.split("=", 1)[1].strip().strip('"')
    raise SystemExit("FATAL: DATABASE_URL tidak ada di " + HQ_ENV)


def pg_connect():
    from pg8000 import dbapi
    u = urllib.parse.urlparse(load_database_url())
    con = dbapi.connect(user=urllib.parse.unquote(u.username),
                        host=u.hostname, port=u.port or 5432,
                        password=urllib.parse.unquote(u.password or ""),
                        database=u.path.lstrip("/"))
    return Pg(con)


class Pg:
    """Selimut DB-API pg8000: execute(sql[, args]) -> rows | rowcount, auto-commit."""
    def __init__(self, con):
        self.con = con
        self.cur = con.cursor()

    def execute(self, sql, args=None):
        if args is None:
            self.cur.execute(sql)
        else:
            self.cur.execute(sql, tuple(args))
        self.con.commit()
        if self.cur.description:
            return list(self.cur.fetchall())
        return self.cur.rowcount

    def close(self):
        try:
            self.con.close()
        except Exception:
            pass


def ensure_schema(pg):
    pg.execute(DDL)
    pg.execute(DDL_IDX)


def covered_task_ids(pg):
    """Peta cakupan AgentRequest per task: open=ada baris belum selesai;
    last_end=penutupan terakhir (naive UTC+7). Baris 'zombie running' TIDAK
    dianggap cakupan — intervalnya palsu (finishedAt = waktu restart bridge),
    jadi run kanban-nya harus tetap dicerminkan (preseden SPK-002)."""
    out = {}
    for tid, fin, status, err in pg.execute(
            'SELECT "hermesTaskId", "finishedAt", status, error FROM "AgentRequest" '
            'WHERE "hermesTaskId" IS NOT NULL'):
        if err and err.startswith("zombie running"):
            continue
        d = out.setdefault(tid, {"open": False, "last_end": None})
        if status in ("queued", "running", "dispatched") or \
                (fin is None and status not in ("done", "failed", "rejected",
                                                "cancelled")):
            d["open"] = True
        if fin is not None and (d["last_end"] is None or fin > d["last_end"]):
            d["last_end"] = fin
    return out


# ------------------------------------------------------------- sync engine
def sync_once(pg, days=14, label="cycle"):
    """Satu siklus penuh: baca kanban.db ro (jendela `days` hari) -> bangun
    baris cermin -> upsert WorkerTrace. Deterministik atas jendela; hasil
    siklus berikutnya selalu konvergen terhadap event terbaru."""
    since = int(time.time()) - days * 86400
    con = open_kanban_ro()
    try:
        evs, assignee, liveness = fetch_events(con, since)
    finally:
        con.close()
    covered = covered_task_ids(pg)
    rows = build_mirror_rows(evs, assignee, covered, liveness)
    n_ins = n_upd = 0
    for r in rows:
        n = pg.execute(
            'INSERT INTO "WorkerTrace" (id, task_id, profile, started_at,'
            ' ended_at, outcome, source)'
            " VALUES (%s, %s, %s, %s, %s, %s, 'mirror')"
            " ON CONFLICT (id) DO UPDATE SET profile=EXCLUDED.profile,"
            " ended_at=EXCLUDED.ended_at, outcome=EXCLUDED.outcome",
            (r["id"], r["task_id"], r["profile"], dt(r["started_at"]),
             dt(r["ended_at"]), r["outcome"]))
        n_upd += 1 if (n and n > 1) else 0
        n_ins += 1 if not n or n <= 1 else 0
    # cermin yang terwakili AR (AR terbuka ATAU spawn <= penutupan AR+5mnt): hapus.
    # Baris 'zombie running' bukan cakupan sah (interval palsu).
    n_del = pg.execute(
        'DELETE FROM "WorkerTrace" w WHERE w.source=\'mirror\' AND EXISTS ('
        ' SELECT 1 FROM "AgentRequest" a WHERE a."hermesTaskId" = w.task_id'
        "  AND (a.error IS NULL OR a.error NOT LIKE 'zombie running%')"
        "  AND (a.status IN ('queued','running','dispatched')"
        "       OR (a.\"finishedAt\" IS NOT NULL"
        "           AND w.started_at <= a.\"finishedAt\" + interval '5 minutes')))") or 0
    print(f"[{label}] events={len(evs)} mirror_rows={len(rows)} "
          f"upserted={n_ins} multirow_updated={n_upd} dedup_deleted={n_del}",
          flush=True)
    return rows


# ----------------------------------------------------------------- measure
def _overlap_minute_counts(intervals, win_start, win_end):
    """Konkurensi per menit (rata, puncak) dari interval naive (start, end)."""
    minutes = {}
    for (s, e) in intervals:
        s = max(s, win_start)
        e = min(e, win_end)
        if e <= s:
            continue
        m = s.replace(second=0, microsecond=0)
        while m < e:
            minutes[m] = minutes.get(m, 0) + 1
            m += timedelta(minutes=1)
    total_min = max(1, int((win_end - win_start).total_seconds() // 60))
    base = win_start.replace(second=0, microsecond=0)
    vals = [minutes.get(base + timedelta(minutes=i), 0)
            for i in range(total_min)]
    return (sum(vals) / total_min, max(vals) if vals else 0)


def measure(hours=3, ago=0, include_zombies=False):
    """Konkurensi rata/puncak per menit pada jendela sama, tiga sumber:
    AgentRequest saja / AgentRequest+WorkerTrace / dispatcher kanban (ground truth).
    Semua interval dalam bingkai naive UTC+7.
    include_zombies=False (bawaan): buang baris AgentRequest ber-error
    'zombie running' — cacat hulu terdokumentasi (finishedAt dipalsukan ke waktu restart bridge oleh
    self-heal bridge.mjs; preseden SPK-002: truth di atas fidelity). Bawaan AKTIF;
    pakai --include-zombies utk melihat angka mentah."""
    pg = pg_connect()
    ensure_schema(pg)
    now = now_local()
    we = now - timedelta(hours=ago)
    ws = we - timedelta(hours=hours)

    zfilter = "" if include_zombies else \
        " AND (error IS NULL OR error NOT LIKE 'zombie running%')"
    ar = pg.execute(
        'SELECT "startedAt", COALESCE("finishedAt", now()::timestamp)'
        ' FROM "AgentRequest" WHERE "startedAt" IS NOT NULL'
        ' AND COALESCE("finishedAt", now()::timestamp) > %s'
        ' AND "startedAt" < %s' + zfilter, (ws, we))
    wt = pg.execute(
        'SELECT started_at, COALESCE(ended_at, now()::timestamp)'
        ' FROM "WorkerTrace" WHERE started_at IS NOT NULL'
        ' AND COALESCE(ended_at, now()::timestamp) > %s'
        ' AND started_at < %s', (ws, we))
    ar_i = [(r[0], r[1]) for r in ar]
    wt_i = [(r[0], r[1]) for r in wt]

    con = open_kanban_ro()
    try:
        evs, _a, liveness = fetch_events(con, int((ws - timedelta(days=2)).timestamp()))
    finally:
        con.close()
    disp = []
    for (tid, rid, s, e, outcome) in build_run_rows(evs, liveness):
        disp.append((dt(s), dt(e) if e is not None else now))

    a_avg, a_pk = _overlap_minute_counts(ar_i, ws, we)
    b_avg, b_pk = _overlap_minute_counts(ar_i + wt_i, ws, we)
    d_avg, d_pk = _overlap_minute_counts(disp, ws, we)
    selisih_a = abs(a_avg - d_avg) / d_avg * 100 if d_avg else float("nan")
    selisih_b = abs(b_avg - d_avg) / d_avg * 100 if d_avg else float("nan")
    print(f"jendela {hours} jam: {ws.isoformat()} .. {we.isoformat()} (UTC+7)")
    print(f"AgentRequest saja       : rata={a_avg:.2f} puncak={a_pk} n={len(ar_i)}")
    print(f"AgentRequest+WorkerTrace: rata={b_avg:.2f} puncak={b_pk} "
          f"n={len(ar_i)}+{len(wt_i)}")
    print(f"dispatcher (kanban)     : rata={d_avg:.2f} puncak={d_pk} n={len(disp)}")
    print(f"selisih sebelum : {selisih_a:.1f}%   sesudah: {selisih_b:.1f}%  "
          f"(target <=20%)")
    return {"window_h": hours, "ar": (a_avg, a_pk), "ar_wt": (b_avg, b_pk),
            "dispatcher": (d_avg, d_pk), "selisih_sebelum_pct": selisih_a,
            "selisih_sesudah_pct": selisih_b}


# ------------------------------------------------------------------- main
def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("cmd", choices=["backfill", "once", "daemon", "measure"])
    ap.add_argument("--days", type=int, default=14)
    ap.add_argument("--hours", type=int, default=3)
    ap.add_argument("--interval", type=int, default=10)
    ap.add_argument("--ago", type=int, default=0,
                    help="measure: geser akhir jendela N jam ke belakang")
    ap.add_argument("--include-zombies", action="store_true",
                    help="measure: sertakan AgentRequest 'zombie running' (cacat hulu)")
    a = ap.parse_args()

    if a.cmd == "measure":
        measure(a.hours, ago=a.ago, include_zombies=a.include_zombies)
        return
    pg = pg_connect()
    ensure_schema(pg)
    if a.cmd == "backfill":
        sync_once(pg, days=a.days, label=f"backfill-{a.days}d")
    elif a.cmd == "once":
        sync_once(pg, days=a.days, label="once")
    elif a.cmd == "daemon":
        print(f"[daemon] pid={os.getpid()} interval={a.interval}s", flush=True)
        while True:
            try:
                sync_once(pg, days=a.days, label="daemon")
            except Exception as e:
                print(f"[daemon] ERROR {type(e).__name__}: {e}", flush=True)
                try:
                    pg.close()
                except Exception:
                    pass
                try:
                    pg = pg_connect()
                    ensure_schema(pg)
                except Exception:
                    pass
            time.sleep(a.interval)


if __name__ == "__main__":
    main()
