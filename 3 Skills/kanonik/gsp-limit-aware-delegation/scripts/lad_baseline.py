#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""lad_baseline.py - baseline metrik pra-deploy kebijakan LAD (F-8, spesifikasi C.6).

Dijalankan SEKALI sebelum kartu patuh pertama. Read-only total terhadap kanban
DB: satu-satunya operasi tulis adalah berkas BASELINE.md di folder kontrak
(path default bisa dioverride dengan --out; --out hanya boleh dipakai untuk
bukti smoke, mis. BASELINE-SMOKE.md).

Cara jalan (Windows, python nyata):
  C:/Users/TRIAL/AppData/Roaming/uv/python/cpython-3.11.15-windows-x86_64-none/python.exe \
      lad_baseline.py [--window-days 14] [--out <path>] [--db <path>]

Metrik wajib C.6.2 selama jendela (default 14 hari):
  M1 jumlah run per outcome; M2 kartu done tanpa summary/result;
  M3 kartu dengan >1 run (proksi dispatch ulang); M4 durasi run median/p90.
Kejujuran C.6.3: bila kolom pencacah iterasi per run tidak ada di skema DB,
metrik iterasi TIDAK tersedia -> V-10 memakai proksi dan tetap NEEDS_REVIEW
sampai >= 10 kartu pasca-deploy. Skema di-introspeksi (PRAGMA table_info)
sebelum kueri; tidak ada nama kolom yang dikarang.
"""
import argparse
import os
import sqlite3
import sys
import time
from datetime import datetime, timezone

DEFAULT_CONTRACT = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-limit-aware-delegation"
# Kandidat lokasi DB dispatcher (C.6.1): keduanya dicek, yang hidup yang dibaca.
DB_CANDIDATES = [
    os.path.join(os.path.expanduser("~"), ".hermes", "kanban.db"),
    os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "kanban.db"),
]


def pick_db(cli_db):
    """Pilih DB kanban yang hidup: non-zero, header SQLite valid, punya tabel tasks."""
    cands = [cli_db] if cli_db else DB_CANDIDATES
    report = []
    for p in cands:
        if not p or not os.path.exists(p):
            report.append((p, "TIDAK ADA"))
            continue
        size = os.path.getsize(p)
        if size == 0:
            report.append((p, f"kosong (0 B) -> dilewati"))
            continue
        try:
            con = sqlite3.connect("file:{}?mode=ro".format(p.replace("\\", "/")), uri=True)
            ok = con.execute(
                "SELECT COUNT(*) FROM sqlite_master WHERE type='table' AND name='tasks'"
            ).fetchone()[0]
            con.close()
            if ok:
                report.append((p, "hidup (tabel tasks ada) -> DIPILIH"))
                return p, report
            report.append((p, f"{size} B tapi tanpa tabel tasks -> dilewati"))
        except Exception as e:
            report.append((p, f"gagal dibuka ({e}) -> dilewati"))
    return None, report


def table_cols(cur, table):
    return [r[1] for r in cur.execute("PRAGMA table_info(%s)" % table)]


def percentile(sorted_vals, q):
    """Persentil nearest-rank pada daftar terurut (stdlib saja)."""
    if not sorted_vals:
        return None
    idx = max(0, min(len(sorted_vals) - 1, int(round(q * (len(sorted_vals) - 1)))))
    return sorted_vals[idx]


def fmt_ts(ts):
    if ts is None:
        return "-"
    return datetime.fromtimestamp(ts, tz=timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ")


def main():
    ap = argparse.ArgumentParser(description="Baseline metrik LAD (read-only, C.6)")
    ap.add_argument("--window-days", type=int, default=14)
    ap.add_argument("--out", default=os.path.join(DEFAULT_CONTRACT, "BASELINE.md"),
                    help="satu-satunya berkas yang boleh ditulis skrip ini")
    ap.add_argument("--db", default=None, help="override lokasi DB (default: deteksi)")
    args = ap.parse_args()

    out_path = os.path.abspath(args.out)
    db_path, db_report = pick_db(args.db)
    lines = []
    lines.append("# BASELINE - metrik pra-deploy kebijakan LAD (spesifikasi C.6)")
    lines.append("")
    lines.append("- Dibuat: %s (UTC) oleh scripts/lad_baseline.py" %
                 datetime.now(timezone.utc).strftime("%Y-%m-%d %H:%M:%SZ"))
    lines.append("- Jendela metrik: %d hari terakhir sejak eksekusi." % args.window_days)
    lines.append("- Metode: baca kanban DB mode read-only (`mode=ro`, tanpa commit);")
    lines.append("  skema di-introspeksi lewat `PRAGMA table_info` sebelum kueri;")
    lines.append("  tidak ada kolom yang dikarang. Satu-satunya tulis: berkas ini.")
    lines.append("")
    lines.append("## Lokasi DB yang dicek (C.6.1)")
    for p, st in db_report:
        lines.append("- `%s` - %s" % (p, st))
    if not db_path:
        lines.append("")
        lines.append("VERDICT: FAIL - tidak ada kanban DB hidup yang terbaca.")
        print("\n".join(lines))
        return 2
    now = time.time()
    cutoff = now - args.window_days * 86400
    lines.append("- Timestamp epoch: now=%d cutoff=%d" % (int(now), int(cutoff)))
    lines.append("")

    con = sqlite3.connect("file:" + db_path.replace("\\", "/") + "?mode=ro", uri=True)
    cur = con.cursor()
    tables = [r[0] for r in cur.execute(
        "SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'")]

    # --- Introspeksi skema (WAJIB sebelum kueri) ---
    lines.append("## Skema hasil introspeksi (PRAGMA table_info)")
    schema_cols = {}
    for t in sorted(tables):
        schema_cols[t] = table_cols(cur, t)
        lines.append("- `%s`: %s" % (t, ", ".join(schema_cols[t])))
    lines.append("")

    # --- Deteksi kolom pencacah iterasi (kejujuran C.6.3 / D-TA-07) ---
    iter_pat = ("iter", "turn", "step_count", "tool_calls")
    # Kolom KNOWN yang cocok pola tapi bukan pencacah iterasi per-run:
    #   step_key            = kunci langkah workflow (bukan hitungan)
    #   goal_mode/goal_max_turns = knob konfigurasi dispatch (budget, bukan terpakai)
    non_counters = {"step_key", "goal_mode", "goal_max_turns"}
    iter_cols = [(t, c) for t, cols in schema_cols.items()
                 for c in cols
                 if any(k in c.lower() for k in iter_pat) and c not in non_counters]

    # --- M1: run per outcome dalam jendela ---
    m1_lines = []
    if "task_runs" in schema_cols and "outcome" in schema_cols["task_runs"]:
        rows = cur.execute(
            "SELECT COALESCE(outcome,'(NULL/in-flight)'), COUNT(*) FROM task_runs "
            "WHERE started_at >= ? GROUP BY outcome ORDER BY 2 DESC", (cutoff,)).fetchall()
        total_runs = sum(n for _, n in rows)
        m1_lines.append("Total run dalam jendela: %d" % total_runs)
        for o, n in rows:
            m1_lines.append("- %s: %d" % (o, n))
    else:
        m1_lines.append("TIDAK TERSEDIA - tabel task_runs/kolom outcome tidak ada.")

    # --- M2: kartu done tanpa summary/result ---
    m2_lines = []
    tc = schema_cols.get("tasks", [])
    rc = schema_cols.get("task_runs", [])
    if "tasks" in schema_cols and "status" in tc:
        sel = "COUNT(*)"
        cond = ["t.status = 'done'",
                "(t.completed_at IS NULL OR t.completed_at >= ?)"]
        params = [cutoff]
        has_result = "result" in tc
        has_summary = "summary" in rc
        if not has_result and not has_summary:
            m2_lines.append("TIDAK TERSEDIA - kolom result/summary tidak ada di skema.")
        else:
            parts = []
            if has_result:
                parts.append("NULLIF(TRIM(t.result),'') IS NULL")
            if has_summary:
                parts.append("NOT EXISTS (SELECT 1 FROM task_runs r "
                             "WHERE r.task_id = t.id AND NULLIF(TRIM(r.summary),'') IS NOT NULL)")
            q = ("SELECT %s FROM tasks t WHERE %s AND (%s)" %
                 (sel, " AND ".join(cond), " AND ".join(parts)))
            n_done_nosum = cur.execute(q, params).fetchone()[0]
            n_done_total = cur.execute(
                "SELECT COUNT(*) FROM tasks t WHERE t.status='done' "
                "AND (t.completed_at IS NULL OR t.completed_at >= ?)", params).fetchone()[0]
            m2_lines.append("Kartu done selesai dalam jendela: %d" % n_done_total)
            m2_lines.append("- done TANPA summary (run) dan TANPA result: %d" % n_done_nosum)

    # --- M3: kartu dengan >1 run (proksi dispatch ulang) ---
    m3_lines = []
    if "task_runs" in schema_cols and "task_id" in rc:
        rows = cur.execute(
            "SELECT COUNT(*), COALESCE(SUM(n),0), COALESCE(MAX(n),0) FROM ("
            "SELECT task_id, COUNT(*) n FROM task_runs WHERE started_at >= ? "
            "GROUP BY task_id HAVING COUNT(*) > 1)", (cutoff,)).fetchone()
        m3_lines.append("Kartu dengan lebih dari satu run: %d "
                        "(total run ekstra=%d, maksimum run utk 1 kartu=%d)"
                        % (rows[0], rows[1] - rows[0], rows[2]))
    else:
        m3_lines.append("TIDAK TERSEDIA - tabel task_runs tidak ada.")

    # --- M4: durasi run median/p90 ---
    m4_lines = []
    if all(c in rc for c in ("started_at", "ended_at")):
        durs = sorted(d for (s, e) in cur.execute(
            "SELECT started_at, ended_at FROM task_runs WHERE started_at >= ? "
            "AND ended_at IS NOT NULL AND ended_at >= started_at", (cutoff,))
            for d in [e - s])
        if durs:
            med = percentile(durs, 0.5)
            p90 = percentile(durs, 0.9)
            m4_lines.append("Run berakhir dalam jendela: %d" % len(durs))
            m4_lines.append("- durasi median: %.1f menit" % (med / 60.0))
            m4_lines.append("- durasi p90:    %.1f menit" % (p90 / 60.0))
            m4_lines.append("- durasi maks:   %.1f menit" % (durs[-1] / 60.0))
        else:
            m4_lines.append("TIDAK TERSEDIA - tidak ada run ber-ended_at dalam jendela.")
    else:
        m4_lines.append("TIDAK TERSEDIA - kolom waktu run tidak lengkap di skema.")

    # --- Render laporan ---
    lines.append("## M1 - run per outcome (%d hari terakhir)" % args.window_days)
    lines += m1_lines
    lines.append("")
    lines.append("## M2 - kartu done tanpa summary/result")
    lines += m2_lines
    lines.append("")
    lines.append("## M3 - kartu dengan >1 run (proksi dispatch ulang)")
    lines += m3_lines
    lines.append("")
    lines.append("## M4 - durasi run")
    lines += m4_lines
    lines.append("")
    lines.append("## Pernyataan jujur: metrik iterasi per run (C.6.3, D-TA-07)")
    if iter_cols:
        lines.append("- Kolom kandidat pencacah iterasi TERDETEKSI: %s - perlu "
                     "verifikasi manusia sebelum dipakai sebagai angka." %
                     ", ".join("%s.%s" % x for x in iter_cols))
    else:
        lines.append("- Hasil scan nama kolom (substring 'iter'/'turn'/'step_count'/"
                     "'tool_calls'; dikecualikan karena diketahui bukan pencacah: "
                     "step_key, goal_mode, goal_max_turns): TIDAK ADA kolom pencacah "
                     "iterasi per run di skema DB kanban ini.")
        lines.append("- Konsekuensi: metrik iterasi-per-run TIDAK dapat dihitung dari DB; "
                     "V-10 memakai proksi (M1/M3/M4) dan statusnya NEEDS_REVIEW sampai "
                     ">= 10 kartu pasca-deploy diaudit.")
    lines.append("")
    lines.append("_Read-only total: koneksi `mode=ro`, tidak ada statement tulis; "
                 "satu-satunya operasi tulis skrip ini adalah berkas BASELINE ini._")
    report = "\n".join(lines) + "\n"

    # --- Satu-satunya operasi tulis ---
    os.makedirs(os.path.dirname(out_path), exist_ok=True)
    with open(out_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(report)
    con.close()

    print(report)
    print("[lad_baseline] BASELINE ditulis ke: %s (%d byte)" %
          (out_path, os.path.getsize(out_path)))
    return 0


if __name__ == "__main__":
    sys.exit(main())
