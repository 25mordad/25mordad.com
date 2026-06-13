# TASKS

## P1 — Publish "The Peoples of Iran" (overdue: was June 4, 2026)

Article draft is at `files/PanorAIma/مردمان ایران.odt`.

Slug plan:
- EN: `PanorAIma/peoples-of-iran-en/index.html`
- FA: `PanorAIma/peoples-of-iran-fa/index.html`

- [x] Read the `.odt` draft and extract full article content — DONE (FA: 16 sections in `peoples-of-iran-fa.md`)
- [x] Generate section image cards (HTML → PNG approach) — DONE 2026-06-07
  - Card design: bordered panel (gold border, dark semi-transparent bg) floating over full-bleed photo; photo shows in margins ← locked 2026-06-07
  - Background: `files/PanorAIma/peoples-of-iran/bg-d.png` (dark, preferred)
  - Output: `images/PanorAIma/peoples-of-iran/stories/<section-slug>.jpg` (16 JPEG cards, q=98)
- [x] Generate square hero images — DONE 2026-06-07 (16 heroes in `images/PanorAIma/peoples-of-iran/heroes/`)
- [x] Render covers — DONE 2026-06-07
  - FA cover: `images/PanorAIma/peoples-of-iran/cover.jpg` (Vazirmatn, RTL)
  - EN cover: `images/PanorAIma/peoples-of-iran/cover-en.jpg` (Space Grotesk, LTR)
- [x] Add post card to `PanorAIma/index.html` — DONE 2026-06-07
- [x] Add both EN + FA URLs to `sitemap.xml` with `xhtml:link` alternates and `lastmod 2026-06-07` — DONE
- [x] Extract/translate EN article body to `peoples-of-iran-en.md` — DONE (16 sections, no short EN version)
- [x] Create `PanorAIma/peoples-of-iran-en/index.html` — DONE 2026-06-07
  - Cover image at top, ToC, superscript citations, refs section, PDF link, `AI-Assisted` chip
- [x] Create `PanorAIma/peoples-of-iran-fa/index.html` — DONE (610 lines, 16 heroes embedded, correct meta)
- [x] Verify hreflang in FA page — DONE 2026-06-07 (x-default now consistently → EN slug)
- [x] Run `npm run build:css` — DONE 2026-06-07
- [x] Commit and push — DONE 2026-06-07

## P1.5 — Fix peoples-of-iran Instagram card texts for outsider clarity

Card titles and some bodies were written from an insider perspective (as if the reader already knows the article concepts). Instagram viewers haven't read the article — a title like "سبک زندگی، سطحِ نیروهای پنهان است" is cryptic to a new reader (what forces? hidden how?). All 16 cards need an outsider-clarity review.

- [x] Review all 16 titles: flag any that rely on article-internal concepts without enough standalone context
- [x] Rewrite flagged titles so they carry the section's idea on their own — no jargon, no assumed knowledge
- [x] Review bodies for the same issue (titles are higher priority)
- [x] Update `files/PanorAIma/peoples-of-iran/card-texts.md` with revised copy
- [x] Delete the story card JPEGs that changed (so gen_section_cards.py re-renders them): `rm images/PanorAIma/peoples-of-iran/stories/<slug>.jpg`
- [x] Run `python3 files/PanorAIma/peoples-of-iran/gen_section_cards.py` to regenerate affected cards
- [x] Visually verify each re-rendered card before committing
- [ ] Commit and push (pending — modified story cards + card-texts.md staged)

## P1.6 — peoples-of-iran Instagram feed post cards

- [x] Build gen_post_cards.py (Playwright, 1080×1080) — `files/PanorAIma/peoples-of-iran/gen_post_cards.py`
- [x] Add general-caption block to card-texts.md (single caption for full carousel)
- [x] Render all 16 feed post images — `images/PanorAIma/peoples-of-iran/posts/01-*.jpg … 16-*.jpg`
- [x] Fix section 1 post_body (trimmed 4→2 paragraphs to match all other sections)
- [ ] Commit gen_post_cards.py, test-post-d.html, updated card-texts.md, and all 16 post images

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
  - [ ] Brainstorm 3–5 candidate topics aligned with PanorAIma's analytical lens (social/historical/cultural/economic Iran)
    - [ ] Candidate A: Iranian bazaar — economic structure, guild culture, political role
    - [ ] Candidate B: Iranian diaspora — identity, cultural negotiation, dual belonging
    - [ ] Candidate C: Persian language — spread, survival, political uses across history
    - [ ] Candidate D: Women in Iranian history — beyond the modern lens, pre-Islamic + Qajar + Constitutional era
    - [ ] Candidate E: Iranian calendar and time perception — Nowruz, seasonal rhythm, cosmological worldview
  - [ ] Cross-check shortlist against existing articles (`iran-lahzeye-feshordeh-tarikh`, `peoples-of-iran`) to avoid thematic overlap
  - [ ] Note chosen topic + rationale in WORKLOG
  - [ ] Derive slug plan (EN + FA slugs) and note in TASKS under new P1 block
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates ← depends on topic
  - [ ] Update `<title>`, meta description/keywords, og:title, og:description, twitter:title, twitter:description
  - [ ] Update JSON-LD headline, description, and estimated publish date
  - [ ] Update teaser body text (heading + preview paragraphs) in the article body
  - [ ] Swap og:image / twitter:image to `images/PanorAIma/soon.jpg` (or a new teaser image if available)
- [ ] Update teaser card in `PanorAIma/index.html` ← depends on topic
  - [ ] Restore the commented-out teaser `<section>` block
  - [ ] Update title, description, and `.lang-actions` links in the teaser card
- [ ] Commit and push P2 teaser updates ← depends on above three
- [ ] Update memory: `project_panoraima_next.md` to reflect peoples-of-iran published and new topic chosen
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Clarify the comment surface (Instagram DMs, website, or both)
  - [ ] Draft the reply prompt template (referencing article content + reader message) and save to `files/ai-reply-template.md`
  - [ ] Test the template against a sample comment from peoples-of-iran article

## Done

- **Publish "The Peoples of Iran"** — All 18 checklist steps completed (FA + EN pages, covers, story cards, hero images, post card, sitemap, hreflang fix, build, commit/push) — 2026-06-07
