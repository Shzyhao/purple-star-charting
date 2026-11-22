import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import topics
from purple_star.chart import chart, liunian


class TestTopics(unittest.TestCase):
    def setUp(self):
        self.ch = chart("男", "庚午", 4, 21, 7)
        self.ln = liunian(self.ch, "丙午", 37)

    def test_all_topics(self):
        for name in ("marriage", "career", "wealth", "health"):
            md = topics.analyze_topic(name, self.ch, self.ln)
            self.assertGreater(len(md), 50)
            self.assertNotIn("「", md)
            self.assertIn("不构成", md)

    def test_health_disclaimer(self):
        md = topics.analyze_topic("health", self.ch)
        self.assertIn("非医学", md)

    def test_unknown_topic(self):
        with self.assertRaises(ValueError):
            topics.analyze_topic("fortune", self.ch)


if __name__ == "__main__":
    unittest.main()
