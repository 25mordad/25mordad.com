# TASKS

## P1 — Publish "The Peoples of Iran" (overdue: was June 4, 2026)

Article draft is at `files/PanorAIma/مردمان ایران.odt`.

Slug plan:
- EN: `PanorAIma/peoples-of-iran-en/index.html`
- FA: `PanorAIma/peoples-of-iran-fa/index.html`

- [x] Read the `.odt` draft and extract full article content — DONE (FA: 16 sections in `peoples-of-iran-fa.md`)
- [x] Generate section image cards (HTML → PNG approach) — DONE 2026-06-07
  - Card design: bordered panel (gold border, dark semi-transparent bg) floating over full-bleed photo; photo shows in margins ← locked 2026-06-07
  - Background: `files/PanorAIma/peoples-of-iran/bg-d.png` (dark, preferred)
  - Output: `images/PanorAIma/peoples-of-iran/stories/<section-slug>.jpg` (16 JPEG cards, q=98)
- [x] Generate square hero images — DONE 2026-06-07 (16 heroes in `images/PanorAIma/peoples-of-iran/heroes/`)
- [x] Render covers — DONE 2026-06-07
  - FA cover: `images/PanorAIma/peoples-of-iran/cover.jpg` (Vazirmatn, RTL)
  - EN cover: `images/PanorAIma/peoples-of-iran/cover-en.jpg` (Space Grotesk, LTR)
- [x] Add post card to `PanorAIma/index.html` — DONE 2026-06-07
- [x] Add both EN + FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod 2026-06-07` — DONE
- [x] Extract/translate EN article body to `peoples-of-iran-en.md` — DONE (16 sections, no short EN version)
- [x] Create `PanorAIma/peoples-of-iran-en/index.html` — DONE 2026-06-07
  - Cover image at top, ToC, superscript citations, refs section, PDF link, `AI-Assisted` chip
- [x] Create `PanorAIma/peoples-of-iran-fa/index.html` — DONE (610 lines, 16 heroes embedded, correct meta)
- [x] Verify hreflang in FA page — DONE 2026-06-07 (x-default now consistently → EN slug)
- [x] Run `npm run build:css` — DONE 2026-06-07
- [x] Commit and push — DONE 2026-06-07

## P1.5 — Fix peoples-of-iran Instagram card texts for outsider clarity

Card titles and some bodies were written from an insider perspective (as if the reader already knows the article concepts). Instagram viewers haven't read the article — a title like "سبک زندگی، سطحِ نیروهای پنهان است" is cryptic to a new reader (what forces? hidden how?). All 16 cards need an outsider-clarity review.

- [x] Review all 16 titles: flag any that rely on article-internal concepts without enough standalone context
- [x] Rewrite flagged titles so they carry the section's idea on their own — no jargon, no assumed knowledge
- [x] Review bodies for the same issue (titles are higher priority)
- [x] Update `files/PanorAIma/peoples-of-iran/card-texts.md` with revised copy
- [x] Delete the story card JPEGs that changed (so gen_section_cards.py re-renders them): `rm images/PanorAIma/peoples-of-iran/stories/<slug>.jpg`
- [x] Run `python3 files/PanorAIma/peoples-of-iran/gen_section_cards.py` to regenerate affected cards
- [x] Visually verify each re-rendered card before committing
- [x] Commit and push — DONE 2026-06-13 (fae56cd: 4 titles rewritten, 3 story card JPEGs regenerated)

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
  - [ ] Add a config mapping slug → ordered list of story card filenames for the publish script to read (currently takes a single URL arg, no slug/ordering logic yet)
- [ ] Add posting-state tracking — manifest (e.g. `posted.json` per article) so the script knows which cards are already posted and picks the next one in order
- [ ] Build the cadence/scheduler — cron job or GitHub Actions to run every couple of days, matching existing posting cadence
  - [ ] Decide between a local cron job vs a GitHub Actions scheduled workflow ← depends on credential security decision
- [ ] Secure credentials — app secret + access token as env vars / GitHub Actions secrets, never committed
- [ ] Handle token expiry — add a refresh step or calendar reminder (IG long-lived tokens expire ~60 days)
- [ ] Add failure handling — log/alert (push notification or email) on a failed publish call instead of silently skipping
- [ ] Wire into the existing pipeline — decide whether new articles auto-enqueue story cards for posting or require manual trigger per article

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
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
  - [ ] Upload all 18 images as a single carousel in filename order (00a → 00b → 01 → … → 16)
  - [ ] Paste the FA `caption` field from `general-caption` block as the post caption
  - [ ] Immediately after publishing, post `first_comment_en` as the first comment (no flag emojis)
  - [ ] Note: this is a one-off manual carousel post — separate from the recurring story-card automation in P1.8
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Clarify the comment surface (Instagram DMs, website, or both)
  - [ ] Draft the reply prompt template (referencing article content + reader message) and save to `files/ai-reply-template.md`
  - [ ] Test the template against a sample comment from peoples-of-iran article
- [ ] Create root `llms.txt` for AI crawler / LLM-friendly site guidance
  - [ ] Decide content scope: site summary, owner/contact, canonical sections, PanorAIma article URLs, and usage/licensing notes
  - [ ] Check `robots.txt` for any existing AI-crawler directives to keep `llms.txt` consistent with them
  - [ ] Add `/llms.txt` at the site root with concise Markdown-style guidance and important links
  - [ ] Verify `https://25mordad.com/llms.txt` is served after deploy
  - [ ] Consider adding `llms.txt` mention/link to README and sitemap if useful

## Done

- **Publish "The Peoples of Iran"** — All 18 checklist steps completed (FA + EN pages, covers, story cards, hero images, post card, sitemap, hreflang fix, build, commit/push) — 2026-06-07
