# Ronde 17-10 rf: umur akar gateway wajib (satu lintasan CIM) sebagai bukti kontinuitas
import json, os, subprocess, datetime

SELF = {os.getpid(), os.getppid()}
PS = r"C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe"
q = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" "
     "| Select-Object ProcessId,ParentProcessId,CreationDate,CommandLine | ConvertTo-Json -Compress")
p = subprocess.run([PS, "-NoProfile", "-NonInteractive", "-Command", q],
                   capture_output=True, text=True, timeout=150)
if p.returncode != 0 or not p.stdout.strip():
    print(f"LINTASAN-BUTA rc={p.returncode} err={p.stderr.strip()[:200]}")
    raise SystemExit(2)
raw = json.loads(p.stdout)
if isinstance(raw, dict):
    raw = [raw]

now = datetime.datetime.now(datetime.timezone.utc)
rows = []
for pr in raw:
    cl = pr.get("CommandLine") or ""
    pid = int(pr["ProcessId"])
    if pid in SELF or "gateway run" not in cl or any(
            t in cl.lower() for t in ("sweep", "audit", "monitor", "probe")):
        continue
    prof = "default"
    toks = cl.split()
    for i, t in enumerate(toks):
        if t == "--profile" and i + 1 < len(toks):
            prof = toks[i + 1]
        elif t.startswith("--profile="):
            prof = t.split("=", 1)[1]
    cd = str(pr.get("CreationDate", ""))
    age_h = -1
    if "/Date(" in cd:
        ms = int(cd.split("/Date(")[1].split(")")[0].lstrip("+"))
        age_h = (now.timestamp() * 1000 - ms) / 3600000.0
    else:
        try:
            t = datetime.datetime.fromisoformat(cd.replace("Z", "+00:00"))
            if t.tzinfo is None:
                t = t.replace(tzinfo=datetime.timezone.utc)
            age_h = (now - t).total_seconds() / 3600.0
        except Exception:
            pass
    rows.append((pid, int(pr["ParentProcessId"]), prof, age_h))

pids = {r[0] for r in rows}
print(f"CIM: {len(raw)} baris, {len(rows)} proses 'gateway run' terhitung")
for w in ("gsp-thinker", "gsp-worker", "gsp-worker-fast"):
    ent = [r for r in rows if r[2] == w]
    roots = [r for r in ent if r[1] not in pids]
    print(f"  WAJIB {w:<16} root={len(roots)} umur_akar={[round(r[3],1) for r in roots]} jam")
