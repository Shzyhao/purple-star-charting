# -*- coding: utf-8 -*-
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star.chart import chart, liunian, gz_of_year, doujun
from purple_star import interpret, render


class TestChart(unittest.TestCase):
    def setUp(self):
        # 1990-05-15 14:30 男 -> 农历庚午年四月廿一未时
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_basic(self):
        self.assertEqual(self.ch["ming_zhi"], "戌")
        self.assertEqual(self.ch["shen_zhi"], "子")
        self.assertEqual(self.ch["ju"], "土五局")
        self.assertEqual(self.ch["ziwei"], "戌")

    def test_stars(self):
        ming = self.ch["palaces"]["命宮"]["stars"]
        self.assertIn("紫微", ming)
        self.assertIn("天相", ming)
        cai = self.ch["palaces"]["財帛"]["stars"]
        self.assertIn("武曲", cai)

    def test_hua(self):
        # 庚干：太阳禄、武曲权、天同科、天相忌
        self.assertEqual(self.ch["hua"].get("天相"), "忌")
        self.assertEqual(self.ch["hua"].get("武曲"), "權")

    def test_daxian(self):
        orders = sorted(d["from"] for d in self.ch["daxian"].values())
        self.assertEqual(orders[0], 5)  # 土五局 5 岁起限
        self.assertEqual(len(orders), 12)

    def test_liunian_2026(self):
        ln = liunian(self.ch, "丙午", 37)
        self.assertEqual(ln["ming"], "午")
        self.assertEqual(ln["hua"]["祿"], "天同")

    def test_leap_month(self):
        a = chart("女", "辛未", 12, 13, 9)
        b = chart("女", "辛未", 12, 13, 9, leap_month=True)
        self.assertNotEqual(a["ming_zhi"], b["ming_zhi"])

    def test_doujun(self):
        self.assertEqual(doujun("午", 8, 10), "酉")

    def test_gz(self):
        self.assertEqual(gz_of_year(2026), "丙午")


class TestRender(unittest.TestCase):
    def test_svg(self):
        ch = chart("男", "庚午", 4, 21, 7)
        out = os.path.join(ROOT, "out_test.svg")
        try:
            render.draw_svg(ch, out)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("<svg", text)
            self.assertIn("紫微", text)
        finally:
            if os.path.exists(out):
                os.remove(out)


class TestInterpret(unittest.TestCase):
    def test_no_quoted_text(self):
        ch = chart("男", "庚午", 4, 21, 7)
        md = interpret.analyze(ch, liunian(ch, "丙午", 37))
        self.assertNotIn("「", md)
        self.assertIn("说明", md)


if __name__ == "__main__":
    unittest.main()
