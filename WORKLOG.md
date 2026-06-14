# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

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

## 2026-06-13 — Intro post cards + outsider-clarity documentation

### What we built

| Feature | Files |
|---|---|
| Title card HTML template (no panel, full-bleed vignette) | `files/PanorAIma/peoples-of-iran/test-post-title.html` |
| Dedication card HTML template (solemn dark overlay, gold rules) | `files/PanorAIma/peoples-of-iran/test-post-dedication.html` |
| Rendered title card (1080×1080, q=98) | `images/PanorAIma/peoples-of-iran/posts/00a-title-card.jpg` |
| Rendered dedication card (1080×1080, q=98) | `images/PanorAIma/peoples-of-iran/posts/00b-dedication.jpg` |
| card-texts.md blocks for slots -1 and 0 | `files/PanorAIma/peoples-of-iran/card-texts.md` |
| Outsider-clarity rule + 18-card carousel structure | `CLAUDE.md`, `memory/project_story_card_pipeline.md`, `memory/project_feed_post_pipeline.md` |

### Decisions

#### 1. Title card design: no bordered panel, full-bleed vignette
**Why:** The title card is a cover/intro — it should feel like a movie poster, not a section card. A gold-bordered panel would make it look identical to the 16 section cards, losing the visual hierarchy that tells viewers "this is the beginning."
**How:** Full-bleed background photo with a centered dark vignette overlay, text centered directly on photo. No gold border box, no label, no CTA.

#### 2. Dedication card design: solemn dark, two gold gradient rules
**Why:** The dedication is personal and memorial — it needs quiet gravitas, not the card's usual design language (label, body, CTA). A heavy dark overlay and minimal gold accents respect the tone.
**How:** Heavy dark overlay, two thin gold gradient rules bracketing the dedication text, faint ❝ opener. No section label, no CTA, no footer tagline.

#### 3. 18-card carousel structure (slots -1, 0, 1–16)
**Why:** Every article should open with a title card and dedication before the sections — it sets context for new viewers and mirrors the article's own opening structure.
**How:** Slots -1 (title-card) and 0 (dedication) defined in card-texts.md. For peoples-of-iran (sections already committed as 01–16), intro cards use 00a/00b prefix so they sort before 01. Future articles use 01/02 prefix with sections 03–18. Documented in CLAUDE.md carousel structure table.

#### 4. Outsider-clarity rule locked in for all future articles
**Why:** The original peoples-of-iran cards were written from an insider perspective — the author knew the article, so shorthand felt obvious. To a new Instagram viewer who has never read the piece, titles like «این نیروها» (these forces) are opaque. Every card must stand alone.
**How:** Rule added to CLAUDE.md story card section and both pipeline memory files. Principle: write every title and body for someone who has never read the article. If a stranger scrolling past the card wouldn't grasp the idea → rewrite it.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Playwright chromium not installed | Ran `playwright install chromium`, then rendered successfully |

### Pending / TODO

- [ ] User approval of 00a-title-card.jpg and 00b-dedication.jpg designs
- [ ] Commit test-post-title.html, test-post-dedication.html, both rendered cards, updated card-texts.md
- [ ] P2: Decide next article topic (candidates A–E in TASKS.md)
- [ ] P2: Update PanorAIma/next/index.html + teaser card in PanorAIma/index.html
- [ ] Post peoples-of-iran Instagram feed post carousel (16 section cards + 2 new intro cards)

---

## 2026-06-13 — Instagram feed post cards pipeline — peoples-of-iran

### What we built

| Feature | Files |
|---|---|
| General carousel caption block | `files/PanorAIma/peoples-of-iran/card-texts.md` |
| Feed post card renderer (Playwright, 1080×1080) | `files/PanorAIma/peoples-of-iran/gen_post_cards.py` |
| HTML template for feed post cards | `files/PanorAIma/peoples-of-iran/test-post-d.html` |
| All 16 feed post images (numbered 01–16) | `images/PanorAIma/peoples-of-iran/posts/01-*.jpg … 16-*.jpg` |
| Fixed section 1 post_body (trimmed 4→2 paragraphs) | `files/PanorAIma/peoples-of-iran/card-texts.md` |
| 3 re-rendered story cards (outsider-clarity fix) | `images/PanorAIma/peoples-of-iran/stories/from-differences-to-knots.jpg`, `lifestyle-visible-surface.jpg`, `university-social-media-contact.jpg` |

### Decisions

#### 1. Single general-caption block (not per-section captions)
**Why:** All 16 images post as one Instagram carousel (Instagram max=20), so a single caption serves the whole deck. Per-section captions would be unused and add maintenance noise.
**How:** Stripped per-section `post_caption` fields (sections 1–13), added a `## general-caption` block at the top of `card-texts.md` with hashtags including `#هوش‌واره`.

#### 2. Numbered filenames (01- through 16-)
**Why:** Instagram requires uploading images in carousel order; numbered names make it unambiguous which card is which and avoid mis-ordering when selecting files in the upload dialog.
**How:** `f"{s['num']:02d}-{s['slug']}.jpg"` in `gen_post_cards.py`.

#### 3. Body font auto-scale (27px → 13px min)
**Why:** `post_body` paragraphs vary in length across sections. A fixed font size would either truncate long bodies or leave short ones looking sparse. User wants all text fully visible.
**How:** Inline JS in the rendered HTML shrinks `.section-body` font-size until `card.scrollHeight ≤ card.clientHeight`.

#### 4. Caption CTA phrasing change
**Why:** "نوشتارِ کامل از لینکِ بایو" felt promotional and indirect; user wanted something more direct that names the site.
**How:** Changed to "نوشتار کامل در وب‌سایت ۲۵مرداد 25mordad.com"; added `#هوش‌واره` to the hashtag block.

### Challenges & Solutions

| Challenge | Solution |
|---|---|
| Section 1 had 4 paragraphs in post_body vs 2 for all others → font auto-scaled too small | Trimmed section 1 post_body to 2 paragraphs in card-texts.md |
| Playwright chromium missing after system update | Ran `playwright install chromium` |
| post_closing/ref cut off in first render | Body auto-scale JS fixed the overflow |

### Pending / TODO

- [ ] Commit gen_post_cards.py, updated card-texts.md, and all 16 post images
- [ ] P1.5: commit remaining story card fixes (4 re-rendered stories already committed in fae56cd)
- [ ] P2: decide next article topic, update PanorAIma/next/index.html and teaser card

---

## 2026-06-07 — Publish peoples-of-iran EN page + bilingual cover pipeline

### What we built

| Feature | Files |
|---|---|
| EN article page (long draft, cover at top, ToC, citations, PDF link) | `PanorAIma/peoples-of-iran-en/index.html` |
| EN cover image (Space Grotesk, LTR, 1200×1200, q=98) | `files/PanorAIma/peoples-of-iran/test-cover-en.html`, `images/PanorAIma/peoples-of-iran/cover-en.jpg` |
| EN long draft staged | `files/PanorAIma/peoples-of-iran/peoples-of-iran-en.md` |
| Sitemap entries for EN + FA with xhtml:link alternates | `sitemap.xml` |
| hreflang x-default fix in FA page (x-default → EN slug) | `PanorAIma/peoples-of-iran-fa/index.html` |

### Decisions

#### 1. No short EN version
**Why:** EN readers get the full long draft. A short version would dilute the content and add maintenance overhead for a language variant that already has fewer readers than FA.
**How:** Removed the short EN step from Phase 1 of the article checklist. `peoples-of-iran-en.md` is the only EN draft file.

#### 2. No per-section hero images in EN page
**Why:** Hero images are Vazirmatn FA-script labels and Persian body text — they don't make sense on an English page. The EN cover (Space Grotesk, LTR) serves as the single visual anchor.
**How:** EN page has one `.cover-image` div at the top of the article body. No `<figure>` embeds after headings.

#### 3. Two covers per article (FA + EN)
**Why:** OG/Twitter meta and the article body both need a language-appropriate cover. Using the FA cover (Vazirmatn, RTL) as the EN page's OG image looks broken to English-speaking sharers.
**How:** `test-cover-d.html` → `cover.jpg` (FA, Vazirmatn, RTL); `test-cover-en.html` → `cover-en.jpg` (Space Grotesk, LTR). Both templates and outputs are archived in the peoples-of-iran folder as the canonical example.

#### 4. x-default hreflang standardized to EN slug
**Why:** Google's hreflang spec requires x-default to point to the same URL consistently across all language variants. The FA page had x-default → FA slug (itself), creating a mismatch with the EN page and sitemap.
**How:** Fixed `<link rel="alternate" hreflang="x-default">` in the FA page to point to the EN slug, matching the EN page and sitemap entries.

### Pending / TODO

- [ ] P2: Decide next article topic
- [ ] P2: Update `PanorAIma/next/index.html` with new title, description, and dates
- [ ] P2: Update teaser card in `PanorAIma/index.html`
- [ ] P2: Update memory `project_panoraima_next.md`
- [ ] P2: Draft AI-assisted comment reply prompt template

---

## 2026-06-07 — Add peoples-of-iran post card to PanorAIma listing

### What we built

| Feature | Files |
|---|---|
| Post card for "مردمان ایران" on listing page | `PanorAIma/index.html` |
| Cover image at top of card (full-width, height:auto) | `PanorAIma/index.html` |
| Teaser "Coming Next" removed (article published) | `PanorAIma/index.html` |

### Decisions

#### 1. No max-height on cover image in card
**Why:** The cover is a 1200×1200 square; applying max-height caused it to render visibly cropped, cutting off the design.
**How:** Set `height:auto` with no overflow constraint — the full image renders at its natural proportions inside the card.

#### 2. Hide teaser rather than delete
**Why:** The teaser HTML is reusable for the next article announcement (P2). Deleting it means rewriting it from scratch.
**How:** Replaced the teaser `<section>` with an HTML comment so content is preserved for P2 re-use.

### Pending / TODO

- [ ] Add EN + FA URLs to sitemap.xml with xhtml:link alternates and lastmod 2026-06-07
- [ ] Translate FA long draft → peoples-of-iran-en.md (16 sections, preserve [n] citations)
- [ ] Produce peoples-of-iran-en-short.md (short EN, same 16 sections + refs)
- [ ] Create PanorAIma/peoples-of-iran-en/index.html from EN short draft + hero images
- [ ] Run npm run build:css
- [ ] Commit and push
- [ ] P2: Decide next article topic, update next/index.html and teaser card

---

> Older entries archived in WORKLOG_ARCHIVE.md
