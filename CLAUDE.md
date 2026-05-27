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
