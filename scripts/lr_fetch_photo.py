#!/usr/bin/env python3
"""Fetch new photos from the Lightroom "instagram" album into images/ig-queue/.

For each asset in the album not already present locally: downloads the 2048px
rendition, scans it for accidentally-embedded local file paths (safety check,
not just an assumption), and writes an image + a JSON status record.

Usage:
    scripts/.venv/bin/python scripts/lr_fetch_photo.py
"""

import datetime
import json
import re
import sys
from pathlib import Path

import requests

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import get_access_token, lr_get, LR_API_BASE  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
ALBUM_NAME = "instagram"
# 1280 keeps well above Instagram's ~1080px recommended minimum while being
# far lighter than 2048 (~300KB vs ~1.1MB) — IG's feed only displays up to
# ~1440px anyway, so the larger rendition bought no visible quality.
RENDITION_SIZE = "1280"
# Active series — everything fetched belongs to this series until the user
# says otherwise and this constant gets updated for the next one.
SERIES_NAME = "دنیا بزرگتر از اونه که ما تصور می‌کنیم"
OUTPUT_DIR = REPO_ROOT / "images" / "ig-queue"

# Local-path patterns that must never end up in a committed file — these would
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


def main():
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
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

    new_count = 0
    for entry in assets.get("resources", []):
        asset = entry.get("asset", {})
        asset_id = asset.get("id")
        if not asset_id:
            continue

        image_path = OUTPUT_DIR / f"{asset_id}.jpg"
        record_path = OUTPUT_DIR / f"{asset_id}.json"
        if image_path.exists() and record_path.exists():
            continue  # already fetched — skip logic, same convention as the other gen_*.py scripts

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

        scan_for_leaks(resp.content, str(image_path))
        image_path.write_bytes(resp.content)

        payload = asset.get("payload", {})
        record = {
            "asset_id": asset_id,
            "image": image_path.name,
            "capture_date": payload.get("captureDate"),
            "fetched_at": datetime.datetime.now(datetime.timezone.utc).isoformat(),
            "status": "draft",
            "series": SERIES_NAME,
            "title": None,
            "caption": None,
        }
        # Deliberately not including payload.importSource here — see TASKS.md
        # P1.9 privacy note: it carries the on-device file path.
        record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")

        print(f"Fetched {asset_id} -> {image_path.relative_to(REPO_ROOT)}")
        new_count += 1

    if new_count == 0:
        print("No new photos — everything in the album is already fetched.")
    else:
        print(f"{new_count} new photo(s) fetched into {OUTPUT_DIR.relative_to(REPO_ROOT)}/")


if __name__ == "__main__":
    main()
