import csv
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import cli, fly, liunian_stars, solartime
from purple_star.chart import chart, liunian


class TestLiunianStars(unittest.TestCase):
    def test_positions(self):
        s = liunian_stars.liunian_stars("丙午")
        self.assertEqual(s["流祿"], "巳")  # 丙干禄存在巳
        self.assertEqual(s["流羊"], "午")
        self.assertEqual(s["流陀"], "辰")
        self.assertEqual(s["流馬"], "申")  # 寅午戌马在申
        self.assertEqual(s["流魁"], "亥")
        self.assertEqual(s["流鉞"], "酉")

    def test_place(self):
        ch = chart("男", "庚午", 4, 21, 7)
        placed, raw = liunian_stars.place(ch, "丙午")
        self.assertEqual(raw["流祿"], "巳")
        self.assertIn("流祿", placed.get("疾厄", []))


class TestFeixing(unittest.TestCase):
    def test_gans(self):
        ch = chart("男", "庚午", 4, 21, 7)
        gans = fly.palace_gans(ch)
        self.assertEqual(len(gans), 12)
        self.assertEqual(gans["命宮"], "丙")  # 庚年寅干戊，命宫戌 -> 戊+8=丙

    def test_feixing(self):
        ch = chart("男", "庚午", 4, 21, 7)
        fx = fly.feixing(ch)
        for p in fx:
            self.assertIn("gan", fx[p])
            self.assertIsInstance(fx[p]["hua"], dict)


class TestLiunianPalaces(unittest.TestCase):
    def test_twelve_palaces(self):
        ch = chart("男", "庚午", 4, 21, 7)
        ln = liunian(ch, "丙午", 37)
        self.assertEqual(len(ln["palaces"]), 12)
        self.assertEqual(ln["palaces"][0]["palace"], "命宮")
        self.assertEqual(ln["palaces"][0]["zhi"], "午")
        self.assertEqual(len(ln["stars"]), 8)
        self.assertEqual(ln["stars"]["流昌"], "申")
        self.assertEqual(ln["stars"]["流曲"], "午")


class TestSchool(unittest.TestCase):
    def test_sihua_common(self):
        a = chart("男", "庚午", 4, 21, 7)
        b = chart("男", "庚午", 4, 21, 7, school={"sihua": "common"})
        self.assertEqual(a["hua"].get("天同"), "科")
        self.assertEqual(b["hua"].get("天同"), "忌")
        self.assertEqual(b["hua"].get("太陰"), "科")

    def test_huoling_hour(self):
        a = chart("男", "庚午", 4, 21, 7)
        b = chart("男", "庚午", 4, 21, 7, school={"huoling": "hour"})
        pa = [p for p, i in a["palaces"].items() if "火星" in i["stars"]][0]
        pb = [p for p, i in b["palaces"].items() if "火星" in i["stars"]][0]
        self.assertNotEqual(pa, pb)

    def test_daxian_ming(self):
        ch = chart("男", "庚午", 4, 21, 7, school={"daxian": "ming"})
        first = [d for d in ch["daxian"].values() if d["from"] == ch["ju_number"]][0]
        z = [k for k, v in ch["daxian"].items() if v is first][0]
        self.assertEqual(z, ch["ming_zhi"])


class TestSolarTime(unittest.TestCase):
    def test_true_solar(self):
        h, m = solartime.true_solar(14, 30, 1990, 5, 15, 118.05)
        self.assertTrue(abs((h * 60 + m) - (14 * 60 + 30 - 7.8 + solartime.equation_of_time(1990, 5, 15))) < 1)
        self.assertEqual(solartime.hour_index_true(16, 43), 8)  # 申

    def test_city_db(self):
        self.assertIn("淄博", solartime.CITY_LON)
        self.assertAlmostEqual(solartime.CITY_LON["淄博"], 118.05, places=1)


class TestJsonAndBatch(unittest.TestCase):
    def test_json_payload(self):
        ch = chart("男", "庚午", 4, 21, 7)
        ln = liunian(ch, "丙午", 37)
        p = cli._json_payload(ch, ln)
        self.assertIn("palaces", p)
        self.assertEqual(p["ming"]["zhi"], "戌")
        self.assertEqual(len(p["feixing"]), 12)

    def test_batch(self):
        d = os.path.join(ROOT, "out_test_batch_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
        csv_path = os.path.join(d, "in.csv")
        try:
            with open(csv_path, "w", encoding="utf-8-sig", newline="") as f:
                w = csv.writer(f)
                w.writerow(["name", "gender", "solar", "time", "year"])
                w.writerow(["a", "男", "1990-05-15", "14:30", "2026"])
            try:
                code = cli.main(["--batch", csv_path, "--out", d, "--no-render"])
            except SystemExit:
                code = None
            self.assertIn(code, (0, None))
            self.assertTrue(os.path.exists(os.path.join(d, "batch_summary.csv")))
        finally:
            import shutil

            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
