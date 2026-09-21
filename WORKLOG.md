# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

---

## 2026-09-21 — Drafted section 3 («اقتصاد») of the «زنده‌ماندن یا زیستن؟» carousel

### What this session produced

Bahman asked for "part 3 for Instagram" — the third per-section carousel, built from
`sections/04-eghtesad-roshantarin-meydan-tabavari.md` (the usual N → N+1 file mapping).
Text for all 18 slides, the source lines, and all 18 English illustration prompts were
written, reviewed with him, and committed into `gen_ig_slides.py` under a new `"03"` key.
**Only slide 1 (the cover) was rendered**; the other 17 are deliberately not generated yet,
following the same one-at-a-time review rhythm as sections 1 and 2.

Full slide-by-slide plan, run commands, and remaining steps: `instagram-plan.md`, section
«بخش ۳ — «اقتصاد»».

### The numbers were deliberately cut from slide 4 — and that forced slide 5 to change

The first draft of slide 4 carried the article's World Bank / IMF figures verbatim (2.7%
GDP contraction, −6.1% growth, 68.9% consumer inflation). Flagged in review that a forecast
number on a standalone Instagram slide, stripped of the article's framing, reads as a
statement of current fact no matter how carefully the «برآورد کرده» / «پیش‌بینی کرده» hedges
are preserved. Bahman chose to drop them.

Two consequences worth knowing before anyone re-edits that slide:

- The IMF's entire contribution to this section was those two forecast numbers, so its name
  came out of the source line too — it would otherwise credit a source whose content is no
  longer on the slide. If the numbers ever go back, the IMF goes back into the source line.
- Slide 5 opened with «اما نکته اصلی این نوشتار عددها نیست» and was titled «نکته، عددها
  نیست» — a sentence and a title whose only job was to dismiss numbers that no longer
  appear anywhere in the deck. Both were cut (title is now «مردم منتظر نمی‌مانند»). This is
  the general shape of the hazard: cutting a slide's content can leave a *later* slide
  referring to something the reader never saw.

### Section 3's visual motif: a room whose ceiling keeps lowering

Section 1 was the fork in the road, section 2 was the facade and what shows through it.
Section 3 is a side-cutaway room whose cold slate blue ceiling slab descends across the
deck while warm ochre figures keep rearranging themselves to fit under it.

Chosen over a set of scales, a well with a falling water level, and an emptying shopping
basket because it is the only one that carries *both* faces of the section's argument at
once — the clever rearranging is the practical intelligence the article insists must not be
belittled, and the steadily lower ceiling is the erosion. It is also the section's own
closing image («عادت‌کردن به زندگی‌ای که مدام کوچک‌تر می‌شود»), and it needs no readable
text, which the generator's prompt forbids outright.

### Two mechanical things that cost time

- **A Cyrillic `е` (U+0435) ended up inside a slug** (`fesharе-mohit`), which would have
  produced a filename no `<slug>` CLI argument could ever match. Caught by `cat -A` before
  any render. Worth an ASCII check on new slugs — the two characters are visually identical
  in a monospace editor.
- **Playwright's chromium cache was empty again** (`chromium_headless_shell-1234` missing),
  the same recurring blocker as 2026-09-13. Fixed with
  `scripts/.venv/bin/python -m playwright install chromium`. Note the failure is harmless to
  the budget: `draw_illustration()` runs *before* the browser launches, so the gpt-image-2
  call had already completed and cached its PNG — the re-run after the install drew nothing
  new.

### Also committed: section 2's untracked output

Section 2's rendered slides, cached illustrations and caption file
(`images/PanorAIma/surviving-or-living/instagram/section-02/`,
`ig-illustrations/section-02/`, `section-02-caption.txt`) had never been committed even
though that carousel published on 2026-09-17. They went in with this commit. The article is
published, so the old draft-stage gitignore lines no longer apply to these paths.

---

## 2026-09-17 — Generated and published section 2 of the «زنده‌ماندن یا زیستن؟» carousel

### What this session produced

Followed on directly from the drafting session below (same day). Bahman asked for the cover
image first, then to generate the rest of the deck, then to add a dedication slide, then to
send the finished deck to Telegram for manual posting. End state: **all 17 images generated,
sent to the project's Telegram channel, and Bahman posted the carousel manually to
@25mordad** — confirmed live via the Graph API (`graph.instagram.com/me/media`): a
`CAROUSEL_ALBUM` with 17 children, `timestamp: 2026-09-17T10:52:09+0000`,
https://www.instagram.com/p/DdYsFqqgopm/.

**Resolved same day:** the API response's `caption` field initially came back empty for this
post. Bahman fixed it directly on Instagram; re-checked via the Graph API and the caption now
returns in full, matching `section-02-caption.txt` exactly (including hashtags).

### `gen_ig_slides.py` was parameterized for multiple sections (previously hardcoded to section 1)

- `SLIDES` became `SLIDES_BY_SECTION = {"01": [...], "02": [...]}`; run with
  `gen_ig_slides.py [slug] [section]` (section defaults to `01`, so section 1 usage is
  unchanged).
- `ILLUS_DIR`/`OUTPUT_DIR` became per-call `illus_dir`/`output_dir` derived from the section
  arg; section 1's illustrations stay flat in `ig-illustrations/` (untouched, backward
  compatible), section 2+ get their own `ig-illustrations/section-<NN>/` subfolder.
- `TOTAL` (the "n/16" footer count) is no longer a fixed constant — it's `len(slides)` for
  whichever section is running, since section 2 ended up at 17 slides, not 16.

**Real bug found and fixed in the same session:** the temp HTML file Playwright renders from
(`tmp = ILLUS_DIR / f"_tmp-{nn}.html"`) was left pointing at the old global `ILLUS_DIR` even
after the illustration path itself was parameterized. Since the HTML references its image by
relative filename only, the first section-2 cover render silently loaded section 1's cached
`01-cover.png` (the desert fork-in-the-road image) instead of the freshly generated urban
street illustration — no error, just the wrong picture. Fixed by pointing `tmp` at the local
`illus_dir` param. Anyone touching this script again for section 3+ should know this class of
bug is easy to reintroduce if a new path gets parameterized without checking every reference
to the old global.

### Section 2's illustration briefs were translated from `instagram-plan.md`'s Farsi

The plan file only had Farsi scene descriptions (`تصویر: ...`); gpt-image-2 needs English
prompts in the same "warm ochre / cold slate blue" vocabulary as section 1's briefs, so each
of the 15 content-slide illustrations was translated/adapted into that vocabulary rather than
copied verbatim — this is not yet reflected back into `instagram-plan.md` itself, which still
only shows the original Farsi briefs.

### Dedication ("تقدیم") slide added after the fact, not in the original plan

`instagram-plan.md`'s section-2 plan never included a تقدیم slide — that was section 1 only.
Bahman asked mid-session to add the same dedication text as section 1 (illustration adapted to
section 2's own facade/alley visual language instead of reusing section 1's desert-road image),
inserted as slide 2, pushing the deck from 16 to 17 slides. This required renumbering every
already-generated file (both the cached `ig-illustrations/section-02/*.png` and the rendered
`instagram/section-02/*.jpg`) up by one index, then deleting and re-rendering just the *text
layer* of all 17 jpgs so the "n/17" footer count is correct everywhere — no illustrations were
redrawn except the new dedication slide's, so this cost exactly one extra `gpt-image-2` call,
not sixteen.

### Known cosmetic issue on slide 13 ("دو جهان معنا"), left as-is at Bahman's call

Its body text + reference line together overflow the panel and visually overlap the
`25Mordad.com` / page-number footer. Flagged mid-session; Bahman reviewed both this slide and
the next one and said both were fine, so no fix was applied — recorded here in case it comes up
again later.

### Credential-leak guard applied again this session

This machine's shell had stale `OPENAI_API_KEY`, `TELEGRAM_BOT_TOKEN`, `IG_ACCESS_TOKEN`, and
`IG_BUSINESS_ACCOUNT_ID` values left over from a different project (same class of incident as
the 2026-08-13 Dornyx/@25mordad mix-up below) — confirmed by comparing suffixes against this
repo's own `.env` before every gpt-image-2, Telegram, and Instagram Graph API call, and
unsetting the shell's copy per call so `load_dotenv()` picked up this repo's real value instead.

---

## 2026-09-17 — Drafted section 2 of the «زنده‌ماندن یا زیستن؟» Instagram carousel (text + illustration briefs)

### What this session produced

Bahman asked to start section 2 of the per-section carousel, and specifically asked for the
**slide text first** so the illustrations can be commissioned against approved copy rather than
the other way round. Output is a full 16-slide draft (text, per-slide illustration brief,
caption) appended to `files/PanorAIma/surviving-or-living/instagram-plan.md` under
«بخش ۲ — زندگی روزمره». **Nothing was generated and nothing was published** — no `gpt-image-2`
call was made, so this session cost no image-API money.

Source section: `sections/03-zendegi-rouzmareh-jayi-mian-kenaramadan-va-fasele-gereftan.md`.

### Section-number ↔ file-number mapping (easy to get wrong)

The published "بخش اول" carousel is **`sections/02-tabavari-ya-adi-sazi.md`**, not `01-`.
`00-daramad.md` and `01-zendegi-ke-ba-bohran-tanzim-shode.md` are not posted at all, per the
plan's own post list. So carousel section N = section file N+1. Section 2 = file `03-`.

### First draft was written on Sonnet, then re-checked on Opus at Bahman's request

The Opus pass caught things worth recording, because they generalize to every future deck:

- **Two illustration briefs were impossible to render.** The generator's `STYLE` prompt forbids
  text/letters outright, but two briefs leaned on letterforms (speech bubbles, a typed line vs.
  a handwritten line) to carry their metaphor. Any brief whose meaning depends on *reading*
  something is dead on arrival — the metaphor has to survive with zero glyphs.
- **Slide bodies had drifted into paraphrase.** The format's rule is that slide prose is the
  article's own approved sentences, shortened or reordered — not rewritten. The first pass had
  quietly paraphrased in several places; the Opus pass put the article's sentences back.
- **Two load-bearing nuances had been compressed out** and were restored to their own slides:
  «سکوت، رضایت نیست» (silence is cost calculation, not consent) and «هر شوخی مقاومت نیست»
  (don't call every joke resistance). These are exactly the qualifications that keep the post
  from reading as a slogan.
- **Source lines were in the rejected academic format** and were rewritten to the approved
  «بر پایه‌ی …» form. Two of the three references (Scott, Barry) had also landed on
  back-to-back slides; they were separated.
- **The cover title was too long** — the full section title «زندگی روزمره؛ جایی میان کنارآمدن و
  فاصله‌گرفتن» wraps to three lines at the cover's 86px weight. Split into title
  «زندگی روزمره» + subtitle carrying the rest.

### New convention: each section gets its own recurring visual motif

Section 1's deck was built on the fork («راه باز به افق» vs «حلقه‌ی بسته»). Section 2 is built
on **«نما و پشتِ نما»** — a cold uniform facade with warm life visible through its gaps, under
its ground line, or behind it. The cover establishes it and the penultimate slide returns to
the cover image, mirroring how section 1's «معیار» slide returned to its fork. The three-color
palette stays fixed across all sections; only the motif changes.

### Bahman's decisions this session

- Greek diglossia example (کاتارووسا/دیموتیکی) was cut in the Opus draft for brevity, then
  **restored on his request** — slide 9 now carries both the Arabic and Greek examples.
- Still open for his approval: whether to keep «اسلام سیاسی» (the article's own wording) on
  slide 12 of a public post, and whether to hold at 16 slides (manual upload, as section 1) or
  trim to 10 for API publishing.

### Terminal can't render Persian

Worth noting for future sessions in this repo: the chat terminal mangles Persian script, so a
long Persian review block pasted there is unreadable to Bahman — he answered a full slide
table with a single «چی؟». Persian drafts need to go to a file he opens, or to Telegram.

---

## 2026-08-13 — Incident: «مذهب» Story republished to the wrong Instagram account (Dornyx, not @25mordad)

### What happened

Bahman deleted the live «مذهب» Story and asked (via a late Telegram reply, msg 1117) to
regenerate and republish it. Investigated from a sibling yaroo session (interactive, not the
usual unattended `/photo-beshno` bridge) — confirmed `gpt-image-2` deterministically blocks
this photo's typography edit (children in frame, known limitation, see decision #3 below), kept
the existing Playwright fallback graphic, and ran `retry_story_publish.py` to republish it.
It posted to **Dornyx's** Instagram account instead of `@25mordad`. Bahman had to notice it on
the wrong account and ask why.

### Root cause

Not a bug in this repo's code — `IG_ACCESS_TOKEN` in this repo's own `.env` was, and still is,
correctly `@25mordad`'s token. The session that ran `retry_story_publish.py` had a *different*,
already-set `IG_ACCESS_TOKEN` (Dornyx's) directly in its shell environment, from an
unidentified source. `python-dotenv`'s `load_dotenv()` never overrides an already-set env var,
so the script silently used the shell's leaked value instead of this repo's correct `.env`
value. Same mechanism as an earlier Telegram-token leak in that other session (documented
2026-08-12), just a different credential this time — full incident writeup and the general
fix lives in the yaroo repo's `WORKLOG.md` (2026-08-13 entry) and memory
`feedback_shell_env_telegram_token_leak.md`, since the contamination is a property of that
session's shell, not of this repo.

### Fix

Republished correctly to `@25mordad` with the contaminated vars explicitly stripped
(`env -u IG_ACCESS_TOKEN ...`), verified via the Graph API's own `/me` that the token in use
actually resolves to `@25mordad` before trusting it, and verified the new Story media_id
resolves under that same token. Also added a defined procedure to `photo-beshno.md` for
"regenerate an already-posted Story" requests (previously undefined — root cause of the
original msg-1117 stall before this account mix-up even happened) and fixed an unrelated real
bug found along the way: Playwright's Chromium browser was never installed in this repo's
`scripts/.venv` on the voidloop mini PC.

### Pending / TODO

- [ ] Consider having `publish_story_for_asset()`/`publish_feed_photo()` in `lr_common.py`
      assert the token's `/me` username matches an expected `IG_EXPECTED_USERNAME` (or similar)
      from `.env` before publishing, rather than relying on whoever runs the script to remember
      to check for shell contamination first — this incident wasn't caught by anything in code
- [ ] Source of the leaked credentials in the yaroo session's shell is still unidentified

---

## 2026-08-12 — Built and automated the Lightroom→Instagram photo pipeline end-to-end via Telegram

### What we built

| Feature | Files |
|---|---|
| Adobe Lightroom OAuth + fetch/publish scripts (P1.9 base) | `scripts/lr_auth.py`, `lr_refresh_token.py`, `lr_common.py`, `lr_list_album.py`, `lr_fetch_photo.py`, `lr_publish_photo.py` |
| First live post («یارو») | published to `@25mordad`, verified live |
| Full Telegram-driven automation: title pick → story pick → schedule confirm → auto-advance | `.claude/commands/photo-beshno.md`, `scripts/telegram_send.py`, sibling repo's `handle_photo_pipeline_trigger.py` |
| GPT-image-2 quality enhance + moderation fallback | `scripts/gpt_enhance_photo.py`, `scripts/image_common.py` |
| Per-photo Story typography graphics (bespoke prompt per photo) + video with music | `scripts/gpt_story_typography.py`, `scripts/make_story_video.py`, `assets/audio/dunya-bozorgtar-theme.mp3` |
| Scheduled auto-publish | `scripts/lr_check_schedule.py`, hourly cron at `:23` |
| Manual Telegram trigger keyword | `عکس‌بشنو` / `photobeshno`, handled in the sibling repo |

### Decisions

#### 1. Reuse a sibling private repo's Telegram bot instead of a new dedicated one
**Why:** Bahman's explicit call — one bot/chat to manage, not two. But two independent
`getUpdates` consumers on the same bot token steal each other's updates (confirmed real bug
in that repo's own remote-trigger handler), so this repo can never run its own consumer.
**How:** Sending goes through the sibling repo's `notify_telegram.py` (subprocess); receiving
is a new file in that repo (`handle_photo_pipeline_trigger.py`) that writes a handoff into
this repo's `images/ig-queue/_inbox/` and launches `claude -p "/photo-beshno"` here. Neither
that repo's name nor its filesystem path is ever hardcoded or named in this **public** repo —
caught during an explicit pre-commit review pass Bahman asked for, not on the first pass.

#### 2. Story-drafting is Persian-only until picked, and delegated to an Opus subagent
**Why:** Translating every offered option to English before Bahman even picks one was wasted
effort (his own feedback, live). Separately, he wants the actual creative Persian prose running
at a higher model tier than this skill's mechanical steps (fetch, prompts, scheduling) — same
Sonnet-for-mechanical/Opus-for-prose split already used elsewhere.
**How:** Story options are drafted Persian-only via an Agent-tool subagent pinned to `opus`;
translation to English happens only once, when building the final caption after a pick.

#### 3. gpt-image-2 moderation blocks photos with children — accepted, not fought
**Why:** OpenAI's output moderation hard-rejected the very first real photo tried (two
children) for both the quality-enhance and the story-typography steps. Confirmed this
recurs, not a fluke. Rewording the prompt to route around a safety system is not something
to attempt.
**How:** Both `gpt_enhance_photo.py` and `gpt_story_typography.py` retry once (cheap, and a
real transient failure would succeed on retry), then fall back to a non-AI path: an
optimize-only copy of the source for the feed photo, and a Playwright + real Vazirmatn-font
overlay (same guaranteed-correct-Persian-text method already used everywhere else in this
repo) for the Story graphic. Never thematic in the fallback case — accepted as a real,
permanent downgrade for that subset of photos, not a bug to keep chasing.

#### 4. Story-graphic visual style: bespoke per-photo prompt, atmospheric over template
**Why:** The first Story design (photo + flat bottom gradient box + centered text) was
functionally fine but explicitly rejected as "not creative enough." A second attempt tying
the visual mood directly to that photo's chosen story (dusty golden-hour light + faint
footprints for یارو's "walks the same path" story) was accepted — then a third attempt, after
more feedback, went further: reframing the composition itself (tiny figure in a vast painterly
landscape) to visually *embody* the series tagline rather than just decorate the photo with it.
**How:** `gpt_story_typography.py` now requires a bespoke `--prompt` every call — the skill
must never call it with the generic default. See memory `feedback_story_visual_style.md`.

#### 5. Scheduling default: start tomorrow, not "~1 week out"
**Why:** The skill's first cut defaulted new posts to ~7 days out, extrapolated from an
earlier "keep the queue ~1 week ahead" remark about *drafting* lead time. Bahman corrected
this live: posting should start **tomorrow** and go roughly daily, sequential — the 1-week
comment was about always having a week of drafted photos in reserve, not about delaying the
first post by a week.
**How:** `photo-beshno.md` now proposes tomorrow (or the day after the latest scheduled post)
by default, with a general-best-practice time until real post-performance stats exist.

#### 6. Queue-of-one auto-advance must never be skipped, not even "just this once"
**Why:** Mid-session, a concurrent automated run and a manual intervention collided; rather
than working through it, the schedule-confirm step was closed out with "I'll send the next
photo whenever" instead of immediately continuing to the next photo in the same run. Nothing
else was ever going to restart the pipeline — it only runs in response to a reply to its own
prior message — so it just sat idle until Bahman noticed and asked.
**How:** Manually restarted the pipeline for photo 3, and hardened `photo-beshno.md`'s
language: the auto-advance step is unconditional, every time, no exceptions.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Telegram's `getUpdates` offset is one shared cursor — no partial-ack | A side message interleaved between two pipeline replies used to stall the whole pipeline (the trigger script stopped scanning at the first non-match and handed the rest to a downstream skill with no write access here). Fixed: safe-to-skip text messages are skipped past; only genuinely unsafe content (photos, reactions) still hard-stops the scan. |
| Headless `claude -p` runs hit interactive permission prompts mid-task | One automated run got stuck asking for Edit-tool approval it could never receive, silently stalling a reply. Root cause identified (this repo lacks the `Skill(fewer-permission-prompts)` grant the sibling repo already has) but the fix itself — broadening this repo's own permissions — was correctly blocked by Claude Code's auto-mode safety classifier as a self-permission-grant; applied only after Bahman explicitly approved it via a direct question. |
| Adobe's Lightroom rendition API only serves up to 2048px, no original/master | Verified live rather than assumed — `lr_fetch_photo.py` now documents this rather than guessing at a larger size that doesn't exist. |
| gpt-image-2 output at ~3MB+, this repo's images run ~300-500KB | `image_common.optimize_jpeg()`, shared between the enhance and story-typography scripts. |

### Pending / TODO

- [ ] Refresh-token lifetime for Lightroom still unverified — re-check around 2026-08-25
- [ ] Consider whether `lr_check_schedule.py`'s hourly cron needs a same-day catch-up path if the mini PC is offline when a `scheduled_for` slot passes
- [ ] Watch whether gpt-image-2's moderation block on photos-with-children is truly deterministic or has real variance (two data points so far, inconsistent)
- [ ] P1.8 Instagram Stories automation subtasks — still open, untouched this session (see TASKS.md)
- [ ] P2: peoples-of-iran Instagram feed carousel post — still open, untouched this session
- [ ] P3: third article "زنده‌ماندن یا زیستن؟" — still open, untouched this session

---

## 2026-08-11 — Planned Lightroom → Instagram Feed photo pipeline; migrated project to the mini PC

### What we planned (no code written yet)

A new, separate pipeline from the PanorAIma article system: curate a series of personal photos
in a Lightroom (cloud/CC) album, get an AI-written bilingual caption for each, and have them
drip out to the `@25mordad` Instagram Feed automatically every couple of days. Full design is
in `TASKS.md` under **P1.9** — this entry covers the *why* behind the decisions.

### Decisions

#### 1. Feed posts only for now, Stories deferred
**Why:** Instagram's Stories API has no caption field at all — there's no way to attach the
"cool story" text to a Story slide without either a compositing step (burn text onto the image)
or giving up on text entirely. That's a real design fork, not a small detail, so it was
explicitly parked for a later session rather than guessed at.
**How:** Only Feed posts are in scope for the first build. Story support is still on the
roadmap (P1.9 in TASKS.md) once the text-on-Story question gets its own design pass.

#### 2. Photos get committed to git, not uploaded to external object storage
**Why:** An existing internal pattern for Instagram publishing (elsewhere on this machine)
uploads media to Cloudflare R2 at publish time instead of committing it. Considered that here,
but the user pointed out 25mordad.com is already a fully public repo with every other site
image committed straight into `images/` — adding a second storage mechanism just for this one
pipeline would be inconsistent with zero benefit.
**How:** New photos land in `images/ig-queue/`, committed like everything else, served by
Cloudflare Pages the same way the PanorAIma image folders already are.

#### 3. Drafting and posting are split into two phases
**Why:** Writing a caption requires actually looking at the photo — that can't run unattended
inside a scheduled job. Every other script in this repo's automation is purely mechanical
(HTTP calls, no AI-in-the-loop at run time), and the posting scheduler should keep that
property rather than becoming the one exception.
**How:** Drafting happens interactively in a session (batch-caption a new stack of curated
photos, calibrate tone on the first one, approve the rest). Posting is a separate, dumb,
scheduled script that only ever picks the oldest `approved` item and posts it — never drafts.

#### 4. Reusing existing patterns instead of building from scratch
**Why:** Before designing this from zero, checked what already exists elsewhere on this
machine for Instagram publishing and for getting the user's approval outside of a chat
session. Found a mature, already-working publish flow (status-gated record per post, always
previews before publishing, requires a typed confirmation, single-image/carousel/video all
handled) and a working Telegram-based approval channel (bot sends a message, a 👌/👎 emoji
reaction on it resolves back to what it was approving).
**How:** Adapting both patterns rather than reinventing them — the publish gate/preview/confirm
shape, and Telegram as an alternative approval path to the existing story cards' in-session
review. Kept out of this public repo's docs by name/path (see below) since they live in other,
unrelated private projects — only the *pattern* is documented here, not where it came from.

#### 5. Migrated the project to the mini PC (`voidloop`)
**Why:** The user is consolidating several personal/business projects onto an always-on home
mini PC instead of running them ad hoc from the laptop — this project was next on that list,
and better to move it now, before the new Instagram/Lightroom scheduler exists, so the cron
only ever gets set up once, in its final home.
**How:** Followed the existing migration runbook (`rsync`, not `git clone` — this repo has
gitignored state that matters: `.env`, the still-private third-article draft, `.claude/`
project settings). Full checklist and verification in the runbook; laptop copy stays untouched
and canonical until the mini PC copy is proven stable.

### Pending / TODO

- [ ] P1.9 rollout subtasks (Adobe Developer Console setup, Lightroom OAuth, fetch/publish
      scripts, Telegram approval wiring) — see TASKS.md, nothing built yet
- [ ] Continue future 25mordad.com sessions from the mini PC copy, not this laptop session
- [ ] Everything already pending from the 2026-08-09 entry (third-article friend review, P1.8
      Instagram token refresh, P2 carousel post) is still open and untouched this session

---

> Older entries archived in WORKLOG_ARCHIVE.md
