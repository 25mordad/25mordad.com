"""Instagram carousel slides for «زنده‌ماندن یا زیستن؟».

Two-stage render (decided 2026-09-13):
  1. gpt-image-2 `images/generations` draws the illustration ONLY (no text) —
     cached as files/PanorAIma/surviving-or-living/ig-illustrations/<nn>-<slug>.png
     (section 02+ gets its own subfolder there) so re-rendering text never
     costs another API call.
  2. Playwright composes the 1088x1360 slide: illustration on top, cream text
     panel below, Persian text in Vazirmatn (guaranteed-correct glyphs).

Output: images/PanorAIma/surviving-or-living/instagram/section-<NN>/<nn>-<slug>.jpg

Run:  scripts/.venv/bin/python files/PanorAIma/surviving-or-living/gen_ig_slides.py [slug] [section]
Section defaults to 01. Delete an output jpg to re-render text; delete the cached png to redraw.
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
IMAGES_DIR = REPO_ROOT / "images" / "PanorAIma" / "surviving-or-living" / "instagram"

STYLE = (
    "Flat editorial illustration in a magazine style, subtle film grain texture. "
    "Strict three-color palette: warm cream background (#f3ecdd), earthy ochre "
    "(#b8702a) for anything open, alive or hopeful, cold slate blue (#4d5b6b) for "
    "anything closed, stagnant or worn. Soft black only for thin outlines. One central "
    "metaphor, generous negative space, calm composition. Human figures, if any, are "
    "simple faceless silhouettes. Absolutely no text, no letters, no words, no "
    "watermark, no border. Wide landscape composition."
)

SLIDES_BY_SECTION = {"01": [
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
], "02": [
    {
        "slug": "cover",
        "tag": "بخش دوم",
        "title": "زندگی روزمره",
        "subtitle": "جایی میان کنارآمدن و فاصله‌گرفتن — از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": (
            "A wide urban street seen from slightly above. The building facades lining it "
            "are cold slate blue, flat and uniform, pressed tightly together. In the narrow "
            "alleys and gaps between them, warm ochre light glows and small signs of life "
            "are visible, tucked out of sight from the street itself."
        ),
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": (
            "A narrow alley between two tall cold slate blue building facades, seen "
            "straight on, fading into the distance in evening light. Deep within the "
            "alley, one single small warm ochre point of light glows quietly, like a "
            "candle or a lit window, the only warmth visible. No human figure. Minimal, "
            "still, solemn twilight composition."
        ),
    },
    {
        "slug": "tasvir-naqes",
        "title": "تصویر ناقص",
        "body": "اگر فقط از بیرون نگاه کنیم، جامعه ایران بسیار سازگار به نظر می‌رسد: جامعه‌ای که با تورم، فیلترینگ، بی‌ثباتی، کاهش کیفیت زندگی و بحران‌های تکرارشونده کنار آمده و هنوز زندگی را ادامه می‌دهد. اما این تصویر کامل نیست.",
        "illustration": (
            "A rectangular picture frame hanging in empty space, showing a calm warm ochre "
            "scene inside it. Just outside the frame's edges, on all sides, the very same "
            "scene continues, but rendered cold slate blue, more crowded and cluttered. "
            "Minimal, symmetrical composition, wide negative space around the frame."
        ),
    },
    {
        "slug": "porsesh-dorost",
        "title": "پرسش درست",
        "body": "همان جامعه‌ای که در بعضی حوزه‌ها خود را با وضعیت وفق داده، در حوزه‌های دیگر فاصله‌اش را با آن حفظ کرده است. مسئله این نیست که جامعه ایران سازگار است یا ناسازگار؛ مسئله این است که کجا کنار می‌آید، کجا فاصله می‌گیرد، و این فاصله را در چه شکل‌هایی نشان می‌دهد.",
        "illustration": (
            "A wide open plain seen from above, its ground broken into a patchwork of warm "
            "ochre and cold slate blue patches with no clean borders between them, irregular "
            "and overlapping. A single small silhouette walks across it, stepping from one "
            "patch into another. Minimal, aerial, quiet composition."
        ),
    },
    {
        "slug": "sazgari-anja-peydast",
        "title": "سازگاری، آنجا که پیداست",
        "body": "در سطح اقتصاد و سیاست، سازگاری بیشتر دیده می‌شود. مردم راهی پیدا می‌کنند که با درآمد کمتر، قیمت‌های بالاتر، آینده مبهم‌تر و قواعد ناپایدارتر زندگی را بچرخانند. در بسیاری از موقعیت‌های سیاسی هم جامعه یاد گرفته محتاط‌تر، کم‌صداتر و غیرمستقیم‌تر رفتار کند.",
        "illustration": (
            "A busy street at ground level, full of small warm ochre silhouette figures "
            "going about ordinary business, walking and moving normally. But every one of "
            "their paths curves and bends around several massive, motionless cold slate "
            "blue blocks planted in the street. Life flows, but obstacles shape its course. "
            "Wide bustling composition."
        ),
    },
    {
        "slug": "sokut-nist-rezayat",
        "title": "سکوت، رضایت نیست",
        "body": "این لزوماً به معنای رضایت نیست. گاهی فقط یعنی هزینه ناسازگاری مستقیم بالاست، نتیجه آن نامطمئن است، و آدم‌ها بین خطر فوری و ادامه زندگی، راه دوم را انتخاب می‌کنند.",
        "illustration": (
            "A warm ochre coiled spring, compressed completely flat under a heavy cold "
            "slate blue weight resting on top of it. Perfectly still, but visibly full of "
            "compressed tension and stored energy. Minimal, close, dramatic side lighting."
        ),
    },
    {
        "slug": "se-rah",
        "title": "سه راه",
        "body": "آلبرت هیرشمن می‌گوید وقتی آدم‌ها با افت کیفیت در یک نهاد یا نظم اجتماعی روبه‌رو می‌شوند، معمولاً سه مسیر دارند: بیرون می‌روند، اعتراض می‌کنند، یا می‌مانند و تحمل می‌کنند.",
        "ref": "بر پایه‌ی کتاب آلبرت هیرشمن درباره‌ی خروج، اعتراض و وفاداری (۱۹۷۰)",
        "illustration": (
            "Three paths branch out from a single point on flat ground, seen from above. "
            "One warm ochre path runs straight off the edge of the frame. Another warm "
            "ochre path rises upward and out of view. The third path, cold slate blue, "
            "continues flat and straight along the ground beneath, going nowhere in "
            "particular. Minimal, symmetrical, aerial composition."
        ),
    },
    {
        "slug": "har-se-hamzaman",
        "title": "هر سه، هم‌زمان",
        "body": "در ایران هم می‌شود همین سه مسیر را دید: مهاجرت نوعی خروج است، اعتراض و نوشتن و مقاومت مدنی نوعی صداست، و ماندن و چرخاندن زندگی شکلی از تحمل. اما این سه همیشه از هم جدا نیستند. یک نفر می‌تواند در کشور بماند، اما ذهنش به خروج فکر کند؛ می‌تواند زندگی روزمره‌اش را با وضعیت تنظیم کند، اما زبان و روایتش با روایت رسمی یکی نباشد.",
        "illustration": (
            "A single silhouette standing with its feet planted on a flat cold slate blue "
            "path. Its long cast shadow stretches out toward one warm ochre path leading "
            "off into the distance, while its raised arm reaches up toward another warm "
            "ochre path rising above. One body pulled in three directions at once. Minimal, "
            "dramatic low-angle composition."
        ),
    },
    {
        "slug": "har-shookhi-moghavemat-nist",
        "title": "هر شوخی مقاومت نیست",
        "body": "مردم همیشه با زبان روزمره اعتراض نمی‌کنند. گاهی فقط زندگی می‌کنند: شوخی می‌کنند، کنایه می‌زنند، درد را قابل‌تحمل‌تر می‌کنند. پس نباید هر شوخی یا هر فاصله‌ای از زبان رسمی را فوراً «مقاومت» نامید. اما همین فاصله نشان می‌دهد که جامعه کاملاً در روایت رسمی حل نشده است.",
        "illustration": (
            "A warm ochre silhouette figure carrying a heavy, oversized cold slate blue "
            "burden on its back. A single small warm ochre balloon is tied to the load, "
            "lifting it just slightly off the ground, not all the way. Minimal, quiet, "
            "slightly wry composition."
        ),
    },
    {
        "slug": "do-farsi",
        "title": "دو فارسی",
        "body": "این فاصله فقط سیاسی هم نیست. فارسی رسمی و فارسی گفتاری از اساس با هم تفاوت دارند؛ به این وضعیت «دوگانگی زبانی» می‌گویند. در جهان عرب، عربی معیار زبان رسمی و رسانه است و لهجه‌های محلی زبان زندگی روزمره. در یونان هم مدت‌ها میان کاتارووسا، زبان رسمی و تصفیه‌شده، و دیموتیکی، زبان مردم، شکاف بود. فاصله میان زبان رسمی و زبان زندگی پدیده‌ای شناخته‌شده است، نه استثنایی کاملاً ایرانی.",
        "illustration": (
            "A single spring of water splitting into two streams. One flows into a "
            "straight, cold slate blue concrete channel, rigid and engineered. The other "
            "winds as a warm ochre natural brook through bare earth, curving and organic. "
            "One source of water, two very different beds. Minimal, calm composition."
        ),
    },
    {
        "slug": "inja-farq-darad",
        "title": "اما اینجا فرق دارد",
        "body": "اما در ایران امروز، این فاصله فقط تفاوت محاوره و نوشتار نیست. زبان رسمی اغلب حامل روایت دولت، اخلاق رسمی، ایدئولوژی، تصویر رسمی از مردم و تعریف رسمی از آینده است. به همین دلیل، زبان روزمره می‌تواند به جایی تبدیل شود که آدم‌ها روایت دیگری از وضعیت می‌سازند.",
        "illustration": (
            "A close view of a straight cold slate blue concrete water channel, water "
            "flowing down it. A row of small identical cold slate blue silhouette shapes "
            "float on the water's surface, evenly spaced, drifting downstream in perfect "
            "uniform order. Minimal, rigid, slightly cold composition."
        ),
    },
    {
        "slug": "matn-penhan",
        "title": "متن پنهان",
        "body": "جیمز سی. اسکات می‌گوید گروه‌هایی که زیر فشار قدرت زندگی می‌کنند معمولاً فقط یک زبان ندارند. یک زبان عمومی دارند که در برابر قدرت به کار می‌رود، و یک زبان پنهان‌تر که در خلوت، شوخی، قصه و گفت‌وگوی روزمره زنده می‌ماند. این زبان پنهان همیشه شورش نیست؛ اما نشان می‌دهد فاصله‌ای وجود دارد.",
        "ref": "بر پایه‌ی پژوهش جیمز سی. اسکات درباره‌ی متن پنهان (۱۹۹۰)",
        "illustration": (
            "A cutaway cross-section of the ground. Above the ground line: a cold slate "
            "blue public square, silhouette figures standing formally, spaced apart from "
            "one another, upright and reserved. Below the ground line, in warm ochre soil: "
            "the very same silhouette figures now standing close together, facing one "
            "another, relaxed and intimate. Minimal, symmetrical cutaway composition."
        ),
    },
    {
        "slug": "do-jahan-mana",
        "title": "دو جهان معنا",
        "body": "جیمز بری درباره‌ی ایران توضیح می‌دهد که گفتار رسمی می‌کوشد حول انقلاب، اسلام سیاسی و تصویری واحد از ملت، زبانی مرکزی و وحدت‌بخش بسازد؛ اما این زبان با صداهای متکثر قومی، مذهبی و روزمره وارد تنش می‌شود. شکاف میان زبان دولت و زبان مردم فقط تفاوت «اداری» و «محاوره‌ای» نیست؛ گاهی تفاوت میان دو جهان معناست: جهانی که می‌خواهد وضعیت را توضیح دهد، و جهانی که آن وضعیت را زندگی می‌کند.",
        "ref": "بر پایه‌ی پژوهش جیمز بری درباره‌ی زبان رسمی در ایران",
        "illustration": (
            "A huge smooth cold slate blue dome attempting to cover a wide open plain. "
            "But the ground beneath it is warm ochre, uneven and richly textured, and the "
            "dome's edges never quite touch down to the ground anywhere around its "
            "perimeter, leaving visible gaps. Minimal, wide architectural composition."
        ),
    },
    {
        "slug": "ghodrat-ham-vared-mishavad",
        "title": "قدرت هم وارد می‌شود",
        "body": "این شکاف یک‌طرفه نیست. حکومت هم بیرون از زبان روزمره نمانده است. وقتی زبان رسمی برای بخشی از جامعه قانع‌کننده نبوده، قدرت کوشیده از مسیرهایی وارد شود که به زندگی روزمره نزدیک‌ترند: فیلم، سریال، ورزش، موسیقی، چهره‌های محبوب، طنز و شبکه‌های اجتماعی. اینجا دیگر با زبان خشک اداری طرف نیستیم؛ با تلاشی برای نزدیک‌کردن زبان قدرت به زبان مردم.",
        "ref": "این بحث در بخش مربوط به پروپاگاندا جداگانه باز می‌شود.",
        "illustration": (
            "A single cold slate blue humanoid silhouette, now draped in a warm ochre "
            "robe, standing among a crowd of warm ochre figures. The robe sits awkwardly, "
            "obviously separate from the body beneath it, with cold slate blue visibly "
            "showing at its edges and seams. Minimal, quiet, slightly uneasy composition."
        ),
    },
    {
        "slug": "faghat-zaban-nist",
        "title": "فقط زبان نیست",
        "body": "این فاصله فقط در زبان دیده نمی‌شود. کنارآمدن با پایین‌آمدن استاندارد زندگی، اما مقاومت در برابر از دست‌دادن سبک زندگی شخصی. پناه‌بردن به حلقه‌های نزدیک، اما بی‌اعتمادی به فضای عمومی. پذیرفتن کیفیت پایین‌تر کالا و خدمات، اما حفظ حساسیت در پوشش، بدن، موسیقی، سفر، اینترنت و رابطه‌ها.",
        "illustration": (
            "A simple, sparse room where every piece of furniture is cold slate blue, worn "
            "and faded. Only one small object — a patterned vase or an embroidered cloth — "
            "glows warm ochre, clearly cared for and preserved, lit by a soft warm light. "
            "Minimal, quiet, intimate interior composition."
        ),
    },
    {
        "slug": "keshmakesh-bar-sar-mana",
        "title": "کشمکش بر سر معنا",
        "body": "جامعه ایران را نمی‌شود فقط با شاخص‌های اقتصادی یا رفتار سیاسی توضیح داد. زندگی روزمره فقط محل سازگاری نیست؛ محل کشمکش بر سر معنا هم هست. مردم هم راهی برای ادامه‌دادن پیدا می‌کنند، هم گاهی فاصله‌شان را نشان می‌دهند. جامعه ممکن است با بحران کنار آمده باشد، اما این کنارآمدن همیشه به معنای پذیرش کامل روایت رسمی از بحران نیست.",
        "illustration": (
            "A return to the cover's urban street, same angle but seen from farther back. "
            "Now warm ochre light glows from within the cold slate blue building facades "
            "themselves, and cold slate blue silhouette figures also appear within the "
            "warm ochre alleys. The two are interwoven throughout the scene, not "
            "separated. Wide, layered composition."
        ),
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: اقتصاد",
        "author": "بهمن رشادی",
        "body": "این بخش دوم از نوشتار «زنده‌ماندن یا زیستن؟» بود. جامعه‌ای که ادامه می‌دهد، اما همیشه با همان زبانی که از او انتظار می‌رود، ادامه‌دادن را توضیح نمی‌دهد. بخش بعد: اقتصاد، روشن‌ترین میدان تاب‌آوری.",
        "illustration": (
            "The same cover street, now at dusk, seen further along its length. Ahead, a "
            "doorway glows with warm ochre light, inviting and open, at the end of the "
            "street's cold slate blue facades. A sense of continuing forward. Wide, warm, "
            "hopeful composition."
        ),
    },
], "03": [
    {
        "slug": "cover",
        "tag": "بخش سوم",
        "title": "اقتصاد",
        "subtitle": "روشن‌ترین میدان تاب‌آوری — از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": (
            "A side cutaway view of one modest, simple room. Its ceiling is a single heavy "
            "cold slate blue slab that has come down low, pressing the space from above. "
            "Inside, warm ochre faceless silhouette figures carry on ordinary daily life, "
            "standing slightly stooped beneath it, still moving and busy. Wide composition, "
            "generous negative space around the room."
        ),
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": (
            "The same cutaway room at dusk, now empty of any human figure. A single small "
            "warm ochre point of light, like a candle flame, glows quietly on the floor "
            "beneath the low cold slate blue ceiling slab. The rest of the space is dim and "
            "still. Minimal, solemn, respectful composition."
        ),
    },
    {
        "slug": "bohran-lams-mishavad",
        "title": "بحران لمس می‌شود",
        "body": "روشن‌ترین میدان سازگاری جامعه ایران، اقتصاد است. نه چون اقتصاد مهم‌تر از سیاست، فرهنگ یا زبان است؛ بلکه چون فشار اقتصادی هر روز و هر ساعت خودش را به زندگی تحمیل می‌کند. تورم، اجاره، قیمت غذا، دارو، حمل‌ونقل، آموزش، اینترنت، درمان و حتی تفریح، بحران را از سطح خبر به سطح بدن و خانه می‌آورند. اقتصاد جایی است که بحران دیگر فقط شنیده نمی‌شود؛ لمس می‌شود.",
        "illustration": (
            "A close interior view: the cold slate blue ceiling slab has come down low "
            "enough to touch. A warm ochre faceless silhouette stands beneath it with one "
            "hand raised, palm resting flat against the underside of the slab. Intimate, "
            "close composition, soft light."
        ),
    },
    {
        "slug": "feshar-mohit",
        "title": "فشار، به محیط تبدیل شده",
        "body": "در گزارش‌های جدید بانک جهانی درباره ایران، اقتصاد کشور زیر فشار هم‌زمان چند عامل توصیف شده است: چالش‌های ساختاری، تحریم‌ها، کمبود آب و انرژی، اختلال‌های تجاری و فشارهای ناشی از نااطمینانی سیاسی و منطقه‌ای. بانک جهانی نوشته است که تورم بالا و کاهش درآمد واقعی، تقاضای داخلی را ضعیف می‌کند و فقر می‌تواند افزایش یابد. فشار اقتصادی در ایران یک فشار گذرا نیست؛ به محیط زندگی تبدیل شده است.",
        "ref": "بر پایه‌ی گزارش‌های بانک جهانی درباره‌ی ایران",
        "illustration": (
            "An aerial view of a whole neighbourhood of identical simple rooms seen in "
            "cutaway, side by side and row after row. One single continuous cold slate blue "
            "slab lies across every one of their ceilings, unbroken, with no gap anywhere. "
            "Warm ochre life visible in each room below. Wide, calm, architectural composition."
        ),
    },
    {
        "slug": "montazer-nemimanand",
        "title": "مردم منتظر نمی‌مانند",
        "body": "نکته این است که جامعه با این فشار چه می‌کند. مردم وقتی با تورم مزمن روبه‌رو می‌شوند، فقط منتظر نمی‌مانند.",
        "illustration": (
            "Inside the low room, one empty cold slate blue chair sits alone in the middle "
            "of the floor, unused. Several warm ochre faceless silhouettes move past it in "
            "different directions, mid-task and busy, none of them looking at it. Minimal, "
            "quiet, kinetic composition."
        ),
    },
    {
        "slug": "hesab-ketab-roozmareh",
        "title": "حساب‌وکتاب روزمره",
        "body": "سبد خرید تغییر می‌کند. برندها عوض می‌شوند. کیفیت پایین‌تر پذیرفته می‌شود. مقدار خرید کم می‌شود. خریدهای بزرگ عقب می‌افتد. پس‌انداز به طلا، ارز، کالا، یا هر چیزی که کمتر آب برود منتقل می‌شود. کار دوم و سوم عادی‌تر می‌شود. قرض، قسط، حساب‌وکتاب، مقایسه قیمت، خرید از این‌جا و آن‌جا، و حذف آرام خواسته‌ها بخشی از زندگی می‌شود.",
        "illustration": (
            "Inside the room, warm ochre faceless silhouettes are busy rearranging the "
            "furniture to fit beneath the lowered cold slate blue ceiling: stacking, "
            "folding, shifting pieces sideways, tucking things underneath one another. Many "
            "small skilful actions at once. Busy, warm, competent composition."
        ),
    },
    {
        "slug": "faghat-iran-nist",
        "title": "فقط مخصوص ایران نیست",
        "body": "این رفتارها فقط مخصوص ایران نیست. بانک مرکزی اروپا در بررسی رفتار خانوارها در دوره تورم بالا نشان می‌دهد که مردم برای سازگاری با قیمت‌های بالاتر، بیشتر دنبال قیمت بهتر می‌گردند، به کالاهای ارزان‌تر یا کم‌کیفیت‌تر رو می‌آورند، مقدار خرید را کم می‌کنند، از پس‌انداز مصرف می‌کنند، یا بیشتر کار می‌کنند. تفاوت ایران در این است که این وضعیت برای بسیاری از مردم نه یک دوره کوتاه، بلکه تجربه‌ای مزمن و تکرارشونده شده است.",
        "ref": "بر پایه‌ی بررسی بانک مرکزی اروپا درباره‌ی رفتار خانوارها در تورم بالا",
        "illustration": (
            "Several cutaway rooms standing in a row. In most of them the cold slate blue "
            "ceiling has come down only a little, hovering just below its original height. "
            "In one room, the ceiling has descended far lower than all the others and has "
            "clearly stayed there a long time. Warm ochre figures inside each. Wide, "
            "comparative composition."
        ),
    },
    {
        "slug": "tarjihat-sazegarshode",
        "title": "ترجیحات سازگارشده",
        "body": "در چنین وضعیتی، سازگاری فقط در رفتار خرید دیده نمی‌شود؛ در خواسته‌ها هم دیده می‌شود. جان الستر در بحث «ترجیحات سازگارشده» می‌گوید گاهی آدم‌ها خواسته‌های خود را با آنچه در دسترس است تنظیم می‌کنند. یعنی وقتی چیزی مدام دور از دسترس می‌شود، ممکن است کم‌کم نه فقط از برنامه زندگی، بلکه از تخیل زندگی هم حذف شود.",
        "ref": "بر پایه‌ی بحث جان الستر درباره‌ی ترجیحات سازگارشده",
        "illustration": (
            "A tall shelf on the room's wall holding a few warm ochre objects. The cold "
            "slate blue ceiling has descended below the level of the shelf's upper part, so "
            "the objects up there are now cut off, out of reach and fading into cold slate "
            "blue. A warm ochre silhouette stands below. Minimal, quiet composition."
        ),
    },
    {
        "slug": "tavagho-az-zendegi",
        "title": "توقع از زندگی",
        "body": "وقتی خانه، سفر، آموزش باکیفیت، درمان مطمئن، فراغت، امنیت شغلی یا آینده قابل‌برنامه‌ریزی مدام دورتر می‌شود، جامعه فقط مصرفش را کم نمی‌کند؛ گاهی توقعش از زندگی را هم پایین می‌آورد.",
        "illustration": (
            "The same wall shelf, now completely empty and bare. Below it, a warm ochre "
            "faceless silhouette sits comfortably settled on the floor, facing forward, no "
            "longer looking up toward the shelf at all. Calm, still, quietly sad composition."
        ),
    },
    {
        "slug": "chehreye-aval-hoosh-amali",
        "title": "چهره‌ی اول: هوش عملی",
        "body": "اینجاست که تاب‌آوری اقتصادی دو چهره پیدا می‌کند. یک چهره‌اش هوش عملی مردم است: توانایی پیدا کردن راه، کم‌کردن هزینه، ساختن شبکه کمک، استفاده از فرصت‌های کوچک، تغییر شغل، یادگرفتن مهارت تازه، یا زنده نگه‌داشتن خانواده زیر فشار. این بخش را نباید کوچک شمرد. جامعه‌ای که زیر فشار اقتصادی همچنان کار می‌کند، می‌سازد، مراقبت می‌کند و راهی برای ادامه پیدا می‌کند، ظرفیت بالایی برای انطباق دارد.",
        "illustration": (
            "One warm ochre faceless silhouette holds a slender warm ochre post braced "
            "against a corner of the low cold slate blue ceiling, propping it up. Beneath "
            "the space this creates, several other warm ochre figures work and move more "
            "freely. Cooperative, capable, warm composition."
        ),
    },
    {
        "slug": "chehreye-dovom-farsayesh",
        "title": "چهره‌ی دوم: فرسایش",
        "body": "اما چهره دیگر، فرساینده است. وقتی آدم‌ها برای حفظ حداقل زندگی، بدن و روان و زمان و رابطه‌هایشان را خرج می‌کنند، سازگاری دیگر فقط نشانه توان نیست. وقتی کیفیت غذا پایین می‌آید، درمان عقب می‌افتد، فراغت حذف می‌شود، خواب کم می‌شود، خشم بیشتر می‌شود، و آینده به چند هفته یا چند ماه بعد محدود می‌شود، جامعه هنوز ادامه می‌دهد؛ اما با مصرف کردن منابعی که قرار بود آینده را بسازند.",
        "illustration": (
            "The same slender propping post, now visibly bent and splintering under the "
            "weight of the cold slate blue ceiling. The figure still holding it has cold "
            "slate blue creeping up into its warm ochre silhouette, starting at the hands "
            "and spreading upward through the arms. Close, strained composition."
        ),
    },
    {
        "slug": "kambood-zehn-ra-eshghal-mikonad",
        "title": "کمبود، ذهن را هم اشغال می‌کند",
        "body": "سندیل مولاینیتن و الدار شفیر توضیح می‌دهند که کمبود فقط جیب را کوچک نمی‌کند؛ ذهن را هم اشغال می‌کند. وقتی آدم دائماً باید کمبود پول، وقت یا امکان را مدیریت کند، بخش زیادی از ظرفیت ذهنی‌اش صرف همین مدیریت می‌شود. فشار اقتصادی فقط قدرت خرید را پایین نمی‌آورد؛ تمرکز، آرامش، تصمیم‌گیری، رابطه و توان برنامه‌ریزی را هم مصرف می‌کند.",
        "ref": "بر پایه‌ی کتاب «کمبود» نوشته‌ی سندیل مولاینیتن و الدار شفیر",
        "illustration": (
            "The room's whole interior is crammed full of stacked cold slate blue boxes and "
            "bundles, filling nearly all the space from floor to the low ceiling. A single "
            "warm ochre faceless silhouette has only a narrow sliver of room left to stand "
            "in. Crowded, pressing, claustrophobic composition."
        ),
    },
    {
        "slug": "khatarnaktarin-meydan",
        "title": "خطرناک‌ترین میدان عادی‌سازی",
        "body": "به همین دلیل، اقتصاد روشن‌ترین میدان تاب‌آوری است، اما شاید خطرناک‌ترین میدان عادی‌سازی هم باشد. چون مردم مجبورند هر روز با آن کار کنند. کسی نمی‌تواند تا حل شدن بحران اقتصادی غذا نخورد، اجاره ندهد، کار نکند یا بچه‌اش را مدرسه نفرستد. همین اجبار روزمره باعث می‌شود بحران اقتصادی زودتر از بسیاری بحران‌های دیگر به عادت تبدیل شود.",
        "illustration": (
            "A cutaway room where the low cold slate blue ceiling has clearly been there a "
            "very long time: the doorway, the shelves, the furniture and the walking paths "
            "have all been rebuilt at the new lower height, fitted neatly to it. Nothing "
            "looks cramped any more. The room now matches its ceiling. Calm, settled, "
            "unsettlingly tidy composition."
        ),
    },
    {
        "slug": "vaghti-tavarom-maharat-mishavad",
        "title": "وقتی تورم مهارت می‌شود",
        "body": "تورم دیگر فقط عدد نیست؛ تبدیل می‌شود به مهارت زندگی. بی‌ثباتی فقط مشکل نیست؛ تبدیل می‌شود به روش محاسبه. کاهش کیفیت فقط استثنا نیست؛ تبدیل می‌شود به انتظار جدید.",
        "illustration": (
            "Three small separate vignettes arranged in a row across the frame, all in warm "
            "ochre on cream: a figure walking confidently through a low space without "
            "stooping awkwardly; a figure neatly folding a large cloth down to a small size; "
            "a figure reaching for a low shelf without looking at it. Skill born of "
            "constraint. Clean, rhythmic, three-part composition."
        ),
    },
    {
        "slug": "in-entekhab-nist",
        "title": "این انتخاب نیست",
        "body": "اینجا باید دوباره مراقب قضاوت اخلاقی بود. این سازگاری انتخاب آزادانه و آرام مردم نیست. بیشتر وقت‌ها واکنش به فشاری است که از بیرون بر زندگی تحمیل شده است.",
        "illustration": (
            "A wide pulled-back view revealing what presses the ceiling down: an enormous "
            "cold slate blue mass resting on the room's roof from outside, vastly larger "
            "than the room itself, extending beyond the edges of the frame. The small warm "
            "ochre room sits beneath it. Wide, imposing composition."
        ),
    },
    {
        "slug": "ofogh-kootah-mishavad",
        "title": "افق کوتاه می‌شود",
        "body": "اما نتیجه‌اش فقط اقتصادی نمی‌ماند. بحران اقتصادی فقط جیب مردم را خالی نمی‌کند؛ افق همکاری را هم کوتاه می‌کند. وقتی آینده نامطمئن است، آدم‌ها بیشتر به نجات کوتاه‌مدت فکر می‌کنند. وقتی اعتماد کم است، معامله‌ها محتاط‌تر، رابطه‌ها ابزاری‌تر، و دایره کمک کوچک‌تر می‌شود.",
        "illustration": (
            "Inside the room, a group of warm ochre faceless silhouettes that once formed a "
            "circle now stand apart from one another, the circle broken open, each figure "
            "turned away and holding its own small separate bundle close to its body. The "
            "low cold slate blue ceiling presses above them. Quiet, isolated composition."
        ),
    },
    {
        "slug": "porsesh",
        "title": "پرسش",
        "body": "تاب‌آوری اقتصادی وقتی ارزشمند است که ظرفیت زندگی، همکاری و آینده را حفظ کند. اما وقتی ادامه‌دادن با پایین‌آوردن مداوم استانداردها، حذف آرام خواسته‌ها، فرسایش بدن و روان، و کوتاه‌شدن افق آینده ممکن شود، دیگر باید پرسید: این هنوز تاب‌آوری است، یا عادت‌کردن به زندگی‌ای که مدام کوچک‌تر می‌شود؟",
        "illustration": (
            "A return to the cover's room, same cutaway angle but seen from very far back. "
            "It is now one of countless identical rooms stretching away to the horizon, all "
            "beneath one single continuous cold slate blue ceiling. In every one of them a "
            "warm ochre light is burning. Vast, wide, layered composition."
        ),
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: وقتی سازگاری فرساینده می‌شود",
        "author": "بهمن رشادی",
        "body": "این بخش سوم از نوشتار «زنده‌ماندن یا زیستن؟» بود. اقتصاد در این نوشتار فقط یک بخش جداگانه نیست؛ آزمایشگاه اصلی بحث ماست. در اقتصاد می‌شود دید که جامعه ایران چگونه راهی برای ادامه پیدا کرده است — و در همان‌جا هم می‌شود دید که این ادامه‌دادن چه هزینه‌ای داشته است. بخش بعد: وقتی سازگاری فرساینده می‌شود.",
        "illustration": (
            "The same room at dusk. In one of its walls a doorway stands open at full "
            "original height, with warm ochre light spilling through from beyond it — a "
            "space where a person could stand upright again. Warm, open, hopeful composition."
        ),
    },
]}

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


def render_slide(idx: int, slide: dict, illus_dir: Path, output_dir: Path, total: int) -> Path:
    nn = f"{idx:02d}"
    png_path = illus_dir / f"{nn}-{slide['slug']}.png"
    out_path = output_dir / f"{nn}-{slide['slug']}.jpg"
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
            .replace("__IDX__", f"{idx} / {total}"))
    tmp = illus_dir / f"_tmp-{nn}.html"
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
    output_dir.mkdir(parents=True, exist_ok=True)
    out_path.write_bytes(optimize_jpeg(raw, max_dim=1360, target_kb=600))
    print(f"  saved {out_path.relative_to(REPO_ROOT)} ({out_path.stat().st_size // 1024} KB)")
    return out_path


def main():
    want = sys.argv[1] if len(sys.argv) > 1 else None
    section = sys.argv[2] if len(sys.argv) > 2 else "01"
    slides = SLIDES_BY_SECTION[section]
    illus_dir = ILLUS_DIR if section == "01" else ILLUS_DIR / f"section-{section}"
    illus_dir.mkdir(parents=True, exist_ok=True)
    output_dir = IMAGES_DIR / f"section-{section}"
    total = len(slides)
    for i, slide in enumerate(slides, start=1):
        if want and slide["slug"] != want:
            continue
        render_slide(i, slide, illus_dir, output_dir, total)


if __name__ == "__main__":
    main()
