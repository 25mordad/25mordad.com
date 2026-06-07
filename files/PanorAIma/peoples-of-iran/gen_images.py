#!/usr/bin/env python3
"""
DEPRECATED — approach changed 2026-06-07.

Original plan: generate 16 section images via OpenAI image API.
New plan: use a single background image + styled HTML overlaid with Farsi text,
          then export each section as PNG via Playwright (see gen_section_cards.py).

This file is kept for reference. Do not run it.
"""
raise SystemExit("This script is deprecated. Use gen_section_cards.py instead.")

import base64
import os
import sys
from pathlib import Path

try:
    from openai import OpenAI
except ImportError:
    sys.exit("openai package not installed. Run: pip install openai")

MODEL = "gpt-image-1"          # update if OpenAI releases gpt-image-2
SIZE = "1536x1024"
QUALITY = "high"

REPO_ROOT = Path(__file__).resolve().parents[3]
OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma"

STYLE = (
    "Painterly editorial illustration, muted earth tones with hints of deep blue "
    "and ochre, no text, suitable for a long-form article about Iranian society."
)

SECTIONS = [
    (
        "هرکس از مردم خودش حرف می‌زند",
        "everyone-their-own-people",
        "A fragmented crowd, each group pointing to themselves as 'the people', "
        "diverse faces each claiming to represent the whole. " + STYLE,
    ),
    (
        "از اختلاف نظر تا جهان‌های اجتماعی متفاوت",
        "disagreement-to-social-worlds",
        "Two parallel worlds side by side in the same city — same skyline, "
        "radically different interiors and lives. " + STYLE,
    ),
    (
        "قومیت؛ لایه حافظه، نه واحد اصلی تحلیل امروز",
        "ethnicity-memory-layer",
        "Layered historical memory — old photographs, faded maps, and traditional "
        "patterns overlapping into a single composition. " + STYLE,
    ),
    (
        "آیا این فقط مسئله ایران است؟",
        "pluralism-beyond-iran",
        "A world map where many countries are visibly divided into internal regions, "
        "each with its own coloring — plurality is universal, not uniquely Iranian. " + STYLE,
    ),
    (
        "سبک زندگی؛ سطح قابل مشاهده نیروهای زیرین",
        "lifestyle-visible-surface",
        "Cafes, bazaars, gyms and smartphones all under one sky — the visible "
        "surface of many hidden social forces. " + STYLE,
    ),
    (
        "سبک زندگی فقط نتیجه نیست؛ گاهی موتور تغییر است",
        "lifestyle-as-engine-of-change",
        "One changed habit rippling outward through a neighborhood like a stone "
        "dropped in still water, concentric circles of transformation. " + STYLE,
    ),
    (
        "دانشگاه و شبکه‌های اجتماعی؛ میدان‌های تماس",
        "university-social-media-contact",
        "A campus scene merging with glowing social media feeds — cross-cultural "
        "collision of lifestyles and ideas in a single frame. " + STYLE,
    ),
    (
        "رسانه؛ فروپاشی روایت واحد",
        "media-collapse-single-narrative",
        "A shattered television screen, competing narratives scattered outward "
        "like broken glass, each fragment showing a different version of reality. " + STYLE,
    ),
    (
        "نگاه تکاملی؛ چرا هرکس مردم خودش را می‌بیند؟",
        "evolutionary-ingroup-bias",
        "An abstract evolutionary tree branching into isolated tribal clusters, "
        "each branch curving protectively inward around its own group. " + STYLE,
    ),
    (
        "از تفاوت‌ها به گره‌ها",
        "from-differences-to-knots",
        "Knotted threads of many different colors — tension and connection "
        "at every junction, none fully separate from the rest. " + STYLE,
    ),
    (
        "رنج‌های مشترک؛ میدان مشترک، نه الزاماً اتحاد",
        "shared-suffering",
        "Diverse people waiting in a long queue, same tired faces, same shared "
        "exhaustion cutting across all backgrounds and dress. " + STYLE,
    ),
    (
        "از رنج به پیوند؛ وابستگی‌های عملی روزمره",
        "from-pain-to-connection",
        "Hands from visibly different backgrounds passing something carefully "
        "across a divide — an act of practical necessity, not sentiment. " + STYLE,
    ),
    (
        "زبان فارسی؛ میدان مشترکِ گفت‌وگو و سوءتفاهم",
        "persian-language-shared-field",
        "Persian calligraphy dissolving at its edges into argument and noise — "
        "a shared script that carries both dialogue and misunderstanding. " + STYLE,
    ),
    (
        "اقتصاد؛ میدان عملی همکاری میان مردمان متفاوت",
        "economy-practical-cooperation",
        "A marketplace transaction between two visibly different people — hands "
        "exchanging goods across a counter, no shared ideology required. " + STYLE,
    ),
    (
        "خانواده و خویشاوندی؛ تماس اجباری با دیگری",
        "family-kinship-forced-contact",
        "A multi-generational family gathering — traditional and modern dress "
        "side by side, tension visible but the connection unbreakable. " + STYLE,
    ),
    (
        "مردمان متفاوت، زندگی‌های درهم‌تنیده",
        "intertwined-lives",
        "Aerial view of a city at night — different districts lit in different "
        "colors, all connected by roads and bridges flowing between them. " + STYLE,
    ),
]


def main():
    api_key = os.environ.get("OPENAI_API_KEY")
    if not api_key:
        sys.exit(
            "OPENAI_API_KEY is not set.\n"
            "Run: OPENAI_API_KEY=sk-... python gen_images.py"
        )

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    client = OpenAI(api_key=api_key)
    total = len(SECTIONS)
    results = []

    for i, (fa_heading, en_slug, prompt) in enumerate(SECTIONS, 1):
        out_path = OUTPUT_DIR / f"peoples-of-iran-{en_slug}.png"
        prefix = f"[{i:02d}/{total}]"

        if out_path.exists():
            print(f"{prefix} SKIP  {en_slug}")
            results.append((en_slug, "skipped"))
            continue

        print(f"{prefix} GEN   {en_slug} …", end="", flush=True)
        try:
            response = client.images.generate(
                model=MODEL,
                prompt=prompt,
                size=SIZE,
                quality=QUALITY,
                response_format="b64_json",
                n=1,
            )
            image_bytes = base64.b64decode(response.data[0].b64_json)
            out_path.write_bytes(image_bytes)
            print(f" ✓  {out_path.name}")
            results.append((en_slug, "ok"))
        except Exception as exc:
            print(f" ✗  {exc}")
            results.append((en_slug, f"error: {exc}"))

    ok      = sum(1 for _, s in results if s == "ok")
    skipped = sum(1 for _, s in results if s == "skipped")
    errors  = sum(1 for _, s in results if s.startswith("error"))

    print("\n─── Summary ──────────────────────────────────────────────────────")
    for slug, status in results:
        icon = "✓" if status == "ok" else "→" if status == "skipped" else "✗"
        print(f"  {icon}  {slug}")
    print(f"──────────────────────────────────────────────────────────────────")
    print(f"  Generated: {ok}   Skipped: {skipped}   Errors: {errors}")


if __name__ == "__main__":
    main()
