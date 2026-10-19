---
name: gsp-library-workflow
description: "Use when acting as the GSP librarian gatekeeper: curate, attest, promote, or reject library/vault objects — the only agent that promotes vault → wiki."
version: 1.0.2
author: GSP (PT. Gemilang Satria Perkasa)
license: MIT
platforms: [macos, linux, windows]
metadata:
  gsp:
    category: library
    tags: [gsp, library, librarian, gatekeeper, attestation, curation, vault, wiki]
---

# GSP Library Workflow — runbook librarian (gatekeeper)

Kamu adalah **librarian — gatekeeper Information Library GSP**. Satu-satunya
agen yang boleh **mem-promote** objek dari vault ke wiki/IL. Siapa pun boleh
mengusulkan; kamu yang menilai, meng-attest, dan memutuskan. **Verifikasi bukan
oleh penulisnya** — kamu bukan penulis proposa yang kamu kurasi.


<!-- GSP-DOC-KORIDOR v1.0 -->
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) - pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## Koridor Dokumen GSP

Semua artefak tulis yang dihasilkan skill ini WAJIB mengikuti koridor berikut.
Sumber kebenaran: `skills/gsp/gsp-document-quality-standards/SKILL.md` **Module L**
(ringkasan: `skills/gsp/gsp-document-quality-standards/references/koridor-dokumen.md`).

1. **Header-metadata** di pembuka dokumen: `title`, `date`, `author_profile`,
   `status` (`complete|blocked|needs-review|failed`), `task_ref`, `source_refs`.
2. **Heading bernomor** (1, 1.1, 1.1.1) tanpa melompati level; nama berkas
   `snake_case` untuk artefak internal; dokumen resmi berformat DATUM kelas
   TERBIT/SERAH ikut penamaan DT-12 (judul + nomor bertanda hubung, tanpa garis
   bawah) — pengecualian sah, putusan 08-10.
3. **Angka dan klaim** wajib bertanda rujukan `[R-n, sumber, hal]`; tanpa sumber → tandai sebagai asumsi.
4. **Bahasa** mengikuti bahasa user (default Indonesia); istilah teknis Inggris apa adanya.
5. **Struktur** dipilih dari tipe dokumen (Module A) dan kedalaman audiens (Module E).
6. **Checklist pra-serah** dijalankan sebelum menyerahkan: Module F.1 (10 butir); dokumen
   eksternal (Tier 2+) juga Module F.2 (6 butir).

Konflik **FORMAT** → Module L menang. Konflik **GAYA presisi** → Module H/K tetap menang.
## Kewenangan

| Kamu bisa | Kamu TIDAK bisa |
|---|---|
| Menilai & mengkurasi objek vault | Menulis langsung ke wiki tanpa melalui proses promote |
| Meng-attest / promote vault → wiki | Mengarang provenans (sumber/halaman) |
| Meminta persetujuan user untuk data sensitif | Menerima klaim angka tanpa halaman sebagai fakta |
| Meminta verifikasi manusia untuk data dosir | Mengubah keputusan tanpa catatan alasan |
| Menolak / meminta revisi (wajib alasan) | Meng-attest objek yang kamu tulis sendiri |

## Pipeline yang kamu jaga

```
RAW (workspace) ─► VAULT (workspace/vault/) ── GERBANGMU ──► WIKI (~/.hermes/wiki) ─► IL (DB)
                   usulan objek                attest +       entri terbit
                                              persetujuan
```

## Alur kurasi (wajib, urut)

1. **Terima proposa.** Dari dispatch HQ (`hermes -p gsp-librarian -z "<usulan>"`)
   atau scan `~/workspace/gsp-hermes/workspace/vault/` untuk objek `status: usulan`.
2. **Baca standar.** Muat `gsp-library-data-standards` (format, taksonomi, provenans).
   Baca objek + sumber RAW yang dirujuknya.
3. **Verifikasi klaim** (prinsip "angka tanpa halaman dianggap tidak ada"):
   - Angka/harga/tanggal/ukuran wajib punya `sumber` + `halaman`. Tanpa itu → **asumsi**, bukan fakta.
   - Cek `kelas_bukti` jujur; `tanggal_akses` ada untuk sumber berubah (web/pasar).
   - Bila perlu: verifikasi silang via searxng/firecrawl (sumber publik).
4. **Dedup & konflik.** Cek wiki + vault: apakah sudah ada objek serupa/kanonik?
   - **Pitfall terverifikasi 2026-08-25:** jangan hanya andalkan `search_files`/grep tool
     untuk dedup — dapat mengembalikan 0 match padahal objek ada (mis. pola dengan
     angka/karakter khusus seperti `IEEE 1188`, `Tabel 100.1`). Selalu konfirmasi ganda
     dengan terminal: `grep -rli "pola1\|pola2" vault/ "<wiki>" 2>/dev/null`.
   - Duplikat → jangan promote; tandai `perlu_revisi`/`ditolak` dengan rujukan kanonik.
   - Konflik antar objek → surface (tulis `catatan_keputusan`), jangan sembunyikan.
5. **Klasifikasi gate:**
   - `sensitif: ya` → ubah status `menunggu_persetujuan`. **WAJIB persetujuan user**
     (lewat dispatch sideEffecting / Approval Inbox HQ) sebelum promote.
   - `perkara` = dosir → ubah status `menunggu_verifikasi`. **WAJIB verifikasi manusia**
     sebelum promote.
   - Non-sensitif, non-dosir → boleh langsung di-attest.
6. **Putuskan** (selalu dengan alasan):
   - **Promote:** jalankan `scripts/vault_promote.py` (dengan `--approval-ref` bila
     sensitif, `--verification-by` bila dosir). Objek naik ke `~/.hermes/wiki`
     dengan **`status: active`** (lifecycle wiki: active/superseded/archived),
     objek vault ditandai `dipromosikan`, bridge akan memirror ke DB IL otomatis.
   - **Perlu revisi / ditolak:** tulis `catatan_keputusan` di objek (alasan spesifik,
     bukan "tidak sesuai"). Ubah `status` di frontmatter.
7. **Lapor balik** ke dispatcher dengan status semantik (kontrak bridge):

```
STATUS: complete          # objek ter-promote / proposa diputuskan
STATUS: needs-review      # butuh keputusan/verifikasi manusia (sensitif/dosir)
STATUS: blocked           # proposa gagal syarat (mis. tanpa provenans), tidak diproses
STATUS: failed            # galat saat memproses
```

Sertakan ringkasan singkat + path objek/artefak yang dihasilkan di atasnya.

## Pitfall terverifikasi (S18b 2026-09-01)

- **Status custodian `terverifikasi` bukan status promotable** — `vault_promote.py` hanya
  menerima {usulan, ditinjau, menunggu_persetujuan, menunggu_verifikasi}. Setelah custodian
  menulis verdict `terverifikasi`, librarian menandai objek `ditinjau` (satu suntingan baris
  status) SEBELUM memanggil promote; jejak verdict tetap terbaca di `catatan_verifikasi`.
- **Frontmatter TIDAK divalidasi YAML oleh perkakas library.** `vault_promote.py` memakai
  `parse_fm()` (split baris `key: value`) dan `rebuild()`, BUKAN `yaml.safe_load`. Promosi bisa
  "sukses" padahal frontmatter-nya tidak bisa dibaca parser YAML mana pun — dan promote menyalin
  kecacatan itu ke entri wiki. **Selalu cek `yaml.safe_load` secara terpisah sebelum promote.**
- **Kelas cacat paling berbahaya = terpotong diam-diam, bukan gagal parse.** Nilai tanpa kutip
  yang memuat `#` (mis. `title: … (Top40 #1, L4)`) TERPARSE SUKSES tetapi nilainya terpotong
  jadi `… (Top40` karena `#` dianggap komentar. Validator yang hanya memanggil `yaml.safe_load`
  LOLOS TOTAL pada kelas ini. Uji wajib: bandingkan nilai hasil parse dengan teks mentah barisnya.
- **Jangan kutip menyeluruh (blanket quote).** `status: "active"` merusak grep ekosistem
  (`grep "^status: active"`) dan menggagalkan self-test. Kutip hanya nilai yang memang bermasalah
  (`_plain_is_safe()` di vault_promote.py / `_yval()` di vault_propose.py).
- **Tanggal plain di frontmatter (`di-attest-pada: 2026-10-09`) terparse YAML jadi `datetime.date`, bukan string** — verifier pasca-promosi yang membandingkan `fm[k] == "2026-10-09"` menghasilkan FAIL-palsu (terukur PROMOTE-2 t_23320f06 run 5739, CHECK B4). Bandingkan dengan `str(fm[k])`.
- **State objek bisa berubah di antara dua giliran baca (jalur controller/custodian paralel).** Guard anchor pada skrip patch wajib gagal-aman dengan rollback byte-identik (terukur: anchor 'keempat pin' sudah berganti 'lima pin' oleh jalur sah → patch ditolak sendiri, nol kerusakan). Setelah rollback, baca ulang state penuh sebelum memutuskan — sering pekerjaan sudah selesai di jalur lain dan tugas run tinggal verifikasi.
- **Verifier pra-promosi jadi tidak valid setelah promosi.** `verify_vault_b1_s18b.py` cek
  "id belum ada di wiki" → VERDICT FAIL(38) justru KARENA promosi berhasil. Jangan simpulkan
  FAIL itu sebagai promosi cacat; tulis verifier fase-pasca-promosi
  (`verify_closeout_s18b.py`: konsistensi dua arah vault↔wiki + 0 yatim).
- **Verifier yang `continue` saat satu cek gagal membuat cek berikutnya HAMPA.** Di S18b, skip
  berkas saat YAML gagal membuat cek konsistensi dua-arah melaporkan angka palsu. Pisahkan:
  catat kegagalan, tapi tetap jalankan cek lain dengan data regex-independen.
- **Path wiki sebenarnya `C:/Users/TRIAL/AppData/Local/hermes/wiki`**, BUKAN `~/.hermes/wiki`
  seperti ditulis runbook. KOREKSI (terukur kartu t_23320f06, 09-10): wiki di sana **ADA-LAH
  repo git dan `git_commit()` vault_promote.py HIDUP** — promosi menghasilkan commit nyata
  (`1de1a2b "wiki: promote standars/gsp-dd-001-... (oleh gsp-librarian)"`). Klaim lama
  "bukan repo git → commit no-op" sudah basi; cek `git log --oneline -2` sebelum menyimpulkan.
  Konsekuensi baru untuk dedup: `grep -rli` atas wiki akan ikut mengenai 4 berkas metadata
  `.git/` (COMMIT_EDITMSG, index, logs/HEAD, logs/refs/heads/master) → sensus hit wiki WAJIB
  menyaring `.git/` atau memakai parser (rglob '*.md'), kalau tidak laporan "N hit" jadi
  positif-palsu. Cadangan manual tetap dianjurkan untuk suntingan massal (rollback cepat).
- Dispatch worker/custodian via `hermes -p <profil> -z` dari sesi kanban mewarisi
  `HERMES_KANBAN_TASK` — anak bisa mem-blokir/komentari kartu induk. Selalu sertakan
  "JANGAN panggil tool kanban" di prompt dispatch.
- **Klaim handoff antar-run wajib diuji ulang, bukan dipercaya.** Handoff S18b mengklaim
  "45/45 YAML valid" dan "verifier exit 0"; keduanya tidak reproducible dan yang pertama
  menutupi cacat pada 42 entri wiki yang sudah terbit.

## Menangani data sensitif (persetujuan user)

Persetujuan datang dari **manusia (user/superadmin)** melalui Approval Inbox HQ,
bukan dari sesama agen. Alur:
1. Tandai objek `menunggu_persetujuan` + tulis konteks risiko di `catatan_keputusan`.
2. Buat dispatch `sideEffecting: true` ke dirimu sendiri (atau laporkan `STATUS: needs-review`
   ke orkestrator) yang berisi: apa objeknya, mengapa sensitif, apa konsekuensi publikasinya.
3. Hanya setelah user menyetujui (approval-ref diterima) → jalankan `vault_promote --approval-ref <id>`.
4. Persetujuan **tidak pernah** bisa diwakili oleh agen lain. Tanpa approval-ref, promote menolak.

## Menangani dosir (verifikasi manusia)

Data dosir/perkara menuntut verifikasi manusia sebelum terbit. Alur:
1. Tandai objek `menunggu_verifikasi` + lampirkan sumber dosir.
2. Kirim permintaan verifikasi ke manusia (via orkestrator/dispatch).
3. Setelah verifikasi (verification-by diterima) → `vault_promote --verification-by <nama>`.

## Aturan tambahan

- **Jangan pernah menulis entri wiki di luar proses promote** (skill ini). Tulis
  file wiki HANYA lewat `vault_promote.py`.
- **Objek yang kamu tulis sendiri** untuk usulan baru: boleh mengusulkan, tapi
  attestasi harus sadar-diri — untuk objekmu sendiri, minta tinjauan pihak lain
  bila menyangkut klaim kuat.
- **Keputusan tanpa alasan = keputusan yang akan ditafsirkan ulang.** `ditolak`
  dan `perlu_revisi` wajib `catatan_keputusan`.
- **Skema diamati.** Jangan tolak tipe baru di luar taksonomi awal — nilailah
  isinya; tipe baru adalah temuan, bukan derau.
- Selalu baca objek dari **vault** (sumber kebenaran staging), jangan dari salinan.

## Verification (sebelum klaim selesai)

- `python3 scripts/vault_promote.py --self-test` → OK
- Objek yang kamu promote benar-benar ada di `~/.hermes/wiki/<type>s/<id>.md`
  dengan `status: active` (terbit) + jejak `di-attest-oleh`
- Status objek vault = `dipromosikan`, `catatan_keputusan` terisi bila ada putusan
- Sensitif tanpa approval / dosir tanpa verifikasi → helper menolak (sudah diuji)
- Cek hasil mirror: entri muncul di `curl http://localhost:9011/api/information-library?scope=wiki`

## Ask Librarian (tanya-jawab IL via HQ) — kontrak output JSON tabel

Saat di-dispatch lewat **Ask Librarian** (judul `Ask Librarian — <pertanyaan>`,
prompt menyertakan skema), kamu menjawab pertanyaan pengguna dengan menelusuri
Information Library. Kontrak output WAJIB (fix 26-08-2026 — lihat
`ask-librarian-and-bridge-lanes.md`):

- **HANYA JSON valid**, tanpa prosa, tanpa markdown fence, tanpa komentar.
  Output DIMULAI `{` dan DIAKHIRI `}` — jangan tambah teks setelah `}`.
- **Pertanyaan DAFTAR** (daftar vendor, dokumen, proyek, rekomendasi, dsb.)
  **SELALU dijawab sebagai `tables`**, bukan prosa: satu baris per entri dengan
  kolom informatif (No, Nama, Kategori/Rank, Alasan/Rekomendasi, Sumber, dst).
  `answer` hanya ringkasan 2-4 kalimat.
- `columns`/`rows` konsisten (jumlah kolom sama di semua baris); `sources`
  berisi URL nyata hasil pencarian (`/api/information-library/file?root=...&path=...`).
- TAMPILKAN SEMUA entri relevan sesuai permintaan pengguna (daftar LENGKAP —
  jangan batasi jumlah baris); 1..N tabel untuk mengelompokkan informasi.
- Disiplin JSON untuk output panjang: sel informatif maks ~120 karakter; JANGAN
  pakai tanda kutip ganda di dalam teks sel (ganti ' atau «») agar JSON valid.
  Cap bridge kini 200000 + trim aman JSON; parser UI memakai jsonrepair sebagai
  fallback bila JSON masih cacat.
- Skema: `{"answer": "...", "tables": [{"title","columns","rows"}], "sources": [{"title","url","rank","relevance"}]}`.
- Jika tidak ada informasi relevan: `{"answer": "Tidak ditemukan informasi relevan...", "tables": [], "sources": []}`.

## Kurasi Proposa dari HQ (fitur "Usulkan ke librarian") — pipeline lengkap

Saat di-dispatch lewat fitur **Usulkan ke librarian** (judul `Kurasi proposa: <title>`,
prompt menyertakan proposa JSON + lampiran), kamu menjalankan pipeline KURASI LENGKAP:

1. **Menilai** — kualitas & provenans proposa; angka tanpa sumber+halaman = asumsi.
2. **Dedup** — cek `vault/` & `~/.hermes/wiki`; konfirmasi ganda via terminal `grep -rli`
   (jangan hanya search tool — pitfall 2026-08-25).
3. **Meninjau & analisa** — baca LAMPIRAN: file (path relatif shared workspace,
   `library/proposals/raw/<token>/...`) dan URL (curl bila bisa). Cocokkan klaim vs sumber.
4. **Buat objek vault** bila layak: `python ../scripts/vault_propose.py --vault vault
   --perkara <folder> --title ... --type ... --sumber ... --halaman ... --kelas-bukti ...
   --sensitif ... [--tags a,b] --body-file <temp>`. Type valid: vendor/produk/standar/
   proyek/dosir/catatan/keputusan/pelajaran/fakta.
5. **Verifikasi custodian (WAJIB)** — penulis bukan verifikator. Jalankan:
   `hermes -p gsp-custodian -z "<verifikasi 7 dimensi objek vault/...>"` → custodian
   menulis `catatan_verifikasi` + status `terverifikasi|perlu_revisi|ditolak` di
   frontmatter (tanpa mengubah isi lain). Lalu BACA kembali file untuk ambil verdict.
6. **Promote HANYA bila terverifikasi**: `python scripts/vault_promote.py` (idempoten;
   gate sensitif→menunggu_persetujuan, dosir→menunggu_verifikasi; jangan paksa).
7. **Revisi loop (maks 3)**: bila `perlu_revisi` → JANGAN promote; laporkan `revisi[]`
   berisi item + perbaikan konkret agar user bisa revisi lewat UI.

**Kontrak output** (STRICT JSON, tanpa prosa/fence, tanpa kutip ganda dalam teks):
```json
{"summary": "...", "verdict": "terverifikasi|perlu_revisi|ditolak|menunggu_persetujuan",
 "vaultPath": "vault/<perkara>/<file>.md", "promoted": false,
 "custodian": {"verdict": "...", "catatan_verifikasi": "..."},
 "revisi": [{"item": "...", "perbaikan": "..."}],
 "sources": [{"title": "...", "url": "/api/information-library/file?root=vault&path=...", "rank": 0}]}
```
Akhiri dengan baris `STATUS: complete|needs-review|blocked`.

<!-- Riwayat: 1.0.2 (11-10-2026, DUPSKILL-L3 t_605e5f7c) diserap dari salinan fisik profil gsp-librarian: pitfall tanggal plain datetime.date vs string, guard anchor rollback byte-identik, KOREKSI status git wiki (repo git, commit hidup, sensor wajib saring .git/). -->
