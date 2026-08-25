#!/usr/bin/env python3
"""Send a photo-pipeline message via this project's own dedicated Telegram
bot/group (see CLAUDE.md's Personal Photo Series > Automated routine section).

This repo now runs its own getUpdates consumer (scripts/telegram_receive.py,
invoked by cron every few minutes) — safe because this bot token is used by
nothing else. Sending happens directly against the Telegram Bot API via
telegram_common.py, no cross-repo shelling out.

Every tagged send (asset_id/stage given) is recorded in
images/ig-queue/_telegram_sent.json (gitignored, transient) so
telegram_receive.py can resolve an incoming reply back to the asset_id/stage
it belongs to.

Usage (as a library, from the /photo-beshno skill or other scripts):
    from telegram_send import send
    send("caption text", asset_id="...", stage="awaiting_title")
    send("caption text", asset_id="...", stage="awaiting_title", image_path="images/ig-queue/<id>.jpg")

Usage (CLI, mainly for connectivity testing):
    scripts/.venv/bin/python scripts/telegram_send.py "test message"
    scripts/.venv/bin/python scripts/telegram_send.py "caption" --asset-id <id> --stage awaiting_title --file images/ig-queue/<id>.jpg
"""

import argparse
import json
import sys
from pathlib import Path
from typing import Optional

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_common import send_message, send_photo, send_video  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
SENT_MAP_FILE = REPO_ROOT / "images" / "ig-queue" / "_telegram_sent.json"


def _record_sent(message_id: int, asset_id: str, stage: str) -> None:
    entries = {}
    if SENT_MAP_FILE.exists():
        try:
            entries = json.loads(SENT_MAP_FILE.read_text())
        except Exception:
            entries = {}
    entries[str(message_id)] = {"asset_id": asset_id, "stage": stage}
    SENT_MAP_FILE.parent.mkdir(parents=True, exist_ok=True)
    SENT_MAP_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


def send(message: str, asset_id: Optional[str] = None, stage: Optional[str] = None,
          image_path: Optional[str] = None, reply_to: Optional[int] = None) -> Optional[int]:
    """Sends `message` (optionally with an attached image/video) to this
    project's Telegram group. Returns the sent message_id, or None on
    failure. `reply_to` threads the send to a specific past message_id."""
    try:
        if image_path:
            path = Path(image_path)
            is_video = path.suffix.lower() in (".mp4", ".mov")
            message_id = (send_video if is_video else send_photo)(path, caption=message, reply_to=reply_to)
        else:
            message_id = send_message(message, reply_to=reply_to)
    except SystemExit as e:
        print(str(e), file=sys.stderr)
        return None

    if asset_id or stage:
        _record_sent(message_id, asset_id, stage)
    return message_id


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--asset-id")
    parser.add_argument("--stage")
    parser.add_argument("--file", help="Path to an image or video to attach")
    parser.add_argument("--reply-to", type=int, help="message_id to thread this reply to")
    args = parser.parse_args()

    message_id = send(args.message, args.asset_id, args.stage, args.file, args.reply_to)
    print(f"sent {message_id}" if message_id else "failed")
    sys.exit(0 if message_id else 1)


if __name__ == "__main__":
    main()
