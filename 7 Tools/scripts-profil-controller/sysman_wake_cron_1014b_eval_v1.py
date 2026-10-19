#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Sensus read-only ronde wake 14-10 (dua baris fase-stalled).
Kolom diverifikasi dulu lewat PRAGMA sebelum query dipakai."""
import os
import sqlite3
import sys
import time

DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")


def connect_ro(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con


def cols(con, table):
    return [r[1] for r in con.execute("PRAGMA table_info(%s)" % table)]


def main():
    now = int(time.time())
    con = connect_ro(DB)
    try:
        print("== PRAGMA ==")
        for t in ("tasks", "task_comments", "task_events", "task_runs", "task_links"):
            print(t, cols(con, t))

        print("\n== SANITY: umur event terakhir papan (menit) ==")
        r = con.execute("SELECT MAX(created_at) AS m, COUNT(*) AS n FROM task_events").fetchone()
        print("last_event_age_min=%d total_events=%d" % ((now - r["m"]) // 60, r["n"]))
        r = con.execute("SELECT COUNT(*) AS n FROM tasks").fetchone()
        print("tasks=%d" % r["n"])
        r = con.execute("SELECT COUNT(*) AS n FROM task_comments").fetchone()
        print("comments=%d" % r["n"])

        print("\n== SENSUS STATUS (kartu terbuka) ==")
        for row in con.execute("SELECT status, COUNT(*) AS n FROM tasks GROUP BY status ORDER BY n DESC"):
            print("%s=%d" % (row["status"], row["n"]))

        print("\n== BLIND SPOT: kartu running dengan LAPOR tanpa ACK author-lain ==")
        run_rows = con.execute("SELECT id, title, tenant, assignee, started_at FROM tasks WHERE status='running'").fetchall()
        print("running_total=%d" % len(run_rows))
        for row in run_rows:
            lap = con.execute(
                "SELECT author, MAX(created_at) AS ts, COUNT(*) AS n FROM task_comments "
                "WHERE task_id=? AND (body LIKE '%LAPOR-SELESAI%' OR body LIKE '%LAPOR-SELESEI%')",
                (row["id"],)).fetchone()
            if not lap["n"]:
                continue
            acks = con.execute(
                "SELECT author FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                (row["id"],)).fetchall()
            other_ack = [a["author"] for a in acks if (a["author"] or "") != (lap["author"] or "~")]
            hb = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=? AND kind='heartbeat'",
                             (row["id"],)).fetchone()["m"]
            print("RUNNING %s | tenant=%s | assignee=%s | lap_author=%s lap_age_min=%d | ack_lain=%s | hb_age_min=%s | %s" % (
                row["id"], row["tenant"], row["assignee"], lap["author"],
                (now - lap["ts"]) // 60, other_ack or "-",
                str((now - hb) // 60) if hb else "NO-HB",
                (row["title"] or "")[:60]))

        print("\n== TENANT GSF-1012 (kartu jangkar ber-tenant NULL dihitung terpisah) ==")
        tot = con.execute("SELECT COUNT(*) AS n FROM tasks WHERE tenant='GSF-1012'").fetchone()["n"]
        print("tenant_GSF-1012_cards=%d" % tot)
        for row in con.execute("SELECT id, status, title, created_at FROM tasks WHERE tenant='GSF-1012' ORDER BY created_at"):
            ackn = con.execute(
                "SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                (row["id"],)).fetchone()["n"]
            print("%s | %s | ack=%d | age_h=%d | %s" % (
                row["id"], row["status"], ackn, (now - row["created_at"]) // 3600, (row["title"] or "")[:70]))

        print("\n== TENANT SYNCNAS-1013M + induk 1013 ==")
        for row in con.execute("SELECT id, status, tenant, title, created_at FROM tasks WHERE tenant LIKE 'SYNCNAS%' ORDER BY created_at"):
            ackn = con.execute(
                "SELECT COUNT(*) AS n FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%'",
                (row["id"],)).fetchone()["n"]
            print("%s | %s | tenant=%s | ack=%d | %s" % (
                row["id"], row["status"], row["tenant"], ackn, (row["title"] or "")[:70]))

        print("\n== DETAIL DUA KARTU WAKE: komentar pasca-promoted terakhir ==")
        for tid in ("t_6359bba5", "t_bb725705"):
            ts = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=? AND kind='promoted'",
                             (tid,)).fetchone()["m"]
            print("--- %s promoted_age_min=%d" % (tid, (now - ts) // 60))
            for c in con.execute("SELECT author, created_at, substr(body,1,90) AS b FROM task_comments WHERE task_id=? ORDER BY created_at", (tid,)):
                print("   [%s] age_h=%d fase=%s :: %s" % (
                    c["author"], (now - c["created_at"]) // 3600,
                    "[FASE]" in c["b"], c["b"].replace("\n", " ")))
            ev = con.execute("SELECT MAX(created_at) AS m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
            print("   last_event_age_h=%.1f" % ((now - ev) / 3600.0))

        print("\n== RE-SCAN KANONIS (scan() modul pemindai) ==")
        sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
        import importlib.util
        spec = importlib.util.spec_from_file_location(
            "wake_scan", os.path.join(os.path.dirname(os.path.abspath(__file__)), "gsp_mission_wake_scan.py"))
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        findings = mod.scan(DB, now, mod.DEFAULT_AUTHORS.split(","))
        print("findings=%d" % len(findings))
        for f in findings:
            print("WAKE %s %s %d" % f)
    finally:
        con.close()


if __name__ == "__main__":
    main()
