"""Shared helpers for Lightroom API scripts — token refresh + authenticated GET requests."""

import json
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)

IMS_HOST = "https://ims-na1.adobelogin.com"
LR_API_BASE = "https://lr.adobe.io/v2/"
SCOPES = "openid,AdobeID,lr_partner_apis,lr_partner_rendition_apis,offline_access"


def get_access_token():
    """Exchange the stored refresh token for a fresh access token.

    Returns (client_id, access_token). Rotates LR_REFRESH_TOKEN in .env if
    Adobe issues a new one on this call.
    """
    client_id = os.environ.get("LR_CLIENT_ID")
    client_secret = os.environ.get("LR_CLIENT_SECRET")
    refresh_token = os.environ.get("LR_REFRESH_TOKEN")
    if not client_id or not client_secret:
        raise SystemExit("LR_CLIENT_ID / LR_CLIENT_SECRET not found in .env")
    if not refresh_token:
        raise SystemExit("LR_REFRESH_TOKEN not found in .env — run scripts/lr_auth.py first")

    resp = requests.post(
        f"{IMS_HOST}/ims/token/v1",
        files={
            "client_id": (None, client_id),
            "client_secret": (None, client_secret),
            "scope": (None, SCOPES),
            "grant_type": (None, "refresh_token"),
            "refresh_token": (None, refresh_token),
        },
        timeout=15,
    )
    if not resp.ok:
        raise SystemExit(f"Token refresh failed: HTTP {resp.status_code} — {resp.json()}")

    data = resp.json()
    if data.get("refresh_token") and data["refresh_token"] != refresh_token:
        set_key(str(ENV_PATH), "LR_REFRESH_TOKEN", data["refresh_token"])

    return client_id, data["access_token"]


def lr_get(client_id, access_token, path, params=None):
    """GET a Lightroom API path (relative to LR_API_BASE) and return parsed JSON.

    Adobe prefixes every response body with `while (1) {}` as XSSI protection —
    strip it before parsing.
    """
    resp = requests.get(
        LR_API_BASE + path,
        headers={
            "X-API-Key": client_id,
            "Authorization": f"Bearer {access_token}",
        },
        params=params,
        timeout=15,
    )
    if not resp.ok:
        raise SystemExit(f"Lightroom API GET {path} failed: HTTP {resp.status_code} — {resp.text[:500]}")
    text = resp.text
    if text.startswith("while (1) {}"):
        text = text[len("while (1) {}"):]
    return json.loads(text) if text.strip() else {}
