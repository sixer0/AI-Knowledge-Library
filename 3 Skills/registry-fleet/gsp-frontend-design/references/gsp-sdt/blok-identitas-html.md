# GSP-SDT di Kanal HTML - Carrier gsp-frontend-design

> Bagian SDT (blueprint langkah 21, SM-2 t_4cc4e6b9). Sumber: SPEC-DOC-SYSTEM.md §3.3 + paket
> `gsp-document-quality-standards/references/gsp-sdt/`. Hierarki D-TA-4.3: blok identitas +
> klasifikasi header/footer WAJIB dulu, baru palet/tipografi DS. Nilai warna/font TETAP dari
> paket token DS - berkas ini hanya mendefinisikan STRUKTUR kepatuhan dokumen.

## 1. Urutan wajib isi `<body>` (blok identitas = elemen pertama)

```html
<!-- 1. BLOK IDENTITAS (C-25) - elemen pertama body, sebelum <header> visual -->
<section class="sdt-identity" data-rezim="BIZ" data-kelas="K2" data-bobot="9">
  <!-- bentuk strip (profesional) -->
  <p class="sdt-strip">DOKUMEN GSP-SDT-BIZ-002 | REGISTER 033/GSP/STD/VIII/2026
     | REVISI A · 01 SEP 2026 | STATUS Berlaku · Direktur &amp; Tim GSP</p>
  <!-- varian CY: slot keempat = INTEGRITAS: SHA-256 · diisi saat terbit -->
  <!-- bentuk kisi 6×4 (pertahanan): pakai .sdt-grid dengan 12 field per blok-identitas.md -->
</section>

<!-- 2. HEADER sticky berisi klasifikasi (C-08/C-22) - screen + print -->
<header class="sdt-head" data-klasifikasi="TERBATAS">
  <span>GSP-SDT-BIZ-002 · PROPOSAL TEKNIS …</span><span class="sdt-pill">TERBATAS</span>
</header>

<main>…anatomi per kelas (anatomi-per-kelas.md), blok ● tidak boleh kosong…</main>

<!-- 3. FOOTER sticky: perusahaan | klasifikasi · Terkendali | nomor lembar pola rezim -->
<footer class="sdt-foot"><span>PT GEMILANG SATRIA PERKASA</span>
  <span>TERBATAS · Terkendali</span><span class="sdt-pageno"></span></footer>
```

## 2. Kelas CSS struktural (nama peran DS, bukan hex lepas)

```css
.sdt-head, .sdt-foot { position: sticky; z-index: 10; background: var(--paper);
  border-block-color: var(--rule); }            /* pil klasifikasi = komponen DS yang sudah ada */
.sdt-pill { border-radius: 999px; padding: .1em .6em; font: 600 var(--fs-label)/1 var(--font-data); }
.sdt-strip { font: 400 var(--fs-small)/1.4 var(--font-data); letter-spacing: .02em; }
.sdt-grid  { display: grid; grid-template-columns: auto 1fr auto 1fr; gap: .25rem 1rem; }
[data-provenance]::after { content: attr(data-provenance-icon); margin-inline-start: .3em; }
```

Palet/peran tipografi diambil dari `gsp-ds-sets.json` lewat pointer DS yang sudah ada di
SKILL.md skill ini (section MASTER_DESIGN) - JANGAN hardcode hex di kelas SDT.

## 3. Ketertelusuran mesin (C-02 "dapat diperiksa mesin")

- Setiap kebutuhan: anchor `id="REQ-K1-014"` (atau `LI-nnn`/`BB-nnn`/`FND-Kx-nnn`) - dipakai
  juga sebagai target tautan silang antar bagian.
- Setiap angka teknis: `data-provenance="terukur|diturunkan|pemasok|asumsi"` + ikon terlihat
  ■◈◇△ (`provenans.md` §5). Atribut ini yang dipindai verifier Part B.
- Gambar/tabel: `<figure>`/`<table>` bernomor per klausul + `<figcaption>SUMBER: …</figcaption>`
  wajib (C-14).

## 4. Pagination print (C-16/C-17/C-21 di medium HTML)

```css
@page { size: A4 portrait; margin: 24mm 22mm;   /* minimum rezim target - lihat penomoran-footer.md §4 */
        @bottom-center { content: "PT GEMILANG SATRIA PERKASA | TERBATAS · Terkendali | " counter(page) " / " counter(pages); } }
@media print {
  .sdt-head, .sdt-foot { position: static; }
  figure, table { break-inside: avoid; }        /* C-17: tidak dipenggal tanpa penanda */
  h1 { break-before: page; }
}
```

Pola nomor lembar layar mengikuti rezim via teks `.sdt-pageno` (JS total halaman statis boleh;
pola per rezim: `n - mm`, `SHEET nn OF mm`, `LEMBAR n DARI m`, `HAL nn / mm`, `HLM n / mm`, `n / mm`).

## 5. Gerbang sebelum serah

Jalankan `checklist-pra-terbit.md` butir 1–17 + varian rezim, lalu gerbang render-lokal skill
ini (section DS §gerbang): render lokal, cek klasifikasi tampil di screen DAN print, blok
identitas elemen pertama, nol hex lepas di luar blok token. Konflik dua standar: bentuk &
klasifikasi → SDT menang; warna & rasa → DS menang selama tidak melanggar klausul (C-21).

> Penanda D16: middle dot (U+00B7) yang tersisa di berkas ini adalah kutipan verbatim master design (string blok terkendali atau teks halaman terkutip ber-rujukan halaman), bukan prosa; jangan dianggap pelanggaran aturan teks keluaran.
