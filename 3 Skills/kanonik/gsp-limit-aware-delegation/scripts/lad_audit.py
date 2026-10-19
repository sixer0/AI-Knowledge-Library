#!/usr/bin/env python3
"""lad_audit.py -- guard anti-mundur delegasi Limit-Aware (LAD, kebijakan 02-09-2026).

Spesifikasi: pasal C.5 kontrak docs/2026-09-02-limit-aware-delegation.
Deterministik: hanya stdlib + CLI hermes. Mode kedua `--probe` (D-LAD-05)
membaca kondisi concurrency live dari API HQ; jalur itu butuh jaringan,
sisanya tetap offline.

Perilaku (nomor butir mengikuti C.5):
1. Argumen: --since <iso-ts> (marker deploy yang dicatat controller di
   kontrak; WAJIB eksplisit agar tidak ada ambang diam-diam), --board
   (default default), --json-out opsional, --report-window-jam opsional.
2. Ambil `hermes kanban --board <board> list --archived --json`; untuk
   SETIAP kartu ber-assignee dengan created_at >= since:
   - CHECK blok: string literal `LIMIT-AWARE` muncul di body ATAU komentar.
   - CHECK cap: angka iterasi dalam blok == agent.max_turns config profil
     target saat-itu (config tidak terbaca = NEEDS_REVIEW, bukan FAIL).
   - CHECK estimasi: jejak `ESTIMASI:` ada, ATAU flag interaktif eksplisit
     (`interaktif`) disebut di body.
3. CHECK kematian senyap: run ber-outcome/status crash|gave_up|timeout pada
   kartu pasca-marker wajib disertai komentar memuat string literal
   `partial-handoff`; tidak ada = VIOLASI (FAIL).
4. CHECK rantai: sufiks judul `(lanjutan N/M)` dengan N > 3 atau M > 3 =
   VIOLASI batas mata (D-TA-06).
5. Keluaran: baris `CHECK n: PASS|FAIL|NEEDS_REVIEW - nama` + satu baris
   `VERDICT:` akhir; laporan timestamped ditulis ke folder kontrak.
   Exit code 0 hanya bila tidak ada FAIL.
6. Sumber kebenaran pola HANYA string literal `LIMIT-AWARE` dan
   `partial-handoff` (D-TA-13); sinonim tidak dihitung.
7. Mode probe (`--probe`, D-LAD-05): sebelum gelombang paralel dilepas,
   baca (a) kedalaman antrean AgentRequest queued+approved+running dan
   (b) rasio failed-timeout dispatch jendela terakhir (--window-min,
   default 15) dari API HQ; keluaran baris `PROBE: SEHAT|TEKANAN|UNKNOWN`
   + angka mentah. Exit 0=SEHAT, 1=TEKANAN, 2=UNKNOWN. Fail-safe: nilai
   gelombang boleh naik di atas statis 5 per misi tanpa batas per jenis HANYA saat
   SEHAT. Secret INTERNAL_API_SECRET dibaca dari env lalu config
   gsp-datacenter/.env, tidak pernah di-hardcode. `--fixture F.json`
   mengganti sumber HQ dengan berkas JSON (uji sintetis, bukan live).

Jendela laporan (bukti detector tidak buta): kartu ber-assignee dengan
created_at dalam [since - report-window, since) dilaporkan sebagai
NEEDS_REVIEW tanpa memblokir; daftar lengkap (id, judul, epoch, lokal)
masuk laporan kontrak + --json-out. Default jendela 168 jam (7 hari).
"""

import argparse
import datetime as dt
import json
import os
import re
import ssl
import subprocess
import sys
import urllib.request
from pathlib import Path

PATTERN_BLOCK = "LIMIT-AWARE"        # satu-satunya penanda blok sah (D-TA-13)
PATTERN_HANDOFF = "partial-handoff"  # satu-satunya penanda tutup parsial sah
FALLBACK_CAP = 500
DEAD_STATES = ("crash", "gave_up", "timeout")
CHAIN_RE = re.compile(r"\(lanjutan\s+(\d+)\s*/\s*(\d+)\)")
MAX_CHAIN = 3
DEFAULT_REPORT_WINDOW_JAM = 168
GLOBAL_CONFIG_CANDIDATES = (
    Path(os.environ.get("LOCALAPPDATA", "")) / "hermes" / "config.yaml",
    Path.home() / ".hermes" / "config.yaml",
)

# Regex angka iterasi blok: baris wajib memuat kata 'iterasi' supaya baris
# lain (mis. FORMAT LAPORAN yang menyebut SISA_KERJA) tidak ikut tertangkap.
CAP_PATTERNS = (
    re.compile(r"ANGGARAN.*?(\d+)\s*iterasi"),
    re.compile(r"Anggaran agen ini:\s*(\d+)\s*iterasi"),
    re.compile(r"(\d+)\s*iterasi\s+tool"),
)


def profiles_dir():
    la = os.environ.get("LOCALAPPDATA")
    if la:
        return Path(la) / "hermes" / "profiles"
    return Path.home() / "AppData" / "Local" / "hermes" / "profiles"


def parse_iso(s):
    """ISO-8601 -> epoch detik. Naive dianggap waktu lokal mesin."""
    try:
        d = dt.datetime.fromisoformat(s)
    except ValueError:
        raise SystemExit("ERROR: --since '%s' bukan ISO-8601 sah "
                         "(contoh: 2026-09-02T15:00 atau 2026-09-02T15:00+07:00)" % s)
    if d.tzinfo is None:
        d = d.astimezone()
    return int(d.timestamp())


_cap_cache = {}


def cap_for(assignee):
    """agent.max_turns profil target saat-itu. Return (cap|None, peringatan|None)."""
    if assignee in _cap_cache:
        return _cap_cache[assignee]
    res = (None, None)
    cfg = profiles_dir() / assignee / "config.yaml" if assignee else None
    if cfg and cfg.exists():
        try:
            with open(cfg, encoding="utf-8") as fh:
                for line in fh:
                    m = re.match(r"\s*max_turns:\s*(\d+)", line)
                    if m:
                        res = (int(m.group(1)), None)
                        break
                else:
                    res = (None, "config terbaca tapi tidak memuat agent.max_turns")
        except OSError as exc:
            res = (None, "config error: %s" % exc)
    elif cfg:
        res = (None, "config tidak ditemukan: %s" % cfg)
    else:
        res = (None, "assignee kosong")
    _cap_cache[assignee] = res
    return res


def global_default_cap():
    """agent.max_turns global (untuk pesan; TIDAK dipakai sebagai pembanding)."""
    for cfg in GLOBAL_CONFIG_CANDIDATES:
        try:
            with open(cfg, encoding="utf-8") as fh:
                for line in fh:
                    m = re.match(r"\s*max_turns:\s*(\d+)", line)
                    if m:
                        return int(m.group(1))
        except OSError:
            continue
    return None


def run_list(board):
    cmd = ["hermes", "kanban", "--board", board, "list", "--archived", "--json"]
    proc = subprocess.run(cmd, capture_output=True)
    if proc.returncode != 0:
        raise SystemExit("ERROR: `%s` gagal (exit %d): %s" % (
            " ".join(cmd), proc.returncode,
            proc.stderr.decode("utf-8", "replace").strip()[:400]))
    return json.loads(proc.stdout.decode("utf-8", "replace"))


def show_card(board, task_id, timeout=60):
    """Detail satu kartu (komentar + runs) via CLI; None bila gagal."""
    cmd = ["hermes", "kanban", "--board", board, "show", task_id, "--json"]
    try:
        proc = subprocess.run(cmd, capture_output=True, timeout=timeout)
    except (subprocess.TimeoutExpired, OSError):
        return None
    if proc.returncode != 0:
        return None
    try:
        return json.loads(proc.stdout.decode("utf-8", "replace"))
    except json.JSONDecodeError:
        return None


def extract_cap_number(text):
    for rx in CAP_PATTERNS:
        for line in text.splitlines():
            if "iterasi" not in line:
                continue
            m = rx.search(line)
            if m:
                return int(m.group(1))
    return None


def fmt_local(epoch):
    return dt.datetime.fromtimestamp(epoch).strftime("%Y-%m-%d %H:%M:%S")


# ---------------------------------------------------------------------------
# SUBMODUL PROBE concurrency dinamis (D-LAD-05)
# Subperintah: python lad_audit.py --probe [--fixture F.json] [--window-min 15]
# Keluaran: baris CHECK n: PASS|FAIL|NEEDS_REVIEW - nama, lalu baris PROBE:
# dan VERDICT:. Exit code: 0=SEHAT, 1=TEKANAN, 2=UNKNOWN (fail-safe: hanya
# SEHAT yang mengizinkan naik di atas statis 5 per misi tanpa batas per jenis).
# Sumber angka: API HQ (dispatch-kpi untuk kedalaman antrean penuh; requests
# tanpa light=1 untuk jendela waktu -- light memanggang kolom error/finishedAt
# yang justru dibutuhkan rasio failed-timeout, terbukti uji live 02-09).
# Secret INTERNAL_API_SECRET dibaca dari env lalu config gsp-datacenter/.env;
# tidak pernah dicetak, tidak pernah di-hardcode.
# ---------------------------------------------------------------------------

HQ_URL = os.environ.get("GSP_HQ_URL", "https://localhost:9011")
DC_ENV = r"C:/Users/TRIAL/gsp-datacenter/.env"
TAKE_MAX = 200            # kap endpoint /api/brahma/requests
QUEUE_SEHAT_MAX = 4       # queued+approved+running <= 4 -> kandidat SEHAT
QUEUE_TEKANAN_MIN = 10    # >= 10 -> TEKANAN langsung
RATIO_SEHAT_MAX = 0.10    # rasio failed-timeout <= 0.10 -> kandidat SEHAT
RATIO_TEKANAN_MIN = 0.25  # >= 0.25 -> TEKANAN; pita tengah -> TEKANAN (fail-safe)
TIMEOUT_RE = re.compile(r"timeout|timed.?out|tidak mencapai status terminal", re.I)
TERMINAL = ("done", "failed")


def _secret():
    s = (os.environ.get("INTERNAL_API_SECRET") or "").strip()
    if s:
        return s, "env"
    try:
        txt = open(DC_ENV, encoding="utf-8", errors="replace").read()
        m = re.search(r"(?m)^\s*INTERNAL_API_SECRET\s*=\s*(.+?)\s*$", txt)
        if m:
            v = m.group(1).strip().strip('"').strip("'")
            if v:
                return v, "gsp-datacenter/.env"
    except OSError:
        pass
    return None, None


def _hq_get(path, sec, timeout=12):
    ctx = ssl.create_default_context()
    ctx.check_hostname = False
    ctx.verify_mode = ssl.CERT_NONE  # sertifikat self-signed HQ (pola curl -sk)
    req = urllib.request.Request(HQ_URL + path, headers={"x-internal-secret": sec})
    op = urllib.request.build_opener(urllib.request.ProxyHandler({}),
                                     urllib.request.HTTPSHandler(context=ctx))
    with op.open(req, timeout=timeout) as r:
        return json.loads(r.read().decode("utf-8"))


def _parse_ts(v):
    if not v:
        return None
    try:
        return dt.datetime.fromisoformat(str(v).replace("Z", "+00:00"))
    except ValueError:
        return None


def probe_collect(window_min=15, fixture=None):
    """Ambil mentahan probe. Return dict; key 'error' bila jalur gagal."""
    if fixture:
        with open(fixture, encoding="utf-8") as fh:
            data = json.load(fh)
        data["source"] = "FIXTURE " + fixture
        return data
    sec, src = _secret()
    if not sec:
        return {"error": "INTERNAL_API_SECRET tidak ditemukan di env maupun " + DC_ENV}
    try:
        kpi = _hq_get("/api/brahma/dispatch-kpi", sec)
        rq = _hq_get("/api/brahma/requests?take=%d" % TAKE_MAX, sec)
    except Exception as e:  # noqa: BLE001 - semua kegagalan jalur = UNKNOWN
        return {"error": "%s: %s" % (type(e).__name__, str(e)[:160])}
    return {"source": src, "generatedAt": kpi.get("generatedAt"),
            "byStatus": kpi.get("byStatus", {}),
            "requests": rq.get("requests", []), "window_min": window_min}


def probe_evaluate(data, window_min=15, now=None):
    """Deterministik: kembalikan (status, checks) dengan checks=[(st, nama, angka)]."""
    checks = []
    if "error" in data:
        checks.append(("NEEDS_REVIEW", "jalur_hq", data["error"]))
        return "UNKNOWN", checks
    now = now or dt.datetime.now(dt.timezone.utc)
    win = now - dt.timedelta(minutes=window_min)

    bs = data.get("byStatus", {})
    depth = sum(int(bs.get(k, 0) or 0) for k in ("queued", "approved", "running"))
    ok = depth <= QUEUE_SEHAT_MAX
    checks.append((("PASS" if ok else ("FAIL" if depth >= QUEUE_TEKANAN_MIN else "NEEDS_REVIEW")),
                   "kedalaman_antrean",
                   "queued+approved+running=%d (queued=%s approved=%s running=%s; sehat<=%d tekanan>=%d)"
                   % (depth, bs.get("queued", 0), bs.get("approved", 0), bs.get("running", 0),
                      QUEUE_SEHAT_MAX, QUEUE_TEKANAN_MIN)))

    rows = data.get("requests", [])

    def ts_done(r):
        return _parse_ts(r.get("finishedAt")) or _parse_ts(r.get("updatedAt"))

    term = [r for r in rows if r.get("status") in TERMINAL and (ts_done(r) or win) >= win]
    ft = [r for r in term if r.get("status") == "failed" and TIMEOUT_RE.search(r.get("error") or "")]
    ratio = (len(ft) / len(term)) if term else 0.0
    truncated = len(rows) >= TAKE_MAX and any(
        (_parse_ts(r.get("createdAt")) or now) >= win for r in rows[-1:])
    st = "PASS"
    if truncated or ratio >= RATIO_TEKANAN_MIN:
        st = "FAIL"
    elif not (ratio <= RATIO_SEHAT_MAX) or (0 < len(term) < 3 and ft):
        st = "NEEDS_REVIEW"
    checks.append((st, "rasio_failed_timeout_%dmenit" % window_min,
                   "terminal=%d failed_timeout=%d rasio=%.2f (sehat<=%.2f tekanan>=%.2f)%s"
                   % (len(term), len(ft), ratio, RATIO_SEHAT_MAX, RATIO_TEKANAN_MIN,
                      " SAMPEL_TERPOTONG(>=%d)" % TAKE_MAX if truncated else "")))

    # keputusan (fail-safe: hanya SEHAT yang lolos; sisanya statis 2/4)
    if truncated or depth >= QUEUE_TEKANAN_MIN or ratio >= RATIO_TEKANAN_MIN:
        status = "TEKANAN"
    elif depth <= QUEUE_SEHAT_MAX and ratio <= RATIO_SEHAT_MAX and not (0 < len(term) < 3 and ft):
        status = "SEHAT"
    else:
        status = "TEKANAN"  # pita tengah = gagal aman
    return status, checks


def run_probe(window_min=15, fixture=None):
    data = probe_collect(window_min=window_min, fixture=fixture)
    status, checks = probe_evaluate(data, window_min=window_min)
    print("PROBE SUMBER: %s" % data.get("source", "?"))
    for i, (st, name, num) in enumerate(checks, 1):
        print("CHECK %d: %s - %s | %s" % (i, st, name, num))
    rec = ("naik di atas 5 boleh atas keputusan operator" if status == "SEHAT"
           else "pakai statis 5 per misi tanpa batas per jenis")
    print("PROBE: %s | rekomendasi gelombang: %s" % (status, rec))
    verdict = {"SEHAT": "PASS", "TEKANAN": "FAIL", "UNKNOWN": "NEEDS_REVIEW"}[status]
    print("VERDICT: %s" % verdict)
    return {"SEHAT": 0, "TEKANAN": 1, "UNKNOWN": 2}[status]


def main(argv=None):
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except (AttributeError, ValueError):
        pass

    ap = argparse.ArgumentParser(
        prog="lad_audit.py",
        description="Guard anti-mundur delegasi Limit-Aware (pasal C.5).")
    ap.add_argument("--since", default=None,
                    help="marker deploy ISO-8601 yang dicatat controller di "
                         "kontrak (WAJIB untuk mode audit; tanpa zona waktu = lokal mesin)")
    ap.add_argument("--probe", action="store_true",
                    help="mode probe concurrency D-LAD-05 (baca API HQ; "
                         "--since tidak dipakai pada mode ini)")
    ap.add_argument("--fixture", default=None,
                    help="mode --probe: ganti sumber HQ dengan berkas JSON fixture "
                         "(uji sintetis; nyatakan sebagai fixture, bukan data live)")
    ap.add_argument("--window-min", type=int, default=15,
                    help="mode --probe: lebar jendela rasio failed-timeout dalam menit "
                         "(default 15)")
    ap.add_argument("--board", default="default", help="kanban board (default default)")
    ap.add_argument("--json-out", default=None,
                    help="opsional: tulis hasil terstruktur ke berkas JSON ini")
    ap.add_argument("--report-window-jam", type=int, default=DEFAULT_REPORT_WINDOW_JAM,
                    help="lama jendela laporan pra-marker dalam jam (default %d; "
                         "0 = jendela laporan dimatikan)" % DEFAULT_REPORT_WINDOW_JAM)
    ap.add_argument("--no-report", action="store_true",
                    help="jangan menulis laporan ke folder kontrak (debug saja)")
    args = ap.parse_args(argv)

    if args.probe:
        return run_probe(window_min=args.window_min, fixture=args.fixture)
    if not args.since:
        ap.error("--since wajib kecuali mode --probe (lihat --help)")

    since = parse_iso(args.since)
    window_lo = since - args.report_window_jam * 3600 if args.report_window_jam > 0 else None

    cards = run_list(args.board)
    assigned = [c for c in cards if c.get("assignee")]
    unassigned = len(cards) - len(assigned)
    scope = [c for c in assigned if (c.get("created_at") or 0) >= since]
    scope.sort(key=lambda c: (c.get("created_at") or 0, c.get("id") or ""))
    prewin = sorted((c for c in assigned
                     if window_lo is not None
                     and (c.get("created_at") or 0) < since
                     and (c.get("created_at") or 0) >= window_lo),
                    key=lambda c: (c.get("created_at") or 0, c.get("id") or ""))

    checks = []          # (status, nama)
    detail_pre = []      # kartu pra-marker tanpa blok (laporan)
    detail_json = []     # semua temuan terstruktur

    def add(status, nama, **extra):
        checks.append((status, nama))
        rec = {"check": nama, "status": status}
        rec.update(extra)
        detail_json.append(rec)

    # --- Jendela laporan: bukti detector tidak buta terhadap kartu lama ----
    n_prewin_noblok = 0
    for c in prewin:
        if PATTERN_BLOCK not in (c.get("body") or ""):
            n_prewin_noblok += 1
            detail_pre.append({
                "id": c.get("id"), "title": c.get("title"),
                "assignee": c.get("assignee"),
                "created_at": c.get("created_at"),
                "created_lokal": fmt_local(c.get("created_at") or 0),
            })
    if window_lo is not None:
        if n_prewin_noblok:
            contoh = ", ".join(d["id"] for d in detail_pre[:10])
            add("NEEDS_REVIEW",
                "laporan jendela pra-marker: %d/%d kartu lama ber-assignee TANPA "
                "blok LIMIT-AWARE di body (pra-kebijakan, tidak memblokir; "
                "daftar lengkap di laporan; contoh: %s)"
                % (n_prewin_noblok, len(prewin), contoh),
                kind="prewindow", jumlah=n_prewin_noblok, total=len(prewin),
                kartu=detail_pre)
        else:
            add("PASS",
                "laporan jendela pra-marker: %d kartu lama ber-assignee, semua "
                "sudah memuat blok LIMIT-AWARE di body" % len(prewin),
                kind="prewindow", jumlah=0, total=len(prewin))

    # --- Check per kartu dalam lingkup (created_at >= since) ---------------
    gcap = global_default_cap()
    for c in scope:
        tid = c.get("id") or "?"
        title = (c.get("title") or "")[:60]
        assignee = c.get("assignee") or ""
        body = c.get("body") or ""

        # Detail selalu diambil: komentar needed utk cek blok fallback,
        # runs needed utk cek kematian senyap + rantai.
        det = show_card(args.board, tid)
        comments_text = ""
        runs = []
        if det:
            comments_text = "\n".join(
                (cm.get("body") or "") for cm in (det.get("comments") or []))
            runs = det.get("runs") or []
        else:
            add("NEEDS_REVIEW", "%s %s - detail kartu tidak terbaca via "
                "`kanban show --json` (cek komentar/run dilewati)" % (tid, title),
                kind="show_gagal")

        hay = body + "\n" + comments_text

        # C.5.2a: kehadiran blok LIMIT-AWARE (body ATAU komentar).
        if PATTERN_BLOCK in hay:
            add("PASS", "%s %s - blok LIMIT-AWARE hadir" % (tid, title),
                kind="blok", kartu=tid)
        else:
            add("FAIL", "%s %s - TIDAK ADA blok LIMIT-AWARE di body/komentar "
                "(kartu pasca-marker ber-assignee)" % (tid, title),
                kind="blok", kartu=tid)

        # C.5.2b: angka iterasi blok == max_turns profil saat-itu.
        cfg_cap, cfg_warn = cap_for(assignee)
        blok_num = extract_cap_number(hay) if PATTERN_BLOCK in hay else None
        if PATTERN_BLOCK not in hay:
            pass  # sudah FAIL di cek blok; angka tidak bisa dinilai
        elif blok_num is None:
            add("NEEDS_REVIEW", "%s %s - blok LIMIT-AWARE ada tapi angka "
                "iterasinya tidak terbaca pola (perlu tinjau manual)" % (tid, title),
                kind="cap", kartu=tid)
        elif cfg_cap is None:
            add("NEEDS_REVIEW", "%s %s - config profil '%s' tidak terbaca (%s); "
                "blok menulis %d, pembanding tidak tersedia (default global %s "
                "hanya informasi, bukan pembanding)"
                % (tid, title, assignee, cfg_warn, blok_num,
                   gcap if gcap else "?"),
                kind="cap", kartu=tid, nilai_blok=blok_num)
        elif blok_num != cfg_cap:
            add("FAIL", "%s %s - angka blok %d != agent.max_turns profil '%s' "
                "saat-itu = %d" % (tid, title, blok_num, assignee, cfg_cap),
                kind="cap", kartu=tid, nilai_blok=blok_num, nilai_config=cfg_cap)
        else:
            add("PASS", "%s %s - angka blok %d == max_turns '%s'" % (
                tid, title, blok_num, assignee),
                kind="cap", kartu=tid, nilai_blok=blok_num)

        # C.5.2c: jejak ESTIMASI atau flag interaktif eksplisit di body.
        if "ESTIMASI:" in hay:
            add("PASS", "%s %s - jejak ESTIMASI ada" % (tid, title),
                kind="estimasi", kartu=tid)
        elif "interaktif" in body:
            add("PASS", "%s %s - pengecualian interaktif eksplisit di body "
                "(tanpa jejak ESTIMASI)" % (tid, title),
                kind="estimasi", kartu=tid)
        else:
            add("FAIL", "%s %s - tidak ada jejak ESTIMASI dan tidak ada flag "
                "interaktif eksplisit di body" % (tid, title),
                kind="estimasi", kartu=tid)

        # C.5.3: kematian senyap (crash/gave_up/timeout wajib partial-handoff).
        dead = [r for r in runs
                if (r.get("outcome") or "") in DEAD_STATES
                or (r.get("status") or "") in DEAD_STATES]
        if dead:
            if PATTERN_HANDOFF in hay:
                add("PASS", "%s %s - %d run mati (crash/gave_up/timeout) "
                    "didampingi komentar memuat '%s'" % (
                        tid, title, len(dead), PATTERN_HANDOFF),
                    kind="mati_senyap", kartu=tid)
            else:
                outs = ",".join(sorted({(r.get("outcome") or r.get("status") or "?")
                                        for r in dead}))
                add("FAIL", "%s %s - kematian senyap: run ber-outcome [%s] tanpa "
                    "komentar memuat string literal '%s'" % (
                        tid, title, outs, PATTERN_HANDOFF),
                    kind="mati_senyap", kartu=tid)

        # C.5.4: rantai (lanjutan N/M) dengan N>3 atau M>3 = violasi D-TA-06.
        m = CHAIN_RE.search(c.get("title") or "")
        if m:
            n_, mtot = int(m.group(1)), int(m.group(2))
            if n_ > MAX_CHAIN or mtot > MAX_CHAIN:
                add("FAIL", "%s %s - rantai (lanjutan %d/%d) melewati batas "
                    "maksimum %d mata (D-TA-06)" % (tid, title, n_, mtot, MAX_CHAIN),
                    kind="rantai", kartu=tid, n=n_, m=mtot)
            else:
                add("PASS", "%s %s - rantai (lanjutan %d/%d) dalam batas %d mata" % (
                    tid, title, n_, mtot, MAX_CHAIN),
                    kind="rantai", kartu=tid, n=n_, m=mtot)

    # --- Ringkasan + VERDICT ------------------------------------------------
    n_fail = sum(1 for s, _ in checks if s == "FAIL")
    n_nr = sum(1 for s, _ in checks if s == "NEEDS_REVIEW")
    n_pass = sum(1 for s, _ in checks if s == "PASS")

    lines = []
    for i, (status, nama) in enumerate(checks, 1):
        lines.append("CHECK %d: %s - %s" % (i, status, nama))
    verdict = ("FAIL (%d FAIL, %d NEEDS_REVIEW, %d PASS)" % (n_fail, n_nr, n_pass)
               if n_fail else
               ("NEEDS_REVIEW (%d NEEDS_REVIEW, %d PASS, 0 FAIL)" % (n_nr, n_pass)
                if n_nr else
                "PASS (%d PASS)" % n_pass))
    lines.append("VERDICT: %s" % verdict)

    for ln in lines:
        print(ln)

    now = dt.datetime.now()
    stamp = now.strftime("%Y%m%d_%H%M%S")
    exit_code = 1 if n_fail else 0

    print("kartu total=%d ber-assignee=%d tanpa-assignee(dilaporkan)=skip=%d "
          "lingkup(pasca-marker)=%d jendela-pra=%d | since=%s(%d) exit=%d"
          % (len(cards), len(assigned), unassigned, len(scope), len(prewin),
             args.since, since, exit_code))

    if not args.no_report:
        contract_dir = Path(os.environ.get("GSP_SHARED_WS",
                                           "C:/Users/TRIAL/workspace/gsp-hermes/workspace")
                            ) / "docs" / "2026-09-02-limit-aware-delegation"
        report_path = contract_dir / ("AUDIT-LAD_%s.md" % stamp)
        try:
            contract_dir.mkdir(parents=True, exist_ok=True)
            with open(report_path, "w", encoding="utf-8", newline="\n") as fh:
                fh.write("# Laporan Audit LAD (lad_audit.py)\n\n")
                fh.write("- Waktu: %s\n" % now.strftime("%Y-%m-%d %H:%M:%S"))
                fh.write("- Perintah: `%s`\n" % " ".join(
                    ["lad_audit.py"] + (argv if argv is not None else sys.argv[1:])))
                fh.write("- Marker --since: %s (epoch %d)\n" % (args.since, since))
                fh.write("- Board: %s | sumber data: `hermes kanban --board %s "
                         "list --archived --json`\n" % (args.board, args.board))
                fh.write("- Kartu: total %d, ber-assignee %d, tanpa-assignee "
                         "(di luar cakupan C.5) %d\n" % (
                             len(cards), len(assigned), unassigned))
                fh.write("- Lingkup audit (created_at >= since): %d kartu; "
                         "jendela laporan pra-marker: %d kartu (%d tanpa blok)\n\n"
                         % (len(scope), len(prewin), n_prewin_noblok))
                fh.write("## Keluaran CHECK/VERDICT (mentah)\n\n```\n")
                fh.write("\n".join(lines))
                fh.write("\n```\n\n")
                fh.write("Exit code: %d\n\n" % exit_code)
                if detail_pre:
                    fh.write("## Kartu pra-marker TANPA blok LIMIT-AWARE "
                             "(dilaporkan, tidak memblokir)\n\n")
                    fh.write("| id | judul | assignee | dibuat (lokal) | epoch |\n")
                    fh.write("|---|---|---|---|---|\n")
                    for d in detail_pre:
                        fh.write("| `%s` | %s | %s | %s | %s |\n" % (
                            d["id"], (d["title"] or "").replace("|", "\\|"),
                            d["assignee"], d["created_lokal"], d["created_at"]))
                    fh.write("\n")
        except OSError as exc:
            print("PERINGATAN: laporan gagal ditulis: %s" % exc)
            report_path = None
        if report_path:
            print("laporan: %s" % report_path)

    if args.json_out:
        try:
            with open(args.json_out, "w", encoding="utf-8") as fh:
                json.dump({
                    "generated_at": now.isoformat(timespec="seconds"),
                    "board": args.board, "since_iso": args.since, "since_epoch": since,
                    "cards_total": len(cards), "cards_assigned": len(assigned),
                    "cards_unassigned_skipped": unassigned,
                    "scope_cards": [c.get("id") for c in scope],
                    "prewindow_no_block": detail_pre,
                    "checks": detail_json,
                    "counts": {"pass": n_pass, "fail": n_fail, "needs_review": n_nr},
                    "verdict": verdict, "exit_code": exit_code,
                }, fh, ensure_ascii=False, indent=1)
            print("json: %s" % args.json_out)
        except OSError as exc:
            print("PERINGATAN: json-out gagal ditulis: %s" % exc)

    return exit_code


if __name__ == "__main__":
    sys.exit(main())
