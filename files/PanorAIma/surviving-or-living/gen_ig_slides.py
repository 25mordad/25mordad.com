"""Instagram carousel slides for «زنده‌ماندن یا زیستن؟» — section 1.

Two-stage render (decided 2026-09-13):
  1. gpt-image-2 `images/generations` draws the illustration ONLY (no text) —
     cached as files/PanorAIma/surviving-or-living/ig-illustrations/<nn>-<slug>.png
     so re-rendering text never costs another API call.
  2. Playwright composes the 1088x1360 slide: illustration on top, cream text
     panel below, Persian text in Vazirmatn (guaranteed-correct glyphs).

Output: images/PanorAIma/surviving-or-living/instagram/section-01/<nn>-<slug>.jpg

Run:  scripts/.venv/bin/python files/PanorAIma/surviving-or-living/gen_ig_slides.py [slug]
Delete an output jpg to re-render text; delete the cached png to redraw.
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

ILLUS_DIR = HERE / "ig-illustrations"
OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "surviving-or-living" / "instagram" / "section-01"

STYLE = (
    "Flat editorial illustration in a magazine style, subtle film grain texture. "
    "Strict three-color palette: warm cream background (#f3ecdd), earthy ochre "
    "(#b8702a) for anything open, alive or hopeful, cold slate blue (#4d5b6b) for "
    "anything closed, stagnant or worn. Soft black only for thin outlines. One central "
    "metaphor, generous negative space, calm composition. Human figures, if any, are "
    "simple faceless silhouettes. Absolutely no text, no letters, no words, no "
    "watermark, no border. Wide landscape composition."
)

SLIDES = [
    {
        "slug": "cover",
        "tag": "بخش اول",
        "title": "تاب‌آوری یا عادی‌سازی؟",
        "subtitle": "از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": (
            "A single dirt road in the foreground splits into two at one point. The left "
            "branch, painted in warm ochre, runs straight toward a bright open horizon with "
            "a low sun. The right branch, in cold slate blue, curls back on itself into a "
            "closed, worn loop that goes nowhere. Seen from slightly above, wide open land."
        ),
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": (
            "A single small warm ochre point of light, like a candle flame, glowing quietly "
            "on the same dirt road at dusk, seen from a distance. No human figure. The rest "
            "of the wide landscape is calm and dim, fading into soft cold slate blue "
            "twilight. Minimal, solemn, respectful stillness."
        ),
    },
    {
        "slug": "shoroo-yeksan",
        "title": "شروع یکسان",
        "body": "تاب‌آوری و عادی‌سازی شبیه هم شروع می‌شوند، اما به یک جا نمی‌رسند. هر دو از فشار می‌آیند. هر دو یعنی جامعه نمی‌تواند هر روز از نو فرو بریزد، پس ناچار است بخشی از بحران را قابل‌تحمل کند.",
        "illustration": (
            "A massive smooth boulder in cold slate blue rests on flat cream-colored ground, "
            "pressing down heavily. From the single point beneath it, two thin cracks begin "
            "to run outward across the ground, one tinted warm ochre, one slate blue, still "
            "close together near their shared origin. Minimal, quiet, seen from a low angle."
        ),
    },
    {
        "slug": "tafavot-dar-natijeh",
        "title": "تفاوت در نتیجه",
        "body": "تفاوت در نتیجه است. تاب‌آوری جامعه را زنده نگه می‌دارد و راه آینده را باز می‌گذارد. عادی‌سازی هم جامعه را زنده نگه می‌دارد، اما حساسیتش به بحران را کم می‌کند.",
        "illustration": (
            "Two thin cracks in flat cream ground, seen from above, far from where they began. "
            "The warm ochre crack runs straight to the bright right edge of the frame where "
            "the ground opens into light. The cold slate blue crack curls around and closes "
            "on itself into a tight ring, going nowhere. Minimal, quiet, lots of empty ground."
        ),
    },
    {
        "slug": "tabavari-yani-che",
        "title": "تاب‌آوری یعنی چه؟",
        "body": "پژوهش تاب‌آوری اجتماعی همین تفاوت را می‌گوید. فرن نوریس و همکارانش تاب‌آوری را فقط «ادامه‌دادن بعد از بحران» نمی‌دانند. تاب‌آوری وقتی معنا دارد که به سلامت روان، کیفیت زندگی، سرمایه اجتماعی و توان جمعی هم وصل باشد. اگر جامعه‌ای دوام بیاورد، اما سلامت و اعتماد و توان همکاری‌اش فرسوده شود، نمی‌شود با خیال راحت گفت تاب‌آور مانده است.",
        "ref": "بر پایه‌ی پژوهش فرن نوریس درباره‌ی تاب‌آوری اجتماع (۲۰۰۸)",
        "illustration": (
            "A single tree standing upright on flat cream ground. Its trunk and branches are "
            "cold slate blue and bare, most leaves fallen in a slate blue scatter at its base. "
            "Below the ground line, a cutaway shows its wide roots in warm ochre, still alive "
            "and reaching deep into the soil. Calm, minimal, centered."
        ),
    },
    {
        "slug": "sazgari-salem",
        "title": "سازگاری سالم",
        "body": "سازگاری می‌تواند سالم باشد. مردم راه‌های تازه برای مراقبت از هم پیدا می‌کنند. خانواده‌ها و دوستان بار هم را سبک می‌کنند. کسب‌وکارها خودشان را با شرایط تازه وفق می‌دهند. زبان و طنز فشار را قابل‌تحمل‌تر می‌کند. اینجا تاب‌آوری هنوز معنای مثبت دارد، چون دارد امکان ادامه را نگه می‌دارد.",
        "illustration": (
            "Several simple faceless silhouettes in warm ochre, standing close together, "
            "passing a large heavy bundle hand to hand across the group. One figure's posture "
            "is tilted back as if laughing. The ground beneath them is warm cream, open and "
            "sunlit. Calm, cooperative composition, no slate blue present."
        ),
    },
    {
        "slug": "hamishe-salem-nist",
        "title": "اما همیشه سالم نیست",
        "body": "اما سازگاری همیشه سالم نیست. گاهی جامعه برای کم‌کردن فشار امروز، راهی پیدا می‌کند که فردا را سخت‌تر می‌کند. سه‌تای‌شان را می‌بینیم: خانواده، کار، دورزدن قانون.",
        "illustration": (
            "A staircase seen from the side, each step visibly carved away from the step "
            "above it, as if material was borrowed upward to build downward. The lower steps "
            "are warm ochre and solid; the upper steps turn cold slate blue, thin and "
            "incomplete, crumbling at the edges. Minimal background, dramatic side lighting."
        ),
    },
    {
        "slug": "khanevade",
        "title": "نمونه‌ی اول: خانواده",
        "body": "وقتی خانواده جای نهادهای حمایتی را می‌گیرد، در کوتاه‌مدت کمک است. اگر دائمی شود، فشار از ساختارها به رابطه‌های نزدیک منتقل شده است.",
        "illustration": (
            "A small family of warm ochre silhouettes — two adults and a child — standing "
            "together, arms raised, holding up the underside of a massive cold slate blue "
            "building ceiling above their heads with their bare hands. The structure is far "
            "too large for them, straining. Minimal cream background, quiet dramatic lighting."
        ),
    },
    {
        "slug": "kar",
        "title": "نمونه‌ی دوم: کار",
        "body": "وقتی آدم‌ها بیشتر کار می‌کنند تا فقط عقب نمانند، راهی برای بقا پیدا کرده‌اند. اگر این کار با فرسودگی بدن، حذف فراغت، بی‌خوابی و اضطراب همراه شود، دیگر فقط تاب‌آوری نیست.",
        "illustration": (
            "A single warm ochre silhouette walking on a treadmill at night, seen from the "
            "side. Ahead of it stretches a cold slate blue horizon under a dark sky that never "
            "gets any closer. Above, a large clock face on the wall has no hands. Minimal, "
            "quiet, isolating composition."
        ),
    },
    {
        "slug": "dorzadan",
        "title": "نمونه‌ی سوم: دورزدن",
        "body": "وقتی مردم راه دورزدن محدودیت‌ها را یاد می‌گیرند، زندگی ممکن‌تر می‌شود. اگر دورزدن جای اصلاح را بگیرد، جامعه فقط در زندگی در وضعیت معیوب ماهر شده است.",
        "illustration": (
            "A broken cold slate blue bridge over a gap, missing its middle section, clearly "
            "unrepaired. Beside it, a rough dirt detour path in warm ochre, worn smooth and "
            "flat from heavy repeated use, winding down into the gap and back up the other "
            "side. No one is working on the bridge. Minimal landscape, wide empty sky."
        ),
    },
    {
        "slug": "adisazi-enheraf",
        "title": "عادی‌سازی انحراف",
        "body": "دایان وان در مطالعه‌ی معروفش درباره‌ی فاجعه‌ی شاتل چلنجر نشان داد که در ناسا بعضی نشانه‌های خطر به‌مرور عادی شدند. چیزی که اول نشانه‌ی مشکل بود، چون بارها تکرار شد و هر بار به فاجعه نرسید، کم‌کم قابل‌قبول شد. تکرار بحران حساسیت به خود بحران را کم می‌کند. چیزی که باید هشدار باشد، بخشی از روال می‌شود.",
        "ref": "بر پایه‌ی کتاب دایان وان درباره‌ی فاجعه‌ی چلنجر (۱۹۹۶)",
        "illustration": (
            "A row of identical warning lights mounted on a wall, seen straight on. Each light "
            "from left to right glows dimmer than the one before, fading from warm ochre "
            "toward cold slate blue, the final one completely dark. Below the row, a torn "
            "desk calendar with pages peeling away rests on a ledge. Minimal, quiet, "
            "unsettling stillness."
        ),
    },
    {
        "slug": "khatare-asli",
        "title": "خطر اصلی در ایران",
        "body": "خطر اصلی در ایران شاید خود بحران نباشد. خوگرفتن با بحران است. تورم، فیلترینگ، بی‌ثباتی شغلی، مهاجرت دائمی، اضطراب آینده. هرکدام اول شوک بودند. وقتی سال‌ها ادامه پیدا کردند، ذهن و رفتار مردم با آن‌ها تنظیم شد.",
        "illustration": (
            "A calm warm ochre silhouette sitting in a chair reading a newspaper, in a room "
            "flooded with cold slate blue water up to the knees, entirely undisturbed by it. "
            "The wall behind is bare except for a few faint worn marks and cracks, abstract, "
            "no legible text. Minimal, calm, unsettling stillness."
        ),
    },
    {
        "slug": "yadgereftan",
        "title": "یادگرفتن",
        "body": "آدم‌ها یاد گرفتند در همین وضعیت خرید کنند، کار کنند، بخندند، برنامه بریزند، بروند یا بمانند. این یادگیری گاهی نشانه‌ی قدرت است. اما اگر باعث شود اصل وضعیت دیگر مسئله به نظر نرسد، وارد قلمرو عادی‌سازی شده‌ایم.",
        "illustration": (
            "A busy, lively warm ochre marketplace scene full of small faceless silhouette "
            "figures in motion, warm and animated. The ground beneath their feet is subtly "
            "tilted at an odd angle, uneven and cracked in cold slate blue, yet none of the "
            "figures notice or react to it. Wide bustling composition."
        ),
    },
    {
        "slug": "porsesh",
        "title": "پرسش نوشتار",
        "body": "پرسشی که بقیه‌ی این نوشتار دنبال می‌کند همین است: کدام بخش از سازگاری ایرانیان هنوز نیروی بقاست، و کدام بخش دارد وضعیتی را عادی می‌کند که نباید عادی باشد؟",
        "illustration": (
            "A large simple balance scale with two pans, perfectly level. One pan and its arm "
            "are warm ochre, the other cold slate blue, both holding equal weight. A single "
            "silhouette hand reaches up toward the fulcrum from below, not yet touching either "
            "side. Minimal, symmetrical, still composition."
        ),
    },
    {
        "slug": "meyar",
        "title": "معیار",
        "body": "یک معیار تاب‌آوری را از عادی‌سازی جدا می‌کند: سازگاری ظرفیت آینده را نگه می‌دارد، یا خرجش می‌کند. اولی راه زیستن را باز می‌گذارد. دومی فقط زنده‌ماندن را کش می‌دهد. جامعه‌ی ایران هر دو را با هم دارد، و کار سخت، تشخیص مرز میان آن‌هاست.",
        "illustration": (
            "A wide aerial view of a single dirt road forking into two, seen from far away and "
            "slightly hazy with distance. The left branch runs warm ochre toward a bright open "
            "horizon, the right branch curls cold slate blue into a closed loop. A single small "
            "silhouette figure stands exactly at the fork point, back turned to the viewer, "
            "motionless. Vast, quiet open landscape."
        ),
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: زندگی روزمره",
        "author": "بهمن رشادی",
        "body": "این بخش اول از نوشتار «زنده‌ماندن یا زیستن؟» بود. بخش‌های بعد: زندگی روزمره، اقتصاد، فرسودگی، اعتماد، ناسازگاری، مرز باریک. منتظر بخش بعدی باشید.",
        "illustration": (
            "The same warm ochre dirt road from the very first image, now seen continuing "
            "forward and curving gently out of the right edge of the frame, disappearing into "
            "soft golden light on the horizon, as if the journey keeps going beyond what is "
            "visible. A single small silhouette walks along it, moving away from the viewer "
            "toward the bend. Wide open landscape, warm and inviting, a sense of more to come."
        ),
    },
    # __NEXT_SLIDE__
]

TOTAL = 16  # planned deck length, shown as n/16 in the corner

HTML = """<!doctype html><html lang="fa" dir="rtl"><head><meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@300;400;500;700;900&display=swap" rel="stylesheet">
<style>
  *{margin:0;padding:0;box-sizing:border-box}
  html,body{width:1088px;height:1360px;background:#f3ecdd;font-family:'Vazirmatn',sans-serif;color:#1a1410;overflow:hidden}
  .art{position:absolute;top:0;left:0;width:1088px;height:725px;overflow:hidden}
  .art img{width:100%;height:100%;object-fit:cover;display:block}
  .art::after{content:"";position:absolute;left:0;right:0;bottom:0;height:120px;
    background:linear-gradient(to bottom,rgba(243,236,221,0),#f3ecdd)}
  .panel{position:absolute;top:725px;left:0;width:1088px;height:635px;padding:10px 72px 0}
  .tag{display:inline-block;font-size:26px;font-weight:500;color:#b8702a;letter-spacing:.5px;
    border-bottom:3px solid #b8702a;padding-bottom:6px;margin-bottom:26px}
  .title{font-size:86px;font-weight:900;line-height:1.25;color:#1a1410}
  .subtitle{font-size:34px;font-weight:300;color:#4d5b6b;margin-top:22px;line-height:1.6}
  .author{font-size:30px;font-weight:500;color:#b8702a;margin-top:14px}
  .body{font-size:33px;font-weight:400;line-height:1.85;color:#2a221a;margin-top:10px;text-align:justify}
  .ref{font-size:22px;font-weight:300;color:#7a8391;margin-top:18px}
  .footer{position:absolute;left:72px;right:72px;bottom:38px;display:flex;justify-content:space-between;
    align-items:center;font-size:22px;color:#4d5b6b;font-weight:400;direction:ltr}
  .footer .site{font-weight:700;color:#b8702a;letter-spacing:.5px}
</style></head><body>
<div class="art"><img src="__IMG__"></div>
<div class="panel">
  __TAG__
  __TITLE__
  __SUBTITLE__
  __AUTHOR__
  __BODY__
  __REF__
</div>
<div class="footer"><span class="site">25Mordad.com</span><span>__IDX__</span></div>
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
    png_path.write_bytes(base64.b64decode(resp.json()["data"][0]["b64_json"]))
    print(f"  saved {png_path.relative_to(REPO_ROOT)}")


def render_slide(idx: int, slide: dict) -> Path:
    nn = f"{idx:02d}"
    png_path = ILLUS_DIR / f"{nn}-{slide['slug']}.png"
    out_path = OUTPUT_DIR / f"{nn}-{slide['slug']}.jpg"
    print(f"[{nn}] {slide['slug']}")
    if out_path.exists():
        print("  already rendered, skipping (delete to re-render)")
        return out_path
    draw_illustration(png_path, slide["illustration"])

    html = (HTML
            .replace("__IMG__", png_path.name)
            .replace("__TAG__", f'<div class="tag">{slide["tag"]}</div>' if slide.get("tag") else "")
            .replace("__TITLE__", f'<div class="title">{slide["title"]}</div>' if slide.get("title") else "")
            .replace("__SUBTITLE__", f'<div class="subtitle">{slide["subtitle"]}</div>' if slide.get("subtitle") else "")
            .replace("__AUTHOR__", f'<div class="author">{slide["author"]}</div>' if slide.get("author") else "")
            .replace("__BODY__", f'<div class="body">{slide["body"]}</div>' if slide.get("body") else "")
            .replace("__REF__", f'<div class="ref">{slide["ref"]}</div>' if slide.get("ref") else "")
            .replace("__IDX__", f"{idx} / {TOTAL}"))
    tmp = ILLUS_DIR / f"_tmp-{nn}.html"
    tmp.write_text(html, encoding="utf-8")
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            page = browser.new_page(viewport={"width": 1088, "height": 1360})
            page.goto(f"file://{tmp}", wait_until="networkidle", timeout=60_000)
            page.wait_for_function("document.fonts.ready")
            page.wait_for_timeout(300)
            raw = page.screenshot(type="jpeg", quality=96,
                                  clip={"x": 0, "y": 0, "width": 1088, "height": 1360})
            browser.close()
    finally:
        tmp.unlink(missing_ok=True)
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(optimize_jpeg(raw, max_dim=1360, target_kb=600))
    print(f"  saved {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")
    return out_path


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    for i, slide in enumerate(SLIDES, start=1):
        if want and slide["slug"] != want:
            continue
        render_slide(i, slide)


if __name__ == "__main__":
    main()
