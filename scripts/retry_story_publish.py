#!/usr/bin/env python3
"""Retry publishing a single already-posted photo's Story, for the one
asset_id that failed. Targeted counterpart to publish_feed_photo()'s
best-effort story attempt in lr_common.py — that one only fires once, right
after the feed post; this is what the hourly check_pipeline_errors.py cron
(in the sibling yaroo repo) calls to retry it later without re-running the
whole schedule check (the record's pipeline_state is already "posted" by
then, so lr_check_schedule.py's own due_records() would never look at it
again).

Exit 0 + clears story_publish_error on success, exit 1 (record untouched
beyond a fresh error message) on failure — the caller decides whether to
retry again next time or escalate.

Usage:
    scripts/.venv/bin/python scripts/retry_story_publish.py <asset_id>
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import publish_story_for_asset  # noqa: E402
from telegram_send import send as telegram_alert  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"


def main() -> None:
    if len(sys.argv) != 2:
        raise SystemExit("Usage: retry_story_publish.py <asset_id>")
    asset_id = sys.argv[1]

    record_path = QUEUE_DIR / f"{asset_id}.json"
    if not record_path.exists():
        print(f"No record for {asset_id} at {record_path}", file=sys.stderr)
        sys.exit(1)
    record = json.loads(record_path.read_text())

    try:
        story_media_id = publish_story_for_asset(asset_id)
    except SystemExit as e:
        detail = str(e)
        print(f"❌ {asset_id}: story retry failed — {detail}", file=sys.stderr)
        record["story_publish_error"] = detail
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        sys.exit(1)

    if not story_media_id:
        print(f"{asset_id}: no story asset exists — nothing to retry", file=sys.stderr)
        sys.exit(1)

    record["story_media_id"] = story_media_id
    record["story_posted_at"] = datetime.now(timezone.utc).isoformat()
    record["story_publish_error"] = ""
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    print(f"✅ {asset_id}: story published on retry (media_id={story_media_id})")
    try:
        telegram_alert(f"✅ استوری عکس «{record.get('title')}» هم منتشر شد (تلاش دوباره موفق بود).",
                        stage="schedule_alert")
    except Exception as e:
        print(f"   (alert failed: {e})", file=sys.stderr)


if __name__ == "__main__":
    main()
