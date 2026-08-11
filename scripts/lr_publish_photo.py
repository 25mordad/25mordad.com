#!/usr/bin/env python3
"""Publish one approved photo from images/ig-queue/ to the @25mordad Instagram Feed.

Only ever posts a photo whose record has status "approved". Always previews
first; only actually calls the Instagram API when --confirm-publish is passed
(mirrors the reused internal publish-gate pattern: preview + explicit typed
confirmation before anything goes live).

The image must already be publicly reachable at
https://25mordad.com/images/ig-queue/<asset-id>.jpg — i.e. committed and
pushed, with Cloudflare Pages deployed — before it can be posted, since the
Instagram Graph API fetches the image itself from that URL.

Usage:
    scripts/.venv/bin/python scripts/lr_publish_photo.py [asset_id] [--confirm-publish]

    Without asset_id: picks the oldest "approved" (not yet "posted") photo.
    Without --confirm-publish: dry run — preview only, nothing is posted.
"""

import argparse
import json
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import publish_feed_photo, PUBLIC_BASE  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"


def load_record(asset_id):
    path = QUEUE_DIR / f"{asset_id}.json"
    if not path.exists():
        raise SystemExit(f"No record for {asset_id} at {path}")
    return path, json.loads(path.read_text())


def pick_oldest_approved():
    candidates = []
    for path in QUEUE_DIR.glob("*.json"):
        record = json.loads(path.read_text())
        if record.get("status") == "approved":
            candidates.append((record.get("fetched_at", ""), path, record))
    if not candidates:
        raise SystemExit("No photo with status 'approved' found in images/ig-queue/")
    candidates.sort(key=lambda c: c[0])
    _, path, record = candidates[0]
    return path, record


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id", nargs="?", default=None)
    parser.add_argument("--confirm-publish", action="store_true")
    args = parser.parse_args()

    if args.asset_id:
        record_path, record = load_record(args.asset_id)
    else:
        record_path, record = pick_oldest_approved()

    asset_id = record["asset_id"]

    if record.get("status") != "approved":
        raise SystemExit(f"Refusing to publish {asset_id}: status is {record.get('status')!r}, not 'approved'")

    image_url = f"{PUBLIC_BASE}/{asset_id}.jpg"

    head = requests.head(image_url, timeout=15)
    if not head.ok:
        raise SystemExit(
            f"Image not publicly reachable yet: HTTP {head.status_code} for {image_url}\n"
            f"Commit and push images/ig-queue/{asset_id}.jpg (+ its .json record), "
            f"wait for the Cloudflare Pages deploy, then retry."
        )

    print("=" * 60)
    print(f"Title:  {record.get('title')}")
    print(f"Series: {record.get('series')}")
    print(f"Image:  {image_url}")
    print("-" * 60)
    print(record.get("caption", ""))
    print("=" * 60)

    if not args.confirm_publish:
        print("\nDRY RUN — nothing posted. Re-run with --confirm-publish to actually post.")
        return

    media_id = publish_feed_photo(asset_id, record, record_path)
    print(f"Published: media_id={media_id}")
    print(f"Record updated: {record_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
