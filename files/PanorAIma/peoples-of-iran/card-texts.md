# Card Texts — مردمان ایران (Peoples of Iran)

Copy deck for the 16 section **Instagram story cards**. One card per article section,
posted to Instagram every couple of days. Each card's job is to **convey the main idea
of that section** in a single story — a self-contained taste of the concept. The card body
stands on its own; a short, **non-repeating CTA** then invites the reader to the full
article (the actual link/sticker is placed on the story later, not baked into the image).
`gen_section_cards.py` reads this file and renders one card per block over the background
photo, exporting to `images/PanorAIma/peoples-of-iran/<slug>.png`.

Purpose note: these are concept-delivery stories. We do **not** ask the audience to comment.
The body carries the section's core idea on its own; the **cta** only nudges them to read more.

## Format

Each block starts with `## <n> — <slug>` (the slug is the output PNG filename) and
carries these labelled lines:

- **label:** the gold section label (Persian ordinal — بخش اول، دوم، …)
- **title:** the white card title. Use `<br>` to control the line break.
- **body:** the section's core idea, ~3–6 short lines, self-contained. `<br>` allowed.
- **ref:** *(optional)* a faint one-line source credit, rendered small under the body.
  Only present where a single named thinker anchors the section **and** there's room —
  per the rule "mention the ref only when char limits allow," many cards omit it.
- **cta:** a short, **different-every-time** phrase encouraging the reader to open the
  full article. The clickable link is attached on the story afterwards.
- **music:** 3 concept-fit candidate tracks for the story audio, ★ = recommended.
  Instrumental / Persian classical / folk / cinematic — no language limit. Pick one when posting.

## Shared elements (same on every card — set in the script, not here)

- Byline context: نوشته‌ی بهمن رشادی، در گفت‌وگو با هوش‌واره
- Footer site: 25Mordad.com
- Footer tagline: فراتر از قاب
- Background: `bg-d.png` (dark, preferred)

---

## 1 — everyone-their-own-people
- **label:** بخش اول
- **title:** هرکس از مردم<br>خودش حرف می‌زند
- **body:** همه از «مردم» حرف می‌زنند؛<br>مردم می‌خواهند، مردم خسته‌اند.<br>اما هیچ‌کس همه‌ی مردم را نمی‌بیند.<br>هرکس فقط بخشی را می‌بیند<br>که برایش آشناست —<br>و همان را جای کل می‌گذارد.
- **ref:** بندیکت اندرسون: ملت، یک «جماعت خیالی» است.
- **cta:** متن کامل این بحث را در «فراتر از قاب» بخوان
- **music:**
  - ★ Kayhan Kalhor — *I Will Not Stand Alone* (kamancheh; a single voice insisting it isn't alone — perfectly ironic for the section)
  - Hossein Alizadeh — *Ney Nava* (a solitary reed against the ensemble)
  - Max Richter — *On the Nature of Daylight* (aching, universal)

## 2 — disagreement-to-social-worlds
- **label:** بخش دوم
- **title:** اختلاف بر سر نظر نیست،<br>بر سرِ خودِ واقعیت است
- **body:** دو نفر از یک رویداد حرف می‌زنند،<br>اما از دو جهان سخن می‌گویند.<br>تفاوت‌ها فقط از عقیده نمی‌آیند؛<br>از جایگاهِ زندگی می‌آیند:<br>پول، شهر، خانواده، رسانه، ترس.
- **ref:** پی‌یر بوردیو: نگاه ما از دل موقعیت اجتماعی ساخته می‌شود.
- **cta:** این فقط آغاز بحث است — ادامه‌اش را بخوان
- **music:**
  - ★ Ludovico Einaudi — *Experience* (two layers building side by side, never quite merging)
  - Ólafur Arnalds — *Near Light*
  - Nils Frahm — *Says*

## 3 — ethnicity-memory-layer
- **label:** بخش سوم
- **title:** قومیت، لایه‌ی حافظه است،<br>نه همه‌ی داستان
- **body:** قومیت هنوز هست:<br>در زبان، موسیقی، رنج و تعلق.<br>اما دیگر به‌تنهایی نمی‌گوید<br>مردمان ایران چگونه زندگی می‌کنند.<br>گاهی دو نفر از دو قوم،<br>به هم نزدیک‌ترند تا دو هم‌قوم.
- **cta:** چرا قومیت دیگر همه‌چیز نیست؟ در نوشتار بخوان
- **music:**
  - ★ Kayhan Kalhor & Erdal Erzincan — *Night Silence Desert* (memory, desert, lineage)
  - Rastak Ensemble — regional folk medley (Iranian peoples in one breath)
  - Ardavan Kamkar — santur solo (Kurdish-rooted, nostalgic)

## 4 — pluralism-beyond-iran
- **label:** بخش چهارم
- **title:** هر ملتِ مدرن<br>از مردمانِ متفاوت ساخته شده
- **body:** هر ملت مدرن از مردمانی متفاوت ساخته شده.<br>ترکیه، پاکستان، روسیه، اروپا —<br>هرکدام به شکل خود چندپاره‌اند.<br>مسئله این نیست که ایران تنهاست؛<br>مسئله ترکیبِ خاصِ اوست:<br>تاریخ، زبان، انقلاب، مهاجرت، بی‌اعتمادی.
- **cta:** مقایسه‌ی ایران با جهان را کامل بخوان
- **music:**
  - ★ Yo-Yo Ma & Silk Road Ensemble — *Ascending Bird* / Silk Road pieces (many traditions, one stage)
  - Anouar Brahem — oud (cross-regional, world)
  - Ludovico Einaudi — *Nuvole Bianche*

## 5 — lifestyle-visible-surface
- **label:** بخش پنجم
- **title:** سبک زندگی فقط سلیقه نیست؛<br>نشانه‌ی چیزهای عمیق‌تر است
- **body:** سبک زندگی فقط مصرف و سلیقه نیست.<br>نشانه‌ی چیزهای عمیق‌تر است:<br>پول، آموزش، شهر، دین، رسانه، امنیت.<br>«زندگی عادی» برای همه یک معنا ندارد —<br>و همین، یکی از شکاف‌های ماست.
- **ref:** پی‌یر بوردیو: سبک زندگی، بازتابِ موقعیت اجتماعی است.
- **cta:** لایه‌های پنهانش را در نوشتار ببین
- **music:**
  - ★ Nils Frahm — *Says* (a bright surface over a deep drone)
  - Bonobo — *Kerala* (instrumental, modern urban texture)
  - Tigran Hamasyan — *Markos & Markos*

## 6 — lifestyle-as-engine-of-change
- **label:** بخش ششم
- **title:** سبک زندگی،<br>گاهی موتورِ تغییر است
- **body:** آدم‌ها سبک زندگی را فقط به ارث نمی‌برند.<br>گاهی آن را می‌بینند، می‌خواهند،<br>و برای رسیدن به آن، خود را تغییر می‌دهند.<br>سبک زندگی فقط «آنچه هست» نیست؛<br>«آنچه باید بشود» هم هست — یک وعده.
- **ref:** لئون فستینگر: ما خود را مدام با دیگران می‌سنجیم.
- **cta:** این تغییر را کامل دنبال کن
- **music:**
  - ★ Ludovico Einaudi — *Experience* (the build = the pull toward another life)
  - Hans Zimmer — *Time*
  - Ólafur Arnalds — *re:member*

## 7 — university-social-media-contact
- **label:** بخش هفتم
- **title:** وقتی زندگیِ دیگران<br>پیشِ چشمت می‌آید
- **body:** تا وقتی فقط جهانِ خودت را ببینی،<br>همان را طبیعی‌ترین شکلِ زندگی می‌دانی.<br>دانشگاه و شبکه‌های اجتماعی<br>زندگی‌های دیگر را پیش چشمت آوردند.<br>اما دیدن، همیشه توانستن نیست —<br>گاهی فقط میل را بیشتر می‌کند.
- **cta:** بقیه‌ی ماجرا را در «فراتر از قاب» بخوان
- **music:**
  - ★ Tycho — *Awake* (movement, contact, the buzz of mixing worlds)
  - Bonobo — *Kiara*
  - GoGo Penguin — *Hopopono*

## 8 — media-collapse-single-narrative
- **label:** بخش هشتم
- **title:** روایتِ واحد فرو ریخت،<br>حقیقتِ مشترک نیامد
- **body:** رسانه فقط خبر نمی‌دهد؛ وزن می‌دهد.<br>وقتی انحصارِ روایت شکست،<br>جای آن را حقیقتِ مشترک نگرفت —<br>روایت‌های رقیب نشستند.<br>مسئله گاهی کمبودِ خبر نیست؛<br>زیادیِ روایت است.
- **ref:** مک‌کامبز و شاو: رسانه تعیین می‌کند به چه فکر کنیم.
- **cta:** تحلیل کاملِ رسانه را از دست نده
- **music:**
  - ★ Hildur Guðnadóttir — *Chernobyl* suite (collapse, dread, broken signal)
  - Jóhann Jóhannsson — *The Sun's Gone Dim* (a single narrative dissolving)
  - Max Richter — *Infra 5*

## 9 — evolutionary-ingroup-bias
- **label:** بخش نهم
- **title:** چرا هرکس<br>مردمِ خودش را می‌بیند؟
- **body:** هیچ‌کس «مردم» را نمی‌بیند؛<br>ما همیشه نمونه‌هایی را می‌بینیم.<br>ذهنِ انسان برای جامعه‌های میلیونی ساخته نشده.<br>پس «مردم» برای هرکس می‌شود<br>همان‌هایی که می‌شناسد و می‌فهمد.
- **ref:** رابین دانبار: توانِ ما برای رابطه‌ی مستقیم، محدود است.
- **cta:** چراییِ این محدودیت را کامل بخوان
- **music:**
  - ★ Hans Zimmer — *Dune (Paul's Dream)* (deep, tribal, pre-modern)
  - Dead Can Dance — *The Host of Seraphim*
  - Armand Amar — *Home* score

## 10 — from-differences-to-knots
- **label:** بخش دهم
- **title:** با این همه تفاوت،<br>چه چیزی هنوز ما را به هم وصل می‌کند؟
- **body:** دیدنِ تفاوت‌ها، نیمه‌ی اولِ ماجراست.<br>ایران نه یک مردمِ یکدست است،<br>نه جزیره‌هایی کاملاً جدا.<br>پرسشِ مهم‌تر این است:<br>با این همه تفاوت،<br>چه چیزی هنوز ما را به هم گره می‌زند؟
- **cta:** این گره‌ها را در نوشتار بشناس
- **music:**
  - ★ Zoë Keating — *Optimist* (looped cello literally weaving itself into knots)
  - Ólafur Arnalds — *Saman*
  - Sohrab Pournazeri — *Toranj* (interlacing Persian strings)

## 11 — shared-suffering
- **label:** بخش یازدهم
- **title:** رنجِ مشترک،<br>میدانِ مشترک — نه اتحاد
- **body:** تورم، درمان، مهاجرت، بی‌اعتمادی<br>بر همه اثر می‌گذارند،<br>اما نه یکسان، نه با یک معنا.<br>رنجِ مشترک خودبه‌خود اتحاد نمی‌سازد؛<br>میدانِ مشترک می‌سازد —<br>و گاهی شکاف را عمیق‌تر می‌کند.
- **cta:** چرا رنجِ مشترک ما را متحد نمی‌کند؟ بخوان
- **music:**
  - ★ Kayhan Kalhor — *The Silent City* (written after Halabja; collective grief)
  - Mohammad Reza Shajarian — *Morghe Sahar* (vocal; the anthem of shared suffering)
  - Henryk Górecki — *Symphony No. 3, II*

## 12 — from-pain-to-connection
- **label:** بخش دوازدهم
- **title:** از رنج<br>به پیوند
- **body:** رنج به‌تنهایی همکاری نمی‌سازد.<br>لازم نیست آدم‌ها شبیه هم باشند<br>تا به هم کار بدهند و مراقبت کنند.<br>جامعه فقط با شباهت نمی‌ماند؛<br>با هزاران رابطه‌ی کوچکِ قابل اتکا می‌ماند.
- **ref:** داگلاس نورث: نهادها، قواعدِ بازیِ زندگیِ مشترک‌اند.
- **cta:** پس چه چیزی ما را وصل می‌کند؟ بخوان
- **music:**
  - ★ Ludovico Einaudi — *Una Mattina* (small, warm, human connection)
  - Yann Tiersen — *La Valse d'Amélie*
  - Ólafur Arnalds — *Lag Fyrir Ömmu*

## 13 — persian-language-shared-field
- **label:** بخش سیزدهم
- **title:** فارسی؛ میدانِ مشترکِ<br>گفت‌وگو و سوءتفاهم
- **body:** فارسی فقط زبانِ توافق نیست؛<br>زبانِ اختلاف هم هست.<br>برای بسیاری، هم امکان است هم فشار.<br>اما شاید یکی از آخرین میدان‌هایی باشد<br>که مردمانِ متفاوت هنوز در آن<br>یکدیگر را خطاب می‌کنند — حتی وقتی قانع نمی‌شوند.
- **cta:** درباره‌ی نقشِ زبانِ فارسی بیشتر بخوان
- **music:**
  - ★ Mohammad Reza Lotfi — solo setar (the Persian tongue distilled to a string)
  - Mohammad Reza Shajarian — *Bidad* (Homayoun; voice carried by Persian poetry)
  - Ali Ghamsari — *Bird of Dawn* (contemporary tar)

## 14 — economy-practical-cooperation
- **label:** بخش چهاردهم
- **title:** اقتصاد؛ میدانِ عملیِ<br>همکاری میانِ تفاوت‌ها
- **body:** اقتصاد فقط رنج تولید نمی‌کند؛<br>رابطه هم تولید می‌کند.<br>فروشنده لازم نیست سبکِ زندگیِ خریدار را بپسندد.<br>نیازِ متقابل، آدم‌های ناشبیه را<br>دورِ یک میز می‌نشاند —<br>اگر قاعده و اعتماد باشد.
- **ref:** مارک گرانوتر: اقتصاد در دلِ روابطِ اجتماعی تنیده است.
- **cta:** نقشِ اقتصاد را کامل بخوان
- **music:**
  - ★ Rastak Ensemble — up-tempo folk (the rhythm of regions trading, working together)
  - Bushehri neyanbān / port folk (trade-port pulse)
  - Niyaz — *Beni Beni* (groove built on exchange)

## 15 — family-kinship-forced-contact
- **label:** بخش پانزدهم
- **title:** خانواده؛<br>تماسِ اجباری با دیگری
- **body:** در رسانه، آدم‌ها زود «آن‌ها» می‌شوند.<br>اما در خانواده، همان «آن‌ها»<br>عمو، خواهر، پدر و دخترخاله‌اند.<br>خانواده اختلاف را حل نمی‌کند،<br>اما نمی‌گذارد «دیگری» بی‌چهره شود.
- **cta:** این بخشِ خواندنی را از دست نده
- **music:**
  - ★ Iranian *لالایی* (lullaby) — instrumental arrangement (kinship across generations)
  - Yann Tiersen — *Comptine d'un autre été*
  - Ludovico Einaudi — *Nuvole Bianche*

## 16 — intertwined-lives
- **label:** بخش شانزدهم
- **title:** مردمانِ متفاوت،<br>زندگی‌هایِ درهم‌تنیده
- **body:** شاید «مردمِ واحد» وجود نداشته باشد،<br>اما ایران جزیره‌های جدا هم نیست.<br>سرزمینی از مردمانِ متفاوت<br>که زندگی‌هاشان به هم گره خورده.<br>فهمِ این گره‌ها،<br>شاید اولین قدمِ زبانی تازه باشد.
- **ref:** به تعبیرِ بندیکت اندرسون، ملت یک «جماعت خیالی» است.
- **cta:** جمع‌بندیِ کامل را در «فراتر از قاب» بخوان
- **music:**
  - ★ Kayhan Kalhor & Brooklyn Rider — *Ascending Bird* (separate voices rising into one)
  - Sohrab Pournazeri — *Toranj*
  - Zbigniew Preisner — *Lacrimosa*
