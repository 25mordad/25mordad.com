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

## 2026-07-01 — Added title/dedication story cards; published full 18-card story deck; API capability research

### What we built

| Feature | Files |
|---|---|
| Title-card + dedication story slides (dark/gold style, matching the 16 section cards) | `files/PanorAIma/peoples-of-iran/gen_section_cards.py` |
| Rendered title-card.jpg, dedication.jpg | `images/PanorAIma/peoples-of-iran/stories/{title-card,dedication}.jpg` |
| Full 18-card story deck published live to `@25mordad` | none (Instagram, ephemeral 24h) |

### Decisions

#### 1. Story deck gets the same title/dedication slides as the feed-post carousel
**Why:** The story deck previously only had the 16 section cards — no opening title or dedication slide, unlike the post carousel which already had both (slots `-1` and `0` in `card-texts.md`). Brought the two decks to parity.
**How:** Extended `gen_section_cards.py`'s parser to accept negative/zero slot numbers (`-1`, `0`) and added two new dark/gold-styled HTML templates (`HTML_TITLE_TEMPLATE`, `HTML_DEDICATION_TEMPLATE`) reusing the existing story card's CSS classes. Output: `stories/title-card.jpg`, `stories/dedication.jpg`.

#### 2. No hashtags on Stories
**Why:** Confirmed via research that Stories have no `caption` field and no hashtag-sticker support in the Content Publishing API — a hashtag would have to be manually added as an app sticker after the API post, or baked into the image as non-functional decorative text. User decided to skip hashtags on Stories entirely rather than do either.
**How:** No code change; documented as a deliberate decision, not an oversight.

#### 3. Published the full 18-card deck in one sitting, not the usual every-few-days cadence
**Why:** User explicitly asked to "go all in order" rather than spread the deck out — a one-time exception to the documented posting cadence for this article's launch.
**How:** Looped `publish_story.py` over the deck in article order (title-card → dedication → sections 1–16). Confirmed via `GET /me/stories` that exactly 18 Stories are live.
**Note:** this was a deliberate one-off; future articles should default back to the "every couple of days" cadence unless told otherwise.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Cloudflare Pages was disconnected from the GitHub repo, so the first push of title-card.jpg/dedication.jpg never deployed (404 for ~15 min) | User reconnected Cloudflare Pages to the repo; pushed an empty commit to retrigger the deploy, then confirmed both URLs returned 200 |
| The publish loop for all 17 remaining cards hit the Bash tool's 5-minute timeout mid-run, truncating the terminal output right after `economy-practical-cooperation` | Cross-checked the live Stories via `GET /me/stories` (returned IDs + timestamps) against the script's printed `Published:` IDs to confirm that card *had* actually published before the timeout killed the process — avoided a duplicate post, then ran the 2 genuinely-missing cards (`family-kinship-forced-contact`, `intertwined-lives`) |

### API capability research (Stories)

- **Supported:** `image_url`/`video_url` (single media per Story), and `user_tags` (mention accounts with optional x/y placement — added to the API July 2025).
- **Not supported via API (app-only):** captions, music stickers, link/swipe-up stickers, poll/quiz/question stickers, location stickers, hashtag stickers.
- **The "Say something…" reply box** seen on every Story is automatic platform UI (private DM reply), not something added via API or configurable per-post.
- **Comments API is feed/Reels/carousel only.** Stories have no public comment thread on Instagram at all — replies are always private DMs. `GET/POST /{ig-media-id}/comments` doesn't apply to Stories.

### Pending / TODO

- [ ] Add slug → ordered story-card-filenames config to the publish script (still single-URL-arg only)
- [ ] Posting-state tracking, scheduler, credential security for CI, token refresh, failure handling (remaining P1.8 subtasks)
- [ ] P2: Decide next article topic (still open)

---

> Older entries archived in WORKLOG_ARCHIVE.md
