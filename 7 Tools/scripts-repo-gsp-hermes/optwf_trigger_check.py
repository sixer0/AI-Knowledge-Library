#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
optwf_trigger_check.py - pemeriksaan harian trigger O-E (misi OPT-WF-0907, kartu t_ca58ea04 / OPT-WF-D9).

Tiga trigger beku (blueprint 02_structured.md rank 7 - O-E):
  (a) backlog promoted-tak-claimed > 5 kartu selama > 10 menit
  (b) kejadian at-capacity di log tick dispatcher muncul rutin
  (c) running >= 18 sustain

Definisi operasional (dipakukan D9, 2026-09-08; sumber mentah disebut per angka):
  (a) max_ambil_tunggu = maksimum atas waktu-tick dispatcher (baris "kanban dispatcher
      [board]:" di gateway.log*) dari jumlah kartu status ready yang sudah >=600 dtk
      menunggu diambil. Waktu masuk-ready = event 'promoted'; kartu tanpa event
      promoted (kartu awal tanpa parent) memakai created_at. Kartu yang belum
      pernah claimed dihitung sampai now() saat pengukuran; yang sudah claimed
      sampai claimed pertamanya. BUNYI bila max_ambil_tunggu > 5.
      Catatan: pembanding tambahan = jumlah kartu yang PERNAH menunggu promoted->klaim
      > 10 menit dalam hari itu (bukan kondisi simultan; tidak memicu vonis).
  (b) dua lapis: (b1) grep kata kunci kapasitas ('capacit', 'at cap', 'max_spawn',
      'max_in_progress', 'pressure') pada baris dispatcher hari itu - mesin tidak
      menulis kata "at-capacity" eksplisit (dibuktikan probe 08-09), jadi (b1)
      struktural SENYAP; (b2) proksi rekonstruksi dari task_runs: jumlah MENIT
      berjalan=cap host (max_in_progress aktif, dibaca dari log startup) DAN ada
      kartu ready menunggu pada menit yang sama. BUNYI (b2) bila menit_at_cap >= 60
      (ambang "rutin" dipakukan: >=60 menit/hari; ambang lain dicatat di JSON).
  (c) running = interval task_runs (started_at..ended_at|now) per menit lokal.
      Sustain dipakukan: >=18 selama >=30 menit berturut. BUNYI bila sustain>=18
      >= 30 menit. Puncak running dilaporkan sebagai konteks; kondisi cap host
      sudah dicakup proksi (b2).

Pemakaian:
  python optwf_trigger_check.py [--date YYYY-MM-DD] [--tz-offset 7]
      [--kanban-db PATH] [--logs-glob PATH] [--no-write]
Default --date = hari ini zona Asia/Jakarta (UTC+7). Output: blok markdown ke stdout,
append ke measures/TRIGGER-LOG.md (idempoten: blok tanggal sama diganti), dan JSONL
ke measures/trigger/<tanggal>.jsonl. Tidak mengubah konfigurasi apa pun (read-only).
"""

import argparse
import glob
import json
import os
import re
import sqlite3
import sys
from datetime import datetime, timedelta, timezone

DEFAULT_DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
DEFAULT_LOGS = r"C:/Users/TRIAL/AppData/Local/hermes/logs/gateway.log*"
DEFAULT_MEAS = ("C:/Users/TRIAL/workspace/gsp-hermes/workspace/"
                "docs/2026-09-07-opt-orchestration-throughput/measures")

TICK_RE = re.compile(
    r"^(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2}),\d{3} INFO gateway\.run: "
    r"kanban dispatcher(?: \[([^\]]+)\])?: ?(.*)$")
# baris tick per-board = rentetan key=value berpasangan (spawned=1 reclaimed=0 ...)
TICK_TAIL_RE = re.compile(r"^\w+=\d+(?: \w+=\d+)+$")
CAP_RE = re.compile(r"capacit|at cap|pressure", re.I)
RUNNING_CAP_RE = re.compile(r"^max_(?:in_progress|spawn)(?:_per_profile)?=(\d+|None)$")

MIN_WAIT_A = 600        # (a) "lama" = minimal 10 menit
BACKLOG_A = 5           # (a) > 5 kartu
ATCAP_MIN_B = 60        # (b2) >= 60 menit/hari dianggap rutin
SUSTAIN_C_MIN = 30      # (c) sustain >= 30 menit
HIGH_C = 18             # (c) ambang running
LINE = "-" * 70


def parse_args():
    ap = argparse.ArgumentParser()
    ap.add_argument("--date", help="YYYY-MM-DD (default: hari ini Asia/Jakarta)")
    ap.add_argument("--tz-offset", type=float, default=7.0)
    ap.add_argument("--kanban-db", default=DEFAULT_DB)
    ap.add_argument("--logs-glob", default=DEFAULT_LOGS)
    ap.add_argument("--meas-dir", default=DEFAULT_MEAS)
    ap.add_argument("--no-write", action="store_true")
    return ap.parse_args()


def main():
    a = parse_args()
    tz = timezone(timedelta(hours=a.tz_offset))
    now_dt = datetime.now(tz)
    if a.date:
        day = datetime.strptime(a.date, "%Y-%m-%d").replace(tzinfo=tz)
    else:
        day = now_dt.replace(hour=0, minute=0, second=0, microsecond=0)
    d0, d1 = int(day.timestamp()), int(day.timestamp()) + 86400
    now_ep = int(now_dt.timestamp())
    end = min(d1, now_ep)  # hari berjalan: potong sampai sekarang

    con = sqlite3.connect(a.kanban_db)
    con.row_factory = sqlite3.Row

    # ------------------------------------------------ log dispatcher
    tick_ts = []            # epoch semua baris tick per-board
    cap_kw_lines = []       # (ts, potongan baris) kata kunci kapasitas
    cap_cfg = None          # max_in_progress dari baris startup
    files = sorted(glob.glob(a.logs_glob))
    for fp in files:
        try:
            f = open(fp, encoding="utf-8", errors="ignore")
        except OSError:
            continue
        with f:
            for line in f:
                m = TICK_RE.match(line)
                if not m:
                    continue
                ts = int(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S")
                         .replace(tzinfo=tz).timestamp())
                if not (d0 <= ts <= end):
                    continue
                tail = m.group(3)
                if TICK_TAIL_RE.match(tail):
                    tick_ts.append(ts)
                else:
                    mm = RUNNING_CAP_RE.match(tail)
                    if mm and mm.group(1).isdigit():
                        cap_cfg = int(mm.group(1))
                    if CAP_RE.search(tail):
                        cap_kw_lines.append((ts, tail[:120]))
    tick_ts.sort()
    if cap_cfg is None:
        cap_cfg = 20  # fallback terdokumentasi: nilai on-disk config master 08-09

    # ------------------------------------------------ (a) backlog ambil-tugas
    # batas hidup siap-diukur utk kartu claimed: claimed pertama; selain itu now.
    first_promoted = {r["task_id"]: r["t"] for r in con.execute(
        "SELECT task_id, MIN(created_at) t FROM task_events WHERE kind='promoted' GROUP BY 1")}
    first_claimed = {r["task_id"]: r["t"] for r in con.execute(
        "SELECT task_id, MIN(created_at) t FROM task_events WHERE kind='claimed' GROUP BY 1")}
    tasks = {}  # id -> (enter_ready, exit_ready|None)
    for r in con.execute("SELECT id, status, created_at FROM tasks"):
        enter = first_promoted.get(r["id"])
        if enter is None:
            # tanpa event promoted: masuk-ready saat created HANYA bila memang
            # pernah claimable (pernah claimed) atau masih ready sekarang
            if r["id"] in first_claimed or r["status"] == "ready":
                enter = r["created_at"]
            else:
                continue
        claim = first_claimed.get(r["id"])
        if claim is None and r["status"] != "ready":
            # tidak pernah claimed dan tidak lagi ready -> tak terukur; lewati
            continue
        exit_ = claim  # None bila masih ready (dipotong now_ep di backlog_at)
        tasks[r["id"]] = (enter, exit_)
    # hitung di tiap tick + snapshot akhir
    def backlog_at(t):
        n = 0
        for enter, exit_ in tasks.values():
            out = exit_ if exit_ is not None else now_ep
            if enter + MIN_WAIT_A <= t < out:
                n += 1
        return n
    max_a = 0
    max_a_t = None
    samples = tick_ts + [end]
    for t in samples:
        n = backlog_at(t)
        if n > max_a:
            max_a, max_a_t = n, t
    # pembanding: kartu yang promoted->klaim > 10 mnt dengan klaim di hari ini
    gt10_slow = 0
    for cid, cl in first_claimed.items():
        if not (d0 <= cl <= end):
            continue
        pr = first_promoted.get(cid)
        if pr is not None and cl - pr > MIN_WAIT_A and cl - pr < 86400 * 30:
            gt10_slow += 1
    trig_a = max_a > BACKLOG_A

    # ------------------------------------------------ (c) running per menit
    # Dispatcher menghitung running = tasks.status='running'. Rekonstruksi dari
    # task_runs: interval started_at..ended_at; baris ber-ended_at NULL dihitung
    # sampai now HANYA bila kartunya masih berstatus running (baris NULL milik
    # kartu mati = zombie jejak crash/reclaim, bukan running aktif).
    live_set = {r["id"] for r in con.execute("SELECT id FROM tasks WHERE status='running'")}
    runs = []
    for r in con.execute("SELECT task_id, started_at, ended_at FROM task_runs "
                         "WHERE started_at IS NOT NULL"):
        if r["ended_at"] is None:
            if r["task_id"] not in live_set:
                continue
            e = max(now_ep, r["started_at"] + 1)
        else:
            e = max(r["ended_at"], r["started_at"] + 1)
        runs.append((r["started_at"], e))
    minutes = list(range(d0, end, 60))
    run_series = []
    for m0 in minutes:
        c = sum(1 for s, e in runs if s <= m0 < e)
        run_series.append(c)
    peak_c = max(run_series) if run_series else 0
    # sustain >= HIGH_C menit berturut
    best_run = cur = 0
    for c in run_series:
        cur = cur + 1 if c >= HIGH_C else 0
        best_run = max(best_run, cur)
    # vonis (c) sesuai definisi beku: >=18 SUSTAIN; puncak >= cap dilaporkan
    # sebagai konteks dan sudah tercakup proksi (b2), bukan pemicu terpisah.
    trig_c = best_run >= SUSTAIN_C_MIN

    # ------------------------------------------------ (b) at-capacity
    b1 = len(cap_kw_lines)  # struktural 0 (mesin tak menulis kata kapasitas saat kap)
    # b2 proksi: menit dengan running >= cap DAN backlog ready (siap diambil) >= 1
    def ready_any_at(t):
        for enter, exit_ in tasks.values():
            out = exit_ if exit_ is not None else now_ep
            if enter <= t < out:
                return True
        return False
    at_cap_min = 0
    for i, m0 in enumerate(minutes):
        if run_series[i] >= cap_cfg and ready_any_at(m0):
            at_cap_min += 1
    trig_b = b1 > 0 or at_cap_min >= ATCAP_MIN_B

    # ------------------------------------------------ laporan
    ts_now = now_dt.strftime("%Y-%m-%d %H:%M:%S%z")
    def st(v):
        return "BUNYI" if v else "senyap"
    jam_ukur = "%.1f" % ((end - d0) / 3600.0)
    blok = []
    blok.append("## %s (diukur %s WIB; jendela ukur %s jam)" % (day.strftime("%Y-%m-%d"), now_dt.strftime("%H:%M"), jam_ukur))
    blok.append("")
    blok.append("| Trigger | Angka | Ambang | Status |")
    blok.append("|---|---|---|---|")
    blok.append("| (a) backlog ambil-tunggu | maks %s kartu siap >10 mnt (pada %s) | >5 kartu | %s |" % (
        max_a, datetime.fromtimestamp(max_a_t, tz).strftime("%H:%M") if max_a_t else "-", st(trig_a)))
    blok.append("| (b) at-capacity dispatcher | b1 kata-kunci=%s; b2 menit cap+backlog=%s (cap=%s) | b1>0 atau b2>=%s mnt | %s |" % (
        b1, at_cap_min, cap_cfg, ATCAP_MIN_B, st(trig_b)))
    blok.append("| (c) running tinggi | puncak %s; sustain >=18 selama %s mnt | >=18 sustain %s mnt (cap host %s) | %s |" % (
        peak_c, best_run, SUSTAIN_C_MIN, cap_cfg, st(trig_c)))
    blok.append("")
    blok.append("Pembanding (a): kartu yang PERNAH menunggu promoted->klaim >10 mnt dengan klaim hari ini: %s." % gt10_slow)
    blok.append("Sumber: kanban.db (tasks/task_events/task_runs) + gateway.log* baris 'kanban dispatcher'; "
                "tick terbaca %s; definisi operasional dipakukan di blok setup TRIGGER-LOG.md. "
                "Vonis hari ini: %s." % (len(tick_ts), "TERPICU" if (trig_a or trig_b or trig_c) else "SENYAP"))
    blok_txt = "\n".join(blok)

    # JSON jejak
    rec = {"tanggal": day.strftime("%Y-%m-%d"), "diukur": ts_now,
           "jendela_jam": float(jam_ukur), "cap_host": cap_cfg,
           "tick_lines": len(tick_ts),
           "a": {"max_backlog_gt10m": max_a, "pada": max_a_t, "pembanding_gt10m": gt10_slow, "bunyi": trig_a},
           "b": {"kata_kunci": b1, "menit_cap_dengan_backlog": at_cap_min, "ambang_menit": ATCAP_MIN_B, "bunyi": trig_b},
           "c": {"puncak": peak_c, "sustain_ge18_menit": best_run, "ambang_sustain": SUSTAIN_C_MIN, "bunyi": trig_c},
           "vonis": "TERPICU" if (trig_a or trig_b or trig_c) else "SENYAP"}

    print(blok_txt)
    if a.no_write:
        return

    os.makedirs(a.meas_dir, exist_ok=True)
    tlog = os.path.join(a.meas_dir, "TRIGGER-LOG.md")
    header_needed = not os.path.exists(tlog)
    old = ""
    if not header_needed:
        old = open(tlog, encoding="utf-8").read()
    # buang blok tanggal sama lalu append
    marker = "## %s (diukur" % day.strftime("%Y-%m-%d")
    if marker in old:
        pre, rest = old.split(marker, 1)
        nxt = rest.find("\n## ")
        old = pre + (rest[nxt:] if nxt != -1 else "")
    if header_needed:
        old = ("# TRIGGER-LOG - pemantauan trigger O-E harian (OPT-WF-D9)\n\n"
               "Masa uji: 08-09 s/d 15-09. Vonis NO-ACTION selama trigger tidak bunyi "
               "(blueprint O-E rank 7). Satu blok per hari, ditulis skrip "
               "`workspace/gsp-hermes/scripts/optwf_trigger_check.py` via cron profil "
               "gsp-data-analyst (job optwf-d9-trigger-harian, 06:30 WIB, repeat 8; "
               "fallback manual: `python <skrip> --date YYYY-MM-DD`).\n\n"
               "### Definisi operasional (dipakukan 2026-09-08, kartu t_ca58ea04)\n\n"
               "- (a) maksimum simultan kartu status ready yang sudah >=600 dtk menunggu "
               "diambil, dievaluasi pada tiap waktu tick dispatcher (gateway.log). "
               "Masuk-ready = event promoted; kartu awal tanpa parent pakai created_at. "
               "BUNYI bila >5.\n"
               "- (b) b1 = kata kunci kapasitas pada baris dispatcher (mesin tidak "
               "menulis kata 'at-capacity' eksplisit; dibuktikan probe 08-09, jadi b1 "
               "struktural nol). b2 = proksi rekonstruksi: menit dengan running == cap "
               "host (max_in_progress dari log startup, kini 20) DAN ada kartu ready "
               "menunggu. BUNYI (b) bila b1>0 ATAU b2>=60 menit/hari.\n"
               "- (c) running per menit direkonstruksi dari interval task_runs "
               "(baris ended_at NULL dihitung s/d waktu ukur hanya bila kartunya "
               "masih running; NULL milik kartu mati = zombie, dikecualikan). BUNYI "
               "bila >=18 selama >=30 menit berturut; puncak running dilaporkan "
               "sebagai konteks (kondisi cap host dicakup proksi b2).\n"
               "- Alat: read-only terhadap kanban.db + gateway.log*; konfigurasi tidak "
               "pernah diubah oleh pemantauan ini.\n\n")
    with open(tlog, "w", encoding="utf-8") as f:
        f.write(old.rstrip() + "\n\n" + blok_txt + "\n")
    jdir = os.path.join(a.meas_dir, "trigger")
    os.makedirs(jdir, exist_ok=True)
    with open(os.path.join(jdir, day.strftime("%Y-%m-%d") + ".jsonl"), "a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    print("\n[ditulis] %s\n[json] %s/%s.jsonl" % (tlog, jdir, day.strftime("%Y-%m-%d")))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    main()
