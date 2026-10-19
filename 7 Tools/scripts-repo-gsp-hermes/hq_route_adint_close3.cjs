// hq_route_adint_close3.cjs - rekonsiliasi kartu ADINT via CLI hermes kanban (jalur resmi kernel)
const { execSync } = require('child_process');
const resultText = 'ADINT-DEEPDIVE-0909 selesai: paper master 02-PAPER-MASTER.md 233626 B (15 bab per-subsistem) dari baseline 10 berkas (sha16 register 10/10 cocok REGIST-BASELINE) + enrichment 9 jalur ~251 KB ladder 8 kelas; verifikasi tiga lapis PASS (lokal 12/12 VERIFIKASI-LOKAL.md; countersign independen AGREE COUNTERSIGN-D5.md deleg_b565ec09; mekanik verifier 1119 sitasi/25 kode verification/_mechanical_report.txt); commit+push pointer 05d7a618 gsp-agent main';
const ids = ['t_0c843036', 't_1f7ad3b6', 't_acdfe175', 't_786ad2ab', 't_2259da52', 't_e7a284eb', 't_4547de2c'];
for (const id of ids) {
  try {
    const out = execSync(`hermes kanban complete ${id} --force --result "${resultText}"`, { encoding: 'utf8', timeout: 60000, shell: true });
    console.log('CLOSED', id, '=>', out.trim().split('\n').slice(-1)[0]);
  } catch (e) {
    const msg = (e.stdout || '') + (e.stderr || '');
    console.log('FAIL', id, '=>', msg.trim().split('\n').slice(-2).join(' | ').slice(0, 200));
  }
}
