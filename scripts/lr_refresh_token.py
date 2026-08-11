#!/usr/bin/env python3
"""Verify the Lightroom refresh token in .env by exchanging it for a fresh access token.

Usage:
    scripts/.venv/bin/python scripts/lr_refresh_token.py
"""

from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)

CLIENT_ID = os.environ.get("LR_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LR_CLIENT_SECRET")
REFRESH_TOKEN = os.environ.get("LR_REFRESH_TOKEN")

if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit("LR_CLIENT_ID / LR_CLIENT_SECRET not found in .env")
if not REFRESH_TOKEN:
    raise SystemExit("LR_REFRESH_TOKEN not found in .env — run scripts/lr_auth.py first")

SCOPES = "openid,AdobeID,lr_partner_apis,lr_partner_rendition_apis,offline_access"

resp = requests.post(
    "https://ims-na1.adobelogin.com/ims/token/v1",
    files={
        "client_id": (None, CLIENT_ID),
        "client_secret": (None, CLIENT_SECRET),
        "scope": (None, SCOPES),
        "grant_type": (None, "refresh_token"),
        "refresh_token": (None, REFRESH_TOKEN),
    },
    timeout=15,
)
if not resp.ok:
    raise SystemExit(f"Refresh failed: HTTP {resp.status_code} — {resp.json()}")

data = resp.json()
print(f"Token refresh OK — access_token received, expires_in={data.get('expires_in', 'unknown')}s")

if data.get("refresh_token") and data["refresh_token"] != REFRESH_TOKEN:
    set_key(str(ENV_PATH), "LR_REFRESH_TOKEN", data["refresh_token"])
    print("IMS rotated the refresh_token — .env updated")
