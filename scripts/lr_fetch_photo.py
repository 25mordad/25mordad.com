#!/usr/bin/env python3
"""Pick ONE random not-yet-processed photo from the Lightroom "instagram" album
and fetch it at the largest rendition Adobe's API actually serves, for the
photo-pipeline's GPT quality-enhance step.

Verified live 2026-08-12: Adobe's rendition endpoint only accepts "1280" and
"2048" — "2560", "fullsize", "3072", "original" all 400/404. So "full size" in
this pipeline means 2048px, not a resize-free master; there is no original/
master download exposed via this API tier. The output goes to
images/ig-queue/_source/<asset_id>.jpg — a working file for gpt_enhance_photo.py,
never committed (see .gitignore) — NOT the final public/committed image at
images/ig-queue/<asset_id>.jpg, which gpt_enhance_photo.py produces.

The "queue of one" is primarily the caller's (the /photo-beshno skill)
responsibility — it should only call this script when no record is
currently in flight. As a backstop (added 2026-08-19 after a confirmed
incident where an unattended run bootstrapped a second photo while one was
already at `awaiting_title`), this script also refuses to fetch a new photo
itself if any existing record's `pipeline_state` is outside the terminal set
— see TERMINAL_STATES below. It also makes sure it never re-picks an asset
that already has a local record (any status).

Usage:
    scripts/.venv/bin/python scripts/lr_fetch_photo.py
    scripts/.venv/bin/python scripts/lr_fetch_photo.py <asset_id>   # fetch a specific asset instead of picking randomly
"""

import datetime
import json
import random
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import get_access_token, lr_get, LR_API_BASE  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
ALBUM_NAME = "instagram"
RENDITION_SIZE = "2048"  # the largest rendition Adobe's API serves — see module docstring
# Active series — everything fetched belongs to this series until the user
# says otherwise and this constant gets updated for the next one.
SERIES_NAME = "دنیا بزرگتر از اونه که ما تصور می‌کنیم"
QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"
SOURCE_DIR = QUEUE_DIR / "_source"

# Mirrors photo-beshno.md's own definition of "in flight" (anything outside
# this set counts as a photo currently mid-pipeline).
TERMINAL_STATES = {"scheduled", "posted", "rejected"}

# Local-path patterns that must never end up in a saved file — these would
# only appear if Adobe's rendition unexpectedly embeds Lightroom catalog
# metadata (device storage paths) into the JPEG itself.
LEAK_PATTERNS = [
    rb"/storage/[^\s\"]+",
    rb"/Users/[^\s\"]+",
    rb"/home/[^\s\"]+",
    rb"[A-Za-z]:\\\\Users[^\s\"]+",
]


def scan_for_leaks(data: bytes, label: str):
    for pattern in LEAK_PATTERNS:
        match = re.search(pattern, data)
        if match:
            raise SystemExit(
                f"REFUSING to save {label}: found a local-path-like string embedded in the "
                f"downloaded file ({match.group(0)[:40]!r}...). Investigate before proceeding."
            )


def refuse_if_already_in_flight():
    in_flight = []
    for p in QUEUE_DIR.glob("*.json"):
        try:
            record = json.loads(p.read_text())
        except (OSError, json.JSONDecodeError):
            continue
        state = record.get("pipeline_state")
        if state and state not in TERMINAL_STATES:
            in_flight.append((record.get("asset_id", p.stem), state))
    if in_flight:
        described = ", ".join(f"{asset_id} ({state})" for asset_id, state in in_flight)
        raise SystemExit(
            f"Refusing to fetch a new photo — {len(in_flight)} record(s) already in flight: "
            f"{described}. The pipeline's queue-of-one invariant requires exactly one photo in "
            "flight at a time; advance or resolve the existing record(s) first."
        )


def main():
    QUEUE_DIR.mkdir(parents=True, exist_ok=True)
    SOURCE_DIR.mkdir(parents=True, exist_ok=True)
    refuse_if_already_in_flight()
    client_id, access_token = get_access_token()

    catalog = lr_get(client_id, access_token, "catalog")
    catalog_id = catalog["id"]

    albums = lr_get(client_id, access_token, f"catalogs/{catalog_id}/albums")
    matches = [
        a for a in albums.get("resources", [])
        if a.get("payload", {}).get("name") == ALBUM_NAME
    ]
    if not matches:
        raise SystemExit(f"No album named {ALBUM_NAME!r} found")
    album_id = matches[0]["id"]

    assets = lr_get(
        client_id, access_token,
        f"catalogs/{catalog_id}/albums/{album_id}/assets",
        params={"embed": "asset"},
    )
    album_assets = {
        entry["asset"]["id"]: entry["asset"]
        for entry in assets.get("resources", [])
        if entry.get("asset", {}).get("id")
    }

    requested_id = sys.argv[1] if len(sys.argv) > 1 else None
    if requested_id:
        if requested_id not in album_assets:
            raise SystemExit(f"{requested_id!r} is not in the {ALBUM_NAME!r} album")
        asset_id = requested_id
    else:
        already_processed = {p.stem for p in QUEUE_DIR.glob("*.json")}
        unprocessed = [aid for aid in album_assets if aid not in already_processed]
        if not unprocessed:
            print("No unprocessed photos left in the album — every asset already has a local record.")
            return
        asset_id = random.choice(unprocessed)

    asset = album_assets[asset_id]
    source_path = SOURCE_DIR / f"{asset_id}.jpg"
    record_path = QUEUE_DIR / f"{asset_id}.json"

    rendition_url = (
        f"{LR_API_BASE}catalogs/{catalog_id}/assets/{asset_id}/renditions/{RENDITION_SIZE}"
    )
    resp = requests.get(
        rendition_url,
        headers={"X-API-Key": client_id, "Authorization": f"Bearer {access_token}"},
        timeout=30,
    )
    if not resp.ok:
        raise SystemExit(f"Rendition download failed for {asset_id}: HTTP {resp.status_code}")

    scan_for_leaks(resp.content, str(source_path))
    source_path.write_bytes(resp.content)

    payload = asset.get("payload", {})
    record = {
        "asset_id": asset_id,
        "image": f"{asset_id}.jpg",  # written later by gpt_enhance_photo.py
        "capture_date": payload.get("captureDate"),
        "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
        "status": "draft",
        "pipeline_state": "enhancing",
        "series": SERIES_NAME,
        "title": None,
        "story": None,
        "caption": None,
        "scheduled_for": None,
    }
    # Deliberately not including payload.importSource here — it carries the
    # on-device file path (confirmed live 2026-08-12: importSource.localAssetId
    # is literally "/storage/emulated/0/..."). See CLAUDE.md's Personal Photo
    # Series privacy constraint.
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")

    print(f"Fetched {asset_id} -> {source_path.relative_to(REPO_ROOT)}")
    print(f"Record written -> {record_path.relative_to(REPO_ROOT)}")


if __name__ == "__main__":
    main()
