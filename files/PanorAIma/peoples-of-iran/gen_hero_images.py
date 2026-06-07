#!/usr/bin/env python3
"""
gen_hero_images.py — render square hero image JPEGs for مردمان ایران.

Usage:
  python gen_hero_images.py                        # all sections
  python gen_hero_images.py everyone-their-own-people  # one slug only

Output : images/PanorAIma/peoples-of-iran/heroes/<slug>.jpg  (1200 × 1200 px, JPEG q=98)
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

ASSETS_DIR = Path(__file__).resolve().parent          # files/PanorAIma/peoples-of-iran/
REPO_ROOT  = ASSETS_DIR.parents[2]                    # repo root
OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "peoples-of-iran" / "heroes"
CARD_TEXTS = ASSETS_DIR / "card-texts.md"
BG_OPTIONS = ["bg-d.png", "bg.png"]

SIZE = 1200

# ── CSS ───────────────────────────────────────────────────────────────────────

CSS_TEMPLATE = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  width: %(size)dpx;
  height: %(size)dpx;
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl;
  overflow: hidden;
  position: relative;
  background-image: url('%(bg)s');
  background-size: cover;
  background-position: center;
}

.card {
  position: absolute;
  inset: 80px;
  background: rgba(14, 11, 8, 0.82);
  border: 1.5px solid rgba(201, 168, 76, 0.55);
  border-radius: 22px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 56px 72px 48px;
}

.section-icon {
  font-size: 26px;
  color: rgba(201, 168, 76, 0.45);
  margin-bottom: 14px;
}

.section-label {
  font-size: 30px;
  font-weight: 500;
  color: #c9a84c;
  letter-spacing: 0.05em;
  margin-bottom: 20px;
}

.section-title {
  font-size: 70px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.28;
  margin-bottom: 32px;
}

.divider {
  display: flex;
  align-items: center;
  gap: 18px;
  width: 65%%;
  margin-bottom: 36px;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: rgba(201, 168, 76, 0.45);
}

.divider-dot { font-size: 14px; color: #c9a84c; }

.section-body {
  font-size: 36px;
  font-weight: 400;
  color: #ede5d5;
  line-height: 2.0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.body-quote {
  font-size: 28px;
  color: rgba(201, 168, 76, 0.35);
  display: block;
  margin-bottom: 16px;
}

.section-ref {
  font-size: 22px;
  font-weight: 300;
  color: rgba(201, 168, 76, 0.5);
  margin-top: 20px;
  line-height: 1.7;
}

.footer {
  width: 100%%;
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  padding-top: 24px;
  margin-top: 28px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.footer-site {
  font-size: 34px;
  font-weight: 700;
  color: #c9a84c;
  letter-spacing: 0.06em;
  direction: ltr;
}

.footer-tagline {
  font-size: 24px;
  font-weight: 300;
  color: #7a7060;
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
  <div class="card">
    <div class="section-icon">✦</div>
    <div class="section-label">{label}</div>
    <h1 class="section-title">{title}</h1>
    <div class="divider">
      <div class="divider-line"></div>
      <div class="divider-dot">◆</div>
      <div class="divider-line"></div>
    </div>
    <p class="section-body">
      <span class="body-quote">❝</span>
      {body}
    </p>
    {ref_html}
    <div class="footer">
      <div class="footer-site">25Mordad.com</div>
      <div class="footer-tagline">✦ فراتر از قاب ✦</div>
    </div>
  </div>
  <script>
    (function () {{
      const title = document.querySelector('.section-title');
      const targetLines = title.innerHTML.split(/<br[\\s/]*>/i).length;
      let size = 70;
      title.style.fontSize = size + 'px';
      while (title.scrollHeight > size * 1.28 * targetLines + 8 && size > 32) {{
        size -= 1;
        title.style.fontSize = size + 'px';
      }}
    }})();
  </script>
</body>
</html>
"""


# ── Parser ────────────────────────────────────────────────────────────────────

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


# ── Renderer ──────────────────────────────────────────────────────────────────

def build_html(section: dict, bg: str) -> str:
    css = CSS_TEMPLATE % {"size": SIZE, "bg": bg}
    ref_html = (
        f'<p class="section-ref">{section["ref"]}</p>'
        if section.get("ref") else ""
    )
    return HTML_TEMPLATE.format(
        css=css,
        label=section.get("label", ""),
        title=section.get("title", ""),
        body=section.get("body", ""),
        ref_html=ref_html,
    )


def render_hero(section: dict, out_path: Path):
    bg = random.choice(BG_OPTIONS)
    html = build_html(section, bg)

    tmp = ASSETS_DIR / f"_tmp_hero_{section['slug']}.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": SIZE, "height": SIZE})
            page.goto(f"file://{tmp}", wait_until="networkidle", timeout=30_000)
            page.wait_for_function("document.fonts.ready")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": SIZE, "height": SIZE},
                quality=98,
            )
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)

    print(f"  ✓  {out_path.name}  (bg: {bg})")


# ── Main ──────────────────────────────────────────────────────────────────────

def main():
    filter_slug = sys.argv[1] if len(sys.argv) > 1 else None
    sections = parse_card_texts(CARD_TEXTS)

    if filter_slug:
        sections = [s for s in sections if s["slug"] == filter_slug]
        if not sections:
            sys.exit(f"slug '{filter_slug}' not found in {CARD_TEXTS.name}")

    total = len(sections)
    for i, s in enumerate(sections, 1):
        out = OUTPUT_DIR / f"{s['slug']}.jpg"
        prefix = f"[{i:02d}/{total}]"
        if out.exists():
            print(f"{prefix} SKIP  {out.name}")
            continue
        print(f"{prefix} …     {s['slug']}")
        render_hero(s, out)

    print("\nDone.")


if __name__ == "__main__":
    main()
