# -*- coding: utf-8 -*-
"""
embed_fonts.py — langkah font DATUM v2.0.0: probe registry, instal per-user,
embed TrueType ke DOCX (kelas builder/render DHS-RB-05, 2026-10-05; kartu t_28d93e3c).

PROVENANS: pola instal per-user tanpa admin dipindah utuh dari pitfalls terwaris
paket datum-house-style v2.0.0 SKILL.md (validated DEMS-DATUM-0925): salin ttf ke
%LOCALAPPDATA%\\Microsoft\\Windows\\Fonts, tulis value "<Family> <Style> (TrueType)"
-> filename di HKCU ...\\CurrentVersion\\Fonts (KEY_WOW64_64KEY), lalu
AddFontResourceExW(path,0,0) + broadcast WM_FONTCHANGE. Sumber ttf fleet:
workspace/EXPO [2026]/Font_DATUM/ dan gsp-hermes/skills/gsp-canvas-design/canvas-fonts/.
ensure_fonts() hard-fail mengikuti pitfall yang sama: raise, bukan diam-diam fallback.
Langkah embed DOCX memakai Word COM EmbedTrueTypeFonts (satu-satunya penanaman
font nyata yang tersedia di host Windows ini; python-docx tidak menulis fontPart).
Bukan restorasi Rev J.

Pemakaian:
    python embed_fonts.py check                 # exit 0 trio Plex terdaftar
    python embed_fonts.py install               # instal yang hilang (per-user)
    python embed_fonts.py embed <dok.docx>      # Word COM: embed TrueType + simpan
    from embed_fonts import ensure_fonts        # panggil SEBELUM build apa pun
"""
import ctypes
import json
import os
import shutil
import subprocess
import sys
import winreg

_HERE = os.path.dirname(os.path.abspath(__file__))
if _HERE not in sys.path:
    sys.path.insert(0, _HERE)

from datumbind import tokens_path

_TOK = json.load(open(tokens_path(), encoding="utf-8"))
_FACES = _TOK["type"]["faces"]          # serif/condensed/mono/workbook_ui

FONT_DIR = os.path.join(os.environ["LOCALAPPDATA"], "Microsoft", "Windows", "Fonts")
REG_PATH = r"Software\Microsoft\Windows NT\CurrentVersion\Fonts"

# sumber ttf fleet (path tetap dua lokasi terbukti ada di host)
WS = r"C:/Users/TRIAL/workspace"
SRC_DIRS = [
    WS + "/EXPO [2026]/Font_DATUM",
    WS + "/gsp-hermes/skills/gsp-canvas-design/canvas-fonts",
]
# keluarga wajib DATUM (token type.faces) -> kandidat berkas (basename, dir index)
NEED = {
    _FACES["serif"]:     ["IBMPlexSerif-Regular.ttf", "IBMPlexSerif-Bold.ttf"],
    _FACES["mono"]:      ["IBMPlexMono-Regular.ttf", "IBMPlexMono-Bold.ttf"],
    _FACES["condensed"]: ["IBMPlexSansCond-Regular.ttf",
                          "IBMPlexSansCondensed-Bold.ttf"],
}


class FontDefect(Exception):
    pass


def _registry_faces():
    """Kumpulkan value nama font (TrueType) dari HKCU lalu HKLM."""
    found = {}
    for hive in (winreg.HKEY_CURRENT_USER, winreg.HKEY_LOCAL_MACHINE):
        try:
            k = winreg.OpenKey(hive, REG_PATH, 0,
                               winreg.KEY_WOW64_64KEY | winreg.KEY_READ)
        except FileNotFoundError:
            continue
        for i in range(winreg.QueryInfoKey(k)[1]):
            name, val, _ = winreg.EnumValue(k, i)
            found[name.lower()] = (name, val, hive is winreg.HKEY_CURRENT_USER)
    return found


def ensure_fonts(families=None):
    """Hard-fail sebelum build: trio wajah token wajib terdaftar di registry font.
    Raise FontDefect bila ada yang hilang — jangan diam-diam fallback (pitfall)."""
    faces = _registry_faces()
    want = families or list(NEED.keys())
    missing = []
    for fam in want:
        if not any(fam.lower() in name for name in faces):
            missing.append(fam)
    if missing:
        raise FontDefect(
            "ensure_fonts: wajah token DATUM tidak terdaftar di host: "
            + ", ".join(missing)
            + ". Jalankan `python embed_fonts.py install` atau pasang manual; "
              "build dengan fallback diam-diam = dokumen salah wajah (DATUM-05).")
    return {f: True for f in want}


def _find_src(fname):
    for d in SRC_DIRS:
        p = os.path.join(d, fname)
        if os.path.isfile(p):
            return p
    return None


def _style_of(fname):
    low = fname.lower()
    if "bolditalic" in low or "bold italic" in low:
        return "Bold Italic"
    if "bold" in low or low.endswith("-bold.ttf"):
        return "Bold"
    if "italic" in low:
        return "Italic"
    if "semibold" in low:
        return "SemiBold"
    return "Regular"


def install_fonts(report=print):
    """Instal per-user (tanpa admin) seluruh kandidat NEED yang belum terdaftar.
    Return dict {family: [file terpasang/dipakai]}. FontDefect bila sumber ttf
    tidak ditemukan sama sekali untuk keluarga yang hilang."""
    faces = _registry_faces()
    installed = {}
    user_dir = FONT_DIR
    os.makedirs(user_dir, exist_ok=True)
    for fam, files in NEED.items():
        have = any(fam.lower() in n for n in faces)
        got = []
        for fname in files:
            already = any(fam.lower() in n and _style_of(fname).lower() in n
                          for n in faces)
            src = _find_src(fname)
            if src is None:
                if not have:
                    raise FontDefect(f"sumber ttf {fname} tidak ada di {SRC_DIRS} "
                                     f"dan keluarga '{fam}' belum terpasang.")
                continue
            dst = os.path.join(user_dir, fname)
            if not os.path.isfile(dst):
                shutil.copyfile(src, dst)
                report(f"  salin {fname} -> {user_dir}")
            key = f"{fam} {_style_of(fname)} (TrueType)"
            try:
                k = winreg.OpenKey(winreg.HKEY_CURRENT_USER, REG_PATH, 0,
                                   winreg.KEY_WOW64_64KEY | winreg.KEY_WRITE)
                winreg.SetValueEx(k, key, 0, winreg.REG_SZ, fname)
                winreg.CloseKey(k)
            except OSError as ex:
                raise FontDefect(f"registry HKCU gagal ditulis untuk '{key}': {ex!r}")
            # daftarkan ke sesi GDI + beri tahu semua aplikasi
            added = ctypes.windll.gdi32.AddFontResourceExW(dst, 0, 0)
            HWND_BROADCAST = 0xFFFF; WM_FONTCHANGE = 0x001D
            ctypes.windll.user32.SendMessageTimeoutW(
                HWND_BROADCAST, WM_FONTCHANGE, 0, 0, 0x0002, 1000,
                ctypes.byref(ctypes.c_ulong(0)))
            report(f"  daftar {key} (AddFontResource={added})")
            got.append(fname)
        installed[fam] = got
    return installed


def _restore_update_fields(path):
    """Word membuang w:updateFields saat save dengan EmbedTrueTypeFonts (temuan
    uji COM DHS-RB-05, probe_word_save.py). Pasca-proses zip: sisipkan kembali
    <w:updateFields w:val='true'/> sebelum w:compat bila hilang."""
    import zipfile, shutil
    tmp = path + ".tmp"
    with zipfile.ZipFile(path) as zin:
        items = [(n, zin.read(n)) for n in zin.namelist()]
    with zipfile.ZipFile(tmp, "w", zipfile.ZIP_DEFLATED) as zout:
        for name, data in items:
            if name == "word/settings.xml":
                s = data.decode("utf-8")
                if 'w:updateFields' not in s:
                    ins = '<w:updateFields w:val="true"/>'
                    i = s.find("<w:compat")
                    s = (s[:i] + ins + s[i:]) if i != -1 else \
                        s.replace("</w:settings>", ins + "</w:settings>")
                    data = s.encode("utf-8")
            zout.writestr(name, data)
    shutil.move(tmp, path)


def embed_docx(path, subset=True):
    """Tanam TrueType ke DOCX lewat Word COM (jalur nyata host Windows).
    Pitfall warisan dihormati: ReadOnly=False, AddToRecentFiles=False, Close(False)
    hanya bila mengubah; di sini kita SaveAs2 ke path yang sama setelah embed.
    Pasca-proses: pulihkan w:updateFields yang dibuang Word saat save embed."""
    try:
        import win32com.client
    except Exception as ex:
        raise FontDefect(f"pywin32 tidak tersedia: {ex!r}")
    app = None
    abspath = os.path.abspath(path)
    try:
        app = win32com.client.DispatchEx("Word.Application")
        app.Visible = False; app.DisplayAlerts = 0
        doc = app.Documents.Open(abspath, ReadOnly=False, AddToRecentFiles=False)
        doc.EmbedTrueTypeFonts = True
        doc.SaveSubsetFonts = bool(subset)
        doc.Save()
        ok = bool(doc.EmbedTrueTypeFonts)
        doc.Close(False)
    finally:
        if app is not None:
            try:
                app.Quit()
            except Exception:
                pass
    _restore_update_fields(abspath)
    return ok


def verify_embedded(path):
    """Cek hasil: fontTable.xml/w:fonts ada? Berkas font tertanam di /fonts/ zip?"""
    import zipfile
    with zipfile.ZipFile(path) as z:
        names = z.namelist()
        embedded = [n for n in names if n.startswith("word/fonts/")
                    and n.endswith((".odttf", ".ttf"))]
    return embedded


def main(argv):
    if not argv or argv[0] == "check":
        try:
            res = ensure_fonts()
            print("CHECK fonts: PASS — trio Plex terdaftar:", ", ".join(res))
            return 0
        except FontDefect as ex:
            print("CHECK fonts: FAIL —", ex)
            return 1
    if argv[0] == "install":
        got = install_fonts()
        for fam, files in got.items():
            print(f"  {fam}: {files or 'sudah ada'}")
        res = ensure_fonts()
        print("VERDICT: PASS —", ", ".join(res))
        return 0
    if argv[0] == "embed" and len(argv) > 1:
        ok = embed_docx(argv[1])
        emb = verify_embedded(argv[1])
        print(f"embed={ok} font_part={len(emb)}")
        return 0 if ok else 1
    print(__doc__)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
