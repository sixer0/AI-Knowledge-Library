# Pembatalan misi ("batalkan semua task X") - teardown recipe

Kelas: user memerintahkan pembatalan seluruh task milik satu misi (contoh nyata 03-09: CICAK-VID-0903, video generation cicak, 25 kartu). Pembatalan = penutupan misi, bukan sekadar ganti status: inventaris SEMUA kanal eksekusi, hentikan klaim dispatcher, verifikasi nol, tinggalkan jejak.

## 1. Inventaris sebelum menyentuh apa pun (batch paralel)
- Kanban: `hermes kanban --board default list --json` lalu filter regex judul+body dengan slug misi (via python). Sekalian daftar kartu `running` MISI LAIN supaya tidak ikut disentuh.
- Kontrak: grep slug misi di `workspace/gsp-hermes/workspace/docs/`.
- Antrean Agent HQ: query Postgres langsung (resep di bawah), cari status `queued`/`running`/`needs-review` terkait misi.
- Cron: `cronjob list` (profil default) + grep slug di `$LOCALAPPDATA/hermes/cron/` dan `$LOCALAPPDATA/hermes/profiles/*/cron/`.
- Proses hidup: PowerShell `Get-Process` dan `Get-CimInstance Win32_Process` disaring CommandLine (nama mesin render: comfy/ffmpeg/python worker), + cek port mesin (ComfyUI 8188) via `netstat -ano | grep :8188`.
- Watchdog cron yang terikat misi (watchdog fleet/per-misi) ikut dicek.

## 2. Urutan teardown (cepat - dispatcher gateway mengklaim kartu `ready` seketika)
1. `hermes kanban comment <id> "DIBATALKAN oleh user <dd-mm>: <alasan>" --author swarm` untuk SETIAP kartu aktif (blocked/todo/ready/review).
2. `hermes kanban archive <id1> <id2> ...` (bulk diterima). Archive BUKAN hapus: reversibel, jejak audit utuh, dan menghentikan klaim dispatcher. Purge `--rm <ids>` hanya atas instruksi tersurat.
3. Kartu `done` dibiarkan sebagai riwayat kecuali user minta purge.
4. Bunuh proses hidup hanya jika temuannya ada.

## 3. Verifikasi penutupan (semua wajib nol)
- List board ulang: kartu misi berstatus non-terminal = 0.
- DB HQ: AgentRequest misi `queued`/`running` = 0.
- Cron = 0 job misi; proses = 0; port mesin bebas.
- Jangan klaim "dibatalkan" ke user sebelum keempat angka ini terukur (claim ladder: L2).

## 4. Jejak wajib controller
- Kartu penutupan `<SLUG>-CANCEL` dibuat lalu di-`complete` dengan bukti terukur (id kartu, hitungan, hasil cek).
- Kontrak misi: banner STATUS DIBATALKAN di kepala dokumen + entri Decision Log (apa yang diarsipkan, apa yang jadi riwayat, nasib artefak).
- Append laporan `[FASE]` T-4 penutupan ke `docs/<kontrak>/PHASE-REPORTS.md`.
- Artefak di disk TIDAK dihapus tanpa instruksi; tawarkan penghapusan sebagai opsi terpisah.

## Resep tool
### Query langsung AgentRequest HQ (fallback saat HTTP 401)
`curl -sk -H "x-internal-<nama-header>: <nilai>" https://localhost:9011/api/brahma/requests` bisa tetap 401 walau nilainya benar (kemungkinan CR terbawa). Jalur yang terbukti jalan, hanya dengan izin eksplisit atas kredensial itu (tanpa izin, berhenti dan lapor): Postgres langsung memakai modul `pg` milik bridge:
```js
// jalankan: node "C:/Users/TRIAL/Temp/query.cjs" (node tidak kenal path MSYS /c/...)
const { Client } = require('C:\\Users\\TRIAL\\<folder-layanan>\\hermes-bridge\\node_modules\\pg');
// DATABASE_URL diberikan pemilik dengan izin eksplisit, bukan diambil dari berkas lokal; lalu trim
// contoh: SELECT id,title,profile,status FROM "AgentRequest" WHERE title ILIKE '%slug%' ORDER BY "createdAt" DESC
```
- Kolom `kanbanTaskId` TIDAK ada di `AgentRequest`; jangan sertakan di SELECT.
- `node` gagal resolve path MSYS (`/c/...` -> MODULE_NOT_FOUND); selalu `C:/Users/...`.
- `tasklist | grep` bisa kosong lewat pipe bash di host ini; pakai PowerShell `Get-Process` / `Get-CimInstance Win32_Process` (escape `$_` sebagai `\$_` di dalam kutip ganda bash).

### Gerbang naturalisasi jawaban user
Pindai draf jawaban sebelum dikirim, dengan path WINDOWS (path MSYS membuat scanner membaca masukan kosong):
```
uv run --python 3.11 python "$LOCALAPPDATA/hermes/skills/gsp/gsp-output-naturalization/scripts/scan_ai_footprint.py" "C:/Users/TRIAL/Temp/draft.md" --channel chat
```
- Pitfall A5 (terjadi 03-09): frasa literal "dispatch hq" di prosa chat menyalakan CHECK A5 (label fungsi internal bocor) -> VERDICT FAIL. Parafrase netral bahasa Indonesia (mis. "antrean tugas di pusat agen"), pindai ulang sampai `VERDICT: PASS`.
- Edit draf lewat `sed` bertingkat mudah merusak struktur paragraf; lebih aman tulis ulang draf penuh sekali jalan.
