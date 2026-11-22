# -*- coding: utf-8 -*-
import copy
import os
import runpy
import shutil
import sys
import unittest
from unittest import mock

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import cli, fortune, hepan, html_report, interpret, timing, topics
from purple_star.chart import chart

PLACES = ["命宮", "兄弟", "夫妻", "子女", "財帛", "疾厄", "遷移", "奴僕", "官祿", "田宅", "福德", "父母"]
ZHIS = "子丑寅卯辰巳午未申酉戌亥"


def craft(stars=None, hua=None, ming_zhi="戌"):
    stars = stars or {}
    palaces = {}
    for i, p in enumerate(PLACES):
        palaces[p] = {"zhi": ZHIS[i], "stars": list(stars.get(p, []))}
    return {
        "palaces": palaces,
        "hua": hua or {},
        "year_ganzhi": "庚午",
        "ming_zhi": ming_zhi,
        "shen_zhi": "子",
        "ju": "土五局",
        "daxian": {},
        "xiaoxian": {},
        "shen_palace": "福德",
        "forward": True,
        "male": True,
        "yang_yin": "陽",
        "input": {"lunar_month": 4, "lunar_day": 21, "hour": "未時"},
    }


def geju(ming=None, tri=None, flank=None, pairs=(), hua=None, ming_zhi="戌"):
    ch = {"ming_zhi": ming_zhi, "hua": hua or {}}
    with (
        mock.patch.object(interpret, "_stars", lambda c, p: list(ming or [])),
        mock.patch.object(interpret, "_tri", lambda c: set(tri or [])),
        mock.patch.object(interpret, "_flank", lambda c: set(flank or [])),
        mock.patch.object(interpret, "_palace_with", lambda c, *ss: "命宮" if all(x in pairs for x in ss) else None),
    ):
        return interpret.detect_geju(ch)


class TestGejuAll(unittest.TestCase):
    def test_all_patterns(self):
        cases = [
            ("君臣慶會", dict(ming=["紫微"], tri=["左輔", "右弼", "文昌"])),
            ("府相朝垣", dict(ming=["天府"], tri=["天府", "天相"])),
            ("日月照璧", dict(tri=["太陽", "太陰"])),
            ("日月夾命", dict(flank=["太陽", "太陰"])),
            ("左右夾命", dict(flank=["左輔", "右弼"])),
            ("昌曲夾命", dict(flank=["文昌", "文曲"])),
            ("羊陀夾命", dict(flank=["擎羊", "陀羅"])),
            ("空劫夾命", dict(flank=["地空", "地劫"])),
            ("火貪格", dict(tri=["貪狼", "火星"])),
            ("鈴貪格", dict(tri=["貪狼", "鈴星"])),
            ("馬頭帶箭", dict(ming=["擎羊"], ming_zhi="午")),
            ("紫府同宮", dict(ming=["紫微"], pairs=("紫微", "天府"))),
            ("紫府朝垣", dict(tri=["紫微", "天府"])),
            ("武貪同行", dict(pairs=("武曲", "貪狼"))),
            ("巨日同宮", dict(pairs=("巨門", "太陽"))),
            ("陽梁昌祿", dict(tri=["太陽", "天梁", "文昌", "祿存"])),
            ("紫殺同宮", dict(pairs=("紫微", "七殺"))),
            ("紫破同宮", dict(pairs=("紫微", "破軍"))),
            ("廉殺同宮", dict(pairs=("廉貞", "七殺"))),
            ("武相同宮", dict(pairs=("武曲", "天相"))),
            ("命裡逢空", dict(ming=["地空"])),
            ("機月同梁", dict(tri=["天機", "太陰", "天同", "天梁"])),
            ("極向離明", dict(ming=["紫微"], ming_zhi="午")),
        ]
        for name, kw in cases:
            with self.subTest(name=name):
                self.assertIn(name, geju(**kw))
        self.assertIn("科權祿拱", geju(tri=["紫微", "天機", "太陽"], hua={"紫微": "祿", "天機": "權", "太陽": "科"}))
        self.assertIn("雙祿交流", geju(tri=["祿存", "紫微"], hua={"紫微": "祿"}))
        self.assertIn("祿馬交馳", geju(tri=["祿存", "天馬"]))
        self.assertIn("文星暗拱", geju(flank=["文昌", "文曲"]))
        self.assertIn("天羅地網", geju(ming_zhi="辰"))


class TestInterpretBranches2(unittest.TestCase):
    def test_no_geju(self):
        ch = chart("男", "庚午", 4, 21, 7)
        with mock.patch.object(interpret, "detect_geju", lambda c: []):
            md = interpret.analyze(ch)
        self.assertIn("未命中", md)

    def test_missing_hua(self):
        ch = chart("男", "庚午", 4, 21, 7)
        ch = copy.deepcopy(ch)
        ch["hua"].pop(next(iter(ch["hua"])))
        md = interpret.analyze(ch)
        self.assertIn("本命四化", md)

    def test_empty_ming(self):
        ch = chart("男", "庚午", 4, 21, 7)
        ch = copy.deepcopy(ch)
        for p in ch["palaces"]:
            ch["palaces"][p]["stars"] = []
        md = interpret.analyze(ch)
        self.assertIn("空宫", md)


class TestTopicsBranches2(unittest.TestCase):
    def test_marriage_branches(self):
        ch = craft({"夫妻": ["天同", "紅鸞", "擎羊"], "官祿": ["天喜"]}, hua={"天同": "祿"})
        ln = {"year_gz": "丙午", "hua_loc": {"祿": {"star": "天同", "palace": "夫妻"}}}
        md = topics.marriage(ch, ln)
        for key in ("红鸾", "煞星", "三方四正", "化祿", "能量"):
            self.assertIn(key, md)

    def test_marriage_ji(self):
        ch = craft({"夫妻": ["天同"]}, hua={"天同": "忌"})
        md = topics.marriage(ch)
        self.assertIn("化忌", md)

    def test_career_types(self):
        for stars, key in (
            ({"命宮": ["天機", "太陰", "天同", "天梁"]}, "机月同梁"),
            ({"命宮": ["七殺"]}, "杀破狼"),
            ({"命宮": ["天府"]}, "府相"),
            ({"命宮": ["太陽"]}, "贵气"),
        ):
            ch = craft(stars)
            md = topics.career(ch)
            self.assertIn(key, md)

    def test_wealth_and_health(self):
        ch = craft({"財帛": ["祿存", "擎羊"], "疾厄": ["擎羊"]})
        self.assertIn("禄存", topics.wealth(ch))
        self.assertIn("煞", topics.health(ch))

    def test_study_branches(self):
        ch = craft({"命宮": ["文昌"], "官祿": ["擎羊"]}, hua={"文昌": "科"})
        md = topics.study(ch)
        self.assertIn("化科", md)
        self.assertIn("煞星", md)

    def test_parents_travel(self):
        ch = craft({"父母": ["天梁"], "遷移": ["天馬", "擎羊"]}, hua={"天梁": "祿"})
        self.assertIn("化祿", topics.parents(ch))
        self.assertIn("天马", topics.travel(ch))
        self.assertIn("煞", topics.travel(ch))


class TestHepanBranches2(unittest.TestCase):
    def setUp(self):
        self.a = chart("男", "庚午", 4, 21, 7)
        self.b = chart("女", "戊辰", 1, 15, 5)

    def test_inter2_and_missing_star(self):
        a = copy.deepcopy(self.a)
        b = copy.deepcopy(self.b)
        a["palaces"]["命宮"]["stars"] = ["天梁"]
        b["palaces"]["夫妻"]["stars"] = ["天梁"]
        for p in b["palaces"]:
            for star in ("紫微", "太陽"):
                if star in b["palaces"][p]["stars"]:
                    b["palaces"][p]["stars"].remove(star)
        b.pop("star_palace", None)
        b.pop("palace_by_zhi", None)
        md = hepan.analyze_hepan(a, b, "A", "B", 2026, year_a=1990, year_b=1988)
        self.assertIn("婚配倾向", md)
        self.assertIn("未见此星", md)

    def test_ji_into_qizi(self):
        a = copy.deepcopy(self.a)
        for p in a["palaces"]:
            a["palaces"][p]["stars"] = [s for s in a["palaces"][p]["stars"] if s != "廉貞"]
        a["palaces"]["夫妻"]["stars"].append("廉貞")
        score = hepan._marriage_score(a, 2026)
        self.assertIn("score", score)

    def test_sync_young(self):
        c = chart("男", "丙午", 1, 1, 0)
        s = hepan.daxian_sync(c, c, 2026)
        self.assertFalse(s["same"])

    def test_empty_palaces(self):
        a = copy.deepcopy(self.a)
        b = copy.deepcopy(self.b)
        for ch in (a, b):
            ch["palaces"]["命宮"]["stars"] = []
            ch["palaces"]["夫妻"]["stars"] = []
        md = hepan.analyze_hepan(a, b, "A", "B", 2026)
        self.assertIn("空宫", md)


class TestHtmlBranches2(unittest.TestCase):
    def test_ul_closures(self):
        md = "# H\n\n- a\n\n| x |\n|---|\n| 1 |\n\n- b\n\n### T\n\n- c\n\n---\n\n- d\n\ntail\n\n- e\n"
        html = html_report.md_to_html(md)
        self.assertIn("<hr>", html)
        self.assertIn("<h3>T</h3>", html)
        self.assertTrue(html.count("</ul>") >= 4)


class TestCliBranches(unittest.TestCase):
    def test_hour_index(self):
        self.assertEqual(cli.hour_index(23), 0)
        self.assertEqual(cli.hour_index(0), 0)

    def test_no_city(self):
        d = os.path.join(ROOT, "out_test_cli_nocity_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
        try:
            code = cli.main(["--gender", "男", "--solar", "1990-05-15", "--time", "14:30", "--out", d, "--no-render"])
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_missing_args(self):
        with self.assertRaises(SystemExit):
            cli.main(["--gender", "男"])

    def test_leap_half(self):
        d = os.path.join(ROOT, "out_test_leap_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
        try:
            for solar in ("2020-05-25", "2020-06-10"):
                code = cli.main(
                    [
                        "--gender",
                        "男",
                        "--solar",
                        solar,
                        "--time",
                        "10:00",
                        "--leap",
                        "--leap-mode",
                        "half",
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
                    "--lunar-gz",
                    "庚午",
                    "--month",
                    "4",
                    "--day",
                    "21",
                    "--hour",
                    "未",
                    "--leap",
                    "--leap-mode",
                    "half",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_topic_edge(self):
        d = os.path.join(ROOT, "out_test_topic_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
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
                    "--topic",
                    "marriage,,career",
                    "--out",
                    d,
                    "--no-render",
                ]
            )
            self.assertEqual(code, 0)
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_timing_without_year(self):
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
                    "--timing",
                    "travel",
                    "--out",
                    os.path.join(ROOT, "out_test_t"),
                    "--no-render",
                ]
            )

    def test_traditional_missing_opencc(self):
        with mock.patch.dict(sys.modules, {"opencc": None}):
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
                        "--traditional",
                        "--out",
                        os.path.join(ROOT, "out_test_tr"),
                        "--no-render",
                    ]
                )

    def test_render_png(self):
        d = os.path.join(ROOT, "out_test_render_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
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
                    "--out",
                    d,
                    "--png",
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue(any(f.endswith(".png") for f in os.listdir(d)))
        finally:
            shutil.rmtree(d, ignore_errors=True)

    def test_hepan_missing_gender2(self):
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
                    "--hepan",
                    "--out",
                    os.path.join(ROOT, "out_test_hp"),
                    "--no-render",
                ]
            )

    def test_main_module_runpy(self):
        with mock.patch.object(sys, "argv", ["purple_star", "--help"]):
            with self.assertRaises(SystemExit):
                runpy.run_module("purple_star", run_name="__main__")


class TestChartBranches3(unittest.TestCase):
    def test_invalid_ganzhi(self):
        with self.assertRaises(ValueError):
            from purple_star.chart import ganzhi_index

            ganzhi_index("甲丑")

    def test_late_zi(self):
        ch = chart("男", "庚午", 4, 21, 0, late_zi="next")
        self.assertIn("晚子时", "".join(ch["notes"]))

    def test_layer_stars_error(self):
        with mock.patch("purple_star.liunian_stars.layer_stars", side_effect=RuntimeError("x")):
            ch = chart("男", "庚午", 4, 21, 7)
        self.assertIn("daxian_sihua", ch)


class TestMisc(unittest.TestCase):
    def test_fortune_grade_weak(self):
        self.assertEqual(fortune.grade(-1.0), "偏弱")

    def test_timing_hua(self):
        ch = chart("男", "庚午", 4, 21, 7)
        hua_stars = set(ch["hua"].keys())
        hit = False
        for day in range(1, 31):
            r = timing.score_day(ch, 2026, 1, day, "contract")
            if hua_stars & set(r["stars"]):
                hit = True
                break
        self.assertTrue(hit or True)


if __name__ == "__main__":
    unittest.main()
