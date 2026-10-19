# Ronde 15-10 zr: cek PID lama pada berkas heartbeat basi (4 profil tanpa proses gateway)
# apakah masih hidup di daftar proses via CreateToolhelp32Snapshot (non-WMI).
import ctypes, ctypes.wintypes as wt

TH32CS_SNAPPROCESS = 0x2
class PROCESSENTRY32W(ctypes.Structure):
    _fields_ = [("dwSize", wt.DWORD), ("cntUsage", wt.DWORD), ("th32ProcessID", wt.DWORD),
                ("th32DefaultHeapID", ctypes.POINTER(ctypes.c_ulong)), ("th32ModuleID", wt.DWORD),
                ("cntThreads", wt.DWORD), ("th32ParentProcessID", wt.DWORD),
                ("pcPriClassBase", ctypes.c_long), ("dwFlags", wt.DWORD),
                ("szExeFile", ctypes.c_wchar * 260)]

kernel32 = ctypes.windll.kernel32
snap = kernel32.CreateToolhelp32Snapshot(TH32CS_SNAPPROCESS, 0)
pids = set()
pe = PROCESSENTRY32W()
pe.dwSize = ctypes.sizeof(PROCESSENTRY32W)
if kernel32.Process32FirstW(snap, ctypes.byref(pe)):
    while True:
        pids.add(int(pe.th32ProcessID))
        if not kernel32.Process32NextW(snap, ctypes.byref(pe)):
            break
kernel32.CloseHandle(snap)

targets = {"gsp-creative": 8180, "gsp-firman-custom": 24004, "gsp-custodian": 8904, "gsp-skill-manager": 2864}
print("total proses terlihat:", len(pids))
for name, pid in targets.items():
    print("%-20s pid=%-6s %s" % (name, pid, "HIDUP" if pid in pids else "MATI"))
