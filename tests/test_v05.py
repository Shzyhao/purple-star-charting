import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import fortune, hepan, timing, topics
from purple_star.chart import chart


class TestNewTopics(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_all_new_topics(self):
        for name in ("study", "children", "parents", "travel", "partnership", "legal"):
            md = topics.analyze_topic(name, self.ch)
            self.assertGreater(len(md), 50)
            self.assertNotIn("「", md)
            self.assertIn("不构成", md)


class TestTiming(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_events_defined(self):
        for k in ("contract", "interview", "travel", "date", "medical", "opening"):
            self.assertIn(k, timing.EVENTS)

    def test_score_day(self):
        r = timing.score_day(self.ch, 2026, 5, 8, "contract")
        self.assertIn("score", r)
        self.assertIn("palace", r)

    def test_md(self):
        md = timing.timing_md(self.ch, 2026, 5, "contract")
        self.assertIn("择时", md)
        self.assertIn("不构成", md)


class TestFortune(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)

    def test_scores(self):
        dx = fortune.daxian_score(self.ch, 37)
        ln = fortune.liunian_score(self.ch, 2026)
        self.assertIn("score", dx)
        self.assertIn("score", ln)
        self.assertIn(fortune.grade(0.0), ("平", "偏顺", "偏弱", "顺", "弱"))

    def test_curve(self):
        md = fortune.curve_md(self.ch, 2024, 2030)
        self.assertIn("运势曲线", md)
        self.assertEqual(md.count("| 20"), 7)


class TestHepanV05(unittest.TestCase):
    def setUp(self):
        self.a = chart("男", "庚午", 4, 21, 7)
        self.b = chart("女", "戊辰", 1, 15, 5)

    def test_windows(self):
        rows = hepan.marriage_windows(self.a, self.b, 2026, 6)
        self.assertEqual(len(rows), 6)
        self.assertIn("both", rows[0])

    def test_sync(self):
        s = hepan.daxian_sync(self.a, self.b, 2026)
        self.assertIn("same", s)

    def test_sections(self):
        md = hepan.analyze_hepan(self.a, self.b, "A", "B", 2026, year_a=1990, year_b=1988)
        self.assertIn("姻缘窗口交集", md)
        self.assertIn("大限同步度", md)


if __name__ == "__main__":
    unittest.main()
