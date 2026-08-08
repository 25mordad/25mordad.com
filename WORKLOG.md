# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

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

## 2026-08-09 — Wrote and polished third PanorAIma article "زنده‌ماندن یا زیستن؟" (draft, unpublished)

### What we built

| Feature | Files |
|---|---|
| Third article moved from wrong (public) path into private working dir | `files/PanorAIma/surviving-or-living/sections/*.md` |
| Citations converted to project's `[n]` + `## منابع` convention, 25 sources, strict ascending order | `files/PanorAIma/surviving-or-living/sections/99-manabe.md` |
| Merged single-file draft for review | `surviving-or-living-fa.md` (frozen, untouched after creation) |
| Fully revised working draft: de-duplicated repeated concepts, unified formatting, numbered ToC removed → added, two new war-normalization paragraphs, restructured "concerns" passage | `surviving-or-living-fa-v2.md` |
| Short version (~3,900 words, all 25 citations + all named thinkers preserved) | `surviving-or-living-fa-short.md` |
| Review PDFs (30pp long, 15pp short) for sharing with close friends | `surviving-or-living-fa-v2.pdf`, `surviving-or-living-fa-short.pdf` |
| Reusable markdown→PDF generator (Chrome headless, RTL, Persian-digit ToC) | `make_pdf.py` |
| Suggestion tracker for unapplied/resolved proposals | `review-notes.md` |

### Decisions

#### 1. Keep the whole draft article out of the public repo until publication is decided
**Why:** Unlike every prior PanorAIma article, this one is not yet approved for publication — the user wants to share PDFs with close friends for feedback first. The standard convention (`files/PanorAIma/<slug>/` is tracked, only PDFs/previews are gitignored) would have exposed the full draft, including in-progress research and unresolved statistical claims, on the public repo.
**How:** Added `files/PanorAIma/surviving-or-living/` as its own line in `.gitignore` (existing PDF/preview patterns weren't enough — the whole directory was untracked but NOT ignored, so a bare `git add -A` would have picked it up). Remove this line once the article is approved and moved to `PanorAIma/<slug>-fa|en/`.

#### 2. Don't silently "correct" uncited statistics — verify or fold into what the source actually says
**Why:** The original draft had a specific inflation figure (۴۲.۲٪ for 2025) that turned out to not exist in any source — the World Bank's most recent data point is 2024. Guessing or inventing a number for a public-facing article would be a factual-integrity risk.
**How:** Web-searched each of 4 flagged statistics individually. Where the number existed but was wrong (IMF Iran 2026 growth), corrected it with the right vintage. Where it didn't exist at all (2025 inflation), rewrote the sentence to use the two years that ARE verified (2023: 44.6%, 2024: 32.5%) rather than inventing a replacement.

#### 3. Never introduce a new concept in two sections — pick the section where it's structurally load-bearing
**Why:** Found three near-duplicate passages across sections (Diane Vaughan's "normalization of deviance," `maladaptation`, and McEwen's "allostatic load" all appeared in both section 2 and section 5, nearly verbatim). Established a repeatable test: keep the concept in whichever section it's the central thesis for, not wherever it was first drafted.
**How:** Section 5 ("وقتی سازگاری فرساینده می‌شود") is literally about erosive adaptation — `maladaptation` and allostatic load are foundational there. Section 2 ("تاب‌آوری یا عادی‌سازی؟") already has its defining citations (Norris, Vaughan); removed the decorative repeats and rewrote the connecting sentences so the paragraph flow survives the cut.

#### 4. Renumbering citations after a mid-document edit requires re-deriving the whole sequence, not patching numbers
**Why:** An earlier edit (removing a duplicate Vaughan paragraph from section 1) had left a citation-ordering bug — `[۵]` appeared before `[۴]` in reading order because the number wasn't re-verified after the paragraph that used it was deleted. Discovered only because today's cleanup touched the same numbers again.
**How:** Built the full first-appearance sequence from scratch (source → its correct position in reading order) each time a citation moved sections, remapped every old→new number, and re-verified with `grep -oE '\[[۰-۹]+\]'` across every section file, the merged file, and the references list before considering it done.

#### 5. A short version's job is compression, not selection — verified nothing was dropped
**Why:** User explicitly required that "پشتوانه‌ی فکری" (every citation and every named thinker) survive into the short version, not just the concepts.
**How:** After drafting the short version, ran a grep pass checking every one of the 21 named thinkers and all 25 citation numbers appear in the short file before presenting it — caught that `diglossia` (the only uncited concept in the whole article) had been dropped, and restored it on request.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Draft material was sitting inside the *published* site path (`PanorAIma/3-materials/`) instead of the private `files/` convention | Moved to `files/PanorAIma/surviving-or-living/sections/` before anything was committed — confirmed nothing had been pushed, so no exposure occurred |
| User's explicit "don't touch the text, only propose" instruction mid-session vs. later explicit "let's fix it" approvals | Tracked every proposal in `review-notes.md` first; only edited files after an explicit go-ahead per item, never bundled |
| A background `grep` search (queued earlier for ToC precedent-checking) resolved mid-conversation as an unrelated task notification | Confirmed its (empty) result actually answered the pending question — published FA articles have no ToC — before treating it as closed |

### Pending / TODO

- [ ] User to review both PDFs with close friends before any publish decision
- [ ] Final full read-through pass on Opus model (session currently on Sonnet for routine work, per user's model-switching plan)
- [ ] Once approved for publication: move to `PanorAIma/<slug>-fa|en/`, remove the `.gitignore` exclusion, follow the full Phase 2–4 checklist in CLAUDE.md (covers, hero images, story/post card decks, sitemap, EN translation)
- [ ] Build a tone/voice profile for the user (using articles 2 and 3 as reference) — explicitly deferred to last, after this article is fully finalized
- [ ] No Instagram/Twitter work of any kind for this article — that whole system is being redesigned separately (standing constraint for this article)
- [ ] P1.8 Instagram automation subtasks — untouched this session, still open (see TASKS.md)
- [ ] P2: peoples-of-iran Instagram feed carousel post — untouched this session, still open

---

> Older entries archived in WORKLOG_ARCHIVE.md
