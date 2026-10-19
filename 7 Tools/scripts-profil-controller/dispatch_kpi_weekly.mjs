// GSP Dispatch KPI — digest mingguan (R2, 29-08-2026)
// Jalankan: node dispatch_kpi_weekly.mjs  (dipakai cronjob no_agent, output = pesan)
import { createRequire } from "node:module";
import fs from "node:fs";
import path from "node:path";

const DC = "C:/Users/TRIAL/gsp-datacenter";
const require2 = createRequire(path.join(DC, "package.json"));

// DATABASE_URL dari gsp-datacenter/.env
const envText = fs.readFileSync(path.join(DC, ".env"), "utf8");
const m = envText.match(/^DATABASE_URL=(.*)$/m);
if (!m) { console.error("DATABASE_URL tidak ditemukan di gsp-datacenter/.env"); process.exit(1); }
let dbUrl = m[1].trim();
const a = dbUrl.charCodeAt(0), b = dbUrl.charCodeAt(dbUrl.length - 1);
if ((a === 34 || a === 39) && b === a) dbUrl = dbUrl.slice(1, -1);
process.env.DATABASE_URL = dbUrl;

const { PrismaClient } = require2("@prisma/client");
const prisma = new PrismaClient();

const fmt = (n) => String(n).padStart(3, " ");

function main(j) {
  const lines = [];
  lines.push("GSP DISPATCH KPI — digest mingguan (" + j.generatedAt.slice(0, 10) + ")");
  lines.push("");
  lines.push("Antrean review tertunda : " + j.review.pending);
  lines.push("Dispatch berjalan       : " + j.review.running);
  lines.push("Zombie edge orkestrasi  : " + j.orchestration.zombieEdges);
  lines.push("");
  lines.push("Status semua waktu:");
  for (const [s, n] of Object.entries(j.byStatus)) lines.push("  " + s.padEnd(18) + fmt(n));
  lines.push("");
  lines.push("24 jam terakhir: total " + j.last24h.total + " · needs-review " + j.last24h.needsReview + " · done " + j.last24h.done + " · failed " + j.last24h.failed);
  lines.push("");
  lines.push("Delegasi: edge " + j.orchestration.totalEdges + " · non-brahma(multi-hop) " + j.orchestration.nonBrahmaEdges + " (" + j.orchestration.multiHopPct + "%)");
  lines.push("Self-claim historis (pra review-gate 29-08): " + j.review.selfClaimHistoris);
  const warn = [];
  if (j.review.pending > 5) warn.push("antrean review menumpuk (" + j.review.pending + ") — assignor perlu review/force-done");
  if (j.orchestration.zombieEdges > 0) warn.push(j.orchestration.zombieEdges + " zombie edge — restart bridge untuk auto-recover");
  if (j.last24h.failed > 2) warn.push(j.last24h.failed + " dispatch gagal 24 jam terakhir");
  if (j.review.running > 3) warn.push(j.review.running + " dispatch berjalan bersamaan — waspada kontensi CLI");
  if (warn.length) { lines.push(""); lines.push("PERHATIAN:"); for (const w of warn) lines.push("  - " + w); }
  return lines.join("\n");
}

try {
  const [statusCounts, pendingReview, runningNow, selfClaim, total] = await Promise.all([
    prisma.agentRequest.groupBy({ by: ["status"], _count: { _all: true } }),
    prisma.agentRequest.count({ where: { status: "needs-review" } }),
    prisma.agentRequest.count({ where: { status: "running" } }),
    prisma.agentRequest.count({ where: { status: "done", decidedAt: null, kind: { in: ["oneshot", "chat"] } } }),
    prisma.agentRequest.count(),
  ]);
  const since = new Date(Date.now() - 24 * 3600 * 1000);
  const last24h = await prisma.agentRequest.findMany({ where: { createdAt: { gte: since } }, select: { status: true } });
  const runningEdges = await prisma.orchestrationRecord.findMany({ where: { status: "running" }, select: { runId: true } });
  const parentIds = runningEdges.map((e) => e.runId).filter(Boolean);
  const parents = parentIds.length ? await prisma.agentRequest.findMany({ where: { id: { in: parentIds } }, select: { id: true, status: true } }) : [];
  const parentMap = new Map(parents.map((p) => [p.id, p.status]));
  const zombieEdges = runningEdges.filter((e) => parentMap.get(e.runId || "") !== "running").length;
  const totalEdges = await prisma.orchestrationRecord.count();
  const nonBrahmaEdges = await prisma.orchestrationRecord.count({ where: { fromAgent: { notIn: ["brahma", "default"] } } });

  const byStatus = {};
  for (const g of statusCounts) byStatus[g.status] = g._count._all;
  const j = {
    generatedAt: new Date().toISOString(),
    total, byStatus,
    review: { pending: pendingReview, running: runningNow, selfClaimHistoris: selfClaim },
    orchestration: { zombieEdges, totalEdges, nonBrahmaEdges, multiHopPct: totalEdges ? Math.round((nonBrahmaEdges / totalEdges) * 100) : 0 },
    last24h: {
      total: last24h.length,
      needsReview: last24h.filter((r) => r.status === "needs-review").length,
      done: last24h.filter((r) => r.status === "done").length,
      failed: last24h.filter((r) => r.status === "failed").length,
    },
  };
  console.log(main(j));
} catch (e) {
  console.error("KPI error:", e.message);
  process.exit(1);
} finally {
  await prisma.$disconnect();
}
