# Tasks Archive

### Done 2026-08-09

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
- [x] Commit and push — DONE 2026-06-13 (fae56cd: 4 titles rewritten, 3 story card JPEGs regenerated)
