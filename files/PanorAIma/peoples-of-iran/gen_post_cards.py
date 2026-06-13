#!/usr/bin/env python3
"""
gen_post_cards.py — render Instagram feed post JPEGs for مردمان ایران.

Usage:
  python gen_post_cards.py                              # all sections
  python gen_post_cards.py everyone-their-own-people   # one slug only

Output : images/PanorAIma/peoples-of-iran/posts/<nn>-<slug>.jpg  (1080 × 1080 px, JPEG q=98)
BG     : randomly chosen between bg-d.png and bg.png each run.
Skips  : already-generated files (delete to re-render).
"""

import random
import re
import sys
from pathlib import Path

try:
    from playwright.sync_api import sync_playwright
except ImportError:
    sys.exit(
        "playwright not installed.\n"
        "Run: pip install playwright && playwright install chromium"
    )

ASSETS_DIR = Path(__file__).resolve().parent
REPO_ROOT  = ASSETS_DIR.parents[2]
OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "peoples-of-iran" / "posts"
CARD_TEXTS = ASSETS_DIR / "card-texts.md"
BG_OPTIONS = ["bg-d.png", "bg.png"]

CSS = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  width: 1080px;
  height: 1080px;
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl;
  overflow: hidden;
  position: relative;
  background-image: url('%(bg)s');
  background-size: cover;
  background-position: center top;
}

.tagline-outer {
  position: absolute;
  bottom: 18px;
  left: 0;
  right: 0;
  text-align: center;
  font-size: 22px;
  font-weight: 300;
  color: rgba(201, 168, 76, 0.6);
}

.card {
  position: absolute;
  inset: 68px 76px 54px;
  background: rgba(14, 11, 8, 0.86);
  border: 1.5px solid rgba(201, 168, 76, 0.55);
  border-radius: 20px;
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 44px 60px 38px;
}

.section-label {
  font-size: 26px;
  font-weight: 500;
  color: #c9a84c;
  letter-spacing: 0.05em;
  margin-bottom: 14px;
  text-align: center;
}

.section-title {
  font-size: 60px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.28;
  margin-bottom: 22px;
  text-align: center;
}

.divider {
  display: flex;
  align-items: center;
  gap: 14px;
  width: 60%%;
  margin-bottom: 28px;
}

.divider-line { flex: 1; height: 1px; background: rgba(201, 168, 76, 0.45); }
.divider-dot { font-size: 12px; color: #c9a84c; }

.section-body {
  font-size: 27px;
  font-weight: 400;
  color: #ede5d5;
  line-height: 1.9;
  text-align: right;
  width: 100%%;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
  gap: 1.1em;
}

.section-ref {
  font-size: 19px;
  font-weight: 300;
  color: rgba(201, 168, 76, 0.55);
  text-align: right;
  width: 100%%;
  margin-top: 18px;
}

.closing {
  font-size: 25px;
  font-weight: 700;
  color: #ffffff;
  text-align: right;
  width: 100%%;
  margin-top: 18px;
  line-height: 1.65;
}

.footer {
  width: 100%%;
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  padding-top: 18px;
  margin-top: 22px;
  text-align: center;
}

.footer-site {
  font-size: 28px;
  font-weight: 700;
  color: #c9a84c;
  letter-spacing: 0.06em;
  direction: ltr;
}
"""

HTML_TEMPLATE = """\
<!DOCTYPE html>
<html lang="fa" dir="rtl">
<head>
  <meta charset="UTF-8">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap" rel="stylesheet">
  <style>{css}</style>
</head>
<body>
  <div class="tagline-outer">✦ فراتر از قاب ✦</div>
  <div class="card">
    <div class="section-label">{label}</div>
    <h1 class="section-title">{title}</h1>
    <div class="divider">
      <div class="divider-line"></div>
      <div class="divider-dot">◆</div>
      <div class="divider-line"></div>
    </div>
    <div class="section-body">
      {body_html}
    </div>
    {ref_html}
    <div class="closing">{closing}</div>
    <div class="footer">
      <div class="footer-site">25Mordad.com</div>
    </div>
  </div>
  <script>
    (function () {{
      // Title auto-scale
      const title = document.querySelector('.section-title');
      const targetLines = title.innerHTML.split(/<br[\\s/]*>/i).length;
      let titleSize = 60;
      title.style.fontSize = titleSize + 'px';
      while (title.scrollHeight > titleSize * 1.28 * targetLines + 8 && titleSize > 36) {{
        titleSize -= 1;
        title.style.fontSize = titleSize + 'px';
      }}
      // Body auto-scale: shrink until all card content fits
      const card = document.querySelector('.card');
      const body = document.querySelector('.section-body');
      let bodySize = 27;
      body.style.fontSize = bodySize + 'px';
      while (card.scrollHeight > card.clientHeight && bodySize > 13) {{
        bodySize -= 0.5;
        body.style.fontSize = bodySize + 'px';
      }}
    }})();
  </script>
</body>
</html>
"""


def parse_card_texts(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    parts = re.split(r"\n## (\d+) — ([a-z0-9-]+)\n", text)
    sections = []
    it = iter(parts[1:])
    for num, slug, content in zip(it, it, it):
        fields: dict = {"num": int(num), "slug": slug}
        for line in content.splitlines():
            m = re.match(r"^- \*\*(\w+):\*\* (.+)$", line.strip())
            if m:
                fields[m.group(1)] = m.group(2).strip()
        sections.append(fields)
    return sections


def build_html(section: dict, bg: str) -> str:
    css = CSS % {"bg": bg}

    raw_body = section.get("post_body", "")
    paragraphs = [p.strip() for p in raw_body.split("¶") if p.strip()]
    body_html = "\n      ".join(f"<p>{p}</p>" for p in paragraphs)

    ref_html = (
        f'<div class="section-ref">{section["post_ref"]}</div>'
        if section.get("post_ref") else ""
    )

    return HTML_TEMPLATE.format(
        css=css,
        label=section.get("label", ""),
        title=section.get("title", ""),
        body_html=body_html,
        ref_html=ref_html,
        closing=section.get("post_closing", ""),
    )


def render_card(section: dict, out_path: Path):
    bg = random.choice(BG_OPTIONS)
    html = build_html(section, bg)

    tmp = ASSETS_DIR / f"_tmp_post_{section['slug']}.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1080})
            page.goto(f"file://{tmp}", wait_until="networkidle", timeout=30_000)
            page.wait_for_function("document.fonts.ready")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": 1080, "height": 1080},
                quality=98,
            )
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)

    print(f"  ✓  {out_path.name}  (bg: {bg})")


def main():
    filter_slug = sys.argv[1] if len(sys.argv) > 1 else None
    sections = parse_card_texts(CARD_TEXTS)

    if filter_slug:
        sections = [s for s in sections if s["slug"] == filter_slug]
        if not sections:
            sys.exit(f"slug '{filter_slug}' not found in {CARD_TEXTS.name}")

    total = len(sections)
    for i, s in enumerate(sections, 1):
        out = OUTPUT_DIR / f"{s['num']:02d}-{s['slug']}.jpg"
        prefix = f"[{i:02d}/{total}]"
        if out.exists():
            print(f"{prefix} SKIP  {out.name}")
            continue
        print(f"{prefix} …     {s['slug']}")
        render_card(s, out)

    print("\nDone.")


if __name__ == "__main__":
    main()
