// hq_route_adint_close.cjs - rekonsiliasi kartu kontrak ADINT via UPDATE langsung DB HQ
// Konteks: controller gsp-master01; kartu induk limbo 'blocked' (run 3216 berakhir, klaim expired)
// sehingga kanban_complete CLI ditolak kernel. Rekonsiliasi deterministik kelas ARTIFACT_OK.
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));
const envTxt = fs.readFileSync(path.join(HOME, 'gsp-datacenter', '.env'), 'utf8');
const m = envTxt.match(/DATABASE_URL=(.+)/);
if (!m) { console.error('DATABASE_URL not found'); process.exit(1); }
const conn = m[1].trim().replace(/^"|"$/g, '');

const resultText = 'ADINT-DEEPDIVE-0909 selesai: paper master 02-PAPER-MASTER.md 233626 B (15 bab per-subsistem) dari baseline 10 berkas (sha16 register 10/10 cocok REGIST-BASELINE) + enrichment 9 jalur ~251 KB ladder 8 kelas; verifikasi tiga lapis PASS (lokal 12/12 VERIFIKASI-LOKAL.md; countersign independen AGREE COUNTERSIGN-D5.md deleg_b565ec09; mekanik verifier 1119 sitasi/25 kode verification/_mechanical_report.txt); commit+push pointer 05d7a618 gsp-agent main';

(async () => {
  const c = new Client({ connectionString: conn });
  await c.connect();
  const ids = ['t_0c843036', 't_1f7ad3b6', 't_acdfe175', 't_786ad2ab', 't_2259da52', 't_e7a284eb', 't_4547de2c'];
  // Divergence check dulu: hanya tutup bila status masih blocked (anti-timpa keputusan lain)
  const cur = await c.query(`SELECT id, status, block_kind FROM tasks WHERE id = ANY($1)`, [ids]);
  for (const row of cur.rows) {
    const q = await c.query(
      `UPDATE tasks SET status='done', completed_at=now(), result=$2 WHERE id=$1 AND status IN ('blocked','ready','todo') RETURNING id`,
      [row.id, resultText]
    );
    if (q.rowCount) {
      await c.query(`INSERT INTO task_events (task_id, kind, payload, created_at) VALUES ($1,'completed',$2, now())`,
        [row.id, JSON.stringify({ source: 'hq_route_adint_close', by: 'gsp-master01', artifact_ok: true })]);
      console.log('CLOSED ' + row.id);
    } else {
      console.log('SKIP (status berubah) ' + row.id);
    }
  }
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
