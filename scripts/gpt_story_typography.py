#!/usr/bin/env python3
"""Generate an Instagram Story typography design for one photo in the photo
pipeline — the photo itself as the base image, the series' fixed bilingual
tagline baked in as elegant Persian typography.

The tagline is the same on every photo's story (it's the series' fixed
closing line, already used in every caption) — what changes per photo is the
base image. One of these gets made per published post, not once for the
whole series (confirmed 2026-08-12 after an initial one-off attempt was
mistaken for a series-wide asset).

Primary path: gpt-image-2 `images/edits` (same endpoint/model as
gpt_enhance_photo.py) draws the typography directly onto the photo. Retries
once on an OpenAI `moderation_blocked` response (confirmed 2026-08-12: this
can happen on photos with children, same as gpt_enhance_photo.py — never
reword the prompt to route around it).

Fallback (persistent moderation block): Playwright + real Vazirmatn web
font, the same guaranteed-correct-Persian-rendering method already used
throughout this repo for every other typography asset (story cards, hero
images, covers) — a dark gradient panel over the untouched photo with the
tagline rendered as real HTML/CSS text, not AI-drawn. Slower to set up but
never garbles Persian script and never hits a moderation wall (it's not an
AI image edit at all).

Reads the FINAL, already-published photo at images/ig-queue/<asset_id>.jpg
(not the working _source/ copy) and writes to
images/ig-queue/stories/<asset_id>.jpg — mirrors the
images/PanorAIma/<slug>/stories/ naming convention used elsewhere in this
repo. Always resized/recompressed via image_common.optimize_jpeg() before
saving — an unoptimized gpt-image-2 story output can be 3MB+, well outside
this repo's usual ~300-500KB image weight.

Usage:
    scripts/.venv/bin/python scripts/gpt_story_typography.py <asset_id>
"""

import argparse
import base64
import os
import sys
import tempfile
import time
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from image_common import optimize_jpeg  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"
STORIES_DIR = QUEUE_DIR / "stories"

API_KEY = os.environ.get("OPENAI_API_KEY")
EDIT_API_URL = "https://api.openai.com/v1/images/edits"

TAGLINE = "دنیا بزرگتر از اونه که ما تصور می‌کنیم"

PROMPT = f"""Turn this photograph into a striking vertical Instagram Story design (portrait
9:16 composition, 1088x1920). Keep the original photo as the main visual — do not change
the subject, pose, or setting — but you may add a tasteful dark gradient/vignette at the
bottom third of the frame to create legible contrast for text.

Add large, elegant Persian (Farsi) typography, in Persian script, reading exactly this
phrase, on two lines:

{TAGLINE}

Style the typography: warm gold/amber color, a modern elegant Persian typeface (like
Vazirmatn or a similarly clean geometric Persian typeface), positioned in the lower third
over the dark gradient, generous letter spacing, right-to-left reading order preserved
correctly. Add a small thin gold decorative line or ornament above the text. Do not add any
other text, no logos, no watermarks, no English text anywhere in the image."""

HTML_TEMPLATE = """<!doctype html>
<html><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@500;700&display=swap" rel="stylesheet">
<style>
  * {{ margin: 0; padding: 0; box-sizing: border-box; }}
  body {{ width: 1088px; height: 1920px; position: relative; overflow: hidden; }}
  .bg {{ position: absolute; inset: 0; width: 100%; height: 100%; object-fit: cover; }}
  .gradient {{
    position: absolute; left: 0; right: 0; bottom: 0; height: 55%;
    background: linear-gradient(to top, rgba(0,0,0,0.92) 10%, rgba(0,0,0,0.55) 55%, rgba(0,0,0,0) 100%);
  }}
  .ornament {{
    position: absolute; bottom: 420px; left: 0; right: 0; text-align: center;
    color: #d4af37; font-size: 28px; letter-spacing: 12px;
  }}
  .tagline {{
    position: absolute; bottom: 200px; left: 60px; right: 60px; text-align: center;
    font-family: 'Vazirmatn', sans-serif; font-weight: 700; color: #d4af37;
    font-size: 64px; line-height: 1.6; direction: rtl;
  }}
</style></head>
<body>
  <img class="bg" src="{photo_path}">
  <div class="gradient"></div>
  <div class="ornament">&#10022;</div>
  <div class="tagline">{tagline}</div>
</body></html>"""


def _is_moderation_block(resp: requests.Response) -> bool:
    try:
        return resp.json().get("error", {}).get("code") == "moderation_blocked"
    except Exception:
        return False


def _generate_via_gpt(source_path: Path) -> bytes | None:
    """Returns raw image bytes on success, None if persistently moderation-blocked."""
    for attempt in range(2):
        with open(source_path, "rb") as f:
            resp = requests.post(
                EDIT_API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                files={"image": (source_path.name, f, "image/jpeg")},
                data={"model": "gpt-image-2", "prompt": PROMPT, "size": "1088x1920", "quality": "high"},
                timeout=180,
            )
        if resp.ok:
            return base64.b64decode(resp.json()["data"][0]["b64_json"])
        if _is_moderation_block(resp):
            if attempt == 0:
                print("gpt-image-2 rejected this photo (moderation_blocked) — retrying once...", file=sys.stderr)
                time.sleep(2)
                continue
            return None
        raise SystemExit(f"Story generation failed ({resp.status_code}): {resp.text[:500]}")
    return None


def _generate_via_playwright(source_path: Path) -> bytes:
    from playwright.sync_api import sync_playwright

    html = HTML_TEMPLATE.format(photo_path=source_path.resolve().as_uri(), tagline=TAGLINE)
    with tempfile.NamedTemporaryFile("w", suffix=".html", delete=False, dir=source_path.parent) as f:
        f.write(html)
        html_path = Path(f.name)
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1088, "height": 1920})
            page.goto(html_path.resolve().as_uri(), wait_until="networkidle", timeout=30_000)
            page.wait_for_function("document.fonts.ready")
            screenshot = page.screenshot(clip={"x": 0, "y": 0, "width": 1088, "height": 1920})
            browser.close()
        return screenshot
    finally:
        html_path.unlink(missing_ok=True)


def generate(asset_id: str) -> Path:
    if not API_KEY:
        raise SystemExit("OPENAI_API_KEY not found in .env")

    source_path = QUEUE_DIR / f"{asset_id}.jpg"
    if not source_path.exists():
        raise SystemExit(f"No published photo at {source_path}")

    STORIES_DIR.mkdir(parents=True, exist_ok=True)
    out_path = STORIES_DIR / f"{asset_id}.jpg"

    raw = _generate_via_gpt(source_path)
    if raw is None:
        print("gpt-image-2 rejected this photo twice (moderation_blocked) — "
              "falling back to the Playwright/Vazirmatn overlay.", file=sys.stderr)
        raw = _generate_via_playwright(source_path)

    # max_dim=1920 (not the 1440 used for feed photos) — 1088x1920 is
    # already the correct target size for a Story, so this only
    # recompresses quality/bytes, never shrinks the dimensions.
    out_path.write_bytes(optimize_jpeg(raw, max_dim=1920))
    return out_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id")
    args = parser.parse_args()

    out_path = generate(args.asset_id)
    print(f"Saved: {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
