# -*- coding: utf-8 -*-
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star.chart import chart
from purple_star.hepan import analyze_hepan


class TestHepan(unittest.TestCase):
    def setUp(self):
        self.a = chart("男", "庚午", 4, 21, 7)
        self.b = chart("女", "戊辰", 1, 15, 5)

    def test_sections(self):
        md = analyze_hepan(self.a, self.b, "A", "B", 2026, year_a=1990, year_b=1988)
        for key in ("双方基本盘", "命宫对命宫", "夫妻宫互看", "四化互落", "大限节奏", "年龄差与角色", "相处建议"):
            self.assertIn(key, md)

    def test_age_diff(self):
        md = analyze_hepan(self.a, self.b, "A", "B", 2026, year_a=1990, year_b=1988)
        self.assertIn("相差 2 岁", md)

    def test_no_quoted_text(self):
        md = analyze_hepan(self.a, self.b, "A", "B", 2026, year_a=1990, year_b=1988)
        self.assertNotIn("「", md)
        self.assertIn("不构成", md)

    def test_empty_palace_tolerated(self):
        # 构造一个可能空宫的盘，确保不抛异常
        c = chart("女", "辛未", 12, 13, 9)
        md = analyze_hepan(self.a, c, "A", "C", 2026)
        self.assertIn("合盘分析", md)


if __name__ == "__main__":
    unittest.main()
