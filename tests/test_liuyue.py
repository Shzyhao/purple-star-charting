# -*- coding: utf-8 -*-
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star.chart import chart
from purple_star import liuyue


class TestLiuyue(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)  # 1990-05-15 14:30 男，命宫戌

    def test_doujun(self):
        # 2026 丙午，生月 4、生时 未 -> 斗君在戌
        self.assertEqual(liuyue.doujun(self.ch), "戌")

    def test_month_gz(self):
        self.assertEqual(liuyue.month_gz("丙", 1), "庚寅")
        self.assertEqual(liuyue.month_gz("丙", 12), "辛丑")

    def test_table(self):
        t = liuyue.liuyue_table(self.ch, 2026)
        self.assertEqual(t["year_gz"], "丙午")
        self.assertEqual(len(t["rows"]), 12)
        self.assertEqual(t["rows"][0]["zhi"], "戌")   # 正月在斗君
        self.assertEqual(t["rows"][0]["palace"], "命宮")

    def test_liuri(self):
        d = liuyue.liuri(self.ch, 2026, 10, 28)  # 农历十月廿八 -> 流日命宫 戌
        self.assertEqual(d["day_zhi"], "戌")
        self.assertEqual(d["day_palace"], "命宮")

    def test_md(self):
        md = liuyue.liuyue_md(self.ch, 2026)
        self.assertIn("流月", md)
        self.assertIn("可靠性", md)
        self.assertNotIn("「", md)


if __name__ == "__main__":
    unittest.main()
