"""One-off Instagram Story announcing the new post (section 1's carousel) is up.

Reuses the already-generated cover illustration (ig-illustrations/01-cover.png)
so no new gpt-image-2 call is needed. Same visual system as gen_ig_slides.py
(cream/ochre/slate-blue palette, Vazirmatn), sized 1080x1920 (Story ratio).
No link/sticker baked in — that's added on the Story in-app afterward.

Output: images/PanorAIma/surviving-or-living/stories/new-post-announcement.jpg

Run: scripts/.venv/bin/python files/PanorAIma/surviving-or-living/gen_announcement_story.py
"""
import sys
from pathlib import Path

from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from image_common import optimize_jpeg  # noqa: E402

IMG = HERE / "ig-illustrations" / "01-cover.png"
OUT = REPO_ROOT / "images" / "PanorAIma" / "surviving-or-living" / "stories" / "new-post-announcement.jpg"

HTML = """<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1080px;height:1920px;background:#f3ecdd;font-family:'Vazirmatn',sans-serif;color:#1a1410;overflow:hidden}
  .art{position:absolute;top:0;left:0;width:1080px;height:1180px;overflow:hidden}
  .art img{width:100%;height:100%;object-fit:cover;display:block}
  .art::after{content:"";position:absolute;left:0;right:0;bottom:0;height:220px;
    background:linear-gradient(to bottom,rgba(243,236,221,0),#f3ecdd)}
  .panel{position:absolute;top:1080px;left:0;width:1080px;height:840px;padding:0 84px;text-align:center}
  .badge{display:inline-block;font-size:34px;font-weight:700;color:#f3ecdd;background:#b8702a;
    letter-spacing:2px;padding:14px 40px;border-radius:999px;margin-bottom:44px}
  .title{font-size:80px;font-weight:900;line-height:1.3;color:#1a1410}
  .subtitle{font-size:32px;font-weight:400;color:#4d5b6b;margin-top:28px;line-height:1.7}
  .divider{width:90px;height:3px;background:#b8702a;margin:40px auto}
  .cta{font-size:36px;font-weight:500;color:#b8702a;margin-top:8px}
  .footer{position:absolute;left:0;right:0;bottom:56px;text-align:center;
    font-size:26px;color:#4d5b6b;font-weight:700;letter-spacing:.5px}
</style></head><body>
<div class="art"><img src="ig-illustrations/01-cover.png"></div>
<div class="panel">
  <div class="badge">✦ پست جدید ✦</div>
  <div class="title">تاب‌آوری یا عادی‌سازی؟</div>
  <div class="subtitle">بخش اول از نوشتار «زنده‌ماندن یا زیستن؟»</div>
  <div class="divider"></div>
  <div class="cta">پست جدید رو ببین ←</div>
</div>
<div class="footer">25Mordad.com</div>
</body></html>"""


def main():
    tmp = HERE / "_tmp-announcement.html"
    tmp.write_text(HTML, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1080, "height": 1920})
            page.goto(f"file://{tmp}", wait_until="networkidle", timeout=60_000)
            page.wait_for_function("document.fonts.ready")
            page.wait_for_timeout(300)
            raw = page.screenshot(type="jpeg", quality=96,
                                  clip={"x": 0, "y": 0, "width": 1080, "height": 1920})
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_bytes(optimize_jpeg(raw, max_dim=1920, target_kb=600))
    print(f"saved {OUT.relative_to(REPO_ROOT)} ({OUT.stat().st_size // 1024} KB)")


if __name__ == "__main__":
    main()
