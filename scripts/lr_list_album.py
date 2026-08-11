#!/usr/bin/env python3
"""List assets in a named Lightroom album — verifies OAuth + album access.

Usage:
    scripts/.venv/bin/python scripts/lr_list_album.py "<album name>"
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import get_access_token, lr_get  # noqa: E402

if len(sys.argv) != 2:
    raise SystemExit("Usage: lr_list_album.py <album name>")

ALBUM_NAME = sys.argv[1]

client_id, access_token = get_access_token()

account = lr_get(client_id, access_token, "account")
print(f"Authenticated as: {account.get('full_name') or account.get('email') or account.get('id')}")

catalog = lr_get(client_id, access_token, "catalog")
catalog_id = catalog["id"]

albums = lr_get(client_id, access_token, f"catalogs/{catalog_id}/albums")
resources = albums.get("resources", [])
matches = [a for a in resources if a.get("payload", {}).get("name") == ALBUM_NAME]

if not matches:
    seen = [a.get("payload", {}).get("name") for a in resources]
    print(f"No album named {ALBUM_NAME!r} found. Albums visible to this account: {seen}")
    print("Raw album list (for debugging field names):")
    print(albums)
    raise SystemExit(1)

album = matches[0]
album_id = album["id"]
print(f"Found album {ALBUM_NAME!r} (id={album_id})")

assets = lr_get(
    client_id, access_token,
    f"catalogs/{catalog_id}/albums/{album_id}/assets",
    params={"embed": "asset"},
)
asset_resources = assets.get("resources", [])
print(f"{len(asset_resources)} asset(s) in album:")
for a in asset_resources:
    asset = a.get("asset", {})
    payload = asset.get("payload", {})
    import_source = payload.get("importSource", {})
    filename = import_source.get("fileName", "?")
    captured = payload.get("captureDate", "?")
    print(f"  - {asset.get('id')}  {filename}  captured={captured}")

if not asset_resources:
    print("(no assets — but album access itself works)")
    print("Raw response (for debugging field names):")
    print(assets)
