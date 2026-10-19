# -*- coding: utf-8 -*-
"""Sapuan sampel chat fleet untuk gerbang naturalisasi (NAT-S20).

Deterministik dan read-only. Mengunion 54 store pesan (DB utama + 53 DB profil),
memilih pesan asisten terbaru per store (default N=200), lalu menilai tiap sampel
dengan scanner resmi fleet `scan_ai_footprint.py` pada kanal yang sesuai sumber sesi.

Pemetaan kanal (kebijakan D-TA-05 / D-TA-07):
  webui|desktop|cli|telegram|discord|whatsapp|signal|slack|matrix -> chat (K1)
  kanban                                                          -> kanban (K5)
  cron                                                            -> notif (K4)
  subagent                                                        -> INTERNAL, dikecualikan

Keluaran:
  - stdout: baris CHECK n: PASS|FAIL|N/A - nama | detail, diakhiri satu baris VERDICT:
  - --json-out PATH: bukti mentah (angka nyata per store, rincian temuan per kode)
  - --report PATH   : laporan markdown (bisa dipakai verifier sebagai bahan uji ulang)

Ambang (blueprint langkah 20 + RT 5.2):
  A. ambang absolut 0: U+2014 (C-1), U+00B7 di luar blok D16 (C-2), emoji/ikon (C-3)
  B. ambang berat <=5%: sampel dengan indikator berat (VERDICT FAIL dari C-4..C-9)

Skrip ini TIDAK menulis ke DB mana pun (URI mode=ro) dan tidak mengirim pesan.

Guard timeout per-sampel (NAT-HIL-F, 02-09):
  Defect NAT-S20: satu pesan beracun (gsp-custodian id=292, backtracking eksponensial
  pola D16 di scanner v1.2.0) membekukan sapuan penuh tanpa batas. Sejak versi ini
  setiap pemanggilan scanner berjalan di SATU proses pekerja (spawn) yang dipantau
  induk dengan batas dinding --sample-timeout detik per sampel (default 15, rentang
  wajar 10-30). Sampel yang melewati batas: pekerja di-kill, sampel dicatat status
  TIMEOUT (msg_id + snippet di JSON), pekerja dihidupkan ulang, sapuan lanjut ke
  sampel berikutnya. Tanpa retry agar deterministik. Sampel TIMEOUT/SCAN_ERROR tidak
  pernah hilang diam-diam: dihitung sebagai FAIL konservatif lewat CHECK guard
  tersendiri sehingga vonis absolut ikut FAIL, dan dilaporkan terpisah. Loop baseline
  per-store yang dipakai verifier (batas 90 dtk/store, `timeout 90` eksternal) tetap
  berlaku: store dengan satu sampel beracun kini selesai dalam puluhan detik.
  Definisi ambang A dan B TIDAK diubah; angka pct_heavy tetap dihitung atas sampel
  yang berhasil dipindai (komparabel dengan run historis), ketidakjelasan sampel
  guard ditangani lewat CHECK guard khusus.
  Determinisme JSON: stempel waktu lahir/durasi hanya tercetak di stdout dan laporan,
  tidak lagi di JSON, dan urutan baris DB diberi pemecah seri `m.id desc`, sehingga
  dua run atas DB yang sama menghasilkan JSON byte-identik.
"""
import argparse
import json
import multiprocessing
import os
import sqlite3
import sys
import time

sys.dont_write_bytecode = True

HERE = os.path.dirname(os.path.abspath(__file__))
HOME = os.environ.get("LOCALAPPDATA") or os.path.expanduser("~")
HERMES = os.path.join(HOME, "hermes")

# --- locate scanner resmi fleet -------------------------------------------------
SCANNER_CANDIDATES = [
    os.path.join(HERMES, "skills", "gsp", "gsp-output-naturalization", "scripts", "scan_ai_footprint.py"),
    os.path.join(HERMES, "skills", "gsp", "gsp-output-naturalization", "scripts", "scan_ai_footprint.py"),
    r"C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-output-naturalization/scripts/scan_ai_footprint.py",
]

CHAT_SOURCES = {"webui", "desktop", "cli", "telegram", "discord", "whatsapp", "signal", "slack", "matrix", "email"}
KANBAN_SOURCES = {"kanban"}
NOTIF_SOURCES = {"cron"}
INTERNAL_SOURCES = {"subagent"}


def load_scanner():
    for p in SCANNER_CANDIDATES:
        if os.path.isfile(p):
            import importlib.util
            spec = importlib.util.spec_from_file_location("scan_ai_footprint", p)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, p
    raise SystemExit("scanner resmi tidak ditemukan di: " + " | ".join(SCANNER_CANDIDATES))


def channel_for_source(src):
    src = (src or "").lower()
    if src in CHAT_SOURCES:
        return "chat"
    if src in KANBAN_SOURCES:
        return "kanban"
    if src in NOTIF_SOURCES:
        return "notif"
    if src in INTERNAL_SOURCES:
        return None            # internal, tidak sampai ke user
    return "chat"              # sumber tak dikenal: perlakukan sebagai kanal terketat


def discover_stores():
    """(label, path, kind) untuk DB utama + seluruh DB profil."""
    stores = []
    main = os.path.join(HERMES, "state.db")
    if os.path.isfile(main):
        stores.append(("MAIN(default)", main, "main"))
    prof_root = os.path.join(HERMES, "profiles")
    if os.path.isdir(prof_root):
        for name in sorted(os.listdir(prof_root)):
            db = os.path.join(prof_root, name, "state.db")
            if os.path.isfile(db):
                stores.append((name, db, "profile"))
    return stores


def fetch_samples(db_path, n, min_chars, since=0.0, sess_since=None):
    """Ambil pesan asisten terbaru; kembalikan list dict(content, source, ts, id).

    sess_since: bila diisi, hanya pesan dari sesi yang DIMULAI (sessions.started_at)
    pada/after batas ini. Ini mengukur efektivitas gerbang pada agen yang benar-benar
    memuat kebijakan baru, bukan sesi lama yang lahir sebelum rollout."""
    uri = "file:%s?mode=ro" % db_path.replace("\\", "/").replace("?", "%3f")
    con = sqlite3.connect(uri, uri=True, timeout=20)
    con.row_factory = sqlite3.Row
    out, truncated_reason = [], None
    try:
        cur = con.cursor()
        have_sessions = cur.execute(
            "select 1 from sqlite_master where type='table' and name='sessions'").fetchone()
        q = ("select m.id as mid, m.content as content, m.timestamp as ts, "
             + ("s.source as source" if have_sessions else "'' as source")
             + " from messages m"
             + (" left join sessions s on s.id = m.session_id" if have_sessions else "")
             + " where m.role='assistant' and m.content is not null and length(trim(m.content)) >= ?"
             + (" and coalesce(m.timestamp,0) >= ?" if since else "")
             + (" and coalesce(s.started_at, 0) >= ?" if (sess_since and have_sessions) else "")
             + " order by coalesce(m.timestamp, 0) desc, m.id desc limit ?")
        params = [min_chars] + ([since] if since else []) + ([sess_since] if (sess_since and have_sessions) else []) + [n * 4]
        for row in cur.execute(q, params):
            ch = channel_for_source(row["source"])
            if ch is None:
                continue
            txt = row["content"]
            if len(out) >= n:
                break
            out.append({"content": txt, "source": (row["source"] or "?"), "channel": ch,
                        "ts": row["ts"], "id": row["mid"]})
        if len(out) < n:
            truncated_reason = "store hanya memuat %d pesan asisten >= %d karakter%s" % (
                len(out), min_chars, (" dan >= %s" % time.strftime("%Y-%m-%d %H:%M", time.localtime(since)) if since else ""))
    except sqlite3.Error as exc:
        truncated_reason = "sqlite error: %s" % exc
    finally:
        con.close()
    return out, truncated_reason


ABS_CODES = {"C-1": "U+2014 em dash", "C-2": "U+00B7 middle dot", "C-3": "emoji/ikon dekoratif"}


def _scan_worker(scanner_path, conn):
    """Entry proses pekerja (spawn): muat scanner resmi, layani permintaan berurutan.

    Protokol: terima (idx, text, channel, opts_dict) -> kirim ('ok', codes) atau
    ('error', pesan). Batas waktu per sampel ditegakkan oleh induk (SampleGuard);
    pekerja yang melampaui batas di-kill tanpa sempat membalas."""
    try:
        import importlib.util
        spec = importlib.util.spec_from_file_location("scan_ai_footprint", scanner_path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
    except Exception as exc:
        try:
            conn.send(("fatal", "gagal muat scanner: %s: %s" % (type(exc).__name__, exc)))
        except OSError:
            pass
        return
    while True:
        try:
            req = conn.recv()
        except (EOFError, OSError):
            break
        idx, text, channel, opts_dict = req
        try:
            doc = mod.extract_plain("sample_%d.md" % idx, text)
            res = mod.evaluate(doc, channel, argparse.Namespace(**opts_dict))
            codes = {}
            for st, nama, detail in res.rows:
                if st != "FAIL":
                    continue
                codes[mod._code_of(nama)] = (nama, detail)
            conn.send(("ok", codes))
        except Exception as exc:
            try:
                conn.send(("error", "%s: %s" % (type(exc).__name__, exc)))
            except OSError:
                break


class SampleGuard:
    """Pemanggilan scanner per-sampel dengan batas waktu dinding (NAT-HIL-F).

    Satu proses pekerja persisten melayani seluruh sampel. Bila satu sampel
    melampaui limit_sec, induk terminate pekerja, mengembalikan status TIMEOUT,
    lalu menghidupkan pekerja baru untuk melanjutkan. Tanpa retry: keputusan
    serba dinding jam pertama, sehingga hasil dua run atas data sama identik."""

    def __init__(self, scanner_path, opts_base, limit_sec):
        self.scanner_path = os.path.abspath(scanner_path)
        self.opts_base = opts_base
        self.limit = float(limit_sec)
        self.ctx = multiprocessing.get_context("spawn")
        self.proc = None
        self.conn = None
        self._restart()

    def _restart(self):
        if self.proc is not None:
            try:
                self.proc.terminate()
                self.proc.join(5)
            except Exception:
                pass
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
        parent_conn, child_conn = self.ctx.Pipe()
        self.proc = self.ctx.Process(target=_scan_worker,
                                     args=(self.scanner_path, child_conn),
                                     daemon=True)
        self.proc.start()
        child_conn.close()
        self.conn = parent_conn

    def scan(self, text, channel, idx):
        """Kembalikan (status, codes): 'ok' | 'TIMEOUT' | 'SCAN_ERROR'."""
        try:
            self.conn.send((idx, text, channel, vars(self.opts_base)))
        except OSError:
            self._restart()
            return "SCAN_ERROR", {}
        if not self.conn.poll(self.limit):
            self._restart()          # sampel beracun: kill + hidupkan ulang
            return "TIMEOUT", {}
        try:
            kind, payload = self.conn.recv()
        except (EOFError, OSError):
            self._restart()
            return "SCAN_ERROR", {}
        if kind == "ok":
            return "ok", payload
        self._restart()              # 'error' atau 'fatal': pekerja dianggap tak tepercaya
        return "SCAN_ERROR", {}

    def shutdown(self):
        if self.conn is not None:
            try:
                self.conn.close()
            except Exception:
                pass
        if self.proc is not None:
            try:
                self.proc.terminate()
                self.proc.join(5)
            except Exception:
                pass


def main(argv=None):
    ap = argparse.ArgumentParser(prog="scan_chat_sweep_20260902.py")
    ap.add_argument("--n", type=int, default=200, help="sampel per store (default 200)")
    ap.add_argument("--min-chars", type=int, default=40, help="panjang minimum pesan asisten")
    ap.add_argument("--stores", default="", help="filter prefix nama store, dipisah koma")
    ap.add_argument("--json-out", default="")
    ap.add_argument("--report", default="")
    ap.add_argument("--heavy-limit", type=float, default=5.0, help="ambang persen sampel berindikator berat")
    ap.add_argument("--since", default="", help="batas bawah jendela waktu, ISO 'YYYY-MM-DD[ HH:MM[:SS]]' atau epoch; hanya pesan >= batas yang dihitung")
    ap.add_argument("--window-label", default="", help="label jendela waktu untuk laporan (mis. baseline / pasca-gerbang)")
    ap.add_argument("--sessions-started-after", default="", help="sama format --since, tapi disaring ke sessions.started_at (hanya sesi yang lahir setelah batas)")
    ap.add_argument("--sample-timeout", type=float, default=15.0,
                    help="batas detik per pemanggilan scanner per sampel (NAT-HIL-F; default 15, wajar 10-30)")
    args = ap.parse_args(argv)

    mod, scanner_path = load_scanner()
    opts_base = argparse.Namespace(scan_code=False, require_marker=False,
                                   no_self_exclude=False, sosmed=False)

    since = 0.0
    def parse_when(val):
        if not val:
            return 0.0
        v = val.strip()
        if v.replace(".", "", 1).isdigit():
            return float(v)
        for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M", "%Y-%m-%d"):
            try:
                return time.mktime(time.strptime(v, fmt))
            except ValueError:
                continue
        raise SystemExit("batas waktu tidak dikenali: %s" % v)
    since = parse_when(args.since) or since
    sess_since = parse_when(args.sessions_started_after)
    window = args.window_label or (("sejak " + time.strftime("%Y-%m-%d %H:%M", time.localtime(since))) if since else "seluruh riwayat")
    if sess_since:
        window += " | hanya sesi lahir >= " + time.strftime("%Y-%m-%d %H:%M", time.localtime(sess_since))

    stores = discover_stores()
    if args.stores:
        pref = [p.strip() for p in args.stores.split(",") if p.strip()]
        stores = [s for s in stores if any(s[0].startswith(p) for p in pref)]

    per_store = []
    total_samples = 0
    abs_hits = {c: 0 for c in ABS_CODES}
    abs_examples = {c: [] for c in ABS_CODES}
    heavy_samples = 0
    chan_counts = {}
    total_timeouts = 0
    total_scan_errors = 0

    guard = SampleGuard(scanner_path, opts_base, args.sample_timeout)
    t0 = time.time()
    try:
        for label, path, kind in stores:
            samples, reason = fetch_samples(path, args.n, args.min_chars, since, sess_since)
            rec = {"store": label, "path": path, "kind": kind, "requested": args.n,
                   "scanned": len(samples), "reason_short": reason,
                   "abs_violations": 0, "heavy_violations": 0,
                   "timeout_samples": 0, "scan_error_samples": 0,
                   "guard_events": [],
                   "by_code": {}, "internal_skipped": 0}
            for i, s in enumerate(samples):
                chan_counts[s["channel"]] = chan_counts.get(s["channel"], 0) + 1
                status, codes = guard.scan(s["content"], s["channel"], i)
                if status != "ok":
                    key = "timeout_samples" if status == "TIMEOUT" else "scan_error_samples"
                    rec[key] += 1
                    if status == "TIMEOUT":
                        total_timeouts += 1
                    else:
                        total_scan_errors += 1
                    if len(rec["guard_events"]) < 20:
                        rec["guard_events"].append({
                            "status": status, "msg_id": s["id"], "source": s["source"],
                            "ts": s["ts"],
                            "snippet": s["content"][:160].replace("\n", " ")})
                    continue
                total_samples += 1
                heavy = {c: v for c, v in codes.items() if c not in ABS_CODES}
                for code in codes:
                    rec["by_code"][code] = rec["by_code"].get(code, 0) + 1
                    if code in abs_hits:
                        abs_hits[code] += 1
                        rec["abs_violations"] += 1
                        if len(abs_examples[code]) < 5:
                            abs_examples[code].append({"store": label, "source": s["source"],
                                                       "snippet": s["content"][:160].replace("\n", " ")})
                if heavy:
                    heavy_samples += 1
                    rec["heavy_violations"] += 1
            rec["by_code"] = dict(sorted(rec["by_code"].items()))
            per_store.append(rec)
    finally:
        guard.shutdown()

    dur = time.time() - t0
    pct_heavy = (100.0 * heavy_samples / total_samples) if total_samples else 0.0
    lines = []

    def emit(status, nama, detail=""):
        lines.append("CHECK %d: %s - %s%s" % (len(lines) + 1, status, nama,
                                              (" | " + detail) if detail else ""))

    emit("INFO", "scanner resmi", "%s v%s" % (scanner_path, getattr(mod, "__version__", "?")))
    emit("INFO", "jendela waktu", window)
    emit("INFO", "store dipindai", "%d store (utama %d, profil %d)" % (
        len(stores), sum(1 for s in stores if s[2] == "main"), sum(1 for s in stores if s[2] == "profile")))
    emit("INFO", "total sampel terukur", "%d pesan asisten; kanal: %s" % (total_samples, json.dumps(chan_counts, sort_keys=True)))
    short_stores = [r["store"] for r in per_store if r["reason_short"]]
    if short_stores:
        emit("INFO", "store di bawah N", "%d store (alasan teknis tercatat di JSON)" % len(short_stores))

    for code, desc in ABS_CODES.items():
        if total_samples == 0:
            emit("N/A", "ambang absolut %s %s" % (code, desc), "tidak ada sampel terbaca")
        elif abs_hits[code] == 0:
            emit("PASS", "ambang absolut %s %s = 0" % (code, desc), "0 temuan dari %d sampel" % total_samples)
        else:
            emit("FAIL", "ambang absolut %s %s = 0" % (code, desc), "%d temuan" % abs_hits[code])

    if total_samples == 0:
        emit("N/A", "ambang berat <= %.1f%%" % args.heavy_limit, "tidak ada sampel terbaca")
    elif pct_heavy <= args.heavy_limit:
        emit("PASS", "ambang berat <= %.1f%%" % args.heavy_limit, "%.2f%% (%d/%d)" % (pct_heavy, heavy_samples, total_samples))
    else:
        emit("FAIL", "ambang berat <= %.1f%%" % args.heavy_limit, "%.2f%% (%d/%d)" % (pct_heavy, heavy_samples, total_samples))

    # Guard NAT-HIL-F: sampel TIMEOUT/SCAN_ERROR = FAIL konservatif, bukan hilang.
    guard_bad = total_timeouts + total_scan_errors
    if guard_bad == 0 and total_samples == 0:
        emit("N/A", "guard timeout per-sampel (batas %.0f dtk)" % args.sample_timeout, "tidak ada sampel terbaca")
    elif guard_bad == 0:
        emit("PASS", "guard timeout per-sampel (batas %.0f dtk)" % args.sample_timeout,
             "0 TIMEOUT/SCAN_ERROR dari %d sampel attempted" % (total_samples + guard_bad))
    else:
        emit("FAIL", "guard timeout per-sampel (batas %.0f dtk)" % args.sample_timeout,
             "%d TIMEOUT + %d SCAN_ERROR dihitung FAIL konservatif; msg_id rincian di JSON"
             % (total_timeouts, total_scan_errors))

    worst = sorted(per_store, key=lambda r: -(r["abs_violations"] + r["heavy_violations"]))[:8]
    emit("INFO", "store dengan temuan tertinggi",
         "; ".join("%s(abs %d, berat %d)" % (w["store"], w["abs_violations"], w["heavy_violations"]) for w in worst))

    fails = [l for l in lines if ": FAIL -" in l]
    verdict = "FAIL" if fails else ("NEEDS_REVIEW" if total_samples == 0 else "PASS")
    if verdict == "NEEDS_REVIEW":
        lines.append("VERDICT: NEEDS_REVIEW")
    else:
        lines.append("VERDICT: %s" % verdict)

    payload = {"generated_at": time.strftime("%Y-%m-%d %H:%M:%S"), "window": window,
               "scanner": scanner_path, "scanner_version": getattr(mod, "__version__", "?"),
               "n_requested": args.n, "min_chars": args.min_chars,
               "sample_timeout_sec": args.sample_timeout,
               "stores_total": len(stores), "samples_total": total_samples,
               "timeout_samples": total_timeouts, "scan_error_samples": total_scan_errors,
               "channel_counts": dict(sorted(chan_counts.items())),
               "abs_hits": abs_hits, "abs_examples": abs_examples,
               "heavy_samples": heavy_samples, "heavy_pct": round(pct_heavy, 2),
               "heavy_limit_pct": args.heavy_limit,
               "duration_sec": round(dur, 1), "verdict": verdict,
               "per_store": per_store}

    if args.json_out:
        # Determinisme JSON (NAT-HIL-F): nilai volatil (stempel lahir, durasi) hanya
        # hidup di memori/laporan; JSON berisi angka hasil ukur saja agar dua run
        # atas DB yang sama byte-identik.
        jpayload = {k: v for k, v in payload.items()
                    if k not in ("generated_at", "duration_sec")}
        with open(args.json_out, "w", encoding="utf-8", newline="\n") as fh:
            json.dump(jpayload, fh, ensure_ascii=False, indent=1)
    if args.report:
        write_report(args.report, payload, lines)

    sys.stdout.write("\n".join(lines) + "\n")
    return 0 if verdict == "PASS" else (1 if verdict == "FAIL" else 2)


def write_report(path, p, lines):
    L = []
    L.append("# Sapuan Sampel Chat Fleet (NAT-S20)")
    L.append("")
    L.append("- Tanggal: %s" % p["generated_at"])
    L.append("- Scanner: `%s` v%s" % (p["scanner"], p["scanner_version"]))
    L.append("- Skrip: `workspace/gsp-hermes/scripts/scan_chat_sweep_20260902.py` (read-only, URI mode=ro)")
    L.append("- Jendela waktu: %s" % p["window"])
    L.append("- Store dipindai: %d (DB utama + DB profil)" % p["stores_total"])
    L.append("- Sampel terukur: %d pesan asisten; distribusi kanal: %s" % (p["samples_total"], json.dumps(p["channel_counts"], sort_keys=True)))
    L.append("- Guard per-sampel (NAT-HIL-F): batas %s detik/sampel; TIMEOUT %d, SCAN_ERROR %d (dihitung FAIL konservatif, msg_id di JSON)"
             % (p["sample_timeout_sec"], p["timeout_samples"], p["scan_error_samples"]))
    L.append("- Durasi: %s detik" % p["duration_sec"])
    L.append("")
    L.append("## 1. Vonis per ambang")
    L.append("")
    L.append("```")
    L.extend(lines)
    L.append("```")
    L.append("")
    L.append("## 2. Temuan absolut per kode")
    L.append("")
    L.append("| Kode | Deskripsi | Temuan |")
    L.append("|---|---|---|")
    for code, desc in ABS_CODES.items():
        L.append("| %s | %s | %d |" % (code, desc, p["abs_hits"][code]))
    L.append("")
    if p["abs_examples"]:
        L.append("## 3. Contoh temuan absolut (maks 5 per kode)")
        L.append("")
        for code, exs in p["abs_examples"].items():
            if not exs:
                continue
            L.append("### %s" % code)
            for e in exs:
                L.append("- `%s` (%s): %s" % (e["store"], e["source"], e["snippet"]))
            L.append("")
    L.append("## 4. Angka per store")
    L.append("")
    L.append("| Store | Diminta | Terukur | Absolut | Berat | TIMEOUT | SCAN_ERROR | Alasan kurang dari N |")
    L.append("|---|---|---|---|---|---|---|---|")
    for r in p["per_store"]:
        L.append("| %s | %d | %d | %d | %d | %d | %d | %s |" % (r["store"], r["requested"], r["scanned"],
                                                                 r["abs_violations"], r["heavy_violations"],
                                                                 r["timeout_samples"], r["scan_error_samples"],
                                                                 r["reason_short"] or "-"))
    L.append("")
    evs = [(r["store"], e) for r in p["per_store"] for e in r["guard_events"]]
    if evs:
        L.append("## 4a. Sampel kena guard (maks 20 per store)")
        L.append("")
        for store, e in evs:
            L.append("- `%s` msg_id=%s (%s, %s): %s" % (store, e["msg_id"], e["status"], e["source"], e["snippet"]))
        L.append("")
    L.append("## 5. Batas klaim (D-TA-10)")
    L.append("")
    L.append("Angka berlaku untuk sampel dan tanggal run ini, bukan klaim fleet-wide nol. "
             "Sesi subagent dikecualikan karena bukan keluaran yang dibaca user; "
             "ringkasan dan komentar kanban ikut disaring sebagai prosa sesuai D-TA-07.")
    L.append("")
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        fh.write("\n".join(L))


if __name__ == "__main__":
    sys.exit(main())
