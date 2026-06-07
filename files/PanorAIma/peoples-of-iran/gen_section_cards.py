#!/usr/bin/env python3
"""
gen_section_cards.py — render Instagram story card JPEGs for مردمان ایران.

Usage:
  python gen_section_cards.py                        # all sections
  python gen_section_cards.py everyone-their-own-people  # one slug only

Output : images/PanorAIma/peoples-of-iran/stories/<slug>.jpg  (941 × 1672 px, JPEG q=98)
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
OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "peoples-of-iran" / "stories"
CARD_TEXTS = ASSETS_DIR / "card-texts.md"
BG_OPTIONS = ["bg-d.png", "bg.png"]

# ── CSS (shared across both BG variants; bg is injected at render time) ──────

CSS_TEMPLATE = """
* { margin: 0; padding: 0; box-sizing: border-box; }

body {
  width: 941px;
  height: 1672px;
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl;
  overflow: hidden;
  position: relative;
  background-image: url('%(bg)s');
  background-size: cover;
  background-position: center top;
}

.card {
  position: absolute;
  inset: 136px 88px;
  background: rgba(14, 11, 8, 0.82);
  border: 1.5px solid rgba(201, 168, 76, 0.55);
  border-radius: 22px;
  display: flex;
  flex-direction: column;
  align-items: center;
  text-align: center;
  padding: 66px 64px 52px;
}

.section-label {
  font-size: 32px;
  font-weight: 500;
  color: #c9a84c;
  letter-spacing: 0.05em;
  margin-bottom: 22px;
}

.section-title {
  font-size: 76px;
  font-weight: 900;
  color: #ffffff;
  line-height: 1.28;
  margin-bottom: 40px;
}

.divider {
  display: flex;
  align-items: center;
  gap: 18px;
  width: 70%%;
  margin-bottom: 48px;
}

.divider-line {
  flex: 1;
  height: 1px;
  background: rgba(201, 168, 76, 0.45);
}

.divider-dot { font-size: 14px; color: #c9a84c; }

.section-body {
  font-size: 40px;
  font-weight: 400;
  color: #ede5d5;
  line-height: 2.0;
  flex: 1;
  display: flex;
  flex-direction: column;
  justify-content: center;
}

.section-ref {
  font-size: 23px;
  font-weight: 300;
  color: rgba(201, 168, 76, 0.5);
  margin-top: 24px;
  line-height: 1.7;
}

.footer {
  width: 100%%;
  border-top: 1px solid rgba(201, 168, 76, 0.25);
  padding-top: 28px;
  margin-top: 32px;
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 5px;
}

.footer-cta {
  font-size: 27px;
  font-weight: 400;
  color: rgba(237, 229, 213, 0.55);
  margin-bottom: 10px;
}

.footer-site {
  font-size: 38px;
  font-weight: 700;
  color: #c9a84c;
  letter-spacing: 0.06em;
  direction: ltr;
}

.footer-tagline {
  font-size: 27px;
  font-weight: 300;
  color: #7a7060;
}

.section-icon {
  font-size: 28px;
  color: rgba(201, 168, 76, 0.45);
  margin-bottom: 16px;
}

.body-quote {
  font-size: 32px;
  color: rgba(201, 168, 76, 0.35);
  display: block;
  margin-bottom: 18px;
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
      <div class="footer-cta">← {cta}</div>
      <div class="footer-site">25Mordad.com</div>
      <div class="footer-tagline">✦ فراتر از قاب ✦</div>
    </div>
  </div>
  <script>
    (function () {{
      const title = document.querySelector('.section-title');
      // target lines = number of <br> tags + 1
      const targetLines = title.innerHTML.split(/<br[\s/]*>/i).length;
      let size = 76;
      title.style.fontSize = size + 'px';
      // shrink until scrollHeight fits within the intended line count
      while (title.scrollHeight > size * 1.28 * targetLines + 8 && size > 36) {{
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
    """Return a list of section dicts parsed from card-texts.md."""
    text = path.read_text(encoding="utf-8")
    # Split on section headers: ## <n> — <slug>
    parts = re.split(r"\n## (\d+) — ([a-z0-9-]+)\n", text)
    # parts = [preamble, num, slug, content, num, slug, content, ...]
    sections = []
    it = iter(parts[1:])
    for num, slug, content in zip(it, it, it):
        fields: dict = {"num": int(num), "slug": slug}
        for line in content.splitlines():
            # Named field on its own line: - **key:** value
            m = re.match(r"^- \*\*(\w+):\*\* (.+)$", line.strip())
            if m:
                fields[m.group(1)] = m.group(2).strip()
        sections.append(fields)
    return sections


# ── Renderer ──────────────────────────────────────────────────────────────────

def build_html(section: dict, bg: str) -> str:
    css = CSS_TEMPLATE % {"bg": bg}
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
        cta=section.get("cta", ""),
    )


def render_card(section: dict, out_path: Path):
    bg = random.choice(BG_OPTIONS)
    html = build_html(section, bg)

    # Temp HTML lives next to the bg images so relative url('bg*.png') resolves
    tmp = ASSETS_DIR / f"_tmp_{section['slug']}.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 941, "height": 1672})
            page.goto(f"file://{tmp}", wait_until="networkidle", timeout=30_000)
            page.wait_for_function("document.fonts.ready")
            out_path.parent.mkdir(parents=True, exist_ok=True)
            page.screenshot(
                path=str(out_path),
                clip={"x": 0, "y": 0, "width": 941, "height": 1672},
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
        render_card(s, out)

    print("\nDone.")


if __name__ == "__main__":
    main()
