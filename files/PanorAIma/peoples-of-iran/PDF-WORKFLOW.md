# Markdown to PDF workflow

This document records how we make PDFs from the Persian Markdown essay files in this folder, especially files like:

- `peoples-of-iran-fa-short.md`
- `peoples-of-iran-fa.md`

## Goal

Generate a clean RTL Persian PDF from a Markdown source file with:

- no browser date/title header on top of pages
- no file path/footer at the bottom of pages
- each `##` section starting on a new page
- a working table of contents/index linking to sections
- Persian-friendly fonts and right-to-left layout

## Tools used

The current workflow uses:

- Python 3
- Python `markdown` package
- Google Chrome headless PDF printing
- Persian-capable fonts installed on the system, for example:
  - `Vazir`
  - `Noto Naskh Arabic`
  - `Noto Sans Arabic`

Useful checks:

```bash
python3 -c "import markdown; print(markdown.__version__)"
command -v google-chrome
fc-list :lang=fa family file | head
```

## Process

### 1. Convert Markdown to HTML

The Markdown is converted to HTML first. During this step we need to:

1. enable Markdown extensions such as `extra`, `toc`, and `sane_lists`
2. preserve RTL layout with `lang="fa"` and `dir="rtl"`
3. add print CSS for A4 pages
4. add `break-before: page` / `page-break-before: always` to `h2`
5. ensure table-of-contents links match the generated section IDs

For Persian headings, automatic slug generation can be fragile. The safer approach is:

- read the links already written in the Markdown table of contents
- map each TOC title to a stable generated section ID, such as `section-01`, `section-02`, etc.
- rewrite the generated HTML links to use those stable IDs

This prevents broken index links in the PDF.

### 2. Important print CSS

The generated HTML should include CSS like this:

```css
@page {
  size: A4;
  margin: 18mm 16mm;
}

html,
body {
  direction: rtl;
}

body {
  font-family: Vazir, "Noto Naskh Arabic", "Noto Sans Arabic", Tahoma, Arial, sans-serif;
  font-size: 12.5pt;
  line-height: 1.9;
  text-align: right;
}

p {
  text-align: justify;
}

h2 {
  break-before: page;
  page-break-before: always;
}
```

`h2` is used as the section level, so this makes every section start on a new page.

### 3. Print HTML to PDF with Chrome

Use Chrome headless with `--no-pdf-header-footer`:

```bash
google-chrome \
  --headless=new \
  --no-sandbox \
  --disable-gpu \
  --no-pdf-header-footer \
  --print-to-pdf="$PWD/files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.pdf" \
  "file://$PWD/files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.html"
```

The important flag is:

```bash
--no-pdf-header-footer
```

Without this flag, Chrome adds:

- date/time at the top
- document title at the top
- local file path at the bottom

## Verification

After generating the PDF, check basic metadata and page count:

```bash
pdfinfo files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.pdf
```

Check that there is no file path or date printed in the PDF text:

```bash
pdftotext files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.pdf - | grep -E 'file://|/home/bahman|6/7/26' || true
```

Check that each page starts with the expected section heading:

```bash
pdftotext -layout files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.pdf - | \
python3 -c 'import sys; pages=sys.stdin.read().split("\f");
for i,p in enumerate(pages,1):
    lines=[l.strip() for l in p.splitlines() if l.strip()]
    if lines: print(i, lines[0])'
```

## Current short-file outputs

For the short version, the generated files are:

- HTML: `files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.html`
- PDF: `files/PanorAIma/peoples-of-iran/peoples-of-iran-fa-short.pdf`

The last known fixed version had:

- no Chrome header/footer
- working index links
- each `##` section starting on a new page
- 20 PDF pages

## Note

Do not regenerate PDFs unless explicitly requested. If the user only asks for documentation, update this workflow document without rebuilding the PDF files.
