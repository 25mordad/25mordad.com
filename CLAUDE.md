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
| `images/PanorAIma/<slug>/cover.jpg` | Cover / feature image for the article listing card — generated from `test-cover-d.html` |
| `images/PanorAIma/<slug>/heroes/<section-slug>.jpg` | Square hero images (1200×1200) — one per section, embedded in article body |
| `images/PanorAIma/<slug>/stories/<section-slug>.jpg` | Vertical Instagram story cards (941×1672) — one per section |
| `images/PanorAIma/soon.jpg` | Placeholder feature image used on the teaser page before the cover is ready |
| `images/site.webmanifest` | PWA manifest (icon paths are `/images/…`) |

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
4. Write short EN draft → `<slug>-en-short.md` mirroring the FA short (same sections + refs).

#### Phase 2 — Image assets

5. Place background images `bg-d.png` (dark, preferred) and `bg.png` (light) in `files/PanorAIma/<slug>/`.
6. Write `card-texts.md` — one `## <n> — <section-slug>` block per section (label, title, body, ref, cta, music). See **Instagram Story Card Deck** for field rules.
7. Copy `gen_section_cards.py` from the previous article, update `OUTPUT_DIR` slug → run → 16 story cards in `images/PanorAIma/<slug>/stories/`.
8. Copy `gen_hero_images.py` from the previous article, update `OUTPUT_DIR` slug → run → 16 hero images in `images/PanorAIma/<slug>/heroes/`. See **Hero Images**.
9. Create `test-cover-d.html` (copy from previous article, update title + subtitle + tagline) → render → save as `images/PanorAIma/<slug>/cover.jpg`. See **Cover / Feature Image**.

#### Phase 3 — HTML pages

10. `mkdir -p PanorAIma/<slug>-fa && cp PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html PanorAIma/<slug>-fa/index.html`
11. In the FA page update: `<title>`, meta description/keywords, all OG/Twitter tags, canonical, hreflang (FA↔EN + x-default), JSON-LD `BlogPosting` (`headline`, `datePublished`, `dateModified`, `url`, `inLanguage: "fa-IR"`). Replace article body with FA content. Add `تحلیل با هوش‌واره` chip.
12. Embed hero images: after each `<h2>` section heading add `<figure><img src="/images/PanorAIma/<slug>/heroes/<section-slug>.jpg" alt="<section title in FA>"></figure>`.
13. `mkdir -p PanorAIma/<slug>-en && cp PanorAIma/iran-compressed-historical-moment-en/index.html PanorAIma/<slug>-en/index.html`
14. In the EN page update all the same fields (inLanguage: `"en"`). Replace article body with EN content. Add `AI-Assisted` chip. Embed hero images with English alt text.

#### Phase 4 — Publish

15. Add post card to `PanorAIma/index.html` above the teaser card (`.post-card` pattern: `.meta-pill` date in both EN and FA calendar, `.lang-actions` EN/FA links, `.fa-preview` block for FA subtitle).
16. Add both EN and FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod`.
17. Update `PanorAIma/next/index.html` to point to the next upcoming article.
18. Run `npm run build:css`.
19. Commit and push.

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

Each article ships with a deck of **Instagram story cards** — one card per article section
— to promote the piece on Instagram (posted every couple of days). Source of truth is
`files/PanorAIma/<slug>/card-texts.md`; cards render via `gen_section_cards.py` (Playwright,
941×1672) over a single background photo (`bg-d.png`, dark preferred), output to
`images/PanorAIma/<slug>/stories/<section-slug>.jpg`.

Purpose: each card **delivers one section's core idea on its own** (a self-contained taste,
not a teaser, and **not** a request for comments). A short CTA then nudges the reader to the
full article; the actual link/sticker is added on the story afterwards, not baked into the image.

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

Each article has **one cover image** — used as the listing card thumbnail, OG image, and Twitter card. It shows only the article title, subtitle, a one-line tagline, and the author. No section label, no body paragraphs, no CTA.

**To create for a new article:**

1. Copy `test-cover-d.html` from the previous article into `files/PanorAIma/<new-slug>/`.
2. Update three things hardcoded in the HTML:
   - `<h1 class="article-title">` — the article's main title
   - `<p class="article-subtitle">` — the article's subtitle
   - `<p class="tagline">` — a single punchy line describing what the article is about (write fresh, not from card-texts.md)
3. Render and preview, then save final as `images/PanorAIma/<new-slug>/cover.jpg`.

**Layout (top to bottom inside the card):**
```
✦  (ornament, gold, faint)
article title  (large bold white, auto-scales)
article subtitle  (muted white, lighter weight)
──◆──  (gold divider)
tagline  (one line, muted white, 32px)
```
Footer sits outside the card, absolutely positioned at bottom:
```
بهمن رشادی  (gold, 26px, medium weight)
25Mordad.com  (gold, 30px, bold, LTR)
✦ فراتر از قاب ✦  (dim gold, 22px, light)
```

**Rules:**
- **Author:** always `بهمن رشادی` (two-part, not full surname, not first name only)
- **Tagline:** write fresh per article — one line, RTL Persian, captures the article's core question or tension
- **Background:** always `bg-d.png` (dark) — do not randomise the cover
- **Format:** 1200×1200 px JPEG `quality=98`
- **Output path:** `images/PanorAIma/<slug>/cover.jpg`

**Render snippet (inline, no script needed):**
```python
from pathlib import Path
from playwright.sync_api import sync_playwright

html_file = Path("files/PanorAIma/<slug>/test-cover-d.html").resolve()
out = Path("images/PanorAIma/<slug>/cover.jpg")

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
