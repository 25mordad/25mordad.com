#!/usr/bin/env python3
"""check_schedule.py — Publish any photo whose scheduled time has arrived.

Zero LLM tokens — deterministic, mirrors kavosh/dariche's
scripts/check_schedule.py pattern. Meant to run on a cron interval (e.g.
every 15 min, matching that project's own interval).

A photo is published when, and only when, ALL of these hold:
  1. `pipeline_state: "scheduled"` — only /photo-beshno writes this, and only
     after an explicit schedule confirmation arrived in Telegram
  2. `status: "approved"` — the gate lr_publish_photo.py / publish_feed_photo()
     already enforces
  3. `scheduled_for` is in the past
  4. the final image actually exists on disk at images/ig-queue/<asset_id>.jpg

Condition 1 carries the consent — the Telegram confirmation *is* the
authorization, given earlier rather than skipped, which is why this may run
unattended. Condition 4 is checked here rather than left to the publisher
because a missing asset must be an alert, never a silent skip.

MAX_ATTEMPTS immediate retries happen within the same tick (changed 2026-09-08:
with the cron now running once daily instead of hourly, spreading retries
across ticks meant a bad day could wait 24h before trying again). A failed
attempt retries right away, in-process; only once MAX_ATTEMPTS is exhausted
does it give up, leave `pipeline_state: "scheduled"` untouched, and send a
Telegram alert explaining what failed and why a human is needed.

Usage:
    scripts/.venv/bin/python scripts/lr_check_schedule.py
    scripts/.venv/bin/python scripts/lr_check_schedule.py --dry-run
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import publish_feed_photo  # noqa: E402
from telegram_send import send as telegram_alert  # noqa: E402
from report_error import log_error  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"
MAX_ATTEMPTS = 2


def due_records():
    now = datetime.now()
    for record_path in sorted(QUEUE_DIR.glob("*.json")):
        record = json.loads(record_path.read_text())
        asset_id = record.get("asset_id", record_path.stem)

        if record.get("pipeline_state") != "scheduled":
            continue
        if record.get("status") != "approved":
            yield record_path, record, asset_id, f"pipeline_state is scheduled but status is {record.get('status')!r}"
            continue
        when = (record.get("scheduled_for") or "").strip()
        if not when:
            yield record_path, record, asset_id, "pipeline_state is scheduled but scheduled_for is empty"
            continue
        try:
            slot = datetime.fromisoformat(when)
        except ValueError:
            yield record_path, record, asset_id, f"scheduled_for is not a valid date: {when!r}"
            continue
        if slot.tzinfo is not None:
            slot = slot.astimezone().replace(tzinfo=None)
        if slot <= now:
            yield record_path, record, asset_id, None


def alert(text: str) -> None:
    try:
        telegram_alert(text, stage="schedule_alert")
    except Exception as e:
        print(f"   (alert failed: {e})", file=sys.stderr)


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="report only, publish nothing")
    args = ap.parse_args()

    published = failed = 0
    for record_path, record, asset_id, problem in due_records():
        if problem:
            print(f"❌ {asset_id}: {problem}")
            failed += 1
            if not args.dry_run and not record.get("publish_error"):
                record["publish_error"] = problem
                record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
                alert(f"⚠️ عکس {asset_id}\n\nزمان انتشارش رسیده ولی نمی‌شود منتشرش کرد:\n{problem}")
                log_error("lr_check_schedule.py:record_problem", "needs-diagnosis",
                          f"{asset_id}: {problem}", context={"asset_id": asset_id})
            continue

        image_path = QUEUE_DIR / f"{asset_id}.jpg"
        if not image_path.exists():
            msg = f"scheduled but no final image on disk at {image_path.name}"
            print(f"❌ {asset_id}: {msg}")
            failed += 1
            if not args.dry_run and not record.get("publish_error"):
                record["publish_error"] = msg
                record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
                alert(f"⚠️ عکس {asset_id}\n\nزمان انتشارش رسیده ولی فایلش روی دیسک نیست.")
                log_error("lr_check_schedule.py:record_problem", "needs-diagnosis",
                          f"{asset_id}: {msg}", context={"asset_id": asset_id})
            continue

        attempts = int(record.get("publish_attempts", 0) or 0)
        if attempts >= MAX_ATTEMPTS:
            print(f"⏭  {asset_id}: {attempts} failed attempts — giving up, needs a human")
            continue

        print(f"▶  {asset_id}: due, publishing")
        if args.dry_run:
            continue

        # Retry immediately, in-process, up to MAX_ATTEMPTS — the cron now
        # runs only once a day, so waiting for "the next tick" would mean a
        # bad day isn't retried until 24h later.
        media_id = None
        detail = None
        while attempts < MAX_ATTEMPTS:
            attempts += 1
            record["publish_attempts"] = attempts
            record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
            try:
                media_id = publish_feed_photo(asset_id, record, record_path)
                detail = None
                break
            except Exception as e:
                # Was `except SystemExit` only — see lr_common.py's matching fix
                # (2026-08-25): a raw exception here can otherwise skip the
                # publish_attempts write and risk a duplicate feed publish on
                # a later attempt.
                detail = str(e)
                print(f"❌ {asset_id}: attempt {attempts}/{MAX_ATTEMPTS} failed — {detail}")

        if media_id is None:
            if not record.get("publish_error"):
                record["publish_error"] = detail
                record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
            alert(f"⚠️ عکس {asset_id} («{record.get('title')}»)\n\n"
                  f"بعد از {MAX_ATTEMPTS} تلاش پشت‌سرهم منتشر نشد:\n{detail}\n\n"
                  f"دیگر تلاش خودکاری نمی‌شود — نیاز به بررسی دستی است.")
            log_error("lr_check_schedule.py:publish_error", "needs-diagnosis",
                      f"{asset_id}: feed publish failed after {MAX_ATTEMPTS} immediate attempts — {detail}",
                      context={"asset_id": asset_id})
            failed += 1
            continue

        # publish_feed_photo() already set status/posted_at/media_id and wrote
        # the record — this only moves the pipeline state and clears any
        # stale failure flags.
        record["pipeline_state"] = "posted"
        record["publish_error"] = ""
        record["publish_attempts"] = 0
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
        print(f"✅ {asset_id}: published (media_id={media_id})")
        if record.get("story_media_id"):
            print(f"   story also published (media_id={record['story_media_id']})")
            alert(f"✅ عکس «{record.get('title')}» منتشر شد، استوریش هم همراهش رفت.")
        elif record.get("story_publish_error"):
            alert(
                f"✅ عکس «{record.get('title')}» منتشر شد.\n\n"
                f"⚠️ ولی استوریش منتشر نشد:\n{record['story_publish_error']}"
            )
            # Known-safe recovery exists (just retry publish_story_for_asset
            # for this asset_id) — the hourly cron can do this itself without
            # an LLM call, no need to wait for a full diagnosis run.
            log_error("lr_check_schedule.py:story_publish_error", "auto-retry",
                      f"{asset_id}: story publish failed — {record['story_publish_error']}",
                      context={"asset_id": asset_id})
        else:
            alert(f"✅ عکس «{record.get('title')}» منتشر شد.")
        published += 1

    if published or failed:
        print(f"\n{published} published, {failed} failed")
    else:
        print("nothing due")


if __name__ == "__main__":
    main()
