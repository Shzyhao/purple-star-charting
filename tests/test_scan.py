import os
import subprocess
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


class TestCopyrightScan(unittest.TestCase):
    def test_repo_clean(self):
        script = os.path.join(ROOT, "scripts", "copyright_scan.py")
        r = subprocess.run(
            [sys.executable, script, ROOT], capture_output=True, text=True, encoding="utf-8", errors="replace"
        )
        self.assertEqual(r.returncode, 0, "copyright scan failed:\n" + r.stdout + r.stderr)


if __name__ == "__main__":
    unittest.main()
