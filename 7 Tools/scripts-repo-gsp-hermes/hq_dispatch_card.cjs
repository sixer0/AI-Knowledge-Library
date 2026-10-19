// hq_dispatch_card.cjs — dispatch AgentRequest TERIKAT kartu kontrak (hermesTaskId)
// Usage: node hq_dispatch_card.cjs "<title>" "<profile>" "<prompt-file>" "<hermesTaskId>"
// Varian hq_dispatch.cjs (2026-08-31) + kolom hermesTaskId agar bridge menutup kartu
// kontrak yang sama dan TIDAK membuat kartu duplikat tipis (lihat bridge.mjs baris ~233).
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));

const envTxt = fs.readFileSync(path.join(HOME, 'gsp-datacenter', '.env'), 'utf8');
const m = envTxt.match(/DATABASE_URL=(.+)/);
if (!m) { console.error('DATABASE_URL not found'); process.exit(1); }
const conn = m[1].trim().replace(/^"|"$/g, '');

const [title, profile, promptFile, taskId, agentArg] = process.argv.slice(2);
if (!title || !profile || !promptFile || !taskId) {
  console.error('usage: hq_dispatch_card.cjs <title> <profile> <prompt-file> <hermesTaskId> [agentId]');
  process.exit(1);
}
const prompt = fs.readFileSync(promptFile, 'utf8');

// FIX 02-09-2026 (temuan #4 HQ): inisiator sebenarnya (arg > env > HERMES_HOME profil aktif).
function inferAgent() {
  if (agentArg) return String(agentArg).trim();
  if (process.env.HERMES_DISPATCH_AGENT) return process.env.HERMES_DISPATCH_AGENT.trim();
  const hh = (process.env.HERMES_HOME || '').replace(/[\\/]+$/, '');
  const base = path.basename(path.dirname(hh));
  const name = path.basename(hh);
  if (base === 'profiles' && name && name !== 'hermes') return name;
  return 'brahma';
}
const requestedBy = inferAgent();

(async () => {
  const c = new Client({ connectionString: conn });
  await c.connect();
  const r = await c.query(
    `INSERT INTO "AgentRequest" (id, origin, "requestedBy", kind, title, prompt, profile, "sideEffecting", status, "hermesTaskId", "createdAt", "updatedAt")
     VALUES ($4, 'brahma-controller', $6, 'oneshot', $1, $2, $3, false, 'queued', $5, now(), now()) RETURNING id`,
    [title, prompt, profile, crypto.randomUUID(), taskId, requestedBy]
  );
  console.log('DISPATCHED id=' + r.rows[0].id + ' profile=' + profile + ' card=' + taskId + ' by=' + requestedBy);
  await c.end();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
