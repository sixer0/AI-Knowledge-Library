# Registrasi knowledge multi-domain berantai (preseden misi terkait, 24-09-2026)

Lapisan tambahan di atas resep misi terkait (lihat [`knowledge-activation-rbac-verification.md`](knowledge-activation-rbac-verification.md))
untuk misi "daftarkan N domain korpus secara berantai dengan prosedur yang sama".

## Urutan & paralelisme

- "Sequential" dari user = urutan RILIS (VERIF + laporan home channel per domain),
  BUKAN urutan preparasi. STU/LIB/MEM-prep domain n+1 boleh paralel dengan LIB/VERIF
  domain n (pekerja dan artefak berbeda, wave aktif <=5). Gerbang: D(n+1) tidak masuk
  VERIF/LAPOR sebelum D(n) VERIF PASS.
- Laporan home channel PER DOMAIN yang selesai bila user meminta begitu; gerbang kirim
  yang sudah terbukti hidup di misi sebelumnya tidak dites ulang tiap domain -
  kegagalan nyata pertama = stop + eskalasi, bukan vonis.

## Bekukan keputusan silang-domain SEKALI

- Kartu G-1 (librarian): skema objek vault + anatomi 8 bagian + daftar tag beku per
  domain + penamaan `<slug>-korpus-ekas-<mmdd>` - satu keputusan untuk N domain,
  bukan N keputusan di N kartu domain. Keyword lengkap hidup di TAG objek IL karena
  baris rute L0 dipangkas cap.
- Kartu G-2 (system-manager): SATU skrip rollout parametrik `--domain <slug>`
  (dry-run/apply/selftest) dibangun dari preseden skrip domain pertama - bukan N
  varian skrip. Idempoten per domain karena kunci token per domain berbeda.
- Undian RBAC: mekanisme beku, hasil ditarik controller per domain di langkah V0;
  seed+ts+3 akun dicatat di kartu + Decision Log SEBELUM dispatch; pekerja/verifier
  dilarang mengarang akun terpilih.
- Pekerja studi per domain = spesialis terdekat yang ADA di disk
  (networking->gsp-infra-specialist, fiber->gsp-fiber-specialist, dst.); jangan bikin
  profil baru hanya karena nama domain.

## Kapasitas baris rute L0 (kehadiran token != keterlihatan agen)

- Injeksi memori ke konteks terpotong pada jendela +-2.200 char segmen indeks (angka
  terukur pada giliran desain; ukur ulang sebelum dipakai). Baris rute yang ditempel
  di EKOR berkas bisa tercut dari injeksi meski grep menemukannya - rollout
  grep-only = cacat laten.
- Aturan turun-temurun: cap hard 150 char/baris; SISIP tepat sesudah baris jangkar
  yang terbukti terlihat (mis. `INDEX #vss-korpus`), bukan ekor berkas; skrip WAJIB
  mengukur posisi karakter baris per profil dan melapor NEEDS_REVIEW bila lewat
  jendela; fallback sah = konsolidasi lintas-misi dengan arsip verbatim + persetujuan
  controller.
- Aritmetika plafon pra-rollout: PINNED + baris rute kumulatif vs jendela; N baris
  rute sekaligus bisa menjebol profil yang indeksnya sudah penuh - dry-run wajib
  melapor sisa char per profil.
- Bentuk hemat terbukti: `INDEX #<slug>-korpus: <token> -> muat pustaka-teknis;
  baca ekas/05_DOMAIN-KNOWLEDGE/<DIR>/; cari IL` (~126-140 char). Nama objek IL
  deterministik dari slug, jadi "cari IL" tidak kehilangan sasaran.
- Jalur folder di baris rute dan objek IL WAJIB nama nyata di disk (probe ls
  langsung); label folder dari KATALOG-RUMUS sering bukan nama disk.

## Register kontradiksi & adjudikasi halaman sebelum vonis rilis

- Kartu studi WAJIB berisi register kontradiksi dengan predikat eksplisit
  ("kontradiksi terukur" vs "calon - perlu pembacaan PDF primer oleh manusia") +
  jalur baris; nol butir didiamkan (pelajaran Tabel 7 BS EN 62676).
- Butir uji spesifik ditanam di kartu studi dari register pra-uji blueprint TA
  (varian halaman buku bersama antar-domain, ambang delta-T lintas lapis, batas
  jarak MM ~550 m, offset halaman per buku).
- Register kontradiksi antar-domain dibaca silang SEBELUM LIB: buku yang sama
  dikutip di dua domain (Fall & Stevens di NETWORKING dan STORAGE); varian salah
  di satu domain = defect di domain lawan. Vonis rilis kedua domain ditahan
  sampai semua lapis bertanda (pola FIXx hanya-tambah).
- Adjudikasi selisih sitasi halaman pakai aturan offset cetak-vs-PDF yang tercetak
  di rak sendiri (mis. cetak+39=PDF untuk TCP/IP Illustrated; validasi terhadap
  peta bab, 0 pelanggaran = offset sah). Mayoritas lapis + offset konsisten = vonis
  sementara lapis teks; status akhir BELUM TERKONFIRMASI sampai manusia membuka PDF.
- Pola identik searah di baris bertetangga (dua salah kutip dalam paragraf sama) =
  petunjuk satu suntingan hulu keliru, bukan dua kekeliruan bebas - catat sebagai
  bukti.
- Cek atribusi silang-buku: rentang halaman yang cocok persis dengan peta bab buku
  LAIN = kandidat nomor halaman orang lain dilaporkan atas nama penulis A (kasus
  Odom vs Donahue di RANTAI-JAMINAN NETWORKING); tandai walau angkanya benar.
- Angka contoh yang dipakai lapis pakai tapi tidak terdaftar di ASUMSI-BAKU
  (mis. faktor puncak 1,5 pada contoh 240 Mb/s) = lubang tata kelola; masuk bagian
  BATAS objek IL, jangan dipromosikan diam-diam sebagai asumsi sah.
- Lapis yang MEMUAT bentuk benar bukan target tambalan; CHANGELOG historis jangan
  dianotasi (preseden VSSKB).

## Mekanika papan saat gelombang cepat

- `lad_card.py` menerbitkan `ready` dan dispatcher mengklaim dalam hitungan menit;
  `reclaim` pada kartu yang masih antre gagal (`not running or unknown id`) - itu
  normal, biarkan dispatcher, jangan dipaksa.
- Watchdog latar: loop `show --json` parse lewat python (bukan grep/awk kolom -
  pitfall parser 23-09 menangkap id alih-alih status), cek per 120 dtk, keluar saat
  semua kartu gelombang mencapai status terminal (done/blocked/needs-review).
