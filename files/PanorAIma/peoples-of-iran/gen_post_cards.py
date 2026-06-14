#!/usr/bin/env python3
"""
gen_post_cards.py — render Instagram feed post JPEGs for مردمان ایران.
Produces 18 cards: 00a title, 00b dedication, 01–16 sections.

Usage:
  python gen_post_cards.py                              # all 18 cards
  python gen_post_cards.py everyone-their-own-people   # one slug only

Output : images/PanorAIma/peoples-of-iran/posts/<prefix>-<slug>.jpg (1080×1080 px, JPEG q=98)
BG     : bg.png (light) — always.
Skips  : already-generated files (delete to re-render).
"""

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
BG         = "bg.png"

FA_DIGITS = str.maketrans("0123456789", "۰۱۲۳۴۵۶۷۸۹")
def to_fa(n: int) -> str:
    return str(n).translate(FA_DIGITS)

def out_filename(section: dict) -> str:
    num, slug = section["num"], section["slug"]
    if num == -1: return f"00a-{slug}.jpg"
    if num == 0:  return f"00b-{slug}.jpg"
    return f"{num:02d}-{slug}.jpg"


# ── CSS ──────────────────────────────────────────────────────────────────────

FONTS = (
    '<link rel="preconnect" href="https://fonts.googleapis.com">'
    '<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>'
    '<link href="https://fonts.googleapis.com/css2?family=Vazirmatn'
    ':wght@300;400;500;700;900&display=swap" rel="stylesheet">'
)

BASE_CSS = f"""
* {{ margin: 0; padding: 0; box-sizing: border-box; }}
body {{
  width: 1080px; height: 1080px;
  font-family: 'Vazirmatn', sans-serif;
  direction: rtl; overflow: hidden; position: relative;
  background-image: url('{BG}');
  background-size: cover;
  background-position: center center;
}}
"""

TITLE_CSS = BASE_CSS + """
.overlay {
  position: absolute; inset: 0;
  background: rgba(252, 247, 238, 0.80);
}
.content {
  position: absolute; inset: 0;
  display: flex; flex-direction: column;
  align-items: center; justify-content: center;
  padding: 80px 110px 120px;
}
.ornament { font-size: 34px; color: rgba(160,120,40,0.55); margin-bottom: 36px; letter-spacing: 0.2em; }
.article-title { font-size: 100px; font-weight: 900; color: #1a0c03; text-align: center; line-height: 1.2; margin-bottom: 32px; }
.divider { display: flex; align-items: center; gap: 18px; width: 52%; margin-bottom: 30px; }
.divider-line { flex: 1; height: 1px; background: rgba(160,120,40,0.50); }
.divider-dot { font-size: 13px; color: #a07828; }
.article-subtitle { font-size: 37px; font-weight: 300; color: rgba(40,24,6,0.72); text-align: center; letter-spacing: 0.015em; margin-bottom: 28px; }
.author { font-size: 27px; font-weight: 500; color: #8a6412; text-align: center; letter-spacing: 0.05em; }
.footer { position: absolute; bottom: 0; left: 0; right: 0; padding-bottom: 26px; display: flex; flex-direction: column; align-items: center; gap: 5px; }
.footer-site { font-size: 27px; font-weight: 700; color: #8a6412; letter-spacing: 0.07em; direction: ltr; }
.footer-tagline { font-size: 19px; font-weight: 300; color: rgba(138,100,18,0.55); }
"""

DEDICATION_CSS = BASE_CSS + """
.overlay { position: absolute; inset: 0; background: rgba(252, 247, 238, 0.82); }
.card {
  position: absolute; inset: 44px 52px 88px;
  display: flex; flex-direction: column; align-items: center; justify-content: center;
  padding: 0 40px;
}
.quote-mark { font-size: 100px; font-weight: 900; color: rgba(160,120,40,0.20); line-height: 1; align-self: flex-start; margin-bottom: -12px; }
.rule { width: 100%; height: 1.5px; background: linear-gradient(to left, rgba(160,120,40,0) 0%, rgba(160,120,40,0.60) 20%, rgba(160,120,40,0.60) 80%, rgba(160,120,40,0) 100%); }
.rule-top { margin-bottom: 32px; }
.rule-bottom { margin-top: 32px; margin-bottom: 18px; }
.dedication-text { font-size: 44px; font-weight: 450; color: rgba(18,10,3,0.88); line-height: 1.90; text-align: right; width: 100%; }
.ornament-bottom { font-size: 22px; color: rgba(160,120,40,0.50); letter-spacing: 0.25em; }
.footer { position: absolute; bottom: 0; left: 0; right: 0; padding-bottom: 22px; display: flex; flex-direction: column; align-items: center; gap: 4px; }
.footer-site { font-size: 26px; font-weight: 700; color: #8a6412; letter-spacing: 0.07em; direction: ltr; }
.footer-tagline { font-size: 18px; font-weight: 300; color: rgba(138,100,18,0.55); }
"""

SECTION_CSS = BASE_CSS + """
.tagline-outer { position: absolute; bottom: 18px; left: 0; right: 0; text-align: center; font-size: 22px; font-weight: 300; color: rgba(120,85,20,0.60); }
.card {
  position: absolute; inset: 44px 52px 52px;
  background: rgba(252,248,240,0.92);
  border: 1.5px solid rgba(160,120,40,0.38);
  border-radius: 20px;
  display: flex; flex-direction: column; align-items: center;
  padding: 36px 56px 28px;
}
.section-badge {
  position: absolute; top: 18px; left: 20px;
  width: 36px; height: 36px; border-radius: 50%;
  border: 1.5px solid rgba(160,120,40,0.48);
  display: flex; align-items: center; justify-content: center;
  font-size: 16px; font-weight: 600; color: rgba(140,100,30,0.68); direction: ltr;
}
.section-title { font-size: 60px; font-weight: 900; color: #1a0c03; line-height: 1.28; margin-bottom: 20px; text-align: center; }
.divider { display: flex; align-items: center; gap: 14px; width: 60%; margin-bottom: 24px; }
.divider-line { flex: 1; height: 1px; background: rgba(160,120,40,0.45); }
.divider-dot { font-size: 12px; color: #a07828; }
.section-body { font-size: 34px; font-weight: 400; color: rgba(28,16,4,0.85); line-height: 1.9; text-align: right; width: 100%; flex: 1; display: flex; flex-direction: column; justify-content: center; gap: 1.1em; }
.section-ref { font-size: 19px; font-weight: 300; color: rgba(140,100,30,0.72); text-align: right; width: 100%; margin-top: 16px; }
.closing { font-size: 26px; font-weight: 700; color: #1a0c03; text-align: right; width: 100%; margin-top: 16px; line-height: 1.65; }
.footer { width: 100%; border-top: 1px solid rgba(160,120,40,0.28); padding-top: 16px; margin-top: 20px; text-align: center; }
.footer-site { font-size: 28px; font-weight: 700; color: #8a6412; letter-spacing: 0.06em; direction: ltr; }
"""


# ── HTML templates ────────────────────────────────────────────────────────────

def html_title(section: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8">{FONTS}
<style>{TITLE_CSS}</style></head><body>
<div class="overlay"></div>
<div class="content">
  <div class="ornament">✦</div>
  <h1 class="article-title" id="title">{section['title']}</h1>
  <div class="divider"><div class="divider-line"></div><div class="divider-dot">◆</div><div class="divider-line"></div></div>
  <p class="article-subtitle">{section['subtitle']}</p>
  <p class="author">{section['author']}</p>
</div>
<div class="footer">
  <div class="footer-site">25Mordad.com</div>
  <div class="footer-tagline">✦ فراتر از قاب ✦</div>
</div>
<script>
  const el = document.getElementById('title');
  const maxW = document.body.clientWidth - 220;
  let size = 100;
  while (el.scrollWidth > maxW && size > 54) {{ size -= 2; el.style.fontSize = size + 'px'; }}
</script>
</body></html>"""


def html_dedication(section: dict) -> str:
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8">{FONTS}
<style>{DEDICATION_CSS}</style></head><body>
<div class="overlay"></div>
<div class="card">
  <div class="quote-mark">❝</div>
  <div class="rule rule-top"></div>
  <p class="dedication-text" id="ded">{section['body']}</p>
  <div class="rule rule-bottom"></div>
  <div class="ornament-bottom">✦</div>
</div>
<div class="footer">
  <div class="footer-site">25Mordad.com</div>
  <div class="footer-tagline">✦ فراتر از قاب ✦</div>
</div>
<script>
  const card = document.querySelector('.card');
  const el = document.getElementById('ded');
  let size = 44;
  el.style.fontSize = size + 'px';
  while (card.scrollHeight > card.clientHeight && size > 22) {{ size -= 0.5; el.style.fontSize = size + 'px'; }}
</script>
</body></html>"""


def html_section(section: dict) -> str:
    paragraphs = [p.strip() for p in section.get("post_body", "").split("¶") if p.strip()]
    body_html = "\n      ".join(f"<p>{p}</p>" for p in paragraphs)
    ref_html = (
        f'<div class="section-ref">{section["post_ref"]}</div>'
        if section.get("post_ref") else ""
    )
    num_fa = to_fa(section["num"])
    return f"""<!DOCTYPE html>
<html lang="fa" dir="rtl"><head><meta charset="UTF-8">{FONTS}
<style>{SECTION_CSS}</style></head><body>
<div class="tagline-outer">✦ فراتر از قاب ✦</div>
<div class="card">
  <div class="section-badge">{num_fa}</div>
  <h1 class="section-title">{section.get('title', '')}</h1>
  <div class="divider"><div class="divider-line"></div><div class="divider-dot">◆</div><div class="divider-line"></div></div>
  <div class="section-body">
    {body_html}
  </div>
  {ref_html}
  <div class="closing">{section.get('post_closing', '')}</div>
  <div class="footer"><div class="footer-site">25Mordad.com</div></div>
</div>
<script>
(function () {{
  const title = document.querySelector('.section-title');
  const targetLines = title.innerHTML.split(/<br[\\s/]*>/i).length;
  let titleSize = 60; title.style.fontSize = titleSize + 'px';
  while (title.scrollHeight > titleSize * 1.28 * targetLines + 8 && titleSize > 36) {{
    titleSize -= 1; title.style.fontSize = titleSize + 'px';
  }}
  const card = document.querySelector('.card');
  const body = document.querySelector('.section-body');
  let bodySize = 34; body.style.fontSize = bodySize + 'px';
  while (card.scrollHeight > card.clientHeight && bodySize > 13) {{
    bodySize -= 0.5; body.style.fontSize = bodySize + 'px';
  }}
}})();
</script>
</body></html>"""


# ── Parser ────────────────────────────────────────────────────────────────────

def parse_card_texts(path: Path) -> list[dict]:
    text = path.read_text(encoding="utf-8")
    chunks = re.split(r"\n## (-?\d+) — ([a-z0-9-]+)\n", text)
    sections = []
    it = iter(chunks[1:])
    for num_str, slug, content in zip(it, it, it):
        fields: dict = {"num": int(num_str), "slug": slug}
        lines = content.splitlines()
        i = 0
        while i < len(lines):
            m = re.match(r"^- \*\*(\w+):\*\*\s*(.*)$", lines[i].strip())
            if m:
                key, val = m.group(1), m.group(2).strip()
                if not val:
                    # value is on the next indented line(s)
                    parts = []
                    i += 1
                    while i < len(lines) and lines[i].startswith("  "):
                        if lines[i].strip():
                            parts.append(lines[i].strip())
                        i += 1
                    fields[key] = " ".join(parts)
                    continue
                fields[key] = val
            i += 1
        sections.append(fields)
    return sections


# ── Renderer ──────────────────────────────────────────────────────────────────

def build_html(section: dict) -> str:
    num = section["num"]
    if num == -1: return html_title(section)
    if num == 0:  return html_dedication(section)
    return html_section(section)


def render_card(section: dict, out_path: Path):
    html = build_html(section)
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
                type="jpeg", quality=98,
            )
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    print(f"  ✓  {out_path.name}")


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
        out = OUTPUT_DIR / out_filename(s)
        prefix = f"[{i:02d}/{total}]"
        if out.exists():
            print(f"{prefix} SKIP  {out.name}")
            continue
        print(f"{prefix} …     {s['slug']}")
        render_card(s, out)

    print("\nDone.")


if __name__ == "__main__":
    main()
