#!/usr/bin/env python3.11
# monitor_cycle.py — sweep read-only 7 kelas temuan untuk cron GSP Task Monitoring.
# Output: blok A..E + blok F_* + F_AGGREGATE + TOTAL TEMUAN. Read-only (SQLite mode=ro + GET HQ). Tidak ada mutasi.
# v1.1.0 (TMNUDGE-0909): tambah kelas F1-F5 (kegagalan senyap, ambang TA-D2), resolusi pemilik
# gerbang (roster + task_links + fallback gsp-master), agregasi per pemilik, kap 3/siklus,
# parked-guard, dedup vs notepad ping_sent. Skrip TIDAK membuat kartu (D-11/TA-D7): eksekusi
# P1 adalah tugas agen cron via tool kanban_create, hanya bila notepad ping_mode=live.
# Blok A-E tidak diubah perilakunya dari v1.0.0 (KS-7).
# FIX1 (TMNUDGE-0909 retry-1, verdict+countersign CHECK 21): predikat anti-rekursi
# [PING][tm] dijadikan satu helper _is_ping dipakai F1/F2/F3; F4/F5 menyaring via pola
# LIKE yang diturunkan dari PING_PREFIX; class_f3 kini mengecualikan judul ping dari
# calon wakil rantai (rep) — sebelumnya ping bisa jadi wakil -> ping-atas-ping.
# Pemakaian: /c/Users/TRIAL/.local/bin/python3.11 monitor_cycle.py [--json]
import json
import os
import re
import sqlite3
import subprocess
import sys

KANBAN_DB = "C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
PROFILES_DIR = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
DC_ENV = "C:/Users/TRIAL/gsp-datacenter/.env"
HQ_BASE = "https://localhost:9011/api/brahma/requests"
GATE_HOURS = 2.0

# --- konstanta kelas F (ambang TA-D2; KALIBRASI-DRYRUN, dikunci langkah 9) ---
ROSTER_JSON = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-31-enforcement-fleet/controller-roster.json"
FALLBACK_OWNER = "gsp-master"
JOB_ID = "9d2c115874fa"
HERMES_HOME_ROOT = "C:/Users/TRIAL/AppData/Local/hermes"
F1_STALE_S = 90 * 60            # F1: heartbeat/started_at stale > 90 m
F2_GRACE_S, F2_MARGIN_S = 600, 900  # F2: umur run > max_runtime + grace kernel + margin deteksi
F3_SILENT_S = 2 * 3600          # F3: rantai hening > 2 jam dengan anggota hidup
F4_READY_S = 30 * 60            # F4: ready tanpa klaim > 30 m
F5_GATE_S = 30 * 60             # F5: gerbang gave_up/timed_out tanpa komentar pihak lain > 30 m
PING_CAP = 3                    # kap kartu ping per siklus (KS-4)
PING_PREFIX = "[PING][tm]"      # anti-rekursi: judul berawalan ini tidak pernah masuk sweep F

def _is_ping(title, prefix=PING_PREFIX):
    """Predikat bersama anti-rekursi (TMNUDGE-FIX1, countersign FINDING-2): kartu berjudul
    berawalan [PING][tm] DIKECUALIKAN dari SEMUA sweep kelas F (F1..F5). Satu sumber
    kebenaran — jangan tulis ulang predikat ini per kelas."""
    return (title or "").startswith(prefix)

def con():
    return sqlite3.connect("file:" + KANBAN_DB.replace("\\", "/") + "?mode=ro", uri=True)

def hq_get(pathq):
    try:
        secret = None
        with open(DC_ENV, encoding="utf-8", errors="ignore") as f:
            for line in f:
                if line.startswith("INTERNAL_API_SECRET="):
                    secret = line.split("=", 1)[1].strip().strip('"')
                    break
        if not secret:
            return None, "no INTERNAL_API_SECRET"
        r = subprocess.run(
            ["curl", "-sk", "-H", "x-internal-secret: " + secret, HQ_BASE + pathq],
            capture_output=True, text=True, timeout=30)
        return json.loads(r.stdout), None
    except Exception as e:  # noqa: BLE001
        return None, str(e)

def class_a(c):
    rows = c.execute("""
      SELECT t.id, t.status, t.assignee, t.block_kind, e.ts,
             ROUND((strftime('%s','now') - e.ts)/3600.0, 1)
      FROM tasks t JOIN (
        SELECT task_id, MAX(created_at) ts FROM task_events
        WHERE kind IN ('blocked','review_requested','changes_requested','gave_up','timed_out')
        GROUP BY task_id) e ON e.task_id = t.id
      WHERE t.status IN ('blocked','review') ORDER BY 6 DESC""").fetchall()
    return [dict(id=r[0], status=r[1], assignee=r[2], block_kind=r[3], gate_ts=r[4], age_h=r[5],
                 stale24=bool(r[5] and r[5] > 24)) for r in rows if r[5] is not None and r[5] >= GATE_HOURS]

def card_status(c, cid):
    row = c.execute("SELECT status FROM tasks WHERE id LIKE ?", (cid + "%",)).fetchone()
    return row[0] if row else None

def class_b(c):
    out = []
    aw, err = hq_get("?status=awaiting_approval&light=1&take=100")
    if aw is None:
        return out, "HQ_UNREACHABLE(awaiting): " + str(err)
    for rq in aw.get("requests", []):
        m = re.search(r"(t_[0-9a-f]{8})", rq.get("title", ""))
        if m:
            st = card_status(c, m.group(1))
            if st in ("done", "archived", None):
                out.append(dict(sub="b1", req=rq["id"], card=m.group(1), card_status=st,
                                action="PATCH reject AUTO-SYNC + komentar kartu"))
    dj, err2 = hq_get("?status=rejected&light=1&take=50")
    if dj is None:
        return out, "HQ_UNREACHABLE(rejected): " + str(err2)
    for rq in dj.get("requests", []):
        m = re.search(r"(t_[0-9a-f]{8})", rq.get("title", ""))
        if m:
            st = card_status(c, m.group(1))
            if st in ("blocked", "review"):
                out.append(dict(sub="b2", req=rq["id"], card=m.group(1), card_status=st,
                                action="sinkron balik: baca result entri, komentar keputusan ke kartu"))
    return out, None

def class_c(c):
    try:
        profiles = set(os.listdir(PROFILES_DIR)) | {"default"}
    except OSError as e:
        return [dict(error="profiles dir unreadable: %s" % e)]
    rows = c.execute("""SELECT DISTINCT t.assignee, COUNT(*) FROM tasks t
      WHERE t.status NOT IN ('done','archived') AND t.assignee IS NOT NULL AND t.assignee != ''
      GROUP BY t.assignee""").fetchall()
    return [dict(assignee=a, cards=n) for (a, n) in rows if a not in profiles]

def class_d(c):
    out = []
    fl, err = hq_get("?status=failed&take=50")
    if fl is None:
        return out, "HQ_UNREACHABLE(failed): " + str(err)
    for rq in fl.get("requests", []):
        full, _ = hq_get("/" + rq["id"])
        row = (full or {}).get("request") or {}
        if row.get("result"):
            out.append(dict(req=rq["id"], title=(row.get("title") or "")[:80],
                            action="force-done + komentar (zombie bridge)"))
    return out, None

def class_e(c):
    rows = c.execute("""
      SELECT t.id, t.assignee, ROUND((strftime('%s','now')-t.created_at)/3600.0,1)
      FROM tasks t WHERE t.status='todo' AND t.created_at < strftime('%s','now')-7200
      AND NOT EXISTS (SELECT 1 FROM task_links l JOIN tasks p ON p.id=l.parent_id
        WHERE l.child_id=t.id AND p.status IN ('running','todo','ready','review','blocked'))""").fetchall()
    return [dict(id=r[0], assignee=r[1], age_h=r[2]) for r in rows]

# ================= KELAS F (v1.1.0) — read-only; tidak membuat kartu =================

def _now(c):
    return int(c.execute("SELECT strftime('%s','now')").fetchone()[0])

def load_roster():
    try:
        with open(ROSTER_JSON, encoding="utf-8") as f:
            return set(json.load(f).get("controllers", [])), None
    except Exception as e:  # noqa: BLE001
        return set(), "roster_unreadable: %s" % e

def notepad_get(key):
    """Baca satu key notepad cron job monitor (root HERMES_HOME). None = tidak terbaca/kosong."""
    try:
        env = dict(os.environ, HERMES_HOME=HERMES_HOME_ROOT)
        r = subprocess.run(["hermes", "cron", "notepad", JOB_ID, "get", key],
                           capture_output=True, text=True, timeout=30, env=env)
        out = (r.stdout or "").strip()
        if not out or out.startswith("No notepad key"):
            return None
        return out
    except Exception:  # noqa: BLE001
        return None

def parse_parked(raw):
    try:
        return set(json.loads(raw).keys()) if raw else set()
    except Exception:  # noqa: BLE001
        return set()

def parse_ping_sent(raw):
    try:
        d = json.loads(raw)
        return d if isinstance(d, dict) else {}
    except Exception:  # noqa: BLE001
        return {}

def episode_ts(c, cid):
    """Episode = event insiden TERBARU kartu (gave_up/timed_out/blocked); fallback created_at."""
    row = c.execute("""SELECT MAX(created_at) FROM task_events
        WHERE task_id=? AND kind IN ('gave_up','timed_out','blocked')""", (cid,)).fetchone()
    if row and row[0]:
        return int(row[0])
    row2 = c.execute("SELECT created_at FROM tasks WHERE id=?", (cid,)).fetchone()
    return int(row2[0]) if row2 and row2[0] else 0

def resolve_owner(c, cid, roster):
    """Resolusi deterministik 01 pasal 6: (1) assignee di roster; (2) parent terdekat di
    roster (BFS naik via task_links); (3) fallback gsp-master. created_by='user' tidak pernah
    jadi target. Return (owner, rule_no, note)."""
    seen, queue = set(), [cid]
    first = True
    while queue:
        cur = queue.pop(0)
        if cur in seen:
            continue
        seen.add(cur)
        row = c.execute("SELECT assignee, created_by FROM tasks WHERE id=?", (cur,)).fetchone()
        if row:
            assignee, created_by = row
            if assignee and assignee in roster and first:
                return assignee, 1, None
            if assignee and assignee in roster and not first:
                return assignee, 2, None
        queue.extend(p for (p,) in c.execute(
            "SELECT parent_id FROM task_links WHERE child_id=?", (cur,)).fetchall())
        first = False
    return FALLBACK_OWNER, 3, "fallback gsp-master (E5: tak ada leluhur roster)"

def _runs_col_ok(c):
    cols = [r[1] for r in c.execute("PRAGMA table_info(task_runs)")]
    return "started_at" in cols and "id" in cols

def class_f1(c, parked):
    rows = c.execute("""SELECT id, assignee, title,
        COALESCE(last_heartbeat_at, started_at) ref,
        strftime('%s','now') - COALESCE(last_heartbeat_at, started_at) age_s
        FROM tasks WHERE status='running'
        AND (strftime('%s','now') - COALESCE(last_heartbeat_at, started_at)) > ?
        ORDER BY age_s DESC""", (F1_STALE_S,)).fetchall()
    return [dict(id=r[0], assignee=r[1], title=(r[2] or "")[:70], ref_ts=r[3], age_h=round(r[4] / 3600.0, 2))
            for r in rows if r[0] not in parked and not _is_ping(r[2], PING_PREFIX)]

def class_f2(c, parked):
    out = []
    use_runs = _runs_col_ok(c)
    rows = c.execute("""SELECT id, assignee, title, max_runtime_seconds, current_run_id, started_at
        FROM tasks WHERE status='running' AND max_runtime_seconds IS NOT NULL""").fetchall()
    for r in rows:
        cid, assignee, title, mrs, run_id, t_started = r
        if cid in parked or _is_ping(title, PING_PREFIX):
            continue
        run_started, src = None, None
        if use_runs and run_id:
            rr = c.execute("SELECT started_at FROM task_runs WHERE id=?", (run_id,)).fetchone()
            if rr and rr[0]:
                run_started, src = rr[0], "task_runs.started_at"
        if run_started is None and t_started:
            run_started, src = t_started, "tasks.started_at(fallback)"
        if run_started is None:
            continue
        thresh = mrs + F2_GRACE_S + F2_MARGIN_S
        age = _now(c) - run_started
        if age > thresh:
            out.append(dict(id=cid, assignee=assignee, title=(title or "")[:70], max_runtime=mrs,
                            age_h=round(age / 3600.0, 2), thresh_h=round(thresh / 3600.0, 2), age_src=src))
    n_null = c.execute("SELECT COUNT(*) FROM tasks WHERE status='running' AND max_runtime_seconds IS NULL").fetchone()[0]
    return out, n_null  # E1: NULL max_runtime -> lewati, dicacah

def _chain_groups(c):
    links = c.execute("SELECT parent_id, child_id FROM task_links").fetchall()
    kids, parents = {}, {}
    for p, ch in links:
        kids.setdefault(p, []).append(ch)
        parents.setdefault(ch, []).append(p)
    stat = dict(c.execute("SELECT id, status FROM tasks"))
    lastev = dict(c.execute("SELECT task_id, MAX(created_at) FROM task_events GROUP BY task_id"))
    cre = dict(c.execute("SELECT id, created_at FROM tasks"))

    def closure(seed):
        seen, stack = set(), [seed]
        while stack:
            x = stack.pop()
            if x in seen:
                continue
            seen.add(x)
            stack.extend(kids.get(x, []))
            stack.extend(parents.get(x, []))
        return seen

    groups, assigned = [], set()
    for tid, s in stat.items():
        if s not in ("running", "ready", "todo") or tid in assigned:
            continue
        grp = closure(tid)
        assigned |= grp
        groups.append(grp & set(stat.keys()))
    return groups, stat, lastev, cre

def class_f3(c, parked):
    groups, stat, lastev, cre = _chain_groups(c)
    titles = dict(c.execute("SELECT id, title FROM tasks"))
    now = _now(c)
    out = []
    for grp in groups:
        members = sorted(grp)
        if not any(stat[m] in ("running", "ready", "todo") for m in members):
            continue
        chain_last = max(max(lastev.get(m, 0), cre.get(m, 0)) for m in members)
        silence = now - chain_last
        if silence > F3_SILENT_S:
            live_all = [m for m in members if stat[m] in ("running", "ready", "todo")]
            # FIX1 anti-rekursi: kartu berawalan [PING][tm] dikecualikan dari calon wakil
            # rantai (helper bersama _is_ping); guard parked tetap menguji live_all utuh.
            live = [m for m in live_all if not _is_ping(titles.get(m), PING_PREFIX)]
            if not live:
                continue
            rep = min(live, key=lambda m: cre.get(m, 0))  # kartu hidup tertua = wakil rantai
            if rep in parked or any((m in parked) for m in live_all):
                continue
            out.append(dict(id=rep, members=len(members), live=live[:8],
                            silence_h=round(silence / 3600.0, 2)))
    return out

def class_f4(c, parked):
    rows = c.execute("""SELECT t.id, t.assignee, t.title,
        COALESCE((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id AND e.kind IN ('promoted','claimed')), t.created_at) rts,
        strftime('%s','now') - COALESCE((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id AND e.kind IN ('promoted','claimed')), t.created_at) age_s
        FROM tasks t WHERE t.status='ready'
        AND NOT EXISTS (SELECT 1 FROM task_events e WHERE e.task_id=t.id AND e.kind='claimed')
        AND t.title NOT LIKE ?  -- FIX1: pola diturunkan dari PING_PREFIX; awalan [PING][tm] (predikat bersama _is_ping)
        AND (strftime('%s','now') - COALESCE((SELECT MAX(created_at) FROM task_events e WHERE e.task_id=t.id AND e.kind IN ('promoted','claimed')), t.created_at)) > ?
        ORDER BY age_s DESC""", (PING_PREFIX + "%", F4_READY_S,)).fetchall()
    return [dict(id=r[0], assignee=r[1], title=(r[2] or "")[:70], ready_ts=r[3], age_h=round(r[4] / 3600.0, 2))
            for r in rows if r[0] not in parked]

def class_f5(c, parked):
    rows = c.execute("""SELECT t.id, t.status, t.assignee, ge.ts,
        strftime('%s','now') - ge.ts age_s,
        (SELECT COUNT(*) FROM task_comments tc
          WHERE tc.task_id=t.id AND tc.created_at >= ge.ts
          AND tc.author != 'task-monitor'
          AND NOT (tc.author='default' AND tc.body LIKE '%task-monitor%')) others
        FROM tasks t JOIN (SELECT task_id, MAX(created_at) ts FROM task_events
          WHERE kind IN ('gave_up','timed_out') GROUP BY task_id) ge ON ge.task_id=t.id
        WHERE t.status IN ('blocked','review')
        AND t.title NOT LIKE ?  -- FIX1: pola diturunkan dari PING_PREFIX; awalan [PING][tm] (predikat bersama _is_ping)
        AND (strftime('%s','now') - ge.ts) > ?
        ORDER BY age_s DESC""", (PING_PREFIX + "%", F5_GATE_S,)).fetchall()
    return [dict(id=r[0], status=r[1], assignee=r[2], gate_ts=r[3], age_h=round(r[4] / 3600.0, 2))
            for r in rows if r[0] not in parked and r[5] == 0]

def build_candidates(c, f_lists, roster, parked, ping_sent):
    """Flatten temuan F -> kandidat ping mentah (dedup primer ping_sent per (kartu,episode))."""
    cls_of = {"F1_worker_idle_stale": "F1", "F2_run_over_runtime": "F2",
              "F3_chain_silent": "F3", "F4_ready_unclaimed": "F4", "F5_gate_crash_unanswered": "F5"}
    cands, deduped = [], []
    for key, items in f_lists.items():
        klass = cls_of[key]
        for it in items:
            cid = it["id"]
            ep = episode_ts(c, cid)
            if ("%s|%d" % (cid, ep)) in ping_sent:
                deduped.append(dict(id=cid, klass=klass, episode_ts=ep, why="ping_sent primer"))
                continue
            owner, rule, note = resolve_owner(c, cid, roster)
            cands.append(dict(id=cid, klass=klass, episode_ts=ep, owner=owner, rule=rule,
                              note=note, age_h=it.get("age_h") or it.get("silence_h"), detail=it))
    return cands, deduped

def aggregate(c, cands, ping_sent):
    """Agregasi per pemilik + dedup sekunder (judul identik masih hidup) + kap PING_CAP."""
    by_owner = {}
    for cd in cands:
        by_owner.setdefault(cd["owner"], []).append(cd)
    groups = []
    for owner, lst in by_owner.items():
        lst.sort(key=lambda x: -(x.get("age_h") or 0))
        primary = lst[0]
        title = "%s %s triase kegagalan senyap (kartu %s%s)" % (
            PING_PREFIX, primary["klass"], primary["id"],
            (" +%d" % (len(lst) - 1)) if len(lst) > 1 else "")
        dup_live = c.execute("""SELECT COUNT(*) FROM tasks WHERE title=? AND status NOT IN ('done','archived')""",
                             (title,)).fetchone()[0]
        groups.append(dict(owner=owner, title=title, cards=[x["id"] for x in lst],
                           klasses=sorted({x["klass"] for x in lst}), rule=primary["rule"],
                           oldest_age_h=primary.get("age_h"), dedup_secondary=bool(dup_live)))
    groups.sort(key=lambda g: -(g.get("oldest_age_h") or 0))  # umur tertua dulu
    for i, g in enumerate(groups):
        g["within_cap"] = i < PING_CAP
    return groups

def main():
    c = con()
    res, errs = {}, []
    res["A_gate_over_2h"] = class_a(c)
    res["B_two_channel_gap"], e = class_b(c); errs.append(e) if e else None
    res["C_orphan_assignee"] = class_c(c)
    res["D_zombie_bridge"], e = class_d(c); errs.append(e) if e else None
    res["E_todo_hanging"] = class_e(c)

    # --- blok F (v1.1.0) ---
    roster, rerr = load_roster()
    if rerr:
        errs.append(rerr)
    parked = parse_parked(notepad_get("parked"))
    ping_sent = parse_ping_sent(notepad_get("ping_sent"))
    ping_mode = (notepad_get("ping_mode") or "dry").strip().splitlines()[-1].strip() or "dry"
    if ping_mode not in ("dry", "live"):
        errs.append("ping_mode_tak_dikenal=%s -> dianggap dry (gagal aman)" % ping_mode)
        ping_mode = "dry"
    f_lists = {}
    f_lists["F1_worker_idle_stale"] = class_f1(c, parked)
    f_lists["F2_run_over_runtime"], n_null = class_f2(c, parked)
    f_lists["F3_chain_silent"] = class_f3(c, parked)
    f_lists["F4_ready_unclaimed"] = class_f4(c, parked)
    f_lists["F5_gate_crash_unanswered"] = class_f5(c, parked)
    res.update(f_lists)
    cands, deduped = build_candidates(c, f_lists, roster, parked, ping_sent)
    groups = aggregate(c, cands, ping_sent)
    planned = [g for g in groups if g["within_cap"] and not g["dedup_secondary"]]
    total = sum(len(res[k]) for k in ("A_gate_over_2h", "B_two_channel_gap", "C_orphan_assignee",
                                      "D_zombie_bridge", "E_todo_hanging"))  # KS-7: TOTAL lama = A-E saja
    total_f = sum(len(v) for v in f_lists.values())
    payload = dict(findings=res, errors=[x for x in errs if x], total=total, total_f=total_f,
                   f_context=dict(ping_mode=ping_mode, parked_guard=sorted(parked),
                                  skipped_null_maxruntime=n_null, cap=PING_CAP,
                                  candidates=len(cands), deduped=deduped,
                                  aggregate=[{k: g[k] for k in ("owner", "title", "cards", "klasses",
                                                                "rule", "within_cap", "dedup_secondary")}
                                             for g in groups],
                                  planned_ping=len(planned)))
    if "--json" in sys.argv:
        print(json.dumps(payload, ensure_ascii=False))
    else:
        for k, v in res.items():
            print(k + ":")
            for item in v:
                print("   ", json.dumps(item, ensure_ascii=False))
        for x in errs:
            if x:
                print("ERROR:", x)
        print("TOTAL TEMUAN:", total)
        print("TOTAL KELAS F:", total_f)
        print("F_CONTEXT:")
        print("   ping_mode:", ping_mode, "| parked_guard:", sorted(parked),
              "| skipped_null_maxruntime:", n_null, "| cap:", PING_CAP)
        print("   kandidat:", len(cands), "| dedup primer:", len(deduped))
        for dd in deduped:
            print("   DEDUP:", json.dumps(dd, ensure_ascii=False))
        print("F_AGGREGATE (per pemilik; umur tertua dulu, kap %d/siklus):" % PING_CAP)
        for g in groups:
            print("   ", json.dumps({k: g[k] for k in ("owner", "title", "cards", "klasses",
                                                       "rule", "within_cap", "dedup_secondary")},
                                    ensure_ascii=False))
        mode_label = "CALON-PING (mode dry - TIDAK ada kartu dibuat skrip)" if ping_mode == "dry" else \
                     "RENCANA-PING (mode live - eksekusi oleh agen cron via tool kanban_create, BUKAN skrip)"
        print(mode_label)
        for g in groups:
            if g["within_cap"] and not g["dedup_secondary"]:
                print("   ", json.dumps({"assignee": g["owner"], "priority": 50, "title": g["title"],
                                         "cards": g["cards"]}, ensure_ascii=False))
        if not groups:
            print("    (tidak ada kandidat)")

if __name__ == "__main__":
    main()
