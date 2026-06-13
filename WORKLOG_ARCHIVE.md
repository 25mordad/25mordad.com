# Worklog Archive

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
