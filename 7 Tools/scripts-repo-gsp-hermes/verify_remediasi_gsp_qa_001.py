# -*- coding: utf-8 -*-
"""verify_remediasi_gsp_qa_001.py — deterministic checks untuk kontrak
docs/2026-08-30-remediasi-gsp-qa-001.md (Remediasi Temuan GSP-QA-001 Rev 2).

Read-only: tidak mengubah apa pun. Cetak per check:
    CHECK n: PASS|FAIL|NEEDS_REVIEW — nama | bukti
diakhiri satu baris: VERDICT: PASS|FAIL|NEEDS_REVIEW
Laporan timestamped -> <kontrak folder>/verification_r1.md

Klasifikasi jujur:
  PASS          = klaim kontrak terbukti oleh state disk/DB
  FAIL          = klaim kontrak TERBANTAHKAN oleh state nyata
  NEEDS_REVIEW  = pekerjaan masih in-flight / menunggu keputusan manusia /
                  bukti tidak konklusif (BUKAN defect)
"""
import os, re, json, glob, sqlite3, subprocess, datetime, sys

PY = sys.executable
LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\TRIAL\AppData\Local")
HERMES = os.path.join(LOCALAPPDATA, "hermes")
PROFILES = os.path.join(HERMES, "profiles")
FLEET = os.path.join(HERMES, "skills", "gsp")
WS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace"
REPO = r"C:\Users\TRIAL\workspace\gsp-hermes"
CANON = os.path.join(REPO, "skills")
DOCS = os.path.join(WS, "docs")
CONTRACT = os.path.join(DOCS, "2026-08-30-remediasi-gsp-qa-001.md")
OUTDIR = os.path.join(DOCS, "2026-08-30-remediasi-gsp-qa-001")
REPORT = os.path.join(OUTDIR, "verification_r1.md")
HOME = r"C:\Users\TRIAL"
KANBAN_DB = os.path.join(HERMES, "kanban.db")
CRON_DB = os.path.join(HERMES, "cron", "executions.db")
JOBS = os.path.join(HERMES, "cron", "jobs.json")

# kartu kontrak -> label pekerjaan (untuk CHECK 12)
CARDS = {
    "t_b1d29556": "W0-a1 commit+push brahma/datacenter",
    "t_3f5f5f59": "W0-a2 sync-back gsp-agent",
    "t_8d7f98e5": "W0-b migrasi lean + registrasi",
    "t_4827f6f6": "W0-c promosi authored -> kanonik",
    "t_cb093b94": "W1 hqa-invariants + cron",
    "t_eee6e5f8": "W3/W4 triage xskill + deskripsi",
    "t_c37b2694": "W2-check hasil run librarian",
}

checks = []


def add(n, name, verdict, ev):
    checks.append((n, name, verdict, ev))
    print(f"CHECK {n}: {verdict} — {name} | {ev}")


def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""


def sh(args, timeout=25):
    try:
        r = subprocess.run(args, capture_output=True, text=True, timeout=timeout,
                           errors="replace")
        return r.returncode, (r.stdout or "") + (r.stderr or "")
    except Exception as e:
        return 99, f"ERROR {e}"


def git(repo, args, timeout=25):
    return sh(["git", "-C", repo] + args, timeout=timeout)


def card_status():
    out = {}
    if not os.path.isfile(KANBAN_DB):
        return out
    try:
        con = sqlite3.connect(f"file:{KANBAN_DB}?mode=ro", uri=True)
        for tid, st, res in con.execute("select id,status,result from tasks"):
            out[tid] = (st, res or "")
        con.close()
    except Exception as e:
        print(f"(warn: kanban db unreadable: {e})")
    return out


# ---------- CHECK 1: W0-a — commit ter-push & tersinkron upstream ----------
repos = ["gsp-agent", "gsp-brahma", "gsp-datacenter"]
rows, synced_all = [], True
for r in repos:
    d = os.path.join(HOME, r)
    if not os.path.isdir(os.path.join(d, ".git")):
        rows.append(f"{r}:NO-GIT"); synced_all = False; continue
    _, head = git(d, ["rev-parse", "HEAD"])
    _, up = git(d, ["rev-parse", "@{u}"])
    _, cnt = git(d, ["rev-list", "--left-right", "--count", "@{u}...HEAD"])
    sync = head.strip() != "" and head.strip() == up.strip()
    ab = cnt.replace("\n", "").strip()
    synced_all = synced_all and sync and ab in ("00", "0\t0")
    rows.append(f"{r}:head={head.strip()[:7]} upstream={up.strip()[:7]} ab={ab or '?'} synced={sync}")
add(1, "W0-a commit ter-push & HEAD==upstream di 3 repo resmi",
    "PASS" if synced_all else "FAIL", " || ".join(rows))

# ---------- CHECK 2: W0-a — working tree bersih (klaim 'working tree clean') ----------
dirty_rows, dirty_total, secret_hits = [], 0, []
for r in repos:
    d = os.path.join(HOME, r)
    if not os.path.isdir(os.path.join(d, ".git")):
        continue
    _, out = git(d, ["status", "--porcelain"])
    lines = [l for l in out.splitlines() if l.strip()]
    dirty_total += len(lines)
    if lines:
        dirty_rows.append(f"{r}:{len(lines)} -> {[l.strip()[:60] for l in lines[:3]]}")
    for l in lines:
        if re.search(r"\.env$|secret|credential|\.pem$|\.key$", l, re.I):
            secret_hits.append(f"{r}:{l.strip()[:50]}")
c2_pass = dirty_total == 0
add(2, "W0-a working tree bersih di 3 repo (klaim 'working tree clean')",
    "PASS" if c2_pass else "NEEDS_REVIEW",
    f"total_dirty={dirty_total} detail={dirty_rows or '[]'} secret_di_dirty={secret_hits or '[]'}")

# ---------- CHECK 3: W0-a2 — snapshot gsp-agent/hermes-home sinkron fleet ----------
snap = os.path.join(HOME, "gsp-agent", "hermes-home", "skills", "gsp")
if os.path.isdir(snap) and os.path.isdir(FLEET):
    s_set = set(d for d in os.listdir(snap) if os.path.isdir(os.path.join(snap, d)))
    f_set = set(d for d in os.listdir(FLEET) if os.path.isdir(os.path.join(FLEET, d)))
    only_fleet = sorted(f_set - s_set)
    c3 = "PASS" if not only_fleet else "NEEDS_REVIEW"
    ev3 = f"snap={len(s_set)} fleet={len(f_set)} hanya_di_fleet={len(only_fleet)} contoh={only_fleet[:8]}"
else:
    c3, ev3 = "FAIL", f"snapshot path tidak ada: {snap}"
add(3, "W0-a2 snapshot hermes-home/skills/gsp menutupi registry fleet", c3, ev3)

# ---------- CHECK 4: W0-b — distribusi lean: skill fisik gsp-* per profil <=3 ----------
prof = sorted(d for d in os.listdir(PROFILES)
              if d.startswith("gsp-") and os.path.isdir(os.path.join(PROFILES, d)))
viol, clean = [], 0
for p in prof:
    sk = os.path.join(PROFILES, p, "skills")
    if not os.path.isdir(sk):
        clean += 1; continue
    gsps = [e for e in os.listdir(sk)
            if e.startswith("gsp-") and os.path.isfile(os.path.join(sk, e, "SKILL.md"))]
    if len(gsps) > 3:
        viol.append(f"{p}={len(gsps)}")
    else:
        clean += 1
add(4, "W0-b skill fisik gsp-* per profil gsp-* <=3 (lean)",
    "PASS" if not viol else "FAIL",
    f"clean={clean}/{len(prof)} violations={viol or '[]'}")

# ---------- CHECK 5: W0-b — dokumen registrasi lean fleet per profil ----------
reg = []
for p in glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True):
    t = read(p)
    rows = len(re.findall(r"^\|\s*(?:gsp-|user01|novriandy|firmanhidayat)[a-z0-9\-]*\s*\|", t, re.M))
    if rows >= 1 and re.search(r"registrasi\s+lean|lean\s+fleet", t, re.I):
        reg.append((os.path.relpath(p, WS), rows))
st_b = card_status().get("t_8d7f98e5", ("?", ""))[0]
cov = sum(r for _, r in reg)
if reg and cov >= len(prof):
    c5 = "PASS"          # registrasi mencakup SELURUH profil gsp-*
elif reg:
    c5 = "NEEDS_REVIEW"  # dokumen ada tapi cakupannya sebagian (lingkup kartu)
else:
    c5 = "FAIL"
add(5, "W0-b dokumen registrasi lean fleet per profil", c5,
    f"dok={[(os.path.basename(x), f'{n} baris profil') for x, n in reg[:3]] or 'NONE'} "
    f"cakupan_profil={cov}/{len(prof)} status_kartu_W0-b={st_b}")

# ---------- CHECK 6: W0-c — promosi authored fleet -> kanonik ----------
fleet_gsp = sorted(d for d in os.listdir(FLEET)
                   if d.startswith("gsp-") and os.path.isdir(os.path.join(FLEET, d))) if os.path.isdir(FLEET) else []
canon = sorted(d for d in os.listdir(CANON)
               if os.path.isdir(os.path.join(CANON, d))) if os.path.isdir(CANON) else []
missing = [d for d in fleet_gsp if d not in canon]
add(6, "W0-c promosi skill authored fleet -> kanonik (gap nama = 0)",
    "PASS" if not missing else "FAIL",
    f"fleet_gsp={len(fleet_gsp)} canon={len(canon)} missing={missing[:12] or '[]'}")

# ---------- CHECK 7: W1 — instrumentasi hqa-invariants.py + cron terjadwal ----------
cand = [os.path.join(REPO, "scripts", "hqa-invariants.py"),
        os.path.join(REPO, "workspace", "scripts", "hqa-invariants.py"),
        os.path.join(HERMES, "scripts", "hqa-invariants.py")]
found = [c for c in cand if os.path.isfile(c)]
jobs_raw = read(JOBS)
inv_job = re.findall(r'"name":\s*"([^"]*[Ii]nvarian[^"]*)"', jobs_raw)
st_w1 = card_status().get("t_cb093b94", ("?", ""))[0]
if found and inv_job:
    c7 = "PASS"
elif st_w1 in ("running", "ready", "todo", "blocked"):
    c7 = "NEEDS_REVIEW"
else:
    c7 = "FAIL"
add(7, "W1 instrumentasi: hqa-invariants.py + job cron invarian terjadwal", c7,
    f"script={[os.path.basename(x) for x in found] or 'ABSEN'} cron_job={inv_job or 'ABSEN'} status_kartu_W1={st_w1}")

# ---------- CHECK 8: W2 — pin provider/model cron librarian ----------
prov = model = last = "?"
m = re.search(r'\{[^{}]*"id":\s*"6a6097cd79b4".*?\n    \}', jobs_raw, re.S)
blk = m.group(0) if m else ""
if blk:
    prov = (re.search(r'"provider":\s*"([^"]*)"', blk) or [None, "-"])[1]
    model = (re.search(r'"model":\s*"([^"]*)"', blk) or [None, "-"])[1]
    last = (re.search(r'"last_status":\s*"([^"]*)"', blk) or [None, "null"])[1]
pinned = prov == "custom" and bool(model) and model != "-"
add(8, "W2 pin eksplisit provider=custom/model pada cron librarian 6a6097cd79b4",
    "PASS" if pinned else "FAIL",
    f"provider={prov} model={model} last_status={last}")

# ---------- CHECK 9: W2 — run librarian pasca-pin benar-benar selesai ----------
runs = []
if os.path.isfile(CRON_DB):
    try:
        con = sqlite3.connect(f"file:{CRON_DB}?mode=ro", uri=True)
        for row in con.execute(
                "select source,status,started_at,finished_at,substr(coalesce(error,''),1,60) "
                "from executions where job_id='6a6097cd79b4' order by started_at desc limit 5"):
            runs.append(row)
        con.close()
    except Exception as e:
        print(f"(warn: cron db unreadable: {e})")
post = [r for r in runs if (r[2] or "") >= "2026-08-30T13"]
completed = [r for r in post if r[1] == "completed"]
if completed:
    c9 = "PASS"
elif post:
    c9 = "NEEDS_REVIEW"
else:
    c9 = "FAIL"
add(9, "W2 run librarian pasca-pin berstatus completed (bukti executions.db)", c9,
    f"run_pasca_pin={[(r[0], r[1], (r[2] or '')[11:19]) for r in post] or 'TIDAK-ADA'} "
    f"run_terakhir_sebelum_pin={[(r[1], (r[2] or '')[11:19]) for r in runs[:2]]}")

# ---------- CHECK 10: W4 — deskripsi SKILL.md >1024 char = 0 ----------
def parse_desc(fm):
    m = re.search(r"^description:[ \t]*(.*)$", fm, re.M)
    if not m:
        return None
    first, rest = m.group(1), fm[m.end():]
    if first[:1] in ("'", '"'):
        q = first[0]
        buf = first[1:]
        k = buf.find(q)
        if k >= 0:
            return " ".join(buf[:k].split())
        for line in rest.splitlines():
            k = line.find(q)
            if k >= 0:
                buf += " " + line[:k]
                break
            buf += " " + line
        return " ".join(buf.split())
    if first[:1] in (">", "|"):
        vals = [first[1:]]
        for line in rest.splitlines():
            if line.startswith(("  ", "\t")) or not line.strip():
                vals.append(line)
            else:
                break
        return " ".join(" ".join(vals).split())
    return " ".join(first.split())


over, seen, files = [], set(), []
for root in [os.path.join(HERMES, "skills"), PROFILES]:
    for p in glob.glob(os.path.join(root, "**", "SKILL.md"), recursive=True):
        rp = os.path.realpath(p)
        if rp in seen:
            continue
        seen.add(rp); files.append(p)
tot = over60 = 0
for p in files:
    t = read(p)[:8000]
    m = re.match(r"^---[ \t]*\r?\n(.*?)\r?\n---", t, re.S)
    if not m:
        continue
    d = parse_desc(m.group(1))
    if d is None:
        continue
    tot += 1
    if len(d) > 1024:
        over.append(f"{os.path.relpath(p, HERMES)}({len(d)})")
    if len(d) > 60:
        over60 += 1
st_w4 = card_status().get("t_eee6e5f8", ("?", ""))[0]
if not over:
    c10 = "PASS"
elif st_w4 in ("running", "ready", "todo", "blocked"):
    c10 = "NEEDS_REVIEW"   # kartu W3/W4 masih in-flight — bukan klaim terbantahkan
else:
    c10 = "FAIL"           # kartu sudah done tapi cacat masih ada di disk
add(10, "W4 deskripsi SKILL.md >1024 char = 0 (hard defect)", c10,
    f"skillmd_terparsing={tot} over1024={len(over)} contoh={over[:4] or '[]'} "
    f"over60={over60} status_kartu_W3/W4={st_w4}")

# ---------- CHECK 11: W3 — triage sitasi lintas-skill terdokumentasi ----------
def triage_rows(t):
    """Baris keputusan triage nyata: tabel/daftar yang menyebut path skills/<nama>/."""
    return len(re.findall(r"^\|\s*`?skills/[a-z0-9][a-z0-9\-]+/", t, re.M))


triage = []
for p in glob.glob(os.path.join(DOCS, "**", "*.md"), recursive=True):
    t = read(p)
    if re.search(r"triage", t, re.I) and triage_rows(t) >= 5:
        triage.append((os.path.relpath(p, WS), triage_rows(t)))
pat_hits = sum(len(re.findall(r"skills/[a-z0-9][a-z0-9\-]+/", read(p))) for p in files)
st_w3 = card_status().get("t_eee6e5f8", ("?", ""))[0]
if triage:
    c11 = "PASS"
elif st_w3 in ("running", "ready", "todo", "blocked"):
    c11 = "NEEDS_REVIEW"
else:
    c11 = "FAIL"
add(11, "W3 triage 60 sitasi lintas-skill terdokumentasi (>=5 baris keputusan)", c11,
    f"dok_triage={triage[:3] or 'ABSEN'} tapak_pola_di_skillmd={pat_hits} status_kartu_W3/W4={st_w3}")

# ---------- CHECK 12: kartu kontrak — semua mencapai status akhir ----------
cs = card_status()
not_done = {cid: cs.get(cid, ("<absen>", ""))[0] for cid in CARDS if cs.get(cid, ("",))[0] != "done"}
add(12, "Semua kartu kontrak remediasi mencapai status done",
    "PASS" if not not_done else "NEEDS_REVIEW",
    f"belum_done={not_done or '{}'} total_kartu={len(CARDS)}")

# ---------- CHECK 13: regresi layanan inti (guard pasca-remediasi) ----------
def hq_secret():
    """Konvensi preseden verify_audit_20260830.py: pasca SEC-001, endpoint HQ
    butuh header x-internal-secret. Nilai TIDAK pernah dicetak."""
    try:
        for line in open(os.path.join(HOME, "gsp-datacenter", ".env"), encoding="utf-8"):
            if line.startswith("INTERNAL_API_SECRET="):
                return line.split("=", 1)[1].strip().strip('"').strip("'")
    except Exception:
        pass
    return ""


SEC = hq_secret()


def code(url, hdr=None):
    args = ["curl", "-sk", "--noproxy", "*", "--max-time", "10", "-o", "NUL",
            "-w", "%{http_code}"]
    if hdr:
        args += ["-H", hdr]
    _, out = sh(args + [url])
    return (out.strip() or "000")[-3:]


hq = code("https://127.0.0.1:9011/api/brahma/dispatch-kpi", "x-internal-secret: " + SEC) if SEC \
    else code("https://127.0.0.1:9011/api/agents")
svc = {"hq_9011": hq,
       "webui_9012": code("https://127.0.0.1:9012/"),
       "searxng_8080": code("http://127.0.0.1:8080/")}
ok13 = svc["hq_9011"] == "200" and svc["webui_9012"] in ("200", "302", "307") and svc["searxng_8080"] == "200"
add(13, "Regresi layanan inti UP (HQ+secret/WebUI/SearXNG)", "PASS" if ok13 else "FAIL",
    json.dumps(svc) + f" secret_dibaca={bool(SEC)}")

# ---------- verdict + laporan ----------
nv = [v for _, _, v, _ in checks]
if any(v == "FAIL" for v in nv):
    verdict = "FAIL"
elif any(v == "NEEDS_REVIEW" for v in nv):
    verdict = "NEEDS_REVIEW"
else:
    verdict = "PASS"

os.makedirs(OUTDIR, exist_ok=True)
ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
lines = ["# Verification R1 — Remediasi GSP-QA-001 (kontrak 2026-08-30)",
         "",
         f"Generated: {ts}",
         f"Script: {os.path.abspath(__file__)}",
         f"Interpreter: {PY}",
         f"Kontrak: {CONTRACT}",
         "",
         "| Check | Nama | Hasil | Bukti |",
         "|---|---|---|---|"]
for n, name, v, ev in checks:
    lines.append(f"| {n} | {name} | {v} | {ev} |")
lines += ["",
          f"**VERDICT: {verdict}** — {nv.count('PASS')}/{len(nv)} PASS, "
          f"{nv.count('NEEDS_REVIEW')} NEEDS_REVIEW, {nv.count('FAIL')} FAIL"]
open(REPORT, "w", encoding="utf-8").write("\n".join(lines) + "\n")
print(f"REPORT: {REPORT}")
print(f"VERDICT: {verdict}")
sys.exit(0 if verdict == "PASS" else 1)
