# Ronde 17-10 r20: satu lintasan CIM berfilter nama -> sapuan registri penuh + hantu + saksi heartbeat
import json, os, subprocess, datetime, collections

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
REG = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
SELF_PIDS = {os.getpid(), os.getppid()}

PS = """
Get-CimInstance -ClassName Win32_Process -Filter "Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'" |
Select-Object ProcessId, ParentProcessId, CreationDate, CommandLine | ConvertTo-Json -Compress
"""

t0 = datetime.datetime.now()
ps = subprocess.run(["powershell", "-NoProfile", "-Command", PS],
                    capture_output=True, text=True, timeout=150)
dt = (datetime.datetime.now() - t0).total_seconds()
if ps.returncode != 0:
    print("CIM-GALAT rc=%s stderr=%s" % (ps.returncode, ps.stderr[:400]))
    raise SystemExit(2)
raw = json.loads(ps.stdout)
if isinstance(raw, dict):
    raw = [raw]
print("CIM lintasan=%.1fs baris=%d" % (dt, len(raw)))

reg = json.load(open(REG, encoding="utf-8"))
live = set(reg["hidup"])
wajib = list(reg["gateway_wajib_hidup"])

rows = []
for p in raw:
    cl = p.get("CommandLine") or ""
    if "gateway run" not in cl:
        continue
    pid = int(p["ProcessId"])
    if pid in SELF_PIDS:
        continue
    prof = "default"
    toks = cl.split()
    for i, t in enumerate(toks):
        if t == "--profile" and i + 1 < len(toks):
            prof = toks[i + 1]
        elif t.startswith("--profile="):
            prof = t.split("=", 1)[1]
    rows.append((pid, int(p["ParentProcessId"]), prof))

by_prof = collections.defaultdict(list)
for pid, ppid, prof in rows:
    by_prof[prof].append((pid, ppid))
pids_all = {r[0] for r in rows}

print("=== SWEEP REGISTRI (dump CIM ronde ini) ===")
ghost = []
for prof in sorted(by_prof):
    entries = by_prof[prof]
    roots = [e for e in entries if e[1] not in pids_all]
    tag = "DI-DAFTAR" if prof in live else ">>> DI-LUAR-DAFTAR <<<"
    if prof not in live:
        ghost.append((prof, [e[0] for e in roots]))
    print("  %-22s proses=%d root=%d pids=%s %s" % (prof, len(entries), len(roots), [e[0] for e in entries], tag))

print("--- vonis wajib ---")
ok = True
for w in wajib:
    entries = by_prof.get(w, [])
    roots = [e for e in entries if e[1] not in pids_all]
    st = "OK" if len(roots) == 1 else ("MATI" if len(entries) == 0 else "ROOT-GANDA(%d)" % len(roots))
    if st != "OK":
        ok = False
    print("  WAJIB %-20s root=%d -> %s" % (w, len(roots), st))

print("--- hantu (di luar daftar hidup) ---")
if ghost:
    for prof, rp in ghost:
        print("  HANTU: %s root_pids=%s" % (prof, rp))
else:
    print("  nol")

print("--- saksi heartbeat non-WMI (wajib) ---")
now = datetime.datetime.now(datetime.timezone.utc)
for w in wajib:
    hb = os.path.join(HOME, "profiles", w, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print("  %s: TIDAK-ADA-BERKAS" % w)
        ok = False
        continue
    try:
        data = json.load(open(hb, encoding="utf-8"))
    except Exception as e:
        print("  %s: baca-gagal %s" % (w, e))
        continue
    upd = data.get("updated_at") or data.get("ts") or ""
    age = "?"
    try:
        t = datetime.datetime.fromisoformat(str(upd).replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=datetime.timezone.utc)
        age = int((now - t).total_seconds())
        if age > 180:
            ok = False
    except Exception:
        pass
    print("  %s: pid=%s umur=%ss" % (w, data.get("pid"), age))

print("VERDICT-SWEEP: %s" % ("SEHAT" if (ok and not ghost) else "PERLU-AKSI"))
