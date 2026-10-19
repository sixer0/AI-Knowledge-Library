"""Spawn WhatsApp bridge detached, meniru env yang dipasang adapter resmi.

Dipakai saat gateway menolak spawn ulang (reuse bridge lama via health
handshake) dan restart gateway bukan wewenang orkestrator. Bridge membaca
process.env sendiri: mode, allowlist, forward-owner, cache dirs.
"""
import os
import subprocess
import sys
from pathlib import Path

HH = Path(r"C:\Users\TRIAL\AppData\Local\hermes")
BRIDGE = HH / "hermes-agent/scripts/whatsapp-bridge/bridge.js"
SESSION = HH / "platforms/whatsapp/session"
LOG = HH / "platforms/whatsapp/bridge-manual.log"
NODE = r"C:\Program Files\nodejs\node.exe"


def read_env_keys():
    vals = {}
    for line in (HH / ".env").read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if line.startswith("WHATSAPP") and "=" in line:
            k, _, v = line.partition("=")
            vals[k.strip()] = v.strip()
    return vals


def main():
    wa = read_env_keys()
    mode = wa.get("WHATSAPP_MODE", "self-chat")
    env = os.environ.copy()
    env["HERMES_HOME"] = str(HH)
    for k, v in wa.items():
        env[k] = v
    env.setdefault("WHATSAPP_SEND_READ_RECEIPTS", "false")
    env["HERMES_IMAGE_CACHE_DIR"] = str(HH / "cache/images")
    env["HERMES_AUDIO_CACHE_DIR"] = str(HH / "cache/audio")
    env["HERMES_DOCUMENT_CACHE_DIR"] = str(HH / "cache/documents")

    creationflags = 0x00000008 | 0x00000200  # DETACHED | NEW_PROCESS_GROUP
    with open(LOG, "a", encoding="utf-8") as fh:
        p = subprocess.Popen(
            [NODE, str(BRIDGE), "--port", "3000", "--session", str(SESSION),
             "--mode", mode],
            stdout=fh, stderr=fh, env=env, cwd=str(BRIDGE.parent),
            creationflags=creationflags,
        )
    (SESSION / "bridge.pid").write_text(str(p.pid), encoding="utf-8")
    print(f"spawned pid={p.pid} mode={mode} "
          f"forward_owner={wa.get('WHATSAPP_FORWARD_OWNER_MESSAGES')} "
          f"allowed={wa.get('WHATSAPP_ALLOWED_USERS')}")


if __name__ == "__main__":
    sys.exit(main())
