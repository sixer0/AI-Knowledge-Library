#!/usr/bin/env python3
"""phase_report_audit.py - guard anti-mundur kebijakan Laporan Kenaikan Fase (ORC).

Rumah kanonik: skills/gsp-orchestrator-worker/scripts/phase_report_audit.py (D-ORC-TA-12).
Sembilan check G-1..G-9 (blueprint identification/02_structured.md par. 7.1, misi
docs/2026-09-02-laporan-kenaikan-fase):
  G-1 Pairing    : tiap kenaikan fase DF-1 pasca-marker punya blok [FASE] berpasangan
                   dengan kunci ketat (misi, fase-lama -> fase-baru) per blueprint
                   par. 4.2 plus jendela waktu <= 900 s (D-VRF-02; sebelumnya hanya
                   misi+jendela sehingga blok transisi lain bisa menutupi)
  G-2 Kelengkapan: tiap blok punya marker [FASE] + enam bidang berurutan
                   (RINGKAS/ARTEFAK/JALUR/RENCANA/ESTIMASI)
  G-3 Batas bentuk: <= 7 baris, <= 1300 karakter total, <= 220 karakter/baris,
                   RINGKAS memuat >= 1 digit
  G-4 Isi minimum: RINGKAS tidak trivial (>= 20 karakter, bukan daftar penolakan
                   "done/selesai/lanjut"), RENCANA memuat nama profil assignee nyata
  G-5 Anti-dobel : kunci (misi, transisi) tepat satu blok di arsip
  G-6 Deteksi macet: block_kind needs_input/capability, atau kartu non-terminal
                   tanpa event > 7200 s, tanpa laporan T-3 (HAMBAT) berpasangan
  G-7 Artefak nyata: path di ARTEFAK ada di disk; ukuran/line-count tidak mengecil
                   dari yang dikutip (boleh membesar)
  G-8 Naturalisasi: sampel >= 3 blok terbaru bebas U+2014/U+00B7/U+2013/emoji/basa-basi
  G-9 Efek orientasi: butuh baseline; TANPA baseline = NEEDS_REVIEW (dilarang klaim PASS)
Definisi kenaikan fase: DF-1 pasangan event completed (parent terakhir) + promoted
(child pertama; fallback claimed), waktu acuan = max(kedua event). Query mengikuti
par. 4.3 blueprint; DB dibuka READ-ONLY (mode=ro), tidak ada tulis ke DB.
Payung waktu menyimpang dari format F-3 '## YYYY-MM-DD HH:MM' dilaporkan eksplisit
sebagai TEMUAN PAYUNG (D-VRF-03; tidak memengaruhi exit code karena jejak typo bisa
disengaja dipertahankan), bukan diwarisi dalam diam.
Keluaran: baris CHECK n: PASS|FAIL|NEEDS_REVIEW - nama | detail, lalu VERDICT.
Exit 0 hanya bila G-1..G-8 semua PASS. G-9 selalu dilaporkan terpisah.
Dipakai juga watchdog nat_gate_watchdog.py (SEKSI FASE) via fungsi publik
read_marker / df1_pairings / parse_archive / bolos_reports (pola kandidat LAD).
"""
import argparse
import datetime as dt
import os
import re
import sqlite3
import sys

DB_CANDIDATES = (
    "C:/Users/TRIAL/AppData/Local/hermes/kanban.db",
    "C:/Users/TRIAL/AppData/Local/hermes/kanban/kanban.db",
)
PROFILES_DIR = "C:/Users/TRIAL/AppData/Local/hermes/profiles"
CONTRACT_DIRS = {
    "ORC-": "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-laporan-kenaikan-fase",
    "LAD-": "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-limit-aware-delegation",
    "NAT-": "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-naturalisasi-output",
}
MARKER_FALLBACK = "2026-09-02T18:40:00+07:00"   # D-ORC-TA-13 fallback konstanta
PAIR_WINDOW_S = 900
STUCK_S = 7200
FIELDS = ("RINGKAS", "ARTEFAK", "JALUR", "RENCANA", "ESTIMASI")
TRIVIAL = {"done", "selesai", "lanjut", "ok", "oke", "beres", "done.", "selesai.", "lanjut ke fase berikutnya"}
BASA_BASI = ("berikut adalah", "semoga membantu", "tentu,", "baik, saya", "dengan senang hati", "tentu saja")
EMOJI_RE = re.compile("[" + chr(0x1F300) + "-" + chr(0x1FAFF) + chr(0x2600) + "-" + chr(0x27BF) + chr(0x1F600) + "-" + chr(0x1F64F) + "]")


def mission_match(block_mission, db_mission):
    """Kunci misi arsip vs DB: sama persis, ATAU DB lebih rinci (ORC-RT) dari
    akar misi arsip (ORC) lewat hyphen."""
    return bool(block_mission) and (block_mission == db_mission
                                    or db_mission.startswith(block_mission + "-"))
UMBRELLA_RE = re.compile(r"^##\s+(\d{4}-\d{2}-\d{2} \d{2}:\d{2})\s*$")
FIELDMATCH_RE = re.compile(r"^(RINGKAS|ARTEFAK|JALUR|RENCANA|ESTIMASI):\s*(.*)$")


def phase_of(title):
    """Fase misi dari judul kartu: 'ORC-SM: ...' -> 'SM'; 'ORC-FIX-NET: ...' -> 'NET'."""
    return ((title or "?").split(":")[0].split("-")[-1]).strip()


def _norm_trans(t):
    return (t or "").replace(" ", "")


def unpaired_events(rows, arc, window_s):
    """Kunci ketat pairing (misi, fase-lama -> fase-baru) per blueprint par. 4.2
    (D-VRF-02; pengganti kunci longgar misi+jendela yang membiarkan blok transisi
    lain menutupi laporan hilang). Satu peristiwa kenaikan = satu child; beberapa
    parent paralel/fan-in (mis. SM dan VRF sama-sama parent CLOSE, atau dua kartu
    NET/CHAN hasil satu kartu CLOSE) digabung jadi satu peristiwa dan cukup
    dibayar satu blok [FASE] dengan salah satu kombinasi parent->child sah
    (sejajar E-4 dan kaidah 'satu kenaikan dilaporkan satu kali'). Blok wajib
    cocok transisi HANYA, jadi blok transisi lain tidak bisa lagi menutupi."""
    events = {}
    for r in rows:
        ev = events.setdefault(r["child_id"], {"want": set(), "mission": r["mission"],
                                               "t": set()})
        ev["want"].add(_norm_trans("%s -> %s" % (phase_of(r["p_title"]),
                                                 phase_of(r["c_title"]))))
        ev["t"].add(r["t_acuan"])
    miss = []
    for cid, ev in sorted(events.items()):
        ok = any(mission_match(b["mission"], ev["mission"])
                 and _norm_trans(b["transition"]) in ev["want"]
                 and b["ts"] is not None
                 and any(abs(b["ts"] - t) <= window_s for t in ev["t"])
                 for b in arc)
        if not ok:
            miss.append({"child_id": cid, "t_acuan": max(ev["t"]),
                         "mission": ev["mission"],
                         "want": " / ".join(sorted(ev["want"]))})
    return miss


def umbrella_findings(path):
    """D-VRF-03: payung waktu yang mengawali tanggal (token '## YYYY-MM-DD...')
    tetapi menyimpang dari format F-3 '## YYYY-MM-DD HH:MM' menjadi temuan
    eksplisit, bukan diwarisi dalam diam. Judul seksi non-tanggal tidak ditagih."""
    if not os.path.exists(path):
        return []
    out = []
    datey = re.compile(r"^##\s+\d{4}-\d{2}-\d{2}")
    for i, line in enumerate(open(path, encoding="utf-8", errors="replace"), 1):
        ln = line.rstrip("\n")
        if datey.match(ln) and not UMBRELLA_RE.match(ln):
            out.append("baris %d: %r tidak sesuai F-3 '## YYYY-MM-DD HH:MM'" % (i, ln.strip()))
    return out


def g1_exceptions(contract_md):
    """Catatan pengecualian pairing di Decision Log kontrak (escape hatch sah
    blueprint par. 7.1 G-1: 'transisi tanpa pasangan TANPA catatan pengecualian
    = FAIL'). Baris kontrak berisi 'PENGEKUALIAN-G1' mengambil id kartu t_xxx
    pada baris yang sama; dipakai utk promosi tindak-lanjut pasca-tutup misi
    yang bukan kenaikan fase (analog E-2)."""
    ids = set()
    try:
        txt = open(contract_md, encoding="utf-8", errors="replace").read()
    except OSError:
        return ids
    for m in re.finditer(r"PENGEKUALIAN[- ]G-?1[^\n]*", txt):
        ids.update(re.findall(r"t_[0-9a-f]{6,}", m.group(0)))
    return ids


def open_db():
    """Buka board DB read-only; kandidat pertama yang ada dan tidak nol byte."""
    for p in DB_CANDIDATES:
        try:
            if os.path.exists(p) and os.path.getsize(p) > 0:
                return sqlite3.connect("file:%s?mode=ro" % p.replace("\\", "/"), uri=True), p
        except sqlite3.Error:
            continue
    return None, None


def read_marker(contract_md, fallback=MARKER_FALLBACK):
    """Marker deploy D-ORC-TA-13: baca dinamis dari contract.md, fallback konstanta."""
    iso, src = fallback, "fallback-konstanta"
    try:
        txt = open(contract_md, encoding="utf-8", errors="replace").read()
        m = re.search(r"MARKER DEPLOY KEBIJAKAN ORC\s*=\s*\*\*\s*([^*\s]+)", txt)
        if m:
            iso, src = m.group(1), "contract.md"
    except OSError:
        pass
    try:
        d = dt.datetime.fromisoformat(iso)
        if d.tzinfo is None:
            d = d.astimezone()
        return int(d.timestamp()), iso, src
    except ValueError:
        d = dt.datetime.fromisoformat(MARKER_FALLBACK)
        return int(d.timestamp()), MARKER_FALLBACK, "fallback-invalid-dipaksa"


def df1_pairings(conn, prefixes, since):
    """Kenaikan fase DF-1 pasca-marker: pasangan (parent done -> child promoted/claimed)."""
    rows = []
    if conn is None:
        return rows, "DB board tidak tersedia (kedua kandidat kosong/absen)"
    for prefix in prefixes:
        base = conn.execute(
            """
            SELECT l.parent_id, l.child_id, pc.created_at, pt.title, ct.title, ct.assignee
            FROM task_links l
            JOIN task_events pc ON pc.task_id = l.parent_id AND pc.kind = 'completed'
            JOIN tasks pt ON pt.id = l.parent_id
            JOIN tasks ct ON ct.id = l.child_id
            WHERE pc.id = (SELECT MAX(id) FROM task_events
                           WHERE task_id = l.parent_id AND kind = 'completed')
              AND pt.title GLOB ?
              AND pc.created_at >= ?
            """,
            (prefix + "*", since),
        ).fetchall()
        for parent_id, child_id, t_done, p_title, c_title, c_assignee in base:
            t_promo = conn.execute(
                "SELECT MIN(created_at) FROM task_events WHERE task_id = ? AND kind = 'promoted'",
                (child_id,),
            ).fetchone()[0]
            kind = "promoted"
            if t_promo is None:
                t_promo = conn.execute(
                    "SELECT MIN(created_at) FROM task_events WHERE task_id = ? AND kind = 'claimed'",
                    (child_id,),
                ).fetchone()[0]
                kind = "claimed"
            if t_promo is None:
                continue
            t_acuan = max(t_done, t_promo)
            if t_acuan >= since:
                mission = (p_title or "?").split(":")[0].split(" ")[0]
                rows.append({
                    "parent_id": parent_id, "child_id": child_id,
                    "t_done": t_done, "t_promo": t_promo, "kind": kind,
                    "t_acuan": t_acuan, "mission": mission,
                    "p_title": p_title, "c_title": c_title, "c_assignee": c_assignee,
                })
    rows.sort(key=lambda r: r["t_acuan"])
    return rows, None


def parse_archive(path):
    """Pars arsip PHASE-REPORTS.md -> daftar blok [FASE]. Return (blocks, file_exists)."""
    if not os.path.exists(path):
        return [], False
    txt = open(path, encoding="utf-8", errors="replace").read()
    blocks, cur_ts, cur = [], None, None
    for line in txt.splitlines():
        m = UMBRELLA_RE.match(line)
        if m:
            if cur:
                blocks.append((cur_ts, cur))
            cur_ts, cur = m.group(1), None
            continue
        if line.startswith("[FASE]"):
            if cur:
                blocks.append((cur_ts, cur))
            cur = [line]
        elif cur is not None:
            if line.strip() == "" or line.startswith("## "):
                blocks.append((cur_ts, cur))
                cur = None
            else:
                cur.append(line)
    if cur:
        blocks.append((cur_ts, cur))
    out = []
    for ts_str, ls in blocks:
        epoch = None
        if ts_str:
            try:
                epoch = int(dt.datetime.strptime(ts_str, "%Y-%m-%d %H:%M").astimezone().timestamp())
            except ValueError:
                pass
        mission, transition = "?", "?"
        m = re.match(r"\[FASE\]\s*(\S+)\s*\|\s*([^|]+)\|\s*(.*)", ls[0])
        if m:
            mission, transition = m.group(1).strip(), m.group(2).strip()
        fields, seen, curf = {}, [], None
        for ln in ls[1:]:
            fm = FIELDMATCH_RE.match(ln)
            if fm:
                name = fm.group(1)
                if name not in seen:
                    seen.append(name)
                    curf = name
                    fields[name] = fm.group(2).strip()
                else:
                    curf = name
                    fields[name] += " " + fm.group(2).strip()
            elif curf is not None and ln.strip():
                fields[curf] += " " + ln.strip()
        out.append({
            "ts": epoch, "ts_str": ts_str, "lines": ls,
            "mission": mission, "transition": transition,
            "fields": fields, "complete": seen == list(FIELDS),
        })
    return out, True


def profile_names():
    try:
        return set(os.listdir(PROFILES_DIR))
    except OSError:
        return set()


def check_blocks(blocks):
    """G-2, G-3, G-4, G-5, G-8 atas blok arsip."""
    profs = profile_names()
    res = {}
    bad_fields, bad_form, bad_isi, dup, bad_nat = [], [], [], [], []
    keys = set()
    sample = blocks[-3:] if len(blocks) >= 3 else blocks
    nat_probed = 0
    for b in blocks:
        k = (b["mission"], b["transition"])
        if k in keys:
            dup.append("%s %s" % k)
        keys.add(k)
        if not b["complete"]:
            bad_fields.append("%s %s (bidang: %s)" % (b["mission"], b["transition"],
                                 ",".join(b["fields"].keys()) or "kosong"))
        n = len(b["lines"])
        chars = sum(len(l) + 1 for l in b["lines"])
        maxline = max(len(l) for l in b["lines"])
        rk = b["fields"].get("RINGKAS", "")
        if n > 7 or chars > 1300 or maxline > 220 or not re.search(r"\d", rk):
            bad_form.append("%s %s (%d baris, %d kar, maksbar %d, digit RINGKAS: %s)"
                            % (b["mission"], b["transition"], n, chars, maxline, bool(re.search(r"\d", rk))))
        low = rk.strip().lower().rstrip(".")
        if low in TRIVIAL or len(rk.strip()) < 20:
            bad_isi.append("%s %s RINGKAS trivial (%d kar): VIOLASI steering D-ORC-03"
                           % (b["mission"], b["transition"], len(rk.strip())))
        else:
            rn = b["fields"].get("RENCANA", "")
            toks = set(re.findall(r"[A-Za-z0-9_-]{4,}", rn))
            if not (toks & profs):
                bad_isi.append("%s %s RENCANA tanpa nama profil assignee nyata" % (b["mission"], b["transition"]))
        if b in sample:
            nat_probed += 1
            raw = "\n".join(b["lines"])
            hits = []
            if chr(0x2014) in raw: hits.append("em-dash U+2014")
            if chr(0x00B7) in raw: hits.append("middle-dot U+00B7")
            if chr(0x2013) in raw: hits.append("en-dash U+2013")
            if EMOJI_RE.search(raw): hits.append("emoji")
            lowraw = raw.lower()
            for ph in BASA_BASI:
                if ph in lowraw: hits.append("basa-basi: " + ph)
            if hits:
                bad_nat.append("%s %s: %s" % (b["mission"], b["transition"], "; ".join(hits)))
    res["G-2"] = ("FAIL", "%d blok tak lengkap: %s" % (len(bad_fields), "; ".join(bad_fields[:3]))) if bad_fields \
        else ("PASS", "%d blok lengkap enam bidang berurutan" % len(blocks))
    res["G-3"] = ("FAIL", "%d blok lewat batas: %s" % (len(bad_form), "; ".join(bad_form[:3]))) if bad_form \
        else ("PASS", "%d blok dalam batas 7 baris/1300 kar/220 kar-per-baris + digit" % len(blocks))
    res["G-4"] = ("FAIL", "%d pelanggaran isi: %s" % (len(bad_isi), "; ".join(bad_isi[:3]))) if bad_isi \
        else ("PASS", "%d blok lulus uji isi minimum (RINGKAS substantif + RENCANA ber-assignee)" % len(blocks))
    res["G-5"] = ("FAIL", "kunci ganda: %s" % "; ".join(dup[:3])) if dup \
        else ("PASS", "kunci (misi, transisi) unik untuk %d blok" % len(blocks))
    if nat_probed == 0:
        res["G-8"] = ("PASS", "arsip kosong, nol blok untuk disampel")
    else:
        res["G-8"] = ("FAIL", "%d/%d blok sampel tercemar: %s" % (len(bad_nat), nat_probed, "; ".join(bad_nat[:2]))) if bad_nat \
            else ("PASS", "sampel %d blok bebas A1/A2/emoji/basa-basi" % nat_probed)
    return res


def check_artefak(blocks, ws_root="C:/Users/TRIAL/workspace/gsp-hermes/workspace"):
    """G-7: path ARTEFAK ada dan tidak mengecil dari angka yang dikutip."""
    bad, n_paths = [], 0
    for b in blocks:
        af = b["fields"].get("ARTEFAK", "")
        if not af.strip():
            continue
        paths = re.findall(r"(?:[A-Za-z]:/[^\s;()]+|docs/[^\s;()]+)", af)
        for p in paths:
            n_paths += 1
            full = p if p.startswith("C:") else os.path.join(ws_root, p)
            if not os.path.exists(full):
                bad.append("path mati: %s" % p)
                continue
            mb = re.search(r"(\d+)\s*(?:byte|bytes|B)\b", af)
            ml = re.search(r"(\d+)\s*baris", af)
            if mb:
                if os.path.getsize(full) < int(mb.group(1)):
                    bad.append("%s mengecil: kutip %s B < kini %d B" % (p, mb.group(1), os.path.getsize(full)))
            elif ml:
                try:
                    nlines = sum(1 for _ in open(full, "rb"))
                    if nlines < int(ml.group(1)):
                        bad.append("%s baris menyusut: kutip %s < kini %d" % (p, ml.group(1), nlines))
                except OSError:
                    bad.append("path tak terbaca: %s" % p)
    return ("FAIL", "%d/%d path bermasalah: %s" % (len(bad), n_paths, "; ".join(bad[:3]))) if bad \
        else ("PASS", "%d path ARTEFAK ada di disk, ukuran tidak menyusut" % n_paths)


def stuck_cards(conn, prefixes):
    """G-6: kartu non-terminal bermasalah (block_kind atau sunyi event > 7200 s)."""
    out = []
    if conn is None:
        return out, "DB tidak tersedia"
    now = int(dt.datetime.now().astimezone().timestamp())
    rows = conn.execute(
        "SELECT id, title, status, block_kind FROM tasks WHERE status NOT IN ('done','archived','cancelled')"
    ).fetchall()
    for tid, title, status, block_kind in rows:
        if not any((title or "").startswith(p) for p in prefixes):
            continue
        last = conn.execute("SELECT MAX(created_at) FROM task_events WHERE task_id = ?", (tid,)).fetchone()[0]
        if block_kind in ("needs_input", "capability"):
            out.append((tid, title, status, "block_kind=%s" % block_kind))
        elif last is not None and status in ("todo", "ready", "running") and now - last > STUCK_S:
            out.append((tid, title, status, "tanpa event %d menit" % ((now - last) // 60)))
    return out, None


def bolos_reports(prefixes, since, window_s=PAIR_WINDOW_S, conn=None):
    """Temuan P1 untuk watchdog SEKSI FASE: kenaikan fase DF-1 lebih tua dari
    window tanpa blok [FASE] berpasangan dengan kunci ketat (misi, transisi).
    D-VRF-01: pencocokan misi via mission_match (misi turunan ORC-SM cocok akar
    arsip ORC); filter lama r['mission'] != prefix.rstrip('-') tidak pernah cocok
    sehingga jaring mati. D-VRF-02: kunci ketat per blueprint par. 4.2.
    D-VRF-03: payung malformed dilaporkan eksplisit (P2-payung), bukan diam."""
    if conn is None:
        conn, _ = open_db()
    lines = []
    if conn is None:
        return ["P1-error DB board tidak tersedia"]
    rows, err = df1_pairings(conn, prefixes, since)
    if err:
        return ["P1-error " + err]
    now = int(dt.datetime.now().astimezone().timestamp())
    seen_children = set()
    for prefix in prefixes:
        cdir = CONTRACT_DIRS.get(prefix)
        if not cdir:
            continue
        arc_path = os.path.join(cdir, "PHASE-REPORTS.md")
        arc, _ = parse_archive(arc_path)
        exc = g1_exceptions(os.path.join(cdir, "contract.md"))
        sub = [r for r in rows if mission_match(prefix.rstrip("-"), r["mission"])
               and r["child_id"] not in exc]
        for m in unpaired_events(sub, arc, window_s):
            if m["child_id"] in seen_children:
                continue
            seen_children.add(m["child_id"])
            if now - m["t_acuan"] <= window_s:
                continue          # masa tenggang laporan transisi baru
            delta = (now - m["t_acuan"]) // 60
            hh = dt.datetime.fromtimestamp(m["t_acuan"]).strftime("%H:%M")
            lines.append("P1-bolos-laporan %s %s acuan=%s delta=%d menit (child %s)"
                         % (m["mission"], m["want"], hh, delta, m["child_id"]))
        for f in umbrella_findings(arc_path):
            lines.append("P2-payung-malformed %s %s" % (prefix.rstrip("-"), f))
    return lines


def main(argv=None):
    ap = argparse.ArgumentParser(description="Audit kebijakan Laporan Kenaikan Fase (ORC)")
    ap.add_argument("--board", default="default")
    ap.add_argument("--prefix", default="ORC-", help="prefix misi, pisah koma, mis. ORC-,LAD-")
    ap.add_argument("--contract", default=CONTRACT_DIRS["ORC-"] + "/contract.md")
    ap.add_argument("--archive", default=None, help="path arsip; default <dir kontrak>/PHASE-REPORTS.md")
    ap.add_argument("--out", default=None, help="tulis salinan laporan ke path ini")
    ap.add_argument("--show-pairings", type=int, default=0, help="tampilkan N pasangan DF-1 terakhir (abaikan marker)")
    ap.add_argument("--marker", default=None, help="override marker (ISO8601)")
    args = ap.parse_args(argv)
    prefixes = [p.strip() for p in args.prefix.split(",") if p.strip()]
    conn, dbp = open_db()
    since, marker_iso, marker_src = read_marker(args.contract)
    if args.marker:
        try:
            d = dt.datetime.fromisoformat(args.marker)
            since, marker_src = int(d.astimezone().timestamp()), "arg --marker"
        except ValueError:
            print("CHECK 0: FAIL - marker-arg | ISO tidak valid: %s" % args.marker)
            return 2
    pairings, perr = df1_pairings(conn, prefixes, since)
    arc_path = args.archive or os.path.join(os.path.dirname(args.contract), "PHASE-REPORTS.md")
    arc_blocks, _ = parse_archive(arc_path)
    checks = dict(check_blocks(arc_blocks))
    if perr:
        g1 = ("FAIL", perr)
    elif not pairings:
        g1 = ("PASS", "nol transisi DF-1 pasca-marker %s (%s)" % (marker_iso, marker_src))
    else:
        exc = g1_exceptions(args.contract)
        sub = [r for r in pairings if r["child_id"] not in exc]
        miss = unpaired_events(sub, arc_blocks, PAIR_WINDOW_S)
        n_ev = len({r["child_id"] for r in sub})
        note_exc = ("; dikecualikan via Decision Log: %s"
                    % ",".join(sorted(exc)) if exc else "")
        g1 = ("FAIL", "%d/%d kenaikan tanpa blok [FASE] berkunci (misi,transisi): %s%s"
              % (len(miss), n_ev, "; ".join("%s %s child=%s" % (m["mission"], m["want"], m["child_id"])
                                            for m in miss[:3]), note_exc)) if miss \
            else ("PASS", "%d/%d kenaikan DF-1 berpasangan blok [FASE] kunci (misi,transisi) dalam %d s%s"
                  % (n_ev, n_ev, PAIR_WINDOW_S, note_exc))
    checks["G-1"] = g1
    checks["G-7"] = check_artefak(arc_blocks)
    stuck, serr = stuck_cards(conn, prefixes)
    if serr:
        checks["G-6"] = ("FAIL", serr)
    elif stuck:
        unrep = [s for s in stuck if not any(
            "HAMBAT:" in "\n".join(b["lines"]) and b["mission"] == s[1].split(":")[0].split(" ")[0]
            for b in arc_blocks)]
        checks["G-6"] = ("FAIL", "%d kartu anomali tanpa laporan T-3: %s" % (len(unrep),
                         "; ".join("%s[%s]%s" % (t, st, why) for _, t, st, why in unrep[:3]))) if unrep \
            else ("PASS", "%d anomali sudah berpasangan laporan T-3" % len(stuck))
    else:
        checks["G-6"] = ("PASS", "nol kartu macet/anomali pada prefix %s" % ",".join(prefixes))
    base = os.path.join(os.path.dirname(args.contract), "baseline_orientasi.json")
    if os.path.exists(base):
        checks["G-9"] = ("NEEDS_REVIEW", "baseline ada (%s); bandingkan frekuensi manual, dilarang auto-PASS" % os.path.basename(base))
    else:
        checks["G-9"] = ("NEEDS_REVIEW", "tanpa baseline orientasi; DILARANG klaim PASS (pola V-ORC-9/D-TA-10)")
    order = ["G-1", "G-2", "G-3", "G-4", "G-5", "G-6", "G-7", "G-8"]
    names = {"G-1": "Pairing", "G-2": "Kelengkapan bidang", "G-3": "Batas bentuk", "G-4": "Isi minimum",
             "G-5": "Anti-dobel", "G-6": "Deteksi macet", "G-7": "Artefak nyata", "G-8": "Naturalisasi sampel"}
    out_lines = []
    for i, k in enumerate(order, 1):
        st, det = checks[k]
        out_lines.append("CHECK %d: %s - %s | %s" % (i, st, names[k], det))
    st, det = checks["G-9"]
    out_lines.append("CHECK 9: %s - Efek orientasi | %s" % (st, det))
    umb = umbrella_findings(arc_path)
    for f in umb:
        out_lines.append("TEMUAN PAYUNG: %s" % f)   # D-VRF-03: eksplisit, bukan diam
    ok = all(checks[k][0] == "PASS" for k in order)
    out_lines.append("VERDICT: %s (G-1..G-8 wajib; G-9 temuan terpisah; marker %s via %s; DB %s)"
                     % ("PASS" if ok else "FAIL", marker_iso, marker_src, os.path.basename(dbp) if dbp else "N/A"))
    if args.show_pairings:
        rows, err = df1_pairings(conn, prefixes, 0)
        out_lines.append("INFO pasangan DF-1 terakhir (abaikan marker): %d" % (len(rows) if not err else 0))
        for r in (rows or [])[-int(args.show_pairings):]:
            out_lines.append("  %s | %s -> %s | done=%s promo=%s(%s) | assignee=%s"
                             % (r["mission"], (r["p_title"] or "")[:40], (r["c_title"] or "")[:40],
                                dt.datetime.fromtimestamp(r["t_done"]).strftime("%H:%M:%S"),
                                dt.datetime.fromtimestamp(r["t_promo"]).strftime("%H:%M:%S"),
                                r["kind"], r["c_assignee"]))
    text = "\n".join(out_lines)
    print(text)
    if args.out:
        open(args.out, "w", encoding="utf-8", newline="\n").write(text + "\n")
    if conn:
        conn.close()
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
