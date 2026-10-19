// hq_dispatch.cjs — insert AgentRequest (kind=oneshot, sideEffecting=false) ke DB HQ
// Usage: node hq_dispatch.cjs "<title>" "<profile>" "<prompt-file|inline prompt>"
// Dibuat 2026-08-31 utk kontrak docs/2026-08-31-standar-dokumen-fleet
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));

const envPath = path.join(HOME, 'gsp-datacenter', '.env');
const envTxt = fs.readFileSync(envPath, 'utf8');
const m = envTxt.match(/DATABASE_URL=(.+)/);
if (!m) { console.error('DATABASE_URL not found in .env'); process.exit(1); }
const conn = m[1].trim().replace(/^"|"$/g, '');

const [title, profile, promptArg, agentArg] = process.argv.slice(2);
if (!title || !profile || !promptArg) { console.error('usage: hq_dispatch.cjs <title> <profile> <prompt-file-or-text> [agentId]'); process.exit(1); }
let prompt = promptArg;
if (fs.existsSync(promptArg)) prompt = fs.readFileSync(promptArg, 'utf8');

// FIX 02-09-2026 (temuan #4 HQ): catat inisiator sebenarnya agar graf
// orkestrasi tidak menyamakan semua dispatch dgn brahma. Urutan: arg ke-4 >
// env HERMES_DISPATCH_AGENT > turunan HERMES_HOME (profil aktif) > brahma.
function inferAgent() {
  if (agentArg) return String(agentArg).trim();
  if (process.env.HERMES_DISPATCH_AGENT) return process.env.HERMES_DISPATCH_AGENT.trim();
  const hh = (process.env.HERMES_HOME || '').replace(/[\\/]+$/, '');
  const base = path.basename(path.dirname(hh));
  const name = path.basename(hh);
  if (base === 'profiles' && name && name !== 'hermes') return name; // profil gsp-* aktif
  return 'brahma';
}
const requestedBy = inferAgent();

(async () => {
  const c = new Client({ connectionString: conn });
  await c.connect();
  const r = await c.query(
    `INSERT INTO "AgentRequest" (id, origin, "requestedBy", kind, title, prompt, profile, "sideEffecting", status, "createdAt", "updatedAt")
     VALUES ($4, 'brahma-controller', $5, 'oneshot', $1, $2, $3, false, 'queued', now(), now()) RETURNING id`,
    [title, prompt, profile, crypto.randomUUID(), requestedBy]
  );
  console.log('DISPATCHED id=' + r.rows[0].id + ' profile=' + profile + ' by=' + requestedBy + ' title=' + title);
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
