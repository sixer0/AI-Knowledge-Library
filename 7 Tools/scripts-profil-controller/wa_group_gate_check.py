"""Verifikasi deterministik: apakah load_gateway_config() kini memuat
group_policy=allowlist + group_allow_from untuk whatsapp, dan apakah fungsi
intake asli adapter meloloskan pesan grup terkonfigurasi."""
import sys, os
sys.path.insert(0, r"C:\Users\TRIAL\AppData\Local\hermes\hermes-agent")
os.environ.setdefault("HERMES_HOME", r"C:\Users\TRIAL\AppData\Local\hermes")

GROUP = "120363412892547244@g.us"
SENDER_LID = "270660903399486@lid"  # Budi = 6281944335200

from gateway.config import load_gateway_config, Platform  # noqa: E402

cfg = load_gateway_config()
wa = cfg.platforms.get(Platform.WHATSAPP)
print("whatsapp enabled:", wa.enabled if wa else None)
extra = (wa.extra if wa else {}) or {}
print("extra.group_policy:", extra.get("group_policy"))
print("extra.group_allow_from:", extra.get("group_allow_from"))

# Jalankan gerbang intake ASLI (mixin) dengan extra hasil loader
from gateway.platforms.whatsapp_common import WhatsAppBehaviorMixin  # noqa: E402


class Harness(WhatsAppBehaviorMixin):
    def __init__(self, extra):
        class Cfg:
            pass
        self.config = Cfg()
        self.config.extra = extra
        self._group_policy = str(extra.get("group_policy") or "pairing").lower()
        raw = extra.get("group_allow_from") or []
        self._group_allow_from = {str(p).strip() for p in raw if str(p).strip()}
        self._dm_policy = "allowlist"
        self._allow_from = {"6281944335200", "20646662766775"}
        self._dm_allowlist_source = "WHATSAPP_ALLOWED_USERS"
        self._mention_patterns = []
        self.name = "whatsapp"

    def _is_broadcast_chat(self, cid):
        return "status" in cid

    def _live_dm_allow_from(self):
        return self._allow_from

    def _open_dm_opted_in(self):
        return False


h = Harness(extra)
data = {
    "chatId": GROUP,
    "isGroup": True,
    "senderId": SENDER_LID,
    "body": "Halo swarm",
    "botIds": ["6289525726790@s.whatsapp.net", "20646662766775@lid"],
    "mentionedIds": [],
}
print("intake grup (pengirim terdaftar, tanpa mention):", h._should_process_message(data))

data_other_group = dict(data, chatId="120363000000000000@g.us")
print("intake grup LAIN (tidak terdaftar) harus False:", h._should_process_message(data_other_group))

# authz gateway: sender match via ekspansi LID
from gateway.whatsapp_identity import expand_whatsapp_aliases  # noqa: E402
allowed = set()
for uid in ("6281944335200", "20646662766775"):
    allowed.update(expand_whatsapp_aliases(uid))
check_ids = {SENDER_LID, SENDER_LID.split("@")[0]}
check_ids.update(expand_whatsapp_aliases(SENDER_LID))
print("authz sender match (ekspansi LID):", bool(check_ids & allowed))
