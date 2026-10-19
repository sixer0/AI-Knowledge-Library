# Jejak tool-call sesi induk & anak: kanal spawn RT + kanal penutup kartu
import sqlite3, json, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gspuser02/state.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

for sid in ("20261018_070053_5932f2", "20261018_070141_c8f61c"):
    print("="*70)
    print("SESSION", sid)
    s = con.execute("SELECT source,profile_name,parent_session_id,cwd FROM sessions WHERE id=?", (sid,)).fetchone()
    print("meta:", dict(s) if s else None)
    for r in con.execute(
        "SELECT id,role,tool_name,tool_calls,substr(content,1,300) c,timestamp,effect_disposition "
        "FROM messages WHERE session_id=? ORDER BY id", (sid,)):
        ts = time.strftime('%H:%M:%S', time.localtime(r['timestamp'])) if r['timestamp'] else '?'
        if r['tool_calls']:
            try:
                tcs = json.loads(r['tool_calls'])
                names = [t.get('function',{}).get('name') or t.get('name') for t in tcs]
                args = []
                for t in tcs:
                    a = t.get('function',{}).get('arguments') or t.get('arguments') or ''
                    args.append((a[:260]).replace('\n','\\n'))
                print(f"{ts} msg#{r['id']} role={r['role']} TOOL_CALL names={names}")
                for a in args:
                    print(f"      args={a}")
            except Exception as e:
                print(ts, "msg#", r['id'], "parse-err", e, r['tool_calls'][:200])
        elif r['role'] == 'tool':
            print(f"{ts} msg#{r['id']} role=tool name={r['tool_name']} resp={r['c']!r}")
