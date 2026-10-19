# -*- coding: utf-8 -*-
"""Cek cepat: dari 46 done-24j tanpa ACK di VIBE-BIBLE-1013, berapa yang sudah ber-marker
RANTAI-WAKE done-unacked (sisa tagihan baru vs sudah ditandai ronde sysman sebelumnya)."""
import sqlite3, os, time, pathlib
HOME = pathlib.Path(os.environ.get('LOCALAPPDATA', '')) / 'hermes'
con = sqlite3.connect(f'file:{HOME/"kanban.db"}?mode=ro', uri=True)
cur = con.cursor()
now = int(time.time()); DAY = now - 86400
cur.execute("""
SELECT
 SUM(CASE WHEN EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%') THEN 1 ELSE 0 END),
 SUM(CASE WHEN NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-WAKE done-unacked%') THEN 1 ELSE 0 END)
FROM tasks t
WHERE t.status='done' AND t.completed_at>=? AND COALESCE(t.tenant,'')='VIBE-BIBLE-1013'
AND NOT EXISTS (SELECT 1 FROM task_comments c WHERE c.task_id=t.id AND c.body LIKE '%RANTAI-ACK%')""", (DAY,))
m, nm = cur.fetchone()
print(f'done-24j VIBE tanpa-ACK: ber-marker={m} tanpa-marker(baru)={nm}')
con.close()
