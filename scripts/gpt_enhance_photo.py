#!/usr/bin/env python3
"""Quality-enhance a fetched photo via OpenAI's gpt-image-2 image-edit endpoint,
before it's shown to Bahman for review in Telegram and eventually published.

Request shape mirrors the proven pattern already used across kavosh/dariche's
scripts/reel_stills.py, podcast_cover.py, gen_instagram_slides_ai.py — same
model name ("gpt-image-2", confirmed live in that codebase, not "gpt-image-1"),
same multipart images/edits POST. `size` defaults to "auto" (not a fixed WxH
like kavosh's from-scratch generations use) specifically because this is a
real photograph whose original aspect ratio must be preserved, not redrawn to
a chosen frame.

Moderation fallback (confirmed live 2026-08-12): OpenAI's output moderation
sometimes hard-blocks edits of photos that include children, even for a plain
sharpen/contrast pass — no prompt wording should ever be used to route around
that, it's their safety system working as intended. This script retries once
(a real transient failure is cheap to retry; a deterministic policy block just
fails the same way twice), and if it's still blocked, falls back to an
optimize-only pass on the untouched source — no AI enhancement, but still a
valid final image, so the pipeline never stalls on a rejected photo.

Every final image is resized/recompressed (optimize_jpeg()) regardless of
which path produced it — Instagram's feed never displays past ~1440px, and
this repo's other images are all in the ~300-500KB range; a full 2048px
gpt-image-2 output would be well outside that.

Reads images/ig-queue/_source/<asset_id>.jpg (the full-2048px fetch from
lr_fetch_photo.py — never committed) and writes the result to the final,
committed, public path images/ig-queue/<asset_id>.jpg.

Usage:
    scripts/.venv/bin/python scripts/gpt_enhance_photo.py <asset_id> --prompt "..."
"""

import argparse
import base64
import io
import os
import sys
import time
from pathlib import Path

import requests
from dotenv import load_dotenv
from PIL import Image

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

QUEUE_DIR = REPO_ROOT / "images" / "ig-queue"
SOURCE_DIR = QUEUE_DIR / "_source"

API_KEY = os.environ.get("OPENAI_API_KEY")
EDIT_API_URL = "https://api.openai.com/v1/images/edits"

MAX_DIM = 1440   # Instagram's feed never displays a photo past ~1440px
TARGET_KB = 500  # keep final images comparable in weight to the rest of the repo's assets
MIN_QUALITY = 55


def optimize_jpeg(data: bytes, max_dim: int = MAX_DIM, target_kb: int = TARGET_KB) -> bytes:
    img = Image.open(io.BytesIO(data)).convert("RGB")
    if max(img.size) > max_dim:
        ratio = max_dim / max(img.size)
        img = img.resize((round(img.width * ratio), round(img.height * ratio)), Image.Resampling.LANCZOS)

    quality = 90
    buf = io.BytesIO()
    while True:
        buf = io.BytesIO()
        img.save(buf, format="JPEG", quality=quality, optimize=True)
        if buf.tell() <= target_kb * 1024 or quality <= MIN_QUALITY:
            return buf.getvalue()
        quality -= 5


def _is_moderation_block(resp: requests.Response) -> bool:
    try:
        return resp.json().get("error", {}).get("code") == "moderation_blocked"
    except Exception:
        return False


def enhance(asset_id: str, prompt: str, size: str = "auto") -> tuple[Path, bool]:
    """Returns (out_path, was_gpt_enhanced)."""
    if not API_KEY:
        raise SystemExit("OPENAI_API_KEY not found in .env")

    source_path = SOURCE_DIR / f"{asset_id}.jpg"
    if not source_path.exists():
        raise SystemExit(f"No source image at {source_path} — run lr_fetch_photo.py first")

    out_path = QUEUE_DIR / f"{asset_id}.jpg"

    for attempt in range(2):
        with open(source_path, "rb") as f:
            resp = requests.post(
                EDIT_API_URL,
                headers={"Authorization": f"Bearer {API_KEY}"},
                files={"image": (source_path.name, f, "image/jpeg")},
                data={"model": "gpt-image-2", "prompt": prompt, "size": size, "quality": "high"},
                timeout=180,
            )
        if resp.ok:
            b64 = resp.json()["data"][0]["b64_json"]
            out_path.write_bytes(optimize_jpeg(base64.b64decode(b64)))
            return out_path, True
        if _is_moderation_block(resp):
            if attempt == 0:
                print("gpt-image-2 rejected this photo (moderation_blocked) — retrying once...", file=sys.stderr)
                time.sleep(2)
                continue
            break
        raise SystemExit(f"Image edit failed ({resp.status_code}): {resp.text[:500]}")

    print("gpt-image-2 rejected this photo twice (moderation_blocked) — "
          "falling back to an optimize-only pass, no AI enhancement.", file=sys.stderr)
    out_path.write_bytes(optimize_jpeg(source_path.read_bytes()))
    return out_path, False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("asset_id")
    parser.add_argument("--prompt", required=True, help="Photo-specific quality-enhance prompt")
    parser.add_argument("--size", default="auto")
    args = parser.parse_args()

    out_path, was_enhanced = enhance(args.asset_id, args.prompt, args.size)
    label = "GPT-enhanced" if was_enhanced else "optimize-only fallback (GPT rejected it)"
    print(f"Saved [{label}]: {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
