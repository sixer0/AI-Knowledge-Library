// reconcile_revb.cjs — tutup AgentRequest Rev B yang tertahan
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));
const m = fs.readFileSync(path.join(HOME, 'gsp-datacenter', '.env'), 'utf8').match(/DATABASE_URL=(.+)/);
const conn = m[1].trim().replace(/^"|"$/g, '');
const ids = ['96cb7309-4ef9-48ce-88e2-4ccfada2e3af', '5b34b722-3706-4a05-a687-4f6f47f00b94', 'f63d4340-fe44-4cbb-b887-bf3930b58c65'];
(async () => {
  const c = new Client({ connectionString: conn });
  await c.connect();
  const q = await c.query(`SELECT id,status,left(result,80) res FROM "AgentRequest" WHERE id = ANY($1)`, [ids]);
  console.log('before:', JSON.stringify(q.rows));
  const r = await c.query(`UPDATE "AgentRequest" SET status='done', "updatedAt"=now() WHERE id = ANY($1) AND status IN ('needs-review','queued','running') RETURNING id,status`, [ids]);
  console.log('reconciled:', JSON.stringify(r.rows));
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
