import re
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


TARGET_PAGES = [
    "index.html",
    "about/index.html",
    "note/index.html",
    "instagram/index.html",
    "tools/index.html",
]

EXCLUDED_PAGES = [
    "contact/index.html",
    "privacy/index.html",
    "disclaimer/index.html",
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


class A8AdPlacementTests(unittest.TestCase):
    def test_ad_asset_preserves_generated_ai_a8_code(self):
        ad_html = read("assets/a8/generated-ai.html")

        self.assertIn("px.a8.net/svt/ejp?a8mat=4B3VRB+1SBLE+50+7RXDHT", ad_html)
        self.assertEqual(len(re.findall(r'a8mat=', ad_html)), 2)

    def test_target_pages_have_ad_slot_and_loader(self):
        for page in TARGET_PAGES:
            with self.subTest(page=page):
                html = read(page)
                self.assertIn('class="affiliate-ad"', html)
                self.assertIn('data-a8-ad="generated-ai"', html)
                self.assertIn("アフィリエイト広告", html)
                self.assertIn("/assets/a8-ads.js", html)

    def test_excluded_pages_have_no_ad_slot_or_loader(self):
        for page in EXCLUDED_PAGES:
            with self.subTest(page=page):
                html = read(page)
                self.assertNotIn('class="affiliate-ad"', html)
                self.assertNotIn("/assets/a8-ads.js", html)

    def test_loader_uses_fetch_and_does_not_rewrite_ad_markup(self):
        loader = read("assets/a8-ads.js")

        self.assertIn("fetch('/assets/a8/' + adName + '.html'", loader)
        self.assertIn("body.innerHTML = html", loader)
        self.assertNotIn("replace(", loader)


if __name__ == "__main__":
    unittest.main()
