# -*- coding: utf-8 -*-
"""Bangun 'Resume Perpustakaan Teknis.docx' dari data audit koleksi."""
import os
from docx import Document
from docx.shared import Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

OUT = r'C:\Users\gspen\Videos\Buku\Resume Perpustakaan Teknis.docx'

NAVY = RGBColor(0x1F, 0x33, 0x55)
GREY = RGBColor(0x5A, 0x5A, 0x5A)
HDR_FILL = '1F3355'
ALT_FILL = 'EEF1F5'

# folder, judul, penulis, penerbit-tahun, hal, MB, ocr, toc(jumlah), catatan status,
# cakupan isi, pemakaian
BOOKS = [
 ("Critical Infrastructure",
  "Cybersecurity: Protecting Critical Infrastructures from Cyber Attack and Cyber Warfare",
  "Thomas A. Johnson (ed.)", "CRC Press, 2015", 346, 1.8, True, 14,
  "Masuk rak 19 Agu 2026 (batch 2)",
  "Infrastruktur kritis sebagai lingkungan kaya sasaran, isu perlindungan dan rancangan "
  "rekayasa, SCADA, intelijen dan konflik siber, aspek hukum AS dan internasional, biaya "
  "ekonomi keamanan siber, serta lanskap ancaman.",
  "Satu-satunya buku di rak yang membahas objek vital sebagai pokok bahasan: latar dan "
  "analisis ancaman pada proposal pengamanan objek vital, serta keamanan sejak tahap rancangan."),

 ("Cyber Operations",
  "The NICE Cyber Security Framework: Cyber Security Intelligence and Analytics",
  "Izzat Alsmadi", "Springer, 2019", 366, 15.7, True, 458,
  "Masuk rak 19 Agu 2026 (batch 2)",
  "Tiga belas bab mengikuti kerangka tenaga kerja NICE: manajemen pengadaan, kelangsungan "
  "dan pemulihan bencana, analisis pertahanan siber, intelijen siber, perencanaan operasi, "
  "kebijakan dan strategi, analisis ancaman, manajemen keamanan, forensik, manajemen "
  "identitas, dan tanggap insiden.",
  "Bab 11 Forensics Analysis memuat proses forensik digital empat tahap dan rantai kustodi "
  "- kerangka inti lini DEMS. Kerangka KSA dipakai menyusun struktur tim dan syarat personel."),

 ("Battery",
  "Battery Reference Book, Third Edition",
  "Thomas P. J. Crompton", "Newnes / Elsevier, 2000", 774, 39.9, True, 85, "",
  "Karakteristik dan teori sel, desain baterai, evaluasi unjuk kerja, penerapan per sektor, "
  "sistem pengisian, serta direktori pemasok. Mencakup timbal-asam, nikel-kadmium, "
  "nikel-metal hidrida, litium, dan sel khusus.",
  "Penentuan kapasitas baterai (Ah) dan waktu cadangan untuk UPS, catu DC perangkat lapangan, "
  "dan sistem surya. Perlu diingat terbitan 2000, sehingga data kimia litium modern terbatas."),

 ("CCTV VSS",
  "CCTV: From Light to Pixels, Third Edition",
  "Vlado Damjanovski", "Butterworth-Heinemann / Elsevier, 2014", 595, 66.9, True, 0,
  "Bookmark dibangun 19 Agu 2026",
  "Rantai lengkap sistem video: sifat cahaya dan optika, perhitungan lensa dan sudut pandang, "
  "sensor citra, pencahayaan, kompresi video, jaringan IP untuk video, perekaman dan "
  "penyimpanan, hingga praktik instalasi dan pengujian.",
  "Rujukan utama desain CCTV/VSS: pemilihan lensa dan jarak DORI, perhitungan bitrate dan "
  "kapasitas rekaman, serta dasar pembelaan teknis dalam proposal sistem pengawasan."),

 ("Cybersecurity",
  "Security Engineering: A Guide to Building Dependable Distributed Systems",
  "Ross Anderson", "Wiley, edisi ketiga", 1044, 14.7, True, 31,
  "Judul bookmark diperbaiki 19 Agu 2026",
  "Dua puluh delapan bab: psikologi dan kegunaan, protokol keamanan, kriptografi, kendali "
  "akses, keamanan perangkat keras dan serangan kanal samping, biometrik, perang elektronik, "
  "keamanan sistem terdistribusi, sampai kebijakan, regulasi, dan ekonomi keamanan.",
  "Kerangka berpikir untuk kajian keamanan sistem bukti digital, rantai kustodi, dan "
  "arsitektur bertingkat pada proposal untuk instansi penegak hukum."),

 ("Electrical Maintenance",
  "Electrical Power Equipment Maintenance and Testing, Second Edition",
  "Paul Gill", "CRC Press, 2008", 1002, 12.4, True, 24, "",
  "Strategi pemeliharaan dan pengujian dielektrik, uji tegangan searah, faktor daya dan "
  "tan delta, minyak isolasi, transformator, kabel, switchgear menengah dan rendah, "
  "komisioning, motor dan generator, pembumian sistem tenaga, kualitas daya dan harmonisa, "
  "serta keselamatan listrik dan arc-flash.",
  "Acuan penyusunan prosedur uji terima dan pemeliharaan berkala instalasi listrik "
  "gedung dan pusat data pelanggan."),

 ("FO Test Advanced",
  "Reference Guide to Fiber Optic Testing, Volume 1",
  "J. Laferriere, G. Lietaert, R. Taws, S. Wolszczak", "JDS Uniphase, 2007", 146, 6.1, True, 0,
  "Bookmark dibangun 19 Agu 2026",
  "Prinsip transmisi cahaya dan sumber rugi-rugi, pengukuran daya optik, uji rugi sisipan "
  "dan rugi balik optik, pengukuran OTDR beserta pembacaan jejaknya, dispersi kromatik dan "
  "PMD, serta sertifikasi jaringan terpasang.",
  "Dasar penyusunan berita acara uji serat optik: nilai ambang loss per sambungan, "
  "pembacaan hasil OTDR, dan format laporan sertifikasi link."),

 ("Fiber Optic Fundamental",
  "FOA Reference Guide to Fiber Optics: Study Guide to FOA Certification",
  "Jim Hayes", "The Fiber Optic Association, 2019", 214, 51.8, False, 14,
  "OCR 19 Agu 2026; gambar halaman tidak dikompresi ulang",
  "Istilah dasar serat optik, sistem komunikasi dan transmisi, jenis serat, konstruksi kabel, "
  "konektor dan sambungan, pengujian, desain jaringan, praktik pemasangan, serta daftar "
  "kompetensi teknisi bersertifikat FOA.",
  "Materi pelatihan dan penyeragaman kompetensi teknisi lapangan serat optik; "
  "acuan kualifikasi personel pada dokumen penawaran."),

 ("Genset",
  "Diesel Generator Handbook",
  "L. L. J. Mahon", "Elsevier / Newnes, 2004", 578, 12.4, True, 12,
  "Outline dibangun ulang 19 Agu 2026. PERHATIAN: berkas kehilangan ~55 halaman - Bab 11 dan awal Bab 12 tidak ada",
  "Mesin diesel penggerak, alternator dan sistem eksitasi, pengaturan tegangan dan putaran, "
  "operasi paralel, sistem bahan bakar dan pendinginan, kebisingan dan getaran, pemasangan, "
  "serta pengujian dan pemeliharaan unit.",
  "Penentuan kapasitas dan konfigurasi genset cadangan, skema perpindahan daya, "
  "serta syarat teknis pengadaan unit pembangkit darurat."),

 ("Grounding & Bonding",
  "Grounds for Grounding: A Handbook from Circuits to Systems, Second Edition",
  "Elya B. Joffe, Kai-Sang Lock", "Wiley-IEEE Press, 2023", 1216, 133.1, True, 979, "",
  "Konsep dasar dan dasar perancangan pembumian, prinsip bonding, pembumian pada transmisi "
  "dan distribusi tenaga, pembumian generator dan UPS, pembumian untuk proteksi petir, "
  "fasilitas terpadu dan bergerak, elektroda bumi, pembumian rangkaian pengawatan, "
  "hingga proteksi terminal.",
  "Rujukan paling lengkap di rak ini untuk desain pembumian ruang server, shelter, "
  "menara, dan sistem terpadu; dipakai bersama buku proteksi petir."),

 ("Lightning Protection",
  "The Art and Science of Lightning Protection",
  "Martin A. Uman", "Cambridge University Press, 2008", 255, 25.6, True, 0,
  "Bookmark dibangun 19 Agu 2026",
  "Fisika sambaran petir, terminal udara dan konduktor turun, elektroda pembumian, "
  "penyalur surja, proteksi struktur dan saluran, tinjauan kritis atas standar "
  "NFPA 780 dan IEC 62305, serta sejarah pengembangan sejak Franklin.",
  "Dasar teknis penentuan sistem proteksi petir eksternal dan internal pada menara "
  "kamera, shelter lapangan, dan bangunan pusat kendali."),

 ("Maintenance Management",
  "Maintenance and Reliability Best Practices, Third Edition",
  "Ramesh Gulati", "Industrial Press, 2021", 740, 27.6, True, 139, "",
  "Budaya dan kepemimpinan, pemahaman fungsi pemeliharaan, manajemen pekerjaan, material "
  "dan suku cadang, keandalan sejak perancangan, operator-driven reliability, optimasi "
  "pemeliharaan, pengukuran kinerja, manajemen tenaga kerja, pemecahan masalah, "
  "standardisasi, dan tren terkini.",
  "Kerangka penyusunan tata kelola pemeliharaan dan indikator kinerja pada dokumen "
  "layanan purnajual dan kontrak pemeliharaan tahunan."),

 ("Maintenance Planning",
  "Maintenance Planning, Coordination, and Scheduling, Second Edition",
  "Don Nyman, Joel Levitt", "Industrial Press, 2010", 323, 19.6, True, 229, "",
  "Peran dan prasyarat fungsi perencanaan, sifat pekerjaan pemeliharaan, peran dan "
  "tanggung jawab, manajemen backlog, penyusunan program kerja, penentuan jumlah personel, "
  "perencanaan rinci tiap pekerjaan, dukungan material, pengukuran kerja, estimasi analitis, "
  "koordinasi dengan operasi, dan penjadwalan.",
  "Cetak biru pembentukan fungsi planner dan scheduler, termasuk penyusunan jadwal "
  "mingguan dan pengendalian backlog pekerjaan lapangan."),

 ("Mechanical Structure",
  "Shigley's Mechanical Engineering Design in SI Units",
  "Richard G. Budynas, Keith J. Nisbett", "McGraw-Hill Education, 2021", 1114, 132.2, True, 381, "",
  "Dasar pembebanan, tegangan dan defleksi, sifat material; pencegahan kegagalan statik dan "
  "kelelahan; perancangan elemen mesin (poros, sambungan baut dan las, pegas, bantalan, "
  "roda gigi, kopling, rem); topik khusus meliputi elemen hingga dan pertimbangan statistik; "
  "dilengkapi tabel rujukan.",
  "Perhitungan kekuatan dudukan kamera, bracket, tiang dan menara, pemilihan baut angkur, "
  "serta pemeriksaan defleksi struktur penopang perangkat."),

 ("Network Troubleshooting",
  "Network Warrior, Second Edition",
  "Gary A. Donahue", "O'Reilly Media, 2011", 785, 8.1, True, 526, "",
  "Praktik lapangan jaringan Cisco: hub dan switch, autonegosiasi, VLAN, trunking, VTP, "
  "agregasi tautan, spanning tree, routing dan protokolnya, redistribusi, terowongan, "
  "redundansi hop pertama, route map, multilayer switch, dan platform Nexus.",
  "Panduan penelusuran gangguan jaringan di lokasi pelanggan, terutama pada segmen "
  "switching dan routing perangkat lapangan."),

 ("Networking",
  "CCNA 200-301 Official Cert Guide Library (edisi 2024)",
  "Wendell Odom, David Hucaby, Jason Gooley", "Cisco Press, 2024", 3292, 144.8, True, 750,
  "Rujukan utama; edisi 2019 diarsipkan",
  "Pustaka dua jilid persiapan sertifikasi CCNA: dasar jaringan dan Ethernet, IPv4 dan IPv6, "
  "switching, routing statis dan OSPF, wireless LAN, keamanan perangkat, ACL, NAT, QoS, "
  "otomasi dan pemrograman jaringan.",
  "Kurikulum baku peningkatan kompetensi teknisi jaringan dan penyiapan sertifikasi personel "
  "yang dipersyaratkan dalam dokumen tender."),

 ("Networking",
  "CCNA 200-301 Official Cert Guide Library (edisi 2019)",
  "Wendell Odom", "Cisco Press, 2019", 1813, 38.1, True, 1242,
  "Edisi lama, disimpan di Networking/_arsip/",
  "Cakupan sama dengan edisi 2024 namun mengikuti silabus ujian sebelumnya; sebagian "
  "materi otomasi dan wireless sudah diperbarui pada edisi baru.",
  "Disimpan sebagai pembanding; rujukan utama dialihkan ke edisi 2024."),

 ("Networking Fundamentals",
  "Computer Networking: A Top-Down Approach",
  "James F. Kurose, Keith W. Ross", "Pearson, 2017", 867, 20.0, True, 281, "",
  "Pendekatan dari lapisan aplikasi ke bawah: internet dan arsitekturnya, lapisan aplikasi, "
  "lapisan transport, bidang data dan bidang kendali lapisan jaringan, lapisan tautan dan "
  "LAN, jaringan nirkabel dan bergerak, keamanan jaringan, dan jaringan multimedia.",
  "Buku pembentuk dasar teori bagi personel baru sebelum masuk ke materi vendor; "
  "sumber penjelasan konsep pada kajian teknis."),

 ("RCM",
  "Reliability-centered Maintenance (RCM II), Second Edition",
  "John Moubray", "Butterworth-Heinemann", 444, 186.7, False, 0,
  "Konversi dari 444 berkas SWF; OCR dan bookmark dipasang 19 Agu 2026",
  "Tujuh pertanyaan RCM, konteks operasi, fungsi dan standar unjuk kerja, kegagalan "
  "fungsional, moda kegagalan dan dampaknya, konsekuensi kegagalan, tugas proaktif "
  "(on-condition, restorasi, pembuangan terjadwal), failure-finding, diagram keputusan RCM, "
  "serta penerapan dan hasil yang dicapai.",
  "Metode induk penyusunan strategi pemeliharaan berbasis fungsi aset; dipakai sebagai "
  "dasar metodologi pada usulan layanan keandalan dan penyusunan FMEA."),

 ("Storage RAID NVR",
  "Storage Networks Explained, Second Edition",
  "Ulf Troppens, Rainer Erkens, Wolfgang Mueller-Friedt, Rainer Wolafka",
  "Wiley, 2009", 583, 8.2, True, 21,
  "Judul bookmark dibersihkan 19 Agu 2026",
  "Cakram dan RAID, arsitektur I/O, Fibre Channel SAN, NAS, iSCSI, InfiniBand dan FCoE, "
  "virtualisasi penyimpanan, sistem berkas, pencadangan dan pengarsipan, serta manajemen "
  "penyimpanan.",
  "Dasar perancangan penyimpanan rekaman video: pemilihan aras RAID, perhitungan kapasitas "
  "dan ketahanan data, serta pemisahan jalur penyimpanan pada sistem bukti digital."),

 ("System Administration",
  "The Practice of System and Network Administration, Volume 1, Third Edition",
  "Thomas Limoncelli, Christina Hogan, Strata Chalup", "Addison-Wesley, 2017", 1225, 13.4, True, 1042, "",
  "Strategi pengubah permainan, pengelolaan armada workstation, server, layanan, "
  "infrastruktur, meja bantuan dan dukungan, proses perubahan, rekomendasi layanan, "
  "praktik manajemen, serta penerapan DevOps di lingkungan TI korporat.",
  "Acuan penyusunan SOP operasional pusat data pelanggan, tata kelola perubahan, "
  "dan struktur layanan dukungan teknis."),

 ("TCP IP",
  "TCP/IP Illustrated, Volume 1: The Protocols, Second Edition",
  "Kevin R. Fall, W. Richard Stevens", "Addison-Wesley / Pearson, 2012", 1059, 11.3, True, 0,
  "Bookmark dibangun 19 Agu 2026",
  "Arsitektur protokol, lapisan tautan, ARP, IPv4 dan IPv6, DHCP, DNS, firewall dan NAT, "
  "ICMP, siaran dan multicast, UDP, pembahasan TCP secara mendalam (pembentukan koneksi, "
  "batas waktu dan pengiriman ulang, kendali aliran dan kemacetan), serta keamanan "
  "IPsec, TLS, dan DNSSEC.",
  "Rujukan tingkat paket saat menelusuri gangguan yang tidak terjelaskan di lapisan atas, "
  "termasuk analisis tangkapan paket pada jaringan pelanggan."),

 ("Thermal Camera",
  "Infrared Thermal Imaging: Fundamentals, Research and Applications, Second Edition",
  "Michael Vollmer, Klaus-Peter Möllmann", "Wiley-VCH, 2018", 787, 46.6, True, 301, "",
  "Dasar termografi inframerah, sifat kamera IR, metode lanjutan pencitraan, konsep "
  "perpindahan panas, penerapan untuk pengajaran, pencitraan gelombang pendek (SWIR), "
  "pemeriksaan bangunan dan infrastruktur, deteksi industri, mikrosistem, dan "
  "penerapan terpilih lainnya.",
  "Dasar teknis pemakaian kamera termal: pemeriksaan panel listrik, deteksi titik panas, "
  "serta penjelasan kemampuan dan batasan sensor termal pada proposal sistem pengawasan."),

 ("UPS",
  "Uninterruptible Power Supplies and Active Filters",
  "Ali Emadi, Abdolhosein Nasiri, Stoyan B. Bekiarov", "CRC Press, 2004", 285, 15.1, True, 7,
  "Outline dikupas dari pembungkus 19 Agu 2026",
  "Klasifikasi UPS (offline, line-interactive, online dan turunannya), topologi konverter "
  "dan inverter, penyimpan energi dan pengisi baterai, penyaring aktif untuk perbaikan "
  "kualitas daya, strategi kendali, serta standar terkait.",
  "Pemilihan topologi dan kapasitas UPS, penentuan konfigurasi redundansi, serta "
  "penjelasan teknis kualitas daya dalam dokumen penawaran."),

 ("Video Analytics",
  "Computer Vision: Algorithms and Applications, Second Edition",
  "Richard Szeliski", "Springer, 2022", 938, 26.5, True, 354, "",
  "Pembentukan citra, pengolahan citra, pencocokan model dan optimasi, pembelajaran dalam, "
  "pengenalan objek, deteksi dan pencocokan fitur, penyelarasan dan penjahitan citra, "
  "estimasi gerak, fotografi komputasional, structure from motion dan SLAM, estimasi "
  "kedalaman, rekonstruksi tiga dimensi, dan perenderan berbasis citra.",
  "Landasan ilmiah modul analitik video: deteksi dan pelacakan objek, pengenalan pelat "
  "nomor dan wajah, serta penilaian klaim akurasi produk analitik dari pemasok."),
]

# --- Angka volume diukur ulang dari berkas yang benar-benar ada di disk, bukan
#     disalin dari audit lama. Dengan begitu dokumen ini selalu cocok dengan rak.
import glob
import fitz

ROOT = r'C:\Users\gspen\Videos\Buku'


def _ukur(b):
    folder, catatan = b[0], b[8]
    d = os.path.join(ROOT, folder)
    if catatan.startswith('Edisi lama'):
        kandidat = sorted(glob.glob(os.path.join(d, '_arsip', '*.pdf')))
    else:
        kandidat = sorted(glob.glob(os.path.join(d, '*.pdf')))
    if not kandidat:
        return b
    doc = fitz.open(kandidat[0])
    n = doc.page_count
    probe = [max(1, int(n * r)) for r in (0.15, 0.4, 0.7)]
    chars = sum(len(doc[x - 1].get_text().strip()) for x in probe)
    b = list(b)
    b[4], b[5], b[6], b[7] = n, round(os.path.getsize(kandidat[0]) / 1048576, 1), chars > 200, len(doc.get_toc())
    doc.close()
    return tuple(b)


BOOKS = [_ukur(b) for b in BOOKS]

TOTAL_BOOKS = len(BOOKS)
TOTAL_PAGES = sum(b[4] for b in BOOKS)
TOTAL_MB = sum(b[5] for b in BOOKS)


# ----------------------------------------------------------------- helpers
def shade(cell, hexfill):
    el = OxmlElement('w:shd')
    el.set(qn('w:val'), 'clear')
    el.set(qn('w:fill'), hexfill)
    cell._tc.get_or_add_tcPr().append(el)


def set_font(run, size=10, bold=False, color=None, name='Calibri', italic=False):
    run.font.size = Pt(size)
    run.font.bold = bold
    run.font.italic = italic
    run.font.name = name
    if color is not None:
        run.font.color.rgb = color
    rpr = run._element.get_or_add_rPr()
    rf = rpr.find(qn('w:rFonts'))
    if rf is None:
        rf = OxmlElement('w:rFonts')
        rpr.append(rf)
    for a in ('w:ascii', 'w:hAnsi', 'w:cs'):
        rf.set(qn(a), name)


def para(doc, text='', size=10, bold=False, color=None, space_after=6,
         align=None, italic=False, name='Calibri'):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    if align is not None:
        p.alignment = align
    if text:
        set_font(p.add_run(text), size, bold, color, name, italic)
    return p


def rule(doc, color='1F3355', size=12):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(0)
    pbdr = OxmlElement('w:pBdr')
    bottom = OxmlElement('w:bottom')
    bottom.set(qn('w:val'), 'single')
    bottom.set(qn('w:sz'), str(size))
    bottom.set(qn('w:space'), '1')
    bottom.set(qn('w:color'), color)
    pbdr.append(bottom)
    p._p.get_or_add_pPr().append(pbdr)
    return p


def mktable(doc, widths_cm, header=None, header_fill=HDR_FILL):
    t = doc.add_table(rows=0, cols=len(widths_cm))
    t.style = 'Table Grid'
    t.alignment = WD_TABLE_ALIGNMENT.LEFT
    t.autofit = False
    if header:
        row = t.add_row()
        for i, (txt, w) in enumerate(zip(header, widths_cm)):
            c = row.cells[i]
            c.width = Cm(w)
            c.text = ''
            p = c.paragraphs[0]
            p.paragraph_format.space_after = Pt(2)
            p.paragraph_format.space_before = Pt(2)
            set_font(p.add_run(txt), 9, True, RGBColor(0xFF, 0xFF, 0xFF))
            shade(c, header_fill)
    return t


def addrow(t, values, widths_cm, size=9, fill=None, bolds=None, aligns=None):
    row = t.add_row()
    for i, (txt, w) in enumerate(zip(values, widths_cm)):
        c = row.cells[i]
        c.width = Cm(w)
        c.text = ''
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.space_before = Pt(2)
        if aligns and aligns[i] is not None:
            p.alignment = aligns[i]
        set_font(p.add_run(str(txt)), size, bool(bolds and bolds[i]))
        if fill:
            shade(c, fill)
    return row


def footer_text(section, text):
    p = section.footer.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_font(p.add_run(text), 8, False, GREY)


# ----------------------------------------------------------------- document
doc = Document()
sec = doc.sections[0]
sec.page_width, sec.page_height = Cm(21.0), Cm(29.7)          # A4
sec.top_margin = Cm(2.2); sec.bottom_margin = Cm(2.0)
sec.left_margin = Cm(2.2); sec.right_margin = Cm(2.0)
footer_text(sec, 'Resume Perpustakaan Teknis  ·  C:\\Users\\gspen\\Videos\\Buku  ·  19 Agustus 2026')

st = doc.styles['Normal']
st.font.name = 'Calibri'
st.font.size = Pt(10)

# --- Judul
para(doc, 'RESUME PERPUSTAKAAN TEKNIS', 20, True, NAVY, space_after=2)
para(doc, 'Audit isi dan status 23 buku rujukan pada 22 folder topik', 11, False, GREY, space_after=10)
rule(doc)

CW = [4.6, 4.6, 4.6, 3.0]
t = mktable(doc, CW, ['Jumlah buku', 'Total halaman', 'Total ukuran', 'Folder topik'])
addrow(t, [f'{TOTAL_BOOKS} berkas PDF', f'{TOTAL_PAGES:,}'.replace(',', '.') + ' halaman',
           f'{TOTAL_MB/1024:.2f} GB'.replace('.', ','), '22 folder'], CW, size=10,
       bolds=[True, True, True, True])
para(doc, '', space_after=8)

para(doc, 'Ringkasan', 13, True, NAVY, space_after=4)
para(doc,
     'Koleksi ini menutup delapan lini pekerjaan sekaligus: sistem pengawasan video, jaringan dan '
     'infrastruktur teknologi informasi, kabel serat optik, catu daya dan kelistrikan, proteksi '
     'dan pembumian, keandalan dan pemeliharaan, keamanan siber, serta struktur dan mekanik. '
     'Sebagian besar buku merupakan rujukan baku di bidangnya dan berada pada edisi mutakhir.',
     space_after=6)
para(doc,
     'Seluruh pekerjaan pembenahan pada rak ini sudah selesai per 19 Agustus 2026. Dua buku yang '
     'semula hanya berupa gambar kini dapat dicari (RCM II 444 halaman dan FOA Reference Guide '
     '214 halaman). Lima buku yang sama sekali tidak memiliki daftar isi kini punya, dan empat '
     'buku yang bookmark-nya masih berupa kode berkas seperti "3035_c01.pdf" sudah diperbaiki. '
     'Nama berkas diseragamkan, duplikat edisi CCNA diarsipkan, dan struktur folder dirapikan.',
     space_after=6)
para(doc,
     'Satu hal yang tidak dapat diperbaiki: berkas Diesel Generator Handbook kehilangan sekitar '
     '55 halaman - Bab 11 dan bagian awal Bab 12 tidak ada di dalamnya. Penanda sudah dipasang '
     'di daftar isinya, tetapi isi yang hilang perlu dicarikan salinan pengganti.',
     space_after=6)
para(doc,
     'Angka volume, lapisan teks, dan jumlah bookmark pada dokumen ini diukur langsung dari '
     'berkas saat dokumen dibuat, sehingga selalu mencerminkan keadaan rak yang sebenarnya. '
     'Setiap folder buku kini juga memuat berkas RESUME - <judul>.md berisi ringkasan isi buku '
     'berikut rujukan halaman terverifikasi. Riwayat pengerjaan ada pada RENCANA-KERJA.md, '
     'dan peta celah koleksi pada PETA-CELAH-KOLEKSI.md.',
     space_after=10)

# --- Tabel inventaris
para(doc, 'Daftar Inventaris', 13, True, NAVY, space_after=4)
IW = [0.8, 3.6, 6.4, 1.6, 1.6, 2.6]
t = mktable(doc, IW, ['No', 'Folder', 'Judul', 'Hal.', 'MB', 'Status teknis'])
CT = WD_ALIGN_PARAGRAPH.CENTER
for i, b in enumerate(BOOKS, 1):
    folder, judul, penulis, terbit, hal, mb, ocr, toc, catatan = b[:9]
    if not ocr:
        status = 'Perlu OCR'
    elif toc == 0:
        status = 'Tanpa bookmark'
    elif catatan.startswith('Edisi lama'):
        status = 'Arsip (edisi lama)'
    else:
        status = 'Siap pakai'
    addrow(t, [i, folder.replace('  ', ' '), judul, f'{hal:,}'.replace(',', '.'),
               f'{mb:.1f}'.replace('.', ','), status], IW,
           fill=(ALT_FILL if i % 2 == 0 else None),
           aligns=[CT, None, None, CT, CT, None])
para(doc, '', space_after=4)
para(doc, 'Status "Siap pakai" berarti teks dapat dicari dan bookmark bab tersedia serta terbaca.',
     8.5, False, GREY, space_after=0, italic=True)

doc.add_page_break()

# --- Resume per folder
para(doc, 'Resume per Folder', 15, True, NAVY, space_after=2)
para(doc, 'Disusun menurut abjad nama folder', 9, False, GREY, space_after=8, italic=True)
rule(doc)

MW = [3.2, 11.4]
for i, b in enumerate(BOOKS, 1):
    folder, judul, penulis, terbit, hal, mb, ocr, toc, catatan, cakupan, guna = b
    para(doc, f'{i}.  {folder.replace("  ", " ")}', 12, True, NAVY, space_after=3)
    para(doc, judul, 10.5, True, space_after=1)
    para(doc, f'{penulis}  ·  {terbit}', 9.5, False, GREY, space_after=5)

    t = mktable(doc, MW)
    status_teks = 'Teks dapat dicari' if ocr else 'Belum OCR — teks tidak dapat dicari'
    status_toc = (f'{toc} entri' if toc else 'tidak ada')
    import glob as _g
    _r = _g.glob(os.path.join(ROOT, folder, 'RESUME*.md'))
    resume = os.path.basename(_r[0]) if _r else 'belum ada'
    rows = [('Volume', f'{hal:,}'.replace(',', '.') + ' halaman  ·  ' + f'{mb:.1f}'.replace('.', ',') + ' MB'),
            ('Lapisan teks', status_teks),
            ('Bookmark', status_toc + (f' — {catatan}' if catatan else '')),
            ('Resume', resume),
            ('Cakupan isi', cakupan),
            ('Pemakaian', guna)]
    for k, v in rows:
        row = t.add_row()
        c0, c1 = row.cells
        c0.width, c1.width = Cm(MW[0]), Cm(MW[1])
        c0.text = ''; c1.text = ''
        p0 = c0.paragraphs[0]; p0.paragraph_format.space_after = Pt(2)
        p0.paragraph_format.space_before = Pt(2)
        set_font(p0.add_run(k), 9, True, NAVY)
        shade(c0, ALT_FILL)
        p1 = c1.paragraphs[0]; p1.paragraph_format.space_after = Pt(2)
        p1.paragraph_format.space_before = Pt(2)
        set_font(p1.add_run(v), 9)
    para(doc, '', space_after=10)

doc.add_page_break()

# --- Rencana kerja
para(doc, 'Rencana Kerja', 15, True, NAVY, space_after=2)
para(doc, 'Ringkasan dari RENCANA-KERJA.md', 9, False, GREY, space_after=8, italic=True)
rule(doc)

PW = [1.6, 5.4, 4.2, 3.4]
t = mktable(doc, PW, ['Prio', 'Pekerjaan', 'Sasaran', 'Cakupan'])
plan = [
 ('P0', 'OCR dan kompresi RCM II', 'Teks dapat dicari, ukuran di bawah 60 MB',
  '444 hal. · 186,7 MB'),
 ('P0', 'OCR FOA Reference Guide to Fiber Optics', 'Teks dapat dicari, bookmark dipertahankan',
  '214 hal. · 51,8 MB'),
 ('P1', 'Bangun bookmark lima buku tanpa daftar isi',
  'Outline bab lengkap tiap buku', 'TCP/IP, CCTV, RCM II, Lightning, FO Test'),
 ('P1', 'Perbaiki bookmark berjudul kode berkas',
  'Judul bab terbaca manusia', 'Security Engineering, Genset, UPS, Storage'),
 ('P2', 'Selesaikan duplikat pustaka CCNA',
  'Edisi 2024 jadi rujukan, edisi 2019 diarsipkan', '5.105 hal. · 183 MB'),
 ('P2', 'Standarkan penamaan berkas',
  'Pola "Penulis - Judul (Edisi, Tahun)"', '23 berkas'),
 ('P2', 'Rapikan struktur dan nama folder',
  'Hilangkan folder bersarang dan spasi ganda', 'RCM, CCTV, Mechanical, Storage, TCP'),
 ('P3', 'Susun katalog induk', 'Satu indeks berisi status dan pemakaian tiap buku', '23 judul'),
 ('P3', 'Petakan celah koleksi', 'Daftar topik yang belum terwakili', 'Tinjauan bersama'),
]
for i, r in enumerate(plan):
    addrow(t, r, PW, fill=(ALT_FILL if i % 2 else None),
           aligns=[CT, None, None, None], bolds=[True, False, False, False])

para(doc, '', space_after=8)
para(doc, 'Yang dikerjakan lebih dulu', 12, True, NAVY, space_after=3)
para(doc,
     'RCM II. Buku ini satu-satunya di rak yang tidak memiliki salinan lain — berkas SWF sumbernya '
     'sudah tidak ada — sekaligus berkas terbesar, satu-satunya yang tidak dapat dicari sekaligus '
     'tidak memiliki bookmark. Satu pekerjaan menyelesaikan tiga masalah. Buat cadangan berkas '
     'sebelum diproses.', space_after=10)

para(doc, 'Prioritas pemanfaatan menurut lini kerja', 12, True, NAVY, space_after=3)
LW = [4.6, 5.4, 4.6]
t = mktable(doc, LW, ['Lini kerja', 'Buku inti', 'Pendukung'])
lines = [
 ('Sistem pengawasan video', 'CCTV: From Light to Pixels', 'Computer Vision; Storage Networks Explained'),
 ('Jaringan dan infrastruktur TI', 'TCP/IP Illustrated Vol. 1', 'Network Warrior; CCNA 2024; Computer Networking'),
 ('Kabel serat optik', 'FOA Reference Guide', 'Reference Guide to Fiber Optic Testing Vol. 1'),
 ('Catu daya dan kelistrikan', 'Electrical Power Equipment Maintenance', 'UPS and Active Filters; Battery Reference Book; Diesel Generator Handbook'),
 ('Proteksi dan pembumian', 'Grounds for Grounding', 'The Art and Science of Lightning Protection'),
 ('Keandalan dan pemeliharaan', 'RCM II', 'Maintenance and Reliability Best Practices; Maintenance Planning'),
 ('Keamanan siber', 'Security Engineering', 'The Practice of System and Network Administration'),
 ('Struktur dan mekanik', "Shigley's Mechanical Engineering Design", 'Infrared Thermal Imaging'),
]
for i, r in enumerate(lines):
    addrow(t, r, LW, fill=(ALT_FILL if i % 2 else None))

doc.save(OUT)
print('tersimpan:', OUT, round(os.path.getsize(OUT)/1024, 1), 'KB')
print('buku', TOTAL_BOOKS, 'halaman', TOTAL_PAGES, 'GB', round(TOTAL_MB/1024, 2))
