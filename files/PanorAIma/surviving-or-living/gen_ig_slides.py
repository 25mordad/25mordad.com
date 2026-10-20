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
], "04": [
    # Motif: a small house kept warm by a fire fed with pieces of the house itself —
    # getting through today by burning what was meant to make tomorrow possible.
    {
        "slug": "cover",
        "tag": "بخش چهارم",
        "title": "وقتی سازگاری فرساینده می‌شود",
        "subtitle": "از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": (
            "A side cutaway view of one small simple wooden house on a cold night. In the "
            "middle of its floor a warm ochre fire burns, and faceless ochre silhouette "
            "figures sit close around it. One figure is feeding the fire a plank that has "
            "clearly been pried from the house's own wall: several gaps already show in the "
            "walls, letting the cold slate blue night in. Wide composition, generous "
            "negative space around the house."
        ),
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": (
            "The same small cutaway house at dusk, intact and empty of any human figure. A "
            "single small warm ochre flame glows quietly at the centre of its floor; the "
            "cold slate blue evening surrounds the house. Minimal, solemn, respectful "
            "composition."
        ),
    },
    {
        "slug": "hamishe-bad-nist",
        "title": "سازگاری همیشه بد نیست",
        "body": "سازگاری همیشه بد نیست. بدون سازگاری، زندگی روزمره زیر فشارهای طولانی از هم می‌پاشد. آدم‌ها باید بتوانند راهی برای ادامه پیدا کنند؛ خانواده باید بتواند خودش را حفظ کند؛ کسب‌وکار باید بتواند با شرایط تازه کنار بیاید؛ جامعه باید بتواند در برابر شوک‌ها کاملاً فلج نشود. مسئله از جایی شروع می‌شود که سازگاری، به‌جای حفظ زندگی، شروع کند به مصرف‌کردن خودِ زندگی.",
        "illustration": (
            "The small cutaway house, whole and intact, in a cold slate blue winter night. "
            "Warm ochre faceless figures huddle around a fire inside it, built from fallen "
            "branches gathered outside; a little stack of such branches waits by the door. "
            "The fire is what keeps them going. Warm, protective, quiet composition."
        ),
    },
    {
        "slug": "asibpaziri-bishtar",
        "title": "پاسخی که آسیب‌پذیری را بیشتر می‌کند",
        "body": "در ادبیات بحران و تغییر اقلیم، مفهومی هست برای سازگاری‌ای که در ظاهر پاسخ به بحران است، اما در بلندمدت آسیب‌پذیری را بیشتر می‌کند. این مفهوم فقط برای محیط زیست به کار نمی‌آید. برای فهم جامعه هم مفید است.",
        "ref": "بر پایه‌ی واژه‌نامه‌ی گزارش ارزیابی ششم هیئت بین‌دولتی تغییر اقلیم (IPCC)",
        "illustration": (
            "Close view inside the house: a warm ochre fire burns directly on the wooden "
            "floorboards. A faceless ochre figure warms its hands over it, while beneath the "
            "flames the floorboards are visibly charring into cold slate blue ash. Intimate, "
            "close composition."
        ),
    },
    {
        "slug": "kharj-az-ayandeh",
        "title": "خرج‌کردن از جیب آینده",
        "body": "گاهی راه‌حلی که امروز فشار را کم می‌کند، فردا مسئله را عمیق‌تر می‌کند. جامعه برای اینکه امروز را بگذراند، از منابعی خرج می‌کند که باید آینده را ممکن می‌کردند: اعتماد، سلامت، آموزش، کیفیت رابطه‌ها، محیط زیست، زمان، امید و توان همکاری.",
        "illustration": (
            "Beside the fire inside the house, a woodpile waits to be burned — but it is "
            "made of things meant for the future: a small child's chair, a bookshelf, a "
            "cradle, a ladder, a garden gate. A faceless ochre figure reaches for the next "
            "piece. Still-life composition, generous negative space."
        ),
    },
    {
        "slug": "az-bagha-ta-farsoodegi",
        "title": "از بقا تا فرسودگی",
        "body": "در اقتصاد روزمره، این را روشن‌تر می‌بینیم. خانواده‌ای که برای جبران تورم، کار بیشتر، مصرف کمتر، کیفیت پایین‌تر و حذف فراغت را انتخاب می‌کند، دارد راهی برای بقا پیدا می‌کند. اما اگر این وضعیت طولانی شود، دیگر فقط یک تصمیم اقتصادی نیست. بدن فرسوده می‌شود، روان خسته می‌شود، رابطه‌ها پرتنش‌تر می‌شوند، آموزش بچه‌ها طبقاتی‌تر می‌شود، درمان عقب می‌افتد، و آینده به چیزی تبدیل می‌شود که فقط باید از آن جان سالم به در برد.",
        "illustration": (
            "A family of faceless ochre silhouettes around the fire inside the house, "
            "slumped and tired, sitting apart from one another. Many planks are now missing "
            "from the walls and cold slate blue air pours in through the gaps. The fire "
            "still burns. Heavy, weary composition."
        ),
    },
    {
        "slug": "tanzim-farsayesh",
        "title": "وقتی خودِ تنظیم‌شدن فرسایش می‌شود",
        "body": "بروس مک‌اوِن در بحث «بار آلوستاتیک» توضیح می‌دهد که بدن برای مواجهه با فشار، خودش را تنظیم می‌کند. این تنظیم در کوتاه‌مدت لازم است، اما اگر فشار مزمن شود، خودِ سازگاری به فرسایش بدن تبدیل می‌شود. ما نباید بدن فردی را مستقیم با جامعه یکی بگیریم، اما تشبیهش برای این بحث دقیق است: جامعه هم می‌تواند آن‌قدر با فشار تنظیم شود که خودِ تنظیم‌شدن، به فرسایش تبدیل شود.",
        "ref": "بر پایه‌ی پژوهش بروس مک‌اوِن درباره‌ی «بار آلوستاتیک» و استرس مزمن",
        "illustration": (
            "A single standing faceless silhouette seen in profile. A small warm ochre fire "
            "glows inside its chest, keeping it upright, but the outer edges of the "
            "silhouette are thinning and crumbling away into cold slate blue flakes that "
            "drift off. Minimal, centred composition."
        ),
    },
    {
        "slug": "faghat-pool-nist",
        "title": "فقط در سطح پول نیست",
        "body": "این فرسایش فقط در سطح پول نیست. ممکن است در خودمان یا اطرافیانمان نشانه‌هایی از آن ببینیم: عادت‌کردن به کیفیت پایین‌تر، پایین‌آوردن تدریجی انتظارمان از زندگی، پذیرفتن خدمات بد، بی‌حسی نسبت به تخریب محیط زیست، مصرف‌گرایی بی‌فکر، دورریختن منابع، یا انتقال فشار به آدم‌های نزدیک‌تر. این‌ها حکم قطعی درباره همه جامعه نیستند؛ بیشتر نشانه‌هایی‌اند که در بعضی موقعیت‌ها دیده می‌شوند و باید با احتیاط درباره‌شان حرف زد.",
        "illustration": (
            "Inside the house, quiet small signs of wear: a cracked cup, a withered slate "
            "blue house plant, a window boarded with mismatched scraps, a dimmed lamp. Ochre "
            "figures sit among them without looking up, used to it. The fire in the middle "
            "has become smaller. Calm, observant, detailed composition."
        ),
    },
    {
        "slug": "ofogh-akhlaghi",
        "title": "کوتاه‌شدن افق اخلاقی",
        "body": "یکی از خطرناک‌ترین شکل‌های سازگاری فرساینده، کوتاه‌شدن افق اخلاقی است. وقتی آدم‌ها زیر فشار دائمی‌اند، گاهی فقط به عبور از امروز فکر می‌کنند. ممکن است فروشنده فشار بازار را به مشتری منتقل کند، کارفرما فشار بحران را به کارگر منتقل کند، خانواده فشار اقتصادی را به روابط عاطفی منتقل کند، یا آدم‌ها برای حفظ خودشان، دایره مسئولیت‌شان را کوچک‌تر کنند.",
        "illustration": (
            "A line of faceless ochre silhouettes, each one handing a heavy cold slate blue "
            "stone backwards to the person behind them, none of them turning to look. The "
            "last figure in the line bends low under the weight. Horizontal, rhythmic "
            "composition."
        ),
    },
    {
        "slug": "faghat-jib-nist",
        "title": "فقط جیب نیست",
        "body": "این‌جا مسئله فقط «اخلاق فردی» نیست. بحران اقتصادی فقط جیب مردم را خالی نمی‌کند؛ افق همکاری را هم کوتاه می‌کند.",
        "illustration": (
            "Seen from above at night: a circle of warm ochre firelight on the ground that "
            "was once wide enough for many figures has shrunk to a tight small circle around "
            "one figure. Other faceless figures stand just outside it in the cold slate blue "
            "dark. Minimal, stark composition."
        ),
    },
    {
        "slug": "fazilat-yani-che",
        "title": "فضیلت یعنی چه؟",
        "body": "از زاویه تکاملی و تمدنی، فضیلت فقط این نیست که فردی بتواند در کوتاه‌مدت خودش را نجات دهد. رفتاری فضیلت‌مند است که ظرفیت بقا، همکاری، یادگیری و آینده‌سازی یک جمع انسانی را بیشتر کند. اگر سازگاری باعث شود جامعه بتواند از هم مراقبت کند، منابعش را حفظ کند، خطاهایش را اصلاح کند و امکان آینده را نگه دارد، یک فضیلت اجتماعی است.",
        "illustration": (
            "Ochre faceless figures working together around the house: two carry fresh "
            "planks in to mend a gap in the wall, one tends the fire with branches gathered "
            "from outside, another kneels to plant a young sapling beside the door. Busy, "
            "cooperative, hopeful composition."
        ),
    },
    {
        "slug": "digar-fazilat-nist",
        "title": "وقتی دیگر فضیلت نیست",
        "body": "اما اگر سازگاری فقط به معنای نجات کوتاه‌مدت فرد یا گروه کوچک باشد، در حالی که اعتماد، همکاری، شایستگی، محیط زیست و امکان برنامه‌ریزی را فرسوده می‌کند، دیگر نمی‌شود آن را فضیلت دانست.",
        "illustration": (
            "One faceless ochre figure alone beside a large bright fire. Around it stand "
            "neighbouring houses, stripped bare to their skeleton frames and cold slate "
            "blue, their planks clearly gone into this one fire. Wide, uneasy composition."
        ),
    },
    {
        "slug": "tohi-az-daroon",
        "title": "تاب‌آوری از درون تهی می‌شود",
        "body": "این همان جایی است که تاب‌آوری از درون تهی می‌شود. ظاهرش هنوز ادامه‌دادن است؛ مردم هنوز کار می‌کنند، خرید می‌کنند، خانواده را می‌چرخانند، شوخی می‌کنند و زندگی را جلو می‌برند. اما زیر این ادامه‌دادن، چیزهایی آرام‌آرام مصرف می‌شوند. آدم‌ها کمتر به آینده فکر می‌کنند، کمتر به غریبه اعتماد می‌کنند، کمتر برای کیفیت عمومی می‌جنگند، و بیشتر به حلقه‌های کوچک خودشان پناه می‌برند.",
        "illustration": (
            "The house seen in cutaway: its upper floor looks normal, with warm ochre "
            "windows and figures going about daily life. But below them the floor beams "
            "and supports have almost all been burned away, leaving a hollow cold slate "
            "blue void under their feet. Quietly unsettling composition."
        ),
    },
    {
        "slug": "halgheh-koochak",
        "title": "پناه به حلقه‌های کوچک",
        "body": "البته این پناه‌بردن را هم نباید ساده قضاوت کرد. وقتی نهادها کار نمی‌کنند، وقتی آینده نامطمئن است، وقتی قانون و بازار و سیاست قابل پیش‌بینی نیستند، طبیعی است که آدم‌ها به خانواده، دوست، فامیل، آشنا یا شبکه‌های نزدیک‌تر تکیه کنند. این می‌تواند شکل مهمی از مراقبت باشد. اما اگر تنها شکل اعتماد همین حلقه‌های کوچک بماند، جامعه توان همکاری در مقیاس بزرگ‌تر را از دست می‌دهد. آن‌وقت چیزی که در کوتاه‌مدت امنیت می‌سازد، در بلندمدت جامعه را کوچک‌تر می‌کند.",
        "illustration": (
            "Seen from above at night: several small separate clusters of ochre figures, "
            "each huddled around its own tiny fire, with wide cold slate blue darkness "
            "between them. In the middle of the scene, a large shared hearth in an open "
            "square sits cold and unused. Wide, scattered composition."
        ),
    },
    {
        "slug": "farda-faghirtar",
        "title": "امروز می‌گذرد، فردا فقیرتر می‌شود",
        "body": "پس سازگاری فرساینده یعنی جامعه هنوز ادامه می‌دهد، اما با خرج‌کردن چیزهایی که نباید خرج می‌شدند. یعنی زندگی حفظ می‌شود، اما کیفیت زندگی پایین می‌آید. یعنی بحران مدیریت می‌شود، اما حساسیت نسبت به بحران کم می‌شود. یعنی امروز می‌گذرد، اما فردا فقیرتر می‌شود؛ نه فقط از نظر پول، بلکه از نظر اعتماد، توان، اخلاق همکاری، سلامت، محیط زیست و امکان خیال‌کردن آینده.",
        "illustration": (
            "The house at pale dawn: the fire is still alive and the ochre figures are "
            "still sitting around it — they made it through the night — but the house "
            "around them has been reduced to a few bare cold slate blue beams. Quiet, "
            "ambivalent composition."
        ),
    },
    {
        "slug": "porsesh",
        "title": "پرسش",
        "body": "در این معنا، پرسش اصلی دیگر این نیست که جامعه ایران چقدر تاب‌آور است. پرسش دقیق‌تر این است: این تاب‌آوری چه چیزی را حفظ کرده و چه چیزی را فرسوده است؟ اگر ادامه‌دادن، بدن و روان و اعتماد و آینده را مصرف کند، دیگر فقط نشانه قدرت نیست. نشانه نوعی سازگاری است که باید درباره‌اش نگران بود.",
        "illustration": (
            "A return to the cover's house, same cutaway angle but seen from very far back. "
            "It is now one of many small houses scattered across a cold slate blue night "
            "landscape; in every one a warm ochre fire burns, and every one has gaps in its "
            "walls. Vast, wide, layered composition."
        ),
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: اعتمادهای کوچک در جامعه کم‌اعتماد",
        "author": "بهمن رشادی",
        "body": "این بخش چهارم از نوشتار «زنده‌ماندن یا زیستن؟» بود. سازگاری وقتی ارزشمند است که امکان زندگی آینده را حفظ کند. اما وقتی برای عبور از امروز، آینده را خرج می‌کند، از تاب‌آوری به فرسایش تبدیل می‌شود. بخش بعد: اعتمادهای کوچک در جامعه کم‌اعتماد.",
        "illustration": (
            "Two neighbouring small houses at dusk. A faceless ochre figure from one house "
            "reaches across the gap between them to hand a fresh log to a figure in the "
            "other house's doorway. Warm ochre light spills from both doors. Warm, open, "
            "hopeful composition."
        ),
    },
], "05": [
    # Motif: small warm circles of people scattered on a vast cold plain with nothing
    # connecting them — trust that survives by staying close, but never bridges outward.
    {
        "slug": "cover",
        "tag": "بخش پنجم",
        "title": "اعتمادهای کوچک در جامعه کم‌اعتماد",
        "subtitle": "از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": "A wide cold slate blue open plain at dusk. Scattered across it are several small separate circles of faceless ochre silhouette figures, each circle huddled close and glowing warm around a tiny ochre fire. Large empty cold distances lie between the circles; no path, road or bridge connects any two of them. Wide composition, generous negative space.",
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": "A single small empty circle of flat stones on a cold slate blue plain at dusk, with no human figure. In its centre one small warm ochre flame glows quietly. Minimal, solemn, respectful composition.",
    },
    {
        "slug": "shekl-etemad",
        "title": "شکل اعتماد هم عوض می‌شود",
        "body": "یکی از چیزهایی که زیر فشار بحران‌های طولانی تغییر می‌کند، شکل اعتماد است. جامعه فقط با قیمت‌ها و کمبودها سازگار نمی‌شود؛ با نااطمینانی هم سازگار می‌شود. وقتی آینده روشن نیست، قانون قابل پیش‌بینی نیست، بازار آرام نیست، و نهادها نمی‌توانند حس امنیت عمومی بسازند، آدم‌ها ناچارند برای ادامه زندگی به جاهای نزدیک‌تر پناه ببرند: خانواده، دوست، فامیل، آشنا، همکار مطمئن، همسایه قابل‌اعتماد.",
        "illustration": "A cold slate blue open plain under a heavy sky. Lone faceless silhouette figures walk inward from the empty open space, each heading toward one of a few small warm ochre circles of people, where others are making room for them. Wide composition with movement from the cold edges toward the warm clusters.",
    },
    {
        "slug": "sarzanesh",
        "title": "نباید ساده سرزنشش کرد",
        "body": "این پناه‌بردن را نباید ساده سرزنش کرد. در بسیاری از موقعیت‌ها، همین اعتمادهای کوچک زندگی را نگه می‌دارند. قرض‌دادن، مراقبت از بچه، معرفی کار، ضمانت‌کردن، خبررسانی، کمک درمانی، خرید گروهی، جا دادن کسی در خانه، یا حمایت عاطفی در لحظه‌های سخت، همه از همین حلقه‌های نزدیک می‌آیند. اگر این شبکه‌ها نبودند، فشار بحران برای بسیاری از مردم سنگین‌تر می‌شد.",
        "illustration": "Close view inside one warm ochre circle of faceless silhouette figures sitting together. Hands pass things to one another across the circle: a bowl, a small child, a key, a blanket. One figure rests a hand on another's shoulder. The cold slate blue plain is visible only at the edges. Intimate, warm composition.",
    },
    {
        "slug": "habs",
        "title": "مسئله کجا شروع می‌شود",
        "body": "پس مسئله این نیست که اعتماد خانوادگی یا دوستانه بد است. مسئله از جایی شروع می‌شود که اعتماد در همین حلقه‌های کوچک حبس شود و نتواند به سطح عمومی‌تر جامعه گسترش پیدا کند.",
        "illustration": "One warm ochre circle of faceless figures on the cold plain, now enclosed by a low ring-shaped wall of cold slate blue stone that hugs the circle tightly. The warm glow stays inside the wall and does not reach the ground beyond it. Centered, still composition with wide empty space around.",
    },
    {
        "slug": "do-peyvand",
        "title": "دو نوع پیوند",
        "body": "رابرت پاتنام در بحث سرمایه اجتماعی میان دو نوع پیوند تفاوت می‌گذارد: پیوندهای درون‌گروهی و پیوندهای پل‌ساز. پیوندهای درون‌گروهی آدم‌های شبیه‌تر و نزدیک‌تر را به هم وصل می‌کنند؛ خانواده، دوستان نزدیک، گروه‌های آشنا. پیوندهای پل‌ساز اما آدم‌ها و گروه‌هایی را به هم وصل می‌کنند که شبیه هم نیستند یا از یک حلقه نمی‌آیند.",
        "ref": "بر پایه‌ی کتاب «بولینگ به‌تنهایی» نوشته‌ی رابرت پاتنام (۲۰۰۰)",
        "illustration": "Two scenes side by side on the cold plain. On one side, a closed tight ring of similar faceless ochre figures holding hands facing inward. On the other side, a narrow warm ochre footbridge spans a cold slate blue gap and links two clusters of figures that are visibly different in size and posture. Balanced diptych composition.",
    },
    {
        "slug": "zirsakht",
        "title": "اعتماد، زیرساخت همکاری",
        "body": "جامعه‌ای که فقط پیوندهای نزدیکش را نگه می‌دارد، شاید در بقا قوی باشد، اما در همکاری عمومی ضعیف می‌شود. پاتنام سرمایه اجتماعی را به شبکه‌ها، اعتماد و رابطه‌هایی وصل می‌کند که زندگی جمعی را ممکن می‌کنند؛ یعنی اعتماد فقط احساس شخصی نیست، زیرساخت همکاری است.",
        "illustration": "Many faceless ochre silhouette figures together raise one long heavy roof beam onto two tall posts, a structure far too large for any small group to lift alone. Under the beam the ground is warm; beyond it the plain is cold slate blue. Wide, upward-reaching composition.",
    },
    {
        "slug": "nazdik-va-door",
        "title": "نزدیک‌ها و دورها",
        "body": "در ایران، این تفاوت را می‌شود در تجربه روزمره حس کرد. ممکن است آدم به خانواده یا دوست نزدیک اعتماد کند، اما در معامله با غریبه، کار اداری، همکاری کاری، مشارکت جمعی یا رابطه با نهادها محتاط، بدبین یا دفاعی باشد. این فقط ویژگی اخلاقی افراد نیست؛ واکنشی است به محیطی که در آن خطا، سوءاستفاده، بی‌ثباتی و بی‌پاسخ‌ماندن زیاد تجربه شده است.",
        "illustration": "A single faceless silhouette figure seen in profile, standing between two worlds: the side of its body facing a small warm ochre circle of people is open and relaxed, glowing warm; the side facing the vast cold slate blue plain is hunched, arm raised defensively, in cold shadow. Split, tense composition.",
    },
    {
        "slug": "yekdast-nist",
        "title": "اعتماد یک‌دست نیست",
        "body": "مطالعات مربوط به سرمایه اجتماعی در تهران هم اعتماد را در سطوح مختلف سنجیده‌اند؛ از خانواده و خویشاوندان و دوستان تا همسایگان، همکاران، هم‌قوم و هم‌مذهب، و عموم مردم. همین تفکیک نشان می‌دهد که اعتماد یک چیز یک‌دست نیست؛ آدم‌ها ممکن است در حلقه نزدیک اعتماد داشته باشند، اما نسبت به دایره‌های دورتر محتاط باشند.",
        "ref": "بر پایه‌ی پژوهشی درباره‌ی سرمایه‌ی اجتماعی و سطوح اعتماد در تهران",
        "illustration": "Seen from above: concentric rings of faceless silhouette figures standing on the plain. The innermost small ring is deep warm ochre; each ring further out fades step by step to cooler tones, and the outermost wide ring is cold slate blue with figures spaced far apart. Graphic, symmetrical composition.",
    },
    {
        "slug": "yek-nafar-dakhel-edareh",
        "title": "«یک نفر داخل اداره»",
        "body": "تجربه‌هایی که ممکن است در خودمان یا اطرافیانمان دیده باشیم: کار را به آشنا سپردن، دنبال «یک نفر داخل اداره» گشتن، خرید از کسی که معرفی شده، ترجیح فامیل به غریبه، کمک‌گرفتن از رابطه به‌جای روند رسمی. این‌ها را نمی‌شود یک‌سره فساد یا عقب‌ماندگی نامید. گاهی راه‌هایی‌اند برای کم‌کردن ریسک. اما همین راه‌های بقا، اگر دائمی و فراگیر شوند، به تدریج شایستگی، عدالت و اعتماد عمومی را تضعیف می‌کنند.",
        "illustration": "A large cold slate blue official building with one closed service window and a long weary queue of faceless figures waiting in front of it. To the side, a small warm ochre side door stands ajar, and one figure slips through it, led by a hand reaching out from inside. Wide composition with the queue stretching away.",
    },
    {
        "slug": "blat",
        "title": "آینه‌ای از روسیه",
        "body": "آلنا لدنوا در مطالعه خود درباره شبکه‌های غیررسمی در روسیه شوروی و پساشوروی، از پدیده‌ای به نام «بلات» حرف می‌زند؛ شبکه‌ای از رابطه‌ها، لطف‌ها و آشنایی‌ها که مردم برای دسترسی به کالا، خدمات یا امکان‌هایی استفاده می‌کردند که از مسیر رسمی دشوار یا نامطمئن بود. این نمونه عین ایران نیست، اما برای ما آینه خوبی است.",
        "ref": "بر پایه‌ی کتاب آلنا لدنوا درباره‌ی «اقتصاد لطف‌ها» در روسیه (۱۹۹۸)",
        "illustration": "A web of thin warm ochre threads passed hand to hand between many faceless figures, winding around the outside of a large cold slate blue building instead of going through its locked front door. Small parcels travel along the threads. Intricate yet calm composition.",
    },
    {
        "slug": "emrooz-farda",
        "title": "امروز حل، فردا فرسوده",
        "body": "وقتی سیستم رسمی ناکارآمد یا غیرقابل‌اعتماد می‌شود، رابطه‌های غیررسمی فقط حاشیه زندگی نیستند؛ به بخشی از روش زندگی تبدیل می‌شوند. آن‌ها در کوتاه‌مدت مشکل را حل می‌کنند، اما در بلندمدت می‌توانند همان سیستمی را که به آن بی‌اعتمادیم، بیشتر غیرقابل‌اعتماد کنند.",
        "illustration": "The same large cold slate blue building, now with wide cracks running up its walls. Dense warm ochre threads wrap around it like roots around a stone, and where they pull tightest the cracks are widest. Faceless figures keep passing parcels along the threads. Quiet, ominous composition.",
    },
    {
        "slug": "peyvand-zaeef",
        "title": "قدرت پیوندهای ضعیف",
        "body": "مارک گرانووتر در نظریه «قدرت پیوندهای ضعیف» نکته مهمی دارد: پیوندهای ضعیف، یعنی رابطه‌هایی که به اندازه خانواده و دوست نزدیک صمیمی نیستند، می‌توانند گروه‌های مختلف جامعه را به هم وصل کنند و اطلاعات، فرصت و همکاری را از یک حلقه به حلقه دیگر ببرند. اگر اعتماد فقط در حلقه‌های کوچک بماند، جامعه از درون چندپاره می‌شود.",
        "ref": "بر پایه‌ی مقاله‌ی مارک گرانووتر (۱۹۷۳)",
        "illustration": "Several small warm ochre circles of faceless figures far apart on the cold plain, loosely stitched together by long, very thin warm ochre lines held by single figures standing between circles. Along the lines, small lights travel from one circle to another. Airy, network-like wide composition.",
    },
    {
        "slug": "dayereh-tang",
        "title": "دایره‌ی اعتماد تنگ می‌شود",
        "body": "بحران اقتصادی فقط جیب مردم را خالی نمی‌کند؛ دایره اعتماد را هم کوچک می‌کند. وقتی آدم‌ها دائماً نگران فردا هستند، کمتر ریسک اعتماد به غریبه را می‌پذیرند. وقتی منابع کم می‌شود، رقابت خشن‌تر می‌شود. وقتی تجربه بی‌عدالتی تکرار می‌شود، آدم‌ها به‌جای قواعد عمومی، دنبال مسیرهای خصوصی‌تر می‌گردند.",
        "illustration": "One warm ochre circle of faceless figures pressed tightly shoulder to shoulder, backs turned outward. A faint wider ring traced on the ground shows where the circle used to stand; the cold slate blue plain has crept inward over it. Small in a large empty frame.",
    },
    {
        "slug": "do-chehreh",
        "title": "دو چهره",
        "body": "این وضعیت دو چهره دارد. یک چهره‌اش مثبت است: خانواده، دوستی و شبکه‌های نزدیک مثل ضربه‌گیر اجتماعی عمل می‌کنند. اما چهره دیگرش نگران‌کننده است: اگر اعتماد فقط به نزدیکان محدود شود، همکاری عمومی سخت می‌شود. کار جمعی دشوارتر می‌شود. نهادهای مدنی ضعیف‌تر می‌شوند. شایستگی جای خود را به رابطه می‌دهد.",
        "illustration": "A circle of faceless figures split down the middle: on the left half, warm ochre figures shield one another under a sheltering curve like an umbrella against falling cold rain; on the right half, the same circle's outer edge has hardened into a cold slate blue wall turned toward the empty plain. Symmetric, two-sided composition.",
    },
    {
        "slug": "mahaye-koochak",
        "title": "«ما»های کوچک",
        "body": "جامعه به جای اینکه از «ما»ی گسترده‌تر ساخته شود، به مجموعه‌ای از «ما»های کوچک و محتاط تبدیل می‌شود. مردم هنوز از هم مراقبت می‌کنند، اما بیشتر از کسانی که می‌شناسند. هنوز کمک می‌کنند، اما در دایره‌هایی که می‌توانند کنترل کنند. هنوز همکاری می‌کنند، اما بیشتر وقتی طرف مقابل از قبل آزموده شده، معرفی شده، یا به حلقه‌ای آشنا وصل است.",
        "illustration": "Seen from a high angle: a wide plain filled with many small separate circles of faceless figures, each circle facing inward and glowing faint warm ochre, with cold slate blue ground between them. No circle faces another. Pattern-like, repetitive wide composition.",
    },
    {
        "slug": "ostrom",
        "title": "با توصیه‌ی اخلاقی ساخته نمی‌شود",
        "body": "الینور اوستروم در کارهایش درباره حکمرانی منابع مشترک نشان داد که همکاری پایدار فقط با نیت خوب ساخته نمی‌شود. مردم وقتی بهتر همکاری می‌کنند که قواعد روشن، نظارت قابل‌اعتماد، امکان مشارکت در تصمیم‌ها، سازوکار حل اختلاف و برخورد تدریجی با سوءاستفاده وجود داشته باشد. جامعه برای اعتمادکردن به غریبه‌ها، به نهاد، قاعده و تجربه‌های تکرارشونده از انصاف نیاز دارد.",
        "ref": "بر پایه‌ی پژوهش الینور اوستروم درباره‌ی حکمرانی منابع مشترک (نوبل اقتصاد ۲۰۰۹)",
        "illustration": "A shared well in the middle of a field, marked out by simple clear stone boundary lines. Faceless ochre figures who came from different small circles take turns drawing water, and the warm field around the well is tended together, contrasting with the cold slate blue plain beyond. Orderly, calm composition.",
    },
    {
        "slug": "dopahloo",
        "title": "دوباره دوپهلو",
        "body": "این همان جایی است که سازگاری دوباره دوپهلو می‌شود. اعتمادهای کوچک جامعه را در بحران نگه می‌دارند، اما اگر جای اعتماد عمومی را بگیرند، جامعه را کوچک‌تر می‌کنند. حلقه‌های نزدیک، زندگی را نجات می‌دهند؛ اما اگر تنها پناهگاه باقی بمانند، امکان ساختن آینده مشترک ضعیف می‌شود.",
        "illustration": "A return to the cover's scene, same dusk light but seen from very far back and high up: hundreds of tiny warm ochre circles scattered like embers across a vast cold slate blue plain that stretches to the horizon, with nothing connecting them. Vast, wide, layered composition.",
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: ناسازگاری به‌عنوان نیروی اصلاح",
        "author": "بهمن رشادی",
        "body": "این بخش پنجم از نوشتار «زنده‌ماندن یا زیستن؟» بود. اعتماد کوچک، شکل مهمی از بقاست؛ اما جامعه برای آینده فقط به خانواده و آشنا نیاز ندارد. به اعتماد میان غریبه‌ها هم نیاز دارد. بخش بعد: ناسازگاری به‌عنوان نیروی اصلاح.",
        "illustration": "Two small warm ochre circles of faceless figures on the cold plain at dusk. One figure from each circle has stepped out and together they lay the last plank of a short warm ochre footbridge across the cold gap between them. Warm, open, hopeful composition.",
    },
], "06": [
    # Motif: warm sprouts breaking through cracks in a vast cold paved ground; at first
    # alone, then their roots meet underground into a network — dissent that becomes capacity.
    {
        "slug": "cover",
        "tag": "بخش ششم",
        "title": "ناسازگاری به‌عنوان نیروی اصلاح",
        "subtitle": "از نوشتار «زنده‌ماندن یا زیستن؟»",
        "author": "بهمن رشادی",
        "body": "",
        "illustration": "A vast flat expanse of cold slate blue paving stones stretching to the horizon at dusk. In the middle, from a single thin crack, one small warm ochre sprout with two leaves has pushed up through the stone. Wide composition, generous empty space around the sprout.",
    },
    {
        "slug": "taghdim",
        "tag": "تقدیم",
        "body": "این نوشته را به یاد کسانی آغاز می‌کنم که به زنده‌ماندن بسنده نکردند. کسانی که بخشی از زندگی، آرامش، یا حتی جان خود را گذاشتند تا زیستن برای دیگران ممکن‌تر شود: زیستن با کرامت، با انتخاب، با آینده‌ای که بشود برایش برنامه ریخت. آن‌هایی که نامشان را می‌دانیم. آن‌هایی که نامشان در شلوغی روزها گم شده. و آن‌هایی که هنوز در دل زندگی روزمره ما ادامه دارند.",
        "illustration": "A single open hand, drawn as a simple faceless silhouette, held palm up against a cold slate blue background. In the centre of the palm rests one small warm ochre seed. Minimal, solemn, respectful composition.",
    },
    {
        "slug": "do-niroo",
        "title": "دو نیرو، دو کار",
        "body": "اگر سازگاری برای ادامه‌دادن لازم است، ناسازگاری برای اصلاح لازم است. جامعه‌ای که هیچ‌وقت سازگار نمی‌شود، زیر فشارهای طولانی از هم می‌پاشد؛ اما جامعه‌ای که همیشه سازگار می‌شود، کم‌کم توان تشخیص خطا را از دست می‌دهد.",
        "illustration": "Two plants side by side on cold slate blue paving. On the left, a dry brittle plant that has snapped and cracked apart. On the right, a pale faded plant lying perfectly flat, pressed under a heavy slab of stone, its colour drained away. Balanced two-part composition.",
    },
    {
        "slug": "har-nasazegari",
        "title": "هر ناسازگاری‌ای خوب نیست",
        "body": "مسئله این نیست که ناسازگاری همیشه خوب است. ناسازگاری کور، پراکنده، عصبی یا صرفاً تخریبی می‌تواند خودش بخشی از فرسایش باشد. اما نوعی از ناسازگاری هست که کارکرد اصلاحی دارد: یادآوری می‌کند که وضعیت موجود، طبیعی و نهایی نیست.",
        "illustration": "Cold slate blue paving. On one side, a jagged shattered patch of broken stone fragments with nothing growing in it. On the other side, a clean thin crack from which a healthy warm ochre sprout grows upright. Clear contrast, calm composition.",
    },
    {
        "slug": "faghat-khiaban-nist",
        "title": "فقط خیابان نیست",
        "body": "در این معنا، ناسازگاری فقط اعتراض خیابانی یا مخالفت سیاسی مستقیم نیست. گاهی در حفظ یک استاندارد دیده می‌شود؛ در نپذیرفتن تحقیر؛ در اصرار بر کیفیت؛ در روایت‌کردن تجربه‌ای که زبان رسمی نمی‌خواهد ببیند؛ در سبک زندگی؛ در بدن؛ در طنز؛ در هنر؛ در نپذیرفتن دروغی که قرار است عادی شود.",
        "illustration": "A cold slate blue wall meeting a paved sidewalk. From many different small cracks in the wall and the pavement grow different warm ochre plants: a small flower, a tuft of grass, a curling leaf, a tiny vine. Each is different, scattered across the frame. Wide, rhythmic composition.",
    },
    {
        "slug": "moghavemat-roozmareh",
        "title": "شکل‌های روزمره‌ی مقاومت",
        "body": "جیمز سی. اسکات از «شکل‌های روزمره مقاومت» حرف می‌زند؛ یعنی رفتارهای کوچک و غیرقهرمانانه‌ای که الزاماً شبیه انقلاب نیستند، اما نشان می‌دهند مردم کاملاً با نظم مسلط یکی نشده‌اند. نباید فقط دنبال لحظه‌های بزرگ ناسازگاری بگردیم؛ بخشی از فاصله جامعه با وضعیت، در رفتارهای خرد و روزمره نگه داشته می‌شود.",
        "ref": "بر پایه‌ی کتاب «سلاح‌های ضعیفان» نوشته‌ی جیمز سی. اسکات (۱۹۸۵)",
        "illustration": "Cross-section close view just beneath cold slate blue paving stones: a thin warm ochre root quietly finding its way through the gaps beneath the stones, slowly lifting one stone edge by a hair. Quiet, patient, detailed composition.",
    },
    {
        "slug": "har-raftar",
        "title": "هر رفتار متفاوتی مقاومت نیست",
        "body": "هر رفتار متفاوتی مقاومت نیست. هر شوخی‌ای اعتراض نیست. اگر همه چیز را مقاومت بنامیم، مفهوم مقاومت را بی‌معنا می‌کنیم. بهتر است بگوییم این‌ها می‌توانند نشانه‌هایی باشند از این‌که جامعه هنوز تماماً با وضعیت یکی نشده است. هنوز فاصله‌ای هست؛ هنوز زبان دیگری هست.",
        "illustration": "Several loose dry leaves scattered on cold slate blue paving, lying on the surface without roots. Among them, only one small warm ochre leaf is actually rooted, growing from a crack. Sparse, still composition.",
    },
    {
        "slug": "zendegi-dar-haghighat",
        "title": "زندگی در حقیقت",
        "body": "واسلاو هاول در «قدرت بی‌قدرتان» از «زندگی در حقیقت» حرف می‌زند. منظور او این نبود که هر شهروند باید قهرمان سیاسی شود. بحثش ساده‌تر و عمیق‌تر بود: در نظامی که از مردم می‌خواهد در نمایش رسمی شرکت کنند، گاهی خودداری از تکرار آن نمایش، شکلی از قدرت است.",
        "ref": "بر پایه‌ی متن «قدرت بی‌قدرتان» نوشته‌ی واسلاو هاول (۱۹۷۸)",
        "illustration": "A long straight row of identical pale cold slate blue plastic pots holding identical stiff artificial plants. In the middle of the row, one pot holds a real living warm ochre plant, slightly irregular and alive. Repetitive, frontal composition.",
    },
    {
        "slug": "noskhe-tekrari",
        "title": "نسخه‌ی تکراری نیست",
        "body": "این ایده را نباید مستقیم و ساده به ایران منتقل کرد. اما یک شباهت تحلیلی وجود دارد: نظم‌های ایدئولوژیک فقط با زور کار نمی‌کنند؛ از مردم می‌خواهند در زبان، مناسک، تصویرها و روایت‌های رسمی هم مشارکت کنند. در چنین وضعیتی، ناسازگاری گاهی یعنی آدم‌ها اجازه ندهند زبان رسمی، همه تجربه زیسته‌شان را تصاحب کند.",
        "illustration": "A tall wall covered edge to edge with identical blank cold slate blue rectangular posters (no text on them). From a torn corner of one poster, a warm ochre vine has pushed out and begun to climb. Flat, frontal composition.",
    },
    {
        "slug": "aine-orupa",
        "title": "آینه‌ی اروپای شرقی",
        "body": "تجربه اروپای شرقی برای ما آینه مقایسه‌ای است، نه نسخه آماده. بعضی جامعه‌ها توانستند سریع‌تر خود را بازسازی کنند، بعضی دچار فساد، پوپولیسم، مافیا، بی‌اعتمادی یا اقتدارگرایی تازه شدند. تفاوت در این هم بود که جامعه زیر فشار چه چیزهایی را حفظ کرده بود: نهادهای مستقل، حافظه مقاومت، شبکه‌های اعتماد، زبان انتقادی، تجربه سازمان‌یابی و توان همکاری.",
        "illustration": "Two plots of ground side by side after snow has melted, with patches of cold slate blue snow still at the edges. The left plot is green-ochre again with new growth, and a cutaway shows living roots kept alive under the soil. The right plot is bare, with no roots beneath. Two-part comparative composition.",
    },
    {
        "slug": "linz-stepan",
        "title": "فقط تغییر حکومت نیست",
        "body": "خوان لینتس و آلفرد استپان می‌گویند عبور از رژیم غیردموکراتیک فقط به تغییر حکومت یا برگزاری انتخابات وابسته نیست. چند میدان باید ظرفیت داشته باشند: جامعه مدنی، جامعه سیاسی، حاکمیت قانون، دستگاه اداری مؤثر، و اقتصادی که کاملاً در قدرت سیاسی حل نشده باشد. ناسازگاری وقتی نیروی اصلاح می‌شود که بتواند از واکنش فردی به ظرفیت اجتماعی تبدیل شود.",
        "ref": "بر پایه‌ی کتاب خوان لینتس و آلفرد استپان درباره‌ی گذار و تثبیت دموکراتیک (۱۹۹۶)",
        "illustration": "A young warm ochre tree shown with a cutaway of the ground beneath it: five distinct, strong main roots spread out in different directions, each firmly anchored. Cold slate blue stone surrounds the soil. Centered, grounded composition.",
    },
    {
        "slug": "lahestan",
        "title": "نمونه‌ی لهستان",
        "body": "در لهستان، اعتراض و سازمان‌یابی اجتماعی، به‌ویژه تجربه جنبش همبستگی، فقط در فروپاشی نظم کمونیستی نقش نداشت؛ پس از آن هم بر تثبیت دموکراتیک اثر گذاشت. خشم اجتماعی اگر به شبکه، حافظه، سازمان، مطالبه و زبان مشترک تبدیل نشود، زود مصرف می‌شود؛ اما اگر این ظرفیت‌ها را بسازد، می‌تواند بعداً بخشی از بازسازی باشد.",
        "ref": "بر پایه‌ی پژوهش گژگوش اکی‌یرت و یان کوبیک درباره‌ی جامعه‌ی مدنی لهستان (۱۹۸۹–۱۹۹۳)",
        "illustration": "Two fires on cold slate blue ground at night. On the left, a quick flare of loose straw already collapsing into grey ash. On the right, a fire built from carefully stacked logs, burning steady and warm ochre, with faceless figures sitting around it. Side-by-side comparison.",
    },
    {
        "slug": "iran",
        "title": "ناسازگاری در ایران",
        "body": "در ایران، ناسازگاری در سال‌های اخیر فقط در سیاست رسمی دیده نشده؛ در زندگی روزمره، در سبک پوشش، در بدن، در رابطه با اینترنت، در مهاجرت، در طنز، در هنر، در زبان نسل‌ها، در روایت زنان از خودشان، در حساسیت نسبت به تحقیر، در تلاش برای حفظ استانداردهای شخصی و حرفه‌ای هم دیده شده است. این‌ها را نباید بیش از اندازه رمانتیک کرد. اما همه‌شان یک چیز را نشان می‌دهند: جامعه هنوز کاملاً با عادی‌سازی بحران یکی نشده است.",
        "illustration": "A dense Middle Eastern city like Tehran seen from high above in cold slate blue: low and mid-rise flat-roofed concrete apartment blocks packed close together, narrow streets, and a long snow-capped mountain range rising behind the city. No skyscrapers, no rooftop water towers, no Western landmarks. Here and there, in cracks of streets, flat rooftops, balconies and walls, small warm ochre and green patches of growth appear, scattered across the whole city. Wide aerial composition.",
    },
    {
        "slug": "neshane-ta-zarfiat",
        "title": "از نشانه تا ظرفیت",
        "body": "اگر فقط به شکل خشم پراکنده بمانند، فرسوده می‌شوند. اگر فقط به مهاجرت فردی تبدیل شوند، بخشی از انرژی جامعه از کشور خارج می‌شود. اگر فقط در شوخی و کنایه بمانند، ممکن است بحران را قابل‌تحمل‌تر کنند، اما الزاماً آن را تغییر نمی‌دهند. اما اگر به زبان دقیق، شبکه‌های اعتماد، همکاری مدنی، مطالبه روشن، اخلاق حرفه‌ای، حافظه جمعی و نهادهای کوچک تبدیل شوند، می‌توانند نقش اصلاحی پیدا کنند.",
        "illustration": "A cross-section of the ground. Above, on cold slate blue paving, several separate warm ochre sprouts stand apart from each other. Below the surface, their thin roots reach out sideways and begin to meet and intertwine into a single network. Layered composition, surface above and roots below.",
    },
    {
        "slug": "fazilat",
        "title": "فضیلت تکاملی",
        "body": "ناسازگاری‌ای که فقط ویران کند، فقط تحقیر کند، فقط نفی کند، یا فقط فرد را از جمع جدا کند، لزوماً فضیلت نیست. اما ناسازگاری‌ای که خطا را نشان دهد، دروغ را عادی نکند، استاندارد زندگی را پایین‌تر از حد انسانی نپذیرد، امکان همکاری را حفظ کند و جامعه را به اصلاح خود وادار کند، یک نیروی حیاتی است.",
        "illustration": "A warm ochre plant that has pushed one cold slate blue paving stone aside. In the opened patch of soil next to it, several smaller new sprouts are now growing, sheltered by the first plant. Warm, generous composition.",
    },
    {
        "slug": "har-do-niroo",
        "title": "هر دو نیرو",
        "body": "جامعه به هر دو نیرو نیاز دارد: سازگاری برای زنده‌ماندن، ناسازگاری برای سالم‌ماندن. نقطه دشوار، نگه‌داشتن هر دو است: ادامه‌دادن بدون تسلیم کامل؛ فاصله‌گرفتن بدون فروپاشی؛ اعتراض بدون از دست‌دادن توان همکاری؛ و حفظ زندگی بدون عادی‌کردن چیزی که نباید عادی شود.",
        "illustration": "A single tall warm ochre reed bending in a strong cold slate blue wind, curved but not broken, its roots firmly anchored in the ground and its tip turned upward toward a warm light. Dynamic yet balanced composition.",
    },
    {
        "slug": "tashkhis-khata",
        "title": "دستگاه تشخیص خطا",
        "body": "ناسازگاری یعنی جامعه هنوز دستگاه تشخیص خطا دارد. هنوز می‌تواند بگوید این کیفیت زندگی کافی نیست. این زبان رسمی همه حقیقت نیست. این تحقیر طبیعی نیست. این آینده کوچک‌شده نباید سرنوشت قطعی باشد.",
        "illustration": "A dark cold slate blue space beneath heavy paving stones. A thin beam of warm light falls through a narrow crack above, and a small pale sprout below bends and stretches toward that beam. Dark, focused composition with one line of light.",
    },
    {
        "slug": "faghat-na-nagooyad",
        "title": "فقط «نه» نگوید",
        "body": "ناسازگاری وقتی نیروی اصلاح می‌شود که فقط «نه» نگوید؛ بلکه چیزی را حفظ کند که جامعه برای بازسازی آینده به آن نیاز دارد: اعتماد، زبان مستقل، حافظه، سازمان، استاندارد اخلاقی و توان همکاری.",
        "illustration": "A return to the cover's scene, same dusk light but seen from farther back: dozens of warm ochre sprouts growing from cracks across the vast cold slate blue paving, and a cutaway along the bottom edge shows their roots joined underground into one continuous network. Vast, wide, layered composition.",
    },
    {
        "slug": "payan",
        "title": "ادامه دارد…",
        "subtitle": "بخش بعد: مرز باریک؛ از تحمل تا امکان تغییر",
        "author": "بهمن رشادی",
        "body": "این بخش ششم از نوشتار «زنده‌ماندن یا زیستن؟» بود. جامعه به هر دو نیرو نیاز دارد: سازگاری برای زنده‌ماندن، ناسازگاری برای سالم‌ماندن. بخش بعد: مرز باریک؛ از تحمل تا امکان تغییر.",
        "illustration": "The same vast paved ground at sunset. In its middle, the cold slate blue paving has been split open and a small living warm ochre garden grows there, with a few faceless figures tending it together. Warm, open, hopeful composition.",
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
            # Shrink body text until the panel clears the footer (long slides overflowed it).
            page.evaluate("""() => {
                const b = document.querySelector('.body');
                const last = document.querySelector('.panel').lastElementChild;
                if (!b || !last) return;
                let fs = 33;
                while (last.getBoundingClientRect().bottom > 1270 && fs > 24) {
                    fs -= 1;
                    b.style.fontSize = fs + 'px';
                }
            }""")
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
