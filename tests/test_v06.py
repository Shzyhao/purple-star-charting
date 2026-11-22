import importlib.util
import os
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, ROOT)

from purple_star import cli, html_report


class TestHtml(unittest.TestCase):
    def test_md_to_html(self):
        md = "# 标题\n\n## 小节\n\n- 项目一\n- 项目二\n\n| a | b |\n|---|---|\n| 1 | 2 |\n"
        html = html_report.md_to_html(md)
        self.assertIn("<h1>标题</h1>", html)
        self.assertIn("<h2>小节</h2>", html)
        self.assertIn("<table>", html)
        self.assertIn("<li>项目一</li>", html)

    def test_write(self):
        d = os.path.join(ROOT, "out_test_html_" + str(os.getpid()))
        os.makedirs(d, exist_ok=True)
        try:
            md = os.path.join(d, "a.md")
            with open(md, "w", encoding="utf-8") as f:
                f.write("# t\n")
            out = html_report.write_html(md, os.path.join(d, "a.html"))
            self.assertTrue(os.path.exists(out))
            with open(out, encoding="utf-8") as f:
                self.assertIn("<!DOCTYPE html>", f.read())
        finally:
            import shutil

            shutil.rmtree(d, ignore_errors=True)

    def test_cli_html(self):
        d = os.path.join(ROOT, "out_test_html_cli_" + str(os.getpid()))
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
                    "--no-render",
                    "--html",
                ]
            )
            self.assertEqual(code, 0)
            self.assertTrue(any(f.endswith(".html") for f in os.listdir(d)))
        finally:
            import shutil

            shutil.rmtree(d, ignore_errors=True)


class TestPackaging(unittest.TestCase):
    def test_pyproject(self):
        try:
            import tomllib
        except ImportError:
            self.skipTest("tomllib requires py3.11+")
        with open(os.path.join(ROOT, "pyproject.toml"), "rb") as f:
            data = tomllib.load(f)
        self.assertEqual(data["project"]["name"], "purple-star-charting")
        self.assertIn("purple-star", data["project"]["scripts"])

    def test_install_scripts(self):
        self.assertTrue(os.path.exists(os.path.join(ROOT, "scripts", "install_skill.ps1")))
        self.assertTrue(os.path.exists(os.path.join(ROOT, "scripts", "install_skill.sh")))


OPENCC = importlib.util.find_spec("opencc") is not None


class TestTraditional(unittest.TestCase):
    @unittest.skipUnless(OPENCC, "opencc not installed")
    def test_traditional_output(self):
        d = os.path.join(ROOT, "out_test_trad_" + str(os.getpid()))
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
                    "--no-render",
                    "--traditional",
                ]
            )
            self.assertEqual(code, 0)
            files = [f for f in os.listdir(d) if f.endswith(".md")]
            with open(os.path.join(d, files[0]), encoding="utf-8") as f:
                self.assertIn("命盤", f.read())
        finally:
            import shutil

            shutil.rmtree(d, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
