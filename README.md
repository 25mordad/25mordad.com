# 25mordad.com

![Bahman](images/bahman.png)

Personal website of Bahman Reshadi / Bahman Reshadipour.
Built as a static site with HTML + Tailwind CSS.

## Live

- https://25mordad.com

## Tech Stack

- HTML5
- Tailwind CSS (`src/tailwind.css` -> `assets/tailwind.css`)
- Font Awesome
- Vanilla JavaScript

## Main Sections

- `/` home page
- `/projects` projects page
- `/PanorAIma` writing section (**PanorAIma | فراتر از قاب**)

## PanorAIma Structure

PanorAIma is bilingual and each post has two dedicated pages (EN + FA).

Current structure:

```text
PanorAIma/
  index.html
  next/                                     ← permanent "coming next" teaser slot
    index.html
  iran-compressed-historical-moment-en/
    index.html
  iran-lahzeye-feshordeh-tarikh-fa/
    index.html
```

Notes:

- `/writings` currently redirects to `/PanorAIma` for backward compatibility.
- Landing page (`PanorAIma/index.html`) contains all post cards — teaser card (dashed border) at the top, published articles below.
- `PanorAIma/next/` is a permanent slot — always updated to preview the upcoming article. When a new article is announced, update the title, dates, description, and feature image (`images/soon.jpg` or new image).

## Terminology

- In Persian copy, use `هوش‌واره` as the project’s preferred Persian word for AI / AI-assisted work.
- Keep the spelling with the zero-width non-joiner: `هوش‌واره`.
- For Persian PanorAIma tags/chips, use `تحلیل با هوش‌واره`.

## Adding a New Post (EN + FA)

Use this workflow for every new article:

1. Create two slug folders under `PanorAIma/`:
- `your-post-slug-en/index.html`
- `your-post-slug-fa/index.html`

2. Start from existing post templates:
- Copy `PanorAIma/iran-compressed-historical-moment-en/index.html`
- Copy `PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html`

3. Update content + metadata in both files:
- `<title>`
- `meta description`
- `meta keywords`
- OpenGraph + Twitter tags
- `canonical`
- `hreflang` alternates (EN <-> FA)
- JSON-LD (`BlogPosting`: headline, datePublished, dateModified, url, inLanguage)

4. Add/update callouts and tags inside article content:
- Keep AI tag visible (e.g. `AI-Assisted` / `تحلیل با هوش‌واره`)
- Keep icon-based callouts for editorial style consistency

5. Add the new post card/link to `PanorAIma/index.html`.

6. Update `sitemap.xml`:
- Add both EN/FA URLs
- Add `lastmod`
- Add `xhtml:link` alternates between EN and FA pages

7. Rebuild CSS:

```bash
npm run build:css
```

## Dev Commands

```bash
npm install
npm run watch:css
npm run build:css
```

## Python Automation Scripts (`scripts/`)

Used for Instagram API automation (publishing Stories/Feed posts) and the Lightroom→Instagram
photo pipeline, separate from the Node/Tailwind toolchain.

```bash
python3 -m venv scripts/.venv
scripts/.venv/bin/pip install -r scripts/requirements.txt
scripts/.venv/bin/python3 -m playwright install chromium   # one-time, for the Story-typography fallback
scripts/.venv/bin/python scripts/<script>.py
```

Also requires `ffmpeg`/`ffprobe` on `PATH` (system package, not in `requirements.txt`) for
`make_story_video.py`.

Requires a project-root `.env` (gitignored, not committed) with:
- `IG_ACCESS_TOKEN` — Instagram Graph API access token
- `LR_CLIENT_ID` / `LR_CLIENT_SECRET` / `LR_REFRESH_TOKEN` — Adobe Lightroom API (see CLAUDE.md's Personal Photo Series section)
- `OPENAI_API_KEY` — gpt-image-2 quality-enhance and Story typography generation
- `TELEGRAM_BRIDGE_DIR` — local path to a sibling private repo whose Telegram bot/chat this pipeline sends through (see CLAUDE.md — deliberately not documented further here, this repo is public)

This repo is public — never commit `.env` or print secret values.

## Contact

- Website: https://25mordad.com
- GitHub: https://github.com/25mordad
- LinkedIn: https://www.linkedin.com/in/25mordad
- Telegram: https://t.me/Xoaan

## License

MIT

"Open your source, open your mind."
