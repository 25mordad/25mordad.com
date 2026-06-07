# TASKS

## P1 — Publish "The Peoples of Iran" (overdue: was June 4, 2026)

Article draft is at `files/PanorAIma/مردمان ایران.odt`.

Slug plan:
- EN: `PanorAIma/peoples-of-iran-en/index.html`
- FA: `PanorAIma/peoples-of-iran-fa/index.html`

- [x] Read the `.odt` draft and extract full article content — DONE (FA: 16 sections in `peoples-of-iran-fa.md`)
- [ ] Generate section image cards (HTML → PNG approach)
  - ~~`gen_images.py` (OpenAI API) deprecated 2026-06-07~~ — approach changed
  - Card design: bordered panel (gold border, dark semi-transparent bg) floating over full-bleed photo; photo shows in margins ← locked 2026-06-07
  - Background: `files/PanorAIma/peoples-of-iran/bg-d.png` (dark, preferred)
  - Output folder: `images/PanorAIma/peoples-of-iran/` (created)
  - Output files: `images/PanorAIma/peoples-of-iran/<en-slug>.png` (16 files)
  - [ ] Render `test-card-d.html` to PNG (Playwright at 941×1672) to validate card design before scaling up ← do first
  - [ ] Confirm `bg-d.png` vs `bg.png` choice from the rendered test card
  - [ ] Install/verify Playwright + chromium (`pip install playwright && playwright install chromium`) ← blocks gen_section_cards.py
  - [ ] Write `card-texts.md` — one entry per section with: FA section label, FA title, 2–3 line FA summary, CTA text; covers both bg variants
    - [ ] After section-1 card is approved, write `card-texts.md` sections 2–16 (mirror the section-1 block format; only section 1 exists now)
  - [ ] Write `gen_section_cards.py` — reads `card-texts.md`, builds one HTML per section, screenshots via Playwright at 941×1672
    - [ ] Vazirmatn via Google Fonts, RTL, already-generated files skipped
    - [ ] Reuse the `.card`/`.section-*`/`.footer` CSS from `test-card-d.html` as the template
  - [ ] Run script and review all 16 cards
  - [ ] Pick best card as feature image → `images/PanorAIma/peoples-of-iran.jpg`
- [ ] Add feature image `images/PanorAIma/peoples-of-iran.jpg`
  - [ ] Convert chosen PNG to JPG: `convert "images/PanorAIma/peoples-of-iran/<slug>.png" images/PanorAIma/peoples-of-iran.jpg`
  - [ ] If none ready, use `soon.jpg` as placeholder
- [ ] Add post card to `PanorAIma/index.html` (`.post-card` pattern, with `.fa-preview` block)
  - [ ] Insert above teaser card
  - [ ] Include `.meta-pill` date (June 6 2026 / ۱۶ خرداد ۱۴۰۵), `.lang-actions` EN/FA links
- [ ] Update `PanorAIma/next/index.html` to point to next upcoming article ← depends on [P2 topic]
- [ ] Add both EN + FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod 2026-06-07`
  - [ ] Keep `next/` entry with `changefreq: weekly`
- [ ] Extract/translate EN article body to `peoples-of-iran-en.md` from the FA draft ← blocks EN page
  - [ ] Produce EN short version `peoples-of-iran-en-short.md` mirroring the FA short (same sections + refs)
- [ ] Create `PanorAIma/peoples-of-iran-en/index.html` from EN article template ← last
  - [ ] Copy from `PanorAIma/iran-compressed-historical-moment-en/index.html`
  - [ ] Update all meta/OG/Twitter/JSON-LD/canonical/hreflang fields
  - [ ] Replace article body with EN content; add `AI-Assisted` chip
  - [ ] Embed section images (`<figure>` after each `<h2>`, with alt + title attrs)
- [ ] Create `PanorAIma/peoples-of-iran-fa/index.html` from FA article template ← last
  - [ ] Copy from `PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html`
  - [ ] Update all meta/OG/Twitter/JSON-LD/canonical/hreflang fields
  - [ ] Replace article body with FA content; add `تحلیل با هوش مصنوعی` chip
  - [ ] Embed section images (`<figure>` after each `<h2>`, with alt + title attrs)
- [ ] Run `npm run build:css`
- [ ] Commit and push

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
  - [ ] Brainstorm 3–5 candidate topics and pick one (note shortlist in WORKLOG)
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates
- [ ] Update teaser card in `PanorAIma/index.html`
- [ ] Update memory: `project_panoraima_next.md`
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Draft the reply prompt template and save it under `files/` (or a memory entry) for reuse
