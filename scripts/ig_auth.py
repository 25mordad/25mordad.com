#!/usr/bin/env python3
"""One-time OAuth flow to obtain a fresh long-lived Instagram access token.

Uses the "Instagram API with Instagram Login" (Business Login) flow — same
product the existing IG_ACCESS_TOKEN was originally issued under (graph.instagram.com).

Usage:
    scripts/.venv/bin/python scripts/ig_auth.py
"""

import http.server
import secrets
import threading
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)

APP_ID = os.environ.get("IG_APP_ID")
APP_SECRET = os.environ.get("IG_APP_SECRET")
if not APP_ID or not APP_SECRET:
    raise SystemExit("IG_APP_ID / IG_APP_SECRET not found in .env")

PORT = 8889
REDIRECT_URI = f"http://localhost:{PORT}/callback"
SCOPES = (
    "instagram_business_basic,"
    "instagram_business_content_publish,"
    "instagram_business_manage_comments,"
    "instagram_business_manage_messages"
)
AUTHORIZE_URL = "https://www.instagram.com/oauth/authorize"
TOKEN_URL = "https://api.instagram.com/oauth/access_token"
EXCHANGE_URL = "https://graph.instagram.com/access_token"


class CallbackHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path != "/callback":
            self.send_response(404)
            self.end_headers()
            return
        self.server.result = urllib.parse.parse_qs(parsed.query)
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(b"<html><body>Authorized \xe2\x80\x94 you can close this tab.</body></html>")
        threading.Thread(target=self.server.shutdown).start()

    def log_message(self, format, *args):
        # Default logging would print the callback query string (contains
        # the one-time authorization code) to the terminal — suppress it.
        pass


def main():
    state = secrets.token_urlsafe(24)
    auth_params = {
        "client_id": APP_ID,
        "redirect_uri": REDIRECT_URI,
        "response_type": "code",
        "scope": SCOPES,
        "state": state,
    }
    auth_url = f"{AUTHORIZE_URL}?{urllib.parse.urlencode(auth_params)}"

    server = http.server.HTTPServer(("localhost", PORT), CallbackHandler)
    server.result = None

    print("Open this URL in a browser to authorize:")
    print(auth_url)
    print()
    print("Sign in with the Instagram account that owns @25mordad and approve access.")
    print("Waiting for the redirect...")

    server.serve_forever()

    result = server.result
    if result is None:
        raise SystemExit("No callback received")
    if "error" in result:
        desc = result.get("error_description", [""])[0]
        raise SystemExit(f"Authorization failed: {result['error'][0]} — {desc}")
    if result.get("state", [None])[0] != state:
        raise SystemExit("State mismatch on callback — possible CSRF, aborting")
    code = result.get("code", [None])[0]
    if not code:
        raise SystemExit("No authorization code in callback")
    code = code.split("#")[0]  # Instagram sometimes appends "#_" to the code

    token_resp = requests.post(
        TOKEN_URL,
        data={
            "client_id": APP_ID,
            "client_secret": APP_SECRET,
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "code": code,
        },
        timeout=15,
    )
    if not token_resp.ok:
        raise SystemExit(f"Token exchange failed: HTTP {token_resp.status_code} — {token_resp.json()}")

    short_lived = token_resp.json().get("access_token")
    if not short_lived:
        raise SystemExit("No access_token in token exchange response")

    exchange_resp = requests.get(
        EXCHANGE_URL,
        params={
            "grant_type": "ig_exchange_token",
            "client_secret": APP_SECRET,
            "access_token": short_lived,
        },
        timeout=15,
    )
    if not exchange_resp.ok:
        raise SystemExit(f"Long-lived exchange failed: HTTP {exchange_resp.status_code} — {exchange_resp.json()}")

    long_lived = exchange_resp.json()
    access_token = long_lived.get("access_token")
    if not access_token:
        raise SystemExit("No access_token in long-lived exchange response")

    set_key(str(ENV_PATH), "IG_ACCESS_TOKEN", access_token)
    print("Success — IG_ACCESS_TOKEN saved to .env")
    print(f"Long-lived token expires_in={long_lived.get('expires_in', 'unknown')}s (value itself not printed)")


if __name__ == "__main__":
    main()
