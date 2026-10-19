# Isi pesan sesi anak RT: tool call delegate_task penuh + aksi papan yang dilakukan anak
import sqlite3, json, time

DB = r"C:/Users/TRIAL/AppData/Local/hermes/profiles/gspuser02/state.db"
con = sqlite3.connect(f"file:{DB}?mode=ro", uri=True)
con.row_factory = sqlite3.Row

# 1) argumen delegate_task penuh dari induk
r = con.execute("SELECT id,content,tool_calls FROM messages WHERE session_id='20261018_070053_5932f2' AND id=53995").fetchone()
tcs = json.loads(r['tool_calls'])
for t in tcs:
    fn = t.get('function',{})
    if (fn.get('name') or t.get('name')) == 'delegate_task':
        args = fn.get('arguments') or t.get('arguments')
        print("== delegate_task args penuh ==")
        print(args[:3000])
        print()

# 2) semua pesan anak
print("== SESI ANAK 20261018_070141_c8f61c ==")
for r in con.execute(
    "SELECT id,role,tool_name,tool_calls,substr(content,1,400) c,timestamp FROM messages "
    "WHERE session_id='20261018_070141_c8f61c' ORDER BY id"):
    ts = time.strftime('%H:%M:%S', time.localtime(r['timestamp'])) if r['timestamp'] else '?'
    if r['tool_calls']:
        try:
            tcs = json.loads(r['tool_calls'])
            for t in tcs:
                fn = t.get('function',{})
                nm = fn.get('name') or t.get('name')
                a = (fn.get('arguments') or t.get('arguments') or '')[:400].replace('\n','\\n')
                print(f"{ts} msg#{r['id']} CALL {nm} args={a}")
        except Exception as e:
            print(ts, "parse-err", e)
    elif r['role'] == 'tool':
        print(f"{ts} msg#{r['id']} RESP[{r['tool_name']}] {r['c']!r}")
    elif r['role'] == 'assistant':
        print(f"{ts} msg#{r['id']} ASST {r['c']!r}")
    else:
        print(f"{ts} msg#{r['id']} {r['role'].upper()} {r['c']!r}")
