// templates/register_approval.cjs — daftarkan permohonan keputusan user ke Approval Inbox HQ
// (AgentRequest awaiting_approval, origin requestedBy='task-monitor'). Pola sumber:
// C:/Users/TRIAL/gsp-datacenter/scripts/approval_triage_0907c.cjs (misi TRIAGE-0907C).
// JALANKAN dari cwd C:/Users/TRIAL/gsp-datacenter (butuh @prisma/client + DATABASE_URL di .env).
// Edit array reqs[] lalu: node register_approval.cjs  (idempoten: skip dup judul status hidup)
const { PrismaClient } = require('@prisma/client');
const p = new PrismaClient();
(async () => {
  const reqs = [
    {
      title: 'APPROVAL: <ringkasan keputusan yang diminta> (kartu t_xxxxxxxx)',
      prompt: '<konteks + angka + opsi + aksi user yang diharapkan; kontrak misi: docs/...>',
    },
  ];
  for (const r of reqs) {
    const dup = await p.agentRequest.findFirst({
      where: { title: r.title, status: { in: ['queued', 'awaiting_approval', 'approved', 'running', 'done'] } },
    });
    if (dup) { console.log('SKIP dup:', r.title.slice(0, 50), dup.id, dup.status); continue; }
    const c = await p.agentRequest.create({
      data: {
        origin: 'hermes', requestedBy: 'task-monitor', kind: 'oneshot',
        sideEffecting: false, status: 'awaiting_approval',
        profile: null, title: r.title, prompt: r.prompt,
      },
    });
    console.log('CREATED awaiting_approval:', c.id, '|', c.title.slice(0, 60));
  }
  const open = await p.agentRequest.count({ where: { status: 'awaiting_approval' } });
  console.log('total awaiting_approval kini:', open);
  await p.$disconnect();
})().catch(e => { console.error('ERR', e.message); process.exit(1); });
