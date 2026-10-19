---
name: gsp-tool-adoption-pipeline
description: Use when adopting an external tool/MCP into the fleet.
license: MIT
version: 1.0.0
metadata:
  hermes:
    tags: [gsp, orchestration, mcp, supply-chain, windows]
    category: gsp
---

# Tool Adoption Pipeline — eval & pasang alat pihak ketiga ke fleet GSP

Preseden: misi GRAFT-0909 (trailhq/Graft, npm `@nanonets/graft`), semua gerbang di bawah
terjalankan dan terbukti bekerja 11-09. Kelas tugas: user menunjuk repo/paket eksternal dan
meminta "pelajari X dan terapkan di swarm". Ini BUKAN pekerjaan worker riset — ia misi
bergerbang dengan kontrak + kartu per tahap.

## Urutan gerbang (WAJIB, jangan dibalik)

1. **SEK dulu, instal kemudian.** Kartu audit keamanan paralel dengan studi mekanisme:
   lifecycle scripts npm (pre/postinstall), permukaan jaringan (grep fetch/http di src+dist),
   permukaan tulis disk (di repo & machine-wide), dependensi & native binaries, provenance
   (organisasi, attestation, SECURITY.md), telemetri. Keluaran: vonis
   AMAN / AMAN-DENGAN-SYARAT / TIDAK AMAN + syarat bernomor S-1..S-n dengan bukti path:line.
   Vonis SEK mengikat semua tahap hilir.
2. **Instal terisolasi, versi terkunci.** Unduh tarball, cocokkan `sha512/sha1` lokal vs
   `npm view <pkg> <ver> dist --json` (anchor rantai pasok), lalu
   `npm install ./pkg-x.y.z.tgz --ignore-scripts --save-exact` di direktori uji
   (mis. `gsp-data/tools/_npm-<tool>/pilot`). Dilarang `npm i -g`, dilarang di repo produksi.
3. **Snapshot isolasi sebelum/sesudah.** Scan depth-1 home + direktori config agen
   (`~/.claude`, `~/.codex`, `~/.gemini`, `LOCALAPPDATA/hermes`) sebagai
   `{path: {entry: [mtime,size]}}`; bandingkan sesudah. Delta hanya boleh whitelist yang
   diputuskan controller di Decision Log (mis. state dir milik tool). Pakai
   `scripts/snapshot_diff.py` — perbandingan HARUS via `json.dumps` equality (tuple vs list
   pasca-roundtrip JSON memberi ratusan false-positive bila bandingkan mentah).
4. **Telemetri mati berlapis + bukti.** Env `DO_NOT_TRACK=1` di SEMUA invocation, disable
   bawaan tool, lalu buktikan tiga cara: status tool, isi berkas state tool
   (mis. `~/.graft/telemetry.json` `"enabled": false`), dan mode debug tool.
5. **Wiring ke Hermes lewat CLI resmi, per profil.**
   `hermes -p <profil> mcp add <nama> --env KEY=VAL --command <biner-lokal> --args <...>` —
   CLI interaktif menanyakan "Enable all N tools? [Y/n]": pipe `echo "y" |` untuk run naskah.
   Verifikasi `hermes -p <profil> mcp list`. Sesi BARU membaca config tanpa restart
   gateway/bridge/HQ (restart = wewenang user; kalau ternyata butuh restart: STOP, ajukan
   putusan). Jangan pernah `init --yes` / tulis machine-wide alat pihak ketiga.
   Probe server stdio dulu dengan `scripts/probe_mcp_stdio.sh`; gagal probe = jangan daftarkan.
6. **Ukur biaya schema-per-turn sebelum klaim murah.** Probe prompt identik
   ("Balas hanya: OK") sebelum vs sesudah registrasi; baca angka dari
   `<profil>/state.db` tabel `sessions` (`source='cli'`, kolom `input_tokens`,
   `output_tokens`, `api_call_count`). Di root `~/.hermes/state.db` kolomnya
   `profile_name` (BUKAN `profile`). Sahkan ambang rollback SEBELUM ukur (preseden: >10%
   baseline = `hermes mcp remove`; hasil Graft +3,1% = aman).
7. **Bukti pemakaian nyata (P6), bukan narasi.** Spawn sesi CLI baru yang DIPERINTAH
   memanggil tool target; jejak diambil dari tabel `messages` profil
   (`tool_name LIKE '%<nama>%'`, kolom `tool_calls`, `content`). Silang-cek angka jawaban
   agen dengan pengukuran independen (preseden: agen jawab "16" kluster == 16 di
   `graft map --json`).
8. **Rollback drill wajib.** remove → sesi baru mengonfirmasi tool hilang → add ulang →
   list pulih. Rollback yang belum dilatih bukan rollback.
9. **Manfaat diukur sendiri, ambang terkunci sebelum eksekusi** (standar anti-blind user):
   A/B >=3 tugas nyata; lulus bila median tool-call lengan-with <= 80% without pada >=2/3
   DAN ketepatan berkas tidak turun di semua tugas. Ground truth disusun pihak verifier,
   BUKAN pelaksana (pihak yang diuji tidak membuat kunci jawabannya). Angka vendor selalu
   berlabel klaim-vendor, dilarang masuk kolom hasil.
10. **Distribusi skill hanya setelah A/B lulus**, via `gsp-skill-manager` (G-1), sebagai
    USULAN tanpa rollout; rollout = misi tersendiri dengan persetujuan user.

## Pitfall Windows (terbukti 11-09; resep lengkap references/windows-node-gyp-msvc.md)

- Paket dengan grammar/modul native (tree-sitter dll.) bisa TIDAK ship `prebuilds/win32-x64`
  padahal CLI-nya eager-import semua grammar saat start → crash `node-gyp-build: No native
  build was found` justru KARENA `--ignore-scripts` (syarat langkah 2). Diagnosis: cek
  `prebuilds/` per paket + `grep 'from "tree-sitter' dist/`. Fix sah: compile ulang HANYA
  paket itu dengan node-gyp + MSVC BuildTools via penangkapan env vcvars dari bash
  (resep di references). Bukan jalur terlarang: tidak menambah kode pihak ketiga
  (parser.c sudah ada di tarball hash-cocok); catat sebagai restatus di Decision Log.
- Berkas `.bat` ditulis dari git-bash ber-LF → cmd salah baca; butuh `sed -i 's/$/\r/'`.
  Lebih andal sama sekali: jangan pakai .bat, tangkap `vcvars64.bat && set` ke file lalu
  export ke bash dan jalankan node-gyp langsung.
- `hermes mcp add` tanpa TTY menunggu jawaban "Enable all N tools?" selamanya → pipe `y`.

## Pitfall terminal Hermes (hardline gate)

- Payload inline besar (heredoc python panjang, one-liner raksasa) DITOLAK gerbang parser
  `BLOCKED (hardline)` dan disimpan ke `%LOCALAPPDATA%/hermes/cache/blocked-scripts/*.sh`.
  Jangan retry inline; tulis skrip via write_file lalu `bash C:/path/ke/script.sh`.
  Simpan python parser kecil sebagai `.py` terpisah, jangan heredoc dalam pipe.
- Program native (python/node/git) butuh path `C:/...` (forward slash), BUKAN `/c/...`.

## Support files

- `references/graft-0909.md` — ringkasan kasus acuan: anatomi Graft, vonis SEK, hasil
  Tahap A/B terukur, resep skor P2 (`hits[].pointer` top-3 vs ground truth terkunci).
- `references/windows-node-gyp-msvc.md` — resep vcvars-capture + diagnosis prebuilds.
- `scripts/probe_mcp_stdio.sh` — probe JSON-RPC initialize+tools/list ke server MCP stdio.
- `scripts/snapshot_diff.py` — snapshot/diff isolasi dengan perbandingan json benar.

## See also

- `gsp-orchestration-execution` — jejak wajib (kartu, kontrak doc, trace) untuk setiap tahap.
- `gsp-fleet-profile-operations` — operasi profil/bridge bila wiring menyangkut fleet luas.
- `gsp-verification-before-completion` — predikat L1/L2; "terpasang" != "terapkan".
