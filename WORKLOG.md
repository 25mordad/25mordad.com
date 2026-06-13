# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

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

## 2026-06-07 — Commit & push peoples-of-iran story card pipeline

### What we built

| Feature | Files |
|---|---|
| 16 JPEG story cards (941×1672, q=98) for all article sections | `images/PanorAIma/peoples-of-iran/stories/*.jpg` |
| Story card generator script | `files/PanorAIma/peoples-of-iran/gen_section_cards.py` |
| Card texts source of truth | `files/PanorAIma/peoples-of-iran/card-texts.md` |
| Background images (light + dark variants) | `files/PanorAIma/peoples-of-iran/bg-d.png`, `bg.png` |
| HTML test card templates | `files/PanorAIma/peoples-of-iran/test-card-d.html`, `test-card.html` |
| Updated FA long + short drafts | `files/PanorAIma/peoples-of-iran/peoples-of-iran-fa.md`, `peoples-of-iran-fa-short.md` |
| Extended .gitignore to exclude generated outputs | `.gitignore` |
| Pipeline documentation | `files/PanorAIma/peoples-of-iran/PDF-WORKFLOW.md` |

### Decisions

#### 1. Exclude generated HTML/PDF/preview PNGs from git
**Why:** Regenerable from MD sources; 900KB+ PDFs bloat the repo history with no meaningful diff value.
**How:** Added gitignore patterns `files/PanorAIma/**/*.pdf`, `files/PanorAIma/**/peoples-of-iran-*.html`, `files/PanorAIma/**/preview-*.png`.

#### 2. Keep gen_images.py (deprecated OpenAI API approach)
**Why:** Historical record of the old approach — useful context if the strategy ever reverts to API-generated images.
**How:** Committed alongside the new `gen_section_cards.py` with a deprecation note in the card-texts header.

### Pending / TODO

- [ ] Pick one story card as feature image → copy to `images/PanorAIma/peoples-of-iran.jpg`
- [ ] Add post card to `PanorAIma/index.html` (.post-card pattern, date ۱۶ خرداد ۱۴۰۵, EN/FA links)
- [ ] Update `PanorAIma/next/index.html` to point to next upcoming article
- [ ] Add both URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod 2026-06-07`
- [ ] Extract/translate EN article body to `peoples-of-iran-en.md` from FA draft
- [ ] Produce EN short version `peoples-of-iran-en-short.md`
- [ ] Create `PanorAIma/peoples-of-iran-en/index.html` (copy from iran-compressed-historical-moment-en)
- [ ] Create `PanorAIma/peoples-of-iran-fa/index.html` (copy from iran-lahzeye-feshordeh-tarikh-fa)
- [ ] Run `npm run build:css`
- [ ] Final commit and push

---

## 2026-06-06 — Organize article files and plan image generation

### What we built

| Feature | Files |
|---|---|
| Consolidated all peoples-of-iran draft + script files into one folder | `files/PanorAIma/peoples-of-iran/` (peoples-of-iran-fa.md, peoples-of-iran-fa-short.md, مردمان ایران.odt, .odt.bak, gen_short.py, slugfix.py) |
| Restructured TASKS.md: merged image-gen tasks into P1, added gen_images.py task, removed separate P3 section | `TASKS.md` |

### Decisions

#### 1. One folder per article for draft and script files
**Why:** As articles accumulate, having scattered draft files at the repo root becomes hard to navigate. Consolidating everything for an article into `files/PanorAIma/<slug>/` makes it obvious what belongs to what and keeps the root clean.
**How:** Moved all peoples-of-iran working files (markdown drafts, helper scripts, odt and its backup) under `files/PanorAIma/peoples-of-iran/`.

#### 2. Use gpt-image-2 instead of dall-e-3
**Why:** dall-e-3 access had expired; gpt-image-2 is the currently active model on the account.
**How:** `gen_images.py` will target `gpt-image-2` with `size=1536x1024`, `quality=high`, PNG output.

#### 3. Image generation is part of the P1 publish flow
**Why:** The best generated image becomes the feature image, so image generation must happen before the feature image selection step — it is not a standalone task block.
**How:** Image-gen subtasks are embedded in P1 directly, before the feature image step.

### Pending / TODO

- [ ] Create PanorAIma/peoples-of-iran-fa/index.html
- [ ] Create PanorAIma/peoples-of-iran-en/index.html
- [ ] Write gen_images.py (14 sections, gpt-image-2, hardcoded prompts + style suffix)
- [ ] Run gen_images.py and review output
- [ ] Add feature image, embed section images, post card, sitemap, build CSS, commit/push
- [ ] Decide next article topic (P2)

---

## 2026-06-05 — Session start + .gitignore odt fix

### What we built

| Feature | Files |
|---|---|
| Created TASKS.md with P1/P2 task lists | TASKS.md |
| Added *.odt to .gitignore | .gitignore |

### Decisions

#### 1. Ignore *.odt globally
**Why:** Draft files are private working documents and should not be version-controlled.
**How:** Added `*.odt` pattern to `.gitignore`.

### Pending / TODO

- [ ] Read .odt draft and finalize article content
- [ ] Create PanorAIma/peoples-of-iran-en/index.html
- [ ] Create PanorAIma/peoples-of-iran-fa/index.html
- [ ] Add feature image: images/PanorAIma/peoples-of-iran.jpg
- [ ] Add post card to PanorAIma/index.html
- [ ] Update PanorAIma/next/index.html to point to next topic
- [ ] Add EN + FA URLs to sitemap.xml with xhtml:link alternates
- [ ] Run npm run build:css
- [ ] Commit and push article
- [ ] Decide next article topic and update teaser

---

## 2026-05-28

### Images — PanorAIma directory
- Created `images/PanorAIma/` as the dedicated image folder for all PanorAIma articles
- Moved `soon.jpg` into `images/PanorAIma/soon.jpg`
- Added `images/PanorAIma/iran-lahzeye-feshordeh-tarikh.jpg` as feature image for first article
- Updated all three pages (`next/`, EN article, FA article): og:image, twitter:image, JSON-LD image, and in-page `<img>` tag

### Feature images — first article (EN + FA)
- Added `<div class="feature-image">` block between `</header>` and `<div class="story-wrap">` in both article files
- `object-fit: cover`, `max-height: 480px`

---

## 2026-05-27

### CLAUDE.md — initial creation
- Documented dev commands, architecture table, PanorAIma article checklist, fonts/direction rules, SEO pattern, design tokens, and project gotchas

### PanorAIma/next/ — teaser page
- Created `PanorAIma/next/index.html` as a permanent "coming next" slot
- Design: pulsing border glow, blinking cursor on title, bilingual EN + FA
- Social CTAs: X and Instagram links for audience to submit questions
- Added to `sitemap.xml` with `changefreq: weekly`
- Linked from `PanorAIma/index.html` with dashed cyan border card (distinct from `.post-card`)

### Second article announced
- **Title (FA):** مردم‌های ایران؛ چند جامعه زیر یک نام
- **Title (EN):** The Peoples of Iran: Multiple Societies Under One Name
- **Publish date:** June 4, 2026 (۱۴ خرداد ۱۴۰۵)
- Updated `next/index.html` with full bilingual content, publication date pills, "در حال شکل‌گیری" chip
- Updated teaser card in `PanorAIma/index.html` with new title, description, and date
- Full SEO added to `next/`: keywords, author, all OG tags, Twitter card, canonical, JSON-LD (`@type: Article`)

### README.md + CLAUDE.md updates
- Added `PanorAIma/next/` to structure tree and architecture table
- Documented teaser page workflow in CLAUDE.md (JSON-LD type, feature image, card style, sitemap)
- Noted `images/PanorAIma/` naming convention

### Memory initialized
- Created `/memory/MEMORY.md`, `project_panoraima_next.md`, `project_site_structure.md`

---

## 2026-05-23 *(from git history)*

- Added PanorAIma bilingual article section — first article EN + FA, refined typography and SEO
- Fixed manifest icon paths
- Updated favicon assets

