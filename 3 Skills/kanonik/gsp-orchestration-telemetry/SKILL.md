---
name: gsp-orchestration-telemetry
description: "Rekam interaksi lintas profil ke Agent HQ (orchestration telemetry) agar jejak delegasi/handoff/verifikasi tervisualisasi, bukan hanya tercatat di dokumen. Muat saat mendelegasikan kerja ke profil gsp-* lain, menutup edge, atau mengirim dispatch via HQ."
version: 1.1.0
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: orchestration
    tags: [gsp, orchestration, telemetry, agent-headquarter, visualization, delegation, handoff, interaction]
---

# GSP Orchestration Telemetry

> Setiap interaksi **lintas profil** (bukan sub-agen internal) WAJIB direkam ke GSP Agent
> Headquarter — begitu kerja didelegasikan ke profil `gsp-*` lain, dan lagi saat hasilnya
> kembali. Tujuannya: rekam jejak orkestrasi **tervisualisasi** di dashboard (halaman
> `/orchestration`, graf interaksi antar profil), bukan hanya tersimpan sebagai file di
> document contract.

## Kapan digunakan

- Kamu (controller/orchestrator) mendelegasikan tugas ke profil `gsp-*` lain.
- Tugas dari profil lain selesai / blocked / butuh review — tutup edge yang terbuka.
- Dispatch dikirim dari HQ ke profil tertentu (otomatis direkam bridge, tak perlu manual).
- Kamu ingin mengecek jejak interaksi terakhir / status edge.

## Model interaksi (satu baris = satu edge terarah A → B)

| Field | Nilai |
|-------|-------|
| `from` / `to` | id profil (mis. `gsp-master-controller`, `brahma`) |
| `kind` | `delegate` (turunkan kerja) · `handoff` (serah kerja antar spesialis) · `verify` (minta verifikasi) · `report` (lapor balik) · `review` · `gate` (persetujuan fase) · `dispatch` (dari HQ/bridge) |
| `status` | `running` (edge dibuka) · `done` · `blocked` · `needs-review` · `failed` · `rejected` |
| `runId` | pengelompok satu run orkestrasi (pakai slug tanggal_tugas atau id AgentRequest) — dipakai untuk idempotensi |
| `taskTitle` | judul tugas singkat |
| `message` | ringkasan hasil / blocker |
| `artifactPath` | path artefak `docs/[date]_[task]/...` (hubungkan ke Documentation Contract) |

## Cara merekam — helper CLI (wajib terpasang di `~/.local/bin/`)

```bash
# 1) BUKA edge saat mendelegasikan (status running)
gsp-hq-record gsp-master-controller gsp-request-translator delegate running \
  --run 2026_08_21_riset_vendor \
  --title "RT: terjemahkan permintaan" \
  --msg "didelegasikan via RT-FIRST"

# 2) TUTUP edge saat hasil kembali (status done/blocked/needs-review/failed)
#    runId+from+to+kind sama → memperbarui edge yang sama (idempoten)
gsp-hq-record gsp-master-controller gsp-request-translator delegate done \
  --run 2026_08_21_riset_vendor \
  --title "RT: terjemahkan permintaan" \
  --msg "TRANSLATED" \
  --artifact "docs/2026_08_21_riset_vendor/identification/01_translated.md"

# 3) Update status live agen (opsional, untuk halaman Agents)
gsp-hq-agent gsp-coder-execution --status running --task "Implementasi modul X"
gsp-hq-agent gsp-coder-execution --status idle --action "Selesai: modul X"
```

Endpoint langsung (WAJIB header `x-internal-secret: <INTERNAL_API_SECRET dari C:/Users/TRIAL/gsp-datacenter/.env>` sejak 30-08 — HQ production, tanpa header ini semua /api/** balas 401). Contoh: `curl -sk -X POST https://localhost:9011/api/orchestration -H "content-type: application/json" -H "x-internal-secret: $SEC" -d '{...}'`. Endpoint: `POST http://localhost:9011/api/orchestration` dengan JSON
`{"from","to","kind","status","runId","taskTitle","message","artifactPath"}`.
Untuk membuat REQUEST dispatch (bukan edge manual) lewat HTTP, gunakan
`POST /api/brahma/dispatch` dengan body `{title, prompt, profile, agentId}` —
`agentId` = id profil pengirim (WAJIB untuk pemanggil mesin; lihat seksi atribusi).
Cek rekaman: `curl -s "http://localhost:9011/api/orchestration?limit=20"`.
Hapus (housekeeping): `curl -s -X DELETE "http://localhost:9011/api/orchestration?runId=<id>"`.

## Aturan (WAJIB)

1. **Catat SAJA interaksi lintas profil.** Delegasi internal `delegate_task(...)` ke sub-agen
   dalam sesi yang sama TIDAK direkam — itu bukan interaksi antar profil.
2. **Buka edge saat mengirim, tutup saat menerima hasil.** Jangan biarkan edge menggantung
   `running` setelah tugas selesai (kecuali memang masih berjalan).
3. **Gunakan `runId` yang konsisten** untuk satu run orkestrasi agar timeline/graf
   mengelompok dengan benar. Contoh: `2026_08_21_<slug_tugas>` atau id AgentRequest.
4. **Sertakan `artifactPath`** dari Documentation Contract — graf menampilkannya sebagai
   tautan jejak audit (kontrak GSP-2).
5. **Jika HQ mati** (curl gagal): catat interaksi di document contract seperti biasa, lalu
   rekam ke HQ begitu tersedia. Jangan blok tugas hanya karena HQ down.
6. **Jangan pernah mengirim rahasia** (API key, token, kredensial) di `--msg`/`--meta`.
7. Bridge otomatis merekam edge `dispatch` saat request dijalankan lewat HQ dengan field
   `profile` — jangan duplikasi manual untuk kasus itu. Sejak FIX 02-09-2026 (temuan #4
   HQ), sisi `from` edge bukan lagi selalu `brahma`: bridge membaca
   `AgentRequest.requestedBy` (fallback `brahma` bila null). Lihat seksi
   "Atribusi inisiator" di bawah — aturan wajib untuk SEMUA controller/orkestrator.
8. **Format respons menentukan status edge**: bridge mendeteksi status semantik dari teks
   respons — sertakan baris `STATUS: complete|blocked|needs-review|failed` (atau
   `KODE: RT_BYPASS` / `BLOCKED:`) di akhir respons agar edge tercatat sesuai outcome
   asli, bukan sekadar `done` karena eksekusi selesai. Laporan blocked otomatis muncul
   di panel "Blocker terbaru" halaman `/orchestration`.

## Atribusi inisiator (WAJIB, FIX 02-09-2026 temuan #4)

Graf orkestrasi harus menunjukkan SIAPA memulai delegasi, bukan menyamakan semua edge
dengan `brahma`. Ada tiga jalur sah, dan setiap controller/orkestrator WAJIB memakai
jalur yang benar sesuai kondisinya:

| Jalur | Cara | Nilai `from` di graf |
|-------|------|----------------------|
| Login manusia di HQ/WebUI → dispatch | Tidak perlu aksi tambahan: rute `POST /api/brahma/dispatch` membaca cookie sesi dan mengisi `AgentRequest.requestedBy = user:<username>` | `user:<username>` (node virtual grup "Pengguna" di graf) |
| Agen controller dispatch via helper DB (`hq_dispatch.cjs` / `hq_dispatch_card.cjs`) | Helper mengirim arg ke-4 `[agentId]`; tanpa arg, nilai ditebak dari env `HERMES_DISPATCH_AGENT` lalu dari `HERMES_HOME` profil aktif | id profil pengirim (mis. `gspuser01`) |
| Agen controller dispatch via HTTP `POST /api/brahma/dispatch` (x-internal-secret) | Sertakan field body `"agentId": "<profil-mu>"` — WAJIB, karena pemanggil mesin tidak punya cookie sesi | id profil pengirim |

Aturan turunannya:

1. **Jangan mengaku brahma.** Controller non-default yang mengirim dispatch tanpa
   `agentId` via jalur mesin akan tercatat `brahma` dan mengaburkan graf; itu cacat
   pelaporan, sama seperti edge menggantung.
2. **Nama agen = nama folder profil** (`gspuser01`, `gsp-master`, dst.), bukan username
   login, saat pemanggilnya mesin. Username hanya dipakai untuk jalur browser.
3. **Edge manual `delegate/handoff/verify` tetap wajib** untuk interaksi lintas profil
   yang tidak lewat bridge (aturan 1-3 di atas); atribusi inisiator hanya memperbaiki
   sisi `dispatch`.
4. **Data historis jujur:** record lama tanpa inisiator tersimpan ditandai `user:web`
   (asal origin) atau tetap `brahma` (asal agen). Jangan menulis ulang from record lama
   ke username tertentu tanpa bukti.
5. **Verifikasi atribusi setelah dispatch pertama dari profil baru:** cek
   `GET /api/orchestration?limit=5` atau halaman `/orchestration`; edge baru harus
   ber-`from` id profil/akun-mu sendiri. Kalau masih `brahma`, berarti `agentId` belum
   terkirim — perbaiki pemanggilnya, jangan tutup mata.

## Hubungan dengan kontrak lain

- Documentation Contract (AGENTS.md GSP-2): artefak file tetap ditulis; telemetry ini
  adalah **indeks visual** dari interaksi yang menghasilkan artefak tersebut.
- `gsp-controller-templates` / `gsp-phase-accountability`: setelah gate fase ditutup,
  rekam edge `gate` (controller → controller lain atau controller → brahma).
- `gsp-agent-headquarter`: cara memulai/memverifikasi dashboard dan bridge.

## Verifikasi

```bash
curl -s "http://localhost:9011/api/orchestration" | python3 -m json.tool   # edge terlihat?
curl -s http://localhost:9011/orchestration                                  # HTTP 200
# atribusi (FIX 02-09): dispatch dari login user -> from=user:<username>;
# dispatch mesin dgn agentId -> from=<id profil>. Tanpa agentId via mesin = temuan cacat.
```
