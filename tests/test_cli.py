import os
import shutil
import sys
import unittest
import uuid

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star.cli import main


class TestCli(unittest.TestCase):
    def test_lunar_full(self):
        d = os.path.join(ROOT, "out_test_" + uuid.uuid4().hex[:8])
        os.makedirs(d, exist_ok=True)
        self.addCleanup(shutil.rmtree, d, True)
        code = main(
            [
                "--gender",
                "男",
                "--lunar-gz",
                "庚午",
                "--month",
                "4",
                "--day",
                "21",
                "--hour",
                "未",
                "--year",
                "2026",
                "--topic",
                "all",
                "--liuyue",
                "2026",
                "--out",
                d,
                "--no-render",
            ]
        )
        self.assertEqual(code, 0)
        files = os.listdir(d)
        self.assertTrue(any(f.endswith(".md") for f in files))

    def test_hepan_cli(self):
        d = os.path.join(ROOT, "out_test_" + uuid.uuid4().hex[:8])
        os.makedirs(d, exist_ok=True)
        self.addCleanup(shutil.rmtree, d, True)
        code = main(
            [
                "--gender",
                "男",
                "--lunar-gz",
                "庚午",
                "--month",
                "4",
                "--day",
                "21",
                "--hour",
                "未",
                "--year",
                "2026",
                "--hepan",
                "--gender2",
                "女",
                "--lunar-gz2",
                "戊辰",
                "--month2",
                "1",
                "--day2",
                "15",
                "--hour2",
                "巳",
                "--name",
                "A",
                "--name2",
                "B",
                "--out",
                d,
                "--no-render",
            ]
        )
        self.assertEqual(code, 0)
        self.assertTrue(any("_x_" in f for f in os.listdir(d)))


if __name__ == "__main__":
    unittest.main()
