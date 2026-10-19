#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
gsp_mission_wake_scan.py - Pemindai kebutuhan tangan controller untuk cron mission-wake
(PMODE-1010, D-04: backstop agar misi tidak berhenti di tengah jalan).

Pola diam-sehat: stdout kosong = tidak ada yang perlu dibangunkan (exit 0).
BACA-SAJA: sqlite dibuka URI 'file:...?mode=ro' + PRAGMA query_only; tidak menulis apa pun.

Temuan (satu baris per temuan, sortir stabil tid lalu alasan):
  WAKE <tid> stalled <umur_menit>          kartu blocked/review/todo; event terakhir >30 menit
                                           DAN belum ada komentar author controller setelah event itu.
  WAKE <tid> run-<outcome> <umur_menit>    run outcome crashed/timed_out/gave_up <=6 jam terakhir
                                           milik kartu yang belum done/archived.
  WAKE <tid> fase-stalled <umur_menit>     promoted antar-fase terakhir >60 menit tanpa komentar
  WAKE <tid> done-unacked <umur_menit>     kartu selesai <60 mnt lalu, tanpa RANTAI-ACK dan tanpa wake-sub (silent-done PMODE-DELEG-1010)
                                           [FASE] sesudahnya (kartu belum done/archived).

Kecuali: status done/archived; tenant kosong era-lama yang sudah berjejak PROF-MERGE-1010
(komentar memuat 'PROF-MERGE-1010').

WAKE-FIX-1015 (15-10-2026, anti-refire): SEMUA kelas diberi dedup sekali-per-kejadian.
Agen cron (mission-wake) menulis marker komentar "RANTAI-WAKE <kelas> <epoch>" setelah
melaporkan sebuah kejadian; pemindai tidak melaporkan ulang kejadian yang sudah
ber-marker, tetapi kejadian BARU (event lebih muda dari marker terakhir) tetap
dilaporkan. Lampu merah tetap menyala di papan (status kartu tidak diubah);
yang dihentikan hanya pengulangan pesan yang sama tiap siklus.

Determinisme: --now <epoch> membekukan jam dinding; tanpa itu pakai waktu kini.

Owner-dinamis (STA13-N1WAKESCAN, misi SERAH-TERIMA-ASIGNOR-1013): author controller yang
sah per kartu = daftar basis (--controller-authors, default DEFAULT_AUTHORS) UNION created_by
kartu tersebut. Kartu ber-owner created_by nyata (mis. gsp-master/gsp-master01) dikenali
sebagai controller penugas, bukan divonis 'asing' oleh daftar statis. Daftar statis lama
tetap diterima penuh.
"""
import argparse
import os
import sqlite3
import sys

DEFAULT_DB = os.path.join(os.environ.get("LOCALAPPDATA", r"C:/Users/TRIAL/AppData/Local"), "hermes", "kanban.db")
# STA13-N1WAKESCAN: basis statis; owner dinamis kartu (created_by) di-union per kartu di scan().
DEFAULT_AUTHORS = "default,sysmanager-cleaner,mission-wake"
STALLED_MIN = 30
RUN_WINDOW_H = 6
FASE_STALL_MIN = 60
DONE_UNACKED_MIN = 5  # silent-done: selesai >=5 mnt tanpa ACK/wake
DONE_UNACKED_WINDOW = 6 * 3600  # rute-4b: jendela selebar kelas run (dedup marker)
# rute-4b: protokol serah-terima baru mengikat sejak tayang 10-10 18:00;
# kartu selesai sebelum itu = warisan historis, bukan cacat serah terima.
DONE_UNACKED_CUTOFF = 1791630000  # 2026-10-10 17:40 WIB (pra-tayang 20 mnt)
OPEN_STATUSES = ("blocked", "review", "todo")
BAD_OUTCOMES = ("crashed", "timed_out", "gave_up")


def connect_ro(db_path):
    uri = "file:" + db_path.replace("\\", "/") + "?mode=ro"
    con = sqlite3.connect(uri, uri=True)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA query_only = ON")
    return con


def excluded_ids(con):
    """done/archived + tenant kosong era-lama berjejak PROF-MERGE-1010."""
    out = set(r["id"] for r in con.execute(
        "SELECT id FROM tasks WHERE status IN ('done','archived')"))
    for r in con.execute(
            "SELECT DISTINCT c.task_id AS id FROM task_comments c "
            "JOIN tasks t ON t.id = c.task_id "
            "WHERE c.body LIKE '%PROF-MERGE-1010%' AND (t.tenant IS NULL OR t.tenant = '')"):
        out.add(r["id"])
    return out


def scan(db_path, now, controller_authors):
    findings = []
    con = connect_ro(db_path)
    try:
        excl = excluded_ids(con)

        # (a) stalled: status buka, event terakhir basi, tanpa komentar controller setelahnya.
        # STA13-N1WAKESCAN: author sah per kartu = basis --controller-authors UNION created_by
        # kartu (owner-dinamis; penugas nyata seperti gsp-master/gsp-master01 bukan 'asing').
        for r in con.execute(
                "SELECT t.id AS id, t.status AS status, t.created_by AS created_by, "
                "COALESCE((SELECT MAX(e.created_at) FROM task_events e WHERE e.task_id = t.id), t.created_at) AS last_ev "
                "FROM tasks t WHERE t.status IN (%s)" % ",".join("?" * len(OPEN_STATUSES)), OPEN_STATUSES):
            if r["id"] in excl:
                continue
            age_min = int((now - r["last_ev"]) // 60)
            if age_min <= STALLED_MIN:
                continue
            authors = list(controller_authors)
            owner = (r["created_by"] or "").strip()
            if owner and owner not in authors:
                authors.append(owner)
            ph_a = ",".join("?" * len(authors))
            has_ctrl = con.execute(
                "SELECT 1 FROM task_comments c WHERE c.task_id = ? AND c.author IN (%s) "
                "AND c.created_at >= ? LIMIT 1" % ph_a,
                [r["id"]] + authors + [r["last_ev"]]).fetchone()
            if not has_ctrl:
                # WAKE-FIX-1015: dedup anti-refire. Marker RANTAI-WAKE stalled yang
                # ditulis agen cron sesudah anchor kejadian menutup ronde laporan
                # itu; kejadian baru (event > marker) dilaporkan lagi seperti biasa.
                # Komentar papan tidak menggerakkan last_ev (events-only), jadi
                # marker tidak me-reset timer stall.
                told = con.execute(
                    "SELECT 1 FROM task_comments c WHERE c.task_id = ? AND "
                    "c.body LIKE '%RANTAI-WAKE stalled%' AND c.created_at >= ? LIMIT 1",
                    (r["id"], r["last_ev"])).fetchone()
                if not told:
                    findings.append((r["id"], "stalled", age_min))

        # (b) run gagal baru
        for r in con.execute(
                "SELECT ru.task_id AS id, ru.outcome AS outcome, "
                "COALESCE(ru.ended_at, ru.started_at) AS ts, t.status AS tstatus "
                "FROM task_runs ru JOIN tasks t ON t.id = ru.task_id "
                "WHERE ru.outcome IN (%s)" % ",".join("?" * len(BAD_OUTCOMES)), list(BAD_OUTCOMES)):
            if r["id"] in excl or r["tstatus"] in ("done", "archived"):
                continue
            age_min = int((now - r["ts"]) // 60)
            if 0 <= age_min <= RUN_WINDOW_H * 60:
                # WAKE-FIX-1015: satu laporan per kejadian run gagal; marker
                # RANTAI-WAKE run-* sesudah ts run menangkap ronde lama tanpa
                # menahan laporan run gagal berikutnya (ts baru > marker).
                told = con.execute(
                    "SELECT 1 FROM task_comments c WHERE c.task_id = ? AND "
                    "c.body LIKE '%RANTAI-WAKE run-%' AND c.created_at >= ? LIMIT 1",
                    (r["id"], r["ts"])).fetchone()
                if not told:
                    findings.append((r["id"], "run-" + r["outcome"], age_min))

        # (c) promoted tanpa laporan [FASE]
        for r in con.execute(
                "SELECT t.id AS id, MAX(e.created_at) AS ts, t.status AS tstatus "
                "FROM tasks t JOIN task_events e ON e.task_id = t.id AND e.kind = 'promoted' "
                "GROUP BY t.id HAVING tstatus NOT IN ('done','archived')"):
            if r["id"] in excl:
                continue
            age_min = int((now - r["ts"]) // 60)
            if age_min <= FASE_STALL_MIN:
                continue
            has_fase = con.execute(
                "SELECT 1 FROM task_comments c WHERE c.task_id = ? AND c.body LIKE '%[FASE]%' "
                "AND c.created_at >= ? LIMIT 1", (r["id"], r["ts"])).fetchone()
            if not has_fase:
                # WAKE-FIX-1015: dedup sekali-per-kejadian juga untuk fase-stalled.
                told = con.execute(
                    "SELECT 1 FROM task_comments c WHERE c.task_id=? AND "
                    "c.body LIKE '%RANTAI-WAKE fase-stalled%' AND "
                    "c.created_at >= ? LIMIT 1", (r["id"], r["ts"])).fetchone()
                if not told:
                    findings.append((r["id"], "fase-stalled", age_min))
        # PMODE-DELEG-1010 rute-3: silent-DONE. Kartu menutup sendiri
        # (completed/blocked) tanpa pernah ada ACK dari author controller
        # DAN tanpa subscriber wake = rantai selesai senyap (bukti papan
        # t_3dfdc01a ronde-2 RETURN, 18:10, tidak membangunkan siapa pun).
        for r in con.execute(
                "SELECT e.task_id AS id, MAX(e.created_at) AS ts "
                "FROM task_events e JOIN tasks t ON t.id = e.task_id "
                "WHERE e.kind IN ('completed','blocked') AND t.status IN "
                "('done','review','blocked') AND e.created_at >= ? AND "
                "e.created_at >= ? AND "
                "t.tenant IS NOT NULL AND t.tenant != '' AND "
                "(t.assignee IS NULL OR t.assignee NOT IN (%s)) "
                "GROUP BY e.task_id HAVING ts >= ?"
                % ",".join("?" * len(controller_authors)),
                (now - DONE_UNACKED_WINDOW, DONE_UNACKED_CUTOFF,
                 *(controller_authors + [now - DONE_UNACKED_WINDOW]))):
            age_min = int((now - r["ts"]) // 60)
            if age_min < DONE_UNACKED_MIN:
                continue
            # Anchor ACK = komentar LAPOR-SELESAI terakhir bila ada (protokol
            # rute-4: ACK mendarat SEBELUM complete), jika tidak pakai event
            # terminal sebagai anchor (jalur lama/park).
            anchor = con.execute(
                "SELECT MAX(created_at) FROM task_comments WHERE task_id=? "
                "AND body LIKE '%LAPOR-SELESAI%'", (r["id"],)).fetchone()[0]
            anchor = anchor if anchor is not None else r["ts"]
            acked = con.execute(
                "SELECT 1 FROM task_comments c WHERE c.task_id = ? AND "
                "c.body LIKE '%RANTAI-ACK%' AND c.created_at >= ? LIMIT 1",
                (r["id"], anchor)).fetchone()
            # Rute-4b (10-10): wake-sub TIDAK lagi jadi pengecualian.
            # Bukti papan t_81a6fb00: kartu punya subs wake warisan era lama
            # yang membangunkan WhatsApp USER, bukan controller - dan tetap
            # menutup tanpa serah terima. Satu-satunya bukti serah terima
            # yang sah = token RANTAI-ACK dari author controller.
            if not acked:
                # rute-4b: ACK sah dari author mana pun KECUALI penulis
                # LAPOR-SELESAI (worker tidak boleh ACK dirinya sendiri).
                lap_author = con.execute(
                    "SELECT author FROM task_comments WHERE task_id=? AND "
                    "body LIKE '%LAPOR-SELESAI%' ORDER BY id DESC LIMIT 1",
                    (r["id"],)).fetchone()
                acks = con.execute(
                    "SELECT author FROM task_comments WHERE task_id=? AND "
                    "body LIKE '%RANTAI-ACK%'", (r["id"],)).fetchall()
                acked = any((a["author"] or '') != ((lap_author[0]
                          if lap_author else '') or '~') for a in acks)
            if not acked:
                # dedup: jangan laporkan kartu yang sudah pernah dilaporkan
                # kelas ini (marker RANTAI-WAKE ditulis cron agent).
                told = con.execute(
                    "SELECT 1 FROM task_comments WHERE task_id=? AND "
                    "body LIKE '%RANTAI-WAKE done-unacked%' LIMIT 1",
                    (r["id"],)).fetchone()
                if not told:
                    # WAKE-FIX-1015: marker baku RANTAI-WAKE sesudah anchor
                    # juga dihitung, bukan hanya varian legacy dengan nama
                    # kelas. Tanpa filter author (terukur: marker lama ber-
                    # author 'gsp-system-manager', bukan 'mission-wake' ->
                    # gerbang author membuat dedup mati senyap).
                    told = con.execute(
                        "SELECT 1 FROM task_comments c WHERE c.task_id=? AND "
                        "c.body LIKE '%RANTAI-WAKE %' AND c.created_at >= ? "
                        "LIMIT 1",
                        (r["id"], anchor)).fetchone()
                if not told:
                    findings.append((r["id"], "done-unacked", age_min))
    finally:
        con.close()
    findings.sort(key=lambda x: (x[0], x[1]))
    return findings


def main(argv=None):
    ap = argparse.ArgumentParser(prog="gsp_mission_wake_scan.py", description="Pemindai mission-wake read-only (PMODE-1010 D-04)")
    ap.add_argument("--db", default=DEFAULT_DB, help="jalur kanban.db (dibuka mode ro)")
    ap.add_argument("--now", type=int, default=None, help="epoch pembeku waktu (determinisme uji)")
    ap.add_argument("--controller-authors", default=DEFAULT_AUTHORS,
                    help="daftar author controller basis, dipisah koma "
                         "(created_by tiap kartu selalu ikut sah, STA13-N1WAKESCAN)")
    args = ap.parse_args(argv)
    authors = [a.strip() for a in args.controller_authors.split(",") if a.strip()]
    import time
    now = args.now if args.now is not None else int(time.time())
    try:
        findings = scan(args.db, now, authors)
    except sqlite3.Error as e:
        print("ERROR: %s" % e, file=sys.stderr)
        return 2
    for tid, alasan, umur in findings:
        sys.stdout.write("WAKE %s %s %d\n" % (tid, alasan, umur))
    return 0


if __name__ == "__main__":
    sys.exit(main())
