# -*- coding: utf-8 -*-
"""Sanity read-only untuk cron mission-wake (sysman).
Bukti papan hidup saat pemindai diam: sensus status, umur event terakhir,
jumlah baris tasks/events/comments. Dibuka mode ro; tidak menulis apa pun.
"""
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"),
                  "hermes", "kanban.db")

def main():
    if not os.path.exists(DB):
        print("FATAL: kanban.db tidak ada di", DB)
        return 2
    uri = "file:" + DB.replace("\\", "/") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")

    tables = [r[0] for r in con.execute(
        "SELECT name FROM sqlite_master WHERE type='table'")]
    print("tables:", ",".join(sorted(tables)))

    for t in ("tasks", "events", "comments"):
        if t in tables:
            n = con.execute(f"SELECT COUNT(*) FROM {t}").fetchone()[0]
            print(f"count.{t} = {n}")

    # Sensus status
    if "tasks" in tables:
        print("-- census status --")
        for r in con.execute(
                "SELECT status, COUNT(*) c FROM tasks GROUP BY status ORDER BY c DESC"):
            print(f"{r['status']} = {r['c']}")

    # Umur event terakhir (kolom waktu paling mungkin created_at/ts)
    now = time.time()
    best = None
    for t in tables:
        cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
        tcols = [c for c in cols if c in ("created_at", "updated_at", "ts",
                                          "timestamp", "heartbeat_at")]
        for c in tcols:
            try:
                v = con.execute(f"SELECT MAX({c}) FROM {t}").fetchone()[0]
            except sqlite3.Error:
                continue
            if v is None:
                continue
            try:
                ts = float(v)
            except (TypeError, ValueError):
                continue
            if ts > 1e12:  # epoch millis
                ts /= 1000.0
            age_min = (now - ts) / 60.0
            if best is None or ts > best[0]:
                best = (ts, f"{t}.{c}", age_min)
    if best:
        print(f"last_event = {best[1]} age_min = {best[2]:.1f}")
    else:
        print("last_event = TIDAK TERUKUR (kolom waktu non-numerik?)")
        for t in tables:
            cols = [r[1] for r in con.execute(f"PRAGMA table_info({t})")]
            print(t, cols)
    con.close()
    return 0

if __name__ == "__main__":
    sys.exit(main())
