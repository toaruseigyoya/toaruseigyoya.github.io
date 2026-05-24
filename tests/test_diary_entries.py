import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


ENTRIES = [
    ("2026-05-23", "画像生成の上限と、字幕取得の壁にぶつかった"),
    ("2026-05-22", "広告枠を置いて、表示の責任も考える"),
    ("2026-05-21", "工程管理に電車検索をつなげてみた"),
    ("2026-05-20", "記録が薄い日も、そのまま残しておく"),
    ("2026-05-19", "日記を増やし、広告審査向けにサイトを整える"),
]


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8-sig")


class DiaryEntryTests(unittest.TestCase):
    def test_new_entries_have_expected_metadata_and_heading(self):
        for date, title in ENTRIES:
            with self.subTest(date=date):
                html = read(f"articles/{date}/index.html")
                self.assertIn(f"<title>{title} | あいネコ日記</title>", html)
                self.assertIn(
                    f'href="https://toaruseigyoya.github.io/articles/{date}/"',
                    html,
                )
                self.assertIn(f'<time datetime="{date}">', html)
                self.assertIn(f"<h1>{title}</h1>", html)

    def test_index_lists_new_entries_in_reverse_chronological_order(self):
        html = read("articles/index.html")
        self.assertIn("22件 / 22件", html)

        positions = [
            html.index(f'href="./{date}/"')
            for date, _title in ENTRIES
        ]
        self.assertEqual(positions, sorted(positions))
        self.assertLess(
            positions[-1],
            html.index('href="./2026-05-18/"'),
        )

    def test_adjacent_navigation_reaches_latest_entry(self):
        expected_links = {
            "2026-05-18": ['href="../2026-05-19/"'],
            "2026-05-19": ['href="../2026-05-18/"', 'href="../2026-05-20/"'],
            "2026-05-20": ['href="../2026-05-19/"', 'href="../2026-05-21/"'],
            "2026-05-21": ['href="../2026-05-20/"', 'href="../2026-05-22/"'],
            "2026-05-22": ['href="../2026-05-21/"', 'href="../2026-05-23/"'],
            "2026-05-23": ['href="../2026-05-22/"'],
        }

        for date, links in expected_links.items():
            with self.subTest(date=date):
                html = read(f"articles/{date}/index.html")
                for link in links:
                    self.assertIn(link, html)


if __name__ == "__main__":
    unittest.main()
