#!/usr/bin/env python3
"""Publish a single Instagram Story from a public image or video URL.

Auto-detects image vs video from the URL's extension (.mp4/.mov -> video_url,
everything else -> image_url). Thin CLI wrapper around lr_common.py's
publish_story_from_url() — the same helper lr_check_schedule.py and
lr_publish_photo.py now call automatically (via publish_feed_photo(), added
2026-08-12 per Bahman's ask that every feed post always brings its Story
along). This script is for ad-hoc/manual publishing of an arbitrary URL —
e.g. testing before an asset is committed to this repo.

Usage:
    scripts/.venv/bin/python scripts/publish_story.py <image_or_video_url>
"""

import sys
from pathlib import Path

from dotenv import load_dotenv
import os

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import publish_story_from_url  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

TOKEN = os.environ.get("IG_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("IG_ACCESS_TOKEN not found in .env")

if len(sys.argv) != 2:
    raise SystemExit("Usage: publish_story.py <image_or_video_url>")

MEDIA_URL = sys.argv[1]
media_id = publish_story_from_url(TOKEN, MEDIA_URL)
print("Published:", media_id)
