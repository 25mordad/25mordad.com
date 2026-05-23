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
  iran-compressed-historical-moment-en/
    index.html
  iran-lahzeye-feshordeh-tarikh-fa/
    index.html
```

Notes:

- `/writings` currently redirects to `/PanorAIma` for backward compatibility.
- Landing page (`PanorAIma/index.html`) contains the featured post card and links to both language versions.

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
- Keep AI tag visible (e.g. `AI-Assisted` / `تحلیل با هوش مصنوعی`)
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

## Contact

- Website: https://25mordad.com
- GitHub: https://github.com/25mordad
- LinkedIn: https://www.linkedin.com/in/25mordad
- Telegram: https://t.me/Xoaan

## License

MIT

"Open your source, open your mind."
