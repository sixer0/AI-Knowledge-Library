# Ask Librarian + Bridge Lanes (25-08-2026)

Fitur tanya-jawab Information Library: UI mengirim pertanyaan → dispatch
`gsp-librarian` (kind=oneshot) → librarian menelusuri IL via curl → jawab
JSON multi-table → UI render tabel dinamis + sumber ber-URL.

## Kontrak endpoint

| Endpoint | Method | Fungsi |
|---|---|---|
| `/api/information-library/ask` | POST `{question}` | buat AgentRequest kind=oneshot, profile=gsp-librarian, title=`Ask Librarian — <q>`; prompt berisi instruksi curl + skema JSON |
| `/api/brahma/requests/<id>` | GET | poll status + result (handler GET ditambahkan 25-08-2026; sebelumnya hanya PATCH approve/reject) |

Skema respons librarian (HANYA JSON, tanpa prosa/fence):

```json
{
  "answer": "Ringkasan 2-4 kalimat",
  "tables": [{"title": "...", "columns": ["A","B"], "rows": [["a","b"]]}],
  "sources": [{"title": "...", "url": "/api/information-library/file?root=workspace|wiki|vault&path=...", "rank": 0, "relevance": "tinggi"}]
}
```

- Prompt librarian WAJIB memuat: instruksi curl `https://localhost:9011/api/information-library?q=<kata>&scope=all&status=all` (pakai `-sk`, self-signed), skoring rank × relevansi (wiki 0 > vault 1 > insight 2 > memory 3 > arsip 4), dan "Output dimulai { dan diakhiri }".
- Pertanyaan DAFTAR (vendor/dokumen/proyek/rekomendasi) WAJIB dijawab sebagai `tables`, bukan prosa; daftar LENGKAP tanpa batas jumlah baris; sel maks ~120 char; JANGAN pakai kutip ganda di dalam teks sel (ganti ' atau «»); self-check JSON sebelum kirim (fix 26-08-2026).
- URL sumber vault = `root=vault&path=vault/<perkara>/...` — endpoint file memperlakukan root != wiki sebagai SHARED_WS, jadi root=vault tetap resolve.
- Bridge menyimpan respons di `AgentRequest.result` — cap kini **200000** (`BRIDGE_RESULT_MAX`) + `trimResult()` yang TIDAK memotong JSON di tengah (parse-check backward; fix 26-08-2026: cap lama 8000 membuat JSON Ask terpotong → UI gagal render). UI me-parse toleran: buang markdown fence, ambil `{...}` pertama-terakhir, **fallback `jsonrepair`** bila JSON cacat, dan tampilkan hasil mentah bila tetap gagal (`parseAskResult` di page.tsx).
- Riwayat Ask: `GET /api/brahma/requests?title=Ask Librarian&take=N&light=1` (light = tanpa result/error/prompt). Klik item → GET `/api/brahma/requests/<id>` → render ulang jawaban (atau lanjut polling bila masih queued/running).
- Sesi Ask dipersist di `localStorage` (`hq.ask.session.v1`) → refresh tidak menghilangkan progres; panel terbuka lagi otomatis dan polling dilanjutkan.
- Progres loading MONOTONIK berbasis status nyata (queued=15%, approved=35%, running=60%) + elapsed timer — bukan teks fase berputar.

## Bridge: main lane + askLane

- `processQueue()`: `SELECT ... WHERE status IN ('queued','approved') AND title NOT LIKE 'Ask Librarian%' ORDER BY "createdAt" ASC LIMIT 1` dalam loop `for(;;)` — SATU request per iterasi, pick ulang tiap selesai.
- `askLane()`: loop terpisah `WHERE status='queued' AND title LIKE 'Ask Librarian%' ORDER BY "createdAt" ASC LIMIT 1` → request Ask dijawab seketika PARALEL dengan rebuild. Keduanya `runRequest` yang sama (kanban card + status + result).
- Kenapa bukan sekadar ORDER BY priority: batch 3 lama membuat ask yang masuk di tengah batch menunggu batch selesai (2-30m/task rebuild). Lane paralel memotong tunggu itu.
- Konkurensi 2× `hermes -p gsp-librarian -z` (ask + rebuild) teruji aman; setAgentState menulis tabel DB (Postgres), bukan file per-profil.

## Propose Librarian ("Usulkan ke librarian") — fitur 26-08-2026

Mirip Ask Librarian, untuk USULAN knowledge + lampiran file/URL, workflow lengkap:
librarian menilai → dedup → meninjau/analisa lampiran → buat objek vault
(`vault_propose.py`) → verifikasi INDEPENDEN gsp-custodian → promote (`vault_promote.py`)
bila terverifikasi, atau lapor revisi (loop maks 3 via tombol "Revisi & kirim ulang").

**Endpoints:**
- `POST /api/information-library/propose/upload` — multipart `file`+`token` (UUID client) →
  simpan ke `<SHARED_WORKSPACE>/library/proposals/raw/<token>/<ts>-<name>`; ekstensi whitelist
  (pdf/docx/xls/pptx/md/txt/csv/img/json), maks 25MB; balas `{name, path, size}` (path relatif shared ws).
- `POST /api/information-library/propose` — JSON `{title, body, type, tags[], sensitif, perkara,
  sumber, halaman, kelas_bukti, attachments:[{name,kind:file|url,value}], revisiOf?, revisiNote?, feedback?}`.
  Dispatch gsp-librarian (title `Kurasi proposa: <title>` / `(revisi)`), `sideEffecting` bila sensitif.
  Prompt memuat pipeline + kontrak output JSON:
  `{"summary","verdict":"terverifikasi|perlu_revisi|ditolak|menunggu_persetujuan","vaultPath","promoted","wikiPath","custodian":{"verdict","catatan_verifikasi"},"revisi":[{"item","perbaikan"}],"sources":[]}`
- Poll: GET `/api/brahma/requests/<id>`; riwayat: `?title=Kurasi%20proposa&light=1`.

**UI (page.tsx `ProposePanel`):** form + attach file (upload langsung) / URL; loading monotonic;
render verdict pills + catatan custodian + daftar revisi + link vault + tombol revisi;
riwayat 3 + "Lihat riwayat lebih lama"; sesi `localStorage hq.propose.session.v1` (refresh lanjut);
payload revisi di `hq.propose.last.v1` (agar "Revisi & kirim ulang" dari riwayat ter-prefill).

**Pitfall (fix 26-08):** `onRevise(result, requestId)` — panel harus kirim requestId, BUKAN title
(3-arg → requestId keisi judul → key remount salah → form tidak ter-prefill).
**Gate sensitif:** librarian/custodian bisa menaikkan `sensitif: ya` secara konservatif
(ujian tanpa konfirmasi user) → status `menunggu_persetujuan`, TIDAK auto-promote.

## Zombie 'running' (pola umum)

Bridge restart saat request berjalan → AgentRequest stuck `running` tanpa proses.
- Monitor/script harus menghitung stale running (startedAt > 45m) sebagai selesai/gagal — jangan biarkan memblokir kondisi "queue kosong".
- Setelah restart bridge, tandai request `running` yang tersisa → `failed` (error: "dibatalkan saat restart bridge").
- Pengecualian nyata: task lama sehari (non-IL) juga bisa zombie.

## Verifikasi end-to-end (tanpa browser daemon)

Playwright + chromium lokal (`executable_path` chromium-1228 + `--ignore-certificate-errors`):
1. Buka `/information-library` → klik "Ask Librarian" → panel muncul.
2. Isi pertanyaan → Tanya → loading state ("Librarian sedang menelusuri…").
3. Poll sampai `table` muncul → periksa tabel + `a[href*="file?"]` count.
- Uji API langsung: `POST /api/information-library/ask` → GET status → status done + result berisi JSON valid.

## Pitfall: patch tool Windows mengubah `\r` → CR literal

Saat mengedit file yang mengandung `\r` (regex `\r?\n`, CRLF handling) dengan
tool `patch`, new_string yang berisi `\r\n` bisa ditulis sebagai CR literal →
file rusak (regex terpotong baris, compile error). Untuk teks ber-`\r`:
- tulis via `write_file` (verbatim) lalu jalankan, ATAU
- script Python byte-safe: bangun string dengan `chr(92)` (backslash) +
  `open(path,"wb")`, verifikasi dengan baca ulang dari DISK (jangan dari
  variabel in-memory — verifikasi variabel bisa menipu).
