"""Shared image post-processing for the photo pipeline — resize/recompress
so nothing heavy lands in the repo, used by both gpt_enhance_photo.py and
gpt_story_typography.py."""

import io

from PIL import Image

MAX_DIM = 1440   # Instagram's feed/story never displays a photo past ~1440px
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
