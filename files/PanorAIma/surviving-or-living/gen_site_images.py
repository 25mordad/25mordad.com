"""Site assets for «زنده‌ماندن یا زیستن؟»: cover (FA+EN) and per-section hero images.

Same illustration style as gen_ig_slides.py (flat editorial, cream/ochre/slate,
faceless silhouettes, no text). New illustrations are cached in
files/PanorAIma/surviving-or-living/site-illustrations/<slug>.png. The cover
reuses the already-drawn Instagram cover illustration (ig-illustrations/01-cover.png).

Output:
  images/PanorAIma/surviving-or-living/cover.jpg       (1200x1200, FA)
  images/PanorAIma/surviving-or-living/cover-en.jpg     (1200x1200, EN)
  images/PanorAIma/surviving-or-living/heroes/<slug>.jpg (1200x1200, one per section)

Run:  scripts/.venv/bin/python files/PanorAIma/surviving-or-living/gen_site_images.py [target]
      target one of: cover, cover-en, hero:<slug>, or omit for everything.
Delete an output file to re-render it; delete a cached PNG to redraw the illustration.
"""
import base64
import os
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv
from playwright.sync_api import sync_playwright

HERE = Path(__file__).resolve().parent
REPO_ROOT = HERE.parents[2]
sys.path.insert(0, str(REPO_ROOT / "scripts"))
from image_common import optimize_jpeg  # noqa: E402

load_dotenv(REPO_ROOT / ".env")
API_KEY = os.environ.get("OPENAI_API_KEY")
GEN_URL = "https://api.openai.com/v1/images/generations"

IG_ILLUS_DIR = HERE / "ig-illustrations"
SITE_ILLUS_DIR = HERE / "site-illustrations"
IMG_DIR = REPO_ROOT / "images" / "PanorAIma" / "surviving-or-living"
HEROES_DIR = IMG_DIR / "heroes"

STYLE = (
    "Flat editorial illustration in a magazine style, subtle film grain texture. "
    "Strict three-color palette: warm cream background (#f3ecdd), earthy ochre "
    "(#b8702a) for anything open, alive or hopeful, cold slate blue (#4d5b6b) for "
    "anything closed, stagnant or worn. Soft black only for thin outlines. One central "
    "metaphor, generous negative space, calm composition. Human figures, if any, are "
    "simple faceless silhouettes. Absolutely no text, no letters, no words, no "
    "watermark, no border. Wide landscape composition."
)

COVER = {
    "title_fa": "زنده‌ماندن یا زیستن؟",
    "subtitle_fa": "جامعه‌ای که دوام آورده — اما به چه قیمتی؟",
    "tagline_fa": "بین ادامه‌دادن و پذیرفتن، مرزی باریک هست",
    "title_en": "Surviving or Living?",
    "subtitle_en": "A society that has endured — but at what price?",
    "tagline_en": "Between continuing and accepting, there is a narrow line.",
    "author_fa": "بهمن رشادی",
    "author_en": "Bahman Reshadipour",
    "png": IG_ILLUS_DIR / "01-cover.png",
}

SECTIONS = [
    {
        "slug": "resilience-or-normalization",
        "label": "بخش اول",
        "title": "تاب‌آوری یا عادی‌سازی؟",
        "body": "تاب‌آوری و عادی‌سازی شبیه هم شروع می‌شوند: هر دو یعنی جامعه بخشی از بحران را قابل‌تحمل می‌کند تا از هم نپاشد. اما به یک‌جا نمی‌رسند. تاب‌آوری راه آینده را باز نگه می‌دارد؛ عادی‌سازی فقط حساسیت به بحران را کم می‌کند. معیار اصلی این است: سازگاری دارد ظرفیت آینده را نگه می‌دارد یا خرجش می‌کند؟",
        "ref": "بر پایه‌ی پژوهش فرن نوریس درباره‌ی تاب‌آوری اجتماع (۲۰۰۸) و مفهوم «عادی‌سازی انحراف» دایان وان (۱۹۹۶)",
        "png": IG_ILLUS_DIR / "01-cover.png",
    },
    {
        "slug": "everyday-life",
        "label": "بخش دوم",
        "title": "زندگی روزمره؛ جایی میان کنارآمدن و فاصله‌گرفتن",
        "body": "جامعه ایران در اقتصاد و سیاست بیشتر کنار می‌آید؛ در زبان، شوخی، بدن و سبک زندگی بیشتر فاصله می‌گیرد. زبان روزمره جایی می‌شود که روایت رسمی در آن کامل نمی‌نشیند. این فاصله همیشه اعتراض نیست، اما نشان می‌دهد جامعه با وضعیت موجود یکی نشده است.",
        "ref": "بر پایه‌ی نظریه‌ی «خروج، اعتراض و وفاداری» آلبرت هیرشمن (۱۹۷۰) و مفهوم «متن پنهان» جیمز اسکات (۱۹۹۰)",
        "illustration": (
            "A wide public square paved in cold slate blue stone, with a tall austere "
            "statue-like column at its center facing outward. In one corner of the square, "
            "mostly in shadow, a small group of warm ochre faceless silhouettes sit close "
            "together sharing a quiet moment, turned away from the column. Minimal, calm, "
            "distant relationship between the two zones."
        ),
    },
    {
        "slug": "economy",
        "label": "بخش سوم",
        "title": "اقتصاد؛ روشن‌ترین میدان تاب‌آوری",
        "body": "فشار اقتصادی هر روز خودش را به زندگی تحمیل می‌کند: در خرید، در تعمیر، در خودکفایی دارویی، در پس‌انداز. بخشی از این سازگاری هوش عملی مردم است. بخش دیگرش فرساینده است؛ سطح متوسط زندگی در یک دهه نزدیک به یک‌پنجم افت کرده. اقتصاد شاید روشن‌ترین میدان تاب‌آوری باشد، اما خطرناک‌ترین میدان عادی‌سازی هم هست.",
        "ref": "بر پایه‌ی داده‌های بانک جهانی و صندوق بین‌المللی پول، و پژوهش جواد صالحی‌اصفهانی درباره‌ی افت سطح زندگی در ایران (۲۰۲۳)",
        "illustration": (
            "A round loaf of bread on a plain wooden table, seen from directly above, being "
            "sliced into thinner and thinner pieces spreading across the frame from warm "
            "ochre at one end to cold slate blue at the other, the last slice almost "
            "translucent. Minimal still life, soft directional light."
        ),
    },
    {
        "slug": "erosive-adaptation",
        "label": "بخش چهارم",
        "title": "وقتی سازگاری فرساینده می‌شود",
        "body": "بدن و روان هم زیر همین فشار تنظیم می‌شوند. نزدیک به یک نفر از هر چهار ایرانی دست‌کم یک اختلال روان‌پزشکی را در یک سال تجربه کرده، و روند در سه دهه‌ی اخیر بالا رفته. بخش بزرگی از این فرسایش اصلاً ثبت نمی‌شود: عادت‌کردن به کیفیت پایین‌تر، کوتاه‌شدن افق اخلاقی، انتقال فشار به نزدیک‌ترین رابطه‌ها.",
        "ref": "بر پایه‌ی مفهوم «بار آلوستاتیک» بروس مک‌اوِن (۲۰۰۴) و پیمایش‌های ملی سلامت روان در ایران",
        "illustration": (
            "A single standing faceless silhouette, upright and calm from the waist up in "
            "warm ochre, its lower legs and the ground beneath slowly eroding away into fine "
            "cold slate blue dust blowing sideways in the wind. Minimal bare ground, quiet "
            "unsettling stillness."
        ),
    },
    {
        "slug": "small-circles-of-trust",
        "label": "بخش پنجم",
        "title": "اعتمادهای کوچک در جامعه کم‌اعتماد",
        "body": "وقتی نهادها حس امنیت نمی‌سازند، مردم به حلقه‌های نزدیک پناه می‌برند: خانواده، دوست، آشنا. همین حلقه‌ها زندگی را نگه می‌دارند. اما اگر اعتماد فقط همان‌جا حبس بماند و به سطح عمومی نرسد، جامعه در زنده‌ماندن قوی و در ساختن آینده مشترک ناتوان می‌شود.",
        "ref": "بر پایه‌ی نظریه‌ی سرمایه‌ی اجتماعی رابرت پاتنام (۲۰۰۰) و «قدرت پیوندهای ضعیف» مارک گرانووتر (۱۹۷۳)",
        "illustration": (
            "An aerial view of several small warm ochre circular islands scattered across a "
            "flat expanse of cold slate blue water, each island tightly self-contained, no "
            "bridges or paths connecting any island to another. Minimal, calm, wide empty "
            "water."
        ),
    },
    {
        "slug": "nonconformity-as-repair",
        "label": "بخش ششم",
        "title": "ناسازگاری به‌عنوان نیروی اصلاح",
        "body": "اگر سازگاری برای ادامه‌دادن لازم است، ناسازگاری برای اصلاح لازم است. در سبک زندگی، در بدن، در طنز، در نپذیرفتن یک دروغ، جامعه هنوز نشان می‌دهد با وضعیت موجود یکی نشده. مسئله این است که این نشانه‌ها چطور از خشم پراکنده به ظرفیت جمعی برسند — راهی که خودبه‌خود بسته نمانده، بسته نگه داشته شده است.",
        "ref": "بر پایه‌ی مفهوم «زندگی در حقیقت» واسلاو هاول (۱۹۷۸) و «سلاح‌های ضعیفان» جیمز اسکات (۱۹۸۵)",
        "illustration": (
            "A single small warm ochre plant sprouting up through a thin crack in an "
            "otherwise unbroken slab of cold slate blue pavement that stretches to the "
            "horizon. Minimal, low angle, quiet defiant stillness."
        ),
    },
    {
        "slug": "the-narrow-line",
        "label": "بخش هفتم",
        "title": "مرز باریک؛ از تحمل تا امکان تغییر",
        "body": "پرسش این نیست که جامعه ایران چقدر تاب‌آور است؛ پاسخش را می‌دانیم: بسیار. پرسش این است که این تاب‌آوری از کجا به عادی‌سازی وضعیتی تبدیل می‌شود که نباید عادی شود. امید در خودِ تاب‌آوری نیست؛ در توان تشخیص لحظه‌ای است که دیگر نباید تاب آورد.",
        "ref": "بر پایه‌ی رویکرد «قابلیت‌ها»ی آمارتیا سن و مفهوم «جامعه‌ی شایسته»ی آویشای مارگالیت (۱۹۹۶)",
        "illustration": (
            "A thin narrow rope-and-plank bridge stretched tight across a wide chasm, warm "
            "ochre at the near end fading gradually to cold slate blue at the far end. A "
            "single small faceless silhouette walks carefully along the middle of it. Vast "
            "quiet space below and around, wide open sky."
        ),
    },
]

COVER_HTML = """<!doctype html><html lang="{lang}" dir="{dir}"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *{{margin:0;padding:0;box-sizing:border-box}}
  html,body{{width:1200px;height:1200px;background:#f3ecdd;font-family:'Vazirmatn',sans-serif;color:#1a1410;overflow:hidden;position:relative}}
  .art{{position:absolute;top:0;left:0;width:1200px;height:660px;overflow:hidden}}
  .art img{{width:100%;height:100%;object-fit:cover;display:block}}
  .art::after{{content:"";position:absolute;left:0;right:0;bottom:0;height:140px;
    background:linear-gradient(to bottom,rgba(243,236,221,0),#f3ecdd)}}
  .panel{{position:absolute;top:660px;left:0;width:1200px;height:540px;
    display:flex;flex-direction:column;align-items:center;text-align:center;padding:36px 80px 0}}
  .ornament{{font-size:30px;color:#b8702a;opacity:.7;margin-bottom:22px}}
  .title{{font-size:74px;font-weight:900;line-height:1.3;color:#1a1410}}
  .subtitle{{font-size:32px;font-weight:400;color:#4d5b6b;margin-top:20px;line-height:1.6}}
  .divider{{display:flex;align-items:center;gap:16px;width:50%;margin:30px 0}}
  .divider-line{{flex:1;height:1px;background:rgba(184,112,42,.4)}}
  .divider-dot{{font-size:12px;color:#b8702a}}
  .tagline{{font-size:26px;font-weight:300;color:#5a4f42}}
  .footer{{position:absolute;left:0;right:0;bottom:34px;display:flex;flex-direction:column;
    align-items:center;gap:6px}}
  .footer-author{{font-size:24px;font-weight:500;color:#b8702a}}
  .footer-site{{font-size:28px;font-weight:700;color:#b8702a;letter-spacing:.5px;direction:ltr}}
  .footer-tagline{{font-size:20px;font-weight:300;color:#8a7f6f}}
</style></head><body>
<div class="art"><img src="{img}"></div>
<div class="panel">
  <div class="ornament">✦</div>
  <div class="title">{title}</div>
  <div class="subtitle">{subtitle}</div>
  <div class="divider"><div class="divider-line"></div><div class="divider-dot">◆</div><div class="divider-line"></div></div>
  <div class="tagline">{tagline}</div>
</div>
<div class="footer">
  <div class="footer-author">{author}</div>
  <div class="footer-site">25Mordad.com</div>
  <div class="footer-tagline">✦ {beyond} ✦</div>
</div>
</body></html>"""

HERO_HTML = """<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1200px;height:1200px;background:#f3ecdd;font-family:'Vazirmatn',sans-serif;color:#1a1410;overflow:hidden;position:relative}
  .art{position:absolute;top:0;left:0;width:1200px;height:600px;overflow:hidden}
  .art img{width:100%;height:100%;object-fit:cover;display:block}
  .art::after{content:"";position:absolute;left:0;right:0;bottom:0;height:130px;
    background:linear-gradient(to bottom,rgba(243,236,221,0),#f3ecdd)}
  .panel{position:absolute;top:600px;left:0;width:1200px;height:600px;padding:34px 84px 0}
  .label{font-size:24px;font-weight:500;color:#b8702a;letter-spacing:.4px;
    border-bottom:2px solid #b8702a;padding-bottom:6px;display:inline-block;margin-bottom:22px}
  .title{font-size:50px;font-weight:900;line-height:1.35;color:#1a1410}
  .body{font-size:29px;font-weight:400;line-height:1.85;color:#2a221a;margin-top:22px;text-align:justify}
  .ref{font-size:20px;font-weight:300;color:#7a8391;margin-top:18px}
  .footer{position:absolute;left:84px;right:84px;bottom:34px;display:flex;justify-content:space-between;
    align-items:center;font-size:20px;color:#4d5b6b;font-weight:400;direction:ltr}
  .footer .site{font-weight:700;color:#b8702a;letter-spacing:.5px}
</style></head><body>
<div class="art"><img src="__IMG__"></div>
<div class="panel">
  <div class="label">__LABEL__</div>
  <div class="title">__TITLE__</div>
  <div class="body">__BODY__</div>
  <div class="ref">__REF__</div>
</div>
<div class="footer"><span class="site">25Mordad.com</span><span>✦ فراتر از قاب ✦</span></div>
</body></html>"""


def draw_illustration(png_path: Path, description: str) -> None:
    if png_path.exists():
        print(f"  illustration cached: {png_path.name}")
        return
    if not API_KEY:
        raise SystemExit("OPENAI_API_KEY not found in .env")
    print("  drawing illustration with gpt-image-2 ...")
    resp = requests.post(
        GEN_URL,
        headers={"Authorization": f"Bearer {API_KEY}"},
        json={"model": "gpt-image-2", "prompt": STYLE + " Scene: " + description,
              "size": "1536x1024", "quality": "high", "n": 1},
        timeout=240,
    )
    if not resp.ok:
        raise SystemExit(f"generation failed ({resp.status_code}): {resp.text[:500]}")
    png_path.parent.mkdir(parents=True, exist_ok=True)
    png_path.write_bytes(base64.b64decode(resp.json()["data"][0]["b64_json"]))
    print(f"  saved {png_path.relative_to(REPO_ROOT)}")


def _screenshot(html: str, tmp_path: Path, out_path: Path) -> None:
    tmp_path.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1200, "height": 1200})
            page.goto(f"file://{tmp_path}", wait_until="networkidle", timeout=60_000)
            page.wait_for_function("document.fonts.ready")
            page.wait_for_timeout(300)
            raw = page.screenshot(type="jpeg", quality=96,
                                  clip={"x": 0, "y": 0, "width": 1200, "height": 1200})
            browser.close()
    finally:
        tmp_path.unlink(missing_ok=True)
    out_path.parent.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(optimize_jpeg(raw, max_dim=1200, target_kb=600))
    print(f"  saved {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")


def render_cover(lang: str) -> Path:
    out_path = IMG_DIR / ("cover.jpg" if lang == "fa" else "cover-en.jpg")
    print(f"[cover-{lang}]")
    if out_path.exists():
        print("  already rendered, skipping (delete to re-render)")
        return out_path
    html = COVER_HTML.format(
        lang=lang, dir="rtl" if lang == "fa" else "ltr",
        img=COVER["png"].name,
        title=COVER["title_fa"] if lang == "fa" else COVER["title_en"],
        subtitle=COVER["subtitle_fa"] if lang == "fa" else COVER["subtitle_en"],
        tagline=COVER["tagline_fa"] if lang == "fa" else COVER["tagline_en"],
        author=COVER["author_fa"] if lang == "fa" else COVER["author_en"],
        beyond="فراتر از قاب" if lang == "fa" else "Beyond The Frame",
    )
    tmp = IG_ILLUS_DIR / f"_tmp-cover-{lang}.html"
    _screenshot(html, tmp, out_path)
    return out_path


def render_hero(section: dict) -> Path:
    slug = section["slug"]
    out_path = HEROES_DIR / f"{slug}.jpg"
    print(f"[hero] {slug}")
    if out_path.exists():
        print("  already rendered, skipping (delete to re-render)")
        return out_path
    png_path = section.get("png")
    if png_path is None:
        png_path = SITE_ILLUS_DIR / f"{slug}.png"
        draw_illustration(png_path, section["illustration"])
    html = (HERO_HTML
            .replace("__IMG__", f"file://{png_path}")
            .replace("__LABEL__", section["label"])
            .replace("__TITLE__", section["title"])
            .replace("__BODY__", section["body"])
            .replace("__REF__", section.get("ref", "")))
    tmp = SITE_ILLUS_DIR / f"_tmp-hero-{slug}.html"
    tmp.parent.mkdir(parents=True, exist_ok=True)
    _screenshot(html, tmp, out_path)
    return out_path


def main():
    target = sys.argv[1] if len(sys.argv) > 1 else None
    if target in (None, "cover"):
        render_cover("fa")
    if target in (None, "cover-en"):
        render_cover("en")
    if target is None:
        for s in SECTIONS:
            render_hero(s)
    elif target.startswith("hero:"):
        slug = target.split(":", 1)[1]
        match = next((s for s in SECTIONS if s["slug"] == slug), None)
        if not match:
            raise SystemExit(f"no section with slug '{slug}'")
        render_hero(match)


if __name__ == "__main__":
    main()
