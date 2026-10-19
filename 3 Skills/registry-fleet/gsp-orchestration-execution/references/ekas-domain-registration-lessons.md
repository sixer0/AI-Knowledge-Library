# Registrasi domain EKAS — aktivasi rantai, GT RBAC domain-lokal, dan pemulihan (pelajaran CVLK-0929, 29-30/09)

Kelas misi: domain rak EKAS -> objek vault -> custodian -> promote wiki/IL -> rute memori fleet -> VERIF akun RBAC undian -> laporan home channel. Lapisan ini berlaku UNTUK SEMUA domain baru selain yang sudah tercatat di [`knowledge-register-multi-domain.md`](knowledge-register-multi-domain.md) / [`knowledge-activation-rbac-verification.md`](knowledge-activation-rbac-verification.md).

## 1. Gap aktivasi: rantai hasil studi WAJIB hidup di folder rak sebelum VERIF
Preseden CVLK C2: rantai jaminan berasal dari studi tapi hanya ada di objek vault; akun VERIF menjawab dari FOLDER domain (baris rute memori menunjuk folder) dan menjawab faktual benar "RANTAI BELUM ADA" -> gerbang FAIL 6/9 yang cacatnya hulu controller, bukan akun.
Aturan turun-temurun (D-14): untuk domain yang rantainya BARU disusun dari studi (bukan RANTAI-JAMINAN.md warisan), penerbitan rantai ke folder domain adalah PRASYARAT dispatch VERIF. Bentuknya: berkas `RANTAI-JAMINAN.md` salinan VERBATIM bagian rantai objek + kepala pointer "objek kanonik: <slug> (sha256 ...)" + catatan terbit pasca-VERIF. Kartu FIX hanya menambah berkas, tidak menyentuh objek/rute.

## 2. Predikat GT instrumen VERIF harus domain-lokal
Preseden C2-R2 (CAPPED): predikat konsekuensi q1 diwarisi dari leksikon domain sipil ("larang klaim lulus", "non-selamat") yang terukur 0 kemunculan di teks rantai domain target (grep vs 4 hit di sipil) — jawaban paling setia-rak pun tak bisa memenuhi. Ini cacat pasangan GT/instrumen/domain, BUKAN produk.
Resep: sebelum vonis per-butir, verifier/controller meng-grep SETIAP token predikat GT ke sumber yang akan dibaca akun (folder domain + baris rute); token 0-hit = predikat tak teruji -> selaraskan GT ke teks domain (fixture hijau dirakit dari teks itu; fixture merah wajib bertahan: angka telanjang, atribusi fabrikasi, klaim 'utuh' tanpa negasi) ATAU terbitkan teksnya di rak dulu (putusan controller, tercatat di Decision Log). Dilarang melonggarkan gerbang tanpa bukti per-kalimat.

## 3. Pool undian RBAC = kueri sensus WebUiUser hidup, bukan daftar statis
Dua insiden satu batch: label `gsp-budi` (C1) dan `novriandy` (C3) adalah profil pensiun tanpa home + tanpa baris WebUiUser. C1 butuh rekonsiliasi deterministik verifier (MAP); C3 draw-1 di-VOID sebelum probe mana pun + re-draw beku kedua di berkas yang sama dengan alasan void.
Aturan: pool undian dibangun dari hasil query tabel WebUiUser pada giliran itu (bukan daftar nama dari memori/skill lama), lalu setiap label dicek `ls $LOCALAPPDATA/hermes/profiles | grep -x <nama>`. Rekon DB (gsp-datacenter, Prisma): kolom profil adalah `hermesProfile` (BUKAN `profile`):
`node -e "...webUiUser.findMany({select:{username:true,role:true,hermesProfile:true}})..."`
Bekukan seed + draw + (bila ada) void-reason dalam SATU berkas JSON sebelum dispatch; tidak pernah mengundi ulang tanpa mencatat draw lama.

## 4. Drift baris rute memori pasca-probe + jalur koreksi terdokumentasi
Preseden: sesi profil agentriset mengonsolidasi memorinya sendiri setelah probe dispatch — baris `INDEX #construction-korpus` jadi 417 char (konten benar, bentuk beku cap-150 kontrak K-2 hilang). Konsolidasi sesi aktif tidak bisa dicegah; D-18 (sapuan fleet ulang setelah semua gerbang) tetap wajib, TAMBAHAN: ukur distribusi panjang baris rute per token SETELAH tiap gelombang VERIF (glob profiles/*/memories/MEMORY.md + root, regex baris token, hitung >cap).
Jalur koreksi yang sah (D-20): kartu revisi konstanta ke skrip rollout memakai HAK KOREKSI TERBUKA yang diberikan blueprint (rujukan eksplisit seksi K-2 "dokumen ini dikoreksi TERBUKA"), plus moda `--replace-existing` (hanya mengganti baris ber-token domain itu, backup manifest), dan sunting blueprint K-2 terbuka dengan teks final baru. Pekerja dilarang menyunting konstanta diam-diam; akun/penyebab drift tidak ditambal manual per-profil.

## 5. Indeks hulu ikut dirilis: sinkronkan inventaris AGENTS.md
Preseden: `workspace/gsp-hermes/workspace/AGENTS.md` inventaris domain ("12 sudah punya rantai") terbaca akun dan BASI setelah rantai baru terbit (nyata 14) -> akun menjawab status salah dari indeks. Setiap penerbitan rantai/domain baru: kartu FIX sinkron inventaris (ukur `ls ekas/05_DOMAIN-KNOWLEDGE/*/RANTAI-JAMINAN.md | wc -l` dulu; sunting hanya wilayah inventaris; diff + sha dilaporkan).

## 6. Pemulihan per-butir (ronde-R pola VS-R4)
Bila setelah remediasi hulu hanya SATU sel (akun x pertanyaan) yang tersisa gagal: jangan ulangi 9 probe. Dispatch ulang hanya sel itu (pertanyaan verbatim sama, undian beku sama, sesi baru), instrumen beku tanpa sunting (sha pra==sesudah dicatat), vonis gabungan = carry-over sel PASS lama + sel pulih, tabel gabungan per akun diterbitkan. Preseden: C2 FAIL 8/9 -> R4 PASS 9/9 satu probe.

## 7. CAPPED-with-evidence = kelas vonis sah, putusan milik controller
Verifier yang menemukan cacat instrumen/domain-pairing TIDAK memvonis FAIL produk diam-diam dan tidak menambal sendiri: ia mengirim CAPPED dengan bukti reproduksi + opsi. Controller menyahkan lewat ruling di komentar kartu + Decision Log kontrak (pola D-15/D-20), dan ruling menyebut mana yang produk vs instrumen vs cacat akun (T1) — ketiganya punya jalur perbaikan berbeda (GT fix / shelf fix / memori-akun FIXB).

## 8. Pecul alat yang terbukti giliran ini
- `lad_card.py` TIDAK mengenal `--json`; id kartu diekstrak `grep -oE 't_[0-9a-f]{8}' | head -1`.
- `hermes kanban complete` pada kartu yang sudah terminal ditolak kernel ("unknown id or terminal state") — temuan penutup ditulis sebagai KOMENTAR, bukan complete ulang.
- `hermes send -t whatsapp:<chat_id> -f <naskah>` (bukan `--channel`).
- Frontmatter kanonik objek korpus = 18 kunci (bukan 21; angka lama longgar) — validator promote uji 18/18 vs templat objek domain sebelumnya.
- Naskah home channel sering butuh 2-3 iterasi scanner naturalisasi: C-8b menuntut token leksikon literal ('batasan'/'keterbatasan', bukan parasinon), C-5 italic ≤2, C-12 dua sinyal gaya catatan cepat (panah ASCII + rantai titik-koma) = FAIL; ganti panah dengan kata, gabung klausa dengan 'dan'.
