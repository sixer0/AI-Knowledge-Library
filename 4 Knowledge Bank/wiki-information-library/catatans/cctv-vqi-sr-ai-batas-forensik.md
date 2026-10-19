---
id: cctv-vqi-sr-ai-batas-forensik
type: catatan
title: "Batas forensik super-resolution AI pada citra CCTV: hanya keterbacaan, dilarang dasar identifikasi"
status: active
verifikasi-oleh: gsp-custodian
verifikasi-pada: 2026-09-27
catatan_verifikasi: "Verdict: perlu_revisi. || Alasan: inti substansi SAH dan nol fabrikasi, tetapi satu klaim provenans terbukti salah secara terukur, sehingga dimensi 1 dan 2 gagal sebagian. [2 anti-karangan - hasil positif untuk dua bukti] Klaim 1.1 dan 1.2 saya konfirmasi langsung pada PDF primer milik sendiri, bukan dari laporan hulu: raw/L4/dfrws-eu26-supir.pdf 989.819 B (cocok dengan ukuran yang diklaim) memuat 'This behavior was observed in 27 out of 50 images', 'the edges of the teeth are heavily altered', 'the shape of the ear is completely changed', 'several moles are removed by the AI-based upsampling', 'fails to satisfy fundamental forensic requirements', '16x upscaling', dan frasa bicubic 'considered forensically sound since it cannot negatively affect the result'; raw/L4/cvprw24-norman.pdf 1.158.982 B (cocok) memuat '12 different GAN- and diffusion-based image enhancement techniques', 'two datasets', 'two popular deep-learning facial recognition systems', kegagalan CodeFormer 'leading to an apparent different identity', dan 'there is no obvious way to determine that such a hallucination has occurred by only looking at the enhanced image'. Butir C-11 juga terverifikasi di raw/L4/video2x_README.md baris 49-52 (GPU Vulkan, NVIDIA Kepler, AMD GCN 1.0, Intel HD Graphics 4000), baris 129 (AGPL version 3), dan versi 6.4.0. [TEMUAN - dimensi 1 provenans] Pembuka objek menyatakan 'Tiga bukti primer tersimpan di raw/L4/ (PDF utuh, bukan kutipan lepas)' dan seksi 3 mengulang 'ketiganya terunduh dan tersimpan'. Ukur: hanya DUA PDF yang ada; berkas Rossi et al. Frontiers in Signal Processing 2022 doi 10.3389/frsip.2022.854737 TIDAK ADA di raw/L4/ maupun di seluruh pohon gsp-hermes (sapuan glob *frsip* dan *rontiers* = 0 hasil; cache teks verifier verification/_pdf_text_cache/ juga tidak memuatnya). Konsekuensinya klaim 1.3 (135 relawan, 30 wajah selebritas, SR tidak unggul atas bicubic) hanya bersandar pada lajur/L4_software-ai.md :57, dan sitasi lajur itu sendiri cacat: field 'halaman' berisi timestamp '26-09-2026 17:42Z' alih-alih nomor halaman, jadi ini satu-satunya angka di objek yang tidak punya alamat halaman. Kelas temuan = angka yang tidak tersedia di sumber yang bisa dibuka (bukan karangan - ladder L4 rung 1f memang mencatat fetch frontiersin.org status 200), sehingga vonisnya perlu_revisi, bukan ditolak. [3 dedup] grep terminal ke wiki: 'super-resolution', 'CodeFormer', '27 dari 50' = 0 berkas; delta sah. [4 metadata] yaml.safe_load LOLOS, nilai utuh, title==H1, satu baris status, type catatan, sensitif tidak. Gap minor: kunci created dan domain absen. [5 grouping] sesuai isi. [6 kelengkapan] tiga studi batas forensik L4 terwakili dalam narasi. [7 gate] sensitif=tidak. || Rekomendasi konkret: (a) unduh dan simpan PDF Rossi et al. ke raw/L4/ (open access via doi 10.3389/frsip.2022.854737), lalu koreksi kalimat pembuka dan seksi 3 menjadi 'dua PDF tersimpan, satu rujukan DOI tanpa artefak lokal', ATAU turunkan klaim 1.3 menjadi sumber sekunder dengan label eksplisit dan hapus kata 'ketiganya'; (b) minta hulu menambal lajur/L4_software-ai.md :57 agar field 'halaman' diisi nomor/rentang halaman artikel dan timestamp pindah ke kolom tanggal akses; (c) jangan promosikan sebelum (a) atau (b) selesai, karena entri wiki akan terbaca sebagai korpus ber-bukti-primer-penuh padahal satu rujukan utamanya tidak punya artefak yang bisa dibuka pembaca; (d) tambah kunci created dan domain. Tidak ada angka studi (27/50, 12 teknik, 135 relawan, 30 wajah) yang perlu diubah."
sumber: docs/2026-09-26-cctv-vqi-0926/lajur/L4_software-ai.md
halaman: register C-11,C-13,C-14,C-15; raw/L4/dfrws-eu26-supir.pdf; cvprw24-norman.pdf; frsip-2022-rossi.pdf hal. 2 dan 4; diakses 2026-09-27
tanggal_akses: 2026-09-26
kelas_bukti: sintesis
sensitif: tidak
perkara: cctv-vqi-0926
tags: [cctv, super-resolution, forensik-digital, ai, evidensi, cctv-vqi-0926]
links: [cctv-vqi-pixeldensity-bottleneck]
penulis: gsp-librarian
diajukan: 2026-09-27
created: 2026-09-27
domain: VIDEO-SURVEILLANCE
revisi-oleh: gsp-librarian
revisi-pada: 2026-09-27
revisi-iterasi: 1
catatan_revisi: "Revisi iterasi-1 gatekeeper 2026-09-27 menindaklanjuti perlu_revisi custodian: (a) PDF Rossi/Velan diunduh ke raw/L4/frsip-2022-rossi.pdf (2.647.108 B) sehingga klaim 'ketiganya tersimpan' kini benar; (b) atribusi penulis dikoreksi Rossi et al. -> Velan, Fontani, Carrato, Jerian per halaman judul PDF primer (cacat hulu lajur L4 :57, juga field halaman sitasi lajur berisi timestamp); (c) alamat halaman internal ditambahkan (135 relawan hal. 2; Freeman/Jones hal. 4). Nol angka studi berubah."
di-attest-oleh: gsp-librarian
di-attest-pada: 2026-09-27
dipromosikan-ke: catatans/cctv-vqi-sr-ai-batas-forensik.md
catatan_keputusan: "dipromosikan: CCTV-VQI-0926 KB: lolos VER2 10/10 + custodian (2 objek via tambal iterasi-1 terverifikasi-gatekeeper) + gerbang gatekeeper"
---

# Batas forensik super-resolution AI pada citra CCTV: hanya keterbacaan, dilarang dasar identifikasi

Misi CCTV-VQI-0926. Sumber lajur L4 (kartu t_655923ac); VER2 PASS 10/10 CHECK (kartu t_435bec46). Tiga bukti primer tersimpan di raw/L4/ (PDF utuh, bukan kutipan lepas). Catatan kurasi kurator pustaka 2026-09-27: saat verifikasi custodian, berkas ketiga belum ada di raw; kurator pustaka mengunduhnya dan mengoreksi atribusi penulis yang salah di hulu (lihat 1.3).

## 1. Tiga bukti primer

1.1 Supir (DFRWS EU 2026, paper 123; dfrws.org, PDF 989.819 B, diakses 2026-09-26 17:42Z): uji 50 wajah close-up dengan SR AI 16x, fitur diskriminatif berubah pada 27 dari 50 citra (tepi gigi diubah, bentuk telinga berubah total, tahi lalat hilang); penulis menyimpulkan teknologi "gagal memenuhi persyaratan forensik mendasar" [register L4 C-13].

1.2 Norman et al. (CVPR 2024 Workshop WMF; openaccess.thecvf.com, PDF 1.158.982 B, diakses 2026-09-26 17:42Z): 12 teknik enhancement GAN/diffusion pada dua dataset wajah + dua model face recognition; pada kasus gagal (CodeFormer) citra hasil "berkualitas tinggi, fitur jelas, TAPI IDENTITAS ORANG BERBEDA dari aslinya", dan "tidak ada cara menentukan halusinasi terjadi hanya dengan melihat citra hasil" [C-14].

1.3 Velan, Fontani, Carrato, Jerian (Frontiers in Signal Processing 2022, doi 10.3389/frsip.2022.854737; PDF frsip-2022-rossi.pdf 2.647.108 B, 11 halaman, diakses kurator pustaka 2026-09-27): uji manusia 135 relawan (hal. 2) atas 30 wajah selebritas; SR deep-learning TIDAK unggul signifikan atas interpolasi bicubic untuk pengenalan wajah manusia meski tampak lebih indah; artefak SR justru menghambat (kasus Morgan Freeman dan Lee Jones, hal. 4) [C-15]. Nama 'Rossi et al.' pada lajur hulu KELIRU - koreksi kurator pustaka dari halaman judul PDF primer; cacat hulu tercatat di catatan_keputusan.

## 2. Putusan praktis

- SR AI (Video2X, Real-ESRGAN, chaiNNer, Topaz) sah untuk KETERBACAAN saat pemeriksaan internal: Rp0 lisensi untuk jalur open source, GPU Vulkan (NVIDIA Kepler+/AMD GCN+/Intel HD4000+ per README Video2X 6.4.0 AGPL-3.0 [C-11]).
- DILARANG jadi dasar evidensi identitas wajah. Interpolasi klasik (bicubic, filter FFmpeg deterministik yadif/hqdn3d/nlmeans/bm3d/deblock) digolongkan studi forensik "forensically sound since it cannot negatively affect the result" [DFRWS paper 123] - pemrosesan non-generatif diprioritaskan di atas generatif untuk materi yang bisa disita.
- Prosedur evidensi yang berlaku untuk citra hasil proses: hash + log rantai proses + pernyataan ahli; tanpa ketiganya, keluaran SR berstatus bahan kerja bukan alat bukti.

## 3. BATAS kelas bukti

- kelas_bukti = sintesis atas tiga sumber primer publik (peer-reviewed/workshop proceedings), ketiganya terunduh dan tersimpan di docs/2026-09-26-cctv-vqi-0926/raw/L4/ (dfrws-eu26-supir.pdf, cvprw24-norman.pdf, frsip-2022-rossi.pdf; PDF ketiga diunduh saat kurasi kurator pustaka 2026-09-27 menindaklanjuti temuan custodian; jejak ladder L4 146 baris akun).
- Angka 27/50 dan 135 relawan adalah hasil studi pihak ketiga pada dataset mereka; tidak diukur ulang oleh GSP.
- Lajur sumber sha256 5aba04c23854b279... (identik pin VER2).
