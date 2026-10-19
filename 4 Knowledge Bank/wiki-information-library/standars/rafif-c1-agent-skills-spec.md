---
id: rafif-c1-agent-skills-spec
type: standar
title: Spesifikasi Open Standard Agent Skills + Mekanisme Aktivasi Claude.AI/Claude Code
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-10-11
catatan_verifikasi: "Verdict iterasi-2: terverifikasi || Dasar: re-verifikasi delta-only sesuai syarat vonis iterasi-1 (cacat kelas ALAMAT mekanis pada marker rujukan), bukan audit muatan ulang. || Bukti ukur custodian 2026-10-11: diff terhadap cadangan pra-retag (AppData/Local/Temp/c1.pre-etag.md) = tepat 12 baris body berubah (28,29,30,32,33,34,49,50,51,55,57,58) dan SELURUH perubahan berada di dalam kurung siku; prosa di luar kurung byte-identik per baris; multiset ID keluarga per baris invarian; multiset angka prosa luar-kurung grup body identik (123 token pra == 123 kini); EOL CRLF utuh (72 CRLF dari 72 LF); blok frontmatter pra-retag identik byte dengan kini (retag tidak menyentuh metadata). Sensus tag grup body pasca-retag: B-01..B-14 dan B-42 serta K-1 seluruhnya berada di bawah R-1 (matriks bukti), L1-01..L1-82 dan U-10/U-11 di bawah R-2 (L1_skill_spec), probe P-1..P-12 di bawah R-7 - nol sisa ID keluarga yang menempel di kurung tag rujukan lain, sehingga pembacaan literal kini mengalamat berkas yang benar. Sampling needle 30/30 titik angka beban pada baris tersunting (64/1024/500/~100 token/5.000/500 baris/satu lapis/1.536/25.000/v2.1.273/20 skill/30 MB/46 klien/19 skill/140 B/pushed_at 2026-10-09T18:45:52Z + baris B-01..B-14,B-42,K-1 matriks) tertelusur ke sumber beku; pin sha256[:16] 4/4 cocok (L1 17a31168b3cc676e, matriks 69b125e91103ccaa, L2 8086e5da4844a1f9, L3 32e41ac440292210). Metadata: yaml.safe_load lolos, 17 kunci pra-verdict nol duplikat (18 termasuk riwayat-catatan-verifikasi hasil suntingan ini), tepat satu ^status:, nilai frontmatter utuh (parsed == mentah), title == H1. || Riwayat: catatan_verifikasi iterasi-1 dipertahankan VERBATIM di kunci riwayat-catatan-verifikasi. Body tidak diubah oleh suntingan verdict ini (md5 grup body dipatok konstanta dd7fc09657285a68d15748a0e7aa9973)."
riwayat-catatan-verifikasi: "Verdict: perlu_revisi || Alasan: muatan sah - 19/19 angka tertelusur ke sumber beku (pin byte-identik 10/10), kelengkapan 21/21 butir proposa bagian 3, DISKREP K-1 dua angka berkonteks (200 vs 1024 char) hadir utuh bersama UNVERIFIED-LIVE, dedup wiki/vault 0 hit, YAML utuh; namun 14 rujukan marker menempatkan ID keluarga B di dalam kurung tag [R-2 ...] (baris objek 25,26,27,29x2,30,31,46,47,48,52,54,55x1+1) padahal baris B-01..B-14/B-42 hidup di matriks [R-1]; pembacaan literal mengalamatkan berkas salah walau seluruh isi baris B yang dirujuk terverifikasi cocok dengan angka objek (nol angka teknik berubah) - kelas ALAMAT mekanis sesuai preseden custodian 2026-09-24. || Rekomendasi: pecah kurung agar tiap ID membawa tag sendiri, mis. '[R-2 L1-03, B-01]' menjadi '[R-2 L1-03; R-1 B-01]' pada 14 rujukan itu; tidak ada angka yang perlu diubah; setelah retag objek layak terverifikasi tanpa audit ulang muatan."
sumber: docs/2026-10-10_rafif-gameskill-guide/research/lanes/L1_skill_spec.md (+ss. rujukan penuh di body; salinan beku vault/rafif-gameskill-1010/sources/)
halaman: ss.2 baris L1-01..L1-82; ss.4 D-1..D-5
tanggal_akses: 2026-10-11
kelas_bukti: primer
sensitif: tidak
perkara: rafif-gameskill-1010
tags: [agent-skills, claude, claude-code, spesifikasi, rafif-gameskill-1010]
links: [docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md, vault/rafif-gameskill-1010/sources/L1_skill_spec.md]
penulis: gsp-librarian
diajukan: 2026-10-11
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-10-11
dipromosikan-ke: standars/rafif-c1-agent-skills-spec.md
catatan_keputusan: "dipromosikan: RG21b t_98725c99: retag alamat sesuai vonis custodian iter-1; terverifikasi iter-2 2026-10-11"
---

# Spesifikasi Open Standard Agent Skills + Mekanisme Aktivasi Claude.AI/Claude Code

Objek baseline Information Library dari misi RAFIF-GAMESKILL-1010 (kandidat RAFIF-C1, lajur riset L1). Semua angka terukur ulang pada giliran promosi 2026-10-11 pukul 10:12-10:19 WIB (probe P-1..P-12) terhadap artefak riset beku ber-pin. Kelas bukti per baris: PRIMER = teks persis halaman resmi; PRIMER-DUA = dikonfirmasi dua sumber primer independen; DISKREP = dua sumber resmi bertentangan, keduanya dicatat.

## 1. Spesifikasi format (agentskills.io = rumah resmi open standard)

- Skill = direktori berisi minimal satu `SKILL.md` (YAML frontmatter + body Markdown); konvensi subfolder `scripts/` (kode eksekusi), `references/` (dokumentasi), `assets/` (template/sumber daya). [R-2 L1-01/L1-02, agentskills.io/specification.md]
- Field wajib `name`: maks 64 karakter; hanya huruf kecil, digit, hyphen; tidak boleh mulai/akhir dengan hyphen; tanpa hyphen beruntun; WAJIB sama dengan nama folder induk. [R-2 L1-03; R-7 P-1 token 'Max 64 characters'; platform.claude.com overview mengonfirmasi = PRIMER-DUA; R-1 B-01]
- Field wajib `description`: 1-1024 karakter, non-empty; harus memuat APA yang skill lakukan dan KAPAN dipakai. [R-2 L1-04; R-7 P-1 token 'Max 1024 characters'; PRIMER-DUA dengan platform overview; R-1 B-02]
- Field opsional `compatibility`: maks 500 karakter (syarat lingkungan; 'Most skills do not need the compatibility field'). [R-2 L1-06; R-7 P-1 token 'Max 500 characters'; R-1 B-04]
- Field opsional `license`, `metadata` (map string->string, key disarankan unik), dan `allowed-tools` (string tool pra-disetujui dipisah spasi; status EKSPERIMENTAL, dukungan bervariasi antar implementasi). [R-2 L1-05/L1-07/L1-08]
- Progressive disclosure 3 tahap: (1) metadata `name`+`description` ~100 token dimuat saat startup untuk SEMUA skill; (2) body `SKILL.md` dimuat saat aktivasi, disarankan < 5.000 TOKEN (satuan token, bukan kata); (3) resources dimuat hanya saat dibutuhkan. [R-2 L1-09; R-7 P-1 token '~100 tokens' dan '< 5000 tokens'; platform overview 'Under 5k tokens' = PRIMER-DUA; R-1 B-05, B-06]
- Body `SKILL.md` disarankan < 500 baris. [R-2 L1-10; R-7 P-1 token '500 lines'; platform best-practices + Claude Code docs = PRIMER-DUA; R-1 B-07]
- Referensi file memakai path relatif dari root skill dan dijaga SATU LAPIS dari `SKILL.md` (hindari rantai bertingkat). [R-2 L1-11; R-7 P-1 token 'one level deep'; R-1 B-08]
- Validator resmi: `skills-ref validate ./my-skill` mengecek frontmatter sah + konvensi penamaan. [R-2 L1-12; R-7 P-1 token 'skills-ref validate']

## 2. Mekanisme aktivasi claude.ai (permukaan chat)

- Skill tersedia di claude.ai untuk paket Free/Pro/Max/Team/Enterprise; butuh code execution aktif. [R-2 L1-20, support.claude.com art. 12512176]
- Aktivasi otomatis lewat pencocokan description ('Claude determines when each skill is needed'), atau eksplisit dengan menyebut nama skill. [R-2 L1-21, art. 12512180]
- Pasang skill custom: Settings nyalakan 'Code execution and file creation', lalu Customize > Skills > '+' > 'Create skill' > 'Upload a skill' berupa ZIP; struktur ZIP wajib folder skill sebagai root arsip dan nama folder sama dengan nama skill. [R-2 L1-22/L1-23]
- DISKREP cap `description` jalur claude.ai (dua angka berkonteks, bukan dipilih satu): dokumentasi Help Center art. 12512198 menulis 'maximum 200 characters' untuk skill custom claude.ai, sedangkan spesifikasi resmi dan platform docs menetapkan maks 1024 char. Rekomendasi putusan kerja (K-1): desain paket pada INTERSEKSI terketat <= 200 char; kedua angka tetap disebut dengan konteksnya. Perilaku validator UI claude.ai (penolakan > 200 char) berstatus UNVERIFIED-LIVE (butuh login; yang terverifikasi hanya teks dokumentasinya). [R-2 L1-24; R-1 K-1; R-7 P-6 art. 12512198 HTTP 200]
- Field `dependencies` (daftar paket) muncul hanya di Help Center claude.ai, TIDAK ada di spec resmi; paket portabel menyimpan syarat paket di body/`compatibility`. [R-2 L1-25, D-2]

## 3. Mekanisme aktivasi Claude Code (permukaan terminal/IDE)

- Skills Claude Code mengikuti open standard; custom commands merger ke skills (`.claude/commands/deploy.md` setara `.claude/skills/deploy/SKILL.md`). [R-2 L1-40]
- Aktivasi dua jalur: otomatis saat tugas cocok `description`, atau manual `/skill-name`. [R-2 L1-42]
- Anggaran listing: gabungan `description`+`when_to_use` dipotong pada 1.536 char per skill; budget total listing = 1% jendela konteks. [R-2 L1-45; R-7 P-2 HTTP 200; R-1 B-09]
- Auto-compaction: skill teraktivasi dilampirkan ulang pasca-ringkasan dengan plafon 5.000 token pertama per skill dan budget gabungan 25.000 token -> instruksi terpenting harus di bagian ATAS `SKILL.md`. [R-2 L1-46; R-1 B-10]
- Sinkronan akun: skill yang di-enable di claude.ai ikut termuat di Claude Code (login akun yang sama) via sync satu-arah ke `~/.claude/skills/synced/` mulai Claude Code v2.1.273; tidak sync bila login pakai API key/Bedrock. [R-2 L1-27; R-1 B-42]

## 4. Limit API dan ekosistem

- Skills API: maks 20 skill per request; ukuran upload skill maks 30 MB (total semua berkas, uncompressed); container API tanpa akses jaringan dan tanpa instal paket runtime. [R-2 L1-81, platform.claude.com skills-guide; R-1 B-11]
- Portabilitas lintas permukaan: jalur claude.ai upload, Skills API, dan packaging hanya menerima 6 field spec (`name`, `description`, `license`, `metadata`, `allowed-tools`, `compatibility`); field di luar itu = hard error saat upload/packaging. [R-2 L1-48]
- Ekosistem: 46 klien terdaftar mendukung format (termasuk GitHub Copilot, Cursor, Hermes Agent; token klien terverifikasi ulang pada probe giliran promosi). [R-2 U-11; R-7 P-9 clients.md 25.457 B identik, token 'Hermes Agent' x2, 'GitHub Copilot' x2, 'Cursor' x7; R-1 B-12]
- Repo contoh `anthropics/skills` berisi 19 skill (template minimal 140 B = `name`+`description` saja); push terakhir 2026-10-09T18:45:52Z terverifikasi ulang pada giliran promosi. [R-2 U-10; R-7 P-12 pushed_at identik; R-1 B-13, B-14]
- Spesifikasi dipublikasikan sebagai open standard (pengumuman revisi blog rekayasa Anthropic 18-12-2025). [R-2 L1-82]

## 5. BATAS dan prospektif

- Kelas bukti objek ini PRIMER (sintesis lintas sumber resmi Anthropic/agentskills.io); baris bertanda DISKREP memuat dua angka resmi yang bertentangan dan keduanya wajib disebut, dilarang memilih satu.
- Register terlarang yang TIDAK masuk objek ini: perilaku validator UI claude.ai sebagai fakta live (UNVERIFIED-LIVE), dan klaim nama model dari artefak hulu lain (belum uji per-field).
- Sumber web berubah; prosedur DELTA: bandingkan terhadap salinan beku di `vault/rafif-gameskill-1010/sources/` (pin tabel rujukan), bukan berkas hidup.

## 6. Register rujukan

- [R-1] `vault/rafif-gameskill-1010/sources/06_evidence_matrix.md` (53.891 B, sha256[:16] 69b125e91103ccaa) ss.5 keputusan K-1; ss.7 baris B-01..B-14, B-42.
- [R-2] `vault/rafif-gameskill-1010/sources/L1_skill_spec.md` (39.682 B, sha256[:16] 17a31168b3cc676e) ss.2 baris L1-01..L1-82, ss.4 D-1..D-5.
- [R-5] `vault/rafif-gameskill-1010/sources/02_freshness_test.md` (24.736 B, sha256[:16] 8c1702cf52c56016) ss.2 baris 1-2.
- [R-7] Probe hidup giliran librarian 2026-10-11 10:12-10:19 WIB (P-1 agentskills.io/specification.md 200 + 7/7 token; P-2 code.claude.com/docs/en/skills.md 200; P-6 support.claude.com art. 12512198 200; P-9 clients.md identik; P-12 api.github.com anthropics/skills identik) per tabel 2.2 `docs/2026-10-10_rafif-gameskill-guide/research/99_promotion_proposal.md` (sha256[:16] cc2cf2e093641ecf).
