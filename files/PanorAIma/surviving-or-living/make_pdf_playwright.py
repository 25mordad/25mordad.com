#!/usr/bin/env python3
"""Convert a markdown draft to a print-ready PDF via Playwright's Chromium.

google-chrome is not installed on this machine (see project memory
project_pdf_generation_no_chrome.md), so make_pdf.py's --print-to-pdf path
doesn't work here. This uses Playwright's bundled chromium + page.pdf()
instead, same visual result.

Usage: python3 make_pdf_playwright.py <file.md> [--lang fa|en]
"""
import sys
from pathlib import Path

import markdown
from playwright.sync_api import sync_playwright

HERE = Path(__file__).parent

CSS_FA = """
@page { size: A4; margin: 18mm 16mm; }
@font-face {
  font-family: 'Vazirmatn';
  src: local('Vazirmatn');
}
html, body { direction: rtl; }
body {
  font-family: 'Vazirmatn', Tahoma, Arial, sans-serif;
  font-size: 12.5pt; line-height: 1.9; text-align: right;
}
p { text-align: justify; }
blockquote {
  border-right: 3px solid #ccc; border-left: none;
  padding-right: 1em; padding-left: 0; margin-right: 0;
  color: #444; font-style: italic;
}
h1 { font-size: 20pt; margin-top: 0; }
h1:not(:first-of-type), h2 { break-before: page; }
h2 { font-size: 16pt; }
a { color: inherit; text-decoration: none; }
"""

CSS_EN = """
@page { size: A4; margin: 18mm 16mm; }
html, body { direction: ltr; }
body {
  font-family: 'Source Serif 4', Georgia, serif;
  font-size: 12pt; line-height: 1.75; text-align: left;
}
p { text-align: justify; }
blockquote {
  border-left: 3px solid #ccc; padding-left: 1em;
  margin-left: 0; color: #444; font-style: italic;
}
h1 { font-size: 20pt; margin-top: 0; }
h1:not(:first-of-type), h2 { break-before: page; }
h2 { font-size: 16pt; }
a { color: inherit; text-decoration: none; }
sup { font-size: 0.7em; }
"""

HTML_TEMPLATE = """<!doctype html>
<html lang="{lang}" dir="{dir}">
<head>
<meta charset="utf-8">
<link rel="preconnect" href="https://fonts.googleapis.com">
<link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
<link href="https://fonts.googleapis.com/css2?family=Vazirmatn:wght@400;500;700;900&family=Source+Serif+4:opsz,wght@8..60,400;8..60,700&display=swap" rel="stylesheet">
<title>{title}</title>
<style>{css}</style>
</head>
<body>
{body}
</body>
</html>
"""


def convert(md_path: Path, lang: str):
    text = md_path.read_text(encoding="utf-8")
    body_html = markdown.markdown(text, extensions=["extra", "sane_lists"])
    title = md_path.stem
    css = CSS_FA if lang == "fa" else CSS_EN
    direction = "rtl" if lang == "fa" else "ltr"
    html = HTML_TEMPLATE.format(title=title, css=css, body=body_html, lang=lang, dir=direction)

    html_path = md_path.with_suffix(".html")
    html_path.write_text(html, encoding="utf-8")

    pdf_path = md_path.with_suffix(".pdf")
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()
        page.goto(f"file://{html_path}", wait_until="networkidle", timeout=60_000)
        page.wait_for_function("document.fonts.ready")
        page.pdf(path=str(pdf_path), format="A4", margin={"top": "18mm", "bottom": "18mm", "left": "16mm", "right": "16mm"}, print_background=True)
        browser.close()
    html_path.unlink()
    print(f"wrote {pdf_path}")


if __name__ == "__main__":
    args = sys.argv[1:]
    lang = "fa"
    if "--lang" in args:
        i = args.index("--lang")
        lang = args[i + 1]
        del args[i:i + 2]
    for t in args:
        convert(HERE / t, lang)
