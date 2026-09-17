# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

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
