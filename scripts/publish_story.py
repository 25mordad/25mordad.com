#!/usr/bin/env python3
"""Publish a single Instagram Story from a public image URL.

Usage:
    scripts/.venv/bin/python scripts/publish_story.py <image_url>
"""

import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

TOKEN = os.environ.get("IG_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("IG_ACCESS_TOKEN not found in .env")

if len(sys.argv) != 2:
    raise SystemExit("Usage: publish_story.py <image_url>")

IMAGE_URL = sys.argv[1]

# Step 1: get the IG user id
me = requests.get(
    "https://graph.instagram.com/me",
    params={"fields": "id,username", "access_token": TOKEN},
    timeout=10,
)
if not me.ok:
    raise SystemExit(f"Failed to fetch profile: HTTP {me.status_code} — {me.json()}")
ig_user_id = me.json()["id"]
print(f"Publishing to @{me.json()['username']} (id={ig_user_id})")

# Step 2: create a media container
create = requests.post(
    f"https://graph.instagram.com/{ig_user_id}/media",
    data={
        "image_url": IMAGE_URL,
        "media_type": "STORIES",
        "access_token": TOKEN,
    },
    timeout=15,
)
if not create.ok:
    raise SystemExit(f"Failed to create container: HTTP {create.status_code} — {create.json()}")
container_id = create.json()["id"]
print(f"Container created: {container_id}")

# Step 3: poll container status until FINISHED
for attempt in range(10):
    status = requests.get(
        f"https://graph.instagram.com/{container_id}",
        params={"fields": "status_code", "access_token": TOKEN},
        timeout=10,
    )
    if not status.ok:
        raise SystemExit(f"Failed to poll container status: HTTP {status.status_code} — {status.json()}")
    code = status.json().get("status_code")
    print(f"  status: {code}")
    if code == "FINISHED":
        break
    if code == "ERROR":
        raise SystemExit("Container processing failed")
    time.sleep(2)
else:
    raise SystemExit("Container did not finish processing in time")

# Step 4: publish the container
publish = requests.post(
    f"https://graph.instagram.com/{ig_user_id}/media_publish",
    data={
        "creation_id": container_id,
        "access_token": TOKEN,
    },
    timeout=15,
)
if not publish.ok:
    raise SystemExit(f"Failed to publish: HTTP {publish.status_code} — {publish.json()}")
print("Published:", publish.json())
