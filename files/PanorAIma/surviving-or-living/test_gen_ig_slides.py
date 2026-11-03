"""Checks for gen_ig_slides.py that never draw, render or call any service.

Run:  python3 -m unittest files/PanorAIma/surviving-or-living/test_gen_ig_slides.py

External modules (requests, dotenv, playwright, image_common) are stubbed, and the
stubs fail loudly if anything tries to call an image service or open a browser.

The approved Persian section text is gitignored. To check that section 7's slides
use the section's own sentences, point SURVIVING_SECTIONS_DIR at the live copy's
`sections/` folder; without it those checks are skipped.
"""
import importlib.util
import os
import base64
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
CALLS = []


def _forbidden(name):
    def call(*args, **kwargs):
        CALLS.append(name)
        raise AssertionError(f"{name} must not be called")
    return call


def _load_generator():
    requests = types.ModuleType("requests")
    requests.post = _forbidden("requests.post")
    requests.RequestException = type("RequestException", (Exception,), {})
    dotenv = types.ModuleType("dotenv")
    dotenv.load_dotenv = lambda *a, **k: None
    playwright = types.ModuleType("playwright")
    sync_api = types.ModuleType("playwright.sync_api")
    sync_api.sync_playwright = _forbidden("sync_playwright")
    image_common = types.ModuleType("image_common")
    image_common.optimize_jpeg = _forbidden("optimize_jpeg")
    sys.modules.update({
        "requests": requests, "dotenv": dotenv, "playwright": playwright,
        "playwright.sync_api": sync_api, "image_common": image_common,
    })
    spec = importlib.util.spec_from_file_location("gen_ig_slides", HERE / "gen_ig_slides.py")
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    mod.API_KEY = None
    return mod


GEN = _load_generator()
SEC7 = GEN.SLIDES_BY_SECTION.get("07", [])


def _clauses(text):
    return [c.strip() for c in re.split(r"[.؟?!؛،:]", text) if c.strip()]


def _normalize_source(text):
    text = re.sub(r"\s*\([A-Za-z][^)]*\)", "", text)   # (Amartya Sen)
    text = re.sub(r"\s*\[[۰-۹0-9]+\]", "", text)        # [۲۴]
    text = text.replace("*", "")
    return re.sub(r"\s+", " ", text)


class Section7Deck(unittest.TestCase):
    def test_cover(self):
        cover = SEC7[0]
        self.assertEqual(cover["tag"], "بخش هفتم")
        self.assertEqual(cover["title"], "مرز باریک")
        self.assertIn("از تحمل تا امکان تغییر", cover["subtitle"])
        self.assertIn("از نوشتار «زنده‌ماندن یا زیستن؟»", cover["subtitle"])
        self.assertEqual(cover["author"], "بهمن رشادی")
        self.assertEqual(cover["body"], "")

    def test_dedication_matches_earlier_sections(self):
        self.assertEqual(SEC7[1]["slug"], "taghdim")
        self.assertEqual(SEC7[1]["body"], GEN.SLIDES_BY_SECTION["06"][1]["body"])

    def test_body_slides_have_short_title_and_prose(self):
        for slide in SEC7[2:-1]:
            self.assertTrue(slide.get("title"), slide["slug"])
            self.assertLessEqual(len(slide["title"].split()), 6, slide["slug"])
            self.assertTrue(slide.get("body"), slide["slug"])

    def test_closing_slide_points_to_next_section(self):
        end = SEC7[-1]
        self.assertEqual(end["slug"], "payan")
        self.assertEqual(end["title"], "ادامه دارد…")
        self.assertEqual(end["subtitle"], "بخش بعد: آنچه ماند، آنچه خرج شد")
        self.assertIn("این بخش هفتم از نوشتار «زنده‌ماندن یا زیستن؟» بود.", end["body"])

    def test_every_slide_has_an_illustration_and_unique_slug(self):
        self.assertGreaterEqual(len(SEC7), 15)
        slugs = [s["slug"] for s in SEC7]
        self.assertEqual(len(slugs), len(set(slugs)))
        for s in SEC7:
            self.assertTrue(s.get("illustration"), s["slug"])
            self.assertNotRegex(s["illustration"], r"[؀-ۿ]", s["slug"])

    def test_penultimate_returns_to_cover_from_farther_away(self):
        brief = SEC7[-2]["illustration"].lower()
        self.assertIn("cover", brief)
        self.assertIn("farther", brief)

    def test_caption(self):
        lines = (HERE / "section-07-caption.txt").read_text(encoding="utf-8").strip().splitlines()
        text = "\n".join(lines)
        self.assertIn("«فراتر از قاب»", text)
        self.assertIn("لینک در بایو", text)
        self.assertTrue(lines[-1].startswith("#هوش‌واره"))
        self.assertTrue(all(w.startswith("#") for w in lines[-1].split()))


@unittest.skipUnless(os.environ.get("SURVIVING_SECTIONS_DIR"), "approved section text not available")
class Section7UsesOwnSentences(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        src = Path(os.environ["SURVIVING_SECTIONS_DIR"]) / "08-marz-barik-az-tahammol-ta-emkan-taghyir.md"
        raw = src.read_text(encoding="utf-8")
        cls.paragraphs = [_normalize_source(p) for p in raw.split("\n\n")[1:] if p.strip()]
        cls.source = " ".join(cls.paragraphs)

    FRAMING = ("این بخش هفتم از نوشتار «زنده‌ماندن یا زیستن؟» بود.",
               "بخش بعد: آنچه ماند، آنچه خرج شد.")

    def _own_prose(self, slide):
        body = slide["body"]
        for line in self.FRAMING:
            body = body.replace(line, "")
        return body

    def test_body_clauses_are_verbatim(self):
        for slide in SEC7[2:]:
            for clause in _clauses(self._own_prose(slide)):
                self.assertTrue(clause in self.source, f"{slide['slug']}: {clause}")

    def test_slides_cover_every_paragraph(self):
        used = " ".join(self._own_prose(s) for s in SEC7[2:])
        for p in self.paragraphs:
            self.assertTrue(any(c in used for c in _clauses(p)), p[:60])


class EarlierSectionsDrawNothing(unittest.TestCase):
    def test_sections_1_to_6_render_nothing_new(self):
        CALLS.clear()
        argv = sys.argv
        try:
            for section in ["01", "02", "03", "04", "05", "06"]:
                sys.argv = ["gen_ig_slides.py", "", section]
                GEN.main()
        finally:
            sys.argv = argv
        self.assertEqual(CALLS, [])


class _Resp:
    def __init__(self, status, payload=None, text=""):
        self.status_code = status
        self.ok = 200 <= status < 300
        self._payload = payload
        self.text = text

    def json(self):
        return self._payload


PNG = b"\x89PNG fake"
OK = _Resp(200, {"data": [{"b64_json": base64.b64encode(PNG).decode()}]})


class DrawIllustration(unittest.TestCase):
    """Drives draw_illustration with a fake image service; nothing real is called."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.png = Path(self.tmp.name) / "01-x.png"
        self.requests = []
        self.saved = (GEN.API_KEY, GEN.requests.post, GEN.REPO_ROOT)
        GEN.API_KEY = "test-key"
        GEN.REPO_ROOT = Path(self.tmp.name)

    def tearDown(self):
        GEN.API_KEY, GEN.requests.post, GEN.REPO_ROOT = self.saved
        self.tmp.cleanup()

    def _service(self, *replies):
        replies = list(replies)

        def post(url, **kwargs):
            self.requests.append(kwargs["json"])
            reply = replies.pop(0)
            if isinstance(reply, Exception):
                raise reply
            return reply
        GEN.requests.post = post

    def test_new_illustration_is_requested_at_medium_quality(self):
        self._service(OK)
        GEN.draw_illustration(self.png, "a ridge")
        self.assertEqual(len(self.requests), 1)
        self.assertEqual(self.requests[0]["model"], "gpt-image-2")
        self.assertEqual(self.requests[0]["quality"], "medium")
        self.assertEqual(self.png.read_bytes(), PNG)

    def test_failed_call_is_retried_once(self):
        self._service(_Resp(500, text="server error"), OK)
        GEN.draw_illustration(self.png, "a ridge")
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(self.png.read_bytes(), PNG)

    def test_network_error_is_retried_once(self):
        self._service(GEN.requests.RequestException("timed out"), OK)
        GEN.draw_illustration(self.png, "a ridge")
        self.assertEqual(len(self.requests), 2)
        self.assertEqual(self.png.read_bytes(), PNG)

    def test_second_failure_stops_with_clear_message(self):
        self._service(_Resp(500, text="first"), _Resp(429, text="rate limited"), OK)
        with self.assertRaises(SystemExit) as stop:
            GEN.draw_illustration(self.png, "a ridge")
        self.assertEqual(len(self.requests), 2)
        message = str(stop.exception.code)
        self.assertIn("01-x.png", message)
        self.assertIn("429", message)
        self.assertIn("rate limited", message)
        self.assertFalse(self.png.exists())

    def test_cached_illustration_is_never_requested(self):
        self.png.write_bytes(b"old")
        self._service()
        GEN.draw_illustration(self.png, "a ridge")
        self.assertEqual(self.requests, [])
        self.assertEqual(self.png.read_bytes(), b"old")


if __name__ == "__main__":
    unittest.main()
