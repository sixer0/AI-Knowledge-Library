#!/usr/bin/env node
/**
 * rbac_roster.mjs — regenerasi controller-roster.json dari WebUiUser (RBAC).
 * Aturan user 31-08-2026: SEMUA profil yang terikat akun RBAC = kelas CONTROLLER,
 * plus orchestrator gsp yang mendelegasikan pekerjaan (basis statis).
 * Pemakaian: node rbac_roster.mjs            -> tulis roster + cetak ringkasan
 *            node rbac_roster.mjs --check     -> exit 1 bila DB punya profil RBAC yg belum ada di roster
 */
import fs from "fs";
import path from "path";
import { createRequire } from "module";

const require = createRequire(import.meta.url);
const DC = "C:/Users/TRIAL/gsp-datacenter";
const ROSTER_F = "C:/Users/TRIAL/workspace/gsp-hermes/workspace/docs/2026-08-31-enforcement-fleet/controller-roster.json";
const BASE = ["default", "gsp-crawler-orchestrator", "gsp-skill-manager", "gsp-system-manager", "gsp-pm-planner"];

const env = fs.readFileSync(path.join(DC, ".env"), "utf8");
const m = env.match(/DATABASE_URL=(.+)/);
if (!m) { console.error("DATABASE_URL tidak ada di gsp-datacenter/.env"); process.exit(2); }
const url = m[1].trim().replace(/^"|"$/g, "");
const { Client } = require(path.join(DC, "node_modules/pg"));

const c = new Client({ connectionString: url, ssl: /sslmode=require/.test(url) ? { rejectUnauthorized: false } : undefined });
await c.connect();
const { rows } = await c.query('select username, role, "hermesProfile" as profile from "WebUiUser" order by "hermesProfile"');
await c.end();

const rbac = rows.map((r) => r.profile).filter(Boolean);
// Rekonsiliasi S7 GATE-SM (03-09): profil hantu (home hilang dari disk) tidak boleh
// bertahan lewat union dengan roster lama. default dikecualikan: terikat akun
// superadmin dan memang tanpa home fisik sejak F-4 (S1).
const PROFILES_DIR = "C:/Users/TRIAL/AppData/Local/hermes/profiles";
const HOME_WHITELIST = new Set(["default"]);
const hasHome = (p) => HOME_WHITELIST.has(p) || fs.existsSync(path.join(PROFILES_DIR, p));
const prev = fs.existsSync(ROSTER_F) ? JSON.parse(fs.readFileSync(ROSTER_F, "utf8")) : null;
const merged = [...new Set([...BASE, ...rbac, ...(prev ? prev.controllers : [])])]
  .filter(hasHome)
  .sort();

if (process.argv.includes("--check")) {
  const missing = rbac.filter((p) => prev && !prev.controllers.includes(p));
  console.log(JSON.stringify({ rbac, missing }));
  process.exit(missing.length ? 1 : 0);
}

const out = {
  policy: "controller-lane",
  rule: "Profil tipe CONTROLLER = (a) terikat akun WebUiUser/RBAC (semua role), PLUS (b) orchestrator gsp yang mendelegasikan pekerjaan. Sumber aturan: keputusan user 31-08-2026. Regenerasi: node rbac_roster.mjs.",
  updated: new Date().toISOString().slice(0, 10),
  controllers: merged,
};
fs.mkdirSync(path.dirname(ROSTER_F), { recursive: true });
fs.writeFileSync(ROSTER_F, JSON.stringify(out, null, 2) + "\n");
console.log(`roster=${merged.length} (rbac=${rbac.length}, basis=${BASE.length}) -> ${ROSTER_F}`);
