# TASKS

## P1 — Publish "The Peoples of Iran" (overdue: was June 4, 2026)

Article draft is at `files/PanorAIma/مردمان ایران.odt`.

Slug plan:
- EN: `PanorAIma/peoples-of-iran-en/index.html`
- FA: `PanorAIma/peoples-of-iran-fa/index.html`

- [ ] Read the `.odt` draft and extract full article content (EN + FA)
  - [ ] Convert with: `libreoffice --headless --convert-to txt "files/PanorAIma/مردمان ایران.odt" --outdir /tmp/`
  - [ ] Identify EN sections and FA sections in the extracted text
- [ ] Create `PanorAIma/peoples-of-iran-en/index.html` from EN article template
  - [ ] Copy from `PanorAIma/iran-compressed-historical-moment-en/index.html`
  - [ ] Update `<title>`, `<meta description>`, `<meta keywords>`, all OG/Twitter tags
  - [ ] Update `<link rel="canonical">` and `hreflang` alternates (EN↔FA + `x-default`)
  - [ ] Update JSON-LD `BlogPosting` block (headline, datePublished, dateModified, url, inLanguage)
  - [ ] Replace article body with EN content from draft
  - [ ] Add `AI-Assisted` tag chip in article header
- [ ] Create `PanorAIma/peoples-of-iran-fa/index.html` from FA article template
  - [ ] Copy from `PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html`
  - [ ] Update all meta/OG/Twitter/JSON-LD/canonical/hreflang fields (mirror EN steps)
  - [ ] Replace article body with FA content from draft
  - [ ] Add `تحلیل با هوش مصنوعی` tag chip in article header
- [ ] Generate section images via OpenAI API
  - Script: `files/PanorAIma/peoples-of-iran/gen_images.py`
  - Model: `gpt-image-2` · Size: `1536x1024` · Quality: `high` · Format: PNG
  - Output: `images/PanorAIma/peoples-of-iran-<en-slug>.png` (14 files)
  - Reads `OPENAI_API_KEY` from env
  - [ ] Write `gen_images.py` with hardcoded 14-row section table `(fa_heading, en_slug, en_prompt)`
    - [ ] Each prompt = thematic EN description + shared style suffix:
          *"Painterly editorial illustration, muted earth tones with hints of deep blue and ochre, no text, suitable for a long-form article about Iranian society."*
    - [ ] Section slugs and prompt themes:
          1. `everyone-their-own-people` — fragmented crowd, each group pointing to themselves as "the people"
          2. `disagreement-to-social-worlds` — two parallel worlds side by side in the same city
          3. `ethnicity-memory-layer` — layered historical memory: photos, maps, traditional patterns
          4. `lifestyle-visible-surface` — cafes, bazaars, gyms, smartphones under one sky
          5. `lifestyle-as-engine-of-change` — one changed habit rippling through a neighborhood
          6. `university-social-media-contact` — campus + social feeds, cross-cultural collision
          7. `media-collapse-single-narrative` — shattered TV screen, competing narratives scattered
          8. `evolutionary-ingroup-bias` — abstract evolutionary tree branching into tribal clusters
          9. `from-differences-to-knots` — knotted threads of different colors, tension and connection
          10. `shared-suffering` — diverse people in a queue, same tired faces
          11. `from-pain-to-connection` — hands from different backgrounds passing something across a divide
          12. `economy-practical-cooperation` — marketplace transaction between visibly different people
          13. `family-kinship-forced-contact` — multi-generational family, traditional and modern dress
          14. `intertwined-lives` — aerial city at night, different districts all connected
    - [ ] Detect repo root as `Path(__file__).resolve().parents[3]`
    - [ ] Check `OPENAI_API_KEY` at startup; exit with message if missing
    - [ ] Wrap each API call in try/except — print error and continue on failure
    - [ ] Print per-image progress + final summary table
  - [ ] Run `gen_images.py` (`OPENAI_API_KEY=sk-... python files/PanorAIma/peoples-of-iran/gen_images.py`)
  - [ ] Review generated images and pick which ones to use (manual step)
- [ ] Add feature image: pick best generated image as `images/PanorAIma/peoples-of-iran.jpg`
  - [ ] If no generated image is ready, use `soon.jpg` as placeholder and note in commit
- [ ] Embed accepted section images in FA (and EN) HTML pages
  - [ ] Use `<figure>` + `<figcaption>` inside `.article` body, after each `<h2>`
  - [ ] Add `alt` text (English) and `title` (Farsi) attributes for SEO/accessibility
- [ ] Add post card to `PanorAIma/index.html` (`.post-card` pattern, with `.fa-preview` block)
  - [ ] Insert above teaser card, not below it
  - [ ] Include `.meta-pill` date (June 6 2026 / ۱۶ خرداد ۱۴۰۵), `.lang-actions` EN/FA links
- [ ] Update `PanorAIma/next/index.html` to point to next upcoming article (clear current teaser)
  - [ ] Depends on P2 topic decision ← depends on [P2 topic]
- [ ] Add both EN + FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod`
  - [ ] Set `lastmod` to today: `2026-06-06`
  - [ ] Keep `next/` entry with `changefreq: weekly`
- [ ] Run `npm run build:css`
- [ ] Commit and push

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates
- [ ] Update teaser card in `PanorAIma/index.html`
- [ ] Update memory: `project_panoraima_next.md`
