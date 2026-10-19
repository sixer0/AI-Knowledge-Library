# Ronde 17-10 rf: sapuan registri penuh SEGAR (satu lintasan CIM sendiri) + saksi heartbeat
import json, os, subprocess, datetime, collections

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
REG = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
SELF_PIDS = {os.getpid(), os.getppid()}
TOOL_TOKENS = ("sweep", "audit", "monitor", "probe", "rootage", "witness", "broadsweep", "ghostcheck")

reg = json.load(open(REG, encoding="utf-8"))
live = set(reg["hidup"])
wajib = list(reg["gateway_wajib_hidup"])

PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
q = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe' OR Name='hermes.exe'\" "
     "| Select-Object ProcessId,ParentProcessId,CreationDate,Name,CommandLine | ConvertTo-Json -Compress")
t0 = datetime.datetime.now()
rc = None
raw = None
for attempt in (1, 2):
    p = subprocess.run([PS, "-NoProfile", "-NonInteractive", "-Command", q],
                       capture_output=True, text=True, timeout=150)
    rc = p.returncode
    if rc == 0 and p.stdout.strip():
        raw = json.loads(p.stdout)
        break
    print(f"PERINGATAN: lintasan CIM percobaan {attempt} rc={rc} err={p.stderr.strip()[:200]}")
dt = (datetime.datetime.now() - t0).total_seconds()
if raw is None:
    print(f"LINTASAN-BUTA: CIM gagal dua kali rc={rc} dalam {dt:.0f} dtk -> vonis TIDAK BISA dibuat")
    raise SystemExit(2)
if isinstance(raw, dict):
    raw = [raw]
print(f"CIM satu lintasan: {len(raw)} proses berfilter nama dalam {dt:.0f} dtk")

rows = []
mine = []
for pr in raw:
    cl = pr.get("CommandLine") or ""
    pid = int(pr["ProcessId"])
    if pid in SELF_PIDS:
        mine.append(("self", pid))
        continue
    if any(tok in cl.lower() for tok in TOOL_TOKENS):
        mine.append(("tool", pid, cl[:70]))
        continue
    if "gateway run" not in cl:
        mine.append(("nonrun", pid, cl[:70]))
        continue
    prof = "default"
    toks = cl.split()
    for i, t in enumerate(toks):
        if t == "--profile" and i + 1 < len(toks):
            prof = toks[i + 1]
        elif t.startswith("--profile="):
            prof = t.split("=", 1)[1]
    rows.append((pid, int(pr["ParentProcessId"]), prof))

pids_all = {r[0] for r in rows}
by_prof = collections.defaultdict(list)
for pid, ppid, prof in rows:
    by_prof[prof].append((pid, ppid))

print("--- profil ber-gateway vs registri ---")
ghost = []
for prof in sorted(by_prof):
    entries = by_prof[prof]
    roots = [e for e in entries if e[1] not in pids_all]
    tag = "DI-DAFTAR" if prof in live else ">>> DI-LUAR-DAFTAR <<<"
    if prof not in live:
        ghost.append((prof, [e[0] for e in roots]))
    print(f"  {prof:<22} proses={len(entries)} root={len(roots)} pids={[e[0] for e in entries]} {tag}")

print("--- registri hidup tanpa gateway (normal utk profil manusia/manager) ---")
print("  " + ", ".join(sorted(live - set(by_prof))))

print("--- vonis wajib ---")
ok = True
for w in wajib:
    entries = by_prof.get(w, [])
    roots = [e for e in entries if e[1] not in pids_all]
    st = "OK" if len(roots) == 1 else ("MATI" if not entries else f"ROOT-GANDA({len(roots)})")
    ok = ok and st == "OK"
    print(f"  WAJIB {w:<20} root={len(roots)} -> {st}")

print("--- hantu (gateway di luar daftar hidup) ---")
print("  nol" if not ghost else "\n".join(f"  HANTU: {p} root_pids={r}" for p, r in ghost))

print("--- saksi heartbeat non-WMI (wajib) ---")
now = datetime.datetime.now(datetime.timezone.utc)
for w in wajib:
    hb = os.path.join(HOME, "profiles", w, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print(f"  {w}: TIDAK-ADA-BERKAS")
        continue
    data = json.load(open(hb, encoding="utf-8"))
    upd = data.get("updated_at") or data.get("ts") or ""
    age = "?"
    try:
        t = datetime.datetime.fromisoformat(str(upd).replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=datetime.timezone.utc)
        age = int((now - t).total_seconds())
    except Exception:
        pass
    print(f"  {w}: pid={data.get('pid')} umur={age}s")

print("--- proses tersaring (bukti self-exclude bekerja) ---")
for m in mine:
    print("  " + " ".join(str(x) for x in m))

print(f"VERDICT-SWEEP: {'SEHAT' if (ok and not ghost) else 'PERLU-AKSI'}")
