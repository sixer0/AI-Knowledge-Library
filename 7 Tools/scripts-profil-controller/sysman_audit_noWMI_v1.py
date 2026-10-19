#!/usr/bin/env python3
"""Audit gateway tanpa WMI (NtQuerySystemInformation + NtQueryInformationProcess).

Alasan ada: 15-10 malam WMI/CIM di host wedged (psutil process_iter >150 dtk,
CIM berfilter nama juga >150 dtk). Instrumen ini baca daftar proses + commandline
melalui ntdll native, tanpa sentuh WMI. Read-only.
"""
import ctypes, ctypes.wintypes as wt, json, re, datetime, pathlib, sys, os

k32 = ctypes.WinDLL('kernel32.dll', use_last_error=True)
nt = ctypes.WinDLL('ntdll.dll', use_last_error=True)
nt.NtQuerySystemInformation.restype = ctypes.c_ulong
nt.NtQueryInformationProcess.restype = ctypes.c_ulong

STATUS_SUCCESS = 0
SystemProcessInformation = 5
ProcessCommandLineInformation = 60
PROCESS_QUERY_LIMITED_INFORMATION = 0x1000

# SYSTEM_PROCESS_INFORMATION iterasi manual: pakai blok mentah + parse offset.
# Layout x64: ULONG NextEntryOffset; ULONG NumberOfThreads; LARGE_INTEGER WorkingSetPrivateSize;
# ULONG HardFaultCount; ULONG NumberOfThreadsHighWatermark; ULONGLONG CycleTime;
# LARGE_INTEGER CreateTime; LARGE_INTEGER UserTime; LARGE_INTEGER KernelTime;
# UNICODE_STRING ImageName; KPRIORITY BasePriority; HANDLE UniqueProcessId; HANDLE InheritedFromUniqueProcessId;
# ULONG HandleCount; ULONG SessionId; ULONG UniqueProcessKey; SIZE_T PeakVirtualSize; ...
def list_processes():
    size = 0x10000
    buf = ctypes.create_string_buffer(size)
    while True:
        rv = nt.NtQuerySystemInformation(SystemProcessInformation, buf, size, ctypes.byref(ctypes.c_ulong()))
        if rv == 0xC0000004:  # STATUS_INFO_LENGTH_MISMATCH
            size *= 2
            buf = ctypes.create_string_buffer(size)
            continue
        if rv != STATUS_SUCCESS:
            print(f"NtQuerySystemInformation gagal rc=0x{rv & 0xffffffff:08x}", file=sys.stderr)
            return []
        break
    out = []
    off = 0
    raw = buf.raw
    total = len(raw)
    while off < total - 48:
        next_off = int.from_bytes(raw[off:off+4], 'little')
        # ImageName UNICODE_STRING at offset 0x38 (Length, MaxLen, Buffer ptr)
        p = off
        img_len = int.from_bytes(raw[p+0x38:p+0x3A], 'little')
        img_ptr = int.from_bytes(raw[p+0x40:p+0x48], 'little')
        pid = int.from_bytes(raw[p+0x50:p+0x58], 'little')       # UniqueProcessId
        ppid = int.from_bytes(raw[p+0x58:p+0x60], 'little')      # InheritedFromUniqueProcessId
        img = ''
        if img_ptr and img_len:
            try:
                img = ctypes.wintypes.c_wchar_p.from_buffer_copy(
                    raw[off + (img_ptr - id(buf)):] if False else '',
                ).value if False else ctypes.c_wchar_p(raw[shift_of(raw, off, img_ptr):][:img_len] if False else '').value
            except Exception:
                img = ''
        # fallback sederhana: baca wchar dari buffer asli via address
        try:
            img = ctypes.wstring_at(ctypes.addressof(buf) + off + 0 if False else img_ptr, img_len // 2)
        except Exception:
            img = ''
        out.append((pid, ppid, img))
        if next_off == 0:
            break
        off += next_off
    return out

def shift_of(raw, off, ptr):
    # konversi pointer -> offset di buffer (silang buffer asli)
    try:
        import ctypes
        base = ctypes.addressof(ctypes.create_string_buffer(1))  # dummy; pakai fallback
    except Exception:
        pass
    return 0

def cmdline_for_pid(pid):
    try:
        h = 0
        for access in (0x1000, 0x0400):  # PROCESS_QUERY_LIMITED_INFORMATION, lalu penuh
            h = k32.OpenProcess(access, 0, pid)
            if h:
                break
        if not h:
            return None
        try:
            ret_len = ctypes.c_ulong(0)
            # probe ukuran: buffer NULL
            rc = nt.NtQueryInformationProcess(h, ProcessCommandLineInformation, None, 0, ctypes.byref(ret_len))
            need = ret_len.value
            if need == 0:
                return None
            buf = ctypes.create_string_buffer(need)
            rc = nt.NtQueryInformationProcess(h, ProcessCommandLineInformation, buf, need, ctypes.byref(ret_len))
            if rc != STATUS_SUCCESS:
                return None
            # buf = UNICODE_STRING {USHORT Length; USHORT MaximumLength; pad4; WCHAR* Buffer}
            length = int.from_bytes(buf.raw[0:2], 'little')
            ptr = int.from_bytes(buf.raw[8:16], 'little')
            if not ptr or length == 0:
                return None
            return ctypes.wstring_at(ptr, length // 2)
        finally:
            k32.CloseHandle(h)
    except Exception:
        return None

REG = pathlib.Path(r'C:/Users/TRIAL/workspace/gsp-hermes/workspace/fleet/PROFILE-REGISTRY.json')
d = json.loads(REG.read_text(encoding='utf-8'))
live = set(d['hidup'])
must = set(d['gateway_wajib_hidup'])

procs = list_processes()
runs = {}
notes = []
for pid, ppid, img in procs:
    if img not in ('python.exe', 'pythonw.exe', 'hermes.exe'):
        continue
    cl = cmdline_for_pid(pid) or ''
    if 'gateway' not in cl:
        continue
    m = re.search(r'--profile\s+(\S+)', cl) or re.search(r'-p\s+(\S+)', cl)
    prof = m.group(1) if m else 'default'
    if 'gateway run' in cl:
        runs.setdefault(prof, []).append((pid, ppid))
    else:
        notes.append((prof, pid, cl[:120]))

print("=== AUDIT GATEWAY FLEET (noWMI)", datetime.datetime.now().isoformat(timespec='seconds'), "===")
print(f"registri hidup: {len(live)} | wajib gateway: {sorted(must)}")
print("--- proses 'gateway run' per profil (root = instans independen) ---")
all_pids = {p for pids in runs.values() for p,_ in pids}
for prof in sorted(runs):
    roots = [p for p,pp in runs[prof] if pp not in all_pids]
    tag = "HIDUP" if prof in live else "DI-LUAR-DAFTAR-HIDUP"
    print(f"  {prof:<22} proses={len(runs[prof]):<2} root={len(roots)} pids={[p for p,_ in sorted(runs[prof])]} {tag}")
if not runs:
    print("  (tidak ada proses 'gateway run' terdeteksi)")
print("--- vonis ---")
mati=[]; hantu=[]; ganda=[]
for m in sorted(must):
    roots = [p for p,pp in runs.get(m, []) if pp not in all_pids]
    if not roots:
        mati.append(m); print(f"  WAJIB {m:<20} root=0 -> MATI (monitor harus start)")
    elif len(roots) > 1:
        ganda.append((m, roots)); print(f"  WAJIB {m:<20} root={len(roots)} {roots} -> GANDA (instans duplikat nyata)")
    else:
        print(f"  WAJIB {m:<20} root=1 -> OK")
for prof in sorted(runs):
    if prof not in live:
        hantu.append(prof); print(f"  HANTU {prof:<20} pids={[p for p,_ in runs[prof]]} -> di luar daftar hidup, hentikan")
for prof, pid, c in notes:
    print(f"  CATATAN {prof:<18} proses ber-'gateway' tanpa 'gateway run': pid={pid} cmd={c[:80]}")
ok = not mati and not hantu and not ganda
print("VERDICT:", "SEHAT" if ok else f"PERLU-AKSI (wajib_mati={mati}, hantu={hantu}, ganda={[g[0] for g in ganda]})")
