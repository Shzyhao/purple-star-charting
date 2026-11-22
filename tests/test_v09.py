# -*- coding: utf-8 -*-
import os
import shutil
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys_path_ok = ROOT in __import__("sys").path

import sys

sys.path.insert(0, ROOT)

from purple_star import cli, fly, fortune, hepan, html_report, render, solartime, timing, topics
from purple_star.chart import chart, gz_of_year, liunian


def _outdir(name):
    d = os.path.join(ROOT, "out_test_" + name + "_" + str(os.getpid()))
    os.makedirs(d, exist_ok=True)
    return d


class TestCliMore(unittest.TestCase):
    def test_city_and_lon(self):
        d = _outdir("city")
        try:
            code = cli.main(
                [
                    "--gender",
                    "男",
                    "--solar",
                    "1990-05-15",
                    "--time",
                    "14:30",
                    "--city",
                    "淄博",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
            code = cli.main(
                [
                    "--gender",
                    "男",
                    "--solar",
                    "1990-05-15",
                    "--time",
                    "14:30",
                    "--lon",
                    "118.05",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_school_flags(self):
        d = _outdir("school")
        try:
            code = cli.main(
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
                    "--school-sihua",
                    "common",
                    "--school-huoling",
                    "hour",
                    "--school-daxian",
                    "ming",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_date_liuyue_fortune_timing(self):
        d = _outdir("flows")
        try:
            code = cli.main(
                [
                    "--gender",
                    "男",
                    "--solar",
                    "1990-05-15",
                    "--time",
                    "14:30",
                    "--date",
                    "2026-12-06",
                    "--liuyue",
                    "2026",
                    "--fortune",
                    "2024-2026",
                    "--timing",
                    "travel",
                    "--year",
                    "2026",
                    "--lunar-month",
                    "5",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_json_out(self):
        d = _outdir("json")
        try:
            jp = os.path.join(d, "a.json")
            code = cli.main(
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
                    "--out",
                    d,
                    "--no-render",
                    "--json-out",
                    jp,
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(jp))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_batch_invalid_row(self):
        d = _outdir("batchbad")
        try:
            csv_path = os.path.join(d, "in.csv")
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                f.write("name,gender,solar,time,year\n")
                f.write("bad,男,not-a-date,14:30,2026\n")
                f.write("ok,女,1988-03-02,09:00,2026\n")
            code = cli.main(["--batch", csv_path, "--out", d, "--no-render"])
            self.assertEqual(code, 0)
            self.assertTrue(os.path.exists(os.path.join(d, "batch_summary.csv")))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_errors(self):
        with self.assertRaises(SystemExit):
            cli.main(["--solar", "1990-05-15"])
        with self.assertRaises(SystemExit):
            cli.main(
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
                    "--fortune",
                    "bad",
                    "--out",
                    _outdir("e1"),
                    "--no-render",
                ]
            )
        with self.assertRaises(SystemExit):
            cli.main(
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
                    "--topic",
                    "nope",
                    "--out",
                    _outdir("e2"),
                    "--no-render",
                ]
            )


class TestChartBranches(unittest.TestCase):
    def test_bad_ganzhi(self):
        with self.assertRaises((ValueError, TypeError)):
            gz_of_year("x")

    def test_notation_notes(self):
        ch = chart("男", "庚午", 4, 21, 7, leap_month=True, late_zi="next")
        self.assertTrue(ch["notes"])

    def test_wood_ju_day9(self):
        ch = chart("男", "甲子", 2, 9, 0)
        self.assertIn("ziwei", ch)


class TestHepanBranches(unittest.TestCase):
    def test_no_daxian_age(self):
        a = chart("男", "庚午", 4, 21, 7)
        b = chart("女", "戊辰", 1, 15, 5)
        s = hepan.daxian_sync(a, b, 2030)
        self.assertIn("same", s)

    def test_windows(self):
        a = chart("男", "庚午", 4, 21, 7)
        b = chart("女", "辛未", 12, 13, 9)
        rows = hepan.marriage_windows(a, b, 2026, 3)
        self.assertEqual(len(rows), 3)


class TestFortuneBranches(unittest.TestCase):
    def test_out_of_range(self):
        ch = chart("男", "庚午", 4, 21, 7)
        self.assertIsNone(fortune.daxian_score(ch, 200))

    def test_curve(self):
        ch = chart("男", "庚午", 4, 21, 7)
        md = fortune.curve_md(ch, 2026, 2026)
        self.assertIn("2026", md)


class TestSolarBranches(unittest.TestCase):
    def test_wrap(self):
        h, m = solartime.true_solar(23, 55, 2020, 6, 1, 130.0)
        self.assertTrue(0 <= h < 24)
        h, m = solartime.true_solar(0, 5, 2020, 6, 1, 100.0)
        self.assertTrue(0 <= h < 24)


class TestTimingBranches(unittest.TestCase):
    def test_hua_branch(self):
        ch = chart("男", "庚午", 4, 21, 7)
        for day in (1, 5, 10, 15, 20, 25):
            r = timing.score_day(ch, 2026, 4, day, "contract")
            self.assertIn("score", r)


class TestTopicsBranches(unittest.TestCase):
    def test_topics_with_liunian(self):
        ch = chart("男", "庚午", 4, 21, 7)
        ln = liunian(ch, "丙午", 37)
        for name in topics.TOPICS:
            md = topics.analyze_topic(name, ch, ln)
            self.assertGreater(len(md), 30)


class TestHtmlBranches(unittest.TestCase):
    def test_md_variants(self):
        md = "# H\n\n## S\n\n### T\n\n- a\n- b\n\n---\n\nparagraph\n\n| x |\n|---|\n| 1 |\n"
        html = html_report.md_to_html(md)
        self.assertIn("<h3>T</h3>", html)
        self.assertIn("<hr>", html)
        self.assertIn("<table>", html)


class TestRenderBranch(unittest.TestCase):
    def test_find_font_cached(self):
        a = render._find_font()
        b = render._find_font()
        self.assertEqual(a, b)


class TestFlyBranch(unittest.TestCase):
    def test_default_table(self):
        ch = chart("男", "庚午", 4, 21, 7)
        fx = fly.feixing(ch)
        self.assertEqual(len(fx), 12)


if __name__ == "__main__":
    unittest.main()
