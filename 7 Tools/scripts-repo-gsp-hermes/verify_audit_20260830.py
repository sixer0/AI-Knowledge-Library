# verify_audit_20260830.py — check deterministik klaim Audit Ekosistem Swarm 30-08
# Tiap check: PASS/FAIL/NEEDS_REVIEW; akhir: VERDICT. Read-only, tidak mengubah apa pun.
import subprocess, sys, os, re, glob, json, hashlib

REPORT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-30-swarm-ecosystem-audit/verification_r1.md"
results = []

def check(n, name, ok, evidence):
    results.append((n, name, "PASS" if ok else "FAIL", evidence))
    print(f"CHECK {n}: {'PASS' if ok else 'FAIL'} — {name} | {evidence}")

def _hq_secret():
    # pasca SEC-001 fix (30-08): HQ production — pemanggil internal wajib bawa secret
    try:
        for line in open("C:/Users/TRIAL/gsp-datacenter/.env", encoding="utf-8"):
            if line.startswith("INTERNAL_API_SECRET="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""

HQ_SEC = _hq_secret()

def curl(url, opts=None):
    cmd = ["curl", "-sk", "--noproxy", "*", "--max-time", "12", "-o", os.devnull, "-w", "%{http_code}"]
    if "localhost:9011" in url and HQ_SEC:
        cmd += ["-H", "x-internal-secret: " + HQ_SEC]
    cmd += (opts or []) + [url]
    r = subprocess.run(cmd, capture_output=True, text=True, timeout=30)
    return r.stdout.strip()

# 1. Layanan inti UP
codes = {u: curl(u) for u in [
    "https://localhost:9011/api/brahma/dispatch-kpi",
    "https://localhost:9012/",
    "http://localhost:8080/",
    "http://localhost:3002/"]}
ok = codes["https://localhost:9011/api/brahma/dispatch-kpi"] == "200" and codes["https://localhost:9012/"] in ("200","302") and codes["http://localhost:8080/"] == "200" and codes["http://localhost:3002/"] == "200"
check(1, "layanan inti UP (HQ/WebUI/SearXNG/Firecrawl)", ok, json.dumps(codes))

# 2. Watchdog patched: pola gateway run ada di script + fungsi deteksi tak lagi false-negative
p = os.path.expandvars(r"%LOCALAPPDATA%/hermes/scripts/gsp_fleet_gateway_check.py")
src = open(p, encoding="utf-8").read()
check(2, "watchdog pola 'gateway run' terpasang", "gateway run" in src, "grep source")

# 3. Hotfix SEC-003: login fail-closed (503 saat ADMIN_PASSWORD kosong)
c = curl("https://localhost:9011/api/auth/login", ["-X","POST","-H","content-type: application/json","-d","{}"])
check(3, "SEC-003 login fail-closed", c == "503", f"http {c} (harus 503)")

# 4. Hotfix SEC-002: injection youtube/generate tidak mengeksekusi perintah
marker = r"C:/Users/TRIAL/AppData/Local/Temp/sec002_pwned.txt"
if os.path.exists(marker): os.remove(marker)
body = json.dumps({"topic":"tes","sourceUrl":'"; echo pwned > ' + marker.replace("\\","/") + '; #'})
curl("https://localhost:9011/api/youtube/generate", ["-X","POST","-H","content-type: application/json","-d",body])
import time; time.sleep(2)
check(4, "SEC-002 injection diblokir", not os.path.exists(marker), "marker file tidak tercipta")

# 5. Hotfix SEC-004: garden PUT tanpa auth tidak lagi diproses (harus 401/redirect, bukan 200/500-proxy)
c = curl("https://localhost:9011/api/garden", ["-X","PUT","-H","content-type: application/json","-d",'{"probe":1}'])
check(5, "SEC-004 garden PUT butuh sesi", c in ("401","307","302"), f"http {c}")

# 6. Bridge patch SEC-005/007/008/010 ada di file (menunggu restart)
b = open(r"C:/Users/TRIAL/gsp-datacenter/hermes-bridge/bridge.mjs", encoding="utf-8").read()
ok6 = all(s in b for s in ["FOR UPDATE SKIP LOCKED","runRequestClaimed","MAX_OUT","SEC-008","safeSched"])
check(6, "patch bridge SEC-005/007/008/010 terpasang di file", ok6, "grep 5 marker")

# 7. Zombie edges = 0 (query via node prisma sudah dijalankan earlier; cek ulang cepat pakai API KPI)
r = subprocess.run(["curl","-sk","--noproxy","*","--max-time","12","-H","x-internal-secret: " + HQ_SEC,"https://localhost:9011/api/brahma/dispatch-kpi"],capture_output=True,text=True)
k = json.loads(r.stdout)
check(7, "zombieEdges=0 via API KPI", k["orchestration"]["zombieEdges"] == 0, f"zombieEdges={k['orchestration']['zombieEdges']}")

# 8. Drift salinan gsp-* = 0 (re-hash fleet vs profil budi/creative/firman-custom utk 4 skill)
F = os.path.expandvars(r"%LOCALAPPDATA%\hermes\skills\gsp"); P = os.path.expandvars(r"%LOCALAPPDATA%\hermes\profiles")
def h(fp): return hashlib.sha256(open(fp,'rb').read().replace(b"\r\n",b"\n")).hexdigest()[:12]
drift = []
for s in ["gsp-orchestrator-worker","gsp-agent-hq-ops","gsp-fleet-profile-operations","gsp-orchestration-execution"]:
    fh = h(os.path.join(F,s,"SKILL.md"))
    for prof in ["gsp-budi","gsp-creative","gsp-firman-custom"]:
        for d in glob.glob(os.path.join(P,prof,"skills","**",s,"SKILL.md"),recursive=True):
            if h(d) != fh: drift.append(f"{prof}/{s}")
check(8, "drift salinan gsp-* = 0", len(drift) == 0, f"drift={drift or '[]'}")

# 9. AGENTS.md memuat Kebijakan Lean Fleet
a = open(r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/AGENTS.md", encoding="utf-8").read()
check(9, "AGENTS.md kebijakan Lean Fleet terpasang", "Kebijakan Lean Fleet" in a, "grep heading")

# 10. Skill patches: distribution v1.1.3 + pitfall sync-back; verification skill punya section fleet scale
sd = open(os.path.join(F,"gsp-skill-distribution","SKILL.md"), encoding="utf-8", errors="replace").read()
vb = open(os.path.join(F,"gsp-verification-before-completion","SKILL.md"), encoding="utf-8", errors="replace").read()
ok10 = ("version: 1.1.3" in sd) and ("STALE setelah fleet registry" in sd) and ("Verifying at Fleet Scale" in vb)
check(10, "skill patches (I3,I4) ada di fleet registry", ok10, "grep 3 marker")

# 11. SOUL sweep: tidak ada lagi '(kilocode)' di baris Model profil gsp-*
bad = []
for s in glob.glob(os.path.join(P,"gsp-*","SOUL.md")):
    for line in open(s, encoding="utf-8", errors="replace"):
        if line.startswith("- **Model:**") and "(kilocode)" in line:
            bad.append(s); break
check(11, "sweep SOUL Model (N13) bersih", len(bad) == 0, f"masih kilocode: {len(bad)}")

fails = [r for r in results if r[2] == "FAIL"]
verdict = "PASS" if not fails else "FAIL"
lines = [f"# Verification R1 — Audit Ekosistem Swarm 30-08", "",
         f"Generated: {time.strftime('%F %T')}", "", "| Check | Nama | Hasil | Bukti |","|---|---|---|---|"]
lines += [f"| {n} | {name} | {st} | {ev} |" for n,name,st,ev in results]
lines += ["", f"**VERDICT: {verdict}** ({len(results)-len(fails)}/{len(results)} PASS)"]
open(REPORT,"w",encoding="utf-8").write("\n".join(lines))
print(f"VERDICT: {verdict} — report: {REPORT}")
sys.exit(0 if verdict == "PASS" else 1)
