# Windows/WSL2: Docker published ports unreachable from Windows

## Symptom
- Container is `Up`, service answers from inside the container (`docker exec <c> wget -qO- http://localhost:PORT`) and from inside the docker-desktop distro (`wsl -d docker-desktop ... 127.0.0.1:PORT`).
- From Windows: `curl http://localhost:PORT` → HTTP 000 / "Empty reply"; `docker port <c>` may show the mapping or be empty; `netstat -ano | grep :PORT` shows no Windows-side listener (or one whose data never flows).

## Diagnostic ladder (cheapest first)
1. `docker ps --filter name=<c>` + `docker port <c>` — is the mapping registered?
2. `netstat -ano | grep ":<PORT>"` on Windows — is anything listening on the host side?
3. `docker exec <c> <probe>` — does the service answer inside the container?
4. `wsl -d docker-desktop sh -c "netstat -tln | grep <PORT>"` — is docker-proxy listening in the distro? (`ip -4 addr` in the distro shows mirrored vs NAT interfaces: mirrored shares Windows IPs e.g. `100.x`/`192.168.x`, NAT gets a private `172.x`.)
5. Identify Windows listeners: `powershell Get-Process -Id <PID>` — expect `com.docker.backend` (0.0.0.0) and `wslrelay` ([::1]) as the relay pair.
6. `.wslconfig` — `networkingMode=mirrored` is the prime suspect.
7. Hyper-V firewall: `powershell Get-NetFirewallHyperVVMSetting -PolicyStore ActiveStore` — `DefaultInboundAction: Block` can block too.

## Fixes (in order)
1. Hyper-V firewall → Allow (needs UAC; run via `Start-Process powershell -Verb RunAs` with a script that writes a result file, then poll):
   `Set-NetFirewallHyperVVMSetting -Name '{40E0AC32-46A5-438A-A0B2-2B479E8F2E90}' -DefaultInboundAction Allow`
   (May require a WSL VM restart — `wsl --shutdown` + `docker desktop start` — to take effect.)
2. **The fix that actually worked:** switch `.wslconfig` from `networkingMode=mirrored` to `networkingMode=default` (NAT), keep a `.wslconfig.bak`, then `wsl --shutdown` + `docker desktop stop` + `docker desktop start`. In mirrored mode the relay accepted TCP but dropped payloads; NAT mode's standard relay forwards correctly.

## Protocol-aware testing (the trap that wasted a session)
- `curl` against a non-HTTP service (e.g. redis on a published port) reports "Empty reply from server" / HTTP 000 even when forwarding is healthy — redis answers RESP, not HTTP.
- bash `/dev/tcp` + `timeout head -c` can silently return nothing in git-bash/MSYS.
- Correct probe: Python socket speaking the service's protocol:
```python
import socket
s = socket.create_connection(('127.0.0.1', 16379), timeout=5)
s.sendall(b'PING\r\n'); s.settimeout(3)
print(repr(s.recv(100)))   # expect b'+PONG\r\n'
```
Test all paths: `127.0.0.1`, `::1` (wslrelay), and the distro NAT IP — all three answered `+PONG` after the NAT fix.

## Post-fix state to expect (NAT mode)
- Distro shows `eth0` with a `172.x` NAT IP (no more mirrored `100.x`/`192.168.x` interfaces).
- Windows shows relay listeners on the published port; `docker port` shows `0.0.0.0:PORT` and `[::]:PORT`.
- Tailscale on the Windows side (tailscaled.exe) is unaffected by the mode switch.
