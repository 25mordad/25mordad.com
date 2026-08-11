# TASKS

## P1.6 — peoples-of-iran Instagram feed post cards

- [x] Build gen_post_cards.py (Playwright, 1080×1080) — `files/PanorAIma/peoples-of-iran/gen_post_cards.py`
- [x] Add general-caption block to card-texts.md (single caption for full carousel)
- [x] Render all 16 feed post images — `images/PanorAIma/peoples-of-iran/posts/01-*.jpg … 16-*.jpg`
- [x] Fix section 1 post_body (trimmed 4→2 paragraphs to match all other sections)
- [x] Commit gen_post_cards.py, test-post-d.html, updated card-texts.md, and all 16 post images — DONE 2026-06-13 (e7c17e6)
- [ ] Generate 2 intro post cards for peoples-of-iran carousel:
  - [x] Design `test-post-title.html` — title card (مردمان ایران + چند جامعه زیر یک نام + بهمن رشادی, no section label/body/CTA)
  - [x] Design `test-post-dedication.html` — dedication card (full text, centered, RTL, no label/CTA)
  - [x] Render `images/PanorAIma/peoples-of-iran/posts/00a-title-card.jpg` (1080×1080, q=98)
  - [x] Render `images/PanorAIma/peoples-of-iran/posts/00b-dedication.jpg` (1080×1080, q=98)
  - [x] Get user approval of 00a-title-card.jpg and 00b-dedication.jpg designs
  - [x] Commit both new cards + updated card-texts.md (test-post-title.html, test-post-dedication.html, 00a-title-card.jpg, 00b-dedication.jpg) — DONE 2026-06-14
  - [x] Update gen_post_cards.py to handle slots -1 (title-card) and 0 (dedication) from card-texts.md so future articles produce all 18 cards in one script run — DONE 2026-06-14

## P1.7 — Redesign feed post cards: light bg + 90% fill + compact section number

User feedback: text too small (doesn't fill the image), yellow-on-dark is hard to read, "بخش اول" label wastes space.
Solution: light background, dark text, larger starting font, replace label with compact corner number badge.

### 00b dedication card (do first — user approves before touching 01–16)

- [x] Redesign `test-post-dedication.html` — DONE 2026-06-14
- [x] Re-render `images/PanorAIma/peoples-of-iran/posts/00b-dedication.jpg` — DONE 2026-06-14
- [x] User approval of redesigned 00b — DONE 2026-06-14

### 01–16 section cards (after 00b approval)

- [x] Redesign `test-post-d.html` — DONE 2026-06-14
- [x] Re-render all 16 via `python3 files/PanorAIma/peoples-of-iran/gen_post_cards.py` — DONE 2026-06-14
- [x] Visual check on 2–3 cards before committing all 16 — DONE 2026-06-14
- [ ] Commit all redesigned templates + gen_post_cards.py + re-rendered post cards + card-texts.md

## P1.8 — Automate Instagram story posting

12-step plan to automate IG story posting for the existing story card decks (covers account setup, Meta dev app, access token, public image hosting, publish script, posting-state tracking, scheduler, credential security, token refresh, failure handling, dry-run test, pipeline integration). Prioritized as P1.8 (not P2) — user wants to start immediately.

- [x] Confirm IG account is a Business/Creator profile linked to a Facebook Page (required for API publishing) — DONE 2026-06-16
- [x] ~~Resolve current Meta setup blocker: Facebook Page creation/add is temporarily blocked~~ — NOT NEEDED, RESOLVED 2026-07-01: built the Meta app via the **Instagram API with Instagram Login** flow (not the Facebook-login flow), which does not require a linked Facebook Page at all. Page-linkage subtasks below are obsolete for this path.
  - ~~Check Meta Business Help Center / Account Quality for the specific reason the Page creation/add is blocked~~ — moot
  - ~~Try creating or linking the Page via business.facebook.com (Business Suite)~~ — moot
  - ~~If still blocked after a retry, escalate via Meta Business Help Center support chat~~ — moot
- ~~Link `25mordad` Instagram to the chosen Facebook Page and make sure both are in the same Business Portfolio~~ — moot, see above
- [x] Create a Meta developer app, add the Instagram API product (Instagram Login setup) — DONE 2026-07-01
- [x] Generate a long-lived access token scoped with publish + comments + messages + insights permissions (granted "Ready for testing" in dev mode, no App Review needed) — DONE 2026-07-01
  - Token stored in project-root `.env` (`IG_ACCESS_TOKEN`), gitignored — never commit this file or its value anywhere (repo is public)
- [x] Solve the public-URL requirement — story card images confirmed publicly reachable directly at `https://25mordad.com/images/PanorAIma/<slug>/stories/<section-slug>.jpg` (200 OK), no extra hosting needed — DONE 2026-07-01
- [x] Set up `scripts/` folder for Python automation — Python venv at `scripts/.venv/` (gitignored), `scripts/requirements.txt` (`requests`, `python-dotenv`), run via `scripts/.venv/bin/python scripts/<script>.py` — DONE 2026-07-01
- [x] Write a token-verification script (`scripts/test_ig_token.py`) — loads token from `.env`, calls the profile endpoint, confirms it works — DONE 2026-07-01
- [x] Write the publish script (`scripts/publish_story.py`) — takes an image URL arg, creates a media container (`media_type=STORIES`), polls status until `FINISHED`, then publishes via `media_publish` — DONE 2026-07-01
  - [x] End-to-end test: published a real Story from `peoples-of-iran/stories/everyone-their-own-people.jpg` to the live `@25mordad` account — succeeded — DONE 2026-07-01
  - Note: Instagram's Content Publishing API does **not** support attaching a music sticker — that's app-only (manual posting). Automated posts will always be music-less.
  - Note: Stories support `user_tags` (mention accounts, added to the API July 2025) but no captions, link/poll/location/hashtag stickers — those remain app-only. Decided to skip hashtags on Stories entirely rather than fake them as baked-in image text.
  - Note: the Comments API (`/{ig-media-id}/comments`) only applies to feed posts/Reels/carousels — Stories have no public comment thread on Instagram at all, only private DM replies (the automatic "Say something…" box, not API-controlled).
  - [ ] Add a config mapping slug → ordered list of story card filenames for the publish script to read (currently takes a single URL arg, no slug/ordering logic yet)
    - [ ] Derive the deck order by parsing `card-texts.md` block order (slots -1, 0, 1–16) instead of hardcoding filenames, so new articles need no manual list
    - [ ] Add `scripts/deck.py` helper exposing `deck_for(slug) -> [(card_slug, public_url), …]` used by every publish script
    - [ ] Extend `publish_story.py` to accept `--slug <slug> --card <card-slug>` in addition to the current raw-URL arg (keep the raw-URL path working)
    - [ ] Add `--dry-run` flag: resolve the URL, HEAD-check it returns 200, print what would be posted, publish nothing
    - [ ] Add a URL reachability pre-check (HEAD request) before creating the media container, so a 404 fails fast with a clear message
- [x] Add title-card + dedication story slides to the `peoples-of-iran` deck (previously only the 16 section cards existed for Stories; now matches the 18-card post carousel structure) — `gen_section_cards.py` extended with two new dark/gold templates — DONE 2026-07-01
- [x] Published the full 18-card story deck (title → dedication → 16 sections) live to `@25mordad` in one sitting, per user request — confirmed via `GET /me/stories` returning exactly 18 items — DONE 2026-07-01
  - Note: this was a one-time exception to the "every couple of days" cadence for this article's launch; default back to the slower cadence for future articles unless told otherwise
- [ ] Add posting-state tracking — manifest (e.g. `posted.json` per article) so the script knows which cards are already posted and picks the next one in order
  - [ ] Decide manifest location + whether it is committed or gitignored (`scripts/state/posted-<slug>.json`) and document the choice ← blocks scheduler work
  - [ ] Define the manifest schema: card slug, container id, published media id, `published_at` ISO timestamp
  - [ ] Write `scripts/publish_next.py` — read deck order + manifest, pick the first unposted card, publish it, append the result to the manifest ← depends on deck config
  - [ ] Backfill a `peoples-of-iran` manifest marking all 18 story cards as already posted (2026-07-01) so nothing gets reposted
  - [ ] Add a `--status` mode printing posted/remaining counts per slug
  - [ ] Guard against duplicate posts — cross-check `GET /me/stories` before publishing (the 2026-07-01 timeout incident showed the script's own output can be truncated mid-run)
  - [ ] Before backfilling the `peoples-of-iran` manifest, re-check `GET /me/stories` for what's currently live — Stories expire after 24h so the 2026-07-01 deck is long gone; manifest should record *history* (what was posted and when), not assume anything is still visible
- [ ] Build the cadence/scheduler — cron job or GitHub Actions to run every couple of days, matching existing posting cadence
  - [ ] Decide between a local cron job vs a GitHub Actions scheduled workflow ← depends on credential security decision
  - [ ] Note the constraint in the decision: `.env` is local-only, so GH Actions requires putting the token in a repo secret on a **public** repo
  - [ ] Write the chosen artifact — crontab entry or `.github/workflows/publish-story.yml` on a 2-day schedule ← depends on the decision above
  - [ ] Make the scheduler a no-op (exit 0, log a line) when the deck for the active slug is fully posted
  - [ ] Add an "active slug" setting so the scheduler knows which article's deck is currently being drip-posted
- [ ] Secure credentials — app secret + access token as env vars / GitHub Actions secrets, never committed
  - [ ] Add a repo guard that greps tracked files for the token/app-secret pattern and fails loudly if one leaks
  - [ ] Re-verify `.env` is still gitignored and untracked before any commit that touches `scripts/`
- [ ] Handle token expiry — add a refresh step or calendar reminder (IG long-lived tokens expire ~60 days)
  - [x] **2026-08-12 UPDATE:** the 2026-07-01 token was found invalid this session (Meta error 190 — session invalidated, not just expired; `scripts/test_ig_token.py`'s traceback-leak bug was discovered and fixed while diagnosing this, see the fix commit). User manually generated a **new** token via the Meta dashboard directly (not through the `ig_auth.py` OAuth script written for this — that script is untested/unused so far, kept for future automated refresh) — confirmed working via `test_ig_token.py`.
    - [ ] **Unknown whether the new manual token is long-lived (~60 days) or short-lived (~1 hour, if generated via Graph API Explorer's default button)** — wasn't confirmed at generation time. If posting starts failing again soon after 2026-08-12, this is the first thing to check; consider running `ig_auth.py` (needs `IG_APP_ID`/`IG_APP_SECRET` in `.env`, not yet added) to get a properly long-lived token deterministically instead of relying on manual dashboard generation again.
  - [ ] **Original time-sensitive item (superseded by the above, kept for history):** token was issued 2026-07-01 → expired ~2026-08-30 window turned out to not matter — it invalidated early for a different reason (session invalidation, not natural expiry)
  - [ ] **As of 2026-08-11 only ~19 days remain** — run `scripts/test_ig_token.py` this session to confirm the token still works before doing any further IG API work
  - [ ] Write `scripts/refresh_token.py` — call `GET /refresh_access_token?grant_type=ig_refresh_token`, rewrite `IG_ACCESS_TOKEN` in `.env`, never print the value
  - [ ] If `refresh_token.py` isn't written before the deadline, do a manual refresh via Meta Graph API Explorer as a stop-gap and note the new expiry date in WORKLOG
  - [ ] Make `test_ig_token.py` also report days-to-expiry so the state is visible at a glance
  - [ ] Have the scheduler auto-refresh when the token is within ~10 days of expiry ← depends on refresh_token.py
- [ ] Add failure handling — log/alert (push notification or email) on a failed publish call instead of silently skipping
  - [ ] Wrap the container-create / poll / publish steps in try-except and append failures to `scripts/state/publish.log`
  - [ ] Distinguish retryable (rate limit, transient 5xx) from terminal (bad token, 404 image) failures and retry only the former
  - [ ] Pick the alert channel (email vs push) and implement it for terminal failures
- [ ] Wire into the existing pipeline — decide whether new articles auto-enqueue story cards for posting or require manual trigger per article
  - [ ] Add a Phase-4 checklist step in CLAUDE.md for registering a new slug with the story-deck publisher
  - [ ] Document the whole automation flow (deck config → manifest → scheduler → refresh) in a short `scripts/README.md`

## P1.9 — Lightroom-curated photo series → Instagram Feed (personal photography pipeline)

New, separate pipeline from the PanorAIma article system: curate a series of personal photos in a
Lightroom (cloud/CC) album, get an AI-written bilingual caption for each, and have them drip out to
the `@25mordad` Instagram Feed automatically every couple of days — no per-post manual trigger.
Planned 2026-08-11; not started, no code written yet.

**Locked-in decisions:**
- Feed posts only for now — Stories deferred (Instagram's Stories API has no caption field at all,
  so that needs its own design pass later; explicitly parked, not forgotten)
- Bilingual captions: FA caption on the post itself, EN translation as the first comment —
  mirrors the existing `card-texts.md` `general-caption` convention, no flag emojis
- One photo per Feed post (not a carousel) — "post them one by one"
- Photo selection: a named album inside the Lightroom app; automation reads it via Adobe's
  Lightroom API (self-serve OAuth via Adobe Developer Console).
  - **2026-08-11 RE-VERIFIED:** research this session initially found Adobe's docs
    inconsistent — Firefly Services "Lightroom APIs" require an Enterprise contract, and
    "Lightroom Partner APIs" require Adobe partner approval. But the plain "Lightroom
    Services" API in the standard Developer Console (confirmed live in-console this session)
    offers self-serve **OAuth Web App / Single-Page App / Native App** credentials with no
    Enterprise-contract mention — this is the real path. Chose **OAuth Web App** (confidential
    client, client_secret + backend-stored refresh token) to match the unattended-script plan.
- Photos are committed straight into the git repo (new `images/ig-queue/` folder) — same
  pattern as every other site image, since the repo is already public. No external object
  storage needed for this project.
- **Series + naming workflow (2026-08-11):** the current batch flowing into `images/ig-queue/`
  is the **Ethiopia series**, titled **«دنیا بزرگتر از اونه که ما تصور می‌کنیم»** — every photo
  fetched belongs to this series until the user explicitly says a new series is starting
  (tracked as the `SERIES_NAME` constant in `lr_fetch_photo.py`, and a `series`/`title` field
  on each photo's JSON record). The user picks and approves each photo's individual `title`
  themselves — the only thing they need to sign off on per photo. They've asked me to propose
  candidate titles each time too, explicitly so I can learn their naming style/playfulness
  from which ones they pick or rewrite — treat this as an ongoing calibration, not a one-off.
- **Privacy constraint (2026-08-11):** standard EXIF (camera model, lens, exposure settings)
  is fine to keep on committed photos. What must never leak into anything committed or logged
  is the **local file path on the phone or computer** — Lightroom's asset metadata includes a
  `payload.importSource.localAssetId` field with the exact on-device storage path (e.g.
  `/storage/emulated/0/ax/.../R0002269.DNG`), plus `uniqueDeviceId`/`importedBy` device
  identifiers. These are Lightroom-catalog-only fields (not standard EXIF), so the downloaded
  rendition JPEG itself shouldn't contain them — but `lr_fetch_photo.py` must (1) never
  print/store/commit the `importSource` block from the API response anywhere, and (2) verify
  the actual downloaded JPEG's embedded metadata (e.g. via exiftool) has no local path before
  the first real commit, to confirm rather than assume.
- Publish flow reuses an existing internal pattern (adapted, not copied verbatim): each queued
  photo gets a small record (status, caption fields); publishing refuses anything not
  `status: approved`, always prints a preview, and requires a typed confirmation before it
  actually calls the Instagram API — same shape as `scripts/publish_story.py`'s
  container→poll→publish, just for single-image Feed posts with a real caption.
  Also reusing an existing Telegram-bot approval channel (send photo + draft caption to a
  chat, resolve a 👌/👎 emoji reaction back to that item) as an alternative to approving
  inside a chat session — TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID would go in this project's
  own `.env`, never committed.
- Two-phase split — drafting is interactive (AI needs to actually look at each photo, can't
  run unattended in a cron), posting is purely mechanical:
  1. **Drafting (session-time):** pull new album photos, draft FA caption + EN first comment
     for each, validate the *first* photo's tone with the user before batch-drafting the rest
     (same "approve item 1 before the rest" rule already used for story cards)
  2. **Posting (scheduled, unattended):** unattended job posts the oldest `approved` item every
     ~2 days — no AI/drafting inside this step, HTTP calls only

**Rollout subtasks:**
- [x] User creates the Adobe Developer Console project + adds the Lightroom Services API (OAuth Web App credential) — DONE 2026-08-11
- [x] User creates the Lightroom album — named **`instagram`** (Latin, lowercase — not the Persian "اینستاگرام" originally assumed), 1 photo added so far — DONE 2026-08-11
- [x] Build Lightroom OAuth setup + refresh scripts; verify the refresh token actually works
      end-to-end — DONE 2026-08-11, confirmed via live token refresh call
  - [x] Register the Lightroom Services API in the Adobe Developer Console project, obtain client_id/client_secret — DONE 2026-08-11
  - [x] Store `LR_CLIENT_ID` / `LR_CLIENT_SECRET` / `LR_REFRESH_TOKEN` in project-root `.env` (gitignored, never commit) — DONE 2026-08-11
  - [x] Write `scripts/lr_auth.py` — one-time OAuth authorization-code flow (local HTTPS redirect handler) to obtain the initial access + refresh token — DONE 2026-08-11
  - [x] Write `scripts/lr_refresh_token.py` — exchange refresh token for a new access token — DONE 2026-08-11, end-to-end check passed
  - [ ] **Unverified refresh-token lifetime:** Adobe's token response doesn't return the refresh token's own expiry (only the access_token's `expires_in`, observed ≈41.6 days). Community reports suggest Adobe IMS refresh tokens often default to ~14 days, but some services use a sliding inactivity window instead (renews on use) — unclear which applies to Lightroom. Since the posting scheduler will call the refresh endpoint every ~2 days anyway, a sliding window would keep it alive indefinitely; a hard 14-day expiry would not. Re-run `scripts/lr_refresh_token.py` around **2026-08-25** (~14 days out) to empirically determine which model applies before relying on it unattended.
- [ ] Build the album-fetch script (list assets → request rendition → poll → download JPEG →
      commit to `images/ig-queue/`)
  - [x] Write `scripts/lr_list_album.py` — list assets in the configured album via the Lightroom API — DONE 2026-08-11, confirmed against the live `instagram` album (1 photo: `R0002269.DNG`, RICOH GR IIIx RAW, captured 2026-02-03)
    - Technical notes for `lr_fetch_photo.py`: base API is `https://lr.adobe.io/v2/`, auth via `X-API-Key: <LR_CLIENT_ID>` + `Authorization: Bearer <access_token>` headers; every response body is prefixed with `while (1) {}` (XSSI protection) — must be stripped before JSON parsing (handled in `scripts/lr_common.py`'s `lr_get`); album-assets listing needs `?embed=asset` or fields come back mostly empty; the real asset id/payload is nested under `resources[].asset`, not the outer `resources[]` (that outer id is the album-membership id); rendition download hrefs are `assets/{asset_id}/renditions/{2048|1280|640|thumbnail2x}`
  - [x] Decide the per-photo record filename/schema — DONE 2026-08-11: `images/ig-queue/<asset-id>.jpg` + sidecar `images/ig-queue/<asset-id>.json` with `{asset_id, image, capture_date, fetched_at, status: "draft", caption_fa, first_comment_en}`. Deliberately excludes the `importSource` block (local file path). `status` will gate publishing later (draft → approved → posted), mirroring the existing internal pattern.
  - [x] Write `scripts/lr_fetch_photo.py` — DONE 2026-08-11. Turned out renditions return synchronously (200 + JPEG bytes on first GET, no async poll needed — simpler than assumed). Includes a built-in safety scan of the raw downloaded bytes for local-path patterns (`/storage/`, `/Users/`, `/home/`, `C:\Users`) that refuses to save if any match — tested against the real photo, zero matches, confirmed clean.
    - [x] Rendition size tuned to `1280` (not `2048`) — DONE 2026-08-11. User flagged the first fetch (2048px, ~1.1MB) as too heavy for the repo compared to every other image type here (~400-500KB). Instagram's feed only displays up to ~1440px and recommends 1080px minimum, so `1280` (~300KB, still well above IG's floor) has no visible quality cost.
    - [x] End-to-end test: fetched the 1 real photo from the `instagram` album into `images/ig-queue/` — verified visually (a black-and-white/selective-color portrait, subject walking away in a dry landscape wearing a blue jacket, matches the user's "Ethiopia" album) — DONE 2026-08-11
    - [ ] Not yet committed to git — image + record currently only in the working tree; commit is a separate, deliberate step (not done automatically by the fetch script)
- [x] Draft captions for the first photo only, get tone/style calibration before the rest — DONE 2026-08-11, photo 1 (`e88d9e2e96b84f9389823d0754676ed9`, titled «یارو») approved after 3 rounds of calibration
  - **Locked caption format for this series** (supersedes the split FA-caption/EN-first-comment convention used by PanorAIma carousels — this series uses ONE combined caption, no first comment at all):
    1. Line 1: the user's chosen photo title, in Persian quotation marks («»), on its own
    2. A short **fictional** micro-story inspired by the photo — explicitly not documentary/travel-journal, doesn't need to relate to the actual location — first in Persian, then the English translation, both in the same caption block
    3. Fixed closing line, bilingual: `دنیا بزرگتر از اونه که ما تصور می‌کنیم.` / `The world is bigger than we imagine.` — appears in every photo in this series
    4. ~28-30 hashtags mixing Persian and English, biased toward **high-volume/trending** tags (e.g. `#photography #travelphotography #instatravel #wanderlust #explorepage`, `#عکاسی #سفر #هنر`) rather than niche invented compounds — plus the series tags (`#یارو`-style per-photo title tag, `#دنیای_بزرگتر`/`#TheWorldIsBigger`) and **always `#هوش‌واره`** since the pipeline is AI-assisted
  - Record schema updated to match: `caption` (single bilingual field, replaces the earlier `caption_fa`/`first_comment_en` split) — updated in both the photo-1 record and `lr_fetch_photo.py`'s template for future fetches
  - Photo 1's `status` set to `"approved"` (caption finalized) — actual posting still blocked on the publish script not existing yet
  - **New standing rule (2026-08-11):** always draft **two** distinct fictional story options per photo (documented in CLAUDE.md's Personal Photo Series section) — for photo 1, offered a mystical/lyrical option vs. a deadpan/absurdist one (man searching for something he lost 30 years ago, forgot what it was); user picked the deadpan one, confirming the same taste signal as the «یارو» title pick. See memory `feedback_photo_naming_style.md`.
  - Whole pipeline documented in `CLAUDE.md` under a new **Personal Photo Series (Lightroom → Instagram Feed)** top-level section — DONE 2026-08-11
- [x] Build the publish script (adapted from the existing internal pattern above), test with
      `--dry-run` first, then one real live post triggered manually — DONE 2026-08-12
  - [x] Adapt the container→poll→publish flow from `scripts/publish_story.py` for a single-image Feed post (default `media_type`, not `STORIES`) plus a real caption — `scripts/lr_publish_photo.py` — DONE 2026-08-12
  - [x] Add the status-gated preview + typed-confirmation gate before any live publish call — implemented as default dry-run + explicit `--confirm-publish` flag (only ever passed after the user explicitly says to post, in-session) — DONE 2026-08-12
  - No first comment for this series (superseded — see the locked caption format above; everything's in one combined caption)
  - **First real live post, 2026-08-12:** photo `e88d9e2e96b84f9389823d0754676ed9` ("یارو") published to `@25mordad` — https://www.instagram.com/p/Db6pBdIDtb5/ (media_id `18098543159625393`). Record `status` auto-updated to `"posted"` with `posted_at`/`media_id`.
  - **IG token had to be regenerated mid-session** — the 2026-07-01 token was invalid (see P1.8 above). User manually generated a replacement via the Meta dashboard rather than using the new `ig_auth.py` script (which needs `IG_APP_ID`/`IG_APP_SECRET`, not yet added to `.env`) — works, but token type (long vs. short-lived) unconfirmed; watch for another sudden failure.
- [ ] Only after a manual post is verified live on `@25mordad`: wire up a scheduled job
      (GitHub Actions cron, ~2-day interval) for unattended posting — manual post now verified live, this is next
- [ ] Wire up the Telegram approval channel as an alternative review path
- [ ] Document the finished pipeline in `CLAUDE.md` (new section, same depth as the existing
      Instagram Story/Feed Post sections) once it's actually built

## P3 — Finalize third article "زنده‌ماندن یا زیستن؟" (draft, gitignored — not yet public)

User pre-drafted this article's material via ChatGPT before this session; work here was cleanup, citation integrity, de-duplication, and producing review copies. Working files live in `files/PanorAIma/surviving-or-living/` — this whole directory is in `.gitignore` until publication is decided (see CLAUDE.md note).

- [x] Move draft material from wrong public path (`PanorAIma/3-materials/`) to `files/PanorAIma/surviving-or-living/sections/`
- [x] Convert inline links to project's `[n]` + `## منابع` citation convention (25 sources)
- [x] Research and add real citations for 6 previously-uncited claims (Hirschman, Scott, Barry, IMF figures, Sen, Margalit)
- [x] Fix factual error: IMF 2026 Iran growth figure corrected via web research
- [x] Merge 9 section files into single review draft `surviving-or-living-fa.md` (kept frozen/untouched)
- [x] Remove 3 near-duplicate passages found across sections (Diane Vaughan, maladaptation, McEwen allostatic load) — each kept in its structurally correct section only
- [x] Fix citation numbering end-to-end (including a leftover ordering bug from an earlier edit) — strict ascending first-appearance order, verified via grep
- [x] Add the user's "war normalization" closing question to the section-8 question list
- [x] Unify formatting sitewide in the revised draft: book titles, Persian glosses for Latin terms, repeated-name trimming, section-heading punctuation, reference-list format
- [x] Remove section numbers from headings, add a numbered-free table of contents (`surviving-or-living-fa-v2.md`)
- [x] Verify/correct 4 statistical claims via live web research; found and removed one fabricated figure (2025 inflation number had no source)
- [x] Complete 2 previously incomplete reference entries ([14] McEwen 2004, [16] Asadi-Lari et al. 2016, Urban HEART-2 Tehran study)
- [x] Produce short version `surviving-or-living-fa-short.md` (~3,900 words) — verified all 25 citations and 21 named thinkers survive the cut
- [x] Generate review PDFs (`surviving-or-living-fa-v2.pdf` 30pp, `surviving-or-living-fa-short.pdf` 15pp) via `make_pdf.py`
- [x] Add `files/PanorAIma/surviving-or-living/` to `.gitignore` — draft not yet approved for publication
- [ ] User to review both PDFs with close friends before any publish decision
  - [ ] Check in with user on friend-review status — last touched 2026-08-09, ~2 days idle as of session start 2026-08-11
- [ ] Final full read-through pass on Opus model (user's plan: research/mechanical work on Sonnet, final polish on Opus)
- [ ] Decide official EN title + produce EN translation (long version only, per convention — no short EN)
  - [ ] Draft 2–3 candidate EN titles for «زنده‌ماندن یا زیستن؟» ahead of time so translation can start immediately once friend review clears ← depends on publish approval
- [ ] Once approved: move to `PanorAIma/<slug>-fa|en/`, remove the `.gitignore` line, follow full Phase 2–4 checklist in CLAUDE.md (covers, hero images, story/post card decks, sitemap, hreflang)
- [ ] After this article is fully finalized: build a tone/voice profile for the user using articles 2 (مردمان ایران) and 3 (this one) as reference — explicitly deferred to last
- ~~No Instagram/Twitter work of any kind for this article~~ — standing constraint for this article only; that whole system is being redesigned separately

## P2 — Teaser: announce next article after "Peoples of Iran"

- [x] Decide next article topic — RESOLVED via a different path than planned below: user pre-drafted "زنده‌ماندن یا زیستن؟" independently (see new P3 block above) rather than through the brainstorm/shortlist process outlined in the subtasks. Subtasks below kept as-is (not this article's actual path, but still valid process for the *next* one after this).
  - [ ] Brainstorm 3–5 candidate topics aligned with PanorAIma's analytical lens (social/historical/cultural/economic Iran)
    - [ ] Candidate A: Iranian bazaar — economic structure, guild culture, political role
    - [ ] Candidate B: Iranian diaspora — identity, cultural negotiation, dual belonging
    - [ ] Candidate C: Persian language — spread, survival, political uses across history
    - [ ] Candidate D: Women in Iranian history — beyond the modern lens, pre-Islamic + Qajar + Constitutional era
    - [ ] Candidate E: Iranian calendar and time perception — Nowruz, seasonal rhythm, cosmological worldview
  - [ ] For each shortlisted candidate, sanity-check source availability (academic refs reachable for `[n]` citations, similar to peoples-of-iran's sourcing)
  - [ ] Cross-check shortlist against existing articles (`iran-lahzeye-feshordeh-tarikh`, `peoples-of-iran`) to avoid thematic overlap
  - [ ] Present the shortlisted candidates to the user as a numbered list for a final pick
  - [ ] Note chosen topic + rationale in WORKLOG
  - [ ] Derive slug plan (EN + FA slugs) and note in TASKS under new P1 block
  - [ ] Draft the 16-section outline for the chosen topic (matching peoples-of-iran's structure) ← depends on topic pick
  - [ ] Collect the source list up front so `[n]` citations are settled before drafting ← depends on outline
  - [ ] Source and place `bg-d.png` / `bg.png` background photos in `files/PanorAIma/<new-slug>/` ← depends on topic
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates ← depends on topic
  - [ ] Update `<title>`, meta description/keywords, og:title, og:description, twitter:title, twitter:description
  - [ ] Update JSON-LD headline, description, and estimated publish date
  - [ ] Update teaser body text (heading + preview paragraphs) in the article body
  - [ ] Swap og:image / twitter:image to `images/PanorAIma/soon.jpg` (or a new teaser image if available)
- [ ] Update teaser card in `PanorAIma/index.html` ← depends on topic
  - [ ] Restore the commented-out teaser `<section>` block
  - [ ] Update title, description, and `.lang-actions` links in the teaser card
- [ ] Commit and push P2 teaser updates ← depends on above three
- [ ] Update memory: `project_panoraima_next.md` to reflect peoples-of-iran published and new topic chosen
- [ ] Post peoples-of-iran Instagram feed post carousel (18 cards in `images/PanorAIma/peoples-of-iran/posts/`, numbered 00a/00b + 01–16) — caption is in `files/PanorAIma/peoples-of-iran/card-texts.md` under `## general-caption`
  - [ ] Verify all 18 post images return 200 from `https://25mordad.com/images/PanorAIma/peoples-of-iran/posts/…` before posting
  - [ ] Confirm 18 fits Instagram's carousel limit (max 20 items) — no split needed
  - [ ] Upload all 18 images as a single carousel in filename order (00a → 00b → 01 → … → 16)
  - [ ] Paste the FA `caption` field from `general-caption` block as the post caption
  - [ ] Immediately after publishing, post `first_comment_en` as the first comment (no flag emojis)
  - [ ] Note: this is a one-off manual carousel post — separate from the recurring story-card automation in P1.8
  - [ ] Optional follow-up: script it (`scripts/publish_carousel.py` — child containers with `is_carousel_item=true` → CAROUSEL container → publish → POST first comment) so future articles don't need a manual upload
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Clarify the comment surface (Instagram DMs, website, or both)
  - [ ] Draft the reply prompt template (referencing article content + reader message) and save to `files/ai-reply-template.md`
  - [ ] Test the template against a sample comment from peoples-of-iran article
  - [ ] Note: no real reader comments exist yet since the peoples-of-iran feed carousel hasn't been posted — either post the carousel first or draft synthetic sample comments to test against ← depends on carousel post above
- [ ] Create root `llms.txt` for AI crawler / LLM-friendly site guidance
  - [ ] Decide content scope: site summary, owner/contact, canonical sections, PanorAIma article URLs, and usage/licensing notes
  - [ ] Check `robots.txt` for any existing AI-crawler directives to keep `llms.txt` consistent with them
  - [ ] Add `/llms.txt` at the site root with concise Markdown-style guidance and important links
  - [ ] Confirm Cloudflare Pages serves root `.txt` files as `text/plain` (no build step needed for a static file)
  - [ ] Verify `https://25mordad.com/llms.txt` is served after deploy
  - [ ] Consider adding `llms.txt` mention/link to README and sitemap if useful
  - [ ] Add an llms.txt refresh step to the article-publish checklist so new PanorAIma URLs get listed

## Done

- **Publish "The Peoples of Iran"** — All 18 checklist steps completed (FA + EN pages, covers, story cards, hero images, post card, sitemap, hreflang fix, build, commit/push) — 2026-06-07
