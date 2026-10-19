import subprocess
CMD = ("Get-CimInstance Win32_Process -Filter \"Name='python.exe' OR Name='pythonw.exe'\" | "
       "ForEach-Object { if ($_.ProcessId -eq 536312 -or $_.ProcessId -eq 236288) { "
       "$_.ProcessId.ToString() + ' || ' + $_.CommandLine } }")
r = subprocess.run(['powershell.exe','-NoProfile','-Command',CMD],capture_output=True,text=True,timeout=150)
print(r.stdout.strip() or "(kedua PID tidak ditemukan - proses sudah selesai)")
