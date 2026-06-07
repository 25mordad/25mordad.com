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

## P2 — Teaser: announce next article after "Peoples of Iran"

- [ ] Decide next article topic
  - [ ] Brainstorm 3–5 candidate topics and pick one (note shortlist in WORKLOG)
- [ ] Update `PanorAIma/next/index.html` with new title, description, and dates ← depends on topic
- [ ] Update teaser card in `PanorAIma/index.html` ← depends on topic
- [ ] Update memory: `project_panoraima_next.md` to reflect peoples-of-iran published and next topic TBD
- [ ] Consider AI-assisted comment replies — draft a workflow or prompt template for replying to reader comments on published articles using AI
  - [ ] Draft the reply prompt template and save it under `files/` (or a memory entry) for reuse

## Done

- **Publish "The Peoples of Iran"** — All 18 checklist steps completed (FA + EN pages, covers, story cards, hero images, post card, sitemap, hreflang fix, build, commit/push) — 2026-06-07
