#!/usr/bin/env python3
"""gsp_deleg_watch.py - gerbang rantai delegasi era PMODE-DELEG-1010 (v1).

Tiga subperintah, satu berkas, stdlib-only, deterministik:

  dead [--dry-run]        Safety net MATI-JEMBATAN: jalankan deteksi PID kernel
                          (release_stale_claims + detect_crashed_workers) pada
                          board nyata. Selama bridge hidup, dispatcher sudah
                          memanggil ini tiap tick; cron ini menutup lubang saat
                          proses bridge/gateway mati sehingga reclaim tidak
                          berhenti. Vonis MATI hanya fakta biner PID hilang
                          (keputusan D-A); gap heartbeat TIDAK pernah jadi
                          criterion reclaim.
  claim TID [--window 60] GERBANG-KLAIM controller: setelah menulis kartu
                          delegasi, buktikan kartu diklaim dalam jendela.
                          CLAIMED (ada run+pid) exit 0; LOST exit 1 -> mediasi
                          M1, dilarang tutup giliran tanpa vonis.
  ack TID                 GERBANG-ACK sisi baca: apakah author controller sudah
                          meng-ACK hasil (komentar bertoken ACK setelah event
                          completed terakhir). ACKED exit 0; PENDING exit 2;
                          NO-RESULT exit 3.
  ack-post TID [--by A]   Tulis komentar ACK standar atas nama A.

Postur tulis: hanya dua jalur tulis, keduanya mekanisme kernel yang sudah ada
(add_comment) atau fungsi reclaim kernel yang sama dengan dispatcher (CAS +
write_txn). Tidak ada skema pesan baru (keputusan D-C).

Prasyarat jalan (terukur SYS-NET-RT-PAPAN-1018, 18-10; kontrak
docs/2026-10-18_sys-net-rt-papan-1018/system_change.md):
  1. Dependensi: impor hermes_cli.kanban_db menarik hermes_cli.config yang butuh
     PyYAML. Dari interpreter bersih pakai:
       uv run --python 3.11 --no-project --with pyyaml python <skrip> ...
     (venv hermes-agent sudah punya yaml; interpreter lain -> ModuleNotFoundError.)
  2. Jalur tulis (ack-post; juga jejak PARKED pada wait-ack) menembus write_txn
     kernel yang fail-closed bila env HERMES_DELEGATED_CHILD_CONTEXT terpasang.
     Dari DALAM run papan marker bisa ikut terekspor ke shell worker lewat
     snapshot bash bersama (kanal kebocoran kelas DEFECT-RT-PAPAN-1018). Bila
     pemanggil adalah worker pemilik kartu (HERMES_KANBAN_TASK terisi dan sama
     dengan target), sah melepas marker untuk panggilan ini saja:
       env -u HERMES_DELEGATED_CHILD_CONTEXT <perintah>
     Anak delegate_task sungguhan tidak melihat HERMES_KANBAN_TASK (di-scrub oleh
     _make_run_env) -> panggilan tetap gagal tertutup; DILARANG memakai env -u
     ini dari dalam subagen.
  3. wait-ack dari terminal foreground sesi papan/cron selalu terpotong plafon
     tool (< plafon skrip): jalankan background lalu poll; PARKED exit 4 sah
     (preseden E1SPEC/E1PURGE 14-10).
"""
import argparse
import os
import sys
import time
from pathlib import Path

sys.path.insert(0, r'C:/Users/TRIAL/AppData/Local/hermes/hermes-agent')
from hermes_cli import kanban_db as kb  # noqa: E402

ACK_TOKEN = 'RANTAI-ACK'
GRACE_LOOKAHEAD_S = 420  # tick 300 + margin 60 + grace 30 kernel -
# sengaja > tick interval agar jendela kernel tak pernah terlewat


def _conn():
    # DELEG_WATCH_DB: override path utk fixture merah-hijau (misi MIKROVERIF-DISP-1011);
    # produksi tidak memasang env ini -> perilaku tak berubah.
    _db = os.environ.get('DELEG_WATCH_DB')
    return kb.connect(Path(_db)) if _db else kb.connect()


def cmd_dead(args):
    conn = _conn()
    try:
        if args.dry_run:
            rows = conn.execute(
                "SELECT id, worker_pid, started_at FROM tasks "
                "WHERE status='running' AND worker_pid IS NOT NULL").fetchall()
            n_dead = sum(1 for r in rows if not kb._pid_alive(r['worker_pid']))
            print(f"DRY: running={len(rows)} pid-hilang={n_dead}")
            return 0
        # rute-4c: enforcer independen. Dispatcher lama (proses hidup
        # pra-patch; pengukur: claim lock DESKTOP-BR2DLT9:13168 = gateway
        # agentriset sejak 07-10) tidak memuat grace notice. Cron ini proses
        # BARU tiap tick -> kode baru selalu jalan. Karena tick 5 mnt bisa
        # melewatkan jendela grace 30 dtk kernel, cron memakai LOOKAHEAD:
        # notice terbit saat sisa <= TICK+MARGIN+GRACE (kanal yang sama:
        # komentar dispatcher + event terminal_grace, dedup per-run). Kill
        # tetap lewat enforce_max_runtime kernel (CAS anti-ganda).
        try:
            now_i = int(time.time())
            for row in conn.execute(
                    "SELECT t.id, COALESCE(r.started_at, t.started_at) st, "
                    "t.max_runtime_seconds lim FROM tasks t "
                    "LEFT JOIN task_runs r ON r.id = t.current_run_id "
                    "WHERE t.status='running' AND t.worker_pid IS NOT NULL "
                    "AND t.max_runtime_seconds IS NOT NULL").fetchall():
                if not row['st']:
                    continue
                sisa = int(row['lim']) - (now_i - int(row['st']))
                if 0 < sisa <= GRACE_LOOKAHEAD_S:
                    sudah = conn.execute(
                        "SELECT 1 FROM task_events WHERE task_id=? AND "
                        "kind='terminal_grace' AND created_at>=? LIMIT 1",
                        (row['id'], int(row['st']))).fetchone()
                    if not sudah:
                        try:
                            kb.add_comment(
                                conn, row['id'], 'dispatcher',
                                f'TERMINAL GRACE: run menabrak cap runtime '
                                f'({row["lim"]}s) dalam ~{sisa}s. Hentikan '
                                f'pekerjaan baru; tulis hasil terbaik '
                                f'(complete parsial / block dengan catatan '
                                f'resume) agar percobaan berikut lanjut dari '
                                f'checkpoint, bukan mati tanpa laporan.')
                            kb._append_event(conn, row['id'],
                                             'terminal_grace',
                                             {'remaining_seconds': sisa,
                                              'limit_seconds': int(row['lim']),
                                              'emitter': 'rantai-watch'})
                            print(f'GRACE {row["id"]} sisa={sisa}s')
                        except Exception as e:
                            print(f'GRACE-ERR {row["id"]}: {e}')
            to_new = kb.enforce_max_runtime(conn)
            for t in to_new:
                print(f'TIMED-OUT {t} (enforcer cron)')
        except Exception as e:
            print(f'ENFORCE-ERR {e}')
        expired_n = kb.release_stale_claims(conn)
        crashed = kb.detect_crashed_workers(conn)
        # release_stale_claims mengembalikan HITUNGAN (kontrak kernel); id
        # tergembalik dibaca dari event 'reclaimed' 60 dtk terakhir.
        expired = [row['task_id'] for row in conn.execute(
            "SELECT DISTINCT task_id FROM task_events WHERE kind="
            "'reclaimed' AND created_at >= ?", (int(time.time()) - 60,))]
        print(f'RECLAIMED count={expired_n} ids={expired}')
        for t in crashed:
            print(f'CRASHED {t} (pid-hilang)')
        auto = getattr(kb.detect_crashed_workers, '_last_auto_blocked', [])
        for t in auto:
            print(f'AUTO-BLOCKED {t}')
        rl = getattr(kb.detect_crashed_workers, '_last_rate_limited', [])
        for t in rl:
            print(f'QUOTA-DEFERRED {t}')
        # PUTUSAN USER 10-10 (direktif tersurat): rantai mati TIDAK menunggu
        # keputusan user - setiap kematian dirutekan balik ke controller
        # PEMBER TUGAS (created_by kartu) lewat komentar papan ber-token,
        # supaya wake-scan membangunkan controller itu untuk mediasi M4
        # (split/reassign/checkpoint-resume). User hanya menerima laporan
        # dari controller, dan hanya untuk ambang wewenang (mis. kredit).
        routed = 0
        dead_items = ([(x, 'crashed') for x in crashed]
                      + [(x, 'claim-expired') for x in expired]
                      + [(x, 'auto-blocked') for x in auto]
                      + [(x, 'quota-deferred') for x in rl])
        for t, klass in dead_items:
            row = conn.execute(
                "SELECT created_by, assignee, title FROM tasks WHERE id=?",
                (t,)).fetchone()
            if row is None:
                continue
            owner = (row['created_by'] or 'default').strip()
            tok = f'RANTAI-MATI {klass}'
            seen = conn.execute(
                "SELECT 1 FROM task_comments WHERE task_id=? AND author="
                "'rantai-watch' AND body LIKE ? AND created_at >= "
                "(SELECT COALESCE(MAX(ended_at),0) FROM task_runs WHERE "
                "task_id=?)", (t, f'%{tok}%', t)).fetchone()
            if seen:
                continue
            try:
                kb.add_comment(
                    conn, t, 'rantai-watch',
                    f'{tok}: run worker berhenti ({klass}). Rantai '
                    f'DIKEMBALIKAN ke controller penugasan @{owner} untuk '
                    f'mediasi M4 (lanjut checkpoint / split / reassign). '
                    f'DILARANG menggantung menunggu keputusan user; user '
                    f'hanya dilapori oleh @{owner} bila menyentuh ambang '
                    f'wewenang (mis. kredit provider).')
                print(f'ROUTED {t} -> @{owner} ({klass})')
                routed += 1
            except Exception as e:
                print(f'ROUTE-FAIL {t}: {e}')
        print(f'SUMMARY expired={len(expired)} crashed={len(crashed)} '
              f'routed={routed}')
        return 0
    finally:
        conn.close()


def cmd_claim(args):
    deadline = time.time() + args.window
    tid = args.task_id
    while True:
        conn = _conn()
        try:
            row = conn.execute(
                "SELECT status, worker_pid, current_run_id FROM tasks "
                "WHERE id=?", (tid,)).fetchone()
        finally:
            conn.close()
        if row is None:
            print(f'LOST {tid} (kartu tidak ada di board)')
            return 1
        if row['status'] == 'running' and row['current_run_id']:
            print(f'CLAIMED {tid} pid={row["worker_pid"]} run={row["current_run_id"]}')
            return 0
        if row['status'] in ('done', 'archived'):
            print(f'CLAIMED {tid} (sudah {row["status"]} sebelum jendela habis)')
            return 0
        if time.time() >= deadline:
            print(f'LOST {tid} status={row["status"]} dalam {args.window}s '
                  '-> mediasi M1: cek dispatcher hidup, assignee terdaftar, '
                  'rantai hulu menahan?')
            return 1
        time.sleep(args.interval)


def _owner(conn, tid):
    """created_by kartu = sasaran serah terima (TARGET-SERAH-Terima 11-10)."""
    row = conn.execute("SELECT created_by FROM tasks WHERE id=?", (tid,)).fetchone()
    if row is None:
        return None
    return (row['created_by'] or 'default').strip()


def cmd_ack(args):
    conn = _conn()
    try:
        owner = _owner(conn, args.task_id)
        if owner is None:
            print(f'NOT-FOUND {args.task_id}')
            return 3
        author = args.author or owner
        comp = conn.execute(
            "SELECT created_at FROM task_events WHERE task_id=? AND kind IN "
            "('completed','blocked') ORDER BY id DESC LIMIT 1",
            (args.task_id,)).fetchone()
        if comp is None:
            print(f'NO-RESULT {args.task_id} (belum ada transisi terminal)')
            return 3
        # Bandingkan antar-waktu, BUKAN antar-id: task_comments.id dan
        # task_events.id adalah ruang ID berbeda (temuan uji loop 10-10).
        # TARGET-SERAH-Terima 11-10: ACK sah = author==created_by ATAU ber-tag PROXY.
        ack = conn.execute(
            "SELECT author, body FROM task_comments WHERE task_id=? "
            "AND body LIKE ? AND created_at >= ? ORDER BY id DESC LIMIT 1",
            (args.task_id, f'%{ACK_TOKEN}%', comp['created_at'])).fetchone()
        if ack and ack['author'] == owner:
            print(f'ACKED {args.task_id} oleh {ack["author"]} (owner)')
            return 0
        if ack and 'PROXY-ACK' in (ack['body'] or ''):
            print(f'PROXY-ACKED {args.task_id} oleh {ack["author"]} '
                  f'(bukan owner @{owner}) - owner WAJIB dilanjari/dilaporkan')
            return 0
        if ack:
            print(f'MISMATCH {args.task_id}: ACK dibayar {ack["author"]} tanpa tag '
                  f'PROXY-ACK; owner = @{owner}. Bayar ulang via ack-post --proxy '
                  f'atau tunggu owner.')
            return 2
        print(f'PENDING {args.task_id} (hasil terminal, belum di-ACK owner @{owner})')
        return 2
    finally:
        conn.close()


def cmd_ack_post(args):
    conn = _conn()
    try:
        owner = _owner(conn, args.task_id)
        if owner is None:
            print(f'NOT-FOUND {args.task_id}')
            return 3
        by = args.by or os.environ.get('HERMES_PROFILE', 'default')
        tag = ''
        if by != owner:
            if not args.proxy:
                print(f'REFUSED {args.task_id}: kamu ({by}) BUKAN penugas '
                      f'(owner @{owner}). Serah terima wajib ke penugas '
                      '(TARGET-SERAH-Terima 11-10). Kalau kamu memang '
                      'pembayar proxy (wake/mediasi), ulangi dengan --proxy.')
                return 5
            tag = f' [PROXY-ACK oleh {by}; owner @{owner} perlu vonis akhir]'
        cid = kb.add_comment(conn, args.task_id, by,
                             f'{ACK_TOKEN}: laporan diterima controller, '
                             'rantai tersambung.' + tag + ' ' + (args.note or ''))
        print(('PROXY-' if tag else '') + f'ACKED {args.task_id} (comment {cid} oleh {by}, owner @{owner})')
        return 0
    finally:
        conn.close()


def cmd_wait_ack(args):
    """GERBANG-ACK sisi worker (protokol wajib PMODE-DELEG-1010 rute-4,
    direktif user 10-10): DILARANG complete-then-wait - kernel mengakhiri run
    seketika saat transisi completed mendarat (bukti papan 10-10: panggilan
    wait-ack pasca-complete tercatat tanpa hasil, run mati di detik completed).
    Protokol benar: LAPOR (komentar token) -> wait-ack -> baru complete.
    Poll komentar RANTAI-ACK setelah anchor LAPOR-SELESAI; vonis dicetak:
    ACKED (exit 0, worker lanjut complete), PARKED (exit 4, plafon habis,
    jejak ditulis - complete dengan prefix PARKED dan wake-scan done-unacked
    menutup sisanya)."""
    tid = args.task_id
    deadline = time.time() + args.timeout
    while True:
        conn = _conn()
        try:
            anchor = conn.execute(
                "SELECT MAX(created_at) m FROM task_comments WHERE task_id=? "
                "AND body LIKE '%LAPOR-SELESAI%'", (tid,)).fetchone()['m']
            if anchor is None:
                print(f'NO-REPORT {tid} (belum ada komentar LAPOR-SELESAI - '
                      'urutan protokol: tulis artefak, komentar LAPOR-SELESAI, '
                      'baru wait-ack, lalu complete)')
                return 3
            owner = _owner(conn, tid) or 'default'
            ack = conn.execute(
                "SELECT author, body FROM task_comments WHERE task_id=? AND body LIKE ? "
                "AND created_at >= ? ORDER BY id DESC LIMIT 1",
                (tid, f'%{ACK_TOKEN}%', anchor)).fetchone()
            if ack and ack['author'] == owner:
                print(f'ACKED {tid} oleh {ack["author"]} (owner/penugas) - '
                      'laporan diterima, boleh kanban_complete dan berhenti')
                return 0
            if ack and 'PROXY-ACK' in (ack['body'] or ''):
                print(f'ACKED {tid} oleh {ack["author"]} PROXY-ACK (owner @{owner} '
                      'belum vonis akhir) - complete dengan menyebut proxy di LAPOR')
                return 0
            if ack:
                print(f'IGNORED-ACK {tid}: RANTAI-ACK dari {ack["author"]} bukan '
                      f'penugas @{owner} dan tanpa tag PROXY-ACK - lanjut menunggu')
            if time.time() >= deadline:
                try:
                    kb.add_comment(
                        conn, tid, os.environ.get('HERMES_PROFILE', 'worker'),
                        f'PARKED: LAPOR-SELESAI sudah terbit tetapi belum '
                        f'di-ACK controller dalam {args.timeout}s. Complete '
                        f'dengan prefix PARKED; wake-scan done-unacked akan '
                        f'membangunkan controller untuk mediasi. Bukan '
                        f'kegagalan kerja.')
                    print(f'PARKED {tid} (plafon {args.timeout}s habis, jejak '
                          'ditulis - complete dengan prefix PARKED)')
                    return 4
                except Exception as e:
                    print(f'PARK-FAIL {tid}: {e}')
                    return 5
        finally:
            conn.close()
        time.sleep(args.interval)


def main():
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    sub = ap.add_subparsers(dest='cmd', required=True)
    d = sub.add_parser('dead'); d.add_argument('--dry-run', action='store_true')
    d.set_defaults(fn=cmd_dead)
    c = sub.add_parser('claim'); c.add_argument('task_id')
    c.add_argument('--window', type=int, default=60); c.add_argument('--interval', type=int, default=5)
    c.set_defaults(fn=cmd_claim)
    a = sub.add_parser('ack'); a.add_argument('task_id')
    a.add_argument('--author', default=None); a.set_defaults(fn=cmd_ack)
    w = sub.add_parser('wait-ack'); w.add_argument('task_id')
    w.add_argument('--timeout', type=int, default=900)
    w.add_argument('--interval', type=int, default=10)
    w.set_defaults(fn=cmd_wait_ack)
    p = sub.add_parser('ack-post'); p.add_argument('task_id')
    p.add_argument('--by', default=None); p.add_argument('--note', default=''); p.add_argument('--proxy', action='store_true', help='bayar ACK utk kartu milik controller lain (wajib tag PROXY-ACK)')
    p.set_defaults(fn=cmd_ack_post)
    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == '__main__':
    main()
