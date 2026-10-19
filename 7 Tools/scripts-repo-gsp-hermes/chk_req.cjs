// Cek status AgentRequest lewat DB (read-only). Usage: node chk_req.cjs <id>
const fs = require('fs');
const path = require('path');
const HOME = 'C:\\Users\\TRIAL';
const { Client } = require(path.join(HOME, 'gsp-datacenter', 'hermes-bridge', 'node_modules', 'pg'));
const envTxt = fs.readFileSync(path.join(HOME, 'gsp-datacenter', '.env'), 'utf8');
const m = envTxt.match(/DATABASE_URL=(.+)/);
const conn = m[1].trim().replace(/^"|