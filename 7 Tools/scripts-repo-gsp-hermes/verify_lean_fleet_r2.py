# -*- coding: utf-8 -*-
"""Verify Lean Fleet R2 — deterministic checks (no LLM judgment needed).
Writes report to docs/2026-08-29-lean-fleet/system_control_verification_r2.md
Prints final verdict line: VERDICT: PASS|NEEDS_REVIEW|FAIL
"""
import os, re, json, subprocess, datetime

LOCALAPPDATA = os.environ.get("LOCALAPPDATA", r"C:\Users\TRIAL\AppData\Local")
PROFILES = os.path.join(LOCALAPPDATA, "hermes", "profiles")
FLEET = os.path.join(LOCALAPPDATA, "hermes", "skills", "gsp")
ORCH = os.path.join(LOCALAPPDATA, "hermes", "skills", "orchestration")
WS = r"C:\Users\TRIAL\workspace\gsp-hermes\workspace"
DOCS = os.path.join(WS, "docs", "2026-08-29-lean-fleet")
REPORT = os.path.join(DOCS, "system_control_verification_r2.md")

checks = []  # (num, name, verdict, evidence_lines)

def add(n, name, verdict, ev):
    checks.append((n, name, verdict, ev))

# ---------- CHECK 1: SOUL structure across gsp-* profiles ----------
prof = sorted(d for d in os.listdir(PROFILES) if d.startswith("gsp-") and os.path.isdir(os.path.join(PROFILES, d)))
ok, no_fallback, no_always, has_ondemand = 0, [], [], []
for p in prof:
    sp = os.path.join(PROFILES, p, "SOUL.md")
    if not os.path.isfile(sp):
        no_always.append(p + ":SOUL-MISSING"); continue
    t = open(sp, encoding="utf-8", errors="replace").read()
    if "ALWAYS LOAD" not in t or "AWARENESS" not in t:
        no_always.append(p); continue
    if "ON DEMAND" in t:
        has_ondemand.append(p); continue
    if "Fallback mandiri" not in t:
        no_fallback.append(p); continue
    ok += 1
total = len(prof)
if ok == total:
    add(1, f"SOUL 48/48: ALWAYS+AWARENESS+fallback, tanpa ON DEMAND", "PASS",
        [f"ok={ok}/{total}", f"no_fallback={len(no_fallback)}", f"missing_structure={len(no_always)}", f"has_on_demand={len(has_ondemand)}"])
else:
    v = "NEEDS_REVIEW"
    add(1, f"SOUL struktur: {ok}/{total} lengkap", v,
        [f"ok={ok}/{total}", f"no_fallback={no_fallback[:8]}", f"missing={no_always[:8]}", f"on_demand={has_ondemand[:8]}"])

# ---------- CHECK 2: physical gsp skills per profile (flat gsp-* only) ----------
viol, clean, bundled_ok = [], 0, 0
for p in prof:
    sk = os.path.join(PROFILES, p, "skills")
    if not os.path.isdir(sk):
        clean += 1; continue
    gsps = [e for e in os.listdir(sk)
            if e.startswith("gsp-") and os.path.isdir(os.path.join(sk, e))
            and os.path.isfile(os.path.join(sk, e, "SKILL.md"))]
    # engine-bundled category dirs contain .bundled_manifest at skills root OR category dir lacks SKILL.md directly
    cat_dirs = [e for e in os.listdir(sk)
                if os.path.isdir(os.path.join(sk, e)) and not e.startswith(("gsp-", "."))]
    bundled = os.path.isfile(os.path.join(sk, ".bundled_manifest"))
    if bundled:
        bundled_ok += 1
    if len(gsps) > 3:
        viol.append(f"{p}={len(gsps)}")
    else:
        clean += 1
c2_pass = len(viol) == 0
add(2, f"Skill gsp fisik per profil <=3 (flat)", "PASS" if c2_pass else "NEEDS_REVIEW",
    [f"clean={clean}/{total}", f"bundled_manifest_profiles={bundled_ok}", f"violations={viol}"])

# ---------- CHECK 3: defect protocol markers ----------
def read(p):
    try:
        return open(p, encoding="utf-8", errors="replace").read()
    except Exception:
        return ""

spots = {
    "dist/fleet": (os.path.join(FLEET, "gsp-skill-distribution", "SKILL.md"), ["CHANGE REQUEST", "BUG"]),
    "dist/manager": (os.path.join(PROFILES, "gsp-skill-manager", "skills", "gsp-skill-distribution", "SKILL.md"), ["CHANGE REQUEST", "BUG"]),
    "auth/fleet": (os.path.join(FLEET, "gsp-skill-authoring", "SKILL.md"), ["CHANGE REQUEST", "BUG"]),
    "auth/creator": (os.path.join(PROFILES, "gsp-skill-creator", "skills", "gsp-skill-authoring", "SKILL.md"), ["CHANGE REQUEST", "BUG"]),
}
res3 = {}
for tag, (p, marks) in spots.items():
    t = read(p)
    res3[tag] = all(m in t for m in marks) if t else False
c3_pass = all(res3.values())
add(3, "Protokol defect di distribution+authoring (fleet & salinan profil)", "PASS" if c3_pass else "FAIL",
    [f"{k}={v}" for k, v in res3.items()])

# ---------- CHECK 4: registry integrity ----------
n_fleet = len([d for d in os.listdir(FLEET) if os.path.isdir(os.path.join(FLEET, d))]) if os.path.isdir(FLEET) else 0
orch_items = sorted(os.listdir(ORCH)) if os.path.isdir(ORCH) else []
dup_gone = "gsp-orchestrator-worker" not in orch_items and "gsp-orchestration-execution" not in orch_items
c4_pass = n_fleet >= 120 and dup_gone
add(4, f"Fleet registry >=120 ({n_fleet}); duplikat orchestration dihapus", "PASS" if c4_pass else "FAIL",
    [f"fleet_dirs={n_fleet}", f"orchestration_items={orch_items}"])

# ---------- CHECK 5: health endpoints ----------
def http_code(url):
    try:
        out = subprocess.run(["curl", "-sk", "-o", "NUL", "-w", "%{http_code}", "--max-time", "10", url],
                             capture_output=True, text=True, timeout=15).stdout.strip()
        return out
    except Exception as e:
        return f"ERR:{e}"
h1, h2, h3 = http_code("https://127.0.0.1:9011/api/agents"), http_code("https://127.0.0.1:9012"), http_code("http://127.0.0.1:8080")
c5 = (h1 == "200") and (h2 in ("200", "302")) and (h3 == "200")
add(5, "Health HQ/WebUI/Bridge", "PASS" if c5 else "FAIL", [f"9011={h1}", f"9012={h2}", f"8080={h3}"])

# ---------- CHECK 6: contract consistency ----------
contract = read(os.path.join(DOCS, "contract.md"))
c6 = ("Putaran 1" in contract) and ("Verifikasi Akhir" in contract)
add(6, "contract.md memuat rekonsiliasi Putaran 1", "PASS" if c6 else "FAIL",
    [f"has_putaran1={'Putaran 1' in contract}", f"has_verif={'Verifikasi Akhir' in contract}"])

# ---------- verdict ----------
names = {1: "PASS", 2: "PASS"}
verdicts = [c[2] for c in checks]
if all(v == "PASS" for v in verdicts):
    verdict = "PASS"
elif any(v == "FAIL" for v in verdicts):
    verdict = "FAIL"
else:
    verdict = "NEEDS_REVIEW"

now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
lines = [
    "# System Control Verification — Lean Fleet R2 (deterministik)",
    "",
    f"- **Tanggal:** {now}",
    "- **Metode:** script `scripts/verify_lean_fleet_r2.py` — checks mekanis deterministic, dieksekusi langsung.",
    f"- **Verdict:** {verdict}",
    "",
    "| # | Check | Hasil | Bukti |",
    "|---|---|---|---|",
]
for n, name, v, ev in checks:
    lines.append(f"| {n} | {name} | **{v}** | {'; '.join(ev[:4])} |")
lines += ["", "## Detail", ""]
for n, name, v, ev in checks:
    lines.append(f"### CHECK {n} — {v}")
    for e in ev:
        lines.append(f"- {e}")
    lines.append("")
lines.append("---")
lines.append(f"VERDICT: {verdict}")
os.makedirs(DOCS, exist_ok=True)
open(REPORT, "w", encoding="utf-8", newline="\n").write("\n".join(lines))
print("\n".join(f"CHECK {n}: {v} — {name}" for n, name, v, ev in checks))
print(f"REPORT: {REPORT}")
print(f"VERDICT: {verdict}")
