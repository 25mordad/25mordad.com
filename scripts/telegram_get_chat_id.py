#!/usr/bin/env python3
"""One-off setup helper: after adding this project's dedicated bot to its
Telegram group and sending it at least one message there, run this to see
every chat this bot has received a message from — copy the right chat.id
into .env as TELEGRAM_CHAT_ID.

Usage:
    scripts/.venv/bin/python scripts/telegram_get_chat_id.py
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_common import _BOT_TOKEN  # noqa: E402

import requests  # noqa: E402


def main() -> None:
    if not _BOT_TOKEN:
        raise SystemExit("TELEGRAM_BOT_TOKEN not set in .env")

    resp = requests.get(
        f"https://api.telegram.org/bot{_BOT_TOKEN}/getUpdates",
        params={"timeout": 0},
        timeout=15,
    )
    if not resp.ok:
        raise SystemExit(f"getUpdates failed: HTTP {resp.status_code} — {resp.text[:500]}")
    body = resp.json()
    if not body.get("ok"):
        raise SystemExit(f"getUpdates returned ok=false — {str(body)[:500]}")

    updates = body["result"]
    if not updates:
        print("No updates yet — send a message in the group first, then re-run this.")
        return

    seen = {}
    for update in updates:
        message = update.get("message") or update.get("channel_post")
        if not message:
            continue
        chat = message["chat"]
        seen[chat["id"]] = chat.get("title") or chat.get("username") or chat.get("type")

    for chat_id, label in seen.items():
        print(f"chat_id={chat_id}  ({label})")
    print("\nCopy the right chat_id above into .env as TELEGRAM_CHAT_ID.")


if __name__ == "__main__":
    main()
