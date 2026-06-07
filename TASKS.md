# TASKS

## P1 — Publish "The Peoples of Iran" (overdue: was June 4, 2026)

Article draft is at `files/PanorAIma/مردمان ایران.odt`.

Slug plan:
- EN: `PanorAIma/peoples-of-iran-en/index.html`
- FA: `PanorAIma/peoples-of-iran-fa/index.html`

- [x] Read the `.odt` draft and extract full article content — DONE (FA: 16 sections in `peoples-of-iran-fa.md`)
- [x] Generate section image cards (HTML → PNG approach) — DONE 2026-06-07
  - ~~`gen_images.py` (OpenAI API) deprecated 2026-06-07~~ — approach changed
  - Card design: bordered panel (gold border, dark semi-transparent bg) floating over full-bleed photo; photo shows in margins ← locked 2026-06-07
  - Background: `files/PanorAIma/peoples-of-iran/bg-d.png` (dark, preferred)
  - Output folder: `images/PanorAIma/peoples-of-iran/stories/` (created)
  - Output files: `images/PanorAIma/peoples-of-iran/stories/<section-slug>.jpg` (16 JPEG cards, q=98)
  - [x] Render `test-card-d.html` to PNG (Playwright at 941×1672) to validate card design
  - [x] Confirm `bg-d.png` vs `bg.png` choice from the rendered test card
  - [x] Install/verify Playwright + chromium
  - [x] Write `card-texts.md` — all 16 sections with label, title, body, ref, cta, music
  - [x] Write `gen_section_cards.py` — reads `card-texts.md`, JPEG q=98, skip logic, Vazirmatn, RTL
  - [x] Run script and review all 16 cards
  - [ ] Pick best card as feature image → `images/PanorAIma/peoples-of-iran.jpg`
- [ ] Generate square hero images (one per section, embedded in article body)
  - [ ] Decide square pixel size (e.g. 1200×1200)
  - [ ] Design `test-hero-d.html` — square layout, same card design minus CTA field; label + title + body + optional ref only
  - [ ] Render test hero to validate design before generating all 16
  - [ ] Write `gen_hero_images.py` — reads same `card-texts.md`, skips `cta` field, outputs square JPEG q=98 to `images/PanorAIma/peoples-of-iran/heroes/<section-slug>.jpg`
  - [ ] Run script and review all 16 hero images
  - [ ] Pick one hero image as article feature image → `images/PanorAIma/peoples-of-iran.jpg`
  - NOTE 2026-06-07: gen_hero_images.py + test-hero-d.html already created; all 16 heroes generated to `images/PanorAIma/peoples-of-iran/heroes/`. Cover image rendered at `images/PanorAIma/peoples-of-iran/cover.jpg` (from test-cover-d.html) — post card and FA OG tag already reference this path; `peoples-of-iran.jpg` flat path may be obsolete.
- [ ] Add feature image `images/PanorAIma/peoples-of-iran.jpg`
  - [ ] Copy chosen hero: `cp images/PanorAIma/peoples-of-iran/heroes/<slug>.jpg images/PanorAIma/peoples-of-iran.jpg`
  - [ ] If none ready, use `soon.jpg` as placeholder
- [x] Add post card to `PanorAIma/index.html` (`.post-card` pattern, with `.fa-preview` block) — DONE 2026-06-07
  - [x] Insert above teaser card
  - [x] Include `.meta-pill` date (June 6 2026 / ۱۶ خرداد ۱۴۰۵), `.lang-actions` EN/FA links
  - [x] Cover image full-width, height:auto (no max-height — square cover was cropped otherwise)
  - [x] Teaser "Coming Next" hidden via HTML comment (preserved for P2 re-use)
- [ ] Update `PanorAIma/next/index.html` to point to next upcoming article ← depends on [P2 topic]
- [x] Add both EN + FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod 2026-06-07` — DONE
  - [x] `next/` entry with `changefreq: weekly` preserved
- [x] Extract/translate EN article body to `peoples-of-iran-en.md` from the FA draft — DONE
  - [x] `peoples-of-iran-en.md` exists (380 lines, 16 sections, all [n] citations preserved)
  - No short EN version — decision 2026-06-07
- [x] Create `PanorAIma/peoples-of-iran-en/index.html` — DONE 2026-06-07
  - [x] Built from EN template; cover image at top (no per-section heroes)
  - [x] All meta/OG/Twitter/JSON-LD/canonical/hreflang fields updated
  - [x] Long EN content with ToC, superscript citations, references section; `AI-Assisted` chip
- [ ] Create `PanorAIma/peoples-of-iran-fa/index.html` from FA article template ← depends on FA draft
  - [ ] `mkdir -p PanorAIma/peoples-of-iran-fa && cp PanorAIma/iran-lahzeye-feshordeh-tarikh-fa/index.html PanorAIma/peoples-of-iran-fa/index.html`
  - [ ] Update all meta/OG/Twitter/JSON-LD/canonical/hreflang fields (slug: `peoples-of-iran-fa`, lang: `fa`, inLanguage: `fa-IR`)
  - [ ] Replace article body with FA content from `peoples-of-iran-fa.md`; add `تحلیل با هوش‌واره` chip
  - [ ] Embed section images (`<figure>` after each `<h2>`, alt = section title in FA)
  - NOTE 2026-06-07: FA page already exists at `PanorAIma/peoples-of-iran-fa/index.html` (610 lines, correct meta, 16 heroes embedded) — verify hreflang points to EN slug once EN page is created
  - [ ] Verify hreflang in FA page: confirm `href="https://25mordad.com/PanorAIma/peoples-of-iran-en"` and `x-default` are correct after EN page is live
- [x] Run `npm run build:css` — DONE 2026-06-07
- [ ] Commit and push

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
  - [ ] Brainstorm 3–5 candidate topics and pick one (note shortlist in WORKLOG)
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates
- [ ] Update teaser card in `PanorAIma/index.html`
- [ ] Update memory: `project_panoraima_next.md`
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Draft the reply prompt template and save it under `files/` (or a memory entry) for reuse
