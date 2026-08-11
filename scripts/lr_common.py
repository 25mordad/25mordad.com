"""Shared helpers for Lightroom API scripts — token refresh, authenticated GET
requests, and the Instagram Feed publish sequence (container -> poll -> publish)
shared between the manual (lr_publish_photo.py) and scheduled
(lr_check_schedule.py) publishers."""

import datetime
import json
import time
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

PUBLIC_BASE = "https://25mordad.com/images/ig-queue"


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


def publish_feed_photo(asset_id: str, record: dict, record_path: Path) -> str:
    """Publish one photo to the @25mordad Instagram Feed: HEAD-check public
    reachability, then container -> poll status_code -> media_publish. Updates
    and writes `record`/`record_path` on success (status, posted_at, media_id).
    Returns the media_id. Raises SystemExit with a clear message on any
    failure — callers (lr_publish_photo.py for a manual run, lr_check_schedule.py
    for the cron) are expected to let that propagate or catch it themselves."""
    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        raise SystemExit("IG_ACCESS_TOKEN not found in .env")

    caption = record.get("caption")
    if not caption:
        raise SystemExit(f"Refusing to publish {asset_id}: record has no caption")

    image_url = f"{PUBLIC_BASE}/{asset_id}.jpg"
    head = requests.head(image_url, timeout=15)
    if not head.ok:
        raise SystemExit(
            f"Image not publicly reachable yet: HTTP {head.status_code} for {image_url}\n"
            f"Commit and push images/ig-queue/{asset_id}.jpg (+ its .json record), "
            f"wait for the Cloudflare Pages deploy, then retry."
        )

    me = requests.get(
        "https://graph.instagram.com/me",
        params={"fields": "id,username", "access_token": token},
        timeout=10,
    )
    if not me.ok:
        raise SystemExit(f"Failed to fetch profile: HTTP {me.status_code} — {me.json()}")
    ig_user_id = me.json()["id"]

    create = requests.post(
        f"https://graph.instagram.com/{ig_user_id}/media",
        data={"image_url": image_url, "caption": caption, "access_token": token},
        timeout=15,
    )
    if not create.ok:
        raise SystemExit(f"Failed to create container: HTTP {create.status_code} — {create.json()}")
    container_id = create.json()["id"]

    for _ in range(10):
        status = requests.get(
            f"https://graph.instagram.com/{container_id}",
            params={"fields": "status_code", "access_token": token},
            timeout=10,
        )
        if not status.ok:
            raise SystemExit(f"Failed to poll container status: HTTP {status.status_code} — {status.json()}")
        code = status.json().get("status_code")
        if code == "FINISHED":
            break
        if code == "ERROR":
            raise SystemExit("Container processing failed")
        time.sleep(2)
    else:
        raise SystemExit("Container did not finish processing in time")

    publish = requests.post(
        f"https://graph.instagram.com/{ig_user_id}/media_publish",
        data={"creation_id": container_id, "access_token": token},
        timeout=15,
    )
    if not publish.ok:
        raise SystemExit(f"Failed to publish: HTTP {publish.status_code} — {publish.json()}")

    media_id = publish.json().get("id")
    record["status"] = "posted"
    record["posted_at"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    record["media_id"] = media_id
    record_path.write_text(json.dumps(record, ensure_ascii=False, indent=2) + "\n")
    return media_id
