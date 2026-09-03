"""Shared low-level Telegram Bot API client for this project's own dedicated
bot (separate token/chat from any other project's bot — see CLAUDE.md's
Personal Photo Series > Automated routine section for why). Mirrors
lr_common.py's style: REPO_ROOT-relative .env loading, plain requests,
explicit timeout on every call, SystemExit with a truncated body on failure.

Usage:
    from telegram_common import send_message, send_photo, send_video, get_updates
"""

import os
from pathlib import Path

import requests
from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

_BOT_TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN")
_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")

API_BASE = f"https://api.telegram.org/bot{_BOT_TOKEN}" if _BOT_TOKEN else None


def _require_config():
    if not _BOT_TOKEN:
        raise SystemExit(
            "TELEGRAM_BOT_TOKEN not set in .env — this project's own dedicated "
            "bot token (from @BotFather), not shared with any other project."
        )
    if not _CHAT_ID:
        raise SystemExit(
            "TELEGRAM_CHAT_ID not set in .env — run scripts/telegram_get_chat_id.py "
            "after adding the bot to the project's Telegram group and sending it "
            "one message."
        )


def chat_id() -> str:
    _require_config()
    return _CHAT_ID


def _post(method: str, data: dict = None, files: dict = None, timeout: int = 30) -> dict:
    _require_config()
    resp = requests.post(f"{API_BASE}/{method}", data=data, files=files, timeout=timeout)
    if not resp.ok:
        raise SystemExit(f"Telegram {method} failed: HTTP {resp.status_code} — {resp.text[:500]}")
    body = resp.json()
    if not body.get("ok"):
        raise SystemExit(f"Telegram {method} returned ok=false — {str(body)[:500]}")
    return body["result"]


def send_message(text: str, reply_to: int = None) -> int:
    """Sends a plain text message to the configured chat. Returns message_id."""
    data = {"chat_id": chat_id(), "text": text}
    if reply_to:
        data["reply_to_message_id"] = reply_to
    return _post("sendMessage", data=data)["message_id"]


def send_photo(path, caption: str = None, reply_to: int = None) -> int:
    """Sends a local image file as a photo, with an optional caption. Returns message_id."""
    data = {"chat_id": chat_id()}
    if caption:
        data["caption"] = caption
    if reply_to:
        data["reply_to_message_id"] = reply_to
    with open(path, "rb") as f:
        return _post("sendPhoto", data=data, files={"photo": f}, timeout=60)["message_id"]


def send_video(path, caption: str = None, reply_to: int = None) -> int:
    """Sends a local video file, with an optional caption. Returns message_id."""
    data = {"chat_id": chat_id()}
    if caption:
        data["caption"] = caption
    if reply_to:
        data["reply_to_message_id"] = reply_to
    with open(path, "rb") as f:
        return _post("sendVideo", data=data, files={"video": f}, timeout=120)["message_id"]


def get_updates(offset: int = None, timeout: int = 0) -> list:
    """Short poll for new updates since `offset` (exclusive of anything before
    it — pass last_update_id + 1). Returns the raw list of update dicts."""
    _require_config()
    params = {"timeout": timeout}
    if offset is not None:
        params["offset"] = offset
    resp = requests.get(f"{API_BASE}/getUpdates", params=params, timeout=timeout + 15)
    if not resp.ok:
        raise SystemExit(f"Telegram getUpdates failed: HTTP {resp.status_code} — {resp.text[:500]}")
    body = resp.json()
    if not body.get("ok"):
        raise SystemExit(f"Telegram getUpdates returned ok=false — {str(body)[:500]}")
    return body["result"]


def get_webhook_info() -> dict:
    """Returns Telegram's own view of pending/webhook state for this bot —
    added 2026-09-03 as a diagnostic for messages that vanish before
    get_updates() ever sees them (webhook briefly set elsewhere would push
    updates out-of-band and clear them from the getUpdates backlog)."""
    _require_config()
    resp = requests.get(f"{API_BASE}/getWebhookInfo", timeout=15)
    if not resp.ok:
        raise SystemExit(f"Telegram getWebhookInfo failed: HTTP {resp.status_code} — {resp.text[:500]}")
    body = resp.json()
    if not body.get("ok"):
        raise SystemExit(f"Telegram getWebhookInfo returned ok=false — {str(body)[:500]}")
    return body["result"]
