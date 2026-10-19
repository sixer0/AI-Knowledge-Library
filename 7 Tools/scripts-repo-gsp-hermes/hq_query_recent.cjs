// hq_query_recent.cjs — tampilkan AgentRequest terbaru (read-only, utk verifikasi dispatch)
// Usage: node hq_query_recent.cjs [limit]
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));

const envTxt = fs.readFileSync(path.join(HOME, 'gsp-datacenter', '.env'), 'utf8');
const m = envTxt.match(/DATABASE_URL=(.+)/);
if (!m) { console.error('DATABASE_URL not found'); process.exit(1); }
const conn = m[1].trim().replace(/^"|"$/g, '');

const limit = parseInt(process.argv[2] || '10', 10);

(async () => {
  const c = new Client({ connectionString: conn });
  await c.connect();
  const r = await c.query(
    'SELECT id,title,profile,status,"createdAt","updatedAt",length(coalesce(result,\'\')) AS rlen FROM "AgentRequest" ORDER BY "createdAt" DESC LIMIT $1',
    [limit]
  );
  for (const x of r.rows) {
    console.log(
      x.createdAt.toISOString().slice(5, 16),
      String(x.status).padEnd(9),
      String(x.profile || '-').padEnd(22),
      'rlen=' + String(x.rlen).padEnd(6),
      x.id.slice(0, 8),
      String(x.title).slice(0, 58)
    );
  }
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
