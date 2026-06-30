# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

---

## 2026-07-01 — Set up Instagram API access + published first test Story via API

### What we built

| Feature | Files |
|---|---|
| Meta app for Instagram API access (Instagram Login flow) | none (Meta dashboard only) |
| Long-lived access token, stored locally | `.env` (gitignored, not committed) |
| Python automation scripts folder | `scripts/.venv/` (gitignored venv), `scripts/requirements.txt` |
| Token verification script | `scripts/test_ig_token.py` |
| Story publish script (container create → poll → publish) | `scripts/publish_story.py` |
| Updated ignore rules | `.gitignore` (`.env`, `scripts/.venv/`) |

### Decisions

#### 1. Use Instagram API with Instagram Login, not Facebook Login
**Why:** The Facebook-login-based Graph API setup was blocked on creating/linking a Facebook Page (logged as a blocker in the 2026-06-16 sessions). The newer "Instagram API with Instagram Login" product authenticates directly against the Instagram Business/Creator account and does **not** require a Facebook Page at all.
**How:** Built the Meta app using "API setup with Instagram login," added the account as a tester, and generated the token from that flow. This resolves the P1.8 blocker entirely — see [[project_ig_automation]].

#### 2. Generate the token from the dashboard, not via OAuth redirect exchange
**Why:** Tokens generated through the App Dashboard's "Generate token" button for a tester account come back long-lived (~60 days) already — no separate short-to-long-lived token exchange step needed.
**How:** Used the in-dashboard "Generate token" action; confirmed via API call that it returns valid profile data.

#### 3. Required permissions were already "Ready for testing" — no App Review needed
**Why:** In Development mode, an app's own tester accounts get granted core permissions (basic profile, comments, messages, insights, **content publish**) without going through Meta's App Review process. Only extra permissions like `business_management`/`ads_management` (not needed here) require additional verification.
**How:** Confirmed all five needed permissions show "Ready for testing" status on the Permissions and features page before generating the token.

#### 4. Store the token in project-root `.env`, not an external path
**Why:** User preference — keep it inside the repo (the conventional, easy-to-find location) rather than `~/.config/...`. Safe as long as `.gitignore` excludes `.env` *before* the file is created, which was verified.
**How:** Added `.env` to `.gitignore` first, confirmed it wasn't already tracked, then wrote the token there. Old external copy deleted.

#### 5. Python automation lives in its own `scripts/` folder with its own venv
**Why:** Keeps Instagram-automation Python tooling (requests-based, dashboard-driven) separate from the per-article Playwright generator scripts that already live under `files/PanorAIma/<slug>/`. Avoids polluting the project's Node/Tailwind toolchain with Python deps.
**How:** `scripts/.venv/` (gitignored) + `scripts/requirements.txt` for reproducibility. Run scripts via `scripts/.venv/bin/python scripts/<script>.py`.

#### 6. Story card images are served directly from `25mordad.com` — no separate hosting needed
**Why:** The Instagram Content Publishing API requires a publicly reachable `image_url`. Checked with a HEAD request and confirmed `images/PanorAIma/<slug>/stories/*.jpg` already returns 200 from the live site, so no extra image host/CDN step is needed.
**How:** `curl -sI https://25mordad.com/images/PanorAIma/peoples-of-iran/stories/everyone-their-own-people.jpg` → `200 image/jpeg`.

#### 7. End-to-end test: published a real Story via the API
**Why:** Validate the full publish flow (container create → status poll → publish) against the live account before building scheduling/state-tracking on top of it.
**How:** Wrote `scripts/publish_story.py` (takes an image URL, creates a `media_type=STORIES` container, polls `status_code` until `FINISHED`, then calls `media_publish`). Ran it against the `peoples-of-iran` story deck's `everyone-their-own-people.jpg` — published successfully to `@25mordad` (24h Story).
**Note:** the Content Publishing API has no support for music stickers — that's an Instagram-app-only feature. Automated posts will always be music-less; if music matters for a given post, it has to go up manually.

### Security note

**This repo is public.** No app ID, app secret, account numeric ID, or token value was written into any tracked file (verified via grep before and after edits). The only place the live token exists is `.env`, which is gitignored and was confirmed untracked before being created. Any future scripts that print API responses should avoid echoing the raw token.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Adding a permission scope threw a generic "Sorry something went wrong" error | Permission was already granted/"Ready for testing" — no action was actually needed; error was a red herring from trying to re-add an existing scope |
| Token was pasted directly into chat despite a request not to | Saved it immediately to a protected file, then later moved to project `.env` per user preference; flagged that rotating it is good hygiene since it passed through the transcript |

### Pending / TODO

- [ ] Add slug → ordered story-card-filenames config to the publish script (currently single-URL-arg only)
- [ ] Posting-state tracking, scheduler, credential security for CI, token refresh, failure handling (remaining P1.8 subtasks)
- [ ] P2: Decide next article topic (still open)

---

## 2026-06-16 — Plan Instagram story automation setup

### What we built

| Feature | Files |
|---|---|
| Added llms.txt planning task | `TASKS.md` |
| Guided Meta/Instagram setup path for automated story publishing | none |

### Decisions

#### 1. Start with manual Meta API setup before coding
**Why:** Avoid building automation before the Page/account/token prerequisites are working.
**How:** Create/connect the Business Portfolio, Facebook Page, Instagram Creator/Business account, then test one story publish manually.

#### 2. Delay Business Verification unless required
**Why:** Own-account development-mode testing may work before full verification.
**How:** Try Development mode first; complete business verification only if Meta blocks the required permissions.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| No available Business Portfolio during app creation | Inspect/create/use an existing portfolio. |
| Business portfolio creation limit reached | Delete an unused portfolio or reuse an existing one. |
| Instagram account add failed with unknown Meta error | Verify account type/Page linkage and try Business Suite, incognito, or another portfolio. |
| Facebook Page creation blocked temporarily | Check Account Status/Security Center, try normal Page creation, or wait/use an existing Page. |

### Pending / TODO

- [ ] Resolve Facebook Page creation/add restriction or use an existing Page
- [ ] Link 25mordad Instagram Creator/Business account to a Facebook Page
- [ ] Add Page + Instagram account to the same Business Portfolio
- [ ] Return to Meta Developer app creation and continue Instagram publishing setup
- [ ] Complete one manual story publish API test before writing automation

---

## 2026-06-16 — Plan Instagram story automation; confirm Creator account Facebook link

### What we built

| Feature | Files |
|---|---|
| New P1.8 task block "Automate Instagram story posting" with 12 subtasks | `TASKS.md` |
| Confirmed IG Creator account is linked to a Facebook Page (manual user action, no files) | — |

### Decisions

#### 1. Prioritize IG story automation as P1.8, not P2
**Why:** User wants to start immediately rather than queue it behind the next-article-topic decision (P2).
**How:** Added a 12-step plan covering account setup, Meta dev app, access token, public image hosting, publish script, posting-state tracking, scheduler, credential security, token refresh, failure handling, dry-run test, and pipeline integration.

#### 2. Use Development mode with own account as a tester
**Why:** Avoids the overhead of full Meta App Review, which isn't needed for self-only automation.
**How:** Add the own Instagram account as a tester inside the Meta developer app instead of submitting the app for review.

### Pending / TODO

- [ ] Create Meta developer app at developers.facebook.com, add Instagram Graph API product (P1.8 task 2)
- [ ] Generate long-lived access token with `instagram_content_publish` scope (P1.8 task 3)
- [ ] Remaining P1.8 subtasks (image hosting, publish script, scheduler, etc.)
- [ ] P2: Decide next article topic (still open from prior session)

---

## 2026-06-14 — Redesign feed post cards — light bg, dark text, section badge, caption rules

### What we built

| Feature | Files |
|---|---|
| Redesigned dedication card (light bg, 44px, fills 90%) | `files/PanorAIma/peoples-of-iran/test-post-dedication.html`, `images/.../posts/00b-dedication.jpg` |
| Redesigned title card (same light treatment) | `files/PanorAIma/peoples-of-iran/test-post-title.html`, `images/.../posts/00a-title-card.jpg` |
| Redesigned section card template (light panel, dark text, section badge) | `files/PanorAIma/peoples-of-iran/test-post-d.html` |
| Rewrote gen_post_cards.py (all 18 cards in one run) | `files/PanorAIma/peoples-of-iran/gen_post_cards.py` |
| Re-rendered all 18 post cards (00a, 00b, 01–16) | `images/PanorAIma/peoples-of-iran/posts/` |
| Updated carousel caption + added first_comment_en field | `files/PanorAIma/peoples-of-iran/card-texts.md` |
| CLAUDE.md + memory updated with new design spec | `CLAUDE.md`, `memory/project_feed_post_pipeline.md` |

### Decisions

#### 1. Light background (`bg.png`) always — never dark, never random
**Why:** Dark bg + gold/yellow text was hard to read on Instagram. Light bg + dark text is far more legible for Instagram feed scrolling. The contrast ratio is dramatically better in a bright feed environment.
**How:** Hardcoded `bg.png` in `gen_post_cards.py`; removed `BG_OPTIONS` randomness entirely.

#### 2. `background-position: center center`
**Why:** Top/bottom crops were cutting off photo subjects and showing empty sky or ground. Center anchors the most visually meaningful part of the photo throughout the card.
**How:** CSS property updated in all 3 templates (test-post-d.html, test-post-title.html, test-post-dedication.html).

#### 3. Large starting fonts (34px body, 44px dedication)
**Why:** Previous 27px/24px starting sizes left too much blank space inside the cards — text felt lost. The auto-scale already shrinks down if needed, so starting high means text fills ~90% of the card for typical paragraph lengths.
**How:** JS auto-scale now starts at 34px (section body) and 44px (dedication), shrinks to 13px / 22px min.

#### 4. Section badge replaces "بخش اول" label
**Why:** The old label (بخش اول، دوم، ...) consumed ~40px of vertical space without adding meaningful value for a viewer. A compact 36×36px corner circle preserves carousel tracking (which card am I on?) without eating into the body area.
**How:** Absolute-positioned circle in top-left corner with Persian numeral (۱, ۲, …). Label field in card-texts.md is now ignored for post cards; badge number is auto-generated from section number.

#### 5. gen_post_cards.py produces all 18 cards
**Why:** The two intro cards (title, dedication) were previously rendered via ad-hoc inline Python snippets. One script is cleaner, reproducible, and ensures new article pipelines just need to copy + update one file.
**How:** Added `html_title()` and `html_dedication()` functions; updated card-texts.md parser to handle `-1` and `0` slot numbers.

#### 6. Caption uses actual blank lines (not ¶) and substance-first framing
**Why:** `¶` as a paragraph separator would appear literally if copy-pasted into Instagram. "۱۶ بخش" framing is insider logic — new viewers don't know or care how many sections there are.
**How:** Rewrote caption block with real newlines; restructured around article substance (what the reader learns) not article structure (how it's organized).

#### 7. first_comment_en field
**Why:** EN followers see a FA caption they can't read. A first comment in EN immediately after publishing gives them an entry point to the EN article.
**How:** New field in `## general-caption` block in card-texts.md. Posted as the first comment manually right after publishing. No flag emojis (house rule).

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Playwright chromium not installed | Ran `playwright install chromium` |

### Pending / TODO

- [ ] Commit all redesigned post cards + updated templates, gen_post_cards.py, card-texts.md, CLAUDE.md
- [ ] P2: Decide next article topic (candidates A–E in TASKS.md)
- [ ] P2: Update `PanorAIma/next/index.html` + teaser card

---

---

> Older entries archived in WORKLOG_ARCHIVE.md
