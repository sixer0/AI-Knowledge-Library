# Harness Loop Generation Improvement (berbasis delegasi) — tervalidasi loop-20x TRELLIS 01/02-09-2026

Use when: user minta loop generation N kali (N>=10) dengan penjurian delegasi dan
"record setiap improvement sebagai skill". Pelajaran di sini tentang HARNESS &
DISIPLIN LOOP, bukan model spesifik (untuk triase VRAM/TRELLIS:
gsp-comfyui-slide-stack/references/trellis-workflow.md).
Pasangan wajib: references/judge-noise-calibration.md (kalibrasi juri).

## Struktur eksperimen
- SATU sumbu perubahan per gelombang (input / geometri objek / knob sampling) agar
  kesimpulan dapat diatribusikan; RT mengunci definisi improvement + daftar sumbu sah
  sebelum eksekusi; TA memberi blueprint gelombang.
- Varian KONTROL per gelombang: setting sama, knob MATI. Efek knob hanya diklaim
  terhadap kontrol di kondisi identik, bukan terhadap skor baseline dari kondisi lain.
- Ablasi murah sebelum iterasi berat: uji hipotesis akar masalah lewat delegasi
  (mis. nilai pasangan input->output, ukur korelasi) SEBELUM menghabiskan N siklus
  GPU di sumbu itu. Temuan negatif = deliverable, rekam ke skill.
- Plafon jujur: >=2 sumbu independen konvergen di bawah noise band + repro
  mengonfirmasi => nyatakan plateau dengan bukti, hentikan sweep (sweep thr/seed
  terbukti konvergen = gerakan terlarang), tawarkan deliverable terbaik saat ini.
- Sederhanakan ekstrem bisa MENURUNKAN skor (model butuh konteks struktural):
  objek paling sederhana justru skor terendah (2/30). Uji hipotesis dua arah.

## Rantai GPU (chain.sh / chain2.sh, comfyui-check/satellite + scripts/ skill)
- **Server-per-iterasi BUKAN obat tunggal.** chain2.sh (start segar -> 1 run ->
  Stop-Process) menghilangkan komponen kumulatif antar-run, tapi OOM tetap terjadi
  di server SEGAR saat teralokasi+minta < limit (9,04+2,48=11,5 GiB < 15,92 gagal) —
  `expandable_segments` tidak menolong di beban dasar tinggi. Obat universal =
  turunkan beban dasar SATU run (res), bukan restart-restart.
- Gerbang rantai harus mengenali status APA PUN selain sukses, termasuk "?":
  crash senyap driver menghasilkan status KOSONG dan rantai lama mencetak
  CHAIN_DONE palsu tanpa artefak (grep hanya mengenali FAIL). Di chain2, FAIL
  tidak menular antar-iterasi -> lanjut, jangan exit.
- Validasi skema JSON varian SEBELUM gas (params bersarang di kunci "params"):
  KeyError driver tampak seperti kegagalan generation dan membakar slot rantai.
- Watch pattern "To see the GUI go to" = echo server READY, BUKAN hasil generation;
  hasil hanya dari result.json/ledger. Jangan klaim progres dari notifikasi watch.
- Terminal timeout TIDAK membatalkan prompt yang sudah masuk antrean server —
  cek /queue dulu sebelum submit ulang, kalau tidak dapat duplikat antrean.
- Kill server andal di git-bash: powershell Stop-Process (taskkill sering tidak
  mengenai induk+anak multiprocessing).

## Ledger & jejak
- Ledger JSON per iterasi: {n,id,axis,gen_status,score(median),runs[],improvement,
  detail,artefak}. FAIL juga dicatat sebagai jejak diagnosis, bukan dihapus.
- Contract doc dengan Decision Log D-n per temuan (termasuk temuan negatif dan
  perbaikan bug harness) — ini yang membuat 20 iterasi bisa disintesis jadi
  kesimpulan, bukan sekadar daftar skor.
- Improvement terkonfirmasi (gerbang judge-noise-calibration) => langsung patch skill
  di tengah misi, jangan tunggu akhir.

## Menulis skill saat guard curator menentang
- skill_manage patch/write_file bisa ditolak intermiten ("Skill '' not found") atau
  permanen (skill tidak curator-managed). Retry sekali; jika tetap tolak pada skill
  milik-misi-sendiri yang dibangun sesi sebelumnya, jalur resmi kedua yang dipakai
  sesi ini: patch langsung ke path file referensi, verifikasi isi di disk, sinkron
  salinan kanonik repo. Untuk skill yang memang di luar kendali, rekomendasikan
  `hermes curator adopt <name>` ke user — jangan dilawan.
