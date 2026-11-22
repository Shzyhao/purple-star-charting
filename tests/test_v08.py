# -*- coding: utf-8 -*-
import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import fly, fortune, liunian_stars, render, solartime, strength, timing
from purple_star.chart import chart


class TestRenderMore(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_cells(self):
        cells = render._cells(self.ch)
        self.assertEqual(len(cells), 12)
        self.assertIn("命宮", [c["palace"] for c in cells.values()])

    def test_svg_all_palaces(self):
        out = os.path.join(ROOT, "out_test_svg2.svg")
        try:
            render.draw_svg(self.ch, out)
            with open(out, encoding="utf-8") as f:
                text = f.read()
            self.assertIn("<svg", text)
            self.assertIn("命宮", text)
        finally:
            if os.path.exists(out):
                os.remove(out)

    @unittest.skipUnless(__import__("importlib").util.find_spec("PIL"), "Pillow not installed")
    def test_png(self):
        out = os.path.join(ROOT, "out_test_png.png")
        try:
            render.draw_png(self.ch, out, W=480, H=480)
            self.assertTrue(os.path.exists(out))
        finally:
            if os.path.exists(out):
                os.remove(out)

    def test_find_font(self):
        fp = render._find_font()
        self.assertTrue(fp is None or isinstance(fp, str))


class TestSolarTimeMore(unittest.TestCase):
    def test_eot_range(self):
        for md in ((1, 15), (4, 15), (7, 15), (10, 15)):
            v = solartime.equation_of_time(2020, md[0], md[1])
            self.assertGreaterEqual(v, -17.0)
            self.assertLessEqual(v, 17.0)

    def test_true_solar(self):
        h, m = solartime.true_solar(12, 0, 2020, 6, 1, 120.0)
        self.assertTrue(0 <= h < 24)
        self.assertTrue(0 <= m < 60)
        h2, m2 = solartime.true_solar(0, 10, 2020, 6, 1, 118.0)
        self.assertTrue(0 <= h2 < 24)

    def test_hour_index(self):
        cases = {(23, 59): 0, (0, 0): 0, (1, 0): 1, (2, 59): 1, (3, 0): 2, (12, 0): 6, (21, 0): 11, (22, 59): 11}
        for (h, m), idx in cases.items():
            self.assertEqual(solartime.hour_index_true(h, m), idx)


class TestLiunianStarsMore(unittest.TestCase):
    def test_layer_stars(self):
        s = liunian_stars.layer_stars("戊", "午")
        self.assertEqual(s["運昌"], "申")
        self.assertEqual(s["運曲"], "午")
        self.assertIn("運祿", s)

    def test_all_gans(self):
        for g in "甲乙丙丁戊己庚辛壬癸":
            s = liunian_stars.liunian_stars(g + "子")
            self.assertTrue(s["流昌"])
            self.assertTrue(s["流曲"])


class TestStrengthMore(unittest.TestCase):
    def test_bad_miaowang(self):
        self.assertEqual(strength.load_miaowang(os.path.join(ROOT, "no_such.json")), {})

    def test_grade_boundaries(self):
        self.assertEqual(strength.level_of(1.5), "强")
        self.assertEqual(strength.level_of(0.5), "偏强")
        self.assertEqual(strength.level_of(-0.5), "偏弱")
        self.assertEqual(strength.level_of(-1.5), "弱")

    def test_unknown_star(self):
        self.assertIsNone(strength.star_score("不存在", "子"))


class TestTimingFortuneMore(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_all_events(self):
        for ev in timing.EVENTS:
            md = timing.timing_md(self.ch, 2026, 3, ev)
            self.assertIn("择时", md)

    def test_grade(self):
        self.assertEqual(fortune.grade(2.0), "顺")
        self.assertEqual(fortune.grade(0.0), "平")
        self.assertEqual(fortune.grade(-2.0), "弱")

    def test_curve_range(self):
        md = fortune.curve_md(self.ch, 2025, 2025)
        self.assertIn("2025", md)


class TestFlyMore(unittest.TestCase):
    def test_custom_table(self):
        ch = chart("男", "庚午", 4, 21, 7)
        table = {"甲": {"祿": "廉貞", "權": "破軍", "科": "武曲", "忌": "太陽"}}
        fx = fly.feixing(ch, table)
        self.assertIn("命宮", fx)


class TestMainModule(unittest.TestCase):
    def test_help(self):
        env = dict(os.environ)
        env["PYTHONPATH"] = ROOT
        r = subprocess.run(
            [sys.executable, "-m", "purple_star", "--help"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            env=env,
            timeout=60,
        )
        self.assertEqual(r.returncode, 0)
        self.assertIn("紫微斗数", r.stdout)


if __name__ == "__main__":
    unittest.main()
