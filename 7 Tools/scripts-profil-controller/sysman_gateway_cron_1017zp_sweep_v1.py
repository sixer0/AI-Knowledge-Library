# Ronde 17-10 zp: sapuan registri penuh + saksi heartbeat dari dump CIM mentah (tanpa query baru)
import json, os, sys, datetime

SCRIPTS = r"C:/Users/TRIAL/AppData/Local/hermes/scripts"
RAW = os.path.join(SCRIPTS, "sysman_cron_1017zp_proc_raw.json")
REG = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json"
HOME = r"C:/Users/TRIAL/AppData/Local/hermes"
SELF_PIDS = {os.getpid(), os.getppid()}

reg = json.load(open(REG, encoding="utf-8"))
live = set(reg["hidup"])
wajib = list(reg["gateway_wajib_hidup"])

raw = json.load(open(RAW, encoding="utf-8"))
if isinstance(raw, dict):
    raw = [raw]

rows = []
for p in raw:
    cl = p.get("CommandLine") or ""
    if "gateway run" not in cl:
        continue
    pid = int(p["ProcessId"])
    if pid in SELF_PIDS:
        continue
    # profil dari --profile <nama> atau default
    prof = "default"
    toks = cl.split()
    for i, t in enumerate(toks):
        if t == "--profile" and i + 1 < len(toks):
            prof = toks[i + 1]
        elif t.startswith("--profile="):
            prof = t.split("=", 1)[1]
    rows.append((pid, int(p["ParentProcessId"]), prof, str(p.get("CreationDate", ""))))

by_prof = {}
for pid, ppid, prof, cd in rows:
    by_prof.setdefault(prof, []).append((pid, ppid, cd))

pids_all = {r[0] for r in rows}
print("=== SWEEP REGISTRI (dari dump CIM ronde ini) ===")
ghost = []
for prof in sorted(by_prof):
    entries = by_prof[prof]
    roots = [e for e in entries if e[1] not in pids_all]
    tag = "DI-DAFTAR" if prof in live else ">>> DI-LUAR-DAFTAR <<<"
    if prof not in live:
        ghost.append((prof, [e[0] for e in roots]))
    print(f"  {prof:<22} proses={len(entries)} root={len(roots)} pids={[e[0] for e in entries]} {tag}")

print("--- vonis wajib ---")
ok = True
for w in wajib:
    entries = by_prof.get(w, [])
    roots = [e for e in entries if e[1] not in pids_all]
    st = "OK" if len(roots) == 1 else ("MATI" if len(entries) == 0 else f"ROOT-GANDA({len(roots)})")
    if st != "OK":
        ok = False
    print(f"  WAJIB {w:<20} root={len(roots)} -> {st}")

print("--- hantu (di luar daftar hidup) ---")
if ghost:
    for prof, rp in ghost:
        print(f"  HANTU: {prof} root_pids={rp}")
else:
    print("  nol")

print("--- saksi heartbeat non-WMI (wajib) ---")
now = datetime.datetime.now(datetime.timezone.utc)
for w in wajib:
    hb = os.path.join(HOME, "profiles", w, "state", "gateway.heartbeat")
    if not os.path.exists(hb):
        print(f"  {w}: TIDAK-ADA-BERKAS")
        continue
    try:
        data = json.load(open(hb, encoding="utf-8"))
    except Exception as e:
        print(f"  {w}: baca-gagal {e}")
        continue
    upd = data.get("updated_at") or data.get("ts") or ""
    age = "?"
    try:
        t = datetime.datetime.fromisoformat(str(upd).replace("Z", "+00:00"))
        if t.tzinfo is None:
            t = t.replace(tzinfo=datetime.timezone.utc)
        age = int((now - t).total_seconds())
    except Exception:
        pass
    print(f"  {w}: pid={data.get('pid')} umur={age}s mentah={upd}")

verdict = "SEHAT" if (ok and not ghost) else "PERLU-AKSI"
print(f"VERDICT-SWEEP: {verdict}")
