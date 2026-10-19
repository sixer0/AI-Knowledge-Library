---
id: wlp-angka-outline-window
type: fakta
title: Angka terverifikasi biaya outline window WebUI (misi WLP F17-F23)
status: active
sumber: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F23-rewalk.md
halaman: §4,§6; CP-F17 §1; CP-F19 §3,§5
tanggal_akses: 2026-09-07
kelas_bukti: primer
sensitif: tidak
perkara: wlp
tags: [webui, performa, angka, encodedbodysize, wlp, brahma]
links: [wlp-resep-ukur-performa, wlp-pelajaran-objek-vs-content]
penulis: gsp-librarian
diajukan: 2026-09-07
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-07
catatan_verifikasi: "Verdict: terverifikasi. Alasan spesifik: seluruh angka tabel biaya dicocokkan independen ke berkas RAW oleh parser kurasi (bukan kutip indeks): f23_agg.txt mencetak enc_sum 378806/330321, komponen 356679+22127 dan 317792+12529, DELTA vs OFF -82.1/-75.5, rasio F23/F19cacat 15.1/19.7; f19_walk_samples.jsonl memuat enc_sum 2512442/1676060 dengan komposisi reqs tertutup (IDX 22127 + WALK 356679 + BARE 2111509 + IDX 22127; WALK 317792 + BARE 1345739 + IDX 12529); CP-F17 par.1 memuat 2.111.509/1.345.739 dan 41.345/12.529. Aritmetika dihitung ulang: delta -82,1%/-75,5%, keadaan cacat +19,0%/+24,5%, rasio 15,1%/19,7%, buka panel -98,0%/-99,1% semuanya cocok. Timestamp jendela ukur (F17 08:16-08:52, F19 09:13-09:35, F23 10:31-10:35), proyeksi mc 2701/1694, preseden 2672->2701, sertifikat V1-V17 SALAH-TARGET=0 dan VERDICT PASS terverifikasi di CP-F23 par.1/par.6/par.7. Determinisme byte-identik antar attempt terkonfirmasi di f23_agg.txt (4 record, dua eksekusi 10:31-10:32 dan 10:34). Rekomendasi konkret: tidak ada perubahan isi; saat promosi pertahankan batas-waktu butir 4.1 (angka terikat build fe71a74, sesi beku, tanggal ukur 2026-09-07) agar nilai absolut tidak dipakai pada sesi yang tumbuh."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-07
dipromosikan-ke: faktas/wlp-angka-outline-window.md
---

# Angka terverifikasi biaya outline window WebUI (misi WLP F17-F23)

1. Tabel biaya (encodedBodySize, urutan buka-panel + klik target-dalam-pita)

| Keadaan | LONGP | MEDIUM | Acuan |
|---|---|---|---|
| Baseline OFF (F17, 2026-09-07 08:16-08:52) | 2.111.509 B | 1.345.739 B | [R-1] |
| ON keadaan CACAT pra-tambalan (F19, 09:13-09:35) | 2.512.442 B (+19,0% vs OFF) | 1.676.060 B (+24,5% vs OFF) | [R-2] |
| ON pasca-tambalan (F23, 10:31-10:35) | 378.806 B (-82,1% vs OFF) | 330.321 B (-75,5% vs OFF) | [R-3] |
| Rasio F23 terhadap keadaan cacat F19 | 15,1% | 19,7% | [R-3] |

Komponen F23: LONGP = 356.679 B halaman walk + 22.127 B refresh indeks; MEDIUM = 317.792 B + 12.529 B. Sanity penjumlahan tertutup dan delta persen dihitung ulang alat pada giliran kurasi ini (09-09) dari angka mentah [R-3][R-4]; cocok dengan cetakan sumber.

2. Konteks angka

2.1 Keadaan cacat F19 adalah kasus "optimasi yang malah memperburuk": klik dalam-pita mengunduh halaman walk (356.679/317.792 B) yang lalu dibuang karena fail-closed ke bare, sehingga total = bare + halaman walk terbuang. Baseline OFF LONGP 2.111.509 B identik persis dengan angka F7 (determinisme respons bare) [R-1][R-2].

2.2 Penghematan buka panel arm ON (jalur indeks, bukan walk): 41.345 B vs 2.111.509 B (LONGP) dan 12.529 B vs 1.345.739 B (MEDIUM) = -98,0%/-99,1% [R-1].

2.3 Sertifikat F23: VERDICT PASS, tabel VERIFIKASI-AKURASI V1-V17 populasi penuh, SALAH-TARGET = 0; sampling 2 attempt per sesi pada dua eksekusi terpisah, hasil byte-identik antar attempt [R-3].

2.4 Putusan enablement flag `wlp_outline_window` adalah wewenang user; default flag tetap False [R-3][R-5].

3. Register rujukan

- R-1: docs/2026-09-05-webui-long-transcript-perf/checkpoints/CP-F17-smokebench.md §1 (tabel smoke 4/4 sampel; enc buka panel per arm).
- R-2: checkpoints/CP-F19-walk.md §3 (tabel sampel mentah; bentuk permintaan) dan §5 (dampak biaya +19,0%/+24,5%).
- R-3: checkpoints/CP-F23-rewalk.md §4 (tabel biaya final + sanity aritmetika), §6 (V1-V17), §7 (VERDICT PASS).
- R-4: research/raw/wlp-f23/f23_agg.txt (cetakan alat: enc_sum, komponen, DELTA vs OFF) dan research/raw/wlp-f19/f19_walk_samples.jsonl (enc_sum 2512442/1676060).
- R-5: CONTRACT.md Decision Log D-14/D-15 (putusan enablement tetap milik user).

4. Batas berlaku

4.1 Angka terikat build serve fe71a74 (md5 statik 4d396b43...), sesi beku LONGP (mc 2701) / MEDIUM (mc 1694), dan tanggal ukur 2026-09-07; sesi yang tumbuh mengubah nilai absolut (preseden LONGP 2672 -> 2701 antara F13A dan F17). Delta persen terhadap baseline OFF tetap sah hanya selama metode ukur [R-4] tidak berubah. XL tidak termasuk tabel ini (jalur walk-nya tidak terprovisi pada giliran ini).
