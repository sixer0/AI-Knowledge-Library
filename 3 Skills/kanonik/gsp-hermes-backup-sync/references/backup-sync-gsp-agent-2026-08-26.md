# Backup sync gsp-agent (2026-08-26) — catatan sesi nyata

## Konteks
`gsp-agent` = repo backup GSP (salinan org `gemilang-perkasa/gsp-agent`, 1 commit
awal 24-08). Isi: `docs-backup/` (5 file), `engine/` (mirror hermes-agent lokal),
`hermes-home/` (HERMES_HOME). Clone pertama 26-08 ke `C:/Users/TRIAL/gsp-agent`
(79 MB, 13.053 file, credential store menangani auth — username per-host sudah
dipatok).

## Diff sebelum sync (26-08)
- engine/ vs hermes-agent lokal: 630 changed, 381 only-lokal (update upstream +
  2 carried commits GSP), 41 only-repo (docs/agents/* pindah upstream,
  tests/stress/* dihapus upstream, artefak default.tar.gz/log.txt).
- hermes-home/ vs $LOCALAPPDATA/hermes: 778 changed, 3380 only-lokal
  (mayoritas wiki/vendors/* = knowledge base IL + profil baru `firmanhidayat`
  + cron/output), 385 only-repo (curator blobs lama, config.yaml.bak, cache).

## Insiden & fix
1. **Runtime state lolos filter (separator bug)** — filter Python memakai
   `rel.startswith('cron/ticker_')` tapi `os.walk` menghasilkan `cron\ticker_...`
   (backslash di Windows) → 127 file runtime ter-stage di pass pertama, 168 lagi
   (channel_directory.json, models_dev_cache.etag, ticker per 40 profil) di pass
   kedua. Fix: normalisasi `rel = rel.replace('\\','/')` di awal fungsi filter.
   Pelajaran: SELALU normalisasi separator sebelum cocokkan nama/path.
2. **GitHub 100 MB limit** — `hermes-home/webui/bootstrap-9012.log` (183 MB,
   115.189 baris) lolos karena `*.log` tidak di-exclude; pre-receive hook
   menolak push. Fix: `git rm --cached` + hapus file + `.gitignore` tambah
   `hermes-home/**/*.log` + `hermes-home/webui/attachments/` + amend commit.
   Cek sebelum push: `git ls-tree -r -l HEAD | sort -k4 -rn | head`.
3. **File runtime tracked dari backup lama** — setelah rm --cached, 169 file `D`
   tertinggal (ticker, executions.db, channel_directory, models cache per
   profil). Semua runtime → commit penghapusan agar repo lean.

## Verifikasi akhir
```
git ls-remote origin refs/heads/main == git rev-parse HEAD  ✓ SINKRON
git status --short = 0
```
Commit final: c8a7cc1 (backup 26-08) setelah amend 0ed63cd (buang 183MB log).

## Angka backup final (26-08)
- engine: +689 update, -32 hapus
- hermes-home: +3.712 copy (685 wiki vendors, 91 skills, profil firmanhidayat),
  295 runtime di-unstage/dibuang
- file terbesar di repo setelah bersih: 4.1 MB (models_dev_cache.json lama,
  sudah ter-track sejak backup 24-08)
