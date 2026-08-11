#!/usr/bin/env python3
"""Send a photo-pipeline message via a sibling private automation repo's
Telegram bot/chat.

This repo deliberately does NOT run its own Telegram getUpdates consumer —
two independent long-poll consumers on the same bot token steal each other's
updates (confirmed a real bug in that sibling repo's own remote-trigger
handler, 2026-08-11). So sending is done by shelling out to that repo's own,
already-safe notify_telegram.py (cwd=that repo, which loads its own .env —
no Telegram secrets, and no other repo's local filesystem path or name, are
hardcoded or duplicated into this public repo; its location comes from the
`TELEGRAM_BRIDGE_DIR` env var in this repo's own gitignored .env). Every send
is tagged with `--record-context {"type": "photo_pipeline", ...}` so a later
reply resolves back to this pipeline via that repo's own
inbox/telegram_action_map.json — see its handle_photo_pipeline_trigger.py,
the receiving half of this bridge (documented in CLAUDE.md's Personal Photo
Series section, without naming the other repo or its path — this repo is
public).

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
import os
import subprocess
import sys
import tempfile
from pathlib import Path
from typing import Optional

from dotenv import load_dotenv

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

_bridge_dir = os.environ.get("TELEGRAM_BRIDGE_DIR")
if not _bridge_dir:
    raise SystemExit(
        "TELEGRAM_BRIDGE_DIR not set in .env — should point to the sibling "
        "automation repo whose Telegram bot/chat this pipeline sends "
        "through. Not hardcoded here deliberately: this repo is public."
    )
BRIDGE_DIR = Path(_bridge_dir)


def send(message: str, asset_id: Optional[str] = None, stage: Optional[str] = None,
          image_path: Optional[str] = None) -> Optional[int]:
    """Sends `message` (optionally with an attached image) via the bridge
    repo's notify_telegram.py, tagged as a photo_pipeline message. Returns
    the sent message_id, or None on failure."""
    context = {"type": "photo_pipeline"}
    if asset_id:
        context["asset_id"] = asset_id
    if stage:
        context["stage"] = stage

    with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False) as f:
        json.dump(context, f, ensure_ascii=False)
        context_path = f.name

    try:
        if image_path:
            # Resolve to an absolute path — the subprocess below runs with
            # cwd=BRIDGE_DIR, so a path relative to this repo would otherwise
            # be looked up in the wrong directory.
            abs_image_path = str(Path(image_path).resolve())
            cmd = [sys.executable, "notify_telegram.py", "--file", abs_image_path,
                   "--caption", message, "--record-context", context_path]
        else:
            cmd = [sys.executable, "notify_telegram.py", message, "--record-context", context_path]
        result = subprocess.run(cmd, cwd=BRIDGE_DIR, capture_output=True, text=True, timeout=60)
        print(result.stdout.strip(), file=sys.stderr)
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
            return None
        # notify_telegram.py prints "sent <id>" or "failed"
        line = result.stdout.strip().splitlines()[-1] if result.stdout.strip() else ""
        if line.startswith("sent "):
            return int(line.split()[1])
        return None
    finally:
        Path(context_path).unlink(missing_ok=True)


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("message")
    parser.add_argument("--asset-id")
    parser.add_argument("--stage")
    parser.add_argument("--file", help="Path to an image to attach")
    args = parser.parse_args()

    message_id = send(args.message, args.asset_id, args.stage, args.file)
    print(f"sent {message_id}" if message_id else "failed")
    sys.exit(0 if message_id else 1)


if __name__ == "__main__":
    main()
