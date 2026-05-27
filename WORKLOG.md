# WORKLOG

Reverse-chronological log of work sessions on 25mordad.com.

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

