# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Personal website of Bahman Reshadipour (25mordad). A fully static site — plain HTML files with Tailwind CSS compiled locally. No JavaScript framework, no SSG, no server-side logic. Live at https://25mordad.com.

## Dev Commands

```bash
npm install           # install tailwindcss devDependency
npm run watch:css     # rebuild assets/tailwind.css on every src/tailwind.css change
npm run build:css     # one-shot minified build (run before committing)
```

After any HTML change that uses new Tailwind utility classes, rebuild CSS. The Tailwind config scans `index.html`, `404.html`, `projects/**/*.html`, `PanorAIma/**/*.html`, and `writings/**/*.html`.

## Architecture

| Path | Purpose |
|------|---------|
| `src/tailwind.css` | Source CSS (just three `@tailwind` directives) |
| `assets/tailwind.css` | Compiled + minified output — never edit directly |
| `index.html` | Home page |
| `projects/index.html` | Projects page with anchor sections (`#fintech`, `#science`, `#travel`, `#news`, `#it`, `#selfexperience`) |
| `PanorAIma/index.html` | Writing section landing page — lists post cards |
| `PanorAIma/next/index.html` | Permanent "coming next" teaser slot — always points to the upcoming article |
| `PanorAIma/<slug>/index.html` | Individual published article pages |
| `sitemap.xml` | Must be updated manually with every new page |
| `assets/pdf/PanorAIma/<slug>/<slug>-fa.pdf` | FA article PDF — committed and served; source in `files/` is gitignored |
| `assets/pdf/PanorAIma/<slug>/<slug>-en.pdf` | EN article PDF — same pattern |
| `images/PanorAIma/<slug>/cover.jpg` | Cover / feature image for the article listing card — generated from `test-cover-d.html` |
| `images/PanorAIma/<slug>/heroes/<section-slug>.jpg` | Square hero images (1200×1200) — one per section, embedded in article body |
| `images/PanorAIma/<slug>/stories/<section-slug>.jpg` | Vertical Instagram story cards (941×1672) — one per section |
| `images/PanorAIma/<slug>/posts/<nn>-<section-slug>.jpg` | Square Instagram feed post cards (1080×1080) — one per section, numbered 01–16 for carousel upload order |
| `images/PanorAIma/soon.jpg` | Placeholder feature image used on the teaser page before the cover is ready |
| `images/site.webmanifest` | PWA manifest (icon paths are `/images/…`) |
| `scripts/` | Python automation scripts (Instagram API, Lightroom API) — separate from the per-article Playwright generators in `files/PanorAIma/<slug>/` |
| `images/ig-queue/<asset-id>.jpg` + `.json` | Personal photo series queue — fetched from Lightroom, one image + status/caption record per photo. See **Personal Photo Series** |
| `scripts/.venv/` | Python virtualenv for `scripts/` — gitignored, recreate with `python3 -m venv scripts/.venv && scripts/.venv/bin/pip install -r scripts/requirements.txt` |
| `.env` | Project-root secrets (e.g. `IG_ACCESS_TOKEN`) — gitignored, never committed. **This repo is public** — never write secret values into any tracked file, including this one |

## Python Automation Scripts (`scripts/`)

Run any script with the venv's interpreter directly — no need to activate first:
```bash
scripts/.venv/bin/python scripts/<script>.py
```
Scripts that need credentials load them from project-root `.env` via `python-dotenv` (see `scripts/test_ig_token.py` for the pattern). Never print/log raw secret values — this repo is public.

`scripts/publish_story.py <image_url>` publishes a single Instagram Story from a public image URL (container create → poll `status_code` until `FINISHED` → `media_publish`). Default posting cadence is one card every couple of days; a same-session full-deck blast is a deliberate one-off, not the default. The Stories API supports only `image_url`/`video_url` and `user_tags` (mentions) — no captions, music, link/poll/location/hashtag stickers (app-only). Comments API applies to feed/Reels/carousel posts only, never Stories.

## PanorAIma (Writing Section)

Each article is **bilingual** — one EN page and one FA page, always published together.

Slug convention:
- English: `PanorAIma/your-post-slug-en/index.html`
- Farsi: `PanorAIma/your-post-slug-fa/index.html`

### Terminology

- In Persian site copy and metadata, use `هوش‌واره` as the project’s preferred Persian word for AI / AI-assisted work.
- Keep the spelling with the zero-width non-joiner: `هوش‌واره`.
- Persian PanorAIma chips should use `تحلیل با هوش‌واره`.

### Adding a New Article — Checklist

Work in this order. Each phase depends on the previous.

#### Phase 1 — Drafts

1. Write the long FA draft → `files/PanorAIma/<slug>/<slug>-fa.md` (section headings + body + `[n]` citations + `## منابع` list).
2. Write the short FA draft → `<slug>-fa-short.md` (same sections + same refs, compressed to ~1–3 paragraphs per section — see **Short and Long Versions**).
3. Translate long FA → long EN draft → `<slug>-en.md` (preserve all `[n]` inline citations).
   - **No short EN version** — the EN article always uses the long draft only.

#### Phase 2 — Image assets

5. Place background images `bg-d.png` (dark, preferred) and `bg.png` (light) in `files/PanorAIma/<slug>/`.
6. Write `card-texts.md` — one `## <n> — <section-slug>` block per section (label, title, body, ref, cta, music). See **Instagram Story Card Deck** for field rules.
7. Copy `gen_section_cards.py` from the previous article, update `OUTPUT_DIR` slug → run → 18 story cards (title, dedication, 16 sections) in `images/PanorAIma/<slug>/stories/`.
7b. Copy `gen_post_cards.py` from the previous article, update `OUTPUT_DIR` slug → add `## general-caption` to `card-texts.md` → run → 18 feed post cards in `images/PanorAIma/<slug>/posts/`. See **Instagram Feed Post Cards**.
8. Copy `gen_hero_images.py` from the previous article, update `OUTPUT_DIR` slug → run → 16 hero images in `images/PanorAIma/<slug>/heroes/`. See **Hero Images**.
9. Create covers — two files, two renders. See **Cover / Feature Image**:
   - FA cover: `test-cover-d.html` → `images/PanorAIma/<slug>/cover.jpg` (Vazirmatn, RTL, FA text)
   - EN cover: `test-cover-en.html` → `images/PanorAIma/<slug>/cover-en.jpg` (Space Grotesk, LTR, EN text)

#### Phase 3 — HTML pages

10. `mkdir -p PanorAIma/<slug>-fa && cp PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html PanorAIma/<slug>-fa/index.html`
11. In the FA page update: `<title>`, meta description/keywords, all OG/Twitter tags (OG image → `cover.jpg`), canonical, hreflang (FA↔EN + x-default), JSON-LD `BlogPosting` (`headline`, `datePublished`, `dateModified`, `url`, `inLanguage: "fa-IR"`, `image: cover.jpg`). Replace article body with FA content. Add `تحلیل با هوش‌واره` chip.
12. Embed hero images in FA page: after each `<h2>` heading add `<figure><img src="/images/PanorAIma/<slug>/heroes/<section-slug>.jpg" alt="<section title in FA>"></figure>`.
13. `mkdir -p PanorAIma/<slug>-en && cp PanorAIma/peoples-of-iran-en/index.html PanorAIma/<slug>-en/index.html`
14. In the EN page update all the same fields (inLanguage: `"en"`, OG image → `cover-en.jpg`). Replace article body with **long EN content only** (no short version). Add `AI-Assisted` chip.
    - **No per-section hero images in the EN page.** Place only the EN cover at the top of the article body (inside `.cover-image` div, `border-radius: 1rem`).
    - Add PDF download link (`.versions-block`) after the byline: `<a href="/assets/pdf/PanorAIma/<slug>/<slug>-en.pdf">Full version</a>`.
    - EN page template to copy: `PanorAIma/peoples-of-iran-en/index.html` (has ToC, superscript citations, `.refs` section, `.cover-image` div, `.versions-block`).

#### Phase 4 — Publish

15. Copy PDFs to committed path: `mkdir -p assets/pdf/PanorAIma/<slug> && cp files/PanorAIma/<slug>/*.pdf assets/pdf/PanorAIma/<slug>/`. PDFs in `files/` are gitignored; `assets/pdf/` is committed and served.
16. Add post card to `PanorAIma/index.html` above the teaser card (`.post-card` pattern: `.meta-pill` date in both EN and FA calendar, `.lang-actions` EN/FA links, `.fa-preview` block for FA subtitle).
17. Add both EN and FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod`.
18. Update `PanorAIma/next/index.html` to point to the next upcoming article.
18. Run `npm run build:css`.
19. Commit and push.

### Draft-Stage Privacy

Normally an article's whole `files/PanorAIma/<slug>/` working directory is tracked and committed (only PDFs/HTML previews are gitignored — see the table above). If an article is still being drafted/reviewed and publication hasn't been decided yet (e.g. sharing PDFs with friends for feedback first), add the whole `files/PanorAIma/<slug>/` directory as its own line in `.gitignore` instead. A bare `git add -A` does **not** skip untracked-but-not-ignored directories, so without this the draft — including unresolved statistical claims, private notes, etc. — would land on the public repo. Remove the `.gitignore` line once publication is approved and the article moves to `PanorAIma/<slug>-fa|en/`.

### Short and Long Versions

Each article has a **long** draft and a **short** draft (e.g. `peoples-of-iran-fa.md` and `peoples-of-iran-fa-short.md`). The short version exists because many readers today are put off by long-form pieces — it's prepared for people who want to read faster.

Rules for producing the short version from the long one:

- **Same structure** — identical section headings in the identical order. The short version is a section-by-section mirror, not a re-outline.
- **Keep the concept** — every section's core idea must survive the cut. Compress wording, never drop a concept.
- **Always keep the references** — the same `[n]` citations and the same numbered `## منابع` list carry over. Condensing the prose must not strip the scholarly sourcing.
- **Compress, don't summarize away** — each section becomes ~1–3 tight paragraphs.
- When the long version gains a new section or reference, mirror the same change into the short version (heading, condensed body, and any new `[n]` reference).
- Shared front matter (author byline, dedication) appears in both versions.

### Instagram Story Card Deck

Each article ships with a deck of **Instagram story cards** — a title card, a dedication
card, then one card per article section (18 cards total, mirroring the feed-post carousel
structure) — to promote the piece on Instagram (posted every couple of days, or as a
one-off full-deck blast around launch — see Posting Cadence note below). Source of truth is
`files/PanorAIma/<slug>/card-texts.md`; cards render via `gen_section_cards.py` (Playwright,
941×1672) over a single background photo (`bg-d.png`, dark preferred), output to
`images/PanorAIma/<slug>/stories/<section-slug>.jpg` (section cards) and
`images/PanorAIma/<slug>/stories/{title-card,dedication}.jpg` (intro cards, reusing the
`-1`/`0` blocks already defined for the post carousel — `title`/`subtitle`/`author` for the
title card, `body` for the dedication card — rendered in the same dark/gold story style via
dedicated `HTML_TITLE_TEMPLATE`/`HTML_DEDICATION_TEMPLATE`).

**Posting cadence:** the default is one card every couple of days. A full-deck same-session
publish (all 18 cards back-to-back) is a deliberate one-off for an article's launch, not the
standing default — only do it when explicitly asked.

Purpose: each card **delivers one section's core idea on its own** (a self-contained taste,
not a teaser, and **not** a request for comments). A short CTA then nudges the reader to the
full article; the actual link/sticker is added on the story afterwards, not baked into the image.

**Outsider-clarity rule (always):** write every title and body for someone who has **never read
the article** and may not know the topic. As the author, shorthand that references article
concepts feels obvious — to a new Instagram viewer it is opaque. Every card must stand alone:
no article-internal jargon, no floating references («این نیروها», «گره‌ها», etc.) without context.
If a stranger scrolling past the card wouldn't grasp the idea → rewrite it.

`card-texts.md` structure:
- A header (purpose note + `## Format` + `## Shared elements`), then one `## <n> — <section-slug>` block per section.
- Each block carries these labelled lines:
  - **label:** gold section label, Persian ordinal (بخش اول، دوم، …).
  - **title:** white card title; `<br>` controls line breaks.
  - **body:** the section's core idea, ~3–6 short lines, self-contained, RTL Persian.
  - **ref:** *(optional)* a faint one-line source credit, only where a single named thinker
    anchors the section **and** there's room — mention the ref only when char limits allow,
    otherwise omit. Derived from the article's `[n]` source for that section.
  - **cta:** a **different-every-time** phrase encouraging the reader to open the full article
    (never reuse the same wording across cards). When the CTA names the blog, use the blog
    name **«فراتر از قاب»** — never «۲۵مرداد» / «25Mordad». When referring to the piece
    itself, always use **نوشتار** — never «مقاله».
  - **music:** 3 concept-fit candidate tracks for the story audio, `★` = recommended.
    Inline in each block (not a separate list). Instrumental / Persian classical / folk /
    cinematic — chosen to match the section's *mood*, no language limit.
- **Shared elements** (byline, footer site `25Mordad.com`, tagline, background) are set in
  the script, not repeated per block.

Workflow rules:
- Build and approve **section 1's card first** (design validation) before writing the rest.
- One block per article section, in the **same order** as the article; bodies mirror the
  section's concept (compress, never drop the idea).
- The card design template lives in `files/PanorAIma/<slug>/test-card-d.html` (`.card`,
  `.section-*`, `.footer` CSS) — reuse it in `gen_section_cards.py`. When rendering, wire
  `ref` as a faint line under the body and `cta` just above the footer; `music` is not drawn
  on the card (it's the audio picked when posting).

Technical decisions (locked in — replicate for every article):
- **Output format:** JPEG at `quality=98` (not PNG). ~400–500 KB per card vs ~1.6 MB PNG.
  Playwright outputs JPEG natively when the path ends in `.jpg`.
- **Output path:** `images/PanorAIma/<slug>/stories/<section-slug>.jpg` — the `stories/`
  subfolder separates story cards from other article assets (feature image, feed posts, etc.).
- **Background:** two variants (`bg-d.png` dark, `bg.png` light) both placed in
  `files/PanorAIma/<slug>/`. The script picks one **randomly** on each render run. To re-render
  with a different bg, delete the output file and run again.
- **Title auto-scaling:** an inline JS snippet in the rendered HTML shrinks the title
  `font-size` (from 76px down to min 36px) until the title fits exactly within the number of
  lines implied by its `<br>` tags. This prevents long titles from wrapping unexpectedly.
- **Icons:** Unicode symbols only — no CDN fonts, no Font Awesome. Current set:
  `✦` top ornament above section label, `❝` decorative quote opener before body,
  `←` before CTA text, `✦ … ✦` flanking the footer tagline.
- **Renderer:** Playwright chromium, viewport 941×1672. Temp HTML is written next to the bg
  images so `url('bg-d.png')` resolves correctly, then deleted after screenshot. Waits for
  `document.fonts.ready` to ensure Vazirmatn loads before capture.
- **Skip logic:** already-generated files are skipped automatically. Delete a file to re-render it.
- **Running:** `python3 gen_section_cards.py` (all sections) or
  `python3 gen_section_cards.py <slug>` (one section).

### Instagram Feed Post Cards

Each article ships with a deck of **Instagram feed post cards** — one per section — posted as a single carousel (18 cards total, one caption). Source data is `card-texts.md`; the script is `gen_post_cards.py`.

**`gen_post_cards.py` produces all 18 cards in one run** — including the two intro cards. Do not render intro cards separately with ad-hoc Python snippets.

**Carousel structure (18 cards total):**

Every carousel has 2 intro cards before the 16 section cards:

| Slot | Slug | Content | Filename |
|------|------|---------|----------|
| -1 | `title-card` | Article title + subtitle + author name (no body, no CTA) | `01-title-card.jpg` |
| 0 | `dedication` | Full dedication text from article opening (no label, no CTA) | `02-dedication.jpg` |
| 1–16 | `<section-slug>` | Section cards (badge number, title, body, ref, closing) | `03-` through `18-<slug>.jpg` |

For peoples-of-iran (legacy — sections committed as `01–16`): intro cards are `00a-title-card.jpg` and `00b-dedication.jpg`.
For all future articles: `01-title-card.jpg`, `02-dedication.jpg`, sections `03–18`.

The `## -1 — title-card` and `## 0 — dedication` blocks in `card-texts.md` carry the intro card content. Each article's dedication text comes from the article's opening paragraph.

**To create for a new article:**

1. Copy `gen_post_cards.py` from `files/PanorAIma/peoples-of-iran/` into `files/PanorAIma/<new-slug>/`.
2. Update the one line: `OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "<new-slug>" / "posts"`.
3. Add `## -1 — title-card`, `## 0 — dedication`, and `## general-caption` blocks to `card-texts.md`.
4. Run: `python3 gen_post_cards.py`.

**Technical spec (locked in — do not change):**
- Viewport: 1080×1080 px (Instagram feed square format)
- Output: `images/PanorAIma/<slug>/posts/<nn>-<section-slug>.jpg`
- Format: JPEG `quality=98`
- **Background: `bg.png` (light) — always. Never dark, never random.** Reason: dark bg with gold text is hard to read; light bg with dark text is far more legible on Instagram.
- **Background-position: `center center`** — shows the photo's subjects throughout the image, not cut off at top or bottom.
- **Light card panel** (`rgba(252,248,240,0.92)`) with subtle gold border — replaces the old dark semi-transparent panel.
- **Dark text** throughout: title/closing `#1a0c03`, body `rgba(28,16,4,0.85)`, gold accents `#8a6412`. No white or cream text on dark.
- **Section badge replaces section label:** a small 36×36px circle in the top-left corner of the card carries the Persian section numeral (۱, ۲, …). The old "بخش اول / بخش دوم" label consumed ~40px of vertical space that is now freed for body text.
- **Body font starts large and scales down:** `.section-body` starts at 34px → 13px min; dedication starts at 44px → 22px min. Text fills ~90% of the image. Previous default of 27px left too much empty space.
- Title auto-scale: 60px → 36px min (unchanged).
- Skip logic: already-generated files are skipped automatically. Delete a file to re-render it.
- Running: `python3 gen_post_cards.py` (all 18) or `python3 gen_post_cards.py <slug>` (one card).

**card-texts.md fields used:**
- Title card (`-1`): `title`, `subtitle`, `author`
- Dedication card (`0`): `body` (multi-line, indented continuation supported by parser)
- Section cards (`1–16`): `title`, `post_body` (paragraphs separated by `¶`), `post_ref` (optional), `post_closing`
- Ignored: `label` (replaced by auto-generated badge number), `cta`, `music`, `body` (story-only field)

**Caption and first comment (`## general-caption` block):**
- `caption` field: the FA Instagram caption for the whole carousel.
  - Use **actual blank lines** as paragraph breaks — not `¶`. The caption is copy-pasted directly into Instagram; `¶` would appear literally.
  - Write about the article's **substance**, not its structure. Never reference "۱۶ بخش" or the card count — that's an insider framing invisible viewers won't care about.
  - Keep hashtags on the last line.
- `first_comment_en` field: an English first comment for EN followers. Post this as the first comment immediately after publishing.
  - Briefly explain what the article is about and link to the EN page.
  - **Never use flag emojis** (🇬🇧 etc.) — house rule.

### Hero Images

Each article ships with **square hero images** — one per section — embedded inside the article HTML body after each `<h2>` heading. Same visual design as story cards (gold-bordered dark panel over full-bleed bg photo) but square and no CTA.

**To create for a new article:**

1. Copy `gen_hero_images.py` from the previous article into `files/PanorAIma/<new-slug>/`.
2. Update the one line: `OUTPUT_DIR = REPO_ROOT / "images" / "PanorAIma" / "<new-slug>" / "heroes"`.
3. Create `test-hero-d.html` (copy from previous article, update the hardcoded section 1 content to match the new article's first section).
4. Render the test card to validate: `python3 gen_hero_images.py <section-1-slug>` — review the output before running all.
5. Run all: `python3 gen_hero_images.py`.

**Source data:** same `card-texts.md` as story cards. Fields used: `label`, `title`, `body`, `ref` (optional). Fields ignored: `cta`, `music`.

**Technical spec (locked in — do not change):**
- Viewport: 1200×1200 px
- Card: `position: absolute; inset: 80px` — leaves bg visible in margins
- Font sizes: label 30px, title 70px (auto-scales down to 32px min), body 36px, ref 22px, footer-site 34px, footer-tagline 24px
- Background: random `bg-d.png` / `bg.png` each render — delete file to re-render with different bg
- Output: `images/PanorAIma/<slug>/heroes/<section-slug>.jpg`, JPEG `quality=98`
- Skip logic: already-generated files are skipped automatically
- Running: `python3 gen_hero_images.py` (all) or `python3 gen_hero_images.py <slug>` (one section)

### Cover / Feature Image

Each article has **two cover images** — one FA, one EN. Both use the same layout but different language, font, and direction. The FA cover is used on the listing card (`PanorAIma/index.html`) and the FA article page. The EN cover is used only on the EN article page.

| File | Used by | Language | Font | Direction |
|------|---------|----------|------|-----------|
| `images/PanorAIma/<slug>/cover.jpg` | Listing card, FA page OG | FA | Vazirmatn | RTL |
| `images/PanorAIma/<slug>/cover-en.jpg` | EN page OG + body cover | EN | Space Grotesk | LTR |

**To create for a new article:**

1. Copy `test-cover-d.html` from the previous article (`peoples-of-iran`) into `files/PanorAIma/<new-slug>/`.
2. Update three things hardcoded in the FA HTML:
   - `<h1 class="article-title">` — FA title
   - `<p class="article-subtitle">` — FA subtitle
   - `<p class="tagline">` — one punchy RTL Persian line (write fresh)
3. Render → `images/PanorAIma/<new-slug>/cover.jpg`.
4. Copy `test-cover-en.html` from `peoples-of-iran` into `files/PanorAIma/<new-slug>/`.
5. Update the three equivalent EN fields.
6. Render → `images/PanorAIma/<new-slug>/cover-en.jpg`.

**Layout (same for both covers, top to bottom inside the card):**
```
✦  (ornament, gold, faint)
article title  (large bold white, auto-scales down to 36px min)
article subtitle  (muted white, lighter weight)
──◆──  (gold divider)
tagline  (one line, muted white)
```
Footer sits outside the card, absolutely positioned at bottom:
```
FA: بهمن رشادی  /  EN: Bahman Reshadipour  (gold, 26px, medium)
25Mordad.com  (gold, 30px, bold)
FA: ✦ فراتر از قاب ✦  /  EN: ✦ Beyond The Frame ✦  (dim gold, 22px, light)
```

**Rules:**
- **Background:** always `bg-d.png` (dark) — do not randomise the cover
- **Format:** 1200×1200 px JPEG `quality=98`
- **FA author:** always `بهمن رشادی`; **EN author:** always `Bahman Reshadipour`
- **Tagline:** write fresh per article and per language — captures the article's core question or tension

**Render snippet (run once per cover file):**
```python
from pathlib import Path
from playwright.sync_api import sync_playwright

# FA cover
html_file = Path("files/PanorAIma/<slug>/test-cover-d.html").resolve()
out = Path("images/PanorAIma/<slug>/cover.jpg")

# EN cover — change both paths:
# html_file = Path("files/PanorAIma/<slug>/test-cover-en.html").resolve()
# out = Path("images/PanorAIma/<slug>/cover-en.jpg")

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page(viewport={"width": 1200, "height": 1200})
    page.goto(f"file://{html_file}", wait_until="networkidle", timeout=30_000)
    page.wait_for_function("document.fonts.ready")
    out.parent.mkdir(parents=True, exist_ok=True)
    page.screenshot(path=str(out), clip={"x":0,"y":0,"width":1200,"height":1200}, quality=98)
    browser.close()
```

### Fonts and Direction

- English article body: `"Source Serif 4"` (serif, via Google Fonts)
- PanorAIma landing + UI chrome: `"Space Grotesk"` (sans-serif, via Google Fonts)
- Home page Farsi inline text: `"Vazir"` (CDN: `rastikerdar/vazir-font`)
- PanorAIma Farsi text: `"Vazirmatn"` (via Google Fonts), class `fa-text`, always paired with `dir="rtl"` and `lang="fa"`

### Teaser Page (`PanorAIma/next/`)

A permanent slot that always previews the next upcoming article. Workflow:

- Update title, description, dates, and feature image (`images/soon.jpg` or similar) when a new article is announced.
- Uses `@type: Article` JSON-LD (not `BlogPosting` — content isn't published yet).
- Feature image is placed inside `.teaser-card` with `rounded-2xl overflow-hidden` and `max-height: 360px`; also set as OG/Twitter image.
- Teaser card in `PanorAIma/index.html` uses a dashed cyan border style — distinct from the solid `.post-card` used for published articles.
- `sitemap.xml` entry uses `changefreq: weekly` (updates more often than published articles).
- When the article publishes: create the proper EN + FA slug folders, update `PanorAIma/next/` to point to the next topic.

### SEO Pattern

Every page includes: canonical, OG tags (title, description, type, url, image, locale), Twitter card tags, and JSON-LD structured data. Article pages use `@type: BlogPosting`; teaser page uses `@type: Article`; home page uses `@type: Person` + `@type: WebSite`.

## Personal Photo Series (Lightroom → Instagram Feed)

A pipeline separate from PanorAIma: curates the owner's personal photography from a Lightroom
Cloud album into single-image Instagram Feed posts, drip-posted over time (not a carousel —
"post them one by one"). Built 2026-08-11 on the mini PC.

### Adobe Lightroom API access

- Adobe's docs are inconsistent across three different surfaces — Firefly Services (Enterprise
  contract required), Lightroom Partner APIs (needs Adobe partner approval), and a plain
  **Lightroom Services** option in the standard Developer Console that's genuinely self-serve.
  Use the third one: Developer Console → new project → Add API → **Lightroom Services** →
  credential type **OAuth Web App** (not Native/SPA — needs a `client_secret` for the
  unattended refresh flow). No Enterprise contract required. Scopes
  `openid,AdobeID,lr_partner_apis,lr_partner_rendition_apis,offline_access` are included by
  default and can't be deselected.
- Adobe requires the redirect URI to be **HTTPS even for localhost** — `scripts/lr_auth.py`
  generates a self-signed cert into `scripts/.certs/` (gitignored) on first run; the browser
  will show a one-time cert warning during the consent flow, expected.
- IMS auth endpoint: `GET https://ims-na1.adobelogin.com/ims/authorize/v1`. Token
  exchange/refresh (same endpoint for both): `POST https://ims-na1.adobelogin.com/ims/token/v1`,
  form-encoded body. (These are verified against Adobe's own `aio-lib-ims` SDK source — Adobe's
  prose docs are unreliable/inconsistent about version suffixes.)
- The actual Lightroom data API is a **different host**: `https://lr.adobe.io/v2/`, headers
  `X-API-Key: <LR_CLIENT_ID>` + `Authorization: Bearer <access_token>`. Every response body is
  prefixed with `while (1) {}` (XSSI guard) — must be stripped before JSON parsing (handled by
  `scripts/lr_common.py`'s `lr_get()`).
- Album-assets listing needs `?embed=asset` or the payload comes back empty; the real asset is
  nested at `resources[].asset`, not the outer `resources[]` (that outer id is just the
  album-membership id). Rendition downloads (`assets/{id}/renditions/{size}`) return the JPEG
  **synchronously** on the first `GET` — no async poll needed.
- **Refresh-token lifetime is unverified.** Access token confirmed ≈41.6 days via live API
  response, but Adobe doesn't return the refresh token's own expiry. Re-run
  `scripts/lr_refresh_token.py` around **2026-08-25** to check whether it's still valid or
  `scripts/lr_auth.py` needs to be re-run.

### Scripts (`scripts/`, same `.venv` as the Instagram Story scripts — `requests` + `python-dotenv`, no new deps)

| Script | Purpose |
|---|---|
| `lr_auth.py` | One-time OAuth flow (local HTTPS callback server), saves `LR_REFRESH_TOKEN` to `.env` |
| `lr_refresh_token.py` | Verifies/renews the refresh token |
| `lr_common.py` | Shared `get_access_token()` / `lr_get()` helpers |
| `lr_list_album.py "<album name>"` | Lists an album's assets — spot-check tool |
| `lr_fetch_photo.py` | Pulls new assets from the Lightroom album named **`instagram`** at the `1280` rendition (not `2048` — ~300KB vs ~1.1MB, no visible quality loss since Instagram's feed only displays up to ~1440px), writes `images/ig-queue/<asset-id>.jpg` + a JSON record, skip-logic on already-fetched assets |

### Privacy constraint

Standard EXIF (camera model, lens, exposure settings) is fine to keep on committed photos.
What must **never** leak into anything committed or logged is the **local file path on the
phone or computer** — Lightroom's `payload.importSource.localAssetId` field carries the exact
on-device storage path, plus `uniqueDeviceId`/`importedBy` device identifiers. Confirmed via a
raw-byte scan of a real downloaded rendition that these are Lightroom-catalog-only fields, not
embedded in the JPEG itself — but `lr_fetch_photo.py` still (1) never writes the
`importSource` block into any record and (2) runs a built-in raw-byte safety scan on every
downloaded file (checking for `/storage/`, `/Users/`, `/home/`, `C:\Users` patterns), refusing
to save if any match.

### Per-photo record (`images/ig-queue/<asset-id>.json`)

```json
{
  "asset_id": "...",
  "image": "<asset-id>.jpg",
  "capture_date": "...",
  "fetched_at": "...",
  "status": "draft",
  "series": "<active series name>",
  "title": null,
  "caption": null
}
```

`status` gates publishing (`draft` → `approved` → `posted` — nothing gets posted unless
`approved`, mirroring the Instagram Story publish pattern). `series` auto-fills from the
`SERIES_NAME` constant in `lr_fetch_photo.py` — update that constant when the user starts a
new series (current series: **«دنیا بزرگتر از اونه که ما تصور می‌کنیم»**, Ethiopia photos).

### Caption workflow (per photo)

1. Propose **two distinct fictional micro-stories** inspired by the photo — explicitly not
   documentary/travel-journal, doesn't need to relate to the actual location — and let the
   user pick between them. Their pick is a live calibration signal for tone/imagery
   preference; note what distinguished the winning option so future drafts lean that way.
2. The user names the photo themselves (the one thing they must approve per photo) — offer
   title suggestions too, spanning blunt/colloquial to poetic; their taste so far has run
   toward short deadpan slang (e.g. «یارو») over lyrical phrasing.
3. Assemble the final caption in this exact structure — **one combined bilingual caption, no
   first comment** (different from the PanorAIma carousel convention of FA caption + EN first
   comment — don't conflate the two):
   1. Line 1: the chosen title in Persian quote marks («»), alone on its own line
   2. The winning fictional story — Persian version, then its English translation, both in
      the same caption block
   3. Fixed bilingual closing line, appears on **every** photo in the series:
      `دنیا بزرگتر از اونه که ما تصور می‌کنیم.` / `The world is bigger than we imagine.`
   4. ~28-30 hashtags, Persian + English mixed, biased toward **high-volume/trending**
      photography-travel tags (e.g. `#photography #travelphotography #instatravel
      #wanderlust #explorepage`, `#عکاسی #سفر #هنر`) over niche invented compounds — plus the
      series tags and **always `#هوش‌واره`** (this whole pipeline is AI-assisted)

### Not yet built

Publish script (adapted from `scripts/publish_story.py`'s container→poll→publish pattern, for
a single-image Feed post with a real caption instead of a Story), the ~2-day scheduled posting
job, and a Telegram-based approval channel as an alternative to approving in-session.

## Icons

Font Awesome via kit `b4878587d2.js` (loaded from fontawesome.com). All icon usage is `<i class="fa-...">`.

## Design Tokens (PanorAIma pages)

```css
--bg-1: #1b2129;
--bg-2: #111722;
--line: rgba(148, 163, 184, 0.28);
--panel: rgba(15, 23, 42, 0.74);
--ink: #e5e7eb;
```

Home page uses flat `bg-[#212529]`. PanorAIma pages use layered `radial-gradient` + `linear-gradient` backgrounds defined inline per page.

## Notes

- `/writings` redirects to `/PanorAIma` at the hosting level (backward compat — no redirect file in the repo).
- `images/site.webmanifest` lives under `images/`, not root — favicon `<link>` tags reference `/images/site.webmanifest`.
- CV PDF is at `files/bahman-reshadipour-CV.pdf`.
