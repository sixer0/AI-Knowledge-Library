# Cek deterministik: pesan WhatsApp hanya hasil akhir
import sys, json
sys.path.insert(0, r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent")
from hermes_cli.config import load_config
from gateway.display_config import resolve_display_setting

cfg = load_config()
keys = ["tool_progress", "show_reasoning", "streaming",
        "interim_assistant_messages", "long_running_notifications",
        "busy_ack_detail", "busy_steer_ack_enabled"]
fails = 0
expect = {"tool_progress": "off", "show_reasoning": False, "streaming": False,
          "interim_assistant_messages": False, "long_running_notifications": False,
          "busy_ack_detail": False, "busy_steer_ack_enabled": False}
for k in keys:
    v = resolve_display_setting(cfg, "whatsapp", k)
    ok = (type(v) == type(expect[k]) and v == expect[k])
    if k == "tool_progress":
        # gerbang run.py L28436: enabled bila mode TIDAK in {"off","log"};
        # False/None lolos gerbang -> wajib string "off" persis.
        ok = (v == "off")
    print(("PASS" if ok else "FAIL"), k, "=", repr(v))
    if not ok:
        fails += 1
wrap = cfg.get("cron", {}).get("wrap_response", True)
ok = wrap is False
print(("PASS" if ok else "FAIL"), "cron.wrap_response =", repr(wrap))
if not ok:
    fails += 1
foot = cfg.get("display", {}).get("runtime_footer", {})
enabled = foot.get("enabled", False) if isinstance(foot, dict) else False
ok = not enabled
print(("PASS" if ok else "FAIL"), "display.runtime_footer.enabled =", repr(enabled))
if not ok:
    fails += 1
print("VERDICT:", "PASS" if fails == 0 else f"FAIL ({fails})")
