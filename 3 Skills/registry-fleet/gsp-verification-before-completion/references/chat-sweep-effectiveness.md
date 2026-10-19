# Mengukur EFEKTIVITAS gerbang perilaku pada keluaran agen nyata (NAT-S20, 02-09)

Bedanya dengan `deterministic-verification.md`: skrip di sana membuktikan artefak/instalasi
benar; pola ini membuktikan **kebijakan yang dipasang benar-benar mengubah teks yang
dihasilkan agen** setelah rollout. Ini satu-satunya cara jujur menjawab "apakah gate-nya jalan?".

## Pola yang terbukti jalan

Satu skrip deterministik milik controller (bukan dikerjakan worker via tool call):
[`C:/Users/TRIAL/workspace/gsp-hermes/scripts/scan_chat_sweep_20260902.py`](../../../../7%20Tools/scripts-repo-gsp-hermes/scan_chat_sweep_20260902.py)
(args: `--n --min-chars --since --sessions-started-after --window-label --stores --json-out --report --heavy-limit`)

1. **Impor scanner resmi sebagai modul** (`importlib.util.spec_from_file_location` ke
   `skills/gsp/<skill>/scripts/scan_*.py`), lalu panggil `extract_plain()` + `evaluate(doc,
   channel, opts)` per sampel. Jangan shell-out per pesan (ribuan proses, lambat).
2. **Read-only, union semua store sesi**: `sqlite3.connect("file:...?mode=ro", uri=True)`;
   DB utama `%LOCALAPPDATA%\hermes\state.db` + 53 `profiles/*/state.db` (54 store, TERPISAH
   bukan salinan, irisan id = 0; sesi worker kanban tersimpan di DB PROFIL-nya).
   Filter: `role='assistant' AND content IS NOT NULL AND length(trim(content)) >= min_chars`.
3. **Kanal per `sessions.source`**: webui/desktop/cli/messenger → chat (K1); kanban → K5;
   cron → notif; **subagent DIKECUALIKAN** (internal, tidak dibaca user). Tanpa pemetaan ini
   ambang D-TA-05 (metrik mati di kanal pendek) salah terpasang.
4. **Dua jendela wajib, dan yang menilai gerbang hanya jendela efektivitas**:
   - baseline: seluruh riwayat;
   - efektivitas: `--sessions-started-after <epoch rollout>` pakai `sessions.started_at`
     (BUKAN timestamp pesan) supaya sesi panjang yang lahir sebelum rollout tidak dihitung.
     Epoch rollout diambil dari `completed_at` kartu pemasangan gate
     (`hermes kanban show <id> --json` → `task.completed_at`).
   Delta baseline→pasca adalah angka efektivitasnya; vonis absolut dinilai di jendela pasca.

## Pitfalls yang membayar mahal

- **Worker tidak boleh menjalankan scanner per-sampel lewat tool call.** Kartu NAT-S20 mati
  DUA kali (crashed; lalu `gave_up` Iteration budget exhausted 150/150) melakukan itu.
  Pembagian kerja yang benar: controller menulis skrip + menjalankan sekali sebagai bukti,
  verifier tinggal re-run (detik) + menyusun laporan kanonis + mencatat FAIL apa adanya.
  Koreksi dikirim sebagai komentar kartu + `unblock`, bukan kartu baru.
- **Sapuan riwayat penuh melewati timeout foreground** (ter-clamp ±420 detik meski diminta
  600): jalankan via terminal background + notify_on_complete; jendela efektivitas kecil
  (510 sampel/54 DB = 1,4 detik) boleh foreground.
- **Gate berumur beberapa jam TIDAK memperbaiki riwayat** — jangan goda meloloskan artefak
  karena "masih baru". Lapor FAIL + disposition (kartu perbaikan akar, mis. celah cakupan
  rollout) adalah hasil yang benar; temuan sapuan hari itu justru menemukan root profile
  terlewat (lihat pitfall fleet-ops).
- Angka `store di bawah N` wajib dilaporkan dengan alasan teknis nyata (store kosong,
  jendela terlalu sempit), bukan diam-diam mengecilkan denominator.

## Bahan diagnosis cepat

Query langsung untuk attribution per sumber sesi (read-only):
```sql
select s.source, count(*),
  sum(case when m.content like '%'||char(0x2014)||'%' then 1 else 0 end)
from messages m left join sessions s on s.id=m.session_id
where m.role='assistant' and m.content is not null and coalesce(m.timestamp,0)>=?
group by s.source;
```
Perbandingan grep blok kebijakan di `profiles/*/SOUL.md` vs SOUL root menjawab
"gate terpasang tapi bocor di mana" dalam satu langkah.
