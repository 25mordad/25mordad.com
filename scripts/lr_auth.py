#!/usr/bin/env python3
"""One-time OAuth Web App flow to obtain a Lightroom refresh token.

Opens a browser consent URL, catches the redirect on a local HTTPS server,
exchanges the authorization code for tokens, and saves LR_REFRESH_TOKEN to
.env. Run once; after that scripts/lr_refresh_token.py verifies/renews.

Usage:
    scripts/.venv/bin/python scripts/lr_auth.py
"""

import http.server
import secrets
import ssl
import subprocess
import threading
import urllib.parse
from pathlib import Path

import requests
from dotenv import load_dotenv, set_key
import os

REPO_ROOT = Path(__file__).resolve().parent.parent
ENV_PATH = REPO_ROOT / ".env"
load_dotenv(ENV_PATH)

CLIENT_ID = os.environ.get("LR_CLIENT_ID")
CLIENT_SECRET = os.environ.get("LR_CLIENT_SECRET")
if not CLIENT_ID or not CLIENT_SECRET:
    raise SystemExit("LR_CLIENT_ID / LR_CLIENT_SECRET not found in .env")

PORT = 8888
REDIRECT_URI = f"https://localhost:{PORT}/callback"
SCOPES = "openid,AdobeID,lr_partner_apis,lr_partner_rendition_apis,offline_access"
IMS_HOST = "https://ims-na1.adobelogin.com"

CERT_DIR = REPO_ROOT / "scripts" / ".certs"
CERT_FILE = CERT_DIR / "localhost.crt"
KEY_FILE = CERT_DIR / "localhost.key"


def ensure_cert():
    if CERT_FILE.exists() and KEY_FILE.exists():
        return
    CERT_DIR.mkdir(exist_ok=True)
    subprocess.run(
        [
            "openssl", "req", "-x509", "-newkey", "rsa:2048",
            "-keyout", str(KEY_FILE), "-out", str(CERT_FILE),
            "-days", "3650", "-nodes", "-subj", "/CN=localhost",
        ],
        check=True,
        capture_output=True,
    )


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
    ensure_cert()

    state = secrets.token_urlsafe(24)
    auth_params = {
        "response_type": "code",
        "client_id": CLIENT_ID,
        "scope": SCOPES,
        "redirect_uri": REDIRECT_URI,
        "state": state,
    }
    auth_url = f"{IMS_HOST}/ims/authorize/v1?{urllib.parse.urlencode(auth_params)}"

    server = http.server.HTTPServer(("localhost", PORT), CallbackHandler)
    server.result = None
    ctx = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    ctx.load_cert_chain(certfile=str(CERT_FILE), keyfile=str(KEY_FILE))
    server.socket = ctx.wrap_socket(server.socket, server_side=True)

    print("Open this URL in a browser to authorize:")
    print(auth_url)
    print()
    print("Notes:")
    print(f"  - The browser will warn about the self-signed cert on localhost:{PORT} — proceed anyway.")
    print("  - If working over SSH/VS Code Remote, make sure this port is forwarded to your local machine.")
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

    token_resp = requests.post(
        f"{IMS_HOST}/ims/token/v1",
        files={
            "client_id": (None, CLIENT_ID),
            "client_secret": (None, CLIENT_SECRET),
            "scope": (None, SCOPES),
            "grant_type": (None, "authorization_code"),
            "code": (None, code),
        },
        timeout=15,
    )
    if not token_resp.ok:
        raise SystemExit(f"Token exchange failed: HTTP {token_resp.status_code} — {token_resp.json()}")

    tokens = token_resp.json()
    refresh_token = tokens.get("refresh_token")
    if not refresh_token:
        raise SystemExit("No refresh_token in response — was offline_access in the requested scope?")

    set_key(str(ENV_PATH), "LR_REFRESH_TOKEN", refresh_token)
    print("Success — LR_REFRESH_TOKEN saved to .env")
    print(f"Access token expires_in={tokens.get('expires_in', 'unknown')}s (value itself not printed)")


if __name__ == "__main__":
    main()
