#!/usr/bin/env python3
"""Verify the Instagram access token in .env by calling the profile endpoint."""

from pathlib import Path

import requests
from dotenv import load_dotenv
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

TOKEN = os.environ.get("IG_ACCESS_TOKEN")
if not TOKEN:
    raise SystemExit("IG_ACCESS_TOKEN not found in .env")

resp = requests.get(
    "https://graph.instagram.com/me",
    params={
        "fields": "id,username,account_type,media_count",
        "access_token": TOKEN,
    },
    timeout=10,
)
resp.raise_for_status()
print(resp.json())
