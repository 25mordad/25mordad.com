#!/usr/bin/env python3
"""Send an Instagram carousel deck (images + caption) to this project's
Telegram group, for manual posting when the Graph API's carousel item cap
(10) is too low for the deck (Instagram's own app allows up to 20, manual
upload only — see publish_ig_carousel.py's docstring for the API limit).

Usage:
    scripts/.venv/bin/python scripts/send_ig_carousel_to_telegram.py <image_dir> --caption-file <path> [--label TEXT]
"""

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from telegram_common import send_message, send_photo  # noqa: E402


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("image_dir")
    parser.add_argument("--caption-file", required=True)
    parser.add_argument("--label", default=None, help="Optional header line sent before the images")
    args = parser.parse_args()

    image_dir = Path(args.image_dir).resolve()
    images = sorted(image_dir.glob("*.jpg"))
    if not images:
        raise SystemExit(f"No .jpg files found in {image_dir}")

    caption = Path(args.caption_file).read_text().strip()

    if args.label:
        send_message(args.label)
    send_message(f"کپشن (برای کپی‌پیست):\n\n{caption}")

    for image_path in images:
        send_photo(image_path)

    print(f"Sent {len(images)} images + caption to Telegram.")


if __name__ == "__main__":
    main()
