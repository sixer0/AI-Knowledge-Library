# sysman cron 15-10 ronde b: hasilkan artefak daftar 33 induk tersingkir VBCB (read-only DB -> tulis md)
import sqlite3, time, re, os

DB = r"C:/Users/TRIAL/AppData/Local/hermes/kanban.db"
NOW = int(time.time())
OUT = r"C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-10-15_mission-wake-vbcb-stalled/daftar-induk-tersingkir.md"
os.makedirs(os.path.dirname(OUT), exist_ok=True)
con = sqlite3.connect(DB); con.row_factory = sqlite3.Row

rows = []
kids = [r["id"] for r in con.execute(
    "SELECT id FROM tasks WHERE tenant='VIBE-BIBLE-1013' AND status='todo' ORDER BY id").fetchall()]
for k in kids:
    t = con.execute("SELECT title FROM tasks WHERE id=?", (k,)).fetchone()
    ps = con.execute("SELECT parent_id FROM task_links WHERE child_id=?", (k,)).fetchall()
    oldp = newp = None
    for pr in ps:
        p = con.execute("SELECT id,status,title FROM tasks WHERE id=?", (pr["parent_id"],)).fetchone()
        if not p: continue
        if p["status"] == "blocked": oldp = p
        elif p["status"] == "done": newp = p
    dig = None
    if oldp:
        for c in con.execute("SELECT body FROM task_comments WHERE task_id=? ORDER BY created_at", (oldp["id"],)):
            m = re.search(r"Digantikan\s+(t_[0-9a-f]{8})", c["body"] or "")
            if m: dig = m.group(1)
    ev = con.execute("SELECT created_at FROM task_events WHERE task_id=? ORDER BY created_at DESC LIMIT 1", (oldp["id"],)).fetchone() if oldp else None
    rows.append((k, (t["title"] or "").replace("[VBCB]","").strip(),
                 oldp["id"] if oldp else "-", oldp["status"] if oldp else "-",
                 round((NOW-ev["created_at"])/60.0) if ev else "-",
                 newp["id"] if newp else "-", newp["status"] if newp else "-",
                 dig or "-"))

with open(OUT, "w", encoding="utf-8") as f:
    f.write("# Daftar 33 induk tersingkir VIBE-BIBLE-1013 (signature parent-tersingkir)\n\n")
    f.write("Diukur cron mission-wake sysman %s (epoch %d). Sumber: kanban.db root, read-only.\n\n" % (time.strftime("%Y-%m-%d %H:%M"), NOW))
    f.write("Kondisi: setiap kartu verifikasi (todo) punya dua orang tua; orang tua penulis lama berstatus blocked dengan komentar `Digantikan ... (M4 rebuild)`, sedangkan orang tua pengganti [M4] sudah done. Kernel tidak pernah mempromosikan anak ber-two-parent selama satu orang tuanya masih blocked.\n\n")
    f.write("| anak verifikasi (todo) | judul | induk blocked | umur evt (mnt) | pengganti done | status pengganti | target komentar Digantikan |\n")
    f.write("|---|---|---|---|---|---|---|\n")
    for r in rows:
        f.write("| %s | %s | %s | %s | %s | %s | %s |\n" % (r[0], r[1], r[2], r[3], r[5], r[6], r[7]))
    n_ok = sum(1 for r in rows if r[7] == r[5] and r[6] == "done")
    f.write("\nCocok silang: %d dari %d baris punya komentar Digantikan yang menunjuk persis ke orang tua done.\n" % (n_ok, len(rows)))
print("ditulis=%s baris=%s cocok=%s" % (OUT, len(rows), n_ok))
