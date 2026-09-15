#!/usr/bin/env python3
"""Publish an Instagram Feed carousel post from a folder of already-committed,
publicly-reachable images (e.g. images/PanorAIma/<slug>/instagram/section-NN/).

Always previews first (image URLs + caption); only calls the Instagram API
when --confirm-publish is passed (same preview + explicit confirmation gate as
lr_publish_photo.py).

Images must already be publicly reachable at
https://25mordad.com/<repo-relative-path> — i.e. committed and pushed, with
Cloudflare Pages deployed — before this can post, since the Instagram Graph
API fetches each image itself from that URL.

Usage:
    scripts/.venv/bin/python scripts/publish_ig_carousel.py <image_dir> --caption-file <path> [--confirm-publish]
    scripts/.venv/bin/python scripts/publish_ig_carousel.py <image_dir> --caption "..." [--confirm-publish]

    Images in <image_dir> are sorted by filename — the deck's own numeric
    prefix (01-, 02-, ...) controls carousel order.
"""

import argparse
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lr_common import publish_carousel_from_urls  # noqa: E402

REPO_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(REPO_ROOT / ".env")

SITE_BASE = "https://25mordad.com"


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir", help="Directory of images to post as one carousel, sorted by filename")
    caption_group = parser.add_mutually_exclusive_group(required=True)
    caption_group.add_argument("--caption-file", help="Path to a text file containing the caption")
    caption_group.add_argument("--caption", help="Caption text inline")
    parser.add_argument("--confirm-publish", action="store_true")
    args = parser.parse_args()

    image_dir = Path(args.image_dir).resolve()
    if not image_dir.is_dir():
        raise SystemExit(f"Not a directory: {image_dir}")

    images = sorted(image_dir.glob("*.jpg"))
    if not images:
        raise SystemExit(f"No .jpg files found in {image_dir}")
    if not (2 <= len(images) <= 20):
        raise SystemExit(f"Carousel must have 2-20 images, found {len(images)} in {image_dir}")

    caption = Path(args.caption_file).read_text().strip() if args.caption_file else args.caption

    image_urls = []
    for image_path in images:
        rel = image_path.relative_to(REPO_ROOT)
        url = f"{SITE_BASE}/{rel.as_posix()}"
        head = requests.head(url, timeout=15)
        if not head.ok:
            raise SystemExit(
                f"Image not publicly reachable yet: HTTP {head.status_code} for {url}\n"
                f"Commit and push {rel}, wait for the Cloudflare Pages deploy, then retry."
            )
        image_urls.append(url)

    print("=" * 60)
    print(f"Carousel: {len(image_urls)} images from {image_dir.relative_to(REPO_ROOT)}")
    for url in image_urls:
        print(f"  {url}")
    print("-" * 60)
    print(caption)
    print("=" * 60)

    if not args.confirm_publish:
        print("\nDRY RUN — nothing posted. Re-run with --confirm-publish to actually post.")
        return

    token = os.environ.get("IG_ACCESS_TOKEN")
    if not token:
        raise SystemExit("IG_ACCESS_TOKEN not found in .env")

    media_id = publish_carousel_from_urls(token, image_urls, caption)
    print(f"Published: media_id={media_id}")


if __name__ == "__main__":
    main()
