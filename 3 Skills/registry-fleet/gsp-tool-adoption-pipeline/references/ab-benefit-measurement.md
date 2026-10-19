# Mengukur MANFAAT alat MCP baru: gerbang validitas ekologis (preseden GRAFT-0909/C, FAIL 11-09)

Berkas ini memperluas langkah 9 SKILL.md. Preseden: Graft (npm @nanonets/graft) lulus
Tahap A (build, ketepatan 4/6, isolasi, telemetri mati) dan Tahap B (P6 pemakaian nyata,
biaya schema +3,1%), lalu vonis Tahap C = **FAIL terukur**. Bukan alatnya gagal — desain
ukurnya yang pertama kali mengungkap kebenaran penting ini.

## Temuan inti: akses tersedia != dipakai

Lengan "with" pada A/B punya 6 tool graft terdaftar dan TERBUKKA terlihat di probe sesi,
tetapi memanggilnya **NOL kali** pada ketiga tugas. Semua kerja diselesaikan dengan
terminal/search_files/read_file. Akibatnya rasio tool-call antar-lengan (0,815 / 1,000 /
1,077) hanyalah derau, dan CHECK1 (median <=0,8 pada >=2/3) gagal 0/3.

Cara audit (jangan percaya narasi laporan): query `state.db` profil lengan, parse kolom
`tool_calls` (JSON) di tabel `messages`, hitung panggilan yang nama function-nya memuat
nama alat. Controller mengulang audit ini independen atas laporan verifier — angka harus
cocok sebelum vonis diterima.

```python
# pola audit invokasi alat per sesi (state.db profil)
import sqlite3, json
db = sqlite3.connect(r"C:/Users/TRIAL/AppData/Local/hermes/profiles/<profil>/state.db")
for sid in session_ids:
    g = 0
    for (tc,) in db.execute("SELECT tool_calls FROM messages WHERE session_id=?", (sid,)):
        if tc:
            for call in json.loads(tc):
                fn = (call.get("function") or {}).get("name") or call.get("name", "")
                if "graft" in str(fn).lower():
                    g += 1
    print(sid, "graft_calls=", g)
```

## Kenapa worker mengabaikan alat baru

1. Baseline sudah optimal untuk kelas tugasnya: repo 108 berkas, pertanyaan lokasi/trace —
   grep + read mencapai 6/6 tepat sasaran di KEDUA lengan. Ruang manfaat struktural nol.
2. Model worker-fast tidak punya pendorong sistemik (skill/instruksi wajib-tool) untuk
   memilih MCP baru dibanding alat bawaan. Preseden P6 membuktikan pemakaian NYATA terjadi
   begitu prompt MENYURUH memakai tool graft.

Implikasi adopsi: nilai alat semacam ini kemungkinan besar baru terealisasi bila pemakaian
dipaksa lewat skill pendorong di profil (yang justru produk Tahap D). Ukur dulu di Tahap C
dengan pendorong eksplisit, jangan simpulkan "alat tidak berguna" dari lengan pasif.

## Desain ulangan sah (C2) — empat tambalan, ambang TETAP

Dilarang moving goalpost: ambang lulus tidak boleh digeser pasca-hasil (standar anti-blind
user). Yang boleh diganti adalah DESAIN EKSPERIMEN:
1. Prompt graft-first wajib di lengan-with; gerbang ekologis `tool_calls(alat) > 0` di
   SEMUA sesi with — kalau 0 lagi = FAIL desain, laporkan, jangan rekayasa.
2. Tugas dinaikkan: repo PENUH termasuk tests/ (~1.500 berkas), pertanyaan lintas modul.
3. Simetri pohon: dua klon commit identik; klon lengan-without TANPA artefak indeks alat
   (folder `graft/` di working tree terlihat sebagai berkas biasa oleh kedua lengan =
   kebocoran keberadaan alat; cacat desain minor preseden C).
4. Kunci protokol (tugas + ground truth + predikat + seed) dengan SHA-256 yang ditempel di
   komentar kartu SEBELUM eksekusi sah pertama.

Maksimal SATU ulangan dengan vonis jujur; ulangan ketiga hanya atas perintah user
(preseden putusan D-09 di contract.md misi).

## Isolasi sesi anak dari konteks kanban

Spawn `hermes -p <profil>` dari sesi yang berjalan di bawah kernel kanban MEWARISI env
sehingga sesi anak mengira dirinya pekerja kartu: pada preseden C, sesi lengan
percobaan-1 menulis 3 komentar + 1 event block ke kartu misi atas nama run verifier
(kartu jadi `blocked` oleh anak, penutupan verifier ditolak kernel). Tambalan: buang var
env kanban/HERMES sebelum spawn, larang tool kanban secara eksplisit di prompt lengan,
guard pasca-run: nol baris `kanban` di tabel sesi lengan.

## Kejadian lain yang layak diingat

- `hermes mcp add` di shell non-TTY bisa berhenti pada prompt "Enable all 6 tools?" lalu
  "Cancelled" dengan rc=0 (GAGAL SENYAP). Fallback sah: backup config profil, pulihkan
  blok `mcp_servers:` langsung, verifikasi sha byte-identik saat restore. Selalu cek
  `mcp list` + probe tool terlihat sebelum menyatakan lengan "with" valid.
- Prompt "repo di cwd" tidak menahan agen dari mengembara ke direktori lain; pakai path
  korpus ABSOLUT dalam prompt lengan dan verifikasi jejak direktori di jawaban akhir.
- Kartu yang diblokir sesi anak cacat: tutup via komentar controller + `complete --force`
  dengan bukti, jangan biarkan menggantung (task-monitor escalate gerbang needs_input
  lewat 2 jam).
