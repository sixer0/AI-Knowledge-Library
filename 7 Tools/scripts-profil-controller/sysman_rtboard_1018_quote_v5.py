# Kutip pesan kunci anak RT untuk laporan traceroot (verbatim, terpotong aman)
import sqlite3, json

DB = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gspuser02/state.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

def args_of(msg_id):
    r = con.execute("SELECT tool_calls FROM messages WHERE id=?", (msg_id,)).fetchone()
    tcs = json.loads(r['tool_calls'])
    out = []
    for t in tcs:
        fn = t.get('function', {})
        out.append((fn.get('name'), fn.get('arguments') or ''))
    return out

for mid in (54011, 54026):
    for nm, a in args_of(mid):
        print(f"--- msg {mid} ({nm}) ---")
        print(a[:900])
        print()

for mid in (54012, 54027):
    r = con.execute("SELECT tool_name, content FROM messages WHERE id=?", (mid,)).fetchone()
    print(f"--- resp {mid} [{r['tool_name']}] ---")
    print(r['content'][:300])
    print()
