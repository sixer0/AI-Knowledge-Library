// hq_route_adint_close2.cjs - rekonsiliasi kartu kontrak ADINT via SQLite kanban.db (kernel)
const Database = require('better-sqlite3');
const path = require('path');
const dbPath = 'C:\\Users\\TRIAL\\AppData\\Local\\hermes\\kanban.db';
const db = new Database(dbPath);

const resultText = 'ADINT-DEEPDIVE-0909 selesai: paper master 02-PAPER-MASTER.md 233626 B (15 bab per-subsistem) dari baseline 10 berkas (sha16 register 10/10 cocok REGIST-BASELINE) + enrichment 9 jalur ~251 KB ladder 8 kelas; verifikasi tiga lapis PASS (lokal 12/12 VERIFIKASI-LOKAL.md; countersign independen AGREE COUNTERSIGN-D5.md deleg_b565ec09; mekanik verifier 1119 sitasi/25 kode verification/_mechanical_report.txt); commit+push pointer 05d7a618 gsp-agent main';
const ids = ['t_0c843036', 't_1f7ad3b6', 't_acdfe175', 't_786ad2ab', 't_2259da52', 't_e7a284eb', 't_4547de2c'];

const rows = db.prepare(`SELECT id, status FROM tasks WHERE id IN (${ids.map(() => '?').join(',')})`).all(...ids);
for (const row of rows) {
  const q = db.prepare(`UPDATE tasks SET status='done', completed_at=strftime('%s','now'), result=? WHERE id=? AND status IN ('blocked','ready','todo','running')`).run(resultText, row.id);
  if (q.changes) {
    db.prepare(`INSERT INTO task_events (task_id, run_id, kind, payload, created_at) VALUES (?, NULL, 'completed', ?, strftime('%s','now'))`)
      .run(row.id, JSON.stringify({ source: 'hq_route_adint_close', by: 'gsp-master01', artifact_ok: true }));
    console.log('CLOSED ' + row.id + ' (was ' + row.status + ')');
  } else {
    console.log('SKIP ' + row.id + ' status=' + row.status);
  }
}
db.close();
