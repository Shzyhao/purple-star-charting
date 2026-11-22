import json
import os
import sys
import tempfile
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import strength
from purple_star.chart import chart


class TestStrength(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_relation_and_score(self):
        self.assertEqual(strength.relation("火", "火"), "比和")
        self.assertEqual(strength.relation("火", "水"), "宮克星")
        self.assertEqual(strength.star_score("太陽", "午"), 1.0)
        self.assertEqual(strength.star_score("太陽", "子"), -2.0)
        self.assertEqual(strength.star_score("紫微", "辰"), 1.0)

    def test_level(self):
        self.assertEqual(strength.level_of(2.0), "强")
        self.assertEqual(strength.level_of(0.0), "平")
        self.assertEqual(strength.level_of(-2.0), "弱")

    def test_palace_strength(self):
        ps = strength.palace_strength(self.ch, "命宮")
        self.assertEqual(ps["zhi"], "戌")
        self.assertEqual(ps["avg"], -0.5)
        self.assertEqual(ps["level"], "偏弱")

    def test_sanfang(self):
        sf = strength.sanfang(self.ch)
        self.assertAlmostEqual(sf["avg"], -0.12, places=2)
        self.assertIn("地空", sf["sha"])
        self.assertIn("地劫", sf["sha"])

    def test_empty_palace(self):
        ps = strength.palace_strength(self.ch, "奴僕")
        self.assertIsNone(ps["avg"])

    def test_miaowang_loader(self):
        data = {"紫微": {"戌": "旺"}, "天相": {"戌": "得地"}}
        with tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, dir=ROOT, encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False)
            tmp = f.name
        try:
            table = strength.load_miaowang(tmp)
            self.assertEqual(strength.miaowang_grade(table, "紫微", "戌"), "旺")
            self.assertEqual(strength.miaowang_grade(table, "天相", "戌"), "得地")
            self.assertIsNone(strength.miaowang_grade(table, "紫微", "子"))
        finally:
            os.unlink(tmp)

    def test_analyze_with_miaowang(self):
        from purple_star import interpret

        table = {"紫微": {"戌": "旺"}}
        md = interpret.analyze(self.ch, None, miaowang=table)
        self.assertIn("强弱与三方四正", md)
        self.assertIn("庙旺（自备表）", md)


if __name__ == "__main__":
    unittest.main()
