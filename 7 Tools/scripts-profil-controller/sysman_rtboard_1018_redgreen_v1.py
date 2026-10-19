# Uji merah-hijau mandat 2 pada salinan DB: marker set -> PermissionError; env -u -> ACKED
import shutil, sqlite3, subprocess, sys, os

SRC = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
DST = r"C:/Users/TRIAL/AppData/Local/Temp/sysman_1018_delegwatch_fixture.db"
SCRIPT = r"C:/Users/TRIAL/AppData/Local/hermes/scripts/gsp_deleg_watch.py"
UV = r"C:/Users/TRIAL/AppData/Local/hermes/bin/uv"

shutil.copy2(SRC, DST)
tid = "t_63b993df"

def run(label, extra_env):
    env = dict(os.environ)
    env["DELEG_WATCH_DB"] = DST
    env.update(extra_env)
    p = subprocess.run(
        [UV, "run", "--python", "3.11", "--no-project", "--with", "pyyaml",
         "python", SCRIPT, "ack-post", tid, "--by", "gsp-system-manager",
         "--proxy", "--note", "UJI-MERAH-HIJAU (fixture, bukan produksi)"],
        capture_output=True, text=True, env=env, timeout=180)
    tail = (p.stdout.strip().splitlines() or [""])[-1]
    err_tail = (p.stderr.strip().splitlines() or [""])[-1]
    print(f"[{label}] rc={p.returncode} out={tail!r} err={err_tail[:120]!r}")
    return p.returncode, p.stdout + p.stderr

rc_red, out_red = run("MERAH marker=1", {"HERMES_DELEGATED_CHILD_CONTEXT": "1"})
ok_red = "PermissionError" in out_red and rc_red != 0
rc_green, out_green = run("HIJAU env bersih", {})
ok_green = "ACKED" in out_green and rc_green == 0

con = sqlite3.connect(DST)
n = con.execute("SELECT COUNT(*) FROM task_comments WHERE task_id=? AND body LIKE '%UJI-MERAH-HIJAU%'", (tid,)).fetchone()[0]
con.close()
print(f"komentar-uji-di-fixture={n}")
print("VERDICT:", "PASS" if (ok_red and ok_green and n == 1) else "FAIL")
