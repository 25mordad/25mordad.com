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
| `images/PanorAIma/` | Feature images for PanorAIma pages — named after the article slug (e.g. `iran-lahzeye-feshordeh-tarikh.jpg`) or `soon.jpg` for the teaser |
| `images/site.webmanifest` | PWA manifest (icon paths are `/images/…`) |

## PanorAIma (Writing Section)

Each article is **bilingual** — one EN page and one FA page, always published together.

Slug convention:
- English: `PanorAIma/your-post-slug-en/index.html`
- Farsi: `PanorAIma/your-post-slug-fa/index.html`

### Adding a New Article — Checklist

1. Copy the existing EN and FA article files as starting templates.
2. In **both** files update: `<title>`, `meta description`, `meta keywords`, all OG/Twitter tags, `<link rel="canonical">`, `hreflang` alternates (EN↔FA + `x-default`), and the JSON-LD `BlogPosting` block (`headline`, `datePublished`, `dateModified`, `url`, `inLanguage`).
3. Add an AI-tag chip to the article header (English: `AI-Assisted`, Farsi: `تحلیل با هوش مصنوعی`).
4. Add the new post card to `PanorAIma/index.html` (follow the `.post-card` pattern with `.meta-pill` date, `.lang-actions` links, and a `.fa-preview` block for the Farsi subtitle).
5. Add both EN and FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod`.
6. Run `npm run build:css`.

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
