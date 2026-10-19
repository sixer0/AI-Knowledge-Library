"""Watchdog misi NAT (gate naturalisasi) + SEKSI LAD (langkah 12 LAD) + SEKSI FASE (ORC).
Cetak laporan HANYA bila ada perubahan status kartu / misi selesai / indikasi macet
/ temuan LAD baru. Stdout kosong = tidak ada yang dilaporkan (cron no_agent = diam).

SEKSI LAD (kebijakan Limit-Aware 02-09-2026, perluasan t_53da72cd):
subset deterministik lad_audit.py -- sejak marker deploy D-LAD-10 (dibaca dinamis
dari contract.md, fallback konstanta):
  L1 kartu pasca-marker ber-assignee TANPA string literal 'LIMIT-AWARE' di body/komentar
  L2 kematian senyap: run crash/gave_up/timeout tanpa komentar memuat 'partial-handoff'
  L3 rantai judul (lanjutan N/M) dengan N>3 atau M>3 (D-TA-06)
Pola HANYA dari konstanta modul lad_audit kanonik (D-TA-13); bila impor gagal,
seksi dilaporkan eksplisit sebagai error, bukan hilang. Setiap laporan yang tercetak
WAJIB memuat SEKSI LAD: temuan, 'nol temuan', atau error eksplisit.
Gagal total watchdog tetap dicetak (perilaku lama dipertahankan)."""
import subprocess, json, os, time, sys, datetime as dt, importlib.util

STATE = os.path.join(os.environ.get("LOCALAPPDATA", ""), "hermes", "cron", "output", "nat_gate_state.json")
CONTRACT = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-limit-aware-delegation/contract.md"
LAD_AUDIT_CANDIDATES = (
    "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-limit-aware-delegation/scripts/lad_audit.py",
    "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-limit-aware-delegation/scripts/lad_audit.py",
)
MARKER_FALLBACK = "2026-09-02T17:10:41+07:00"   # D-LAD-10, contract.md Decision Log
LAD_MAX_CARDS = 80       # kap kartu pasca-marker per siklus (urut terbaru)
LAD_BUDGET_S = 90        # kap detik total sub-audit LAD (fail-safe waktu cron)

# ------------------------------------------------------------- SEKSI FASE (ORC)
# Kebijakan Laporan Kenaikan Fase 02-09-2026 (D-ORC-TA-06/12, blueprint par. 7.2):
# watchdog HANYA menagih laporan [FASE] yang bolos; tidak pernah menyusun resume.
PHASE_AUDIT_CANDIDATES = (
    "C:/Users/TRIAL/workspace/gsp-hermes/skills/gsp-orchestrator-worker/scripts/phase_report_audit.py",
    "C:/Users/TRIAL/AppData/Local/hermes/skills/gsp/gsp-orchestrator-worker/scripts/phase_report_audit.py",
)
ORC_CONTRACT = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-09-02-laporan-kenaikan-fase/contract.md"
MARKER_FASE_FALLBACK = "2026-09-02T18:40:00+07:00"   # fallback D-ORC-TA-13 (epoch distribusi SM)
PHASE_PREFIXES = ("NAT-", "LAD-", "ORC-")
PHASE_BUDGET_S = 90        # kap detik sub-audit FASE (pola LAD_BUDGET_S)
PHASE_WINDOW_S = 900       # jendela pairing DF-1 (D-ORC-TA-04)

def fetch():
    p = subprocess.run(["hermes", "kanban", "--board", "default", "list", "--json"],
                       capture_output=True, text=True, timeout=60)
    cards = json.loads(p.stdout)
    out = {}
    for c in cards:
        t = c.get("title", "")
        if t.startswith("NAT-") or t.startswith("LAD-"):
            out[c["id"]] = {"title": t, "assignee": c.get("assignee"), "status": c.get("status")}
    return out

# ---------------------------------------------------------------- LAD subset
def load_lad_module():
    for path in LAD_AUDIT_CANDIDATES:
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("lad_audit_watchdog", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, path
    return None, None

def lad_marker():
    """Marker deploy D-LAD-10: baca dari contract.md, fallback konstanta."""
    iso = MARKER_FALLBACK
    src = "fallback-konstanta"
    try:
        txt = open(CONTRACT, encoding="utf-8", errors="replace").read()
        import re
        m = re.search(r"MARKER DEPLOY KEBIJAKAN LAD\s*=\s*\*\*\s*([^*\s]+)", txt)
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

def lad_findings():
    """Kembalikan (lines, n_scope, error). lines = temuan L1/L2/L3 (kanonik pola
    dari lad_audit); kosong = nol temuan."""
    mod, mod_path = load_lad_module()
    if mod is None:
        return [], 0, "lad_audit.py tidak ditemukan di kandidat kanonik/fleet"
    since, marker_iso, marker_src = lad_marker()
    try:
        cards = mod.run_list("default")
    except SystemExit as e:
        return [], 0, "kanban list gagal: %s" % str(e)[:200]
    scope = sorted((c for c in cards if c.get("assignee")
                    and (c.get("created_at") or 0) >= since),
                   key=lambda c: -(c.get("created_at") or 0))
    total_scope = len(scope)
    truncated = total_scope > LAD_MAX_CARDS
    lines = []
    t0 = time.time()
    timecut = 0
    for c in scope[:LAD_MAX_CARDS]:
        if time.time() - t0 > LAD_BUDGET_S:
            timecut = 1
            break
        tid = c.get("id") or "?"
        title = (c.get("title") or "")[:58]
        body = c.get("body") or ""
        det = mod.show_card("default", tid)
        comments_text = ""
        runs = []
        if det:
            comments_text = "\n".join((cm.get("body") or "") for cm in (det.get("comments") or []))
            runs = det.get("runs") or []
        hay = body + "\n" + comments_text
        # L1: blok LIMIT-AWARE wajib hadir (body ATAU komentar)
        if mod.PATTERN_BLOCK not in hay:
            lines.append("L1-blok %s %s - TANPA blok LIMIT-AWARE di body/komentar" % (tid, title))
        # L2: kematian senyap wajib partial-handoff
        dead = [r for r in runs
                if (r.get("outcome") or "") in mod.DEAD_STATES
                or (r.get("status") or "") in mod.DEAD_STATES]
        if dead and mod.PATTERN_HANDOFF not in hay:
            outs = ",".join(sorted({(r.get("outcome") or r.get("status") or "?") for r in dead}))
            lines.append("L2-mati-senyap %s %s - run [%s] tanpa komentar '%s'"
                         % (tid, title, outs, mod.PATTERN_HANDOFF))
        # L3: rantai (lanjutan N/M) melewati batas
        m = mod.CHAIN_RE.search(c.get("title") or "")
        if m and (int(m.group(1)) > mod.MAX_CHAIN or int(m.group(2)) > mod.MAX_CHAIN):
            lines.append("L3-rantai %s %s - (lanjutan %s/%s) melewati batas %d mata (D-TA-06)"
                         % (tid, title, m.group(1), m.group(2), mod.MAX_CHAIN))
    note = ("audit %d/%d kartu pasca-marker sejak %s (%s); sumber pola %s%s%s"
            % (min(len(scope), LAD_MAX_CARDS) - timecut, total_scope, marker_iso, marker_src,
               os.path.basename(mod_path),
               "; TERPOTONG kap-kartu %d" % LAD_MAX_CARDS if truncated else "",
               "; TERPOTONG kap-waktu %ds" % LAD_BUDGET_S if timecut else ""))
    return lines, total_scope, None, note

# ---------------------------------------------------------------- FASE subset
def load_phase_module():
    """Pola load_lad_module: kanonik lalu fleet."""
    for path in PHASE_AUDIT_CANDIDATES:
        if os.path.exists(path):
            spec = importlib.util.spec_from_file_location("phase_report_audit_watchdog", path)
            mod = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(mod)
            return mod, path
    return None, None


def phase_marker():
    """Marker deploy D-ORC-TA-13: baca dinamis dari contract.md ORC, fallback konstanta."""
    import re
    iso, src = MARKER_FASE_FALLBACK, "fallback-konstanta"
    try:
        txt = open(ORC_CONTRACT, encoding="utf-8", errors="replace").read()
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
        d = dt.datetime.fromisoformat(MARKER_FASE_FALLBACK)
        return int(d.timestamp()), MARKER_FASE_FALLBACK, "fallback-invalid-dipaksa"


def phase_findings():
    """Kembalikan (lines, error, note). lines = temuan P1-bolos-laporan;
    kosong = nol temuan. Sumber: modul audit phase_report_audit (bolos_reports)."""
    mod, mod_path = load_phase_module()
    if mod is None:
        return [], "phase_report_audit.py tidak ditemukan di kandidat kanonik/fleet", ""
    since, marker_iso, marker_src = phase_marker()
    t0 = time.time()
    try:
        lines = mod.bolos_reports(PHASE_PREFIXES, since, window_s=PHASE_WINDOW_S)
    except Exception as e:
        return [], "%s: %s" % (type(e).__name__, str(e)[:160]), ""
    note = ("audit %d prefix %s sejak %s (%s); sumber %s (%.1fs)"
            % (len(PHASE_PREFIXES), ",".join(PHASE_PREFIXES), marker_iso, marker_src,
               os.path.basename(mod_path), time.time() - t0))
    return list(lines), None, note


def main():
    cur = fetch()
    prev = {}
    prev_ts = 0
    prev_lad_reported = None
    prev_phase_reported = None
    prev_reported_done = False
    if os.path.exists(STATE):
        try:
            d = json.load(open(STATE, encoding="utf-8"))
            prev = d.get("cards", {})
            prev_ts = d.get("last_change_ts", 0)
            prev_lad_reported = (d.get("lad") or {}).get("last_reported")
            prev_phase_reported = (d.get("phase") or {}).get("last_reported")
            prev_reported_done = bool(d.get("reported_done", False))
        except Exception:
            pass
    now = time.time()
    changes = []
    for cid, c in cur.items():
        old = prev.get(cid)
        if old is None and c["status"] in ("running", "done"):
            changes.append(f"BARU jalan/selesai: {c['title'][:58]} [{c['status']}]")
        elif old and old.get("status") != c["status"]:
            changes.append(f"{c['title'][:58]}: {old['status']} -> {c['status']}")
    terminal = ("done", "archived")
    nat_s = {k: v for k, v in cur.items() if v["title"].startswith("NAT-S")}
    all_done = bool(nat_s) and all(v["status"] in terminal for v in nat_s.values())
    done_n = sum(1 for v in nat_s.values() if v["status"] in terminal)
    blocked = [v["title"][:58] for v in cur.values() if v["status"] == "blocked"]

    # --- sub-audit FASE (selalu jalan; hasil selalu tampil di laporan tercetak)
    phase_err = None
    phase_note = ""
    try:
        phase_lines, phase_err, phase_note = phase_findings()
    except Exception as e:
        phase_lines, phase_err, phase_note = [], "%s: %s" % (type(e).__name__, str(e)[:160]), ""

    def phase_section():
        head = "[SEKSI FASE] "
        if phase_err:
            return [head + "ERROR audit: " + phase_err + " (seksi eksplisit, bukan absen)"]
        if phase_lines:
            return ([head + "%d TEMUAN:" % len(phase_lines)]
                    + ["  ! " + l for l in phase_lines[:15]]
                    + ["  (" + phase_note + ")"])
        return [head + "nol temuan (" + phase_note + ")"]

    phase_trigger = bool(phase_err) or (bool(phase_lines) and phase_lines != prev_phase_reported)

    # --- sub-audit LAD (selalu jalan; hasil selalu tampil di laporan tercetak)
    lad_err = None
    lad_note = ""
    try:
        res = lad_findings()
        lad_lines, lad_scope, lad_err = res[0], res[1], res[2]
        lad_note = res[3] if len(res) > 3 else ""
    except Exception as e:
        lad_lines, lad_scope, lad_err = [], 0, "%s: %s" % (type(e).__name__, str(e)[:160])

    def lad_section():
        head = "[SEKSI LAD] "
        if lad_err:
            return [head + "ERROR audit: " + lad_err + " (seksi eksplisit, bukan absen)"]
        if lad_lines:
            return ([head + "%d TEMUAN:" % len(lad_lines)]
                    + ["  ! " + l for l in lad_lines[:15]]
                    + (["  ... +%d temuan lagi" % (len(lad_lines) - 15)] if len(lad_lines) > 15 else [])
                    + ["  (" + lad_note + ")"])
        return [head + "nol temuan (" + lad_note + ")"]

    lad_trigger = bool(lad_err) or (bool(lad_lines) and lad_lines != prev_lad_reported)

    lines = []
    done_transition = all_done and not prev_reported_done   # pesan selesai hanya saat transisi pertama (t_480f6fa4)
    if done_transition:
        lines.append(f"[NAT WATCHDOG] MISI GATE NATURALISASI SELESAI: {done_n}/{len(nat_s)} kartu fase S terminal (done/archived). Cek VERDICT.md dan countersign di docs/2026-09-02-naturalisasi-output/.")
    elif changes:
        lines.append(f"[NAT WATCHDOG] Progres {done_n}/{len(nat_s)} kartu S terminal:")
        lines.extend("  - " + ch for ch in changes[:12])
        if blocked:
            lines.append("  - TERBLOKIR: " + "; ".join(blocked[:5]))
    elif prev and (now - prev_ts) > 7200 and not all_done:
        stuck = [f"{v['title'][:50]}[{v['status']}]" for v in cur.values() if v["status"] in ("todo", "running")]
        lines.append(f"[NAT WATCHDOG] WASPADA MACET: tidak ada perubahan status >2 jam. Sisa {len(stuck)} kartu belum terminal, contoh: " + "; ".join(stuck[:6]))

    if lines or lad_trigger or phase_trigger or done_transition:
        if not lines:
            lines.append("[NAT WATCHDOG] Perubahan status kartu: tidak ada; laporan terpicu oleh temuan/error FASE/LAD.")
        lines.extend(phase_section())
        lines.extend(lad_section())

    new_last_change = prev_ts
    if changes or not prev:
        new_last_change = now
    elif all_done:
        new_last_change = prev_ts
    lad_state = {"last_run_ts": now, "scope": lad_scope,
                 "last_reported": lad_lines if (lines or lad_trigger) else prev_lad_reported,
                 "error": lad_err}
    phase_state = {"last_run_ts": now,
                   "last_reported": phase_lines if (lines or phase_trigger) else prev_phase_reported,
                   "error": phase_err}
    json.dump({"cards": cur, "last_change_ts": new_last_change,
               "reported_done": all_done, "lad": lad_state, "phase": phase_state},
              open(STATE, "w", encoding="utf-8"))
    if lines:
        print("\n".join(lines))

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"[NAT WATCHDOG] ERROR watchdog: {e}")
