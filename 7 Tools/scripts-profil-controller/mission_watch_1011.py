#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""mission_watch_1011.py - watchdog serah-terima misi KORPUS-LANJUTAN-1011 (no_agent cron).

Pola diam-sehat watchdog: stdout kosong = tidak ada yang menuntut tangan controller (cron
tidak mengirim pesan). stdout non-kosong = daftar temuan, dikirim verbatim ke sesi origin
untuk membangunkan controller. Deterministik, stdlib-only, read-only DB.

Kelas temuan (skop tenant misi ini saja, anti-bising lintas-misi):
  SERAH   kartu done/blocked/review >=4 menit tanpa token RANTAI-ACK di komentar
  PARKED  hasil berawalan PARKED yang belum ACKED
  MATI    run crashed/timed_out/gave_up pada kartu non-terminal <=6 jam
  STALL   kartu running tanpa event >=45 menit (dugaan worker mati senyap)
Penanda anti-ulang: komentar 'WATCH-1011 <epoch>' ditulis oleh controller saat menilai;
temuan yang sudah punya komentar WATCH-1011 lebih baru daripada event terakhir tidak dilaporkan lagi.
"""
import json
import os
import sqlite3
import sys
import time

DB = os.environ.get("MISSION_WATCH_DB") or r"C:\Users\TRIAL\AppData\Local\hermes\kanban.db"
TENANTS = ("KORPUS-LANJUTAN-1011",)
SERAH_MIN = 4
STALL_MIN = 45
RUN_WINDOW_H = 6


def connect_ro(path):
    con = sqlite3.connect("file:" + path.replace("\\", "/") + "?mode=ro", uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con


def main():
    now = int(time.time())
    try:
        con = connect_ro(DB)
    except sqlite3.Error as e:
        print("ERROR: tidak bisa membuka kanban.db: %s" % e)
        return 0
    ph = ",".join("?" * len(TENANTS))
    out = []

    tasks = list(con.execute(
        "SELECT id, status, title, assignee FROM tasks WHERE tenant IN (%s)" % ph, list(TENANTS)))
    for t in tasks:
        tid = t["id"]
        # umur = sejak peristiwa MAKNA (completed/blocked/promoted), BUKAN MAX(event) yang
        # terpolusi heartbeat DAN marker RANTAI-WAKE pihak lain (cacat umur-MAX: penanda
        # wake menggeser baseline hingga ACK lama dianggap belum ada - diperbaiki 12:0x)
        last_ev = con.execute(
            "SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind IN "
            "('completed','blocked','promoted','unblocked')", (tid,)).fetchone()["m"]
        if last_ev is None:
            last_ev = con.execute(
                "SELECT MAX(created_at) m FROM task_events WHERE task_id=? AND kind='claimed'",
                (tid,)).fetchone()["m"]
        base = last_ev or 0
        ack_after = con.execute(
            "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%RANTAI-ACK%' AND created_at>=? LIMIT 1",
            (tid, base)).fetchone()
        watch_after = con.execute(
            "SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%WATCH-1011%' AND created_at>=? LIMIT 1",
            (tid, base)).fetchone()
        if ack_after or watch_after:
            continue  # sudah ternilai
        age_min = int((now - base) // 60) if last_ev else None
        if t["status"] == "running":
            # stall: pakai event apa pun (heartbeat sah di sini) - worker diam >= STALL_MIN
            last_any = con.execute(
                "SELECT COALESCE(MAX(created_at),0) m FROM task_events WHERE task_id=?", (tid,)).fetchone()["m"]
            age_min = int((now - last_any) // 60) if last_any else None
        res = con.execute("SELECT result FROM tasks WHERE id=?", (tid,)).fetchone()["result"] or ""
        if t["status"] == "done" and age_min is not None and age_min >= SERAH_MIN:
            tag = "PARKED" if res.startswith("PARKED") else "SERAH"
            out.append("%s %s %s | %s | umur %dm" % (tag, tid, t["assignee"], (t["title"] or "")[:60], age_min))
        elif t["status"] in ("blocked", "review", "needs-review") and age_min is not None and age_min >= SERAH_MIN:
            out.append("SERAH %s %s | %s | status %s umur %dm" % (tid, t["assignee"], (t["title"] or "")[:60], t["status"], age_min))
        elif t["status"] == "running" and age_min is not None and age_min >= STALL_MIN:
            out.append("STALL %s %s | %s | tanpa event %dm" % (tid, t["assignee"], (t["title"] or "")[:60], age_min))

    for r in con.execute(
            "SELECT ru.task_id id, ru.outcome o, COALESCE(ru.ended_at,ru.started_at) ts, t.status tstatus, t.title title "
            "FROM task_runs ru JOIN tasks t ON t.id=ru.task_id "
            "WHERE t.tenant IN (%s) AND ru.outcome IN ('crashed','timed_out','gave_up')" % ph, list(TENANTS)):
        if r["tstatus"] in ("done", "archived"):
            continue
        age_min = int((now - r["ts"]) // 60)
        if 0 <= age_min <= RUN_WINDOW_H * 60:
            watch = con.execute("SELECT 1 FROM task_comments WHERE task_id=? AND body LIKE '%WATCH-1011%' AND created_at>=? LIMIT 1",
                                (r["id"], r["ts"])).fetchone()
            if not watch:
                out.append("MATI %s run-%s %dm | %s" % (r["id"], r["o"], age_min, (r["title"] or "")[:60]))

    if out:
        print("WATCH-1011 butuh tangan controller (%d butir, %s):" % (len(out), time.strftime("%H:%M")))
        for line in sorted(set(out)):
            print(" -", line)
    return 0


if __name__ == "__main__":
    sys.exit(main())
