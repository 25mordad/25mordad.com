#!/usr/bin/env python3
"""Cron-invoked Telegram poller/dispatcher for the photo pipeline — the one
and only getUpdates consumer for this project's dedicated bot (see
CLAUDE.md's Personal Photo Series > Automated routine section). Meant to run
every few minutes via cron, wrapped in `flock -n` so an overlapping tick
(e.g. a slow claude -p run still in flight) is skipped rather than firing
twice.

Each run:
1. Fetches new Telegram updates since the last processed offset.
2. Every message in the configured group gets processed — no keyword
   required (2026-08-26, Bahman's explicit ask):
   - A reply to a message this pipeline sent (looked up in
     images/ig-queue/_telegram_sent.json) becomes a handoff file in
     images/ig-queue/_inbox/<message_id>.json with the resolved
     asset_id/stage.
   - A plain message reading "عکس‌بشنو"/"photobeshno" is a dedicated fast
     path — no handoff file needed, the skill just reads current state.
   - Anything else (a reply to an untracked message, or any other plain
     message) still gets a handoff file, just with asset_id/stage left
     null — the /photo-beshno skill's existing stale-handoff rule already
     knows how to investigate and answer a genuine question, or silently
     drop a no-op.
3. Regardless of Telegram traffic this tick: scans logs/error_log.json for
   unhandled severity="auto-retry" entries and retries them via
   retry_story_publish.py (this replaces what the sibling repo's hourly
   watchdog used to do for the client-timeout-but-actually-published race in
   the Instagram Story publish path).
4. If a handoff file was written or the keyword trigger fired, launches
   `claude -p "/photo-beshno"` synchronously (never backgrounded — matches
   the skill's own "Never do" rule) so the reply/message is acted on.

Usage:
    scripts/.venv/bin/python scripts/telegram_receive.py
"""

import json
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_common import get_updates, chat_id  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"
INBOX_DIR = QUEUE_DIR / "_inbox"
SENT_MAP_FILE = QUEUE_DIR / "_telegram_sent.json"
OFFSET_FILE = REPO_ROOT / "logs" / "telegram_offset.json"
ERROR_LOG_FILE = REPO_ROOT / "logs" / "error_log.json"

KEYWORD_TRIGGERS = {"عکس‌بشنو", "عکس بشنو", "photobeshno"}


def _load_json(path: Path, default):
    if not path.exists():
        return default
    try:
        return json.loads(path.read_text())
    except Exception:
        return default


def _load_offset() -> int:
    return _load_json(OFFSET_FILE, {}).get("last_update_id", 0)


def _save_offset(update_id: int) -> None:
    OFFSET_FILE.parent.mkdir(parents=True, exist_ok=True)
    OFFSET_FILE.write_text(json.dumps({"last_update_id": update_id}, indent=2))


def _write_handoff(message_id: int, asset_id, stage, text: str) -> None:
    INBOX_DIR.mkdir(parents=True, exist_ok=True)
    handoff = {
        "message_id": message_id,
        "asset_id": asset_id,
        "stage": stage,
        "reply_text": text,
        "received_at": datetime.now(timezone.utc).isoformat(),
    }
    (INBOX_DIR / f"{message_id}.json").write_text(json.dumps(handoff, ensure_ascii=False, indent=2))


def _handle_updates() -> bool:
    """Returns True if a handoff file was written or the keyword trigger fired."""
    offset = _load_offset()
    updates = get_updates(offset=offset + 1 if offset else None)
    if not updates:
        return False

    sent_map = _load_json(SENT_MAP_FILE, {})
    target_chat = str(chat_id())
    triggered = False
    max_update_id = offset

    for update in updates:
        max_update_id = max(max_update_id, update["update_id"])
        message = update.get("message")
        if not message or str(message["chat"]["id"]) != target_chat:
            continue

        text = (message.get("text") or message.get("caption") or "").strip()
        reply_to = message.get("reply_to_message")
        message_id = message["message_id"]

        tracked = sent_map.get(str(reply_to["message_id"])) if reply_to else None
        if tracked:
            # Reply to a message this pipeline sent — resolves precisely to
            # the asset_id/stage it belongs to.
            _write_handoff(message_id, tracked.get("asset_id"), tracked.get("stage"), text)
            triggered = True
        elif text.lower() in KEYWORD_TRIGGERS and not reply_to:
            # Dedicated fast path: no handoff needed, the skill just reads
            # current state (still supported, but no longer required — see
            # the branch below).
            triggered = True
        else:
            # Anything else in the group — a reply to an untracked message,
            # or any plain message — still gets processed (2026-08-26,
            # Bahman's explicit ask: no keyword required, everything in this
            # group should reach the pipeline). asset_id/stage are left null
            # since we can't resolve them; the skill's existing stale-handoff
            # rule already handles this (answers a genuine question/comment
            # via --reply-to, silently drops a no-op).
            _write_handoff(message_id, None, None, text)
            triggered = True

    _save_offset(max_update_id + 1)
    return triggered


def _retry_pending_errors() -> None:
    entries = _load_json(ERROR_LOG_FILE, [])
    if not entries:
        return
    changed = False
    for entry in entries:
        if entry.get("severity") != "auto-retry" or entry.get("retried_at"):
            continue
        asset_id = (entry.get("context") or {}).get("asset_id")
        if not asset_id:
            continue
        result = subprocess.run(
            [sys.executable, str(REPO_ROOT / "scripts" / "retry_story_publish.py"), asset_id],
            capture_output=True, text=True, timeout=120,
        )
        entry["retried_at"] = datetime.now(timezone.utc).isoformat()
        entry["retry_exit_code"] = result.returncode
        print(result.stdout.strip())
        if result.returncode != 0:
            print(result.stderr.strip(), file=sys.stderr)
        changed = True
    if changed:
        ERROR_LOG_FILE.write_text(json.dumps(entries, ensure_ascii=False, indent=2))


def main() -> None:
    triggered = _handle_updates()
    _retry_pending_errors()

    if not triggered:
        return

    print("dispatching /photo-beshno")
    result = subprocess.run(["claude", "-p", "/photo-beshno"], cwd=REPO_ROOT, text=True)
    if result.returncode != 0:
        print(f"claude -p exited {result.returncode}", file=sys.stderr)


if __name__ == "__main__":
    main()
